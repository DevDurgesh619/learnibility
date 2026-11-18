"""IB DP Psychology (SL/HL, NEW guide, first assessment May 2027) - ib-g12-psychology.

Year 2 of the course: the human relationships and learning and cognition contexts, class practicals 3
(survey) and 4 (interview), the HL extensions (culture, motivation, technology), inferential statistics
and Paper 3 source skills, and the IA research proposal. Shared machinery (Kit, research-methods
generators, markbands, Paper 2/3 material from year 1) is imported from ib_g11_psychology.

Mock = one examination set mirroring targets.json examPattern (HL), with fixed marks per section:
  Paper 1 (35): 2 short answers x 4, 2 applied short answers x 6, extended response (two options shown,
                answer one) x 15 each.
  Paper 2 (35): 4 practical-based questions x 5 + evaluation of an unseen study 15.
  Paper 3 (30): 4 source-based questions 3 + 6 + 6 + 15, all on one source set per mock.
Inferential-statistics items COMPUTE their answers (Mann-Whitney U, Wilcoxon T, Spearman's rho) and
compare them with published two-tailed critical values at p = 0.05.
"""
from __future__ import annotations

import statistics

from _common import F, mcq, name, two_names, CITIES  # noqa: F401
import ib_g11_psychology as g11
from ib_g11_psychology import Kit, methods, scenarios, cap, lc  # noqa: F401

CONFIG = dict(g11.CONFIG)

# --------------------------------------------------------------------------------------------
# Inferential statistics generators (computed)
# --------------------------------------------------------------------------------------------
MWU_CRIT = {5: 2, 6: 5, 7: 8, 8: 13, 9: 17, 10: 23}          # n1 = n2, two-tailed p = 0.05
WILC_CRIT = {6: 0, 7: 2, 8: 3, 9: 5, 10: 8, 11: 10, 12: 13}   # two-tailed p = 0.05
MWU_CTX = [
    ('number of words recalled', 'students who used retrieval practice', 'students who re-read their notes'),
    ('score on a 20-item comprehension quiz', 'students who took handwritten notes', 'students who typed notes on a laptop'),
    ('number of times a confederate was helped', 'participants tested alone', 'participants tested in a group of four'),
    ('rating of liking for a stranger (1-20)', 'participants told the stranger shared their attitudes', 'participants told the stranger had different attitudes'),
    ('number of anagrams solved', 'participants offered no reward', 'participants offered a cash reward'),
    ('score on a sustained-attention task', 'students who left their phones outside the room', 'students who kept their phones on the desk'),
    ('self-rated intrinsic interest (1-20)', 'children praised for effort', 'children praised for intelligence'),
    ('number of prosocial acts in a game', 'children who watched a prosocial video', 'children who watched a neutral video'),
]
WILC_CTX = [
    ('loneliness score before and after a six-week befriending programme', 'before', 'after'),
    ('anxiety rating before and after a mindfulness session', 'before', 'after'),
    ('number of words recalled after massed and after spaced practice', 'massed', 'spaced'),
    ('reaction time (ms) with and without a smartphone notification sound', 'without', 'with'),
    ('prejudice score before and after a jigsaw classroom unit', 'before', 'after'),
    ('minutes of homework completed before and after a token reward scheme', 'before', 'after'),
    ('self-efficacy score before and after watching a peer model', 'before', 'after'),
]


def _rank_all(vals):
    s = sorted(vals)
    return {v: s.index(v) + 1 for v in vals}


