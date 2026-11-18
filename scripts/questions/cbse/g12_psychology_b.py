"""CBSE class 12 Psychology (chapters 5-7): fact tables for g12_hum_engine."""
from g12_hum_engine import ST

S = 'cbse-g12-psychology-ch'

CH05 = [ST(S + '05-st1', 'nature and process of psychotherapy', """
T: psychotherapy | a voluntary relationship between the client and the therapist whose purpose is to help the client solve psychological problems
T: therapeutic relationship | the special relationship between the client and the therapist, built on trust, that is neither a passing acquaintance nor a permanent one
T: therapeutic alliance | the contractual and limited-duration bond between the therapist and the client in which both work towards the client's well-being
T: unconditional positive regard | the therapist's warmth and acceptance of the client irrespective of what the client says or does
T: empathy | the therapist's ability to understand the client's experiences as if they were the therapist's own
T: client | the person who seeks psychological help from a therapist
Q: The relationship between the therapist and the client is called the: | therapeutic alliance | transference | rapport only | contract of service
Q: Understanding the client's experiences as if they were one's own is called: | empathy | sympathy | intellectual understanding | positive regard
Q: Which of these is NOT a characteristic of psychotherapy? | The therapist may share personal relationships with the client outside therapy | Systematic application of principles of a theory | It is practised by trained persons | It involves a therapeutic relationship
Q: Accepting a client without conditions, whatever the client says, is called: | unconditional positive regard | empathy | catharsis | insight
Q: One goal of psychotherapy is to: | reinforce the client's resolve for betterment | make the client dependent on the therapist | label the client's disorder | replace the client's family
S+: Psychotherapy is a voluntary relationship between the one who seeks treatment and the one who treats
S+: All psychotherapies apply principles of a particular theory in a systematic way
S+: Psychotherapy is practised only by persons trained under supervision
S+: The therapeutic relationship is confidential and has a limited duration
S+: The therapeutic relationship is built on trust and requires empathy and unconditional positive regard from the therapist
S+: Psychotherapy aims at improving the client's self-awareness, decision making and acceptance of self
S-: Psychotherapy is an involuntary relationship imposed on the client | It is a voluntary relationship between the client and the therapist
S-: Sympathy and empathy mean the same in therapy | Empathy is understanding the client's experience from the client's point of view; sympathy is pity
S-: The therapeutic relationship continues for life | It is a contractual relationship of limited duration
C: The client must be able to trust the therapist | the client shares personal and painful experiences that must be kept confidential
C: Empathy is important in therapy | it lets the therapist understand the client's experience from the client's point of view
C: The therapist shows unconditional positive regard | warmth and acceptance help the client open up without fear of judgement
X: C2 D2 2 | Distinguish between empathy and sympathy. | Empathy – understanding the plight of another person as if it were one's own; sympathy – feeling pity or compassion for the person without understanding from their perspective.
X: C3 D3 2 | Why is confidentiality essential in the therapeutic relationship? | The client discloses personal and painful experiences; trust depends on information being kept private; it encourages honest sharing.
X: C3 D3 3 | State any three goals of psychotherapy. | Reinforcing the client's resolve for betterment; lessening emotional pressure; developing potential for positive growth; modifying habits; changing thinking patterns; increasing self-awareness; improving interpersonal relations and decision making.
X: C3 D4 4 | Explain the characteristics of psychotherapy. | Systematic application of a theory; practised by trained persons; voluntary therapeutic relationship; confidentiality; the therapist helps the client solve problems; the relationship is of limited duration.
X: C4 D4 4 | 'The therapeutic relationship is the heart of psychotherapy.' Explain. | Therapeutic alliance – contractual, limited duration; trust and confidentiality; empathy, unconditional positive regard and warmth; the client feels accepted and works towards change.
L: D4 | What is psychotherapy? Explain its characteristics, goals and the nature of the therapeutic relationship. | Voluntary relationship to solve psychological problems; systematic, trained therapist, confidential; goals – resolve for betterment, lessen emotional pressure, self-awareness, decision making; relationship – trust, empathy, unconditional positive regard, limited duration.
"""), ST(S + '05-st2', 'psychodynamic, behaviour and cognitive therapy', """
T: free association | the psychodynamic technique in which the client says whatever comes to mind without censoring it
T: transference | the client's unconscious attaching to the therapist of feelings once held towards significant figures in childhood
T: resistance | the client's unconscious opposition to the progress of therapy to protect the self from painful material
T: interpretation | the psychoanalyst's technique of pointing out unconscious material to the client through confrontation and clarification
T: insight | the client's understanding of unconscious memories, conflicts and feelings that underlie the problem
T: systematic desensitisation | Wolpe's technique of pairing gradually increasing anxiety-provoking stimuli with relaxation to reduce phobias
T: token economy | a behaviour technique in which tokens earned for desired behaviour can be exchanged for rewards
T: modelling | a technique in which the client learns a desired behaviour by observing a model performing it
T: rational emotive therapy | Albert Ellis's therapy that replaces the client's irrational beliefs with rational ones
T: cognitive therapy | Aaron Beck's therapy that changes negative automatic thoughts and dysfunctional beliefs
Q: Systematic desensitisation was introduced by: | Joseph Wolpe | Albert Ellis | Aaron Beck | Sigmund Freud
Q: Rational Emotive Therapy was formulated by: | Albert Ellis | Aaron Beck | Carl Rogers | Viktor Frankl
Q: In the ABC model of rational emotive therapy, 'B' stands for: | beliefs | behaviour | biology | barriers
Q: Exchanging earned tokens for rewards is used in: | token economy | free association | logotherapy | client-centred therapy
Q: When the client transfers positive or negative feelings towards the therapist, it is called: | transference | resistance | interpretation | catharsis
Q: Negative automatic thoughts are changed in the therapy of: | Aaron Beck | Joseph Wolpe | Sigmund Freud | Fritz Perls
Q: Psychodynamic therapy considers the cause of psychological distress to be: | unconscious conflicts from childhood | faulty learning | irrational beliefs | lack of meaning in life
M:therapist: Joseph Wolpe | systematic desensitisation
M:therapist: Albert Ellis | rational emotive therapy
M:therapist: Aaron Beck | cognitive therapy
M:therapist: Sigmund Freud | psychoanalysis
S+: Free association and dream interpretation are methods used to elicit unconscious material in psychoanalysis
S+: Behaviour therapy holds that psychological distress arises from faulty behaviour patterns or thought patterns
S+: In behaviour therapy, antecedent and consequent operations are identified through behavioural analysis
S+: In Ellis's ABC model, the antecedent event, the belief and the consequence are analysed
S+: Beck's therapy identifies core schemas and negative automatic thoughts formed in childhood
S+: Cognitive behaviour therapy combines cognitive and behavioural techniques and is widely used for many disorders
S-: Systematic desensitisation was developed by Albert Ellis | It was developed by Joseph Wolpe
S-: Behaviour therapy focuses on unconscious childhood conflicts | Psychodynamic therapy does; behaviour therapy focuses on faulty learned behaviour
S-: In transference the therapist develops feelings for the client | Transference is the client's feelings towards the therapist; the reverse is counter-transference
C: Psychoanalysis aims at insight | bringing repressed conflicts into consciousness helps the client resolve them
C: Systematic desensitisation reduces phobias | relaxation is incompatible with anxiety and is paired with gradually increasing feared stimuli
C: Rational emotive therapy targets irrational beliefs | it is the belief about an event, not the event itself, that produces emotional distress
X: C2 D2 2 | What is meant by free association? | A psychodynamic technique in which the client reclines and says whatever comes to mind without censoring; it brings unconscious thoughts and conflicts to the surface.
X: C3 D3 2 | How does a token economy work? | Desired behaviours are rewarded with tokens; tokens are later exchanged for rewards; this increases the frequency of desired behaviour.
X: C3 D3 3 | Explain the ABC model of rational emotive therapy. | A – antecedent event; B – belief about the event (often irrational); C – emotional and behavioural consequence; the therapist uses non-directive questioning to replace irrational beliefs with rational ones.
X: C3 D4 4 | Explain transference, resistance and interpretation in psychoanalytic therapy. | Transference – client attaches childhood feelings to therapist (positive or negative); resistance – unconscious opposition to change; interpretation – confrontation and clarification to point out unconscious material; leads to insight.
X: C4 D4 4 | Compare behaviour therapy with cognitive therapy. | Behaviour therapy – distress from faulty learned behaviour; techniques: desensitisation, token economy, modelling, aversive conditioning; cognitive therapy – distress from irrational thoughts and beliefs; Ellis's REBT and Beck's therapy; CBT combines both.
L: D4 | Describe the main techniques of behaviour therapy. | Behavioural analysis of antecedents and consequences; negative reinforcement; aversive conditioning; positive reinforcement and token economy; differential reinforcement; systematic desensitisation; modelling and vicarious learning.
L: D5 | Compare psychodynamic and cognitive therapies with reference to the cause of distress, the method and the outcome sought. | Psychodynamic – unconscious conflicts, free association, dream interpretation, transference, insight; cognitive – irrational beliefs and negative automatic thoughts, REBT and Beck's therapy, questioning, rational thinking.
"""), ST(S + '05-st3', 'humanistic-existential, biomedical and alternative therapies', """
T: logotherapy | Viktor Frankl's therapy that helps the client find meaning in life even in suffering
T: client-centred therapy | Carl Rogers's therapy that gives the client a warm, accepting relationship in which to reconnect with disintegrated feelings
T: Gestalt therapy | Fritz and Laura Perls's therapy that increases the client's self-awareness and self-acceptance
T: existential anxiety | the anxiety arising from problems of meaning and purpose in life
T: biomedical therapy | treatment of psychological disorders with medicines or other physical methods by a qualified psychiatrist
T: electro-convulsive therapy | a biomedical therapy in which a mild electric shock is given to the patient's brain to produce convulsions
T: Sudarshan Kriya Yoga | a rapid breathing technique found useful in reducing stress, anxiety and depression
T: vipasana meditation | a meditation practice of mindfulness in which one observes bodily sensations and thoughts without attaching to them
Q: Logotherapy was developed by: | Viktor Frankl | Carl Rogers | Fritz Perls | Albert Ellis
Q: Client-centred therapy was given by: | Carl Rogers | Viktor Frankl | Aaron Beck | Joseph Wolpe
Q: Gestalt therapy was developed by: | Fritz and Laura Perls | Carl Rogers | Abraham Maslow | Albert Ellis
Q: Which therapy helps clients find meaning in life? | Logotherapy | Token economy | Systematic desensitisation | Free association
Q: Electro-convulsive therapy can be administered by: | a qualified psychiatrist | any counsellor | a social worker | a yoga teacher
Q: Humanistic-existential therapy believes psychological distress arises from: | loneliness, alienation and inability to find meaning in life | unconscious childhood conflicts | faulty conditioning | biochemical imbalance alone
M:therapy: Logotherapy | Viktor Frankl
M:therapy: Client-centred therapy | Carl Rogers
M:therapy: Gestalt therapy | Fritz and Laura Perls
M:therapy: Systematic desensitisation | Joseph Wolpe
S+: Humanistic-existential therapies believe that people have a drive for personal growth and self-actualisation
S+: Frankl calls the process of finding meaning even in suffering the 'meaning-making' process
S+: In client-centred therapy the therapist provides a warm relationship with empathy and unconditional positive regard
S+: Biomedical therapy includes medication such as antidepressants and antipsychotic drugs prescribed by a psychiatrist
S+: Yoga and meditation are among the alternative therapies used for stress and anxiety
S+: Kundalini yoga has been found useful in treating mental disorders
S-: Logotherapy was developed by Carl Rogers | It was developed by Viktor Frankl
S-: Electro-convulsive therapy is a routine first treatment for all disorders | It is used only when drugs are not effective, and only by a psychiatrist
S-: In client-centred therapy the therapist interprets the client's unconscious | The therapist is non-directive and reflects the client's feelings
C: Humanistic therapies are non-directive | the client is seen as capable of growth and finds solutions in an accepting relationship
C: Biomedical therapy must be given by a psychiatrist | only a medically trained psychiatrist can prescribe drugs or administer ECT
C: Alternative therapies are called alternative | they are alternatives to conventional drug or psychotherapy treatments
X: C2 D2 2 | What is logotherapy? | Developed by Viktor Frankl; 'logos' means meaning; helps the client find meaning and responsibility in life, even in suffering; deals with existential anxiety.
X: C3 D3 2 | Why is ECT used only in specific cases? | It produces convulsions through electric current; used only when drugs are ineffective; must be given by a qualified psychiatrist.
X: C3 D3 3 | Explain the main features of client-centred therapy. | Given by Carl Rogers; non-directive; warm, accepting relationship; empathy and unconditional positive regard; the client reconnects with disintegrated feelings and grows.
X: C3 D4 4 | Describe any two alternative therapies. | Yoga – asanas and breathing (pranayama), Sudarshan Kriya Yoga reduces stress, anxiety and depression; meditation – focusing attention, vipasana mindfulness meditation; Kundalini yoga useful in mental disorders.
X: C4 D4 4 | Compare humanistic-existential therapy with biomedical therapy. | Humanistic – distress from loneliness, alienation, lack of meaning; non-directive, client-centred, logotherapy, Gestalt; biomedical – medicines and ECT by a psychiatrist; for severe disorders.
L: D4 | Explain the humanistic-existential therapies. | Drive for self-actualisation; existential anxiety; logotherapy by Frankl – meaning-making; client-centred therapy by Rogers – empathy, unconditional positive regard; Gestalt therapy by Perls – self-awareness, self-acceptance.
"""), ST(S + '05-st4', 'factors in healing, ethics and rehabilitation', """
T: catharsis | the release of pent-up emotions during therapy
T: informed consent | the ethical requirement that the client agrees to therapy after understanding its nature
T: rehabilitation | the process that helps patients with severe disorders become productive members of society
T: occupational therapy | rehabilitation in which patients are taught skills such as candle-making or paper-bag making to develop a work discipline
T: social skills training | rehabilitation in which patients develop interpersonal skills through role play and imitation
T: cognitive retraining | rehabilitation that improves basic cognitive functions such as attention, memory and executive functions
T: vocational training | rehabilitation that helps patients gain skills needed for productive employment
Q: The release of pent-up emotions in therapy is called: | catharsis | insight | resistance | transference
Q: Teaching patients candle-making to develop work discipline is an example of: | occupational therapy | cognitive retraining | logotherapy | free association
Q: Improving attention, memory and executive functions is the aim of: | cognitive retraining | vocational training | social skills training | occupational therapy
Q: Which of these is an ethical standard in psychotherapy? | Informed consent | Sharing case details with friends | Personal relationships with clients | Guaranteeing a cure
Q: The client's motivation for change and the therapist's warmth are examples of: | non-specific factors in healing | techniques of therapy | ethical standards | forms of rehabilitation
S+: The techniques adopted by the therapist and the therapeutic alliance both contribute to healing
S+: Release of emotions, or catharsis, contributes to healing
S+: Non-specific factors such as the client's motivation and the therapist's warmth also contribute to healing
S+: Confidentiality, informed consent and professional competence are ethical standards of psychotherapy
S+: Rehabilitation aims to empower the patient to become a productive member of society
S+: Rehabilitation includes occupational therapy, social skills training, cognitive retraining and vocational training
S-: Healing depends only on the technique used | Alliance, catharsis and non-specific patient and therapist factors also contribute
S-: Rehabilitation begins before the active symptoms are reduced | It is undertaken after the active symptoms are reduced
S-: Therapists may disclose client details to anyone who asks | Confidentiality is an ethical requirement
C: The therapeutic alliance contributes to healing | the client feels supported and works with the therapist towards change
C: Rehabilitation is needed after active symptoms are reduced | patients with severe disorders such as schizophrenia often suffer from negative symptoms and lack of skills
C: Informed consent is required | the client has a right to know the nature of the therapy and to agree to it voluntarily
X: C2 D2 2 | What is meant by catharsis? | The release of pent-up emotions during therapy; the client expresses feelings, which reduces emotional pressure.
X: C3 D3 2 | Why is rehabilitation needed for patients with severe mental disorders? | After active symptoms reduce, negative symptoms, lack of social and work skills remain; rehabilitation makes the patient self-sufficient and productive.
X: C3 D3 3 | State any three ethical standards to be followed by a psychotherapist. | Informed consent; confidentiality; personal distress be alleviated; integrity of the practitioner-client relationship; respect for human rights and dignity; professional competence and skills.
X: C3 D4 4 | Explain the factors contributing to healing in psychotherapy. | Techniques used by the therapist; therapeutic alliance; catharsis; non-specific factors – patient variables (motivation, expectation) and therapist variables (warmth, empathy, experience).
X: C4 D4 4 | Describe the different forms of rehabilitation of the mentally ill. | Occupational therapy – work discipline; social skills training – role play, imitation; cognitive retraining – attention, memory, executive functions; vocational training – skills for employment.
L: D4 | Discuss the factors contributing to healing, the ethics of psychotherapy and the rehabilitation of the mentally ill. | Techniques, alliance, catharsis, non-specific factors; ethics – informed consent, confidentiality, competence, dignity; rehabilitation – occupational, social skills, cognitive retraining, vocational.
L: D5 | 'Treatment does not end with reduction of symptoms.' Justify with reference to rehabilitation. | Negative symptoms and loss of skills persist; patients may not be able to work or relate; rehabilitation – occupational therapy, social skills training, cognitive retraining, vocational training; aim of a productive life.
""")]

