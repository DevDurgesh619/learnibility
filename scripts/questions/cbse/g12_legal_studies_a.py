"""CBSE class 12 Legal Studies (chapters 1-7): fact tables for g12_hum_engine."""
from g12_hum_engine import ST

S = 'cbse-g12-legal-studies-ch'

CH01 = [ST(S + '01-st1', 'structure of courts and judicial review', """
T: judicial review | the power of the courts to examine whether a law or executive action is consistent with the Constitution and to strike it down if it is not
T: original jurisdiction | the power of a court to hear a case in the first instance
T: appellate jurisdiction | the power of a higher court to hear appeals against the decisions of lower courts
T: advisory jurisdiction | the power of the Supreme Court under Article 143 to give its opinion on a question referred by the President
T: court of record | a court whose judgments are recorded for evidence and testimony and which can punish for its contempt
T: basic structure doctrine | the principle that Parliament cannot amend the Constitution so as to destroy its essential features
Q: The Supreme Court of India is established under: | Article 124 | Article 214 | Article 32 | Article 226
Q: Disputes between the Union and one or more States fall under the Supreme Court's: | original jurisdiction under Article 131 | advisory jurisdiction | appellate jurisdiction | writ jurisdiction of High Courts
Q: The President may seek the opinion of the Supreme Court under: | Article 143 | Article 131 | Article 141 | Article 129
Q: Under Article 141, the law declared by the Supreme Court is: | binding on all courts in India | binding only on High Courts | advisory only | binding only on the Union Government
Q: The basic structure doctrine was laid down in: | Kesavananda Bharati v State of Kerala | Maneka Gandhi v Union of India | Vishaka v State of Rajasthan | M.C. Mehta v Union of India
Q: The highest civil court in a district is the court of the: | District Judge | Civil Judge (Junior Division) | Chief Judicial Magistrate | Sessions Judge
Q: The idea of judicial review is traced to the American case of: | Marbury v Madison | Rylands v Fletcher | Donoghue v Stevenson | Salomon v Salomon
M:jurisdiction: Article 131 | original jurisdiction of the Supreme Court
M:jurisdiction: Article 143 | advisory jurisdiction of the Supreme Court
M:jurisdiction: Article 32 | writ jurisdiction of the Supreme Court
M:jurisdiction: Article 226 | writ jurisdiction of the High Courts
Y: 1973 | the Supreme Court's decision laying down the basic structure doctrine in Kesavananda Bharati v State of Kerala
S+: India has an integrated judiciary with the Supreme Court at the top, High Courts in the States and subordinate courts below them
S+: Both the Supreme Court (Article 129) and the High Courts (Article 215) are courts of record
S+: Judicial review in India extends to legislative actions, executive actions and constitutional amendments
S+: Subordinate criminal courts include the Sessions Court and the courts of Judicial Magistrates
S+: Judicial review protects fundamental rights and maintains the federal balance between the Union and the States
S-: High Courts are not courts of record | Both the Supreme Court and the High Courts are courts of record
S-: The basic structure doctrine was laid down in the Maneka Gandhi case | It was laid down in Kesavananda Bharati v State of Kerala (1973)
S-: The law declared by a High Court is binding on the Supreme Court | The law declared by the Supreme Court is binding on all courts (Article 141)
C: The Supreme Court can strike down a law that violates fundamental rights | judicial review lets the courts test laws against the Constitution
C: The Supreme Court is the guardian of the Constitution | it interprets the Constitution finally and enforces fundamental rights
C: India is said to have an integrated judiciary | a single hierarchy of courts, headed by the Supreme Court, enforces both Union and State laws
X: C2 D2 2 | What is meant by judicial review? | The power of courts to examine whether a law or executive action is consistent with the Constitution and to declare it void if it is not; Article 13 makes laws inconsistent with fundamental rights void.
X: C3 D3 2 | Why is the Supreme Court called a court of record? | Its judgments are recorded for perpetual memory and used as precedents; it has power to punish for its contempt (Article 129).
X: C3 D3 3 | Explain the original, appellate and advisory jurisdiction of the Supreme Court. | Original – Centre-State and inter-State disputes (Article 131); appellate – appeals in civil, criminal and constitutional cases from High Courts; advisory – opinion on questions referred by the President (Article 143).
X: C3 D4 3 | Describe the hierarchy of courts in India. | Supreme Court at the apex; High Courts in States; subordinate courts – District Judge and civil judges on the civil side; Sessions Court and Judicial Magistrates on the criminal side.
X: C4 D4 3 | 'Judicial review is a check on the other organs of government.' Explain. | Courts can strike down unconstitutional laws and executive actions; protects fundamental rights; maintains federal balance; constitutional amendments tested against the basic structure (Kesavananda Bharati).
L: D4 | Explain the structure of the Indian judiciary and the jurisdiction of the Supreme Court. | Integrated judiciary; Supreme Court, High Courts, subordinate civil and criminal courts; original, appellate, writ, advisory jurisdiction; court of record; Article 141.
L: D5 | Discuss the doctrine of judicial review in India with reference to the basic structure doctrine. | Meaning; Article 13; review of legislation, executive action and amendments; Kesavananda Bharati (1973) basic structure; importance for rights and federalism; limits – courts do not make policy.
"""), ST(S + '01-st2', 'appointment, transfer and removal of judges', """
T: collegium system | the system in which the Chief Justice of India and senior-most judges of the Supreme Court recommend appointments and transfers of judges
T: National Judicial Appointments Commission | the body created by the 99th Constitutional Amendment to appoint judges, which the Supreme Court struck down in 2015
T: impeachment of a judge | the removal of a judge by the President after an address by both Houses of Parliament on grounds of proved misbehaviour or incapacity
T: independence of the judiciary | the principle that judges must be free from pressure by the executive and the legislature in deciding cases
Q: Judges of the Supreme Court are appointed by the: | President | Prime Minister | Parliament | Chief Justice of India alone
Q: The collegium for appointment of Supreme Court judges consists of the Chief Justice of India and the: | four senior-most judges of the Supreme Court | Law Minister | Attorney General | Chief Justices of all High Courts
Q: The NJAC was struck down by the Supreme Court in: | 2015 | 1993 | 1998 | 2010
Q: A judge of the Supreme Court can be removed on the ground of: | proved misbehaviour or incapacity | a difference of opinion with the government | a vote of the Cabinet | an order of the Chief Justice of India
Q: A judge of the Supreme Court retires at the age of: | 65 years | 62 years | 60 years | 70 years
Q: The collegium system was created by the judgment in the: | Second Judges case (1993) | Kesavananda Bharati case | First Judges case (1981) | Maneka Gandhi case
Q: Judges of High Courts retire at the age of: | 62 years | 65 years | 60 years | 58 years
Y: 2015 | the Supreme Court's striking down of the National Judicial Appointments Commission
Y: 1993 | the Second Judges case that created the collegium system
S+: The removal of a judge requires a motion passed in each House by a majority of its total membership and two-thirds of those present and voting
S+: The Judges (Inquiry) Act 1968 lays down the procedure for investigating charges against a judge
S+: The transfer of High Court judges is made by the President after consultation with the Chief Justice of India (Article 222)
S+: Security of tenure, fixed salaries charged on the Consolidated Fund and restrictions on discussing judges' conduct protect judicial independence
S+: A distinguished jurist in the President's opinion can be appointed a judge of the Supreme Court
S-: Supreme Court judges retire at 62 | They retire at 65; High Court judges retire at 62
S-: The NJAC is the present method of appointing judges | The NJAC was struck down in 2015; the collegium system continues
S-: A judge can be removed by a simple order of the President | Removal needs an address by both Houses with a special majority on proved misbehaviour or incapacity
C: The removal procedure for judges is made very difficult | judges must be protected from political pressure to keep the judiciary independent
C: The Supreme Court struck down the NJAC | it held that giving the executive a role in appointments affected the independence of the judiciary, a basic feature
C: Salaries of judges are charged on the Consolidated Fund of India | they are not subject to a vote of Parliament, which protects judicial independence
X: C2 D2 2 | What is the collegium system? | A system in which the CJI and senior-most judges of the Supreme Court recommend appointments and transfers of judges; created by the Second Judges case (1993).
X: C3 D3 2 | Why did the Supreme Court strike down the NJAC? | It held that the NJAC gave the executive a role that undermined the primacy of the judiciary in appointments and violated judicial independence, a basic feature of the Constitution.
X: C3 D3 3 | State the qualifications for appointment as a judge of the Supreme Court. | Citizen of India; judge of a High Court for at least five years, or an advocate of a High Court for at least ten years, or a distinguished jurist in the opinion of the President.
X: C3 D4 3 | Explain the procedure for the removal of a judge of the Supreme Court. | Grounds – proved misbehaviour or incapacity; motion in either House; inquiry under the Judges (Inquiry) Act 1968; address passed by each House by special majority; removal order by the President.
X: C4 D4 3 | How does the Constitution secure the independence of the judiciary? | Security of tenure; difficult removal; salaries charged on the Consolidated Fund; conduct of judges not discussed in legislature; power to punish for contempt; separation from executive; collegium.
L: D4 | Explain the appointment, transfer and removal of judges of the higher judiciary. | Appointment by President on collegium recommendation; qualifications; transfer under Article 222; removal by address of both Houses; Judges (Inquiry) Act; retirement ages.
L: D5 | Trace the evolution of the collegium system and evaluate the NJAC case. | First Judges case (1981); Second Judges case (1993) – collegium; Third Judges case (1998) – CJI and four senior-most judges; 99th Amendment and NJAC; struck down in 2015; criticism of collegium – lack of transparency.
"""), ST(S + '01-st3', 'public interest litigation and judicial activism', """
T: public interest litigation | litigation filed in a court for the protection of public interest, often by a person not directly affected
T: locus standi | the right or capacity of a person to bring an action before a court
T: epistolary jurisdiction | the practice of the Supreme Court treating letters and postcards as writ petitions
T: judicial activism | an active role of the judiciary in protecting rights and promoting justice, often by expanding the meaning of laws
T: judicial restraint | the principle that courts should avoid interfering in matters of policy that belong to the legislature and executive
Q: PIL relaxed the traditional rule of: | locus standi | res judicata | double jeopardy | sub judice
Q: The case of undertrial prisoners in Bihar that is often called the first PIL is: | Hussainara Khatoon v State of Bihar | Kesavananda Bharati v State of Kerala | Salomon v Salomon | Ashby v White
Q: Judges associated with the growth of PIL in India include: | Justice P.N. Bhagwati and Justice V.R. Krishna Iyer | Justice Fathima Beevi and Justice Leila Seth | Justice Anna Chandy and Justice M.C. Chagla | Justice H.R. Khanna alone
Q: Treating a letter written to a judge as a writ petition is called: | epistolary jurisdiction | appellate jurisdiction | advisory jurisdiction | original jurisdiction
Q: A PIL can be filed in the: | Supreme Court or a High Court | Lok Adalat only | Consumer Forum only | Gram Nyayalaya only
S+: In a PIL, any public-spirited person can approach the court on behalf of those unable to do so
S+: PILs have been used to secure the rights of prisoners, bonded labourers and the environment
S+: Judicial activism has expanded the meaning of the right to life under Article 21
S+: Misuse of PIL for publicity or private interest has been criticised by the courts
S+: The courts have laid down guidelines to prevent frivolous PILs
S-: Only the person whose right is violated can file a PIL | Any public-spirited person can file a PIL on behalf of others
S-: A PIL can be filed only through a formal petition drafted by an advocate | Courts have treated even letters and postcards as petitions
S-: Judicial activism means courts refuse to decide cases | It means an active role of the courts in protecting rights
C: The courts relaxed the rule of locus standi | poor and disadvantaged people could not themselves approach the courts to enforce their rights
C: Judicial activism has been criticised | courts sometimes enter the areas of policy that belong to the legislature and executive
C: PIL is an important tool of social justice | it brings the grievances of the voiceless before the courts
X: C2 D2 2 | What is public interest litigation? | Litigation in the Supreme Court or a High Court for protection of public interest; can be filed by any public-spirited person on behalf of those unable to approach the court.
X: C3 D3 2 | Why was the rule of locus standi relaxed? | Poor, illiterate and disadvantaged people could not approach courts; relaxation allowed public-spirited persons to seek justice for them.
X: C3 D3 3 | Explain any three features of PIL. | Relaxed locus standi; epistolary jurisdiction; non-adversarial, collaborative approach; court may appoint commissions; aim of social justice for the disadvantaged.
X: C3 D4 3 | Distinguish between judicial activism and judicial restraint. | Activism – courts take an active role, expand rights, issue directions; restraint – courts defer to the legislature and executive on policy and avoid overreach.
X: C4 D4 3 | 'PIL is a double-edged weapon.' Explain. | Benefits – justice to the poor, environmental and prisoners' rights, accountability; problems – frivolous and publicity-oriented petitions, burden on courts, judicial overreach; courts' guidelines against misuse.
L: D4 | Explain the meaning and growth of PIL in India. | Relaxed locus standi; Justices Bhagwati and Krishna Iyer; epistolary jurisdiction; Hussainara Khatoon case; areas – prisoners, bonded labour, environment; misuse and safeguards.
"""), ST(S + '01-st4', 'constitutional remedies and writs', """
T: habeas corpus | a writ ordering a person who has detained another to produce the detained person before the court so that the legality of the detention can be examined
T: mandamus | a writ commanding a public authority to perform a public duty that it has failed to perform
T: prohibition | a writ issued by a higher court to a lower court or tribunal to stop it from acting beyond its jurisdiction while the case is pending
T: certiorari | a writ issued by a higher court to quash an order already passed by a lower court or tribunal without jurisdiction or in error of law
T: quo warranto | a writ asking a person by what authority he or she holds a public office
Q: The writ meaning 'to have the body' is: | habeas corpus | mandamus | certiorari | quo warranto
Q: The writ meaning 'we command' is: | mandamus | prohibition | quo warranto | habeas corpus
Q: A writ that challenges a person's right to hold a public office is: | quo warranto | mandamus | prohibition | certiorari
Q: The writ issued to quash an order already passed by a lower court is: | certiorari | prohibition | mandamus | habeas corpus
Q: Dr B.R. Ambedkar called which Article the 'heart and soul' of the Constitution? | Article 32 | Article 226 | Article 21 | Article 14
Q: High Courts issue writs under: | Article 226 | Article 32 | Article 124 | Article 143
M:writ: Habeas corpus | illegal detention
M:writ: Mandamus | public duty not performed
M:writ: Prohibition | stop a lower court during proceedings
M:writ: Certiorari | quash a lower court's order
M:writ: Quo warranto | unlawful holding of public office
S+: The right to constitutional remedies under Article 32 is itself a fundamental right
S+: The writ jurisdiction of High Courts under Article 226 is wider, as it extends to fundamental rights and 'any other purpose'
S+: Mandamus cannot be issued against the President or the Governors
S+: Prohibition is issued while proceedings are pending; certiorari is issued after the order is passed
S+: Habeas corpus can be issued against both public authorities and private persons
S-: The writ of mandamus can be issued against the President | Mandamus does not lie against the President or a Governor
S-: Certiorari is issued before a lower court passes its order | Prohibition is issued during proceedings; certiorari after the order
S-: Article 226 is narrower than Article 32 | Article 226 is wider, as High Courts can issue writs for any other purpose as well
C: Habeas corpus protects personal liberty | it requires the detaining authority to produce the person and justify the detention
C: Article 32 is called the heart and soul of the Constitution | without a remedy, fundamental rights would be meaningless
C: Quo warranto prevents usurpation of public office | the holder must show legal authority to hold the office
X: C2 D2 2 | Distinguish between prohibition and certiorari. | Prohibition – issued during pending proceedings to stop a lower court acting beyond jurisdiction; certiorari – issued after an order is passed, to quash it.
X: C3 D3 2 | Why is Article 32 called the heart and soul of the Constitution? | It makes the right to approach the Supreme Court for enforcing fundamental rights itself a fundamental right; without remedies rights are meaningless (Ambedkar).
X: C3 D3 3 | Explain the writs of habeas corpus, mandamus and quo warranto. | Habeas corpus – produce the detained person, tests legality of detention; mandamus – command to perform public duty; quo warranto – by what authority a person holds a public office.
X: C3 D4 3 | Compare the writ jurisdiction of the Supreme Court and the High Courts. | SC – Article 32, only fundamental rights, itself a fundamental right; HC – Article 226, fundamental rights and any other purpose, discretionary, territorial limits.
X: C4 D4 3 | 'Writs are the guardians of fundamental rights.' Explain. | Five writs give speedy remedies; habeas corpus for liberty; mandamus for public duties; prohibition and certiorari keep lower courts within jurisdiction; quo warranto prevents illegal office holding.
L: D4 | Explain the five writs that the Supreme Court and the High Courts can issue. | Habeas corpus, mandamus, prohibition, certiorari, quo warranto – meaning, against whom, examples; Articles 32 and 226.
"""),
]

