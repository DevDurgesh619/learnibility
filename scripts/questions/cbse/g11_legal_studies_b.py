"""CBSE class 11 Legal Studies (074), chapters 7-12: fact tables for g12_hum_engine.

Only settled facts are used: constitutional articles, statutes with their years, and leading cases with their
well-known holdings. Where a 2023 criminal statute replaced an older code, both are named; section numbers are
given only for the older codes and for the Information Technology Act, 2000."""
from g12_hum_engine import ST

S = 'cbse-g11-legal-studies-ch'

CH07 = [ST(S + '07-st1', 'custom as a source of law', """
T: custom | a rule of conduct followed by a community for a long time and accepted by it as binding
T: legal custom | a custom that courts recognise and enforce as law
T: conventional custom | a custom that binds parties because it is taken to be part of their agreement
T: local custom | a custom followed in a particular area, caste, family or community rather than in the whole country
T: usage | an established practice, especially in trade, which binds parties who are taken to have accepted it
Q: Which of the following is an essential of a valid custom? | Antiquity | Recent origin | Written form | Approval by Parliament
Q: A custom will NOT be enforced by a court if it is: | opposed to public policy or statute law | ancient | continuous | certain
Q: The Hindu Marriage Act, 1955 allows marriage within prohibited degrees of relationship only if: | a custom or usage governing both parties permits it | both parties are above 30 years | the parents consent in writing | the marriage is registered
Q: The historical school regarded custom as: | the earliest and most important source of law, growing from the spirit of the people | a command of the sovereign | a rule made by judges | an inferior and unimportant source
Q: A custom observed only within a particular district or family is called a: | local custom | general custom | conventional custom | legislation
Q: When a custom conflicts with a valid statute, the court will: | apply the statute | apply the custom | apply whichever is older | refer the matter to the Law Commission
S+: Custom is one of the oldest sources of law
S+: A custom must be ancient, continuous, certain, reasonable and peaceably enjoyed to be recognised as law
S+: A custom must not be opposed to morality, public policy or statute law
S+: The person relying on a custom must prove its existence before the court
S+: Hindu law recognises custom; under the Hindu Marriage Act, 1955 a valid custom can permit a marriage within the prohibited degrees
S+: Legislation can abolish or modify a custom
S-: Every custom followed in a village is automatically enforced by courts | A custom is enforced only if it satisfies the tests of a valid custom and is proved
S-: A custom can override a valid statute | A statute prevails over a conflicting custom
S-: A custom that has been followed only occasionally can be valid | A valid custom must have been observed continuously
C: Courts refuse to enforce an immoral custom | a valid custom must be reasonable and not opposed to morality or public policy
C: Custom has declined in importance as a source of law in modern India | legislation now covers most areas of social life and overrides custom
C: The party relying on a custom must prove it | courts do not presume a custom; its antiquity, continuity and certainty are questions of fact
X: C2 D2 2 | State any four essentials of a valid custom. | Antiquity; continuity; certainty; reasonableness; peaceable enjoyment; consistency; conformity with statute law and public policy (any four).
X: C3 D3 3 | Distinguish between legal custom and conventional custom. | Legal custom – binding by its own authority, enforced by courts as law (general or local); conventional custom (usage) – binds only because parties are taken to have accepted it in their agreement; it can be excluded by the contract.
L: D4 | Explain custom as a source of law and discuss the essentials of a valid custom. | Meaning; historical school's view; kinds – legal (general, local) and conventional; essentials – antiquity, continuity, peaceable enjoyment, certainty, reasonableness, consistency, conformity with statute and public policy; proof; declining importance; example from the Hindu Marriage Act.
"""), ST(S + '07-st2', 'legislation as a source of law', """
T: legislation | the making of law by a competent authority, usually a legislature, in the form of written enactments
T: supreme legislation | legislation by a sovereign law-making body that no other legislative authority can repeal or control, apart from the limits of the Constitution
T: subordinate legislation | legislation made by an authority other than the sovereign legislature, under power given by it
T: delegated legislation | rules, regulations and bye-laws made by the executive or other bodies under powers delegated by an Act
T: ordinance | a law made by the President (Article 123) or a Governor (Article 213) when the legislature is not in session
T: ultra vires | beyond the powers given; a rule made beyond the powers of the parent Act is void
T: parent Act | the Act of the legislature that delegates rule-making power to another authority
Q: The President's power to promulgate ordinances is given in: | Article 123 | Article 213 | Article 352 | Article 368
Q: A Governor's power to promulgate ordinances is given in: | Article 213 | Article 123 | Article 356 | Article 226
Q: An ordinance issued by the President ceases to operate if not approved by Parliament within: | six weeks of the reassembly of Parliament | six months of its issue | one year of its issue | three months of its issue
Q: Bye-laws made by a municipal corporation are an example of: | subordinate legislation | supreme legislation | precedent | custom
Q: A rule made by the executive that goes beyond the powers given by the parent Act is: | ultra vires and void | always valid | valid for six months | binding on courts
Q: Which of these is a form of control over delegated legislation? | Judicial review | Presidential pardon | Election petition | Impeachment
Y: 1950 | the Constitution of India comes into force
S+: Legislation is the most important source of law in modern states
S+: Laws made by Parliament under the Constitution are an example of supreme legislation in India, though they are subject to judicial review
S+: Delegated legislation is needed because the legislature lacks time and technical knowledge to make detailed rules
S+: Rules, regulations, notifications and bye-laws are forms of delegated legislation
S+: Delegated legislation is controlled by the legislature, by the courts through judicial review and by procedural safeguards such as publication
S+: Parliament's Committee on Subordinate Legislation examines rules made by the executive
S-: Delegated legislation is made directly by Parliament | Delegated legislation is made by the executive or other bodies under powers given by Parliament
S-: An ordinance can be issued even when both Houses of Parliament are in session | An ordinance can be issued only when Parliament (or at least one House) is not in session
S-: Courts cannot examine delegated legislation | Courts can strike down delegated legislation that is ultra vires or unconstitutional
C: The legislature delegates power to the executive to make detailed rules | the legislature lacks the time and technical expertise to frame every detail and needs flexibility for emergencies
C: A rule made beyond the powers of its parent Act is struck down | delegated legislation must stay within the limits set by the parent Act
C: Legislation is regarded as the most important source of modern law | it is made deliberately by a competent authority, is written, precise and can be changed quickly to meet new needs
X: C2 D2 2 | Distinguish between supreme and subordinate legislation. | Supreme – by the sovereign legislature (Parliament), not controlled by another legislative authority; subordinate – by an authority under power delegated by the supreme legislature, can be repealed or controlled by it.
X: C3 D3 3 | Give three reasons for the growth of delegated legislation. | Pressure on legislative time; technical nature of subjects; flexibility and quick changes; emergencies; experimentation (any three).
X: C4 D4 3 | 'Delegated legislation is a necessary evil.' Discuss with reference to the controls over it. | Necessary – time, expertise, flexibility, emergencies; evil – executive makes law, less debate; controls – parliamentary (laying, Committee on Subordinate Legislation), judicial (ultra vires, constitutionality), procedural (publication, consultation).
L: D4 | Explain legislation as a source of law. Distinguish supreme from subordinate legislation and describe the controls on delegated legislation. | Meaning; advantages over custom and precedent; supreme legislation (Parliament); subordinate – executive, judicial, local, autonomous bodies; ordinances (Articles 123, 213); reasons for delegation; parliamentary, judicial and procedural controls.
"""), ST(S + '07-st3', 'precedent as a source of law', """
T: precedent | a judicial decision that is used as an authority for deciding later cases with similar facts
T: stare decisis | the doctrine of 'standing by things decided', under which courts follow earlier decisions
T: ratio decidendi | the legal principle on which a decision is based; it is the binding part of a precedent
T: obiter dicta | remarks of a judge made 'by the way' that are not necessary for the decision; they are only persuasive
T: binding precedent | a precedent that a lower court must follow
T: persuasive precedent | a precedent that a court may take into account but is not bound to follow
T: overruling | the act of a higher court, or a larger bench, declaring that an earlier decision was wrong in law
Q: Under Article 141, the law declared by the Supreme Court is binding on: | all courts within the territory of India | the Supreme Court alone | only High Courts | only the Union government
Q: The binding part of a judicial decision is the: | ratio decidendi | obiter dicta | headnote | dissenting opinion
Q: Stare decisis means: | to stand by things decided | let the buyer beware | the thing speaks for itself | let it stand
Q: In which case did the Supreme Court hold that it is not bound by its own earlier decisions? | Bengal Immunity Co. v State of Bihar (1955) | Kesavananda Bharati v State of Kerala (1973) | Maneka Gandhi v Union of India (1978) | Vishaka v State of Rajasthan (1997)
Q: The Supreme Court's power to pass any order for doing complete justice is in: | Article 142 | Article 141 | Article 32 | Article 226
Q: A decision of a foreign court cited in an Indian court is: | a persuasive precedent | a binding precedent | a statute | an ordinance
Q: Observations of a judge that are not necessary for the decision are called: | obiter dicta | ratio decidendi | res judicata | stare decisis
M:article: Article 141 | law declared by the Supreme Court binds all courts
M:article: Article 142 | Supreme Court may pass orders for complete justice
M:article: Article 123 | ordinance-making power of the President
M:article: Article 213 | ordinance-making power of the Governor
M:article: Article 137 | Supreme Court may review its own judgments
S+: Precedent brings certainty and consistency to the law
S+: The decisions of a High Court bind the subordinate courts within its territory
S+: The Supreme Court is not bound by its own earlier decisions and can depart from them
S+: A decision of a larger bench binds a smaller bench of the same court
S+: Obiter dicta of the Supreme Court are given great weight by lower courts even though they are not strictly binding
S-: Obiter dicta are the binding part of a judgment | The ratio decidendi is binding; obiter dicta are only persuasive
S-: The Supreme Court is bound by all its earlier decisions | The Supreme Court can depart from its earlier decisions, as held in Bengal Immunity (1955)
S-: A High Court decision binds courts in every state of India | A High Court decision binds only the courts subordinate to it; in other states it is persuasive
C: Precedent is said to make the law certain | courts deciding similar cases in the same way allows people to predict the legal result of their actions
C: The decisions of the Supreme Court bind all courts in India | Article 141 declares that the law declared by the Supreme Court is binding on all courts within India
C: Precedent is sometimes criticised as rigid | a wrong decision can be followed for a long time until a higher court or larger bench overrules it
X: C2 D2 2 | Distinguish between ratio decidendi and obiter dicta. | Ratio decidendi – the principle necessary for the decision, binding; obiter dicta – incidental remarks not needed for the decision, only persuasive.
X: C3 D3 3 | Explain the position of precedent in India with reference to Articles 141 and 142. | Article 141 – law declared by the Supreme Court binds all courts; Supreme Court not bound by its own decisions (Bengal Immunity 1955); High Courts bind subordinate courts; Article 142 – orders for complete justice.
X: C4 D4 3 | 'Judges do not merely declare the law, they also make it.' Examine with reference to precedent. | Declaratory theory vs judge-made law; filling gaps where no statute exists; examples – Vishaka guidelines (1997), basic structure (1973); limits – binding only through ratio, can be overruled or changed by legislation.
L: D4 | Explain precedent as a source of law. Discuss ratio decidendi and obiter dicta, kinds of precedents and the doctrine of precedent in India. | Meaning; stare decisis; ratio and obiter; binding and persuasive; original and declaratory; hierarchy – Supreme Court (Article 141), High Courts, larger and smaller benches; Bengal Immunity (1955); merits and demerits.
"""), ST(S + '07-st4', 'other sources of law', """
T: Shruti | the Vedas, regarded in Hindu law as revealed knowledge and the primary source
T: Smriti | texts 'remembered' by sages, such as the Manusmriti and the Yajnavalkya Smriti, that state rules of conduct
T: Mitakshara | the commentary by Vijnaneshwara on the Yajnavalkya Smriti, followed in most parts of India
T: Dayabhaga | the treatise by Jimutavahana, followed mainly in Bengal and Assam
T: Ijma | consensus of Muslim jurists on a point of law
T: Qiyas | analogical deduction from the Quran, Sunna and Ijma
T: juristic writings | the works of eminent jurists and scholars that courts consult to understand the law
Q: Which is the primary source of Muslim law? | The Quran | Qiyas | Ijma | Fatwa
Q: The Dayabhaga school of Hindu law was followed mainly in: | Bengal and Assam | Punjab and Haryana | Kerala | Gujarat
Q: The Mitakshara is a commentary on the: | Yajnavalkya Smriti | Manusmriti | Rig Veda | Arthashastra
Q: Sunna in Muslim law refers to: | the practices and sayings of the Prophet | consensus of jurists | analogical deduction | decisions of the Caliph
Q: Article 51(c) of the Constitution directs the state to: | foster respect for international law and treaty obligations | protect monuments | promote cottage industries | separate the judiciary from the executive
Q: In Vishaka v State of Rajasthan (1997) the Supreme Court relied on which international convention? | CEDAW | The Geneva Conventions | The UN Convention on the Rights of the Child | The Kyoto Protocol
M:source: Quran | primary source of Muslim law
M:source: Sunna | practice and sayings of the Prophet
M:source: Ijma | consensus of jurists
M:source: Qiyas | analogical deduction
S+: Religion has been an important source of personal law in India
S+: The four classical sources of Muslim law are the Quran, Sunna, Ijma and Qiyas
S+: The two main schools of Hindu law are Mitakshara and Dayabhaga
S+: Courts consult the writings of eminent jurists where statutes and precedents are silent or unclear
S+: Vishaka v State of Rajasthan (1997) used CEDAW to frame guidelines against sexual harassment at the workplace
S+: The guidelines in Vishaka were later replaced by the Sexual Harassment of Women at Workplace Act, 2013
S-: Juristic writings are binding on Indian courts | Juristic writings are only persuasive
S-: Qiyas is the primary source of Muslim law | The Quran is the primary source; Qiyas is analogical deduction
S-: The Mitakshara is followed only in Bengal | The Dayabhaga is followed in Bengal and Assam; the Mitakshara in most other parts of India
C: Juristic writings carry weight in court | they explain and systematise the law and are written by recognised experts, though they are not binding
C: International conventions can influence Indian law | under Article 51(c) and Article 253 India respects treaty obligations, and courts read conventions consistent with Fundamental Rights into domestic law
C: Much of Hindu personal law was codified in the 1950s | the Hindu Marriage Act and related Acts replaced many differing religious rules with uniform statutes
X: C2 D2 2 | Name the four sources of Muslim law. | Quran, Sunna (Hadith), Ijma and Qiyas.
X: C3 D3 3 | How have international conventions acted as a source of law in India? Give an example. | Article 51(c) and 253; courts read conventions into Fundamental Rights where no domestic law exists; Vishaka (1997) used CEDAW to frame guidelines; later the 2013 Act.
L: D4 | Explain religion, juristic writings and international conventions as sources of law with examples. | Hindu law – Shruti, Smriti, commentaries (Mitakshara, Dayabhaga), codification; Muslim law – Quran, Sunna, Ijma, Qiyas; juristic writings – persuasive value; conventions – Article 51(c), 253, Vishaka (1997).
""")]

