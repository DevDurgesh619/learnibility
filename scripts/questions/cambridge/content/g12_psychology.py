"""Cambridge International A Level Psychology 9990 (grade 12): the four specialist options.

Clinical, consumer, health and organisational psychology (five topics each). Items mirror Paper 3
(Specialist options: theory - describe, explain and evaluate theories, studies and treatments, with
evaluation essays) and Paper 4 (Specialist options: application - novel scenarios, data and a
'design a study' planning question). Knowledge packs are turned into items by the builders in
g11_psychology; topic-specific templates add score calculations (BDI, Y-BOCS, SRRS, VIE, MPS,
adherence, expected value, pain and absence measures).
"""
from ._lib import compose, mcq, person, city, fmt
from .g11_psychology import build, ctx, fill, cap, low, d1, d2, dn, T, PROFILE as _P  # noqa: F401

PROFILE = dict(_P)
CHAPTERS = {}


def chapter(order, topics, shared=None):
    if shared:
        for t in topics:
            build(t, shared)
    CHAPTERS[order] = topics


def score_tpl(t, name, make, C=('C3', (1, 2, 3, 4, 5))):
    """make(r, D) -> (intro, [(q, a, key[n])], mcq_tuple or None) ; mcq_tuple = (stem, answer, [distractors], key)."""
    def fn(r, D):
        res = make(r, D)
        if not res:
            return None
        intro, parts, m = res
        if D <= 1 and m:
            stem, ans, ds, key = m
            ds = [x for x in dict.fromkeys(ds) if x != ans]
            if len(ds) < 3:
                return None
            opts, a = mcq(r, ans, ds)
            return {'stem': intro + ' ' + stem, 'options': opts, 'answer': a, 'key': key, 'type': 'mcq'}
        calc = any(q.startswith('Calculate') for q, _, _ in parts)
        out = None
        for _ in range(12):  # keep at least one calculation in every numerical item
            out = compose(r, intro, [(lambda r_, p=p: p) for p in parts], k=(2, 3) if D <= 3 else (3, 4), type_='numerical' if D <= 3 else 'case')
            if not calc or (out and 'Calculate' in out['stem']):
                return out
        return None
    fn.__name__ = name
    t.add(C[0], C[1], 'numerical')(fn)


def band(x, bands):
    for lo, hi, lab in bands:
        if lo <= x <= hi:
            return lab
    return bands[-1][2]


GEN_EVAL_ISSUES = ['reliability', 'validity', 'generalisability', 'ethics', 'usefulness', 'reductionism', 'determinism']


# ============================================================== CLINICAL 1: Schizophrenia

SZ_SHARED = {
    'essays': [
        ('schizophrenia is best explained by biological factors',
         ['Twin and family studies show a genetic component: Gottesman et al. (2010) found about 27% of children with two parents with schizophrenia developed it, compared with under 1% of children of unaffected parents.', 'The dopamine hypothesis is supported by the effects of amphetamines and of antipsychotics that block D2 receptors.'],
         ['Concordance in identical twins is well below 100%, so environment must matter.', 'Cognitive explanations (Frith’s faulty self-monitoring) explain hallucinations as misattributed inner speech.', 'Stress and family environment can trigger onset (diathesis–stress).'],
         ['nature versus nurture', 'reductionism', 'the diathesis–stress model']),
        ('drug treatments are the most effective way of managing schizophrenia',
         ['Antipsychotics reduce positive symptoms quickly for many patients and allow them to live in the community.', 'They are relatively cheap and easy to administer.'],
         ['Side effects (tardive dyskinesia with typical drugs; weight gain and agranulocytosis risk with clozapine) reduce adherence.', 'They treat symptoms, not causes, and are less effective for negative symptoms.', 'CBT (Sensky et al., 2000) and token economies (Paul and Lentz, 1977) improve functioning.'],
         ['effectiveness', 'side effects', 'ethics', 'individual differences']),
    ],
    'exp': [dict(intro=['A hospital in {city} compared symptom scores (0–50, higher = more severe) after six months for {n} patients with schizophrenia receiving antipsychotics plus CBT and {n} receiving antipsychotics only.',
                        '{person} compared symptom severity (0–50) for patients given medication with CBT or medication alone in {city}.'],
                 A='medication plus CBT', B='medication only', gA='patients who receive medication plus CBT', gB='patients who receive medication only',
                 more='will have lower symptom scores than', measure='symptom score', dvshort='Symptom score (0–50)', higher='B', nosample=True,
                 iv='whether patients received CBT in addition to medication', dv='score out of 50 on a symptom rating scale completed by a psychiatrist after six months',
                 range=(5, 50), base=(20, 24), diff=(3, 7), sd=4.5,
                 controls=['the same type and dose of medication in both groups', 'raters who do not know which group each patient is in (blind rating)'],
                 ethics=['all patients continue to receive medication, so no one is denied treatment', 'patients must be able to give informed consent; if not, consent from a guardian is needed'],
                 concl_A='adding CBT increases symptoms.', concl_B='adding CBT to medication reduces symptoms more than medication alone.')],
    'plan': [('whether CBT reduces the distress caused by hallucinations in people with schizophrenia', 'IV: CBT or usual care', 'DV: distress rating from 0 to 10', ['field experiment']),
             ('how family members feel about caring for a relative with schizophrenia', 'topic: experiences of carers', 'measure: rating scales and open answers', ['interview', 'questionnaire'])],
    'plan_lead': 'Design',
}

c1a = T('Diagnostic criteria and characteristics of schizophrenia (DSM-5, ICD-11)', 'diagnostic criteria schizophrenia dsm-5 icd-11')
build(c1a, {
    'terms': [
        ('hallucination', 'a perception that occurs without an external stimulus, such as hearing voices'),
        ('delusion', 'a fixed false belief that is held despite clear evidence against it'),
        ('positive symptoms', 'symptoms that add to or distort normal experience, such as hallucinations and delusions'),
        ('negative symptoms', 'symptoms that reflect a loss or reduction of normal functions, such as avolition and flattened affect'),
        ('avolition', 'a severe reduction in motivation to begin and persist with goal-directed activities'),
        ('catatonia', 'abnormal motor behaviour such as holding rigid poses, or excessive purposeless movement'),
    ],
    'mcq': [
        ('According to DSM-5, for how long must continuous signs of the disturbance persist for a diagnosis of schizophrenia?', 'At least 6 months', ['At least 2 weeks', 'At least 1 week', 'At least 5 years'], 'Six months of continuous signs, including at least one month of active symptoms.'),
        ('Which is a negative symptom of schizophrenia?', 'Alogia (poverty of speech)', ['Auditory hallucinations', 'Delusions of persecution', 'Disorganised speech'], 'Negative symptoms involve loss of normal functions.'),
        ('Believing that one is a famous religious leader with special powers is an example of', 'a delusion of grandeur', ['a hallucination', 'catatonia', 'flattened affect'], 'A false belief of special importance.'),
        ('Approximately what proportion of people develop schizophrenia during their lifetime?', 'About 1%', ['About 25%', 'About 10%', 'About 0.001%'], 'Lifetime prevalence is commonly estimated at just under 1%.'),
    ],
    'ar': [
        ('A diagnosis of schizophrenia requires at least one of delusions, hallucinations or disorganised speech.', 'DSM-5 states that two or more key symptoms are needed, at least one of them being one of these three.', 'AR', 'This is the DSM-5 criterion A rule.'),
        ('Negative symptoms usually respond better to typical antipsychotics than positive symptoms.', 'Typical antipsychotics block dopamine D2 receptors.', 'R', 'A is false: typical antipsychotics mainly reduce positive symptoms; R is true.'),
    ],
    'explain': [
        ('Explain the difference between positive and negative symptoms of schizophrenia, with an example of each.', 'Positive symptoms are additions to normal experience, such as hallucinations (hearing voices); negative symptoms are reductions of normal functioning, such as avolition or flattened emotional expression.', '1 mark each type with example [2]'),
        ('Explain why diagnosing schizophrenia can be unreliable.', 'Symptoms are varied and overlap with other disorders (for example bipolar disorder), diagnosis depends on clinicians’ judgement of self-reported experiences, and DSM-5 and ICD-11 criteria differ slightly, so two clinicians may disagree.', '1 mark reason; 1 mark explained [2]'),
        ('Describe the DSM-5 criteria for diagnosing schizophrenia.', 'Two or more of: delusions, hallucinations, disorganised speech, grossly disorganised or catatonic behaviour, negative symptoms, for a significant part of one month, with at least one being delusions, hallucinations or disorganised speech; continuous signs for at least six months; marked decline in work, relationships or self-care; not caused by substances or another condition.', '1 mark symptoms; 1 mark time criteria; 1 mark functioning/exclusions [3]'),
    ],
    'claims': [
        ('Schizophrenia means having a “split personality”.', False, 'Schizophrenia involves a split from reality (psychosis), not multiple personalities, which is a different (dissociative) disorder.'),
        ('Hearing voices that comment on one’s actions is an example of an auditory hallucination.', True, 'It is a perception without an external stimulus.'),
    ],
    'who': 'the DSM-5 classification of schizophrenia',
    'evals': [
        ('reliability', 'strength', 'Clear criteria with listed symptoms and time periods help different clinicians reach the same diagnosis.'),
        ('validity', 'weakness', 'Two people diagnosed with schizophrenia can share no symptoms at all, which suggests the category may combine different disorders.'),
        ('cultural bias', 'weakness', 'Hearing the voices of ancestors is normal in some cultures, so applying DSM criteria may lead to over-diagnosis of some groups.'),
        ('usefulness', 'strength', 'A diagnosis allows access to treatment and research on causes and treatments.'),
        ('ethics', 'weakness', 'A label of schizophrenia can lead to stigma and discrimination in work and relationships.'),
    ],
    'apply': [
        ('{person}, aged 22, from {city}, has stopped going to university. For the past seven months {person} has believed that neighbours are reading their thoughts, hears a voice commenting on everything they do, and rarely speaks or washes.',
         [('Identify one positive and one negative symptom shown by {person}.', 'Positive: delusion that neighbours read their thoughts, or auditory hallucination (a commenting voice). Negative: alogia (rarely speaks) or avolition (not washing, not attending university).', '1 mark each [2]'),
          ('Explain whether {person} meets the DSM-5 time criterion for schizophrenia.', 'Yes: symptoms have lasted seven months, more than the six months of continuous signs required, with active symptoms for more than one month.', '1 mark yes; 1 mark six-month criterion [2]'),
          ('Explain one reason why a clinician should be careful before diagnosing {person}.', 'The symptoms could be caused by drug use, a medical condition or a mood disorder with psychotic features, which must be ruled out; cultural beliefs must also be considered.', '1 mark alternative cause; 1 mark explained [2]')]),
    ],
})

c1b = T('Explanations: genetic, biochemical (dopamine hypothesis) and cognitive', 'explanations genetic biochemical dopamine hypothesis cognitive')
build(c1b, {
    'terms': [
        ('concordance rate', 'the percentage of pairs of relatives (for example twins) who both have the same disorder'),
        ('dopamine hypothesis', 'the theory that schizophrenia is associated with excess dopamine activity in certain brain pathways'),
        ('diathesis–stress model', 'the view that a disorder results from an inherited vulnerability (diathesis) combined with environmental stress'),
        ('metarepresentation', 'the ability to reflect on one’s own thoughts and intentions and recognise them as one’s own'),
        ('neurotransmitter', 'a chemical messenger that carries signals across the synapse between neurons'),
    ],
    'mcq': [
        ('Which evidence supports the dopamine hypothesis?', 'Amphetamines, which increase dopamine activity, can produce schizophrenia-like symptoms', ['Identical twins always share schizophrenia', 'Schizophrenia is more common in cities', 'CBT reduces distress from voices'], 'Drugs that raise dopamine can mimic positive symptoms.'),
        ('Gottesman et al. (2010) found that when both parents had schizophrenia, the percentage of their children who developed it was about', '27%', ['1%', '7%', '100%'], 'About 27% for two affected parents, about 7% for one, under 1% for none.'),
        ('According to Frith’s cognitive explanation, auditory hallucinations occur because', 'inner speech is not recognised as self-generated', ['the ears are damaged', 'dopamine levels are too low', 'the person is copying others'], 'Faulty self-monitoring leads to external attribution.'),
        ('Which dopamine receptor is blocked by typical antipsychotic drugs?', 'D2', ['5-HT2A', 'GABA-A', 'Nicotinic'], 'Typical antipsychotics are D2 antagonists.'),
    ],
    'ar': [
        ('Genes cannot be the only cause of schizophrenia.', 'Concordance for identical twins is well below 100%.', 'AR', 'MZ twins share all genes, so less than full concordance shows environmental influence.'),
    ],
    'explain': [
        ('Explain the dopamine hypothesis of schizophrenia.', 'It proposes that excess dopamine activity (too much dopamine or too many/oversensitive D2 receptors), especially in the mesolimbic pathway, causes positive symptoms such as hallucinations; low dopamine activity in the prefrontal cortex may relate to negative symptoms.', '1 mark excess dopamine/receptors; 1 mark link to positive symptoms; 1 mark pathway or negative symptoms [3]'),
        ('Explain how twin studies are used to investigate genetic factors in schizophrenia.', 'Concordance rates for identical (MZ) twins, who share 100% of their genes, are compared with fraternal (DZ) twins, who share about 50%; higher MZ concordance suggests a genetic contribution.', '1 mark MZ v DZ; 1 mark interpretation [2]'),
        ('Explain Frith’s cognitive explanation of schizophrenia.', 'Frith suggests a failure of metarepresentation (self-monitoring): the person cannot recognise their own thoughts and intentions as self-generated, so inner speech is experienced as an external voice (hallucination) and actions may feel controlled by others.', '1 mark metarepresentation/self-monitoring; 1 mark hallucination; 1 mark control delusions [3]'),
    ],
    'claims': [
        ('If one identical twin has schizophrenia, the other will always develop it.', False, 'Concordance for MZ twins is roughly 40–50%, not 100%.'),
        ('The diathesis–stress model combines biological vulnerability with environmental triggers.', True, 'It explains why not everyone with a genetic risk develops the disorder.'),
    ],
    'who': 'the dopamine hypothesis of schizophrenia',
    'evals': [
        ('supporting evidence', 'strength', 'Antipsychotic drugs that block D2 receptors reduce positive symptoms, and amphetamines that raise dopamine can cause psychosis, supporting a role for dopamine.'),
        ('reductionism', 'weakness', 'It reduces a complex disorder to one neurotransmitter, ignoring glutamate, genes, cognition and social factors.'),
        ('cause and effect', 'weakness', 'Raised dopamine activity could be a result of the disorder or of stress rather than its cause.'),
        ('usefulness', 'strength', 'It led to the development of antipsychotic drugs that allow many patients to live in the community.'),
        ('negative symptoms', 'weakness', 'It explains positive symptoms better than negative symptoms, which respond poorly to dopamine-blocking drugs.'),
    ],
    'apply': [
        ('Twins {person} and {person2} grew up in {city}. {person} was diagnosed with schizophrenia at 23 after a stressful year; {person2} has not developed it.',
         [('Explain what this case suggests if the twins are identical (MZ).', 'They share all their genes, so the difference shows that genes alone do not cause schizophrenia; environmental factors such as stress matter.', '1 mark same genes; 1 mark environment needed [2]'),
          ('Use the diathesis–stress model to explain why {person} developed schizophrenia.', '{person} may have inherited a vulnerability (diathesis), and the stressful year acted as a trigger that led to onset.', '1 mark diathesis; 1 mark stress trigger [2]'),
          ('Explain one problem with drawing conclusions from one pair of twins.', 'A single case cannot be generalised; concordance must be measured across many twin pairs to estimate genetic influence.', '1 mark single case; 1 mark need large samples [2]')]),
    ],
})


def _gott(r, D):
    rows = [('both parents with schizophrenia', r.randint(250, 290), r.randint(60, 90)), ('one parent with schizophrenia', r.randint(900, 1200), r.randint(50, 90)),
            ('neither parent with schizophrenia', r.randint(20000, 30000), r.randint(150, 280))]
    d = ctx(r)
    intro = fill(r.choice(['A register study in {city} followed children of parents with and without schizophrenia into adulthood.',
                           '{person} analysed national records of children in {city} according to whether their parents had schizophrenia.']), d)
    tbl = ' '.join(f'Children with {a}: {n} followed up, {k} diagnosed with schizophrenia.' for a, n, k in rows)
    a, n, k = r.choice(rows)
    p = 100 * k / n
    parts = [
        (f'Calculate the percentage of children with {a} who were diagnosed with schizophrenia. Give your answer to one decimal place.', f'{d1(p)}%', f'{k} ÷ {n} × 100 = {d1(p)}%. 1 mark working; 1 mark answer [2]'),
        ('Explain what these data suggest about genetic factors in schizophrenia.', 'Risk rises as the number of affected parents rises, which is consistent with a genetic contribution.', '1 mark pattern; 1 mark genetic interpretation [2]'),
        ('Explain why these data cannot prove that schizophrenia is caused by genes.', 'Children usually live with their parents, so they share environment as well as genes (for example stress of living with an unwell parent), and most children of affected parents do not develop schizophrenia.', '1 mark shared environment; 1 mark most do not develop it [2]'),
        ('Suggest one other type of study that could separate genetic and environmental influences.', 'An adoption study comparing adopted children of parents with schizophrenia with adopted children of unaffected parents, or a comparison of MZ and DZ twins.', '1 mark study type; 1 mark how it separates influences [2]'),
    ]
    m = (f'What percentage of the children with {a} were diagnosed with schizophrenia?', f'{d1(p)}%', [f'{d1(100 * k / (n + k))}%', f'{d1(p * 10)}%', f'{d1(p / 2)}%', f'{d1(100 - p)}%'], f'{k} ÷ {n} × 100 = {d1(p)}% [1]')
    return intro + ' ' + tbl, parts, m


score_tpl(c1b, 'gottesman', _gott)

c1c = T('Treatment and management: antipsychotics, ECT, CBT and token economy', 'treatment management antipsychotics ect cbt token economy')
build(c1c, {
    'terms': [
        ('antipsychotic', 'a drug used to reduce psychotic symptoms, usually by blocking dopamine receptors'),
        ('tardive dyskinesia', 'involuntary movements of the face and body that can develop after long-term use of typical antipsychotics'),
        ('electroconvulsive therapy (ECT)', 'a treatment in which a brief electric current is passed through the brain under anaesthetic to cause a controlled seizure'),
        ('token economy', 'a behavioural programme in which desired behaviours are rewarded with tokens that can be exchanged for privileges'),
        ('cognitive–behavioural therapy (CBT)', 'a therapy that helps people identify and challenge distorted thoughts and change their behaviour'),
        ('atypical antipsychotic', 'a newer antipsychotic, such as clozapine, that acts on serotonin as well as dopamine receptors'),
    ],
    'mcq': [
        ('Which drug is an atypical antipsychotic?', 'Clozapine', ['Chlorpromazine', 'Fluoxetine', 'Lithium'], 'Clozapine acts on dopamine and serotonin receptors.'),
        ('In Sensky et al.’s (2000) study, CBT for schizophrenia was compared with', 'befriending', ['ECT', 'no treatment at all', 'flooding'], 'Befriending controlled for therapist contact time.'),
        ('Paul and Lentz (1977) found which treatment most effective for long-stay patients?', 'A social learning programme including a token economy', ['Usual hospital care', 'Milieu therapy', 'ECT'], 'The social learning programme led to most improvement and discharges.'),
        ('For which symptom is ECT most often used in schizophrenia?', 'Catatonia or treatment-resistant symptoms', ['Mild negative symptoms', 'Delusions that respond to drugs', 'Social anxiety'], 'ECT is a last resort, mainly for catatonia.'),
    ],
    'ar': [
        ('Token economies may not generalise outside hospital.', 'Behaviour is maintained by tokens that are not available in everyday life.', 'AR', 'Removing the reinforcers can lead to extinction of the behaviour.'),
    ],
    'explain': [
        ('Explain how typical antipsychotic drugs reduce the symptoms of schizophrenia.', 'They block dopamine D2 receptors in the mesolimbic pathway, reducing excessive dopamine transmission and so reducing positive symptoms such as hallucinations and delusions.', '1 mark block D2; 1 mark reduce positive symptoms [2]'),
        ('Explain how a token economy could be used with patients with schizophrenia.', 'Target behaviours such as self-care or attending activities are defined; patients receive tokens immediately after performing them; tokens are exchanged for rewards such as snacks or outings, reinforcing the behaviours (operant conditioning).', '1 mark target behaviours; 1 mark tokens; 1 mark exchange/reinforcement [3]'),
        ('Explain how CBT is used to treat schizophrenia.', 'The therapist helps the patient to examine the evidence for delusions, to see voices as a product of their own mind, and to develop coping strategies, reducing distress and improving functioning.', '1 mark challenge beliefs; 1 mark coping/normalising; 1 mark outcome [3]'),
    ],
    'claims': [
        ('Antipsychotic drugs cure schizophrenia.', False, 'They reduce symptoms, especially positive symptoms, but do not cure the disorder, and symptoms often return if drugs are stopped.'),
        ('CBT is often used alongside medication rather than instead of it.', True, 'CBT helps patients cope with symptoms that remain while they take medication.'),
    ],
    'who': 'drug therapy (antipsychotics) for schizophrenia',
    'evals': [
        ('effectiveness', 'strength', 'Antipsychotics reduce positive symptoms for many patients within weeks, allowing them to leave hospital and live in the community.'),
        ('side effects', 'weakness', 'Typical antipsychotics can cause tardive dyskinesia and atypicals can cause weight gain, so many patients stop taking them.'),
        ('ethics', 'weakness', 'Drugs may be used to control patients rather than to help them, and some are given medication without full informed consent.'),
        ('cost and practicality', 'strength', 'Drugs are relatively cheap and need little therapist time compared with psychological therapies.'),
        ('reductionism', 'weakness', 'They treat biochemical symptoms but not social or cognitive problems, so relapse is common without psychological support.'),
    ],
    'apply': [
        ('{person}, a man with schizophrenia in {city}, has taken chlorpromazine for five years. His hallucinations are reduced, but he has developed involuntary lip-smacking and rarely leaves his room.',
         [('Identify the side effect {person} is experiencing.', 'Tardive dyskinesia.', '1 mark [1]'),
          ('Suggest a different drug treatment and explain one advantage of it.', 'An atypical antipsychotic such as clozapine, which causes fewer movement side effects and may help negative symptoms.', '1 mark drug; 1 mark advantage [2]'),
          ('Suggest how a token economy could help {person} with his negative symptoms.', 'Reward small steps such as leaving his room, washing or joining activities with tokens exchanged for privileges, reinforcing these behaviours.', '1 mark target behaviour; 1 mark reinforcement [2]'),
          ('Explain one ethical issue with using a token economy.', 'Withholding privileges until tokens are earned may be seen as coercive and could infringe patients’ rights; patients should consent.', '1 mark issue; 1 mark explained [2]')]),
    ],
})
chapter(1, [c1a, c1b, c1c], SZ_SHARED)


# ============================================================== CLINICAL 2: Mood disorders

MOOD_SHARED = {
    'essays': [
        ('depression is best explained by cognitive factors',
         ['Beck’s cognitive triad and negative schemas explain the persistent negative thinking found in depressed people.', 'CBT, based on cognitive theory, is an effective treatment.', 'Learned helplessness explains passivity after uncontrollable events.'],
         ['Negative thinking may be a result, not a cause, of depression.', 'Twin studies show a genetic component, and antidepressants that alter serotonin can reduce symptoms.', 'Cognitive explanations neglect social causes such as poverty.'],
         ['biological explanations', 'cause and effect', 'usefulness']),
        ('antidepressant drugs are more effective than psychological treatments for depression',
         ['SSRIs are easy to give and benefit many people, especially with severe depression.', 'Antidepressants can reduce symptoms enough for people to engage with therapy.'],
         ['Kirsch et al. (2008) found the difference from placebo was small except in severe depression.', 'CBT and REBT teach lasting skills and have lower relapse rates.', 'Side effects reduce adherence.'],
         ['effectiveness', 'placebo', 'side effects']),
    ],
    'exp': [dict(intro=['A clinic in {city} compared BDI-II scores (0–63) after 12 weeks for {n} patients receiving CBT and {n} patients receiving an SSRI antidepressant.',
                        '{person} compared depression scores (BDI-II, 0–63) after 12 weeks for patients randomly allocated to CBT or to an SSRI.'],
                 A='CBT', B='SSRI', gA='patients receiving CBT', gB='patients receiving an SSRI',
                 more='will have lower BDI-II scores than', measure='BDI-II score', dvshort='BDI-II score after 12 weeks', higher='B', nosample=True,
                 iv='whether patients received CBT or an SSRI antidepressant', dv='score on the Beck Depression Inventory (BDI-II, 0–63) after 12 weeks',
                 range=(2, 50), base=(13, 17), diff=(2, 6), sd=4.5,
                 controls=['patients with similar BDI-II scores at the start in both groups', 'the same assessor, who does not know the treatment group, for all patients'],
                 ethics=['patients must be monitored for suicidal thoughts and given help if needed', 'the more effective treatment should be offered to all afterwards'],
                 concl_A='SSRIs reduced depression more than CBT.', concl_B='CBT reduced depression more than an SSRI over 12 weeks.')],
    'plan': [('whether a short course of CBT reduces negative automatic thoughts in students with low mood', 'IV: CBT course or waiting list', 'DV: number of negative thoughts recorded in a diary', ['field experiment']),
             ('whether there is a relationship between hours of daylight and mood', 'co-variable 1: hours of daylight per day', 'co-variable 2: mood rating', ['correlation'])],
    'plan_lead': 'Design',
}

c2a = T('Characteristics of depressive and bipolar disorders', 'characteristics depressive bipolar disorders')
build(c2a, {
    'terms': [
        ('major depressive disorder', 'a mood disorder with at least two weeks of depressed mood or loss of interest, plus other symptoms causing distress or impairment'),
        ('anhedonia', 'a loss of interest or pleasure in activities that were previously enjoyed'),
        ('mania', 'a period of abnormally elevated or irritable mood and increased energy lasting at least one week'),
        ('hypomania', 'a milder form of mania lasting at least four days that does not cause severe impairment'),
        ('bipolar I disorder', 'a mood disorder in which the person has had at least one manic episode'),
        ('flight of ideas', 'rapidly jumping from one idea to another, often seen in mania'),
    ],
    'mcq': [
        ('According to DSM-5, depressive symptoms must be present for at least how long for a major depressive episode?', 'Two weeks', ['Two days', 'Six months', 'One year'], 'Five or more symptoms over the same two-week period.'),
        ('Which feature distinguishes bipolar I disorder from major depressive disorder?', 'At least one manic episode', ['Sadness', 'Loss of appetite', 'Sleep problems'], 'Mania is required for bipolar I.'),
        ('Which is a typical symptom of a manic episode?', 'Decreased need for sleep', ['Psychomotor retardation', 'Excessive guilt', 'Anhedonia'], 'People with mania may feel rested after only a few hours’ sleep.'),
        ('Which symptom must be present for a diagnosis of a major depressive episode?', 'Depressed mood or loss of interest or pleasure', ['Hallucinations', 'Grandiosity', 'Panic attacks'], 'One of these two core symptoms is required.'),
    ],
    'ar': [
        ('Bipolar II disorder involves hypomania rather than full mania.', 'Hypomanic episodes are shorter and less severe than manic episodes.', 'AR', 'Bipolar II = hypomania plus major depressive episodes.'),
    ],
    'explain': [
        ('Describe the characteristics of a major depressive episode.', 'Depressed mood and/or loss of interest or pleasure, with other symptoms such as weight or appetite change, insomnia or hypersomnia, fatigue, feelings of worthlessness or guilt, poor concentration and thoughts of death, for at least two weeks, causing distress or impairment.', '1 mark core symptom; 1 mark further symptoms; 1 mark duration/impairment [3]'),
        ('Explain the difference between bipolar I and bipolar II disorder.', 'Bipolar I requires at least one full manic episode; bipolar II involves at least one hypomanic episode and at least one major depressive episode, but no full mania.', '1 mark each [2]'),
    ],
    'claims': [
        ('People with bipolar disorder are always in either a manic or a depressed state.', False, 'Many people have long periods of normal mood (euthymia) between episodes.'),
        ('Depression can include physical symptoms such as changes in sleep and appetite.', True, 'Somatic symptoms are part of the DSM-5 criteria.'),
    ],
    'who': 'the DSM-5 classification of mood disorders',
    'evals': [
        ('reliability', 'strength', 'Listing symptoms, a minimum number and a time period helps clinicians agree on a diagnosis of depression.'),
        ('validity', 'weakness', 'Normal sadness after a loss may be diagnosed as depression, so the category may over-include ordinary experiences.'),
        ('cultural differences', 'weakness', 'In some cultures depression is expressed mainly through physical complaints, so symptom-based criteria may miss it.'),
        ('usefulness', 'strength', 'Distinguishing bipolar from unipolar depression matters because antidepressants alone can trigger mania in bipolar patients.'),
    ],
    'apply': [
        ('For the last week {person}, from {city}, has slept only three hours a night, talked very fast, spent all their savings on plans to start five businesses and said they will become the richest person in the world.',
         [('Identify two symptoms of mania shown by {person}.', 'Decreased need for sleep; pressured speech; grandiosity; excessive risky activity (spending).', '1 mark each [2]'),
          ('Explain why this episode could lead to a diagnosis of bipolar I rather than bipolar II.', 'It lasts a week and causes marked impairment (spending all savings), which meets the criteria for a full manic episode rather than hypomania.', '1 mark duration; 1 mark severity [2]'),
          ('Explain why it is important not to treat {person} with antidepressants alone.', 'Antidepressants without a mood stabiliser can trigger or worsen manic episodes in people with bipolar disorder.', '1 mark trigger mania; 1 mark need mood stabiliser [2]')]),
    ],
})

c2b = T('Explanations: biochemical, genetic and cognitive (Beck, learned helplessness)', 'explanations biochemical genetic cognitive beck learned helplessness')
build(c2b, {
    'terms': [
        ('cognitive triad', 'Beck’s idea that depressed people hold negative views of themselves, the world and the future'),
        ('negative schema', 'a negative mental framework, often formed in childhood, through which new information is interpreted'),
        ('learned helplessness', 'giving up trying to change a situation after repeated experience that one’s actions have no effect'),
        ('monoamine hypothesis', 'the theory that depression is caused by low levels of monoamine neurotransmitters such as serotonin and noradrenaline'),
        ('attributional style', 'the way a person habitually explains the causes of events, for example as internal, stable and global'),
    ],
    'mcq': [
        ('Which neurotransmitter is most associated with the biochemical explanation of depression?', 'Serotonin', ['Dopamine only', 'Acetylcholine', 'Oxytocin'], 'Low serotonin is linked to depression and targeted by SSRIs.'),
        ('In Seligman’s research, dogs that had received inescapable shocks later', 'failed to escape shocks even when escape was possible', ['learned to escape faster', 'became aggressive', 'showed no change'], 'This is learned helplessness.'),
        ('Which is part of Beck’s cognitive triad?', 'Negative view of the future', ['Positive view of the world', 'Neutral view of others', 'High self-esteem'], 'Self, world and future.'),
        ('A depressive attributional style explains failures as', 'internal, stable and global', ['external, unstable and specific', 'caused by luck', 'caused by other people only'], 'For example “I fail at everything because I am stupid.”'),
    ],
    'ar': [
        ('SSRIs reduce depressive symptoms in many patients.', 'SSRIs increase the availability of serotonin in the synapse.', 'AR', 'Blocking reuptake raises synaptic serotonin.'),
        ('Twin studies show that depression is entirely genetic.', 'MZ twins have higher concordance for depression than DZ twins.', 'R', 'A is false: concordance is well below 100%; R is true.'),
    ],
    'explain': [
        ('Explain Beck’s cognitive explanation of depression.', 'Negative schemas formed in childhood lead to automatic negative thoughts and cognitive biases (such as overgeneralisation); the person develops a negative triad about self, world and future, which maintains depression.', '1 mark schemas; 1 mark triad; 1 mark biases/automatic thoughts [3]'),
        ('Explain the learned helplessness explanation of depression.', 'After repeated uncontrollable negative events, a person learns that their actions make no difference, stops trying to change their situation and becomes passive and depressed, as Seligman’s dogs did.', '1 mark uncontrollable events; 1 mark passivity; 1 mark evidence [3]'),
        ('Explain the biochemical explanation of depression.', 'Depression is linked to low activity of monoamines such as serotonin and noradrenaline; antidepressants that increase their availability reduce symptoms.', '1 mark low monoamines; 1 mark evidence from drugs [2]'),
    ],
    'claims': [
        ('Learned helplessness was first demonstrated in research with animals.', True, 'Seligman and Maier (1967) used dogs given inescapable shocks.'),
        ('Beck argued that depression is caused by low serotonin.', False, 'Beck’s explanation is cognitive: faulty thinking and negative schemas.'),
    ],
    'who': 'Beck’s cognitive explanation of depression',
    'evals': [
        ('supporting evidence', 'strength', 'Depressed people show more negative automatic thoughts and biased recall of negative information, as the theory predicts.'),
        ('usefulness', 'strength', 'It led to CBT, which is an effective treatment for depression.'),
        ('cause and effect', 'weakness', 'Negative thinking may be a symptom of depression rather than its cause.'),
        ('reductionism', 'weakness', 'It focuses on thought processes and neglects biological and social factors such as genes or poverty.'),
        ('blame', 'weakness', 'By locating the problem in the person’s thinking, it may imply the patient is responsible and ignore real adverse circumstances.'),
    ],
    'apply': [
        ('{person}, a student in {city}, failed one exam and now says: “I’m useless at everything. Nothing will ever go right for me, and everyone thinks I’m a failure.”',
         [('Identify the three parts of Beck’s cognitive triad in {person}’s statement.', 'Self: “I’m useless”; future: “Nothing will ever go right”; world/others: “everyone thinks I’m a failure”.', '1 mark for any two, 2 marks for all three [2]'),
          ('Identify the cognitive distortion shown by “useless at everything”.', 'Overgeneralisation: drawing a broad conclusion from one failure.', '1 mark name; 1 mark explanation [2]'),
          ('Explain {person}’s attributional style using the learned helplessness model.', 'The failure is attributed internally (my fault), stably (always) and globally (everything), which leads to hopelessness and passivity.', '1 mark internal/stable/global; 1 mark consequence [2]')]),
    ],
})

c2c = T('Treatment: antidepressants, CBT and rational emotive behaviour therapy', 'treatment antidepressants cbt rational emotive behaviour therapy')
build(c2c, {
    'terms': [
        ('SSRI', 'a selective serotonin reuptake inhibitor, an antidepressant that blocks the reabsorption of serotonin into the presynaptic neuron'),
        ('rational emotive behaviour therapy (REBT)', 'Ellis’s therapy in which irrational beliefs are disputed and replaced with rational ones'),
        ('ABC model', 'Ellis’s model in which an Activating event leads to emotional and behavioural Consequences through the person’s Beliefs'),
        ('disputing', 'challenging irrational beliefs, for example by asking for evidence or showing they are illogical'),
        ('behavioural activation', 'scheduling rewarding activities to increase positive experiences and reduce withdrawal'),
        ('placebo effect', 'improvement caused by the expectation of treatment rather than the treatment itself'),
    ],
    'mcq': [
        ('Which is an SSRI?', 'Fluoxetine', ['Chlorpromazine', 'Lithium', 'Diazepam'], 'Fluoxetine (Prozac) is an SSRI.'),
        ('Kirsch et al. (2008) found that the advantage of antidepressants over placebo was', 'small except for patients with very severe depression', ['very large for all patients', 'zero for all patients', 'larger for mild depression than severe depression'], 'Meta-analysis of FDA trial data.'),
        ('In Ellis’s ABC model, “B” stands for', 'beliefs', ['behaviour', 'brain', 'bias'], 'Activating event, Beliefs, Consequences.'),
        ('Which drug is commonly used as a mood stabiliser for bipolar disorder?', 'Lithium', ['Fluoxetine', 'Clozapine', 'Naltrexone'], 'Lithium reduces manic episodes.'),
    ],
    'ar': [
        ('REBT aims to change emotional consequences by changing beliefs.', 'In Ellis’s model, beliefs about an event, not the event itself, cause emotional responses.', 'AR', 'This is the rationale of REBT.'),
    ],
    'explain': [
        ('Explain how SSRIs are thought to reduce depression.', 'They block the reuptake of serotonin by the presynaptic neuron, so more serotonin remains in the synapse to stimulate the postsynaptic neuron, correcting low serotonin activity.', '1 mark block reuptake; 1 mark more serotonin in synapse [2]'),
        ('Explain how REBT is used to treat depression.', 'The therapist identifies irrational beliefs (such as “I must be perfect”) that lead from an activating event to depression, then actively disputes them, helping the client form an effective new rational belief and new feelings.', '1 mark ABC; 1 mark disputing; 1 mark new belief (E) [3]'),
        ('Explain how CBT is used to treat depression.', 'The client records negative automatic thoughts, tests them against evidence (for example by behavioural experiments), replaces them with more balanced thoughts and increases rewarding activities, with homework between sessions.', '1 mark identify thoughts; 1 mark challenge/test; 1 mark behavioural change [3]'),
    ],
    'claims': [
        ('SSRIs usually start to improve mood within a few hours.', False, 'It usually takes several weeks for SSRIs to have a noticeable effect.'),
        ('CBT involves homework tasks between sessions.', True, 'Clients practise recording and challenging thoughts and scheduling activities.'),
    ],
    'who': 'drug treatment (SSRIs) for depression',
    'evals': [
        ('effectiveness', 'strength', 'Many patients improve, and drugs can lift mood enough for them to engage with therapy.'),
        ('placebo effects', 'weakness', 'Kirsch et al. found that much of the improvement also occurs with placebo, except in severe depression.'),
        ('side effects', 'weakness', 'Side effects such as nausea, weight gain and sexual problems lead some patients to stop treatment.'),
        ('practicality', 'strength', 'Drugs are cheap, widely available and need little time from professionals.'),
        ('long-term outcome', 'weakness', 'They do not teach coping skills, so relapse rates after stopping may be higher than after CBT.'),
    ],
    'apply': [
        ('{person}, from {city}, became depressed after losing a job and believes: “I must be successful at everything or I am worthless.”',
         [('Use the ABC model to analyse {person}’s situation.', 'A: losing the job. B: the irrational belief “I must be successful at everything or I am worthless”. C: depression.', '1 mark each of A, B and C [3]'),
          ('Suggest how an REBT therapist would dispute {person}’s belief.', 'Ask for evidence that failing at one job makes a person worthless, point out that the “must” is illogical, and help replace it with “I would prefer to succeed, but failing does not make me worthless.”', '1 mark disputing technique; 1 mark rational alternative [2]'),
          ('Explain one advantage of REBT over antidepressants for {person}.', 'It addresses the belief that causes the depression, so it teaches lasting coping skills and avoids drug side effects.', '1 mark advantage; 1 mark explained [2]')]),
    ],
})