CH02 = [ST(S + '02-st1', 'adversarial and inquisitorial systems; need for ADR', """
T: adversarial system | a system of justice in which two opposing parties present their cases and a neutral judge decides on the evidence placed before the court
T: inquisitorial system | a system of justice in which the judge actively investigates the facts of the case
T: alternative dispute resolution | methods of settling disputes outside the regular courts, such as arbitration, conciliation, mediation, negotiation and Lok Adalats
T: Section 89 of the Code of Civil Procedure | the provision that allows a civil court to refer a dispute to arbitration, conciliation, judicial settlement including Lok Adalat, or mediation
Q: India mainly follows the: | adversarial system | inquisitorial system | theocratic system | tribal system
Q: The inquisitorial system is associated with countries following: | civil law, such as France | common law, such as England | customary law only | religious law only
Q: In the adversarial system the judge acts as a: | neutral umpire | chief investigator | prosecutor | defence counsel
Q: Reference of a civil dispute to ADR by the court is provided in: | Section 89 of the Code of Civil Procedure | Article 32 | Section 10 of the Contract Act | Article 300A
Q: Which of these is NOT a method of ADR? | Trial in a Sessions Court | Arbitration | Mediation | Lok Adalat
S+: In the adversarial system each party gathers and presents its own evidence and witnesses are cross-examined
S+: Huge pendency of cases, delay and high costs created the need for ADR in India
S+: ADR methods are usually quicker, cheaper, informal and confidential
S+: ADR helps preserve relationships between the parties because it is less hostile than litigation
S+: In the inquisitorial system the judge questions witnesses and directs the inquiry
S-: In the adversarial system the judge investigates the case | The judge is a neutral umpire; the parties present the case
S-: ADR completely replaces the courts | ADR supplements the courts and reduces their burden
S-: India follows the inquisitorial system | India mainly follows the adversarial system inherited from England
C: ADR is needed in India | courts face a huge backlog of cases, and litigation is slow and costly
C: ADR helps maintain relationships | the parties work towards a mutually acceptable settlement instead of a win-lose verdict
C: The adversarial system is criticised as expensive | the outcome depends heavily on the skill of lawyers that parties must pay for
X: C2 D2 2 | Distinguish between the adversarial and inquisitorial systems. | Adversarial – parties present evidence, judge is a neutral umpire (India, England); inquisitorial – judge actively investigates facts (France and civil law countries).
X: C3 D3 2 | Why is ADR needed in India? | Pendency of cases; delay; high cost of litigation; formal procedure; ADR is quick, cheap and flexible.
X: C3 D3 3 | State any three advantages of ADR. | Speedy; less expensive; informal and flexible; confidential; preserves relationships; reduces burden on courts; parties control outcome.
X: C3 D4 3 | Explain the main features of the adversarial system. | Two opposing parties; judge as neutral umpire; parties collect and present evidence; cross-examination; rules of evidence and procedure; decision on material before the court.
X: C4 D4 3 | 'The adversarial system favours the rich.' Examine. | Outcome depends on lawyers' skill and resources; costly and lengthy; poor may not afford good counsel; legal aid and ADR reduce this imbalance.
L: D4 | Compare the adversarial and inquisitorial systems and explain the need for ADR in India. | Features of both; role of judge and parties; India's adversarial system; pendency, delay, cost; ADR methods and advantages; Section 89 CPC.
"""), ST(S + '02-st2', 'arbitration and conciliation', """
T: arbitration | a method of ADR in which the parties refer their dispute to one or more neutral persons whose decision, called an award, is binding
T: arbitration agreement | an agreement in writing by the parties to submit present or future disputes to arbitration
T: arbitral award | the decision of an arbitral tribunal, which is binding on the parties and enforceable like a decree of a court
T: conciliation | a method of ADR in which a conciliator assists the parties to reach an amicable settlement and may propose terms of settlement
T: UNCITRAL Model Law | the model law on international commercial arbitration on which India's Arbitration and Conciliation Act 1996 is based
Q: Arbitration in India is governed by the: | Arbitration and Conciliation Act 1996 | Legal Services Authorities Act 1987 | Indian Contract Act 1872 | Code of Criminal Procedure 1973
Q: The Arbitration and Conciliation Act 1996 is based on the: | UNCITRAL Model Law | Treaty of Versailles | Universal Declaration of Human Rights | TRIPS Agreement
Q: An arbitration agreement must be: | in writing | oral | registered with the police | approved by Parliament
Q: Under the 1996 Act, the number of arbitrators fixed by the parties must be: | an odd number | an even number | exactly four | at least seven
Q: A signed conciliation settlement agreement has the same status as: | an arbitral award on agreed terms | a police report | an advisory opinion | a parliamentary resolution
Q: An arbitral award can be challenged by an application to set it aside under: | Section 34 of the Act | Section 89 CPC | Article 143 | Section 25 of the Contract Act
Y: 1996 | the enactment of the Arbitration and Conciliation Act
S+: Part I of the Arbitration and Conciliation Act deals with domestic arbitration and Part III with conciliation
S+: Part II of the Act provides for enforcement of foreign awards under the New York and Geneva Conventions
S+: An arbitral award is final and binding and is enforced as if it were a decree of the court
S+: The decision of a conciliator is not binding unless the parties sign a settlement agreement
S+: Parties are free to choose the arbitrators, the place and the procedure of arbitration
S-: A conciliator's suggestions are binding on the parties | They bind only when the parties sign a settlement agreement
S-: An arbitration agreement may be oral | It must be in writing
S-: An arbitral award cannot be enforced by a court | It is enforced like a decree of the court
C: Arbitration is popular for commercial disputes | it is quicker, confidential, and the parties can choose experts as arbitrators
C: An arbitral award can be enforced by a court | the Act treats the award as if it were a decree of the court
C: Conciliation is less formal than arbitration | the conciliator only assists the parties and does not impose a decision
X: C2 D2 2 | Distinguish between arbitration and conciliation. | Arbitration – arbitrator gives a binding award after hearing parties; conciliation – conciliator helps parties settle; outcome binding only when they sign a settlement agreement.
X: C3 D3 2 | What is an arbitration agreement? | A written agreement between parties to submit present or future disputes to arbitration; may be a clause in a contract or a separate agreement.
X: C3 D3 3 | Explain any three advantages of arbitration. | Speedy; confidential; choice of expert arbitrator; flexible procedure; binding and enforceable award; limited grounds for challenge; less costly than litigation.
X: C3 D4 3 | Explain the process of conciliation under the Arbitration and Conciliation Act 1996. | Invitation to conciliate and acceptance; appointment of conciliator; parties submit statements; conciliator assists and may propose terms; settlement agreement signed; same status as arbitral award.
X: C4 D4 3 | 'An arbitral award is final, yet not beyond the court.' Explain. | Award is binding and enforced as a decree; but may be set aside on limited grounds under Section 34, such as incapacity, invalid agreement, lack of notice, conflict with public policy.
L: D4 | Explain arbitration under the Arbitration and Conciliation Act 1996. | Basis on UNCITRAL Model Law; arbitration agreement in writing; appointment of arbitrators, odd number; procedure; award binding, enforced like decree; setting aside under Section 34; foreign awards.
"""), ST(S + '02-st3', 'mediation, negotiation and Lok Adalats', """
T: mediation | a voluntary process in which a neutral mediator helps the parties communicate and reach their own settlement
T: negotiation | a process in which the parties discuss their dispute directly, without a third party, to reach a settlement
T: Lok Adalat | a 'people's court' set up under the Legal Services Authorities Act 1987 to settle disputes by compromise
T: Permanent Lok Adalat | a Lok Adalat for disputes relating to public utility services, which can decide a case on merits if settlement fails
Q: A dispute settled by the parties themselves without any third party is settled by: | negotiation | arbitration | mediation | Lok Adalat
Q: Lok Adalats get statutory status under the: | Legal Services Authorities Act 1987 | Arbitration and Conciliation Act 1996 | Advocates Act 1961 | Code of Civil Procedure 1908 only
Q: An award of a Lok Adalat is: | final and deemed to be a decree of a civil court, with no appeal | open to appeal in the High Court | advisory only | binding only on one party
Q: When a case pending in court is settled in a Lok Adalat, the court fee paid is: | refunded | doubled | forfeited | paid to the State
Q: Permanent Lok Adalats deal with disputes relating to: | public utility services | murder trials | constitutional amendments | international treaties
Q: The first Lok Adalat camp was organised in: | Gujarat | Kerala | Punjab | Assam
Y: 1987 | the enactment of the Legal Services Authorities Act
S+: In mediation the mediator does not impose a decision; the parties reach their own agreement
S+: Lok Adalats decide cases on the basis of compromise and settlement between the parties
S+: No court fee is payable for cases taken to a Lok Adalat
S+: Matrimonial, family, motor accident claims and bank recovery disputes are often settled in Lok Adalats
S+: Lok Adalats cannot settle non-compoundable criminal offences
S-: Lok Adalat awards can be appealed in a higher court | The award is final, and no appeal lies against it
S-: A mediator decides the dispute and imposes a binding decision | A mediator only helps the parties reach their own settlement
S-: Negotiation requires a neutral third party | Negotiation is conducted directly between the parties
C: Lok Adalats are popular with ordinary people | they are free, quick and informal and give a final settlement
C: Mediation preserves relationships | the parties themselves craft a solution acceptable to both
C: No appeal lies against a Lok Adalat award | the award is based on the consent of both parties
X: C2 D2 2 | Distinguish between mediation and negotiation. | Mediation – neutral mediator helps parties reach their own settlement; negotiation – parties discuss directly without any third party.
X: C3 D3 2 | Why is no appeal allowed against an award of a Lok Adalat? | The award is based on the compromise and consent of both parties; it is deemed a decree of a civil court and is final.
X: C3 D3 3 | State any three features of Lok Adalats. | Statutory under Legal Services Authorities Act 1987; settlement by compromise; no court fee, refund of fee paid; award deemed a decree, final, no appeal; informal procedure.
X: C3 D4 3 | Explain Permanent Lok Adalats. | For public utility services such as transport, post, telecom, electricity, water, hospitals; first try conciliation; if settlement fails, can decide on merits; award final and binding.
X: C4 D4 3 | 'Lok Adalats deliver speedy justice to the common man.' Justify. | No court fee; informal procedure; quick disposal of large numbers of cases; final award without appeal; reduces court pendency; settles motor accident, family and bank disputes.
L: D4 | Explain mediation, negotiation and Lok Adalats as methods of ADR. | Mediation – process, role of mediator, voluntary; negotiation – direct talks; Lok Adalats – Legal Services Authorities Act 1987, features, award, Permanent Lok Adalats.
"""), ST(S + '02-st4', 'tribunal adjudication', """
T: tribunal | a quasi-judicial body set up to decide disputes in a specialised field, such as service matters, taxation or the environment
T: administrative tribunal | a tribunal under Article 323A that decides disputes about recruitment and conditions of service of public servants
T: Central Administrative Tribunal | the tribunal set up under the Administrative Tribunals Act 1985 to decide service disputes of Union government employees
T: National Green Tribunal | the specialised tribunal set up in 2010 to decide environmental disputes
Q: Articles 323A and 323B were added to the Constitution by the: | 42nd Amendment (1976) | 44th Amendment (1978) | 86th Amendment (2002) | 99th Amendment (2014)
Q: Administrative tribunals for service matters are provided under: | Article 323A | Article 323B | Article 32 | Article 39A
Q: Tribunals for taxation, industrial disputes and land reforms are provided under: | Article 323B | Article 323A | Article 226 | Article 51
Q: The case holding that tribunal decisions are subject to the writ jurisdiction of High Courts is: | L. Chandra Kumar v Union of India | Kesavananda Bharati v State of Kerala | Salomon v Salomon | Hussainara Khatoon v State of Bihar
Q: The Central Administrative Tribunal was set up under the: | Administrative Tribunals Act 1985 | Legal Services Authorities Act 1987 | Arbitration and Conciliation Act 1996 | Environment (Protection) Act 1986
Y: 1985 | the enactment of the Administrative Tribunals Act
S+: Tribunals were created to reduce the burden on courts and to provide specialised and speedy justice
S+: Tribunals follow principles of natural justice but are not bound by the strict procedure of the Code of Civil Procedure
S+: Members of tribunals include judicial members and expert or technical members
S+: Decisions of tribunals are subject to judicial review by the High Courts under Articles 226 and 227
S+: The National Green Tribunal was set up under the National Green Tribunal Act 2010
S-: Decisions of tribunals cannot be reviewed by any court | They are subject to judicial review by the High Courts (L. Chandra Kumar case)
S-: Tribunals are bound by the strict procedure of the Code of Civil Procedure | They follow natural justice and a flexible procedure
S-: Article 323A deals with tax tribunals | Article 323A deals with administrative (service) tribunals; tax tribunals fall under Article 323B
C: Tribunals have expert members | they decide technical disputes that need specialised knowledge
C: Tribunals provide speedy justice | they follow a simple procedure and deal with one specialised area
C: The Supreme Court held tribunal decisions subject to High Court review | judicial review is part of the basic structure of the Constitution
X: C2 D2 2 | What is a tribunal? | A quasi-judicial body set up to decide disputes in a specialised field; e.g. Central Administrative Tribunal, National Green Tribunal.
X: C3 D3 2 | Distinguish between Article 323A and Article 323B. | 323A – administrative tribunals for service matters of public servants (Parliament only); 323B – tribunals for tax, industrial disputes, land reforms, elections and other matters.
X: C3 D3 3 | State any three advantages of tribunal adjudication. | Speedy; specialised expert members; less formal and less costly; reduces burden on courts; flexible procedure based on natural justice.
X: C3 D4 3 | Compare a tribunal with a regular court. | Tribunal – specialised field, judicial and expert members, flexible procedure, part of executive set-up; court – general jurisdiction, judges only, strict procedure under CPC and evidence law.
X: C4 D4 3 | Explain the significance of L. Chandra Kumar v Union of India for tribunals. | Held that judicial review by High Courts and the Supreme Court is a basic feature; tribunals cannot exclude it; tribunal decisions subject to High Court review under Articles 226 and 227.
L: D4 | Explain tribunal adjudication in India with reference to Articles 323A and 323B. | Meaning; 42nd Amendment 1976; Article 323A – service matters, CAT under 1985 Act; Article 323B – tax, industrial, land, elections; advantages; L. Chandra Kumar case; NGT.
"""),
]