CH08 = [ST(S + '08-st1', 'meaning and agencies of law reform', """
T: law reform | the process of changing, repealing or updating laws so that they meet the present needs of society
T: agency of law reform | a body or institution through which law is changed, such as the legislature, judiciary or a Law Commission
T: codification | the collection and systematic arrangement of laws on a subject in a single code
T: repeal | the cancellation of a law by the legislature
T: social legislation | laws passed to bring about social change, such as laws against dowry or child marriage
Q: Which of these is NOT an agency of law reform? | A private club | Legislature | Judiciary | Law Commission
Q: The Bharatiya Nyaya Sanhita, 2023 replaced the: | Indian Penal Code, 1860 | Code of Civil Procedure, 1908 | Indian Evidence Act, 1872 | Indian Contract Act, 1872
Q: The Bharatiya Nagarik Suraksha Sanhita, 2023 replaced the: | Code of Criminal Procedure, 1973 | Indian Penal Code, 1860 | Indian Evidence Act, 1872 | Specific Relief Act, 1963
Q: The Bharatiya Sakshya Adhiniyam, 2023 replaced the: | Indian Evidence Act, 1872 | Code of Criminal Procedure, 1973 | Indian Penal Code, 1860 | Limitation Act, 1963
Q: The three new criminal laws of 2023 came into force on: | 1 July 2024 | 26 January 2024 | 15 August 2023 | 1 April 2025
Q: The main agency that actually changes the text of a law in India is the: | legislature | Law Commission | press | Bar Council
Y: 1860 | enactment of the Indian Penal Code
Y: 2024 | the Bharatiya Nyaya Sanhita and the other new criminal laws come into force
S+: Law must change with society, otherwise it becomes outdated
S+: The legislature is the main agency of law reform because it can enact, amend and repeal laws
S+: The judiciary reforms law through interpretation, precedent and public interest litigation
S+: The Law Commission studies laws and recommends reforms to the government
S+: Public opinion, the media and civil society groups also press for law reform
S+: The Indian Penal Code, the Code of Criminal Procedure and the Indian Evidence Act were replaced by three new laws that came into force on 1 July 2024
S-: Only the courts can reform law in India | Law is reformed by the legislature, the judiciary, the Law Commission and other agencies
S-: Law reform means only making new laws | Law reform also includes amending, consolidating and repealing old laws
S-: The Law Commission can itself amend an Act | The Law Commission only recommends; Parliament or a state legislature amends laws
C: Law reform is a continuous process | society, technology and values keep changing, so laws must be updated to remain relevant
C: Parliament repeals obsolete laws from time to time | old laws that no longer serve a purpose clutter the statute book and can be misused
C: The judiciary is called an agency of law reform | through interpretation and precedent courts fill gaps and adapt the law to new situations
X: C2 D2 2 | What is meant by law reform? Name two agencies of law reform. | Updating, amending, repealing or consolidating laws to meet social needs; legislature, judiciary, Law Commission, executive, civil society (any two).
X: C3 D3 3 | Explain the need for law reform. | Social change; technological change (cyber, data); removing obsolete and colonial laws; filling gaps; ensuring justice and equality; simplifying and consolidating law.
L: D4 | Explain the meaning and need of law reform and discuss the role of the different agencies of law reform in India. | Meaning; need; legislature (enact, amend, repeal; 2023 criminal laws); judiciary (interpretation, PIL); Law Commission (reports); executive (rules, ordinances); public opinion and media.
"""), ST(S + '08-st2', 'the Law Commission of India', """
T: Law Commission of India | a body set up by the Government of India to study laws and recommend legal reform
T: First Law Commission | the commission set up in 1834 under the Charter Act of 1833, chaired by Lord Macaulay
T: report of the Law Commission | a study on a legal topic submitted to the government with recommendations, which are advisory
Q: The first Law Commission (1834) was chaired by: | Lord Macaulay | Lord Cornwallis | Lord Ripon | Lord Curzon
Q: The first Law Commission of independent India (1955) was chaired by: | M.C. Setalvad | B.R. Ambedkar | P.N. Bhagwati | V.R. Krishna Iyer
Q: The first Law Commission of 1834 was set up under the: | Charter Act of 1833 | Regulating Act of 1773 | Government of India Act, 1858 | Indian Councils Act, 1909
Q: The draft of which code was prepared by the first Law Commission under Macaulay? | Indian Penal Code | Code of Civil Procedure | Hindu Code | Constitution of India
Q: The 14th Report of the Law Commission (1958) dealt with: | reform of judicial administration | the death penalty | electoral reforms | cyber crime
Q: Recommendations of the Law Commission are: | advisory and not binding on the government | binding on Parliament | binding on courts | final and cannot be changed
Y: 1834 | the first Law Commission set up under Lord Macaulay
Y: 1955 | the first Law Commission of independent India set up under M.C. Setalvad
Y: 1958 | the 14th Report of the Law Commission on reform of judicial administration
Y: 2015 | the 262nd Report of the Law Commission on the death penalty
S+: The Law Commission of independent India is constituted by the Government of India for a fixed term
S+: The Law Commission is not a constitutional body
S+: The first Law Commission of independent India was chaired by M.C. Setalvad, the first Attorney General of India
S+: The 262nd Report (2015) recommended abolishing the death penalty for all crimes except terrorism-related offences and waging war
S+: Many Law Commission reports have led to new laws or amendments
S-: The Law Commission is established by the Constitution | The Law Commission is set up by the Government of India; it is not a constitutional body
S-: The government must accept every Law Commission report | Law Commission reports are advisory
S-: The first Law Commission of 1834 was chaired by M.C. Setalvad | It was chaired by Lord Macaulay; Setalvad chaired the first Commission after independence (1955)
C: The Law Commission's reports carry weight even though they are advisory | they are prepared by legal experts after detailed study and consultation
C: The government often refers specific questions to the Law Commission | it needs expert study of complex legal issues before changing the law
C: The Law Commission is described as a body for law reform | its main task is to review existing laws and recommend changes, repeal of obsolete laws and new legislation
X: C2 D2 2 | Name the chairpersons of the first Law Commission (1834) and of the first Law Commission of independent India. | Lord Macaulay (1834); M.C. Setalvad (1955).
X: C3 D3 3 | State three functions of the Law Commission of India. | Review laws and recommend reforms; identify obsolete laws for repeal; study subjects referred by the government; suggest new legislation; examine laws in the light of Directive Principles (any three).
L: D4 | Describe the role of the Law Commission of India in law reform with reference to its history and important reports. | Pre-independence commissions (Macaulay 1834, IPC draft); Setalvad Commission 1955; 14th Report (1958, judicial administration); 262nd Report (2015, death penalty); advisory nature; fixed term; impact on legislation.
"""), ST(S + '08-st3', 'the judiciary and public interest litigation', """
T: public interest litigation | a case filed in court for the protection of public interest, by any public-spirited person on behalf of those who cannot approach the court
T: locus standi | the right of a person to bring a case to court
T: epistolary jurisdiction | the practice of treating a letter or postcard sent to a judge as a writ petition
T: judicial activism | an active role by courts in protecting rights and filling gaps in the law
T: absolute liability | the rule that an enterprise engaged in a hazardous activity is fully liable for harm caused, with no exceptions
Q: The development of PIL in India is mainly associated with Justices: | P.N. Bhagwati and V.R. Krishna Iyer | Y.V. Chandrachud and A.N. Ray | H.J. Kania and M.C. Mahajan | J.S. Verma and A.M. Ahmadi
Q: Which case on undertrial prisoners in Bihar was an early PIL? | Hussainara Khatoon v State of Bihar (1979) | Olga Tellis v Bombay Municipal Corporation (1985) | Kesavananda Bharati v State of Kerala (1973) | Shah Bano (1985)
Q: The principle of absolute liability was laid down in: | M.C. Mehta v Union of India (1986) | Vishaka v State of Rajasthan (1997) | Maneka Gandhi v Union of India (1978) | S.P. Gupta v Union of India (1981)
Q: Olga Tellis v Bombay Municipal Corporation (1985) is known for recognising the right to: | livelihood as part of the right to life | privacy | education | information
Q: Bandhua Mukti Morcha v Union of India (1984) concerned: | bonded labour | the death penalty | triple talaq | judicial appointments
Q: In PIL, the rule of locus standi was: | relaxed so that any public-spirited person could approach the court | made stricter | abolished for all cases | applied only to the government
Q: Maneka Gandhi v Union of India (1978) held that procedure under Article 21 must be: | just, fair and reasonable | approved by Parliament | in writing | decided by a jury
M:case: Hussainara Khatoon (1979) | speedy trial for undertrial prisoners
M:case: M.C. Mehta (1986) | absolute liability for hazardous industries
M:case: Olga Tellis (1985) | right to livelihood of pavement dwellers
M:case: Bandhua Mukti Morcha (1984) | release of bonded labourers
M:case: Vishaka (1997) | guidelines against sexual harassment at the workplace
M:case: Maneka Gandhi (1978) | procedure must be just, fair and reasonable
S+: PIL relaxed the traditional rule that only the aggrieved person can approach the court
S+: In S.P. Gupta v Union of India (1981) the Supreme Court broadened the rule of locus standi
S+: PIL can be filed in the Supreme Court under Article 32 and in a High Court under Article 226
S+: Courts have treated letters from citizens and prisoners as writ petitions
S+: Through PIL the courts have widened the meaning of the right to life under Article 21
S+: PIL has been used to protect the environment, prisoners, bonded labourers and workers
S-: Only the person whose right is violated can file a PIL | Any public-spirited person or organisation can file a PIL on behalf of others
S-: PIL can be filed only in the Supreme Court | PIL can be filed in the Supreme Court (Article 32) or a High Court (Article 226)
S-: PIL was introduced by an Act of Parliament | PIL was developed by the judiciary through its decisions
C: PIL is called a tool of social justice | it lets courts protect the rights of poor and disadvantaged people who cannot approach the court themselves
C: Courts have warned against frivolous PILs | misuse for publicity or private interest wastes judicial time and delays genuine cases
C: The judiciary is an important agency of law reform | through PIL and interpretation it has created rights and guidelines where the legislature had not acted
X: C2 D2 2 | What is public interest litigation? Name one judge associated with its growth. | A case filed by any public-spirited person for the public interest or for those unable to approach the court; Justice P.N. Bhagwati or Justice V.R. Krishna Iyer.
X: C3 D3 3 | Explain three ways in which PIL has contributed to law reform in India, with cases. | Speedy trial (Hussainara Khatoon 1979); absolute liability (M.C. Mehta 1986); livelihood (Olga Tellis 1985); bonded labour (Bandhua Mukti Morcha 1984); workplace harassment (Vishaka 1997) (any three).
L: D4 | Discuss the role of the judiciary in law reform with special reference to public interest litigation. Mention its merits and limitations. | Interpretation and precedent; relaxation of locus standi (S.P. Gupta 1981); epistolary jurisdiction; Articles 32 and 226; landmark PILs; widening Article 21 (Maneka Gandhi 1978); merits – access to justice; limits – frivolous PILs, overreach, burden on courts.
""")]