c2d = T('Measuring depression: Beck Depression Inventory', 'measuring depression beck depression inventory')
build(c2d, {
    'terms': [
        ('Beck Depression Inventory (BDI)', 'a 21-item self-report questionnaire measuring the severity of depression'),
        ('psychometric test', 'a standardised test that measures a psychological characteristic and produces a score'),
        ('test–retest reliability', 'the consistency of scores when the same people take a test twice'),
        ('concurrent validity', 'the extent to which scores on a test agree with scores on another established measure taken at the same time'),
    ],
    'mcq': [
        ('How many items are on the Beck Depression Inventory?', '21', ['10', '43', '50'], 'Each item is scored 0–3.'),
        ('What is the maximum possible score on the BDI-II?', '63', ['21', '40', '100'], '21 items × 3 = 63.'),
        ('On the BDI-II, a total score of 29 or more indicates', 'severe depression', ['minimal depression', 'mild depression', 'no depression'], 'Bands: 0–13 minimal, 14–19 mild, 20–28 moderate, 29–63 severe.'),
    ],
    'explain': [
        ('Explain one strength and one weakness of the BDI as a measure of depression.', 'Strength: it is quick, standardised and gives a quantitative score with good reliability. Weakness: it is a self-report, so people may exaggerate or minimise symptoms (social desirability), reducing validity.', '1 mark strength; 1 mark weakness [2]'),
        ('Explain how the concurrent validity of the BDI could be checked.', 'Give the BDI and a clinician’s rating (or another established measure) to the same patients at the same time and correlate the scores; a strong positive correlation shows concurrent validity.', '1 mark compare with established measure; 1 mark correlation [2]'),
    ],
    'claims': [
        ('The BDI can be used on its own to diagnose major depressive disorder.', False, 'It measures severity of symptoms; diagnosis requires a clinical assessment against DSM-5 or ICD-11 criteria.'),
        ('Each BDI item is scored from 0 to 3.', True, 'Higher scores indicate more severe symptoms.'),
    ],
    'who': 'the Beck Depression Inventory',
    'evals': [
        ('reliability', 'strength', 'It is standardised with fixed items and scoring, and gives consistent scores over short intervals (good test–retest reliability).'),
        ('validity', 'weakness', 'It relies on self-report, so patients may under-report symptoms to avoid stigma or over-report to obtain help.'),
        ('usefulness', 'strength', 'It is quick to complete and score, so clinicians can track changes in severity during treatment.'),
        ('cultural bias', 'weakness', 'Items were developed in Western populations; some cultures express distress differently, which may affect scores.'),
    ],
})

BDI_BANDS = [(0, 13, 'minimal'), (14, 19, 'mild'), (20, 28, 'moderate'), (29, 63, 'severe')]


def _bdi(r, D):
    d = ctx(r)
    lvl = r.choice([0.4, 0.8, 1.2, 1.7, 2.2])
    items = [max(0, min(3, int(round(r.gauss(lvl, 0.7))))) for _ in range(21)]
    tot = sum(items)
    b = band(tot, BDI_BANDS)
    intro = f'{d["person"]}, a client at a clinic in {d["city"]}, completed the BDI-II (21 items, each scored 0–3). Item scores: {", ".join(map(str, items))}.'
    later = max(0, tot - r.randint(5, 15))
    parts = [
        ('Calculate the total BDI-II score.', str(tot), f'Sum of the 21 item scores = {tot}. 1 mark working; 1 mark answer [2]'),
        ('Using the bands 0–13 minimal, 14–19 mild, 20–28 moderate and 29–63 severe, state the severity of depression indicated.', f'{cap(b)} ({tot})', f'{tot} falls in the {b} band [1]'),
        (f'After eight weeks of CBT, {d["person"]}’s total was {later}. Calculate the percentage reduction in score.', f'{dn(100 * (tot - later) / tot) if tot else "0"}%',
         f'({tot} − {later}) ÷ {tot} × 100 = {dn(100 * (tot - later) / tot) if tot else "0"}%. 1 mark working; 1 mark answer [2]'),
        ('Explain one reason why {p}’s BDI-II score might not be an accurate measure of their depression.'.format(p=d['person']), 'It is a self-report: the client may minimise symptoms because of stigma or exaggerate them to get help, and mood on the day may affect answers.', '1 mark reason; 1 mark explained [2]'),
        ('Suggest one other way of assessing the client’s depression and explain an advantage of it.', 'A clinical interview by a psychiatrist using DSM-5 criteria, which can explore symptoms in depth and is less affected by misunderstanding of questions.', '1 mark method; 1 mark advantage [2]'),
    ]
    if tot == 0:
        return None
    m = ('What is the total BDI-II score?', str(tot), [str(tot + 1), str(tot - 1), str(tot + 3), str(round(tot / 21, 1)), str(tot - 3)], f'Sum of item scores = {tot} [1]')
    return intro, parts, m


score_tpl(c2d, 'bdi', _bdi)
score_tpl(c2a, 'bdi', _bdi, C=('C3', (2, 3, 4)))
chapter(2, [c2a, c2b, c2c, c2d], MOOD_SHARED)


# ============================================================== CLINICAL 3: Impulse control and non-substance addictive disorders

IMP_SHARED = {
    'essays': [
        ('gambling disorder is best explained by behavioural (operant conditioning) factors',
         ['Variable-ratio reinforcement on slot machines produces persistent behaviour that resists extinction.', 'Near misses and occasional wins act as reinforcers.'],
         ['Cognitive biases (Griffiths, 1994: regular gamblers made more irrational verbalisations) also maintain gambling.', 'Biochemical factors such as dopamine and opioid reward systems are involved, supported by the effectiveness of naltrexone.', 'Not everyone who is reinforced develops a disorder.'],
         ['biochemical explanations', 'cognitive biases', 'individual differences']),
        ('psychological treatments are more effective than drug treatments for impulse control disorders',
         ['Imaginal desensitisation and covert sensitisation target the learned urge and teach control.', 'Case studies (for example Glover, 2011) report long-lasting improvement.'],
         ['Naltrexone reduces urges in many patients in controlled trials.', 'Evidence for psychological treatments often comes from small samples or single cases.'],
         ['effectiveness', 'generalisability', 'case studies']),
    ],
    'exp': [dict(intro=['{person} replicated Griffiths’ (1994) “thinking aloud” study in an arcade in {city}. The percentage of each participant’s verbalisations that were irrational was compared for {n} regular and {n} non-regular gamblers.',
                        'In {city}, regular and non-regular slot-machine players thought aloud while playing, and the percentage of their statements that were irrational was recorded.'],
                 A='regular gamblers', B='non-regular gamblers', gA='regular gamblers', gB='non-regular gamblers',
                 more='will make a higher percentage of irrational verbalisations than', measure='the percentage of irrational verbalisations', dvshort='Irrational verbalisations (%)',
                 iv='whether participants were regular or non-regular gamblers', dv='the percentage of each participant’s spoken statements coded as irrational',
                 range=(0, 30), base=(2, 4), diff=(7, 11), sd=3,
                 controls=['the same slot machine and the same amount of money (number of free plays) for every participant', 'the same coding categories for irrational statements, used by two coders'],
                 ethics=['participants with a gambling problem should not be encouraged to gamble; they should be offered information about help', 'participants should play with money provided, not their own'],
                 concl_A='regular gamblers think more irrationally while gambling.', concl_B='non-regular gamblers think more irrationally while gambling.')],
    'plan': [('whether near-miss outcomes increase the desire to keep playing a game of chance', 'IV: near-miss or clear-loss outcomes', 'DV: number of extra plays chosen', ['laboratory experiment']),
             ('people’s beliefs about luck and skill in gambling', 'topic: beliefs about gambling', 'measure: rating scales and open answers', ['questionnaire', 'interview'])],
    'plan_lead': 'Design',
}

c3a = T('Characteristics of kleptomania, pyromania and gambling disorder', 'characteristics kleptomania pyromania gambling disorder')
build(c3a, {
    'terms': [
        ('kleptomania', 'a recurrent failure to resist impulses to steal objects that are not needed for personal use or for their monetary value'),
        ('pyromania', 'deliberate and purposeful fire-setting on more than one occasion, with tension before the act and pleasure or relief afterwards'),
        ('gambling disorder', 'persistent and recurrent problematic gambling leading to significant impairment or distress'),
        ('impulse control disorder', 'a disorder in which a person repeatedly fails to resist an urge to perform an act that is harmful to themselves or others'),
        ('chasing losses', 'returning to gamble again soon after losing money in an attempt to win it back'),
    ],
    'mcq': [
        ('In kleptomania, the objects stolen are usually', 'not needed for personal use or for their monetary value', ['stolen to sell for profit', 'stolen out of anger or revenge', 'stolen on the instructions of a gang'], 'The act relieves tension rather than serving a practical need.'),
        ('How many of the nine DSM-5 criteria must be met within 12 months for gambling disorder?', 'Four or more', ['One', 'All nine', 'Two'], 'At least four criteria in a 12-month period.'),
        ('Which is NOT a characteristic of pyromania?', 'Setting fires for financial gain, such as insurance fraud', ['Fascination with fire', 'Tension or arousal before setting a fire', 'Pleasure or relief when setting fires'], 'Fires set for gain or revenge exclude pyromania.'),
        ('Which feature is shared by kleptomania and pyromania?', 'Increasing tension before the act and relief or pleasure afterwards', ['Hallucinations', 'Low mood for two weeks', 'Fear of open spaces'], 'Both are impulse control disorders.'),
    ],
    'ar': [
        ('Gambling disorder is classified as a non-substance addictive disorder in DSM-5.', 'It shares features with substance addictions, such as tolerance and withdrawal-like restlessness.', 'AR', 'Shared features are why it is grouped with addictions.'),
    ],
    'explain': [
        ('Describe the characteristics of kleptomania.', 'Repeated failure to resist impulses to steal objects not needed for personal use or their value; rising tension before the theft and pleasure, gratification or relief during it; the stealing is not done out of anger or revenge or because of delusions or hallucinations.', '1 mark impulse/not needed; 1 mark tension and relief; 1 mark exclusions [3]'),
        ('Describe three DSM-5 criteria for gambling disorder.', 'Any three of: needs to gamble with increasing amounts of money to feel excitement; restless or irritable when cutting down; repeated unsuccessful attempts to stop; preoccupied with gambling; gambles when distressed; chases losses; lies to hide gambling; has jeopardised relationships or work; relies on others for money.', '1 mark each criterion [3]'),
    ],
    'claims': [
        ('Most people who shoplift have kleptomania.', False, 'Most shoplifting is done for gain or need; kleptomania is rare and involves stealing items not needed.'),
        ('People with gambling disorder may need to gamble with increasing amounts of money to feel excitement.', True, 'This resembles tolerance in substance addiction.'),
    ],
    'who': 'the DSM-5 classification of impulse control and gambling disorders',
    'evals': [
        ('reliability', 'strength', 'Specific criteria (for example four of nine gambling criteria in 12 months) help clinicians agree on a diagnosis.'),
        ('validity', 'weakness', 'It can be difficult to distinguish kleptomania from ordinary theft, because the diagnosis depends on the person’s own report of their motives.'),
        ('usefulness', 'strength', 'Recognising gambling as an addiction encourages treatment rather than only punishment.'),
        ('labelling', 'weakness', 'Labelling behaviour such as fire-setting as a disorder may be used to excuse responsibility, which raises legal and ethical issues.'),
    ],
    'apply': [
        ('{person}, a well-paid accountant in {city}, has repeatedly taken cheap items such as pens and soap from shops. She feels tense before taking them, relieved afterwards, and later throws the items away.',
         [('Identify the disorder that {person} may have and give two reasons for your answer.', 'Kleptomania: the items are not needed or valued (she can afford them and throws them away), and she feels tension before and relief after stealing.', '1 mark disorder; 1 mark each reason [3]'),
          ('Explain why her behaviour would not be classified as kleptomania if she stole to sell the items.', 'Kleptomania excludes theft for monetary gain; stealing for profit would be ordinary theft.', '1 mark exclusion; 1 mark explained [2]'),
          ('Suggest one treatment that could help {person}.', 'Covert sensitisation (imagining stealing paired with aversive images such as vomiting) or naltrexone to reduce urges.', '1 mark treatment; 1 mark how it helps [2]')]),
    ],
})

c3b = T('Explanations: biochemical, cognitive and behavioural (operant conditioning)', 'explanations biochemical cognitive behavioural operant conditioning')
build(c3b, {
    'terms': [
        ('variable-ratio reinforcement', 'a schedule in which reinforcement is given after an unpredictable number of responses'),
        ('near miss', 'an outcome that is close to a win, which can feel rewarding and encourage further gambling'),
        ('cognitive bias', 'a systematic error in thinking, such as the illusion of control'),
        ('illusion of control', 'the belief that one can influence outcomes that are actually determined by chance'),
        ('reward pathway', 'a dopamine system in the brain that produces feelings of pleasure and motivates repeated behaviour'),
    ],
    'mcq': [
        ('Which schedule of reinforcement best explains why slot-machine gambling is hard to stop?', 'Variable ratio', ['Fixed interval', 'Continuous', 'Fixed ratio'], 'Unpredictable wins produce persistent responding.'),
        ('Griffiths (1994) found that regular gamblers, compared with non-regular gamblers,', 'made more irrational verbalisations while playing', ['won much more money', 'played more slowly', 'made no irrational statements'], 'About 14% versus 2.5% of verbalisations were irrational.'),
        ('Which method did Griffiths (1994) use to study gamblers’ cognitions?', 'The “thinking aloud” method', ['Brain scanning', 'A postal questionnaire', 'Covert observation in casinos'], 'Participants verbalised their thoughts while playing.'),
        ('The biochemical explanation of impulse control disorders mainly involves', 'dopamine and opioid reward systems', ['the visuospatial sketchpad', 'oxytocin levels', 'melatonin'], 'Reward circuitry and impulsivity.'),
    ],
    'ar': [
        ('Naltrexone may reduce gambling urges.', 'Naltrexone blocks opioid receptors, reducing the pleasurable “rush” associated with the behaviour.', 'AR', 'This supports a biochemical explanation.'),
    ],
    'explain': [
        ('Explain how operant conditioning can explain gambling disorder.', 'Wins act as positive reinforcement; on a variable-ratio schedule they are unpredictable, so behaviour is very resistant to extinction; gambling may also be negatively reinforced by relief from low mood or stress.', '1 mark positive reinforcement; 1 mark variable ratio; 1 mark negative reinforcement [3]'),
        ('Explain how cognitive biases can maintain gambling.', 'Gamblers may believe they have skill or control (illusion of control), see near misses as nearly winning, or think a win is “due” (gambler’s fallacy), so they continue despite losses.', '1 mark named bias; 1 mark how it maintains gambling [2]'),
        ('Explain the biochemical explanation of kleptomania or gambling disorder.', 'The behaviour stimulates dopamine release in the reward pathway and opioid activity, producing a pleasurable rush that motivates repetition; low serotonin is linked to poor impulse control.', '1 mark dopamine/opioid reward; 1 mark serotonin/impulsivity [2]'),
    ],
    'claims': [
        ('A gambler who believes they can predict a slot machine’s results is showing an illusion of control.', True, 'Outcomes are random, so the belief in control is a cognitive bias.'),
        ('Operant conditioning cannot explain why people continue to gamble after losing.', False, 'Variable-ratio reinforcement and near misses explain persistence despite losses.'),
    ],
    'who': 'Griffiths’ (1994) study of cognitive biases in fruit-machine gambling',
    'evals': [
        ('ecological validity', 'strength', 'Participants played real fruit machines in a real arcade, so their behaviour was close to normal gambling.'),
        ('the thinking aloud method', 'weakness', 'Speaking thoughts aloud is unnatural and may change how people think while playing.'),
        ('qualitative data', 'strength', 'Verbalisations gave insight into gamblers’ actual thoughts, such as personifying the machine.'),
        ('reliability of coding', 'weakness', 'Deciding whether a statement was irrational involved interpretation, so coders might disagree.'),
        ('generalisability', 'weakness', 'The sample was small and from one area in the UK, mostly male, so it may not apply to other gamblers.'),
    ],
    'apply': [
        ('{person} plays an online slot game in {city} every evening. {person} says: “I nearly won three times today, so a big win is definitely coming.”',
         [('Identify the cognitive bias shown by {person}.', 'Gambler’s fallacy (and interpreting near misses as nearly winning).', '1 mark [1]'),
          ('Explain why near misses encourage {person} to keep playing.', 'Near misses activate the reward system and feel like nearly winning, acting as reinforcement and suggesting skill or that a win is close.', '1 mark reinforcing; 1 mark belief [2]'),
          ('Use operant conditioning to explain why the game is difficult to stop playing.', 'Wins occur on a variable-ratio schedule, so behaviour is highly resistant to extinction; each unpredictable win reinforces playing.', '1 mark VR schedule; 1 mark resistance to extinction [2]')]),
    ],
})

c3c = T('Treatment: covert sensitisation, imaginal desensitisation and drug therapy', 'treatment covert sensitisation imaginal desensitisation drug therapy')
build(c3c, {
    'terms': [
        ('covert sensitisation', 'a behavioural therapy in which the person imagines the unwanted behaviour paired with an unpleasant consequence'),
        ('imaginal desensitisation', 'a therapy in which a relaxed person imagines a situation that triggers the urge and imagines resisting it'),
        ('naltrexone', 'an opioid antagonist drug that reduces urges by blocking the pleasurable effects of the behaviour'),
        ('relaxation training', 'learning techniques such as deep breathing and muscle relaxation to reduce arousal'),
    ],
    'foils': ['flooding', 'token economy'],
    'mcq': [
        ('In covert sensitisation, the unwanted behaviour is paired with', 'an imagined unpleasant consequence', ['a real electric shock', 'a token reward', 'a drug that causes vomiting'], 'Covert = in imagination.'),
        ('Imaginal desensitisation for gambling involves', 'imagining a gambling situation while relaxed and imagining not gambling', ['gambling with real money until bored', 'being punished for gambling', 'taking an antidepressant'], 'Relaxation is paired with the trigger and resisting the urge.'),
        ('Which type of drug is naltrexone?', 'An opioid antagonist', ['An SSRI', 'A typical antipsychotic', 'A benzodiazepine'], 'It blocks opioid receptors.'),
    ],
    'explain': [
        ('Describe how covert sensitisation could be used to treat kleptomania.', 'The client imagines approaching and stealing an item, then imagines an aversive outcome such as nausea, vomiting or being caught; repeated pairing makes the urge to steal associated with disgust, reducing the behaviour (Glover, 2011, used nausea imagery).', '1 mark imagined behaviour; 1 mark aversive imagery; 1 mark association reduces urge [3]'),
        ('Describe imaginal desensitisation as a treatment for gambling disorder.', 'The client learns relaxation, then while relaxed imagines scenes that trigger the urge to gamble and imagines leaving without gambling; the urge becomes associated with relaxation and control rather than arousal.', '1 mark relaxation; 1 mark imagined trigger and resisting; 1 mark mechanism [3]'),
        ('Explain how naltrexone is thought to help people with gambling disorder.', 'By blocking opioid receptors, it reduces the dopamine-related pleasure or “rush” of gambling, so urges and cravings decrease.', '1 mark blocks opioid receptors; 1 mark reduces urges [2]'),
    ],
    'claims': [
        ('Covert sensitisation requires the client to experience real physical punishment.', False, 'The unpleasant consequence is imagined, which is why it is called covert.'),
        ('Drug treatments for gambling disorder may reduce urges but do not teach new coping skills.', True, 'Psychological therapies are often combined with drugs for this reason.'),
    ],
    'who': 'imaginal desensitisation as a treatment for gambling disorder',
    'evals': [
        ('effectiveness', 'strength', 'Studies such as McConaghy et al. found imaginal desensitisation reduced gambling more than aversion therapy, with benefits at follow-up.'),
        ('ethics', 'strength', 'It involves no real punishment or drugs, so it is non-invasive and low risk.'),
        ('individual differences', 'weakness', 'It relies on clients being able to imagine scenes vividly and practise relaxation, which not everyone can do.'),
        ('generalisability', 'weakness', 'Much of the evidence comes from small samples, so it is uncertain how well it works for all gamblers.'),
    ],
    'apply': [
        ('{person}, aged 30, from {city}, has set several fires in rubbish bins and feels intense excitement watching them burn. A therapist suggests covert sensitisation.',
         [('Describe how covert sensitisation would be used with {person}.', '{person} imagines preparing to set a fire, then imagines unpleasant consequences such as choking on smoke, severe burns or being arrested, until the urge is linked with these images.', '1 mark imagined behaviour; 1 mark aversive consequence [2]'),
          ('Explain one weakness of this treatment.', 'It may only work if {person} imagines scenes vividly and practises outside sessions, and evidence comes mainly from case studies.', '1 mark weakness; 1 mark explained [2]'),
          ('Suggest one other treatment and explain how it might help.', 'Naltrexone, which may reduce the excitement or urge associated with fire-setting by blocking opioid receptors.', '1 mark treatment; 1 mark mechanism [2]')]),
    ],
})
chapter(3, [c3a, c3b, c3c], IMP_SHARED)


# ============================================================== CLINICAL 4: Anxiety disorders

ANX_SHARED = {
    'essays': [
        ('phobias are best explained by classical conditioning',
         ['Watson and Rayner (1920) conditioned a fear of a white rat in Little Albert by pairing it with a loud noise.', 'Exposure therapies based on conditioning are effective.'],
         ['Many people with phobias recall no traumatic event.', 'Biological preparedness and genetics (Öst, 1992) explain why some fears are more common.', 'The psychodynamic explanation (Little Hans) sees phobias as displaced anxiety.'],
         ['nature versus nurture', 'reductionism', 'case studies']),
        ('systematic desensitisation is the most effective treatment for phobias',
         ['It is gradual, so it is ethical and acceptable to patients.', 'Many studies show it reduces fear of specific objects.'],
         ['Flooding can work more quickly.', 'Applied tension is more suitable for blood-injection-injury phobia because of fainting.', 'Some patients cannot imagine scenes or learn relaxation.'],
         ['effectiveness', 'ethics', 'individual differences']),
    ],
    'exp': [dict(intro=['A clinic in {city} compared fear ratings (0–10) after treatment for {n} clients with a spider phobia given systematic desensitisation and {n} clients on a waiting list.',
                        '{person} measured fear (0–10) when approaching a spider for clients given systematic desensitisation or placed on a waiting list.'],
                 A='systematic desensitisation', B='waiting list', gA='clients given systematic desensitisation', gB='clients on a waiting list',
                 more='will report lower fear ratings than', measure='fear rating', dvshort='Fear rating (0–10)', higher='B', nosample=True,
                 iv='whether clients received systematic desensitisation or were on a waiting list', dv='fear rating from 0 to 10 when 1 metre from a spider in a box',
                 range=(0, 10), base=(3, 4.5), diff=(2.5, 4), sd=1.3,
                 controls=['the same spider and the same distance for every client', 'clients with similar initial fear ratings in both groups'],
                 ethics=['the waiting-list group should be offered treatment afterwards', 'clients can stop the test at any time'],
                 concl_A='systematic desensitisation increases fear.', concl_B='systematic desensitisation reduces fear compared with no treatment.')],
    'plan': [('whether applied tension reduces fainting during blood tests', 'IV: applied tension or no training', 'DV: number of fainting episodes or dizziness ratings', ['field experiment']),
             ('whether there is a relationship between parents’ fears and their children’s fears', 'co-variable 1: parent fear score', 'co-variable 2: child fear score', ['correlation', 'questionnaire'])],
    'plan_lead': 'Design',
}

c4a = T('Characteristics of phobias: blood-injection-injury, agoraphobia, social anxiety', 'characteristics phobias blood-injection-injury agoraphobia social anxiety')
build(c4a, {
    'terms': [
        ('blood-injection-injury (BII) phobia', 'an intense fear of seeing blood, having injections or injuries, often with fainting'),
        ('agoraphobia', 'fear of situations in which escape might be difficult or help unavailable, such as public transport, open spaces or crowds'),
        ('social anxiety disorder', 'intense fear of social situations in which the person may be scrutinised or judged by others'),
        ('vasovagal response', 'a rise and then sudden fall in heart rate and blood pressure that can cause fainting'),
        ('specific phobia', 'a marked fear of a particular object or situation that is out of proportion to the danger'),
    ],
    'mcq': [
        ('Which response is unusual to blood-injection-injury phobia compared with other phobias?', 'Fainting caused by a drop in blood pressure', ['Increased heart rate only', 'Hallucinations', 'Euphoria'], 'The biphasic vasovagal response.'),
        ('According to DSM-5, agoraphobia involves fear of at least how many of five listed situations?', 'Two', ['One', 'Four', 'All five'], 'Fear of two or more of the five situations.'),
        ('For how long must fear usually last for a DSM-5 diagnosis of a specific phobia?', 'Six months or more', ['One day', 'Two weeks', 'Five years'], 'Persistent fear, typically six months or more.'),
    ],
    'ar': [
        ('People with BII phobia may faint at the sight of blood.', 'In BII phobia, heart rate and blood pressure first rise and then fall sharply.', 'AR', 'The drop in blood pressure causes fainting.'),
    ],
    'explain': [
        ('Explain the difference between a specific phobia and social anxiety disorder.', 'A specific phobia is fear of a particular object or situation (such as needles); social anxiety disorder is fear of social or performance situations where the person might be judged or embarrassed.', '1 mark each [2]'),
        ('Describe the characteristics of agoraphobia.', 'Marked fear of two or more situations (public transport, open spaces, enclosed places, queues or crowds, being outside the home alone) because escape may be difficult or help unavailable; the situations are avoided or endured with intense anxiety, for six months or more.', '1 mark situations; 1 mark reason (escape/help); 1 mark avoidance/duration [3]'),
    ],
    'claims': [
        ('Agoraphobia simply means a fear of open spaces.', False, 'It is a fear of several situations where escape may be difficult, including crowds, public transport and enclosed places.'),
        ('People with a phobia usually recognise that their fear is excessive.', True, 'Adults typically know their fear is out of proportion but cannot control it.'),
    ],
    'who': 'the Blood-Injection Phobia Inventory (BIPI) as a measure of BII phobia',
    'evals': [
        ('reliability', 'strength', 'It is a standardised self-report questionnaire with fixed items and scoring, giving consistent results.'),
        ('validity', 'strength', 'It asks about cognitive, physiological and behavioural responses to blood and injection situations, covering the main features of the phobia.'),
        ('self-report', 'weakness', 'People may under- or over-report their fear, for example to avoid embarrassment.'),
        ('usefulness', 'weakness', 'A questionnaire score cannot show how the person actually behaves when faced with a needle; a behavioural test would add information.'),
    ],
    'apply': [
        ('{person}, a student in {city}, avoids buses, shopping centres and queues, and has not left home alone for eight months because of fear of panicking with no way out.',
         [('Identify the anxiety disorder {person} is likely to have.', 'Agoraphobia.', '1 mark [1]'),
          ('Give two pieces of evidence from the description that support your answer.', 'Fear of at least two situations (public transport, shopping centres/crowds, queues, being outside alone); fear that escape would be difficult; duration over six months.', '1 mark each [2]'),
          ('Explain how {person}’s avoidance may maintain the disorder.', 'Avoiding these places reduces anxiety, which negatively reinforces avoidance, so {person} never learns the situations are safe.', '1 mark negative reinforcement; 1 mark no disconfirmation [2]')]),
    ],
})

c4b = T('Explanations: classical conditioning, psychodynamic (Little Hans) and biological', 'explanations classical conditioning psychodynamic little hans biological')
build(c4b, {
    'terms': [
        ('Little Albert', 'an infant in whom Watson and Rayner (1920) conditioned a fear of a white rat by pairing it with a loud noise'),
        ('Little Hans', 'a boy whose fear of horses Freud (1909) explained as displaced fear of his father linked to the Oedipus complex'),
        ('displacement', 'a defence mechanism in which feelings about one object are redirected onto a safer substitute'),
        ('preparedness', 'Seligman’s idea that humans are biologically ready to learn fears of things that were dangerous in evolutionary history'),
        ('stimulus generalisation', 'when a conditioned response is also produced by stimuli similar to the conditioned stimulus'),
    ],
    'mcq': [
        ('In the Little Albert study, the unconditioned stimulus was', 'a loud noise made by striking a steel bar', ['a white rat', 'a rabbit', 'a Santa Claus mask'], 'The noise naturally produced fear.'),
        ('Freud explained Little Hans’ fear of horses as', 'displaced fear of his father', ['a conditioned fear after being bitten', 'a genetic fear', 'a learned fear from watching his mother'], 'Oedipus complex and castration anxiety.'),
        ('Albert later showed fear of a rabbit and a fur coat. This is an example of', 'stimulus generalisation', ['extinction', 'spontaneous recovery', 'discrimination'], 'Similar stimuli produce the CR.'),
        ('Öst (1992) found that BII phobia is unusual because', 'a high proportion of sufferers have relatives with the same phobia', ['it never runs in families', 'it is caused by brain injury', 'it only affects children'], 'Suggests a strong genetic component.'),
    ],
    'ar': [
        ('Little Hans’ case provides weak scientific evidence for the psychodynamic explanation.', 'Much of the information came from Hans’ father, who was a supporter of Freud.', 'AR', 'Biased, second-hand case data limit the evidence.'),
    ],
    'explain': [
        ('Use classical conditioning to explain how Little Albert acquired his fear of the white rat.', 'The white rat (neutral stimulus) was repeatedly presented with a loud noise (unconditioned stimulus) that caused fear (unconditioned response); the rat became a conditioned stimulus that produced fear (conditioned response) on its own.', '1 mark NS + UCS; 1 mark UCR; 1 mark CS → CR [3]'),
        ('Explain the psychodynamic explanation of Little Hans’ phobia.', 'Freud argued Hans was in the phallic stage and experiencing the Oedipus complex: he desired his mother and feared his father would castrate him; this anxiety was displaced onto horses, which resembled his father (blinkers like glasses, black around the mouth like a moustache).', '1 mark Oedipus complex; 1 mark displacement; 1 mark horse–father link [3]'),
        ('Explain the biological explanation of phobias.', 'Genes may create a vulnerability (BII phobia runs in families, Öst, 1992), and evolution may have prepared humans to fear stimuli that were dangerous to ancestors, such as snakes, heights and blood.', '1 mark genetics; 1 mark preparedness/evolution [2]'),
    ],
    'claims': [
        ('Watson and Rayner extinguished Little Albert’s fear before he left the study.', False, 'Albert left before the fear could be removed, which is a major ethical criticism.'),
        ('Preparedness explains why phobias of snakes are more common than phobias of cars.', True, 'Snakes were a danger throughout evolution; cars are recent.'),
    ],
    'who': 'the psychodynamic explanation of phobias (Little Hans)',
    'evals': [
        ('validity of evidence', 'weakness', 'The data came mainly from Hans’ father, a supporter of Freud, so they may have been biased and interpreted to fit the theory.'),
        ('falsifiability', 'weakness', 'Concepts such as the Oedipus complex are unconscious and cannot be tested scientifically.'),
        ('alternative explanations', 'weakness', 'Hans had seen a horse fall in the street, so classical conditioning offers a simpler explanation.'),
        ('depth of data', 'strength', 'The case study provides detailed qualitative information about the development of a child’s fear.'),
    ],
    'apply': [
        ('{person}, aged 7, in {city}, was bitten by a dog at a park. Since then {person} screams at the sight of any dog, even small ones on television.',
         [('Use classical conditioning to explain how {person}’s fear developed.', 'The dog (neutral stimulus) was paired with the pain of the bite (UCS → fear UCR), so dogs became a conditioned stimulus producing fear (CR).', '1 mark pairing; 1 mark CS → CR [2]'),
          ('Explain why {person} is also afraid of small dogs on television.', 'Stimulus generalisation: stimuli similar to the original CS also produce the fear response.', '1 mark generalisation; 1 mark explained [2]'),
          ('Explain why classical conditioning cannot fully explain phobias.', 'Many people bitten by dogs do not develop phobias and many phobics recall no trauma, so biological preparedness or cognitive factors must also be involved.', '1 mark not everyone; 1 mark alternative factors [2]')]),
    ],
})

c4c = T('Treatment: systematic desensitisation, flooding and applied tension', 'treatment systematic desensitisation flooding applied tension')
build(c4c, {
    'terms': [
        ('systematic desensitisation', 'a therapy in which a relaxed client works gradually up a hierarchy of feared situations'),
        ('anxiety hierarchy', 'a list of feared situations ranked from least to most frightening'),
        ('reciprocal inhibition', 'the principle that two incompatible responses, such as relaxation and fear, cannot occur at the same time'),
        ('flooding', 'a therapy in which the client is exposed immediately to the most feared situation until anxiety subsides'),
        ('applied tension', 'a treatment for BII phobia in which the client tenses muscles to raise blood pressure and prevent fainting'),
    ],
    'mcq': [
        ('Who developed systematic desensitisation?', 'Wolpe', ['Freud', 'Ellis', 'Meichenbaum'], 'Wolpe (1958) based it on reciprocal inhibition.'),
        ('Applied tension is most suitable for treating', 'blood-injection-injury phobia', ['agoraphobia', 'social anxiety disorder', 'schizophrenia'], 'It counters the drop in blood pressure that causes fainting.'),
        ('Flooding works because', 'anxiety cannot stay at a peak for a long time, so the fear response is extinguished', ['the client is punished for being afraid', 'the client is given sedatives', 'the client avoids the feared object'], 'Prolonged exposure leads to extinction.'),
    ],
    'ar': [
        ('Systematic desensitisation is more ethical than flooding.', 'In systematic desensitisation the client controls the pace and anxiety is kept low.', 'AR', 'Gradual, client-controlled exposure causes less distress.'),
    ],
    'explain': [
        ('Describe the procedure of systematic desensitisation.', 'The client learns deep muscle relaxation; together with the therapist they build an anxiety hierarchy; they then work up the hierarchy (in imagination or in vivo), only moving to the next step when they can stay relaxed, until they can face the most feared situation.', '1 mark relaxation; 1 mark hierarchy; 1 mark gradual progression [3]'),
        ('Explain how applied tension helps people with blood-injection-injury phobia.', 'The client learns to tense the muscles of the arms, legs and torso for 10–15 seconds to raise blood pressure, preventing the drop that causes fainting, and practises this while exposed to blood or injection cues.', '1 mark tense muscles; 1 mark raises blood pressure/prevents fainting; 1 mark practised with exposure [3]'),
    ],
    'claims': [
        ('Relaxation is a useful part of treatment for blood-injection-injury phobia.', False, 'Relaxation lowers blood pressure further and could cause fainting; applied tension is used instead.'),
        ('Flooding may be quicker than systematic desensitisation.', True, 'A single long session can be enough, although it is more distressing.'),
    ],
    'who': 'systematic desensitisation',
    'evals': [
        ('effectiveness', 'strength', 'Many studies show it reduces fear of specific objects such as spiders, and gains are maintained.'),
        ('ethics', 'strength', 'The client controls the pace and anxiety is kept low, so it causes little distress.'),
        ('symptom substitution', 'weakness', 'Psychodynamic critics argue that treating the symptom without the underlying cause may lead to a new symptom.'),
        ('practicality', 'weakness', 'It can take many sessions and requires the client to learn relaxation and imagine scenes vividly.'),
        ('generalisability', 'weakness', 'It works well for specific phobias but less well for complex disorders such as agoraphobia or social anxiety.'),
    ],
    'apply': [
        ('{person}, from {city}, needs regular blood tests for a medical condition but faints whenever a needle is used.',
         [('Explain why applied tension is more suitable than systematic desensitisation for {person}.', 'Systematic desensitisation uses relaxation, which lowers blood pressure and could make fainting more likely; applied tension raises blood pressure.', '1 mark relaxation problem; 1 mark tension raises BP [2]'),
          ('Describe how a therapist would teach {person} applied tension.', 'Teach {person} to tense arm, leg and torso muscles for about 10–15 seconds until the face feels warm, release, and repeat; then practise while looking at pictures of blood and needles, building up to a real blood test.', '1 mark tension technique; 1 mark practice with exposure [2]'),
          ('Explain one problem with flooding for {person}.', 'Sudden exposure to needles would be extremely distressing and could cause fainting, and {person} may refuse or drop out.', '1 mark problem; 1 mark explained [2]')]),
    ],
})
chapter(4, [c4a, c4b, c4c], ANX_SHARED)


# ============================================================== CLINICAL 5: OCD

OCD_SHARED = {
    'essays': [
        ('obsessive-compulsive disorder is best explained by biological factors',
         ['Family and twin studies suggest a genetic component.', 'SSRIs reduce symptoms, supporting a role for serotonin; brain scans show overactivity in the orbitofrontal cortex–caudate circuit.'],
         ['Cognitive explanations (inflated responsibility, thought–action fusion) explain the content of obsessions.', 'ERP, a behavioural treatment, is highly effective.', 'Biological findings are correlational.'],
         ['reductionism', 'nature versus nurture', 'cause and effect']),
        ('exposure and response prevention is the best treatment for OCD',
         ['ERP targets the link between obsessions and compulsions directly and has good long-term outcomes.', 'Skills learned reduce relapse.'],
         ['It is distressing, and some patients drop out.', 'SSRIs are easier and help people who cannot face exposure.', 'Combined treatment may be best.'],
         ['effectiveness', 'ethics', 'individual differences']),
    ],
    'exp': [dict(intro=['A clinic in {city} compared Y-BOCS scores (0–40) after 12 weeks for {n} clients with OCD who received exposure and response prevention (ERP) and {n} clients who received relaxation training.',
                        '{person} compared Y-BOCS scores after 12 weeks for clients randomly allocated to ERP or relaxation training.'],
                 A='ERP', B='relaxation training', gA='clients who receive ERP', gB='clients who receive relaxation training',
                 more='will have lower Y-BOCS scores than', measure='Y-BOCS score', dvshort='Y-BOCS score after 12 weeks', higher='B', nosample=True,
                 iv='whether clients received ERP or relaxation training', dv='total score on the Yale–Brown Obsessive Compulsive Scale (0–40) after 12 weeks',
                 range=(2, 40), base=(12, 16), diff=(4, 8), sd=4,
                 controls=['clients with similar Y-BOCS scores at the start in each group', 'the same number and length of sessions in both conditions'],
                 ethics=['exposure can be very distressing, so clients must give informed consent and be able to withdraw', 'the relaxation group should be offered ERP afterwards'],
                 concl_A='relaxation training reduces OCD symptoms more than ERP.', concl_B='ERP reduces OCD symptoms more than relaxation training.')],
    'plan': [('whether people with high anxiety check things more often than people with low anxiety', 'IV: high or low anxiety group', 'DV: number of checking behaviours in a task', ['laboratory experiment', 'observation']),
             ('how OCD symptoms affect people’s daily lives', 'topic: daily impact of OCD', 'measure: open and closed questions', ['interview', 'questionnaire'])],
    'plan_lead': 'Design',
}