CH03 = [ST(S + '03-st1', 'essentials of a valid contract', """
T: contract | an agreement enforceable by law (Section 2(h) of the Indian Contract Act 1872)
T: agreement | every promise and every set of promises forming the consideration for each other (Section 2(e))
T: promise | a proposal that has been accepted (Section 2(b))
T: void agreement | an agreement not enforceable by law (Section 2(g))
T: voidable contract | an agreement enforceable by law at the option of one party but not at the option of the other (Section 2(i))
T: quasi-contract | an obligation imposed by law, though there is no agreement, to prevent unjust enrichment
Q: The Indian Contract Act was passed in: | 1872 | 1882 | 1860 | 1932
Q: A contract is defined as an agreement enforceable by law in: | Section 2(h) | Section 2(a) | Section 10 | Section 56
Q: The essentials of a valid contract are listed in: | Section 10 | Section 2(d) | Section 73 | Section 25
Q: 'All contracts are agreements but all agreements are not contracts' because: | only agreements enforceable by law are contracts | agreements are always written | contracts never need consent | agreements need registration
Q: An agreement to go for a movie with a friend is not a contract because: | there is no intention to create legal relations | it is oral | it lacks a stamp | it involves only two persons
Y: 1872 | the enactment of the Indian Contract Act
S+: A valid contract needs free consent of competent parties, lawful consideration and a lawful object
S+: The agreement must not be one expressly declared void by the Act
S+: The parties must intend to create legal relations; social and domestic agreements are generally not contracts
S+: The terms of a contract must be certain and capable of being performed
S+: A contract may be oral or written, unless a law requires writing or registration
S-: Every agreement is a contract | Only agreements enforceable by law are contracts
S-: A contract must always be in writing | It may be oral unless a law requires writing
S-: A void agreement is enforceable at the option of one party | That is a voidable contract; a void agreement is not enforceable at all
C: A social agreement such as a dinner invitation is not a contract | the parties do not intend to create legal relations
C: An agreement with uncertain terms is void | the court cannot enforce terms whose meaning cannot be ascertained
C: All contracts are agreements but not all agreements are contracts | only agreements that satisfy Section 10 are enforceable by law
X: C2 D2 2 | Distinguish between a void agreement and a voidable contract. | Void – not enforceable by law at all (Section 2(g)); voidable – enforceable at the option of one party, e.g. consent obtained by coercion (Section 2(i)).
X: C3 D3 2 | 'All contracts are agreements but all agreements are not contracts.' Explain. | An agreement becomes a contract only when enforceable by law – needs free consent, competent parties, lawful consideration and object (Section 10); social agreements are not contracts.
X: C3 D3 3 | State any three essentials of a valid contract. | Offer and acceptance; intention to create legal relations; lawful consideration; capacity of parties; free consent; lawful object; certainty; not expressly declared void.
X: C3 D4 3 | Explain the concept of quasi-contract with an example. | Obligation imposed by law without an agreement, to prevent unjust enrichment; e.g. goods delivered by mistake must be returned or paid for; money paid by mistake must be repaid.
X: C4 D4 3 | 'Intention to create legal relations is essential for a contract.' Examine. | Social and domestic agreements not enforceable; commercial agreements presumed to have intention; examples – dinner invitation versus sale of goods.
L: D4 | Explain the essentials of a valid contract under the Indian Contract Act 1872. | Definition Section 2(h); offer and acceptance; intention; consideration; capacity; free consent; lawful object; certainty; possibility; not declared void; legal formalities.
L: D5 | Classify contracts on the basis of validity and explain each. | Valid; void agreement; voidable contract; illegal agreement; unenforceable; quasi-contract – meaning and examples of each.
"""), ST(S + '03-st2', 'offer, acceptance and consideration', """
T: proposal | the signification by one person to another of willingness to do or abstain from doing something, with a view to obtaining the other's assent (Section 2(a))
T: acceptance | the assent of the person to whom a proposal is made, which turns the proposal into a promise
T: invitation to offer | a statement inviting others to make an offer, such as a price list or display of goods in a shop
T: general offer | an offer made to the public at large, which anyone who fulfils its conditions can accept
T: counter-offer | a reply that changes the terms of the original offer and therefore rejects it
T: consideration | something done or abstained from at the desire of the promisor, which is the price for the promise (Section 2(d))
Q: The case of Carlill v Carbolic Smoke Ball Co. is related to: | general offer | minor's agreement | absolute liability | lifting the corporate veil
Q: The display of goods with price tags in a shop is: | an invitation to offer | an offer | an acceptance | a counter-offer
Q: Acceptance must be: | absolute and unqualified | conditional | silent | made after the offer lapses
Q: Under Indian law, consideration may move from: | the promisee or any other person | the promisee only | the promisor only | the court
Q: Lalman Shukla v Gauri Dutt held that: | an offer cannot be accepted without knowledge of it | silence is acceptance | consideration must be adequate | a minor can contract
Q: Durga Prasad v Baldeo held that consideration must be given: | at the desire of the promisor | at the desire of a third party | at the desire of the government | by a court order
Q: Silence of the offeree is generally: | not acceptance | valid acceptance | a counter-offer | consideration
S+: An offer may be express or implied, specific or general
S+: Communication of acceptance is complete against the proposer when it is put in the course of transmission to him
S+: Consideration may be past, present or future
S+: Consideration need not be adequate, but it must be real and lawful
S+: Section 25 makes an agreement without consideration valid when made in writing and registered out of natural love and affection
S+: A promise to pay a time-barred debt, made in writing and signed, is valid without fresh consideration
S-: Consideration must always move from the promisee | Under Indian law it may move from the promisee or any other person
S-: A price tag on goods in a shop is an offer | It is an invitation to offer; the buyer makes the offer
S-: Silence amounts to acceptance | Acceptance must be communicated; silence is generally not acceptance
C: A reply that changes the terms of an offer does not create a contract | it is a counter-offer that rejects the original offer
C: A person who returns a lost item without knowing of a reward cannot claim it | an offer cannot be accepted without knowledge of it
C: An agreement made out of natural love and affection may be valid without consideration | Section 25 makes it an exception when it is in writing and registered
X: C2 D2 2 | Distinguish between an offer and an invitation to offer. | Offer – willingness to be bound on acceptance; invitation to offer – invites others to make offers, e.g. price lists, display of goods, advertisements.
X: C3 D3 2 | What is meant by 'no consideration, no contract'? State one exception. | An agreement without consideration is void; exceptions – natural love and affection (written, registered), past voluntary service, time-barred debt, gift actually made.
X: C3 D3 3 | State any three rules regarding a valid acceptance. | Absolute and unqualified; communicated to the offeror; in the prescribed or usual manner; given within time; by the person to whom the offer is made; knowledge of the offer.
X: C3 D4 3 | Explain the rules of a valid offer. | Intention to create legal relations; definite and certain terms; communicated to offeree; distinct from invitation to offer; may be general or specific; may not contain a term that silence is acceptance.
X: C4 D4 3 | Explain the importance of Carlill v Carbolic Smoke Ball Co. | General offer made through an advertisement; performance of conditions is acceptance; no need to communicate acceptance; reward claimable by anyone fulfilling terms.
L: D4 | Explain the rules regarding offer, acceptance and consideration. | Offer – meaning, kinds, rules, invitation to offer; acceptance – absolute, communicated, mode; consideration – meaning, rules, past/present/future, may move from any person, exceptions in Section 25.
"""), ST(S + '03-st3', 'capacity, free consent and void, voidable and illegal agreements', """
T: coercion | committing or threatening to commit an act forbidden by the Indian Penal Code, or unlawfully detaining property, to make a person enter an agreement (Section 15)
T: undue influence | a situation where one party is in a position to dominate the will of the other and uses it to obtain an unfair advantage (Section 16)
T: fraud | a deliberate false representation or concealment of facts with intent to deceive the other party to enter a contract (Section 17)
T: misrepresentation | an innocent false statement of fact made without intent to deceive (Section 18)
T: free consent | consent not caused by coercion, undue influence, fraud, misrepresentation or mistake (Section 14)
T: wagering agreement | an agreement to pay money on the happening of an uncertain event, declared void by Section 30
Q: A person is competent to contract if he or she has attained majority, is of sound mind and: | is not disqualified by law | owns property | is literate | is employed
Q: Mohori Bibee v Dharmodas Ghose held that an agreement with a minor is: | void ab initio | voidable | valid | illegal and punishable
Q: A contract induced by coercion is: | voidable at the option of the party whose consent was caused | void | valid | illegal
Q: An agreement in which both parties are under a mistake as to a fact essential to it is: | void | voidable | valid | illegal
Q: A wagering agreement is: | void | voidable | valid | enforceable
Q: Capacity to contract is dealt with in: | Section 11 | Section 2(h) | Section 73 | Section 56
M:consent: Coercion | Section 15
M:consent: Undue influence | Section 16
M:consent: Fraud | Section 17
M:consent: Misrepresentation | Section 18
S+: An agreement with a minor is void ab initio, and the minor cannot ratify it on attaining majority
S+: A minor can be a beneficiary of a contract but cannot be bound by it
S+: Contracts induced by coercion, undue influence, fraud or misrepresentation are voidable
S+: Agreements in restraint of marriage, trade or legal proceedings are void
S+: An agreement with an unlawful object or consideration is void under Section 23
S-: A minor's agreement is voidable at the minor's option | It is void ab initio (Mohori Bibee v Dharmodas Ghose)
S-: A mistake of law in India makes a contract void | A mistake as to Indian law does not make a contract voidable; mutual mistake of fact makes it void
S-: Misrepresentation involves an intention to deceive | Misrepresentation is innocent; fraud involves intent to deceive
C: An agreement with a minor is void | the law protects minors who may not understand the consequences of their acts
C: A contract induced by fraud is voidable | the consent of the deceived party was not free
C: A wagering agreement is not enforced by courts | Section 30 declares agreements by way of wager void
X: C2 D2 2 | Distinguish between fraud and misrepresentation. | Fraud – deliberate false representation with intent to deceive (Section 17); misrepresentation – innocent false statement without intent to deceive (Section 18); both make contract voidable.
X: C3 D3 2 | What is the effect of an agreement with a minor? | Void ab initio; cannot be ratified on majority; no estoppel against minor; minor can be a beneficiary; Mohori Bibee v Dharmodas Ghose.
X: C3 D3 3 | Explain the elements that destroy free consent. | Coercion (Section 15); undue influence (Section 16); fraud (Section 17); misrepresentation (Section 18); mistake (Sections 20–22).
X: C3 D4 3 | Distinguish between coercion and undue influence. | Coercion – threat of an act forbidden by penal law or unlawful detention of property; undue influence – abuse of a dominating position of trust; both voidable.
X: C4 D4 3 | Explain any three agreements expressly declared void by the Indian Contract Act. | Restraint of marriage (Section 26); restraint of trade (Section 27); restraint of legal proceedings (Section 28); uncertain agreements (Section 29); wagering agreements (Section 30); impossible acts (Section 56).
L: D4 | Explain capacity to contract and free consent under the Indian Contract Act. | Section 11 – majority, sound mind, not disqualified; minor's agreements void; Section 14 free consent; coercion, undue influence, fraud, misrepresentation, mistake; effects.
L: D5 | Distinguish between void, voidable and illegal agreements with examples. | Void – not enforceable (wager); voidable – at option of aggrieved party (coercion); illegal – forbidden by law, collateral agreements also void (smuggling); consequences of each.
"""), ST(S + '03-st4', 'discharge of contract and remedies for breach', """
T: discharge of contract | the termination of the contractual relationship between the parties
T: doctrine of frustration | the rule in Section 56 that a contract becomes void when its performance becomes impossible or unlawful after it is made
T: novation | the substitution of a new contract for the original one (Section 62)
T: anticipatory breach | a breach that occurs when a party refuses to perform before the due date of performance
T: specific performance | an order of the court directing a party to perform the contract as agreed
T: injunction | an order of the court restraining a party from doing an act in breach of contract
T: quantum meruit | a claim for payment 'as much as is earned' for work done under a contract
Q: Damages for breach of contract are provided under: | Section 73 | Section 10 | Section 2(h) | Section 25
Q: The rule of remoteness of damages was laid down in: | Hadley v Baxendale | Carlill v Carbolic Smoke Ball Co. | Mohori Bibee v Dharmodas Ghose | Rylands v Fletcher
Q: When a concert hall is destroyed by fire before the date of performance, the contract is discharged by: | impossibility of performance | mutual agreement | breach | novation
Q: Specific performance is granted under the: | Specific Relief Act 1963 | Indian Contract Act Section 10 | Transfer of Property Act 1882 | Companies Act 2013
Q: Substituting a new contract for an existing one is: | novation | rescission | remission | alteration
Q: Refusal to perform a contract before the date fixed for performance is: | anticipatory breach | actual breach | frustration | novation
S+: A contract may be discharged by performance, mutual agreement, impossibility, lapse of time, operation of law or breach
S+: Under Section 73, damages are given for loss arising naturally from the breach or contemplated by the parties
S+: Remote and indirect losses are not compensated
S+: Rescission, damages, specific performance, injunction and quantum meruit are remedies for breach
S+: Remission means acceptance of a lesser performance than what was promised (Section 63)
S-: Damages are given for every remote loss caused by the breach | Only losses arising naturally or contemplated by the parties are compensated
S-: Frustration makes a contract voidable | Under Section 56 it becomes void
S-: Anticipatory breach occurs on the date of performance | It occurs before the due date of performance
C: A contract becomes void when performance becomes impossible after it is made | Section 56 discharges the parties by the doctrine of frustration
C: Damages are not given for remote losses | Hadley v Baxendale limits damages to losses that arise naturally or were contemplated
C: Courts grant specific performance in some cases | money cannot adequately compensate for breach, e.g. sale of unique property
X: C2 D2 2 | Distinguish between actual and anticipatory breach. | Actual – failure to perform on the due date; anticipatory – refusal before the due date, express or implied by conduct.
X: C3 D3 2 | What is the doctrine of frustration? | Under Section 56, a contract becomes void when performance becomes impossible or unlawful after it is made, e.g. destruction of subject matter, change of law.
X: C3 D3 3 | Explain any three modes of discharge of contract. | Performance; mutual agreement – novation, rescission, alteration, remission; impossibility; lapse of time; operation of law; breach.
X: C3 D4 3 | Explain the rules regarding damages under Section 73. | Compensation for loss arising naturally or contemplated; no remote or indirect loss (Hadley v Baxendale); compensatory not punitive; duty to mitigate loss.
X: C4 D4 3 | Explain any three remedies available for breach of contract. | Rescission; damages; specific performance; injunction; quantum meruit – meaning and when available.
L: D4 | Explain the modes of discharge of a contract. | Performance; mutual agreement (novation, rescission, alteration, remission); impossibility (Section 56); lapse of time; operation of law; breach – actual and anticipatory.
L: D5 | Discuss the remedies available to the aggrieved party for breach of contract. | Rescission; damages – ordinary, special, nominal, Section 73, Hadley v Baxendale; specific performance; injunction; quantum meruit; examples.
"""),
]

