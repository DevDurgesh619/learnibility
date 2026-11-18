"""CBSE class 11 Political Science, Indian Constitution at Work (chapters 6-10): fact tables for g12_hum_engine."""
from g12_hum_engine import ST

S = 'cbse-g11-political-science-ch'

CH06 = [ST(S + '06-st1', 'independence of the judiciary, appointment and removal of judges', """
T: independence of the judiciary | the principle that the other organs of government do not interfere with the work of the courts, so that judges can decide impartially
T: collegium | the group of the Chief Justice of India and the four senior-most judges of the Supreme Court that recommends appointments of judges
T: removal of judges | the process by which a judge can be removed only on grounds of proven misbehaviour or incapacity by a special majority of both Houses
T: contempt of court | the power of the courts to punish those who disobey or show disrespect to them
Q: Judges of the Supreme Court are appointed by the: | President | Prime Minister | Parliament | Chief Justice alone
Q: A judge of the Supreme Court can be removed on grounds of: | proven misbehaviour or incapacity | disagreeing with the government | losing an election | the wish of the President
Q: A motion for the removal of a judge must be passed by a special majority in: | both Houses of Parliament | the Lok Sabha only | the Rajya Sabha only | the state legislatures
Q: The salaries of judges are charged on the: | Consolidated Fund of India | Contingency Fund of state governments | budget of the Law Ministry, voted every year | Election Commission's funds
Q: Since the late 1990s, the appointment of Supreme Court judges has been based on the recommendation of the: | collegium of senior judges | Prime Minister alone | Lok Sabha | Union Public Service Commission
Q: The retirement age of a Supreme Court judge is: | 65 years | 60 years | 62 years | 70 years
Q: Which judge of the Supreme Court faced a removal motion in Parliament that failed? | Justice V. Ramaswami | Justice P.N. Bhagwati | Justice V.R. Krishna Iyer | Justice H.R. Khanna
S+: The judiciary protects the rule of law and the rights of citizens
S+: Judges have a fixed tenure and cannot be removed easily
S+: The salaries and allowances of judges are not subject to the approval of the legislature
S+: The conduct of judges cannot be discussed in the legislature except during a motion for their removal
S+: The senior-most judge of the Supreme Court is usually appointed Chief Justice, though this convention was broken twice
S+: The removal of judges is very difficult, and no judge of the Supreme Court has been removed so far
S-: Judges can be removed by the President whenever the government wishes | They can be removed only for proven misbehaviour or incapacity by a special majority of both Houses
S-: The salaries of judges are voted every year by Parliament | They are charged on the Consolidated Fund of India and not voted
S-: Parliament can freely discuss the conduct of judges at any time | It can be discussed only during a removal motion
S-: Several Supreme Court judges have been removed by Parliament | No Supreme Court judge has been removed so far
C: The judiciary in India is independent | judges have fixed tenure, salaries charged on the Consolidated Fund and protection from removal except by a difficult process
C: The procedure for removing judges is made difficult | it protects judges from political pressure and ensures independence
C: The collegium plays a key role in appointments | the Supreme Court held that the opinion of senior judges should have primacy in appointing judges
X: C2 D2 2 | What is meant by the independence of the judiciary? | Other organs do not interfere with courts; judges decide impartially without fear; secured by tenure, salaries, removal procedure, contempt powers.
X: C3 D3 2 | How are judges of the Supreme Court removed? | Only on proven misbehaviour or incapacity; motion passed by special majority in both Houses; then President orders removal; difficult – no SC judge removed so far.
X: C3 D4 4 | Explain the provisions that ensure the independence of the judiciary in India. | Appointment with role of collegium; fixed tenure; removal only by difficult procedure; salaries on Consolidated Fund; conduct not discussed in legislature; contempt of court power.
L: D4 | Explain how the Constitution ensures the independence of the judiciary. | Appointment process and collegium; seniority convention; fixed tenure and retirement; removal procedure; financial independence; immunity from criticism; contempt power; importance for rule of law.
"""), ST(S + '06-st2', 'the structure of the judiciary and the jurisdiction of the Supreme Court', """
T: integrated judiciary | a single judicial system in which the Supreme Court is at the top, followed by High Courts and subordinate courts
T: original jurisdiction | the power of the Supreme Court to hear certain cases directly, such as disputes between the Union and the states
T: appellate jurisdiction | the power of a higher court to hear appeals against the decisions of lower courts
T: advisory jurisdiction | the power of the Supreme Court to give its opinion on a question referred to it by the President
T: writ jurisdiction | the power of the courts to issue writs to protect Fundamental Rights
Q: The highest court of appeal in India is the: | Supreme Court | High Court | District Court | Lok Adalat
Q: Disputes between the Union and the states fall under the Supreme Court's: | original jurisdiction | advisory jurisdiction | appellate jurisdiction only | writ jurisdiction only
Q: The President can seek the opinion of the Supreme Court under its: | advisory jurisdiction | original jurisdiction | appellate jurisdiction | writ jurisdiction
Q: The decisions of the Supreme Court are binding on all courts in India under Article: | 141 | 32 | 226 | 356
Q: Under Article 136, the Supreme Court can grant: | special leave to appeal against any judgment of any court | citizenship | election symbols | a pardon
Q: The advisory jurisdiction of the Supreme Court is provided under Article: | 143 | 131 | 32 | 226
S+: India has a single integrated judicial system with the Supreme Court at the top
S+: High Courts hear appeals from lower courts and can issue writs
S+: The Supreme Court hears appeals in civil, criminal and constitutional cases
S+: The Supreme Court can hear disputes between the Union and the states and between states directly
S+: The Supreme Court is a court of record and its decisions are binding on all courts
S+: The advice of the Supreme Court under its advisory jurisdiction is not binding on the President
S-: India has separate federal and state court systems as in the USA | India has a single integrated judicial system
S-: The advisory opinion of the Supreme Court is binding on the President | It is not binding on the President
S-: Disputes between the Union and states are first heard by District Courts | They come under the original jurisdiction of the Supreme Court
C: The Supreme Court has original jurisdiction in federal disputes | it acts as the umpire between the Union and the states
C: The advisory jurisdiction is useful to the government | it can obtain legal advice on difficult questions before taking action
C: India has an integrated judiciary | the Supreme Court's decisions are binding on all courts and appeals rise from lower to higher courts
X: C2 D2 2 | What is the original jurisdiction of the Supreme Court? | The power to hear certain cases directly, such as disputes between the Union and the states or between states (Art 131).
X: C3 D3 2 | Distinguish between appellate and advisory jurisdiction. | Appellate – hears appeals against lower court decisions (civil, criminal, constitutional); advisory – gives opinion on questions referred by the President (Art 143), not binding.
X: C3 D4 4 | Explain the jurisdiction of the Supreme Court of India. | Original (federal disputes, Art 131); writ (Art 32); appellate (civil, criminal, constitutional); advisory (Art 143); special leave (Art 136); court of record, decisions binding (Art 141).
L: D4 | Describe the structure of the judiciary in India and the jurisdiction of the Supreme Court. | Integrated system – Supreme Court, High Courts, district and subordinate courts; original, writ, appellate, advisory jurisdiction; special leave; court of record; binding decisions.
"""), ST(S + '06-st3', 'judicial activism and public interest litigation', """
T: judicial activism | the active role of the courts in protecting rights and addressing public problems, often through PIL
T: public interest litigation | a case filed in court in the public interest by any person or group on behalf of those whose rights are violated
T: epistolary jurisdiction | the practice of treating letters and newspaper reports as petitions in public interest
Q: Public interest litigation in India began in the: | late 1970s | 1950s | 1990s | 1930s
Q: In a public interest litigation, a case can be filed by: | any person or group on behalf of others whose rights are violated | only the person whose rights are violated | only the government | only lawyers of the Supreme Court
Q: The courts began treating letters and newspaper reports as petitions. This is called: | epistolary jurisdiction | original jurisdiction | advisory jurisdiction | pocket veto
Q: Which of the following is a criticism of judicial activism? | It blurs the line between the judiciary and the executive | It reduces access to justice | It removes rights | It weakens the poor
S+: Public interest litigation increased access to justice for the poor and disadvantaged
S+: Under PIL, the courts relaxed the rule that only the affected person could approach them
S+: The courts took up issues such as the rights of prisoners, bonded labour and pollution through PIL
S+: Judicial activism has made the judiciary more responsive to the needs of ordinary people
S+: Critics say judicial activism overburdens the courts and blurs the separation of powers
S-: Under PIL, only the affected person can approach the court | Any person or group can approach the court on behalf of others
S-: Public interest litigation began in India in the 1950s | It began in the late 1970s
S-: Judicial activism has no critics | Critics say it overburdens courts and blurs the separation of powers
C: Public interest litigation made justice more accessible | the courts allowed any person to file a case on behalf of the poor and disadvantaged
C: Judicial activism is criticised | it can make the judiciary take over functions of the executive and the legislature
C: Courts treated letters as petitions | they wanted to help people who could not afford to approach the courts formally
X: C2 D2 2 | What is public interest litigation? | A case filed in public interest by any person or group on behalf of those whose rights are violated; began in late 1970s; letters treated as petitions.
X: C3 D4 4 | Examine the positive and negative effects of judicial activism. | Positive – access to justice for the poor, rights of prisoners and bonded labour, environment, accountability; negative – overburdens courts, blurs separation of powers, executive functions taken over.
L: D4 | What is judicial activism? Explain the role of public interest litigation in it. | PIL from late 1970s; relaxation of locus standi; letters and reports as petitions; issues – prisoners, bonded labour, environment; benefits; criticisms of overreach and burden.
"""), ST(S + '06-st4', 'the judiciary, rights and Parliament: judicial review', """
T: judicial review | the power of the Supreme Court and High Courts to examine whether a law or an executive action is constitutional
T: basic structure | the doctrine laid down in the Kesavananda Bharati case that Parliament cannot amend the basic features of the Constitution
T: Kesavananda Bharati case | the 1973 case in which the Supreme Court held that Parliament can amend the Constitution but not its basic structure
Q: The basic structure doctrine was laid down in the case of: | Kesavananda Bharati (1973) | Golaknath (1967) | Maneka Gandhi (1978) | Indra Sawhney (1992)
Q: In the Golaknath case of 1967, the Supreme Court held that Parliament: | cannot amend Fundamental Rights | can amend any part of the Constitution freely | has no power to make laws | cannot pass money bills
Q: Judicial review means the power of the courts to: | examine the constitutionality of laws and executive actions | make new laws | appoint ministers | conduct elections
Q: The main early conflict between Parliament and the judiciary concerned the right to: | property | vote | education | constitutional remedies
Q: The Supreme Court can declare a law invalid if it: | violates the Constitution | is passed by Parliament | is unpopular | is passed after an election
Y: 1967 | the Golaknath judgement on the amendment of Fundamental Rights
Y: 1973 | the Kesavananda Bharati judgement and the basic structure doctrine
Y: 1978 | the 44th Amendment that removed the right to property from the Fundamental Rights
S+: The term judicial review is not mentioned in the Constitution, but the power follows from it
S+: The Supreme Court can declare laws invalid if they violate Fundamental Rights or the distribution of powers
S+: Conflicts between Parliament and the judiciary arose over the right to property and the power to amend the Constitution
S+: In the Kesavananda Bharati case the Court held that Parliament can amend any part of the Constitution but not its basic structure
S+: Courts have expanded the meaning of the right to life to include the right to livelihood and to a clean environment
S-: The Constitution explicitly uses the term 'judicial review' | The term is not used, but the power follows from the Constitution
S-: In the Kesavananda Bharati case, the Court held that Parliament can change the basic structure | The Court held that the basic structure cannot be amended
S-: Courts can review only executive orders and never laws | Courts can review both laws and executive actions
C: The Supreme Court laid down the basic structure doctrine | it wanted to prevent Parliament from destroying the core features of the Constitution through amendments
C: Conflicts arose between Parliament and the judiciary over property | land reform laws affected the right to property, which was then a Fundamental Right
C: Judicial review protects the Constitution | courts can strike down laws and actions that violate Fundamental Rights or the federal distribution of powers
X: C2 D2 2 | What is judicial review? | Power of the Supreme Court and High Courts to examine constitutionality of laws and executive actions and declare them invalid if unconstitutional.
X: C3 D3 2 | What did the Supreme Court decide in the Kesavananda Bharati case? | Parliament can amend any part of the Constitution, but not its basic structure (1973).
X: C3 D4 4 | Trace the conflict between Parliament and the judiciary over the amendment of the Constitution. | Right to property and land reforms; Golaknath 1967 – Fundamental Rights cannot be amended; amendments by Parliament; Kesavananda 1973 – basic structure doctrine; 44th Amendment 1978 removed property as Fundamental Right.
X: C4 D4 4 | 'The judiciary has become a protector of rights.' Discuss with examples. | Judicial review; expansion of Art 21 (livelihood, environment, dignity); PIL; basic structure; but debates over overreach; balance between Parliament and courts.
L: D4 | Explain the role of the judiciary in protecting rights and its relationship with Parliament. | Writs and Art 32; judicial review; expansion of rights through interpretation; conflicts over property and amendments – Golaknath 1967, Kesavananda 1973, basic structure; 44th Amendment 1978; balance of powers.
L: D5 | 'Judicial review is essential in a democracy, but it must not become judicial supremacy.' Critically examine. | Need – protect rights, federal balance, constitution; Kesavananda; PIL; dangers – overreach, executive and legislative functions; separation of powers; balanced view.
""")]