c5a = T('Characteristics of OCD and measurement (Y-BOCS)', 'characteristics ocd measurement y-bocs')
build(c5a, {
    'terms': [
        ('obsession', 'a recurrent, persistent and intrusive thought, urge or image that causes anxiety'),
        ('compulsion', 'a repetitive behaviour or mental act that a person feels driven to perform to reduce anxiety'),
        ('Yale–Brown Obsessive Compulsive Scale (Y-BOCS)', 'a 10-item clinician-rated scale measuring the severity of obsessions and compulsions'),
        ('hoarding disorder', 'persistent difficulty discarding possessions, regardless of their value, leading to clutter'),
        ('body dysmorphic disorder', 'preoccupation with perceived defects in physical appearance that are not observable or appear slight to others'),
    ],
    'mcq': [
        ('How many items are on the Y-BOCS severity scale?', '10', ['21', '43', '36'], '5 items on obsessions and 5 on compulsions.'),
        ('Each Y-BOCS item is scored from', '0 to 4', ['0 to 3', '1 to 10', '0 to 100'], 'Total 0–40.'),
        ('Which is an example of a compulsion?', 'Washing hands repeatedly until they feel “right”', ['Thinking that the door is unlocked', 'Feeling anxious about germs', 'Hearing voices'], 'A compulsion is an action performed to reduce anxiety.'),
        ('Which case study described a boy who spent hours washing?', 'Charles (Rapoport, 1989)', ['Little Hans (Freud, 1909)', 'Little Albert (Watson and Rayner, 1920)', 'Mr Wallace (Milgram, 1963)'], '“The boy who couldn’t stop washing”.'),
    ],
    'ar': [
        ('Compulsions are maintained by negative reinforcement.', 'Performing a compulsion temporarily reduces anxiety caused by an obsession.', 'AR', 'Relief from anxiety strengthens the compulsion.'),
    ],
    'explain': [
        ('Explain the difference between an obsession and a compulsion.', 'An obsession is an unwanted, intrusive thought, image or urge that causes anxiety (for example fear of contamination); a compulsion is a repetitive behaviour or mental act performed to reduce that anxiety (for example repeated washing).', '1 mark each with example [2]'),
        ('Describe how the Y-BOCS measures OCD.', 'A clinician asks about five aspects of obsessions and five of compulsions (time occupied, interference, distress, resistance and control), scoring each 0–4 to give a total from 0 to 40, where higher scores mean more severe OCD.', '1 mark items/structure; 1 mark scoring; 1 mark interpretation [3]'),
    ],
    'claims': [
        ('People with OCD always believe their compulsions are sensible.', False, 'Most recognise that their obsessions and compulsions are excessive, although insight varies.'),
        ('The Y-BOCS is administered as a semi-structured interview by a clinician.', True, 'It can also be used in a self-report version.'),
    ],
    'who': 'the Y-BOCS as a measure of OCD',
    'evals': [
        ('reliability', 'strength', 'It has standardised questions and scoring, and good inter-rater reliability when used by trained clinicians.'),
        ('validity', 'strength', 'It measures severity in terms of time, distress and interference, regardless of the content of obsessions.'),
        ('usefulness', 'strength', 'It can be repeated during treatment to measure progress.'),
        ('self-report', 'weakness', 'Scores depend on what the patient reports; patients may hide embarrassing obsessions.'),
    ],
    'apply': [
        ('{person}, from {city}, spends about three hours a day checking that doors are locked and the cooker is off, and is often late for work because of it.',
         [('Identify the obsession and the compulsion in this case.', 'Obsession: the intrusive thought that the door is unlocked or the cooker on (fear of harm). Compulsion: repeated checking.', '1 mark each [2]'),
          ('Explain why {person}’s checking is likely to continue.', 'Checking reduces anxiety, so it is negatively reinforced; the obsessional fear is never tested.', '1 mark negative reinforcement; 1 mark explained [2]'),
          ('Explain why the Y-BOCS would be useful for {person}’s therapist.', 'It gives a severity score (for example time occupied and interference) that can be compared before and after treatment to monitor progress.', '1 mark severity; 1 mark monitoring [2]')]),
    ],
})

YB_BANDS = [(0, 7, 'subclinical'), (8, 15, 'mild'), (16, 23, 'moderate'), (24, 31, 'severe'), (32, 40, 'extreme')]


def _ybocs(r, D):
    d = ctx(r)
    lvl = r.choice([1.2, 1.8, 2.3, 2.8, 3.3])
    ob = [max(0, min(4, int(round(r.gauss(lvl, 0.7))))) for _ in range(5)]
    co = [max(0, min(4, int(round(r.gauss(lvl, 0.7))))) for _ in range(5)]
    tot = sum(ob) + sum(co)
    b = band(tot, YB_BANDS)
    intro = (f'A clinician in {d["city"]} rated {d["person"]} on the Y-BOCS (each item 0–4). Obsession items: {", ".join(map(str, ob))}. '
             f'Compulsion items: {", ".join(map(str, co))}.')
    parts = [
        ('Calculate the total Y-BOCS score.', str(tot), f'{sum(ob)} (obsessions) + {sum(co)} (compulsions) = {tot}. 1 mark subtotals; 1 mark total [2]'),
        ('Using the bands 0–7 subclinical, 8–15 mild, 16–23 moderate, 24–31 severe and 32–40 extreme, state the severity of OCD.', f'{cap(b)} ({tot})', f'{tot} lies in the {b} band [1]'),
        ('Calculate the percentage of the maximum possible score that the compulsion subscale represents for this client.', f'{dn(100 * sum(co) / 20)}%', f'{sum(co)} ÷ 20 × 100 = {dn(100 * sum(co) / 20)}%. 1 mark working; 1 mark answer [2]'),
        ('Explain why two clinicians should rate the same client independently.', 'To check inter-rater reliability: if their totals are similar (highly correlated across clients), the scale is being used consistently.', '1 mark independent ratings; 1 mark inter-rater reliability [2]'),
    ]
    m = ('What is the total Y-BOCS score?', str(tot), [str(tot + 2), str(tot - 2), str(sum(ob)), str(sum(co)), str(tot + 4)], f'{sum(ob)} + {sum(co)} = {tot} [1]')
    return intro, parts, m


score_tpl(c5a, 'ybocs', _ybocs)

c5b = T('Explanations: biological, cognitive and psychodynamic', 'explanations biological cognitive psychodynamic')
build(c5b, {
    'terms': [
        ('thought–action fusion', 'the belief that having a thought about an action is the same as doing it, or makes it more likely to happen'),
        ('inflated responsibility', 'an exaggerated belief that one is responsible for preventing harm to oneself or others'),
        ('orbitofrontal cortex', 'a frontal brain area that is overactive in many people with OCD and is linked to worry about errors'),
        ('anal stage', 'Freud’s second psychosexual stage, in which conflict over toilet training may lead to orderliness and control'),
        ('reaction formation', 'a defence mechanism in which an unacceptable impulse is replaced by its opposite'),
    ],
    'mcq': [
        ('Which neurotransmitter is most associated with the biological explanation of OCD?', 'Serotonin', ['Oxytocin', 'Melatonin', 'Testosterone'], 'Low serotonin activity; SSRIs help.'),
        ('Salkovskis’ cognitive explanation of OCD emphasises', 'an inflated sense of responsibility for preventing harm', ['excess dopamine in the mesolimbic pathway', 'learning by imitation', 'conflict in the phallic stage'], 'Intrusive thoughts are interpreted as signs of responsibility.'),
        ('In the psychodynamic explanation, OCD is linked to fixation in the', 'anal stage', ['oral stage', 'phallic stage', 'genital stage'], 'Harsh toilet training may lead to obsessive orderliness.'),
    ],
    'ar': [
        ('Brain scans can show differences in people with OCD.', 'PET scans show increased activity in the orbitofrontal cortex and caudate nucleus in many patients.', 'AR', 'This is evidence for a biological explanation.'),
    ],
    'explain': [
        ('Explain the cognitive explanation of OCD.', 'Everyone has intrusive thoughts, but people with OCD interpret them as meaningful and dangerous (thought–action fusion) and feel responsible for preventing harm (inflated responsibility); this causes anxiety, and compulsions are performed to neutralise it.', '1 mark normal intrusive thoughts; 1 mark faulty interpretation; 1 mark compulsions neutralise [3]'),
        ('Explain the biological explanation of OCD.', 'OCD may be partly genetic (it runs in families), may involve low serotonin activity (SSRIs help) and overactivity in a circuit linking the orbitofrontal cortex, caudate nucleus and thalamus, so worry signals are not switched off.', '1 mark genetics; 1 mark serotonin; 1 mark brain circuit [3]'),
        ('Explain the psychodynamic explanation of OCD.', 'Freud suggested OCD arises from conflict between the id and superego, often from harsh toilet training in the anal stage; defence mechanisms such as isolation, undoing and reaction formation produce obsessions and compulsions.', '1 mark conflict/anal stage; 1 mark defence mechanisms [2]'),
    ],
    'claims': [
        ('Most people experience intrusive thoughts from time to time.', True, 'Research shows intrusive thoughts are common; the difference in OCD is how they are interpreted.'),
        ('The cognitive explanation says that OCD is caused by excess dopamine.', False, 'That would be biological; the cognitive explanation focuses on faulty interpretation of thoughts.'),
    ],
    'who': 'the cognitive explanation of OCD',
    'evals': [
        ('supporting evidence', 'strength', 'People with OCD score higher on measures of inflated responsibility and thought–action fusion than controls.'),
        ('usefulness', 'strength', 'It led to CBT and ERP, which are effective treatments.'),
        ('cause and effect', 'weakness', 'Faulty beliefs may develop as a result of OCD rather than causing it.'),
        ('reductionism', 'weakness', 'It ignores biological evidence such as genetic links and the effectiveness of SSRIs.'),
    ],
    'apply': [
        ('{person}, a new parent in {city}, has a sudden image of dropping the baby and now checks the baby many times each night, believing the thought means something terrible will happen.',
         [('Identify the cognitive bias shown by {person}.', 'Thought–action fusion (and inflated responsibility).', '1 mark [1]'),
          ('Use the cognitive explanation to explain {person}’s checking.', '{person} interprets a normal intrusive thought as dangerous and feels responsible for preventing harm, so checking is used to reduce anxiety.', '1 mark interpretation; 1 mark compulsion reduces anxiety [2]'),
          ('Explain how a biological psychologist might explain {person}’s symptoms.', 'Stress after the birth might trigger an inherited vulnerability, with low serotonin activity or overactivity in the orbitofrontal–caudate circuit.', '1 mark genes/serotonin; 1 mark brain circuit/trigger [2]')]),
    ],
})

c5c = T('Treatment: drugs (SSRIs), CBT and exposure and response prevention', 'treatment drugs ssris cbt exposure response prevention')
build(c5c, {
    'terms': [
        ('exposure and response prevention (ERP)', 'a therapy in which the client is exposed to obsession triggers and prevented from performing compulsions'),
        ('habituation', 'a decrease in anxiety after repeated or prolonged exposure to a stimulus'),
        ('relapse', 'the return of symptoms after a period of improvement'),
        ('cognitive restructuring', 'identifying and changing distorted beliefs, such as inflated responsibility'),
    ],
    'foils': ['flooding', 'token economy'],
    'mcq': [
        ('In ERP for contamination fears, a client might touch a door handle and then', 'not wash their hands', ['wash their hands immediately', 'take a sedative', 'leave the room at once'], 'Response prevention stops the compulsion.'),
        ('Why are SSRIs used to treat OCD?', 'They increase serotonin activity, which is thought to be low in OCD', ['They block dopamine', 'They cause fainting', 'They reduce blood pressure'], 'Fluvoxamine and fluoxetine are licensed for OCD.'),
        ('Why does anxiety fall during ERP?', 'Habituation occurs and the client learns the feared outcome does not happen', ['The client is distracted by rewards', 'The client is sedated', 'The client performs the compulsion secretly'], 'Prolonged exposure without neutralising.'),
    ],
    'explain': [
        ('Describe how exposure and response prevention is used to treat OCD.', 'The client and therapist build a hierarchy of triggers; the client is exposed to each (for example touching a “dirty” object) and prevented from performing the compulsion (washing) until anxiety falls through habituation, moving up the hierarchy.', '1 mark hierarchy; 1 mark exposure; 1 mark response prevention/habituation [3]'),
        ('Explain one advantage of CBT over SSRIs for OCD.', 'CBT teaches clients to challenge beliefs such as inflated responsibility and to resist compulsions, so gains last after treatment ends, whereas symptoms often return when SSRIs are stopped.', '1 mark advantage; 1 mark explained [2]'),
    ],
    'claims': [
        ('ERP allows the client to perform the compulsion as soon as anxiety starts.', False, 'The compulsion is prevented, so the client learns anxiety falls without it.'),
        ('SSRIs may take several weeks to reduce OCD symptoms.', True, 'Higher doses and longer periods are often needed than for depression.'),
    ],
    'who': 'exposure and response prevention for OCD',
    'evals': [
        ('effectiveness', 'strength', 'ERP produces large reductions in Y-BOCS scores in many clients, and gains are often maintained.'),
        ('ethics', 'weakness', 'Exposure is very distressing, so some clients refuse or drop out of treatment.'),
        ('long-term outcome', 'strength', 'Clients learn skills they can use after therapy, so relapse is lower than when drugs are stopped.'),
        ('individual differences', 'weakness', 'It works less well for people with purely mental compulsions or with low motivation.'),
    ],
    'apply': [
        ('{person}, from {city}, has a fear of germs and washes their hands over 50 times a day until the skin bleeds.',
         [('Describe how ERP could be used to help {person}.', 'Build a hierarchy (for example touching a table, a door handle, a bin lid); expose {person} to each step and prevent hand-washing for increasing periods until anxiety falls.', '1 mark hierarchy/exposure; 1 mark response prevention [2]'),
          ('Explain why ERP might be difficult for {person}.', 'Being prevented from washing will cause intense anxiety at first, so {person} may refuse or drop out.', '1 mark distress; 1 mark drop-out [2]'),
          ('Suggest why a doctor might also prescribe an SSRI for {person}.', 'It may reduce anxiety and obsessional thoughts enough for {person} to take part in ERP.', '1 mark reduces symptoms; 1 mark enables therapy [2]')]),
    ],
})
chapter(5, [c5a, c5b, c5c], OCD_SHARED)


from .g11_psychology import add_tally_pct  # noqa: E402

# ============================================================== CONSUMER 6: The physical environment

PHYS_SHARED = {
    'essays': [
        ('the physical environment of a store has a strong influence on what consumers buy',
         ['North et al. (1999): French wine outsold German wine when French music played, and vice versa.', 'Milliman (1982): slow-tempo music slowed shoppers and increased sales.', 'Layout guides customers past more products.'],
         ['Effects are often small and depend on the type of shopper and product.', 'Consumers may not be aware of the influence, but price, brand and need matter more.', 'Field studies have little control over other variables.'],
         ['ecological validity', 'usefulness', 'ethics of influencing consumers']),
    ],
    'exp': [dict(intro=['A supermarket in {city} recorded daily sales (number of items from a promoted display) on {n} days with slow-tempo background music and {n} days with fast-tempo music.',
                        '{person} compared the number of items sold per day from a display when slow-tempo or fast-tempo music was played in a store in {city}.'],
                 A='slow-tempo music', B='fast-tempo music', gA='shoppers on days with slow-tempo music', gB='shoppers on days with fast-tempo music',
                 more='will buy more items than', measure='the number of items sold', dvshort='Items sold per day', nosample=True,
                 iv='the tempo of background music (slow or fast)', dv='the number of items sold from the display each day',
                 range=(40, 160), base=(80, 95), diff=(8, 20), sd=10,
                 controls=['the same volume of music on all days', 'the same days of the week in each condition, so that busy days are balanced', 'no price promotions during the study'],
                 ethics=['shoppers do not know they are in a study, so no personal data should be recorded'],
                 concl_A='slow-tempo music increases sales.', concl_B='fast-tempo music increases sales.')],
    'plan': [('whether the type of background music in a café affects how long customers stay', 'IV: type of music', 'DV: time spent in the café (minutes)', ['field experiment', 'observation']),
             ('how shoppers feel about crowded stores', 'topic: experiences of crowding', 'measure: rating scales and open answers', ['questionnaire', 'interview'])],
    'plan_lead': 'Design',
}

c6a = T('Retail store architecture and layout: grid, freeform, racetrack', 'retail store architecture layout grid freeform racetrack')
build(c6a, {
    'terms': [
        ('grid layout', 'a store layout with long parallel aisles, often used in supermarkets, which makes products easy to find'),
        ('freeform layout', 'an irregular, flowing store layout with displays of different shapes, which encourages browsing'),
        ('racetrack layout', 'a store layout in which a main path loops around the store, leading customers past all departments'),
        ('decompression zone', 'the area just inside a store entrance where shoppers adjust to the new environment and tend not to notice products'),
        ('impulse buying', 'unplanned purchases made on the spur of the moment'),
    ],
    'mcq': [
        ('Which store layout is most typical of a supermarket?', 'Grid', ['Freeform', 'Racetrack', 'Boutique only'], 'Parallel aisles make shopping efficient.'),
        ('Which layout is most likely to encourage browsing and impulse buying in a fashion boutique?', 'Freeform', ['Grid', 'A single long aisle', 'A warehouse layout'], 'Irregular displays slow shoppers down.'),
        ('A furniture store with one path that leads customers past every department uses a', 'racetrack (loop) layout', ['grid layout', 'freeform layout', 'random layout'], 'The path guides customers through the whole store.'),
    ],
    'ar': [
        ('Retailers place essential items such as milk at the back of supermarkets.', 'Shoppers then have to walk past many other products to reach them.', 'AR', 'This increases exposure to other goods and impulse buying.'),
    ],
    'explain': [
        ('Explain one advantage and one disadvantage of a grid layout for consumers.', 'Advantage: products are easy to find and the layout is familiar, so shopping is quick. Disadvantage: it is repetitive and discourages browsing, and shoppers may have to walk long aisles.', '1 mark each [2]'),
        ('Explain why a racetrack layout may increase sales.', 'The loop path exposes customers to every department, so they see more products and are more likely to make unplanned purchases.', '1 mark exposure; 1 mark impulse purchases [2]'),
    ],
    'claims': [
        ('A freeform layout makes it easiest to find a specific product quickly.', False, 'Grid layouts are easiest for finding items; freeform layouts encourage browsing.'),
        ('Store layout can affect how long customers spend in a store.', True, 'Layouts that encourage browsing increase time in store.'),
    ],
    'who': 'Vrechopoulos et al.’s (2004) study of virtual store layouts',
    'evals': [
        ('controls', 'strength', 'Using a virtual store meant products and prices were identical, so only the layout differed between conditions.'),
        ('ecological validity', 'weakness', 'Shopping online in a simulated store is unlike walking through a real shop with crowds, sounds and smells.'),
        ('usefulness', 'strength', 'Online retailers can use the findings to design websites that are easy to use or that encourage browsing.'),
        ('generalisability', 'weakness', 'Participants were from one country and familiar with computers, so the findings may not apply to all shoppers.'),
    ],
    'apply': [
        ('A new bookshop is opening in {city}. The owner, {person}, wants customers to stay longer and buy more books on impulse.',
         [('Recommend a store layout and explain your choice.', 'A freeform layout, with displays of different shapes and themed tables, encourages browsing and impulse buying; or a racetrack that leads customers past all sections.', '1 mark layout; 1 mark justification [2]'),
          ('Explain one disadvantage of the layout you have recommended.', 'Customers looking for a specific book may find it hard to locate and become frustrated, and the layout uses floor space less efficiently.', '1 mark disadvantage; 1 mark explained [2]'),
          ('Suggest where {person} should place popular best-sellers and explain why.', 'Towards the back or centre, beyond the decompression zone, so customers walk past other books on the way.', '1 mark location; 1 mark reason [2]')]),
    ],
})

c6b = T('Sound and music in the retail environment', 'sound music retail environment')
build(c6b, {
    'terms': [
        ('music tempo', 'the speed of music, measured in beats per minute'),
        ('congruent music', 'music that fits the image of the product or store, for example French music with French wine'),
        ('atmospherics', 'the deliberate design of a store environment (sound, lighting, scent, layout) to influence shoppers'),
        ('priming', 'when exposure to one stimulus makes related ideas more accessible and influences later behaviour'),
    ],
    'foils': ['ambient scent', 'choice overload'],
    'mcq': [
        ('In North et al. (1999), what happened when French music was played?', 'More French wine than German wine was sold', ['More German wine was sold', 'No wine was sold', 'Sales of all wine fell'], 'Roughly 40 bottles of French wine versus 8 of German.'),
        ('Milliman (1982) found that slow-tempo music in a supermarket', 'slowed shoppers down and increased sales', ['made shoppers leave quickly', 'had no effect', 'reduced sales'], 'Shoppers moved more slowly and spent more.'),
        ('Areni and Kim (1993) found that playing classical music in a wine store led customers to', 'buy more expensive wine', ['buy cheaper wine', 'buy more bottles of cheap wine', 'leave the store sooner'], 'Classical music primed ideas of quality.'),
        ('When asked, most shoppers in North et al.’s study', 'did not think the music had influenced their choice', ['said the music was the main reason', 'refused to answer', 'said they disliked the music'], 'The influence appeared to be unconscious.'),
    ],
    'ar': [
        ('Background music can influence choices without shoppers being aware of it.', 'Music can prime knowledge related to the product, such as images of France.', 'AR', 'Priming explains unconscious influence.'),
    ],
    'explain': [
        ('Describe the procedure and findings of North et al. (1999).', 'In a UK supermarket, French and German accordion music was played on alternate days next to a display of French and German wines of similar price and sweetness. French wine outsold German when French music played and German wine outsold French when German music played; few shoppers said the music affected them.', '1 mark procedure; 1 mark findings; 1 mark awareness [3]'),
        ('Explain how music tempo can affect shoppers.', 'Slow music slows the pace of movement so shoppers spend longer in the store and see more products, increasing sales; fast music speeds them up, which can be useful in busy fast-food restaurants.', '1 mark slow → longer/more sales; 1 mark fast → quicker turnover [2]'),
    ],
    'claims': [
        ('North et al.’s study was a laboratory experiment.', False, 'It was a field experiment in a real supermarket.'),
        ('Music that fits the product (congruent music) can increase sales of that product.', True, 'For example French music increased French wine sales.'),
    ],
    'who': 'North et al.’s (1999) study of in-store music and wine sales',
    'evals': [
        ('ecological validity', 'strength', 'It took place in a real supermarket with real shoppers buying with their own money.'),
        ('controls', 'strength', 'Wines were matched on price and sweetness and the music alternated days, so the type of music was the main difference.'),
        ('controls', 'weakness', 'As a field experiment, other variables such as the type of customer on different days could not be fully controlled.'),
        ('ethics', 'weakness', 'Shoppers did not consent and were influenced without awareness; only those who agreed answered the questionnaire.'),
        ('sample of purchases', 'weakness', 'Relatively few bottles were sold in total, so a small number of shoppers could affect the pattern.'),
    ],
    'apply': [
        ('A café owner in {city}, {person}, wants customers to stay longer at lunchtime on quiet days but leave more quickly on busy days.',
         [('Suggest how {person} could use music tempo on quiet days and explain why.', 'Play slow-tempo music so customers relax, eat more slowly and stay longer, buying more drinks.', '1 mark slow music; 1 mark effect [2]'),
          ('Suggest how {person} could use music on busy days and explain why.', 'Play faster music so customers eat more quickly and tables are freed for new customers.', '1 mark fast music; 1 mark effect [2]'),
          ('Explain one ethical issue in using music to influence customers.', 'Customers are influenced without awareness or consent, which could be seen as manipulation.', '1 mark issue; 1 mark explained [2]')]),
    ],
})
add_tally_pct(c6b, ['A wine shop in {city} recorded bottles sold from a display of French and German wines on days with different background music.', '{person} counted bottles of French and German wine sold when different music was played.'],
              [('French music days', (30, 45), (6, 12)), ('German music days', (9, 15), (18, 26)), ('No music days', (14, 22), (12, 20))],
              ('French wine', 'German wine', 'bottles'))

c6c = T('Crowding, personal space and lighting in retail and leisure settings', 'crowding personal space lighting retail leisure settings')
build(c6c, {
    'terms': [
        ('density', 'the objective number of people in a given space'),
        ('crowding', 'the subjective, unpleasant feeling that there are too many people in a space'),
        ('proxemics', 'the study of how people use space and distance in social interaction'),
        ('intimate distance', 'the closest personal space zone (up to about 45 cm), reserved for close relationships'),
        ('social distance', 'the zone of about 1.2–3.6 m used for impersonal business interactions'),
    ],
    'mcq': [
        ('Which statement best describes crowding?', 'A subjective feeling that there are too many people present', ['The exact number of people per square metre', 'A store layout with many aisles', 'The number of staff in a store'], 'Crowding is psychological; density is physical.'),
        ('According to Hall, personal distance is about', '45 cm to 1.2 m', ['0 to 45 cm', '1.2 to 3.6 m', 'over 3.6 m'], 'Used for friends and acquaintances.'),
        ('Areni and Kim (1994) found that brighter lighting in a wine store led customers to', 'examine and handle more products', ['buy many more bottles', 'leave the store immediately', 'complain to staff'], 'Handling increased but sales did not change significantly.'),
    ],
    'explain': [
        ('Explain the difference between density and crowding.', 'Density is the objective number of people in a space; crowding is the subjective feeling that the space is too full, which depends on the person, their goals and the situation.', '1 mark each [2]'),
        ('Explain how perceived crowding can affect shoppers.', 'It can cause stress and reduce satisfaction, so shoppers buy only planned items, leave sooner or avoid the store, although some crowding can create excitement in leisure settings.', '1 mark negative effects; 1 mark qualification [2]'),
    ],
    'claims': [
        ('Higher density always makes shoppers feel crowded and unhappy.', False, 'Crowding is subjective; at a concert or market some crowding can be enjoyable.'),
        ('Lighting can draw attention to particular products in a store.', True, 'Spotlights on displays increase the time shoppers spend looking at and handling products.'),
    ],
    'who': 'research on lighting in retail settings (for example Areni and Kim, 1994)',
    'evals': [
        ('ecological validity', 'strength', 'Studies in real stores measure real shopper behaviour, such as handling and buying products.'),
        ('controls', 'weakness', 'Field studies cannot control other influences such as time of day or type of customer.'),
        ('usefulness', 'strength', 'Retailers can use lighting cheaply to highlight products they want to sell.'),
        ('validity', 'weakness', 'Handling a product does not necessarily mean buying it, so effects on sales may be small.'),
    ],
    'apply': [
        ('A department store in {city} is very busy at weekends. Managers notice that customers leave quickly without buying, and complain about being pushed in narrow aisles.',
         [('Use the concept of crowding to explain the customers’ behaviour.', 'High density and invasion of personal space create the unpleasant feeling of crowding, causing stress, so customers leave early.', '1 mark crowding; 1 mark consequence [2]'),
          ('Suggest two changes the managers could make.', 'Widen aisles or reduce displays; open more checkouts; manage entry numbers; use calm lighting and music.', '1 mark each [2]'),
          ('Explain how lighting could be used to increase interest in a new product.', 'Brighter spotlights on the display attract attention and encourage customers to look at and handle the product.', '1 mark lighting; 1 mark effect [2]')]),
    ],
})
chapter(6, [c6a, c6b, c6c], PHYS_SHARED)


# ============================================================== CONSUMER 7: The psychological environment

PSYENV_SHARED = {
    'essays': [
        ('restaurant design has a greater influence on diners than the food itself',
         ['Menu layout, descriptive labels and price format influence what diners choose and spend.', 'Seating and table spacing affect comfort and satisfaction.', 'Atmosphere (music, lighting, scent) affects mood and time spent.'],
         ['Diners return mainly because of food quality and price.', 'Many studies have small effects and use limited samples.', 'Cultural differences in personal space and dining habits limit generalisation.'],
         ['ecological validity', 'usefulness', 'individual differences']),
    ],
    'exp': [dict(intro=['A restaurant in {city} tested two menu designs. On {n} evenings the menu showed prices with a currency symbol and on {n} evenings prices were shown as plain numbers. Average spending per diner was recorded.',
                        '{person} compared average spend per diner (in dollars) on evenings when menu prices included “$” and evenings when they were plain numbers.'],
                 A='plain numbers', B='with currency symbol', gA='diners given menus with plain-number prices', gB='diners given menus with a currency symbol',
                 more='will spend more than', measure='average spending per diner', dvshort='Average spend per diner ($)', nosample=True,
                 iv='whether menu prices were shown with a currency symbol or as plain numbers', dv='the average amount spent per diner each evening in dollars',
                 range=(15, 60), base=(28, 32), diff=(2, 5), sd=3,
                 controls=['the same dishes and prices on both menus', 'the same days of the week in each condition'],
                 ethics=['diners should not be misled about prices; the full price must still be clear'],
                 concl_A='showing prices without a currency symbol increases spending.', concl_B='showing a currency symbol increases spending.')],
    'plan': [('whether diners choose healthier dishes when they are placed at the top of the menu', 'IV: position of healthy dishes', 'DV: number of healthy dishes ordered', ['field experiment']),
             ('where diners prefer to sit in a restaurant', 'behaviour: seat choice', 'categories: wall seat, window seat, centre table, booth', ['observation'])],
    'plan_lead': 'Design',
}

c7a = T('Menu design psychology and food choice', 'menu design psychology food choice')
build(c7a, {
    'terms': [
        ('menu sweet spot', 'a claimed area of a menu (often upper right) where diners’ eyes first look, so items placed there sell more'),
        ('descriptive menu label', 'a menu description that adds detail about origin, taste or tradition, such as “grandma’s homemade”'),
        ('primacy effect', 'the tendency to remember and choose items presented first'),
        ('eye tracking', 'a method that records where and for how long a person looks at a display'),
    ],
    'foils': ['decoy pricing', 'anchoring'],
    'mcq': [
        ('Yang (2012) used eye tracking to study menus and found that diners mostly read menus', 'in a sequential way, like a book', ['starting at the upper-right “sweet spot”', 'from the bottom up', 'without reading prices'], 'The study questioned the sweet-spot idea.'),
        ('Showing menu prices without a currency symbol is thought to', 'reduce the “pain of paying” and increase spending', ['make diners order less', 'make prices harder to read', 'have no effect'], 'Yang, Kimes and Sessarego (2009).'),
        ('Placing a very expensive dish at the top of a menu so that other dishes seem reasonable uses', 'anchoring', ['the bystander effect', 'cognitive dissonance', 'learned helplessness'], 'The high price acts as a reference point.'),
    ],
    'explain': [
        ('Explain how the position of items on a menu can influence food choice.', 'Items at the beginning or end of a list (primacy and recency) or highlighted in boxes are noticed and remembered more, so they are chosen more often.', '1 mark position effect; 1 mark explanation [2]'),
        ('Explain why restaurants may use descriptive labels on menus.', 'Descriptions such as “locally grown” or “slow-cooked” create expectations of quality and taste, so diners are more likely to choose the dish and rate it more highly.', '1 mark expectation; 1 mark effect on choice/rating [2]'),
    ],
    'claims': [
        ('Eye-tracking research has proved that every diner looks at the upper right of a menu first.', False, 'Yang (2012) found diners tend to read menus sequentially; the sweet spot is not supported.'),
        ('Menu design can influence how much diners spend.', True, 'Price format, layout and descriptions all affect choices.'),
    ],
    'who': 'eye-tracking research on menu design',
    'evals': [
        ('objectivity', 'strength', 'Eye tracking records exactly where and for how long people look, without relying on self-report.'),
        ('ecological validity', 'weakness', 'Participants usually read menus in a laboratory with eye-tracking equipment, not while dining with friends.'),
        ('validity', 'weakness', 'Looking at an item does not necessarily mean choosing it.'),
        ('usefulness', 'strength', 'Restaurants can design menus based on how people actually read them.'),
    ],
    'apply': [
        ('{person} is redesigning the menu of a restaurant in {city} to increase sales of the most profitable dishes.',
         [('Suggest two features of menu design {person} could use.', 'Place profitable dishes first in their section or in a highlighted box; add descriptive labels; remove currency symbols; use an expensive anchor dish.', '1 mark each [2]'),
          ('Explain why one of your suggestions might work.', 'For example, descriptive labels create expectations of quality, so diners are more likely to choose those dishes.', '1 mark feature; 1 mark psychological explanation [2]'),
          ('Explain one reason why the changes might not increase sales.', 'Regular customers already know what they want, and food quality and price may matter more than menu design.', '1 mark reason; 1 mark explained [2]')]),
    ],
})

c7b = T('Personal space and the use of seating in restaurants', 'personal space use seating restaurants')
build(c7b, {
    'terms': [
        ('sociopetal seating', 'seating arranged to encourage social interaction, such as chairs around a round table'),
        ('sociofugal seating', 'seating arranged to discourage interaction, such as rows of seats facing the same way'),
        ('table spacing', 'the distance between neighbouring tables in a restaurant'),
        ('prospect–refuge theory', 'the idea that people prefer places from which they can see others (prospect) while feeling protected (refuge)'),
    ],
    'foils': ['intimate distance', 'crowding'],
    'mcq': [
        ('Why do many diners prefer tables along walls or in booths?', 'They feel protected while still being able to see the room', ['They are closer to the kitchen', 'They are always cheaper', 'They have brighter lighting'], 'Prospect–refuge theory.'),
        ('Robson et al. (2011) found that when restaurant tables were very close together, diners', 'felt less comfortable and less satisfied', ['ordered more food', 'felt more private', 'stayed longer'], 'Close spacing reduces privacy.'),
        ('Chairs arranged around a round table are an example of', 'sociopetal seating', ['sociofugal seating', 'a grid layout', 'a racetrack layout'], 'They encourage conversation.'),
    ],
    'explain': [
        ('Explain why table spacing in a restaurant can affect diners’ satisfaction.', 'Tables that are too close invade personal space and reduce privacy, so diners feel uncomfortable and may not return, while more space increases comfort.', '1 mark personal space/privacy; 1 mark satisfaction [2]'),
    ],
    'claims': [
        ('Restaurants can always increase profit by fitting as many tables as possible into the room.', False, 'Very close tables reduce comfort and satisfaction, which may reduce spending and repeat visits.'),
        ('Seating arrangements can encourage or discourage conversation.', True, 'Sociopetal arrangements encourage it; sociofugal arrangements discourage it.'),
    ],
    'who': 'research on table spacing in restaurants',
    'evals': [
        ('usefulness', 'strength', 'Restaurant designers can balance the number of tables against diners’ comfort.'),
        ('cultural differences', 'weakness', 'Preferred personal space differs between cultures, so findings from one country may not apply elsewhere.'),
        ('self-report', 'weakness', 'Many studies ask diners to imagine or rate scenarios, which may not match their real behaviour.'),
        ('ecological validity', 'strength', 'Some studies observe diners’ real seat choices in restaurants.'),
    ],
    'apply': [
        ('A new restaurant in {city} has one large room with tables close together in rows. The manager, {person}, notices that wall tables fill first and that couples ask to move.',
         [('Use prospect–refuge theory to explain why wall tables fill first.', 'Wall tables provide refuge (protection from behind) and a view of the room (prospect), which people find comfortable.', '1 mark prospect; 1 mark refuge [2]'),
          ('Explain why couples may ask to move.', 'Close tables invade personal space and reduce privacy for conversation.', '1 mark personal space; 1 mark privacy [2]'),
          ('Suggest one change to the seating and explain its benefit.', 'Add booths or screens, or increase spacing, to give diners privacy and comfort, increasing satisfaction.', '1 mark change; 1 mark benefit [2]')]),
    ],
})

c7c = T('Consumer behaviour and the psychology of mood and atmosphere', 'consumer behaviour psychology mood atmosphere')
build(c7c, {
    'terms': [
        ('PAD model', 'Mehrabian and Russell’s model in which the environment affects pleasure, arousal and dominance, leading to approach or avoidance'),
        ('approach behaviour', 'responses such as staying longer, exploring and spending more in an environment'),
        ('avoidance behaviour', 'responses such as leaving, spending less or not returning'),
        ('ambient scent', 'a background smell in a store or venue that is not linked to a particular product'),
        ('mood', 'a fairly mild, general emotional state that can influence judgements and behaviour'),
    ],
    'mcq': [
        ('In the PAD model, the three emotional dimensions are', 'pleasure, arousal and dominance', ['price, advertising and design', 'perception, attention and decision', 'pain, anxiety and distress'], 'Environment → emotion → approach/avoidance.'),
        ('A pleasant ambient scent in a shopping centre is most likely to', 'improve mood and increase time spent', ['reduce the number of shoppers', 'cause choice overload', 'make shoppers feel crowded'], 'Scent can improve mood and evaluations.'),
        ('Leaving a shop quickly because it feels unpleasant is an example of', 'avoidance behaviour', ['approach behaviour', 'brand loyalty', 'satisficing'], 'A negative environment leads to avoidance.'),
    ],
    'explain': [
        ('Explain how a store’s atmosphere can influence consumer behaviour, using the PAD model.', 'Features such as music, lighting and scent affect shoppers’ pleasure and arousal (and feeling of control); pleasant, moderately arousing environments produce approach behaviours (staying, spending) while unpleasant ones produce avoidance.', '1 mark atmosphere affects emotion; 1 mark approach/avoidance [2]'),
    ],
    'claims': [
        ('A good mood always makes shoppers spend more.', False, 'Mood effects depend on the shopper, the product and the situation, and may be small.'),
        ('Retailers combine several features (music, scent, lighting) to create an atmosphere.', True, 'This is called atmospherics.'),
    ],
    'who': 'the PAD model of store atmosphere',
    'evals': [
        ('usefulness', 'strength', 'It gives retailers a framework for designing environments that encourage approach behaviour.'),
        ('reductionism', 'weakness', 'It reduces complex consumer responses to three emotional dimensions.'),
        ('measurement', 'weakness', 'Emotions are usually measured by self-report, which may be inaccurate.'),
        ('supporting evidence', 'strength', 'Studies of music, scent and lighting show effects on time spent and evaluations, as the model predicts.'),
    ],
    'apply': [
        ('A shopping centre in {city} has falling visitor numbers. The manager, {person}, wants to make it a more pleasant place to spend time.',
         [('Use the PAD model to suggest two changes to the atmosphere.', 'Add pleasant ambient scent and calm music to increase pleasure; use warm lighting and seating; provide clear signs to increase feelings of control (dominance).', '1 mark each change linked to the model [2]'),
          ('Explain how these changes could increase spending.', 'Increased pleasure leads to approach behaviour: visitors stay longer, see more shops and make more purchases.', '1 mark approach; 1 mark spending link [2]'),
          ('Explain one problem in measuring whether the changes work.', 'Other factors such as season, promotions or the economy also affect visitor numbers, so improvements cannot be attributed only to atmosphere.', '1 mark confounding factors; 1 mark explained [2]')]),
    ],
})
chapter(7, [c7a, c7b, c7c], PSYENV_SHARED)


# ============================================================== CONSUMER 8: Decision-making

