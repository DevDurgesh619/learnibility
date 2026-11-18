"""CBSE class 12 Psychology: curated 'distinguish between' pairs and original case vignettes (Section F style).

extra(chapters) returns {subtopic id: [families]} for g12_hum_engine.families(..., extra).
Each vignette is (text, concept, explanation, kind label); vignettes are original and short.
"""
import qbank
import g12_hum_engine as E

PAIRS = {
    '01-st1': [('psychological test', 'case study')],
    '01-st2': [('two-factor theory', 'primary mental abilities'), ('multiple intelligences', 'triarchic theory'),
               ('structure-of-intellect model', 'PASS model')],
    '01-st3': [('mental age', 'intelligence quotient'), ('intellectual disability', 'giftedness')],
    '01-st4': [('emotional intelligence', 'creativity'), ('emotional quotient', 'intelligence quotient')],
    '02-st1': [('self-esteem', 'self-efficacy'), ('self-efficacy', 'self-regulation')],
    '02-st2': [('type approach', 'trait approach'), ('Big Five factors', 'source traits')],
    '02-st3': [('id', 'ego'), ('ego', 'superego'), ('self-actualisation', 'fully functioning person')],
    '02-st4': [('self-report measures', 'projective techniques'), ('social desirability', 'acquiescence')],
    '03-st1': [('stressor', 'stress'), ('primary appraisal', 'secondary appraisal')],
    '03-st2': [('burnout', 'eustress')],
    '03-st3': [('task-oriented strategy', 'emotion-oriented strategy'), ('emotion-oriented strategy', 'avoidance-oriented strategy'),
               ('biofeedback', 'stress inoculation training')],
    '03-st4': [('resilience', 'hardiness')],
    '04-st1': [('DSM-5', 'ICD'), ('supernatural approach', 'biological approach')],
    '04-st2': [('biological model', 'socio-cultural model'), ('diathesis-stress model', 'biological model')],
    '04-st3': [('anxiety', 'phobia'), ('somatic symptom disorder', 'dissociative identity disorder')],
    '04-st4': [('major depressive disorder', 'bipolar disorder'), ('schizophrenia', 'bipolar disorder')],
    '05-st1': [('empathy', 'unconditional positive regard')],
    '05-st2': [('transference', 'resistance'), ('free association', 'interpretation'),
               ('rational emotive therapy', 'cognitive therapy'), ('token economy', 'systematic desensitisation')],
    '05-st3': [('logotherapy', 'client-centred therapy'), ('client-centred therapy', 'Gestalt therapy'),
               ('Sudarshan Kriya Yoga', 'vipasana meditation')],
    '05-st4': [('occupational therapy', 'vocational training'), ('social skills training', 'cognitive retraining')],
    '06-st1': [('affective component', 'cognitive component'), ('valence', 'extremeness'),
               ('cognitive component', 'behavioural component')],
    '06-st2': [('balance theory', 'cognitive dissonance'), ('association', 'learning through modelling')],
    '06-st3': [('stereotype', 'prejudice'), ('kernel of truth', 'self-fulfilling prophecy')],
    '06-st4': [('schema', 'prototype'), ('primacy effect', 'halo effect'), ('social facilitation', 'social loafing')],
    '07-st1': [('ingroup', 'outgroup'), ('roles', 'norms'), ('status', 'cohesiveness')],
    '07-st2': [('group polarisation', 'groupthink'), ('diffusion of responsibility', 'bandwagon effect')],
    '07-st3': [('conformity', 'compliance'), ('foot-in-the-door technique', 'deadline technique'),
               ('informational influence', 'normative influence')],
    '07-st4': [('superordinate goal', 'realistic conflict')],
}