CH07 = [ST(S + '07-st1', 'federalism and its features in the Indian Constitution', """
T: federalism | an arrangement in which there are two sets of government, one for the whole country and others for the regions, each with its own powers
T: union of states | the description of India in Article 1 of the Constitution
T: linguistic states | states formed on the basis of language, after the States Reorganisation Act of 1956
Q: Article 1 of the Constitution describes India as a: | Union of States | Federation of States | Confederation | Unitary State
Q: Which was the first state to be formed on a linguistic basis in 1953? | Andhra | Gujarat | Maharashtra | Punjab
Q: The States Reorganisation Act was passed in: | 1956 | 1947 | 1950 | 1966
Q: In a federation, a dispute between the centre and a state is decided by the: | judiciary | army | President alone | ruling party
Q: Which of the following is an example of a federation that broke up in 1991? | The Soviet Union | India | The USA | Australia
S+: In a federation, powers are divided between the central and the regional governments by the constitution
S+: A federal constitution is usually written and difficult to amend
S+: An independent judiciary settles disputes between the centre and the states in a federation
S+: The word 'federation' is not used in the Indian Constitution
S+: Federalism helps a diverse country like India accommodate regional and linguistic identities
S+: The break-up of the Soviet Union showed the dangers of concentrating power and ignoring regional aspirations
S-: The Indian Constitution describes India as a federation | Article 1 describes India as a Union of States
S-: In a federation all powers lie with the central government | Powers are divided between the centre and the regions
S-: Federal disputes in India are decided by the Prime Minister | They are decided by the judiciary
C: India adopted a federal system | its large size and diversity required powers to be shared between the centre and the states
C: States were reorganised on a linguistic basis | people wanted administration in their own language and regional identities were strong
C: A federation needs an independent judiciary | disputes between the centre and the states must be settled impartially
X: C2 D2 2 | State any two features of a federal system. | Two sets of governments; division of powers by constitution; written and rigid constitution; independent judiciary to settle disputes.
X: C3 D4 4 | Why did India adopt a federal system? Explain its main features. | Size and diversity; regional and linguistic identities; features – division of powers (Seventh Schedule), written constitution, independent judiciary, bicameral Parliament with Rajya Sabha; 'Union of States'; linguistic reorganisation.
L: D4 | What is federalism? Explain the federal features of the Indian Constitution. | Meaning; two sets of governments; division of powers; written constitution; independent judiciary; Rajya Sabha; linguistic states; 'Union of States'; comparison with USSR break-up.
"""), ST(S + '07-st2', 'federalism with a strong central government and the division of powers', """
T: Union List | the list in the Seventh Schedule of subjects on which only Parliament can make laws, such as defence and foreign affairs
T: State List | the list of subjects on which normally only the states can make laws, such as police and agriculture
T: Concurrent List | the list of subjects on which both Parliament and the states can make laws, such as education and forests
T: residuary powers | the power to make laws on subjects not mentioned in any list, which belongs to Parliament in India
T: Seventh Schedule | the part of the Constitution that contains the Union, State and Concurrent Lists
Q: Defence and foreign affairs are subjects in the: | Union List | State List | Concurrent List | residuary list
Q: Police and agriculture are subjects in the: | State List | Union List | Concurrent List | Ninth Schedule
Q: Education and forests are subjects in the: | Concurrent List | State List | Union List | Eleventh Schedule
Q: In India, residuary powers belong to: | Parliament | the states | the Supreme Court | the President alone
Q: If there is a conflict between a central law and a state law on a Concurrent List subject: | the central law prevails | the state law prevails | both are cancelled | the Governor decides
Q: Under Article 3, the power to create new states and change state boundaries belongs to: | Parliament | the state legislatures | the Supreme Court | the Election Commission
M:subject-list: Defence | Union List
M:subject-list: Police | State List
M:subject-list: Education | Concurrent List
M:subject-list: Subjects not mentioned in any list | Parliament (residuary powers)
S+: The Constitution divides legislative powers through the Union, State and Concurrent Lists
S+: Parliament can create new states and change the boundaries of existing states
S+: During an emergency, the federal system can become almost unitary
S+: The Union government has greater financial resources, and states depend on it for grants
S+: Governors are appointed by the President and can recommend the dismissal of a state government
S+: India has a single citizenship and an integrated judiciary
S-: Residuary powers belong to the states in India | They belong to Parliament
S-: States can create new states by changing boundaries on their own | Under Article 3, Parliament has this power
S-: In a conflict on a Concurrent List subject, the state law prevails | The central law prevails
S-: Governors are elected by the people of the state | Governors are appointed by the President
C: The Indian federation has a strong centre | the makers wanted to protect unity after partition and to promote planned development
C: The states depend financially on the centre | major sources of revenue are with the Union and states receive grants and shares of taxes
C: India's federation can become unitary during an emergency | the Constitution allows the centre to take over powers in such situations
X: C2 D2 2 | Give one example each of subjects in the Union, State and Concurrent Lists. | Union – defence, foreign affairs, banking, currency, atomic energy, railways; State – police, agriculture, local government, public health; Concurrent – education, forests, marriage, adoption, trade unions.
X: C3 D3 2 | Name any two provisions that make the Indian centre strong. | Parliament's power to create states and change boundaries (Art 3); emergency powers; financial dominance; Governor; residuary powers; All India Services; single citizenship.
X: C3 D4 4 | 'The Indian Constitution has created a federation with a strong centre.' Justify. | Union List larger and important; residuary powers with centre; central law prevails in Concurrent List; Art 3; emergency powers; financial dependence of states; Governors; All India Services; integrated judiciary.
L: D4 | Explain the division of powers between the Union and the states and the features that make the Union strong. | Seventh Schedule – Union, State, Concurrent Lists with examples; residuary powers; supremacy in Concurrent List; Art 3; emergencies; finance; Governor; All India Services; reasons for strong centre.
L: D5 | 'India's federalism is cooperative rather than competitive.' Critically discuss. | Shared lists, grants, planning, All India Services; but tensions over autonomy, Governor, Art 356, finances; coalition era increased states' role; balanced view.
"""), ST(S + '07-st3', "conflicts in India's federal system", """
T: Governor | the head of a state, appointed by the President, who acts on the advice of the state Council of Ministers but has some discretionary powers
T: President's Rule | the imposition of central rule in a state under Article 356 when the government of the state cannot be carried on according to the Constitution
T: Sarkaria Commission | the commission appointed in 1983 to examine centre–state relations, which recommended that Governors be impartial
T: demand for autonomy | the demand of some states for more powers and resources from the centre
Q: President's Rule is imposed in a state under Article: | 356 | 370 | 32 | 249
Q: The commission appointed in 1983 to examine centre–state relations was the: | Sarkaria Commission | Kothari Commission | Mandal Commission | Shah Commission
Q: The Governor of a state is appointed by the: | President | Chief Minister | state legislature | Chief Justice
Q: Which of the following is an example of an inter-state river water dispute? | The Cauvery dispute | The Kashmir question | The Bodoland movement | The Sikkim merger
Q: The Cauvery water dispute is mainly between Tamil Nadu and: | Karnataka | Kerala | Andhra Pradesh | Maharashtra
Q: Which of these states was formed in the year 2000? | Jharkhand | Telangana | Haryana | Gujarat
S+: The role of the Governor has been a source of tension between the centre and the states
S+: The use of Article 356 has often been criticised as a misuse for political reasons
S+: Some states have demanded more autonomy and a greater share of financial resources
S+: Inter-state disputes over borders and river waters have caused tension in the federal system
S+: Chhattisgarh, Uttarakhand and Jharkhand were created in 2000, and Telangana in 2014
S+: The Sarkaria Commission recommended that the Governor should be an impartial person
S-: Article 356 has never been used in India | It has been used many times, often criticised as misuse
S-: Governors are elected by the people of the state | Governors are appointed by the President
S-: There have been no disputes between states in India | There have been border and river water disputes, such as the Cauvery dispute
C: The Governor's role has caused tension in centre–state relations | Governors are appointed by the centre and have sometimes acted in its political interest
C: Some states have demanded autonomy | they felt that the centre had too much power and too large a share of resources
C: Article 356 has been called a source of conflict | it has often been used to dismiss state governments run by opposition parties
X: C2 D2 2 | What is President's Rule? | Under Art 356, when the state government cannot be carried on according to the Constitution, the President takes over its administration on the Governor's report.
X: C3 D3 2 | Why has the role of the Governor been controversial? | Appointed by the centre; may act in its political interest; recommendations for President's Rule; role in choosing CM; Sarkaria Commission recommended impartial Governors.
X: C3 D4 4 | Explain the sources of conflict in India's federal system. | Demands for autonomy; Governor's role; Art 356 misuse; demands for new states; inter-state border and river water disputes (Cauvery); financial issues.
L: D4 | Discuss the conflicts in India's federal system with examples. | Centre–state – autonomy demands, Governor, Art 356, Sarkaria Commission, finances; new states (2000, 2014); inter-state disputes – borders and river waters (Cauvery); accommodation through negotiation and courts.
"""), ST(S + '07-st4', 'special provisions for states', """
T: special provisions | provisions in the Constitution that give some states particular powers or protections because of their history, culture or conditions
T: Article 371 | the article containing special provisions for several states, such as development boards and protections for local customs
T: Sixth Schedule | the schedule providing for autonomous district councils in tribal areas of Assam, Meghalaya, Tripura and Mizoram
Q: Special provisions for Nagaland are contained in Article: | 371A | 370 | 356 | 249
Q: Article 370, which gave special status to Jammu and Kashmir, was made inoperative in: | 2019 | 2014 | 1975 | 2000
Q: Autonomous district councils in tribal areas of the north-east are provided under the: | Sixth Schedule | Seventh Schedule | Tenth Schedule | Ninth Schedule
Q: Under Article 371A, an Act of Parliament on Naga customary law applies to Nagaland only if: | the state assembly so decides | the President so decides | the Supreme Court approves | a referendum is held in India
Q: Special provisions for Sikkim are contained in Article: | 371F | 371A | 370 | 371J
S+: The Constitution makes special provisions for some states keeping in mind their history and conditions
S+: The special provisions for the north-eastern states protect their customary laws, land and culture
S+: Special provisions for Maharashtra and Gujarat allow development boards for backward regions
S+: In 2019, Article 370 was made inoperative and Jammu and Kashmir was reorganised into two Union Territories
S+: Asymmetrical federalism allows different states to have different arrangements within the same federation
S-: All Indian states have exactly the same powers and provisions | Some states have special provisions under Article 371 and other articles
S-: The special provisions for Nagaland allow Parliament to change Naga customary law without the state's consent | Such laws apply only if the state assembly so decides
S-: Article 370 still gives special status to Jammu and Kashmir | It was made inoperative in 2019
C: Some north-eastern states have special provisions | they have distinct tribal cultures, customary laws and land systems that need protection
C: India's federalism is called asymmetrical | different states have different arrangements according to their particular needs
C: Development boards were provided for some regions | regions such as Vidarbha and Marathwada lagged behind other parts of their states
X: C2 D2 2 | What is meant by asymmetrical federalism? | Different states have different powers and arrangements within one federation, e.g., special provisions under Art 371 for some states.
X: C3 D4 4 | Explain the special provisions for states in the Indian Constitution. | Art 371 – development boards (Maharashtra, Gujarat); 371A Nagaland and 371G Mizoram – customary law and land; 371F Sikkim; Sixth Schedule autonomous councils; Art 370 (inoperative since 2019); reasons.
L: D4 | Why does the Constitution make special provisions for some states? Explain with examples. | History, culture, tribal customs, backwardness; Art 371 provisions for several states; Nagaland and Mizoram; Sixth Schedule; Jammu and Kashmir and Art 370 (2019 change); asymmetrical federalism.
""")]