DEC_SHARED = {
    'essays': [
        ('consumers make rational decisions when they buy products',
         ['Utility theory assumes consumers compare options and choose the one with the greatest expected value.', 'For expensive purchases, many consumers search for information and compare features.'],
         ['Simon’s satisficing shows consumers often accept the first “good enough” option.', 'Prospect theory shows losses loom larger than gains and choices change with framing.', 'Heuristics, anchoring and choice overload (Iyengar and Lepper, 2000) lead to non-rational choices.'],
         ['models of decision-making', 'cognitive biases', 'usefulness']),
    ],
    'exp': [dict(intro=['{person} set up a tasting stand in a supermarket in {city}. On {n} days it showed 24 flavours of jam and on {n} days it showed 6 flavours. The number of jars bought (per 100 visitors to the stand) was recorded each day.',
                        'In a replication of Iyengar and Lepper in {city}, purchases per 100 visitors were recorded on days with a large (24) or small (6) display of jams.'],
                 A='6 flavours', B='24 flavours', gA='shoppers shown 6 flavours', gB='shoppers shown 24 flavours',
                 more='will buy more jars per 100 visitors than', measure='purchases per 100 visitors', dvshort='Jars bought per 100 visitors', nosample=True,
                 iv='the number of flavours on display (6 or 24)', dv='the number of jars bought per 100 visitors to the stand each day',
                 range=(0, 40), base=(3, 6), diff=(10, 18), sd=3,
                 controls=['the same brand and prices of jam on all days', 'the stand in the same position and staffed by the same person'],
                 ethics=['shoppers should not be pressured to buy; they do not know they are in a study, so no personal data should be recorded'],
                 concl_A='a smaller choice set leads to more purchases (choice overload).', concl_B='a larger choice set leads to more purchases.')],
    'plan': [('whether presenting a price as a discount or as a “saving” changes willingness to buy', 'IV: discount frame or saving frame', 'DV: rating of willingness to buy (1–10)', ['laboratory experiment']),
             ('how consumers decide which smartphone to buy', 'topic: decision strategies', 'measure: open and closed questions', ['interview', 'questionnaire'])],
    'plan_lead': 'Design',
}

c8a = T('Models of decision-making: utility theory, satisficing, prospect theory', 'models decision-making utility theory satisficing prospect theory')
build(c8a, {
    'terms': [
        ('utility theory', 'a model in which rational consumers choose the option with the highest expected value or satisfaction'),
        ('satisficing', 'choosing the first option that meets a minimum standard rather than searching for the best'),
        ('prospect theory', 'Kahneman and Tversky’s model in which choices are judged as gains or losses from a reference point, and losses loom larger than gains'),
        ('loss aversion', 'the tendency to feel a loss more strongly than an equivalent gain'),
        ('maximiser', 'a person who tries to find the best possible option by comparing every alternative'),
        ('framing effect', 'when the way information is presented (as a gain or a loss) changes people’s choices'),
    ],
    'mcq': [
        ('Who introduced the idea of satisficing?', 'Herbert Simon', ['Daniel Kahneman', 'B. F. Skinner', 'Abraham Maslow'], 'Simon (1956) described bounded rationality.'),
        ('According to prospect theory, losing $50 feels', 'worse than gaining $50 feels good', ['exactly as strong as gaining $50', 'better than gaining $50', 'neutral'], 'Loss aversion.'),
        ('Schwartz et al. (2002) found that maximisers, compared with satisficers, tend to be', 'less happy and more regretful about choices', ['happier with their choices', 'less likely to compare options', 'unaffected by choices'], 'Maximisers report more regret.'),
    ],
    'ar': [
        ('Consumers do not always behave as utility theory predicts.', 'People have limited time, information and cognitive capacity (bounded rationality).', 'AR', 'Bounded rationality leads to satisficing.'),
    ],
    'explain': [
        ('Explain the difference between utility theory and satisficing.', 'Utility theory assumes consumers evaluate all options and choose the one with the greatest expected utility (maximising); satisficing assumes they stop searching once they find an option that is good enough, because time and information are limited.', '1 mark each, contrasted [2]'),
        ('Explain the main features of prospect theory.', 'Outcomes are judged as gains or losses relative to a reference point; losses loom larger than gains (loss aversion); people are risk-averse for gains but risk-seeking for losses; small probabilities are overweighted.', '1 mark reference point; 1 mark loss aversion; 1 mark risk attitudes [3]'),
    ],
    'claims': [
        ('Prospect theory assumes that people evaluate the final amount of wealth they will have.', False, 'It assumes people evaluate gains and losses relative to a reference point.'),
        ('Satisficing can reduce the time and effort involved in decisions.', True, 'The search stops once an acceptable option is found.'),
    ],
    'who': 'prospect theory as an explanation of consumer decision-making',
    'evals': [
        ('supporting evidence', 'strength', 'Experiments show consistent loss aversion and framing effects across many samples.'),
        ('usefulness', 'strength', 'Retailers use framing (for example “avoid losing your discount”) to influence choices.'),
        ('ecological validity', 'weakness', 'Much evidence comes from hypothetical gambles in questionnaires rather than real purchases.'),
        ('individual differences', 'weakness', 'People differ in risk attitudes and loss aversion, which the model does not fully explain.'),
    ],
})


def _ev(r, D):
    d = ctx(r)
    p = r.choice([10, 20, 25, 40, 50, 60, 75, 80])
    big = r.choice([100, 200, 400, 500, 1000])
    sure = r.choice([x for x in range(10, big, 10) if abs(x - p * big / 100) >= 10][: 25])
    ev = p * big / 100
    intro = f'{d["person"]} is offered a choice in a promotion at a store in {d["city"]}: Option A — a guaranteed voucher worth ${sure}. Option B — a {p}% chance of winning ${big} (otherwise nothing).'
    better = 'B' if ev > sure else 'A'
    parts = [
        ('Calculate the expected value of Option B.', f'${dn(ev)}', f'{p}% × ${big} = {p / 100:g} × {big} = ${dn(ev)}. 1 mark method; 1 mark answer [2]'),
        ('According to utility theory, which option should a rational consumer choose? Explain your answer.', f'Option {better}, because its expected value (${dn(max(ev, sure))}) is higher than the other option’s (${dn(min(ev, sure))}).', '1 mark option; 1 mark comparison of expected values [2]'),
        ('Use prospect theory to explain why many people would choose Option A even if Option B had a higher expected value.', 'For gains, people are risk-averse: a certain gain is preferred to a gamble, because the possible disappointment of getting nothing weighs heavily.', '1 mark risk-averse for gains; 1 mark explained [2]'),
        ('Explain how the choice could be reframed as a loss and how this might change behaviour.', f'If customers were first given ${big} and told they would lose ${big - sure} for certain or face a {100 - p}% chance of losing it all, prospect theory predicts more would gamble, because people are risk-seeking for losses.', '1 mark loss frame; 1 mark risk-seeking prediction [2]'),
    ]
    m = ('What is the expected value of Option B?', f'${dn(ev)}', [f'${big}', f'${dn(ev * 2)}', f'${dn(ev / 2)}', f'${sure}', f'${dn(big - ev)}'], f'{p}% × ${big} = ${dn(ev)} [1]')
    return intro, parts, m


score_tpl(c8a, 'ev', _ev)

c8b = T('Choice heuristics and choice overload', 'choice heuristics choice overload')
build(c8b, {
    'terms': [
        ('heuristic', 'a mental shortcut that simplifies decision-making'),
        ('choice overload', 'when having too many options makes choosing harder and reduces satisfaction or the likelihood of buying'),
        ('compensatory decision rule', 'a strategy in which a weakness of an option on one attribute can be balanced by a strength on another'),
        ('lexicographic heuristic', 'choosing the option that is best on the single most important attribute'),
        ('elimination by aspects', 'removing options that fail to meet a standard on one attribute at a time until one remains'),
    ],
    'mcq': [
        ('In Iyengar and Lepper’s (2000) jam study, what percentage of shoppers who stopped at the 24-jam display bought jam?', 'About 3%', ['About 30%', 'About 60%', 'About 40%'], '3% with 24 jams versus 30% with 6 jams.'),
        ('In Iyengar and Lepper’s study, which display attracted more shoppers to stop?', 'The 24-jam display', ['The 6-jam display', 'Both attracted no one', 'The display with no jam'], '60% stopped at 24 jams versus 40% at 6.'),
        ('Choosing the cheapest phone and ignoring all other features is an example of the', 'lexicographic heuristic', ['compensatory rule', 'satisficing rule', 'framing effect'], 'One most important attribute decides.'),
    ],
    'ar': [
        ('Large displays can reduce sales.', 'Too many options increase the effort of choosing and fear of making the wrong choice.', 'AR', 'This is choice overload.'),
    ],
    'explain': [
        ('Describe the procedure and findings of Iyengar and Lepper’s (2000) jam study.', 'In a supermarket, a tasting booth displayed either 24 or 6 flavours of jam on alternate hours. More shoppers stopped at the large display (60% versus 40%) but far more of those who stopped at the small display bought jam (30% versus 3%).', '1 mark procedure; 1 mark stopping; 1 mark buying [3]'),
        ('Explain the difference between compensatory and non-compensatory decision rules.', 'Compensatory rules weigh all attributes so that a weakness can be offset by a strength; non-compensatory rules (such as elimination by aspects) reject an option that fails on one attribute regardless of its other strengths.', '1 mark each [2]'),
    ],
    'claims': [
        ('More choice always makes consumers happier.', False, 'Choice overload research shows too much choice can reduce purchases and satisfaction.'),
        ('Heuristics save time but can lead to errors.', True, 'They simplify decisions at the cost of accuracy.'),
    ],
    'who': 'Iyengar and Lepper’s (2000) study of choice overload',
    'evals': [
        ('ecological validity', 'strength', 'It took place in a real supermarket with real shoppers making real purchases.'),
        ('controls', 'weakness', 'Displays alternated by hour, but the shoppers present at different times may have differed.'),
        ('reliability', 'weakness', 'Later replications have not always found choice overload, suggesting the effect depends on conditions.'),
        ('usefulness', 'strength', 'Retailers can simplify displays or product ranges to increase sales.'),
    ],
})
add_tally_pct(c8b, ['A store in {city} recorded whether shoppers who stopped at a tasting stand bought a product, with large and small displays.', '{person} recorded purchases by shoppers who stopped at displays of different sizes.'],
              [('24-flavour display', (3, 9), (110, 160)), ('6-flavour display', (25, 40), (60, 90)), ('12-flavour display', (10, 20), (80, 110))],
              ('bought', 'did not buy', 'shoppers'))

c8c = T('Intuitive thought and cognitive biases in buying', 'intuitive thought cognitive biases buying')
build(c8c, {
    'terms': [
        ('System 1 thinking', 'fast, automatic, intuitive thinking that requires little effort'),
        ('System 2 thinking', 'slow, deliberate, analytical thinking that requires effort'),
        ('anchoring', 'relying too heavily on the first piece of information (such as an initial price) when making a judgement'),
        ('decoy effect', 'when adding a clearly inferior option makes one of the original options more attractive'),
        ('scarcity heuristic', 'judging something as more valuable because it appears to be in short supply'),
    ],
    'mcq': [
        ('A “was $200, now $120” price tag mainly uses', 'anchoring', ['satisficing', 'the bystander effect', 'choice overload'], 'The original price acts as an anchor.'),
        ('Which thinking system is used for quick, impulse purchases?', 'System 1', ['System 2', 'The central route', 'Utility maximisation'], 'Fast, automatic thinking.'),
        ('“Only 3 left in stock!” on a website appeals to', 'the scarcity heuristic', ['the anchoring effect', 'loss of control', 'social facilitation'], 'Scarce items seem more valuable.'),
    ],
    'explain': [
        ('Explain how anchoring can influence how much consumers are willing to pay.', 'An initial number, such as a high “original” price, becomes a reference point; later judgements are adjusted insufficiently from it, so a discounted price seems like good value.', '1 mark anchor/reference point; 1 mark insufficient adjustment [2]'),
        ('Explain the difference between System 1 and System 2 thinking in buying decisions.', 'System 1 is fast and intuitive, used for habitual or impulse purchases; System 2 is slow and analytical, used for expensive or important purchases where options are compared.', '1 mark each with example [2]'),
    ],
    'claims': [
        ('Cognitive biases only affect people with little education.', False, 'Biases such as anchoring affect experts and non-experts alike.'),
        ('Offering a medium-sized drink priced close to a large one can make the large one more attractive.', True, 'This is the decoy effect.'),
    ],
    'who': 'research on anchoring in consumer decisions',
    'evals': [
        ('reliability', 'strength', 'Anchoring effects have been replicated many times with different products and samples.'),
        ('ecological validity', 'weakness', 'Many studies use hypothetical questions rather than real purchases.'),
        ('ethics', 'weakness', 'Retailers can use anchors to mislead consumers about value.'),
        ('usefulness', 'strength', 'Consumers can be taught to recognise anchors and make better decisions.'),
    ],
    'apply': [
        ('An online shop in {city} shows a coffee machine as “Was $450 — now $299. Only 2 left! 15 people are viewing this item.”',
         [('Identify two cognitive biases the shop is using.', 'Anchoring (was $450) and scarcity (only 2 left), plus social proof (15 people viewing).', '1 mark each [2]'),
          ('Explain how one of these biases might lead {person} to buy the machine.', 'The $450 anchor makes $299 seem like a large saving, so {person} judges it as good value without comparing other shops.', '1 mark bias; 1 mark effect [2]'),
          ('Suggest how {person} could use System 2 thinking to make a better decision.', 'Slow down, compare prices and features across shops, and decide on a budget before seeing the anchor.', '1 mark strategy; 1 mark explained [2]')]),
    ],
})
chapter(8, [c8a, c8b, c8c], DEC_SHARED)


# ============================================================== CONSUMER 9: The product

PROD_SHARED = {
    'essays': [
        ('packaging is more important than the product itself in influencing consumer choice',
         ['Packaging colour and shape affect expected taste (Becker et al., 2011).', 'Eye-level shelf placement and attractive packs attract attention.'],
         ['Repeat purchases depend on product quality and brand loyalty.', 'Price and recommendations from others also influence choice.'],
         ['usefulness', 'ecological validity', 'individual differences']),
    ],
    'exp': [dict(intro=['{person} showed {n} children in {city} a film clip in which a brand of cola appeared and {n} children the same clip with the brand removed. Afterwards each child chose a drink, and the number choosing that brand over five occasions was recorded.',
                        'In a product placement study in {city}, children watched a film clip with or without a branded drink and then chose drinks on five occasions.'],
                 A='placement clip', B='no-placement clip', gA='children who see the brand placed in a film clip', gB='children who see the clip without the brand',
                 more='will choose the placed brand more often than', measure='the number of times the brand is chosen', dvshort='Times the brand was chosen (out of 5)',
                 iv='whether the film clip contained the product placement', dv='the number of occasions (out of 5) on which the child chose the placed brand',
                 range=(0, 5), base=(1.8, 2.3), diff=(0.8, 1.4), sd=0.9,
                 controls=['the same film clip apart from the brand', 'the same drinks offered in the same positions'],
                 ethics=['parental consent; children should be offered a healthy alternative drink', 'children should not be exposed to advertising pressure beyond the study'],
                 concl_A='product placement increases children’s choice of the placed brand.', concl_B='product placement reduces choice of the brand.')],
    'plan': [('whether packaging colour affects how sweet people expect a drink to taste', 'IV: packaging colour', 'DV: expected sweetness rating (1–10)', ['laboratory experiment']),
             ('why consumers stay loyal to particular brands', 'topic: reasons for brand loyalty', 'measure: rating scales and open answers', ['questionnaire', 'interview'])],
    'plan_lead': 'Design',
}

c9a = T('Packaging and positioning of products', 'packaging positioning products')
build(c9a, {
    'terms': [
        ('packaging', 'the container and wrapping of a product, which protects it and communicates information and brand image'),
        ('shelf positioning', 'where a product is placed on a shelf, such as at eye level or the end of an aisle'),
        ('facings', 'the number of identical products displayed side by side at the front of a shelf'),
        ('sensory transference', 'when perceptions of the packaging are transferred to perceptions of the product inside'),
    ],
    'foils': ['product placement', 'brand loyalty'],
    'mcq': [
        ('Becker et al. (2011) found that yoghurt in angular packaging was expected to taste', 'more intense (sharper)', ['sweeter and milder', 'exactly the same as in rounded packs', 'unpleasant'], 'Shape cues transfer to taste expectations.'),
        ('Which shelf position is usually most noticed by shoppers?', 'Eye level', ['The bottom shelf', 'Behind the counter', 'The top of a high shelf'], 'Eye-tracking shows more attention at eye level.'),
        ('Increasing the number of facings of a product on a shelf tends to', 'increase attention to the product', ['reduce attention', 'have no effect on attention', 'make it more expensive'], 'More facings are noticed more.'),
    ],
    'explain': [
        ('Explain how packaging can influence consumers’ perception of a product.', 'Through sensory transference, features such as colour, shape and material create expectations of taste, quality or value that affect choice and even the experienced taste.', '1 mark sensory transference; 1 mark example [2]'),
        ('Explain why manufacturers pay for products to be placed at eye level.', 'Shoppers look at eye-level shelves first and longest, so products there are more likely to be noticed and bought.', '1 mark attention; 1 mark purchase [2]'),
    ],
    'claims': [
        ('Packaging only protects a product and has no psychological effect.', False, 'Packaging influences attention, expectations and perceived quality.'),
        ('End-of-aisle displays often increase sales.', True, 'They are highly visible as shoppers turn into aisles.'),
    ],
    'who': 'Becker et al.’s (2011) study of packaging and taste expectations',
    'evals': [
        ('controls', 'strength', 'The packaging differed only in shape and colour saturation while the product was the same, so differences in ratings can be attributed to packaging.'),
        ('ecological validity', 'weakness', 'Participants rated packaging in a study rather than choosing products in a real store.'),
        ('usefulness', 'strength', 'Designers can use shape and colour to signal the intended taste.'),
        ('generalisability', 'weakness', 'The study used one product type and one culture, so effects may differ for other products.'),
    ],
    'apply': [
        ('A company in {city} is launching a new, strong-flavoured mint sweet and asks {person} to design the packaging.',
         [('Suggest two packaging features {person} could use and explain why.', 'Angular shapes and highly saturated colours to signal an intense taste; clear brand name and simple design to stand out.', '1 mark each feature linked to expectation [2]'),
          ('Suggest where in stores the sweets should be placed.', 'At eye level or near checkouts, where impulse purchases are common.', '1 mark position; 1 mark reason [2]'),
          ('Explain one way to test whether the packaging works.', 'Show consumers both versions and ask them to rate expected intensity, or compare sales in stores using each design.', '1 mark method; 1 mark measure [2]')]),
    ],
})

c9b = T('Brand loyalty and brand names', 'brand loyalty brand names')
build(c9b, {
    'terms': [
        ('brand loyalty', 'repeatedly buying the same brand because of a positive attitude towards it'),
        ('brand switching', 'changing from one brand to another, for example because of price or promotions'),
        ('brand name', 'the name of a product or company, which helps consumers recognise and remember it'),
        ('sound symbolism', 'the idea that the sounds of a word suggest meanings, such as size or speed'),
        ('habitual buying', 'repeat buying from habit, with little thought or emotional attachment'),
    ],
    'mcq': [
        ('Which brand name feature is most likely to make a name memorable?', 'It is short, simple and distinctive', ['It is long and complicated', 'It is the same as a competitor’s', 'It has no meaning or sound pattern'], 'Simple names are easier to recall.'),
        ('A shopper who always buys the same toothpaste without thinking about it shows', 'habitual buying (inertia)', ['true brand loyalty with strong attachment', 'choice overload', 'satisficing in a new market'], 'Repeat purchase without commitment.'),
        ('Research on sound symbolism suggests that names with front vowels (as in “bee”) suggest products that are', 'small, light or fast', ['large and heavy', 'slow and strong', 'old-fashioned'], 'Front vowels are linked to smallness.'),
    ],
    'explain': [
        ('Explain the difference between brand loyalty and habitual buying.', 'Brand loyalty involves repeat purchase plus a positive attitude and commitment to the brand; habitual buying is repeat purchase from convenience or inertia, so the consumer easily switches if something changes.', '1 mark each [2]'),
        ('Explain how a brand name can influence consumers.', 'A meaningful or sound-symbolic name can suggest product qualities (speed, softness, strength), and a memorable name increases recognition and recall at the point of purchase.', '1 mark meaning; 1 mark memorability [2]'),
    ],
    'claims': [
        ('Brand loyalty can make consumers less sensitive to price rises.', True, 'Loyal consumers may continue to buy even when prices increase.'),
        ('Consumers choose brand names purely on how they sound.', False, 'Names work together with packaging, advertising, quality and price.'),
    ],
    'who': 'research on brand loyalty',
    'evals': [
        ('usefulness', 'strength', 'Companies can use loyalty programmes and consistent branding to keep customers.'),
        ('measurement', 'weakness', 'Repeat purchase data cannot show whether buying is true loyalty or habit.'),
        ('cultural differences', 'weakness', 'Brand names may have different meanings or sounds in other languages.'),
        ('supporting evidence', 'strength', 'Blind taste tests show branded products are often preferred only when the brand is visible, showing the power of brand image.'),
    ],
})

c9c = T('Product placement and visual attention', 'product placement visual attention')
build(c9c, {
    'terms': [
        ('product placement', 'including a branded product in a film, television programme or game in return for payment'),
        ('implicit memory', 'memory that influences behaviour without conscious awareness'),
        ('mere exposure effect', 'the tendency to develop a preference for things simply because they are familiar'),
        ('visual attention', 'the selection of particular parts of a visual scene for detailed processing'),
    ],
    'foils': ['brand loyalty', 'packaging'],
    'mcq': [
        ('In Auty and Lewis (2004), children who saw a clip from Home Alone with Pepsi were', 'more likely to choose Pepsi than children who saw a clip without it', ['less likely to choose Pepsi', 'unable to remember the film', 'more likely to choose water'], 'About 62% versus 42% chose Pepsi.'),
        ('Product placement may influence choices without awareness because of', 'implicit memory and the mere exposure effect', ['choice overload', 'satisficing', 'learned helplessness'], 'Familiarity increases liking.'),
        ('Which method is often used to study visual attention to products?', 'Eye tracking', ['EEG during sleep', 'Token economy', 'The Y-BOCS'], 'Eye tracking measures fixations.'),
    ],
    'explain': [
        ('Describe the procedure and findings of Auty and Lewis (2004).', 'Children aged about 6–7 and 11–12 watched a clip from Home Alone; for half, Pepsi was shown and mentioned. Afterwards children were offered Pepsi or Coke: about 62% of those who saw the placement chose Pepsi versus about 42% of controls, even if they did not recall seeing it.', '1 mark procedure; 1 mark findings; 1 mark implicit influence [3]'),
        ('Explain why product placement may be more effective than traditional advertising.', 'Viewers do not skip it and may not recognise it as advertising, so they do not resist the message; the product is linked to liked characters.', '1 mark not recognised/not resisted; 1 mark association [2]'),
    ],
    'claims': [
        ('Product placement only works if viewers consciously remember seeing the product.', False, 'Auty and Lewis found effects even when children did not recall the brand, suggesting implicit memory.'),
        ('Product placement in children’s programmes raises ethical concerns.', True, 'Children may not understand the persuasive intent.'),
    ],
    'who': 'Auty and Lewis’s (2004) study of product placement',
    'evals': [
        ('controls', 'strength', 'Children saw the same clip with or without the brand, so the placement was the only difference.'),
        ('ethics', 'weakness', 'Children were exposed to marketing for a sugary drink, and young children may not understand persuasive intent.'),
        ('ecological validity', 'weakness', 'Choosing a drink straight after a clip in school differs from real buying decisions days later.'),
        ('usefulness', 'strength', 'It informs debates about regulating product placement aimed at children.'),
    ],
})
add_tally_pct(c9c, ['After watching a film clip in {city}, children chose between two brands of cola. The table shows their choices.', '{person} recorded children’s drink choices after watching clips with and without a product placement.'],
              [('Saw the placement', (28, 36), (14, 22)), ('Did not see the placement', (17, 24), (24, 32)), ('Saw the placement, older children', (24, 32), (16, 24))],
              ('chose the placed brand', 'chose the other brand', 'children'))
chapter(9, [c9a, c9b, c9c], PROD_SHARED)


# ============================================================== CONSUMER 10: Advertising

ADV_SHARED = {
    'essays': [
        ('advertising to children should be banned',
         ['Young children cannot recognise persuasive intent and are highly brand-aware (Fischer et al., 1991: 91% of 6-year-olds recognised Joe Camel).', 'Advertising of unhealthy food is linked to children’s preferences.'],
         ['Parents can teach media literacy and children learn to recognise advertising as they grow older.', 'Advertising funds children’s programmes and can promote healthy products.'],
         ['ethics', 'children and psychology', 'usefulness']),
        ('the elaboration likelihood model explains how advertising persuades consumers',
         ['High-involvement consumers are persuaded by strong arguments (central route); low-involvement consumers by cues such as celebrities (peripheral route) (Petty et al., 1983).'],
         ['The model does not explain why involvement varies.', 'Emotional advertising can work in both routes.', 'Much evidence comes from laboratory studies with students.'],
         ['ecological validity', 'generalisability', 'reductionism']),
    ],
    'exp': [dict(intro=['{person} showed {n} adults in {city} an advert for a new phone with strong arguments and {n} adults an advert with a famous celebrity and weak arguments. All were told they would soon choose a phone (high involvement). Attitude to the phone (1–20) was measured.',
                        'In a test of the elaboration likelihood model in {city}, high-involvement participants rated a product (1–20) after seeing an advert with strong arguments or with a celebrity endorser.'],
                 A='strong arguments', B='celebrity endorser', gA='high-involvement participants who see strong arguments', gB='high-involvement participants who see a celebrity endorser',
                 more='will give more positive attitude ratings than', measure='attitude rating', dvshort='Attitude rating (1–20)',
                 iv='whether the advert used strong arguments or a celebrity endorser', dv='attitude to the product on a 1–20 rating scale',
                 range=(1, 20), base=(10, 12), diff=(2, 4), sd=2.3,
                 controls=['adverts of the same length and layout', 'the same product and price in both adverts'],
                 ethics=['participants should be debriefed that the product and adverts were invented'],
                 concl_A='highly involved consumers are more persuaded by strong arguments (central route).', concl_B='highly involved consumers are more persuaded by celebrity cues.')],
    'plan': [('whether children can tell the difference between adverts and programmes', 'IV: age of child', 'DV: number of adverts correctly identified', ['laboratory experiment']),
             ('how often adverts aimed at children are shown during children’s programmes', 'behaviour: adverts shown', 'categories: food, toys, games, other', ['observation'])],
    'plan_lead': 'Design',
}

c10a = T('Types of advertising and advertising media', 'types advertising media')
build(c10a, {
    'terms': [
        ('informational advertising', 'advertising that gives factual information about a product’s features, price or benefits'),
        ('transformational advertising', 'advertising that links a product with emotions, lifestyles or experiences'),
        ('comparative advertising', 'advertising that directly compares a product with a competitor’s'),
        ('celebrity endorsement', 'using a famous person to promote a product'),
        ('AIDA model', 'a model of advertising stages: Attention, Interest, Desire and Action'),
    ],
    'mcq': [
        ('An advert showing friends laughing on a beach while drinking a soft drink is an example of', 'transformational advertising', ['informational advertising', 'comparative advertising', 'product placement'], 'It links the drink to positive emotions.'),
        ('In the AIDA model, the first stage is', 'attention', ['action', 'desire', 'interest'], 'Attention, Interest, Desire, Action.'),
        ('Which advertising medium allows adverts to be targeted most precisely at individual consumers?', 'Social media and online advertising', ['Billboards', 'National newspapers', 'Radio'], 'Data allows targeting by interests.'),
    ],
    'explain': [
        ('Explain the difference between informational and transformational advertising.', 'Informational advertising presents facts (features, price, performance) to persuade rationally; transformational advertising associates the product with feelings, images or lifestyles to change how using it feels.', '1 mark each [2]'),
        ('Explain one advantage and one disadvantage of television as an advertising medium.', 'Advantage: reaches a large audience with sound and moving images, attracting attention. Disadvantage: expensive and viewers may skip or ignore adverts.', '1 mark each [2]'),
    ],
    'claims': [
        ('Informational adverts are always more effective than emotional adverts.', False, 'Effectiveness depends on the product and the audience’s involvement.'),
        ('Celebrity endorsement can increase attention to an advert.', True, 'Familiar faces attract attention and may transfer positive feelings.'),
    ],
    'who': 'the AIDA model of advertising',
    'evals': [
        ('usefulness', 'strength', 'It gives advertisers a simple checklist for designing adverts that lead to purchase.'),
        ('reductionism', 'weakness', 'It assumes a fixed sequence of stages, but consumers may buy on impulse or without interest.'),
        ('supporting evidence', 'weakness', 'There is little experimental evidence that consumers pass through the stages in order.'),
        ('practicality', 'strength', 'Each stage can be measured (for example attention by eye tracking, action by sales).'),
    ],
    'apply': [
        ('A sports brand in {city} is launching new running shoes aimed at teenagers and asks {person} to plan the advertising.',
         [('Suggest one type of advertising {person} could use and explain why.', 'Transformational advertising showing teenagers enjoying running with friends, because teenagers are influenced by lifestyle and social image; or celebrity endorsement by a young athlete.', '1 mark type; 1 mark justification [2]'),
          ('Suggest the most suitable advertising medium and justify your choice.', 'Social media, because teenagers spend much time online and adverts can be targeted at their interests.', '1 mark medium; 1 mark justification [2]'),
          ('Explain how the AIDA model could guide the campaign.', 'Grab Attention with an eye-catching video, build Interest with features, create Desire with images of success, and prompt Action with a discount code.', '1 mark stages applied; 1 mark example [2]')]),
    ],
})

c10b = T('Advertising techniques: persuasion models and the elaboration likelihood model', 'advertising techniques persuasion models elaboration likelihood model')
build(c10b, {
    'terms': [
        ('elaboration likelihood model (ELM)', 'Petty and Cacioppo’s model with two routes to persuasion depending on how much a person thinks about a message'),
        ('central route', 'persuasion through careful thought about the quality of the arguments, used when involvement is high'),
        ('peripheral route', 'persuasion through superficial cues such as attractiveness or celebrity, used when involvement is low'),
        ('involvement', 'how personally relevant and important a product or message is to the consumer'),
        ('need for cognition', 'a personality trait describing how much a person enjoys effortful thinking'),
    ],
    'mcq': [
        ('According to the ELM, a consumer with high involvement is most persuaded by', 'strong, relevant arguments', ['a famous celebrity', 'catchy music', 'the number of times the advert is shown'], 'High involvement → central route.'),
        ('Petty, Cacioppo and Schumann (1983) used adverts for', 'disposable razors', ['cigarettes', 'wine', 'running shoes'], 'Involvement was manipulated by telling participants they would choose a razor.'),
        ('Attitude change through the central route tends to be', 'longer lasting and more resistant to counter-arguments', ['brief and easily changed', 'unrelated to behaviour', 'only found in children'], 'Elaborated attitudes are stronger.'),
    ],
    'ar': [
        ('Celebrity endorsements work best for low-involvement products.', 'Consumers who are not motivated to think about a message rely on peripheral cues.', 'AR', 'Peripheral route processing explains this.'),
    ],
    'explain': [
        ('Explain the elaboration likelihood model of persuasion.', 'When motivation and ability to think about a message are high, people use the central route and are persuaded by strong arguments, producing lasting attitudes; when they are low, people use the peripheral route and are persuaded by cues such as attractive sources, producing temporary attitudes.', '1 mark two routes; 1 mark central; 1 mark peripheral [3]'),
        ('Describe the findings of Petty, Cacioppo and Schumann (1983).', 'High-involvement participants’ attitudes to a razor depended mainly on argument strength; low-involvement participants’ attitudes depended more on whether the endorsers were celebrities.', '1 mark high involvement; 1 mark low involvement [2]'),
    ],
    'claims': [
        ('The peripheral route produces stronger, longer-lasting attitude change than the central route.', False, 'Central-route attitudes are more durable and resistant.'),
        ('Distraction can reduce a person’s ability to process arguments centrally.', True, 'Ability to elaborate is reduced, so peripheral cues matter more.'),
    ],
    'who': 'the elaboration likelihood model',
    'evals': [
        ('supporting evidence', 'strength', 'Petty et al. (1983) showed involvement changed whether arguments or celebrities mattered, as predicted.'),
        ('usefulness', 'strength', 'Advertisers can match the type of advert to the involvement of the target audience.'),
        ('ecological validity', 'weakness', 'Much research used students rating mock adverts in a laboratory.'),
        ('explanatory power', 'weakness', 'It is hard to know in advance which route a consumer will use, so predictions are difficult.'),
    ],
    'apply': [
        ('{person} is marketing two products in {city}: an expensive electric car and a cheap chocolate bar.',
         [('Using the ELM, suggest how the car should be advertised and explain why.', 'With strong, detailed arguments (range, safety, running costs) because buyers are highly involved and will process centrally.', '1 mark strong arguments; 1 mark central route [2]'),
          ('Using the ELM, suggest how the chocolate bar should be advertised and explain why.', 'With peripheral cues such as a celebrity, humour or attractive images, because involvement is low.', '1 mark cues; 1 mark peripheral route [2]'),
          ('Explain why attitudes formed through the central route are more useful to the car company.', 'They are longer lasting and resistant to competitors’ messages, so buyers are more likely to stay committed until purchase.', '1 mark durable; 1 mark benefit [2]')]),
    ],
})

c10c = T('Effects of advertising on children; brand recognition', 'effects advertising children brand recognition')
build(c10c, {
    'terms': [
        ('brand recognition', 'the ability to identify a brand from its logo, name or packaging'),
        ('persuasive intent', 'the aim of an advert to make people want to buy something'),
        ('pester power', 'children’s ability to influence parents’ purchases by repeatedly asking'),
        ('media literacy', 'the ability to understand and critically evaluate media messages, including advertising'),
    ],
    'foils': ['product placement', 'brand switching'],
    'mcq': [
        ('Fischer et al. (1991) found that about what percentage of 6-year-olds matched the Joe Camel logo with cigarettes?', 'About 91%', ['About 9%', 'About 30%', 'About 50%'], 'As high as their recognition of the Disney Channel logo.'),
        ('At about what age do most children begin to understand the persuasive intent of adverts?', 'Around 7–8 years', ['Around 2 years', 'Around 16 years', 'Only as adults'], 'Younger children see adverts as information or entertainment.'),
        ('Children asking parents repeatedly for advertised toys is called', 'pester power', ['brand loyalty', 'choice overload', 'satisficing'], 'Children influence family purchases.'),
    ],
    'explain': [
        ('Explain why young children may be particularly vulnerable to advertising.', 'Young children cannot reliably distinguish adverts from programmes or understand persuasive intent, so they accept advertising claims uncritically and develop strong brand preferences.', '1 mark cannot recognise intent; 1 mark consequence [2]'),
        ('Describe the findings of Fischer et al. (1991).', 'Children aged 3–6 matched logos to products; recognition increased with age, and 91% of 6-year-olds matched Joe Camel with cigarettes, as well as they matched Mickey Mouse with the Disney Channel.', '1 mark method; 1 mark findings [2]'),
    ],
    'claims': [
        ('Recognising a brand logo means a child understands what the product is for.', False, 'Children can recognise logos without understanding the product or the advertiser’s intent.'),
        ('Some countries restrict advertising aimed at young children.', True, 'For example, rules limit advertising of unhealthy food during children’s programmes.'),
    ],
    'who': 'Fischer et al.’s (1991) study of brand logo recognition by young children',
    'evals': [
        ('standardisation', 'strength', 'All children did the same matching task with the same logo cards and game board.'),
        ('usefulness', 'strength', 'The findings informed campaigns to end cartoon characters in tobacco advertising.'),
        ('validity', 'weakness', 'Matching a logo to a product shows recognition, not that children like the product or will use it.'),
        ('generalisability', 'weakness', 'Children came from preschools in one area of the USA, so findings may not apply elsewhere.'),
        ('ethics', 'weakness', 'Showing young children tobacco logos could increase familiarity with harmful products.'),
    ],
})
add_tally_pct(c10c, ['Children of different ages in {city} were asked to match brand logos to products. The table shows correct and incorrect matches.', '{person} recorded correct and incorrect logo matches for children of different ages.'],
              [('3-year-olds', (15, 30), (25, 40)), ('4-year-olds', (25, 40), (15, 30)), ('5-year-olds', (35, 50), (10, 20)), ('6-year-olds', (45, 58), (4, 10))],
              ('correct', 'incorrect', 'matches'))
chapter(10, [c10a, c10b, c10c], ADV_SHARED)


# ============================================================== HEALTH 11: The patient–practitioner relationship

PP_SHARED = {
    'essays': [
        ('the way practitioners communicate is the most important factor in the patient–practitioner relationship',
         ['Savage and Armstrong (1990) found consultation style affected patient satisfaction.', 'McKinstry and Wang (1991) found dress affected patients’ confidence in doctors.', 'Non-verbal communication such as eye contact affects disclosure.'],
         ['Patient factors such as delay (Safer et al., 1979) and misuse of services also matter.', 'Patients may disclose more to computers than to doctors (Robinson and West, 1992).', 'Cultural expectations of doctors differ.'],
         ['usefulness', 'individual differences', 'cultural differences']),
    ],
    'exp': [dict(intro=['A health centre in {city} randomly allocated {n} patients to consultations in a directing style and {n} to a sharing style, then measured satisfaction (1–25).',
                        '{person} compared patient satisfaction scores (1–25) after directing-style and sharing-style consultations in {city}.'],
                 A='directing style', B='sharing style', gA='patients who receive a directing-style consultation', gB='patients who receive a sharing-style consultation',
                 more='will report higher satisfaction than', measure='satisfaction score', dvshort='Satisfaction score (1–25)',
                 iv='whether the doctor used a directing or a sharing consultation style', dv='score on a 25-point patient satisfaction questionnaire after the consultation',
                 range=(5, 25), base=(15, 17), diff=(1.5, 3.5), sd=2.5,
                 controls=['the same doctor using both styles', 'patients with similar, minor conditions in both groups'],
                 ethics=['patients must receive appropriate medical care whichever style is used', 'satisfaction answers should be anonymous so patients feel free to be honest'],
                 concl_A='patients are more satisfied with a directing consultation style.', concl_B='patients are more satisfied with a sharing consultation style.')],
    'plan': [('whether patients disclose more sensitive information on a computer form than to a nurse', 'IV: computer form or nurse interview', 'DV: number of sensitive items disclosed', ['field experiment']),
             ('how doctors use non-verbal communication in consultations', 'behaviour: non-verbal behaviours', 'categories: eye contact, smiling, nodding, looking at the computer', ['observation'])],
    'plan_lead': 'Design',
}