VIG = {
    '01-st1': [
        ("Rhea scores very high on a test of mechanical reasoning even though she has never repaired a machine. Her counsellor says she could learn engineering skills quickly with training.",
         'aptitude', "aptitude is the underlying potential to acquire skills with training, not the skill itself", 'psychological attribute'),
        ("Before a new job, a company psychologist spends weeks studying one applicant's school records, family background, interviews and test results to understand him fully.",
         'case study', "a case study is an in-depth study of one individual's history, context and psychological attributes", 'method of assessment'),
        ("Kabir is loud and playful with his friends, but at his grandfather's prayer meeting he sits quietly and speaks softly.",
         'situationism', "situationism holds that situations influence behaviour, so the same person behaves differently in different settings", 'concept'),
    ],
    '01-st2': [
        ("A psychologist says that Meera's good marks in languages, mathematics and science all come from one common mental ability, plus a few specific abilities for each subject.",
         "Spearman's two-factor theory", "it explains intelligence as a general factor (g) together with specific factors (s)", 'theory of intelligence'),
        ("Arjun is a weak reader but finds his way in any new city and can draw a map from memory. His teacher says intelligence comes in several independent kinds.",
         "Gardner's theory of multiple intelligences", "it holds that there are several distinct intelligences, and Arjun shows high spatial intelligence", 'theory of intelligence'),
        ("A street vendor with little schooling quickly adapts to changing customers, shapes his stall to suit the market and moves to better locations when needed.",
         "contextual (practical) intelligence in Sternberg's triarchic theory", "contextual intelligence is the ability to adapt to, shape or select one's environment", 'type of intelligence'),
    ],
    '01-st3': [
        ("An eight-year-old child correctly answers the test items that most ten-year-olds can answer.",
         'mental age above chronological age (IQ of 125)', "mental age is the level of performance typical of an age group; IQ = MA/CA × 100 = 10/8 × 100 = 125", 'concept'),
        ("A child of eleven needs help with daily self-care, scores below 70 on an intelligence test and has difficulty adapting to school routines.",
         'intellectual disability', "it involves significantly below-average intellectual functioning (IQ below 70) and deficits in adaptive behaviour, appearing before 18", 'condition'),
        ("A nine-year-old learns fast, asks unusual questions, prefers older companions and has an IQ well above 130.",
         'giftedness', "gifted children show exceptional general ability, often with an IQ above 130, along with high creativity and motivation", 'condition'),
    ],
    '01-st4': [
        ("Tanvi notices when a classmate is upset, controls her own anger during arguments and calms her team before matches.",
         'emotional intelligence', "it is the ability to perceive, understand, use and manage one's own and others' emotions", 'concept'),
        ("Asked to list uses of an old tyre, Samar suggests a swing, a planter, a sandal sole and a drum, giving many original ideas.",
         'creativity (divergent thinking)', "creativity is the ability to produce ideas that are novel and useful; many original uses show divergent thinking", 'concept'),
        ("A school gives Class 10 students a test of clerical speed and accuracy to predict who will do well in office work after training.",
         'aptitude test', "an aptitude test predicts how well a person can learn a skill with training", 'type of test'),
    ],
    '02-st1': [
        ("Nikhil believes that if he practises daily he can surely learn to swim, even though he cannot swim yet.",
         'self-efficacy', "self-efficacy is the belief that one can achieve a goal through one's own actions", 'aspect of self'),
        ("Priya waits to eat her favourite sweet until she finishes her homework, though she wants it right away.",
         'self-regulation (self-control)', "self-regulation is the ability to organise and monitor one's behaviour, including delaying gratification", 'aspect of self'),
        ("Raghav feels he is a worthwhile person, likes himself and is satisfied with how he does at school and sports.",
         'high self-esteem', "self-esteem is the value judgement one makes about oneself", 'aspect of self'),
    ],
    '02-st2': [
        ("Suresh is always in a hurry, impatient in queues, competitive and easily irritated by delays.",
         'Type-A personality', "Type-A persons show high motivation, impatience, time pressure and hostility, and are prone to heart disease", 'personality type'),
        ("A psychologist describes a student as high on openness and conscientiousness but low on neuroticism.",
         'Big Five factors', "the five-factor model describes personality by openness, conscientiousness, extraversion, agreeableness and neuroticism", 'approach to personality'),
        ("A teacher says some students are simply 'introverts' and others 'extraverts', placing each child in one broad category.",
         'type approach', "the type approach classifies people into broad categories based on observed behaviour patterns", 'approach to personality'),
    ],
    '02-st3': [
        ("Ankit failed to get into the cricket team and told everyone that he never really wanted to play.",
         'rationalisation', "rationalisation is a defence mechanism in which one gives acceptable reasons for unacceptable feelings or failure", 'defence mechanism'),
        ("After a scolding from her boss, Neha comes home and shouts at her younger brother.",
         'displacement', "displacement is a defence mechanism in which feelings are shifted to a less threatening target", 'defence mechanism'),
        ("Ramesh leaves a secure job to paint full time, saying he wants to become everything he is capable of becoming.",
         'self-actualisation', "in Maslow's humanistic view it is the need to realise one's full potential", 'concept'),
    ],
    '02-st4': [
        ("A student is shown an inkblot and asked to describe what she sees in it.",
         'projective technique (Rorschach inkblot test)', "projective techniques use ambiguous stimuli onto which a person projects unconscious feelings", 'assessment technique'),
        ("On a personality questionnaire, Varun answers 'yes' to almost every item regardless of what it asks.",
         'acquiescence', "acquiescence is a response bias in which a person agrees with items irrespective of content", 'problem in self-report'),
        ("Candidates applying for a job tick answers on a personality inventory that make them look honest and helpful, rather than what is true.",
         'social desirability', "it is the tendency to answer in a socially approved manner", 'problem in self-report'),
    ],
    '03-st1': [
        ("Before her board exam, Zoya feels excited and alert, and the pressure pushes her to study well.",
         'eustress', "eustress is a healthy, positive level of stress that improves performance", 'type of stress'),
        ("When told about a surprise test, Kunal first asks himself whether it is a threat to him, and then whether he has enough time and knowledge to cope.",
         'primary and secondary appraisal', "primary appraisal judges whether an event is harmful or a threat; secondary appraisal judges one's resources to cope", 'concept'),
        ("A man who has lost his job first feels shock, then struggles hard for months, and finally becomes exhausted and ill.",
         'general adaptation syndrome', "Selye's GAS has three stages: alarm reaction, resistance and exhaustion", 'model of stress'),
    ],
    '03-st2': [
        ("A nurse working long night shifts for years feels emotionally drained, detached from patients and no longer feels she achieves anything.",
         'burnout', "burnout is a state of physical, emotional and psychological exhaustion due to prolonged stress", 'effect of stress'),
        ("Students who were tense during exam week caught colds more often than in the vacation weeks.",
         'stress weakening the immune system', "psychoneuroimmunology shows that stress affects the immune system and makes people prone to illness", 'concept'),
        ("Over months of work pressure, Sunil eats irregularly, sleeps little, smokes more and skips exercise.",
         'unhealthy lifestyle due to stress', "stress leads to poor health behaviours such as poor diet, less sleep and smoking", 'effect of stress'),
    ],
    '03-st3': [
        ("When her laptop crashes before a deadline, Shreya lists her options, borrows a computer and redoes the work.",
         'task-oriented coping', "it involves obtaining information and taking direct action to change the stressful situation", 'coping strategy'),
        ("Before results day, Aman goes to the cinema and avoids any talk of the results.",
         'avoidance-oriented coping', "it involves denying or minimising the seriousness of the situation and keeping away from it", 'coping strategy'),
        ("A trainer teaches a nervous public speaker to replace negative self-talk with positive statements and to practise in steps.",
         'stress inoculation training', "Meichenbaum's method replaces negative thoughts with positive coping statements in three phases", 'stress management technique'),
    ],
    '03-st4': [
        ("After her house was damaged in floods, Leela rebuilt it, kept her children in school and stayed hopeful.",
         'resilience', "resilience is the ability to bounce back and recover from stressful situations", 'concept'),
        ("Sameer calmly tells his friend that he cannot lend his bike, without being rude or giving in.",
         'assertiveness', "assertiveness is the ability to express one's feelings and needs clearly and confidently", 'life skill'),
        ("A man facing a hard job sees it as a challenge, feels committed to his work and believes he can control the outcome.",
         'hardiness', "Kobasa's hardiness consists of commitment, control and challenge", 'personality characteristic'),
    ],
    '04-st1': [
        ("A woman's fear keeps her from leaving home, distresses her a lot and has made her quit her job.",
         'the four Ds (deviance, distress, dysfunction, danger) of abnormality', "abnormality is identified by deviance, distress, dysfunction and sometimes danger", 'criterion'),
        ("In a village, a man's strange behaviour is blamed on an evil spirit, and an exorcist is called.",
         'supernatural approach', "it explains abnormal behaviour as caused by evil spirits or magic", 'approach to abnormality'),
        ("A hospital records a patient's disorder using the classification system published by the World Health Organization.",
         'ICD (International Classification of Diseases)', "the ICD is the WHO's classification system for disorders", 'classification system'),
    ],
    '04-st2': [
        ("A doctor explains that a patient's depression may be linked to low levels of certain neurotransmitters in the brain.",
         'biological model', "it explains disorders through biochemical, genetic and brain-related causes", 'model'),
        ("Rohit inherited a tendency towards anxiety from his parents, but showed symptoms only after his business failed.",
         'diathesis-stress model', "a biological predisposition (diathesis) produces a disorder only when triggered by stress", 'model'),
        ("Researchers find that disorders are more common among people facing poverty, unemployment and discrimination.",
         'socio-cultural model', "it explains disorders through social and cultural factors such as poverty and prejudice", 'model'),
    ],
    '04-st3': [
        ("Divya is so afraid of lifts that she climbs ten floors daily, though she knows lifts are safe.",
         'specific phobia', "a phobia is an irrational fear of a specific object or situation", 'disorder'),
        ("Raj washes his hands dozens of times a day because he cannot stop thinking that they are dirty.",
         'obsessive-compulsive disorder', "obsessions are uncontrollable thoughts and compulsions are repeated acts to relieve the anxiety", 'disorder'),
        ("Months after a serious bus accident, Asha has nightmares and flashbacks and avoids all buses.",
         'post-traumatic stress disorder', "PTSD follows a traumatic event, with flashbacks, nightmares and avoidance", 'disorder'),
    ],
    '04-st4': [
        ("For weeks Karan has felt sad, lost interest in his hobbies, sleeps badly and feels worthless.",
         'major depressive disorder', "it involves persistent depressed mood or loss of interest with changes in sleep, appetite and energy", 'disorder'),
        ("A patient believes the neighbours are plotting to poison him and hears voices commenting on him.",
         'schizophrenia (delusions and hallucinations)', "schizophrenia includes positive symptoms such as delusions of persecution and hallucinations", 'disorder'),
        ("A seven-year-old cannot sit still, blurts out answers and loses track of tasks within minutes.",
         'attention-deficit hyperactivity disorder', "ADHD involves inattention and hyperactivity-impulsivity", 'disorder'),
    ],
    '05-st1': [
        ("A counsellor listens to a student and says, 'I can see how lonely you have felt since moving cities,' as if feeling it from the student's side.",
         'empathy', "empathy is understanding the client's experience from the client's point of view", 'quality of the therapeutic relationship'),
        ("A therapist accepts her client warmly even after he confesses to things he is ashamed of.",
         'unconditional positive regard', "it is accepting the client fully, without conditions or judgement", 'quality of the therapeutic relationship'),
        ("A client and a therapist agree on the number of sessions, the goals and the rules of their work together.",
         'therapeutic alliance', "it is the contractual, limited-duration relationship between client and therapist", 'concept'),
    ],
    '05-st2': [
        ("A therapist helps a child afraid of dogs to relax, then shows a dog picture, then a dog far away, then nearer, step by step.",
         'systematic desensitisation', "Wolpe's technique pairs relaxation with a graded hierarchy of feared stimuli", 'therapy technique'),
        ("In a hostel for children, residents earn stars for tidying beds, and the stars can be exchanged for a film night.",
         'token economy', "tokens given for desired behaviour are exchanged for rewards, increasing that behaviour", 'therapy technique'),
        ("A client who believes 'everyone must like me' is helped to see the belief as irrational and replace it with a realistic one.",
         'rational emotive therapy', "Ellis's therapy replaces irrational beliefs (B) that cause distressing consequences (C)", 'therapy'),
    ],
    '05-st3': [
        ("A man who lost his family in an earthquake is helped by a therapist to find a purpose in helping other survivors.",
         'logotherapy', "Frankl's logotherapy helps the client find meaning even in suffering", 'therapy'),
        ("A psychiatrist prescribes antidepressant medicines to a severely depressed patient.",
         'biomedical therapy', "biomedical therapy treats disorders with medicines or physical methods given by a psychiatrist", 'therapy'),
        ("Office workers learn a rapid breathing technique that reduces their anxiety and depression over a few weeks.",
         'Sudarshan Kriya Yoga', "SKY is a rapid breathing yoga technique found useful for stress, anxiety and depression", 'alternative therapy'),
    ],
    '05-st4': [
        ("During a session a woman weeps for the first time about her father's death and later feels lighter.",
         'catharsis', "catharsis is the release of pent-up emotions in therapy, which contributes to healing", 'healing factor'),
        ("Patients recovering from schizophrenia at a centre learn to make paper bags and candles each day.",
         'occupational therapy', "it teaches simple work skills that build work discipline in rehabilitation", 'form of rehabilitation'),
        ("Before therapy begins, the psychologist explains the method and its limits, and the client signs an agreement.",
         'informed consent', "it is an ethical standard in which the client agrees to therapy after understanding it", 'ethical standard'),
    ],
    '06-st1': [
        ("Sana believes plastic harms the earth, feels upset when she sees litter and carries a cloth bag to the market.",
         'the A-B-C components of attitude', "the belief is cognitive, the feeling is affective and carrying a cloth bag is behavioural", 'concept'),
        ("Raju strongly dislikes cricket and refuses to watch even a single match.",
         'negative valence and high extremeness', "valence tells that the attitude is negative; extremeness tells how strongly negative it is", 'features of attitude'),
        ("Vikram's belief in honesty shapes his attitudes towards work, friends, politics and money.",
         'centrality', "a central attitude has a strong influence on the other attitudes in the system", 'feature of attitude'),
    ],
    '06-st2': [
        ("Ira likes her friend Tara. Tara likes a new film, but Ira dislikes it. Ira feels uneasy and begins to like the film.",
         "Heider's balance theory", "in the P-O-X triangle two positive and one negative side is unbalanced, so one attitude changes", 'theory of attitude change'),
        ("A smoker reads that smoking causes cancer, feels uncomfortable and decides to quit.",
         "Festinger's cognitive dissonance", "two inconsistent cognitions create dissonance, which is reduced by changing one of them", 'theory of attitude change'),
        ("Children who admire a film star first identify with him, and when he starts promoting tree planting, they begin planting trees too.",
         "Mohsin's two-step concept", "the target first identifies with the source; when the source changes, the target imitates the change", 'theory of attitude change'),
    ],
    '06-st3': [
        ("A shop owner believes that people from a certain region are lazy and refuses to hire them.",
         'prejudice and discrimination', "the negative belief is a prejudice based on a stereotype; refusing jobs is discrimination", 'concept'),
        ("Children from two communities who disliked each other are placed in mixed teams for a school project and become friends.",
         'intergroup contact', "contact in a cooperative, equal-status setting reduces prejudice", 'strategy for handling prejudice'),
        ("Students told repeatedly that their group is 'bad at studies' stop trying and begin to score poorly.",
         'self-fulfilling prophecy', "the target of prejudice behaves in a way that confirms the negative belief", 'source of prejudice'),
    ],
    '06-st4': [
        ("When a new classmate fails a test, students say he is not intelligent, without considering that he was ill that week.",
         'fundamental attribution error', "it is the tendency to overweight internal causes when explaining others' behaviour", 'attributional bias'),
        ("A cyclist rides faster when racing alongside others than when riding alone against the clock.",
         'social facilitation', "the presence of others improves performance on well-learnt tasks (Triplett)", 'concept'),
        ("Because the new teacher smiled and was well dressed, students assumed she was also kind and fair.",
         'halo effect', "one positive trait leads to the assumption of other positive traits", 'effect in impression formation'),
    ],
    '07-st1': [
        ("A college debate club argues fiercely in its first weeks about who should lead, before settling down.",
         'storming stage of group formation', "in storming, members conflict over the task and leadership (Tuckman)", 'stage of group formation'),
        ("Students in a hostel always say 'we' about their own hostel and 'they' about the hostel across the road.",
         'ingroup and outgroup', "one's own group is the ingroup ('we'); others are outgroups ('they')", 'type of group'),
        ("People gathered at a road accident leave when the ambulance arrives; they had no shared goal or structure.",
         'crowd', "a crowd has no structure, norms or feeling of belongingness, unlike a group", 'collection of people'),
    ],
    '07-st2': [
        ("In a tug-of-war team of eight, each student pulls less hard than in a one-to-one contest.",
         'social loafing', "individual effort falls on a collective task because each feels less responsible", 'group influence'),
        ("A committee whose members mildly favoured a strike ends its discussion by calling for an indefinite strike.",
         'group polarisation', "group discussion makes the group's view more extreme in the direction it already favoured", 'group influence'),
        ("A close-knit board ignores warnings and approves a risky plan because no member wants to disturb the agreement.",
         'groupthink', "in cohesive isolated groups the wish for consensus overrides critical evaluation (Janis)", 'group influence'),
    ],
    '07-st3': [
        ("All of Rahul's friends wear a certain brand of shoes, so he buys them too though nobody asked him to.",
         'conformity', "conformity is behaving according to the group norm", 'form of social influence'),
        ("A volunteer first asks a resident to sign a petition and a week later asks her to donate money.",
         'foot-in-the-door technique', "a small first request makes compliance with a larger later request more likely", 'compliance technique'),
        ("A soldier follows his officer's order to march at night though he thinks it is unwise.",
         'obedience', "obedience is behaving in response to an order from an authority figure", 'form of social influence'),
    ],
    '07-st4': [
        ("Two rival villages stop fighting when they must work together to rebuild the only bridge connecting them to the town.",
         'superordinate goal', "a goal that benefits both groups and needs cooperation reduces intergroup conflict", 'conflict resolution strategy'),
        ("Two neighbouring states quarrel repeatedly over sharing the water of a river during drought years.",
         'intergroup conflict over scarce resources', "competition for limited resources makes each group see the other as a threat", 'concept'),
        ("Students of a school who each get a reward only if the whole class passes start helping each other.",
         'cooperation', "cooperation develops when rewards are shared and depend on joint effort", 'concept'),
    ],
}