CH09 = [ST(S + '09-st1', 'cyberspace and cybercrime', """
T: cyberspace | the virtual environment created by connected computers and networks, including the internet
T: cybercrime | any unlawful act in which a computer or network is the tool, the target or both
T: hacking | gaining unauthorised access to a computer system or network
T: phishing | sending fraudulent messages that appear to come from a trusted source to steal personal or financial information
T: identity theft | fraudulently using another person's password, electronic signature or other unique identification feature
T: cyberstalking | repeatedly using electronic communication to harass, threaten or follow a person
T: malware | malicious software, such as viruses, worms or trojans, designed to damage or gain control of a computer
T: ransomware | malware that locks or encrypts a victim's data and demands payment to release it
Q: Sending an e-mail that looks like it is from a bank to obtain a person's login details is: | phishing | cyberstalking | software piracy | spamming
Q: Gaining unauthorised access to someone's computer system is called: | hacking | phishing | spoofing | cyber squatting
Q: Malware that encrypts a victim's files and demands payment is: | ransomware | spyware | adware | freeware
Q: Repeatedly sending threatening messages to a person through social media is: | cyberstalking | phishing | hacking | data diddling
Q: Using another person's password to log in and act as that person is: | identity theft | cyber squatting | denial of service | spamming
Q: Flooding a website with traffic so that genuine users cannot access it is a: | denial of service attack | phishing attack | identity theft | logic bomb
S+: In cybercrime the computer may be the target of the crime, the tool used to commit it, or both
S+: Cybercrimes can be committed from anywhere in the world, which creates problems of jurisdiction
S+: Phishing tricks victims into revealing passwords, card numbers or OTPs
S+: Ransomware attacks lock or encrypt data until a ransom is paid
S+: Victims in India can report cybercrime on the national cybercrime reporting portal or the helpline 1930
S-: Cybercrime can only be committed by professional hackers | Ordinary users can also commit cybercrimes such as cyberstalking or identity theft
S-: Cybercrimes are always limited to one country | Cybercrimes often cross national borders
S-: Phishing means gaining physical access to a computer | Phishing means tricking people into giving personal information through fake messages or websites
C: Cybercrimes are difficult to investigate | offenders can hide their identity and act from other countries, and digital evidence can be easily destroyed
C: Users are advised never to share OTPs and passwords | fraudsters use them to take over accounts and steal money through phishing and identity theft
C: Cyberstalking is treated as a serious offence | it causes fear and mental harm to the victim and can lead to physical harm
X: C2 D2 2 | Distinguish between hacking and phishing. | Hacking – unauthorised access to a computer system; phishing – tricking people with fake messages or sites into revealing personal or financial information.
X: C3 D3 3 | Explain any three types of cybercrime. | Hacking; phishing; identity theft; cyberstalking; ransomware or malware; denial of service (any three, each explained).
L: D4 | What is cybercrime? Explain its main types and suggest measures to prevent it. | Meaning (computer as target or tool); types – hacking, phishing, identity theft, cyberstalking, malware and ransomware, denial of service; problems – anonymity, jurisdiction; prevention – strong passwords, two-factor authentication, not sharing OTPs, updates, reporting (1930, cybercrime portal), awareness.
"""), ST(S + '09-st2', 'the Information Technology Act, 2000', """
T: Information Technology Act, 2000 | India's main law on electronic commerce, electronic records and cybercrime
T: intermediary | a person who on behalf of another receives, stores or transmits electronic records, such as an internet service provider or a social media platform
T: CERT-In | the Indian Computer Emergency Response Team, the national agency for responding to cyber security incidents (section 70B)
T: cyber terrorism | an act against computer resources intended to threaten the unity, integrity, security or sovereignty of India or strike terror in people (section 66F)
T: safe harbour | the protection of an intermediary from liability for third-party content if it observes due diligence (section 79)
Q: The Information Technology Act, 2000 is based on the: | UNCITRAL Model Law on Electronic Commerce, 1996 | Budapest Convention, 2001 | Geneva Conventions | TRIPS Agreement
Q: The IT Act, 2000 was substantially amended in: | 2008 | 2002 | 2012 | 2019
Q: Which section of the IT Act deals with identity theft? | Section 66C | Section 66F | Section 67 | Section 43
Q: Section 66F of the IT Act deals with: | cyber terrorism | identity theft | obscene material | tampering with source documents
Q: In Shreya Singhal v Union of India (2015) the Supreme Court struck down section: | 66A | 66F | 67 | 79
Q: Section 69A of the IT Act empowers the government to: | block public access to information online | punish identity theft | appoint judges | levy GST on software
Q: The national agency for cyber security incidents under section 70B is: | CERT-In | NALSA | CARA | NCPCR
Q: Penalty and compensation for unauthorised access and damage to a computer system is provided in section: | 43 | 66F | 67B | 79
M:section: Section 65 | tampering with computer source documents
M:section: Section 66C | identity theft
M:section: Section 66D | cheating by personation using a computer resource
M:section: Section 66E | violation of privacy by capturing or publishing private images
M:section: Section 66F | cyber terrorism
M:section: Section 67 | publishing obscene material in electronic form
M:section: Section 79 | exemption of intermediaries from liability
Y: 2000 | enactment of the Information Technology Act
Y: 2008 | the Information Technology (Amendment) Act
Y: 2015 | section 66A struck down in Shreya Singhal v Union of India
S+: The IT Act, 2000 gives legal recognition to electronic records and electronic signatures
S+: The IT Act was enacted on the basis of the UNCITRAL Model Law on Electronic Commerce
S+: The 2008 amendment added new offences such as identity theft (66C), cheating by personation (66D), violation of privacy (66E) and cyber terrorism (66F)
S+: Section 66F prescribes punishment of up to imprisonment for life for cyber terrorism
S+: In Shreya Singhal v Union of India (2015) section 66A was struck down as violating freedom of speech under Article 19(1)(a)
S+: Section 79 protects intermediaries from liability for third-party content if they follow due diligence
S-: Section 66A of the IT Act is still in force | Section 66A was struck down in Shreya Singhal v Union of India (2015)
S-: The IT Act deals only with e-commerce and has no offences | The IT Act also defines cyber offences and penalties
S-: Section 66C deals with cyber terrorism | Section 66C deals with identity theft; cyber terrorism is under section 66F
C: Section 66A of the IT Act was struck down | its vague terms like 'grossly offensive' and 'annoyance' violated freedom of speech and expression under Article 19(1)(a)
C: The IT Act was amended in 2008 | new forms of cybercrime such as identity theft and cyber terrorism had appeared and needed specific provisions
C: Intermediaries get conditional protection under section 79 | they only transmit or host content made by others, but they must follow due diligence and act on lawful orders
X: C2 D2 2 | State any two objectives of the Information Technology Act, 2000. | Legal recognition of electronic records and transactions; legal recognition of digital signatures; facilitate e-governance and e-filing; define and punish cyber offences (any two).
X: C3 D3 3 | Explain any three offences under the IT Act, 2000 with their sections. | 65 tampering with source documents; 66 computer-related offences; 66C identity theft; 66D cheating by personation; 66E violation of privacy; 66F cyber terrorism; 67 obscene material (any three).
X: C4 D4 3 | Why was section 66A struck down in Shreya Singhal (2015)? What does this show about the balance between regulating cyberspace and free speech? | Vague and overbroad terms; chilling effect on speech; not saved by reasonable restrictions under Article 19(2); shows that cyber laws must be precise and respect Fundamental Rights while still punishing real harm.
L: D5 | Discuss the objectives and main provisions of the Information Technology Act, 2000, including its offences and the role of intermediaries and CERT-In. | Objectives; UNCITRAL basis; e-records (s.4) and signatures (s.3, 3A); civil penalty (s.43); offences 65, 66, 66C-66F, 67; blocking (s.69A); CERT-In (s.70B); intermediaries (s.79); 2008 amendment; Shreya Singhal (2015).
"""), ST(S + '09-st3', 'electronic records, digital signatures and data protection', """
T: electronic record | data, record or information generated, sent, received or stored in electronic form
T: digital signature | a method of authenticating an electronic record using an asymmetric crypto system and hash function (section 3 of the IT Act)
T: electronic signature | authentication of an electronic record by a technique notified under the IT Act, including digital signatures (section 3A)
T: Certifying Authority | a body licensed to issue Digital Signature Certificates
T: Controller of Certifying Authorities | the authority that licenses and regulates Certifying Authorities under the IT Act
T: data principal | under the DPDP Act, 2023, the individual to whom personal data relates
T: data fiduciary | under the DPDP Act, 2023, a person who decides the purpose and means of processing personal data
Q: Legal recognition of electronic records is given by section: | 4 of the IT Act | 66 of the IT Act | 79 of the IT Act | 43 of the IT Act
Q: A digital signature uses: | a private key and a public key | only a password | a handwritten signature scanned | a rubber stamp
Q: Digital Signature Certificates are issued by: | Certifying Authorities | the Election Commission | the Reserve Bank of India | High Courts
Q: The right to privacy was declared a Fundamental Right in: | Justice K.S. Puttaswamy v Union of India (2017) | Maneka Gandhi v Union of India (1978) | Shreya Singhal v Union of India (2015) | Kesavananda Bharati v State of Kerala (1973)
Q: The Digital Personal Data Protection Act was enacted in: | 2023 | 2000 | 2008 | 2019
Q: Under the DPDP Act, 2023 the individual whose personal data is processed is called the: | data principal | data fiduciary | data processor | Certifying Authority
Q: The body set up under the DPDP Act, 2023 to deal with breaches is the: | Data Protection Board of India | CERT-In | Cyber Appellate Tribunal | Law Commission
Y: 2017 | the nine-judge bench decision in Puttaswamy recognising the right to privacy
Y: 2023 | enactment of the Digital Personal Data Protection Act
S+: The IT Act gives electronic records the same legal recognition as written documents where the law requires writing
S+: A digital signature is created with the signer's private key and verified with the matching public key
S+: Certifying Authorities are licensed and regulated by the Controller of Certifying Authorities
S+: A nine-judge bench in Puttaswamy (2017) held that privacy is a Fundamental Right protected under Article 21 and Part III
S+: The DPDP Act, 2023 requires personal data to be processed for a lawful purpose, generally with the consent of the data principal
S-: Electronic records have no legal value in India | Section 4 of the IT Act gives legal recognition to electronic records
S-: A digital signature is a scanned image of a handwritten signature | A digital signature is created using an asymmetric key pair and a hash function
S-: The right to privacy is not a Fundamental Right in India | Puttaswamy (2017) declared privacy a Fundamental Right
C: Digital signatures make online transactions trustworthy | they authenticate the sender and show whether the record was altered after signing
C: A data protection law was needed in India | huge amounts of personal data are collected online and the Supreme Court had recognised privacy as a Fundamental Right in 2017
C: Certifying Authorities are regulated by a Controller | public trust in digital signatures depends on certificates being issued only after proper verification
X: C2 D2 2 | What is a digital signature? Who issues a Digital Signature Certificate? | Authentication of an electronic record by an asymmetric crypto system and hash function (private and public keys); issued by a licensed Certifying Authority.
X: C3 D3 3 | Explain the significance of the Puttaswamy judgment (2017) for data protection in India. | Nine-judge bench; privacy a Fundamental Right under Article 21 and Part III; informational privacy; led to the need for a data protection law – DPDP Act 2023.
L: D4 | Explain the legal position of electronic records and digital signatures in India and describe the main features of the Digital Personal Data Protection Act, 2023. | IT Act s.4 (e-records), s.3 and 3A (digital and electronic signatures); key pair and hash; Certifying Authorities and Controller; Puttaswamy (2017); DPDP Act – data principal, data fiduciary, consent, lawful purpose, Data Protection Board.
""")]