c11a = T('Practitioner and patient interpersonal skills: verbal and non-verbal communication', 'practitioner patient interpersonal skills verbal non-verbal communication')
build(c11a, {
    'terms': [
        ('verbal communication', 'communication using words, including the content, clarity and use of jargon'),
        ('non-verbal communication', 'communication without words, such as eye contact, facial expression, posture, touch and dress'),
        ('medical jargon', 'technical medical language that patients may not understand'),
        ('rapport', 'a relationship of mutual trust and understanding between practitioner and patient'),
        ('active listening', 'paying full attention, reflecting back and asking questions to show understanding'),
    ],
    'mcq': [
        ('McKinstry and Wang (1991) studied patients’ attitudes to doctors’', 'dress', ['use of computers', 'consultation length', 'prescribing'], 'Patients rated photographs of doctors in different clothing.'),
        ('Patients in McKinstry and Wang’s study generally preferred doctors who', 'dressed formally', ['wore jeans and T-shirts', 'wore no identification', 'dressed in sports clothing'], 'Formal dress inspired more confidence, especially among older patients.'),
        ('Which is an example of non-verbal communication by a doctor?', 'Maintaining eye contact while the patient speaks', ['Explaining a diagnosis', 'Writing a prescription', 'Using medical terms'], 'Eye contact is non-verbal.'),
    ],
    'explain': [
        ('Explain why the use of medical jargon can harm the patient–practitioner relationship.', 'Patients may not understand their diagnosis or treatment instructions, feel confused or intimidated and be less likely to ask questions or follow advice.', '1 mark misunderstanding; 1 mark consequence [2]'),
        ('Explain one way non-verbal communication can improve consultations.', 'Eye contact, nodding and open posture show interest and empathy, building rapport so patients disclose more and are more satisfied.', '1 mark behaviour; 1 mark effect [2]'),
    ],
    'claims': [
        ('A doctor’s clothing has no effect on how patients feel about the consultation.', False, 'McKinstry and Wang found dress affected patients’ confidence and willingness to see a doctor.'),
        ('Looking at a computer screen for most of a consultation can reduce rapport.', True, 'Patients may feel the doctor is not listening.'),
    ],
    'who': 'McKinstry and Wang’s (1991) study of doctors’ dress',
    'evals': [
        ('sample', 'strength', 'A large number of patients from several practices took part, so the results are more representative.'),
        ('ecological validity', 'weakness', 'Patients rated photographs rather than meeting real doctors, so real reactions may differ.'),
        ('usefulness', 'strength', 'It suggests doctors could adapt their dress to patients’ expectations to increase confidence.'),
        ('generalisability', 'weakness', 'Expectations of dress are cultural and change over time, so findings from Scotland in 1991 may not apply today or elsewhere.'),
    ],
    'apply': [
        ('A young doctor in {city}, {person}, often wears casual clothes, rarely looks up from the computer and uses many technical terms. Older patients complain that they do not trust {person}.',
         [('Identify two features of {person}’s communication that may reduce trust.', 'Casual dress; little eye contact (looking at the computer); use of medical jargon.', '1 mark each [2]'),
          ('Use research to explain why older patients in particular may dislike {person}’s dress.', 'McKinstry and Wang found that older patients especially preferred formal dress and had more confidence in formally dressed doctors.', '1 mark finding; 1 mark older patients [2]'),
          ('Suggest two changes {person} could make and explain their benefits.', 'Wear more formal clothing and use plain language with good eye contact, building rapport and understanding.', '1 mark each change with benefit [2]')]),
    ],
})

c11b = T('Patient and practitioner diagnosis and style: misusing health services', 'patient practitioner diagnosis style misusing health services')
build(c11b, {
    'terms': [
        ('doctor-centred style', 'a consultation style in which the doctor controls the conversation, asks closed questions and makes the decisions'),
        ('patient-centred style', 'a consultation style in which the patient is encouraged to talk, express views and share decisions'),
        ('type I error', 'diagnosing an illness in a healthy person (a false positive)'),
        ('type II error', 'failing to diagnose an illness in a person who is ill (a false negative)'),
        ('Munchausen syndrome', 'a factitious disorder in which a person repeatedly fakes or induces illness to gain medical attention'),
        ('delay in seeking treatment', 'waiting before seeking medical help, which Safer et al. divided into appraisal, illness and utilisation delay'),
    ],
    'mcq': [
        ('Savage and Armstrong (1990) found that patients were more satisfied when the doctor used a', 'directing style', ['sharing style', 'silent style', 'computer-only consultation'], 'Patients felt they received a better explanation.'),
        ('Which type of error are doctors more likely to make, according to research on diagnosis?', 'Type I (diagnosing illness in a healthy person)', ['Type II (missing an illness)', 'Neither type', 'Both equally'], 'Doctors tend to err on the side of caution.'),
        ('In Safer et al.’s (1979) model, the time between noticing a symptom and deciding one is ill is', 'appraisal delay', ['illness delay', 'utilisation delay', 'treatment delay'], 'Appraisal → illness → utilisation.'),
        ('Byrne and Long (1976) analysed thousands of recorded consultations and found that most doctors used', 'a doctor-centred style', ['a patient-centred style', 'no consistent style', 'only non-verbal communication'], 'Doctors tended to keep control.'),
    ],
    'explain': [
        ('Explain the difference between a doctor-centred and a patient-centred consultation style.', 'In a doctor-centred style the doctor asks closed questions, focuses on the physical problem and makes decisions; in a patient-centred style the doctor uses open questions, listens to the patient’s concerns and shares decisions.', '1 mark each [2]'),
        ('Explain why doctors may make more type I than type II errors.', 'Missing a serious illness (type II) could harm the patient and lead to blame, so doctors cautiously treat or investigate when unsure, even if the person is healthy.', '1 mark consequences of type II; 1 mark caution [2]'),
        ('Describe Safer et al.’s three stages of delay in seeking treatment.', 'Appraisal delay (time to decide a symptom means illness), illness delay (time to decide to seek care) and utilisation delay (time from deciding to actually attending).', '1 mark each stage [3]'),
    ],
    'claims': [
        ('Munchausen syndrome involves people who genuinely believe they are ill.', False, 'That describes illness anxiety; in Munchausen syndrome symptoms are deliberately faked or induced.'),
        ('Patients who delay seeking help may reduce the effectiveness of treatment.', True, 'Delay can allow illnesses such as cancer to progress.'),
    ],
    'who': 'Savage and Armstrong’s (1990) study of consultation styles',
    'evals': [
        ('random allocation', 'strength', 'Patients were randomly allocated to directing or sharing consultations, so differences in satisfaction are likely to be due to style.'),
        ('ecological validity', 'strength', 'It used real consultations in a real general practice.'),
        ('generalisability', 'weakness', 'It took place in one practice with one doctor, so results may not apply to other doctors or patient groups.'),
        ('ethics', 'weakness', 'Patients were not told their consultation style was being varied, although all received appropriate care.'),
    ],
    'apply': [
        ('{person}, from {city}, noticed a lump three months ago but has only just visited a doctor. {person} says: “At first I thought it was nothing, then I meant to book an appointment but kept putting it off.”',
         [('Identify the stages of delay in {person}’s account using Safer et al.’s model.', 'Appraisal delay (“thought it was nothing”) and utilisation delay (meant to book but put it off).', '1 mark each [2]'),
          ('Suggest one reason for each type of delay.', 'Appraisal: no pain, so the symptom seemed unimportant. Utilisation: fear of a serious diagnosis or practical problems such as work.', '1 mark each [2]'),
          ('Suggest how health services could reduce such delays.', 'Public campaigns about warning signs and easier, faster appointment systems.', '1 mark each [2]')]),
    ],
})

c11c = T('Disclosure of information and consultation styles', 'disclosure information consultation styles')
build(c11c, {
    'terms': [
        ('disclosure', 'the patient revealing information about symptoms or personal behaviour to a practitioner'),
        ('computerised interview', 'a set of questions answered by the patient on a computer rather than face to face'),
        ('confidentiality', 'keeping a patient’s personal information private'),
        ('sharing style', 'a consultation in which the doctor asks the patient’s opinions and involves them in decisions'),
    ],
    'foils': ['type I error', 'directing style'],
    'mcq': [
        ('Robinson and West (1992) found that patients at a genito-urinary clinic disclosed more symptoms', 'on a computer questionnaire than in a face-to-face interview', ['to the doctor than on the computer', 'equally in both formats', 'only to nurses'], 'Computers reduced embarrassment.'),
        ('Why might patients disclose more to a computer?', 'They feel less embarrassed and less judged', ['Computers ask fewer questions', 'Computers give a diagnosis immediately', 'They are paid to use it'], 'Reduced social evaluation.'),
    ],
    'explain': [
        ('Describe the findings of Robinson and West (1992).', 'Patients attending a genito-urinary clinic reported more symptoms and more sensitive information (such as numbers of sexual partners) on a computer questionnaire than on a paper form or to a doctor.', '1 mark more disclosure to computer; 1 mark sensitive information [2]'),
        ('Explain why disclosure is important in consultations.', 'Accurate diagnosis and treatment depend on full information; if patients withhold symptoms through embarrassment, doctors may make type II errors.', '1 mark accurate diagnosis; 1 mark consequence [2]'),
    ],
    'claims': [
        ('Patients always tell doctors everything about their symptoms.', False, 'Embarrassment, fear or social desirability can lead patients to withhold information.'),
        ('Assuring confidentiality may increase disclosure.', True, 'Patients feel safer revealing sensitive information.'),
    ],
    'who': 'Robinson and West’s (1992) study of disclosure to computers',
    'evals': [
        ('ecological validity', 'strength', 'Real patients attending a real clinic answered questions about their own health.'),
        ('usefulness', 'strength', 'Clinics can use computer questionnaires before consultations to collect sensitive information.'),
        ('generalisability', 'weakness', 'Sexual health is especially embarrassing, so patients with other conditions may not disclose more to computers.'),
        ('validity', 'weakness', 'More disclosure on a computer does not prove the information is more accurate.'),
    ],
    'apply': [
        ('A sexual health clinic in {city} finds that patients often do not mention important symptoms to the nurse. The manager, {person}, wants to improve disclosure.',
         [('Use Robinson and West’s findings to suggest one change.', 'Ask patients to complete a confidential computer questionnaire before seeing the nurse.', '1 mark change; 1 mark link to research [2]'),
          ('Explain why this change might increase disclosure.', 'Patients feel less embarrassed and judged by a computer than by a person, so they report sensitive symptoms.', '1 mark reduced embarrassment; 1 mark effect [2]'),
          ('Explain one problem with the change.', 'Some patients, such as older people, may be uncomfortable with computers, and nurses may miss non-verbal cues.', '1 mark problem; 1 mark explained [2]')]),
    ],
})
chapter(11, [c11a, c11b, c11c], PP_SHARED)


# ============================================================== HEALTH 12: Adherence to medical advice

ADH_SHARED = {
    'essays': [
        ('objective measures of adherence are better than subjective measures',
         ['Pill counts and electronic monitors (such as TrackCap) do not rely on honesty or memory.', 'Biological measures (blood or urine tests) can show whether the drug has been taken.'],
         ['Removing pills from a bottle does not prove they were taken.', 'Biological tests are invasive and costly.', 'Self-report is cheap, quick and can reveal reasons for non-adherence.'],
         ['validity', 'practicality', 'ethics']),
        ('non-adherence is usually a rational decision',
         ['Patients may weigh side effects against benefits (rational non-adherence).', 'The health belief model explains adherence through perceived costs and benefits.'],
         ['Much non-adherence is unintentional, such as forgetting.', 'Complex regimens and poor communication cause non-adherence.'],
         ['health belief model', 'individual differences', 'usefulness']),
    ],
    'exp': [dict(intro=['A clinic in {city} gave {n} children with asthma a fun spacer device with a whistle and spinning disc and {n} children a standard spacer. The number of days (out of 14) on which the inhaler was used as prescribed was recorded.',
                        '{person} compared adherence (days out of 14 with correct inhaler use) for children using a fun spacer or a standard spacer.'],
                 A='fun spacer', B='standard spacer', gA='children using a fun spacer', gB='children using a standard spacer',
                 more='will use their inhaler as prescribed on more days than', measure='the number of adherent days', dvshort='Days with correct use (out of 14)',
                 iv='whether children used a fun spacer device or a standard spacer', dv='the number of days out of 14 on which the inhaler was used as prescribed (from parent diaries)',
                 range=(0, 14), base=(7, 9), diff=(1.5, 3.5), sd=2,
                 controls=['children of similar age and asthma severity in both groups', 'the same inhaler medication and instructions'],
                 ethics=['all children must continue to receive their medication', 'parental consent and the child’s agreement'],
                 concl_A='a fun spacer improves children’s adherence to inhaler use.', concl_B='a standard spacer leads to better adherence.')],
    'plan': [('whether text-message reminders improve adherence to medication in young adults', 'IV: reminders or no reminders', 'DV: percentage of doses taken (electronic monitor)', ['field experiment']),
             ('why patients stop taking prescribed medication', 'topic: reasons for non-adherence', 'measure: rating scales and open answers', ['interview', 'questionnaire'])],
    'plan_lead': 'Design',
}

c12a = T('Types of non-adherence and reasons: rational non-adherence, health belief model', 'types non-adherence reasons rational non-adherence health belief model')
build(c12a, {
    'terms': [
        ('adherence', 'the extent to which a patient’s behaviour matches the medical advice they have been given'),
        ('rational non-adherence', 'deliberately not following advice for reasons that make sense to the patient, such as side effects or cost'),
        ('health belief model', 'a model predicting health behaviour from perceived susceptibility, severity, benefits, barriers and cues to action'),
        ('cues to action', 'triggers, such as symptoms or reminders, that prompt a person to take a health action'),
        ('perceived barriers', 'the costs or obstacles a person believes stand in the way of a health behaviour'),
    ],
    'mcq': [
        ('Which component of the health belief model refers to a person’s belief about how likely they are to get an illness?', 'Perceived susceptibility', ['Perceived severity', 'Perceived barriers', 'Cues to action'], 'Susceptibility = likelihood.'),
        ('A patient stops taking tablets because they cause severe nausea and the illness has few symptoms. This is', 'rational non-adherence', ['unintentional non-adherence', 'Munchausen syndrome', 'a type II error'], 'A reasoned decision.'),
        ('Becker et al. (1978) used the health belief model to study', 'mothers’ adherence to their children’s asthma medication', ['doctors’ dress', 'pain in amputees', 'shift work in factories'], 'Adherence was related to HBM beliefs.'),
    ],
    'ar': [
        ('Forgetting to take a tablet is not rational non-adherence.', 'Rational non-adherence involves a deliberate decision not to follow advice.', 'AR', 'Forgetting is unintentional.'),
    ],
    'explain': [
        ('Explain the health belief model as an explanation of adherence.', 'A person is more likely to adhere if they believe they are susceptible to an illness that is serious, that the treatment has benefits that outweigh the barriers (cost, side effects), and if there is a cue to action; self-efficacy may also be included.', '1 mark susceptibility/severity; 1 mark benefits v barriers; 1 mark cues [3]'),
        ('Explain the difference between intentional and unintentional non-adherence.', 'Intentional non-adherence is a deliberate decision (for example because of side effects); unintentional non-adherence happens without a decision, such as forgetting or misunderstanding instructions.', '1 mark each [2]'),
    ],
    'claims': [
        ('Non-adherence to medication is very rare.', False, 'Studies suggest a large proportion of patients (often estimated at around half) do not take medication exactly as prescribed.'),
        ('Complex medication regimes can reduce adherence.', True, 'More doses and drugs make it harder to follow instructions.'),
    ],
    'who': 'the health belief model',
    'evals': [
        ('supporting evidence', 'strength', 'Becker et al. found that mothers’ beliefs about susceptibility and severity were related to adherence measured by blood tests.'),
        ('usefulness', 'strength', 'Interventions can target specific beliefs, for example increasing perceived severity or reducing barriers.'),
        ('reductionism', 'weakness', 'It assumes rational decision-making and ignores emotions, habits and social pressure.'),
        ('measurement', 'weakness', 'Components are measured by self-report and different studies measure them in different ways.'),
    ],
    'apply': [
        ('{person}, aged 55, from {city}, has high blood pressure but often skips tablets. {person} feels well, finds the tablets cause tiredness and does not think the condition is serious.',
         [('Use the health belief model to explain {person}’s non-adherence.', 'Low perceived severity (“not serious”) and susceptibility (feels well), and high perceived barriers (tiredness), so the benefits do not seem to outweigh the costs.', '1 mark severity/susceptibility; 1 mark barriers [2]'),
          ('Identify the type of non-adherence shown by {person}.', 'Rational (intentional) non-adherence.', '1 mark [1]'),
          ('Suggest two ways the doctor could increase {person}’s adherence.', 'Explain the risks of untreated high blood pressure (increasing perceived severity) and change to a drug with fewer side effects (reducing barriers); use reminders as cues to action.', '1 mark each [2]')]),
    ],
})

c12b = T('Measuring adherence: subjective, objective and biological methods', 'measuring adherence subjective objective biological methods')
build(c12b, {
    'terms': [
        ('subjective measure of adherence', 'a measure based on self-report by the patient or the practitioner’s judgement'),
        ('pill count', 'an objective measure in which the number of remaining pills is compared with the number that should remain'),
        ('electronic monitoring', 'a device, such as a smart bottle cap, that records each time a medicine container is opened'),
        ('biological measure of adherence', 'testing blood, urine or breath for the presence of a drug or marker'),
    ],
    'foils': ['health belief model', 'cues to action'],
    'mcq': [
        ('Chung and Naya (2000) used TrackCap to measure adherence to', 'glaucoma eye-drop medication', ['asthma inhalers', 'antidepressants', 'vaccinations'], 'An electronic cap recorded when the bottle was opened.'),
        ('Which is a biological measure of adherence?', 'A blood test for the level of the drug', ['A questionnaire about medication use', 'A pill count', 'A doctor’s rating'], 'It detects the drug in the body.'),
        ('Which is the main weakness of self-report measures of adherence?', 'Patients may overestimate their adherence to please the doctor', ['They are expensive', 'They are invasive', 'They need laboratory equipment'], 'Social desirability bias.'),
    ],
    'explain': [
        ('Explain one strength and one weakness of pill counts as a measure of adherence.', 'Strength: objective and cheap, not relying on memory or honesty. Weakness: removing pills does not prove they were taken correctly (pills may be thrown away or taken at the wrong time).', '1 mark each [2]'),
        ('Explain why biological measures of adherence may be more valid than self-report.', 'They show whether the drug is actually present in the body, so they are not affected by social desirability or poor memory, although levels also depend on metabolism.', '1 mark presence in body; 1 mark not affected by bias [2]'),
    ],
    'claims': [
        ('Electronic monitoring proves that patients have taken their medication.', False, 'It shows when the container was opened, not that the dose was taken.'),
        ('Using more than one method of measuring adherence increases validity.', True, 'Methods can be compared to check agreement.'),
    ],
    'who': 'electronic monitoring (for example TrackCap) as a measure of adherence',
    'evals': [
        ('objectivity', 'strength', 'It records the date and time of each opening automatically, so it does not depend on memory or honesty.'),
        ('validity', 'weakness', 'Opening the container does not guarantee that the medicine was taken correctly.'),
        ('demand characteristics', 'weakness', 'Patients who know they are monitored may adhere better than usual.'),
        ('practicality', 'weakness', 'Devices are expensive compared with questionnaires.'),
    ],
})


def _adh(r, D):
    d = ctx(r)
    days = r.choice([14, 21, 28, 30])
    per = r.choice([1, 2, 3])
    pres = days * per
    taken = r.randint(int(pres * 0.45), pres - 1)
    start = pres + r.choice([0, 4, 6, 10])
    left = start - taken
    p = 100 * taken / pres
    intro = (f'{d["person"]}, a patient in {d["city"]}, was prescribed {per} tablet{"s" if per > 1 else ""} a day for {days} days and given a bottle of {start} tablets. '
             f'At the end of the period, a pill count found {left} tablets left.')
    parts = [
        ('Calculate the number of tablets that should have been taken.', str(pres), f'{per} × {days} = {pres} [1]'),
        ('Calculate the percentage adherence shown by the pill count. Give your answer to one decimal place.', f'{d1(p)}%', f'Taken = {start} − {left} = {taken}; {taken} ÷ {pres} × 100 = {d1(p)}%. 1 mark tablets taken; 1 mark percentage [2]'),
        ('Adherence of 80% or more is often treated as acceptable. State whether this patient meets the standard.', 'Yes' if p >= 80 else 'No' + f' ({d1(p)}%)' if p < 80 else f'Yes ({d1(p)}%)', f'{d1(p)}% is {"at or above" if p >= 80 else "below"} 80% [1]'),
        ('Explain why the pill count may overestimate adherence.', 'Tablets may have been removed but not taken (thrown away, lost or shared), or taken at the wrong times.', '1 mark removal ≠ taking; 1 mark example [2]'),
        ('Suggest a more valid way of measuring this patient’s adherence and explain why.', 'A biological measure such as a blood test for the drug, or electronic monitoring of bottle openings, which does not rely on counting what is left.', '1 mark method; 1 mark reason [2]'),
    ]
    m = ('What percentage adherence does the pill count show, to one decimal place?', f'{d1(p)}%', [f'{d1(100 * left / pres)}%', f'{d1(100 * taken / start)}%', f'{d1(min(99.9, p + 10))}%', f'{d1(max(1, p - 10))}%'], f'{taken} ÷ {pres} × 100 = {d1(p)}% [1]')
    return intro, parts, m


score_tpl(c12b, 'adherence', _adh)

c12c = T('Improving adherence: behavioural techniques and reminders', 'improving adherence behavioural techniques reminders')
build(c12c, {
    'terms': [
        ('prompt', 'a reminder, such as a letter, phone call or text message, to perform a health behaviour'),
        ('positive reinforcement for adherence', 'rewarding patients for following medical advice to increase future adherence'),
        ('Funhaler', 'a spacer device for children’s asthma inhalers with incentive toys (a whistle and spinning disc) that work only with correct breathing'),
        ('tailoring', 'fitting a treatment regime to a patient’s daily routine to make adherence easier'),
    ],
    'foils': ['pill count', 'health belief model'],
    'mcq': [
        ('Yokley and Glenwick (1984) found which intervention most increased children’s immunisation rates?', 'A monetary incentive for parents', ['General prompts only', 'No contact', 'A leaflet about the diseases'], 'Incentives and specific prompts worked best.'),
        ('Watt et al. (2003) found that the Funhaler', 'increased the number of children who were medicated as prescribed', ['reduced adherence', 'had no effect', 'caused side effects'], 'Parents reported better adherence with the Funhaler.'),
        ('Sending a text message at the time a dose is due is an example of', 'a prompt (reminder)', ['a biological measure', 'rational non-adherence', 'a token economy'], 'Cue to action.'),
    ],
    'explain': [
        ('Explain how operant conditioning can be used to improve adherence.', 'Adherent behaviour is followed by a reward (praise, money, toys, tokens), so it is positively reinforced and more likely to be repeated; for example the Funhaler’s whistle rewards correct inhaler use.', '1 mark reinforcement principle; 1 mark example [2]'),
        ('Describe the findings of Watt et al. (2003).', 'Children aged about 1.5–6 years used the Funhaler (with a whistle and spinning disc) instead of a standard spacer; more parents reported medicating their child the previous day and using the correct technique with the Funhaler.', '1 mark procedure; 1 mark findings [2]'),
    ],
    'claims': [
        ('Reminders only help patients who intentionally refuse treatment.', False, 'Reminders mainly help unintentional non-adherence, such as forgetting.'),
        ('Making treatment fun can improve children’s adherence.', True, 'The Funhaler is an example.'),
    ],
    'who': 'Watt et al.’s (2003) Funhaler study',
    'evals': [
        ('repeated measures', 'strength', 'Each child used both the standard spacer and the Funhaler, so differences between children were controlled.'),
        ('self-report', 'weakness', 'Adherence was reported by parents, who may have exaggerated use of the new device.'),
        ('sample size', 'weakness', 'The sample was small (about 30 children), so the results may not generalise.'),
        ('usefulness', 'strength', 'A cheap device could improve the management of asthma in young children.'),
    ],
    'apply': [
        ('A clinic in {city} finds that many teenage patients with diabetes forget to check their blood sugar levels.',
         [('Suggest one behavioural technique to improve adherence and explain how it works.', 'Give points or rewards for each recorded check (positive reinforcement), so checking becomes more frequent.', '1 mark technique; 1 mark explanation [2]'),
          ('Suggest how reminders could be used.', 'Send text-message or app alerts at times when checks are due, acting as cues to action.', '1 mark reminder; 1 mark cue to action [2]'),
          ('Explain one problem with using rewards to improve adherence.', 'Adherence may fall when rewards stop, because the behaviour was maintained by the external reward.', '1 mark extinction; 1 mark explained [2]')]),
    ],
})
chapter(12, [c12a, c12b, c12c], ADH_SHARED)


# ============================================================== HEALTH 13: Pain

PAIN_SHARED = {
    'essays': [
        ('the gate control theory explains pain better than specificity theory',
         ['Gate control theory explains why rubbing an injury or TENS reduces pain (large fibres close the gate).', 'It explains psychological influences on pain, such as attention and mood, through descending signals.', 'It can account for phantom limb pain, which specificity theory cannot.'],
         ['The exact location of the “gate” has not been identified.', 'It does not fully explain chronic pain without injury.', 'Specificity theory correctly identifies specialised pain receptors.'],
         ['psychological factors', 'usefulness', 'reductionism']),
    ],
    'exp': [dict(intro=['A hospital in {city} compared pain ratings (0–10) after minor surgery for {n} patients who used attention diversion (a video game) and {n} patients who did not.',
                        '{person} compared self-reported pain (0–10) for patients using attention diversion or no technique during dressing changes.'],
                 A='attention diversion', B='no technique', gA='patients using attention diversion', gB='patients using no technique',
                 more='will report lower pain than', measure='pain rating', dvshort='Pain rating (0–10)', higher='B', nosample=True,
                 iv='whether patients used attention diversion or no technique', dv='pain rating on a 0–10 numerical scale',
                 range=(0, 10), base=(3.5, 4.5), diff=(1.2, 2.5), sd=1.3,
                 controls=['the same procedure and pain medication for all patients', 'pain rated at the same time point'],
                 ethics=['no patient should be denied normal pain relief', 'patients can stop the technique at any time'],
                 concl_A='attention diversion increases pain.', concl_B='attention diversion reduces reported pain.')],
    'plan': [('whether listening to music reduces pain during a cold-water task', 'IV: music or silence', 'DV: time hand kept in cold water (seconds)', ['laboratory experiment']),
             ('how nurses assess pain in patients who cannot speak', 'behaviour: pain behaviours', 'categories: grimacing, guarding, moaning, restlessness', ['observation'])],
    'plan_lead': 'Design',
}

c13a = T('Types and theories of pain: specificity and gate control theory', 'types theories pain specificity gate control theory')
build(c13a, {
    'terms': [
        ('acute pain', 'pain that lasts for a short time (usually less than three to six months) and is linked to tissue damage'),
        ('chronic pain', 'pain that persists for longer than about three to six months'),
        ('specificity theory', 'the theory that pain is a direct response from specific pain receptors, with the amount of pain proportional to the injury'),
        ('gate control theory', 'Melzack and Wall’s theory that a neural gate in the spinal cord controls how many pain signals reach the brain'),
        ('phantom limb pain', 'pain felt in a limb that has been amputated'),
        ('nociceptor', 'a sensory receptor that responds to potentially damaging stimuli'),
    ],
    'mcq': [
        ('Who proposed the gate control theory of pain?', 'Melzack and Wall', ['Holmes and Rahe', 'Janis and Feshbach', 'Petty and Cacioppo'], 'Melzack and Wall (1965).'),
        ('According to gate control theory, the gate is located in the', 'dorsal horn of the spinal cord', ['hippocampus', 'skin', 'stomach'], 'Signals are modulated in the spinal cord.'),
        ('Which phenomenon is difficult for specificity theory to explain?', 'Phantom limb pain', ['Pain after a cut', 'Pain from a burn', 'Pain from a broken bone'], 'There are no receptors in a missing limb.'),
        ('Rubbing an injured area may reduce pain because it', 'stimulates large fibres that close the gate', ['opens the gate', 'damages nociceptors', 'increases inflammation'], 'Large-diameter fibres inhibit transmission.'),
    ],
    'ar': [
        ('Anxiety can make pain feel worse.', 'Descending signals from the brain can open the pain gate.', 'AR', 'Gate control theory explains psychological influences on pain.'),
    ],
    'explain': [
        ('Explain the gate control theory of pain.', 'Pain signals travel along small fibres to the spinal cord, where a “gate” (in the dorsal horn) controls whether they pass to the brain. Activity in large fibres (touch) and descending signals from the brain (calm, distraction) close the gate; small-fibre activity and anxiety open it.', '1 mark gate in spinal cord; 1 mark small/large fibres; 1 mark descending control [3]'),
        ('Explain one weakness of specificity theory.', 'It cannot explain why the same injury causes different amounts of pain in different situations, or pain without injury such as phantom limb pain, because it ignores psychological factors.', '1 mark weakness; 1 mark example [2]'),
    ],
    'claims': [
        ('Specificity theory says psychological factors strongly affect pain.', False, 'Specificity theory sees pain as a direct response to injury; gate control theory includes psychological factors.'),
        ('Chronic pain may continue after the original injury has healed.', True, 'Chronic pain can persist without ongoing tissue damage.'),
    ],
    'who': 'the gate control theory of pain',
    'evals': [
        ('explanatory power', 'strength', 'It explains psychological effects on pain and why techniques such as distraction, rubbing and TENS reduce pain.'),
        ('usefulness', 'strength', 'It led to treatments such as TENS and supports psychological pain management.'),
        ('evidence', 'weakness', 'The physical gate mechanism has not been clearly located.'),
        ('chronic pain', 'weakness', 'It does not fully explain chronic pain that persists without an obvious physical cause.'),
    ],
})

c13b = T('Measuring pain: self-report scales, observational and behavioural measures', 'measuring pain self-report scales observational behavioural measures')
build(c13b, {
    'terms': [
        ('visual analogue scale (VAS)', 'a line, usually 100 mm long, on which patients mark their pain between “no pain” and “worst pain imaginable”'),
        ('McGill Pain Questionnaire (MPQ)', 'a self-report measure in which patients choose words from groups describing the sensory, affective and evaluative qualities of pain'),
        ('Wong–Baker FACES scale', 'a pain rating scale using drawings of faces from happy to crying, often used with children'),
        ('UAB Pain Behaviour Scale', 'an observational scale in which a clinician rates ten pain behaviours as none, occasional or frequent'),
    ],
    'mcq': [
        ('The McGill Pain Questionnaire was developed by', 'Melzack (1975)', ['Holmes and Rahe (1967)', 'Beck (1961)', 'Hackman and Oldham (1976)'], 'Melzack also co-developed gate control theory.'),
        ('Which pain measure is most suitable for a 4-year-old child?', 'The Wong–Baker FACES scale', ['The McGill Pain Questionnaire', 'A 100-item interview', 'The BDI'], 'Faces do not require reading.'),
        ('In the UAB Pain Behaviour Scale, each behaviour is rated as', 'none (0), occasional (½) or frequent (1)', ['0 to 10', 'yes or no only', '0 to 100'], 'Ten behaviours scored 0, ½ or 1.'),
    ],
    'explain': [
        ('Explain one strength and one weakness of the McGill Pain Questionnaire.', 'Strength: it measures several qualities of pain (sensory, affective, evaluative), not just intensity. Weakness: it needs a good vocabulary and takes time, so it is unsuitable for children or people with limited language.', '1 mark each [2]'),
        ('Explain why observational measures of pain are useful.', 'They can be used with people who cannot report their pain (young children, people with dementia) and are less affected by self-report bias.', '1 mark who; 1 mark reason [2]'),
    ],
    'claims': [
        ('A visual analogue scale measures many different qualities of pain.', False, 'A VAS measures one dimension, usually intensity.'),
        ('Pain is subjective, so self-report is an important part of measuring it.', True, 'Only the person can describe their experience of pain.'),
    ],
    'who': 'the McGill Pain Questionnaire',
    'evals': [
        ('validity', 'strength', 'It measures sensory, affective and evaluative qualities of pain, giving a fuller picture than a single rating.'),
        ('reliability', 'strength', 'It is standardised, with the same word lists and scoring for every patient.'),
        ('usefulness', 'weakness', 'It is long and requires good vocabulary, so it cannot be used with young children or some patients.'),
        ('self-report', 'weakness', 'Patients may exaggerate or minimise pain, for example to obtain medication or to appear brave.'),
    ],
})

UAB = ['vocal complaints (verbal)', 'non-verbal complaints (moans, groans)', 'time spent lying down', 'facial grimaces', 'standing posture', 'mobility', 'body language (clutching, rubbing)', 'use of visible supportive equipment', 'stationary movement', 'medication use']


def _uab(r, D):
    d = ctx(r)
    lvl = r.choice([0.25, 0.4, 0.55, 0.7])
    sc = [r.choices([0, 0.5, 1], weights=[1 - lvl, 0.6, lvl])[0] for _ in UAB]
    tot = sum(sc)
    w = {0: 'none', 0.5: 'occasional', 1: 'frequent'}
    intro = (f'A nurse in {d["city"]} used the UAB Pain Behaviour Scale (none = 0, occasional = ½, frequent = 1) to rate {d["person"]} after surgery: '
             + '; '.join(f'{b}: {w[s]}' for b, s in zip(UAB, sc)) + '.')
    parts = [
        ('Calculate the total UAB Pain Behaviour score.', dn(tot), f'Sum of ratings = {dn(tot)} (out of 10). 1 mark converting ratings; 1 mark total [2]'),
        ('Explain one advantage of using this observational scale rather than asking the patient to rate their pain.', 'It can be used when patients cannot communicate well (for example after anaesthetic) and is less affected by self-report bias.', '1 mark advantage; 1 mark explained [2]'),
        ('Explain why two nurses might give different scores for the same patient.', 'Ratings involve judgement (for example whether grimacing is “occasional” or “frequent”), so inter-rater reliability may be imperfect without training.', '1 mark subjective judgement; 1 mark inter-rater reliability [2]'),
        ('Suggest how the reliability of the scale could be improved.', 'Train nurses with clear definitions and video examples, and check that two nurses rating the same patients agree.', '1 mark training/definitions; 1 mark check agreement [2]'),
    ]
    m = ('What is the total UAB Pain Behaviour score?', dn(tot), [dn(tot + 0.5), dn(max(0, tot - 0.5)), dn(tot + 1), dn(sum(1 for s in sc if s > 0)), dn(max(0, tot - 1))], f'Sum = {dn(tot)} [1]')
    return intro, parts, m


score_tpl(c13b, 'uab', _uab)

c13c = T('Managing and controlling pain: medical and psychological techniques', 'managing controlling pain medical psychological techniques')
build(c13c, {
    'terms': [
        ('analgesic', 'a drug that relieves pain, such as paracetamol or an opioid'),
        ('attention diversion', 'a technique in which the person focuses on something other than the pain'),
        ('non-pain imagery', 'imagining a pleasant scene or experience incompatible with pain'),
        ('cognitive redefinition', 'replacing threatening thoughts about pain with more constructive, realistic ones'),
        ('TENS', 'transcutaneous electrical nerve stimulation: mild electrical pulses through the skin to reduce pain'),
        ('acupuncture', 'inserting fine needles into specific points of the body to relieve pain'),
    ],
    'mcq': [
        ('According to gate control theory, TENS reduces pain by', 'stimulating large fibres that close the gate', ['blocking dopamine receptors', 'damaging nerves', 'increasing anxiety'], 'Electrical stimulation of large fibres.'),
        ('Which is a psychological technique for managing pain?', 'Non-pain imagery', ['Morphine', 'Surgery to cut nerves', 'Ibuprofen'], 'Imagery uses cognition.'),
        ('Which type of analgesic is most likely to cause dependence?', 'Opioids such as morphine', ['Paracetamol', 'Ibuprofen in small doses', 'A placebo'], 'Opioids carry a risk of tolerance and dependence.'),
    ],
    'explain': [
        ('Explain how attention diversion can reduce pain, using gate control theory.', 'Focusing attention away from the pain (on a game, music or a task) sends descending signals from the brain that close the gate in the spinal cord, so fewer pain signals reach the brain.', '1 mark attention away; 1 mark descending signals close gate [2]'),
        ('Explain one strength and one weakness of drug treatments for pain.', 'Strength: analgesics act quickly and are effective for acute pain. Weakness: side effects and, for opioids, tolerance and dependence; they do not address psychological aspects of chronic pain.', '1 mark each [2]'),
    ],
    'claims': [
        ('Psychological techniques can only help with imaginary pain.', False, 'They reduce real pain by changing attention and appraisal, as gate control theory explains.'),
        ('Psychological pain management is often combined with medication.', True, 'Combining approaches is common for chronic pain.'),
    ],
    'who': 'psychological techniques for managing pain (attention diversion, imagery and cognitive redefinition)',
    'evals': [
        ('ethics', 'strength', 'They are non-invasive with no physical side effects or risk of addiction.'),
        ('effectiveness', 'weakness', 'They work best for mild or moderate pain and may not help with severe acute pain.'),
        ('individual differences', 'weakness', 'People differ in their ability to use imagery or to concentrate, so results vary.'),
        ('long-term use', 'strength', 'Patients learn skills they can use repeatedly without cost, which helps with chronic pain.'),
    ],
    'apply': [
        ('{person}, from {city}, has had chronic back pain for two years. Painkillers help a little but {person} worries about becoming dependent on them.',
         [('Suggest one psychological technique {person} could use and explain how it works.', 'Non-pain imagery or attention diversion, which shifts attention away from the pain and, according to gate control theory, closes the gate via descending signals.', '1 mark technique; 1 mark mechanism [2]'),
          ('Explain why {person} might benefit from TENS.', 'Electrical stimulation of large fibres closes the gate, reducing pain without drugs.', '1 mark mechanism; 1 mark benefit [2]'),
          ('Explain one reason why a combination of treatments may be best for {person}.', 'Chronic pain has physical and psychological components, so medication can reduce intensity while psychological techniques reduce distress and reliance on drugs.', '1 mark components; 1 mark explained [2]')]),
    ],
})
chapter(13, [c13a, c13b, c13c], PAIN_SHARED)


# ============================================================== HEALTH 14: Stress