CH08 = [ST(S + '08-st1', 'the need for local governments and their growth in India', """
T: local government | government at the village and district level and in towns and cities, closest to the common people
T: gram sabha | the assembly of all adult voters of a village or panchayat area
T: Community Development Programme | the programme launched in 1952 to promote people's participation in rural development
T: Balwant Rai Mehta Committee | the committee of 1957 that recommended a three-tier system of Panchayati Raj
Q: The Community Development Programme was launched in: | 1952 | 1957 | 1992 | 1882
Q: The three-tier system of Panchayati Raj was recommended by the: | Balwant Rai Mehta Committee | Sarkaria Commission | Mandal Commission | Kothari Commission
Q: The organisation of village panchayats is mentioned in the Constitution as a: | Directive Principle | Fundamental Right | Fundamental Duty | Union List subject
Q: Lord Ripon's resolution on local self-government was issued in: | 1882 | 1919 | 1935 | 1952
Q: Which leader strongly advocated gram swaraj as the basis of Indian democracy? | Mahatma Gandhi | B.R. Ambedkar | Jawaharlal Nehru | Sardar Patel
S+: Local government brings government closer to the people and allows them to solve local problems
S+: Local governments encourage participation of ordinary people in decision-making
S+: Before the 73rd Amendment, local bodies depended on state laws and were often weak
S+: Elections to local bodies were often not held regularly before 1992
S+: Gandhi believed that villages should govern themselves through gram swaraj
S-: Local governments were given constitutional status in 1950 | They received constitutional status through the 73rd and 74th Amendments of 1992
S-: Before 1992, local body elections were held regularly everywhere | Elections were often irregular and local bodies were weak
S-: Local government keeps decision-making far away from people | It brings government closer to the people
C: Local governments are needed | many problems are best solved locally with the participation of the people affected
C: Local bodies were weak before 1992 | they depended on state laws, had few powers and funds, and elections were irregular
C: The Constitution included village panchayats in the Directive Principles | the makers wanted local self-government but left it to the states to implement
X: C2 D2 2 | Why do we need local governments? | Close to people; local problems solved locally; participation; accountability; training ground for democracy.
X: C3 D4 4 | Trace the growth of local government in India before the 73rd Amendment. | Lord Ripon (1882); Government of India Act 1919; Gandhi's gram swaraj; Directive Principle (Art 40); Community Development Programme (1952); Balwant Rai Mehta Committee (1957) – three-tier system; weaknesses – state control, irregular elections, few funds.
L: D4 | Why are local governments important? Describe the growth of local government in India. | Closeness, participation, accountability; history – Ripon 1882, 1919 Act, Gandhi, Art 40, CDP 1952, Mehta Committee 1957; weaknesses before 1992; 73rd and 74th Amendments.
"""), ST(S + '08-st2', 'the 73rd and 74th Amendments', """
T: Panchayati Raj | the system of rural local self-government with panchayats at the village, intermediate and district levels
T: Zilla Parishad | the district-level body of the Panchayati Raj system
T: Eleventh Schedule | the schedule listing 29 subjects that can be transferred to panchayats
T: Twelfth Schedule | the schedule listing 18 subjects that can be transferred to urban local bodies
T: municipal corporation | the urban local body of a large city
Q: The 73rd Amendment deals with: | rural local governments | urban local governments | anti-defection | voting age
Q: The 74th Amendment deals with: | urban local governments | rural local governments | the President's powers | judicial review
Q: The 73rd and 74th Amendments were passed in: | 1992 | 1985 | 1976 | 2002
Q: How many subjects are listed in the Eleventh Schedule? | 29 | 18 | 12 | 52
Q: How many subjects are listed in the Twelfth Schedule? | 18 | 29 | 10 | 47
Q: What proportion of seats in local bodies is reserved for women? | One-third | One-fourth | One-half in all states by the Constitution | One-tenth
Q: The intermediate level of panchayats need not be set up in states with a population of less than: | 20 lakh | 50 lakh | 1 crore | 5 lakh
Q: Elections to local bodies must be held every: | five years | three years | six years | ten years
S+: The 73rd Amendment created a uniform three-tier structure of Panchayati Raj in most states
S+: The gram sabha consists of all adult voters of the panchayat area
S+: One-third of the seats and of the posts of chairpersons in local bodies are reserved for women
S+: Seats are reserved for Scheduled Castes and Scheduled Tribes in proportion to their population
S+: If a local body is dissolved, elections must be held within six months
S+: The 74th Amendment provided for nagar panchayats, municipal councils and municipal corporations
S-: The 73rd Amendment deals with urban local bodies | It deals with rural local bodies; the 74th deals with urban bodies
S-: Elections to local bodies can be postponed indefinitely after dissolution | Elections must be held within six months of dissolution
S-: Women have no reservation in local bodies | One-third of seats and chairperson posts are reserved for women
S-: The Eleventh Schedule lists 18 subjects | It lists 29 subjects; the Twelfth Schedule lists 18
C: The 73rd Amendment strengthened rural local government | it gave panchayats constitutional status, regular elections and reservations
C: Reservation for women in local bodies has increased their participation | one-third of seats and chairperson posts are reserved for them
C: Elections to local bodies are now regular | the Constitution requires elections every five years and within six months of dissolution
X: C2 D2 2 | Name the three tiers of Panchayati Raj. | Gram panchayat (village); panchayat samiti or block/mandal (intermediate); zilla parishad (district).
X: C3 D3 2 | State any two provisions of the 73rd Amendment. | Three-tier structure; gram sabha; elections every five years; one-third reservation for women; SC/ST reservation; State Election Commission; State Finance Commission; Eleventh Schedule.
X: C3 D4 4 | Explain the main provisions of the 73rd and 74th Amendments. | 73rd – three tiers, gram sabha, five-year elections, reservations for women and SC/ST, Eleventh Schedule (29 subjects); 74th – nagar panchayat, municipal council, municipal corporation, Twelfth Schedule (18 subjects); State Election and Finance Commissions.
L: D4 | Describe the main features of the 73rd and 74th Amendments. | 1992; constitutional status; three tiers; gram sabha; elections; reservations; schedules; urban bodies – nagar panchayat, council, corporation; State Election Commission and State Finance Commission.
"""), ST(S + '08-st3', 'implementation of the 73rd and 74th Amendments', """
T: State Election Commission | the independent body in each state responsible for conducting elections to local bodies
T: State Finance Commission | the commission appointed by each state every five years to review the financial position of local governments
T: PESA | the Panchayats (Extension to Scheduled Areas) Act of 1996, which extended the panchayat provisions to Scheduled Areas
Q: Elections to panchayats are conducted by the: | State Election Commission | Election Commission of India | District Collector | Gram Sabha
Q: The State Finance Commission is appointed every: | five years | year | ten years | two years
Q: The PESA Act extending the panchayat provisions to Scheduled Areas was passed in: | 1996 | 1992 | 1976 | 2005
Q: A major problem in the working of local governments is: | dependence on state and central governments for funds | too much money | no elections | absence of women members
S+: Every state has set up a State Election Commission to conduct local elections
S+: The State Finance Commission reviews the finances of local governments and recommends the sharing of revenue
S+: Many states have not transferred all subjects and funds to local governments
S+: Local bodies depend heavily on grants from the state and central governments
S+: The reservation for women has brought a large number of women into local government
S-: Local governments in India are financially independent | They depend heavily on state and central grants
S-: All states have transferred all 29 subjects to panchayats | Many states have not transferred all subjects and funds
S-: The State Election Commission is a part of the state government's ministry | It is an independent body
C: Local governments in India remain weak in practice | many states have not transferred enough subjects and funds to them
C: The State Finance Commission is important for local bodies | local governments need a fair share of state revenue to function
C: Women's participation in local government has increased | the Constitution reserves one-third of the seats and chairperson posts for them
X: C2 D2 2 | What are the functions of the State Finance Commission? | Reviews the financial position of local governments; recommends distribution of revenue between state and local bodies; appointed every five years.
X: C3 D4 4 | Examine the implementation of the 73rd and 74th Amendments. | Regular elections by State Election Commissions; women's and SC/ST participation; but limited transfer of subjects and funds; dependence on grants; bureaucratic control; PESA for Scheduled Areas.
L: D4 | Assess the working of local governments after the 73rd and 74th Amendments. | Achievements – regular elections, State Election Commission, reservations and participation of women, SC/ST; problems – funds, transfer of functions, dependence, state control; State Finance Commission; PESA 1996.
""")]