def distinguish(chapters):
    out = {}
    for subs, _ in chapters:
        terms = {t: m for sb in subs for t, m in sb.T}
        for sb in subs:
            pairs = PAIRS.get(sb.sid.split('-ch')[-1], [])
            for a, b in pairs:
                assert a in terms and b in terms, (sb.sid, a, b)
            d = E.deck([((a, terms[a]), (b, terms[b])) for a, b in pairs])

            def gen(r, d=d):
                (a, ma), (b, mb) = d(r)
                ans = f"{E.cap(a)}: {E.end(ma)} {E.cap(b)}: {E.end(mb)}"
                return {'stem': f"Distinguish between '{a}' and '{b}'.", 'answer': ans,
                        'key': f"2 marks: 1 mark for explaining '{a}' ({E.end(ma)}) and 1 mark for '{b}' ({E.end(mb)}), "
                               f"with the contrast between them made clear.", 'marks': 2, 'minutes': 3}
            out.setdefault(sb.sid, []).append(qbank.F('C2', 'D2', 'explain', gen, marks=2, minutes=3))
    return out


def vignettes(chapters):
    out = {}
    for subs, _ in chapters:
        for sb in subs:
            vs = VIG[sb.sid.split('-ch')[-1]]
            d = E.deck(vs)

            def one(r, d=d):
                text, concept, expl, kind = d(r)
                return {'stem': f"Read the case and answer. {text} Identify the {kind} illustrated.",
                        'answer': E.cap(concept) + '.',
                        'key': f"1 mark: {concept}.", 'marks': 1, 'minutes': 2}

            def two(r, d=d):
                text, concept, expl, kind = d(r)
                return {'stem': f"Read the case and answer. {text} Name the {kind} shown here and explain it briefly.",
                        'answer': f"{E.cap(concept)}: {E.end(expl)}",
                        'key': f"2 marks: 1 mark for naming it ({concept}); 1 mark for the explanation ({expl}).",
                        'marks': 2, 'minutes': 4}
            out.setdefault(sb.sid, []).extend([
                qbank.F('C3', 'D3', 'case', one, marks=1, minutes=2, kinds=('case1',), gap='G7'),
                qbank.F('C4', 'D3', 'case', two, marks=2, minutes=4, kinds=('case2',), gap='G7')])
    return out


def extra(chapters):
    out = distinguish(chapters)
    for sid, fs in vignettes(chapters).items():
        out.setdefault(sid, []).extend(fs)
    return out