STRESS_SHARED = {
    'essays': [
        ('self-report scales are the best way to measure stress',
         ['The SRRS and hassles scales are quick, cheap and can be given to large samples.', 'They measure the person’s own perception of stress.'],
         ['Self-reports may be affected by memory and social desirability.', 'Physiological measures (cortisol, heart rate, GSR) are objective.', 'The SRRS gives fixed values that ignore individual meaning (for example a wanted divorce).'],
         ['validity', 'reliability', 'individual differences']),
        ('psychological methods are more effective than medical methods for managing stress',
         ['SIT and biofeedback teach skills that last and have no side effects (Budzynski et al., 1973).'],
         ['Drugs such as benzodiazepines and beta-blockers work quickly and need little effort.', 'Psychological methods take time and motivation.'],
         ['effectiveness', 'side effects', 'practicality']),
    ],
    'exp': [dict(intro=['A company in {city} compared heart rate (beats per minute) during a stressful presentation for {n} employees who had completed stress inoculation training and {n} who had not.',
                        '{person} measured heart rate (bpm) during a public-speaking task for employees with or without stress inoculation training.'],
                 A='SIT', B='no training', gA='employees who have completed stress inoculation training', gB='employees with no training',
                 more='will have lower heart rates during the presentation than', measure='heart rate', dvshort='Heart rate during presentation (bpm)', higher='B',
                 iv='whether employees had completed stress inoculation training', dv='heart rate in beats per minute measured during the presentation',
                 range=(60, 130), base=(84, 90), diff=(6, 12), sd=6,
                 controls=['the same presentation task and audience for everyone', 'measuring resting heart rate first so groups can be compared'],
                 ethics=['public speaking can be stressful, so employees can withdraw at any time', 'heart-rate data must be confidential and not shared with managers'],
                 concl_A='SIT increases physiological stress.', concl_B='stress inoculation training reduces the physiological stress response.')],
    'corr': [dict(intro=['{person} asked {n} students in {city} to complete a life events scale (LCU score) and recorded the number of days they were ill in the following six months.',
                         'A study in {city} measured life change units (LCU) and days of illness over the next six months for {n} adults.'],
                  x='life change units in the past year', y='days of illness in the next six months', xs='LCU score', ys='days of illness', xr=(50, 450), yr=(0, 20), sign=1,
                  third=['personality (for example Type A behaviour)', 'poor diet or lack of sleep', 'low social support'])],
    'plan': [('whether biofeedback reduces tension headaches in office workers', 'IV: biofeedback or no treatment', 'DV: number of headaches per week', ['field experiment']),
             ('whether daily hassles are related to students’ blood pressure', 'co-variable 1: hassles score', 'co-variable 2: blood pressure', ['correlation'])],
    'plan_lead': 'Design',
}

c14a = T('Causes and sources of stress: physiology (GAS), work and life events', 'causes sources stress physiology gas work life events')
build(c14a, {
    'terms': [
        ('general adaptation syndrome (GAS)', 'Selye’s three-stage model of the body’s response to prolonged stress: alarm, resistance and exhaustion'),
        ('stressor', 'an event or situation that causes stress'),
        ('life events', 'major changes in a person’s life, such as bereavement or divorce, that require adjustment'),
        ('daily hassles', 'minor, everyday irritations, such as losing keys or traffic, that can add up to cause stress'),
        ('HPA axis', 'the hypothalamic–pituitary–adrenal system that releases cortisol in response to long-term stress'),
        ('SAM pathway', 'the sympathetic–adrenal medullary system that releases adrenaline in the immediate fight-or-flight response'),
    ],
    'mcq': [
        ('What are the three stages of Selye’s general adaptation syndrome, in order?', 'Alarm, resistance, exhaustion', ['Resistance, alarm, exhaustion', 'Alarm, exhaustion, recovery', 'Appraisal, illness, utilisation'], 'Selye (1936).'),
        ('In the Social Readjustment Rating Scale, which life event has the highest value?', 'Death of a spouse (100)', ['Divorce (73)', 'Marriage (50)', 'Vacation (13)'], 'Holmes and Rahe (1967).'),
        ('Johansson et al. (1978) found that “finishers” in a Swedish sawmill', 'had higher adrenaline levels and more stress-related illness than cleaners', ['had lower stress than other workers', 'enjoyed their repetitive work', 'had no absences'], 'Machine-paced, repetitive, responsible work was stressful.'),
        ('Which hormone is released by the adrenal cortex during long-term stress?', 'Cortisol', ['Adrenaline', 'Oxytocin', 'Melatonin'], 'HPA axis → cortisol.'),
    ],
    'ar': [
        ('Prolonged stress can make people more likely to become ill.', 'In the exhaustion stage of the GAS, the body’s resources are depleted and immune function is weakened.', 'AR', 'This is Selye’s explanation.'),
    ],
    'explain': [
        ('Describe the general adaptation syndrome.', 'Alarm: the stressor is detected and the sympathetic system and adrenaline produce fight or flight. Resistance: the body adapts and maintains high arousal with cortisol. Exhaustion: with continued stress, resources are depleted and stress-related illness may develop.', '1 mark each stage [3]'),
        ('Explain how work can be a source of stress.', 'Factors such as high workload, lack of control, repetitive machine-paced tasks, long hours and conflict can cause stress; Johansson et al. found repetitive, responsible sawmill work raised adrenaline and illness; Chandola et al. linked work stress to heart disease.', '1 mark factor; 1 mark evidence [2]'),
    ],
    'claims': [
        ('Only negative events count as life events on the SRRS.', False, 'Positive events such as marriage and holidays also require readjustment and are included.'),
        ('Daily hassles may be a better predictor of stress than major life events.', True, 'Research such as Kanner et al. found hassles related strongly to psychological symptoms.'),
    ],
    'who': 'Holmes and Rahe’s Social Readjustment Rating Scale (SRRS)',
    'evals': [
        ('quantitative data', 'strength', 'It gives a single LCU score that can be compared and correlated with illness.'),
        ('individual differences', 'weakness', 'Fixed values ignore the meaning of events for each person (for example a wanted divorce may be a relief).'),
        ('cause and effect', 'weakness', 'Links between LCU and illness are correlational, so illness could cause life changes.'),
        ('validity', 'weakness', 'Some events are ambiguous (for example “change in health”) and it ignores daily hassles and chronic stressors.'),
        ('practicality', 'strength', 'It is quick and easy to complete and score.'),
    ],
})

SRRS = [('death of a spouse', 100), ('divorce', 73), ('marital separation', 65), ('death of a close family member', 63), ('personal injury or illness', 53), ('marriage', 50),
        ('being fired at work', 47), ('retirement', 45), ('pregnancy', 40), ('change in financial state', 38), ('death of a close friend', 37), ('change to a different line of work', 36),
        ('son or daughter leaving home', 29), ('outstanding personal achievement', 28), ('beginning or ending school', 26), ('change in living conditions', 25), ('trouble with boss', 23),
        ('change in residence', 20), ('change in schools', 20), ('change in sleeping habits', 16), ('change in eating habits', 15), ('vacation', 13), ('minor violations of the law', 11)]


def _srrs(r, D):
    d = ctx(r)
    ev = r.sample(SRRS, r.choice([4, 5, 6]))
    tot = sum(v for _, v in ev)
    risk = 'high' if tot >= 300 else 'moderate' if tot >= 150 else 'low'
    intro = (f'In the last year, {d["person"]}, from {d["city"]}, experienced: ' + '; '.join(f'{e} ({v} LCU)' for e, v in ev) + '.')
    parts = [
        ('Calculate {p}’s total life change units (LCU).'.format(p=d['person']), str(tot), f'{" + ".join(str(v) for _, v in ev)} = {tot}. 1 mark working; 1 mark answer [2]'),
        ('Holmes and Rahe suggested that 300 or more LCU is high risk and 150–299 moderate risk of stress-related illness. State the level of risk.', f'{cap(risk)} risk ({tot} LCU)', f'{tot} LCU → {risk} risk [1]'),
        ('Explain why the total may not reflect how stressed this person actually feels.', 'The values are fixed averages; the meaning of each event differs between people (for example a holiday may be relaxing), and daily hassles and coping resources are ignored.', '1 mark fixed values/individual meaning; 1 mark other factors [2]'),
        ('Suggest a physiological measure that could be used alongside the SRRS and explain why.', 'Salivary cortisol or blood pressure, which give objective evidence of the stress response that is not affected by self-report bias.', '1 mark measure; 1 mark reason [2]'),
    ]
    m = ('What is the total LCU score?', str(tot), [str(tot + 10), str(tot - 10), str(tot + 20), str(round(tot / len(ev))), str(tot - 13)], f'Total = {tot} [1]')
    return intro, parts, m


score_tpl(c14a, 'srrs', _srrs)

c14b = T('Measuring stress: physiological measures and self-report scales', 'measuring stress physiological measures self-report scales')
build(c14b, {
    'terms': [
        ('galvanic skin response (GSR)', 'a measure of the electrical conductance of the skin, which rises with sweating during arousal'),
        ('salivary cortisol', 'the level of the stress hormone cortisol measured in a saliva sample'),
        ('Social Readjustment Rating Scale (SRRS)', 'Holmes and Rahe’s list of 43 life events, each with a value in life change units'),
        ('hassles scale', 'a self-report measure of the frequency and severity of minor everyday stressors'),
    ],
    'foils': ['general adaptation syndrome', 'biofeedback'],
    'mcq': [
        ('Geer and Maisel (1972) found that participants who could stop the photographs of car-crash victims showed', 'less physiological stress (lower GSR)', ['more physiological stress', 'no difference from other groups', 'higher heart rates throughout'], 'Perceived control reduced stress.'),
        ('Which is a physiological measure of stress?', 'Heart rate', ['The SRRS', 'A hassles questionnaire', 'An interview about worries'], 'It measures bodily arousal.'),
        ('How many life events are on the SRRS?', '43', ['10', '21', '100'], 'Holmes and Rahe (1967).'),
    ],
    'explain': [
        ('Explain one strength and one weakness of physiological measures of stress.', 'Strength: they are objective and not affected by social desirability. Weakness: arousal can be caused by things other than stress (exercise, excitement, caffeine), and equipment may itself be stressful.', '1 mark each [2]'),
        ('Describe the procedure of Geer and Maisel (1972).', 'Participants viewed photographs of dead car-crash victims while GSR and heart rate were recorded; one group could press a button to end each photo, one group was warned when photos would appear and how long they would last, and one group had no control or warning.', '1 mark stimulus/measures; 1 mark groups [2]'),
    ],
    'claims': [
        ('Physiological measures of stress cannot be affected by the testing situation.', False, 'Being attached to equipment in a laboratory can itself raise arousal.'),
        ('Using both self-report and physiological measures gives a fuller picture of stress.', True, 'Each measure has different strengths and weaknesses.'),
    ],
    'who': 'physiological measures of stress (such as GSR, heart rate and cortisol)',
    'evals': [
        ('objectivity', 'strength', 'They provide numerical data that are not affected by participants’ honesty or memory.'),
        ('validity', 'weakness', 'Arousal can be caused by excitement or exercise, so high readings do not always mean stress.'),
        ('reliability', 'strength', 'Standardised equipment gives consistent readings that can be repeated.'),
        ('ethics', 'weakness', 'Some measures (such as blood samples) are invasive and may cause discomfort or anxiety.'),
    ],
    'apply': [
        ('A school in {city} wants to measure stress in students during exam season.',
         [('Suggest one physiological and one self-report measure the school could use.', 'Physiological: heart rate or salivary cortisol. Self-report: a hassles scale or perceived stress questionnaire.', '1 mark each [2]'),
          ('Explain one problem with the physiological measure for this purpose.', 'It is costly and needs equipment or samples; readings may be affected by exercise or caffeine, not just stress.', '1 mark problem; 1 mark explained [2]'),
          ('Explain one ethical issue in measuring students’ stress.', 'Students must consent (with parents for younger students), results must be confidential, and highly stressed students should be offered support.', '1 mark issue; 1 mark explained [2]')]),
    ],
})

c14c = T('Managing stress: medical, psychological (SIT, biofeedback) and preventing stress', 'managing stress medical psychological sit biofeedback preventing stress')
build(c14c, {
    'terms': [
        ('stress inoculation training (SIT)', 'Meichenbaum’s cognitive-behavioural therapy with three phases: conceptualisation, skill acquisition and rehearsal, and application and follow-through'),
        ('biofeedback', 'a technique that gives a person information about a physiological process (such as muscle tension) so they can learn to control it'),
        ('benzodiazepine', 'an anti-anxiety drug that increases the effect of GABA, reducing arousal'),
        ('beta-blocker', 'a drug that blocks adrenaline’s effects on the heart, reducing heart rate and blood pressure'),
        ('social support', 'help and comfort provided by other people, which can buffer the effects of stress'),
    ],
    'mcq': [
        ('What is the first phase of stress inoculation training?', 'Conceptualisation', ['Application and follow-through', 'Skill acquisition', 'Exhaustion'], 'The client learns about stress and their own stressors.'),
        ('Budzynski et al. (1973) used EMG biofeedback to treat', 'tension headaches', ['phobias', 'schizophrenia', 'gambling disorder'], 'Feedback on forehead muscle tension reduced headaches.'),
        ('Beta-blockers reduce stress symptoms by', 'blocking the effects of adrenaline on the heart', ['increasing GABA', 'raising serotonin', 'blocking dopamine'], 'Reduce physical symptoms such as racing heart.'),
    ],
    'explain': [
        ('Describe the three phases of stress inoculation training.', 'Conceptualisation: the client learns about stress and identifies stressors and thoughts. Skill acquisition and rehearsal: coping skills such as relaxation, positive self-statements and problem-solving are taught and practised. Application and follow-through: skills are used in increasingly stressful real situations with follow-up sessions.', '1 mark each phase [3]'),
        ('Explain how biofeedback can be used to manage stress.', 'Sensors measure a physiological response (for example muscle tension or heart rate) and display it as a sound or graph; the person practises relaxation and learns which strategies reduce the response, until they can control it without the equipment.', '1 mark feedback; 1 mark learning control [2]'),
    ],
    'claims': [
        ('Benzodiazepines are suitable for long-term daily use for stress.', False, 'They can cause dependence and tolerance, so they are usually prescribed only for short periods.'),
        ('SIT aims to prepare people to cope with future stressors as well as current ones.', True, 'Like a vaccination, it builds resistance.'),
    ],
    'who': 'stress inoculation training (SIT)',
    'evals': [
        ('long-term effectiveness', 'strength', 'It teaches coping skills that can be used with future stressors, so benefits last.'),
        ('practicality', 'weakness', 'It requires time, motivation and a trained therapist, so it is costly.'),
        ('side effects', 'strength', 'Unlike drugs, it has no physical side effects or risk of dependence.'),
        ('generalisability', 'weakness', 'It may suit people who are motivated and able to learn cognitive skills, but not everyone.'),
    ],
    'apply': [
        ('{person}, a teacher in {city}, suffers from tension headaches and a racing heart before school inspections.',
         [('Suggest how biofeedback could help {person}.', 'Use EMG sensors on the forehead to show muscle tension; {person} practises relaxation until tension drops, learning to relax without the equipment.', '1 mark sensors/feedback; 1 mark learned control [2]'),
          ('Suggest a medical treatment for the racing heart and explain how it works.', 'A beta-blocker, which blocks adrenaline’s effect on the heart and lowers heart rate.', '1 mark drug; 1 mark mechanism [2]'),
          ('Explain why SIT might be better for {person} in the long term.', 'It teaches coping skills for future inspections and other stressors without side effects or dependence.', '1 mark skills; 1 mark no side effects [2]')]),
    ],
})
chapter(14, [c14a, c14b, c14c], STRESS_SHARED)


# ============================================================== HEALTH 15: Health promotion

HP_SHARED = {
    'essays': [
        ('fear arousal is an effective way of promoting health',
         ['Fear can attract attention and increase perceived severity.', 'Some campaigns using fear appeals have changed behaviour (for example warnings about fire safety).'],
         ['Janis and Feshbach (1953) found minimal fear produced the most change (36% versus 8% for strong fear).', 'High fear can cause denial or avoidance.', 'Fear works best when combined with clear advice and self-efficacy.'],
         ['Yale model', 'usefulness', 'individual differences']),
        ('health promotion is most effective when it targets whole communities',
         ['Farquhar et al. (1977) reduced cardiovascular risk factors through community media campaigns.', 'Community approaches reach many people at once.'],
         ['School programmes (Tapper et al., Food Dudes) and worksite schemes (Fox et al., 1987) can be more targeted.', 'Individual factors such as unrealistic optimism and self-efficacy limit change.'],
         ['effectiveness', 'generalisability', 'individual differences']),
    ],
    'exp': [dict(intro=['A health campaign in {city} showed {n} students a low-fear leaflet about tooth care and {n} students a high-fear leaflet with images of diseased gums. The number of recommended tooth-care behaviours (out of 10) performed a week later was recorded.',
                        '{person} compared tooth-care behaviours (out of 10) one week after a low-fear or a high-fear health message.'],
                 A='low fear', B='high fear', gA='students given a low-fear message', gB='students given a high-fear message',
                 more='will perform more recommended behaviours than', measure='the number of recommended behaviours performed', dvshort='Recommended behaviours performed (out of 10)',
                 iv='the level of fear in the health message (low or high)', dv='the number of the 10 recommended tooth-care behaviours performed one week later (self-report checklist)',
                 range=(0, 10), base=(4.5, 5.5), diff=(1.2, 2.5), sd=1.5,
                 controls=['the same information about tooth care in both leaflets, differing only in fear content', 'the same checklist and timing for all students'],
                 ethics=['frightening images could upset students, so they should be warned and debriefed', 'all students should receive the useful advice afterwards'],
                 concl_A='low-fear messages are more effective than high-fear messages.', concl_B='high-fear messages are more effective than low-fear messages.')],
    'plan': [('whether a classroom programme using peer models increases children’s fruit and vegetable consumption', 'IV: programme or no programme', 'DV: portions of fruit and vegetables eaten at lunch', ['field experiment', 'observation']),
             ('whether self-efficacy is related to the amount of exercise people take', 'co-variable 1: self-efficacy score', 'co-variable 2: hours of exercise per week', ['correlation', 'questionnaire'])],
    'plan_lead': 'Design',
}

c15a = T('Strategies for promoting health: fear arousal and Yale model', 'strategies promoting health fear arousal yale model')
build(c15a, {
    'terms': [
        ('fear arousal', 'using frightening information or images in a health message to motivate behaviour change'),
        ('Yale model of communication', 'Hovland’s model stating that persuasion depends on the source, the message and the audience'),
        ('source credibility', 'how expert and trustworthy the person or organisation delivering a message is perceived to be'),
        ('one-sided message', 'a message that presents only arguments in favour of a position'),
        ('two-sided message', 'a message that presents arguments for and against, then argues against the opposing view'),
    ],
    'mcq': [
        ('In Janis and Feshbach’s (1953) study, which fear condition produced the greatest improvement in dental hygiene?', 'Minimal fear', ['Strong fear', 'Moderate fear', 'No message'], 'Net change 36% (minimal), 22% (moderate), 8% (strong).'),
        ('According to the Yale model, which of these is a feature of the source?', 'Credibility and attractiveness', ['Intelligence of the audience', 'Number of arguments', 'Order of arguments'], 'Who says it.'),
        ('Two-sided messages tend to be more effective with', 'more intelligent or better-informed audiences', ['young children', 'audiences who already agree', 'audiences who are not paying attention'], 'Audiences who know counter-arguments.'),
    ],
    'ar': [
        ('Very frightening health messages can be less effective than mildly frightening ones.', 'High fear can lead people to deny or avoid the message.', 'AR', 'Defensive avoidance explains the finding.'),
    ],
    'explain': [
        ('Describe Janis and Feshbach’s (1953) study.', 'High-school students heard a lecture on dental hygiene with strong, moderate or minimal fear content (or no lecture). A week later, the minimal-fear group showed the greatest improvement in reported dental behaviour (36% net change) and the strong-fear group the least (8%).', '1 mark procedure; 1 mark findings with data [2]'),
        ('Explain the Yale model of persuasive communication.', 'Persuasion depends on the source (credibility, attractiveness), the message (one- or two-sided, emotional or rational, fear level) and the audience (age, intelligence, initial attitude, self-esteem).', '1 mark source; 1 mark message; 1 mark audience [3]'),
    ],
    'claims': [
        ('The more frightening a health message is, the more people will change their behaviour.', False, 'Research (Janis and Feshbach) suggests moderate or low fear can be more effective; high fear can cause avoidance.'),
        ('An expert source is usually more persuasive than a non-expert.', True, 'Credibility increases persuasion according to the Yale model.'),
    ],
    'who': 'Janis and Feshbach’s (1953) study of fear arousal',
    'evals': [
        ('controls', 'strength', 'Students were randomly allocated to lectures that differed only in fear level, with a control group.'),
        ('self-report', 'weakness', 'Dental behaviour was self-reported, so students may have exaggerated improvements.'),
        ('generalisability', 'weakness', 'The sample was from one American high school in the 1950s, so attitudes may differ today and elsewhere.'),
        ('usefulness', 'strength', 'It warns health campaigners that strong fear may backfire.'),
    ],
})
add_tally_pct(c15a, ['After a dental health talk in {city}, students reported whether they had improved their tooth-brushing a week later.', '{person} recorded how many students in each fear condition improved their dental behaviour.'],
              [('Minimal fear', (20, 30), (20, 30)), ('Moderate fear', (14, 22), (26, 34)), ('Strong fear', (6, 12), (36, 44)), ('No talk', (3, 8), (40, 48))],
              ('improved', 'did not improve', 'students'))

c15b = T('Health promotion in schools, worksites and communities', 'health promotion schools worksites communities')
build(c15b, {
    'terms': [
        ('Food Dudes programme', 'a school programme using video peer models and rewards to increase children’s fruit and vegetable consumption'),
        ('worksite health promotion', 'programmes in workplaces to improve employees’ health or safety'),
        ('community health campaign', 'a programme aimed at a whole town or region, often using media and local events'),
        ('token economy', 'a programme in which people earn tokens for target behaviours that can be exchanged for rewards'),
    ],
    'foils': ['fear arousal', 'unrealistic optimism'],
    'mcq': [
        ('Fox et al. (1987) used a token economy to improve safety in', 'open-pit mines', ['primary schools', 'hospitals', 'supermarkets'], 'Workers earned stamps for accident-free periods.'),
        ('Farquhar et al.’s (1977) Stanford study compared', 'three communities receiving different health campaigns', ['two schools with different diets', 'one factory before and after a strike', 'patients in a hospital'], 'Media, media plus face-to-face, and control towns.'),
        ('The Food Dudes programme uses', 'modelling by peer heroes and rewards', ['fear of illness', 'punishment', 'medication'], 'Social learning and reinforcement.'),
    ],
    'explain': [
        ('Describe the findings of Fox et al. (1987).', 'After a token economy was introduced at two open-pit mines, workers earned stamps for working without accidents or injuries; the number of days lost through injury and the costs of accidents fell sharply and remained low for years.', '1 mark procedure; 1 mark findings [2]'),
        ('Describe Farquhar et al.’s (1977) three-community study.', 'One town received a two-year mass media campaign on heart disease risk; a second received the media campaign plus face-to-face instruction for high-risk people; a third was a control. Risk factors fell in both campaign towns, especially with face-to-face instruction.', '1 mark design; 1 mark findings [2]'),
    ],
    'claims': [
        ('Health promotion in schools can only provide information.', False, 'Programmes such as Food Dudes use modelling and rewards to change behaviour.'),
        ('Worksite programmes can reach adults who rarely see a doctor.', True, 'Workplaces give regular access to large groups of adults.'),
    ],
    'who': 'Fox et al.’s (1987) token economy for mine safety',
    'evals': [
        ('ecological validity', 'strength', 'It took place in real workplaces over several years with real accidents measured.'),
        ('usefulness', 'strength', 'It reduced injuries and saved money, so other industries could adopt similar schemes.'),
        ('reporting', 'weakness', 'Workers might have hidden minor accidents to keep their tokens, so accidents may have been under-reported.'),
        ('controls', 'weakness', 'There was no control mine, so other changes over time might explain the improvement.'),
    ],
    'apply': [
        ('A primary school in {city} wants children to eat more vegetables at lunch.',
         [('Suggest how a Food Dudes-style programme could be used.', 'Show videos of heroic peer characters who eat vegetables and reward children with small prizes for tasting and eating them.', '1 mark modelling; 1 mark rewards [2]'),
          ('Explain why this programme might work, using learning theory.', 'Children imitate admired models (social learning) and rewards reinforce eating vegetables (operant conditioning).', '1 mark each [2]'),
          ('Explain one problem with the programme.', 'Eating may decrease when rewards stop, and changes at school may not transfer to home.', '1 mark problem; 1 mark explained [2]')]),
    ],
})

c15c = T('Individual factors in changing health beliefs: unrealistic optimism, self-efficacy', 'individual factors changing health beliefs unrealistic optimism self-efficacy')
build(c15c, {
    'terms': [
        ('unrealistic optimism', 'the belief that one is less likely than other people to experience negative events'),
        ('self-efficacy', 'a person’s belief in their ability to carry out a behaviour successfully'),
        ('health locus of control', 'the extent to which a person believes their health is controlled by themselves, by others or by chance'),
        ('optimistic bias', 'another name for unrealistic optimism about one’s own risks'),
    ],
    'foils': ['fear arousal', 'source credibility'],
    'mcq': [
        ('Weinstein (1980) asked students to rate their chances of experiencing events compared with classmates. He found that', 'students believed they were less likely than others to experience negative events', ['students were accurate about their risks', 'students believed they were more likely to experience negative events', 'students refused to answer'], 'Unrealistic optimism.'),
        ('Who developed the concept of self-efficacy?', 'Bandura', ['Weinstein', 'Selye', 'Melzack'], 'Bandura (1977).'),
        ('A person who believes “my health depends on luck” has', 'an external (chance) health locus of control', ['an internal locus of control', 'high self-efficacy', 'unrealistic optimism'], 'Chance = external.'),
    ],
    'explain': [
        ('Explain how unrealistic optimism can prevent people from changing unhealthy behaviour.', 'If people believe they are less at risk than others (“it won’t happen to me”), they see health messages as relevant to other people and see no need to change.', '1 mark belief; 1 mark consequence [2]'),
        ('Explain why self-efficacy is important in health behaviour change.', 'People who believe they can succeed (for example in quitting smoking) are more likely to try, persist and recover from setbacks, so health promotion should build confidence as well as giving information.', '1 mark belief in ability; 1 mark effect on persistence [2]'),
    ],
    'claims': [
        ('Unrealistic optimism means people are optimistic about everything in life.', False, 'It refers specifically to underestimating one’s own risk compared with others.'),
        ('Health campaigns can increase self-efficacy by showing similar people succeeding.', True, 'Vicarious experience is a source of self-efficacy.'),
    ],
    'who': 'Weinstein’s (1980) study of unrealistic optimism',
    'evals': [
        ('sample', 'strength', 'A sizeable group of students rated many different events, so the pattern was consistent.'),
        ('generalisability', 'weakness', 'Participants were American college students, who may be more optimistic than other groups.'),
        ('self-report', 'weakness', 'Ratings were hypothetical and may not predict real health behaviour.'),
        ('usefulness', 'strength', 'It explains why general health warnings fail and suggests personalised risk information.'),
    ],
    'apply': [
        ('{person}, aged 19, from {city}, smokes and says: “Smoking is bad for some people, but I’m young and healthy so it won’t affect me. Anyway, I could never quit.”',
         [('Identify two individual factors that may prevent {person} from changing behaviour.', 'Unrealistic optimism (“it won’t affect me”) and low self-efficacy (“I could never quit”).', '1 mark each [2]'),
          ('Suggest how a health promoter could address {person}’s unrealistic optimism.', 'Give personalised risk information (for example lung function testing) and examples of young people harmed by smoking.', '1 mark strategy; 1 mark explained [2]'),
          ('Suggest how {person}’s self-efficacy could be increased.', 'Set small achievable goals, provide support and show similar people who have quit successfully.', '1 mark strategy; 1 mark explained [2]')]),
    ],
})
chapter(15, [c15a, c15b, c15c], HP_SHARED)


# ============================================================== ORGANISATIONAL 16: Motivation to work

MOT_SHARED = {
    'essays': [
        ('need theories provide the best explanation of motivation at work',
         ['Maslow, Alderfer and McClelland explain why people want different things from work (security, relationships, growth, achievement).', 'They are easy for managers to apply, for example by offering security before esteem rewards.'],
         ['There is little evidence for a fixed hierarchy of needs; people pursue several needs at once (Alderfer’s ERG theory).', 'Cognitive theories (goal-setting, VIE) explain how people choose how much effort to put in, which need theories ignore.', 'Needs are hard to measure objectively and vary between cultures.'],
         ['individual differences', 'cultural differences', 'usefulness']),
        ('money is the most important motivator at work',
         ['Pay meets physiological and security needs and can be linked to performance through bonuses and performance-related pay.', 'In VIE theory, pay often has high valence for employees.'],
         ['Herzberg classed pay as a hygiene factor that prevents dissatisfaction but does not motivate.', 'Deci (1971) found that paying people for an interesting task reduced their intrinsic motivation.', 'Recognition, responsibility and interesting work also motivate.'],
         ['intrinsic versus extrinsic motivation', 'individual differences', 'validity of evidence']),
    ],
    'exp': [dict(intro=['A call centre in {city} compared the number of calls completed in a shift by {n} employees who were set a specific, difficult target and {n} employees who were told to “do your best”.',
                        '{person} tested goal-setting theory with {n} employees per condition at an office in {city}, recording the number of forms processed in a two-hour session.'],
                 A='specific goal', B='do-your-best', gA='employees given a specific, difficult goal', gB='employees told to do their best',
                 more='will complete more tasks than', measure='the number of tasks completed', dvshort='Tasks completed per session',
                 iv='the type of goal set (specific and difficult, or “do your best”)', dv='the number of tasks completed in the session, counted from the computer system',
                 range=(20, 80), base=(40, 46), diff=(5, 11), sd=5, nosample=True,
                 controls=['the same type of task and length of session for all employees', 'equal experience in the job in both groups'],
                 ethics=['employees should not feel pressured or penalised for failing to meet a goal', 'performance data should be confidential and not used for appraisal without consent'],
                 concl_A='setting specific, difficult goals increases performance.', concl_B='telling employees to do their best leads to higher performance than specific goals.')],
    'plan': [('whether being paid for an interesting task reduces intrinsic motivation', 'IV: paid or not paid', 'DV: time spent on the task in a free-choice period', ['laboratory experiment']),
             ('whether need for achievement is related to sales performance', 'co-variable 1: need for achievement score', 'co-variable 2: monthly sales', ['correlation', 'questionnaire'])],
    'plan_lead': 'Design',
}

c16a = T('Need theories: Maslow, Alderfer ERG and McClelland', 'need theories maslow alderfer erg mcclelland')
build(c16a, {
    'terms': [
        ('hierarchy of needs', 'Maslow’s theory that needs are arranged in levels, from physiological and safety needs up to esteem and self-actualisation'),
        ('self-actualisation', 'the need to fulfil one’s potential, at the top of Maslow’s hierarchy'),
        ('ERG theory', 'Alderfer’s theory that people have existence, relatedness and growth needs, which can operate at the same time'),
        ('frustration–regression', 'Alderfer’s idea that if a higher need is blocked, a person will put more effort into a lower need'),
        ('need for achievement (nAch)', 'in McClelland’s theory, the desire to succeed at challenging tasks and to meet high standards'),
        ('need for affiliation (nAff)', 'in McClelland’s theory, the desire for friendly, close relationships with others'),
        ('need for power (nPow)', 'in McClelland’s theory, the desire to influence, control or be responsible for others'),
    ],
    'mcq': [
        ('Which of Alderfer’s needs corresponds most closely to Maslow’s esteem and self-actualisation needs?', 'Growth', ['Existence', 'Relatedness', 'Affiliation'], 'Growth = personal development.'),
        ('McClelland measured needs using', 'the Thematic Apperception Test (TAT)', ['the Job Descriptive Index', 'the LPC scale', 'the Beck Depression Inventory'], 'Stories written about ambiguous pictures were scored.'),
        ('According to Maslow, which need must be met first?', 'Physiological needs', ['Esteem needs', 'Belonging needs', 'Self-actualisation'], 'Food, water, warmth.'),
        ('A manager offers a worker job security and a safe workplace. Which level of Maslow’s hierarchy is being met?', 'Safety', ['Physiological', 'Esteem', 'Self-actualisation'], 'Security = safety needs.'),
    ],
    'ar': [
        ('Alderfer’s ERG theory is more flexible than Maslow’s hierarchy.', 'ERG theory allows several needs to motivate a person at the same time.', 'AR', 'No strict order of satisfaction.'),
        ('McClelland believed that needs are mainly inherited.', 'McClelland’s needs are acquired through experience and culture.', 'R', 'Needs are learned (acquired needs theory), so the assertion is false.'),
    ],
    'explain': [
        ('Explain two differences between Maslow’s hierarchy of needs and Alderfer’s ERG theory.', 'Maslow has five levels, ERG has three (existence, relatedness, growth); Maslow says lower needs must be satisfied before higher ones, while ERG allows several needs at once and includes frustration–regression.', '1 mark each difference, 2 marks maximum each [4]'),
        ('Describe McClelland’s theory of needs.', 'People have three learned needs – achievement, affiliation and power – in different strengths. The dominant need shapes behaviour at work: high nAch people like moderately difficult tasks with feedback; high nPow people seek influence; high nAff people seek good relationships.', '1 mark three needs; 1 mark acquired; 1 mark effect on work [3]'),
    ],
    'claims': [
        ('Maslow’s theory states that a person cannot be motivated by esteem until safety needs are reasonably satisfied.', True, 'Lower needs must be largely met first.'),
        ('McClelland suggested that people with high need for achievement prefer extremely difficult tasks.', False, 'They prefer moderately difficult tasks with a realistic chance of success and clear feedback.'),
    ],
    'who': 'Maslow’s hierarchy of needs as an explanation of motivation at work',
    'evals': [
        ('usefulness', 'strength', 'It reminds managers that pay and security must be provided before esteem and growth rewards will motivate.'),
        ('face validity', 'strength', 'The idea that basic needs come first matches everyday experience and is easy to understand.'),
        ('empirical support', 'weakness', 'Research has found little evidence for five distinct levels or a strict order of satisfaction.'),
        ('cultural bias', 'weakness', 'It reflects individualist Western values; in collectivist cultures belonging may be more important than self-actualisation.'),
    ],
    'apply': [
        ('{person} works in a factory in {city}. The pay is fair and the job is secure, but {person} says: “I never learn anything new, and nobody ever notices when I do a good job.”',
         [('Identify which of Maslow’s needs are not being met.', 'Esteem (recognition) and self-actualisation (growth).', '1 mark each [2]'),
          ('Using ERG theory, explain what might happen if {person}’s growth needs remain blocked.', 'Frustration–regression: {person} may focus more on relatedness or existence needs, for example socialising or asking for more pay.', '1 mark frustration–regression; 1 mark example [2]'),
          ('Suggest two changes the manager could make to motivate {person}.', 'Give recognition (praise, employee of the month) and provide training or more responsible tasks.', '1 mark each [2]')]),
        ('A sales company in {city} gives a personality test to new staff. {person} scores high on need for power; {person2} scores high on need for affiliation.',
         [('Suggest which employee would be more suited to a team-leader role and explain why.', '{person}, because people with high nPow want to influence and direct others.', '1 mark choice; 1 mark reason [2]'),
          ('Suggest the type of work environment that would motivate {person2}.', 'A cooperative team with friendly colleagues and few conflicts.', '1 mark [1]'),
          ('Explain one problem with measuring needs using the TAT.', 'Scoring stories is subjective, so different scorers may disagree, which lowers reliability.', '1 mark subjectivity; 1 mark reliability [2]')]),
    ],
})

c16b = T('Cognitive theories: goal-setting and expectancy (VIE) theory', 'cognitive theories goal-setting expectancy vie theory')
build(c16b, {
    'terms': [
        ('goal-setting theory', 'Locke’s theory that specific, difficult goals that are accepted, with feedback, lead to higher performance than vague goals'),
        ('expectancy (VIE) theory', 'Vroom’s theory that motivation depends on expectancy, instrumentality and valence'),
        ('expectancy', 'in VIE theory, the belief that effort will lead to successful performance'),
        ('instrumentality', 'in VIE theory, the belief that successful performance will lead to a particular outcome or reward'),
        ('valence', 'in VIE theory, the value a person places on an outcome'),
        ('goal commitment', 'the degree to which a person accepts a goal and is determined to reach it'),
    ],
    'foils': ['hygiene factor', 'self-actualisation'],
    'mcq': [
        ('According to goal-setting theory, which goal is likely to lead to the highest performance?', 'Process 50 orders per day this week', ['Do your best', 'Try to work harder', 'Process as many orders as you like'], 'Specific and challenging.'),
        ('In Vroom’s VIE theory, motivational force is calculated as', 'expectancy × instrumentality × valence', ['expectancy + instrumentality + valence', 'valence ÷ expectancy', '(expectancy + valence) × instrumentality'], 'Multiplicative model.'),
        ('A worker believes that a promotion would be worthless to her. Which VIE component is low?', 'Valence', ['Expectancy', 'Instrumentality', 'Feedback'], 'Value of the outcome.'),
        ('A worker believes that however hard he tries, he cannot reach the target. Which VIE component is low?', 'Expectancy', ['Valence', 'Instrumentality', 'Task identity'], 'Effort → performance.'),
    ],
    'ar': [
        ('In VIE theory, motivation is zero if any one component is zero.', 'The three components are multiplied together.', 'AR', 'Anything × 0 = 0.'),
    ],
    'explain': [
        ('Explain how goal-setting theory could be used to improve the performance of sales staff.', 'Set specific, difficult but achievable sales targets, involve staff in setting them to increase commitment, and give regular feedback on progress.', '1 mark specific/difficult; 1 mark commitment; 1 mark feedback [3]'),
        ('Explain why VIE theory is described as a cognitive theory.', 'It assumes employees think rationally about the likely results of their effort, estimating probabilities (expectancy, instrumentality) and the value of outcomes (valence) before deciding how hard to work.', '1 mark rational thinking; 1 mark reference to components [2]'),
    ],
    'claims': [
        ('Goal-setting theory suggests that easy goals produce the highest performance because they are more likely to be achieved.', False, 'Difficult (but accepted) goals produce higher performance than easy goals.'),
        ('VIE theory predicts that a valuable reward will not motivate if a worker does not believe performance will be rewarded.', True, 'Low instrumentality reduces motivational force.'),
    ],
    'who': 'Vroom’s expectancy (VIE) theory',
    'evals': [
        ('usefulness', 'strength', 'Managers can identify which component is low (for example unclear link between performance and reward) and fix it.'),
        ('individual differences', 'strength', 'It recognises that different employees value different rewards.'),
        ('rationality', 'weakness', 'It assumes people calculate probabilities and values rationally, but many decisions are emotional or habitual.'),
        ('measurement', 'weakness', 'Expectancy, instrumentality and valence are subjective and hard to measure accurately.'),
    ],
    'apply': [
        ('A supermarket in {city} sets checkout staff the goal of “being friendly to customers”. Performance has not improved.',
         [('Using goal-setting theory, explain why this goal may not be effective.', 'It is vague and not measurable, so staff do not know what to aim for or how they are doing.', '1 mark vague; 1 mark consequence [2]'),
          ('Rewrite the goal so that it follows goal-setting principles.', 'For example: greet every customer and achieve an average customer-feedback score of at least 4.5 out of 5 this month.', '1 mark specific; 1 mark measurable/challenging [2]'),
          ('Explain why feedback is important when goals are set.', 'Feedback lets staff see progress and adjust effort, and maintains commitment.', '1 mark [1]')]),
    ],
})


def v2(x):
    return fmt(round(x, 2), 2)