CH06 = [ST(S + '06-st1', 'explaining social behaviour; nature and components of attitudes', """
T: attitude | a state of the mind, a set of views or thoughts regarding some topic (the attitude object), which have an evaluative feature
T: affective component | the emotional aspect of an attitude, such as liking or disliking the attitude object
T: cognitive component | the thought or belief aspect of an attitude about the attitude object
T: behavioural component | the tendency to act in a particular way towards the attitude object
T: valence | the feature of an attitude that tells whether it is positive or negative towards the attitude object
T: extremeness | the feature of an attitude that indicates how positive or negative it is
T: centrality | the role of a particular attitude in the attitude system; a central attitude influences other attitudes
T: social psychology | the branch of psychology that studies how individuals think, feel and behave in social situations
Q: The three components of attitude are known as the: | A-B-C components | P-O-X components | S-O-R components | I-D-E components
Q: The tendency to act in a particular way towards an attitude object is the: | behavioural component | affective component | cognitive component | central component
Q: The feature of an attitude that tells whether it is positive or negative is: | valence | extremeness | simplicity | centrality
Q: The emotional aspect of an attitude is its: | affective component | cognitive component | behavioural component | conative core
Q: An attitude that has a strong influence on many other attitudes is high in: | centrality | simplicity | valence only | complexity only
Q: Beliefs and values are: | closely related to attitudes | the same as attitudes | unrelated to attitudes | always negative
S+: Attitudes are relatively stable and have an evaluative feature
S+: Attitudes have affective, cognitive and behavioural components
S+: The four features of attitudes are valence, extremeness, simplicity or complexity, and centrality
S+: An attitude system may include several related attitudes about one object
S+: Beliefs are the cognitive component of attitudes and values contain a 'should' or 'ought' aspect
S-: An attitude has only an emotional component | It has affective, cognitive and behavioural components
S-: Valence tells how central an attitude is | Valence tells whether the attitude is positive or negative
S-: Attitudes are momentary and change every day | Attitudes are relatively stable
C: Attitudes guide behaviour | they contain a behavioural component, a tendency to act in a certain way
C: An attitude with high centrality is hard to change | it influences many other attitudes in the attitude system
C: Attitudes are evaluative | they carry a positive or negative view of the attitude object
X: C2 D2 2 | What are the components of attitude? | Affective – emotional (like or dislike); cognitive – thoughts and beliefs; behavioural – tendency to act towards the attitude object.
X: C3 D3 2 | How are beliefs and values related to attitudes? | Beliefs are the cognitive component of attitudes, forming the ground on which attitudes stand; values are attitudes or beliefs with a 'should' aspect, such as moral values.
X: C3 D3 3 | Explain the three components of an attitude with an example. | Example – attitude towards environment protection: cognitive – belief that pollution is harmful; affective – feeling unhappy about pollution; behavioural – planting trees or using public transport.
X: C3 D4 4 | Explain the four features of attitudes. | Valence – positive or negative; extremeness – how positive or negative; simplicity or complexity – number of attitudes within the attitude system; centrality – role of the attitude in the system.
X: C4 D4 4 | 'Attitudes are more than opinions.' Examine. | Attitudes have affective, cognitive and behavioural components; they are relatively stable and evaluative; they have valence, extremeness, complexity and centrality; they guide behaviour.
L: D4 | What is an attitude? Explain its components and features. | State of mind with an evaluative feature; ABC components; valence, extremeness, simplicity-complexity, centrality; relation with beliefs and values.
"""), ST(S + '06-st2', 'attitude formation and change', """
T: balance theory | Fritz Heider's theory that attitudes change when the P-O-X triangle of a person, another person and an object is unbalanced
T: cognitive dissonance | Leon Festinger's idea that inconsistency between two cognitions produces discomfort that leads to attitude change
T: two-step concept | S.M. Mohsin's view that attitude change occurs in two steps: identification with the source and then the source's own attitude change
T: association | attitude formation in which a positive or negative attitude is learnt through the connection between an object and a person
T: learning through modelling | attitude formation by observing others being rewarded or punished for expressing an attitude
T: reference group | a group whose norms an individual accepts as a model for attitudes and behaviour
Q: The P-O-X triangle is part of the theory of: | Fritz Heider | Leon Festinger | S.M. Mohsin | Solomon Asch
Q: Cognitive dissonance was proposed by: | Leon Festinger | Fritz Heider | Muzafer Sherif | Stanley Milgram
Q: The two-step concept of attitude change was proposed by: | S.M. Mohsin | Fritz Heider | Leon Festinger | Irving Janis
Q: An imbalance in the P-O-X triangle occurs when the triangle has: | all three negative sides or two positive and one negative side | three positive sides | two negative and one positive side | no sides
Q: In attitude change, the target is more likely to change when the source has: | high credibility | low credibility | an unknown identity | no relation to the target
Q: Learning attitudes by observing others being rewarded for them is called: | learning through modelling | learning by association | learning by direct experience | exposure to information
M:theorist: Fritz Heider | balance theory
M:theorist: Leon Festinger | cognitive dissonance
M:theorist: S.M. Mohsin | two-step concept
M:theorist: Solomon Asch | conformity and impression formation
S+: Attitudes are learnt through association, reward and punishment, modelling, group norms and exposure to information
S+: Family, school, reference groups, personal experiences and the media are factors in attitude formation
S+: In Heider's theory, balance exists when the P-O-X triangle has three positive sides or two negative and one positive side
S+: According to Festinger, the cognitive components of an attitude must be consonant
S+: In Mohsin's two-step concept, the target first identifies with the source and the source then shows attitude change
S+: Characteristics of the existing attitude, the source and the message, and the target all affect attitude change
S-: Balance theory was given by Leon Festinger | It was given by Fritz Heider; Festinger gave cognitive dissonance
S-: In the P-O-X triangle three positive sides produce imbalance | Three positive sides produce balance
S-: Attitudes are inherited and cannot be learnt | Attitudes are learnt through experience, association, modelling and group norms
C: A smoker who knows smoking causes cancer may stop smoking | the two cognitions are dissonant and the person reduces dissonance by changing one of them
C: Attitudes are easier to change when the source is credible | a highly credible source makes the message more convincing to the target
C: Children often share their parents' attitudes | attitudes are learnt in the family through association, reward and modelling
X: C2 D2 2 | Distinguish between balance and imbalance in the P-O-X triangle. | Balance – all three sides positive, or two negative and one positive; imbalance – all three negative, or two positive and one negative; imbalance leads to attitude change.
X: C3 D3 2 | How does the family help in attitude formation? | Parents and family members provide attitudes through association, reward and punishment and modelling in early life.
X: C3 D3 3 | Explain the two-step concept of attitude change. | Proposed by S.M. Mohsin; step 1 – the target identifies with the source (liking, respect); step 2 – the source shows attitude change, and the target imitates it; the source should be credible.
X: C3 D4 4 | Explain Festinger's cognitive dissonance theory with an example. | Cognitions must be consonant; dissonance causes discomfort; example – 'smoking causes cancer' and 'I smoke'; one cognition is changed (e.g. 'I will stop smoking') to reduce dissonance.
X: C4 D4 4 | Explain any four factors that influence attitude change. | Characteristics of the existing attitude – valence, extremeness, centrality; source – credibility, attractiveness; message – rational or emotional appeal, motives activated; target – persuasibility, prejudice, self-esteem, intelligence.
L: D4 | Explain the process of attitude formation and the factors that influence it. | Learning by association, reward and punishment, modelling, group norms, exposure to information; factors – family and school, reference groups, personal experiences, media.
L: D5 | Compare Heider's balance theory, Festinger's cognitive dissonance and Mohsin's two-step concept of attitude change. | P-O-X triangle – balance and imbalance; dissonance between cognitions; identification with source and source's change; all explain how attitudes change through consistency or imitation.
"""), ST(S + '06-st3', 'attitude-behaviour relationship; prejudice and discrimination', """
T: prejudice | a negative attitude towards a particular group, often based on stereotypes
T: stereotype | a cluster of ideas regarding the characteristics of a specific group
T: discrimination | the behavioural component of prejudice, shown as unfair treatment of members of a group
T: self-fulfilling prophecy | the process in which a group that is the target of prejudice comes to behave in ways that confirm the prejudice
T: kernel of truth | a small grain of reality that some stereotypes may contain, which leads people to hold on to them
T: ingroup bias | the tendency to favour one's own group over other groups
Q: The behavioural component of prejudice is: | discrimination | stereotype | belief | schema
Q: LaPiere's study of a Chinese couple in the USA showed that: | attitudes may not always predict behaviour | attitudes always predict behaviour | prejudice is inherited | discrimination is rare
Q: A cluster of ideas regarding the characteristics of a specific group is a: | stereotype | prejudice | schema of the self | reference group
Q: Which of these is a strategy for handling prejudice? | Intergroup contact | Strengthening ingroup bias | Social isolation | Reducing education
Q: Behaviour that confirms the negative beliefs held about a group is called: | self-fulfilling prophecy | kernel of truth | cognitive dissonance | social loafing
S+: Attitudes predict behaviour better when they are strong and occupy a central place in the attitude system
S+: Attitudes predict behaviour when the person is aware of them and there is little external pressure
S+: Prejudice can exist without discrimination and discrimination can exist without prejudice
S+: Learning, a strong social identity with ingroup bias, scapegoating, kernel of truth and self-fulfilling prophecy are sources of prejudice
S+: Education, intergroup contact, highlighting individual identity and minimising learning of prejudice are strategies to handle prejudice
S+: Intergroup contact reduces prejudice when the groups meet in a cooperative context and are of equal status
S-: Attitudes always predict behaviour | Attitudes predict behaviour only under certain conditions, as LaPiere's study showed
S-: Prejudice and discrimination are the same thing | Prejudice is an attitude; discrimination is the behaviour
S-: Stereotypes are accurate descriptions of every member of a group | Stereotypes overgeneralise and ignore individual differences
C: A strong group identity can lead to prejudice | ingroup bias makes people look down upon the outgroup
C: Intergroup contact can reduce prejudice | it brings the groups together in a cooperative setting and corrects stereotypes
C: Members of a group may confirm the prejudice about them | the self-fulfilling prophecy makes them behave as others expect
X: C2 D2 2 | Distinguish between prejudice and discrimination. | Prejudice – negative attitude towards a group (cognitive and affective); discrimination – behaviour showing unfair treatment of the group; one can exist without the other.
X: C3 D3 2 | Under what conditions do attitudes predict behaviour? | Attitude is strong and central; the person is aware of the attitude; little external pressure; behaviour is not watched by others; the person has a direct interest in the behaviour.
X: C3 D3 3 | Describe any three sources of prejudice. | Learning – from family, reference groups, media; strong social identity and ingroup bias; scapegoating – blaming a weaker group; kernel of truth; self-fulfilling prophecy.
X: C3 D4 4 | Explain the strategies for handling prejudice. | Minimising opportunities to learn prejudice; changing attitudes through education; de-emphasising narrow social identity; intergroup contact in a cooperative, equal-status setting; highlighting individual identity.
X: C4 D4 4 | 'People do not always behave as their attitudes suggest.' Explain with reference to LaPiere's study. | LaPiere travelled with a Chinese couple and was refused service in only one place; yet in a later questionnaire most establishments said they would not serve Chinese customers; attitude–behaviour inconsistency; conditions for consistency.
L: D4 | Explain the sources of prejudice and the strategies for handling it. | Learning, social identity and ingroup bias, scapegoating, kernel of truth, self-fulfilling prophecy; strategies – education, intergroup contact, individual identity, reducing learning of prejudice.
L: D5 | Discuss the relationship between attitudes and behaviour, and between prejudice and discrimination. | Conditions under which attitudes predict behaviour; LaPiere's study; prejudice as attitude and discrimination as behaviour; one may occur without the other; sources and remedies.
"""), ST(S + '06-st4', 'social cognition; behaviour in the presence of others', """
T: schema | a mental structure that guides social cognition by organising information about objects, persons and events
T: prototype | a concept-based schema defined by a set of features or properties that defines an object completely
T: impression formation | the process by which a perceiver forms an impression of a target person
T: attribution | the process of explaining the causes of one's own or others' behaviour
T: fundamental attribution error | the tendency to give more weight to internal factors than to external factors when explaining others' behaviour
T: actor-observer effect | the difference in the attribution a person makes for their own experiences and for those of others
T: primacy effect | the tendency for information presented first to have a stronger effect on impression formation
T: halo effect | the tendency to assume that a person with one positive trait also has other positive traits
T: social facilitation | the improvement in performance of a well-learnt task in the presence of others
T: social loafing | the reduction in individual effort when working in a group on a collective task
Q: The tendency to give more weight to internal causes when explaining others' behaviour is the: | fundamental attribution error | actor-observer effect | primacy effect | halo effect
Q: Social facilitation was first studied by: | Norman Triplett | Solomon Asch | Leon Festinger | Irving Janis
Q: The 'warm-cold' study of impression formation was conducted by: | Solomon Asch | Fritz Heider | Stanley Milgram | Muzafer Sherif
Q: Information presented first having a stronger effect on impressions is the: | primacy effect | recency effect | halo effect | self-fulfilling prophecy
Q: Assuming that a friendly person is also honest is an example of the: | halo effect | primacy effect | recency effect | actor-observer effect
Q: In attribution, ability and effort are: | internal factors | external factors | situational factors | chance factors
Q: According to Zajonc, the presence of others produces: | arousal that improves performance on well-learnt tasks | social loafing in every task | conformity | obedience
M:study: Norman Triplett | social facilitation
M:study: Solomon Asch | warm-cold impression formation
M:study: Fritz Heider | attribution as internal or external causes
M:study: Robert Zajonc | arousal in the presence of others
S+: Schemas function as mental short-cuts in social cognition
S+: Stereotypes are group-based schemas
S+: Impression formation and attribution are influenced by the perceiver, the target and the situation
S+: Some traits such as 'warm' and 'cold' are central traits that strongly affect the impression formed
S+: When explaining our own failures we tend to blame external factors, but we blame internal factors for others' failures
S+: Social facilitation is affected by the nature of the task and by whether the others are evaluating the performer
S-: The primacy effect means the last information has the strongest effect | That is the recency effect; primacy refers to information presented first
S-: Social facilitation means people always perform worse in the presence of others | Performance on well-learnt tasks improves; on new or difficult tasks it may worsen
S-: The fundamental attribution error overweights external causes | It overweights internal causes when explaining others' behaviour
C: People often blame a stranger's failure on lack of ability | the fundamental attribution error gives more weight to internal factors for others' behaviour
C: A singer may perform better before an audience | the presence of others produces arousal that improves performance on a well-learnt task
C: First impressions are hard to change | the primacy effect gives more weight to information received first
X: C2 D2 2 | Distinguish between the fundamental attribution error and the actor-observer effect. | FAE – overweighting internal causes for others' behaviour; actor-observer effect – we explain our own failures by external causes but others' failures by internal causes.
X: C3 D3 2 | What is a schema? How does it help in social cognition? | A mental structure organising information about persons, objects and events; acts as a mental short-cut and helps process information quickly.
X: C3 D3 3 | Explain any three effects that influence impression formation. | Primacy effect – first information; recency effect – last information; halo effect – one positive trait implies others; central traits such as warm-cold (Asch).
X: C3 D4 4 | Explain the process of attribution and the errors involved. | Explaining causes of behaviour as internal (ability, effort) or external (task, luck); fundamental attribution error; actor-observer effect; Heider's distinction.
X: C4 D4 4 | How does the presence of others affect performance? | Triplett – social facilitation; Zajonc – arousal improves well-learnt tasks and harms new tasks; evaluation apprehension; nature of task; social loafing on collective tasks.
L: D4 | Explain social cognition with reference to schemas, impression formation and attribution. | Schemas and prototypes, stereotypes; impression formation – perceiver, target, situation; primacy, recency, halo, central traits; attribution – internal and external, FAE, actor-observer effect.
"""),
]