CH04 = [ST(S + '04-st1', 'meaning and essentials of a tort', """
T: tort | a civil wrong, other than a breach of contract, for which the remedy is an action for unliquidated damages
T: injuria sine damno | the violation of a legal right without actual loss, which is actionable
T: damnum sine injuria | actual loss without the violation of a legal right, which is not actionable
T: unliquidated damages | damages not fixed in advance but determined by the court
T: crime | a public wrong against society for which the State prosecutes the offender and punishment is imposed
Q: The word 'tort' is derived from the Latin word 'tortum', meaning: | twisted or crooked | to command | to protect | to agree
Q: Ashby v White is an example of: | injuria sine damno | damnum sine injuria | strict liability | vicarious liability
Q: The Gloucester Grammar School case is an example of: | damnum sine injuria | injuria sine damno | absolute liability | novation
Q: The remedy in tort is mainly: | unliquidated damages | imprisonment | fine to the State | specific performance
Q: In a crime, the case is filed by: | the State | the victim only | a civil court | an arbitrator
S+: The essentials of a tort are a wrongful act or omission, legal damage and a legal remedy
S+: In tort the duty is fixed by law, while in contract the duty is fixed by the parties
S+: The same act may be both a tort and a crime, such as assault
S+: Legal damage means the violation of a legal right, not necessarily actual loss
S+: In a crime the offender is punished, while in a tort the injured person is compensated
S-: Damnum sine injuria is actionable | Loss without violation of a legal right is not actionable
S-: In tort, the duty arises from an agreement between the parties | The duty in tort is fixed by law
S-: A tort is a public wrong prosecuted by the State | A tort is a private civil wrong; a crime is a public wrong
C: Opening a rival school that reduces another school's income is not a tort | it causes loss without violating any legal right (damnum sine injuria)
C: Wrongfully refusing a voter the right to vote is a tort | the violation of a legal right is actionable even without actual loss
C: An act may be both a tort and a crime | it injures a private person and also harms society as a whole
X: C2 D2 2 | Distinguish between injuria sine damno and damnum sine injuria. | Injuria sine damno – violation of legal right without loss, actionable (Ashby v White); damnum sine injuria – loss without violation of legal right, not actionable (Gloucester Grammar School).
X: C3 D3 2 | How is a tort different from a breach of contract? | Tort – duty fixed by law, towards persons generally, unliquidated damages; contract – duty fixed by parties, towards specific persons, damages often based on contract.
X: C3 D3 3 | Explain the essentials of a tort. | Wrongful act or omission; legal damage (violation of a legal right); legal remedy of unliquidated damages.
X: C3 D4 3 | Distinguish between a tort and a crime. | Tort – private wrong, civil proceedings by victim, compensation; crime – public wrong, prosecuted by State, punishment; same act may be both.
X: C4 D4 3 | 'Every loss is not a legal injury.' Explain with cases. | Damnum sine injuria – loss without violation of right not actionable (Gloucester Grammar School); injuria sine damno – violation without loss actionable (Ashby v White).
L: D4 | What is a tort? Explain its essentials and distinguish it from a crime and a breach of contract. | Definition; wrongful act, legal damage, legal remedy; injuria sine damno and damnum sine injuria; differences with crime and contract.
"""), ST(S + '04-st2', 'general defences in torts', """
T: volenti non fit injuria | the defence that a person who voluntarily consents to a risk cannot claim damages for harm arising from it
T: act of God | the defence that harm was caused by natural forces so extraordinary that they could not be foreseen or guarded against
T: inevitable accident | the defence that harm was caused by an accident that could not have been avoided by reasonable care
T: private defence | the defence that reasonable force was used to protect one's person or property
T: necessity | the defence that harm was caused to prevent a greater harm
T: statutory authority | the defence that the act was authorised by a statute
Q: A spectator injured at a car race who knew of the risk cannot claim damages because of: | volenti non fit injuria | act of God | necessity | statutory authority
Q: Nichols v Marsland, where unusually heavy rain broke artificial lakes, is related to: | act of God | volenti non fit injuria | private defence | mistake
Q: Stanley v Powell, where a pellet ricocheted off a tree and hit a person, is related to: | inevitable accident | act of God | necessity | volenti non fit injuria
Q: The defence of volenti non fit injuria does NOT apply to: | rescue cases | spectators at a game | players in a sport | patients consenting to surgery
Q: Pulling down a house to stop a fire from spreading may be defended by: | necessity | volenti non fit injuria | act of God | mistake
S+: Consent under volenti non fit injuria must be free and given with knowledge of the risk
S+: Mere knowledge of a risk does not mean consent to it
S+: In private defence the force used must be reasonable and proportionate
S+: An act of God involves natural forces and an event that could not reasonably be anticipated
S+: Statutory authority protects an act authorised by law if done without negligence
S-: Mere knowledge of a risk always amounts to consent | Knowledge is not consent; the person must voluntarily agree to the risk
S-: Volenti non fit injuria protects a defendant in rescue cases | Rescue cases are an exception to the defence
S-: An inevitable accident must involve natural forces | That is an act of God; an inevitable accident need not involve natural forces
C: A rescuer injured while saving others can claim damages | rescue cases are an exception to volenti non fit injuria
C: The defendant was not liable in Nichols v Marsland | the extraordinary rainfall was an act of God that could not be foreseen
C: Necessity is a valid defence | the harm was caused to prevent a greater harm to the public
X: C2 D2 2 | Distinguish between act of God and inevitable accident. | Act of God – extraordinary natural forces, unforeseeable (Nichols v Marsland); inevitable accident – unavoidable despite reasonable care, need not involve natural forces (Stanley v Powell).
X: C3 D3 2 | Why is volenti non fit injuria not available in rescue cases? | A rescuer acts under a moral or legal duty to save others; consent is not truly free; law encourages rescue (e.g. Haynes v Harwood).
X: C3 D3 3 | Explain the essentials of volenti non fit injuria. | Plaintiff knew of the risk; voluntarily agreed to suffer it; consent free, not by fraud or compulsion; act must be within the limits consented to.
X: C3 D4 3 | Explain the defences of private defence and necessity. | Private defence – reasonable force to protect person or property; necessity – harm caused to prevent greater harm, e.g. demolishing a house to stop fire.
X: C4 D4 3 | 'Knowledge of risk is not consent.' Explain. | Volenti requires voluntary agreement, not mere awareness; workers who knew of risk but had no choice can claim; scienti non fit injuria is not the rule.
L: D4 | Explain the general defences available in an action for tort. | Volenti non fit injuria; plaintiff the wrongdoer; inevitable accident; act of God; private defence; mistake; necessity; statutory authority – with cases.
"""), ST(S + '04-st3', 'negligence; strict and absolute liability', """
T: negligence | the breach of a legal duty to take care which results in damage to the plaintiff
T: duty of care | the legal obligation to take reasonable care to avoid acts that could foreseeably harm others
T: res ipsa loquitur | the principle that 'the thing speaks for itself', under which negligence is presumed from the nature of the accident
T: strict liability | the rule in Rylands v Fletcher that a person who brings a dangerous thing on his land is liable if it escapes, subject to certain exceptions
T: absolute liability | the rule in M.C. Mehta v Union of India that an enterprise engaged in a hazardous activity is liable for harm without any exceptions
T: contributory negligence | the negligence of the plaintiff that contributes to the damage suffered
Q: The rule of strict liability was laid down in: | Rylands v Fletcher | Donoghue v Stevenson | Ashby v White | Hadley v Baxendale
Q: The rule of absolute liability was laid down in: | M.C. Mehta v Union of India (Oleum gas leak case) | Rylands v Fletcher | Kesavananda Bharati v State of Kerala | Vishaka v State of Rajasthan
Q: The 'neighbour principle' in negligence comes from: | Donoghue v Stevenson | Nichols v Marsland | Stanley v Powell | Salomon v Salomon
Q: Strict liability requires a dangerous thing, its escape and: | non-natural use of land | intention to harm | a written contract | a criminal conviction
Q: Under absolute liability, the enterprise: | cannot plead any of the exceptions available under strict liability | can plead act of God | can plead act of a third party | is liable only if negligent
Q: The Oleum gas leak in Delhi occurred in: | 1985 | 1984 | 1992 | 1972
Y: 1868 | the House of Lords decision in Rylands v Fletcher
S+: The essentials of negligence are a duty of care, breach of that duty and consequent damage
S+: Exceptions to strict liability include the plaintiff's own default, act of God, consent, act of a third party and statutory authority
S+: Under absolute liability, compensation is linked to the magnitude and capacity of the enterprise
S+: The absolute liability rule was evolved after the Bhopal gas tragedy and the Oleum gas leak
S+: Under res ipsa loquitur the burden shifts to the defendant to show that there was no negligence
S-: Absolute liability allows the exception of act of God | Absolute liability allows no exceptions
S-: Strict liability was laid down in M.C. Mehta v Union of India | It was laid down in Rylands v Fletcher; M.C. Mehta laid down absolute liability
S-: Negligence requires an intention to cause harm | Negligence is careless conduct; no intention is needed
C: The Supreme Court laid down absolute liability | the strict liability rule with its exceptions was inadequate for hazardous industries in India
C: A surgeon who leaves a swab inside a patient is presumed negligent | under res ipsa loquitur the facts speak for themselves
C: A manufacturer may be liable to a consumer with whom it has no contract | it owes a duty of care to those who may foreseeably be harmed (Donoghue v Stevenson)
X: C2 D2 2 | Distinguish between strict liability and absolute liability. | Strict – Rylands v Fletcher, liability for escape of dangerous thing, with exceptions; absolute – M.C. Mehta, hazardous enterprises, no exceptions, compensation linked to capacity.
X: C3 D3 2 | What is res ipsa loquitur? | 'The thing speaks for itself'; negligence presumed from the nature of the accident when the thing is under defendant's control; burden shifts to defendant.
X: C3 D3 3 | Explain the essentials of negligence. | Duty of care owed to the plaintiff; breach of that duty; damage caused as a result; Donoghue v Stevenson.
X: C3 D4 3 | Explain the essentials of strict liability and any two exceptions. | Dangerous thing; escape from defendant's land; non-natural use; exceptions – plaintiff's default, act of God, consent, act of third party, statutory authority.
X: C4 D4 3 | Why did the Supreme Court evolve the rule of absolute liability? | Strict liability exceptions let hazardous industries escape; Bhopal and Oleum gas leaks; enterprises must bear full cost of harm; compensation proportional to capacity; deterrence.
L: D4 | Explain the rule of strict liability and how it differs from absolute liability. | Rylands v Fletcher – essentials and exceptions; M.C. Mehta (1987) – hazardous enterprise, no exceptions, compensation proportional to capacity; reasons for the change.
L: D5 | Explain negligence as a tort, with its essentials and the principle of res ipsa loquitur. | Duty of care, breach, damage; Donoghue v Stevenson; res ipsa loquitur; contributory negligence; examples of professional and road negligence.
"""), ST(S + '04-st4', 'vicarious liability, nuisance and defamation', """
T: vicarious liability | the liability of one person for a tort committed by another because of a special relationship between them
T: respondeat superior | the principle 'let the master answer', making an employer liable for torts of employees in the course of employment
T: nuisance | an unlawful interference with a person's use or enjoyment of land or of some right over it
T: defamation | the publication of a false statement that lowers the reputation of a person in the eyes of right-thinking members of society
T: libel | defamation in a permanent form, such as writing, print or a picture
T: slander | defamation in a transient form, such as spoken words or gestures
Q: The liability of an employer for the tort of an employee in the course of employment is: | vicarious liability | strict liability | absolute liability | contributory negligence
Q: Defamation in a permanent form such as a newspaper article is: | libel | slander | nuisance | trespass
Q: The State was held liable for the negligence of its driver in: | State of Rajasthan v Vidyawati | Kasturi Lal v State of U.P. | Rylands v Fletcher | Ashby v White
Q: In Kasturi Lal v State of U.P., the State was not held liable because the act was done in: | exercise of sovereign functions | the course of a contract | private capacity | self-defence
Q: Which of these is a defence to defamation? | Truth (justification) | Act of God | Inevitable accident | Res ipsa loquitur
Q: Loud noise from a factory that disturbs a neighbour's sleep is an example of: | private nuisance | libel | trespass to goods | negligence
M:tort: Libel | permanent form of defamation
M:tort: Slander | transient form of defamation
M:tort: Nuisance | interference with use or enjoyment of land
M:tort: Vicarious liability | liability for another's tort
S+: Vicarious liability arises in relationships such as master and servant, principal and agent, and partners
S+: An employer is liable only for torts committed by an employee in the course of employment
S+: Nuisance may be public, affecting the public at large, or private, affecting particular persons
S+: Defences to defamation include truth, fair comment and privilege
S+: For defamation the statement must refer to the plaintiff and be published to a third person
S-: An employer is liable for every act of an employee, even outside work | Liability arises only for acts in the course of employment
S-: Slander is defamation in a permanent form | Slander is transient; libel is permanent
S-: A statement made only to the person defamed is defamation | It must be published to a third person
C: An employer is made liable for an employee's tort | the employer controls the work and is better able to pay compensation
C: Truth is a defence to a civil action for defamation | defamation protects only a reputation that is deserved
C: A private person cannot sue for public nuisance without special damage | public nuisance affects the public generally and is a matter for the State
X: C2 D2 2 | Distinguish between libel and slander. | Libel – defamation in permanent form (writing, print, picture); slander – transient form (spoken words, gestures).
X: C3 D3 2 | When is an employer liable for the tort of an employee? | When there is a master-servant relationship and the tort is committed in the course of employment; principle of respondeat superior.
X: C3 D3 3 | Explain the essentials of defamation. | Statement is false and defamatory; refers to the plaintiff; published to a third person; lowers reputation in the eyes of right-thinking people.
X: C3 D4 3 | Distinguish between public and private nuisance. | Public – affects the public at large, criminal and civil action, private suit only with special damage; private – interferes with a particular person's use or enjoyment of land, civil action.
X: C4 D4 3 | Explain the liability of the State for torts of its servants. | Vidyawati (1962) – State liable for driver's negligence; Kasturi Lal (1965) – no liability for sovereign functions; later decisions narrowed sovereign immunity and allowed compensation for violation of rights.
L: D4 | Explain vicarious liability with reference to master and servant and the State. | Meaning; relationships; course of employment; respondeat superior; Vidyawati and Kasturi Lal cases; trend towards State liability.
L: D5 | Explain the torts of nuisance and defamation and their defences. | Nuisance – public and private, essentials, defences; defamation – libel and slander, essentials, defences of truth, fair comment, privilege.
"""),
]