def _vie(r, D):
    d = ctx(r)
    outs = r.sample([('a cash bonus', 'bonus'), ('a promotion', 'promotion'), ('extra days of holiday', 'extra holiday'), ('a certificate of recognition', 'recognition'), ('a place on a training course', 'training')], 2)
    vals = []
    for name, short in outs:
        E = r.choice([0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9])
        I = r.choice([0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0])
        V = r.randint(2, 10)
        vals.append((name, short, E, I, V, round(E * I * V, 2)))
    if abs(vals[0][5] - vals[1][5]) < 0.15:
        return None
    best = max(vals, key=lambda v: v[5])
    worst = min(vals, key=lambda v: v[5])
    intro = (f'{d["person"]} works for a company in {d["city"]}. Two incentive schemes are offered. ' +
             ' '.join(f'For {n}: expectancy = {v2(E)}, instrumentality = {v2(I)}, valence = {V} (on a scale from −10 to +10).' for n, _, E, I, V, _m in vals))
    n0, s0, E0, I0, V0, M0 = vals[0]
    parts = [
        (f'Calculate the motivational force for {n0}.', v2(M0), f'MF = E × I × V = {v2(E0)} × {v2(I0)} × {V0} = {v2(M0)}. 1 mark method; 1 mark answer [2]'),
        ('Identify which scheme is predicted to motivate more effort, showing your working.', f'{cap(best[0])} (MF = {v2(best[5])} compared with {v2(worst[5])})',
         f'{v2(vals[1][2])} × {v2(vals[1][3])} × {vals[1][4]} = {v2(vals[1][5])}; compare with {v2(M0)}. 1 mark second MF; 1 mark correct choice [2]'),
        (f'Suggest how the manager could increase motivation for {worst[0]} without changing the reward itself.',
         ('Increase expectancy, for example through training or more resources so that effort is more likely to lead to success' if worst[2] <= worst[3] else
          'Increase instrumentality, for example by making clear and guaranteed rules about when the reward is given') + '.',
         f'Identifies the weakest of E ({v2(worst[2])}) or I ({v2(worst[3])}); 1 mark component; 1 mark method [2]'),
        ('Explain one limitation of using VIE theory to predict this employee’s effort.', 'It assumes the employee calculates rationally; valence and probabilities are subjective estimates and may change over time.', '1 mark limitation; 1 mark explained [2]'),
    ]
    m = (f'What is the motivational force for {n0}?', v2(M0), [v2(round(E0 + I0 + V0, 2)), v2(round(E0 * V0, 2)), v2(round(I0 * V0, 2)), v2(round(E0 * I0, 2))], f'{v2(E0)} × {v2(I0)} × {V0} = {v2(M0)} [1]')
    return intro, parts, m


score_tpl(c16b, 'vie', _vie)

c16c = T('Motivators at work: types of reward and intrinsic versus extrinsic motivation', 'motivators work types reward intrinsic extrinsic motivation')
build(c16c, {
    'terms': [
        ('intrinsic motivation', 'motivation that comes from the satisfaction of doing the task itself'),
        ('extrinsic motivation', 'motivation that comes from external rewards such as pay or praise, or from avoiding punishment'),
        ('performance-related pay', 'a reward system in which pay depends on the employee’s measured performance'),
        ('profit-sharing', 'a scheme in which employees receive a share of the organisation’s profits'),
        ('piece rate', 'a pay system in which employees are paid for each item they produce'),
        ('bonus', 'a one-off extra payment, usually for meeting a target'),
        ('non-monetary reward', 'a reward that is not money, such as praise, recognition, flexible hours or extra holiday'),
    ],
    'mcq': [
        ('In Deci’s (1971) study, students who were paid for solving Soma puzzles later', 'spent less free time on the puzzles than unpaid students', ['spent more free time on the puzzles', 'refused to take part', 'solved puzzles faster'], 'Overjustification: extrinsic reward reduced intrinsic motivation.'),
        ('Which of these is an intrinsic motivator?', 'Enjoying solving a challenging problem', ['A Christmas bonus', 'Employee-of-the-month award', 'A company car'], 'Satisfaction from the task itself.'),
        ('A scheme that pays all employees a share of the company’s annual earnings is called', 'profit-sharing', ['piece rate', 'performance-related pay', 'commission'], 'Shared profits.'),
    ],
    'ar': [
        ('Extrinsic rewards can reduce intrinsic motivation.', 'People may come to see the task as something done only for the reward.', 'AR', 'Deci’s overjustification effect.'),
    ],
    'explain': [
        ('Describe Deci’s (1971) study of intrinsic motivation.', 'Students solved Soma cube puzzles in three sessions. In session 2 the experimental group was paid $1 per puzzle; the control group was never paid. In free-choice periods, the paid group spent less time on puzzles in session 3 (after payment stopped) than before, compared with the control group.', '1 mark procedure; 1 mark payment manipulation; 1 mark findings [3]'),
        ('Compare performance-related pay and profit-sharing as reward systems.', 'Performance-related pay links reward to each individual’s measured performance, so it can motivate individuals but may cause competition; profit-sharing rewards everyone according to company success, encouraging teamwork but with a weak link to individual effort.', '1 mark each description; 1 mark comparison [3]'),
    ],
    'claims': [
        ('Paying people for a task they already enjoy always increases their motivation.', False, 'Deci found that payment can undermine intrinsic motivation once it stops.'),
        ('Praise and recognition are forms of extrinsic reward.', True, 'They come from outside the task, though they may support feelings of competence.'),
    ],
    'who': 'Deci’s (1971) laboratory study of rewards and intrinsic motivation',
    'evals': [
        ('controls', 'strength', 'A control group was never paid, so the change in free-choice time can be attributed to payment.'),
        ('objective measure', 'strength', 'Time spent on puzzles in the free-choice period was measured covertly, reducing demand characteristics.'),
        ('ecological validity', 'weakness', 'Solving puzzles for $1 in a laboratory is very different from long-term pay at work.'),
        ('generalisability', 'weakness', 'Participants were university students, so the findings may not apply to employees who need their wage.'),
    ],
    'apply': [
        ('A software company in {city} introduces a bonus for every bug fixed. Programmers who used to enjoy fixing difficult bugs now only fix easy ones.',
         [('Explain this change using the concept of intrinsic and extrinsic motivation.', 'The bonus makes fixing bugs extrinsically motivated; it undermines the enjoyment of challenge (overjustification), and easy bugs earn the same reward for less effort.', '1 mark undermining; 1 mark easy bugs maximise reward [2]'),
          ('Suggest an alternative reward system and explain why it might be better.', 'Profit-sharing or recognition for solving difficult problems, so reward is not tied to the number of bugs and challenge is valued.', '1 mark system; 1 mark reason [2]'),
          ('Suggest one non-monetary way of increasing intrinsic motivation.', 'Give programmers autonomy to choose interesting projects, or time for creative work.', '1 mark [1]')]),
    ],
})
chapter(16, [c16a, c16b, c16c], MOT_SHARED)

# ============================================================== ORGANISATIONAL 17: Leadership and management

LEAD_SHARED = {
    'essays': [
        ('effective leadership depends more on the situation than on the leader’s traits',
         ['Fiedler’s contingency theory shows that task- and relationship-motivated leaders are effective in different situations.', 'Path-goal theory says leaders should change style to suit followers and tasks.'],
         ['Universalist theories such as charismatic and transformational leadership find some traits linked to success in many situations.', 'Situations are hard to measure, and leaders may be unable to change style easily.'],
         ['universalist versus situational', 'usefulness', 'determinism']),
        ('the relationship between leaders and followers is the most important factor in leadership',
         ['LMX theory shows that high-quality exchanges lead to better performance, satisfaction and lower turnover.', 'Leader–member relations are the most important factor in Fiedler’s situational favourableness.'],
         ['Leader behaviour (initiating structure) and the task also matter.', 'In-groups and out-groups can create unfairness in teams.'],
         ['individual differences', 'ethics', 'usefulness']),
    ],
    'exp': [dict(intro=['A retail chain in {city} compared customer-satisfaction ratings (out of 100) for {n} stores whose managers had completed training in considerate leadership and {n} stores whose managers had not.',
                        '{person} compared staff satisfaction scores (out of 100) for {n} teams with leaders trained in “consideration” and {n} teams with untrained leaders.'],
                 A='trained', B='untrained', gA='teams whose leaders received consideration training', gB='teams whose leaders were not trained',
                 more='will have higher satisfaction scores than', measure='satisfaction score', dvshort='Satisfaction score (out of 100)',
                 iv='whether the leader received consideration training', dv='the mean satisfaction score from a questionnaire completed by team members',
                 range=(30, 100), base=(60, 66), diff=(5, 10), sd=6, nosample=True,
                 controls=['teams of similar size and type of work', 'the same questionnaire given at the same time of year'],
                 ethics=['team members’ answers about their leader should be anonymous', 'untrained leaders should be offered the training afterwards'],
                 concl_A='training leaders in consideration increases satisfaction.', concl_B='untrained leaders produce higher satisfaction than trained leaders.')],
    'plan': [('whether team members of high-quality LMX relationships are more satisfied than those in low-quality relationships', 'co-variable 1: LMX score', 'co-variable 2: job satisfaction score', ['correlation', 'questionnaire']),
             ('which leadership behaviours supervisors in a factory use most often', 'behaviour category 1: initiating structure', 'behaviour category 2: consideration', ['observation', 'interview'])],
    'plan_lead': 'Design',
}

c17a = T('Universalist and behavioural theories of leadership', 'universalist behavioural theories leadership')
build(c17a, {
    'terms': [
        ('universalist theory of leadership', 'a theory that the same characteristics make a leader effective in all situations'),
        ('great man theory', 'the universalist idea that leaders are born with traits that make them great'),
        ('transformational leadership', 'leadership that inspires followers through vision, charisma and individual consideration to go beyond their own interests'),
        ('initiating structure', 'leader behaviour that organises tasks, sets goals and defines roles (Ohio State studies)'),
        ('consideration', 'leader behaviour that shows concern, trust and respect for followers (Ohio State studies)'),
        ('managerial grid', 'Blake and Mouton’s model that classifies leaders by concern for people and concern for production, each on a scale of 1 to 9'),
    ],
    'mcq': [
        ('In Blake and Mouton’s managerial grid, a 9,9 leader is described as', 'team management', ['country club management', 'impoverished management', 'authority-compliance management'], 'High concern for both people and production.'),
        ('The Ohio State studies identified which two dimensions of leader behaviour?', 'Initiating structure and consideration', ['Task and relationship motivation', 'Expectancy and valence', 'Assertiveness and cooperativeness'], 'LBDQ dimensions.'),
        ('Which approach assumes leaders are born rather than made?', 'Great man theory', ['Behavioural theory', 'Path-goal theory', 'LMX theory'], 'Innate traits.'),
        ('A leader who shows high concern for people but low concern for production (1,9) is', 'country club management', ['team management', 'middle-of-the-road management', 'impoverished management'], 'Friendly but little focus on output.'),
    ],
    'ar': [
        ('Behavioural theories of leadership suggest that leadership can be trained.', 'Behaviours such as consideration can be learned.', 'AR', 'If leadership is behaviour, it can be taught.'),
        ('Universalist theories of leadership take the situation into account.', 'Universalist theories propose qualities that are effective in all situations.', 'R', 'They ignore the situation, so the assertion is false.'),
    ],
    'explain': [
        ('Explain the difference between universalist and behavioural theories of leadership.', 'Universalist theories focus on who the leader is (traits, charisma) and assume these work everywhere; behavioural theories focus on what the leader does (for example consideration and initiating structure), which can be observed and learned.', '1 mark universalist; 1 mark behavioural; 1 mark difference made explicit [3]'),
        ('Describe Blake and Mouton’s managerial grid.', 'Leaders are rated 1–9 on concern for production and concern for people; positions include impoverished (1,1), country club (1,9), authority-compliance (9,1), middle of the road (5,5) and team management (9,9), which is seen as ideal.', '1 mark two dimensions; 1 mark example styles; 1 mark 9,9 ideal [3]'),
    ],
    'claims': [
        ('Transformational leaders mainly motivate followers through rewards and punishments.', False, 'That is transactional leadership; transformational leaders inspire with vision and charisma.'),
        ('Behavioural theories can be studied by observing or rating what leaders do.', True, 'For example the Leader Behaviour Description Questionnaire.'),
    ],
    'who': 'the Ohio State behavioural studies of leadership',
    'evals': [
        ('usefulness', 'strength', 'Identifying behaviours means leaders can be trained in consideration and structure.'),
        ('measurement', 'strength', 'The LBDQ gives quantitative ratings of leader behaviour from followers.'),
        ('situational factors', 'weakness', 'The best combination of behaviours depends on the situation, which the approach does not fully explain.'),
        ('self-report', 'weakness', 'Followers’ ratings of leaders may be biased by how much they like the leader.'),
    ],
    'apply': [
        ('{person}, a new manager at a bank in {city}, focuses entirely on targets and deadlines and rarely talks to staff about their concerns. Staff turnover has risen.',
         [('Identify {person}’s position on Blake and Mouton’s managerial grid.', 'Authority-compliance (9,1): high concern for production, low concern for people.', '1 mark [1]'),
          ('Using the Ohio State dimensions, explain why turnover may have risen.', 'High initiating structure with low consideration leaves staff feeling unvalued, reducing satisfaction and increasing turnover.', '1 mark low consideration; 1 mark effect [2]'),
          ('Suggest how {person} could become a 9,9 leader.', 'Keep clear goals while involving staff in decisions, listening to concerns and showing appreciation.', '1 mark people; 1 mark production [2]')]),
    ],
})

c17b = T("Leadership style and effectiveness: Fiedler's contingency, path-goal", 'leadership style effectiveness fiedler contingency path-goal')
build(c17b, {
    'terms': [
        ('contingency theory', 'Fiedler’s theory that leader effectiveness depends on the match between the leader’s style and the favourableness of the situation'),
        ('least preferred co-worker (LPC) scale', 'Fiedler’s scale on which leaders rate the person they least like working with; a high score indicates a relationship-motivated leader'),
        ('situational favourableness', 'in Fiedler’s model, how much control the leader has, based on leader–member relations, task structure and position power'),
        ('path-goal theory', 'House’s theory that leaders should clarify the path to goals and choose directive, supportive, participative or achievement-oriented behaviour to suit followers and the task'),
        ('position power', 'the formal authority a leader has to reward and punish'),
    ],
    'foils': ['initiating structure', 'in-group'],
    'mcq': [
        ('According to Fiedler, task-motivated (low-LPC) leaders are most effective when the situation is', 'very favourable or very unfavourable', ['moderately favourable', 'always unfavourable', 'unrelated to performance'], 'Low-LPC fit extremes.'),
        ('Which is NOT one of Fiedler’s three situational factors?', 'Follower intelligence', ['Leader–member relations', 'Task structure', 'Position power'], 'Follower intelligence is not in the model.'),
        ('In path-goal theory, a leader who sets challenging goals and shows confidence in followers is', 'achievement-oriented', ['directive', 'supportive', 'participative'], 'Achievement-oriented.'),
        ('In path-goal theory, consulting followers and using their suggestions is', 'participative leadership', ['directive leadership', 'supportive leadership', 'achievement-oriented leadership'], 'Participative.'),
    ],
    'ar': [
        ('Fiedler believed leaders should be matched to situations rather than trained to change style.', 'Fiedler saw leadership style as fairly fixed.', 'AR', 'Fixed style → change the situation or the leader.'),
        ('Path-goal theory says one leadership style is best in all situations.', 'Path-goal theory describes four types of leader behaviour.', 'R', 'It is a situational theory, so the assertion is false; the reason is true.'),
    ],
    'explain': [
        ('Explain how Fiedler measured leadership style.', 'Leaders rated their least preferred co-worker on 18 bipolar adjective scales (such as unfriendly–friendly) from 1 to 8; a high total shows the leader can still see the co-worker positively (relationship-motivated), a low total shows task motivation.', '1 mark LPC rating; 1 mark scoring; 1 mark interpretation [3]'),
        ('Explain how path-goal theory predicts the best leadership behaviour.', 'The leader’s job is to help followers reach goals; directive behaviour suits ambiguous tasks and inexperienced staff, supportive behaviour suits stressful or boring tasks, participative suits capable staff who want involvement, and achievement-oriented suits complex tasks.', '1 mark role of leader; 2 marks matching examples [3]'),
    ],
    'claims': [
        ('In Fiedler’s model, a leader with good relations, a structured task and strong position power is in a very favourable situation.', True, 'All three factors favour the leader.'),
        ('A high LPC score shows that a leader is task-motivated.', False, 'A high score indicates a relationship-motivated leader.'),
    ],
    'who': 'Fiedler’s contingency theory of leadership',
    'evals': [
        ('situational factors', 'strength', 'It recognises that no single style is best, so it explains why leaders succeed in one role but fail in another.'),
        ('usefulness', 'strength', 'Organisations can match leaders to situations or change the situation (for example task structure).'),
        ('measurement validity', 'weakness', 'It is unclear what the LPC scale really measures, and scores may change over time.'),
        ('flexibility', 'weakness', 'It assumes style is fixed, ignoring evidence that leaders can adapt their behaviour.'),
    ],
    'apply': [
        ('{person} has just become supervisor of a new team of inexperienced call-centre staff in {city}. The procedures are unclear and staff are anxious.',
         [('Using path-goal theory, suggest which leader behaviour {person} should use and explain why.', 'Directive and supportive behaviour: give clear instructions because the task is ambiguous and staff inexperienced, and support them because they are anxious.', '1 mark behaviour; 1 mark reason [2]'),
          ('Explain how {person}’s behaviour should change as staff gain experience.', 'Move towards participative or achievement-oriented behaviour, since experienced staff need less direction and want involvement or challenge.', '1 mark change; 1 mark reason [2]'),
          ('Explain one weakness of path-goal theory.', 'It is complex, with many variables, so it is hard to test and to apply in practice.', '1 mark [1]')]),
    ],
})


def _lpc(r, D):
    d = ctx(r)
    target = r.choice([r.randint(40, 54), r.randint(73, 100), r.randint(56, 71)])
    items = [r.randint(1, 8) for _ in range(18)]
    for _ in range(400):
        s = sum(items)
        if s == target:
            break
        i = r.randrange(18)
        if s < target and items[i] < 8:
            items[i] += 1
        elif s > target and items[i] > 1:
            items[i] -= 1
    tot = sum(items)
    cls = 'relationship-motivated (high LPC)' if tot >= 73 else 'task-motivated (low LPC)' if tot <= 54 else 'in the middle range (neither clearly high nor clearly low LPC)'
    sit = r.choice([('good', 'structured', 'strong', 'very favourable'), ('poor', 'unstructured', 'weak', 'very unfavourable'), ('good', 'unstructured', 'weak', 'moderately favourable'), ('poor', 'structured', 'strong', 'moderately favourable')])
    fit = 'task-motivated (low-LPC)' if sit[3] != 'moderately favourable' else 'relationship-motivated (high-LPC)'
    intro = (f'{d["person"]}, a manager in {d["city"]}, completed Fiedler’s LPC scale. The 18 item ratings (1–8) were: {", ".join(map(str, items))}. '
             f'Fiedler classified totals of 73 or more as high LPC and 54 or less as low LPC. {d["person"]}’s team has {sit[0]} leader–member relations, {"an" if sit[1][0] in "aeiou" else "a"} {sit[1]} task and {sit[2]} position power.')
    parts = [
        ('Calculate the total LPC score.', str(tot), f'Sum of the 18 ratings = {tot}. 1 mark correct total [1]'),
        (f'Identify {d["person"]}’s leadership style.', cap(cls), f'{tot} → {cls} [1]'),
        ('Describe the favourableness of the situation.', cap(sit[3]), f'{sit[0]} relations, {sit[1]} task, {sit[2]} power → {sit[3]}. 1 mark identifies favourableness; 1 mark uses the three factors [2]'),
        ('Using Fiedler’s theory, state which type of leader would be most effective here, and whether this manager is a good match.', f'A {fit} leader; ' + ('the match is good.' if (('task' in fit and tot <= 54) or ('relationship' in fit and tot >= 73)) else 'this manager is not a clear match, so Fiedler would suggest changing the situation or the leader.'),
         '1 mark correct leader type for the situation; 1 mark judgement about this manager [2]'),
        ('Explain one problem with using the LPC scale to measure leadership style.', 'It is a self-report rating of one person, so it may be affected by recent events; it is unclear exactly what it measures, and scores can change over time (low test–retest reliability).', '1 mark problem; 1 mark explained [2]'),
    ]
    m = (f'What is the manager’s total LPC score?', str(tot), [str(tot + 8), str(tot - 6), str(round(tot / 18, 1)), str(tot + 18)], f'Sum = {tot} [1]')
    return intro, parts, m


score_tpl(c17b, 'lpc', _lpc)

c17c = T('Leaders and followers: leader-member exchange theory', 'leaders followers leader-member exchange theory')
build(c17c, {
    'terms': [
        ('leader–member exchange (LMX) theory', 'the theory that leaders form relationships of different quality with each follower, creating in-groups and out-groups'),
        ('in-group', 'in LMX theory, followers with high-quality relationships with the leader, based on trust and mutual support'),
        ('out-group', 'in LMX theory, followers whose relationship with the leader is limited to the formal job contract'),
        ('leadership making', 'Graen and Uhl-Bien’s model in which relationships develop from stranger to acquaintance to mature partnership'),
        ('followership', 'the role and behaviour of people who follow a leader, which affects how effective leadership is'),
    ],
    'foils': ['position power', 'consideration'],
    'mcq': [
        ('According to LMX theory, in-group members tend to receive', 'more responsibility, support and attention from the leader', ['only formal contract benefits', 'fewer challenging tasks', 'lower ratings of performance'], 'High-quality exchange.'),
        ('In Graen and Uhl-Bien’s leadership-making model, the final stage is', 'mature partnership', ['stranger', 'acquaintance', 'storming'], 'Stranger → acquaintance → partnership.'),
        ('Which outcome is linked to high-quality LMX relationships?', 'Lower staff turnover', ['Higher absenteeism', 'More conflict', 'Lower job satisfaction'], 'Better outcomes for in-group members.'),
    ],
    'ar': [
        ('LMX theory differs from many leadership theories.', 'It focuses on the relationship between the leader and each individual follower.', 'AR', 'Dyadic focus rather than a single style for all.'),
    ],
    'explain': [
        ('Explain what is meant by in-groups and out-groups in LMX theory.', 'In-group members have high-quality relationships with trust, support and extra responsibilities beyond the contract; out-group members have low-quality relationships limited to formal job requirements.', '1 mark in-group; 1 mark out-group [2]'),
        ('Explain one ethical problem with LMX theory.', 'Leaders favouring an in-group may treat out-group members unfairly, for example giving them fewer opportunities, which can be discriminatory if based on similarity rather than performance.', '1 mark unfairness; 1 mark explained [2]'),
    ],
    'claims': [
        ('LMX theory suggests that leaders treat all followers in the same way.', False, 'Leaders develop different-quality relationships with different followers.'),
        ('Leaders can be trained to offer high-quality relationships to all followers.', True, 'Leadership-making training aims to develop partnerships with every follower.'),
    ],
    'who': 'leader–member exchange (LMX) theory',
    'evals': [
        ('usefulness', 'strength', 'It explains why some employees are more satisfied and committed than others under the same leader.'),
        ('research support', 'strength', 'High-quality LMX has been linked to better performance, satisfaction and lower turnover.'),
        ('cause and effect', 'weakness', 'Most evidence is correlational, so good performance may cause a good relationship rather than the reverse.'),
        ('ethics', 'weakness', 'It may seem to justify favouritism and unequal treatment of out-group members.'),
    ],
    'apply': [
        ('In an engineering team in {city}, {person} is often given interesting projects and chats with the manager daily, while {person2} receives only routine tasks and formal instructions.',
         [('Using LMX theory, identify which group each employee belongs to.', '{person} is in the in-group; {person2} is in the out-group.', '1 mark [1]'),
          ('Explain how this difference may affect {person2}’s job satisfaction.', '{person2} receives less support, trust and opportunity, so is likely to be less satisfied and more likely to leave.', '1 mark effect; 1 mark reason [2]'),
          ('Suggest how the manager could improve the relationship with {person2}.', 'Offer {person2} a challenging task and regular one-to-one meetings to build trust (moving from stranger towards partnership).', '1 mark action; 1 mark linked to theory [2]')]),
    ],
})
chapter(17, [c17a, c17b, c17c], LEAD_SHARED)

# ============================================================== ORGANISATIONAL 18: Group behaviour in organisations

GRP_SHARED = {
    'essays': [
        ('groups make better decisions than individuals',
         ['Groups combine knowledge and skills; teams with a balance of Belbin roles perform better.', 'Discussion can expose errors that one person would miss.'],
         ['Groupthink (Janis) can lead cohesive groups to poor decisions, for example the Bay of Pigs invasion.', 'Group polarisation can make decisions more extreme.', 'Groups take longer and some members may contribute little (social loafing).'],
         ['groupthink', 'usefulness', 'situational factors']),
        ('conflict at work is always harmful',
         ['Conflict can cause stress, absence and poor communication.', 'Unresolved conflict can lead to staff leaving.'],
         ['Moderate conflict can bring out new ideas and prevent groupthink.', 'Thomas and Kilmann show that conflict can be handled constructively, for example by collaborating.'],
         ['individual differences', 'usefulness', 'situational factors']),
    ],
    'exp': [dict(intro=['{person} gave {n} work teams in {city} a business problem to solve. In half the teams one member was asked to act as devil’s advocate. Two experts rated the quality of each team’s decision out of 20.',
                        'A company in {city} compared decision-quality ratings (out of 20) for {n} teams with an appointed devil’s advocate and {n} teams without one.'],
                 A='devil’s advocate', B='no devil’s advocate', gA='teams with a devil’s advocate', gB='teams without a devil’s advocate',
                 more='will make higher-quality decisions than', measure='decision-quality rating', dvshort='Decision quality (out of 20)',
                 iv='whether the team had an appointed devil’s advocate', dv='the mean decision-quality rating out of 20 given by two independent experts',
                 range=(0, 20), base=(10, 12), diff=(2, 4), sd=2, nosample=True,
                 controls=['the same business problem and time limit for every team', 'experts who did not know which condition each team was in'],
                 ethics=['team members should not be made to feel their abilities are being judged publicly', 'teams should be debriefed about the purpose of the devil’s advocate'],
                 concl_A='having a devil’s advocate improves group decisions.', concl_B='having a devil’s advocate makes group decisions worse.')],
    'plan': [('how often the symptoms of groupthink occur in management meetings', 'behaviour category 1: pressure on dissenters', 'behaviour category 2: self-censorship', ['observation']),
             ('whether teams with a balance of Belbin roles perform better than unbalanced teams', 'IV: balanced or unbalanced team', 'DV: score in a business game', ['field experiment', 'laboratory experiment'])],
    'plan_lead': 'Design',
}

c18a = T('Group development and decision-making: Tuckman, groupthink', 'group development decision-making tuckman groupthink')
build(c18a, {
    'terms': [
        ('forming', 'Tuckman’s first stage of group development, when members are polite, uncertain and getting to know each other'),
        ('storming', 'Tuckman’s stage in which conflict arises over roles, leadership and tasks'),
        ('norming', 'Tuckman’s stage in which the group agrees rules and roles and becomes cohesive'),
        ('performing', 'Tuckman’s stage in which the group works effectively towards its goals'),
        ('groupthink', 'Janis’s term for faulty decision-making in a cohesive group that values agreement more than a realistic appraisal of alternatives'),
        ('mindguard', 'a group member who protects the group from information that might challenge its decisions'),
        ('group polarisation', 'the tendency for group decisions to be more extreme than the average of members’ initial views'),
    ],
    'mcq': [
        ('Which is the correct order of Tuckman’s stages?', 'Forming, storming, norming, performing', ['Forming, norming, storming, performing', 'Storming, forming, norming, performing', 'Norming, forming, performing, storming'], 'Adjourning was added later (1977).'),
        ('Which is a symptom of groupthink according to Janis?', 'Illusion of unanimity', ['Use of outside experts', 'Appointing a devil’s advocate', 'Leader withholding opinions'], 'The others are ways to prevent groupthink.'),
        ('Which fifth stage did Tuckman and Jensen (1977) add?', 'Adjourning', ['Reforming', 'Conforming', 'Transforming'], 'The group breaks up.'),
        ('Which condition makes groupthink more likely?', 'A highly cohesive group with a directive leader', ['A group with many outside experts', 'A leader who encourages criticism', 'No time pressure'], 'Janis’s antecedents.'),
    ],
    'ar': [
        ('Groupthink is more likely in highly cohesive groups.', 'Members of cohesive groups do not want to disrupt agreement.', 'AR', 'Desire for harmony suppresses dissent.'),
        ('Tuckman’s model says that groups never return to an earlier stage.', 'Conflict typically occurs in the storming stage.', 'R', 'Groups can regress (for example when new members join), so the assertion is false.'),
    ],
    'explain': [
        ('Describe three symptoms of groupthink.', 'Illusion of invulnerability (overconfidence); direct pressure on dissenters to conform; self-censorship of doubts; illusion of unanimity; collective rationalisation of warnings; mindguards; stereotyped views of outsiders; belief in the group’s morality.', '1 mark per symptom described [3]'),
        ('Explain two ways an organisation could prevent groupthink.', 'Appoint a devil’s advocate to challenge ideas; the leader should not state a preference at the start; invite outside experts; split into sub-groups; hold a “second-chance” meeting.', '1 mark each method, 1 mark each explanation [4]'),
    ],
    'claims': [
        ('In the storming stage, members are polite and avoid disagreement.', False, 'That describes forming; storming involves conflict.'),
        ('Groupthink can lead to poor decisions even when group members are intelligent.', True, 'The problem is the group process, not ability (for example the Bay of Pigs).'),
    ],
    'who': 'Janis’s theory of groupthink',
    'evals': [
        ('usefulness', 'strength', 'It identifies symptoms and preventive measures, such as a devil’s advocate, that organisations can use.'),
        ('real-world evidence', 'strength', 'It is supported by analyses of real policy failures such as the Bay of Pigs invasion.'),
        ('method', 'weakness', 'Evidence comes largely from retrospective case studies, which are open to interpretation and hindsight bias.'),
        ('cohesion', 'weakness', 'Laboratory studies show cohesion does not always lead to groupthink, so the model may be oversimplified.'),
    ],
    'apply': [
        ('A management board in {city} has worked together for ten years. At a meeting about a risky expansion, the chief executive announces her support first, and nobody raises concerns. One manager later says he had doubts but “didn’t want to spoil the mood”.',
         [('Identify two symptoms of groupthink in this situation.', 'Self-censorship (the manager kept doubts to himself) and illusion of unanimity (no one raised concerns).', '1 mark each [2]'),
          ('Explain why this board was at risk of groupthink.', 'It is highly cohesive after ten years together and the leader stated a preference first, which discourages dissent.', '1 mark cohesion; 1 mark leader [2]'),
          ('Suggest two changes to the board’s decision-making.', 'The chief executive should speak last; appoint a devil’s advocate or bring in an outside expert.', '1 mark each [2]')]),
        ('A new project team in {city} has just been formed. In the first weeks members argued about who should lead and how work should be divided.',
         [('Identify the stage of Tuckman’s model shown by the arguments.', 'Storming.', '1 mark [1]'),
          ('Describe what should happen next if the team develops normally.', 'Norming: members agree roles and rules and become cohesive, then performing: they focus on the task effectively.', '1 mark norming; 1 mark performing [2]'),
          ('Explain one limitation of Tuckman’s model.', 'Not all groups pass through the stages in order; some skip or return to stages, and it was based on reviews of small groups rather than work teams.', '1 mark limitation; 1 mark explained [2]')]),
    ],
})

c18b = T('Team roles and team building: Belbin', 'team roles team building belbin')
build(c18b, {
    'terms': [
        ('team role', 'in Belbin’s theory, a tendency to behave, contribute and interact with others in a particular way'),
        ('plant', 'Belbin’s creative team role that generates ideas and solves difficult problems'),
        ('monitor evaluator', 'Belbin’s team role that judges ideas logically and objectively'),
        ('completer finisher', 'Belbin’s team role that checks for errors and ensures deadlines are met'),
        ('shaper', 'Belbin’s team role that drives the team forward and challenges others'),
        ('co-ordinator', 'Belbin’s team role that clarifies goals, delegates and acts as a chairperson'),
        ('team building', 'activities designed to improve relationships, communication and cooperation in a team'),
    ],
    'mcq': [
        ('Which Belbin role is most likely to produce original ideas?', 'Plant', ['Completer finisher', 'Implementer', 'Teamworker'], 'Creative problem solver.'),
        ('Which Belbin role was added after the original eight?', 'Specialist', ['Shaper', 'Plant', 'Co-ordinator'], 'Specialist was added in 1993.'),
        ('Belbin’s team roles are grouped into which three categories?', 'Action-oriented, people-oriented and thinking-oriented', ['Existence, relatedness and growth', 'Forming, storming and norming', 'Competing, avoiding and accommodating'], 'Three clusters of three.'),
        ('A team member who explores opportunities and develops contacts outside the team is a', 'resource investigator', ['monitor evaluator', 'completer finisher', 'specialist'], 'Outgoing, networking.'),
    ],
    'ar': [
        ('Belbin found that teams of only highly intelligent people did not always perform best.', 'Belbin argued that a balance of team roles matters more than individual ability.', 'AR', 'The “Apollo syndrome”.'),
    ],
    'explain': [
        ('Explain what Belbin meant by a balanced team.', 'A team in which all the necessary roles (for example ideas, evaluation, coordination, implementation and finishing) are covered, so that strengths compensate for allowable weaknesses; people can take more than one role.', '1 mark range of roles; 1 mark compensating weaknesses [2]'),
        ('Explain how Belbin’s theory could be used for team building.', 'Staff complete the self-perception inventory and observer ratings; managers identify missing or duplicated roles, then select or train members and discuss roles so that people understand each other’s contributions.', '1 mark measurement; 1 mark use in selection or discussion [2]'),
    ],
    'claims': [
        ('Each person can perform only one Belbin team role.', False, 'People usually have two or three preferred roles.'),
        ('Belbin’s research was based on management teams playing business games.', True, 'He observed teams at Henley Management College.'),
    ],
    'who': 'Belbin’s team-role theory',
    'evals': [
        ('usefulness', 'strength', 'It gives managers a practical tool to build balanced teams and understand conflicts between roles.'),
        ('research base', 'strength', 'It was developed from years of observing real management teams in business games.'),
        ('reliability', 'weakness', 'The self-perception inventory is self-report and has been criticised for weak reliability and validity.'),
        ('generalisability', 'weakness', 'It was developed with managers in business games, so may not apply to other types of team or real work.'),
    ],
    'apply': [
        ('A design team in {city} produces many creative ideas but often misses deadlines and makes careless errors.',
         [('Using Belbin’s theory, identify a role that the team probably lacks and explain why.', 'Completer finisher (or implementer), who checks for errors and ensures deadlines are met.', '1 mark role; 1 mark reason [2]'),
          ('Identify a role the team probably has too many of.', 'Plant (creative ideas generator).', '1 mark [1]'),
          ('Suggest how the manager could use Belbin’s ideas to improve the team.', 'Assess members’ roles with the inventory, then recruit or reassign someone with completer-finisher strengths and discuss roles openly.', '1 mark assessment; 1 mark action [2]')]),
    ],
})

c18c = T('Conflict at work: causes and management (Thomas-Kilmann)', 'conflict work causes management thomas-kilmann')
build(c18c, {
    'terms': [
        ('organisational conflict', 'disagreement between individuals or groups at work arising from differences in goals, values, interests or resources'),
        ('competing', 'Thomas–Kilmann conflict mode that is assertive and uncooperative: pursuing one’s own concerns at the other’s expense'),
        ('accommodating', 'Thomas–Kilmann conflict mode that is unassertive and cooperative: giving way to the other person'),
        ('avoiding', 'Thomas–Kilmann conflict mode that is unassertive and uncooperative: not addressing the conflict'),
        ('collaborating', 'Thomas–Kilmann conflict mode that is assertive and cooperative: working together to fully satisfy both sides'),
        ('compromising', 'Thomas–Kilmann conflict mode that is moderately assertive and moderately cooperative: each side gives up something'),
    ],
    'foils': ['groupthink', 'norming'],
    'mcq': [
        ('The Thomas–Kilmann model classifies conflict modes on which two dimensions?', 'Assertiveness and cooperativeness', ['Concern for production and concern for people', 'Expectancy and valence', 'Task structure and position power'], 'Assertive (own concerns) vs cooperative (other’s concerns).'),
        ('Which conflict mode is described as “win–win”?', 'Collaborating', ['Compromising', 'Competing', 'Avoiding'], 'Both sides fully satisfied.'),
        ('Two departments compete for the same limited budget. This is an example of conflict caused by', 'scarce resources', ['role ambiguity only', 'groupthink', 'job enrichment'], 'Competition for resources.'),
        ('Which conflict mode is most appropriate when an issue is trivial and tempers need to cool?', 'Avoiding', ['Competing', 'Collaborating', 'Accommodating'], 'Postponing can be useful.'),
    ],
    'ar': [
        ('Compromising often leaves both sides partly dissatisfied.', 'In compromising, each side gives up part of what it wants.', 'AR', 'Middle ground.'),
    ],
    'explain': [
        ('Describe three causes of conflict at work.', 'Competition for scarce resources (budgets, equipment); interdependence of tasks; different goals between departments; unclear roles or responsibilities; poor communication; personality differences or perceived unfairness.', '1 mark per cause described [3]'),
        ('Explain the difference between collaborating and compromising.', 'Collaborating is high in assertiveness and cooperativeness and seeks a solution that fully satisfies both sides; compromising is moderate in both, with each side giving up some of what it wants to reach a quick acceptable solution.', '1 mark each; 1 mark comparison [3]'),
    ],
    'claims': [
        ('According to Thomas and Kilmann, one conflict mode is always the best.', False, 'Each mode can be appropriate in different situations.'),
        ('The Thomas–Kilmann Instrument (TKI) is a questionnaire measuring a person’s preferred conflict modes.', True, 'It uses 30 forced-choice pairs of statements.'),
    ],
    'who': 'the Thomas–Kilmann model of conflict management',
    'evals': [
        ('usefulness', 'strength', 'It helps managers and staff understand their own preferred styles and choose a more suitable one.'),
        ('flexibility', 'strength', 'It recognises that every mode can be useful in some situations rather than prescribing one approach.'),
        ('self-report', 'weakness', 'The TKI relies on self-report, so people may give socially desirable answers.'),
        ('reductionism', 'weakness', 'Reducing conflict behaviour to two dimensions ignores emotions, power and culture.'),
    ],
    'apply': [
        ('{person} and {person2} work in a hospital in {city}. Both want the same week of holiday, and only one can be absent. {person} insists, while {person2} says nothing and lets {person} have the week, but is now resentful.',
         [('Identify the conflict modes used by {person} and {person2}.', '{person}: competing; {person2}: accommodating.', '1 mark each [2]'),
          ('Identify the cause of the conflict.', 'Scarce resources (limited holiday cover).', '1 mark [1]'),
          ('Suggest how the manager could help them collaborate.', 'Meet both, explore underlying needs (for example one needs travel dates, the other a family event) and find a solution such as splitting weeks or finding cover.', '1 mark exploring needs; 1 mark win–win solution [2]')]),
    ],
})
add_tally_pct(c18c, ['An HR department in {city} recorded how workplace disputes were handled and whether they were still unresolved three months later.', '{person} analysed records of disputes at a company in {city} by the conflict mode used.'],
              [('Collaborating', (18, 30), (3, 8)), ('Compromising', (16, 26), (6, 12)), ('Competing', (8, 16), (12, 20)), ('Avoiding', (4, 10), (14, 24)), ('Accommodating', (10, 18), (8, 14))],
              ('resolved', 'unresolved', 'disputes'))