CH10 = [ST(S + '10-st1', 'the hierarchy of courts in India', """
T: integrated judiciary | a single hierarchy of courts with the Supreme Court at the top, which applies both Union and state laws
T: Supreme Court | the highest court of India, established under Article 124
T: High Court | the highest court of a state, established under Article 214
T: subordinate courts | courts below the High Court, such as district courts and magistrates' courts (Articles 233 to 237)
T: District Judge | the highest judicial officer of a district for civil cases; as Sessions Judge he tries serious criminal cases
T: Court of Session | the court of the Sessions Judge, which tries serious criminal offences in a district
Q: The Supreme Court of India is established under: | Article 124 | Article 214 | Article 32 | Article 233
Q: 'There shall be a High Court for each State' is provided in: | Article 214 | Article 124 | Article 226 | Article 141
Q: District judges are appointed by the: | Governor in consultation with the High Court | President on advice of the Prime Minister | Chief Justice of India alone | Union Law Minister
Q: Control over the subordinate courts is vested in the: | High Court | Supreme Court | State Legislature | Chief Minister
Q: Including the Chief Justice, the maximum sanctioned strength of the Supreme Court is now: | 34 | 31 | 26 | 8
Q: Parliament may establish a common High Court for two or more states under: | Article 231 | Article 214 | Article 124 | Article 32
M:court: Article 124 | establishment of the Supreme Court
M:court: Article 214 | High Court for each state
M:court: Article 231 | common High Court for two or more states
M:court: Article 233 | appointment of district judges
M:court: Article 235 | control of the High Court over subordinate courts
S+: India has a single integrated judicial system with the Supreme Court at its apex
S+: The same hierarchy of courts applies both Union and state laws
S+: The Supreme Court started in 1950 with a Chief Justice and seven other judges; its sanctioned strength is now 34 including the Chief Justice
S+: The district court is the principal civil court of a district, and the Sessions Court is its principal criminal court
S+: The High Court controls the subordinate courts in its state under Article 235
S-: India has separate federal and state court systems as in the USA | India has a single integrated judiciary
S-: Subordinate courts are controlled by the state government | Subordinate courts are controlled by the High Court
S-: The Supreme Court has always had 34 judges | It started in 1950 with eight judges; the strength has been increased by Parliament over time
C: India is said to have an integrated judiciary | there is one hierarchy of courts with the Supreme Court at the top applying both Union and state laws
C: Decisions of a High Court bind the subordinate courts of the state | the High Court is at the head of the state judiciary and supervises and controls the subordinate courts
C: The Supreme Court is called the guardian of the Constitution | it interprets the Constitution and can strike down laws and actions that violate it
X: C2 D2 2 | Name the articles under which the Supreme Court and the High Courts are established. | Supreme Court – Article 124; High Courts – Article 214.
X: C3 D3 3 | Describe the structure of subordinate courts in a district. | District Judge (civil) and Sessions Judge (criminal) at the top; below them civil judges (senior and junior division) and judicial magistrates; appointed under Articles 233-237; controlled by the High Court.
L: D4 | Explain the hierarchy of courts in India with the help of a diagram or flow chart. | Supreme Court (Article 124) – High Courts (Article 214, common HC Article 231) – district and sessions courts – civil judges and judicial magistrates; integrated judiciary; Article 235 control; appointments; precedent binding down the hierarchy.
"""), ST(S + '10-st2', 'jurisdiction of the Supreme Court and High Courts', """
T: original jurisdiction | the power of a court to hear a case for the first time
T: appellate jurisdiction | the power of a higher court to hear appeals against decisions of lower courts
T: advisory jurisdiction | the power of the Supreme Court to give its opinion on a question referred by the President (Article 143)
T: writ jurisdiction | the power to issue writs such as habeas corpus and mandamus to enforce rights
T: special leave petition | a petition under Article 136 asking the Supreme Court for leave to appeal against any judgment or order of a court or tribunal in India
T: court of record | a court whose judgments are preserved as evidence and which can punish for its own contempt (Articles 129 and 215)
T: habeas corpus | a writ ordering a person who has detained another to produce the detained person before the court
T: mandamus | a writ commanding a public authority to perform a public duty it has failed to perform
T: certiorari | a writ by which a higher court quashes an order already passed by a lower court or tribunal without jurisdiction
T: quo warranto | a writ asking a person by what authority he holds a public office
Q: Disputes between the Government of India and one or more states fall under the Supreme Court's original jurisdiction under: | Article 131 | Article 136 | Article 143 | Article 226
Q: The advisory jurisdiction of the Supreme Court is given in: | Article 143 | Article 131 | Article 32 | Article 141
Q: Special leave to appeal is granted by the Supreme Court under: | Article 136 | Article 131 | Article 143 | Article 227
Q: The power of a High Court to issue writs is given in: | Article 226 | Article 32 | Article 136 | Article 143
Q: The power of superintendence of a High Court over courts and tribunals in its territory is in: | Article 227 | Article 226 | Article 215 | Article 124
Q: Which writ is issued to release a person who is unlawfully detained? | Habeas corpus | Mandamus | Certiorari | Quo warranto
Q: The writ jurisdiction of a High Court is wider than that of the Supreme Court because: | High Courts can issue writs for Fundamental Rights and for any other purpose | High Courts have more judges | High Courts can overrule the Supreme Court | the Supreme Court cannot issue writs
M:jurisdiction: Article 131 | original jurisdiction in federal disputes
M:jurisdiction: Article 136 | special leave to appeal
M:jurisdiction: Article 143 | advisory jurisdiction
M:jurisdiction: Article 32 | writs for Fundamental Rights by the Supreme Court
M:jurisdiction: Article 226 | writs by High Courts
M:jurisdiction: Article 129 | Supreme Court as a court of record
S+: Article 32 is itself a Fundamental Right, and Dr B.R. Ambedkar called it the heart and soul of the Constitution
S+: Under Article 32 the Supreme Court can issue writs only for the enforcement of Fundamental Rights
S+: Under Article 226 a High Court can issue writs for Fundamental Rights and for any other purpose
S+: The Supreme Court hears appeals in constitutional, civil and criminal cases under Articles 132 to 134
S+: The advice given by the Supreme Court under Article 143 is not binding on the President
S+: Both the Supreme Court and the High Courts are courts of record with power to punish for their own contempt
S-: The opinion given by the Supreme Court under Article 143 is binding on the President | The advisory opinion under Article 143 is not binding
S-: The Supreme Court can issue writs under Article 32 for any legal right | Article 32 writs are only for enforcing Fundamental Rights
S-: Special leave petitions can be filed only against High Court judgments | Under Article 136 special leave may be sought against any court or tribunal in India, except military tribunals
C: The writ jurisdiction of High Courts is wider than that of the Supreme Court | Article 226 allows writs for Fundamental Rights and for any other purpose, while Article 32 is only for Fundamental Rights
C: The Supreme Court acts as a federal court | under Article 131 it alone decides disputes between the Union and the states or between states
C: Article 136 is described as a residuary power | it lets the Supreme Court grant leave to appeal from almost any court or tribunal to prevent grave injustice
X: C2 D2 2 | Distinguish between the writ jurisdiction of the Supreme Court and that of a High Court. | Supreme Court (Article 32) – only for Fundamental Rights, itself a Fundamental Right; High Court (Article 226) – Fundamental Rights and any other purpose, so wider in scope.
X: C3 D3 3 | Explain the original, advisory and appellate jurisdiction of the Supreme Court. | Original – Article 131 federal disputes (and Article 32 writs); advisory – Article 143 reference by the President, not binding; appellate – Articles 132-134 and special leave under Article 136.
X: C4 D4 3 | 'The Supreme Court is the guardian of the Constitution and the protector of Fundamental Rights.' Justify with reference to its jurisdiction. | Article 32 writs; judicial review; Article 131 federal disputes; Article 141 binding law; Article 142 complete justice; Article 136 special leave; advisory role; examples.
L: D5 | Describe the jurisdiction of the Supreme Court and of the High Courts in India. | Supreme Court – original (Article 131), writ (32), appellate (132-134), special leave (136), advisory (143), court of record (129), review (137); High Court – writ (226), superintendence (227), appellate, court of record (215), control of subordinate courts (235); five writs.
"""), ST(S + '10-st3', 'independence of the judiciary and appointment of judges', """
T: independence of the judiciary | the freedom of judges to decide cases impartially without pressure from the executive, legislature or others
T: collegium | the body of the Chief Justice of India and the four senior-most judges of the Supreme Court that recommends appointments and transfers of judges
T: security of tenure | the guarantee that judges can be removed only by the special procedure laid down in the Constitution
T: removal of a judge | removal by an order of the President after an address by both Houses of Parliament with a special majority, on the ground of proved misbehaviour or incapacity
T: NJAC | the National Judicial Appointments Commission created by the 99th Amendment (2014) and struck down by the Supreme Court in 2015
Q: A judge of the Supreme Court retires at the age of: | 65 years | 62 years | 60 years | 70 years
Q: A judge of a High Court retires at the age of: | 62 years | 65 years | 60 years | 58 years
Q: The removal of a Supreme Court judge is provided in: | Article 124(4) | Article 61 | Article 356 | Article 143
Q: The collegium system was created by the: | Second Judges case (1993) | First Judges case (1981) | Kesavananda Bharati case (1973) | Golaknath case (1967)
Q: The National Judicial Appointments Commission was created by the: | 99th Amendment (2014) | 42nd Amendment (1976) | 44th Amendment (1978) | 86th Amendment (2002)
Q: Separation of the judiciary from the executive in public services is a Directive Principle under: | Article 50 | Article 44 | Article 39A | Article 48A
Q: The salaries of Supreme Court judges are charged on the: | Consolidated Fund of India | Contingency Fund of India | Public Account of India | Consolidated Fund of the state
Y: 1981 | the First Judges case (S.P. Gupta v Union of India)
Y: 1993 | the Second Judges case creates the collegium system
Y: 1998 | the Third Judges case enlarges the collegium to five judges
Y: 2014 | the 99th Amendment creates the National Judicial Appointments Commission
S+: Judges of the Supreme Court are appointed by the President under Article 124(2)
S+: Under the collegium system, appointments are recommended by the Chief Justice of India and the four senior-most judges of the Supreme Court
S+: The Supreme Court struck down the NJAC in 2015 and restored the collegium system
S+: The salaries and allowances of judges cannot be varied to their disadvantage after appointment, except during a financial emergency
S+: The conduct of a judge cannot be discussed in Parliament except on a motion for removal (Article 121)
S+: A retired judge of the Supreme Court cannot plead or act in any court in India (Article 124(7))
S-: Supreme Court judges can be removed by the President at any time | They can be removed only after an address by both Houses with a special majority on proved misbehaviour or incapacity
S-: Supreme Court judges retire at 62 | Supreme Court judges retire at 65; High Court judges at 62
S-: The NJAC is the present system of appointing judges | The NJAC was struck down in 2015; the collegium system continues
C: Judges' salaries are charged on the Consolidated Fund of India | this means they are not voted on by Parliament, so the legislature cannot pressure judges through their pay
C: The removal procedure for judges is made difficult | security of tenure lets judges decide fearlessly without worrying about losing office
C: The Supreme Court struck down the NJAC | it held that giving the executive a role in appointments threatened the independence of the judiciary, part of the basic structure
X: C2 D2 2 | State two constitutional provisions that secure the independence of the judiciary. | Security of tenure (removal under Article 124(4)); salaries charged on the Consolidated Fund and not reducible; bar on discussing conduct (Article 121); bar on practice after retirement; power to punish contempt (any two).
X: C3 D3 3 | Trace the development of the collegium system through the Judges cases. | First Judges case (1981) – executive primacy; Second Judges case (1993) – collegium, primacy of CJI; Third Judges case (1998) – CJI plus four senior-most judges; NJAC (2014) struck down in 2015.
L: D4 | Explain how the Constitution secures the independence of the judiciary and discuss the debate over the appointment of judges. | Appointment (Article 124(2)); tenure and removal (124(4)); salaries; Article 121; Article 124(7); contempt power; Article 50; Judges cases (1981, 1993, 1998); NJAC and 2015 judgment; arguments for and against the collegium (transparency vs independence).
"""), ST(S + '10-st4', 'civil and criminal court procedure', """
T: plaint | the written statement of claim filed by the plaintiff to start a civil suit
T: written statement | the defendant's written reply to the plaint
T: framing of issues | the stage in a civil suit at which the court states the points in dispute to be decided
T: decree | the formal expression of the court's decision in a civil suit
T: execution | the process of enforcing a decree
T: FIR | the First Information Report, the information about a cognizable offence first recorded by the police
T: charge sheet | the final report filed by the police after investigation, stating the offences and evidence against the accused
T: cognizable offence | an offence for which the police can arrest without a warrant
T: bail | the release of an accused person from custody on security, pending trial
Q: A civil suit begins with the filing of a: | plaint | charge sheet | FIR | decree
Q: The defendant's reply to the plaint is the: | written statement | charge sheet | decree | summons
Q: The procedure in civil courts is mainly governed by the: | Code of Civil Procedure, 1908 | Bharatiya Nyaya Sanhita, 2023 | Indian Contract Act, 1872 | Specific Relief Act, 1963
Q: In a criminal case, the standard of proof required is: | proof beyond reasonable doubt | preponderance of probabilities | prima facie case | the balance of convenience
Q: The final report of the police after investigation is the: | charge sheet | plaint | decree | written statement
Q: An offence for which the police can arrest without a warrant is: | a cognizable offence | a non-cognizable offence | a civil wrong | a compoundable offence
Q: Criminal procedure in India is now governed by the: | Bharatiya Nagarik Suraksha Sanhita, 2023 | Code of Civil Procedure, 1908 | Bharatiya Sakshya Adhiniyam, 2023 | Indian Penal Code, 1860
S+: The parties in a civil suit are the plaintiff and the defendant
S+: In a criminal case the State prosecutes the accused, usually through a public prosecutor
S+: A civil suit passes through filing of the plaint, summons, written statement, framing of issues, evidence, arguments, judgment and decree
S+: A criminal case usually passes through FIR, investigation, charge sheet, framing of charge, trial, judgment and sentence
S+: In civil cases a fact is proved on a preponderance of probabilities; in criminal cases guilt must be proved beyond reasonable doubt
S+: Witnesses are examined in chief, cross-examined by the other side and may be re-examined
S-: A criminal case begins with the filing of a plaint | A criminal case usually begins with an FIR or a complaint; a plaint starts a civil suit
S-: In a criminal case the victim alone prosecutes the accused | The State prosecutes the accused through the public prosecutor
S-: A decree is the first stage of a civil suit | A decree is passed at the end of a civil suit after the judgment
C: Guilt in a criminal case must be proved beyond reasonable doubt | a criminal conviction can take away a person's liberty, so the law gives the accused the benefit of doubt
C: The court frames issues in a civil suit | it fixes the exact points in dispute so that evidence and arguments are limited to them
C: Cross-examination is an important stage of a trial | it tests the truth and accuracy of a witness's evidence
X: C2 D2 2 | Distinguish between a plaint and an FIR. | Plaint – written claim by the plaintiff that starts a civil suit, filed in court; FIR – information about a cognizable offence recorded by the police, which starts criminal investigation.
X: C3 D3 3 | List in order the main stages of a civil suit. | Plaint; summons; written statement; framing of issues; evidence; arguments; judgment and decree; appeal or execution.
L: D4 | Explain the stages of a civil suit and of a criminal trial, bringing out the main differences between them. | Civil – plaint to decree and execution (CPC 1908); criminal – FIR, investigation, charge sheet, charge, trial, judgment, sentence (BNSS 2023); parties; standard of proof; remedies (damages vs punishment); appeals.
""")]