CH05 = [ST(S + '05-st1', 'concept and kinds of property', """
T: property | everything that can be owned and has value, including rights over things
T: movable property | property that can be moved from one place to another without damage, such as furniture and vehicles
T: immovable property | land, benefits arising out of land and things attached to the earth or permanently fastened to anything attached to the earth
T: tangible property | property that has a physical existence and can be touched, such as land or a car
T: intangible property | property without physical existence, such as copyright, patents and goodwill
Q: Which of these is intangible property? | A patent | A house | A car | A table
Q: Under the Transfer of Property Act, immovable property does NOT include: | standing timber, growing crops and grass | land | buildings | benefits arising out of land
Q: Goodwill of a business is: | intangible movable property | tangible immovable property | not property at all | tangible movable property
Q: A tree rooted in the earth is generally treated as: | immovable property | intangible property | movable property in all cases | not property
Q: Property without physical existence is called: | intangible property | tangible property | immovable property | corporeal property
S+: Property may be classified as movable or immovable, tangible or intangible, and public or private
S+: Things attached to the earth, such as buildings and trees, are generally immovable property
S+: Intellectual property such as copyright and patents is intangible property
S+: The General Clauses Act 1897 defines immovable property to include land, benefits arising out of land and things attached to the earth
S-: Standing timber is immovable property under the Transfer of Property Act | It is excluded from immovable property
S-: Intangible property cannot be owned | Intangible property such as patents and copyright can be owned and transferred
S-: A car is immovable property | It is movable and tangible property
C: Patents and copyright are treated as property | they have value and can be owned, transferred and protected by law
C: Standing timber is treated as movable property | the Transfer of Property Act excludes it, as it is meant to be cut and removed
C: Classification of property matters in law | different rules of transfer, registration and stamp duty apply to movable and immovable property
X: C2 D2 2 | Distinguish between movable and immovable property. | Movable – can be moved without damage (car, furniture); immovable – land, benefits arising out of land and things attached to the earth (house, tree).
X: C3 D3 2 | Distinguish between tangible and intangible property. | Tangible – physical existence (land, car); intangible – no physical existence (copyright, patent, goodwill).
X: C3 D3 3 | Explain any three kinds of property with examples. | Movable and immovable; tangible and intangible; public and private; examples of each.
X: C3 D4 3 | Why is the classification of property important in law? | Different modes of transfer; registration required for immovable property above a value; stamp duty; jurisdiction of courts; rules of succession and taxation differ.
X: C4 D4 3 | 'Property is not only a thing but a bundle of rights.' Explain. | Property includes rights to use, enjoy, possess, transfer and exclude others; intangible property is only rights; ownership is a bundle of these rights.
L: D4 | Explain the concept of property and its kinds. | Meaning; movable and immovable – definitions under General Clauses Act and TPA; tangible and intangible; public and private; significance of classification.
"""), ST(S + '05-st2', 'transfer of property: sale, mortgage, lease, gift and exchange', """
T: transfer of property | an act by which a living person conveys property, in present or in future, to one or more other living persons (Section 5)
T: sale | a transfer of ownership in exchange for a price paid or promised or part-paid and part-promised (Section 54)
T: mortgage | the transfer of an interest in specific immovable property to secure the payment of money advanced as a loan (Section 58)
T: lease | a transfer of a right to enjoy immovable property for a certain time in consideration of a price paid or promised (Section 105)
T: gift | the transfer of existing property made voluntarily and without consideration, and accepted by the donee (Section 122)
T: exchange | the mutual transfer of ownership of one thing for the ownership of another, neither thing being money only (Section 118)
Q: The Transfer of Property Act was enacted in: | 1882 | 1872 | 1908 | 1961
Q: The person who transfers property by way of gift is the: | donor | donee | mortgagee | lessee
Q: In a mortgage, the person who lends money is the: | mortgagee | mortgagor | lessor | donor
Q: A gift of immovable property must be made by a registered instrument signed by the donor and attested by at least: | two witnesses | one witness | five witnesses | ten witnesses
Q: A transfer of the right to enjoy property for a certain time in return for rent is a: | lease | sale | gift | exchange
Q: Transfer of one thing for another, where neither is money only, is: | exchange | sale | mortgage | gift
Q: A gift must be accepted by the donee during the lifetime of the: | donor | donee's parents | witness | registrar
Y: 1882 | the enactment of the Transfer of Property Act
M:transfer: Sale | Section 54
M:transfer: Mortgage | Section 58
M:transfer: Lease | Section 105
M:transfer: Gift | Section 122
S+: The Transfer of Property Act deals with transfers between living persons, not with succession on death
S+: Sale of tangible immovable property of the value of one hundred rupees or more must be made by a registered instrument
S+: In a lease the lessor transfers only the right of enjoyment, not ownership
S+: In a mortgage the property stands as security for repayment of a loan
S+: A gift is void if the donee dies before accepting it
S-: A gift may be made for consideration | A gift is made voluntarily and without consideration
S-: In a lease, ownership passes to the lessee | Only the right to enjoy passes; ownership stays with the lessor
S-: The Transfer of Property Act governs transfer by will | It governs transfers between living persons; wills are governed by succession law
C: A gift becomes void if not accepted during the donor's lifetime | acceptance by the donee during the donor's life is an essential of a gift
C: A sale differs from an exchange | in a sale ownership passes for a price in money, while in an exchange one thing is given for another
C: A mortgagee does not become the owner of the property | a mortgage transfers only an interest to secure a loan
X: C2 D2 2 | Distinguish between a sale and an exchange. | Sale – ownership transferred for a price in money (Section 54); exchange – mutual transfer of ownership of one thing for another, neither being money only (Section 118).
X: C3 D3 2 | Distinguish between a lease and a sale. | Lease – transfer of right to enjoy for a period, for rent, ownership stays with lessor; sale – absolute transfer of ownership for a price.
X: C3 D3 3 | Explain the essentials of a valid gift. | Transfer of existing property; voluntary; without consideration; acceptance by donee during donor's lifetime; immovable gift by registered instrument attested by two witnesses.
X: C3 D4 3 | What is a mortgage? Explain the parties and the nature of the transaction. | Transfer of interest in specific immovable property to secure a loan; mortgagor – borrower; mortgagee – lender; mortgage money; mortgage deed; property returns on repayment.
X: C4 D4 3 | Explain the meaning of 'transfer of property' under Section 5. | Act by which a living person conveys property in present or future to one or more living persons or to himself; includes companies and associations; excludes transfer by will.
L: D4 | Explain sale, mortgage, lease, gift and exchange under the Transfer of Property Act 1882. | Definitions with sections; parties; essentials; registration; examples of each.
L: D5 | Compare a sale, a gift and a lease as modes of transferring interest in property. | Ownership versus right to enjoy; consideration – price, none, rent; duration; registration; parties; examples.
"""), ST(S + '05-st3', 'ownership, possession and the right to property', """
T: ownership | the most complete right over property, including the rights to possess, use, enjoy, transfer and exclude others
T: possession | the physical control of a thing together with the intention to exercise that control
T: adverse possession | a mode of acquiring title by continuous, open and hostile possession of another's property for the period fixed by law
T: Article 300A | the constitutional provision that no person shall be deprived of his property save by authority of law
T: eminent domain | the power of the State to acquire private property for public purpose on payment of compensation
Q: The right to property was removed from the list of fundamental rights by the: | 44th Amendment (1978) | 42nd Amendment (1976) | 86th Amendment (2002) | 73rd Amendment (1992)
Q: After 1978, the right to property is a: | constitutional (legal) right under Article 300A | fundamental right under Article 19 | directive principle | fundamental duty
Q: Article 300A provides that no person shall be deprived of property except by: | authority of law | an order of the Prime Minister | the will of the majority | a resolution of the Gram Sabha
Q: Before 1978 the right to property was in: | Articles 19(1)(f) and 31 | Article 21 | Article 300A | Article 39A
Q: The power of the State to acquire private property for public purposes is called: | eminent domain | adverse possession | sovereign immunity | escheat
Y: 1978 | the 44th Amendment removing the right to property from fundamental rights
S+: Ownership may exist without possession, as when a landlord's property is held by a tenant
S+: Possession has two elements: corpus (physical control) and animus (intention to possess)
S+: Since the 44th Amendment, a person deprived of property cannot directly approach the Supreme Court under Article 32 for a fundamental right violation
S+: Article 300A requires that deprivation of property must be by a valid law
S+: The State acquires land for public purposes under a law that provides compensation
S-: The right to property is still a fundamental right | It is a constitutional right under Article 300A since the 44th Amendment
S-: Possession always means ownership | A person may possess property without owning it, such as a tenant
S-: The State can take property by an executive order without law | Article 300A requires the authority of law
C: A tenant has possession but not ownership | ownership remains with the landlord, who has only parted with physical control
C: The right to property was made a constitutional right instead of a fundamental right | it had obstructed land reforms and the State's welfare measures
C: Article 300A protects property against arbitrary executive action | deprivation must be by authority of a valid law
X: C2 D2 2 | Distinguish between ownership and possession. | Ownership – complete legal right over property, including transfer and exclusion; possession – physical control with intention; ownership may exist without possession.
X: C3 D3 2 | What is the present status of the right to property in India? | Removed from fundamental rights by the 44th Amendment (1978); now a constitutional right under Article 300A; deprivation only by authority of law.
X: C3 D3 3 | Explain the elements of possession. | Corpus – physical control over the thing; animus – intention to possess and exclude others; both needed; examples.
X: C3 D4 3 | Explain the incidents of ownership. | Right to possess; right to use and enjoy; right to transfer and dispose; right to exclude others; indefinite duration; residuary character.
X: C4 D4 3 | 'The right to property is no longer a fundamental right but is still protected.' Explain. | 44th Amendment removed Articles 19(1)(f) and 31; Article 300A requires authority of law; courts test laws; remedy under Article 226; compensation under land acquisition law.
L: D4 | Explain ownership and possession and the constitutional right to property in India. | Meaning and incidents of ownership; elements of possession; adverse possession; Articles 19(1)(f) and 31 earlier; 44th Amendment; Article 300A; eminent domain.
"""),
]