def mann_whitney(rng, slot):
    n = rng.choice([5, 6] if slot.d <= 4 else [7, 8])
    dv, ga, gb = rng.choice(MWU_CTX)
    vals = rng.sample(range(3, 60), 2 * n)
    if rng.random() < 0.6:   # make one group tend to be higher
        vals.sort()
        k = rng.randint(n // 2, n)
        hi_, lo_ = vals[k: k + n], vals[:k] + vals[k + n:]
        A, B = (hi_, lo_) if rng.random() < 0.5 else (lo_, hi_)
    else:
        A, B = vals[:n], vals[n:]
    rng.shuffle(A)
    rng.shuffle(B)
    rk = _rank_all(A + B)
    RA = sum(rk[v] for v in A)
    RB = sum(rk[v] for v in B)
    UA = n * n + n * (n + 1) // 2 - RA
    UB = n * n - UA
    U = min(UA, UB)
    crit = MWU_CRIT[n]
    sig = U <= crit
    who = name(rng)
    stem = (f'{who} compared the {dv} of {ga} (group A) and {gb} (group B), n = {n} in each group.\n'
            f'Group A: {", ".join(map(str, A))}\nGroup B: {", ".join(map(str, B))}\n\n'
            f'Calculate the Mann-Whitney U statistic, using U = n1n2 + n1(n1 + 1)/2 - R1 for each group and taking the smaller value. '
            f'The critical value of U for n1 = n2 = {n} at p = 0.05 (two-tailed) is {crit}; U must be equal to or less than this value to be significant. '
            'State your conclusion.')
    return dict(stem=stem, answer=f'RA = {RA}, RB = {RB}; UA = {UA}, UB = {UB}; U = {U}; {"significant" if sig else "not significant"} at p = 0.05.',
                type='numerical', marks=6 if slot.d >= 5 else 5, gap='G3',
                markingKey=f'M1 rank all {2 * n} scores together (lowest = 1). A1 rank sums RA = {RA}, RB = {RB} (check: RA + RB = {RA + RB} = {2 * n}({2 * n + 1})/2). '
                f'M1 UA = {n * n} + {n * (n + 1) // 2} - {RA} = {UA}; UB = {n * n} - {UA} = {UB}. A1 U = {U}. '
                f'R1 U = {U} {"≤" if sig else ">"} {crit}, so the difference is {"significant - reject" if sig else "not significant - retain"} the null hypothesis '
                f'(p {"<" if sig else ">"} 0.05).' + (' R1 interpretation in context: the higher-ranked group scored higher on ' + dv + '.' if sig else ''))


def wilcoxon(rng, slot):
    n = rng.choice([6, 7, 8] if slot.d <= 4 else [9, 10])
    dv, c1, c2 = rng.choice(WILC_CTX)
    mags = rng.sample(range(1, 16), n)
    bias = rng.choice([0.85, 0.7, 0.5])
    signs = [1 if rng.random() < bias else -1 for _ in range(n)]
    d = [m * s for m, s in zip(mags, signs)]
    before = [rng.randint(18, 40) for _ in range(n)]
    after = [b + x for b, x in zip(before, d)]
    order = sorted(mags)
    rk = {m: order.index(m) + 1 for m in mags}
    pos = sum(rk[abs(x)] for x in d if x > 0)
    neg = sum(rk[abs(x)] for x in d if x < 0)
    T = min(pos, neg)
    crit = WILC_CRIT[n]
    sig = T <= crit
    rows = '\n'.join(f'P{i + 1}: {b} | {a}' for i, (b, a) in enumerate(zip(before, after)))
    stem = (f'A repeated measures study in {rng.choice(CITIES)} measured {dv} for {n} participants.\nParticipant: {c1} | {c2}\n{rows}\n\n'
            f'Calculate the Wilcoxon signed-rank statistic T (rank the absolute differences, then take the smaller of the sums of positive '
            f'and negative ranks). The critical value of T for n = {n} at p = 0.05 (two-tailed) is {crit}; T must be equal to or less than this to be significant. '
            'State whether the difference is significant.')
    return dict(stem=stem, answer=f'Differences ({c2} - {c1}): {d}; sum of positive ranks = {pos}, sum of negative ranks = {neg}; T = {T}; '
                f'{"significant" if sig else "not significant"} at p = 0.05.', type='numerical', marks=6 if slot.d >= 5 else 5, gap='G3',
                markingKey=f'M1 differences {c2} - {c1}: {d}. M1 rank absolute differences (smallest = 1). A1 positive ranks = {pos}, '
                f'negative ranks = {neg} (total {pos + neg} = {n}({n + 1})/2). A1 T = {T}. R1 T {"≤" if sig else ">"} {crit}: '
                f'{"significant - reject" if sig else "not significant - retain"} the null hypothesis.')


TEST_SCEN = [
    ('Two different groups of students are compared on a 1-10 rating of motivation.', 'Mann-Whitney U test', 'independent samples (different participants) and a test of difference on ordinal data'),
    ('The same participants recall words after spaced and after massed practice.', 'Wilcoxon signed-rank test', 'repeated measures and a test of difference with ordinal or non-normal data'),
    ('A researcher measures hours of sleep and exam scores for 25 students to see whether they are related.', 'Spearman\'s rank correlation coefficient', 'a test of relationship (correlation) between two co-variables measured on at least ordinal data'),
    ('Pairs of students matched on GPA are assigned to laptop or longhand note-taking and their quiz scores compared.', 'Wilcoxon signed-rank test', 'matched pairs are treated like repeated measures (related data) for a test of difference'),
    ('Adolescents and adults are compared on the number of risky choices in a driving game.', 'Mann-Whitney U test', 'two independent groups compared for a difference'),
    ('A study tests whether time spent on social media is associated with self-esteem scores in 40 adolescents.', 'Spearman\'s rank correlation coefficient', 'two co-variables; test of association'),
    ('The same participants rate their anxiety before and after a relaxation programme.', 'Wilcoxon signed-rank test', 'repeated measures, test of difference'),
    ('Children who watched a prosocial cartoon are compared with different children who watched a neutral cartoon on number of helping acts.', 'Mann-Whitney U test', 'independent samples, test of difference'),
]
TESTS = ['Mann-Whitney U test', 'Wilcoxon signed-rank test', 'Spearman\'s rank correlation coefficient', 'Chi-squared test']


def choose_test(rng, slot):
    sc, test, why = rng.choice(TEST_SCEN)
    if slot.c == 'C1' or rng.random() < 0.5:
        return mcq(rng, f'{sc} Which inferential test is most appropriate?', test, [t for t in TESTS if t != test], f'{test}: {why}.')
    return dict(stem=f'{sc} Identify the most appropriate inferential test and justify your choice.', answer=f'{test} - {why}.',
                type='short', marks=3, markingKey=f'1 mark: {test}. 2 marks: justification - {why}. (Chi-squared would be used only for nominal frequency data.)')


def p_decision(rng, slot):
    p = rng.choice([0.001, 0.008, 0.02, 0.04, 0.049, 0.051, 0.07, 0.12, 0.3])
    alpha = rng.choice([0.05, 0.05, 0.01])
    tail = rng.choice(['one-tailed', 'two-tailed'])
    ctx = rng.choice(['the effect of spaced practice on recall', 'the difference in helping between alone and group conditions',
                      'the relationship between screen time and sleep quality', 'the effect of extrinsic rewards on intrinsic motivation',
                      'the difference in prejudice scores after a contact programme'])
    sig = p <= alpha
    err = ('a Type I error (rejecting a true null hypothesis - a false positive)' if sig else
           'a Type II error (retaining a false null hypothesis - a false negative)')
    stem = (f'A {tail} test of {ctx} gives p = {p}. The researcher set the significance level at p ≤ {alpha}. '
            'State whether the result is significant, what the researcher should conclude about the null hypothesis, and which type of error she risks.')
    return dict(stem=stem, answer=f'{"Significant" if sig else "Not significant"} (p = {p} {"≤" if sig else ">"} {alpha}); '
                f'{"reject" if sig else "retain (fail to reject)"} the null hypothesis; risk of {err}.', type='short', marks=3,
                markingKey=f'1 mark: {"significant" if sig else "not significant"} because p {"≤" if sig else ">"} {alpha}. 1 mark: '
                f'{"reject" if sig else "retain"} H0. 1 mark: {err}.' + (' Note: p = 0.049 is significant at 0.05 but would not be at 0.01.' if p == 0.049 else ''))


LIKERT_ITEMS = [
    ('I enjoy learning new things in school.', False), ('I often feel bored in lessons.', True),
    ('I keep trying when work is difficult.', False), ('I give up easily on hard problems.', True),
    ('I feel I belong in my class.', False), ('I feel left out by my classmates.', True),
    ('I use my phone to relax after studying.', False), ('I find it hard to stop scrolling at night.', True),
]


def likert(rng, slot):
    k = rng.choice([4, 5, 6])
    items = rng.sample(LIKERT_ITEMS, k)
    if not any(r for _, r in items) or all(r for _, r in items):
        return None
    resp = [rng.randint(1, 5) for _ in items]
    scored = [6 - r if rev else r for (_, rev), r in zip(items, resp)]
    total = sum(scored)
    who = name(rng)
    lines = '\n'.join(f'{i + 1}. "{t}" - response: {r}' for i, ((t, _), r) in enumerate(zip(items, resp)))
    rev_ids = [str(i + 1) for i, (_, rev) in enumerate(items) if rev]
    stem = (f'{who} completed a questionnaire on attitudes to learning using a 5-point Likert scale (1 = strongly disagree, 5 = strongly agree). '
            f'Items {", ".join(rev_ids)} are reverse-scored.\n{lines}\n\nCalculate {who}\'s total score (higher = more positive attitude) and explain why some items are reverse-scored.')
    return dict(stem=stem, answer=f'Scored values: {scored}; total = {total} (out of {5 * k}). Reverse-scored items reduce acquiescence bias and check that participants read each item.',
                type='numerical', marks=3, gap='G3',
                markingKey=f'M1 reverse items {", ".join(rev_ids)} scored as 6 - response. A1 total = {" + ".join(map(str, scored))} = {total}. '
                'R1 reverse-scoring controls acquiescence (yes-saying) and response sets.')


def response_rate(rng, slot):
    sent = rng.choice([200, 250, 300, 400, 500, 600, 800])
    back = rng.randint(sent // 8, sent // 2)
    pct = 100 * back / sent
    who = rng.choice(['A school counsellor in Geneva', 'A researcher in Seoul', 'A student group in Nairobi', 'A university team in Lima'])
    topic = rng.choice(['sleep habits', 'experiences of cyberbullying', 'study strategies', 'attitudes to mental health services', 'screen use'])
    stem = (f'{who} emailed an online questionnaire about {topic} to {sent} students; {back} completed it. Calculate the response rate '
            'and explain one way in which a low response rate could bias the findings.')
    return dict(stem=stem, answer=f'Response rate = {back}/{sent} x 100 = {pct:.1f}%. Non-response bias: those who reply may differ systematically (e.g. more interested in or affected by {topic}).',
                type='numerical', marks=3, markingKey=f'A1 {back}/{sent} x 100 = {pct:.1f}%. R2 non-response (self-selection) bias explained in context: '
                f'respondents may be more motivated or more affected by {topic}, so results may not represent all {sent} students.')


# --------------------------------------------------------------------------------------------
# Mock material (year 2 additions; year 1 material is reused)
# --------------------------------------------------------------------------------------------
PRACTICALS_G12 = g11.PRACTICALS_G11 + [
    ('With reference to the survey you conducted in class, explain one decision you made about question wording.',
     'Describes a specific choice (e.g. avoiding leading or double-barrelled questions, using a balanced 5-point Likert scale, including reverse-scored items) and explains how it improved validity or reduced bias.'),
    ('Explain how you piloted the questionnaire used in your class survey and what you changed as a result.',
     'Describes a pilot with a few comparable participants, the problems found (ambiguous items, time taken, ceiling effects) and specific changes, linked to reliability/validity.'),
    ('Explain one way in which social desirability bias may have affected the results of your survey.',
     'Identifies an item where participants might give socially acceptable answers (e.g. hours of study, phone use) and explains the likely direction of bias; suggests anonymity or indirect questions.'),
    ('Describe how you analysed the closed questions in your class survey.',
     'States the descriptive statistics used (frequencies, percentages, modes or medians for Likert items) and the graph (bar chart), justified by the level of measurement.'),
    ('With reference to the interview you conducted in class, explain why you chose a semi-structured format.',
     'Explains that an interview schedule ensured comparable topics while follow-up probes allowed rich, participant-led data; links to the research question.'),
    ('Explain how you established rapport with your interviewee and why this mattered.',
     'Describes specific steps (setting, informal opening, active listening, neutral body language) and explains that rapport increases openness and the credibility of data.'),
    ('Describe the steps you followed to carry out an inductive content or thematic analysis of your interview transcript.',
     'Transcribed verbatim; read repeatedly; coded meaningful units; grouped codes into categories/themes; reviewed themes against the data; selected illustrative quotes.'),
    ('Explain one way in which you increased the credibility of the findings from your class interview.',
     'E.g. member checking (interviewee confirmed the summary), researcher triangulation (a second student coded the transcript), reflexivity notes about own influence; explains how it increases credibility.'),
    ('Explain one ethical issue in your class interview and how you addressed it.',
     'E.g. confidentiality of a recorded interview (pseudonym, deleting audio after transcription), right to withdraw (including withdrawing quotations), or sensitivity of the topic (avoided distressing topics, debrief).'),
    ('Compare the experiment and the survey you conducted in terms of what each allowed you to conclude.',
     'Experiment: manipulation and control allowed a causal conclusion within its limits; survey: described attitudes or relationships in a larger sample but could not show causation; both affected by sampling of peers.'),
]

UNSEEN_G12 = g11.UNSEEN_G11 + [
    ('Jigsaw lessons and prejudice', 'Two Grade 7 classes at a school in Nairobi with pupils from different ethnic groups took part. One class '
     'used jigsaw learning (each pupil taught a piece of the lesson to a mixed group) for six weeks; the other was taught normally. '
     'Pupils completed a prejudice questionnaire before and after. Prejudice scores fell by 18% in the jigsaw class and 3% in the other class. '
     'The teachers who delivered the lessons also administered the questionnaires.',
     ['quasi-experimental: intact classes not randomly allocated - class differences (teacher, existing friendships) confound the IV',
      'pre-post design with a comparison group is a strength', 'teachers administering questionnaires may create demand characteristics and social desirability bias',
      'self-report prejudice measure - social desirability; needs behavioural measures (e.g. seating choices)',
      'short follow-up - durability unknown', 'consistent with Aronson\'s jigsaw research and contact hypothesis conditions',
      'ethics: consent from parents, sensitivity about ethnic identity, the comparison class should later receive the programme']),
    ('Online survey of loneliness in older adults', 'A charity in Toronto posted a link to an online loneliness questionnaire on its social '
     'media pages. 1,240 people aged 65+ responded. 61% reported feeling lonely "often" or "always". The charity concluded that most '
     'older Canadians are lonely and launched a fundraising campaign.',
     ['self-selected online sample - those who follow a loneliness charity and use social media are not representative of all older adults',
      'online method excludes those without internet - possibly the most isolated', 'large sample is a strength but does not fix sampling bias',
      'single-item self-report; wording "often/always" needs a validated scale (e.g. UCLA Loneliness Scale)',
      'conflict of interest: charity benefits from high figures', 'ethics: anonymity, signposting support for distressed respondents',
      'improvement: stratified random sample, phone or postal option, validated measure']),
    ('Interviews with nurses about burnout', 'A researcher who used to work as a nurse in Mumbai conducted semi-structured interviews with 8 '
     'intensive-care nurses she knew personally. She coded the transcripts alone and identified three themes: "moral injury", '
     '"exhaustion" and "team as family". She did not report how she chose the nurses or whether participants reviewed the findings.',
     ['purposive/opportunity sample of acquaintances - relevant experience but possible bias; small sample appropriate for depth',
      'insider status may increase rapport but also leading questions or assumed understanding - reflexivity needed',
      'single coder - no researcher triangulation; no member checking - reduced credibility',
      'semi-structured format allows rich, participant-led data', 'transferability depends on thick description of context',
      'ethics: confidentiality is difficult when the researcher knows colleagues; dual relationship may pressure participation']),
    ('A spacing app trial', 'Forty volunteers from a language school in Lisbon used a spaced-repetition app for four weeks to learn 100 '
     'vocabulary items; forty different volunteers from the same school studied the same items from a list in massed sessions. The '
     'app group recalled a mean of 71 items and the list group 58 in a final test. The app company funded the research.',
     ['independent samples with volunteers - allocation method unclear; need random allocation', 'same items and test - good control of materials',
      'study time may differ between conditions (confound) - must be equated', 'funding bias - independent replication needed',
      'consistent with research on spacing (Cepeda et al., 2006)', 'no inferential statistics or SDs reported',
      'ethics: informed consent; control group could be offered the app afterwards']),
]

P3_G12 = g11.P3_G11 + [
    dict(theme='Helping strangers in cities',
         sources=['(Interview extract, hypothetical study of commuters in Bogotá) "If the person looks drunk, I think it\'s their own fault." '
                  '"When there are lots of people, I assume someone else already called for help." "I helped once, but I was scared of being robbed."',
                  '(Quantitative data, hypothetical field experiment) Percentage of passers-by who helped a confederate pick up dropped papers: '
                  'alone in the street 64%; 2-3 bystanders 41%; 10+ bystanders 22%. n = 300 trials across five cities.',
                  '(Method summary) Researchers in 23 large cities measured helping in three staged situations (dropped pen, injured leg, blind '
                  'person at a crossing) using local confederates following the same script.'],
         q1=(0, 'Identify three reasons for not helping given by the commuters in Source A.',
             'Victim seen as responsible (drunk) - attribution of blame; diffusion of responsibility in crowds; perceived personal cost/danger (fear of robbery).'),
         q2=(1, 'Interpret the data in Source B.',
             'Helping fell as the number of bystanders rose (64% alone, 41% with 2-3, 22% with 10+), consistent with diffusion of responsibility (Darley and Latané, 1968); no inferential statistics are given, so significance is unknown.'),
         q3=(2, 'Evaluate the method described in Source C.',
             'Strengths: standardised scripts and situations allow cross-city comparison; natural behaviour (high ecological validity). Limitations: confederates differ between cities; situations may have different meanings across cultures; no consent from passers-by; single time of day/location may not represent a city.'),
         q4=('Using all the sources and your own knowledge, discuss factors that influence whether people help strangers.',
             'Situational factors (number of bystanders - Source B; Darley and Latané, 1968), cost-reward judgements and victim characteristics (Source A; Piliavin et al., 1969), and culture (Source C; Levine et al., 2001, simpatía in Rio). Weigh qualitative insight vs quantitative patterns; conclude that helping depends on the interaction of situation, cognition and culture.')),
    dict(theme='Growth mindset in schools',
         sources=['(Teacher focus group extract, hypothetical study, Singapore) "The posters say \'mistakes help you grow\', but our exams punish '
                  'every mistake." "Some students now just say \'I don\'t have a growth mindset\' as an excuse."',
                  '(Quantitative data, hypothetical randomised trial) 2,400 Year 9 students: GPA change after a 50-minute online mindset lesson: '
                  'lower-achieving students +0.10; higher-achieving students +0.01; control group 0.00.',
                  '(Method summary) A survey asked 500 students to rate how far they agreed that "intelligence can be developed" and correlated '
                  'this with their grades (r = 0.12).'],
         q1=(0, 'Identify three problems with implementing growth mindset that the teachers describe in Source A.',
             'Conflict between the message and assessment practices; superficial implementation (posters); students using the label as an excuse.'),
         q2=(1, 'Interpret the results presented in Source B.',
             'The intervention produced a small GPA improvement for lower-achieving students (+0.10) and almost none for higher achievers; random allocation supports causality; effects are small, consistent with Yeager et al. (2019) and Sisk et al. (2018).'),
         q3=(2, 'Evaluate the method used in Source C.',
             'Correlational - cannot show that mindset causes grades; r = 0.12 is very weak; self-report of beliefs (social desirability); single item; large sample is a strength.'),
         q4=('Using all the sources and your own knowledge, evaluate the claim that teaching a growth mindset improves learning.',
             'B gives causal but small effects, mostly for lower achievers; C shows a weak correlation; A shows implementation problems; own knowledge: Blackwell et al. (2007) positive, Sisk et al. (2018) meta-analysis weak, replication concerns. Conclusion: modest benefits for some students when the school context supports the message.')),
    dict(theme='Arranged and love marriages',
         sources=['(Interview extract, hypothetical study of couples in Jaipur) "Our parents chose well - we grew to love each other." '
                  '"In a love marriage, if problems come, you have nobody to blame but yourself." "My family\'s support kept us together."',
                  '(Quantitative data, hypothetical survey) Mean marital satisfaction (1-7): arranged marriages in India 5.4 (SD 1.1), love marriages '
                  'in India 5.3 (SD 1.3), love marriages in the USA 5.2 (SD 1.4); Mann-Whitney comparisons not significant.',
                  '(Method summary) Researchers translated a US marital satisfaction scale into Hindi and gave it to couples recruited through a '
                  'temple community in one city.'],
         q1=(0, 'Identify three factors that the couples in Source A say contributed to their relationships.',
             'Parental judgement in partner choice; love developing over time; family support and shared responsibility (social network).'),
         q2=(1, 'Interpret the results presented in Source B.',
             'Satisfaction was similar across all three groups (5.2-5.4) with no significant differences, consistent with Myers et al. (2005); slightly larger SDs in love marriages suggest more variability; type of marriage does not appear to determine satisfaction.'),
         q3=(2, 'Evaluate the method described in Source C.',
             'Translation of a US scale risks an imposed etic (concepts of satisfaction may differ); temple-community sample is not representative; self-report and social desirability (reluctance to criticise marriage); suggest back-translation, emic items, wider sampling.'),
         q4=('Using all the sources and your own knowledge, discuss the extent to which culture influences relationships.',
             'Culture shapes how relationships form (arranged vs choice), the role of family (Source A) and the meaning of satisfaction; but satisfaction levels may be similar (Source B; Myers et al., 2005); Gupta and Singh (1982) found love grew in arranged marriages; measurement issues (Source C) limit comparison. Conclusion: culture strongly affects relationship formation and maintenance, less clearly outcomes.')),
    dict(theme='Smartphones and attention in class',
         sources=['(Student interview extract, hypothetical study, Melbourne) "Even if it\'s face down I keep thinking someone messaged me." '
                  '"When the school banned phones, I actually talked to people at lunch." "I use my phone to check words - it helps."',
                  '(Quantitative data, hypothetical experiment) Working memory span (mean): phone in another room 31.2; phone in bag 30.1; phone on '
                  'desk face down 28.4. n = 520 students randomly allocated; differences significant (p < 0.05).',
                  '(Method summary) A newspaper compared exam results in schools that banned phones with schools that did not and reported higher '
                  'results in schools with bans.'],
         q1=(0, 'Identify three effects of smartphones described by the students in Source A.',
             'Distraction/attentional capture even when not in use; reduced face-to-face social interaction; a helpful learning tool (dictionary).'),
         q2=(1, 'Interpret the results presented in Source B.',
             'Working memory span was lowest with the phone on the desk (28.4) and highest with it in another room (31.2); random allocation and significance support the claim that phone presence reduces available cognitive capacity ("brain drain"; Ward et al., 2017).'),
         q3=(2, 'Evaluate the method described in Source C.',
             'Not an experiment: schools chose bans, so school differences (resources, intake) confound results; no statistics; media reporting may be biased; need matched schools or a before/after design with controls.'),
         q4=('Using all the sources and your own knowledge, discuss whether schools should ban smartphones to improve learning.',
             'B provides causal evidence of cognitive cost; A shows both distraction and social benefits of bans but also educational uses; C is weak correlational evidence; own knowledge: Ophir et al. (2009) multitasking, Sana et al. (2013). Conclusion: limiting phone presence during focused learning is supported; total bans should consider educational use and enforcement.')),
]

P1_CH_G12 = [1, 2, 3, 4, 5, 8, 9, 10]
P2_CH_G12 = [6, 7, 11, 12]
K = Kit(unseen=UNSEEN_G12, p3=P3_G12, practicals=PRACTICALS_G12, p1_ch=P1_CH_G12, p2_ch=P2_CH_G12)
R = K.R

MOCK = [
    dict(section='Paper 1, Section A - short answer', count=2, c=['C2'], d=[2, 3], marks=4, style='p1a', chapters=P1_CH_G12),
    dict(section='Paper 1, Section B - applied short answer', count=2, c=['C3'], d=[3, 4], marks=6, style='p1b', chapters=P1_CH_G12),
    dict(section='Paper 1, Section C - extended response (answer one of two)', count=2, c=['C4'], d=[4, 5], marks=15, style='p1x', chapters=P1_CH_G12),
    dict(section='Paper 2, Section A - practical-based questions', count=4, c=['C3'], d=[3, 4], marks=5, style='p2q', chapters=P2_CH_G12),
    dict(section='Paper 2, Section B - evaluation of an unseen study', count=1, c=['C4'], d=[5], marks=15, style='p2u', chapters=P2_CH_G12),
    dict(section='Paper 3 - Question 1 (source-based)', count=1, c=['C3'], d=[2], marks=3, style='p3q1'),
    dict(section='Paper 3 - Question 2 (source-based)', count=1, c=['C3'], d=[3], marks=6, style='p3q2'),
    dict(section='Paper 3 - Question 3 (source-based)', count=1, c=['C4'], d=[4], marks=6, style='p3q3'),
    dict(section='Paper 3 - Question 4 (source-based synthesis)', count=1, c=['C4'], d=[5], marks=15, style='p3q4'),
]


def init(subject_id):
    K.init()


def templates(st):
    return K.templates(st)


# =============================================================================================
# CONTENT
# =============================================================================================
# ---------------------------------------------------------------------------------------------
# ch01 Human relationships: personal relationships
# ---------------------------------------------------------------------------------------------
K.facts('ch01-st1', F(
    terms=[('interpersonal attraction', 'the positive feelings and desire to be close to another person that lead to forming a relationship'),
           ('proximity', 'physical or functional closeness between people, which increases the chance of interaction and attraction'),
           ('mere exposure effect', 'the tendency to develop a preference for people or things simply because they are familiar'),
           ('similarity-attraction hypothesis', 'the idea that people are attracted to others who share their attitudes, values and background'),
           ('matching hypothesis', 'the idea that people tend to form relationships with partners of similar social desirability, especially physical attractiveness'),
           ('halo effect', 'the tendency to assume that people who are physically attractive also have other positive traits')],
    facts=[('Festinger, Schachter and Back (1950) found that friendships in the Westgate student housing complex were most strongly predicted by:', 'Physical and functional proximity', ['Shared academic subjects', 'Similar family income', 'Physical attractiveness'],
            'Residents were most likely to befriend next-door neighbours and people near stairways and mailboxes.'),
           ('Byrne (1961) used the "bogus stranger" technique to show that liking increased with:', 'Attitude similarity', ['Physical distance', 'Physical attractiveness only', 'Age difference'],
            'Participants liked a stranger more when the stranger\'s questionnaire showed similar attitudes.'),
           ('In Walster et al.\'s (1966) "computer dance", the best predictor of wanting to date a partner again was:', 'The partner\'s physical attractiveness', ['Similarity of personality', 'Similar intelligence', 'Proximity of homes'],
            'This contradicted the matching hypothesis they set out to test.')],
    why=[('Explain why proximity increases the likelihood of attraction.', 'Proximity creates more opportunities for interaction and the mere exposure effect increases familiarity and liking; it also reduces the cost of maintaining contact (Festinger et al., 1950).'),
         ('Explain why similarity may lead to attraction.', 'Similar others validate our attitudes and beliefs, make interaction predictable and rewarding, and signal likely future agreement, so they are evaluated positively (Byrne, 1961).')],
    contrast=[('the similarity-attraction hypothesis', 'the matching hypothesis', 'The similarity-attraction hypothesis says we like people with similar attitudes and values; the matching hypothesis says we choose partners of similar overall social desirability, especially attractiveness.')],
    misc=[('Online dating has made proximity irrelevant to attraction.', 'Online dating changes "proximity" to functional proximity (frequent contact on apps and messaging) and most couples still need physical meetings; proximity remains important, though in new forms.')],
    cases=[('roommates at an international school', 'Aiko and Freya, from Japan and Norway, are assigned to the same room in a boarding school in Geneva and become best friends within a term, despite different interests.', 'the role of proximity in relationship formation', 'frequent interaction and mere exposure created by shared living space led to liking, consistent with Festinger et al. (1950)')],
    apply=[('A dating app in Seoul matches users on shared hobbies and political views. Using research, evaluate whether this is likely to increase attraction.', 'Similarity predicts liking (Byrne, 1961), so matching on attitudes may help; but physical attractiveness predicted first-date liking (Walster et al., 1966) and actual similarity may matter less than perceived similarity; real-world proximity and interaction still matter.', 4)],
    evaluate=[('Similarity is the most important factor in the formation of relationships.', ['bogus stranger research (Byrne, 1961)', 'similarity of values in long-term couples'],
               ['proximity (Festinger et al., 1950)', 'physical attractiveness (Walster et al., 1966)', 'cultural factors such as family involvement'],
               'Similarity is important, especially for long-term relationships, but formation depends on opportunity (proximity) and initial attraction.')],
))
K.study('ch01-st1', 'Festinger, Schachter and Back', 1950, 'proximity and friendship in student housing', 'to investigate whether physical proximity influences the formation of friendships',
        'Married students randomly assigned to apartments in the Westgate housing complex at MIT were asked to name their three closest friends in the complex; distances between apartments were measured.',
        'friendships were most common between next-door neighbours, and residents in apartments near stairways and mailboxes had more friends (functional proximity)',
        'the role of proximity in relationship formation',
        ['random assignment to apartments rules out choice of neighbours', 'natural setting'],
        ['homogeneous sample (married ex-servicemen students)', 'friendship measured by a simple nomination'],
        mtype='natural experiment', wrong=['Friendships were unrelated to the distance between apartments', 'Residents near stairways had the fewest friends', 'Most friendships were with people in other buildings'])
K.study('ch01-st1', 'Byrne', 1961, 'attitude similarity and attraction', 'to investigate whether similarity of attitudes increases attraction to a stranger',
        'Students completed an attitude questionnaire and two weeks later saw a "stranger\'s" questionnaire (actually faked to be similar or dissimilar to their own), then rated how much they would like the stranger.',
        'participants rated similar strangers as more likeable, more intelligent and better adjusted than dissimilar strangers',
        'the similarity-attraction hypothesis',
        ['controlled manipulation of similarity', 'widely replicated'],
        ['artificial - no real interaction', 'deception', 'US student sample'],
        mtype='laboratory experiment', iv='similarity of the bogus stranger\'s attitudes', dv='rating of liking for the stranger')
K.study('ch01-st1', 'Walster et al.', 1966, 'the "computer dance"', 'to test the matching hypothesis in a real dating situation',
        '752 first-year students at the University of Minnesota bought tickets for a dance and were told a computer would match them with a partner (in fact randomly); their attractiveness was rated secretly, and they rated their partner during the dance.',
        'the strongest predictor of liking and wanting a second date was the partner\'s physical attractiveness, regardless of the participant\'s own attractiveness',
        'the role of physical attractiveness in initial attraction',
        ['real dates - high ecological validity', 'large sample'],
        ['deception about the matching process', 'only short-term first impressions', 'US students in the 1960s'],
        mtype='field experiment')

K.facts('ch01-st2', F(
    terms=[('attribution', 'the explanation a person gives for the causes of their own or others\' behaviour'),
           ('relationship-enhancing attribution', 'explaining a partner\'s positive behaviour as internal and stable, and negative behaviour as external and temporary'),
           ('distress-maintaining attribution', 'explaining a partner\'s negative behaviour as internal and stable, and positive behaviour as external and temporary'),
           ('accommodation', 'responding constructively rather than destructively when a partner behaves badly (Rusbult et al., 1991)'),
           ('self-disclosure', 'revealing personal information about oneself to another person'),
           ('the four horsemen', 'Gottman\'s four communication patterns that predict relationship breakdown: criticism, contempt, defensiveness and stonewalling'),
           ('communication accommodation theory', 'the theory that people adjust their communication style to converge with or diverge from others')],
    facts=[('Which of Gottman\'s "four horsemen" is considered the strongest predictor of divorce?', 'Contempt', ['Criticism', 'Defensiveness', 'Stonewalling'],
            'Contempt (mockery, eye-rolling) signals disrespect and superiority.'),
           ('Fincham and Bradbury (1993) found that attributions measured at the start of their study predicted:', 'Later marital satisfaction', ['Later income', 'Number of children', 'Physical health only'],
            'Distress-maintaining attributions predicted lower satisfaction 12 months later, even controlling for initial satisfaction.'),
           ('Rusbult et al. (1991) found that accommodation was more likely when partners were:', 'Highly committed to the relationship', ['Newly acquainted', 'Highly dissatisfied', 'Living apart'],
            'Commitment predicted willingness to respond constructively to a partner\'s destructive behaviour.')],
    why=[('Explain how attributions can maintain relationship distress.', 'If a partner\'s negative behaviour is attributed to stable, internal causes ("he is selfish") and positive behaviour to external, temporary causes, every event confirms dissatisfaction, reducing goodwill and increasing conflict.'),
         ('Explain why accommodation helps maintain relationships.', 'Responding constructively (voice, loyalty) instead of destructively (exit, neglect) to a partner\'s bad behaviour prevents escalating conflict and signals commitment, which builds trust.')],
    contrast=[('relationship-enhancing attributions', 'distress-maintaining attributions', 'Enhancing attributions credit the partner for positive behaviour and excuse negative behaviour as situational; distress-maintaining attributions do the opposite, blaming the partner for negatives and discounting positives.')],
    misc=[('Couples who never argue have the most stable relationships.', 'Gottman found that how couples argue matters more than whether they argue - conflict with respect and repair is compatible with stability; contempt and stonewalling are the danger signs.')],
    cases=[('a couple after a forgotten anniversary', 'Kwame forgets his partner Nia\'s birthday because of a work crisis. Nia thinks, "He was overwhelmed this week - he usually remembers," and they talk about it calmly.', 'attribution and accommodation', 'Nia makes an external, temporary attribution and responds constructively, which protects satisfaction - a relationship-enhancing pattern')],
    apply=[('A couples counsellor in Toronto wants to improve communication in distressed couples. Using research, suggest two strategies.', 'Train partners to notice and challenge distress-maintaining attributions (Fincham and Bradbury, 1993); teach constructive accommodation and repair attempts; replace contempt with expressions of appreciation (Gottman).', 4)],
    evaluate=[('Communication is the most important factor in maintaining relationships.', ['Gottman\'s research on the four horsemen', 'attributions predict satisfaction (Fincham and Bradbury, 1993)'],
               ['commitment and investment (Rusbult, 1983)', 'external stressors such as poverty', 'communication may be a symptom of dissatisfaction'],
               'Communication strongly predicts outcomes, but it interacts with commitment, resources and context.')],
))
K.study('ch01-st2', 'Fincham and Bradbury', 1993, 'attributions and marital satisfaction', 'to investigate whether the attributions spouses make predict later marital satisfaction',
        '130 married couples in the USA completed measures of attribution and satisfaction, and satisfaction was measured again 12 months later.',
        'wives\' (and to a lesser extent husbands\') distress-maintaining attributions predicted lower satisfaction 12 months later, even when initial satisfaction and depression were controlled',
        'the role of attributions in maintaining relationships',
        ['longitudinal - attributions measured before later satisfaction', 'controlled for initial satisfaction and depression'],
        ['self-report questionnaires', 'married American couples only'],
        mtype='longitudinal study')
K.study('ch01-st2', 'Gottman and Levenson', 1992, 'marital interaction and divorce', 'to investigate whether patterns of interaction predict marital stability',
        '73 couples in Bloomington, Indiana were observed discussing a conflict in the laboratory; interactions and physiological measures were coded and the couples were followed up four years later.',
        'couples whose interactions showed more negative than positive behaviour (e.g. criticism, defensiveness, contempt, stonewalling) were more likely to have considered or obtained divorce',
        'the role of communication in maintaining relationships',
        ['objective coding of observed behaviour with physiological measures', 'longitudinal follow-up'],
        ['lab setting may change how couples argue', 'US sample; communication norms differ across cultures'],
        mtype='longitudinal study')
K.study('ch01-st2', 'Rusbult et al.', 1991, 'accommodation in close relationships', 'to investigate the factors that make partners respond constructively to destructive behaviour',
        'A series of studies with US students in dating relationships used questionnaires and hypothetical scenarios to measure tendencies to accommodate and related variables (commitment, satisfaction, investment).',
        'accommodation was greater in people with higher commitment, satisfaction and investment, and was associated with better relationship functioning',
        'accommodation as a maintenance strategy',
        ['several converging studies'],
        ['self-reported intentions rather than behaviour', 'student dating couples'],
        mtype='correlational study')

K.facts('ch01-st3', F(
    terms=[('social exchange theory', 'the theory that relationships are maintained when rewards exceed costs and outcomes compare well with alternatives (Thibaut and Kelley, 1959)'),
           ('comparison level', 'the level of outcomes a person believes they deserve, based on past relationships and social norms'),
           ('comparison level for alternatives', 'the outcomes a person believes they could get in an alternative relationship or by being alone'),
           ('investment model', 'Rusbult\'s model that commitment depends on satisfaction, quality of alternatives and size of investment'),
           ('investment size', 'the resources (time, emotion, shared friends, possessions, children) a person would lose if the relationship ended'),
           ('commitment', 'the intention to continue a relationship and feel psychologically attached to it')],
    facts=[('According to Rusbult\'s investment model, commitment is predicted by:', 'Satisfaction, quality of alternatives and investment size', ['Proximity, similarity and attractiveness', 'Attributions, communication and conflict', 'Age, income and education'],
            'High satisfaction, poor alternatives and large investments produce high commitment.'),
           ('Le and Agnew\'s (2003) meta-analysis of the investment model included about:', '52 studies and over 11,000 participants', ['5 studies and 200 participants', '500 studies and 1 million participants', 'One longitudinal study'],
            'Satisfaction, alternatives and investment together explained about two-thirds of the variance in commitment.')],
    why=[('Explain how the investment model accounts for people staying in unhappy relationships.', 'Even with low satisfaction, commitment can remain high if investments are large (children, shared home) and alternatives seem poor, so leaving would be too costly - e.g. Rusbult and Martz (1995) on women in abusive relationships.'),
         ('Explain why social exchange theory has been criticised.', 'It assumes people calculate rewards and costs selfishly, which may not fit communal relationships where partners give without keeping score; it also struggles to define rewards and costs objectively.')],
    contrast=[('social exchange theory', 'the investment model', 'Social exchange theory focuses on rewards, costs and comparison levels; the investment model adds investment size and explains commitment, not just satisfaction.')],
    misc=[('Relationships end only when satisfaction falls.', 'Relationships can end when attractive alternatives appear or investment is low even if satisfaction is moderate, and can continue despite low satisfaction when investment is high.')],
    cases=[('a long engagement under strain', 'Diego and Ana have been together for eight years in Lima, share a flat and a dog, and have mutual friends. Ana is unhappy, but says, "We have built so much together."', 'the investment model', 'high investment (time, shared home, friends) keeps commitment high despite low satisfaction, as the model predicts')],
    apply=[('Using the investment model, predict which of two equally satisfied students is more likely to stay in a relationship: one who has just moved to a new city with no friends, or one with many attractive alternatives. Explain.', 'The student with no friends in the new city has poorer alternatives, so commitment should be higher; the student with many attractive alternatives has a higher comparison level for alternatives and lower commitment.', 3)],
    evaluate=[('The investment model is the best explanation of why relationships change or end.', ['meta-analytic support (Le and Agnew, 2003)', 'explains staying in abusive relationships (Rusbult and Martz, 1995)'],
               ['correlational self-report data', 'ignores communication processes and external stress', 'Western, individualist samples'],
               'The investment model predicts commitment well, but a full explanation must include communication and cultural context.')],
))
K.study('ch01-st3', 'Rusbult', 1983, 'commitment in dating relationships', 'to test whether satisfaction, alternatives and investment predict commitment over time',
        'Undergraduate students in heterosexual dating relationships completed questionnaires every 17 days for up to seven months, measuring rewards, costs, satisfaction, alternatives, investment and commitment.',
        'commitment increased as satisfaction and investment rose and alternatives declined; those who broke up had shown falling commitment and rising alternatives',
        'the investment model of commitment',
        ['longitudinal with repeated measures', 'tested specific predictions'],
        ['student dating couples only', 'self-report; correlational'],
        mtype='longitudinal study')
K.study('ch01-st3', 'Le and Agnew', 2003, 'a meta-analysis of the investment model', 'to assess how well satisfaction, alternatives and investment predict commitment across studies',
        'Meta-analysis of 52 studies (60 independent samples, over 11,000 participants) from 1983 to 1999, including studies from several countries and types of relationship.',
        'satisfaction, alternatives and investment each significantly predicted commitment, together explaining about two-thirds of its variance; commitment predicted staying versus leaving',
        'the generalisability of the investment model',
        ['large combined sample across relationship types and some cultures'],
        ['relies on correlational, self-report studies', 'mostly US samples'],
        mtype='meta-analysis')

K.facts('ch01-st4', F(
    terms=[('arranged marriage', 'a marriage in which the families play a central role in choosing the partners, usually with the consent of the couple'),
           ('love marriage', 'a marriage based on the partners\' own choice following romantic attraction'),
           ('collectivist relationship norms', 'norms that emphasise family approval, duty and group harmony in choosing and maintaining relationships'),
           ('voluntary relationship', 'a relationship freely chosen by the individuals, typical of individualist cultures')],
    facts=[('Gupta and Singh (1982) studied 50 couples in Jaipur and found that, after about five years, love was:', 'Higher in arranged marriages than in love marriages', ['Higher in love marriages than in arranged marriages', 'Equal in both types', 'Absent in arranged marriages'],
            'Love declined over time in love marriages but grew in arranged marriages.'),
           ('Myers, Madathil and Tingle (2005) compared marital satisfaction in Indian arranged marriages and US marriages of choice and found:', 'No significant difference in satisfaction', ['Much higher satisfaction in US marriages', 'Much higher satisfaction in arranged marriages', 'Arranged marriages were all unhappy'],
            'Type of marriage did not predict satisfaction in their sample.')],
    why=[('Explain why arranged marriages can be as satisfying as love marriages.', 'Family support and shared values reduce conflict and increase investment; expectations focus on duty and companionship rather than intense romance, and love can grow over time (Gupta and Singh, 1982).')],
    contrast=[('arranged marriage', 'forced marriage', 'In an arranged marriage families help choose a partner but both people consent; in a forced marriage one or both partners do not consent, which is a human rights violation.')],
    misc=[('Arranged marriages are the same as forced marriages.', 'Arranged marriages involve family selection with the couple\'s consent; forced marriage lacks consent.')],
    cases=[('a British Indian family in Leicester', 'Priya\'s parents introduce her to several suitable men; she meets each a few times and chooses one. She describes it as an "assisted" marriage.', 'cultural variation in relationships', 'it shows a blend of collectivist family involvement and individualist choice, common in second-generation migrants')],
    apply=[('A researcher wants to compare satisfaction in arranged and love marriages in Mumbai. Identify two methodological issues she should consider.', 'Self-selection: couples are not randomly assigned to marriage types (confounds such as religion, class); measurement: translated Western satisfaction scales may be an imposed etic; social desirability in reporting marital problems.', 4)],
    evaluate=[('Love marriages are more successful than arranged marriages.', ['choice may produce better initial compatibility', 'higher passionate love early on'],
               ['love grew in arranged marriages (Gupta and Singh, 1982)', 'no difference in satisfaction (Myers et al., 2005)', 'divorce rates reflect stigma and law as well as satisfaction'],
               'There is little evidence that one type is more successful; outcomes depend on cultural expectations and support.')],
))
K.study('ch01-st4', 'Gupta and Singh', 1982, 'love in arranged and love marriages in Jaipur', 'to compare the development of love in arranged and love marriages',
        '50 couples in Jaipur, India, completed Rubin\'s love and liking scales; couples were compared by type of marriage and length of marriage.',
        'love marriages started with higher love that declined after about five years, while love in arranged marriages increased over time',
        'cultural variation in the development of love',
        ['real couples in a culture where both types are common'],
        ['small sample; cross-sectional, not longitudinal', 'Western love scales translated (imposed etic)', 'self-report'],
        mtype='correlational study')
K.study('ch01-st4', 'Myers, Madathil and Tingle', 2005, 'arranged marriages and marriages of choice', 'to compare marital satisfaction in arranged marriages in India with marriages of choice in the USA',
        '45 individuals in arranged marriages in India and 58 in marriages of choice in the USA completed questionnaires on marital satisfaction and well-being.',
        'there was no significant difference in marital satisfaction between the two groups',
        'cultural variation in relationship satisfaction',
        ['cross-cultural comparison with standardised scales'],
        ['small samples; nationality and marriage type confounded', 'translation and self-report issues'],
        mtype='questionnaire survey')

# ---------------------------------------------------------------------------------------------
# ch02 Human relationships: group dynamics
# ---------------------------------------------------------------------------------------------
K.facts('ch02-st1', F(
    terms=[('prejudice', 'a negative attitude towards members of a group based solely on their group membership'),
           ('discrimination', 'unfair behaviour towards members of a group because of their group membership'),
           ('authoritarian personality', 'Adorno et al.\'s (1950) personality type, linked to strict upbringing, characterised by rigid thinking, obedience to authority and hostility to out-groups'),
           ('F-scale', 'the questionnaire developed by Adorno et al. (1950) to measure authoritarian (potentially fascist) tendencies'),
           ('scapegoating', 'blaming an out-group for problems, often when the real cause cannot be attacked'),
           ('implicit bias', 'unconscious, automatic associations about social groups that can influence behaviour')],
    facts=[('Pettigrew (1958) found that white South Africans and white Americans in the South had high prejudice but average authoritarianism. He concluded that prejudice was mainly due to:', 'Conformity to social norms', ['Authoritarian personality', 'Genetic factors', 'Lack of education'],
            'Prejudice reflected cultural norms rather than personality.'),
           ('Which of the following is an example of discrimination rather than prejudice?', 'Refusing to rent a flat to someone because of their ethnicity', ['Disliking a group', 'Believing a stereotype', 'Feeling uncomfortable around a group'],
            'Discrimination is behaviour; prejudice is an attitude.')],
    why=[('Explain how social identity theory accounts for prejudice.', 'People derive self-esteem from group memberships and seek positive distinctiveness, so they favour the in-group and may devalue out-groups in social comparison; categorisation alone can produce bias (Tajfel et al., 1971).'),
         ('Explain why prejudice can be learned from the social environment.', 'Children acquire attitudes through observation and reinforcement from parents, peers and media, and conform to group norms (Pettigrew, 1958).')],
    contrast=[('dispositional explanations of prejudice', 'situational explanations of prejudice', 'Dispositional explanations locate prejudice in personality (authoritarian personality); situational explanations locate it in group processes, competition and norms (SIT, RCT, conformity).')],
    misc=[('Prejudice is mainly caused by having an authoritarian personality.', 'Personality explains only some variation; whole societies can show prejudice through norms (Pettigrew, 1958) and group processes, which personality cannot explain.')],
    cases=[('football chants targeting players', 'Fans in a European league chant abuse at players from an ethnic minority; individual fans who join in say they "would never do it alone".', 'origins of prejudice', 'group norms and deindividuation within a strong social identity encourage discrimination that individuals would not show alone')],
    apply=[('A company in Dubai finds managers rate candidates with foreign-sounding names lower. Using one explanation of prejudice, explain this and suggest one intervention.', 'Implicit bias/stereotypes or in-group favouritism (SIT) affect evaluation; intervention: anonymised CVs, structured interviews with criteria, diverse panels.', 4)],
    evaluate=[('Prejudice is best explained by social identity theory.', ['minimal groups (Tajfel et al., 1971)', 'explains in-group bias without competition'],
               ['realistic conflict (Sherif et al., 1961)', 'norms and conformity (Pettigrew, 1958)', 'personality factors (Adorno et al., 1950)'],
               'SIT explains in-group favouritism well, but prejudice usually results from several interacting factors.')],
))
K.study('ch02-st1', 'Adorno et al.', 1950, 'the authoritarian personality', 'to investigate whether a particular personality type is associated with prejudice',
        'Over 2,000 white middle-class Americans completed scales including the F-scale; some high and low scorers were interviewed about their childhood.',
        'high F-scale scorers were more prejudiced against minorities and often described strict, harsh parenting and conditional love',
        'personality explanations of prejudice',
        ['large sample; combined questionnaires and interviews'],
        ['F-scale items all worded in one direction - acquiescence bias', 'correlational; interviewers knew participants\' scores', 'cannot explain prejudice in whole societies'],
        mtype='correlational study')
K.study('ch02-st1', 'Pettigrew', 1958, 'prejudice in South Africa and the US South', 'to investigate whether prejudice is explained by personality or by social norms',
        'White participants in South Africa and in northern and southern US towns completed measures of authoritarianism and anti-Black prejudice.',
        'levels of prejudice were high in South Africa and the US South, but authoritarianism was not higher there; conformity to local norms predicted prejudice',
        'social norms as an origin of prejudice',
        ['cross-cultural comparison of personality and norms'],
        ['self-report questionnaires', 'correlational'],
        mtype='questionnaire survey')
K.study('ch02-st1', 'Tajfel et al.', 1971, 'minimal groups and discrimination', 'to investigate whether categorisation into trivial groups produces discrimination',
        'British schoolboys aged 14-15 were allocated to groups apparently based on preference for paintings by Klee or Kandinsky (actually random) and then distributed points between anonymous in-group and out-group members.',
        'boys favoured in-group members and often chose to maximise the difference between groups rather than total gain',
        'social categorisation as an origin of prejudice',
        ['controlled; isolates categorisation from conflict'],
        ['artificial setting', 'all-male British sample', 'demand characteristics'],
        mtype='laboratory experiment')

K.facts('ch02-st2', F(
    terms=[('realistic conflict theory', 'Sherif\'s theory that intergroup conflict arises from competition between groups for scarce resources'),
           ('competition', 'a situation in which one group can gain only at another group\'s expense (negative interdependence)'),
           ('cooperation', 'working together towards shared goals (positive interdependence)'),
           ('superordinate goal', 'a goal that both groups want but can achieve only by working together'),
           ('zero-sum situation', 'a situation in which one group\'s gain is the other\'s loss')],
    facts=[('In the Robbers Cave study (Sherif et al., 1961), the two groups of boys called themselves:', 'The Rattlers and the Eagles', ['The Lions and the Tigers', 'The Reds and the Blues', 'The Hawks and the Bears'],
            'The groups formed at a Boy Scouts camp in Oklahoma in 1954.'),
           ('What finally reduced hostility between the groups in the Robbers Cave study?', 'Working towards superordinate goals', ['Simple contact at meals', 'Separating the groups', 'Lectures on tolerance'],
            'E.g. fixing the water supply and pulling a broken-down truck together.'),
           ('Tyerman and Spencer (1983) observed scouts at their annual camp and found:', 'Competition between patrols did not produce hostility', ['Competition produced extreme hostility', 'Scouts refused to compete', 'Cooperation increased prejudice'],
            'Long-standing friendships and a shared identity limited conflict.')],
    why=[('Explain how competition can lead to intergroup conflict.', 'When groups compete for scarce resources in a zero-sum situation, each group\'s goals conflict, producing negative stereotypes, in-group solidarity and hostility (Sherif et al., 1961).'),
         ('Explain why cooperation reduces conflict.', 'When groups depend on each other to reach a shared goal, interactions become positive, the out-group is seen as helpful, and a common identity can develop.')],
    contrast=[('realistic conflict theory', 'social identity theory', 'RCT says conflict arises from competition for resources; SIT says in-group favouritism can arise from categorisation alone, even without competition.')],
    misc=[('Robbers Cave proved that competition always causes conflict.', 'Tyerman and Spencer (1983) found competition did not cause hostility among scouts who already knew each other; the Robbers Cave groups were also influenced by the researchers\' manipulations.')],
    cases=[('rival schools sharing a sports ground', 'Two schools in Melbourne compete every year for the use of the only floodlit pitch; pupils start insulting each other on social media.', 'realistic conflict theory', 'competition for a scarce resource creates negative interdependence, hostility and negative stereotypes of the other school')],
    apply=[('Two departments in a company in Accra compete for a single annual bonus and have become hostile. Using realistic conflict theory, suggest how management could reduce the conflict.', 'Replace the zero-sum bonus with a shared target that requires cooperation (superordinate goal) and reward joint performance; create mixed project teams.', 3)],
    evaluate=[('Competition is the main cause of intergroup conflict.', ['Robbers Cave (Sherif et al., 1961)', 'conflicts over land and water in the real world'],
               ['hostility appeared before competition in Robbers Cave', 'minimal groups show bias without competition', 'Tyerman and Spencer (1983)'],
               'Competition intensifies conflict, but social identity processes are also important and can produce bias on their own.')],
))
K.study('ch02-st2', 'Sherif et al.', 1961, 'the Robbers Cave experiment', 'to investigate whether competition for resources produces intergroup conflict and whether superordinate goals reduce it',
        '22 white, middle-class 11-12-year-old boys at a summer camp in Robbers Cave State Park, Oklahoma (1954) were divided into two groups; after a week of bonding, they competed in a tournament; finally they worked on superordinate goals. Researchers acted as camp staff and observed covertly.',
        'competition produced hostility, name-calling and raids; simple contact did not reduce it, but superordinate goals (fixing the water supply, moving a truck) did',
        'competition and cooperation in intergroup relations',
        ['field experiment with natural behaviour', 'staged sequence shows the effect of competition and of superordinate goals'],
        ['very homogeneous sample', 'researchers may have encouraged conflict (Perry, 2018)', 'no consent from the boys; deception'],
        mtype='field experiment', ethics='The boys did not know they were in a study, were deliberately set against each other and experienced hostility; parents consented but the boys were deceived.',
        wrong=['Competition increased friendship between the groups', 'Simple contact at meals ended the hostility', 'The groups never became hostile'])
K.study('ch02-st2', 'Tyerman and Spencer', 1983, 'competition among scout patrols', 'to investigate whether competition produces intergroup conflict among groups that already share an identity',
        'Researchers observed patrols of a Scout troop in England at their annual camp, where they competed in a series of activities; observation was naturalistic and supplemented by interviews.',
        'competition between patrols did not lead to hostility; long-term friendships and a shared troop identity maintained good relations',
        'the limits of realistic conflict theory',
        ['naturalistic setting', 'challenges generalisation from Robbers Cave'],
        ['small sample; one troop', 'observer bias possible'],
        mtype='naturalistic observation')

K.facts('ch02-st3', F(
    terms=[('contact hypothesis', 'Allport\'s (1954) idea that intergroup contact reduces prejudice under conditions of equal status, common goals, cooperation and institutional support'),
           ('jigsaw classroom', 'Aronson\'s cooperative learning technique in which each student in a mixed group holds part of the material and the group depends on everyone'),
           ('extended contact', 'reduced prejudice resulting from knowing that an in-group member has a friend in the out-group'),
           ('recategorisation', 'creating a common in-group identity that includes former out-group members'),
           ('institutional support', 'backing from authorities, laws or social norms for intergroup contact')],
    facts=[('Pettigrew and Tropp (2006) meta-analysed how many studies of intergroup contact?', '515', ['15', '51', '5,150'],
            '94% of samples showed an inverse relationship between contact and prejudice.'),
           ('Which is NOT one of Allport\'s optimal conditions for contact?', 'Physical separation of the groups', ['Equal status', 'Common goals', 'Support of authorities'],
            'Contact needs interaction; separation is the opposite.'),
           ('Paluck (2009) found that a radio soap opera in Rwanda mainly changed listeners\':', 'Perceptions of social norms and behaviours such as willingness to express dissent', ['Personal beliefs about history', 'Income', 'Religious affiliation'],
            'The programme changed norms and behaviour more than personal beliefs.')],
    why=[('Explain why contact alone may not reduce prejudice.', 'Contact under unequal status, competition or without support can confirm stereotypes and increase anxiety (Robbers Cave: contact at meals led to food fights); Allport\'s conditions are needed.'),
         ('Explain how the jigsaw classroom reduces prejudice.', 'Each student\'s piece is necessary, creating positive interdependence and equal status; students must listen to and value each other, leading to more liking across groups.')],
    contrast=[('contact', 'superordinate goals', 'Contact refers to interaction between members of different groups; superordinate goals are shared goals that require cooperation - a specific form of contact that is especially effective.')],
    misc=[('Bringing groups together is enough to reduce prejudice.', 'Mere contact can increase conflict; it must meet Allport\'s conditions (equal status, common goals, cooperation, support).')],
    cases=[('integrated schools in Northern Ireland', 'Integrated schools in Northern Ireland educate Catholic and Protestant children together, with mixed staff and shared curricula.', 'the contact hypothesis', 'sustained, institutionally supported, equal-status contact is associated with more cross-group friendships and lower prejudice')],
    apply=[('Design an intervention to reduce prejudice between local and refugee students in a school in Vienna, using the contact hypothesis.', 'Mixed cooperative projects with shared goals (jigsaw tasks), equal roles, support from the head teacher and parents, sustained over a term, with extended-contact stories; evaluate with pre/post measures and a comparison school.', 4)],
    evaluate=[('Intergroup contact is an effective way to reduce prejudice.', ['meta-analysis of 515 studies (Pettigrew and Tropp, 2006)', 'jigsaw classroom (Aronson)', 'Paluck (2009)'],
               ['effects smaller when conditions are not met', 'positive contact may not generalise to the whole group', 'self-selection - less prejudiced people seek contact'],
               'Contact is one of the most effective interventions when Allport\'s conditions are met.')],
))
K.study('ch02-st3', 'Pettigrew and Tropp', 2006, 'a meta-analysis of intergroup contact', 'to test whether intergroup contact reduces prejudice across many studies',
        'Meta-analysis of 515 studies (713 samples, about 250,000 participants) from 38 countries examining the relationship between contact and prejudice towards many target groups.',
        'greater contact was associated with lower prejudice in 94% of samples; effects were stronger when Allport\'s conditions were met but contact helped even without them',
        'the effectiveness of contact in reducing prejudice',
        ['very large, cross-national data set', 'included experiments and longitudinal studies'],
        ['many studies correlational - self-selection', 'publication bias'],
        mtype='meta-analysis')
K.study('ch02-st3', 'Aronson and Bridgeman', 1979, 'the jigsaw classroom', 'to investigate whether cooperative jigsaw learning reduces prejudice in newly desegregated schools',
        'In Austin, Texas, fifth-grade classes used jigsaw learning in small ethnically mixed groups for about six weeks; outcomes were compared with traditional classrooms.',
        'children in jigsaw classes showed increased liking for groupmates, higher self-esteem and less prejudice; minority children\'s performance improved',
        'cooperation as a way to reduce prejudice',
        ['real classrooms - high ecological validity', 'practical, low-cost intervention'],
        ['short duration; long-term effects uncertain', 'teachers knew the aims (bias)'],
        mtype='field experiment')
K.study('ch02-st3', 'Paluck', 2009, 'a radio soap opera in post-genocide Rwanda', 'to test whether a media intervention could change prejudice, norms and behaviour after the genocide',
        'Communities across Rwanda were randomly assigned to listen for a year to a radio soap opera about reconciliation or to a control soap opera about health; attitudes, norms and behaviour were measured.',
        'the reconciliation programme changed listeners\' perceptions of social norms and behaviours (e.g. trust, empathy, willingness to express dissent and cooperate) but had little effect on personal beliefs',
        'reducing conflict by changing social norms',
        ['randomised field experiment in a real post-conflict setting'],
        ['short-term measures', 'self-report and role-play behaviour'],
        mtype='field experiment')

# ---------------------------------------------------------------------------------------------
# ch03 Human relationships: social responsibility
# ---------------------------------------------------------------------------------------------
K.facts('ch03-st1', F(
    terms=[('bystanderism', 'the phenomenon in which people fail to help a person in need when others are present'),
           ('bystander effect', 'the finding that the probability of helping decreases as the number of bystanders increases'),
           ('diffusion of responsibility', 'the reduction in each bystander\'s sense of personal responsibility when others are present'),
           ('pluralistic ignorance', 'when bystanders look to each other, see no one reacting and conclude that the situation is not an emergency'),
           ('arousal-cost-reward model', 'Piliavin et al.\'s model that bystanders are aroused by an emergency and choose the response that reduces arousal at the lowest cost'),
           ('five-step model', 'Latané and Darley\'s model of bystander intervention: notice, interpret as an emergency, take responsibility, decide how to help, act')],
    facts=[('In Darley and Latané (1968), what percentage of participants helped before the end of the seizure when they believed they were the only bystander?', '85%', ['31%', '62%', '100%'],
            'With four other bystanders only 31% helped before the end of the seizure.'),
           ('In Latané and Darley\'s (1968) smoke-filled room study, how many participants alone reported the smoke within the time limit?', '75%', ['10%', '38%', '100%'],
            'With two passive confederates only 10% reported it - pluralistic ignorance.'),
           ('Piliavin, Rodin and Piliavin (1969) found that a victim with a cane was helped spontaneously on about what proportion of trials?', '95%', ['50%', '20%', '75%'],
            'The "drunk" victim was helped on about half of trials.')],
    why=[('Explain how diffusion of responsibility can reduce helping.', 'When several bystanders are present, each feels less personally obliged to act and assumes someone else will help, so the probability that any one person helps falls (Darley and Latané, 1968).'),
         ('Explain the arousal-cost-reward model.', 'Seeing an emergency causes unpleasant arousal; bystanders weigh the costs of helping (danger, effort, disgust) and of not helping (guilt, blame) and choose the response that reduces arousal most cheaply, so a "drunk" victim is helped less (higher cost, less blame for not helping).')],
    contrast=[('diffusion of responsibility', 'pluralistic ignorance', 'Diffusion of responsibility concerns sharing the responsibility to act among bystanders; pluralistic ignorance concerns misinterpreting the situation as non-urgent because others look calm.')],
    misc=[('The more people who witness an emergency, the more likely the victim is to be helped.', 'Each individual is less likely to help as group size increases (bystander effect); in some real emergencies, though, the larger number of bystanders makes it more likely at least one person helps (Philpot et al., 2020).')],
    cases=[('a cyclist hit in a busy street', 'A cyclist falls after being clipped by a car on a busy street in Mexico City; dozens of people walk past for a minute before one person stops.', 'bystanderism', 'diffusion of responsibility and pluralistic ignorance among many passers-by delay helping; once one person helps, others often join')],
    apply=[('A university in Singapore wants students to respond to emergencies on campus. Using research on bystanderism, suggest two strategies.', 'Teach the five-step model and that others\' calm may be misleading (reduces pluralistic ignorance); train students to assign responsibility ("You, call security") and give first-aid skills to reduce perceived costs (arousal-cost-reward).', 4)],
    evaluate=[('Bystanders fail to help mainly because of the number of people present.', ['Darley and Latané (1968)', 'smoke-filled room (Latané and Darley, 1968)'],
               ['cost-reward (Piliavin et al., 1969): no diffusion on the subway', 'CCTV analysis: help occurs in about 90% of real conflicts (Philpot et al., 2020)', 'victim characteristics, culture'],
               'Group size matters, but costs, rewards, victim characteristics and culture are also crucial.')],
))
K.study('ch03-st1', 'Darley and Latané', 1968, 'the seizure experiment', 'to investigate whether the number of bystanders affects helping in an emergency',
        '72 New York University students took part in a discussion over an intercom, believing there were 1, 2 or 5 people in the group; one "participant" (a recording) appeared to have a seizure.',
        '85% of those who thought they were alone helped before the end of the seizure, compared with 31% of those who thought four others were present',
        'diffusion of responsibility in bystanderism',
        ['controlled manipulation of group size', 'realistic-seeming emergency'],
        ['deception and distress', 'student sample', 'intercom setting - no visual cues'],
        mtype='laboratory experiment', iv='perceived number of other bystanders (0, 1 or 4)', dv='percentage helping and time taken to report the seizure',
        ethics='Participants were deceived and experienced significant stress believing someone was having a seizure; they were debriefed afterwards.',
        wrong=['More bystanders increased helping', 'Nobody helped in any condition', 'Group size had no effect on helping'])
K.study('ch03-st1', 'Latané and Darley', 1968, 'the smoke-filled room', 'to investigate whether the presence of others affects reporting a possible emergency',
        'Students completed a questionnaire in a room as smoke poured in through a vent; they were alone, with two passive confederates, or in groups of three naive participants.',
        '75% of participants alone reported the smoke, compared with 10% of those with passive confederates and 38% of naive groups',
        'pluralistic ignorance in bystanderism',
        ['standardised, controlled situation'],
        ['deception', 'student sample'],
        mtype='laboratory experiment', iv='social context (alone, two passive confederates, three naive participants)', dv='whether and how quickly the smoke was reported')
K.study('ch03-st1', 'Piliavin, Rodin and Piliavin', 1969, 'helping on the New York subway', 'to investigate the effect of victim characteristics on helping in a natural setting',
        'A confederate collapsed in a New York subway carriage, appearing either ill (carrying a cane) or drunk (smelling of alcohol); observers recorded helping in about 4,450 passengers.',
        'the ill victim was helped spontaneously on 95% of trials and the drunk victim on about 50%; there was no diffusion of responsibility',
        'the arousal-cost-reward model of helping',
        ['high ecological validity; large sample'],
        ['no consent or debriefing', 'observers may have recorded inaccurately'],
        mtype='field experiment')

K.facts('ch03-st2', F(
    terms=[('prosocial behaviour', 'voluntary behaviour intended to benefit others'),
           ('altruism', 'helping another person without expecting any personal benefit, motivated by concern for their welfare'),
           ('empathy-altruism hypothesis', 'Batson\'s hypothesis that empathic concern for another person produces truly altruistic motivation to help'),
           ('egoism', 'helping that is ultimately motivated by self-interest, such as reducing one\'s own distress or gaining rewards'),
           ('negative-state relief model', 'Cialdini\'s model that people help to relieve their own sadness or distress'),
           ('kin selection', 'the evolutionary idea that helping relatives increases the survival of shared genes')],
    facts=[('In Batson et al. (1981), participants high in empathy for "Elaine" helped even when:', 'Escape was easy', ['They were paid not to help', 'Elaine was a stranger from another country', 'They were alone in the room'],
            'High-empathy participants took her place even when they could easily leave, supporting altruism.'),
           ('The negative-state relief model was proposed by:', 'Cialdini and colleagues', ['Batson and colleagues', 'Latané and Darley', 'Piliavin and colleagues'],
            'Cialdini et al. (1987) argued empathic helping may relieve the helper\'s own sadness.')],
    why=[('Explain how the empathy-altruism hypothesis explains helping.', 'Taking the perspective of a person in need produces empathic concern, which creates an altruistic motive to relieve their distress regardless of costs or ease of escape (Batson et al., 1981).'),
         ('Explain why it is difficult to prove that helping is truly altruistic.', 'Almost any helping can be reinterpreted as egoistic (relief of guilt, mood improvement, reputation), and motives cannot be observed directly, so experiments must rule out each egoistic alternative.')],
    contrast=[('altruistic helping', 'egoistic helping', 'Altruistic helping aims to benefit the other person; egoistic helping aims to benefit oneself, e.g. to reduce one\'s own distress, gain praise or avoid guilt.')],
    misc=[('All prosocial behaviour is altruistic.', 'Prosocial behaviour includes any helping, much of which may be egoistically motivated (reputation, reciprocity, mood repair).')],
    cases=[('donating after a disaster appeal', 'After seeing a TV appeal showing a child affected by floods in Pakistan, Felix in Berlin donates; he says he "couldn\'t stop thinking about her".', 'empathy versus egoism', 'empathic concern for a specific victim may cause altruistic helping, but donating may also relieve his own distress (negative-state relief)')],
    apply=[('A charity in Oslo wants to increase donations. Using research on prosocial behaviour, suggest one strategy and explain why it might work.', 'Present a single identifiable victim and encourage perspective-taking to raise empathic concern (Batson); or offer mood-repairing feedback (egoistic motives); public recognition uses reputation motives.', 3)],
    evaluate=[('People help others for selfish reasons.', ['negative-state relief (Cialdini et al., 1987)', 'reputation and reciprocity', 'kin selection'],
               ['Batson et al. (1981): helping with easy escape', 'Toi and Batson (1982)', 'helping anonymous strangers'],
               'Some helping is egoistic, but experimental evidence suggests empathic concern can produce genuinely altruistic motivation.')],
))
K.study('ch03-st2', 'Batson et al.', 1981, 'empathy and helping "Elaine"', 'to test whether empathic concern produces altruistic helping even when escape is easy',
        'Female students watched "Elaine" (a confederate) apparently receiving electric shocks; empathy was manipulated by similarity information and escape was easy or difficult. Participants were offered the chance to take her place.',
        'high-empathy participants offered to take Elaine\'s place even when escape was easy, whereas low-empathy participants helped mainly when escape was difficult',
        'the empathy-altruism hypothesis',
        ['controlled 2x2 design separating empathy and ease of escape'],
        ['deception and distress', 'female US students only', 'hypothetical-seeming situation'],
        mtype='laboratory experiment', iv='empathy (high/low) and ease of escape (easy/difficult)', dv='whether the participant offered to take Elaine\'s place',
        ethics='Participants were deceived into believing someone was being shocked and faced a distressing choice; full debriefing was essential.')
K.study('ch03-st2', 'Toi and Batson', 1982, 'empathy and helping "Carol"', 'to test whether empathy leads to helping even when not helping would carry no social cost',
        'Students listened to a radio interview with "Carol", a student who had broken both legs and was behind in a course; empathy was manipulated by instructions, and the cost of not helping was varied by whether Carol would be in their class.',
        'high-empathy participants helped regardless of whether they would see Carol in class, while low-empathy participants helped mainly when they expected to see her',
        'empathy-based altruism',
        ['manipulated both empathy and cost of not helping'],
        ['deception', 'helping measured as offers, not actual behaviour'],
        mtype='laboratory experiment')
K.study('ch03-st2', 'Cialdini et al.', 1987, 'empathy and sadness as motives for helping', 'to test whether empathic helping is explained by the desire to relieve one\'s own sadness',
        'Participants exposed to a person in need were given an opportunity to help; in some conditions they were led to believe that their mood was "fixed" by a drug (so helping could not improve it) or received a mood-lifting reward first.',
        'when participants believed helping could not improve their mood, or their mood had already been lifted, the link between empathy and helping weakened',
        'egoistic explanations of prosocial behaviour',
        ['tested a specific egoistic alternative'],
        ['later studies by Batson failed to replicate the effect', 'deception about the drug'],
        mtype='laboratory experiment')

K.facts('ch03-st3', F(
    terms=[('simpatía', 'a cultural value in Latin American and Spanish cultures emphasising friendliness, warmth and concern for others\' well-being'),
           ('prosocial modelling', 'demonstrating helping behaviour so others will imitate it'),
           ('empathy training', 'interventions that teach perspective-taking and emotional understanding to increase helping'),
           ('pace of life', 'the speed at which people in a city typically walk, work and live, linked to helping in some studies')],
    facts=[('Levine, Norenzayan and Philbrick (2001) found that the city with the highest rate of helping strangers was:', 'Rio de Janeiro', ['New York', 'Kuala Lumpur', 'Singapore'],
            'Kuala Lumpur had the lowest overall rate in their 23-city sample.'),
           ('Sprafkin, Liebert and Poulos (1975) found that children who watched an episode of "Lassie" in which a boy helped a puppy:', 'Helped more in a later situation', ['Became more aggressive', 'Helped less', 'Ignored puppies'],
            'Prosocial TV content increased helping.')],
    why=[('Explain why helping strangers may differ between cultures.', 'Cultural values (e.g. simpatía), economic conditions, population density and pace of life shape norms about helping strangers; collectivist cultures may emphasise helping in-group members more than strangers.'),
         ('Explain how prosocial behaviour can be promoted through media.', 'Through observational learning: children who see models help and be rewarded learn helping behaviours and expect positive outcomes (Sprafkin et al., 1975).')],
    contrast=[('in-group helping', 'helping strangers', 'In-group helping is directed to family, friends or group members and is strongly emphasised in collectivist cultures; helping strangers is directed to people with no relationship and varies with cultural values like simpatía.')],
    misc=[('Collectivist cultures always help strangers more than individualist cultures.', 'Levine et al. (2001) found individualism-collectivism did not predict helping strangers; collectivism emphasises in-group helping.')],
    cases=[('a "kindness week" at a school in Hanoi', 'A school runs a week of activities where older pupils model helping younger pupils, and acts of kindness are praised in assemblies.', 'promoting prosocial behaviour', 'modelling and social reinforcement increase helping through social learning and new group norms')],
    apply=[('A city council in Lisbon wants more residents to help elderly people with shopping. Using research, propose an intervention.', 'Create visible models (volunteer champions), reduce costs (easy app sign-up), emphasise community norms and identity, and recognise helpers; evaluate with before/after measures.', 4)],
    evaluate=[('Culture is the most important factor in determining whether people help strangers.', ['large cross-city differences (Levine et al., 2001)', 'simpatía in Latin cultures'],
               ['situational factors like bystanders and costs', 'economic productivity predicted helping', 'individual empathy'],
               'Culture influences helping, but situational and individual factors also play major roles.')],
))
K.study('ch03-st3', 'Levine, Norenzayan and Philbrick', 2001, 'helping strangers in 23 cities', 'to investigate cross-cultural differences in helping strangers',
        'Local experimenters in 23 large cities staged three non-emergency situations - dropping a pen, a person with a hurt leg dropping magazines, and a blind person needing help to cross the street - and recorded helping.',
        'helping varied widely; Rio de Janeiro, San José and Lilongwe were among the most helpful and Kuala Lumpur and New York among the least; cities with simpatía values and lower economic productivity helped more',
        'cultural differences in prosocial behaviour',
        ['standardised scenarios across many cultures', 'natural behaviour'],
        ['different experimenters in each city', 'cities may not represent countries', 'no consent from passers-by'],
        mtype='field experiment')
K.study('ch03-st3', 'Sprafkin, Liebert and Poulos', 1975, 'prosocial television and children\'s helping', 'to investigate whether watching prosocial television increases helping in children',
        'First-grade children watched one of three TV episodes: a "Lassie" episode in which a boy rescues a puppy, a neutral "Lassie" episode, or a family sitcom; they were then given a choice between helping distressed puppies or playing a game for points.',
        'children who watched the prosocial episode spent much longer helping the puppies than children in the other conditions',
        'promoting prosocial behaviour through modelling',
        ['controlled experiment with a behavioural DV'],
        ['short-term effect only', 'artificial task'],
        mtype='laboratory experiment')
K.R.f['ch02-st1'].cases += [
    ('scapegoating during an economic crisis', 'During a recession in a European country, unemployment rises and some politicians blame recent migrants for "taking jobs"; hate crimes increase.', 'origins of prejudice', 'frustration over economic loss is displaced onto a weaker out-group (scapegoating), and competition for scarce jobs adds realistic conflict'),
    ('a shop security guard following certain customers', 'A security guard in a Toronto mall follows young Black customers more closely than others, although theft records show no difference between groups.', 'stereotypes and discrimination', 'a stereotype (often formed through illusory correlation and media) leads to discriminatory behaviour, which can be reinforced by confirmation bias'),
    ('online hate after a terrorist attack', 'After a terrorist attack in Europe, social media posts attacking Muslims rise sharply, many from accounts that had not posted about religion before.', 'social identity and threat', 'perceived threat to the in-group increases in-group identification and hostility to an out-group seen as linked to the threat')]
K.R.f['ch02-st1'].apply += [
    ('Using social identity theory, explain why fans of rival football clubs in Buenos Aires may discriminate against each other even when no resources are at stake.', 'Fans categorise themselves as members of a club, identify with it and compare it favourably with the rival to boost self-esteem (positive distinctiveness); minimal group research shows bias needs no material competition.', 4),
    ('A researcher wants to measure implicit prejudice towards migrants in Seoul. Suggest a method and one limitation.', 'The Implicit Association Test (reaction times to pairings of group and good/bad words); limitation: test-retest reliability is modest and IAT scores predict behaviour only weakly, so it may not measure prejudice validly.', 3),
    ('Explain how the authoritarian personality explanation and the conformity explanation would predict different patterns of prejudice in a society.', 'Authoritarian personality predicts prejudice concentrated in individuals with high F-scale scores and strict upbringing; conformity predicts prejudice that varies with local norms across regions, even among people of similar personality (Pettigrew, 1958).', 4)]

# ---------------------------------------------------------------------------------------------
# ch04 Learning and cognition: theories of learning
# ---------------------------------------------------------------------------------------------
K.facts('ch04-st1', F(
    terms=[('classical conditioning', 'learning by association, in which a neutral stimulus comes to trigger a response after being paired with an unconditioned stimulus'),
           ('unconditioned stimulus (UCS)', 'a stimulus that naturally produces a response without learning'),
           ('conditioned stimulus (CS)', 'a previously neutral stimulus that triggers a conditioned response after association with the UCS'),
           ('operant conditioning', 'learning in which behaviour is shaped by its consequences (reinforcement and punishment)'),
           ('positive reinforcement', 'increasing a behaviour by adding a pleasant consequence after it'),
           ('negative reinforcement', 'increasing a behaviour by removing an unpleasant consequence after it'),
           ('extinction', 'the gradual weakening of a learned response when it is no longer reinforced (or the CS is presented without the UCS)'),
           ('token economy', 'a behaviour-modification system in which tokens are given as secondary reinforcers for target behaviours and exchanged for rewards')],
    facts=[('In Watson and Rayner\'s (1920) study, what was the unconditioned stimulus?', 'A loud noise made by striking a steel bar', ['A white rat', 'A rabbit', 'A fur coat'],
            'The loud noise naturally produced fear; the rat became the CS.'),
           ('A student hands homework in on time to stop her teacher\'s daily reminders. This is an example of:', 'Negative reinforcement', ['Positive reinforcement', 'Positive punishment', 'Extinction'],
            'Behaviour increases because an unpleasant stimulus is removed.'),
           ('Ayllon and Azrin (1968) used a token economy with:', 'Patients in a psychiatric hospital', ['Primary school children', 'Prison inmates', 'Laboratory rats'],
            'Patients earned tokens for tasks such as self-care and could exchange them for privileges.'),
           ('Which reinforcement schedule produces the behaviour most resistant to extinction?', 'Variable ratio', ['Continuous reinforcement', 'Fixed interval', 'Fixed ratio'],
            'Unpredictable reinforcement (as in gambling) keeps responding high.')],
    why=[('Explain how classical conditioning can explain a phobia.', 'A neutral stimulus (e.g. a dog) is paired with a frightening UCS (being bitten), so the dog becomes a CS that triggers fear; avoidance is then negatively reinforced because it reduces anxiety (two-process model).'),
         ('Explain how operant conditioning can be used in a classroom.', 'Teachers reinforce desired behaviour (praise, points, privileges) so it increases, use extinction by ignoring minor attention-seeking, and use schedules of reinforcement to maintain behaviour.')],
    contrast=[('classical conditioning', 'operant conditioning', 'Classical conditioning involves associating two stimuli so that a reflexive response is triggered by a new stimulus; operant conditioning involves associating a voluntary behaviour with its consequences.'),
              ('negative reinforcement', 'punishment', 'Negative reinforcement increases behaviour by removing something unpleasant; punishment decreases behaviour by adding something unpleasant or removing something pleasant.')],
    misc=[('Negative reinforcement is the same as punishment.', 'Negative reinforcement increases a behaviour by removing an unpleasant stimulus; punishment decreases a behaviour.')],
    cases=[('a learning app with streaks', 'A language app in Seoul gives users points, badges and a "streak" counter for daily practice; missing a day resets the streak.', 'operant conditioning', 'points and badges positively reinforce practice, and the threat of losing a streak uses loss aversion; variable rewards keep engagement high')],
    apply=[('A teacher in Nairobi wants to reduce shouting out in class. Using operant conditioning, design a strategy.', 'Reinforce hand-raising consistently with praise or points (positive reinforcement), ignore shouting out (extinction), and later move to intermittent reinforcement to maintain the behaviour.', 4)],
    evaluate=[('Conditioning provides a complete explanation of human learning.', ['token economies work (Ayllon and Azrin, 1968)', 'phobias via conditioning (Watson and Rayner, 1920)'],
               ['ignores cognition (latent learning, expectations)', 'observational learning without reinforcement (Bandura)', 'biological preparedness'],
               'Conditioning explains many learned behaviours, but human learning also involves cognition and social learning.')],
))
K.study('ch04-st1', 'Watson and Rayner', 1920, 'Little Albert', 'to investigate whether fear can be classically conditioned in a human infant',
        'An 11-month-old infant was presented with a white rat paired with a loud noise from a steel bar struck behind his head; after several pairings, the rat was shown alone.',
        'Albert cried and tried to crawl away when shown the rat alone; the fear generalised to similar objects such as a rabbit and a fur coat',
        'classical conditioning of emotional responses',
        ['first demonstration of conditioned fear in a human'],
        ['single participant; subjective measures', 'never deconditioned - serious ethical breach'],
        ethics='Deliberately causing fear in an infant without deconditioning breached protection from harm.')
K.study('ch04-st1', 'Skinner', 1938, 'operant conditioning in the Skinner box', 'to investigate how consequences shape voluntary behaviour',
        'Rats (and later pigeons) were placed in a box with a lever; pressing the lever delivered food (positive reinforcement) or switched off an electric current (negative reinforcement), under different schedules.',
        'reinforced behaviours increased in frequency, and partial (especially variable-ratio) schedules produced high, persistent response rates resistant to extinction',
        'operant conditioning',
        ['highly controlled and objective', 'principles applied widely (token economies, apps)'],
        ['animal research - generalisation to humans', 'ignores cognitive processes'],
        mtype='laboratory experiment')
K.study('ch04-st1', 'Ayllon and Azrin', 1968, 'a token economy in a psychiatric hospital', 'to investigate whether a token economy could increase adaptive behaviour in long-stay psychiatric patients',
        '45 female long-stay patients in an Illinois psychiatric hospital earned tokens for work tasks and self-care, exchangeable for privileges; the system was introduced, withdrawn and reintroduced.',
        'target behaviours increased sharply when tokens were given and fell when tokens were withdrawn',
        'operant conditioning applied to human behaviour',
        ['reversal (ABA) design shows the effect of reinforcement', 'practical application'],
        ['behaviour may not generalise outside the system', 'ethical concerns about withholding privileges'],
        mtype='field experiment')

K.facts('ch04-st2', F(
    terms=[('social learning theory', 'Bandura\'s theory that people learn by observing models, through attention, retention, reproduction and motivation'),
           ('model', 'a person whose behaviour is observed and may be imitated'),
           ('vicarious reinforcement', 'learning that occurs when the observer sees a model being rewarded'),
           ('self-efficacy', 'belief in one\'s ability to succeed at a specific task'),
           ('peer modelling', 'learning by observing peers of similar age and ability perform a task'),
           ('symbolic modelling', 'learning from models presented in films, books or digital media rather than in person')],
    facts=[('Schunk and Hanson (1985) found that children\'s self-efficacy for subtraction increased most after watching:', 'A peer model', ['A teacher model', 'No model', 'An older adult model'],
            'Peer models increased self-efficacy and achievement more than teacher models.'),
           ('Bandura and Menlove (1968) found that children\'s fear of dogs was reduced by:', 'Watching films of children interacting with dogs', ['Being punished for avoiding dogs', 'Reading about dog bites', 'Being forced to hold a dog'],
            'Symbolic modelling led to vicarious extinction of avoidance.')],
    why=[('Explain why peer models can be more effective than teacher models.', 'Observers who see a similar person succeed believe "if they can, I can", increasing self-efficacy and attention to the model (Schunk and Hanson, 1985).'),
         ('Explain the role of motivation in social learning.', 'A learned behaviour is performed only if the observer expects a positive outcome - from vicarious reinforcement, direct reinforcement or self-reinforcement (Bandura, 1965).')],
    contrast=[('direct reinforcement', 'vicarious reinforcement', 'Direct reinforcement is a reward given to the learner; vicarious reinforcement is seeing someone else rewarded, which motivates imitation.')],
    misc=[('Social learning theory says children copy everything they see.', 'Imitation depends on attention, retention, ability to reproduce and motivation; models that are similar, high-status or rewarded are more likely to be imitated.')],
    cases=[('worked-example videos by older students', 'A school in Kuala Lumpur records Year 12 students solving maths problems aloud, including mistakes and corrections, for Year 9 students.', 'social learning in the classroom', 'similar coping models increase self-efficacy and show the strategies to reproduce, consistent with Schunk and Hanson (1985)')],
    apply=[('A coach in Accra wants young swimmers to adopt a new technique. Using social learning theory, describe how she should demonstrate it.', 'Use a respected, similar peer as the model; ensure attention (slow motion, highlight key moves), help retention (verbal labels), allow practice (reproduction) and praise the model and learners (vicarious and direct reinforcement).', 4)],
    evaluate=[('Observational learning is the most effective way to learn in the classroom.', ['peer models increase self-efficacy (Schunk and Hanson, 1985)', 'fast acquisition of skills'],
               ['some learning needs practice and feedback (retrieval practice)', 'imitation without understanding', 'conditioning and cognitive strategies also important'],
               'Observational learning is powerful for skills and self-efficacy, but it works best combined with practice and feedback.')],
))
K.study('ch04-st2', 'Schunk and Hanson', 1985, 'peer models and self-efficacy', 'to investigate whether observing peer models increases children\'s self-efficacy and achievement in mathematics',
        '72 children with difficulties in subtraction watched videos of a peer model or a teacher model solving subtraction problems, or saw no model, before an instructional programme; self-efficacy and skill were measured.',
        'children who watched a peer model showed higher self-efficacy and achievement than those who watched a teacher model or no model',
        'observational learning and self-efficacy',
        ['controlled conditions with pre- and post-tests', 'educationally relevant task'],
        ['US sample; short term', 'video models may differ from live classroom models'],
        mtype='laboratory experiment', iv='type of model (peer, teacher, none)', dv='self-efficacy ratings and subtraction test scores')
K.study('ch04-st2', 'Bandura and Menlove', 1968, 'symbolic modelling and fear of dogs', 'to investigate whether filmed models can reduce children\'s avoidance of dogs',
        'Children who were afraid of dogs watched films of a single child or several children interacting increasingly closely with dogs, or neutral films; approach behaviour was then tested.',
        'children who watched the modelling films showed less avoidance and more approach to dogs, especially after seeing several models with several dogs',
        'social learning through symbolic modelling',
        ['behavioural test of approach', 'practical application to fear reduction'],
        ['short-term follow-up', 'children\'s fear may also reduce through familiarity'],
        mtype='laboratory experiment')
K.study('ch04-st2', 'Bandura, Ross and Ross', 1961, 'imitation of aggressive models', 'to investigate whether children imitate aggression shown by adult models',
        '72 nursery children aged 3-6 watched an adult act aggressively or non-aggressively towards a Bobo doll, or saw no model, and were then observed after mild frustration.',
        'children who saw the aggressive model imitated specific aggressive acts; boys showed more physical aggression',
        'observational learning',
        ['controlled, standardised procedure with good inter-rater reliability'],
        ['Bobo doll invites hitting; low ecological validity', 'ethics of exposing children to aggression'],
        mtype='laboratory experiment')

K.facts('ch04-st3', F(
    terms=[('zone of proximal development (ZPD)', 'the difference between what a learner can do alone and what they can achieve with guidance'),
           ('scaffolding', 'temporary, contingent support from a more knowledgeable other that is gradually withdrawn as competence increases'),
           ('more knowledgeable other (MKO)', 'anyone with greater skill or understanding than the learner, such as a teacher, parent, peer or software'),
           ('contingent support', 'help that increases when the learner struggles and decreases when the learner succeeds'),
           ('internalisation', 'Vygotsky\'s process by which social interaction and speech become internal thought'),
           ('reciprocal teaching', 'a method in which students take turns leading discussion using strategies such as questioning, summarising, clarifying and predicting')],
    facts=[('Freund (1990) found that children aged 3-5 sorted dollhouse furniture most accurately after:', 'Working with their mothers', ['Working alone', 'Watching a video', 'Being rewarded with sweets'],
            'Mothers adjusted their help to the child\'s needs within the ZPD.'),
           ('The term "scaffolding" was introduced by:', 'Wood, Bruner and Ross (1976)', ['Vygotsky (1934)', 'Piaget (1952)', 'Bandura (1977)'],
            'It describes adult support that fits the learner\'s level.')],
    why=[('Explain how scaffolding supports learning in the ZPD.', 'The MKO breaks the task into steps, demonstrates, gives hints and feedback, and withdraws help as competence grows, allowing the learner to achieve more than alone and eventually to work independently.'),
         ('Explain why Vygotsky saw language as central to learning.', 'Language is the main tool through which culture transmits knowledge; social speech becomes private speech and then inner thought (internalisation), so dialogue with others shapes thinking.')],
    contrast=[('scaffolding', 'direct instruction', 'Scaffolding is flexible, contingent support adjusted to the learner and gradually removed; direct instruction is teacher-led explanation that is not necessarily adapted moment-to-moment.')],
    misc=[('Scaffolding means doing the task for the learner.', 'Scaffolding gives just enough help for the learner to succeed and is withdrawn as they improve; doing the task for them prevents learning.')],
    cases=[('an adaptive maths tutor app', 'A maths app used in Bogotá gives a hint after one wrong answer, a worked step after two and fewer hints as accuracy improves.', 'scaffolding in the ZPD', 'the app acts as an MKO providing contingent support that is reduced as competence grows')],
    apply=[('A parent in Vienna is helping her 6-year-old build a model. Using research on scaffolding, describe what she should do.', 'Recruit interest, simplify the task, keep the child focused on the goal, highlight critical features, control frustration and demonstrate - giving more help when the child struggles and less when he succeeds (Wood, Bruner and Ross, 1976).', 4)],
    evaluate=[('Learning is most effective when it is guided by a more knowledgeable other.', ['Freund (1990)', 'Wood, Bruner and Ross (1976)', 'reciprocal teaching improves comprehension'],
               ['discovery learning develops independence', 'quality of guidance varies', 'over-scaffolding can create dependence'],
               'Guided learning within the ZPD is highly effective, provided support is contingent and gradually withdrawn.')],
))
K.study('ch04-st3', 'Freund', 1990, 'mothers\' guidance in a sorting task', 'to investigate whether children perform better with guidance from their mothers than alone',
        'Children aged 3 and 5 helped a puppet move house by sorting dollhouse furniture into rooms; some first worked with their mothers and others practised alone, then all did a harder version alone.',
        'children who had worked with their mothers improved more; mothers adjusted their help, giving more guidance to younger children and on harder tasks',
        'the zone of proximal development and guided learning',
        ['controlled comparison of guided and solo practice'],
        ['small sample', 'mothers\' styles varied'],
        mtype='laboratory experiment', iv='guided practice with mother vs practice alone', dv='accuracy of furniture sorting on the final task')
K.study('ch04-st3', 'Wood, Bruner and Ross', 1976, 'scaffolding in tutoring', 'to investigate how adults support young children in problem solving',
        'A tutor helped 30 children aged 3-5 build a pyramid from interlocking wooden blocks; tutor interventions and children\'s progress were recorded.',
        'effective tutoring was contingent - more help after failure, less after success; six scaffolding functions were identified (e.g. recruitment, reduction in degrees of freedom, demonstration)',
        'scaffolding',
        ['detailed observation of tutor-child interaction'],
        ['one tutor and one task', 'small sample'],
        mtype='controlled observation')

REINF = [
    ('A child gets a sticker every time she reads for 20 minutes, and starts reading more.', 'positive reinforcement', 'a pleasant stimulus (sticker) is added and the behaviour increases'),
    ('A driver fastens his seatbelt to stop the car\'s beeping alarm, and soon buckles up immediately.', 'negative reinforcement', 'an unpleasant stimulus (beeping) is removed and the behaviour increases'),
    ('A teenager loses phone privileges for a week after coming home late, and comes home late less often.', 'negative punishment', 'a pleasant stimulus (phone) is removed and the behaviour decreases'),
    ('A pupil is given extra chores after swearing in class, and swears less.', 'positive punishment', 'an unpleasant consequence (chores) is added and the behaviour decreases'),
    ('A student takes a painkiller for a headache; the pain goes, and she takes painkillers more readily in future.', 'negative reinforcement', 'removal of pain strengthens the behaviour'),
    ('A worker receives a bonus for every 50 items packed.', 'positive reinforcement (fixed-ratio schedule)', 'reward after a set number of responses'),
    ('A gambler wins on a slot machine after an unpredictable number of plays and keeps playing.', 'positive reinforcement (variable-ratio schedule)', 'reward after an unpredictable number of responses produces persistent behaviour'),
    ('A teacher stops responding to a pupil\'s calling out, and the calling out gradually stops.', 'extinction', 'the behaviour is no longer reinforced (attention withdrawn) and decreases'),
    ('A dog owner gives a treat every time the dog sits on command, then gradually only some of the time.', 'positive reinforcement moving from a continuous to a partial schedule', 'continuous reinforcement for acquisition, partial for maintenance'),
    ('An employee leaves early on Fridays to avoid the traffic jam, and keeps doing so.', 'negative reinforcement (avoidance)', 'avoiding an unpleasant stimulus strengthens the behaviour'),
    ('A student checks her phone repeatedly because messages arrive at unpredictable times.', 'positive reinforcement (variable-interval schedule)', 'reinforcement available after unpredictable time intervals maintains steady checking'),
    ('After a child is bitten by a dog, he becomes afraid of all dogs.', 'classical conditioning with stimulus generalisation', 'the dog (CS) was paired with pain (UCS) and fear generalises to similar stimuli'),
]


@K.add('ch04-st1', ('C2', 'C3'), (1, 4), 'short')
def reinforcement(rng, slot):
    sc, kind, why = rng.choice(REINF)
    if slot.d <= 2:
        others = sorted({k for _, k, _ in REINF if k != kind})
        rng.shuffle(others)
        return mcq(rng, f'{sc} Which learning process is shown?', kind, others[:3], why)
    return dict(stem=f'{sc} Identify the learning process involved and explain how it changes the behaviour.', answer=f'{cap(kind)}: {why}.',
                type='short', marks=3, markingKey=f'1 mark: {kind}. 2 marks: {why}, applied to the example.')

# ---------------------------------------------------------------------------------------------
# ch05 Learning and cognition: memory, metacognition and technology
# ---------------------------------------------------------------------------------------------
K.facts('ch05-st1', F(
    terms=[('retrieval practice', 'learning by actively recalling information (e.g. self-testing) rather than re-reading it'),
           ('testing effect', 'the finding that being tested on material improves long-term retention more than additional study'),
           ('spacing effect', 'the finding that study sessions spread out over time produce better long-term retention than massed sessions'),
           ('levels of processing', 'Craik and Lockhart\'s (1972) theory that memory depends on the depth of processing: structural, phonemic or semantic'),
           ('elaborative rehearsal', 'processing information by linking it to meaning and existing knowledge'),
           ('interleaving', 'mixing different types of problems or topics within a study session'),
           ('desirable difficulty', 'a learning condition that makes learning feel harder but improves long-term retention (Bjork)')],
    facts=[('In Roediger and Karpicke (2006), which condition produced the best recall after one week?', 'Study, test, test, test', ['Study, study, study, study', 'Study, study, study, test', 'Re-reading with highlighting'],
            'Repeated testing produced about 61% recall vs about 40% for repeated study.'),
           ('Craik and Tulving (1975) found the best recall for words processed:', 'Semantically (by meaning)', ['Structurally (case of letters)', 'Phonemically (by rhyme)', 'Without any question'],
            'Deep processing led to the best recognition.'),
           ('Cepeda et al. (2006) reviewed spacing research and found that spaced practice:', 'Improves long-term retention compared with massed practice', ['Is worse than cramming for all delays', 'Has no effect', 'Only helps young children'],
            'The optimal gap increases with the length of the retention interval.')],
    why=[('Explain why retrieval practice improves long-term memory.', 'Retrieving information strengthens memory traces and retrieval routes, makes later retrieval easier and reveals gaps, whereas re-reading gives an illusion of fluency (Roediger and Karpicke, 2006).'),
         ('Explain why spaced practice is more effective than cramming.', 'Spacing allows some forgetting between sessions so that each retrieval requires more effort (desirable difficulty) and is consolidated in different contexts, strengthening long-term retention.'),
         ('Explain how levels of processing theory can be applied to studying.', 'Students should process material semantically - explaining it in their own words, linking it to examples, asking "why" questions - rather than shallowly copying or reading, because deeper processing leads to more durable memories.')],
    contrast=[('massed practice', 'spaced practice', 'Massed practice concentrates study into one long session (cramming), producing good short-term but poor long-term retention; spaced practice distributes study across sessions, giving better long-term retention.'),
              ('retrieval practice', 're-reading', 'Retrieval practice requires actively recalling information without looking; re-reading is passive review that feels fluent but produces weaker long-term retention.')],
    misc=[('Re-reading notes is the most effective revision strategy because it feels easier.', 'Ease of processing creates an illusion of learning; retrieval practice and spacing feel harder but produce better long-term retention (desirable difficulties).')],
    cases=[('a revision timetable', 'Hana in Geneva plans to study biology for five hours the night before her exam; her friend Kenji plans five one-hour sessions over two weeks with self-quizzing.', 'evidence-based learning strategies', 'Kenji\'s plan uses spacing and retrieval practice, which predict much better long-term retention than Hana\'s massed re-reading'),
           ('flashcard apps', 'A medical student in Melbourne uses a flashcard app that shows each card again just before she is likely to forget it.', 'spaced retrieval practice', 'the app combines retrieval practice with expanding spacing intervals, two of the most effective strategies identified by research')],
    apply=[('A teacher in Lima has 30 minutes a week for revision. Using research, design a revision routine and justify it.', 'Short low-stakes quizzes on old and new material each week (retrieval practice and spacing), interleaved topics, feedback on answers; justify with Roediger and Karpicke (2006) and Cepeda et al. (2006).', 4)],
    evaluate=[('Retrieval practice is the most effective way to improve learning.', ['testing effect (Roediger and Karpicke, 2006)', 'replicated in classrooms', 'works across ages and subjects'],
               ['spacing and elaboration also very effective', 'stressful high-stakes tests may harm learning', 'requires some initial understanding'],
               'Retrieval practice is among the most robust strategies, especially when combined with spacing and feedback.')],
))
K.study('ch05-st1', 'Roediger and Karpicke', 2006, 'the testing effect', 'to investigate whether testing improves long-term retention of prose more than restudying',
        'Students read short prose passages and then either studied them repeatedly (SSSS), studied three times and were tested once (SSST), or studied once and were tested three times (STTT); recall was tested after 5 minutes or 1 week.',
        'after 5 minutes repeated study was slightly better, but after one week the STTT group recalled about 61% compared with about 40% for SSSS',
        'retrieval practice as a learning strategy',
        ['controlled design; educationally relevant materials', 'widely replicated'],
        ['student sample; short prose', 'participants\' predictions of their own learning were wrong - limits self-directed use'],
        mtype='laboratory experiment', iv='study condition (SSSS, SSST, STTT)', dv='percentage of idea units recalled after 5 minutes or one week',
        wrong=['Repeated study produced the best recall after one week', 'Testing reduced long-term recall', 'There was no difference after one week'])
K.study('ch05-st1', 'Craik and Tulving', 1975, 'depth of processing and recognition', 'to test whether deeper processing leads to better memory',
        'Participants answered yes/no questions about words that required structural (Is it in capitals?), phonemic (Does it rhyme with ...?) or semantic processing (Does it fit the sentence ...?), then took a surprise recognition test.',
        'recognition was highest for semantically processed words and lowest for structurally processed words',
        'levels of processing',
        ['clear, replicable effect', 'incidental learning reduces strategy use'],
        ['"depth" is defined circularly', 'semantic questions also took longer - processing time confounded'],
        mtype='laboratory experiment', iv='level of processing (structural, phonemic, semantic)', dv='percentage of words correctly recognised')
K.study('ch05-st1', 'Cepeda et al.', 2006, 'distributed practice in verbal recall', 'to review the effect of spacing between study sessions on retention',
        'A meta-analysis of 317 experiments in 184 articles on distributed practice of verbal material.',
        'spaced practice produced better retention than massed practice, and the optimal gap between sessions increased as the retention interval increased',
        'the spacing effect',
        ['very large evidence base'],
        ['mainly lab studies with verbal material', 'school-based evidence more limited'],
        mtype='meta-analysis')


@K.add('ch05-st1', 'C3', (2, 5), 'numerical')
def recall_gain(rng, slot):
    a_lbl, b_lbl = rng.choice([('retrieval practice', 're-reading'), ('spaced practice', 'massed practice'), ('semantic processing', 'structural processing'),
                               ('interleaved practice', 'blocked practice'), ('self-explanation', 'highlighting')])
    n_items = rng.choice([20, 30, 40, 50])
    a = rng.randint(int(n_items * 0.45), int(n_items * 0.8))
    b = rng.randint(int(n_items * 0.2), a - 2)
    pa, pb = 100 * a / n_items, 100 * b / n_items
    rel = 100 * (a - b) / b
    who = name(rng)
    stem = (f'In a classroom experiment in {rng.choice(CITIES)}, students who used {a_lbl} recalled a mean of {a} out of {n_items} items one week later, '
            f'while those who used {b_lbl} recalled {b}. Calculate the percentage recalled in each condition and the percentage improvement of the first condition '
            'over the second (to 1 decimal place)' + (', and explain one reason why the result might not generalise to real revision.' if slot.d >= 4 else '.'))
    ans = f'{a_lbl}: {pa:.1f}%; {b_lbl}: {pb:.1f}%; improvement = ({a} - {b})/{b} x 100 = {rel:.1f}%'
    key = f'A1 {pa:.1f}% and {pb:.1f}%. M1 ({a} - {b})/{b} x 100. A1 {rel:.1f}%.'
    if slot.d >= 4:
        key += ' R1 e.g. lab materials and a single test differ from real exams; students may not use the strategy voluntarily; sample from one school.'
    return dict(stem=stem, answer=ans, markingKey=key, type='numerical', marks=3 + (slot.d >= 4))


K.facts('ch05-st2', F(
    terms=[('metacognition', 'awareness and control of one\'s own thinking and learning processes - thinking about thinking'),
           ('metacognitive monitoring', 'judging one\'s own learning and understanding, e.g. predicting test performance'),
           ('metacognitive control', 'regulating learning based on monitoring, e.g. choosing to restudy weak topics'),
           ('growth mindset', 'Dweck\'s term for the belief that abilities can be developed through effort, strategies and help'),
           ('fixed mindset', 'the belief that abilities are innate and cannot change much'),
           ('Dunning-Kruger effect', 'the tendency for people with low competence in a domain to overestimate their ability'),
           ('intrinsic motivation to learn', 'learning for its own interest and enjoyment rather than for external rewards')],
    facts=[('Blackwell, Trzesniewski and Dweck (2007) found that students who received growth mindset training:', 'Showed improved maths grades compared with a control group whose grades declined', ['Showed lower grades', 'Became more anxious', 'Showed no change in beliefs'],
            'The intervention group\'s downward trend in maths grades was reversed.'),
           ('Kruger and Dunning (1999) found that participants scoring in the bottom quartile on tests of logic and grammar:', 'Greatly overestimated their performance', ['Underestimated their performance', 'Accurately judged their performance', 'Refused to estimate'],
            'Bottom-quartile participants estimated they were around the 60th percentile.'),
           ('Sisk et al. (2018) meta-analysed growth mindset interventions and found:', 'Very small average effects on academic achievement', ['Very large effects for all students', 'Negative effects', 'Effects only in adults'],
            'Effects were somewhat larger for low-SES and high-risk students.')],
    why=[('Explain how metacognition can improve learning.', 'Students who monitor their understanding accurately can identify what they do not know and choose effective strategies (control), such as self-testing weak topics, rather than relying on misleading feelings of fluency.'),
         ('Explain how mindset might influence motivation to learn.', 'Students with a growth mindset interpret difficulty as a chance to improve and persist with effort and new strategies, while those with a fixed mindset may see failure as a lack of ability and avoid challenge.')],
    contrast=[('a growth mindset', 'a fixed mindset', 'A growth mindset is the belief that ability can be developed through effort and strategies; a fixed mindset is the belief that ability is innate and unchangeable.'),
              ('metacognitive monitoring', 'metacognitive control', 'Monitoring is judging one\'s own learning (e.g. "I don\'t understand this yet"); control is acting on that judgement (e.g. restudying, changing strategy).')],
    misc=[('Growth mindset interventions have been shown to dramatically improve the grades of all students.', 'Large studies (Yeager et al., 2019; Sisk et al., 2018) show small average effects, mostly for lower-achieving students, and some replications show none.')],
    cases=[('a student surprised by a low mark', 'Mateo felt confident after re-reading his history notes but scored 45% on the test; he says, "I knew it all when I read it."', 'metacognition', 'fluency from re-reading created an illusion of knowing - poor monitoring; self-testing would give more accurate judgements')],
    apply=[('A teacher in Kuala Lumpur wants students to develop metacognitive skills. Suggest two classroom strategies and justify them.', 'Ask students to predict scores before quizzes and compare with results (calibrating monitoring); use exam wrappers/reflection on which strategies worked; teach self-testing; model thinking aloud.', 4)],
    evaluate=[('Changing students\' mindsets is an effective way to improve achievement.', ['Blackwell et al. (2007)', 'Yeager et al. (2019) small positive effects for lower achievers'],
               ['small average effects (Sisk et al., 2018)', 'replication concerns', 'school culture must support the message'],
               'Mindset interventions can help some students modestly, but they are not a powerful general solution.')],
))
K.study('ch05-st2', 'Blackwell, Trzesniewski and Dweck', 2007, 'implicit theories of intelligence and achievement', 'to investigate whether beliefs about intelligence predict achievement and whether a growth mindset intervention improves grades',
        'Study 1 followed 373 New York seventh-graders\' maths grades over two years; Study 2 gave 91 students an eight-session workshop on study skills, with or without lessons that the brain grows with effort (incremental theory).',
        'students with a growth mindset showed rising maths grades; in Study 2 the incremental-theory group\'s declining grades were reversed, whereas the control group\'s continued to decline',
        'the effect of mindset on motivation and achievement',
        ['longitudinal and experimental evidence combined', 'real school grades'],
        ['small intervention sample', 'teachers may not have been fully blind', 'later large studies show smaller effects'],
        mtype='field experiment')
K.study('ch05-st2', 'Yeager et al.', 2019, 'a national growth mindset experiment', 'to test whether a short online growth mindset intervention improves achievement in a nationally representative sample',
        'About 12,000 ninth-grade students in 65 US public schools were randomly assigned to two 25-minute online sessions about growth mindset or a control programme; grades and course choices were measured.',
        'the intervention slightly improved grades for lower-achieving students (about 0.10 grade points) and increased enrolment in advanced maths; effects depended on school peer norms',
        'the effectiveness of growth mindset interventions',
        ['very large, nationally representative, pre-registered RCT'],
        ['small effect sizes', 'effects varied by school context'],
        mtype='randomised controlled trial')
K.study('ch05-st2', 'Kruger and Dunning', 1999, 'overestimation of ability by the unskilled', 'to investigate whether people with low competence lack the metacognitive skill to recognise it',
        'Cornell students completed tests of humour, logical reasoning and grammar, then estimated their ability and test score relative to peers.',
        'participants in the bottom quartile greatly overestimated their performance (estimating around the 62nd percentile when they were at about the 12th)',
        'limits of metacognitive monitoring',
        ['several tasks with consistent findings'],
        ['student sample', 'part of the effect may be statistical regression to the mean'],
        mtype='laboratory experiment')

K.facts('ch05-st3', F(
    terms=[('media multitasking', 'using several media at the same time, such as texting while studying'),
           ('task switching', 'shifting attention between tasks, which carries a cost in time and accuracy'),
           ('attentional capture', 'the involuntary drawing of attention by a stimulus, such as a phone notification'),
           ('cognitive load', 'the amount of working memory resources used by a task'),
           ('brain drain hypothesis', 'Ward et al.\'s (2017) idea that the mere presence of one\'s smartphone reduces available cognitive capacity'),
           ('screen time', 'the amount of time spent using devices with screens')],
    facts=[('Ophir, Nass and Wagner (2009) found that heavy media multitaskers:', 'Were more distracted by irrelevant stimuli and slower at task switching', ['Were better at filtering distractions', 'Had better working memory', 'Were faster at task switching'],
            'Heavy multitaskers performed worse on tests of attentional control.'),
           ('Ward et al. (2017) found that available working memory capacity was lowest when participants\' phones were:', 'On the desk', ['In another room', 'In a bag', 'Switched off in another room'],
            'Even face-down and silent, the phone reduced performance.'),
           ('Sana, Weston and Cepeda (2013) found that students seated near a peer who was multitasking on a laptop:', 'Scored lower on a comprehension test', ['Scored higher', 'Were unaffected', 'Took better notes'],
            'Multitasking harmed both the user and nearby peers.')],
    why=[('Explain why multitasking reduces learning.', 'Attention and working memory have limited capacity; switching between tasks has time and accuracy costs and reduces deep processing of the main task, so less information is encoded.'),
         ('Explain how the presence of a smartphone could affect attention.', 'Phones are highly relevant, rewarding stimuli; even when silent, resisting the urge to check them uses cognitive resources, reducing capacity for the task (Ward et al., 2017).')],
    contrast=[('task switching', 'true multitasking', 'Task switching is rapidly alternating attention between tasks (what usually happens); true multitasking is performing two tasks simultaneously, possible only when one is highly automatic.')],
    misc=[('Young people are better at multitasking because they grew up with technology.', 'Research shows heavy media multitaskers are actually worse at filtering distractions and switching tasks (Ophir et al., 2009).')],
    cases=[('a school phone ban', 'A secondary school in Oslo requires students to lock phones in pouches during lessons; teachers report better concentration.', 'technology and attention', 'removing phones removes attentional capture and the "brain drain" cost, though teacher reports may be biased by expectations')],
    apply=[('Design an experiment to test whether music with lyrics affects reading comprehension. Identify the IV, DV and one control.', 'IV: music with lyrics vs silence; DV: score on a 10-question comprehension test after reading a passage; control: same passage and test, same volume, random allocation or counterbalanced repeated measures with equivalent passages.', 4)],
    evaluate=[('Digital technology harms students\' ability to learn.', ['multitasking costs (Ophir et al., 2009)', 'phone presence (Ward et al., 2017)', 'laptop multitasking harms peers (Sana et al., 2013)'],
               ['technology supports retrieval practice and access to information', 'effects small and context dependent', 'replications of brain drain mixed'],
               'Technology can harm learning when it distracts, but it can also support learning; the way it is used is decisive.')],
))
K.study('ch05-st3', 'Ophir, Nass and Wagner', 2009, 'cognitive control in media multitaskers', 'to compare the cognitive control of heavy and light media multitaskers',
        'Stanford students were classified as heavy or light media multitaskers using a questionnaire, then completed tasks measuring filtering of distractors, working memory and task switching.',
        'heavy multitaskers were more affected by irrelevant stimuli and were slower to switch tasks than light multitaskers',
        'the effects of media multitasking on attention',
        ['several standardised cognitive tasks'],
        ['quasi-experimental - multitasking not manipulated, so direction of causality unclear', 'small samples; later replications mixed'],
        mtype='quasi-experiment')
K.study('ch05-st3', 'Ward et al.', 2017, 'the "brain drain" of smartphone presence', 'to investigate whether the mere presence of one\'s smartphone reduces available cognitive capacity',
        'About 520 US university students were randomly assigned to leave their phones on the desk (face down), in a bag or pocket, or in another room, and then completed tests of working memory capacity and fluid intelligence.',
        'participants with phones in another room performed significantly better than those with phones on the desk, with the bag/pocket condition in between',
        'the effect of smartphone presence on cognition',
        ['random allocation; large sample'],
        ['student sample', 'later replications found smaller or no effects'],
        mtype='laboratory experiment', iv='phone location (desk, bag/pocket, other room)', dv='working memory capacity score (operation span task)')
K.study('ch05-st3', 'Sana, Weston and Cepeda', 2013, 'laptop multitasking in lectures', 'to investigate whether multitasking on a laptop affects the learning of users and nearby peers',
        'Canadian university students took notes on laptops during a lecture; some were instructed to complete online tasks as well; in a second experiment, note-takers sat in view of multitasking confederates or not.',
        'multitaskers scored lower on a comprehension test, and so did students who could see a multitasking peer\'s screen',
        'how technology use affects attention in learning',
        ['experimental control; realistic lecture setting'],
        ['instructed multitasking may differ from spontaneous use', 'one university'],
        mtype='laboratory experiment')

K.facts('ch05-st4', F(
    terms=[('neurodiversity', 'the view that neurological differences such as dyslexia, ADHD and autism are natural variations in human brains rather than only deficits'),
           ('dyslexia', 'a specific learning difficulty mainly affecting accurate and fluent word reading and spelling, often linked to phonological processing'),
           ('ADHD', 'attention-deficit/hyperactivity disorder: a neurodevelopmental condition characterised by persistent inattention and/or hyperactivity-impulsivity'),
           ('phonological processing', 'the ability to recognise and manipulate the sound structure of language'),
           ('reasonable adjustment', 'a change to teaching or assessment that removes barriers for neurodivergent learners, such as extra time'),
           ('stimulant medication', 'drugs such as methylphenidate that increase dopamine and noradrenaline activity and are used to treat ADHD')],
    facts=[('Shaywitz et al. (1998) found that dyslexic readers showed under-activation in which region during phonological tasks?', 'Left posterior (temporo-parietal) regions', ['The occipital pole only', 'The cerebellum only', 'The right frontal lobe'],
            'They showed relative over-activation in the left inferior frontal gyrus.'),
           ('The MTA Cooperative Group (1999) study of 579 children with ADHD found that at 14 months, the most effective treatments for core symptoms were:', 'Carefully managed medication, alone or combined with behavioural treatment', ['Behavioural treatment alone', 'Community care alone', 'Dietary change'],
            'Combined treatment had some added benefits for related outcomes.'),
           ('Temple et al. (2003) found that after an intensive training programme, children with dyslexia showed:', 'Increased activity in left temporo-parietal areas and improved reading', ['No change in brain activity', 'Decreased reading ability', 'Activity only in the right hemisphere'],
            'Remediation partly normalised brain activity.')],
    why=[('Explain how dyslexia can be understood from biological and cognitive levels.', 'Biologically, dyslexia is linked to differences in left-hemisphere reading networks (Shaywitz et al., 1998) and is heritable; cognitively, it involves weak phonological processing, making it hard to map letters to sounds.'),
         ('Explain why the neurodiversity perspective matters for education.', 'It shifts focus from "fixing deficits" to removing barriers and using strengths, reducing stigma and supporting adjustments such as assistive technology and flexible assessment.')],
    contrast=[('a medical model of ADHD', 'a neurodiversity perspective on ADHD', 'The medical model treats ADHD as a disorder with symptoms to treat (e.g. stimulant medication); the neurodiversity perspective sees it as a natural variation, emphasising strengths, accommodation and environment.')],
    misc=[('Dyslexia is caused by low intelligence.', 'Dyslexia is a specific difficulty with word reading and phonological processing that occurs across the full range of intelligence.')],
    cases=[('a student with ADHD in an exam hall', 'Leila, 16, in Dubai, has ADHD and struggles to stay focused during long exams in a large hall; she does much better in a smaller room with breaks.', 'neurodiversity and learning', 'reasonable adjustments to the environment reduce barriers related to attention regulation, showing the role of context as well as biology')],
    apply=[('A school in Cape Town wants to support students with dyslexia. Using research, recommend two strategies.', 'Early, systematic phonics-based intervention, which can change brain activity (Temple et al., 2003); assistive technology (text-to-speech), extra time and multi-sensory teaching; avoid stigma with a strengths-based approach.', 4)],
    evaluate=[('Neurodevelopmental differences such as ADHD are best understood as biological disorders.', ['brain imaging differences (Shaywitz et al., 1998)', 'heritability and medication effects (MTA, 1999)'],
               ['diagnosis rates vary across cultures and time', 'environmental and social factors affect outcomes', 'neurodiversity perspective emphasises strengths'],
               'Biological factors are important, but outcomes depend heavily on environment and support; a biopsychosocial view is most useful.')],
))
K.study('ch05-st4', 'Shaywitz et al.', 1998, 'brain activity in dyslexic readers', 'to investigate differences in brain activity between dyslexic and non-impaired readers during reading tasks',
        '29 dyslexic and 32 non-impaired adult readers performed tasks with increasing phonological demands during fMRI.',
        'dyslexic readers showed under-activation in posterior left-hemisphere regions (including Wernicke\'s area and the angular gyrus) and relative over-activation in the left inferior frontal gyrus',
        'the neural basis of dyslexia',
        ['fMRI with graded tasks', 'clear group differences'],
        ['correlational - differences may result from less reading experience', 'adult sample'],
        mtype='quasi-experiment')
K.study('ch05-st4', 'MTA Cooperative Group', 1999, 'treatment strategies for ADHD', 'to compare the long-term effectiveness of medication, behavioural treatment, their combination and community care for ADHD',
        '579 children aged 7-9 with ADHD were randomly assigned to 14 months of medication management, intensive behavioural treatment, combined treatment or standard community care at six sites.',
        'carefully managed medication and combined treatment reduced core ADHD symptoms more than behavioural treatment or community care; combined treatment had added benefits for some outcomes',
        'treatment of ADHD',
        ['large multi-site randomised trial'],
        ['benefits of medication diminished in later follow-ups', 'mostly US sample'],
        mtype='randomised controlled trial')
K.study('ch05-st4', 'Temple et al.', 2003, 'reading remediation and brain activity', 'to investigate whether intensive reading training changes brain activity in children with dyslexia',
        '20 children with dyslexia aged 8-12 were scanned with fMRI before and after about eight weeks of computer-based training in auditory and language processing; 12 typical readers were also scanned.',
        'after training, children with dyslexia improved in reading and showed increased activity in left temporo-parietal regions, becoming more like typical readers',
        'neuroplasticity and support for neurodivergent learners',
        ['pre-post imaging with a typical-reader comparison'],
        ['no dyslexic control group without training', 'small sample'],
        mtype='quasi-experiment')

# ---------------------------------------------------------------------------------------------
# ch06 Class practical 3: conducting a survey
# ---------------------------------------------------------------------------------------------
BAD_ITEMS = [
    ('"Don\'t you agree that social media is harmful to teenagers?"', 'leading question', 'it suggests the expected answer', '"How, if at all, does social media affect you? (very negatively ... very positively)"'),
    ('"How often do you exercise and eat healthily?"', 'double-barrelled question', 'it asks about two behaviours at once, so one answer cannot represent both', 'Split into two items: "How many days a week do you exercise?" and "How many portions of fruit and vegetables do you eat a day?"'),
    ('"Do you study a lot?" (Yes/No)', 'ambiguous wording', '"a lot" means different things to different people', '"On a typical school day, how many hours do you study outside lessons? (0, <1, 1-2, 2-3, >3)"'),
    ('"Do you not think that teachers should not give homework at weekends?"', 'double negative', 'the wording is confusing and responses are unreliable', '"Teachers should give homework at weekends. (strongly disagree ... strongly agree)"'),
    ('"How much do you suffer from the stress caused by your terrible exam timetable?"', 'loaded (emotive) language', '"suffer" and "terrible" bias responses', '"How stressful do you find your exam timetable? (1 = not at all, 5 = extremely)"'),
    ('"Rate your satisfaction with school: Excellent / Very good / Good / Fair"', 'unbalanced response scale', 'there are three positive and no clearly negative options', 'Use a balanced scale: very dissatisfied, dissatisfied, neutral, satisfied, very satisfied'),
    ('"How many times have you cheated in a test?"', 'sensitive question prone to social desirability bias', 'respondents may under-report socially undesirable behaviour', 'Guarantee anonymity, use an online anonymous format and indirect wording ("How common do you think cheating is among students in your year?")'),
    ('"What is your opinion of the school\'s CAS policy and the new timetable?"', 'double-barrelled open question', 'two different topics are combined', 'Ask separately about the CAS policy and the timetable'),
    ('"Most successful people sleep 8 hours. How many hours do you sleep?"', 'leading preamble (social desirability)', 'the preamble signals the "right" answer', 'Remove the preamble: "On a school night, how many hours do you usually sleep?"'),
    ('"Do you use your phone in bed? Always / Sometimes"', 'incomplete response options', 'there is no option for "never" or "rarely"', '"How often do you use your phone in bed? Never / Rarely / Sometimes / Often / Always"'),
]


@K.add('ch06-st1', ('C2', 'C3'), (1, 5), 'short')
def bad_item(rng, slot):
    item, flaw, why, fix = rng.choice(BAD_ITEMS)
    if slot.d <= 2 and rng.random() < 0.6:
        others = list({f for _, f, _, _ in BAD_ITEMS if f != flaw})
        rng.shuffle(others)
        return mcq(rng, f'A student\'s questionnaire includes the item {item} What is the main problem with this item?', flaw, others[:3], f'It is a {flaw}: {why}.')
    return dict(stem=f'A questionnaire on student well-being in {rng.choice(CITIES)} includes the item {item} Identify the problem with this item and rewrite it to improve it.',
                answer=f'Problem: {flaw} - {why}. Improved: {fix}.', type='short', marks=3,
                markingKey=f'1 mark: problem identified ({flaw}). 1 mark: why it biases or confuses responses ({why}). 1 mark: an improved item that removes the problem, e.g. {fix}.')


K.facts('ch06-st1', F(
    terms=[('questionnaire', 'a set of written questions used to collect self-report data from many people'),
           ('closed question', 'a question with a fixed set of response options, producing quantitative data'),
           ('open question', 'a question that allows respondents to answer in their own words, producing qualitative data'),
           ('Likert scale', 'a rating scale on which respondents indicate their level of agreement with statements, usually from 1 to 5 or 1 to 7'),
           ('pilot test', 'a trial of the questionnaire on a small sample to identify unclear or problematic items before the main survey'),
           ('reverse-scored item', 'an item worded in the opposite direction, whose score is reversed before totalling, to reduce acquiescence bias'),
           ('double-barrelled question', 'a question that asks about two things at once'),
           ('leading question', 'a question worded so that it suggests a particular answer')],
    facts=[('Which of the following is a closed question?', '"How many hours did you sleep last night? (0-4, 5-6, 7-8, 9+)"', ['"Describe how you feel before exams."', '"What does friendship mean to you?"', '"Tell me about your best holiday."'],
            'Fixed options produce quantitative data.'),
           ('The main purpose of a pilot test of a questionnaire is to:', 'Find unclear or problematic items and check timing before the main study', ['Increase the sample size', 'Replace the need for informed consent', 'Make the results significant'],
            'A pilot improves validity and reliability of the final instrument.'),
           ('Who developed the attitude scale that bears his name in 1932?', 'Rensis Likert', ['Hans Eysenck', 'Charles Spearman', 'Gordon Allport'],
            'Likert scales measure degree of agreement with statements.')],
    why=[('Explain why questionnaires often include both open and closed questions.', 'Closed questions give quantitative data that are easy to analyse and compare across many respondents; open questions give rich qualitative data that explain the reasons behind answers - together they increase validity (method triangulation within one instrument).'),
         ('Explain why a questionnaire should be pilot tested.', 'A pilot reveals ambiguous, leading or double-barrelled items, unsuitable response options, ceiling effects and timing problems, so the final questionnaire is more valid and reliable.'),
         ('Explain why reverse-scored items are included in a Likert questionnaire.', 'They prevent respondents from agreeing with everything (acquiescence bias) and identify inattentive responding, because a consistent respondent must disagree with reverse-worded items.')],
    contrast=[('open questions', 'closed questions', 'Open questions let respondents answer freely, giving rich qualitative data that are hard to compare; closed questions offer fixed options, giving quantitative data that are easy to analyse but may force answers.')],
    misc=[('A longer questionnaire always produces more valid data.', 'Long questionnaires cause fatigue and careless responding; validity depends on well-designed items that measure the construct, not length.')],
    cases=[('a school well-being survey', 'A school in Singapore surveys 600 students using 20 Likert items on stress plus one open question: "What would most improve your well-being at school?"', 'questionnaire design', 'Likert items give comparable quantitative data on stress; the open question captures unexpected issues in students\' own words')],
    apply=[('Write two Likert-scale items to measure attitudes to homework, one of which is reverse-scored, and explain how they would be scored.', 'E.g. "Homework helps me understand lessons" (1 = strongly disagree ... 5 = strongly agree) and "Homework is a waste of my time" (reverse-scored: 5 becomes 1). Scores are summed so that higher totals mean a more positive attitude.', 3)],
    evaluate=[('Questionnaires are a valid way to measure attitudes.', ['standardised, large samples, quick to analyse', 'validated scales (e.g. PSS) show good reliability'],
               ['social desirability and acquiescence bias', 'self-report may not match behaviour', 'translation and cultural meaning of items'],
               'Questionnaires can measure attitudes validly if items are carefully designed, piloted and validated, but they should be triangulated with other measures.')],
))
methods(K, 'ch06-st1', 'pct')
K.add('ch06-st1', 'C3', (2, 4), 'numerical')(likert)

K.facts('ch06-st2', F(
    terms=[('response bias', 'any systematic tendency to answer questions inaccurately or in a particular way'),
           ('social desirability bias', 'the tendency to answer in a way that will be viewed favourably by others'),
           ('acquiescence bias', 'the tendency to agree with statements regardless of their content ("yea-saying")'),
           ('non-response bias', 'bias that occurs when people who do not respond differ systematically from those who do'),
           ('response rate', 'the percentage of people invited to complete a survey who actually do so'),
           ('central tendency bias', 'the tendency to avoid extreme response options and choose the middle of a scale'),
           ('sampling frame', 'the list from which a sample is drawn, such as a school register')],
    facts=[('Adorno et al.\'s (1950) F-scale was criticised because all items were worded in the same direction, which made it vulnerable to:', 'Acquiescence bias', ['Social desirability bias', 'Non-response bias', 'Observer bias'],
            'People who tend to agree would score high regardless of their real attitudes.'),
           ('Which strategy best reduces social desirability bias in a survey about drug use?', 'Anonymous online responses', ['Face-to-face interviews with teachers', 'Asking students to write their names', 'Using only open questions'],
            'Anonymity reduces the pressure to present oneself favourably.'),
           ('An online survey link is posted on a gaming forum. Which sampling technique is this, and which bias is most likely?', 'Self-selected sampling with volunteer bias', ['Random sampling with no bias', 'Stratified sampling with acquiescence bias', 'Quota sampling with observer bias'],
            'Only interested forum users respond.')],
    why=[('Explain why social desirability bias is a problem in surveys.', 'Respondents may over-report desirable behaviour (exercise, studying) and under-report undesirable behaviour (cheating, prejudice), so the data do not reflect reality and conclusions are invalid.'),
         ('Explain why a high response rate does not guarantee an unbiased sample.', 'If the sampling frame itself is unrepresentative (e.g. only students in one school), or particular groups still fail to respond, the respondents may still differ from the target population.')],
    contrast=[('social desirability bias', 'acquiescence bias', 'Social desirability bias is answering to look good; acquiescence bias is a tendency to agree with statements regardless of content.')],
    misc=[('Online surveys remove all sampling bias because anyone can take part.', 'Online surveys exclude people without internet access and attract self-selected volunteers, which can create serious sampling bias.')],
    cases=[('a survey on academic honesty', 'A school in Toronto asks students to report how often they cheat, using a paper questionnaire with their names on it, collected by their homeroom teacher.', 'response bias in surveys', 'named responses collected by a teacher create strong social desirability bias, so cheating is likely to be under-reported; anonymous online collection would help')],
    apply=[('A researcher in Hanoi wants a representative sample of 15-year-olds for a survey on sleep. Suggest a sampling method and two ways of reducing response bias.', 'Stratified random sampling from school registers across districts and school types; anonymous responses, neutral wording, balanced and reverse-scored items, short questionnaire.', 4)],
    evaluate=[('Survey data are too affected by bias to be useful.', ['social desirability, acquiescence', 'non-response and volunteer bias'],
               ['anonymity and careful design reduce bias', 'large samples give useful patterns', 'validated scales show good reliability and validity'],
               'Surveys are always vulnerable to bias, but careful design and sampling make them useful, especially when triangulated.')],
))
K.add('ch06-st2', 'C3', (1, 4), 'numerical')(response_rate)
methods(K, 'ch06-st2', 'pct')

K.facts('ch06-st3', F(
    terms=[('frequency table', 'a table showing the number of responses in each category'),
           ('bar chart', 'a graph that shows frequencies or means for separate categories, with gaps between bars'),
           ('modal response', 'the response option chosen most often'),
           ('correlation coefficient', 'a number between -1 and +1 indicating the direction and strength of a relationship between two variables'),
           ('scattergram', 'a graph that plots pairs of scores to show a possible correlation'),
           ('Spearman\'s rho', 'a non-parametric correlation coefficient calculated from ranks, used with ordinal data or non-normal interval data')],
    facts=[('Which measure of central tendency is usually most appropriate for responses to a single Likert item?', 'The median or mode', ['The mean only', 'The range', 'The standard deviation'],
            'Single Likert items are ordinal.'),
           ('Which graph is most suitable for showing the relationship between hours of sleep and mood ratings?', 'A scattergram', ['A bar chart', 'A pie chart', 'A histogram of one variable'],
            'Scattergrams display paired co-variables.')],
    why=[('Explain why a correlation between two survey variables cannot show causation.', 'Neither variable is manipulated, so a third variable may explain both and the direction of influence is unknown; survey data are also self-reported.'),
         ('Explain why percentages are often more useful than raw frequencies in survey results.', 'Percentages allow comparison between groups of different sizes (e.g. 30 boys vs 70 girls) and show the proportion of respondents, which is easier to interpret.')],
    contrast=[('a bar chart', 'a scattergram', 'A bar chart shows frequencies or means for separate categories; a scattergram shows the relationship between two continuous variables measured for each participant.')],
    misc=[('If a survey shows a correlation of 0.6 between screen time and anxiety, screen time must cause anxiety.', 'Correlation shows association only; anxious people may use screens more, or a third variable may affect both.')],
    cases=[('a survey on study habits', 'A student survey in Accra finds that 62% of respondents study with music, and those who do report slightly lower concentration ratings.', 'analysing survey data', 'the percentage summarises a frequency; the comparison of ratings is correlational and self-reported, so causal conclusions about music are not justified')],
    apply=[('Survey results: 48 students rated "I feel prepared for exams" as strongly disagree 6, disagree 10, neutral 14, agree 12, strongly agree 6. Identify the modal and median response and suggest an appropriate graph.', 'Modal response: neutral (14). Median: the 24th and 25th responses are both "neutral" (cumulative 6, 16, 30), so median = neutral. Graph: bar chart of frequencies.', 3)],
    evaluate=[('Descriptive statistics are sufficient for analysing survey data.', ['summarise large data sets clearly', 'percentages and modes suit categorical data'],
               ['cannot show whether relationships are significant', 'correlation needs inferential testing', 'open responses need qualitative analysis'],
               'Descriptive statistics are the starting point, but inferential tests and qualitative analysis are needed for full conclusions.')],
))
methods(K, 'ch06-st3', 'pct', 'spearman', 'r')

# ---------------------------------------------------------------------------------------------
# ch07 Class practical 4: conducting an interview
# ---------------------------------------------------------------------------------------------
K.facts('ch07-st1', F(
    terms=[('structured interview', 'an interview using fixed questions in a fixed order for every participant'),
           ('semi-structured interview', 'an interview with an interview schedule of key questions or topics, but flexibility to probe and follow up'),
           ('unstructured interview', 'an interview with no fixed questions that develops like a conversation around a topic'),
           ('interview schedule', 'the list of questions or topics prepared for an interview'),
           ('probe', 'a follow-up question used to obtain more detail or clarification'),
           ('rapport', 'a relationship of trust and comfort between interviewer and interviewee'),
           ('interviewer effect', 'the influence of the interviewer\'s characteristics or behaviour on the interviewee\'s answers')],
    facts=[('Which type of interview gives the most comparable data between participants?', 'Structured', ['Unstructured', 'Semi-structured', 'Focus group'],
            'Fixed questions in a fixed order make answers easy to compare.'),
           ('Which type of interview is most suitable for exploring a sensitive experience in depth while covering key topics?', 'Semi-structured', ['Structured', 'Telephone survey', 'Closed questionnaire'],
            'It balances comparability with flexibility.')],
    why=[('Explain why rapport is important in interviews.', 'When interviewees trust the interviewer, they are more willing to share honest, detailed and sensitive information, increasing the credibility of the data.'),
         ('Explain why interviewer effects can reduce the credibility of interview data.', 'The interviewer\'s age, gender, ethnicity, status or reactions can lead interviewees to give socially desirable answers or to say what they think is expected.')],
    contrast=[('a semi-structured interview', 'an unstructured interview', 'A semi-structured interview follows an interview schedule but allows probes; an unstructured interview has no fixed schedule and is led more by the interviewee.')],
    misc=[('Unstructured interviews are unscientific because each one is different.', 'Unstructured interviews aim for depth and meaning, not comparability; their rigour comes from reflexivity, careful analysis and credibility checks.')],
    cases=[('interviewing young carers', 'A researcher in London interviews 12-15-year-olds who care for a parent with a disability, using a schedule of five topics with follow-up probes.', 'semi-structured interviews', 'the schedule ensures key topics are covered while probes allow each young carer to describe their own experience in depth')],
    apply=[('Write three questions for a semi-structured interview schedule on adolescents\' experiences of moving to a new country, including one probe.', 'E.g. "Can you tell me about your first weeks at your new school?" "What has helped you feel at home?" "What has been most difficult?" Probe: "Can you give me an example of that?"', 3)],
    evaluate=[('Semi-structured interviews are the best type of interview for psychological research.', ['balance between comparability and depth', 'allow probing of meanings'],
               ['structured interviews better for comparison and reliability', 'unstructured interviews allow more participant-led data', 'interviewer effects and time-consuming analysis'],
               'Semi-structured interviews are often the best compromise, but the choice depends on the research question.')],
))
K.facts('ch07-st2', F(
    terms=[('inductive content analysis', 'a qualitative analysis in which categories are derived from the data rather than decided in advance'),
           ('thematic analysis', 'a method for identifying, analysing and reporting patterns (themes) in qualitative data (Braun and Clarke, 2006)'),
           ('code', 'a short label attached to a segment of data that captures its meaning'),
           ('theme', 'a pattern of shared meaning across the data, built from related codes'),
           ('transcript', 'a written, word-for-word record of an interview'),
           ('verbatim transcription', 'transcribing exactly what was said, including pauses and repetitions'),
           ('deductive analysis', 'analysis in which data are coded using categories based on existing theory')],
    facts=[('In Braun and Clarke\'s (2006) thematic analysis, what is the first phase?', 'Familiarising yourself with the data', ['Producing the report', 'Defining and naming themes', 'Generating a hypothesis'],
            'The six phases: familiarisation, initial codes, searching for themes, reviewing themes, defining and naming, writing up.'),
           ('In inductive analysis, categories are:', 'Developed from the data', ['Chosen before reading the data', 'Taken from a published questionnaire', 'Calculated statistically'],
            'Deductive analysis applies pre-existing categories.')],
    why=[('Explain why inductive analysis is useful in interview research.', 'It allows themes to emerge from participants\' own words rather than imposing the researcher\'s categories, so unexpected issues can be found and the findings reflect participants\' perspectives.'),
         ('Explain why two researchers might code the same transcript independently.', 'Comparing codes (researcher triangulation) checks whether interpretations are consistent, reduces individual bias and increases credibility.')],
    contrast=[('a code', 'a theme', 'A code labels a single meaningful segment of data (e.g. "fear of failure"); a theme is a broader pattern that groups related codes across the data (e.g. "pressure to perform").'),
              ('inductive analysis', 'deductive analysis', 'Inductive analysis develops categories from the data; deductive analysis applies categories derived from existing theory.')],
    misc=[('A theme is just a topic that appears often in the data.', 'A theme captures a pattern of meaning relevant to the research question; frequency alone does not make something a theme.')],
    cases=[('a transcript about exam stress', 'Interviewee: "My parents never say it, but I know they expect top grades... I study until 2 a.m. and then I can\'t sleep... my friends are the only ones who get it."', 'thematic analysis', 'codes such as "implicit parental expectations", "late-night studying", "sleep problems" and "peer support" could be grouped into themes like "pressure" and "coping through peers"')],
    apply=[('Read this extract and identify two initial codes: "When I moved to Toronto I stopped speaking up in class... in Seoul you wait until the teacher asks you... now I feel stupid when others just talk."', 'Codes: "cultural norms about classroom participation" (waiting to be asked); "loss of confidence/self-esteem" ("feel stupid"); possibly "comparison with peers".', 3),
           ('Describe the steps a student should take to turn interview transcripts into themes.', 'Transcribe verbatim; read and re-read; generate initial codes line by line; collate codes into candidate themes; review themes against the data; define and name themes; select illustrative quotes; ideally a second coder checks.', 4)],
    evaluate=[('Thematic analysis produces subjective findings.', ['researcher interprets data', 'different researchers may find different themes'],
               ['systematic phases (Braun and Clarke, 2006)', 'credibility checks (member checking, triangulation)', 'reflexivity makes interpretation transparent'],
               'Thematic analysis is interpretive, but systematic procedures and credibility checks make findings trustworthy.')],
))

TRANSCRIPTS = [
    ('"I check my phone the second I wake up. If I have no messages I feel kind of invisible... but when I leave it in the kitchen I actually read more."',
     ['need for social validation', 'habitual phone checking', 'benefits of phone separation'], 'technology and self-worth'),
    ('"At home we speak Arabic and I\'m the translator for my mum at the doctor. At school nobody knows that. Sometimes I\'m tired in class because of it."',
     ['language brokering for family', 'hidden responsibilities', 'fatigue affecting school'], 'acculturation and family roles'),
    ('"My coach shouts when we lose, so I play safe. With the new coach who says mistakes are part of learning, I try harder moves."',
     ['fear of punishment', 'risk avoidance', 'growth-oriented feedback encourages effort'], 'motivation and mindset'),
    ('"When I saw the man fall on the train, everyone looked at each other. I thought maybe he was drunk, so I waited. Then one woman went and we all helped."',
     ['ambiguity of the situation', 'looking to others (pluralistic ignorance)', 'one helper triggers others'], 'bystander behaviour'),
    ('"After my grandmother died I couldn\'t concentrate. My teacher let me hand in work late, and my friends walked home with me every day."',
     ['grief affecting concentration', 'flexible support from school', 'peer social support'], 'stress and social support'),
    ('"In my old school in Lagos the teacher explained, then we copied. Here they ask our opinion all the time. At first I hated it, now I like debating."',
     ['contrasting teaching styles', 'initial discomfort with new norms', 'adaptation over time'], 'culture and learning'),
]


@K.add('ch07-st2', ('C3', 'C4'), (2, 5), 'case')
def transcript(rng, slot):
    text, codes, theme = rng.choice(TRANSCRIPTS)
    if slot.d <= 3:
        return dict(stem=f'Read the interview extract.\n\n{text}\n\nIdentify three initial codes from this extract using inductive analysis.',
                    answer='Possible codes: ' + '; '.join(codes) + '.', type='case', marks=3, gap='G7',
                    markingKey='1 mark for each relevant code grounded in the extract (accept equivalent labels): ' + '; '.join(codes) + '. Codes that are not supported by the text score 0.')
    return dict(stem=f'Read the interview extract.\n\n{text}\n\nIdentify a possible theme related to {theme}, support it with evidence from the extract, and explain one way the researcher could check the credibility of this interpretation.',
                answer=f'Theme related to {theme}, built from codes such as ' + '; '.join(codes) + '. Credibility: member checking or a second coder (researcher triangulation).',
                type='case', marks=5, gap='G7',
                markingKey=f'1 mark theme; 2 marks supporting quotations/codes ({"; ".join(codes)}); 2 marks credibility check explained (member checking, researcher triangulation, reflexivity, audit trail).')


K.facts('ch07-st3', F(
    terms=[('credibility', 'the extent to which qualitative findings accurately represent participants\' experiences'),
           ('transferability', 'the extent to which qualitative findings can be applied to other contexts, judged using thick description'),
           ('thick description', 'a detailed description of the context, participants and process of a study that allows readers to judge transferability'),
           ('member checking', 'asking participants to confirm whether the researcher\'s interpretation of their data is accurate'),
           ('audit trail', 'a transparent record of decisions made during data collection and analysis'),
           ('dependability', 'the qualitative equivalent of reliability: the extent to which the research process is consistent and documented')],
    facts=[('Which technique is used to increase the credibility of interview findings by returning interpretations to the participants?', 'Member checking', ['Counterbalancing', 'Random sampling', 'Standardisation'],
            'Participants confirm or correct interpretations.'),
           ('Which ethical issue is particularly important when quoting interviewees in a report?', 'Confidentiality - quotations must not identify participants', ['Counterbalancing', 'Random allocation', 'Inter-rater reliability'],
            'Use pseudonyms and remove identifying details.')],
    why=[('Explain why transferability rather than generalisability is used to judge interview research.', 'Interview studies use small, purposive samples to explore meaning in depth, so statistical generalisation is not appropriate; instead, thick description allows readers to judge whether findings may transfer to similar contexts.'),
         ('Explain why interviews raise particular ethical concerns.', 'They often involve personal, sensitive topics, recordings and identifiable quotations, so informed consent, confidentiality, the right to withdraw (including data) and protection from distress are crucial.')],
    contrast=[('credibility', 'transferability', 'Credibility concerns whether findings accurately represent the participants\' experiences; transferability concerns whether they can apply to other settings.')],
    misc=[('Interview findings cannot be useful because the samples are small.', 'Small purposive samples are appropriate for depth; findings can be credible and transferable to similar contexts, and can generate hypotheses for larger studies.')],
    cases=[('a recorded interview about bullying', 'A student in Melbourne records an interview with a younger student about being bullied; the interviewee becomes upset halfway through.', 'ethics in interview research', 'the interviewer should pause or stop, remind the interviewee of the right to withdraw, offer support and debrief, and later store the recording securely and anonymise quotations')],
    apply=[('A student interviewed one classmate about exam anxiety. Suggest two ways she could increase the credibility of her findings and one way she could support transferability.', 'Credibility: member checking, a second coder, reflexive notes on her relationship with the classmate. Transferability: thick description of the participant, school context and timing.', 4)],
    evaluate=[('Interview research can be as credible as experimental research.', ['credibility checks and triangulation', 'rich, valid data about meaning'],
               ['researcher bias and interviewer effects', 'small samples', 'no causal conclusions'],
               'Interviews can be highly credible for questions about experience and meaning, although they cannot answer causal questions.')],
))
K.facts('ch07-st4', F(
    terms=[('method triangulation', 'using different methods (e.g. experiment and interview) to study the same question'),
           ('quantitative research', 'research that collects numerical data to test hypotheses and measure relationships'),
           ('qualitative research', 'research that collects non-numerical data to explore meanings and experiences'),
           ('mixed methods', 'research that combines quantitative and qualitative methods in one study'),
           ('unseen study', 'a study described in an exam that students must evaluate using research-methods knowledge')],
    facts=[('Which of the four class practicals is best for establishing cause and effect?', 'The experiment', ['The observation', 'The survey', 'The interview'],
            'Only the experiment manipulates an IV with controls.'),
           ('Which practical is best for understanding how participants make sense of their experiences?', 'The interview', ['The experiment', 'The structured observation', 'The closed questionnaire'],
            'Interviews capture meaning in participants\' own words.')],
    why=[('Explain why combining an experiment with interviews could strengthen a study.', 'The experiment shows whether the IV causes a change in the DV; interviews explain how participants experienced the conditions and why, revealing mechanisms and demand characteristics.'),
         ('Explain why observations and surveys may give different results about the same behaviour.', 'Surveys measure what people say they do (subject to social desirability and memory errors); observations record what people actually do, so the two can diverge.')],
    contrast=[('the survey practical', 'the observation practical', 'A survey gathers self-reported attitudes or behaviour from many people quickly; an observation records actual behaviour directly but takes longer and cannot access thoughts.'),
              ('the experiment practical', 'the interview practical', 'The experiment manipulates an IV to test causal hypotheses with quantitative data; the interview explores meanings and experiences with qualitative data.')],
    misc=[('Quantitative methods are always more scientific than qualitative methods.', 'Both can be rigorous; the appropriate method depends on the research question, and qualitative research has its own standards (credibility, transferability, reflexivity).')],
    cases=[('a study of phone use in class', 'Researchers in Seoul surveyed 400 students about phone use in lessons, observed 20 lessons and interviewed 10 students; students reported less use than was observed.', 'comparing methods', 'triangulation reveals social desirability bias in the survey; observation gives behavioural data and interviews explain motives')],
    apply=[('A researcher wants to study whether a mindfulness programme reduces stress in students. Explain how two different class-practical methods could be combined.', 'Experiment (randomly allocate to programme or waiting list; measure PSS scores) plus semi-structured interviews with participants about how they used the techniques - giving causal evidence and insight into mechanisms.', 4)],
    evaluate=[('No single research method can fully explain behaviour.', ['each method has limitations (causality vs ecological validity vs meaning)', 'triangulation increases credibility'],
               ['some questions are best answered by one method', 'mixed methods are costly and complex'],
               'Combining methods usually gives a fuller explanation, although a single well-chosen method can answer a focused question.')],
))
scenarios(K, 'ch07-st4', g11.SCEN_G11, c=('C3', 'C4'), d=(3, 5))

K.ar('ch06-st2', [
    ('Anonymous questionnaires can reduce social desirability bias.', 'Respondents who cannot be identified feel less pressure to present themselves favourably.', 0, 'R explains A.'),
    ('Reverse-scored items help to detect acquiescence bias.', 'Acquiescence bias is the tendency to agree with statements regardless of content.', 1, 'Both true; R defines the bias but does not itself explain how reverse-scoring detects it (inconsistent agreement with opposite items).'),
    ('A high response rate removes all sampling bias.', 'Non-response bias occurs when non-responders differ from responders.', 3, 'A is false - the sampling frame can still be biased; R is true.'),
    ('Online surveys always produce representative samples.', 'Online surveys can reach large numbers of people quickly.', 3, 'A is false (self-selection, digital exclusion); R is true.'),
    ('Central tendency bias can make Likert data less informative.', 'Some respondents avoid extreme options and choose the midpoint.', 0, 'Clustering at the midpoint hides real differences in attitude.'),
])
K.R.f['ch06-st2'].why += [
    ('Explain why the way a survey is administered can affect responses.', 'Face-to-face or teacher-administered surveys increase social desirability and interviewer effects; anonymous online surveys reduce these but may lower effort and response rates.'),
    ('Explain how acquiescence bias can be reduced in a questionnaire.', 'Include balanced, reverse-worded items so that agreeing with everything produces inconsistent answers; use forced-choice items; keep items specific.'),
    ('Explain why a sampling frame matters in survey research.', 'A sample can only be as representative as the list it is drawn from; if the frame omits groups (e.g. students not on the email list), the sample will be biased however it is selected.')]
K.R.f['ch06-st2'].contrast += [
    ('response bias', 'sampling bias', 'Response bias concerns inaccurate answers from the people who respond; sampling bias concerns who is included in the sample, making it unrepresentative of the population.'),
    ('non-response bias', 'volunteer bias', 'Non-response bias arises when invited people who do not respond differ from those who do; volunteer bias arises when people who choose to take part differ from the population.')]
K.R.f['ch06-st2'].misc += [
    ('If a survey is anonymous, participants will always answer honestly.', 'Anonymity reduces social desirability bias but cannot remove memory errors, misunderstanding, acquiescence or careless responding.')]

INTERVIEW_SCEN = [
    ('A government agency wants to compare stress levels of 500 nurses across 20 hospitals.', 'structured interview', 'fixed questions allow quick, comparable, quantifiable answers across a large sample'),
    ('A researcher wants to understand how survivors of an earthquake in Nepal made sense of their experience.', 'unstructured or semi-structured interview', 'a flexible format lets survivors describe their experience in their own words and the researcher follow sensitive leads'),
    ('A school wants to know how Year 12 students experience the IB extended essay, covering specific stages of the process.', 'semi-structured interview', 'an interview schedule ensures all stages are covered while probes capture individual experiences'),
    ('A market researcher needs to know how many customers prefer each of three logos.', 'structured interview', 'closed, standardised questions produce frequencies that can be compared'),
    ('A psychologist explores how first-generation university students describe their identity.', 'semi-structured interview', 'core topics are covered but the participant\'s own meanings can be explored with probes'),
    ('A researcher studies the life histories of elderly migrants who arrived in the UK in the 1950s.', 'unstructured interview', 'life-history research follows the participant\'s narrative rather than a fixed schedule'),
]


@K.add('ch07-st1', ('C3',), (1, 4), 'short')
def interview_choice(rng, slot):
    sc, kind, why = rng.choice(INTERVIEW_SCEN)
    if slot.d <= 2:
        labels = ['Structured interview', 'Semi-structured interview', 'Unstructured interview', 'Closed questionnaire only', 'Focus group']
        if ' or ' in kind:
            correct, wrongs = 'Semi-structured or unstructured interview', ['Structured interview', 'Closed questionnaire only', 'Telephone poll with fixed options']
        else:
            correct = cap(kind)
            wrongs = [x for x in labels if x != correct]
            rng.shuffle(wrongs)
        return mcq(rng, f'{sc} Which interview format is most suitable?', correct, wrongs[:3], f'{cap(kind)}: {why}.')
    return dict(stem=f'{sc} Recommend an interview format and justify your choice, including one limitation of that format.',
                answer=f'{cap(kind)} - {why}.', type='short', marks=4,
                markingKey=f'1 mark format ({kind}); 2 marks justification ({why}); 1 mark relevant limitation (structured: little depth; semi/unstructured: harder to compare, interviewer effects, time-consuming analysis).')


K.R.f['ch07-st1'].cases += [
    ('a telephone survey of voters', 'A polling company in Mexico City phones 1,000 adults and reads the same ten questions with fixed answer options to each.', 'structured interviews', 'identical questions and options produce comparable, quantifiable data from a large sample, but answers lack depth'),
    ('interviewing a refugee teenager through an interpreter', 'A researcher in Berlin interviews a 15-year-old Afghan refugee about school with the help of an interpreter who is from the same community.', 'interviewer effects and rapport', 'the interpreter may build trust but may also filter or soften answers, and the teenager may be reluctant to criticise in front of a community member'),
    ('an interviewer who nods at certain answers', 'In a pilot interview in Lisbon about study habits, the interviewer smiles and nods when students mention revising early.', 'interviewer bias', 'non-verbal approval reinforces particular answers, so later responses may be socially desirable rather than accurate')]
K.R.f['ch07-st1'].apply += [
    ('Explain two things an interviewer should do at the start of an interview to build rapport.', 'Explain the purpose, confidentiality and right to withdraw in plain language; start with easy, non-threatening questions; choose a comfortable, private setting; use open body language and active listening.', 3),
    ('An interviewer\'s first question is "Don\'t you think the school is too strict?" Explain the problem and rewrite the question.', 'It is a leading question that suggests the answer; rewrite as "How would you describe the school\'s rules?" with probes such as "Can you tell me more about that?"', 3)]

ETHICS_SCEN = [
    ('A student wants to interview a friend about her eating disorder for a class practical.', 'protection from harm and the sensitivity of the topic (also the dual relationship of friend and researcher)', 'choose a less sensitive topic; if any, ensure support is available, the right to withdraw is clear and the friend is not pressured'),
    ('A researcher plans to publish long quotations from interviews with teachers at a small rural school.', 'confidentiality - quotations and context may identify individuals', 'use pseudonyms, remove identifying details, ask participants to approve quotations'),
    ('Audio recordings of interviews are stored on a shared school laptop.', 'data protection and confidentiality', 'store recordings on a password-protected device, transcribe with codes and delete audio after analysis'),
    ('An interviewee asks to withdraw two weeks after her interview.', 'right to withdraw data', 'delete her recording and transcript and exclude her data from the analysis without penalty'),
    ('A teacher interviews her own students about the quality of her teaching.', 'power imbalance and voluntary participation; social desirability', 'use an independent interviewer, anonymous reporting and make it clear that participation does not affect grades'),
    ('A researcher interviews 14-year-olds about online gaming.', 'informed consent with minors', 'obtain parental/guardian consent as well as the participants\' own assent, in age-appropriate language'),
]


@K.add('ch07-st3', ('C3',), (1, 4), 'short')
def interview_ethics(rng, slot):
    sc, issue, fix = rng.choice(ETHICS_SCEN)
    return dict(stem=f'{sc} Identify the main ethical issue and explain how it should be addressed.', answer=f'Issue: {issue}. Response: {fix}.',
                type='short', marks=3 if slot.d <= 2 else 4,
                markingKey=f'1 mark: issue ({issue}). 1-2 marks: explanation of why it matters in this context. 1 mark: appropriate action ({fix}).')


K.R.f['ch07-st3'].cases += [
    ('a member check that changes a theme', 'After analysing interviews with nurses in Manila, a researcher sends each nurse a summary; two nurses say a theme she called "resignation" is better described as "quiet resistance".', 'credibility in interview research', 'member checking corrected an interpretation, showing how participant feedback increases the credibility of qualitative findings'),
    ('a study of rural teachers with thick description', 'A report on interviews with teachers in rural Kenya gives detailed information about class sizes, distances travelled and community expectations.', 'transferability', 'thick description lets readers judge whether the findings may apply to teachers in similar rural contexts elsewhere'),
    ('two coders who disagree', 'Two students code the same interview transcript independently; one finds a theme of "family pressure", the other "self-imposed pressure".', 'researcher triangulation', 'discussing disagreements and returning to the data refines the themes and reduces individual bias, increasing credibility')]
K.R.f['ch07-st3'].apply += [
    ('Explain how a researcher could write a reflexive statement for an interview study on discrimination experienced by Muslim students in France.', 'State her own identity and beliefs (e.g. religion, nationality), relationship to participants, and how these may have shaped questions, rapport and interpretation; explain steps taken to limit bias (second coder, member checks).', 4)]

# ---------------------------------------------------------------------------------------------
# ch08 HL extension: culture
# ---------------------------------------------------------------------------------------------
K.facts('ch08-st1', F(
    terms=[('emic approach', 'studying behaviour from within a culture, using concepts and methods meaningful to its members'),
           ('etic approach', 'studying behaviour from outside, comparing cultures using concepts and measures assumed to be universal'),
           ('imposed etic', 'applying concepts or measures developed in one culture to another as if they were universal'),
           ('derived etic', 'universal concepts that emerge from comparing several emic studies'),
           ('cultural relativism', 'the view that behaviour should be understood in the context of the culture in which it occurs'),
           ('holistic vs analytic cognition', 'Nisbett\'s distinction between attending to context and relationships (more common in East Asia) and to focal objects and categories (more common in the West)'),
           ('culture-bound syndrome', 'a pattern of distress recognised mainly within a particular culture, such as hikikomori in Japan')],
    facts=[('Masuda and Nisbett (2001) found that, when describing underwater scenes, Japanese participants made more statements about:', 'The background and relationships between objects', ['Only the largest fish', 'Nothing - they recalled less', 'The colours of the focal fish only'],
            'American participants focused more on salient focal objects.'),
           ('Kleinman (1982) found that many Chinese patients diagnosed with neurasthenia:', 'Met Western criteria for depression but described mainly physical symptoms', ['Had no psychological symptoms', 'Had a brain tumour', 'Refused any diagnosis'],
            'This illustrates somatisation and culturally shaped symptom expression.'),
           ('Kulkofsky et al. (2011) compared flashbulb memories in five countries and found that the importance of an event to the person:', 'Predicted flashbulb memories less in collectivist cultures such as China', ['Did not matter in any country', 'Mattered most in China', 'Was replaced by fear in all countries'],
            'Personal importance and rehearsal were stronger predictors in individualist cultures.')],
    why=[('Explain why combining emic and etic approaches is useful.', 'Emic research identifies culturally meaningful concepts and avoids imposing outside categories; etic research allows comparison across cultures; derived etics emerge when emic findings from several cultures are compared (Berry, 1969).'),
         ('Explain how culture can influence cognition.', 'Cultural practices and values shape attention and thinking styles - e.g. East Asian participants attend more to context and relationships (holistic) than American participants (analytic) (Masuda and Nisbett, 2001).')],
    contrast=[('an emic approach', 'an etic approach', 'An emic approach studies a culture from the inside with locally meaningful concepts; an etic approach compares cultures from outside using concepts assumed to be universal.')],
    misc=[('Etic research is always biased and should never be used.', 'Etic research allows comparison and can identify universals; the problem is imposed etic, which can be reduced by combining it with emic research and careful translation.')],
    cases=[('depression in rural Zimbabwe', 'Researchers in Zimbabwe found that local people described depression as "kufungisisa" (thinking too much), and lay health workers delivered "Friendship Bench" problem-solving therapy on park benches.', 'emic approaches to culture and health', 'using a local concept of distress and a culturally acceptable delivery made the intervention effective, showing the value of emic understanding')],
    apply=[('A researcher wants to study attachment in rural communities in Mali. Explain how she could combine emic and etic approaches.', 'Begin with emic fieldwork (interviews, observations of caregiving, local concepts of security and multiple carers), then adapt or develop measures; compare with etic measures like the Strange Situation only after checking their meaning.', 4)],
    evaluate=[('Psychological research is culturally biased.', ['WEIRD samples (Henrich et al., 2010)', 'imposed etic measures (Strange Situation in Japan)', 'Western concepts of the self'],
               ['growing cross-cultural and indigenous psychology', 'some findings replicate across cultures', 'emic-etic integration reduces bias'],
               'Much research has been culturally biased, but awareness and cross-cultural methods are reducing the problem.')],
))
K.study('ch08-st1', 'Masuda and Nisbett', 2001, 'attention to context in Japanese and American participants', 'to investigate cultural differences in attention to focal objects and context',
        'Japanese and American university students watched animated underwater scenes and described them; later they were tested on recognising objects against original or new backgrounds.',
        'Japanese participants made more statements about the background and relationships, and their recognition of objects was more affected by changes in background than Americans\'',
        'cultural differences in cognition (holistic vs analytic)',
        ['controlled comparison with identical stimuli', 'converging measures (descriptions and recognition)'],
        ['university students only', 'nationality used as a proxy for culture'],
        mtype='quasi-experiment')
K.study('ch08-st1', 'Kleinman', 1982, 'neurasthenia and depression in China', 'to investigate how depression is expressed and diagnosed in Chinese culture',
        'Kleinman interviewed and assessed 100 patients diagnosed with neurasthenia at a psychiatric clinic in Hunan, China, using Western diagnostic criteria.',
        'most of the patients met Western criteria for major depression but reported mainly physical symptoms such as headaches, dizziness and fatigue',
        'culture and the expression of distress (somatisation)',
        ['in-depth clinical interviews in context', 'challenged universal symptom models'],
        ['applying Western criteria is itself an etic approach', 'one clinic'],
        mtype='semi-structured interview')
K.study('ch08-st1', 'Kulkofsky et al.', 2011, 'cultural variation in flashbulb memories', 'to investigate whether the factors that predict flashbulb memories differ between cultures',
        'Adults in China, Germany, Turkey, the UK and the USA recalled personal circumstances of hearing about public events and rated factors such as personal importance, emotion, surprise and rehearsal.',
        'flashbulb memories were found in all countries, but personal importance and rehearsal predicted them less strongly in China than in more individualist cultures',
        'culture and memory',
        ['five-country comparison with the same measures'],
        ['different events in different countries', 'self-report; translation issues'],
        mtype='cross-cultural survey')

K.facts('ch08-st2', F(
    terms=[('WEIRD', 'Western, educated, industrialised, rich and democratic - describing the populations from which most psychology samples are drawn'),
           ('cultural bias', 'the tendency to interpret or judge behaviour using the standards of one\'s own culture'),
           ('ethnocentrism', 'judging other cultures by the standards of one\'s own culture, often seeing one\'s own as superior'),
           ('back-translation', 'translating a measure into another language and then independently back into the original to check equivalence'),
           ('indigenous psychology', 'psychology developed within a culture, using its own concepts and methods'),
           ('universality', 'the assumption that a psychological process is the same in all cultures')],
    facts=[('Arnett (2008) found that about what percentage of participants in top American psychology journals were from Western industrialised countries?', '96%', ['50%', '70%', '25%'],
            'These countries contain about 12% of the world\'s population.'),
           ('Henrich, Heine and Norenzayan (2010) reported that susceptibility to the Müller-Lyer illusion was:', 'Much lower among San foragers of the Kalahari than among American undergraduates', ['Identical across cultures', 'Highest among San foragers', 'Absent among Americans'],
            'Even basic perception varies across cultures.')],
    why=[('Explain why WEIRD samples limit the generalisability of research.', 'WEIRD populations are psychologically unusual in many respects (e.g. individualism, analytic thinking, susceptibility to some illusions), so findings may not apply to most of the world\'s population.'),
         ('Explain why back-translation is used in cross-cultural research.', 'It checks that the translated questionnaire has the same meaning as the original, reducing measurement bias; differences reveal items that need adapting.')],
    contrast=[('ethnocentrism', 'cultural relativism', 'Ethnocentrism judges other cultures by one\'s own standards; cultural relativism interprets behaviour within its own cultural context.')],
    misc=[('Using participants from many countries removes cultural bias.', 'Cross-national samples still suffer from imposed etic measures, translation problems and urban, educated sub-samples that may not represent their cultures.')],
    cases=[('a Western IQ test used in rural Kenya', 'A Western intelligence test is given to children in rural Kenya, who score lower than British children; local children are, however, highly skilled at identifying medicinal herbs (Sternberg et al., 2001).', 'cultural bias in research', 'the test measures culturally specific knowledge and skills (imposed etic), so lower scores reflect test bias rather than lower intelligence')],
    apply=[('A psychology student plans to use a US self-esteem scale with students in Tokyo. Identify two possible sources of cultural bias and suggest how to reduce them.', 'Translation/meaning (use back-translation and piloting); different norms of self-presentation (modesty may lower scores - include emic items); response styles (avoidance of extremes).', 4)],
    evaluate=[('Most psychological findings cannot be generalised beyond WEIRD populations.', ['96% WEIRD samples (Arnett, 2008)', 'WEIRD people are outliers (Henrich et al., 2010)'],
               ['some processes replicate widely (e.g. basic memory, emotion recognition)', 'cross-cultural replications sometimes confirm findings'],
               'Generalisation should not be assumed; each finding must be tested across cultures.')],
))
K.study('ch08-st2', 'Arnett', 2008, 'the neglected 95%', 'to examine the cultural composition of samples in leading American psychology journals',
        'Arnett analysed the samples reported in articles published in six APA journals between 2003 and 2007.',
        'about 96% of participants were from Western industrialised countries, which contain about 12% of the world\'s population; 68% were American',
        'sampling bias towards WEIRD populations',
        ['systematic content analysis of journals'],
        ['limited to APA journals', 'nationality is only one aspect of culture'],
        mtype='meta-analysis')
K.study('ch08-st2', 'Henrich, Heine and Norenzayan', 2010, 'the weirdest people in the world', 'to review whether WEIRD samples are representative of humans in general',
        'A review of cross-cultural evidence on visual perception, fairness, cooperation, spatial reasoning, categorisation, moral reasoning and self-concept.',
        'WEIRD participants were often outliers compared with other populations, so they are a poor basis for generalising about human psychology',
        'cultural bias in psychological research',
        ['wide range of domains'],
        ['narrative review; possible selection of studies'])
K.study('ch08-st2', 'Sternberg et al.', 2001, 'practical intelligence in Kenyan children', 'to investigate the relationship between academic and practical (tacit) intelligence in rural Kenyan children',
        '85 children aged 12-15 in a rural Kenyan village completed a test of knowledge of natural herbal medicines used to treat illnesses, as well as Western-style tests of academic intelligence and vocabulary.',
        'children with high practical knowledge of herbal medicines tended to score lower on Western academic tests (negative correlations), suggesting different forms of intelligence are valued and developed in different cultures',
        'cultural bias in the measurement of intelligence',
        ['emic measure developed with local knowledge'],
        ['small sample from one village', 'correlational'],
        mtype='correlational study')

K.facts('ch08-st3', F(
    terms=[('culture-bound syndrome', 'a pattern of symptoms recognised mainly within a particular culture'),
           ('somatisation', 'expressing psychological distress through physical symptoms'),
           ('collectivist parenting', 'parenting that emphasises obedience, interdependence and family obligations'),
           ('individualist parenting', 'parenting that emphasises independence, self-expression and personal achievement'),
           ('cultural scripts for relationships', 'shared cultural expectations about how relationships should form and be maintained')],
    facts=[('Which country showed relatively high levels of insecure-resistant attachment in Van IJzendoorn and Kroonenberg (1988)?', 'Japan', ['West Germany', 'Great Britain', 'The USA'],
            'Japanese infants rarely experienced separation from their mothers.'),
           ('Becker et al. (2002) found that after television was introduced in Fiji, the percentage of adolescent girls with high EAT-26 scores rose from about 13% to about:', '29%', ['15%', '50%', '75%'],
            'Interviews linked this to Western media ideals of thinness.')],
    why=[('Explain how culture can affect the expression of mental disorders.', 'Culture shapes which symptoms are considered acceptable to express and how distress is understood - e.g. somatisation in China (Kleinman, 1982) - and influences help-seeking and stigma.'),
         ('Explain how culture influences child development.', 'Through enculturation, children learn culturally valued skills and norms; parenting goals (independence vs interdependence) shape attachment behaviour, emotional expression and cognitive styles.')],
    contrast=[('cultural influences on health', 'cultural influences on relationships', 'Culture affects health through beliefs about illness, symptom expression and treatment; it affects relationships through norms about partner choice (arranged vs love marriage), family roles and communication.')],
    misc=[('Mental disorders are identical in all cultures.', 'Core features of some disorders occur widely, but their expression, prevalence, interpretation and treatment vary considerably across cultures.')],
    cases=[('hikikomori in Japan', 'Some young adults in Japan withdraw completely from social life and stay in their rooms for months or years; the term hikikomori describes this pattern.', 'culture and health', 'cultural factors (academic pressure, shame, family accommodation) shape a form of withdrawal that is recognised and named in Japan, though similar cases are now reported elsewhere')],
    apply=[('A clinic in London serves many patients from South Asia. Using research on culture and health, suggest two ways it could adapt its mental health services.', 'Train staff to recognise somatic presentations of distress (Kleinman, 1982); involve families where appropriate; provide interpreters and culturally adapted CBT; use culturally validated screening tools.', 4)],
    evaluate=[('Culture has a greater influence on behaviour than biology.', ['cultural variation in attachment, relationships, illness expression', 'Becker et al. (2002) - rapid change in eating attitudes'],
               ['universal biological processes (stress response, brain development)', 'gene-culture interaction', 'within-culture variation'],
               'Culture and biology interact; culture strongly shapes how biological predispositions are expressed.')],
))
K.study('ch08-st3', 'Becker et al.', 2002, 'eating attitudes after the introduction of television in Fiji', 'to investigate the impact of Western television on disordered eating among Fijian adolescent girls',
        'Ethnic Fijian schoolgirls completed the EAT-26 in 1995 (shortly after TV arrived) and in 1998; 30 girls were also interviewed in 1998.',
        'high EAT-26 scores rose from 12.7% to 29.2% and self-induced vomiting from 0% to 11.3%; girls described admiring and wanting to resemble TV characters',
        'cultural change and health',
        ['natural experiment with mixed methods'],
        ['different samples in 1995 and 1998', 'other social changes may contribute'])
K.study('ch08-st3', 'Van IJzendoorn and Kroonenberg', 1988, 'attachment across eight countries', 'to compare attachment types across cultures',
        'Meta-analysis of 32 Strange Situation studies from 8 countries (about 2,000 infants).',
        'secure attachment was most common everywhere; avoidant attachment was more common in West Germany and resistant attachment in Japan and Israel; intracultural variation was 1.5 times intercultural',
        'culture and development',
        ['large combined sample'],
        ['Strange Situation may be an imposed etic', 'unequal sample sizes'],
        mtype='meta-analysis')

K.R.f['ch08-st1'].cases += [
    ('the Friendship Bench in Harare', 'Lay health workers ("grandmothers") in Harare deliver six sessions of problem-solving therapy on benches outside clinics, using the Shona idiom "kufungisisa" (thinking too much). A randomised trial (Chibanda et al., 2016) found larger reductions in symptoms than enhanced usual care.', 'combining emic and etic approaches in health', 'an etic method (an RCT of problem-solving therapy) was combined with emic concepts and local delivery, increasing acceptability and effectiveness'),
    ('the Strange Situation in Japan', 'When the Strange Situation was used in Japan, many infants became extremely distressed at separation and were classified as insecure-resistant; Japanese infants are rarely left with strangers.', 'imposed etic', 'a procedure developed in the USA was assumed to measure the same thing everywhere, so cultural differences in childcare were misread as differences in security'),
    ('face-saving and depression screening in Seoul', 'A clinic in Seoul found that a translated Western depression questionnaire missed many patients who described their distress as "hwa-byung" (fire illness) with chest heat and pressure.', 'emic concepts of distress', 'a culturally specific idiom of distress was not captured by an etic instrument, so emic research was needed to adapt the screening tool'),
    ('analytic and holistic attention in eye-tracking', 'Chua, Boland and Nisbett (2005) tracked eye movements as Chinese and American students looked at photographs of objects on complex backgrounds; Chinese students made more fixations to the background.', 'culture and cognition', 'eye-tracking provided an objective, etic measure supporting the holistic-analytic distinction'),
    ('ubuntu and self-construal in South Africa', 'Researchers interviewing Xhosa-speaking adults found that descriptions of the self were full of references to family, community and ancestors, reflecting the value of ubuntu ("a person is a person through other people").', 'emic research on the self', 'open-ended emic interviews revealed an interdependent self-concept that a Western self-esteem scale might not capture'),
]
K.R.f['ch08-st1'].apply += [
    ('A team wants to compare conformity in Brazil, Norway and Indonesia using the Asch paradigm. Explain one problem of imposed etic and one way to reduce it.', 'Problem: the meaning of agreeing publicly with a group (e.g. politeness, harmony) may differ, so conformity rates may not measure the same construct. Reduce it by pilot emic interviews, local researchers, back-translation and checking that the task and confederates are equivalent.', 4),
    ('A psychologist in Toronto is asked to assess an anxious newly arrived refugee from Eritrea. Explain how an emic approach could improve the assessment.', 'Learn local idioms of distress and beliefs about causes (e.g. spiritual, social) through interviews with community members and interpreters; avoid relying only on Western symptom checklists; involve family where valued; interpret symptoms in context.', 4),
    ('Suggest how a researcher could develop a derived etic measure of "respect for elders" across Ghana, India and Germany.', 'Carry out emic studies in each culture (interviews, observation) to find local meanings; identify common elements; build items from the shared elements; test for equivalence in each culture before comparing.', 4),
    ('A study finds that a Western depression inventory gives lower scores in rural Cambodia than in the USA. Explain two reasons why this may not mean depression is less common.', 'Distress may be expressed somatically or through local idioms not covered by the items (imposed etic); stigma may reduce reporting; translation may change meaning; response styles and literacy may differ.', 4),
    ('Using one study, explain how culture may influence cognition. Then suggest a follow-up study that uses an emic approach.', 'E.g. Masuda and Nisbett (2001): Japanese participants attended more to context. Follow-up: ethnographic interviews/observation of how Japanese and American children are taught to describe scenes, to find culturally meaningful reasons for attention styles.', 6),
]

# ============================================================================================
# Chapter 9 - HL Extension: Motivation
# ============================================================================================
K.facts('ch09-st1', F(
    terms=[('intrinsic motivation', 'doing an activity for the inherent satisfaction or interest of the activity itself'),
           ('extrinsic motivation', 'doing an activity to obtain a separable outcome, such as a reward or avoiding punishment'),
           ('self-determination theory (SDT)', 'Deci and Ryan\'s theory that well-being and autonomous motivation depend on satisfying the needs for autonomy, competence and relatedness'),
           ('autonomy (SDT)', 'the need to feel that one\'s behaviour is self-endorsed and volitional'),
           ('competence (SDT)', 'the need to feel effective in interacting with the environment'),
           ('relatedness (SDT)', 'the need to feel connected to and cared for by others'),
           ('overjustification effect', 'the reduction in intrinsic motivation that can follow when an expected external reward is given for an already interesting activity'),
           ('cognitive evaluation theory', 'a sub-theory of SDT stating that rewards perceived as controlling reduce intrinsic motivation, while informational feedback can increase it'),
           ('amotivation', 'a state of lacking any intention to act, often because the person feels incompetent or sees no value in the activity'),
           ('identified regulation', 'a form of extrinsic motivation in which the person consciously values the goal of the behaviour')],
    facts=[('In Deci (1971), students paid $1 per puzzle solved in session 2 later spent:', 'Less free-choice time on the puzzles than unpaid students', ['More free-choice time on the puzzles', 'Exactly the same time as unpaid students', 'No time at all on any puzzle'],
            'Payment shifted the perceived reason for the activity from interest to reward.'),
           ('Which three needs are proposed as basic psychological needs by self-determination theory?', 'Autonomy, competence and relatedness', ['Safety, esteem and self-actualisation', 'Power, achievement and affiliation', 'Hunger, thirst and sex'],
            'Maslow and McClelland proposed the other sets.'),
           ('In Lepper, Greene and Nisbett (1973), which group of children later spent the least free-play time drawing?', 'Children who expected and received a "Good Player" award', ['Children who received an unexpected award', 'Children who received no award', 'All groups spent equal time'],
            'Only the expected-reward condition undermined interest.'),
           ('According to Deci, Koestner and Ryan (1999), which type of reward tends to INCREASE intrinsic motivation?', 'Positive verbal feedback', ['Expected tangible rewards', 'Rewards contingent on completing a task', 'Performance-contingent money'],
            'Verbal rewards are usually experienced as informational rather than controlling.'),
           ('A runner trains because she values health, though she does not enjoy running. In SDT this is:', 'Identified regulation', ['Intrinsic motivation', 'External regulation', 'Amotivation'],
            'She endorses the outcome, but the activity is not done for its own sake.')],
    why=[('Explain why expected rewards can reduce intrinsic motivation.', 'Cognitive evaluation theory: an expected, task-contingent reward is perceived as controlling, shifting the perceived locus of causality from internal to external and thwarting autonomy; people then attribute their behaviour to the reward (overjustification) and lose interest when it stops.'),
         ('Explain how teachers can support autonomous motivation according to SDT.', 'Offer meaningful choices and rationales (autonomy), give optimal challenge and informational feedback (competence), and show warmth and involvement (relatedness); avoid controlling language, threats and surveillance.'),
         ('Explain why extrinsic motivation is not always harmful according to SDT.', 'Extrinsic motivation lies on a continuum; when a person identifies with or integrates the value of a behaviour it becomes relatively autonomous and is linked to persistence and well-being; unexpected or informational rewards need not undermine interest.')],
    contrast=[('intrinsic motivation', 'extrinsic motivation', 'Intrinsic motivation comes from interest or enjoyment in the activity itself; extrinsic motivation comes from outcomes separate from the activity, such as rewards, grades or approval.'),
              ('external regulation', 'identified regulation', 'External regulation is behaviour controlled by rewards or punishments; identified regulation is behaviour the person personally values, so it feels more autonomous.'),
              ('controlling rewards', 'informational rewards', 'Controlling rewards are experienced as pressure to behave in certain ways and reduce autonomy; informational rewards give feedback about competence and can increase intrinsic motivation.')],
    misc=[('Rewards always destroy intrinsic motivation.', 'Only expected, tangible, task-contingent rewards reliably reduce intrinsic motivation (Deci et al., 1999); verbal praise and unexpected rewards usually do not, and rewards can raise motivation for uninteresting tasks.'),
          ('Self-determination theory says people should be left completely alone to be motivated.', 'Autonomy does not mean independence; SDT stresses structure, competence support and relatedness as well as choice.')],
    cases=[('a reading incentive scheme', 'A primary school in Dublin gave children a sticker for every book read; book borrowing doubled during the scheme, but after it ended borrowing fell below its original level.', 'the overjustification effect', 'the expected reward shifted the reason for reading from interest to stickers, so intrinsic motivation was undermined when the reward stopped'),
           ('a coding club in Bangalore', 'A teacher lets students choose their own coding projects, sets challenges just above their current level, and pairs them with friendly peer mentors; attendance stays high all year.', 'self-determination theory', 'choice supports autonomy, optimal challenge supports competence and peer mentoring supports relatedness, producing autonomous motivation'),
           ('sales targets in a call centre', 'A call centre in Manila introduced pay bonuses for staff who exceeded call targets; calls per hour rose, but staff reported lower job satisfaction and more left within a year.', 'controlling extrinsic motivation', 'performance-contingent rewards were experienced as controlling, increasing compliance but thwarting autonomy and well-being'),
           ('music practice at home', 'A 12-year-old in Vienna practised violin only when her parents promised screen time; when she joined an orchestra with friends, she began practising without being asked.', 'internalisation of extrinsic motivation', 'relatedness and valued group goals helped her move from external regulation towards identified or intrinsic motivation')],
    apply=[('A sports coach in Melbourne wants young swimmers to keep training after the season ends. Using SDT, suggest three strategies.', 'Give choice over sessions/goals (autonomy); set achievable targets and give specific informational feedback (competence); build team belonging and warm coach relationships (relatedness); avoid relying on prizes or threats.', 6),
           ('A company plans to pay employees for every online training module they complete. Using research, explain one possible risk of this plan.', 'Expected task-contingent rewards can reduce intrinsic motivation (Deci, 1971; Deci et al., 1999); employees may complete modules quickly without learning and stop when payment ends (overjustification).', 3),
           ('Explain how a parent could praise a child\'s drawing in a way that supports intrinsic motivation.', 'Use informational, specific praise about effort and strategy ("you used shading to show the light") rather than controlling praise or rewards; avoid making praise contingent or comparing with others.', 3)],
    evaluate=[('Self-determination theory provides a convincing explanation of human motivation.', ['Deci (1971) and Lepper et al. (1973): undermining effect', 'Deci et al. (1999) meta-analysis of 128 studies', 'Williams et al. (1996): autonomous motivation predicts weight loss', 'applied successfully in education, health and work'],
               ['much evidence is self-report and correlational', 'cultural debate - is autonomy valued equally in collectivist cultures? (Iyengar and Lepper, 1999)', 'needs are hard to measure directly', 'reward effects are smaller in real settings (Cameron and Pierce, 1994)'],
               'SDT is well supported and widely applied, but its universality and measurement need further testing.'),
              ('Extrinsic rewards should not be used to motivate students.', ['undermining effect of expected rewards', 'controlling climates reduce well-being'],
               ['rewards can kick-start uninteresting but useful activities', 'verbal and unexpected rewards do not undermine', 'token economies can be effective (Ayllon and Azrin, 1968)'],
               'Rewards should be used carefully - informationally, for uninteresting tasks, and faded over time.')],
))
K.study('ch09-st1', 'Deci', 1971, 'monetary rewards and the Soma puzzle', 'to investigate the effect of external rewards on intrinsic motivation',
        '24 university students in the USA solved Soma cube puzzles in three one-hour sessions; in session 2 the experimental group was paid $1 for each puzzle solved. In each session the experimenter left the room for 8 minutes and recorded how long participants spent on the puzzles when free to do anything.',
        'paid participants spent less free-choice time on the puzzles in session 3 than in session 1, whereas unpaid controls slightly increased their time',
        'the undermining effect of extrinsic rewards on intrinsic motivation',
        ['standardised free-choice measure of behaviour', 'baseline and follow-up sessions in an independent groups design'],
        ['small student sample', 'puzzles are an artificial activity', 'short-term effects only'],
        mtype='laboratory experiment', iv='whether participants were paid $1 per puzzle in session 2', dv='time spent on the puzzles in the free-choice period',
        wrong=['Paid participants spent more time on the puzzles afterwards', 'Payment had no effect on free-choice time', 'Unpaid participants stopped doing the puzzles'])
K.study('ch09-st1', 'Lepper, Greene and Nisbett', 1973, 'the "Good Player" award', 'to test the overjustification hypothesis with young children',
        'Nursery school children in California who already liked drawing with felt-tip markers drew under one of three conditions: expected award (a "Good Player" certificate), unexpected award or no award. One to two weeks later their free-play drawing was observed through a one-way mirror.',
        'children in the expected-award condition spent about half as much free-play time drawing as children in the other two conditions',
        'the overjustification effect',
        ['behavioural measure taken unobtrusively in a natural setting', 'unexpected-award group shows it is expectation, not the reward itself'],
        ['young children from one university nursery school', 'single activity and short follow-up', 'observers may have known the conditions'],
        iv='award condition (expected, unexpected or none)', dv='percentage of free-play time spent drawing with the markers',
        wrong=['The unexpected-award group drew least', 'All three groups drew equally', 'The expected-award group drew most'])
K.study('ch09-st1', 'Deci, Koestner and Ryan', 1999, 'a meta-analysis of reward effects', 'to assess the effects of different types of extrinsic reward on intrinsic motivation',
        'Meta-analysis of 128 experiments that measured intrinsic motivation by free-choice behaviour or self-reported interest after rewards.',
        'expected tangible rewards significantly reduced free-choice intrinsic motivation, especially for interesting tasks, while positive verbal feedback increased it',
        'cognitive evaluation theory (controlling vs informational rewards)',
        ['very large combined evidence base', 'distinguished between reward types'],
        ['most studies were short laboratory studies', 'disagreement with other meta-analyses (Cameron and Pierce, 1994)'],
        mtype='meta-analysis')

STAGES = ['precontemplation', 'contemplation', 'preparation', 'action', 'maintenance']
STAGE_SCEN = [
    ('Mateo, a 45-year-old smoker in Buenos Aires, says he enjoys smoking and has no plans to quit.', 0),
    ('Aiko knows her heavy drinking is harming her sleep and keeps thinking about cutting down "sometime this year", but has not decided when.', 1),
    ('Kwame has bought running shoes and signed up for a running club that starts next week.', 2),
    ('Fatima stopped eating fast food three months ago and now cooks at home most days.', 3),
    ('Lars quit smoking two years ago and uses exercise to cope when he feels the urge to smoke.', 4),
    ('Priya, who has high blood pressure, says her diet is fine and her doctor is worrying for nothing.', 0),
    ('Chen weighs up the pros and cons of reducing his gaming time but feels the benefits and costs are about equal.', 1),
    ('Sofia has set a quit date for the end of the month and told her family she will stop vaping.', 2),
    ('Omar started walking 30 minutes every day four weeks ago.', 3),
    ('Hana has kept to her medication routine for a year and has strategies to avoid relapse when travelling.', 4),
    ('Diego has never thought about wearing a cycling helmet and sees no reason to.', 0),
    ('Amira joined a gym and has attended three times a week for the past two months.', 3),
]


@K.add('ch09-st3', ('C3',), (1, 4), 'mcq')
def stage_of_change(rng, slot):
    sc, i = rng.choice(STAGE_SCEN)
    frame = rng.choice(['According to the transtheoretical model, which stage of change is this person in?',
                        'Identify the stage of change (Prochaska and DiClemente, 1983) shown by this person.',
                        'Which stage of the transtheoretical model best describes this person?'])
    wrongs = [cap(s) for k, s in enumerate(STAGES) if k != i]
    rng.shuffle(wrongs)
    return mcq(rng, f'{sc} {frame}', cap(STAGES[i]), wrongs[:3],
               f'{cap(STAGES[i])}: ' + ['not intending to change in the next six months',
                                        'intending to change within six months but not yet committed',
                                        'intending to act soon and taking small steps',
                                        'has changed behaviour within the last six months',
                                        'has sustained change for over six months and works to prevent relapse'][i] + '.')


NEED_SCEN = [
    ('A teacher lets students choose which of three novels to study for their coursework.', 'Autonomy'),
    ('A coach breaks a difficult dive into steps so that each swimmer can succeed before moving on.', 'Competence'),
    ('A new employee is paired with a friendly buddy who invites her to team lunches.', 'Relatedness'),
    ('A piano teacher explains why scales matter and asks the student which pieces she would like to learn.', 'Autonomy'),
    ('A maths app adjusts the difficulty so that learners get about 80% of problems right and receives specific feedback.', 'Competence'),
    ('A care home organises weekly video calls so that residents can talk to their grandchildren.', 'Relatedness'),
    ('A manager allows staff to decide their own working hours, as long as projects are finished on time.', 'Autonomy'),
    ('A language tutor shows a learner a chart of how much her vocabulary has grown over the term.', 'Competence'),
    ('A university sets up small "home groups" so that first-year students meet the same peers every week.', 'Relatedness'),
]


@K.add('ch09-st1', ('C3',), (1, 3), 'mcq')
def sdt_need(rng, slot):
    sc, need = rng.choice(NEED_SCEN)
    frame = rng.choice(['Which basic psychological need in self-determination theory is mainly being supported?',
                        'In SDT terms, which need does this strategy mainly satisfy?',
                        'According to Deci and Ryan, which need is this most likely to support?'])
    wrongs = [n for n in ['Autonomy', 'Competence', 'Relatedness'] if n != need] + ['Self-esteem']
    return mcq(rng, f'{sc} {frame}', need, wrongs,
               f'{need} is supported; SDT proposes three basic needs: autonomy, competence and relatedness (self-esteem is not one of them).')


FREE_CTX = [
    ('university students', 'Soma cube puzzles', 'paid for each puzzle solved', 'seconds'),
    ('Year 8 students in Singapore', 'a word-building game', 'given points exchangeable for snacks', 'seconds'),
    ('volunteers in Cape Town', 'a jigsaw puzzle', 'paid 20 rand per completed section', 'seconds'),
    ('nursery children in Stockholm', 'drawing with new pens', 'promised a gold-star certificate', 'seconds'),
    ('adult learners in Montreal', 'a programming challenge', 'offered a voucher for each level completed', 'seconds'),
]


@K.add('ch09-st1', ('C3', 'C4'), (2, 5), 'numerical')
def free_choice(rng, slot):
    who, task, reward, unit = rng.choice(FREE_CTX)
    b1 = rng.randint(180, 260)
    b2 = b1 + rng.randint(-15, 15)
    r3 = b1 - rng.randint(30, 110)
    c3 = b2 + rng.randint(-10, 40)
    dr, dc = r3 - b1, c3 - b2
    pr = 100 * dr / b1
    stem = (f'In a study of {who}, both groups worked on {task} in session 1. In session 2 the reward group was {reward}; '
            f'the control group received nothing. In sessions 1 and 3, free-choice time on the task was recorded. '
            f'Reward group: mean {b1} {unit} (session 1), {r3} {unit} (session 3). Control group: mean {b2} {unit} (session 1), {c3} {unit} (session 3).')
    if slot.d <= 3:
        q = ' Calculate the change in mean free-choice time for each group and state what the results suggest.'
        ans = f'Reward group change = {r3} - {b1} = {dr} {unit}; control change = {c3} - {b2} = {dc:+d} {unit}. The reward appears to have reduced intrinsic motivation (overjustification).'
        mk = f'A1 reward change {dr}. A1 control change {dc:+d}. R1 reward group decreased relative to control - consistent with the undermining effect.'
        m = 3
    else:
        q = (' (a) Calculate the percentage change for the reward group. (b) Explain what the results suggest about intrinsic motivation, '
             'referring to cognitive evaluation theory. (c) State one reason why this conclusion should be treated with caution.')
        ans = (f'(a) ({r3} - {b1}) / {b1} x 100 = {pr:.1f}%. (b) The expected reward was probably experienced as controlling, shifting the perceived '
               f'locus of causality externally; when the reward stopped, interest fell (overjustification); controls changed by {dc:+d} {unit}. '
               '(c) Descriptive data only - no inferential test; small or unrepresentative sample; short-term artificial task; demand characteristics.')
        mk = (f'(a) M1 change/baseline x 100, A1 {pr:.1f}%. (b) R1 reward group fell while control did not, R1 controlling reward / perceived locus of causality. '
              '(c) R1 any valid limitation in context.')
        m = 6
    return dict(stem=stem + q, answer=ans, type='numerical', marks=m, markingKey=mk)

K.facts('ch09-st2', F(
    terms=[('dopamine', 'a neurotransmitter released by midbrain neurons (ventral tegmental area, substantia nigra) that is central to reward learning and motivation'),
           ('mesolimbic pathway', 'the dopamine pathway from the ventral tegmental area to the nucleus accumbens, often called the reward pathway'),
           ('nucleus accumbens', 'a region of the ventral striatum whose activity rises when rewards are anticipated'),
           ('reward prediction error', 'the difference between the reward received and the reward expected, signalled by changes in dopamine neuron firing'),
           ('incentive salience', 'Berridge and Robinson\'s term for the "wanting" that dopamine attaches to reward cues, as distinct from "liking"'),
           ('intracranial self-stimulation', 'behaviour in which animals work to receive electrical stimulation of brain reward areas'),
           ('expectancy-value theory', 'the cognitive theory that motivation depends on the expectation of success and the value placed on the outcome'),
           ('fixed vs growth mindset', 'Dweck\'s distinction between believing ability is fixed and believing it can be developed through effort'),
           ('goal-setting theory', 'Locke and Latham\'s theory that specific, difficult goals with feedback lead to higher performance than vague "do your best" goals')],
    facts=[('Schultz, Dayan and Montague (1997) reported that, after monkeys learned that a light predicted juice, dopamine neurons fired mainly:', 'When the light appeared, not when the expected juice arrived', ['Only when the juice arrived', 'Never again', 'Only when the monkey was punished'],
            'Firing transferred to the predictive cue; omission of expected juice produced a dip below baseline.'),
           ('If an expected reward is NOT delivered, midbrain dopamine neurons typically:', 'Decrease their firing below baseline at the expected time', ['Fire at their highest rate', 'Show no change at all', 'Fire only at the cue a second time'],
            'This negative prediction error signals "worse than expected".'),
           ('Knutson et al. (2001) found that nucleus accumbens activity during the monetary incentive delay task:', 'Increased with the size of the anticipated monetary reward', ['Increased only for anticipated losses', 'Was unrelated to reward size', 'Decreased when rewards were anticipated'],
            'Activity also correlated with self-reported positive arousal.'),
           ('Olds and Milner (1954) found that rats would press a lever repeatedly to receive:', 'Electrical stimulation of the septal area of the brain', ['Food pellets only', 'Mild electric shocks to the feet', 'Access to another rat'],
            'This was the first evidence of brain reward areas.'),
           ('Berridge and Robinson (1998) showed that rats with dopamine depleted by 6-OHDA lesions:', 'Still showed "liking" reactions to sugar but would not work for it', ['Stopped showing any reaction to sugar', 'Worked harder for sugar', 'Preferred bitter tastes'],
            'Dopamine is linked to wanting (incentive salience) rather than liking.'),
           ('Mueller and Dweck (1998) found that, after a failure, children praised for their intelligence:', 'Persisted less and performed worse than children praised for effort', ['Persisted more than effort-praised children', 'Performed the same as all other groups', 'Chose more challenging problems'],
            'Intelligence praise encouraged a fixed view of ability.')],
    why=[('Explain the role of dopamine in reward learning.', 'Dopamine neurons signal reward prediction errors: they fire to unexpected rewards, transfer their response to cues that predict reward, and dip when expected rewards are omitted (Schultz et al., 1997); this teaching signal updates expectations and energises approach to reward cues.'),
         ('Explain the difference between "wanting" and "liking" in reward.', 'Wanting (incentive salience) is the motivational pull of reward cues, depending on mesolimbic dopamine; liking is the hedonic pleasure, linked to opioid "hot spots"; Berridge and Robinson (1998) found dopamine-depleted rats still liked sugar but did not seek it.'),
         ('Explain how cognitive factors influence motivation.', 'Expectations of success and the value placed on goals (expectancy-value theory), beliefs about ability (mindset; Mueller and Dweck, 1998), attributions for success and failure, and specific goals with feedback (Locke and Latham) all influence how much effort people invest and whether they persist.'),
         ('Explain why dopamine-based reward systems may contribute to addiction.', 'Drugs such as cocaine directly increase dopamine in the nucleus accumbens, producing large prediction-error signals; cues associated with the drug acquire strong incentive salience, so "wanting" grows even when "liking" declines (incentive sensitisation).')],
    contrast=[('biological explanations of motivation', 'cognitive explanations of motivation', 'Biological explanations focus on brain systems such as mesolimbic dopamine and reward prediction error; cognitive explanations focus on beliefs, expectancies, values, goals and attributions.'),
              ('"wanting"', '"liking"', '"Wanting" is the motivational drive towards a reward cue, linked to dopamine; "liking" is the pleasure experienced when the reward is consumed, linked to opioid systems.'),
              ('a positive prediction error', 'a negative prediction error', 'A positive prediction error occurs when a reward is better than expected (dopamine bursts); a negative error occurs when it is worse than expected or omitted (dopamine dips).')],
    misc=[('Dopamine is the brain\'s "pleasure chemical".', 'Dopamine is more closely linked to wanting, prediction and learning about rewards than to pleasure itself; liking depends more on opioid and other systems (Berridge and Robinson, 1998).'),
          ('Finding nucleus accumbens activity during reward shows that this area causes motivation.', 'fMRI is correlational; activity may accompany rather than cause motivation, and many regions interact; causal evidence needs lesion, stimulation or drug studies.'),
          ('Biological and cognitive explanations of motivation contradict each other.', 'They are complementary levels of analysis: cognitive expectations of reward are implemented in neural prediction-error systems.')],
    cases=[('loot boxes in video games', 'A popular online game in South Korea sells "loot boxes" whose rewards are random; some teenagers spend hundreds of dollars, saying the moment of opening the box is more exciting than the item itself.', 'dopamine and variable reward', 'unpredictable rewards create repeated positive prediction errors and give the box cue strong incentive salience ("wanting" more than "liking")'),
           ('a fitness tracker with streaks', 'A fitness app used in Toronto rewards users with badges for daily "streaks"; users report anticipating the badge more than enjoying the exercise.', 'reward anticipation and incentive salience', 'cues predicting reward (the streak counter) drive anticipatory dopamine activity, motivating behaviour'),
           ('praise in a Lagos classroom', 'Two teachers in Lagos praise pupils differently: one says "you are so clever", the other "you worked hard on that strategy". After a difficult test, pupils of the second teacher are more willing to try harder problems.', 'cognitive bases of motivation (mindset)', 'effort praise promotes a growth mindset and mastery goals, as in Mueller and Dweck (1998), making pupils persist after failure'),
           ('Parkinson\'s disease medication and gambling', 'Some patients in Paris treated with dopamine agonists for Parkinson\'s disease developed compulsive gambling that stopped when the medication was reduced.', 'dopamine and reward-seeking', 'increasing dopamine activity increased the motivational pull of rewarding activities, supporting a causal role for dopamine in wanting'),
           ('specific sales goals', 'A bakery chain in Lima replaced "do your best" with specific, challenging weekly targets and feedback; sales rose by 12%.', 'goal-setting theory', 'specific, difficult goals with feedback direct attention and increase effort and persistence (Locke and Latham, 2002)')],
    apply=[('A school in Jakarta wants to use a points system to increase homework completion. Using biological and cognitive research on motivation, explain one benefit and one risk.', 'Benefit: points act as reward cues that drive anticipatory dopamine activity, increasing effort (Knutson et al., 2001). Risk: expected tangible rewards may undermine intrinsic interest (Deci et al., 1999) and encourage fixed, performance-focused goals.', 4),
           ('Explain how reward prediction error could explain why a surprise bonus feels more motivating than a regular expected payment.', 'An unexpected reward produces a positive prediction error and a burst of dopamine firing, strengthening learning and approach; a fully expected reward produces little phasic response because nothing is better than predicted.', 3),
           ('Using one study, explain how a brain-imaging technique has been used to investigate motivation.', 'Knutson et al. (2001) used fMRI with the monetary incentive delay task: nucleus accumbens BOLD activity increased with anticipated reward size and correlated with self-reported positive arousal, showing anticipation of reward is linked to the ventral striatum.', 4),
           ('A teenager plays a smartphone game for hours even though he says he no longer enjoys it. Use the wanting-liking distinction to explain this.', 'Repeated rewards have given game cues strong incentive salience through dopamine (wanting), while hedonic pleasure (liking) has declined; behaviour is driven by cue-triggered wanting (Berridge and Robinson).', 3)],
    evaluate=[('Motivation can be explained by dopamine activity in the brain.', ['Schultz et al. (1997) prediction error', 'Knutson et al. (2001) nucleus accumbens anticipation', 'Olds and Milner (1954) self-stimulation', 'dopamine agonists and compulsive behaviour'],
               ['reductionist - ignores beliefs, goals, culture', 'animal research generalisation', 'fMRI is correlational', 'cognitive evidence: mindset and goals (Mueller and Dweck, 1998)'],
               'Dopamine provides a key mechanism for reward learning and wanting, but a full explanation needs cognitive and sociocultural factors.'),
              ('Cognitive factors are more important than biological factors in motivation.', ['mindset and attributions predict persistence', 'goal-setting effects in work'],
               ['dopamine systems underlie reward anticipation', 'drugs that alter dopamine change motivation'],
               'Biological and cognitive factors interact - expectations are implemented in neural reward systems.')],
))
K.study('ch09-st2', 'Schultz, Dayan and Montague', 1997, 'dopamine and reward prediction error', 'to explain the firing of midbrain dopamine neurons during reward learning in terms of a prediction-error signal',
        'Recordings from single dopamine neurons in monkeys were analysed as the animals learned that a light or tone predicted a drop of juice; responses were compared with a computational temporal-difference learning model.',
        'neurons fired to unexpected juice; after learning they fired to the predictive cue instead, and their firing dipped below baseline when expected juice was omitted',
        'the reward prediction error role of dopamine',
        ['precise single-neuron recordings', 'links biology to a testable computational model'],
        ['animal research - generalisation to human motivation', 'invasive procedures raise ethical concerns', 'explains learning more than complex human goals'],
        wrong=['Dopamine neurons fired only when juice was delivered, even after learning', 'Dopamine firing increased when expected juice was omitted', 'Dopamine neurons did not respond to rewards'])
K.study('ch09-st2', 'Knutson et al.', 2001, 'anticipation of monetary reward', 'to investigate whether anticipation of increasing monetary rewards activates the nucleus accumbens',
        '8 healthy adults in the USA completed the monetary incentive delay task in an fMRI scanner: cues signalled possible gains or losses of $0.20, $1 or $5, which depended on pressing a button quickly when a target appeared.',
        'nucleus accumbens activity increased with the size of the anticipated reward but not anticipated loss, and correlated with self-reported happiness',
        'the role of the nucleus accumbens in reward anticipation',
        ['well-controlled task separating anticipation from outcome', 'combined brain and self-report measures'],
        ['very small sample', 'fMRI is correlational and has limited temporal resolution', 'small monetary rewards in an artificial setting'],
        mtype='laboratory experiment', iv='size of the anticipated reward or loss', dv='BOLD activity in the nucleus accumbens (and self-rated arousal)')
K.study('ch09-st2', 'Olds and Milner', 1954, 'self-stimulation of the brain in rats', 'to investigate whether stimulation of particular brain areas is rewarding',
        'Electrodes were implanted in the brains of rats in Montreal; pressing a lever delivered a brief electrical current to the electrode site.',
        'rats with electrodes in the septal area pressed the lever at very high rates - in some cases thousands of times per hour - whereas other sites did not produce lever pressing',
        'biological reward systems in the brain',
        ['clear causal manipulation of brain stimulation', 'founded research on reward circuits'],
        ['animal model', 'invasive procedure; welfare concerns', 'stimulation is unlike natural rewards'],
        mtype='laboratory experiment', ethics='Rats underwent brain surgery and electrode implantation; this requires strong justification under animal research guidelines (harm-benefit analysis, minimising suffering).')
K.study('ch09-st2', 'Mueller and Dweck', 1998, 'praise for intelligence and effort', 'to investigate the effect of praise for intelligence versus effort on children\'s motivation after failure',
        '128 fifth-grade children in the USA solved problems and were praised for intelligence ("you must be smart"), effort ("you must have worked hard") or given neutral feedback; they then experienced failure on a harder set and completed a third set.',
        'intelligence-praised children chose easier performance tasks, enjoyed the task less, persisted less and performed worse after failure than effort-praised children',
        'cognitive bases of motivation: mindset and goals',
        ['random allocation to praise conditions', 'several behavioural and self-report measures'],
        ['short-term laboratory effects', 'American children only', 'replication of mindset effects is mixed'],
        mtype='laboratory experiment', iv='type of praise (intelligence, effort or control)', dv='persistence, enjoyment and performance after failure')

K.facts('ch09-st3', F(
    terms=[('transtheoretical model', 'Prochaska and DiClemente\'s model in which people move through stages of change: precontemplation, contemplation, preparation, action and maintenance'),
           ('decisional balance', 'a person\'s weighing of the pros and cons of changing a behaviour'),
           ('self-efficacy', 'Bandura\'s term for belief in one\'s ability to carry out a behaviour successfully'),
           ('motivational interviewing', 'a client-centred counselling style that strengthens a person\'s own motivation to change by exploring ambivalence'),
           ('autonomous health motivation', 'engaging in health behaviour because one personally values it, which predicts long-term maintenance'),
           ('warm glow', 'the positive feeling people experience from giving or helping'),
           ('prosocial spending', 'spending money on others or on charity rather than on oneself')],
    facts=[('In the transtheoretical model, a person who has changed their behaviour within the last six months is in the:', 'Action stage', ['Maintenance stage', 'Preparation stage', 'Contemplation stage'],
            'Maintenance begins once change has lasted more than six months.'),
           ('Williams et al. (1996) found that weight loss in a medically supervised programme was predicted by:', 'Autonomous motivation for participating', ['Body weight at the start only', 'Being paid to attend', 'The number of programme leaflets read'],
            'Autonomous motivation also predicted maintenance at 23 months.'),
           ('Dunn, Aknin and Norton (2008) found that people who were told to spend money on others:', 'Were happier at the end of the day than those who spent on themselves', ['Were less happy than those who spent on themselves', 'Were only happier if they spent $20', 'Showed no difference in happiness'],
            'The amount ($5 or $20) did not matter.'),
           ('Warneken and Tomasello (2008) found that toddlers who were given a toy as a reward for helping:', 'Helped less in a later phase than toddlers who were praised or not rewarded', ['Helped more than all other groups', 'Never helped in the first place', 'Helped the same as other groups'],
            'Extrinsic rewards undermined intrinsic helping even at 20 months.'),
           ('A key technique of motivational interviewing is:', 'Eliciting the person\'s own reasons for change and exploring ambivalence', ['Confronting the person with frightening information', 'Prescribing a strict plan the person must follow', 'Rewarding every small change with money'],
            'MI is collaborative and supports autonomy.')],
    why=[('Explain why autonomous motivation is important for long-term health behaviour change.', 'Behaviour that is self-endorsed is more stable: when external pressure or rewards stop, autonomously motivated people continue, as in Williams et al. (1996), where autonomous reasons predicted weight-loss maintenance at 23 months.'),
         ('Explain how the transtheoretical model can be used to design health interventions.', 'Interventions are matched to the person\'s stage: raising awareness for precontemplators, resolving ambivalence for contemplators, planning for preparation, and relapse-prevention for action and maintenance.'),
         ('Explain why people help others according to motivational research.', 'Helping can be intrinsically motivated (empathy, warm glow, autonomy), with prosocial spending increasing happiness (Dunn et al., 2008); external rewards can undermine helping (Warneken and Tomasello, 2008), and autonomous helping benefits both helper and recipient (Weinstein and Ryan, 2010).')],
    contrast=[('the contemplation stage', 'the preparation stage', 'In contemplation the person intends to change within six months but is ambivalent; in preparation the person intends to act within a month and has begun small steps or plans.'),
              ('autonomous helping', 'controlled helping', 'Autonomous helping is chosen and valued by the helper and increases well-being; controlled helping is done because of pressure or reward and gives less benefit to helper and recipient.')],
    misc=[('People move through the stages of change in a straight line from precontemplation to maintenance.', 'Movement is often cyclical: many people relapse and re-enter earlier stages before achieving maintenance.'),
          ('Paying people to help others always increases helping.', 'Extrinsic rewards can undermine intrinsic prosocial motivation (Warneken and Tomasello, 2008); payment may also shift the meaning of helping from moral to economic.')],
    cases=[('a smoking cessation clinic in Bogotá', 'A clinic assesses each patient\'s stage of change; precontemplators receive information about risks, contemplators receive motivational interviewing, and those in action receive coping-skills sessions.', 'the transtheoretical model', 'matching the intervention to the stage of readiness aims to move each person forward rather than giving everyone the same programme'),
           ('volunteering at a food bank in Leeds', 'Students who chose to volunteer at a food bank reported greater satisfaction and continued for longer than students required to volunteer for a course credit.', 'autonomous vs controlled prosocial motivation', 'autonomous helping satisfies autonomy and relatedness needs, increasing well-being and persistence (Weinstein and Ryan, 2010)'),
           ('diabetes self-care in Chennai', 'Nurses in Chennai trained to give patients choices and rationales for diet and medication found improved glucose control compared with a standard advice clinic.', 'SDT in health behaviour', 'autonomy-supportive care increased autonomous motivation and perceived competence, supporting long-term self-management'),
           ('a "giving day" at a company in Tokyo', 'Employees were each given 3,000 yen to spend on a colleague or a charity; surveys afterwards showed higher happiness and team cohesion.', 'prosocial spending', 'consistent with Dunn et al. (2008), spending on others produces a warm glow and strengthens relatedness')],
    apply=[('A university in Sydney wants students to exercise more. Using the transtheoretical model, suggest how it could tailor its campaign.', 'Precontemplation: information on benefits; contemplation: decisional-balance work and MI; preparation: help to plan and sign up; action: reminders and social support; maintenance: relapse-prevention strategies.', 6),
           ('Explain how motivational interviewing could help a young person in Nairobi who is ambivalent about reducing alcohol use.', 'The counsellor uses open questions, reflective listening and affirmations to explore pros and cons, elicits change talk and the person\'s own reasons, and supports autonomy rather than confronting; this resolves ambivalence and builds self-efficacy.', 4),
           ('A charity wants to recruit more blood donors. Using research on motivation, explain one reason why offering cash might backfire.', 'Cash may crowd out intrinsic, altruistic motivation (as rewards undermined toddlers\' helping in Warneken and Tomasello, 2008), reframing donation as a transaction and reducing donation among those who gave for moral reasons.', 3)],
    evaluate=[('The transtheoretical model is a useful explanation of health behaviour change.', ['Prochaska and DiClemente (1983): processes of change differ by stage', 'practical guide for tailoring interventions', 'recognises relapse'],
               ['stages are arbitrary time-based categories', 'stage-matched interventions are not always more effective', 'ignores social and economic factors'],
               'Useful as a practical framework, but limited as a causal explanation.'),
              ('Prosocial behaviour is mainly motivated by self-interest.', ['warm glow and happiness benefits (Dunn et al., 2008)', 'arousal-cost-reward model'],
               ['empathy-altruism (Batson et al., 1981)', 'toddlers help without reward (Warneken and Tomasello, 2008)', 'rewards can undermine helping'],
               'Both self-interested and altruistic motives operate; intrinsic prosocial motivation is evident early in development.')],
))
K.study('ch09-st3', 'Prochaska and DiClemente', 1983, 'stages and processes of self-change in smoking', 'to investigate whether smokers use different processes of change at different stages',
        '872 adult smokers and ex-smokers in the USA who were changing on their own completed questionnaires on the processes of change they used; they were classified into stages such as precontemplation, contemplation, action and maintenance.',
        'people at different stages used different processes - e.g. contemplators used consciousness raising most, while those in action and maintenance used more behavioural processes such as reinforcement and helping relationships',
        'the transtheoretical model of health behaviour change',
        ['large sample of real self-changers', 'practical framework for tailoring interventions'],
        ['self-report questionnaires', 'mainly cross-sectional - cannot show movement between stages', 'stage boundaries are arbitrary'])
K.study('ch09-st3', 'Williams et al.', 1996, 'motivational predictors of weight loss', 'to investigate whether autonomous motivation predicts weight loss and its maintenance',
        '128 severely obese adults in a six-month medically supervised weight-loss programme in the USA completed questionnaires on their reasons for participating and their perceptions of staff autonomy support; weight and attendance were tracked up to 23 months.',
        'autonomous motivation predicted better attendance, greater weight loss and maintenance of weight loss at 23 months; perceived autonomy support from staff predicted autonomous motivation',
        'self-determination theory applied to health behaviour',
        ['objective outcome (weight) over almost two years', 'tests SDT in a real clinical setting'],
        ['correlational - cannot show causation', 'self-report of motivation', 'specific clinical sample'],
        mtype='longitudinal study')
K.study('ch09-st3', 'Dunn, Aknin and Norton', 2008, 'prosocial spending and happiness', 'to test whether spending money on others increases happiness more than spending on oneself',
        '46 participants in Vancouver rated their happiness in the morning, were given $5 or $20 and told to spend it by 5 pm on themselves or on others; happiness was rated again in the evening.',
        'those who spent on others were happier at the end of the day than those who spent on themselves; the amount of money did not matter',
        'prosocial behaviour and well-being',
        ['random allocation in a real-life setting', 'supported by correlational survey data in the same paper'],
        ['small sample', 'short-term self-report of happiness', 'participants may have guessed the aim'],
        mtype='field experiment', iv='spending target (self or others) and amount ($5 or $20)', dv='self-reported happiness in the evening')
K.study('ch09-st3', 'Warneken and Tomasello', 2008, 'rewards and toddlers\' helping', 'to investigate whether extrinsic rewards undermine young children\'s helping',
        '36 20-month-old children in Leipzig had many opportunities to help an adult (e.g. retrieving an out-of-reach object); in the treatment phase they received a toy reward, praise or nothing for helping; a test phase followed with no rewards.',
        'children who had received a material reward helped less often in the test phase than children who had been praised or received nothing',
        'intrinsic prosocial motivation and the undermining effect',
        ['controlled behavioural measure', 'very young children - helping before strong socialisation'],
        ['small sample from one city', 'artificial helping tasks', 'short-term effect'],
        mtype='laboratory experiment', iv='type of reward for helping (material reward, praise or none)', dv='frequency of helping in the test phase')

# ============================================================================================
# Chapter 10 - HL Extension: Technology
# ============================================================================================
K.facts('ch10-st1', F(
    terms=[('functional MRI (fMRI)', 'a brain-imaging technique that measures changes in blood oxygenation (the BOLD signal) as an indirect index of neural activity, with good spatial but limited temporal resolution'),
           ('electroencephalography (EEG)', 'recording the brain\'s electrical activity through scalp electrodes, with millisecond temporal resolution but poor spatial resolution'),
           ('eye-tracking', 'recording where and for how long a person looks, using infrared cameras to measure fixations and saccades'),
           ('fixation', 'a pause of the eyes on one location, typically around 200-250 ms in reading'),
           ('saccade', 'a rapid eye movement between fixations, during which little visual information is taken in'),
           ('online experiment', 'an experiment run over the internet, often through platforms such as Amazon Mechanical Turk or Prolific'),
           ('experience sampling', 'repeatedly prompting participants (often by smartphone) to report their current state and activity in everyday life'),
           ('transcranial magnetic stimulation (TMS)', 'a technique that uses magnetic pulses to temporarily disrupt or excite activity in a brain region, allowing causal inferences')],
    facts=[('Buhrmester, Kwang and Gosling (2011) concluded that data collected through Amazon Mechanical Turk were:', 'At least as reliable as data from traditional methods', ['Much less reliable than student samples', 'Unusable for psychological research', 'Reliable only if participants were paid over $10'],
            'MTurk samples were also more demographically diverse than typical US college samples.'),
           ('Which technique has the best temporal resolution for measuring brain activity?', 'EEG', ['fMRI', 'PET', 'Structural MRI'],
            'EEG records electrical changes in milliseconds.'),
           ('Eisenberger, Lieberman and Williams (2003) found that being excluded in the Cyberball game increased activity in the:', 'Dorsal anterior cingulate cortex', ['Primary visual cortex', 'Cerebellum', 'Hippocampus only'],
            'This region is also active during physical pain.'),
           ('In eye-tracking studies of reading, a saccade is:', 'A rapid movement of the eyes between fixations', ['A long pause on a difficult word', 'A blink caused by fatigue', 'The total time spent reading a sentence'],
            'Information is taken in mainly during fixations.'),
           ('A major advantage of TMS over fMRI is that TMS:', 'Can show that a brain area is necessary for a task by temporarily disrupting it', ['Has better spatial resolution of the whole brain', 'Measures blood oxygen directly', 'Requires no ethical safeguards'],
            'fMRI is correlational; TMS manipulates activity.')],
    why=[('Explain why fMRI findings are described as correlational.', 'fMRI shows which areas change their BOLD signal during a task, but the activity may accompany rather than cause the behaviour; to show necessity researchers use lesion or TMS methods.'),
         ('Explain how eye-tracking can provide evidence about cognitive processes.', 'Fixation duration and location reflect processing difficulty and attention - e.g. longer fixations on unfamiliar words and regressions after ambiguous phrases (Rayner, 1998) - providing an objective, moment-by-moment measure that does not rely on self-report.'),
         ('Explain two advantages of online experiments.', 'Large, diverse samples can be recruited quickly and cheaply (Buhrmester et al., 2011); procedures are standardised by software, reducing experimenter effects; participants can take part from many countries.')],
    contrast=[('fMRI', 'EEG', 'fMRI measures the BOLD signal with high spatial but low temporal resolution; EEG measures electrical activity with high temporal but low spatial resolution.'),
              ('a laboratory experiment', 'an online experiment', 'A laboratory experiment controls the setting and supervises participants; an online experiment reaches larger, more diverse samples but loses control over the environment, attention and identity of participants.')],
    misc=[('Brain scans show exactly what a person is thinking.', 'Imaging shows patterns of activity averaged over time and participants; inferring specific thoughts from activation (reverse inference) is unreliable.'),
          ('Online samples are always less valid than student samples.', 'Online samples are often more diverse than university samples and give comparable reliability, although attention checks and fraud detection are needed.')],
    cases=[('Cyberball in an fMRI scanner', 'Students in Los Angeles played a ball-tossing computer game while being scanned; after a few throws the other two "players" stopped throwing to them.', 'brain imaging and social pain', 'fMRI showed increased dorsal anterior cingulate activity during exclusion, similar to physical pain (Eisenberger et al., 2003)'),
           ('eye-tracking food labels', 'Researchers in Copenhagen used eye-tracking glasses in a supermarket and found that shoppers spent on average less than half a second looking at nutrition labels.', 'eye-tracking as a research tool', 'objective gaze data revealed attention to labels that self-report would probably overestimate'),
           ('a global online Cyberball study', 'Williams, Cheung and Choi (2000) ran Cyberball online with 1,486 participants from 62 countries; excluded participants reported lower belonging and self-esteem.', 'online experiments', 'the internet allowed a very large international sample, though control over the setting was lower'),
           ('EEG and reading in Helsinki', 'Researchers recorded EEG while Finnish children read sentences; an N400 brain wave appeared about 400 ms after a word that did not fit the meaning of the sentence.', 'EEG as a research tool', 'millisecond temporal resolution showed exactly when meaning was processed')],
    apply=[('A researcher in Seoul wants to know whether a brain area is necessary for recognising faces. Explain why she might use TMS rather than fMRI.', 'fMRI would only show that the area is active during face recognition (correlation); TMS temporarily disrupts the area, so if recognition worsens, it shows the area is necessary (causal inference).', 3),
           ('Design an eye-tracking study to test whether students in Madrid read online news headlines or skip them. Identify the measures you would record.', 'Participants read a news webpage while an eye-tracker records fixation count and duration on headlines, saccade paths and regressions; compare time on headlines vs body text; ensure consent for recording.', 4),
           ('Explain two ways a researcher running an online experiment could protect the validity of her data.', 'Use attention-check questions and exclude failures; prevent repeat participation (IP/ID checks); record completion times and exclude implausibly fast responses; use standardised instructions and practice trials.', 4)],
    evaluate=[('Technology has improved the validity of psychological research.', ['objective measures (eye-tracking, EEG)', 'imaging links behaviour to the brain', 'online samples are larger and more diverse'],
               ['fMRI is correlational and expensive', 'artificial scanner settings reduce ecological validity', 'online studies lose control; digital divide in samples'],
               'Technology has added objective and large-scale measures, but each tool has validity limits that must be considered.')],
))
K.study('ch10-st1', 'Eisenberger, Lieberman and Williams', 2003, 'social exclusion in Cyberball', 'to investigate whether social exclusion activates brain regions associated with physical pain',
        '13 university students in the USA played the Cyberball ball-tossing game in an fMRI scanner, first watching (implicit exclusion), then being included, and finally being excluded by the other two "players".',
        'exclusion increased activity in the dorsal anterior cingulate cortex, and this activity correlated with self-reported distress; right ventral prefrontal activity was associated with lower distress',
        'brain imaging of social pain',
        ['combines fMRI with self-report', 'standardised computer paradigm'],
        ['very small sample', 'artificial game in a scanner', 'fMRI is correlational'],
        mtype='laboratory experiment', iv='inclusion versus exclusion in the Cyberball game', dv='BOLD activity in the anterior cingulate cortex and self-reported distress',
        ethics='Participants were deceived that they were playing with other people and were deliberately excluded; debriefing was needed to remove any distress.')
K.study('ch10-st1', 'Buhrmester, Kwang and Gosling', 2011, 'Amazon Mechanical Turk as a research tool', 'to evaluate whether Mechanical Turk provides high-quality data for psychological research',
        'The researchers analysed MTurk participants\' demographics, measured the effects of different payment rates and task lengths on participation, and assessed the test-retest reliability of standard personality measures.',
        'MTurk participants were more demographically diverse than typical American college samples; payment affected participation rate but not data quality; reliability was at least as high as traditional methods',
        'online data collection',
        ['practical evidence for a widely used method', 'large samples analysed'],
        ['MTurk workers may be "professional" participants', 'mostly US and Indian workers', 'self-report measures only'])
K.study('ch10-st1', 'Rayner', 1998, 'eye movements in reading', 'to review twenty years of eye-tracking research on reading and information processing',
        'A review of eye-tracking studies in which readers\' fixations, saccades and regressions were recorded while they read text.',
        'readers fixate most words for about 200-250 ms and make saccades of about 7-9 letter spaces; fixations are longer on low-frequency and unpredictable words, showing that eye movements reflect ongoing cognitive processing',
        'eye-tracking as evidence about cognition',
        ['objective and fine-grained measure', 'very large body of converging research'],
        ['mostly alphabetic languages and skilled adult readers', 'lab reading differs from everyday reading'])
K.study('ch10-st1', 'Williams, Cheung and Choi', 2000, 'cyberostracism on the internet', 'to investigate whether being ostracised by strangers in an online game causes distress',
        '1,486 participants from 62 countries played the Cyberball game online and were included or excluded to varying degrees by two computer-controlled "players".',
        'the more participants were excluded, the worse they felt and the lower their reported belonging and self-esteem, even though the other players were strangers on the internet',
        'online experiments and the effects of exclusion',
        ['very large international sample', 'standardised procedure'],
        ['little control over participants\' environment', 'self-selected internet users', 'deception online - debriefing harder to ensure'],
        iv='degree of inclusion in the online ball game', dv='self-reported belonging, self-esteem and mood')

TOOL_SCEN = [
    ('A researcher wants to know exactly when (to the millisecond) the brain detects a grammatical error in a sentence.', 'EEG (event-related potentials)'),
    ('A researcher wants to locate which brain areas are more active when people view faces of their own versus another ethnic group.', 'fMRI'),
    ('A researcher wants to know whether readers look back (regress) at earlier words when a sentence is ambiguous.', 'Eye-tracking'),
    ('A researcher wants to recruit 3,000 adults from 40 countries for a short reaction-time task within a week.', 'An online experiment platform'),
    ('A researcher wants to measure how adolescents\' mood changes over the day in relation to social media use in real life.', 'Experience sampling via smartphone'),
    ('A researcher wants to test whether a region of the left prefrontal cortex is necessary for verbal fluency.', 'Transcranial magnetic stimulation (TMS)'),
    ('A researcher wants to find out which parts of a website advertisement shoppers notice first.', 'Eye-tracking'),
    ('A researcher wants to compare the timing of brain responses to angry and neutral faces in infants, using a cheap, safe method.', 'EEG (event-related potentials)'),
]
TOOLS = ['EEG (event-related potentials)', 'fMRI', 'Eye-tracking', 'An online experiment platform', 'Experience sampling via smartphone', 'Transcranial magnetic stimulation (TMS)']


@K.add('ch10-st1', ('C3',), (1, 4), 'mcq')
def choose_tool(rng, slot):
    sc, tool = rng.choice(TOOL_SCEN)
    frame = rng.choice(['Which technology is most suitable?', 'Which research tool would best answer this question?', 'Identify the most appropriate technique.'])
    wrongs = [t for t in TOOLS if t != tool]
    rng.shuffle(wrongs)
    why = {'EEG (event-related potentials)': 'EEG has millisecond temporal resolution and is safe and inexpensive.',
           'fMRI': 'fMRI has good spatial resolution to locate active brain regions.',
           'Eye-tracking': 'Eye-tracking records fixations, saccades and regressions.',
           'An online experiment platform': 'Online platforms allow fast recruitment of large international samples.',
           'Experience sampling via smartphone': 'Experience sampling records states repeatedly in everyday life.',
           'Transcranial magnetic stimulation (TMS)': 'TMS temporarily disrupts a region, allowing causal inference.'}[tool]
    return mcq(rng, f'{sc} {frame}', tool, wrongs[:3], why)


RT_CTX = [('an online Stroop task', 'Prolific'), ('an online lexical decision task', 'a university website'),
          ('a reaction-time game on smartphones', 'an app'), ('an online visual search task', 'Amazon Mechanical Turk')]


@K.add('ch10-st1', ('C3',), (2, 5), 'numerical')
def rt_clean(rng, slot):
    task, plat = rng.choice(RT_CTX)
    n = 8 if slot.d <= 3 else 10
    vals = [rng.randint(35, 120) * 10 for _ in range(n)]
    vals[rng.randrange(n)] = rng.choice([120, 150, 90])
    vals[rng.randrange(n)] = rng.choice([2600, 3400, 4100])
    lo, hi = 200, 2000
    keep = [v for v in vals if lo <= v <= hi]
    if len(keep) == n or len(keep) < n - 3:
        return None
    mean_all = sum(vals) / n
    mean_k = sum(keep) / len(keep)
    stem = (f'One participant\'s reaction times (ms) in {task} run through {plat} were: {", ".join(map(str, vals))}. '
            f'The researcher\'s pre-registered rule excludes responses faster than {lo} ms or slower than {hi} ms. '
            'Calculate the mean before and after applying the rule, and explain why such a rule is especially important in online experiments.')
    return dict(stem=stem, type='numerical', marks=4,
                answer=f'Mean of all {n} = {mean_all:.1f} ms; after excluding {n - len(keep)} response(s), mean of {len(keep)} = {mean_k:.1f} ms. '
                       'Online participants cannot be supervised, so very fast responses (anticipations/random clicking) and very slow ones (distraction) are more likely; the rule removes them consistently.',
                markingKey=f'A1 {mean_all:.1f} ms. M1 correct exclusions ({", ".join(str(v) for v in vals if not lo <= v <= hi)}). A1 {mean_k:.1f} ms. '
                           'R1 lack of control over environment/attention online; pre-registration avoids researcher bias.')


K.facts('ch10-st2', F(
    terms=[('Google effect (digital amnesia)', 'the tendency to forget information that we expect to be able to find online'),
           ('transactive memory', 'a shared memory system in which people rely on others - or devices - to store some information'),
           ('cognitive offloading', 'using external tools such as phones or notes to reduce the demands on memory and attention'),
           ('Goldilocks hypothesis', 'Przybylski and Weinstein\'s proposal that moderate digital screen use is not harmful and may be beneficial, while excessive use is linked to lower well-being'),
           ('problematic smartphone use', 'compulsive smartphone use that interferes with daily functioning'),
           ('social comparison', 'evaluating oneself by comparing with others, often upwards on social media'),
           ('displacement hypothesis', 'the idea that screen time harms well-being by replacing beneficial activities such as sleep, exercise and face-to-face contact'),
           ('specification curve analysis', 'a method that runs all reasonable analyses of a dataset to show how much conclusions depend on analytic choices')],
    facts=[('Sparrow, Liu and Wegner (2011) found that participants who believed typed trivia statements would be saved on the computer:', 'Remembered the statements less well than those who believed they would be erased', ['Remembered them better', 'Remembered them equally', 'Could not remember where they were saved'],
            'People remembered where information was stored better than the information itself.'),
           ('Przybylski and Weinstein (2017) studied over 120,000 English 15-year-olds and found that:', 'Moderate digital screen use was not associated with lower well-being', ['Any screen use reduced well-being substantially', 'Screen use had no relationship with well-being at any level', 'Only weekend screen use mattered'],
            'This supports the Goldilocks hypothesis.'),
           ('Kross et al. (2013) used experience sampling and found that the more people used Facebook at one time point:', 'The worse they felt at the next time point', ['The happier they felt afterwards', 'The less lonely they reported being', 'The more their life satisfaction increased'],
            'Feeling bad did not predict later Facebook use, which suggests the direction ran from use to mood.'),
           ('Hunt et al. (2018) found that students who limited social media to 10 minutes per platform per day for three weeks:', 'Showed reduced loneliness and depression compared with controls', ['Became more depressed', 'Showed no change at all', 'Reported more fear of missing out only'],
            'This was an experiment, so it allows causal conclusions.'),
           ('Orben and Przybylski (2019) estimated that technology use explained about what percentage of the variation in adolescent well-being?', 'At most about 0.4%', ['About 25%', 'About 50%', 'About 10%'],
            'They compared it to the association with eating potatoes.'),
           ('Mueller and Oppenheimer (2014) found that students who took lecture notes on laptops:', 'Performed worse on conceptual questions than longhand note-takers', ['Performed better on all questions', 'Wrote fewer words', 'Took notes in their own words more often'],
            'Laptop users tended to transcribe verbatim; later replications found smaller or no effects.')],
    why=[('Explain how digital technology may affect memory.', 'People offload information to devices and treat the internet as a transactive memory partner; they remember where information can be found rather than the information itself (Sparrow et al., 2011), which saves effort but may reduce deep encoding.'),
         ('Explain why it is difficult to establish whether social media causes poor well-being.', 'Most studies are correlational and self-report; the relationship may be bidirectional or due to third variables (e.g. loneliness, sleep); effects are small and depend on analytic choices (Orben and Przybylski, 2019); experiments such as Hunt et al. (2018) are short-term.'),
         ('Explain how digital technology can affect relationships.', 'It can maintain long-distance ties and support marginalised groups, but phone presence can reduce conversation quality ("phubbing"), and social comparison or online conflict can harm relationships.'),
         ('Explain the displacement hypothesis.', 'Screen time may harm well-being not directly but by displacing beneficial activities such as sleep, exercise and face-to-face interaction; harm is therefore expected mainly at high levels of use.')],
    contrast=[('passive social media use', 'active social media use', 'Passive use (scrolling, viewing others\' posts) is more linked to upward social comparison and lower well-being; active use (messaging, posting, interacting) can increase connectedness.'),
              ('correlational studies of screen time', 'experimental studies of screen time', 'Correlational studies examine natural associations in large samples but cannot show causation; experiments manipulate use (e.g. Hunt et al., 2018) and allow causal claims but are short and small.')],
    misc=[('Research has proven that smartphones are destroying a generation\'s mental health.', 'Associations are small and mostly correlational; effect sizes are comparable to everyday factors (Orben and Przybylski, 2019); some moderate use is linked to benefits.'),
          ('Using the internet to find information makes people less intelligent.', 'Offloading changes what we remember (where vs what) but frees resources; there is no clear evidence of reduced intelligence.')],
    cases=[('a phone-free school policy in Oslo', 'A secondary school in Oslo banned smartphones during the school day; teachers reported more conversation at break times and slightly improved grades among lower-achieving pupils.', 'effects of technology on relationships and cognition', 'removing phones may reduce distraction and displacement of face-to-face interaction, though the evidence is natural and not controlled'),
           ('taking photos at a museum', 'Visitors to an art museum in New York who photographed objects later remembered fewer details about them than visitors who simply observed them (Henkel, 2014).', 'cognitive offloading', 'relying on the camera to "remember" reduced encoding of the objects - the photo-taking impairment effect'),
           ('a WhatsApp family group in Manila', 'Filipino nurses working abroad keep daily contact with their children through video calls and a family group chat, reporting that it helps them feel close despite distance.', 'technology and relationships', 'digital communication can maintain relatedness across distance, showing technology is not only harmful'),
           ('a teenager in Toronto and Instagram', 'A 15-year-old spends hours scrolling through influencers\' posts and reports feeling worse about her body afterwards.', 'social comparison and well-being', 'passive use promotes upward comparison with idealised images, linked to lower body satisfaction and mood'),
           ('action video games and attention', 'Green and Bavelier (2003) found that non-gamers trained for 10 hours on an action game improved on visual attention tasks more than those trained on Tetris.', 'positive effects of digital technology on cognition', 'experimental evidence that some technology use can enhance attentional capacity')],
    apply=[('A parent in Dubai asks whether her son\'s 2 hours of gaming per day will harm his well-being. Using research, give a balanced answer.', 'Moderate use is not linked to lower well-being (Przybylski and Weinstein, 2017); effects are small (Orben and Przybylski, 2019); risks come from displacement of sleep/exercise and problematic use; content and social context matter.', 4),
           ('Using one study, explain how technology may affect memory.', 'Sparrow et al. (2011): believing information would be saved reduced recall of it but improved memory for where it was stored, showing cognitive offloading/transactive memory with the computer.', 4),
           ('Design an experiment to test whether limiting social media use improves sleep in university students in Kuala Lumpur.', 'Randomly allocate students to a limit (e.g. 30 min/day, monitored by screen-time apps) or usual use for three weeks; DV: sleep duration/quality (sleep diary or actigraphy); control for baseline; ethical: consent, right to withdraw, data privacy.', 6),
           ('Explain one strength and one limitation of using experience sampling to study the effects of Facebook on mood.', 'Strength: repeated real-time reports reduce recall bias and allow temporal order to be examined (Kross et al., 2013). Limitation: still correlational; prompts may change behaviour (reactivity); self-report.', 4)],
    evaluate=[('Digital technology has a negative effect on adolescent well-being.', ['Kross et al. (2013): Facebook use predicts lower mood', 'Hunt et al. (2018): limiting use reduces loneliness and depression', 'social comparison and displacement'],
               ['Przybylski and Weinstein (2017): moderate use not harmful', 'Orben and Przybylski (2019): tiny effect sizes', 'benefits for connection and support', 'mostly correlational evidence'],
               'Heavy and passive use may be harmful for some adolescents, but average effects are small and context-dependent.'),
              ('Technology improves human cognition.', ['action games improve attention (Green and Bavelier, 2003)', 'offloading frees cognitive resources'],
               ['Google effect (Sparrow et al., 2011)', 'multitasking costs (Ophir et al., 2009)', 'photo-taking impairment'],
               'Technology changes rather than simply improves or harms cognition; outcomes depend on how it is used.')],
))
K.study('ch10-st2', 'Sparrow, Liu and Wegner', 2011, 'the Google effect on memory', 'to investigate whether expecting to have future access to information reduces memory for it',
        'Harvard students typed 40 trivia statements into a computer; half were told the computer would save them and half that they would be erased; recall of the statements, and memory for the folder where each was saved, were then tested.',
        'participants who believed the statements would be erased recalled more of them; participants remembered where information was stored better than the information itself',
        'cognitive offloading and the internet as transactive memory',
        ['controlled manipulation of expectation', 'a series of four experiments with converging results'],
        ['student sample', 'artificial trivia task', 'some later replication attempts found weaker effects'],
        mtype='laboratory experiment', iv='whether participants believed the information would be saved or erased', dv='number of statements recalled',
        wrong=['Believing the information was saved improved recall', 'Participants remembered statements better than where they were stored', 'Expectation of access had no effect on recall'])
K.study('ch10-st2', 'Przybylski and Weinstein', 2017, 'the Goldilocks hypothesis', 'to test whether the relationship between digital screen time and adolescent well-being is non-linear',
        'Over 120,000 15-year-olds in England reported their time on films, games, computers and smartphones on weekdays and weekends and completed the Warwick-Edinburgh Mental Well-Being Scale.',
        'moderate use was not harmful and was slightly associated with higher well-being; well-being declined only above certain levels (e.g. about 1 h 57 min of smartphone use on weekdays), and the effects were small',
        'effects of digital technology on well-being',
        ['very large representative sample', 'tested a precise, non-linear hypothesis'],
        ['self-report of screen time is inaccurate', 'correlational - cannot show causation', 'one cultural context'],
        mtype='correlational study')
K.study('ch10-st2', 'Kross et al.', 2013, 'Facebook use and well-being', 'to investigate whether Facebook use predicts changes in subjective well-being over time',
        '82 young adults in Ann Arbor, USA, were sent text messages five times a day for two weeks asking how they felt, how lonely they were and how much they had used Facebook since the last message.',
        'the more participants used Facebook at one time point, the worse they felt at the next, and the more they used it over two weeks, the more their life satisfaction declined; feeling bad did not predict later Facebook use',
        'social media use and well-being',
        ['experience sampling reduces recall bias', 'time-lagged design suggests direction of effect'],
        ['small sample from one US city', 'correlational; third variables possible', 'self-report'],
        mtype='correlational study')
K.study('ch10-st2', 'Hunt et al.', 2018, 'limiting social media use', 'to test experimentally whether limiting social media use improves well-being',
        '143 undergraduates at the University of Pennsylvania were randomly assigned to limit Facebook, Instagram and Snapchat to 10 minutes per platform per day for three weeks, or to use them as usual; usage was checked with iPhone battery screenshots.',
        'the limited-use group showed significant reductions in loneliness and depression compared with the control group; both groups showed reduced anxiety and fear of missing out',
        'causal effects of social media on well-being',
        ['random allocation allows causal inference', 'objective tracking of usage'],
        ['short three-week period', 'one university', 'participants knew the aim - demand characteristics'],
        mtype='randomised controlled trial', iv='social media use (limited to 10 minutes per platform per day vs usual use)', dv='scores on measures of loneliness and depression')
K.study('ch10-st2', 'Mueller and Oppenheimer', 2014, 'the pen is mightier than the keyboard', 'to compare the effects of laptop and longhand note-taking on learning',
        'Students at Princeton watched TED talks and took notes either on a laptop or by hand; they were then tested on factual and conceptual questions.',
        'both groups did similarly on factual questions, but laptop users performed worse on conceptual questions and transcribed lectures more verbatim',
        'effects of technology on learning and cognition',
        ['controlled comparison with identical lectures', 'analysis of note content explains the effect'],
        ['short videos rather than real lectures', 'Morehead et al. (2019) failed to replicate the effect clearly', 'students from one elite university'],
        mtype='laboratory experiment', iv='note-taking method (laptop or longhand)', dv='scores on factual and conceptual questions')

K.facts('ch10-st3', F(
    terms=[('informed consent (online)', 'agreement to participate given with full knowledge of the purpose and risks; accepting a platform\'s terms of service is not usually regarded as adequate consent for research'),
           ('data privacy', 'participants\' right to control how their personal data are collected, stored and shared'),
           ('anonymisation', 'removing information that could identify participants from a dataset'),
           ('algorithmic bias', 'systematic unfairness in the outputs of an AI system, often because of biased training data or proxy variables'),
           ('digital footprint', 'the data trail people leave online, such as likes, searches and location data'),
           ('GDPR', 'the European Union\'s General Data Protection Regulation (2018), which requires a lawful basis, data minimisation and rights of access and erasure')],
    facts=[('The main ethical criticism of Kramer, Guillory and Hancock (2014) was that:', 'Users\' emotions were manipulated without specific informed consent', ['The sample size was too small', 'Participants were paid too much', 'The results were not published'],
            'Facebook relied on its Data Use Policy rather than research consent.'),
           ('Kosinski, Stillwell and Graepel (2013) showed that Facebook likes could predict:', 'Private traits such as sexual orientation and political views', ['Only users\' favourite films', 'Nothing beyond chance', 'Exact home addresses'],
            'This raised concerns about privacy and digital footprints.'),
           ('Obermeyer et al. (2019) found that a US healthcare algorithm underestimated Black patients\' needs because it:', 'Used past healthcare costs as a proxy for health needs', ['Was given patients\' ethnicity directly', 'Was trained only on children', 'Was never tested on real data'],
            'Less money had historically been spent on Black patients with the same level of need.'),
           ('Fitzpatrick, Darcy and Vierhile (2017) found that students using the Woebot chatbot for two weeks:', 'Showed a significantly greater reduction in depression symptoms than an information-only control group', ['Became more anxious than controls', 'Showed no change in any measure', 'Refused to use the chatbot'],
            'The study was small and short, and the developers were involved.')],
    why=[('Explain why research using social media data raises ethical issues.', 'Users may not know their data are being studied, so informed consent is lacking; even anonymised data can often be re-identified; manipulation of feeds can cause harm (Kramer et al., 2014); the line between public and private data is unclear.'),
         ('Explain how AI can be biased in psychological or health applications.', 'AI learns from historical data that may reflect inequalities; proxy variables (e.g. cost for need) can encode bias (Obermeyer et al., 2019); unrepresentative training samples reduce accuracy for under-represented groups.'),
         ('Explain the ethical benefits and risks of AI chatbots for mental health.', 'Benefits: accessible, low-cost, anonymous support (Fitzpatrick et al., 2017). Risks: inadequate response to crises, data privacy, lack of accountability, over-reliance and limited evidence from independent trials.')],
    contrast=[('anonymity', 'confidentiality', 'Anonymity means that the participant\'s identity is never collected or cannot be linked to data; confidentiality means identity is known to researchers but protected and not disclosed.'),
              ('consent to terms of service', 'informed consent for research', 'Terms of service are general agreements to use a platform; informed consent for research requires specific information about the study\'s aims, procedures, risks and the right to withdraw.')],
    misc=[('Data posted publicly online can be used for any research without ethical considerations.', 'Researchers must still consider users\' expectations of privacy, potential harm, re-identification risk and context; many ethics committees require review.'),
          ('AI systems are objective because they are computers.', 'AI reproduces biases present in its training data and design choices, as shown by Obermeyer et al. (2019).')],
    cases=[('the Facebook emotional contagion study', 'In one week in 2012, Facebook altered the news feeds of 689,003 users to show fewer positive or fewer negative posts and measured the emotional words in their own posts.', 'ethics of online research', 'users were not specifically informed or debriefed and could not withdraw, raising concerns about consent and potential harm, even though the effects were tiny'),
           ('Cambridge Analytica', 'Data from millions of Facebook users were harvested through a personality quiz app and used for political advertising without the users\' knowledge.', 'data privacy', 'data collected for one purpose were misused for another, showing the need for consent, data minimisation and secure storage'),
           ('a mood-tracking app in Berlin', 'A free mood-tracking app shared users\' anonymised mood data with advertisers; journalists showed that some users could be re-identified from their location data.', 'anonymisation and re-identification', 'combining datasets can re-identify "anonymous" users, so anonymisation alone does not guarantee privacy'),
           ('an AI CV-screening tool', 'A company\'s AI tool for screening job applicants was found to rate CVs that mentioned women\'s colleges or clubs lower, because it was trained on past hiring decisions.', 'algorithmic bias', 'the AI learned historical gender bias from its training data, showing that AI decisions need auditing')],
    apply=[('A student plans to analyse public tweets about anxiety for her research. Explain two ethical steps she should take.', 'Seek ethics approval; anonymise usernames and paraphrase quotes so they cannot be searched; avoid vulnerable users\' identifiable content; store data securely and only for the stated purpose.', 4),
           ('A school in Singapore wants to use an AI app that predicts which students are at risk of depression from their online activity. Discuss two ethical issues.', 'Consent and privacy of monitoring students\' online activity; accuracy and bias - false positives may stigmatise, false negatives may miss students; data security; who has access and how decisions are made.', 6),
           ('Explain how a researcher running an online survey could protect participants\' data under GDPR principles.', 'Collect only necessary data (minimisation); explain the purpose and get explicit consent; store securely/encrypted; anonymise; allow withdrawal and deletion; delete data after a set period.', 4)],
    evaluate=[('The benefits of using technology in psychological research outweigh the ethical risks.', ['very large samples and real-world data', 'access to hard-to-reach groups', 'AI tools increase access to support'],
               ['consent and privacy problems (Kramer et al., 2014)', 're-identification of data', 'algorithmic bias (Obermeyer et al., 2019)'],
               'Benefits can outweigh risks only with strong safeguards: ethics review, consent, data protection and bias audits.')],
))
K.study('ch10-st3', 'Kramer, Guillory and Hancock', 2014, 'emotional contagion on Facebook', 'to test whether emotional states can be transmitted through social networks without face-to-face contact',
        'For one week, the news feeds of 689,003 Facebook users were altered to reduce either positive or negative emotional content; the emotional words in the users\' own posts were analysed by software.',
        'users exposed to fewer positive posts produced fewer positive and more negative words, and vice versa, although the effects were very small',
        'ethical issues in online research',
        ['enormous sample in a natural setting', 'objective automated measure of posts'],
        ['tiny effect sizes', 'word counts may not reflect emotions', 'serious ethical concerns over consent'],
        mtype='field experiment', iv='reduction of positive or negative content in the news feed', dv='percentage of positive and negative words in users\' posts',
        ethics='Users gave no specific informed consent (only agreeing to Facebook\'s Data Use Policy), were not debriefed and could not withdraw; their emotions were deliberately manipulated.')
K.study('ch10-st3', 'Kosinski, Stillwell and Graepel', 2013, 'predicting private traits from Facebook likes', 'to test whether digital records of behaviour can predict private personal attributes',
        'Facebook likes of 58,000 US volunteers, who had also completed personality and demographic questionnaires through the myPersonality app, were analysed by a prediction model.',
        'likes predicted sexual orientation in men correctly in 88% of cases, ethnicity (African American vs Caucasian American) in 95% and political party in 85%',
        'data privacy and digital footprints',
        ['very large sample', 'demonstrated real-world risks of data'],
        ['volunteers may not represent all users', 'raises the very privacy risks it reports'],
        mtype='correlational study')
K.study('ch10-st3', 'Fitzpatrick, Darcy and Vierhile', 2017, 'the Woebot chatbot', 'to test whether a conversational AI agent delivering CBT reduces symptoms of depression and anxiety',
        '70 students aged 18-28 at Stanford with self-reported symptoms were randomly assigned to two weeks of the Woebot chatbot or an information-only control (an NIMH e-book on depression).',
        'the Woebot group showed a significantly greater reduction in depression scores (PHQ-9) than controls; both groups reduced anxiety',
        'AI in mental health and its ethical issues',
        ['randomised design', 'accessible, low-cost intervention'],
        ['small sample and only two weeks', 'researchers had links to the company', 'privacy and crisis-response concerns'],
        mtype='randomised controlled trial', iv='use of the Woebot chatbot versus an information e-book', dv='change in PHQ-9 depression and GAD-7 anxiety scores')

# ============================================================================================
# Chapter 11 - Data Analysis and Paper 3 Source-based Skills
# ============================================================================================
K.facts('ch11-st1', F(
    terms=[('null hypothesis (H0)', 'a statement that there is no difference or relationship in the population; any observed effect is due to chance'),
           ('alternative hypothesis (H1)', 'a statement that there is a difference or relationship, either directional (one-tailed) or non-directional (two-tailed)'),
           ('significance level', 'the probability threshold (usually p ≤ 0.05) below which the null hypothesis is rejected'),
           ('p-value', 'the probability of obtaining a result at least as extreme as the one observed if the null hypothesis were true'),
           ('Type I error', 'rejecting a null hypothesis that is actually true (a false positive)'),
           ('Type II error', 'retaining a null hypothesis that is actually false (a false negative)'),
           ('critical value', 'the value a test statistic must reach (or, for U and T, not exceed) for a result to be significant'),
           ('ordinal data', 'data that can be ranked but where intervals between values are not necessarily equal, such as ratings'),
           ('non-parametric test', 'a test such as Mann-Whitney, Wilcoxon or Spearman that uses ranks and does not assume normally distributed interval data'),
           ('effect size', 'a measure of the magnitude of a difference or relationship, independent of sample size')],
    facts=[('The Mann-Whitney U test is used when:', 'Two independent groups are compared for a difference using ordinal data', ['The same participants are tested twice', 'A relationship between two co-variables is tested', 'Frequencies in categories are compared'],
            'Wilcoxon is for related samples; Spearman for correlation; chi-squared for nominal frequencies.'),
           ('For the Mann-Whitney U and Wilcoxon T tests, a result is significant when the calculated value is:', 'Equal to or less than the critical value', ['Greater than the critical value', 'Exactly equal to zero only', 'Greater than 1'],
            'Smaller U or T means less overlap between conditions.'),
           ('A researcher reports p = 0.03 with a significance level of 0.05. She should:', 'Reject the null hypothesis', ['Retain the null hypothesis', 'Conclude a Type II error has occurred', 'Conclude the effect is large'],
            'Significance does not tell us the size of the effect.'),
           ('Using a stricter significance level, such as p ≤ 0.01 instead of 0.05, makes a researcher more likely to make a:', 'Type II error', ['Type I error', 'Sampling error only', 'Calculation error'],
            'It is harder to reject H0, so true effects may be missed.'),
           ('A p-value of 0.04 means that:', 'If H0 were true, a result this extreme would occur about 4% of the time', ['There is a 4% chance that H1 is true', 'The effect is 4% of the total variance', '96% of participants showed the effect'],
            'The p-value is conditional on the null hypothesis being true.'),
           ('Which test would be appropriate for a repeated measures design with ordinal data?', 'Wilcoxon signed-rank test', ['Mann-Whitney U test', 'Spearman\'s rank correlation', 'Chi-squared test'],
            'Repeated measures produce related (paired) data.')],
    why=[('Explain why psychologists use inferential statistics rather than relying only on descriptive statistics.', 'Descriptive statistics summarise the sample but cannot show whether a difference might be due to chance; inferential tests estimate the probability of the result if H0 were true, allowing conclusions about the population.'),
         ('Explain why p ≤ 0.05 is commonly used as the significance level.', 'It balances the risks of Type I and Type II errors: a 5% risk of a false positive is accepted as reasonable for most psychological research; stricter levels (0.01) are used when a false positive would be costly.'),
         ('Explain why a statistically significant result is not necessarily an important result.', 'Significance depends on sample size; with very large samples tiny effects become significant (e.g. Orben and Przybylski, 2019), so effect size and practical importance must also be considered.'),
         ('Explain why non-parametric tests are often used in student research.', 'Student studies often have small samples and ordinal data (ratings, scores) that may not be normally distributed; tests using ranks make fewer assumptions.')],
    contrast=[('a Type I error', 'a Type II error', 'A Type I error is rejecting a true null hypothesis (false positive); a Type II error is retaining a false null hypothesis (false negative).'),
              ('a one-tailed hypothesis', 'a two-tailed hypothesis', 'A one-tailed hypothesis predicts the direction of a difference or correlation; a two-tailed hypothesis predicts an effect without stating its direction.'),
              ('the Mann-Whitney U test', 'the Wilcoxon signed-rank test', 'Mann-Whitney compares two independent groups; Wilcoxon compares two related conditions (repeated measures or matched pairs).'),
              ('statistical significance', 'effect size', 'Significance indicates whether a result is unlikely to be due to chance; effect size indicates how large the difference or relationship is.')],
    misc=[('A non-significant result proves that the null hypothesis is true.', 'It only means there is insufficient evidence to reject H0; the study may lack power (a Type II error is possible).'),
          ('p = 0.001 shows a much larger effect than p = 0.04.', 'p-values depend on sample size as well as effect size; a large sample can give a tiny p for a small effect.'),
          ('If the result is significant, the hypothesis has been proven.', 'Significance tests deal in probabilities; results support but never prove a hypothesis, and replication is needed.')],
    cases=[('a mindfulness pilot in Auckland', 'A school counsellor compared stress ratings of 8 students before and after a mindfulness course; the Wilcoxon test gave T = 4, with a critical value of 3 at p = 0.05.', 'interpreting inferential tests', 'because T is greater than the critical value, the result is not significant; with only 8 students a real effect may have been missed (possible Type II error)'),
           ('a replication of the testing effect in Lyon', 'Students who used retrieval practice recalled more than students who re-read; a Mann-Whitney test gave U = 9 with n = 10 per group (critical value 23).', 'interpreting Mann-Whitney U', 'U = 9 is below the critical value of 23, so the difference is significant at p = 0.05 and H0 is rejected'),
           ('a large online survey', 'A survey of 50,000 adults found a significant correlation (rs = 0.04, p < 0.001) between daily phone use and lower mood.', 'significance vs effect size', 'the correlation is significant because of the huge sample but the effect is negligible, explaining well under 1% of the variation'),
           ('a pre-registered trial in Toronto', 'A team registered its hypothesis, sample size and analysis plan online before collecting data on a growth mindset intervention.', 'pre-registration and the replication crisis', 'pre-registration prevents p-hacking and selective reporting, reducing Type I errors')],
    apply=[('A student wants to test whether boys and girls differ in their ratings (1-10) of fear of missing out. Identify an appropriate inferential test and justify your choice.', 'Mann-Whitney U: two independent groups (boys/girls), test of difference, ordinal rating data.', 3),
           ('A researcher finds p = 0.06. Explain what she should conclude and suggest one way she could investigate further.', 'Not significant at 0.05 - retain H0; possible Type II error; replicate with a larger sample (more power), check effect size, reduce extraneous variables.', 3),
           ('Explain why a researcher might choose a significance level of p ≤ 0.01 when testing a new treatment for anxiety.', 'A false positive (Type I error) could lead to an ineffective treatment being used; a stricter level reduces this risk, though it increases the risk of a Type II error.', 3)],
    evaluate=[('Statistical significance testing is the best way to evaluate psychological findings.', ['objective decision rule', 'controls for chance', 'standard across research'],
               ['arbitrary 0.05 cut-off', 'ignores effect size and confidence intervals', 'p-hacking and the replication crisis', 'significance depends on sample size'],
               'Significance tests are useful but should be combined with effect sizes, confidence intervals, pre-registration and replication.')],
))
K.add('ch11-st1', ('C3', 'C4'), (3, 5), 'numerical')(mann_whitney)
K.add('ch11-st1', ('C3', 'C4'), (3, 5), 'numerical')(wilcoxon)
K.add('ch11-st1', ('C1', 'C3'), (1, 3), 'short')(choose_test)
K.add('ch11-st1', ('C2', 'C3'), (2, 4), 'short')(p_decision)
methods(K, 'ch11-st1', 'spearman', 'r')


QUAL_SRC = [
    ('focus group with six Year 10 students in Manchester about exam stress',
     '"Everyone posts their revision timetables on Instagram, and then you feel like you\'re behind." / "My parents don\'t say anything, but I can tell they expect top grades." / "Honestly the worst bit is not knowing what the questions will be."',
     ['social comparison on social media', 'perceived parental expectations', 'uncertainty about the exam']),
    ('semi-structured interviews with eight nurses in Manila about night shifts',
     '"After a run of nights I can\'t remember simple things, like where I put my keys." / "My kids are asleep when I leave and at school when I get back." / "We cover for each other - that\'s what keeps me going."',
     ['memory problems from sleep loss', 'separation from family', 'peer support at work']),
    ('interviews with five refugees from Syria living in Berlin about learning German',
     '"In class I understand, but at the bakery I freeze." / "My daughter corrects me now - I feel proud and a little ashamed." / "The Arabic-speaking teacher made me feel I could do it."',
     ['anxiety about using language in public', 'role reversal with children', 'value of a culturally familiar teacher']),
    ('a focus group with retired teachers in Kyoto about using smartphones',
     '"My grandson set it up and now I video-call him every Sunday." / "There are so many buttons that I worry I will break something." / "I use it to read the news, but my eyes get tired."',
     ['technology supports family relationships', 'fear of making mistakes', 'physical difficulties with screens']),
    ('interviews with seven first-year university students in Nairobi about motivation',
     '"In high school I studied because my teachers checked everything. Here nobody checks." / "When I chose my own project topic, I worked every weekend." / "Joining a study group made me feel I belonged."',
     ['loss of external control', 'autonomy increases effort', 'relatedness supports motivation']),
    ('interviews with six young volunteers at a food bank in Toronto',
     '"I started because I needed volunteer hours for school, but now I come because I like the people." / "Seeing a family leave with groceries makes my whole week." / "Some days it\'s exhausting and nobody says thanks."',
     ['shift from extrinsic to intrinsic motivation', 'warm glow from helping', 'emotional costs of volunteering']),
]


@K.add('ch11-st2', ('C3', 'C4'), (2, 5), 'case')
def qual_source(rng, slot):
    desc, text, codes = rng.choice(QUAL_SRC)
    lead = rng.choice(['The source below is taken from', 'The following extract comes from', 'Source B reports data from'])
    if slot.d <= 3:
        return dict(stem=f'{lead} a {desc}.\n\n{text}\n\nOutline two themes that are suggested by this qualitative source.',
                    answer='Possible themes: ' + '; '.join(codes) + '.', type='case', marks=4, gap='G7',
                    markingKey='2 x (1 mark theme identified + 1 mark supported by a quotation from the source). Indicative: ' + '; '.join(codes) + '.')
    return dict(stem=f'{lead} a {desc}.\n\n{text}\n\nTo what extent can the conclusions drawn from this source be applied beyond the participants? Refer to the source in your answer.',
                answer='Transferability is limited: small, specific sample (' + desc.split(' about')[0] + '); context-specific experiences; but thick description of themes ('
                       + '; '.join(codes) + ') allows readers to judge similarity to other contexts; triangulation with other sources would increase confidence.',
                type='case', marks=6, gap='G5',
                markingKey='5-6: balanced judgement on transferability explicitly linked to features of the source (sample size and selection, setting, method, thick description, researcher bias); '
                           '3-4: relevant points, partly generic; 1-2: limited or descriptive. Themes in the source: ' + '; '.join(codes) + '.')


K.facts('ch11-st2', F(
    terms=[('quantitative source', 'a source presenting numerical data, such as tables of means, graphs or correlation coefficients'),
           ('qualitative source', 'a source presenting non-numerical data, such as interview extracts, observation notes or themes'),
           ('triangulation', 'using more than one method, source, researcher or theory to check that findings converge'),
           ('thick description', 'a detailed account of context and participants that allows readers to judge transferability'),
           ('credibility of a source', 'how far the findings in a source can be trusted, based on method, sample, measurement, peer review and bias'),
           ('standard deviation', 'a measure of how spread out scores are around the mean'),
           ('scatter graph', 'a graph plotting pairs of scores for two co-variables to show a correlation')],
    facts=[('A table shows that condition A has a mean of 14.2 (SD 1.1) and condition B a mean of 14.9 (SD 6.8). The most accurate interpretation is:', 'Means are similar, but scores in condition B are far more spread out', ['Condition B is clearly superior', 'Scores in condition A are more variable', 'The difference is definitely significant'],
            'SD shows dispersion; without a test we cannot judge significance.'),
           ('Which feature most increases the credibility of a qualitative source?', 'Researcher triangulation and member checking', ['A very large random sample', 'Use of a closed questionnaire', 'Reporting only the mean'],
            'Credibility in qualitative research means faithfully representing participants\' meanings.'),
           ('Which of these is a limitation of using a bar chart of means only?', 'It does not show the spread of scores within each condition', ['It cannot show more than two conditions', 'It shows every individual score', 'It only works for correlations'],
            'Error bars or SDs are needed to show variability.'),
           ('A source reports rs = -0.62 between hours of gaming and sleep duration. This shows:', 'A moderate-to-strong negative correlation', ['Gaming causes reduced sleep', 'A weak positive correlation', 'No relationship'],
            'Correlation does not establish causation.')],
    why=[('Explain why it is important to consider the spread of data as well as the mean.', 'Two conditions can have similar means but very different variability; a high SD suggests individual differences or extraneous variables and makes a difference in means less reliable.'),
         ('Explain how combining quantitative and qualitative sources can strengthen a conclusion.', 'Quantitative data show the size and pattern of an effect in a larger sample; qualitative data explain why it occurs and how participants experience it; agreement between them (method triangulation) increases credibility.'),
         ('Explain why a correlation in a source cannot establish cause and effect.', 'Neither variable is manipulated; the relationship may be bidirectional or caused by a third variable.')],
    contrast=[('a quantitative source', 'a qualitative source', 'A quantitative source presents numerical data that can be summarised and tested statistically; a qualitative source presents words or observations interpreted for meaning and themes.'),
              ('generalisability', 'transferability', 'Generalisability is the extent to which quantitative findings from a sample apply to a population; transferability is the extent to which qualitative findings apply to other contexts, judged by the reader using thick description.')],
    misc=[('Qualitative sources are less scientific and cannot be evaluated.', 'Qualitative sources are evaluated with criteria such as credibility, transferability, reflexivity and triangulation.'),
          ('The condition with the higher mean must be better.', 'Without considering spread, sample size and an inferential test, a higher mean may reflect chance.')],
    cases=[('screen time data from Seoul', 'Source A: a table of 400 Korean adolescents shows mean sleep of 7.4 h for those with under 2 h of daily screen use and 6.6 h for those with over 4 h.', 'interpreting a quantitative source', 'there is a negative association between screen time and sleep, but the design is correlational and other variables (homework, stress) may explain it'),
           ('mixed-methods evaluation in Lima', 'Source C: a reading programme raised mean test scores by 8 points; interviews with teachers said pupils "finally enjoyed books".', 'combining quantitative and qualitative sources', 'the numerical gain is supported by qualitative evidence about motivation, increasing credibility through method triangulation'),
           ('a bar chart without error bars', 'Source B: a bar chart shows mean recall of 12 words after spaced practice and 10 after massed practice, but gives no SD or sample size.', 'limitations of presented data', 'without spread, sample size or a test, we cannot tell whether the difference is reliable or due to chance')],
    apply=[('A Paper 3 source reports that 64% of 50 surveyed students "agree" that social media harms their concentration. Explain two limitations of this source.', 'Self-report/social desirability; small, possibly unrepresentative sample; leading wording of the item; correlational opinion data cannot show cause; percentages hide strength of agreement.', 4),
           ('A source presents interview quotes from four parents in Cairo. Explain how a researcher could increase the credibility of the findings.', 'Member checking with the parents; a second coder (researcher triangulation); reflexivity about the researcher\'s assumptions; collecting more interviews until saturation; triangulating with observations.', 4)],
    evaluate=[('Quantitative sources are more useful than qualitative sources for answering research questions.', ['statistical testing and generalisation', 'large samples', 'replicability'],
               ['qualitative sources explain meaning and context', 'more valid for experiences', 'mixed methods are often strongest'],
               'Usefulness depends on the research question; combining both types usually gives the strongest conclusion.')],
))
methods(K, 'ch11-st2', 'two', 'desc', 'pct', 'irr')

K.facts('ch11-st3', F(
    terms=[('source-based question', 'an exam question that asks candidates to use given sources, together with their own knowledge, to answer it'),
           ('synthesis', 'combining evidence from several sources and one\'s own knowledge into a coherent, evaluated argument'),
           ('command term "evaluate"', 'make an appraisal by weighing up strengths and limitations'),
           ('command term "discuss"', 'offer a considered and balanced review that includes a range of arguments, factors or hypotheses'),
           ('command term "to what extent"', 'consider the merits or otherwise of an argument or concept, reaching a conclusion supported by evidence'),
           ('command term "identify"', 'provide an answer from a number of possibilities, or recognise and state briefly a distinguishing fact or feature'),
           ('own knowledge', 'relevant psychological theory and research that the candidate brings in beyond the sources')],
    facts=[('In the final, highest-mark Paper 3 question, candidates are expected to:', 'Synthesise evidence from all the sources and their own knowledge into a reasoned conclusion', ['Summarise only one source', 'Write about any topic they have revised', 'Copy the sources word for word'],
            'Synthesis and evaluation earn the top markband.'),
           ('Which command term requires a candidate to reach a judgement about how far something is true?', 'To what extent', ['Identify', 'Describe', 'State'],
            '"To what extent" requires a conclusion supported by evidence.'),
           ('In a 3-mark "identify" question about a source, the best strategy is to:', 'Give three brief, accurate points taken from the source', ['Write a full essay with an introduction', 'Evaluate the source in depth', 'Discuss own knowledge only'],
            'Marks are awarded per point; time should be saved for longer questions.'),
           ('With 1 hour 45 minutes for 30 marks in Paper 3, roughly how long should a candidate spend on a 6-mark question?', 'About 20 minutes', ['About 2 minutes', 'About 50 minutes', 'About 1 hour'],
            '105 minutes / 30 marks = 3.5 minutes per mark; 6 x 3.5 = 21 minutes.'),
           ('A candidate notices that a Paper 3 source was funded by a smartphone company. This is most relevant when evaluating the source\'s:', 'Possible bias and credibility', ['Sample size', 'Reliability of the scale', 'Level of measurement'],
            'Funding sources can create conflicts of interest.')],
    why=[('Explain why candidates should refer explicitly to the sources in Paper 3 answers.', 'Marks are awarded for using the sources as evidence; generic answers that do not cite specific data or quotations are capped in lower markbands.'),
         ('Explain why time management is important in Paper 3.', 'The final synthesis question carries half the marks; spending too long on short questions leaves too little time to integrate all sources and own knowledge.'),
         ('Explain how a candidate can evaluate a source in a Paper 3 answer.', 'Comment on the method (design, controls), sample (size, representativeness, culture), measurement (reliability, validity), credibility (peer review, funding, triangulation) and how these affect the conclusions that can be drawn.')],
    contrast=[('describing a source', 'evaluating a source', 'Describing a source reports what it says; evaluating a source judges how trustworthy and useful its evidence is, considering method, sample and bias.'),
              ('using a source', 'using own knowledge', 'Using a source means citing its data or quotations as evidence; own knowledge means adding relevant theory or research not given in the sources to support or challenge them.')],
    misc=[('In Paper 3 you should ignore your own knowledge and only use the sources.', 'The sources are the main evidence, but relevant own knowledge (theories, studies, concepts) is needed to reach the top markbands in the synthesis question.'),
          ('A longer answer always gets more marks.', 'Marks depend on meeting the command term with relevant, source-based evidence; padding or irrelevant description does not earn marks.')],
    cases=[('a well-planned synthesis answer', 'A candidate planned for 5 minutes, then wrote paragraphs each combining one source with a study from her own knowledge, evaluated the sources\' samples and ended with a qualified conclusion.', 'Paper 3 synthesis skills', 'integrating sources with own knowledge, evaluating them and reaching a reasoned judgement meets the top markband descriptors'),
           ('running out of time', 'A candidate wrote two pages for the 3-mark question and had 10 minutes left for the 15-mark synthesis question, which he answered using only Source A.', 'time management in Paper 3', 'over-writing early questions reduced time for the highest-mark question, and using one source limits marks to lower bands'),
           ('quoting without explaining', 'A candidate copied long quotations from Source B but did not explain how they answered the question.', 'using sources effectively', 'evidence must be interpreted and linked to the question; quotation alone shows little understanding')],
    apply=[('A Paper 3 synthesis question asks: "To what extent do the sources support the claim that social media harms adolescent well-being?" Write a plan for a 15-mark answer.', 'Introduction defining the claim; paragraph on supporting sources (with evaluation of design and sample); paragraph on challenging sources; own knowledge (e.g. Kross et al., 2013; Orben and Przybylski, 2019); weigh the quality of evidence; conclusion stating a qualified judgement.', 6),
           ('Explain two ways a candidate could evaluate a quantitative source in Paper 3.', 'Consider sample size and representativeness for generalisation; whether the design allows causal conclusions; reliability/validity of measures; whether descriptive or inferential statistics were reported; possible bias or funding.', 4),
           ('A source gives no information about how participants were recruited. Explain why this matters for evaluating it.', 'Without knowing the sampling method we cannot judge representativeness or self-selection bias, so it is unclear how far the findings generalise.', 3)],
    evaluate=[('The skills tested in Paper 3 are the most important skills for a psychologist.', ['evaluating evidence and synthesising sources is core to research', 'transferable critical thinking'],
               ['psychologists also need practical research and ethical skills', 'timed conditions differ from real research', 'content knowledge is also essential'],
               'Source evaluation and synthesis are central, but practical and ethical skills are equally important.')],
))

K.R.f['ch11-st3'].evaluate += [
    ('Correlational sources are of limited use when answering Paper 3 questions.', ['cannot show causation', 'third variables', 'often self-report'],
     ['large samples and real-world data', 'show patterns that experiments cannot ethically test', 'can be combined with experimental sources'],
     'Correlational sources are useful when their limits are acknowledged and they are combined with experimental and qualitative evidence.'),
    ('Qualitative sources provide stronger evidence than quantitative sources in Paper 3.', ['rich insight into experiences', 'participants\' own meanings', 'can explain quantitative patterns'],
     ['small samples limit transferability', 'researcher interpretation and bias', 'cannot measure effect size'],
     'Neither is stronger in general; the best answers weigh each source\'s credibility and combine them.'),
]
K.R.f['ch11-st3'].extended += [
    ('Source A (survey of 2,000 students in five countries) finds a small negative correlation between phone use and grades; Source B (experiment, n = 60) finds that phones on the desk reduce attention; Source C (interviews with 10 students) reports that phones help with group study. Discuss what these sources suggest about the effect of phones on learning.',
     'Source A: large, cross-cultural but correlational, small effect; Source B: causal but small sample and artificial; Source C: rich but small sample, shows benefits; own knowledge: Ward et al. (2017), Sana et al. (2013); conclusion: phones can impair attention when present/used for distraction, but effects depend on use; evidence quality varies.', 15, 'long'),
    ('Two sources study helping: Source A is a field experiment in 23 cities (Levine et al., 2001); Source B is a laboratory experiment with 40 students in one city. Evaluate which source provides stronger evidence about cultural differences in helping.',
     'Source A: real-world helping, many cultures, but less control, cultural confounds (economic factors, population size); Source B: high control but one culture cannot show cultural differences, low ecological validity; Source A is more relevant for cultural differences; combining both is best.', 8, 'long'),
    ('A Paper 3 source states: "Our app reduced anxiety by 30% in four weeks" and is published on the app developer\'s website. To what extent should this source be trusted?',
     'Limited trust: conflict of interest; not peer reviewed; unclear design (control group? random allocation?), sample and measure; percentage may hide small absolute change; could be supported if independent RCTs replicate; judgement: low credibility until verified.', 8, 'long'),
    ('Source D reports that a growth mindset intervention significantly raised grades (p < 0.001) in 12,000 students, but the effect was 0.1 grade points. Discuss how a candidate should interpret this source.',
     'Statistically significant because of the very large sample, but small effect size; may still matter at population level and for lower-achieving students (Yeager et al., 2019); consider representativeness, pre-registration and replication; practical vs statistical significance.', 6, 'long'),
]
K.R.f['ch11-st3'].apply += [
    ('A source shows that 30 participants in Cairo were recruited from one gym. Explain one implication for the conclusions a candidate can draw.', 'Opportunity/self-selected sample from one gym - likely fitter and more health-motivated than the population, so findings may not generalise; conclusions should be limited to similar groups.', 3),
    ('A source summarises a study but does not report the standard deviations. Explain why this limits interpretation.', 'Without SDs we cannot judge the spread or overlap of scores, so we cannot tell how consistent the effect is or whether the difference in means is meaningful.', 3),
    ('Write a concluding sentence for a Paper 3 synthesis answer that reaches a qualified judgement.', 'E.g. "Overall, the sources suggest that X has a moderate effect, but because Sources A and C are correlational and small-scale, this conclusion should be treated with caution until supported by experimental evidence in other cultures."', 3),
]


@K.add('ch11-st3', ('C3',), (1, 3), 'numerical')
def p3_timing(rng, slot):
    total_min, total_marks = rng.choice([(105, 30), (90, 35), (60, 24), (75, 30), (120, 40)])
    q = rng.choice([3, 4, 5, 6, 8, 10, 15])
    if q >= total_marks:
        return None
    per = total_min / total_marks
    who = name(rng)
    paper = rng.choice(['a source-based paper', 'a mock Paper 3', 'a timed practice paper', 'an end-of-unit paper'])
    return dict(stem=f'{who} is sitting {paper} lasting {total_min} minutes for {total_marks} marks. Calculate the time per mark and how long '
                     f'{who} should spend on a {q}-mark question. Suggest how {who} should use any time saved on short questions.',
                answer=f'{total_min}/{total_marks} = {per:.1f} min per mark; {q} marks x {per:.1f} = {q * per:.0f} minutes. Use saved time to plan and synthesise the highest-mark question.',
                type='numerical', marks=3,
                markingKey=f'A1 {per:.1f} min per mark (accept {per:.2f}). A1 about {q * per:.0f} minutes. R1 sensible use of time (planning/synthesis/checking).')

# ============================================================================================
# Chapter 12 - Internal Assessment: Research Proposal
# ============================================================================================
K.facts('ch12-st1', F(
    terms=[('research question', 'a focused, answerable question that states the variables (or phenomenon) and population being investigated'),
           ('operationalisation', 'defining a variable precisely in terms of how it will be manipulated or measured'),
           ('rationale', 'the justification for a study, linking it to previous theory and research and explaining why it is worth investigating'),
           ('aim', 'a general statement of what a study intends to investigate'),
           ('replication', 'repeating a previous study, sometimes with modifications, to check whether its findings hold'),
           ('justification of method', 'explaining why the chosen method (experiment, survey, interview, observation) is the most appropriate for answering the research question'),
           ('feasibility', 'whether a study can realistically be carried out with the time, resources, participants and ethical limits available')],
    facts=[('Which is the most focused research question for an IA proposal?', 'Does retrieval practice increase the number of Spanish words recalled after one week by Year 11 students compared with re-reading?', ['Does studying help memory?', 'What is the best way to learn languages in the world?', 'How does the brain remember words?'],
            'It names an operationalised IV, DV and target population.'),
           ('A student wants to explore how first-generation university students experience their first term. Which method is most appropriate?', 'Semi-structured interviews', ['A laboratory experiment', 'A correlational study using grades', 'A structured observation with a checklist'],
            'The aim is to explore experiences and meanings, so a qualitative method fits.'),
           ('A student asks: "Is there a relationship between hours of sleep and self-reported mood in Grade 11 students?" The most appropriate method is:', 'A correlational survey', ['A covert participant observation', 'A case study of one student', 'A focus group'],
            'Two co-variables are measured, not manipulated.'),
           ('Which of these is a problem with the research question "Do video games cause violence?" for an IA?', 'It is too broad and the variables are not operationalised', ['It is too narrow', 'It contains too many operational definitions', 'It can be answered by a single observation'],
            'A good RQ must be specific, measurable and feasible.'),
           ('The rationale section of a research proposal should mainly:', 'Link the research question to existing theory and research', ['List the results expected in a table', 'Describe the participants\' names', 'Repeat the procedure in full'],
            'The rationale explains why the study is worth doing.')],
    why=[('Explain why a research question must be operationalised.', 'Precise definitions of how variables will be manipulated and measured make the study testable, replicable and clear to readers, and ensure the data actually answer the question.'),
         ('Explain why the choice of method should follow from the research question.', 'Different questions need different methods: cause-and-effect questions need experiments, relationship questions need correlational designs, and questions about experience or meaning need qualitative methods such as interviews.'),
         ('Explain why linking a proposal to previous research strengthens it.', 'It shows the question is grounded in theory, allows predictions to be justified, and makes it possible to compare findings and contribute to knowledge.')],
    contrast=[('an aim', 'a research question', 'An aim is a broad statement of purpose; a research question is a specific, answerable question naming operationalised variables and the population.'),
              ('a quantitative research question', 'a qualitative research question', 'A quantitative RQ asks about differences or relationships between measurable variables; a qualitative RQ asks how or why people experience or interpret a phenomenon.')],
    misc=[('A good research question should be as broad as possible so that the study is important.', 'A good RQ is narrow and feasible; importance comes from its rationale and links to theory, not from its breadth.'),
          ('Every IA proposal must use a laboratory experiment.', 'The method should be the one best suited to the research question; surveys, interviews and observations can be appropriate.')],
    cases=[('a vague first draft', 'A student in Madrid first wrote: "How does music affect people?" Her teacher asked her to narrow it; she rewrote it as: "Does listening to lyrical music, compared with silence, reduce the number of maths problems solved correctly in 10 minutes by Grade 11 students?"', 'formulating a research question', 'the revised RQ operationalises the IV and DV, names the population and allows an experimental test'),
           ('choosing interviews', 'A student in Johannesburg wanted to understand why some classmates stopped playing sport after age 15. She chose semi-structured interviews rather than a questionnaire.', 'justifying the method', 'the aim was to explore reasons and experiences in participants\' own words, which open-ended interviews capture better than closed items'),
           ('a correlational proposal', 'A student in Hanoi proposed measuring daily step count (phone data) and mood ratings over two weeks in 30 classmates.', 'matching method to research question', 'because neither variable is manipulated, a correlational design is appropriate, but causal conclusions cannot be drawn'),
           ('replicating a classic study', 'A group in Montreal proposed a modified replication of Loftus and Palmer (1974), using a short video of a cycling accident and the verbs "smashed" and "hit".', 'replication with modification', 'replication tests whether a finding generalises to new materials and participants, while the rationale is supported by the original study')],
    apply=[('Rewrite the research question "Does stress affect memory?" so that it would be suitable for an IA proposal.', 'E.g. "Does a 3-minute public-speaking preparation task, compared with a reading task, reduce the number of words recalled from a 20-word list by Grade 12 students?" - IV and DV operationalised, population stated.', 3),
           ('A student wants to know whether students who use social media more report lower self-esteem. Identify and justify the most appropriate method.', 'Correlational survey: measure daily social media use (screen-time data) and Rosenberg Self-Esteem Scale scores; co-variables cannot ethically or practically be manipulated over a long period.', 4),
           ('Write a research question for a qualitative IA proposal about the experiences of international students in Singapore.', 'E.g. "How do international students in their first year at a Singapore university experience and cope with academic pressure?" - open, focused on experience, population stated.', 3),
           ('Explain how a student could use previous research to justify a proposal on the testing effect.', 'Cite Roediger and Karpicke (2006): retrieval practice improved one-week retention; explain theory (retrieval strengthens memory traces); justify the prediction and the choice of a one-week delay; show the gap the study addresses (e.g. different material or age group).', 4),
           ('A student proposes: "Do people in Brazil conform more than people in Japan?" Explain two reasons why this RQ is not feasible for an IA and suggest an alternative.', 'Requires cross-national sampling and translation; nationality is not manipulated and many confounds; ethical/practical limits. Alternative: "Does the number of confederates (1 vs 3) giving a wrong answer increase conformity on a line-judgement task in Grade 11 students?"', 6)],
    evaluate=[('Experiments are always the best method for an IA research proposal.', ['causal conclusions', 'control of variables', 'replicable procedures'],
               ['some questions are about experience and meaning', 'ethical limits on manipulation', 'artificiality and low ecological validity'],
               'The best method is the one that best answers the research question within ethical and practical limits.')],
))

RQ_FLAWS = [
    ('Does technology affect teenagers?', 'the IV and DV are not operationalised and the question is too broad',
     'Does using a phone during homework, compared with leaving it in another room, reduce the number of correct answers on a 20-item maths test in Grade 10 students?'),
    ('Why are some people happier than others?', 'too broad - happiness has many causes and no variables are defined',
     'Is there a correlation between the number of hours of volunteering per month and scores on the Oxford Happiness Questionnaire in Grade 12 students?'),
    ('Do girls have better memories than boys?', 'memory is not operationalised, and gender cannot be manipulated, so it is a quasi-experiment that must be acknowledged',
     'Do female and male Grade 11 students differ in the number of words recalled from a 20-word list after a 5-minute delay?'),
    ('Is the bystander effect real?', 'not operationalised and not ethically testable in a real emergency',
     'Does the number of other people present (0 vs 3) affect whether students pick up dropped pens for a confederate in a school corridor?'),
    ('Does culture affect thinking?', 'culture and thinking are vague, and comparing cultures is not feasible for a student',
     'Do students who score higher on an interdependence scale make more references to background objects when describing a scene?'),
    ('How do people feel about exams?', 'population is not specified and the focus is unclear',
     'How do Grade 12 students at an international school in Dubai experience pressure in the month before final exams?'),
    ('Does sleep matter for school?', 'neither sleep nor school outcomes are operationalised',
     'Is there a correlation between average nightly sleep (recorded in a one-week sleep diary) and reaction time on an online vigilance task in Grade 11 students?'),
    ('Do rewards help motivation?', 'type of reward and measure of motivation are not defined',
     'Does an expected certificate, compared with no reward, reduce the time Grade 9 students spend voluntarily on a puzzle during a 5-minute free-choice period?'),
]


@K.add('ch12-st1', ('C3',), (1, 4), 'short')
def rq_fix(rng, slot):
    rq, flaw, better = rng.choice(RQ_FLAWS)
    frame = rng.choice(['Explain one weakness of this research question and rewrite it so that it is suitable for an IA proposal.',
                        'Evaluate this draft research question and suggest an improved version.',
                        'A teacher says this research question needs to be refined. Explain why, and write a refined version.'])
    return dict(stem=f'A student\'s draft research question is: "{rq}" {frame}', answer=f'Weakness: {flaw}. Improved: "{better}"',
                type='short', marks=4,
                markingKey=f'1 mark weakness identified ({flaw}); 1 mark explanation of why it matters (testability/feasibility/replicability). '
                           '2 marks rewritten RQ with operationalised variable(s) and stated population, e.g. ' + better)


SCEN_G12 = [
    ('A student in Prague proposes to randomly allocate 30 classmates to memorise a list of 20 words either by forming mental images or by repeating them aloud, testing recall after 5 minutes.',
     'encoding strategy (imagery or rote repetition)', 'number of words correctly recalled from 20 after 5 minutes', 'independent samples design',
     'Prior memory ability could differ between groups; controlled by random allocation or matching on a pre-test.',
     'Opportunity sample of classmates - one school and age group, so findings may not generalise to other ages or cultures.'),
    ('A student in Accra proposes that the same 24 participants complete a Stroop task once in silence and once with traffic noise played through headphones.',
     'presence or absence of traffic noise', 'time in seconds to name the ink colours of 40 words', 'repeated measures design',
     'Practice effects could improve the second performance; controlled by counterbalancing the order of conditions.',
     'Volunteer sample from the student\'s school - may be more motivated than the general population.'),
    ('A student in Lisbon proposes to test whether students praised for effort solve more anagrams after failure than students praised for ability, with 40 Grade 9 students randomly allocated.',
     'type of praise (effort or ability)', 'number of anagrams solved in 5 minutes after a very difficult set', 'independent samples design',
     'Verbal ability may differ; controlled by random allocation and by matching on a vocabulary test.',
     'Opportunity sample from one school - limited cultural and age range.'),
    ('A student in Kuala Lumpur proposes to show 20 participants a video of a theft and ask half "How fast was the thief running when he sprinted past?" and half "How fast was the thief walking when he passed?"',
     'wording of the leading question', 'estimated speed of the thief (km/h)', 'independent samples design',
     'Participants\' attention to the video may vary; controlled by standardised viewing conditions and instructions.',
     'Self-selected volunteers from a youth club - small and possibly unrepresentative sample.'),
    ('A student in Santiago proposes to match 32 participants on a baseline attention test and then allocate one of each pair to do a reading task with their phone face-down on the desk and the other with the phone in another room.',
     'location of the phone (on the desk or in another room)', 'number of comprehension questions answered correctly out of 15', 'matched pairs design',
     'Habitual phone use could affect attention; controlled by matching participants on baseline attention and recording phone use.',
     'Opportunity sample from two classes - may not represent adults or heavy phone users.'),
    ('A student in Seoul proposes to compare the number of items recalled from a shopping list by students who studied for 10 minutes in one block with those who studied in two 5-minute blocks separated by an hour.',
     'distribution of practice (massed or spaced)', 'number of items recalled from a 25-item list after 24 hours', 'independent samples design',
     'Activities between learning and testing could interfere; controlled by instructing participants not to rehearse and standardising the delay.',
     'Random sample from the Grade 11 register - representative of that grade but not of other age groups.'),
    ('A student in Cairo proposes that 20 participants rate their mood (1-10) before and after a 15-minute walk in a park.',
     'time of rating (before or after the walk)', 'self-rated mood on a 1-10 scale', 'repeated measures design',
     'Demand characteristics may inflate after-walk ratings; reduced by a cover story and comparison with a control walk indoors.',
     'Volunteer sample of students who like walking - self-selection bias.'),
    ('A student in Vancouver proposes to compare free-choice puzzle time between children promised a sticker for puzzles and children not promised anything, with 30 children randomly allocated.',
     'expected reward (sticker or none)', 'seconds spent on puzzles during a 5-minute free-choice period', 'independent samples design',
     'Prior interest in puzzles could differ; controlled by random allocation and a baseline free-choice measure.',
     'Opportunity sample from one after-school club - parental consent may bias who takes part.'),
]
scenarios(K, 'ch12-st2', SCEN_G12, c=('C3',), d=(1, 4))


@K.add('ch12-st2', ('C3',), (1, 4), 'numerical')
def counterbalance(rng, slot):
    k = rng.choice([2, 2, 3])
    import math
    orders = math.factorial(k)
    n = orders * rng.randint(3, 8)
    conds = rng.choice([['silence', 'music'], ['spaced practice', 'massed practice'], ['phone present', 'phone absent'], ['morning', 'afternoon']] if k == 2 else
                       [['silence', 'instrumental music', 'lyrical music'], ['no reward', 'praise', 'sticker'], ['1 bystander', '2 bystanders', '4 bystanders']])
    who = name(rng)
    if k == 2:
        stem = (f'{who}\'s IA proposal uses a repeated measures design with {n} participants and two conditions ({conds[0]} and {conds[1]}). '
                'Explain how counterbalancing would be used and state how many participants would complete each order.')
        ans = f'ABBA counterbalancing: half do {conds[0]} then {conds[1]}, half the reverse - {n // 2} participants per order. This balances order effects (practice, fatigue) across conditions.'
        mk = f'R1 order effects explained. M1 two orders (AB, BA). A1 {n // 2} in each order.'
    else:
        stem = (f'{who}\'s IA proposal uses a repeated measures design with {n} participants and three conditions ({", ".join(conds)}). '
                'Calculate how many different orders full counterbalancing requires and how many participants would complete each order. Explain the purpose.')
        ans = f'3! = 6 orders; {n} / 6 = {n // 6} participants per order. Purpose: balance practice and fatigue effects across the three conditions.'
        mk = f'M1 3! = 6 orders. A1 {n // 6} per order. R1 controls order effects so they do not confound the IV.'
    return dict(stem=stem, answer=ans, type='numerical', marks=3, markingKey=mk)


STRATA_CTX = [('a school', ['Grade 9', 'Grade 10', 'Grade 11', 'Grade 12']), ('a university faculty', ['first-year', 'second-year', 'third-year']),
              ('a sports club', ['junior', 'adult', 'veteran']), ('a company', ['sales', 'technical', 'administration', 'management'])]


@K.add('ch12-st2', ('C3',), (2, 5), 'numerical')
def stratified(rng, slot):
    place, groups = rng.choice(STRATA_CTX)
    sizes = [rng.randint(4, 30) * 10 for _ in groups]
    N = sum(sizes)
    n = rng.choice([20, 30, 40, 50])
    raw = [s * n / N for s in sizes]
    if any(abs(r - round(r)) > 0.15 for r in raw) or sum(round(r) for r in raw) != n:
        return None
    alloc = [round(r) for r in raw]
    who = name(rng)
    desc = ', '.join(f'{g}: {s}' for g, s in zip(groups, sizes))
    stem = (f'{who} proposes a survey of {place} with {N} members ({desc}). She wants a stratified sample of {n}. '
            'Calculate how many participants should be selected from each group and explain one advantage of stratified sampling for her proposal.')
    return dict(stem=stem, type='numerical', marks=4,
                answer='; '.join(f'{g}: {s}/{N} x {n} = {a}' for g, s, a in zip(groups, sizes, alloc)) + '. Advantage: each subgroup is represented in proportion, so the sample better represents the population.',
                markingKey='M1 proportion of each group x sample size. A2 ' + ', '.join(f'{g} {a}' for g, a in zip(groups, alloc)) +
                           ' (A1 if one error). R1 proportional representation of subgroups increases representativeness/generalisability.')


K.facts('ch12-st2', F(
    terms=[('target population', 'the group to which the researcher wants to generalise the findings'),
           ('sampling technique', 'the method used to select participants, such as random, stratified, opportunity, volunteer or purposive sampling'),
           ('materials', 'the stimuli, questionnaires, apparatus and instructions used in a study'),
           ('standardised procedure', 'a procedure that is identical for all participants so that only the IV varies'),
           ('pilot study', 'a small trial run of a study to check materials, timing and instructions before the main study'),
           ('data analysis plan', 'a statement of which descriptive and inferential statistics (or qualitative analysis) will be used and why'),
           ('counterbalancing', 'varying the order of conditions across participants to control order effects in repeated measures designs'),
           ('random allocation', 'assigning participants to conditions by chance so that participant variables are spread evenly')],
    facts=[('In a proposal with an independent samples design comparing two groups on ordinal data, the appropriate inferential test is:', 'Mann-Whitney U test', ['Wilcoxon signed-rank test', 'Spearman\'s rank correlation', 'No test is needed'],
            'Two independent groups and a test of difference.'),
           ('The main purpose of a pilot study is to:', 'Check that materials, instructions and timing work before the main study', ['Collect the final data', 'Replace the need for consent', 'Increase the sample size'],
            'Problems found in the pilot can be fixed before data collection.'),
           ('Which part of a proposal states exactly what each participant will experience, step by step?', 'The procedure', ['The rationale', 'The research question', 'The data analysis plan'],
            'A clear procedure allows replication.'),
           ('A purposive sample is most appropriate when:', 'Participants with specific experiences are needed, e.g. for an interview study', ['The researcher wants every member of the population to have an equal chance', 'Testing a causal hypothesis in a laboratory', 'Measuring reaction times'],
            'Purposive sampling selects information-rich cases.'),
           ('For a qualitative interview proposal, the most appropriate data analysis plan is:', 'Thematic analysis of transcribed interviews', ['Calculating the mean and a Mann-Whitney test', 'Spearman\'s correlation of responses', 'Chi-squared test of each sentence'],
            'Qualitative data are analysed for meanings and themes.')],
    why=[('Explain why a proposal should include a pilot study.', 'It identifies unclear instructions, ceiling or floor effects, timing problems and ethical issues before the main study, improving validity and reducing wasted resources.'),
         ('Explain why a data analysis plan should be decided before data are collected.', 'Pre-planning prevents choosing analyses after seeing the data (p-hacking), ensures the design produces data suitable for the test, and makes the study transparent and replicable.'),
         ('Explain why standardised instructions are important in a research proposal.', 'They ensure every participant receives the same information, reducing experimenter bias and demand characteristics so that differences in the DV are due to the IV.')],
    contrast=[('random sampling', 'random allocation', 'Random sampling selects participants from the target population so that each has an equal chance; random allocation assigns the selected participants to conditions by chance.'),
              ('an opportunity sample', 'a stratified sample', 'An opportunity sample uses whoever is available; a stratified sample selects participants from subgroups in proportion to their size in the population.')],
    misc=[('A larger sample automatically makes a study valid.', 'Size improves reliability and power, but a large biased sample is still unrepresentative, and validity also depends on measurement and control.'),
          ('The procedure section only needs to list the materials.', 'It must describe step by step what happens to participants, including briefing, instructions, conditions, timing and debriefing.')],
    cases=[('a pilot reveals a ceiling effect', 'A student in Rome piloted a 10-word recall test and found that almost everyone recalled all 10 words, so she increased the list to 25 words.', 'pilot study', 'the pilot revealed a ceiling effect that would have hidden any difference between conditions'),
           ('materials for a survey proposal', 'A student in Bangkok planned to use the Rosenberg Self-Esteem Scale (10 items) and a question on daily social media hours, translated into Thai and back-translated.', 'materials and validity', 'using an established scale with back-translation increases validity and allows comparison with previous research'),
           ('analysis plan for a correlation', 'A student in Warsaw planned to measure sleep hours and reaction time in 25 students, plot a scatter graph, and calculate Spearman\'s rho with p ≤ 0.05.', 'data analysis plan', 'Spearman is appropriate for a relationship between two co-variables, and the scatter graph shows the direction and strength')],
    apply=[('A student proposes a repeated measures experiment on the effect of background music (instrumental music vs silence) on reaction time. Write a brief standardised procedure.', 'Brief and consent (parental consent if under 16); standardised instructions read from a script; participant completes a 2-minute online reaction-time task with music or silence through headphones at a fixed volume (order counterbalanced); short break, then the other condition; debrief; data stored under participant codes.', 6),
           ('Identify the descriptive and inferential statistics you would plan for an experiment comparing recall in two independent groups, and justify them.', 'Descriptive: mean/median and SD for each group, bar chart. Inferential: Mann-Whitney U (independent groups, test of difference, ordinal/non-normal data), p ≤ 0.05.', 4),
           ('Explain how a student could select a purposive sample for an interview proposal on experiences of moving schools.', 'Recruit students who have moved schools in the last two years (e.g. via counsellor notices), aim for 5-8 with varied backgrounds, and obtain consent.', 3)],
    evaluate=[('A detailed procedure is the most important part of a research proposal.', ['enables replication', 'shows controls and standardisation'],
               ['a clear RQ and rationale are needed to make the study worthwhile', 'ethics and analysis plan are equally essential'],
               'All parts depend on each other; the procedure matters most when linked to a clear RQ and appropriate analysis plan.')],
))

K.facts('ch12-st3', F(
    terms=[('informed consent', 'agreement to take part after being told the aim, procedure, risks and right to withdraw; for under-16s parental consent is also needed'),
           ('right to withdraw', 'participants can leave the study and remove their data at any time without penalty'),
           ('debriefing', 'explaining the true aims after participation, answering questions and checking well-being'),
           ('deception', 'misleading participants about the aim or procedure; acceptable only if minor, justified and followed by debriefing'),
           ('protection from harm', 'ensuring participants experience no more physical or psychological harm than in everyday life'),
           ('anticipated limitation', 'a weakness of the proposed design that the researcher expects in advance and explains, e.g. sampling bias or demand characteristics'),
           ('confidentiality', 'keeping participants\' identities and data secure and not disclosing them to others')],
    facts=[('Under IB ethical guidelines for the IA, which of these is NOT allowed?', 'Testing 14-year-old participants without parental or guardian consent', ['Using classmates as participants with their consent', 'Using a cover story followed by debriefing', 'Anonymising data with codes'],
            'Participants under 16 need parental or guardian consent as well as their own.'),
           ('A student plans to tell participants the study is about "visual perception" when it is really about conformity. This raises an issue of:', 'Deception, which requires justification and debriefing', ['Confidentiality only', 'Random allocation', 'Inter-rater reliability'],
            'Deception must be minor and fully debriefed.'),
           ('Which is the best way to protect confidentiality in an IA?', 'Replace names with participant codes and store data securely', ['Publish names with results', 'Share data with friends to check it', 'Ask participants to write their names on answer sheets'],
            'Codes and secure storage prevent identification.'),
           ('A limitation that a student identifies before collecting data, such as using an opportunity sample, is called:', 'An anticipated limitation', ['A Type I error', 'A confounding variable that has been controlled', 'A finding'],
            'Proposals should explain these and their impact on conclusions.')],
    why=[('Explain why the right to withdraw is important in student research.', 'Participants (often classmates) may feel pressure to continue; making it clear they can leave and remove data without consequence protects autonomy and well-being.'),
         ('Explain why debriefing is essential when a proposal uses deception.', 'Debriefing reveals the true aim, removes any misconceptions or distress caused by the deception, and allows participants to withdraw their data.'),
         ('Explain why proposals should identify anticipated limitations.', 'It shows awareness of how sampling, design and measurement may affect validity, allows the researcher to reduce them where possible, and helps readers judge how far conclusions can be generalised.')],
    contrast=[('anonymity', 'confidentiality', 'Anonymity means no identifying information is collected; confidentiality means identifying information is known but kept secure and not shared.'),
              ('an ethical consideration', 'a methodological limitation', 'An ethical consideration concerns the rights and well-being of participants; a methodological limitation concerns the validity or generalisability of the findings.')],
    misc=[('If participants signed a consent form, there are no further ethical concerns.', 'Researchers must still protect participants from harm, maintain confidentiality, respect withdrawal and debrief them.'),
          ('Any deception is forbidden in IB student research.', 'Minor deception (e.g. not revealing the hypothesis) can be acceptable if it causes no harm, is necessary and is followed by full debriefing.')],
    cases=[('a stress induction proposal', 'A student proposed telling participants they would give a speech to the whole school to raise stress before a memory test.', 'protection from harm', 'the stressor could cause more than everyday anxiety; a milder manipulation (e.g. a timed puzzle) should be used, with the right to withdraw and debriefing'),
           ('interviews about bullying', 'A student planned interviews with Grade 9 students about being bullied.', 'ethics with sensitive topics and minors', 'the topic could cause distress; it requires parental and participant consent, a counsellor on hand, the right to skip questions and careful debriefing - or a less sensitive topic'),
           ('a conformity study with classmates', 'A student planned an Asch-type study with confederates giving wrong answers on a line task with classmates.', 'deception and debriefing', 'mild deception is justifiable if participants are debriefed, reassured that conformity is normal, and allowed to withdraw data'),
           ('an online questionnaire on mood', 'A student planned to collect students\' email addresses with mood scores in a shared spreadsheet.', 'confidentiality and data protection', 'identifiable sensitive data in a shared file breaches confidentiality; use anonymous codes and secure storage')],
    apply=[('A student proposes to test whether eating chocolate improves mood in Grade 10 students. Explain why this proposal does not meet IB ethical guidelines and suggest an ethical alternative design.', 'IB guidelines do not allow studies in which participants ingest substances (food, drink or drugs), partly because of allergy and health risks; minors also need parental consent. Alternative: a mild mood-induction study (e.g. a happy vs neutral film clip) with consent, the right to withdraw and debriefing.', 4),
           ('Identify two anticipated limitations of a proposal that uses an opportunity sample of 20 classmates in a repeated measures design, and explain their effect.', 'Small, unrepresentative sample limits generalisability; classmates may guess the aim (demand characteristics); order effects if not counterbalanced; familiarity with the researcher may bias results.', 4),
           ('Write a brief debriefing statement for a proposal in which participants were not told that some questions were leading.', 'Thank participants; explain the true aim (effect of leading questions on memory, as in Loftus and Palmer, 1974); explain why the aim was hidden; reassure that responses were normal; remind of right to withdraw data; give contact details.', 3),
           ('A student plans to observe students\' phone use in the school canteen without telling them. Discuss whether this is ethical and suggest how to improve it.', 'Public behaviour may be observed without consent if no individuals are identified and it is not intrusive; but students may expect privacy at school; improve by recording only anonymous counts, seeking school permission, and debriefing via a notice afterwards.', 6)],
    evaluate=[('Ethical guidelines limit the value of student research.', ['restrict realistic manipulations (stress, deception)', 'small, convenient samples of consenting peers'],
               ['protect participants and the school community', 'encourage creative, valid designs', 'build good research habits'],
               'Guidelines limit some designs, but well-designed ethical studies can still answer meaningful questions.')],
))

K.R.f['ch12-st1'].extended += [
    ('A student wants to investigate whether background music affects concentration. Design a research proposal: write an operationalised research question, justify the method and link it to previous research.',
     'RQ e.g. "Does lyrical music, compared with silence, reduce the number of correct answers on a 5-minute arithmetic task in Grade 11 students?"; method: laboratory experiment (independent samples or counterbalanced repeated measures) because a causal question needs manipulation; link to research on working memory and irrelevant speech; justify controls (same task, volume, room).', 8, 'long'),
    ('Two students propose different methods to study how students cope with exam stress: one a questionnaire survey of 100 students, the other interviews with 6 students. Evaluate which method better answers the question "How do Grade 12 students experience exam stress?"',
     'The RQ asks about experience, so semi-structured interviews give rich, participant-led data and allow thematic analysis; the survey offers breadth and generalisability but closed items may miss meanings; judgement: interviews fit the RQ better, possibly combined with a short survey (mixed methods).', 8, 'long'),
    ('Discuss the strengths and limitations of replicating a classic study, such as Loftus and Palmer (1974), for an IA proposal.',
     'Strengths: clear rationale, established procedure and measures, allows comparison, tests generalisability to new samples/cultures. Limitations: may lack originality, original materials dated, ethical changes needed, small student samples limit conclusions; modifications should be justified.', 8, 'long'),
]
K.R.f['ch12-st2'].extended += [
    ('Design the participants, materials, procedure and data analysis sections of a proposal testing whether spaced practice improves recall of Spanish vocabulary compared with massed practice.',
     'Participants: e.g. 30 Grade 10 students (opportunity or stratified sample), random allocation; materials: 25 unfamiliar words, standardised instructions, recall sheet; procedure: brief/consent, massed (one 10-min block) vs spaced (two 5-min blocks 1 h apart), test after 24 h, debrief; analysis: means/SD, bar chart, Mann-Whitney U at p ≤ 0.05.', 10, 'long'),
    ('Evaluate the decision to use an independent samples design rather than a repeated measures design in a proposal on the effect of phone presence on reading comprehension.',
     'Independent samples avoid order effects and the need for two equivalent texts, and reduce demand characteristics; but participant variables (reading ability, phone habits) may confound - reduce with random allocation or matched pairs; repeated measures would need counterbalancing and parallel texts; judgement in context.', 8, 'long'),
    ('A student proposes to measure "motivation" as the number of minutes spent on an optional puzzle. Evaluate this operationalisation.',
     'Strengths: behavioural, objective, follows Deci (1971) free-choice measure, avoids social desirability. Limitations: time may reflect boredom with alternatives or tiredness; captures intrinsic interest only; needs a standardised free-choice period and unobtrusive recording; could be triangulated with self-report.', 6, 'long'),
]
K.R.f['ch12-st3'].extended += [
    ('A student proposes to replicate a bystander study in the school corridor by having a confederate drop books. Discuss the ethical considerations and anticipated limitations of this proposal.',
     'Ethics: no prior consent (deception) - acceptable only with minimal harm, school permission and debriefing; possible embarrassment; right to withdraw data. Limitations: lack of control over number of bystanders, observer bias (use two observers - inter-rater reliability), familiarity with confederate, limited generalisability.', 8, 'long'),
]