CH11 = [ST(S + '11-st1', 'personal laws and the Uniform Civil Code', """
T: personal law | the law governing family matters such as marriage, divorce, maintenance, adoption and succession, based largely on religion
T: Uniform Civil Code | a single set of civil laws on family matters applicable to all citizens irrespective of religion
T: Hindu Code Bills | the set of laws passed in 1955-56 that codified Hindu personal law
T: Special Marriage Act, 1954 | the law for civil marriage between any two persons irrespective of religion
Q: The Uniform Civil Code is mentioned in: | Article 44 | Article 14 | Article 25 | Article 51A
Q: Which Indian state has long had a common civil code from the Portuguese period? | Goa | Kerala | Punjab | Tamil Nadu
Q: The Muslim Personal Law (Shariat) Application Act was passed in: | 1937 | 1954 | 1955 | 1986
Q: The Hindu Marriage Act, 1955 applies to Hindus and also to: | Buddhists, Jains and Sikhs | Muslims | Christians | Parsis
Q: Two persons of different religions who wish to marry without conversion may do so under the: | Special Marriage Act, 1954 | Hindu Marriage Act, 1955 | Indian Christian Marriage Act, 1872 | Family Courts Act, 1984
Q: In 2024, which state passed its own Uniform Civil Code law? | Uttarakhand | Goa | Gujarat | Kerala
M:law: Hindu Marriage Act | 1955
M:law: Special Marriage Act | 1954
M:law: Muslim Personal Law (Shariat) Application Act | 1937
M:law: Indian Christian Marriage Act | 1872
M:law: Parsi Marriage and Divorce Act | 1936
S+: India has different personal laws for Hindus, Muslims, Christians and Parsis
S+: Hindu personal law was codified in 1955-56 by the Hindu Marriage Act, the Hindu Succession Act, the Hindu Minority and Guardianship Act and the Hindu Adoptions and Maintenance Act
S+: The Uniform Civil Code is a Directive Principle and is not enforceable by courts
S+: Supporters say a Uniform Civil Code promotes gender justice and national integration
S+: Opponents argue that a Uniform Civil Code may affect the freedom of religion and cultural diversity of minorities
S-: The Uniform Civil Code is a Fundamental Right | It is a Directive Principle under Article 44 and is not justiciable
S-: All Indians are governed by a single family law | Family matters are governed by different personal laws based mainly on religion
S-: The Special Marriage Act applies only to Hindus | The Special Marriage Act applies to all persons irrespective of religion
C: Article 44 cannot be enforced in a court | it is a Directive Principle, and Article 37 makes Directive Principles non-justiciable
C: Many argue for a Uniform Civil Code on grounds of gender justice | several personal-law rules have treated women unequally in marriage, divorce and succession
C: The Special Marriage Act provides an alternative to personal laws | it allows any two persons to marry by a civil procedure without changing their religion
X: C2 D2 2 | What is a Uniform Civil Code? Under which article is it mentioned? | A single set of family laws for all citizens irrespective of religion; Article 44 (Directive Principle).
X: C3 D3 3 | Give arguments for and against a Uniform Civil Code. | For – equality and gender justice, national integration, simplification; against – freedom of religion (Articles 25-28), diversity, fears of minorities, need for consensus.
L: D4 | Explain the system of personal laws in India and examine the debate on the Uniform Civil Code. | Personal laws of different communities; Hindu Code (1955-56); Shariat Act 1937; Christian and Parsi laws; Special Marriage Act 1954; Article 44; Goa; Uttarakhand 2024; arguments for and against.
"""), ST(S + '11-st2', 'marriage under Hindu and Muslim law', """
T: saptapadi | the taking of seven steps by the bride and bridegroom around the sacred fire; the marriage is complete when the seventh step is taken (section 7 of the Hindu Marriage Act)
T: sapinda relationship | a relationship within a specified number of generations on the father's or mother's side, within which marriage is barred unless custom permits
T: nikah | marriage under Muslim law, regarded as a civil contract
T: mahr | the money or property that the husband pays or promises to pay to the wife as a mark of respect on marriage
T: ijab and qubul | proposal and acceptance, the essential elements of a Muslim marriage
T: monogamy | the rule that a person may have only one spouse at a time
Q: Under the Hindu Marriage Act, 1955 the minimum age of the bridegroom is: | 21 years | 18 years | 25 years | 16 years
Q: Under the Hindu Marriage Act, 1955 the minimum age of the bride is: | 18 years | 21 years | 16 years | 15 years
Q: The conditions for a valid Hindu marriage are listed in section: | 5 | 7 | 13 | 25
Q: Under Muslim law marriage is regarded as: | a civil contract | a sacrament only | a religious vow that cannot be ended | a property transfer
Q: The dower given to a Muslim wife is called: | mahr | iddat | khula | talaq
Q: A Hindu marriage performed when one party already has a living spouse is: | void | voidable | valid | valid after registration
S+: The Hindu Marriage Act requires that neither party has a living spouse at the time of marriage
S+: Under the Hindu Marriage Act a marriage may be solemnised according to the customary rites of either party
S+: Under the Hindu Marriage Act marriage within prohibited degrees or between sapindas is barred unless custom permits it
S+: A Muslim marriage requires a proposal and acceptance, competent parties and free consent
S+: Mahr is a right of the Muslim wife, and it may be prompt (payable on demand) or deferred
S+: The Prohibition of Child Marriage Act, 2006 also fixes the age of marriage at 21 for males and 18 for females
S-: A Hindu marriage is valid even if one party already has a living spouse | Such a marriage is void; the Act requires monogamy
S-: Mahr is paid by the wife's family to the husband | Mahr is paid or promised by the husband to the wife
S-: Under the Hindu Marriage Act the minimum age of both parties is 18 | The bridegroom must be 21 and the bride 18
C: Muslim marriage is described as a contract | it is formed by proposal and acceptance between competent parties with free consent, and mahr is its consideration
C: A bigamous Hindu marriage is void | section 5 of the Hindu Marriage Act requires that neither party has a spouse living at the time of the marriage
C: Saptapadi is important in many Hindu marriages | where it is part of the rites, the marriage becomes complete and binding when the seventh step is taken
X: C2 D2 2 | State any two conditions of a valid Hindu marriage under section 5 of the Hindu Marriage Act. | No living spouse (monogamy); capacity to give valid consent (sound mind); bridegroom 21 and bride 18; not within prohibited degrees; not sapindas unless custom permits (any two).
X: C3 D3 3 | Explain the essentials of a valid Muslim marriage. | Proposal (ijab) and acceptance (qubul) in one meeting; competence – puberty and sound mind; free consent; no legal bar; mahr; witnesses under Sunni law.
L: D4 | Compare the essentials of a valid marriage under Hindu law and Muslim law. | Hindu – sacrament and statute (HMA 1955), section 5 conditions, section 7 ceremonies (saptapadi), registration; Muslim – contract, ijab and qubul, competence, consent, mahr; void marriages; Prohibition of Child Marriage Act 2006.
"""), ST(S + '11-st3', 'divorce and maintenance under personal laws', """
T: divorce | the legal dissolution of a valid marriage
T: divorce by mutual consent | divorce granted when both spouses jointly apply, having lived separately for at least one year (section 13B of the Hindu Marriage Act)
T: maintenance | the financial support that a person is legally bound to give to a wife, children or parents
T: permanent alimony | maintenance ordered by the court at the time of or after a decree of divorce (section 25 of the Hindu Marriage Act)
T: talaq-e-biddat | instant triple talaq, pronounced at one time, which was set aside by the Supreme Court in 2017
T: khula | divorce at the instance of a Muslim wife, usually by giving up her mahr
T: iddat | the waiting period a Muslim woman observes after divorce or the husband's death before she can remarry
Q: Divorce by mutual consent under the Hindu Marriage Act is provided in section: | 13B | 5 | 7 | 24
Q: Instant triple talaq was set aside in: | Shayara Bano v Union of India (2017) | Shah Bano (1985) | Sarla Mudgal (1995) | Puttaswamy (2017)
Q: Triple talaq was made a punishable offence by the: | Muslim Women (Protection of Rights on Marriage) Act, 2019 | Dissolution of Muslim Marriages Act, 1939 | Special Marriage Act, 1954 | Family Courts Act, 1984
Q: A Muslim wife can seek divorce through a court on statutory grounds under the: | Dissolution of Muslim Marriages Act, 1939 | Hindu Marriage Act, 1955 | Indian Divorce Act, 1869 | Guardians and Wards Act, 1890
Q: In Shah Bano (1985) the Supreme Court held that a divorced Muslim woman could claim maintenance under: | section 125 of the CrPC | Article 44 | section 13 of the Hindu Marriage Act | the Shariat Act, 1937
Q: Maintenance during the pendency of proceedings under the Hindu Marriage Act is provided in section: | 24 | 25 | 13 | 5
Q: Divorce by mutual agreement under Muslim law is called: | mubarat | khula | mahr | iddat
Y: 1985 | the Shah Bano judgment on maintenance of divorced Muslim women
Y: 1986 | the Muslim Women (Protection of Rights on Divorce) Act
Y: 2017 | Shayara Bano v Union of India sets aside instant triple talaq
Y: 2019 | the Act making instant triple talaq a punishable offence
S+: Section 13 of the Hindu Marriage Act lists grounds for divorce such as adultery, cruelty and desertion for at least two years
S+: For divorce by mutual consent the spouses must have lived separately for at least one year, and there is normally a six-month waiting period
S+: Maintenance under section 125 of the CrPC (now the Bharatiya Nagarik Suraksha Sanhita) is available to wives, children and parents of any religion
S+: The Dissolution of Muslim Marriages Act, 1939 lets a Muslim wife obtain divorce on grounds such as the husband's failure to maintain her
S+: Under the 2019 Act, pronouncing instant triple talaq is void and punishable with imprisonment of up to three years
S-: Instant triple talaq is a valid way of divorce in India today | It was set aside in Shayara Bano (2017) and made a punishable offence in 2019
S-: Maintenance under section 125 CrPC is available only to Hindu wives | It is a secular remedy available to persons of all religions
S-: Under the Hindu Marriage Act divorce is possible only by mutual consent | Section 13 also gives grounds such as cruelty, adultery and desertion
C: Maintenance under section 125 CrPC is described as a secular remedy | it applies to all wives, children and parents irrespective of religion and aims to prevent destitution
C: The Hindu Marriage Act provides a waiting period for divorce by mutual consent | it gives the spouses time to reconsider and possibly reconcile
C: Instant triple talaq was set aside by the Supreme Court | it allowed a husband to end a marriage at once, arbitrarily and without any attempt at reconciliation
X: C2 D2 2 | State any two grounds of divorce under section 13 of the Hindu Marriage Act. | Adultery; cruelty; desertion for at least two years; conversion to another religion; unsound mind; venereal disease; renunciation; not heard of for seven years (any two).
X: C3 D3 3 | Explain the significance of the Shah Bano (1985) and Shayara Bano (2017) cases. | Shah Bano – divorced Muslim woman entitled to maintenance under section 125 CrPC, followed by the 1986 Act; Shayara Bano – instant triple talaq set aside, followed by the 2019 Act making it an offence; gender justice.
L: D4 | Discuss the law relating to divorce and maintenance under Hindu and Muslim personal laws. | Hindu – section 13 grounds, section 13B mutual consent, sections 24 and 25 maintenance; Muslim – talaq, khula, mubarat, 1939 Act, mahr, iddat, Shah Bano 1985, 1986 Act, Shayara Bano 2017, 2019 Act; section 125 CrPC.
"""), ST(S + '11-st4', 'family courts and alternative dispute mechanisms', """
T: family court | a court set up under the Family Courts Act, 1984 to deal with matrimonial and family disputes
T: Lok Adalat | a 'people's court' under the Legal Services Authorities Act, 1987 that settles disputes by compromise
T: alternative dispute resolution | methods such as mediation, conciliation, arbitration and Lok Adalats for settling disputes outside the regular court process
T: mediation | a process in which a neutral person helps the parties reach their own settlement
T: NALSA | the National Legal Aid Services Authority, set up under the Legal Services Authorities Act, 1987
Q: Family courts are set up under the: | Family Courts Act, 1984 | Hindu Marriage Act, 1955 | Legal Services Authorities Act, 1987 | Special Marriage Act, 1954
Q: A family court must be set up for every city or town with a population exceeding: | one million | one lakh | five lakh | fifty lakh
Q: Lok Adalats are given statutory status by the: | Legal Services Authorities Act, 1987 | Family Courts Act, 1984 | Arbitration and Conciliation Act, 1996 | Code of Civil Procedure, 1908
Q: An award of a Lok Adalat is: | deemed to be a decree of a civil court, and no appeal lies against it | only advisory | appealable to the Supreme Court as of right | binding only on the government
Q: Equal justice and free legal aid are provided in: | Article 39A | Article 44 | Article 21A | Article 50
Q: An appeal from a judgment of a family court lies to the: | High Court | Supreme Court directly | Lok Adalat | District Collector
S+: Family courts try to bring about reconciliation and settlement between the parties
S+: Under the Family Courts Act, a party is not entitled as of right to be represented by a lawyer
S+: Family courts deal with matters such as divorce, maintenance, custody of children and matrimonial property
S+: In a Lok Adalat no court fee is charged, and fee already paid in court is refunded if the case is settled
S+: Article 39A was added by the 42nd Amendment in 1976
S-: Family courts follow the same strict procedure as ordinary civil courts | Family courts follow a simpler procedure and aim at settlement
S-: An appeal lies against the award of a Lok Adalat | The award is final and no appeal lies against it
S-: Lok Adalats decide cases by imposing punishment | Lok Adalats settle disputes by compromise between the parties
C: Family courts give importance to reconciliation | family disputes involve relationships and children, so a settlement is often better than a contested decree
C: Lok Adalats help reduce the burden on courts | they settle many pending and pre-litigation cases quickly by compromise and without court fees
C: Lawyers are not allowed as of right in family courts | the law wants an informal, less adversarial process in which the parties speak directly
X: C2 D2 2 | State two features of a Lok Adalat. | Settlement by compromise; no court fee; award deemed a civil court decree; award final, no appeal; under the Legal Services Authorities Act 1987 (any two).
X: C3 D3 3 | Explain three features of family courts under the Family Courts Act, 1984. | Set up for cities with population over one million; duty to attempt settlement; no lawyer as of right; simpler procedure; appeal to the High Court; deal with divorce, maintenance and custody (any three).
L: D4 | Describe the role of family courts and alternative dispute resolution mechanisms in the family justice system. | Family Courts Act 1984 – purpose, jurisdiction, settlement, procedure, appeal; Lok Adalats – 1987 Act, NALSA, award as decree; mediation and counselling; Article 39A; benefits – speed, low cost, preserving relationships.
""")]