CH06 = [ST(S + '06-st1', 'concept of intellectual property and its rationale', """
T: intellectual property | creations of the mind, such as inventions, literary and artistic works, designs, symbols and names used in commerce
T: intellectual property rights | legal rights given to creators over the use of their creations for a limited period
T: World Intellectual Property Organization | the UN specialised agency based in Geneva that promotes the protection of intellectual property worldwide
T: public domain | the state of works whose protection has expired, which anyone may freely use
Q: WIPO has its headquarters at: | Geneva | New York | The Hague | Paris
Q: Which of these is NOT a form of intellectual property? | A plot of agricultural land | Copyright | Patent | Trademark
Q: Intellectual property rights are generally granted for: | a limited period | an unlimited period | one day | the life of the State
Q: Industrial property mainly includes: | patents, trademarks, designs and geographical indications | land and buildings | shares and debentures | movable furniture
Q: The Berne Convention deals with the protection of: | literary and artistic works | industrial property | environmental rights | human rights
S+: Intellectual property is broadly divided into copyright and related rights, and industrial property
S+: IPR gives creators an incentive to invent and create by rewarding their labour
S+: IPR balances the interest of creators with the interest of the public in access to knowledge
S+: After the period of protection ends, the work or invention falls into the public domain
S+: The Paris Convention deals with industrial property and the Berne Convention with copyright
S-: Intellectual property rights last forever | They are granted for a limited period, after which the work enters the public domain
S-: Intellectual property is tangible property | It is intangible property
S-: The Paris Convention deals with copyright | It deals with industrial property; the Berne Convention deals with copyright
C: The law protects intellectual property | protection gives creators an incentive to invest time and money in new creations
C: IPR is granted only for a limited period | society must eventually gain free access to knowledge and creations
C: IPR promotes economic growth | protected inventions and brands attract investment and trade
X: C2 D2 2 | What is intellectual property? | Creations of the mind – inventions, literary and artistic works, designs, symbols, names used in commerce; intangible property protected by law.
X: C3 D3 2 | Why are intellectual property rights granted for a limited period? | To balance creators' reward with public access; after expiry works enter the public domain for free use and further innovation.
X: C3 D3 3 | Explain the rationale for protecting intellectual property. | Reward for creative labour; incentive to innovate; disclosure of knowledge; economic growth and investment; protection of consumers from confusion.
X: C3 D4 3 | Classify intellectual property with examples. | Copyright and related rights – books, music, films, software; industrial property – patents, trademarks, industrial designs, geographical indications.
X: C4 D4 3 | 'IPR must balance private reward and public interest.' Explain. | Exclusive rights reward creators; limited term, exceptions like fair dealing, compulsory licensing; access to medicines; public domain after expiry.
L: D4 | Explain the concept of intellectual property, its kinds and the rationale for its protection. | Meaning; copyright and industrial property; WIPO, Paris and Berne Conventions; rationale – reward, incentive, disclosure, growth; limited duration and public interest.
"""), ST(S + '06-st2', 'copyright and trademarks', """
T: copyright | the exclusive right of the author to reproduce, publish, adapt and communicate an original literary, dramatic, musical or artistic work, film or sound recording
T: trademark | a mark capable of being represented graphically that distinguishes the goods or services of one person from those of others
T: fair dealing | the use of a copyright work without permission for purposes such as private study, research, criticism or reporting
T: idea-expression dichotomy | the principle that copyright protects the expression of an idea and not the idea itself
T: passing off | a common law action against a person who misrepresents his goods as those of another trader
Q: Copyright in India is governed by the: | Copyright Act 1957 | Trade Marks Act 1999 | Patents Act 1970 | Designs Act 2000
Q: Copyright in a literary work generally lasts for the life of the author plus: | 60 years | 20 years | 10 years | 100 years
Q: Registration of a trademark in India is valid for: | 10 years and is renewable | 20 years, not renewable | the owner's life | 5 years only
Q: Trademarks in India are governed by the: | Trade Marks Act 1999 | Copyright Act 1957 | Patents Act 1970 | Companies Act 2013
Q: Copyright protects: | the expression of an idea | the idea itself | a scientific discovery | a geographical name
Q: Using a copyright work for private study or criticism is permitted as: | fair dealing | passing off | infringement | compulsory licensing
Y: 1957 | the enactment of the Copyright Act
Y: 1999 | the enactment of the Trade Marks Act
S+: Copyright arises automatically on creation, though registration is available as evidence
S+: Computer programs are protected as literary works under copyright law
S+: A trademark may be a word, logo, symbol, shape, colour combination or sound
S+: Infringement of a trademark occurs when an identical or deceptively similar mark is used for similar goods
S+: A trademark can be renewed indefinitely every ten years
S-: Copyright protects ideas as well as expression | It protects only the expression of an idea
S-: Copyright exists only after registration | Copyright arises automatically on creation
S-: A trademark registration expires permanently after ten years | It can be renewed every ten years indefinitely
C: Two authors may write different books on the same idea without infringement | copyright protects expression, not the idea itself
C: Trademarks protect consumers | they help buyers identify the source and quality of goods and avoid confusion
C: Fair dealing is allowed under copyright law | it promotes education, research and free expression
X: C2 D2 2 | Distinguish between copyright and trademark. | Copyright – protects original literary, artistic, musical works, films, sound recordings; trademark – mark distinguishing goods or services of one trader from another.
X: C3 D3 2 | What is fair dealing? | Use of a copyright work without permission for private study, research, criticism, review or news reporting; not infringement.
X: C3 D3 3 | Explain the works protected by copyright. | Original literary works including computer programs; dramatic; musical; artistic works; cinematograph films; sound recordings.
X: C3 D4 3 | Explain the functions of a trademark. | Identifies source of goods; distinguishes from competitors; indicates quality; advertising and brand value; protects consumers from confusion.
X: C4 D4 3 | Explain infringement of trademark and the remedy of passing off. | Infringement – use of identical or deceptively similar registered mark; passing off – misrepresenting goods as another's, available even for unregistered marks; remedies – injunction, damages, account of profits.
L: D4 | Explain copyright and trademarks under Indian law. | Copyright Act 1957 – works, rights, term, fair dealing, idea-expression; Trade Marks Act 1999 – meaning, registration, renewal, infringement, passing off.
"""), ST(S + '06-st3', 'patents, designs and geographical indications; TRIPS', """
T: patent | an exclusive right granted for an invention that is new, involves an inventive step and is capable of industrial application
T: industrial design | the features of shape, configuration, pattern or ornament applied to an article, which appeal to the eye
T: geographical indication | an indication identifying goods as originating in a particular region, where a quality or reputation is due to that origin
T: TRIPS Agreement | the WTO Agreement on Trade-Related Aspects of Intellectual Property Rights, which sets minimum standards of IP protection
T: compulsory licence | a licence granted by the government to someone other than the patent holder to use a patented invention, such as for public health
Q: The term of a patent in India is: | 20 years | 10 years | 60 years after the inventor's death | 5 years
Q: The first product to get a GI tag in India was: | Darjeeling tea | Basmati rice | Mysore silk | Alphonso mango
Q: Patents in India are governed by the: | Patents Act 1970 | Copyright Act 1957 | Designs Act 2000 | Trade Marks Act 1999
Q: The TRIPS Agreement is administered by the: | World Trade Organization | WIPO | UNESCO | International Court of Justice
Q: Which of these is NOT a condition for granting a patent? | Artistic appeal | Novelty | Inventive step | Industrial application
Q: Section 3(d) of the Patents Act, which prevents 'evergreening', was upheld in: | Novartis v Union of India | Kesavananda Bharati v State of Kerala | Salomon v Salomon | Ashby v White
Y: 1970 | the enactment of the Patents Act
S+: An invention must be new, involve an inventive step and be capable of industrial application to be patented
S+: Registration of a design is valid for ten years, extendable by five years
S+: A geographical indication is registered under the Geographical Indications of Goods Act 1999
S+: The TRIPS Agreement came into force with the WTO in 1995
S+: India amended its patent law in 2005 to allow product patents for pharmaceuticals in line with TRIPS
S-: A patent lasts for the inventor's lifetime | A patent lasts for 20 years
S-: A geographical indication belongs to a single individual | It belongs to producers of the region collectively
S-: Discoveries of natural substances are patentable as inventions | Mere discoveries are not inventions under the Patents Act
C: The Patents Act prevents evergreening | a new form of a known substance is not patentable unless it shows enhanced efficacy (Section 3(d))
C: Geographical indications benefit local producers | they protect the reputation of products linked to a region and fetch better prices
C: India had to change its patent law | the TRIPS Agreement required product patents in all fields of technology
X: C2 D2 2 | Distinguish between a patent and an industrial design. | Patent – protects a new inventive, industrially applicable invention, 20 years; design – protects visual features of shape, pattern or ornament, 10 + 5 years.
X: C3 D3 2 | What is a geographical indication? Give two examples. | Indication that goods originate from a region with a quality or reputation linked to it; e.g. Darjeeling tea, Kanchipuram silk, Mysore silk.
X: C3 D3 3 | State the conditions for an invention to be patentable. | Novelty; inventive step (not obvious); industrial application; not excluded under Section 3, such as mere discoveries.
X: C3 D4 3 | Explain the importance of the TRIPS Agreement for India. | Minimum standards of IP protection for WTO members; India amended patent law in 2005 to allow product patents; GI and design laws; flexibilities like compulsory licensing.
X: C4 D4 3 | 'Patent law must balance innovation with access to medicines.' Explain with reference to India. | Patents reward innovation; Section 3(d) prevents evergreening (Novartis case); compulsory licensing for public health; affordable generics.
L: D4 | Explain patents, industrial designs and geographical indications under Indian law. | Patents Act 1970 – conditions, term, exclusions; Designs Act 2000 – meaning, term; GI Act 1999 – meaning, examples, Darjeeling tea; TRIPS.
"""),
]