CH09 = [ST(S + '09-st1', 'how the Constitution is amended', """
T: amendment | a change made in the Constitution by Parliament following the procedure in Article 368
T: special majority | a majority of the total membership of a House and two-thirds of the members present and voting
T: ratification by states | the approval of at least half of the state legislatures needed for amendments affecting federal provisions
T: rigid and flexible | the balance in the Indian Constitution between provisions that are hard to change and those that are easy to change
Q: The procedure for amending the Constitution is given in Article: | 368 | 356 | 32 | 370
Q: A special majority requires a majority of the total membership of the House and: | two-thirds of members present and voting | one-half of members present | three-fourths of all members | unanimous support
Q: Amendments affecting the distribution of powers between the Union and states also need ratification by: | at least half of the state legislatures | all state legislatures | a referendum | the Supreme Court
Q: Who can initiate an amendment to the Constitution? | Parliament | state legislatures alone | the President alone | the Supreme Court
Q: Is a joint sitting of the two Houses possible for passing an amendment? | No, each House must pass it separately | Yes, always | Only for money bills | Only if the President agrees
S+: The Indian Constitution combines rigidity and flexibility in its amendment procedure
S+: Some parts of the Constitution can be changed by Parliament through a simple majority
S+: Most amendments require a special majority in each House of Parliament
S+: Amendments affecting federal features also require the ratification of half the states
S+: There is no provision for a referendum in the amendment procedure in India
S+: An amendment bill must be passed separately by both Houses, with no joint sitting
S-: The Indian Constitution can be amended only by a referendum | It is amended by Parliament; there is no referendum
S-: All amendments require ratification by all states | Only amendments affecting federal provisions need ratification by half the states
S-: A deadlock on an amendment bill can be resolved by a joint sitting | Each House must pass it separately; no joint sitting
C: The Constitution is neither too rigid nor too flexible | some parts can be changed by simple majority while others need a special majority and ratification by states
C: The states have a say in some amendments | amendments affecting federal provisions need ratification by half of the state legislatures
C: The Constitution can respond to new circumstances | its amendment procedure allows changes when there is wide agreement
X: C2 D2 2 | What is meant by a special majority? | Majority of total membership of the House and two-thirds of members present and voting, in each House separately.
X: C3 D4 4 | Explain the different methods of amending the Indian Constitution. | Simple majority for some provisions; special majority in each House under Art 368; special majority plus ratification by half the states for federal provisions; no referendum, no joint sitting; President's assent.
L: D4 | 'The Indian Constitution is a blend of rigidity and flexibility.' Explain with reference to its amendment procedure. | Art 368; simple majority provisions; special majority; ratification by states; no referendum; no joint sitting; balance between change and stability; large number of amendments.
"""), ST(S + '09-st2', 'why the Constitution has been amended so often', """
T: 42nd Amendment | the extensive amendment of 1976, made during the Emergency, which changed many provisions of the Constitution
T: 44th Amendment | the amendment of 1978 that undid many changes of the 42nd Amendment
T: technical amendments | amendments that clarify or change technical details, such as the retirement age of judges
Q: The amendment that added the words 'socialist' and 'secular' to the Preamble was the: | 42nd Amendment of 1976 | 44th Amendment of 1978 | 1st Amendment of 1951 | 73rd Amendment of 1992
Q: The 42nd Amendment extended the term of the Lok Sabha from five to: | six years | seven years | four years | ten years
Q: Which amendment restored the five-year term of the Lok Sabha? | The 44th Amendment | The 42nd Amendment | The 52nd Amendment | The 61st Amendment
Q: The 15th Amendment raised the retirement age of High Court judges from 60 to: | 62 | 65 | 58 | 70
Q: Which of these amendments was passed through political consensus? | The 61st Amendment reducing the voting age to 18 | The 42nd Amendment of 1976 | The 39th Amendment | The 38th Amendment
S+: Many amendments are technical or administrative in nature
S+: Some amendments resulted from differing interpretations of the Constitution by the judiciary and Parliament
S+: Many amendments were the result of a consensus among political parties
S+: The 42nd Amendment was passed during the Emergency and was very controversial
S+: The 44th Amendment of 1978 reversed many changes made by the 42nd Amendment
S+: Amendments such as the anti-defection law and the reduction of the voting age were passed with consensus
S-: Most amendments changed the basic philosophy of the Constitution | Most were technical or reflected consensus, without changing its basic philosophy
S-: The 42nd Amendment was passed after wide consultation in normal times | It was passed during the Emergency and was controversial
S-: The 44th Amendment extended the term of the Lok Sabha to six years | The 42nd did; the 44th restored the five-year term
C: The Constitution has been amended many times | technical changes, differing interpretations and political consensus have all needed amendments
C: The 44th Amendment was passed in 1978 | the new government wanted to undo the changes made during the Emergency by the 42nd Amendment
C: Many amendments did not change the basic philosophy of the Constitution | they were technical or reflected agreement among parties
X: C2 D2 2 | Give two examples of amendments passed through political consensus. | 52nd (anti-defection, 1985); 61st (voting age 18); 73rd and 74th (local government, 1992); 91st (size of ministry).
X: C3 D4 4 | Why has the Indian Constitution been amended so many times? | Technical/administrative amendments (15th – retirement age); differing interpretations between judiciary and Parliament (property, reservations); political consensus (52nd, 61st, 73rd, 74th); controversial amendments of 1970s (42nd), reversed by 44th.
L: D4 | Classify the amendments to the Indian Constitution with examples. | Technical (15th); differing interpretations (property, Golaknath, Kesavananda); consensus (52nd, 61st, 73rd, 74th, 91st); controversial (38th, 39th, 42nd) and the 44th; most did not change the basic philosophy.
"""), ST(S + '09-st3', 'the basic structure doctrine and the evolution of the Constitution', """
T: basic structure doctrine | the principle that Parliament cannot amend the basic features of the Constitution, such as democracy, federalism and judicial review
T: living document | a constitution that evolves through amendments, judicial interpretation and political practice
T: judicial interpretation | the meaning given to constitutional provisions by the courts in deciding cases
Q: The basic structure doctrine was evolved in the: | Kesavananda Bharati case of 1973 | Golaknath case of 1967 | Minerva Mills case of 1980 | Indra Sawhney case of 1992
Q: Which of these is generally regarded as part of the basic structure? | Judicial review | The number of states | The salary of ministers | The name of the capital
Q: The Supreme Court ruled in the Indra Sawhney case of 1992 that reservations should normally not exceed: | 50 per cent | 25 per cent | 33 per cent | 75 per cent
Q: The Constitution is called a living document because it: | evolves through amendments and judicial interpretation | can never be changed | is written on palm leaves | is changed every year by referendum
S+: The basic structure doctrine has set limits on Parliament's power to amend the Constitution
S+: The basic structure doctrine has itself become a part of the Constitution through judicial interpretation
S+: The Indian Constitution has evolved through amendments, court judgements and political practice
S+: Judicial interpretation has expanded the meaning of rights such as the right to life
S+: The Constitution has survived because it is flexible enough to respond to new situations
S-: The basic structure doctrine allows Parliament to change any feature of the Constitution | It prevents Parliament from changing the basic features
S-: The Indian Constitution has never changed since 1950 | It has evolved through amendments, judgements and practice
S-: The basic structure doctrine was laid down by Parliament | It was laid down by the Supreme Court in the Kesavananda Bharati case
C: The basic structure doctrine protects the core of the Constitution | it prevents a temporary majority in Parliament from destroying democracy, federalism or rights
C: The Constitution is called a living document | it has adapted to new needs through amendments, judicial interpretation and political practice
C: Judicial interpretation has shaped the Constitution | courts have given new meanings to rights and limits on power in deciding cases
X: C2 D2 2 | What is the basic structure doctrine? | Laid down in Kesavananda Bharati (1973); Parliament can amend the Constitution but not its basic features such as democracy, federalism, secularism, judicial review.
X: C3 D4 4 | 'The Indian Constitution is a living document.' Explain. | Amendments when needed; judicial interpretation (basic structure, right to life); political practice and conventions; balance of stability and change; survived over seven decades.
L: D4 | Explain the basic structure doctrine and how the Constitution has evolved as a living document. | Golaknath and Kesavananda; basic features; limits on amendment; judicial interpretation – Art 21, reservations (Indra Sawhney, 50 per cent); amendments and practice; stability with change.
L: D5 | 'The basic structure doctrine strikes a balance between Parliament and the judiciary.' Critically examine. | Parliament can amend widely but not the core; protects democracy; but critics see judicial supremacy and vagueness of the 'basic structure'; acceptance over time; balanced conclusion.
""")]