CH12 = [ST(S + '12-st1', 'the child and child rights', """
T: child | under the UN Convention on the Rights of the Child, every human being below the age of 18 years
T: UNCRC | the United Nations Convention on the Rights of the Child, adopted by the UN General Assembly on 20 November 1989
T: best interests of the child | the principle that in all actions concerning children their best interests shall be a primary consideration
T: right to participation | the right of a child to express views freely in matters affecting the child, given due weight according to age and maturity
T: NCPCR | the National Commission for Protection of Child Rights, set up under the Commissions for Protection of Child Rights Act, 2005
Q: The UN Convention on the Rights of the Child was adopted in: | 1989 | 1959 | 1992 | 2000
Q: India became a party to the UNCRC in: | 1992 | 1989 | 1979 | 2005
Q: Under the UNCRC a child is a person below the age of: | 18 years | 14 years | 16 years | 21 years
Q: Which of these is one of the four guiding principles of the UNCRC? | Best interests of the child | Universal adult franchise | Separation of powers | Rule of law
Q: The National Commission for Protection of Child Rights was set up under an Act of: | 2005 | 1986 | 2009 | 2012
Y: 1989 | adoption of the UN Convention on the Rights of the Child
Y: 1992 | India becomes a party to the UNCRC
Y: 2005 | the Commissions for Protection of Child Rights Act
S+: The four guiding principles of the UNCRC are non-discrimination, best interests of the child, the right to life, survival and development, and respect for the views of the child
S+: Child rights are often grouped as rights to survival, development, protection and participation
S+: 20 November, the day the UNCRC was adopted, is observed as World Children's Day
S+: Countries that are party to the UNCRC report to the UN Committee on the Rights of the Child
S+: The NCPCR monitors whether laws and policies protect child rights in India
S-: The UNCRC defines a child as a person below 14 years | The UNCRC defines a child as a person below 18 years
S-: Children have no right to express their views | The UNCRC gives children the right to express their views in matters affecting them
S-: India has not accepted the UNCRC | India became a party to the UNCRC in 1992
C: Children need special legal protection | they are physically and mentally immature and depend on adults, which makes them vulnerable to abuse and exploitation
C: The best interests of the child guide courts in custody cases | the UNCRC and Indian law make the child's welfare the primary consideration in decisions about children
C: India set up the NCPCR | an independent body was needed to monitor and protect child rights under the laws and the UNCRC
X: C2 D2 2 | Name any two guiding principles of the UNCRC. | Non-discrimination; best interests of the child; right to life, survival and development; respect for the views of the child (any two).
X: C3 D3 3 | Explain the four categories of child rights with an example of each. | Survival – life, health, nutrition; development – education, play; protection – from abuse, exploitation, child labour; participation – expressing views, information.
L: D4 | Explain the concept of the child and the main features of the UN Convention on the Rights of the Child. How has India responded to it? | Child below 18; adoption 1989, India 1992; four principles; four categories of rights; reporting to the UN Committee; Indian response – Article 21A, RTE 2009, POCSO 2012, JJ Act 2015, NCPCR 2005.
"""), ST(S + '12-st2', 'constitutional provisions and laws for children', """
T: right to education | the Fundamental Right of children aged 6 to 14 to free and compulsory education (Article 21A)
T: RTE Act | the Right of Children to Free and Compulsory Education Act, 2009, which came into force on 1 April 2010
T: child labour | work that deprives children of their childhood and education and harms their development; employment of children below 14 is banned
T: adolescent | under child labour law, a person between 14 and 18 years of age
T: POCSO Act | the Protection of Children from Sexual Offences Act, 2012
T: special court | a court designated under the POCSO Act for speedy and child-friendly trial of offences against children
Q: Free and compulsory education for children aged 6 to 14 is a Fundamental Right under: | Article 21A | Article 45 | Article 24 | Article 51A
Q: Article 21A was inserted by the: | 86th Amendment (2002) | 42nd Amendment (1976) | 44th Amendment (1978) | 73rd Amendment (1992)
Q: Employment of children below 14 in factories, mines or hazardous work is prohibited by: | Article 24 | Article 23 | Article 21A | Article 15(3)
Q: The RTE Act requires private unaided schools to reserve for disadvantaged children: | 25% of seats in the entry class | 10% of seats | 50% of seats | 15% of seats
Q: The POCSO Act was enacted in: | 2012 | 2005 | 2009 | 2015
Q: Under the Child Labour Act as amended in 2016, adolescents aged 14 to 18 may NOT be employed in: | hazardous occupations and processes | any work at all | family enterprises after school | school activities
Q: The duty of parents to provide opportunities for education to children aged 6 to 14 is a Fundamental Duty under: | Article 51A(k) | Article 51A(a) | Article 45 | Article 39A
M:childlaw: Article 21A | free and compulsory education for children aged 6-14
M:childlaw: Article 24 | no child below 14 in factories, mines or hazardous work
M:childlaw: Article 45 | early childhood care and education until age six
M:childlaw: Article 15(3) | special provisions for women and children
M:childlaw: Article 51A(k) | duty of parents to provide education
M:childlaw: Article 23 | prohibition of trafficking and forced labour
Y: 1986 | the Child Labour (Prohibition and Regulation) Act
Y: 2002 | the 86th Amendment inserts Article 21A
Y: 2010 | the Right to Education Act comes into force
Y: 2012 | the Protection of Children from Sexual Offences Act
S+: The RTE Act prohibits capitation fees and screening procedures for admission
S+: The 2016 amendment renamed the law the Child and Adolescent Labour (Prohibition and Regulation) Act
S+: The POCSO Act is gender-neutral and protects every person below 18 years
S+: The POCSO Act requires child-friendly procedures, such as recording the child's statement at a place where the child is comfortable
S+: The POCSO Act was amended in 2019 to increase punishments, including the death penalty for aggravated penetrative sexual assault
S+: The Prohibition of Child Marriage Act, 2006 fixes the marriageable age at 18 for females and 21 for males
S-: The POCSO Act protects only girls | The POCSO Act is gender-neutral and protects all children below 18
S-: Article 21A guarantees free education up to class 12 | Article 21A covers children from 6 to 14 years
S-: The RTE Act came into force in 2002 | It came into force on 1 April 2010; the 86th Amendment was in 2002
C: The POCSO Act provides special courts | trials involving child victims need to be quick and child-friendly to avoid further trauma
C: The RTE Act reserves 25% of seats in private unaided schools for disadvantaged children | it aims to make elementary education inclusive and reduce inequality
C: Child labour is prohibited | work deprives children of education and harms their physical and mental development
X: C2 D2 2 | State any two constitutional provisions for the protection of children. | Article 21A; Article 24; Article 15(3); Article 23; Article 39(e)-(f); Article 45; Article 51A(k) (any two with content).
X: C3 D3 3 | State three main features of the RTE Act, 2009. | Free and compulsory education 6-14; 25% seats in private unaided schools for disadvantaged children; no capitation fee or screening; norms for pupil-teacher ratio and infrastructure; in force from 1 April 2010 (any three).
X: C4 D4 3 | How does the POCSO Act, 2012 make the justice system child-friendly? Evaluate its importance. | Gender-neutral, all below 18; special courts; statement at child's place, by woman officer where possible; in-camera trial; identity protected; mandatory reporting; 2019 amendment; importance – protection and deterrence.
L: D5 | Discuss the constitutional provisions and laws relating to education, child labour and sexual offences against children in India. | Articles 15(3), 21A, 23, 24, 39(e)-(f), 45, 51A(k); RTE Act 2009; Child and Adolescent Labour Act (1986, 2016); POCSO Act 2012 and 2019 amendment; Prohibition of Child Marriage Act 2006; NCPCR.
"""), ST(S + '12-st3', 'the Juvenile Justice Act, 2015', """
T: child in conflict with law | a child who is alleged or found to have committed an offence and is below 18 years on the date of the offence
T: child in need of care and protection | a child who is, for example, homeless, abandoned, orphaned, abused or at risk, and needs care
T: Juvenile Justice Board | the body that deals with children in conflict with law, consisting of a magistrate and two social workers, at least one a woman
T: Child Welfare Committee | the body that deals with children in need of care and protection
T: heinous offence | an offence for which the minimum punishment under any law is imprisonment for seven years or more
T: preliminary assessment | the Board's assessment of a 16-18-year-old accused of a heinous offence about his mental and physical capacity and understanding of the consequences
T: CARA | the Central Adoption Resource Authority, the statutory body that regulates adoption in India
Q: The Juvenile Justice (Care and Protection of Children) Act was enacted in: | 2015 | 2000 | 2012 | 1986
Q: Cases of children in conflict with law are dealt with by the: | Juvenile Justice Board | Child Welfare Committee | Family Court | Lok Adalat
Q: Cases of children in need of care and protection are dealt with by the: | Child Welfare Committee | Juvenile Justice Board | Sessions Court | Panchayat
Q: Under the JJ Act, 2015 a heinous offence is one with a minimum punishment of imprisonment of: | seven years or more | three years or more | one year or more | ten years or more
Q: A child of which age group accused of a heinous offence may be tried as an adult after preliminary assessment? | 16 to 18 years | 12 to 14 years | 14 to 16 years | below 12 years
Q: Adoption in India is regulated by the: | Central Adoption Resource Authority | National Legal Aid Services Authority | NCPCR | Law Commission
S+: The JJ Act, 2015 replaced the Juvenile Justice Act of 2000
S+: The Act deals with two groups of children: those in conflict with law and those in need of care and protection
S+: A Juvenile Justice Board has a Metropolitan or Judicial Magistrate and two social workers, at least one of whom is a woman
S+: No child in conflict with law can be sentenced to death or to life imprisonment without the possibility of release
S+: Offences are classified as petty, serious and heinous under the Act
S+: The 2021 amendment empowered District Magistrates to issue adoption orders
S-: Every child accused of any offence is tried as an adult | Only a child of 16-18 accused of a heinous offence may be tried as an adult, after preliminary assessment
S-: A Child Welfare Committee tries children accused of crimes | Children in conflict with law go before the Juvenile Justice Board
S-: A child in conflict with law can be sentenced to death | The JJ Act prohibits death sentence and life imprisonment without the possibility of release for children
C: The JJ Act allows some 16-18-year-olds to be tried as adults | Parliament responded to concern about serious crimes by older adolescents, but kept it subject to the Board's preliminary assessment
C: The Juvenile Justice Board includes social workers | the aim of the juvenile system is reform and rehabilitation rather than only punishment
C: The JJ Act has a separate body for children in need of care and protection | such children have not committed any offence and need care, shelter and rehabilitation, not a trial
X: C2 D2 2 | Distinguish between a child in conflict with law and a child in need of care and protection. | Conflict with law – alleged or found to have committed an offence, before the JJB; care and protection – abandoned, orphaned, abused or at risk, before the CWC.
X: C3 D3 3 | Explain the composition and role of the Juvenile Justice Board. | Metropolitan or Judicial Magistrate (first class) plus two social workers, at least one a woman; inquiry into children in conflict with law; preliminary assessment for 16-18 heinous cases; child-friendly procedure; reformative orders.
L: D4 | Explain the main provisions of the Juvenile Justice (Care and Protection of Children) Act, 2015. | Two categories of children; JJB and CWC; petty, serious and heinous offences; 16-18 heinous – preliminary assessment, Children's Court; no death or life without release; homes and rehabilitation; adoption and CARA; 2021 amendment.
""")]

CHAPTERS = [(CH07, {'chapter_topic': 'the sources of law'}), (CH08, {'chapter_topic': 'law reform'}),
            (CH09, {'chapter_topic': 'cyber laws'}), (CH10, {'chapter_topic': 'the judiciary'}),
            (CH11, {'chapter_topic': 'the family justice system'}), (CH12, {'chapter_topic': 'child rights'})]