CH07 = [ST(S + '07-st1', 'concept of sustainable development', """
T: sustainable development | development that meets the needs of the present without compromising the ability of future generations to meet their own needs
T: intergenerational equity | the principle that the present generation must use natural resources so that future generations have a fair share
T: Brundtland Report | the 1987 report 'Our Common Future' of the World Commission on Environment and Development that defined sustainable development
T: Agenda 21 | the action plan for sustainable development adopted at the Rio Earth Summit
T: Sustainable Development Goals | the 17 goals adopted by the United Nations in 2015 as part of the 2030 Agenda
Q: The Stockholm Conference on the Human Environment was held in: | 1972 | 1992 | 2002 | 1987
Q: The Rio Earth Summit was held in: | 1992 | 1972 | 2015 | 1997
Q: The number of Sustainable Development Goals is: | 17 | 8 | 12 | 21
Q: The term sustainable development was popularised by the: | Brundtland Report | Kyoto Protocol | Stockholm Declaration | Montreal Protocol
Q: The United Nations Environment Programme was set up after the: | Stockholm Conference | Rio Summit | Paris Agreement | Kyoto Protocol
Y: 1972 | the United Nations Conference on the Human Environment at Stockholm
Y: 1992 | the Rio Earth Summit (UN Conference on Environment and Development)
Y: 1987 | the Brundtland Report 'Our Common Future'
Y: 2015 | the adoption of the Sustainable Development Goals
S+: Sustainable development balances economic growth, social development and environmental protection
S+: The Rio Earth Summit adopted the Rio Declaration and Agenda 21
S+: The SDGs succeeded the Millennium Development Goals and are to be achieved by 2030
S+: Intergenerational equity requires the present generation to hold natural resources in trust for future generations
S+: India's Supreme Court has accepted sustainable development as part of the law of the land
S-: The Stockholm Conference was held in 1992 | It was held in 1972; the Rio Summit was in 1992
S-: Sustainable development means stopping all development | It means development that does not compromise the needs of future generations
S-: The SDGs are to be achieved by 2050 | They are to be achieved by 2030
C: Sustainable development is necessary | unchecked use of resources would deprive future generations of their needs
C: The Stockholm Conference is a landmark | it was the first major UN conference on the environment and led to UNEP
C: Development and environment must be balanced | economic growth that destroys the environment cannot be sustained
X: C2 D2 2 | What is sustainable development? | Development that meets the needs of the present without compromising the ability of future generations to meet their own needs (Brundtland Report, 1987).
X: C3 D3 2 | What is intergenerational equity? | The principle that the present generation must use natural resources in a way that leaves a fair share for future generations.
X: C3 D3 3 | Explain the significance of the Stockholm Conference and the Rio Summit. | Stockholm 1972 – first UN conference on environment, Stockholm Declaration, UNEP; Rio 1992 – Rio Declaration, Agenda 21, conventions on climate change and biodiversity.
X: C3 D4 3 | Explain the three pillars of sustainable development. | Economic growth; social equity and inclusion; environmental protection; balance among them.
X: C4 D4 3 | 'Sustainable development is a bridge between development and environment.' Explain. | Development needed for poverty reduction; environment needed for survival; sustainable use, intergenerational equity, SDGs; courts' balancing approach.
L: D4 | Trace the evolution of the concept of sustainable development from Stockholm to the SDGs. | Stockholm 1972; Brundtland Report 1987; Rio 1992 – Agenda 21; Johannesburg 2002; SDGs 2015 – 17 goals, Agenda 2030; Indian courts.
"""), ST(S + '07-st2', 'constitutional provisions and environmental statutes', """
T: Article 48A | the Directive Principle requiring the State to protect and improve the environment and to safeguard forests and wildlife
T: Article 51A(g) | the fundamental duty of every citizen to protect and improve the natural environment and have compassion for living creatures
T: Environment (Protection) Act 1986 | the umbrella law enacted after the Bhopal gas tragedy that empowers the Central Government to protect and improve the environment
T: Central Pollution Control Board | the statutory body constituted under the Water Act 1974 to prevent and control water and air pollution
Q: Articles 48A and 51A(g) were added by the: | 42nd Amendment (1976) | 44th Amendment (1978) | 73rd Amendment (1992) | 86th Amendment (2002)
Q: The Environment (Protection) Act was enacted in: | 1986 | 1974 | 1981 | 1972
Q: The Water (Prevention and Control of Pollution) Act was enacted in: | 1974 | 1981 | 1986 | 1992
Q: The Air (Prevention and Control of Pollution) Act was enacted in: | 1981 | 1974 | 1986 | 1972
Q: The right to a clean environment has been read by the courts into: | Article 21 | Article 300A | Article 51 | Article 323A
Q: The Environment (Protection) Act 1986 was enacted soon after the: | Bhopal gas tragedy | Rio Earth Summit | Stockholm Conference | Oleum gas leak
Y: 1974 | the enactment of the Water (Prevention and Control of Pollution) Act
Y: 1981 | the enactment of the Air (Prevention and Control of Pollution) Act
Y: 1986 | the enactment of the Environment (Protection) Act
M:law: Water Act | 1974
M:law: Air Act | 1981
M:law: Environment (Protection) Act | 1986
M:law: National Green Tribunal Act | 2010
S+: Article 48A is a Directive Principle and Article 51A(g) is a fundamental duty
S+: The Supreme Court has held that the right to life under Article 21 includes the right to a pollution-free environment
S+: The Environment (Protection) Act 1986 is an umbrella legislation covering water, air and land
S+: Pollution Control Boards at the Centre and in the States enforce the Water and Air Acts
S+: The Wildlife (Protection) Act 1972 and the Forest (Conservation) Act 1980 protect wildlife and forests
S-: Article 48A is a fundamental right | It is a Directive Principle of State Policy
S-: The Environment Protection Act was enacted in 1974 | It was enacted in 1986; the Water Act was enacted in 1974
S-: Protecting the environment is only the duty of the State | Article 51A(g) makes it a fundamental duty of every citizen too
C: Citizens can approach the courts for a clean environment | the courts have read the right to a healthy environment into Article 21
C: The Environment (Protection) Act is called an umbrella Act | it gives the Central Government wide powers over all aspects of environmental protection
C: The Environment (Protection) Act 1986 was enacted | the Bhopal gas tragedy showed gaps in existing environmental laws
X: C2 D2 2 | Distinguish between Article 48A and Article 51A(g). | 48A – Directive Principle, State to protect and improve environment, forests and wildlife; 51A(g) – fundamental duty of citizens to protect the natural environment.
X: C3 D3 2 | How has Article 21 been used to protect the environment? | Courts held that the right to life includes the right to a clean and healthy environment, so citizens can file writs and PILs against pollution.
X: C3 D3 3 | Explain the main features of the Environment (Protection) Act 1986. | Umbrella Act; Central Government power to set standards, restrict industries, inspect, close polluting units; penalties; enacted after Bhopal.
X: C3 D4 3 | Explain the constitutional provisions for environmental protection in India. | Article 48A (DPSP); Article 51A(g) (duty); Article 21 (right to healthy environment); 42nd Amendment 1976; Article 253 for implementing treaties.
X: C4 D4 3 | 'India has many environmental laws but weak enforcement.' Examine. | Water Act 1974, Air Act 1981, EPA 1986, Wildlife Act 1972; Pollution Control Boards; limited staff, low penalties, poor monitoring; courts and NGT stepping in.
L: D4 | Explain the constitutional provisions and major statutes for environmental protection in India. | Articles 48A, 51A(g), 21; Water Act 1974; Air Act 1981; Environment (Protection) Act 1986; Wildlife Act 1972; Forest Conservation Act 1980; Pollution Control Boards.
"""), ST(S + '07-st3', 'principles of environmental jurisprudence and the NGT', """
T: polluter pays principle | the principle that the person who causes pollution must bear the cost of preventing it and of restoring the damaged environment
T: precautionary principle | the principle that lack of scientific certainty must not be used as a reason to postpone measures to prevent environmental degradation
T: public trust doctrine | the principle that the State holds natural resources such as rivers, forests and seashores in trust for the public
T: National Green Tribunal | the specialised body set up under the National Green Tribunal Act 2010 for effective and speedy disposal of environmental cases
Q: The polluter pays and precautionary principles were accepted as part of Indian law in: | Vellore Citizens' Welfare Forum v Union of India | Kesavananda Bharati v State of Kerala | Ashby v White | Salomon v Salomon
Q: The public trust doctrine was applied by the Supreme Court in: | M.C. Mehta v Kamal Nath | Rylands v Fletcher | Mohori Bibee v Dharmodas Ghose | Hussainara Khatoon v State of Bihar
Q: The National Green Tribunal was set up in: | 2010 | 1986 | 1992 | 2002
Q: Under the precautionary principle, the burden of proof is on the: | developer or industrialist | environmental activist | court | general public
Q: The NGT is expected to dispose of applications and appeals within: | six months of filing | ten years | one week | five years
Y: 2010 | the setting up of the National Green Tribunal
S+: Under the polluter pays principle, liability extends to compensating victims and restoring the environment
S+: The precautionary principle shifts the burden of proof to the person proposing an activity to show that it is environmentally benign
S+: The NGT is guided by the principles of natural justice and not by the Code of Civil Procedure
S+: The NGT applies sustainable development, the precautionary principle and the polluter pays principle
S+: Under the public trust doctrine the State cannot transfer natural resources meant for public use to private owners for commercial use
S-: Under the precautionary principle, action is taken only after scientific certainty | Lack of certainty is no reason to postpone preventive measures
S-: The NGT is bound by the Code of Civil Procedure | It is guided by the principles of natural justice
S-: The public trust doctrine allows the State to sell rivers to private owners | The State holds such resources in trust for the public
C: The polluter pays principle deters pollution | the polluter must bear the full cost of the damage caused
C: The NGT gives speedy environmental justice | it is a specialised body with expert members that must decide within six months
C: The Supreme Court cancelled a lease of riverbank land given to a motel | the State held the river in public trust and could not hand it to private use
X: C2 D2 2 | What is the polluter pays principle? | The polluter must bear the cost of preventing pollution, compensating victims and restoring the environment; accepted in Vellore Citizens' Welfare Forum.
X: C3 D3 2 | What is the public trust doctrine? | The State holds natural resources such as rivers, forests and seashores in trust for the public and cannot hand them over to private use; M.C. Mehta v Kamal Nath.
X: C3 D3 3 | Explain the precautionary principle. | State must anticipate and prevent environmental harm; lack of scientific certainty no reason to postpone measures; burden of proof on developer; Vellore Citizens' case.
X: C3 D4 3 | Explain the composition and functions of the National Green Tribunal. | Set up under NGT Act 2010; judicial and expert members; civil cases on environmental questions; natural justice; disposal within six months; compensation and restoration orders.
X: C4 D4 3 | 'Indian courts have shaped environmental law through new principles.' Explain. | Polluter pays and precautionary principles (Vellore); public trust (Kamal Nath); absolute liability (M.C. Mehta); Article 21 as right to environment; sustainable development.
L: D4 | Explain the principles of environmental jurisprudence evolved by Indian courts and the role of the NGT. | Polluter pays; precautionary principle; public trust doctrine; sustainable development; cases; NGT Act 2010 – composition, jurisdiction, procedure.
"""),
]

CHAPTERS = [(CH01, {}), (CH02, {}), (CH03, {}), (CH04, {}), (CH05, {}), (CH06, {}), (CH07, {})]