CH10 = [ST(S + '10-st1', 'the philosophy of the Constitution and democratic transformation', """
T: philosophy of the Constitution | the moral values and ideals, such as liberty, equality and justice, that underlie the Constitution
T: Preamble | the introduction to the Constitution that states its basic values and goals
T: democratic transformation | peaceful change in society through democratic and constitutional means, such as breaking caste and feudal hierarchies
Q: The Preamble describes India as a sovereign, socialist, secular, democratic: | republic | monarchy | federation | confederation
Q: Which of the following values is NOT mentioned in the Preamble? | Monarchy | Justice | Liberty | Fraternity
Q: The Preamble promises justice that is social, economic and: | political | religious | military | cultural
Q: To understand the philosophy of the Constitution, it is useful to read the: | Constituent Assembly debates | budget documents | election results | police manuals
S+: The Constitution embodies a moral vision of liberty, equality, fraternity and justice
S+: The Constitution is a means of bringing about peaceful democratic transformation
S+: The Constitution limits power so that no group can dominate others
S+: The debates of the Constituent Assembly help us understand the reasons behind constitutional provisions
S+: The Preamble promises liberty of thought, expression, belief, faith and worship
S+: The Preamble promises equality of status and of opportunity
S-: The Constitution is only a legal document without any values | It embodies a moral vision of liberty, equality, fraternity and justice
S-: The Preamble describes India as a monarchy | It describes India as a sovereign, socialist, secular, democratic republic
S-: The Constitution seeks change only through violent revolution | It seeks peaceful democratic transformation
C: The Constitution is seen as a means of democratic transformation | it allows peaceful change of unjust social hierarchies through law and democratic institutions
C: We need to study the philosophy of the Constitution | its provisions can be properly understood and interpreted only in the light of its underlying values
C: The Constituent Assembly debates are important | they reveal the reasons and values behind the provisions of the Constitution
X: C2 D2 2 | What is meant by the philosophy of the Constitution? | Underlying values and moral vision – liberty, equality, fraternity, justice, dignity; found in the Preamble and Constituent Assembly debates.
X: C3 D4 4 | 'The Constitution is a means of democratic transformation.' Explain. | Limits power; protects rights; breaks caste and feudal hierarchies peacefully; reservations; universal franchise; Preamble goals of justice, liberty, equality, fraternity.
L: D4 | Explain the meaning of the philosophy of the Constitution and how the Constitution acts as a means of democratic transformation. | Moral vision; Preamble values; Constituent Assembly debates; limits on power; peaceful change; social justice; universal franchise.
"""), ST(S + '10-st2', 'the political philosophy of the Indian Constitution', """
T: individual freedom | the commitment of the Constitution to freedom of expression and freedom from arbitrary arrest
T: social justice | the commitment to correct historical injustice through measures such as reservations for Scheduled Castes and Scheduled Tribes
T: minority rights | the rights of religious and linguistic communities to preserve their culture and run their own institutions
T: principled distance | the idea in Indian secularism that the state keeps a distance from religion but may intervene to promote freedom and equality
T: asymmetric federalism | the federal arrangement in which some states have special provisions to accommodate their needs
Q: Universal adult franchise was introduced in India: | from the very beginning of the Constitution in 1950 | gradually after 1970 | only after 1989 | only for educated citizens at first
Q: Indian secularism allows the state to: | intervene in religion to promote freedom and equality | ban all religions | follow one official religion | ignore religious discrimination
Q: Reservations for Scheduled Castes and Scheduled Tribes reflect the constitutional commitment to: | social justice | monarchy | free markets | military rule
Q: The right of minorities to establish their own educational institutions reflects respect for: | diversity and minority rights | uniformity of culture | majority rule alone | centralisation
S+: The Constitution protects individual freedom, including freedom of expression and freedom from arbitrary arrest
S+: The Constitution recognises community-based rights of religious and linguistic minorities
S+: Indian secularism does not mean a wall of separation between religion and the state
S+: The state in India can provide aid to educational institutions run by religious communities
S+: Universal adult franchise was granted from the start, unlike in many Western democracies
S+: India's federalism is asymmetric, with special provisions for some states
S-: Indian secularism requires complete separation between religion and the state | It follows principled distance and allows intervention for freedom and equality
S-: The Constitution recognises only individual rights and no community rights | It also recognises the rights of religious and linguistic minorities
S-: Universal adult franchise was introduced in India only in the 1970s | It was granted from the start in 1950
C: The Constitution grants rights to minority communities | the makers believed that respect for diversity requires protecting the culture of communities
C: The Indian state can intervene in religious matters | it seeks to remove practices such as untouchability that violate equality and dignity
C: Universal adult franchise was a bold step | it trusted all adult citizens with the vote at a time when many were poor and illiterate
X: C2 D2 2 | Mention any two features of the political philosophy of the Constitution. | Individual freedom; social justice; respect for diversity and minority rights; secularism (principled distance); universal franchise; federalism; national identity.
X: C3 D3 2 | How is Indian secularism different from the Western model? | Not a wall of separation; principled distance; state can intervene to reform religion (untouchability) and give aid to minority institutions; equal respect for all religions.
X: C3 D4 4 | Explain the commitment of the Constitution to social justice and minority rights. | Reservations for SC/ST in legislatures and jobs; abolition of untouchability; minority rights to culture and institutions (Arts 29–30); respect for diversity; community rights alongside individual rights.
L: D4 | Explain the main features of the political philosophy of the Indian Constitution. | Individual freedom; social justice and reservations; respect for diversity and minority rights; secularism and principled distance; universal franchise from 1950; asymmetric federalism; national identity.
L: D5 | 'The Indian Constitution balances individual rights and community rights.' Critically examine. | Individual freedoms; minority rights; principled distance; reservations; tensions – personal laws, uniform civil code debates; balancing approach; conclusion.
"""), ST(S + '10-st3', 'procedural achievements and criticisms of the Constitution', """
T: deliberation | careful discussion and reasoning before taking decisions, practised in the Constituent Assembly
T: consensus | general agreement among members, often sought in the Constituent Assembly
T: unwieldy | a criticism that the Constitution is too long and detailed
Q: One criticism of the Indian Constitution is that it is: | unwieldy, being very long and detailed | too short | unwritten | written in a foreign language only
Q: The criticism that the Constituent Assembly was not elected by universal franchise is a claim that the Constitution is: | unrepresentative | unwieldy | alien | rigid
Q: The criticism that the Constitution borrows heavily from Western constitutions is that it is: | alien | unrepresentative | unwieldy | flexible
Q: One limitation of the Constitution is that important social and economic rights are placed in the: | Directive Principles rather than the Fundamental Rights | Preamble only | Ninth Schedule only | Seventh Schedule
S+: The Constituent Assembly reached decisions through deliberation and a spirit of accommodation
S+: The makers of the Constitution tried to reach consensus rather than simply impose majority decisions
S+: Critics say the Constitution is unwieldy because it is very long and detailed
S+: Critics say the Constitution is unrepresentative because the Constituent Assembly was not elected by universal franchise
S+: Critics say the Constitution is alien because it borrows from Western constitutions
S+: Some critics point out that gender justice within the family received little attention
S-: The Constituent Assembly was elected by universal adult franchise | It was elected indirectly by provincial assemblies on a limited franchise
S-: The Constitution has no critics | It has been criticised as unwieldy, unrepresentative and alien
S-: Social and economic rights are all Fundamental Rights in the Constitution | Many are in the Directive Principles, which are not enforceable
C: The Constitution is called a product of deliberation | the Constituent Assembly discussed every provision carefully and sought consensus
C: Some critics call the Constitution unrepresentative | the Constituent Assembly was not elected by universal adult franchise
C: The charge that the Constitution is alien is only partly valid | its borrowed ideas were adapted to Indian conditions and the values of the national movement
X: C2 D2 2 | State any two criticisms of the Indian Constitution. | Unwieldy (too long); unrepresentative (Assembly not elected by universal franchise); alien (borrowed from the West).
X: C3 D4 4 | Examine the criticisms that the Constitution is unwieldy, unrepresentative and alien. | Unwieldy – long but detailed provisions useful; unrepresentative – limited franchise but diverse and deliberative Assembly; alien – borrowed but adapted to Indian conditions; partial validity.
L: D4 | Discuss the procedural achievements and the criticisms and limitations of the Indian Constitution. | Achievements – deliberation, consensus, accommodation, legitimacy; criticisms – unwieldy, unrepresentative, alien; limitations – centralised idea of unity, gender justice, socio-economic rights in DPSP; overall assessment.
""")]

CHAPTERS = [(CH06, {}), (CH07, {}), (CH08, {}), (CH09, {}), (CH10, {})]