CH07 = [ST(S + '07-st1', 'nature and formation of groups; types of groups', """
T: group | an organised system of two or more individuals who interact and are interdependent, with common motives, role relationships and norms
T: norms | the expected standards of behaviour and beliefs established and enforced by a group
T: roles | the socially defined expectations that individuals in a given situation are expected to fulfil
T: status | the relative social position given to group members by others
T: cohesiveness | the togetherness, binding or mutual attraction among group members
T: primary group | a pre-existing group, such as the family, with face-to-face interaction and close emotional bonds
T: secondary group | a group that one joins by choice, such as a political party, with impersonal and short-lived relationships
T: ingroup | one's own group, referred to as 'we'
T: outgroup | another group, referred to as 'they'
Q: Expected standards of behaviour in a group are called: | norms | roles | status | cohesiveness
Q: The first stage of group formation according to Tuckman is: | forming | storming | norming | performing
Q: The stage of group formation in which there is conflict over leadership is: | storming | forming | norming | adjourning
Q: The family is an example of a: | primary group | secondary group | formal group | crowd
Q: A group formed with explicitly stated rules, such as a university, is a: | formal group | informal group | crowd | audience
Q: Mutual attraction and togetherness among group members is called: | cohesiveness | status | norms | roles
Q: The final stage added in Tuckman's model, in which the group is dissolved, is: | adjourning | performing | norming | storming
M:stage: Forming | uncertainty about the group's goal and how it will be achieved
M:stage: Storming | conflict among members over the task and leadership
M:stage: Norming | development of group norms and a group identity
M:stage: Performing | the structure is set and the group works towards its goal
S+: A group differs from a crowd, which has no structure or feeling of belongingness
S+: People join groups for security, status, self-esteem, satisfaction of needs, goal achievement and knowledge
S+: Tuckman's stages of group formation are forming, storming, norming, performing and adjourning
S+: Proximity, similarity and common motives and goals help in group formation
S+: Groups are classified as primary and secondary, formal and informal, and ingroup and outgroup
S-: A crowd has a definite structure and norms | A crowd has no structure or feeling of belongingness; a group has both
S-: The norming stage comes before the storming stage | Storming comes before norming
S-: A political party is a primary group | It is a secondary group joined by choice
C: People join groups for security | being with others gives a sense of protection and reduces insecurity
C: Members of a group with high cohesiveness stay together | mutual attraction gives them a strong sense of belongingness
C: The storming stage involves intragroup conflict | members argue over the task and who will lead the group
X: C2 D2 2 | Distinguish between a group and a crowd. | Group – organised system, interaction, interdependence, norms, roles, sense of belongingness; crowd – collection of people at a place by chance, no structure or belongingness.
X: C3 D3 2 | Why do people join groups? State any two reasons. | Security; status; self-esteem; satisfaction of psychological and social needs; goal achievement; provide knowledge and information.
X: C3 D3 3 | Distinguish between primary and secondary groups. | Primary – pre-existing (family, caste), face-to-face, close bonds, central in socialisation; secondary – joined by choice (political party), impersonal, indirect, easy to leave.
X: C3 D4 4 | Explain the stages of group formation proposed by Tuckman. | Forming – uncertainty; storming – conflict over task and leadership; norming – norms and group identity; performing – structure set, work towards goal; adjourning – group dissolved after the goal is reached.
X: C4 D4 4 | Explain the important elements of group structure. | Roles – expected behaviour; norms – expected standards; status – relative position; cohesiveness – togetherness and mutual attraction.
L: D4 | What is a group? Explain why people join groups and the stages of group formation. | Definition and characteristics; reasons – security, status, self-esteem, needs, goals, knowledge; Tuckman's five stages.
L: D5 | Explain the different types of groups and the elements of group structure. | Primary and secondary, formal and informal, ingroup and outgroup; roles, norms, status, cohesiveness.
"""), ST(S + '07-st2', 'social loafing and group polarisation', """
T: group polarisation | the tendency of a group to make more extreme decisions than individual members would make on their own
T: groupthink | Irving Janis's term for the deterioration in group decision making when members value consensus more than critical evaluation
T: diffusion of responsibility | the feeling that responsibility for an outcome is shared, so that each member feels less responsible
T: bandwagon effect | the tendency to adopt a view because many others in the group hold it
Q: The reduction in individual effort on a collective task is called: | social loafing | social facilitation | conformity | group polarisation
Q: A group making a more extreme decision than its members would alone is called: | group polarisation | groupthink | social loafing | compliance
Q: The term groupthink was given by: | Irving Janis | Bibb Latané | Solomon Asch | Norman Triplett
Q: Social loafing can be reduced by: | making individual efforts identifiable | hiding individual contributions | increasing diffusion of responsibility | making the task meaningless
Q: Which of these is a reason for social loafing? | Members feel less responsible for the task | Each member's effort is evaluated | Members are highly motivated | The task is individual
S+: Social loafing occurs because members feel less responsible and their efforts are not individually evaluated
S+: Social loafing can be reduced by making efforts identifiable, increasing commitment, and making the task important
S+: Group polarisation occurs because of exposure to new arguments, the bandwagon effect and identification with the ingroup
S+: Groupthink occurs in highly cohesive groups that are isolated from outside opinion
S+: Strengthening group cohesiveness and increasing the importance of each member's contribution reduce social loafing
S-: Social loafing increases when each member's effort is identifiable | It decreases when individual efforts are identifiable
S-: Group polarisation makes groups take moderate decisions | It makes the group's decision more extreme in the direction already favoured
S-: Groupthink is a sign of good decision making | It is a deterioration of decision making due to excessive concern for consensus
C: Members of a rope-pulling team may pull less hard than when alone | they feel less responsible and their individual effort cannot be evaluated
C: Like-minded group members may arrive at a more extreme position | they hear new arguments in favour of their view and feel the bandwagon effect
C: Cohesive groups sometimes make poor decisions | the desire for consensus suppresses critical evaluation, leading to groupthink
X: C2 D2 2 | What is social loafing? | The reduction in individual effort when working on a collective task in a group, compared with working alone.
X: C3 D3 2 | Why does social loafing occur? Give any two reasons. | Members feel less responsible (diffusion of responsibility); individual performance is not evaluated; less motivation; poor coordination.
X: C3 D3 3 | Explain the reasons for group polarisation. | Exposure to new arguments favouring one's view; bandwagon effect – the view is held by many; identification with the ingroup and wish to conform to its position.
X: C3 D4 4 | Explain the ways in which social loafing can be reduced. | Make individual efforts identifiable; increase pressure to work hard by commitment; increase the apparent importance of the task; make each person feel his or her contribution matters; strengthen group cohesiveness.
X: C4 D4 4 | 'Groups do not always make better decisions than individuals.' Explain with reference to group polarisation and groupthink. | Polarisation – extreme decisions due to new arguments, bandwagon effect, ingroup identity; groupthink – cohesive isolated groups value consensus, illusion of unanimity, suppression of dissent.
L: D4 | Explain social loafing and group polarisation with their causes. | Loafing – reduced effort on collective tasks; causes – less responsibility, no evaluation, diffusion of responsibility; ways to reduce; polarisation – extreme decisions; causes – new arguments, bandwagon effect, ingroup identity.
"""), ST(S + '07-st3', 'conformity, compliance and obedience', """
T: conformity | behaving according to the group norm, that is, the expectations of other group members
T: compliance | behaving in response to a request from another person or group even without a norm
T: obedience | behaving in response to an order from an authority figure
T: foot-in-the-door technique | a compliance technique that starts with a small request and follows it with a larger one
T: deadline technique | a compliance technique that presents an offer as available only for a limited time
T: informational influence | influence that results from accepting evidence about reality provided by others
T: normative influence | influence that results from a person's desire to be accepted or admired by others
Q: Behaving according to the group norm is called: | conformity | compliance | obedience | polarisation
Q: Obedience to authority was studied in a well-known experiment by: | Stanley Milgram | Solomon Asch | Muzafer Sherif | Norman Triplett
Q: The line-judgment experiments on conformity were conducted by: | Solomon Asch | Stanley Milgram | Leon Festinger | Irving Janis
Q: A salesperson who first asks for a small favour and then for a larger one uses the: | foot-in-the-door technique | deadline technique | door-in-the-face technique | bandwagon effect
Q: Behaving in response to an order from an authority figure is: | obedience | conformity | compliance | cohesiveness
Q: 'Offer valid only till Sunday' is an example of the: | deadline technique | foot-in-the-door technique | modelling technique | token economy
M:influence: Conformity | following the group norm
M:influence: Compliance | responding to a request
M:influence: Obedience | responding to an order from authority
M:influence: Foot-in-the-door | small request first, larger one later
S+: Obedience is the most explicit form of social influence and conformity the least explicit
S+: Conformity is greater in small groups, when the norm is clear, and when the person's response is public
S+: Conformity is lower when the individual has strong information and a minority is present
S+: Sherif's autokinetic effect experiment showed how group norms form
S+: People obey because they feel less responsible when following orders and because authority has symbols of status
S-: Conformity is behaving in response to an order from authority | That is obedience; conformity is following the group norm
S-: Conformity is greater when responses are private | Conformity is greater when responses are public
S-: Asch studied obedience using electric shocks | Milgram studied obedience; Asch studied conformity with line judgments
C: People conform even when the group is wrong | they want to be accepted and avoid disapproval (normative influence)
C: People often obey orders that they personally disapprove of | they feel the authority is responsible for the consequences
C: Conformity is reduced when even one member disagrees with the majority | a minority gives the individual support to resist group pressure
X: C2 D2 2 | Distinguish between compliance and obedience. | Compliance – behaving in response to a request without a norm; obedience – behaving in response to an order from an authority figure.
X: C3 D3 2 | Why do people obey authority even when it is wrong? | They feel the authority is responsible for the outcome; authority has symbols of status; obedience is gradual; events move fast.
X: C3 D3 3 | Explain any three factors that influence conformity. | Size of the group – greater in small groups; size of the minority – less conformity when a dissenter is present; nature of the task; public or private response; personality.
X: C3 D4 4 | Explain conformity, compliance and obedience as forms of social influence. | Conformity – following norms (least explicit), Asch's experiment; compliance – request, foot-in-the-door, deadline technique; obedience – order from authority (most explicit), Milgram's study.
X: C4 D4 4 | Explain informational and normative influence as determinants of conformity. | Informational influence – accepting others' evidence about reality, in ambiguous situations; normative influence – desire to be accepted and avoid rejection; both produce conformity.
L: D4 | Explain conformity, compliance and obedience with reasons why people conform and obey. | Definitions and explicitness; Asch and Sherif on conformity; determinants of conformity; compliance techniques; Milgram on obedience; reasons for obedience.
L: D5 | 'Social influence ranges from the subtle to the explicit.' Discuss with reference to conformity, compliance and obedience. | Conformity – least explicit, norm-based, informational and normative influence; compliance – request, foot-in-the-door, deadline; obedience – most explicit, Milgram; factors that strengthen or weaken each.
"""), ST(S + '07-st4', 'cooperation and competition; intergroup conflict and its resolution', """
T: cooperation | working together to achieve shared group goals
T: competition | working against each other when each person or group wants to achieve its own goal
T: social identity theory | Tajfel and Turner's view that part of a person's self-concept comes from group membership, which leads to ingroup favouritism
T: intergroup conflict | a process in which one party perceives that its interests are being opposed by another party
T: superordinate goal | a goal mutually beneficial to both parties, which can be achieved only through cooperation
T: realistic conflict | conflict between groups arising from competition over limited resources
Q: The 'Robbers Cave' summer camp experiments on intergroup conflict were conducted by: | Muzafer Sherif | Henri Tajfel | Stanley Milgram | Irving Janis
Q: Social identity theory was proposed by: | Henri Tajfel and John Turner | Leon Festinger | Fritz Heider | Solomon Asch
Q: A goal that both parties can achieve only by working together is a: | superordinate goal | realistic goal | distal goal | competitive goal
Q: Working together to achieve shared goals is: | cooperation | competition | conflict | conformity
Q: According to Deutsch, cooperative groups show: | more coordination and effective communication | more mistrust | less helping | lower productivity
S+: Cooperation develops when rewards are shared and competition when rewards are for individual achievement
S+: Social identity places us in a social world and gives us a sense of who we are
S+: Lack of communication, relative deprivation and the belief that one's group is better than others contribute to intergroup conflict
S+: Superordinate goals, altering perceptions, increasing intergroup contacts, redrawing group boundaries, negotiation and structural solutions help resolve conflict
S+: In Sherif's camp study, competition produced hostility, and working on common goals reduced it
S-: Cooperative groups show less coordination than competitive groups | Cooperative groups show more coordination and effective communication
S-: Superordinate goals increase intergroup conflict | They reduce conflict because both groups must cooperate to achieve them
S-: Social identity has nothing to do with group membership | Social identity is based on membership of groups
C: Introducing superordinate goals reduces intergroup conflict | both groups must cooperate to achieve a goal that benefits them both
C: Intergroup conflict increases when groups compete for scarce resources | each group sees the other as a threat to its interests
C: A strong social identity can lead to conflict | members see their group as better and the outgroup as inferior
X: C2 D2 2 | Distinguish between cooperation and competition. | Cooperation – working together to achieve shared goals, shared rewards; competition – working against each other for individual or group goals, individual rewards.
X: C3 D3 2 | What is a superordinate goal? Give an example. | A goal that benefits both groups and can be achieved only through cooperation; e.g. two villages jointly repairing a shared water supply.
X: C3 D3 3 | Explain any three causes of intergroup conflict. | Lack of communication and faulty perceptions; relative deprivation; belief that one's group is better; feeling of disrespect; desire for more resources and power; competition for scarce resources; escalation through threats.
X: C3 D4 4 | Explain the strategies for resolving intergroup conflict. | Introducing superordinate goals; altering perceptions through persuasion and education; increasing intergroup contacts; redrawing group boundaries; negotiation; structural solutions – equitable distribution; respect for other groups' norms.
X: C4 D4 4 | Explain social identity and its role in intergroup relations. | Self-concept based on group membership (Tajfel); gives a sense of who we are; ingroup favouritism; when identity is threatened, members may enhance their group and look down on outgroups, leading to conflict.
L: D4 | Explain the causes of intergroup conflict and the strategies for its resolution. | Causes – communication, relative deprivation, belief in superiority, competition, perceived threat; Sherif's study; strategies – superordinate goals, perceptions, contact, boundaries, negotiation, structural solutions.
"""),
]

CHAPTERS = [(CH05, {}), (CH06, {}), (CH07, {})]