chapter(18, [c18a, c18b, c18c], GRP_SHARED)

# ============================================================== ORGANISATIONAL 19: Organisational work conditions

WC_SHARED = {
    'essays': [
        ('open-plan offices are good for employees',
         ['They can increase communication and teamwork and make supervisors more accessible.', 'They are cheaper and more flexible.'],
         ['Oldham and Brass (1979) found satisfaction and motivation fell after a move to open-plan.', 'Noise and interruptions reduce concentration and privacy.'],
         ['validity of evidence', 'individual differences', 'usefulness']),
        ('organisations can reduce the harmful effects of shift work',
         ['Czeisler et al. (1982) found forward rotation and longer rotation periods improved satisfaction, health and productivity.', 'Bright light and planned sleep can help adjust circadian rhythms.'],
         ['Gold et al. (1992) found rotating nurses had more sleep problems and accidents than fixed-shift nurses.', 'Some workers never fully adjust to nights, and family life is disrupted.'],
         ['biological explanations', 'usefulness', 'individual differences']),
    ],
    'exp': [dict(intro=['{person} measured the number of errors made in a data-entry task by {n} employees in {city} working in a quiet private office and {n} employees in a noisy open-plan office.',
                        'A company in {city} compared data-entry errors per hour for {n} staff in private offices and {n} staff in an open-plan office.'],
                 A='private office', B='open-plan office', gA='employees in private offices', gB='employees in open-plan offices',
                 more='will make fewer errors than', measure='the number of errors', dvshort='Errors per hour', higher='B',
                 iv='the type of office (private or open-plan)', dv='the number of data-entry errors per hour recorded by the computer system',
                 range=(0, 40), base=(8, 12), diff=(3, 7), sd=3, nosample=True,
                 controls=['the same data-entry task for all employees', 'similar experience and typing speed in both groups'],
                 ethics=['employees should consent to their errors being recorded', 'results should not be used to discipline individuals'],
                 concl_A='open-plan offices increase errors.', concl_B='private offices increase errors.')],
    'plan': [('whether forward-rotating shifts lead to fewer errors than backward-rotating shifts', 'IV: direction of shift rotation', 'DV: errors per shift', ['field experiment']),
             ('how employees feel about moving to an open-plan office', 'theme 1: privacy', 'theme 2: communication with colleagues', ['interview', 'questionnaire'])],
    'plan_lead': 'Design',
}

c19a = T('Physical and psychological work conditions: open-plan offices', 'physical psychological work conditions open-plan offices')
build(c19a, {
    'terms': [
        ('open-plan office', 'a large shared workspace without walls or private offices'),
        ('Hawthorne effect', 'a change in behaviour because people know they are being studied or receiving attention'),
        ('physical work conditions', 'features of the work environment such as lighting, noise, temperature and space'),
        ('psychological work conditions', 'social and emotional features of work such as relationships, bullying, privacy and control'),
        ('privacy', 'the ability to control interaction with others and to work without being seen or overheard'),
    ],
    'mcq': [
        ('Oldham and Brass (1979) found that after moving to an open-plan office, newspaper employees', 'reported lower satisfaction and internal motivation', ['reported higher satisfaction', 'made fewer interruptions', 'showed no change'], 'Satisfaction and motivation fell.'),
        ('In the Hawthorne studies, productivity increased when lighting was', 'both increased and decreased', ['only increased', 'only decreased', 'kept constant'], 'Attention, not lighting, explained the change.'),
        ('Which of these is a psychological work condition?', 'Workplace bullying', ['Lighting levels', 'Temperature', 'Noise from machinery'], 'Social/emotional.'),
    ],
    'ar': [
        ('Productivity rose in the Hawthorne studies regardless of the lighting change.', 'Workers knew they were being observed and given attention.', 'AR', 'The Hawthorne effect.'),
    ],
    'explain': [
        ('Describe Oldham and Brass’s (1979) study.', 'A quasi-experiment at a US newspaper office measured employees’ satisfaction and motivation before and after a move from conventional offices to an open-plan office, with control groups. After the move, satisfaction with work and supervisors, friendship opportunities and internal motivation fell, and employees reported more interruptions and less concentration.', '1 mark design; 1 mark measures; 1 mark findings [3]'),
        ('Explain why open-plan offices may reduce job satisfaction.', 'They increase noise, interruptions and the feeling of being watched, and reduce privacy and control over the workspace, so concentration and feedback relationships suffer.', '1 mark feature; 1 mark effect [2]'),
    ],
    'claims': [
        ('Open-plan offices always improve communication and satisfaction.', False, 'Oldham and Brass found satisfaction fell; communication may become more superficial.'),
        ('The Hawthorne effect is a problem for studies of work conditions.', True, 'Workers may change behaviour because they know they are being studied.'),
    ],
    'who': 'Oldham and Brass’s (1979) study of a move to an open-plan office',
    'evals': [
        ('ecological validity', 'strength', 'It was a real office move with real employees, so the findings reflect real working life.'),
        ('controls', 'strength', 'Measures before and after the move, plus control groups, allowed change to be attributed to the office design.'),
        ('self-report', 'weakness', 'Satisfaction was measured by questionnaire, which may be affected by social desirability.'),
        ('generalisability', 'weakness', 'It studied one newspaper organisation, so the findings may not apply to other types of work.'),
    ],
    'apply': [
        ('A technology company in {city} plans to move all staff into one open-plan office to save money and improve teamwork.',
         [('Using research, explain one risk of this change.', 'Oldham and Brass found satisfaction and internal motivation fell after a move to open-plan, partly due to interruptions and lack of privacy.', '1 mark risk; 1 mark research [2]'),
          ('Suggest two ways the company could reduce the problems of open-plan offices.', 'Provide quiet rooms or booths for concentration, use partitions or sound-absorbing materials, and allow some home working.', '1 mark each [2]'),
          ('Explain why measuring staff satisfaction straight after the move might be misleading.', 'The novelty and attention could cause a temporary Hawthorne effect, so long-term measures are needed.', '1 mark Hawthorne/novelty; 1 mark need for later measure [2]')]),
    ],
})

c19b = T('Temporal conditions of work environments: shift work and rotation', 'temporal conditions work environments shift work rotation')
build(c19b, {
    'terms': [
        ('shift work', 'work organised so that different groups of employees work at different times, often including nights'),
        ('forward rotation', 'changing shifts in the order morning → afternoon → night (phase delay), which is easier for the body clock to adjust to'),
        ('backward rotation', 'changing shifts in the order night → afternoon → morning (phase advance)'),
        ('rapid rotation', 'a shift system in which workers change shift every few days'),
        ('compressed working week', 'working the usual weekly hours in fewer, longer days'),
        ('circadian rhythm', 'a biological cycle of about 24 hours, such as the sleep–wake cycle'),
    ],
    'mcq': [
        ('Czeisler et al. (1982) studied workers at', 'a mineral and chemical plant in Utah', ['a hospital in Massachusetts', 'a newspaper office', 'a coal mine'], 'Great Salt Lake Minerals and Chemicals Corporation.'),
        ('Czeisler et al. recommended changing shift schedules so that they', 'rotated forwards and changed less often', ['rotated backwards every week', 'rotated every day', 'were all at night'], 'Phase delay with longer rotation periods.'),
        ('Gold et al. (1992) found that nurses on rotating shifts, compared with those on fixed shifts, had', 'more accidents and errors linked to sleepiness', ['fewer sleep problems', 'better health', 'no differences'], 'Rotators reported more accidents/errors.'),
    ],
    'ar': [
        ('Forward-rotating shifts are easier to adjust to than backward-rotating shifts.', 'The body clock finds it easier to lengthen the day (phase delay) than to shorten it.', 'AR', 'Free-running rhythm is slightly longer than 24 hours.'),
    ],
    'explain': [
        ('Describe the findings of Czeisler et al. (1982).', 'Workers moved from backward rotation every week to forward rotation (some with 21-day rotation) reported greater satisfaction with their schedules and better health; staff turnover fell and productivity rose.', '1 mark change made; 2 marks findings [3]'),
        ('Explain why shift work can affect health and safety.', 'Working at night conflicts with circadian rhythms, causing sleep loss and fatigue; tiredness reduces attention and increases accidents and errors, and long-term disruption is linked to health problems.', '1 mark rhythm disruption; 1 mark fatigue; 1 mark consequence [3]'),
    ],
    'claims': [
        ('Changing shifts every week is the best schedule for the body clock.', False, 'Czeisler found longer rotation periods (21 days) allowed better adjustment.'),
        ('Rotating shift workers may be at greater risk of accidents than fixed-shift workers.', True, 'Gold et al. found nurses on rotating shifts reported more accidents and errors.'),
    ],
    'who': 'Czeisler et al.’s (1982) study of shift rotation',
    'evals': [
        ('ecological validity', 'strength', 'It changed real shift schedules in a real workplace, so the findings apply directly to industry.'),
        ('usefulness', 'strength', 'It showed a simple, cheap change to schedules that improved satisfaction and productivity.'),
        ('controls', 'weakness', 'Workers knew the schedule had been changed, so improvements may partly be a Hawthorne effect.'),
        ('generalisability', 'weakness', 'It studied one male-dominated industrial plant, so the results may not apply to other jobs.'),
    ],
    'apply': [
        ('A factory in {city} rotates workers every week from nights to afternoons to mornings. Accidents are highest in the first days after each change.',
         [('Identify the type of rotation used.', 'Backward rotation (phase advance), changed weekly (rapid).', '1 mark [1]'),
          ('Using research, suggest two changes to the schedule.', 'Rotate forwards (morning → afternoon → night) and lengthen the rotation period, for example to 21 days (Czeisler et al.).', '1 mark each [2]'),
          ('Explain why accidents are highest just after a change.', 'Circadian rhythms have not adjusted to the new hours, so workers are sleepy and less alert.', '1 mark rhythm; 1 mark alertness [2]')]),
    ],
})
add_tally_pct(c19b, ['A hospital in {city} asked nurses on different schedules whether they had nodded off while driving to or from work in the past year.', '{person} surveyed nurses in {city} about falling asleep while driving after a shift, grouped by shift pattern.'],
              [('Fixed day shift', (6, 14), (90, 120)), ('Fixed night shift', (14, 24), (70, 95)), ('Rotating shifts', (22, 36), (65, 90))],
              ('yes', 'no', 'nurses'))

c19c = T('Health and safety: accidents, error and safety promotion', 'health safety accidents error safety promotion')
build(c19c, {
    'terms': [
        ('slip', 'in Reason’s classification, an error in carrying out a correct plan, such as pressing the wrong button'),
        ('lapse', 'in Reason’s classification, a memory failure, such as forgetting a step'),
        ('mistake', 'in Reason’s classification, an error in planning, where the intended action itself is wrong'),
        ('violation', 'a deliberate departure from safe procedures or rules'),
        ('Swiss cheese model', 'Reason’s model in which accidents happen when holes (weaknesses) in several layers of defence line up'),
        ('safety culture', 'shared attitudes, values and practices in an organisation that put safety first'),
    ],
    'foils': ['Hawthorne effect', 'forward rotation'],
    'mcq': [
        ('According to Reason, an error in which a nurse intends to give the correct drug but picks up the wrong bottle is a', 'slip', ['mistake', 'violation', 'lapse'], 'Correct plan, wrong action.'),
        ('Reason’s “Theory B” of accidents blames', 'the system and organisation', ['only the individual operator', 'chance', 'the victim'], 'Theory A = person, Theory B = system.'),
        ('Fox et al. (1987) improved safety in open-pit mines using', 'a token economy with stamps for injury-free periods', ['fear-arousing posters', 'longer shifts', 'open-plan offices'], 'Trading stamps rewarded safe work.'),
        ('Forgetting to switch off a machine before cleaning it is a', 'lapse', ['violation', 'mistake', 'slip'], 'Memory failure.'),
    ],
    'ar': [
        ('Reason argues that blaming individuals does not prevent accidents.', 'Accidents usually result from weaknesses in several layers of an organisation’s defences.', 'AR', 'Swiss cheese / Theory B.'),
    ],
    'explain': [
        ('Explain Reason’s Swiss cheese model of accidents.', 'Organisations have several layers of defence (procedures, training, equipment, supervision); each has weaknesses (holes) caused by active failures and latent conditions; an accident happens when holes in all layers line up.', '1 mark layers; 1 mark holes; 1 mark line up [3]'),
        ('Describe the findings of Fox et al. (1987).', 'At two open-pit mines, workers earned trading stamps for periods without lost-time injuries and for safety suggestions; days lost through injury and the cost of accidents fell substantially and stayed low for years.', '1 mark procedure; 1 mark findings [2]'),
    ],
    'claims': [
        ('Reason’s classification treats all unsafe acts as deliberate.', False, 'Slips, lapses and mistakes are unintentional; only violations are deliberate.'),
        ('A token economy can be used to promote workplace safety.', True, 'Fox et al. (1987) rewarded injury-free periods with stamps.'),
    ],
    'who': 'Fox et al.’s (1987) token economy for safety in mines',
    'evals': [
        ('ecological validity', 'strength', 'It was carried out in real mines over many years with real injury records.'),
        ('usefulness', 'strength', 'Large reductions in injuries and costs show that behavioural safety programmes can work.'),
        ('reporting bias', 'weakness', 'Workers may have hidden minor injuries to keep their stamps.'),
        ('controls', 'weakness', 'With no control mine, other changes such as new equipment might explain the improvement.'),
    ],
    'apply': [
        ('In a chemical plant in {city}, an operator opened the wrong valve during a busy shift. The investigation found that the two valves look identical, training was short, and the alarm had been switched off because of false alarms.',
         [('Classify the operator’s error using Reason’s categories.', 'A slip (correct intention, wrong action).', '1 mark [1]'),
          ('Using the Swiss cheese model, explain why this accident happened.', 'Several layers had holes – identical valves (design), short training, disabled alarm – and these lined up with the operator’s slip.', '1 mark identifies layers; 1 mark line up [2]'),
          ('Suggest two ways to prevent a similar accident.', 'Colour-code or label valves differently, improve training, fix the alarm, and introduce a reward scheme for safe behaviour.', '1 mark each [2]')]),
    ],
})
chapter(19, [c19a, c19b, c19c], WC_SHARED)

# ============================================================== ORGANISATIONAL 20: Satisfaction at work

SAT_SHARED = {
    'essays': [
        ('job design is the most effective way of increasing job satisfaction',
         ['Hackman and Oldham’s job characteristics model links skill variety, autonomy and feedback to satisfaction and motivation.', 'Job enrichment gives motivators (Herzberg) such as responsibility and achievement.'],
         ['Some employees do not want enriched jobs (low growth-need strength).', 'Pay, relationships and leadership also affect satisfaction.', 'Job rotation may just swap one boring task for another.'],
         ['individual differences', 'usefulness', 'validity of evidence']),
        ('questionnaires are the best way to measure job satisfaction',
         ['Standardised scales such as the JDI and MSQ give quantitative, comparable data from many employees.', 'They can measure different facets of satisfaction.'],
         ['Employees may give socially desirable answers if they fear managers will see them.', 'Fixed questions miss the reasons for dissatisfaction, which interviews can reveal.', 'Behavioural measures such as absence and turnover may be more objective.'],
         ['reliability', 'validity', 'social desirability']),
    ],
    'exp': [dict(intro=['A company in {city} enriched the jobs of {n} assembly workers (giving them responsibility for a whole product and quality checks) and compared their satisfaction scores (out of 50) with {n} workers on the unchanged assembly line.',
                        '{person} compared job satisfaction scores (out of 50) for {n} employees whose jobs had been enriched and {n} whose jobs had not.'],
                 A='enriched', B='unchanged', gA='workers with enriched jobs', gB='workers with unchanged jobs',
                 more='will have higher job satisfaction scores than', measure='job satisfaction score', dvshort='Job satisfaction score (out of 50)',
                 iv='whether the job had been enriched', dv='the total score on a 10-item job satisfaction questionnaire (each item 1–5)',
                 range=(10, 50), base=(28, 32), diff=(3, 7), sd=4, nosample=True,
                 controls=['similar products and pay in both groups', 'the same questionnaire given at the same time'],
                 ethics=['answers should be anonymous so employees are not afraid to criticise managers', 'workers with unchanged jobs should be offered enrichment later if it helps'],
                 concl_A='job enrichment increases job satisfaction.', concl_B='unchanged jobs lead to higher satisfaction than enriched jobs.')],
    'corr': [dict(intro=['{person} collected job satisfaction scores and the number of days absent in the last year for {n} employees at a company in {city}.',
                         'A study in {city} recorded job satisfaction (questionnaire score) and days of absence over a year for {n} office workers.'],
                  x='job satisfaction score', y='days absent in the past year', xs='satisfaction score', ys='days absent', xr=(10, 50), yr=(0, 20), sign=-1,
                  third=['health problems', 'family responsibilities', 'the quality of the relationship with the manager'])],
    'plan': [('whether job rotation increases satisfaction among supermarket staff', 'IV: job rotation or fixed role', 'DV: job satisfaction score', ['field experiment']),
             ('whether organisational commitment is related to absenteeism', 'co-variable 1: commitment score', 'co-variable 2: days absent', ['correlation', 'questionnaire'])],
    'plan_lead': 'Design',
}

c20a = T('Theories of job satisfaction and job design: job enrichment, rotation', 'theories job satisfaction job design job enrichment rotation')
build(c20a, {
    'terms': [
        ('two-factor theory', 'Herzberg’s theory that hygiene factors prevent dissatisfaction while motivators produce satisfaction'),
        ('hygiene factors', 'in Herzberg’s theory, features of the job context such as pay, working conditions and supervision that cause dissatisfaction if poor'),
        ('motivators', 'in Herzberg’s theory, features of the job content such as achievement, recognition and responsibility that cause satisfaction'),
        ('job enrichment', 'redesigning a job to give more responsibility, autonomy and control (vertical loading)'),
        ('job enlargement', 'adding more tasks at the same level of responsibility (horizontal loading)'),
        ('job rotation', 'moving employees between different tasks or jobs at regular intervals'),
        ('job characteristics model', 'Hackman and Oldham’s model linking five core job characteristics to psychological states and work outcomes'),
    ],
    'mcq': [
        ('In Herzberg’s two-factor theory, which is a motivator?', 'Recognition', ['Salary', 'Company policy', 'Working conditions'], 'The others are hygiene factors.'),
        ('Which is NOT one of Hackman and Oldham’s core job characteristics?', 'Pay level', ['Skill variety', 'Autonomy', 'Feedback'], 'The five: skill variety, task identity, task significance, autonomy, feedback.'),
        ('Giving an employee responsibility for planning and checking their own work is', 'job enrichment', ['job enlargement', 'job rotation', 'a hygiene factor'], 'Vertical loading.'),
        ('Herzberg developed his theory by', 'interviewing engineers and accountants about times they felt good or bad about their jobs', ['giving the JDI to factory workers', 'observing managers in business games', 'measuring productivity under different lighting'], 'Critical incident technique.'),
    ],
    'ar': [
        ('In Herzberg’s theory, improving pay may not increase motivation.', 'Pay is a hygiene factor.', 'AR', 'Hygiene factors only prevent dissatisfaction.'),
        ('Job rotation always increases job satisfaction.', 'Job rotation moves employees between tasks.', 'R', 'Rotating between equally boring tasks may not help, so the assertion is false.'),
    ],
    'explain': [
        ('Explain the difference between hygiene factors and motivators.', 'Hygiene factors (pay, conditions, supervision, policy) are about the job context: when poor they cause dissatisfaction, but improving them only removes dissatisfaction. Motivators (achievement, recognition, responsibility, the work itself, advancement) are about job content and produce satisfaction and motivation.', '1 mark hygiene; 1 mark motivators; 1 mark difference in effect [3]'),
        ('Explain the difference between job enrichment and job enlargement.', 'Enrichment adds responsibility and control (vertical loading), such as planning and checking work; enlargement adds more tasks of the same level (horizontal loading).', '1 mark each [2]'),
    ],
    'claims': [
        ('Herzberg argued that satisfaction and dissatisfaction are opposite ends of one scale.', False, 'He argued they are separate dimensions caused by different factors.'),
        ('In Hackman and Oldham’s model, autonomy leads to experienced responsibility for outcomes.', True, 'Autonomy → responsibility; feedback → knowledge of results.'),
    ],
    'who': 'Herzberg’s two-factor theory of job satisfaction',
    'evals': [
        ('usefulness', 'strength', 'It led to job enrichment programmes that give employees more responsibility and recognition.'),
        ('research base', 'strength', 'It was based on detailed accounts of real experiences at work using the critical incident technique.'),
        ('self-serving bias', 'weakness', 'People tend to credit themselves for good events and blame the context for bad events, which may explain the two factors.'),
        ('generalisability', 'weakness', 'The original sample was about 200 engineers and accountants, so it may not apply to manual or low-paid workers.'),
    ],
    'apply': [
        ('Workers in a clothing factory in {city} each sew one seam on hundreds of shirts per day. Absence and staff turnover are high.',
         [('Using Hackman and Oldham’s model, identify two core job characteristics that are low in this job.', 'Skill variety and task identity (also autonomy).', '1 mark each [2]'),
          ('Suggest how job enrichment could be used.', 'Give small teams responsibility for whole shirts, including planning and quality checks.', '1 mark responsibility; 1 mark whole task [2]'),
          ('Explain why job rotation alone might not solve the problem.', 'Moving between equally simple, repetitive tasks adds variety but not responsibility or meaning.', '1 mark [1]')]),
    ],
})


def _mps(r, D):
    d = ctx(r)
    jobs = r.sample([('a call-centre operator', 'call-centre operator'), ('a hospital porter', 'porter'), ('a graphic designer', 'designer'), ('a warehouse picker', 'picker'),
                     ('a bank cashier', 'cashier'), ('a laboratory technician', 'technician'), ('a bus driver', 'driver')], 2)
    vals = []
    for name, short in jobs:
        sv, ti, ts, a, f = [r.randint(1, 7) for _ in range(5)]
        mps = (sv + ti + ts) / 3 * a * f
        vals.append((name, short, sv, ti, ts, a, f, mps))
    if abs(vals[0][7] - vals[1][7]) < 1:
        return None
    intro = (f'{d["person"]}, an occupational psychologist in {d["city"]}, used the Job Diagnostic Survey (scores 1–7) to rate two jobs. ' +
             ' '.join(f'For {n}: skill variety {sv}, task identity {ti}, task significance {ts}, autonomy {a}, feedback {f}.' for n, _, sv, ti, ts, a, f, _m in vals) +
             ' Motivating potential score (MPS) = ((skill variety + task identity + task significance) ÷ 3) × autonomy × feedback.')
    n0, _, sv, ti, ts, a, f, m0 = vals[0]
    n1, _, sv1, ti1, ts1, a1, f1, m1 = vals[1]
    hi, lo = (vals[0], vals[1]) if m0 > m1 else (vals[1], vals[0])
    weak = min([('skill variety', lo[2]), ('task identity', lo[3]), ('task significance', lo[4]), ('autonomy', lo[5]), ('feedback', lo[6])], key=lambda x: x[1])
    parts = [
        (f'Calculate the MPS for {n0}. Give your answer to one decimal place.', f'{d1(m0)}', f'(({sv} + {ti} + {ts}) ÷ 3) × {a} × {f} = {d2((sv + ti + ts) / 3)} × {a * f} = {d1(m0)}. 1 mark mean of first three; 1 mark answer [2]'),
        (f'Calculate the MPS for {n1} and state which job has the higher motivating potential.', f'{d1(m1)}; {hi[0]}', f'(({sv1} + {ti1} + {ts1}) ÷ 3) × {a1} × {f1} = {d1(m1)}. 1 mark MPS; 1 mark comparison [2]'),
        (f'Explain why autonomy and feedback have a larger effect on MPS than skill variety.', 'Skill variety is averaged with task identity and significance, whereas autonomy and feedback are multipliers, so a low score on either greatly reduces MPS (a score of 1 makes MPS very low).', '1 mark averaged vs multiplied; 1 mark consequence [2]'),
        (f'Suggest one way to redesign the job of {lo[1]} to increase its MPS.',
         {'skill variety': 'Add a wider range of tasks that use different skills', 'task identity': 'Let the employee complete a whole, identifiable piece of work from start to finish',
          'task significance': 'Show the employee how the work affects other people, for example customer feedback', 'autonomy': 'Allow the employee to plan and schedule their own work and decide how to do it',
          'feedback': 'Give regular information on performance, for example daily results or quality checks'}[weak[0]] + f' (its lowest characteristic is {weak[0]}, {weak[1]}).',
         '1 mark identifies a low characteristic; 1 mark suitable redesign [2]'),
        ('Explain one weakness of measuring job characteristics with the Job Diagnostic Survey.', 'It is self-report, so ratings may reflect how satisfied the employee already is (common-method bias) rather than objective features of the job.', '1 mark self-report; 1 mark explained [2]'),
    ]
    m = (f'What is the MPS for {n0}, to one decimal place?', f'{d1(m0)}', [f'{d1((sv + ti + ts) * a * f)}', f'{d1((sv + ti + ts + a + f) / 5)}', f'{d1((sv + ti + ts) / 3 + a * f)}', f'{d1((sv + ti + ts) / 3 * (a + f))}'], f'(({sv} + {ti} + {ts}) ÷ 3) × {a} × {f} = {d1(m0)} [1]')
    return intro, parts, m


score_tpl(c20a, 'mps', _mps)

c20b = T('Measuring job satisfaction: questionnaires and rating scales', 'measuring job satisfaction questionnaires rating scales')
build(c20b, {
    'terms': [
        ('Job Descriptive Index (JDI)', 'a questionnaire by Smith, Kendall and Hulin measuring satisfaction with five facets: the work itself, pay, promotion, supervision and co-workers'),
        ('Minnesota Satisfaction Questionnaire (MSQ)', 'a questionnaire by Weiss et al. measuring satisfaction with 20 facets of work, in a long (100-item) or short (20-item) form'),
        ('faces scale', 'Kunin’s rating scale on which employees choose the face that best shows how they feel about their job'),
        ('Likert scale', 'a rating scale on which respondents show how much they agree with a statement, for example from 1 (strongly disagree) to 5 (strongly agree)'),
        ('reverse scoring', 'scoring negatively worded items the opposite way round so that a high total always means the same thing'),
        ('facet satisfaction', 'satisfaction with a particular aspect of a job, such as pay or supervision'),
    ],
    'mcq': [
        ('Which of these is NOT one of the five facets measured by the JDI?', 'Working hours', ['Pay', 'Supervision', 'Co-workers'], 'Work itself, pay, promotion, supervision, co-workers.'),
        ('The short form of the Minnesota Satisfaction Questionnaire has', '20 items', ['5 items', '50 items', '100 items'], 'Long form 100 items.'),
        ('Why are some questionnaire items worded negatively?', 'To reduce response bias such as always agreeing', ['To make the questionnaire longer', 'To increase social desirability', 'To make scoring easier'], 'Acquiescence bias.'),
        ('Kunin’s faces scale is especially useful because it', 'is quick and can be used by people with limited reading ability', ['gives detailed qualitative data', 'measures 20 facets', 'is completed by managers'], 'Simple pictorial scale.'),
    ],
    'ar': [
        ('Job satisfaction questionnaires may be affected by social desirability.', 'Employees may fear that their managers will see their answers.', 'AR', 'Anonymity helps.'),
    ],
    'explain': [
        ('Explain one strength and one weakness of using rating scales to measure job satisfaction.', 'Strength: quantitative scores are easy to compare between employees and over time, and the scale can be standardised. Weakness: fixed responses do not explain why employees feel as they do, and answers may be socially desirable.', '1 mark each point, 1 mark each explanation [4]'),
        ('Describe the Job Descriptive Index.', 'Developed by Smith, Kendall and Hulin (1969), it lists adjectives or short phrases for five facets of the job (work itself, pay, promotion, supervision, co-workers); employees answer yes, no or ? (cannot decide) for each.', '1 mark facets; 1 mark response format [2]'),
    ],
    'claims': [
        ('A single overall rating of job satisfaction tells managers exactly which aspect of the job needs improving.', False, 'Facet measures such as the JDI or MSQ are needed to identify the problem area.'),
        ('Anonymous questionnaires are likely to give more valid answers about satisfaction.', True, 'Employees are less afraid of consequences, reducing social desirability.'),
    ],
    'who': 'the use of questionnaires (such as the JDI and MSQ) to measure job satisfaction',
    'evals': [
        ('reliability', 'strength', 'Standardised items and scoring mean results can be compared across organisations and over time.'),
        ('practicality', 'strength', 'Questionnaires can be given to large numbers of employees quickly and cheaply.'),
        ('social desirability', 'weakness', 'Employees may hide dissatisfaction if they think managers will see their answers.'),
        ('depth', 'weakness', 'Closed questions give little detail about the reasons for dissatisfaction.'),
    ],
    'apply': [
        ('A hotel chain in {city} wants to find out why staff turnover is high. The manager plans to ask staff one question: “Are you happy at work? Yes/No.”',
         [('Explain two problems with this question.', 'It gives no information about which aspects of work cause dissatisfaction, and a yes/no answer cannot show degrees of satisfaction.', '1 mark each [2]'),
          ('Suggest a better way to measure job satisfaction and explain why.', 'Use an anonymous standardised facet questionnaire such as the JDI or short-form MSQ with rating scales, which shows the level of satisfaction with each aspect.', '1 mark method; 1 mark reason [2]'),
          ('Suggest how qualitative data could also be collected.', 'Exit interviews or an open question asking staff what they would change.', '1 mark [1]')]),
    ],
})


def _likert(r, D):
    d = ctx(r)
    pool = [('I find my work interesting.', False), ('My pay is fair for the work I do.', False), ('My supervisor supports me.', False), ('I get on well with my colleagues.', False),
            ('I have good chances of promotion.', False), ('I often feel bored at work.', True), ('I would leave this job if I could.', True), ('My work is not appreciated.', True)]
    n = 5 if D <= 3 else 6
    its = r.sample(pool[:5], n - 2) + r.sample(pool[5:], 2)
    r.shuffle(its)
    resp = [r.randint(1, 5) for _ in its]
    scored = [6 - x if neg else x for (s, neg), x in zip(its, resp)]
    tot = sum(scored)
    raw = sum(resp)
    mean = tot / n
    lines = ' '.join(f'({i + 1}) “{s}” – {x}.' for i, ((s, _), x) in enumerate(zip(its, resp)))
    negs = [str(i + 1) for i, (s, neg) in enumerate(its) if neg]
    intro = (f'{d["person"]}, an employee in {d["city"]}, completed a job satisfaction questionnaire. Each item was rated from 1 (strongly disagree) to 5 (strongly agree). '
             f'Responses: {lines} Negatively worded items are reverse-scored (1 = 5, 2 = 4, 3 = 3, 4 = 2, 5 = 1).')
    parts = [
        ('Identify the items that must be reverse-scored.', f'Items {negs[0]} and {negs[1]}', '1 mark both items [1]'),
        ('Calculate the total job satisfaction score after reverse scoring.', str(tot), f'Scored values: {", ".join(map(str, scored))}; total = {tot}. 1 mark reverse scoring; 1 mark total [2]'),
        ('Calculate the mean item score, to two decimal places.', f'{d2(mean)}', f'{tot} ÷ {n} = {d2(mean)}. 1 mark [1]'),
        ('Explain why negatively worded items are included and reverse-scored.', 'They reduce response bias (agreeing with everything) and reverse scoring makes a high score always mean high satisfaction.', '1 mark response bias; 1 mark consistent direction [2]'),
        ('Explain one reason why this score may not be a valid measure of the employee’s satisfaction.', 'The employee may give socially desirable answers if not anonymous, or the few items may not cover all facets of the job.', '1 mark reason; 1 mark explained [2]'),
    ]
    m = ('What is the total satisfaction score after reverse scoring?', str(tot), [str(raw), str(tot + 2), str(tot - 2), str(n * 5 - tot)], f'Reverse-score items {negs[0]} and {negs[1]}; total = {tot} [1]')
    return intro, parts, m


score_tpl(c20b, 'likert', _likert)

c20c = T('Attitudes to work: absenteeism, organisational commitment and sabotage', 'attitudes work absenteeism organisational commitment sabotage')
build(c20c, {
    'terms': [
        ('absenteeism', 'failing to attend work when scheduled, especially when it is voluntary or avoidable'),
        ('voluntary absence', 'absence that the employee chooses, for example taking a day off when not ill'),
        ('organisational commitment', 'the psychological attachment of an employee to the organisation'),
        ('affective commitment', 'in Meyer and Allen’s model, staying with an organisation because one wants to (emotional attachment)'),
        ('continuance commitment', 'in Meyer and Allen’s model, staying with an organisation because leaving would be too costly'),
        ('normative commitment', 'in Meyer and Allen’s model, staying with an organisation because one feels obliged to'),
        ('sabotage', 'deliberate behaviour intended to damage or disrupt an organisation’s products, property, reputation or operations'),
    ],
    'mcq': [
        ('An employee stays in a job only because they would lose their pension if they left. This is', 'continuance commitment', ['affective commitment', 'normative commitment', 'voluntary absence'], 'Cost of leaving.'),
        ('Meyer and Allen’s model of organisational commitment has', 'three components', ['two factors', 'five facets', 'four stages'], 'Affective, continuance, normative.'),
        ('Giacalone and Rosenfeld (1987) studied', 'the justifications employees gave for sabotage', ['shift-work rotation', 'fear arousal in health campaigns', 'the effect of open-plan offices'], 'Employees rated reasons for sabotage.'),
        ('The Bradford factor gives more weight to', 'many short absences than a few long absences', ['a few long absences than many short ones', 'absences on Fridays only', 'authorised holidays'], 'S² × D.'),
    ],
    'ar': [
        ('Frequent short absences are seen as more disruptive than one long absence.', 'The Bradford factor squares the number of spells of absence.', 'AR', 'S² × D penalises frequency.'),
    ],
    'explain': [
        ('Explain the three components of Meyer and Allen’s model of organisational commitment.', 'Affective: wanting to stay because of emotional attachment; continuance: needing to stay because leaving is costly (pay, pension, few alternatives); normative: feeling obliged to stay because of loyalty or a sense of duty.', '1 mark each component [3]'),
        ('Explain two reasons why employees may commit sabotage.', 'To get revenge for perceived unfair treatment; to protest or gain control over their work; to make work easier or relieve boredom; to protect themselves or others.', '1 mark each reason, 1 mark each explanation [4]'),
    ],
    'claims': [
        ('All absence from work shows low job satisfaction.', False, 'Much absence is involuntary (illness, family emergencies); only voluntary absence is clearly linked to attitudes.'),
        ('Employees with high affective commitment are less likely to leave the organisation.', True, 'Affective commitment is negatively related to turnover.'),
    ],
    'who': 'Meyer and Allen’s three-component model of organisational commitment',
    'evals': [
        ('usefulness', 'strength', 'It helps organisations see that employees may stay for different reasons and target affective commitment, which predicts performance best.'),
        ('measurement', 'strength', 'Each component can be measured with standardised questionnaire scales.'),
        ('overlap', 'weakness', 'Affective and normative commitment are highly correlated, so they may not be separate components.'),
        ('cultural bias', 'weakness', 'The model was developed in Western organisations and may work differently in collectivist cultures.'),
    ],
    'apply': [
        ('{person} has worked at a bank in {city} for 15 years. She dislikes her job but says she cannot leave because she would lose her pension. Her absence record shows many single days off on Mondays.',
         [('Identify {person}’s type of organisational commitment.', 'Continuance commitment.', '1 mark [1]'),
          ('Explain what the pattern of absence suggests.', 'Many short Monday absences suggest voluntary absence linked to low job satisfaction rather than illness.', '1 mark voluntary; 1 mark link to attitude [2]'),
          ('Suggest how the bank could increase {person}’s affective commitment.', 'Give her more interesting responsibilities, recognition and involvement in decisions.', '1 mark action; 1 mark link to affective commitment [2]')]),
    ],
})


def _absence(r, D):
    d = ctx(r)
    names = r.sample(['A', 'B', 'C', 'D'], 2)
    recs = []
    for nm in names:
        s = r.randint(1, 8)
        days = r.randint(s, s * r.choice([1, 2, 3, 4]) + 2)
        recs.append((nm, s, days, s * s * days))
    if recs[0][3] == recs[1][3]:
        return None
    staff = r.choice([20, 25, 40, 50, 80])
    wdays = r.choice([220, 230, 240, 250])
    lost = r.randint(int(staff * wdays * 0.02), int(staff * wdays * 0.07))
    rate = 100 * lost / (staff * wdays)
    intro = (f'A company in {d["city"]} with {staff} employees, each scheduled to work {wdays} days a year, recorded {lost} days lost to absence last year. '
             + ' '.join(f'Employee {nm} had {s} separate spell{"s" if s > 1 else ""} of absence totalling {dd} days.' for nm, s, dd, _ in recs)
             + ' The Bradford factor = S² × D, where S is the number of spells and D the total days absent.')
    hi = max(recs, key=lambda x: x[3])
    a, b = recs
    parts = [
        ('Calculate the lost-time rate (percentage of scheduled working days lost to absence). Give your answer to one decimal place.', f'{d1(rate)}%', f'{lost} ÷ ({staff} × {wdays}) × 100 = {lost} ÷ {staff * wdays} × 100 = {d1(rate)}%. 1 mark scheduled days; 1 mark answer [2]'),
        (f'Calculate the Bradford factor for employee {a[0]} and for employee {b[0]}.', f'{a[0]}: {a[3]}; {b[0]}: {b[3]}', f'{a[1]}² × {a[2]} = {a[3]}; {b[1]}² × {b[2]} = {b[3]}. 1 mark each [2]'),
        ('Explain why the Bradford factor may be more useful than total days absent for managers.', 'Frequent short absences are more disruptive and more likely to be voluntary, and the Bradford factor gives them more weight by squaring the number of spells.', '1 mark disruption/voluntary; 1 mark squaring [2]'),
        (f'Explain one ethical or practical problem with using the Bradford factor to discipline employee {hi[0]}.', 'It does not distinguish between voluntary absence and genuine illness or disability, so an employee with a chronic condition could be treated unfairly.', '1 mark problem; 1 mark explained [2]'),
    ]
    m = (f'What is the Bradford factor for employee {a[0]}?', str(a[3]), [str(a[1] * a[2]), str(a[1] * a[2] * a[2]), str(a[1] * a[1] + a[2]), str(a[3] + a[2])], f'{a[1]}² × {a[2]} = {a[3]} [1]')
    return intro, parts, m


score_tpl(c20c, 'absence', _absence)
chapter(20, [c20a, c20b, c20c], SAT_SHARED)
