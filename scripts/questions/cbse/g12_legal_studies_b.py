"""CBSE class 12 Legal Studies (chapters 8-13): fact tables for g12_hum_engine."""
from g12_hum_engine import ST

S = 'cbse-g12-legal-studies-ch'

CH08 = [ST(S + '08-st1', 'legal persons: natural and artificial', """
T: legal person | any entity that the law recognises as capable of having rights and duties
T: natural person | a human being who has rights and duties in law
T: artificial person | an entity such as a company, corporation or university that is created by law and recognised as a person
T: juristic person | a legal person other than a human being, such as a company, a trust or a deity recognised by law
T: corporation sole | a corporation consisting of a single office-holder, such as the office of a Postmaster General, that continues beyond the individual
T: corporation aggregate | a corporation made up of a number of members, such as a company
Q: A company registered under the Companies Act is a/an: | artificial person | natural person | partnership firm | unincorporated body
Q: Which of these has been recognised as a juristic person by Indian courts? | A Hindu idol | A household pet | A cricket team without registration | A crowd at a fair
Q: An artificial person comes into existence by: | operation of law | birth | marriage | a court decree in every case
Q: A corporation consisting of a single office-holder is called a: | corporation sole | corporation aggregate | partnership | trust
S+: A legal person can own property, enter contracts, sue and be sued in its own name
S+: An artificial person acts through human agents such as directors and officers
S+: Universities, municipal corporations and companies are examples of artificial persons
S+: Indian courts have recognised Hindu idols as juristic persons capable of owning property
S+: An artificial person continues to exist even when its members change
S-: Only human beings can be legal persons | The law also recognises artificial persons such as companies and corporations
S-: An artificial person can act without any human agent | It acts through human agents such as directors
S-: An artificial person ends when one of its members dies | It has perpetual succession
C: A company can sue and be sued in its own name | the law treats it as an artificial person separate from its members
C: A company acts through its directors | an artificial person has no physical existence and cannot act by itself
C: The law recognises artificial persons | it allows groups and institutions to own property and carry on activities as single units
X: C2 D2 2 | Distinguish between a natural person and an artificial person. | Natural person – human being with rights and duties; artificial person – entity created by law such as a company, corporation or university.
X: C3 D3 2 | Why does the law create artificial persons? | To let groups and institutions own property, contract, sue and be sued as one unit and continue beyond the lives of their members.
X: C3 D3 3 | Explain the characteristics of a legal person. | Recognised by law; capacity to own property; enter contracts; sue and be sued; rights and duties; artificial persons act through agents.
X: C3 D4 3 | Distinguish between a corporation sole and a corporation aggregate. | Corporation sole – single office-holder continuing beyond the individual (e.g. a public office); corporation aggregate – group of members, e.g. a company.
X: C4 D4 3 | 'Personality in law is not limited to human beings.' Explain. | Law confers personality on companies, corporations, universities, trusts and idols; they hold rights and duties; act through agents; perpetual existence.
L: D4 | Explain the concept of legal personality with reference to natural and artificial persons. | Meaning of legal person; natural persons; artificial persons – companies, corporations, universities, idols; corporation sole and aggregate; features.
"""), ST(S + '08-st2', 'sole proprietorship, partnership and LLP', """
T: sole proprietorship | a business owned and controlled by one person who bears unlimited liability
T: partnership | the relation between persons who have agreed to share the profits of a business carried on by all or any of them acting for all (Section 4, Indian Partnership Act 1932)
T: mutual agency | the feature of a partnership that each partner is both an agent of the firm and of the other partners
T: unlimited liability | liability of an owner extending to personal assets for the debts of the business
T: limited liability partnership | a body corporate under the LLP Act 2008 that combines the flexibility of a partnership with the limited liability of a company
T: designated partner | a partner of an LLP responsible for compliance with the LLP Act
Q: Partnership in India is governed by the: | Indian Partnership Act 1932 | Companies Act 2013 | LLP Act 2008 | Indian Contract Act Section 10
Q: The LLP Act was passed in: | 2008 | 1932 | 2013 | 1956
Q: The liability of partners in a general partnership is: | unlimited, joint and several | limited to their capital | nil | limited by guarantee
Q: An LLP must have at least: | two designated partners | one partner only | seven members | fifty partners
Q: Which business form is a separate legal entity? | Limited liability partnership | Sole proprietorship | General partnership | Joint Hindu family business
Q: The basis of a partnership is: | an agreement | status by birth | a statute only | a court order
Y: 1932 | the enactment of the Indian Partnership Act
Y: 2008 | the enactment of the Limited Liability Partnership Act
S+: A sole proprietor has full control and keeps all profits but bears unlimited liability
S+: A sole proprietorship has no separate legal existence from its owner
S+: Registration of a partnership firm is optional, but an unregistered firm cannot sue third parties to enforce contracts
S+: An LLP has perpetual succession and the liability of partners is limited to their agreed contribution
S+: In an LLP one partner is not responsible for the misconduct of another partner
S-: A general partnership is a separate legal entity | A general partnership firm is not a separate legal entity from its partners
S-: Partners in an LLP have unlimited liability | Their liability is limited to their agreed contribution
S-: Registration of a partnership firm is compulsory | It is optional, though non-registration has disadvantages
C: A partner can bind the firm by acts done in the course of business | each partner is an agent of the firm and of the other partners (mutual agency)
C: A sole proprietor's personal property can be used to pay business debts | a sole proprietor has unlimited liability
C: LLPs are preferred by professionals | they combine partnership flexibility with limited liability
X: C2 D2 2 | Distinguish between a partnership and an LLP. | Partnership – not a separate entity, unlimited joint liability, Partnership Act 1932; LLP – body corporate, limited liability, perpetual succession, LLP Act 2008.
X: C3 D3 2 | What is meant by mutual agency in a partnership? | Each partner is an agent of the firm and of the other partners; acts of one partner in the course of business bind all.
X: C3 D3 3 | State the essentials of a partnership. | Agreement between two or more persons; business; sharing of profits; business carried on by all or any of them acting for all (mutual agency).
X: C3 D4 3 | Explain the features of a sole proprietorship. | Single owner; full control; all profits to owner; unlimited liability; no separate legal entity; easy formation and closure.
X: C4 D4 3 | Explain the main features of a limited liability partnership. | Body corporate, separate entity; perpetual succession; limited liability to contribution; at least two designated partners; flexible internal management by LLP agreement.
L: D4 | Compare sole proprietorship, partnership and LLP as forms of business organisation. | Ownership, governing law, legal status, liability, continuity, registration, management – features of each.
"""), ST(S + '08-st3', 'companies and lifting the corporate veil', """
T: company | an artificial person registered under the Companies Act, having a separate legal entity, perpetual succession and limited liability of members
T: separate legal entity | the principle that a company is distinct from its members, as laid down in Salomon v Salomon and Co.
T: perpetual succession | the continued existence of a company irrespective of changes in its membership
T: lifting the corporate veil | the disregarding of a company's separate personality by courts to identify the persons behind it in cases such as fraud
T: one person company | a company with only one person as its member, introduced by the Companies Act 2013
T: memorandum of association | the charter document of a company that defines its name, objects, registered office and the liability of members
Q: The principle of separate legal entity of a company was laid down in: | Salomon v Salomon and Co. | Rylands v Fletcher | Carlill v Carbolic Smoke Ball Co. | Ashby v White
Q: The minimum number of members in a private company is: | 2 | 7 | 1 | 50
Q: The minimum number of members in a public company is: | 7 | 2 | 1 | 200
Q: The maximum number of members in a private company is generally: | 200 | 50 | 7 | unlimited
Q: The concept of a one person company was introduced by the: | Companies Act 2013 | Companies Act 1956 | Partnership Act 1932 | LLP Act 2008
Q: Courts may lift the corporate veil when the company is used for: | fraud or evasion of tax | lawful business | paying dividends | holding general meetings
Y: 2013 | the enactment of the present Companies Act
S+: A company has a separate legal entity, perpetual succession, limited liability and transferable shares
S+: Shares of a public company are freely transferable, while a private company restricts transfer
S+: Courts lift the corporate veil in cases of fraud, tax evasion, enemy character and avoidance of legal obligations
S+: The Companies Act 2013 permits a company to be formed for any lawful purpose by registration
S+: A company's memorandum and articles of association govern its objects and internal management
S-: A company ends when its main shareholder dies | A company has perpetual succession
S-: A private company must have at least seven members | A private company needs at least two members; a public company needs seven
S-: Shareholders are personally liable for all company debts | Their liability is limited to the unpaid amount on their shares
C: A company can own property in its own name | it is a separate legal entity distinct from its members
C: Courts sometimes lift the corporate veil | the separate personality of a company may be misused as a cloak for fraud
C: A company continues even if all members change | it has perpetual succession
X: C2 D2 2 | What is meant by lifting the corporate veil? | Disregarding the separate personality of a company to look at the persons behind it, in cases of fraud, tax evasion, enemy character or evasion of law.
X: C3 D3 2 | What did Salomon v Salomon and Co. decide? | A company is a separate legal person from its members, even if one person holds almost all shares; members are not personally liable for its debts.
X: C3 D3 3 | Explain any three features of a company. | Artificial person; separate legal entity; perpetual succession; limited liability; transferable shares; common seal (optional); can sue and be sued.
X: C3 D4 3 | Distinguish between a private company and a public company. | Private – minimum 2 members, maximum 200, restricts transfer of shares, cannot invite public; public – minimum 7 members, no maximum, freely transferable shares, can invite public.
X: C4 D4 3 | 'The corporate veil is not an iron curtain.' Explain. | Separate entity is the rule (Salomon); courts lift the veil for fraud, tax evasion, enemy character, sham companies, avoiding welfare laws; also under statutory provisions.
L: D4 | Explain the features of a company under the Companies Act 2013. | Artificial person; separate entity (Salomon); perpetual succession; limited liability; transferable shares; kinds – private, public, OPC; memorandum and articles.
L: D5 | Explain the doctrine of lifting the corporate veil with the circumstances in which courts apply it. | Separate entity principle; meaning of lifting; fraud; tax evasion; enemy character; sham or facade companies; protection of public interest; statutory instances.
"""),
]

CH09 = [ST(S + '09-st1', 'criminal law: meaning, elements and the new criminal laws', """
T: crime | an act or omission forbidden by law and punishable by the State
T: actus reus | the guilty act or physical element of a crime
T: mens rea | the guilty mind or mental element of a crime, such as intention or knowledge
T: Bharatiya Nyaya Sanhita 2023 | the substantive criminal law of India that replaced the Indian Penal Code 1860
T: Bharatiya Nagarik Suraksha Sanhita 2023 | the law of criminal procedure that replaced the Code of Criminal Procedure 1973
T: Bharatiya Sakshya Adhiniyam 2023 | the law of evidence that replaced the Indian Evidence Act 1872
Q: The Bharatiya Nyaya Sanhita 2023 replaced the: | Indian Penal Code 1860 | Code of Criminal Procedure 1973 | Indian Evidence Act 1872 | Indian Contract Act 1872
Q: The new criminal laws came into force on: | 1 July 2024 | 26 January 2023 | 15 August 2023 | 1 April 2025
Q: The maxim 'actus non facit reum nisi mens sit rea' means: | an act does not make a person guilty unless the mind is also guilty | the thing speaks for itself | let the master answer | no consideration, no contract
Q: The guilty act in a crime is called: | actus reus | mens rea | res judicata | locus standi
Q: Which stage of a crime is generally NOT punishable? | Intention | Attempt | Commission | Preparation to wage war against the Government of India
Q: The Bharatiya Sakshya Adhiniyam 2023 deals with: | evidence | substantive offences | criminal procedure | contracts
M:law: Bharatiya Nyaya Sanhita | replaced the Indian Penal Code
M:law: Bharatiya Nagarik Suraksha Sanhita | replaced the Code of Criminal Procedure
M:law: Bharatiya Sakshya Adhiniyam | replaced the Indian Evidence Act
S+: The elements of a crime are a human being, mens rea, actus reus and injury
S+: The stages of a crime are intention, preparation, attempt and commission
S+: Mere intention is not punishable, and preparation is punishable only for a few grave offences
S+: The Bharatiya Nyaya Sanhita introduced community service as a form of punishment
S+: Some offences of strict liability can be committed without mens rea
S-: Mere intention to commit a crime is punishable | Mere intention is not punishable; the law punishes acts
S-: The Bharatiya Nagarik Suraksha Sanhita replaced the Indian Evidence Act | It replaced the Code of Criminal Procedure; the Bharatiya Sakshya Adhiniyam replaced the Evidence Act
S-: A crime is a private wrong against an individual only | A crime is a public wrong against society, prosecuted by the State
C: Crimes are prosecuted by the State | a crime is regarded as a wrong against society as a whole
C: Mere intention is not punished | an evil thought without an act causes no harm and is hard to prove
C: The new criminal laws were enacted | the colonial-era codes needed to be replaced with laws suited to present needs, including technology and victim-centred justice
X: C2 D2 2 | Distinguish between actus reus and mens rea. | Actus reus – the guilty act or omission; mens rea – the guilty mind, such as intention or knowledge; both generally needed for a crime.
X: C3 D3 2 | Why is mere intention not punishable? | Thought alone causes no harm; it is impossible to prove; law punishes acts; the person may change his mind.
X: C3 D3 3 | Explain the elements of a crime. | Human being under a legal duty; mens rea – guilty mind; actus reus – guilty act; injury to another person or society.
X: C3 D4 3 | Explain the stages of a crime. | Intention – not punishable; preparation – punishable only for grave offences; attempt – punishable; commission – punishable.
X: C4 D4 3 | Explain the new criminal laws of 2023. | Bharatiya Nyaya Sanhita replaced IPC; Bharatiya Nagarik Suraksha Sanhita replaced CrPC; Bharatiya Sakshya Adhiniyam replaced Evidence Act; in force from 1 July 2024; community service, electronic records.
L: D4 | Explain the meaning of crime, its elements and stages. | Crime as public wrong; elements – human being, mens rea, actus reus, injury; maxim; stages – intention, preparation, attempt, commission.
L: D5 | Explain the reforms introduced by the new criminal laws of 2023. | BNS, BNSS, BSA replacing IPC, CrPC, Evidence Act; from 1 July 2024; community service; Zero FIR and e-FIR; electronic evidence; victim-centred provisions.
"""), ST(S + '09-st2', 'general exceptions and kinds of punishment', """
T: general exceptions | circumstances recognised by criminal law in which an act that would otherwise be an offence is not an offence
T: mistake of fact | the exception for an act done by a person who, by a mistake of fact and not of law, in good faith believes himself bound or justified by law to do it
T: right of private defence | the right to use reasonable force to protect one's own or another's body or property
T: unsoundness of mind | the exception for a person who, at the time of the act, because of unsoundness of mind, is incapable of knowing the nature of the act or that it is wrong
T: community service | a punishment introduced by the Bharatiya Nyaya Sanhita in which the offender does work that benefits the community
Q: An act done by a child under seven years of age is: | not an offence | always an offence | a civil wrong only | punishable with fine
Q: Which of these is NOT a general exception? | Ignorance of law | Mistake of fact | Accident | Private defence
Q: Which of these is a punishment under the Bharatiya Nyaya Sanhita? | Community service | Injunction | Specific performance | Quantum meruit
Q: The test of insanity in criminal law is derived from: | the McNaghten Rules | the Brundtland Report | the Hadley v Baxendale rule | the Salomon principle
Q: Imprisonment under criminal law may be: | rigorous or simple | only rigorous | only simple | only for life
S+: The punishments under the BNS include death, imprisonment for life, imprisonment, forfeiture of property, fine and community service
S+: Rigorous imprisonment involves hard labour, while simple imprisonment does not
S+: An act of a child above seven and under twelve is not an offence if the child has not attained sufficient maturity to understand the act
S+: The right of private defence is not available against the lawful acts of public servants acting in good faith
S+: Involuntary intoxication can be a defence, but voluntary intoxication generally is not
S-: Ignorance of law is a valid defence | Ignorance of law is no excuse; mistake of fact in good faith is a defence
S-: Private defence allows any amount of force | The force must be reasonable and proportionate
S-: Voluntary intoxication is always a complete defence | Generally only involuntary intoxication is a defence
C: A child under seven is not punished | the law presumes that such a child cannot form a guilty mind
C: Mistake of fact is a defence but mistake of law is not | everyone is presumed to know the law of the land
C: Community service was introduced as a punishment | it reforms petty offenders without sending them to prison
X: C2 D2 2 | Distinguish between mistake of fact and mistake of law. | Mistake of fact in good faith is a general exception; mistake of law is not, as ignorance of law is no excuse.
X: C3 D3 2 | Why is an act of a person of unsound mind not an offence? | Such a person cannot know the nature of the act or that it is wrong; there is no mens rea; McNaghten Rules.
X: C3 D3 3 | Explain any three general exceptions under criminal law. | Mistake of fact; judicial acts; accident; infancy; insanity; involuntary intoxication; consent; necessity; private defence.
X: C3 D4 3 | Explain the kinds of punishment under the Bharatiya Nyaya Sanhita. | Death; imprisonment for life; imprisonment – rigorous or simple; forfeiture of property; fine; community service.
X: C4 D4 3 | Explain the limits of the right of private defence. | Not against lawful acts of public servants in good faith; not when there is time to seek help of public authorities; force must be reasonable and proportionate.
L: D4 | Explain the general exceptions under criminal law. | Mistake of fact; accident; infancy; insanity; intoxication; consent; necessity; private defence – meaning and limits of each.
"""), ST(S + '09-st3', 'criminal procedure: FIR, arrest, bail, investigation and trial', """
T: First Information Report | the information about the commission of a cognizable offence given to the officer in charge of a police station, which sets the criminal law in motion
T: cognizable offence | an offence in which the police can arrest without a warrant and start investigation without the magistrate's order
T: non-cognizable offence | an offence in which the police cannot arrest without a warrant or investigate without the magistrate's permission
T: bail | the release of an accused person from custody on security, with an undertaking to appear before the court
T: bailable offence | an offence in which the accused has a right to be released on bail
T: Zero FIR | an FIR that can be lodged at any police station irrespective of where the offence took place
T: charge sheet | the final report filed by the police after investigation, stating the offences and the evidence against the accused
Q: An arrested person must be produced before a magistrate within: | 24 hours, excluding journey time | 48 hours | 72 hours | one week
Q: Murder is an example of a: | cognizable and non-bailable offence | non-cognizable and bailable offence | civil wrong | compoundable offence in all cases
Q: An FIR is lodged for a: | cognizable offence | non-cognizable offence only | civil dispute | breach of contract
Q: In a bailable offence, bail is: | a matter of right | at the discretion of the court only | never granted | granted only by the Supreme Court
Q: An FIR that can be lodged at any police station regardless of jurisdiction is a: | Zero FIR | charge sheet | complaint case | police diary
Q: After investigation, the police file a: | charge sheet (police report) | writ petition | plaint | arbitral award
S+: The officer in charge of a police station must record information about a cognizable offence
S+: The informant is entitled to a free copy of the FIR
S+: The new criminal procedure law allows electronic FIRs (e-FIR) and Zero FIR
S+: Anticipatory bail can be sought by a person who apprehends arrest for a non-bailable offence
S+: Criminal trials include sessions trials, warrant trials, summons trials and summary trials
S-: The police can investigate a non-cognizable offence without the magistrate's permission | They need the magistrate's permission
S-: An FIR can be lodged only at the police station of the place of the offence | A Zero FIR can be lodged at any police station
S-: Bail is never a right | Bail is a matter of right in bailable offences
C: An arrested person must be produced before a magistrate within 24 hours | Article 22 protects against unlawful and prolonged detention by the police
C: The FIR is an important document | it sets the criminal law in motion and records the earliest version of the events
C: Zero FIR helps victims | the victim need not go from one police station to another and the case can be transferred later
X: C2 D2 2 | Distinguish between cognizable and non-cognizable offences. | Cognizable – police can arrest without warrant and investigate without magistrate's order (murder); non-cognizable – need warrant and permission (simple hurt, defamation).
X: C3 D3 2 | What is a Zero FIR? | An FIR lodged at any police station irrespective of jurisdiction; later transferred to the police station having jurisdiction; avoids delay for victims.
X: C3 D3 3 | Explain the importance of an FIR. | Sets criminal law in motion; first version of events; basis of investigation; free copy to informant; corroborative evidence at trial.
X: C3 D4 3 | Distinguish between bailable and non-bailable offences. | Bailable – bail as a matter of right, less serious offences; non-bailable – bail at the discretion of the court, serious offences such as murder.
X: C4 D4 3 | Explain the steps in a criminal case from FIR to trial. | FIR; investigation – spot visit, statements, arrest, evidence; charge sheet; cognizance by magistrate; framing of charges; trial – evidence, arguments; judgment.
L: D4 | Explain the criminal procedure from the registration of an FIR to the end of trial. | FIR and Zero FIR; investigation; arrest and production within 24 hours; bail; charge sheet; charges; trial; judgment and sentence; appeal.
"""), ST(S + '09-st4', 'rights of the accused and of victims', """
T: presumption of innocence | the principle that an accused person is presumed innocent until proved guilty beyond reasonable doubt
T: double jeopardy | the protection under Article 20(2) that no person shall be prosecuted and punished for the same offence more than once
T: right against self-incrimination | the protection under Article 20(3) that no accused person shall be compelled to be a witness against himself
T: ex post facto law | a law that makes an act a crime with retrospective effect, which Article 20(1) forbids for criminal punishment
T: victim compensation scheme | a scheme under which the State provides funds to compensate victims of crime who suffer loss or injury
Q: Protection against double jeopardy is provided by: | Article 20(2) | Article 21 | Article 22(1) | Article 39A
Q: The right against self-incrimination is provided by: | Article 20(3) | Article 20(1) | Article 22(2) | Article 32
Q: Guidelines on arrest and detention were laid down in: | D.K. Basu v State of West Bengal | Salomon v Salomon | Ashby v White | Carlill v Carbolic Smoke Ball Co.
Q: The right of an arrested person to consult a lawyer of his choice is in: | Article 22(1) | Article 20(2) | Article 300A | Article 51A
Q: An accused person is presumed to be: | innocent until proved guilty | guilty until proved innocent | guilty if arrested | innocent only if released on bail
S+: An arrested person has the right to be informed of the grounds of arrest
S+: An arrested person has the right to consult and be defended by a legal practitioner of his choice
S+: An accused who cannot afford a lawyer is entitled to free legal aid
S+: The right to a speedy trial has been read into Article 21
S+: Victims have a right to compensation, information about the case and to be heard in certain matters
S-: An accused can be compelled to be a witness against himself | Article 20(3) protects against self-incrimination
S-: A person can be punished twice for the same offence | Article 20(2) forbids double jeopardy
S-: Victims have no role or rights in criminal cases | Victims have rights to compensation, information and in some matters to be heard
C: The police must inform an arrested person of the grounds of arrest | the person must be able to seek bail and legal help (Article 22)
C: A conviction requires proof beyond reasonable doubt | an accused person is presumed innocent until proved guilty
C: Victim compensation schemes exist | the State has a duty to help victims recover from the loss and injury caused by crime
X: C2 D2 2 | What is meant by double jeopardy? | Article 20(2) – no person shall be prosecuted and punished for the same offence more than once.
X: C3 D3 2 | Why is an accused presumed innocent? | Burden is on the prosecution; protects against wrongful conviction; guilt must be proved beyond reasonable doubt.
X: C3 D3 3 | State any three rights of an arrested person. | To be informed of grounds of arrest; to consult a lawyer of choice; to be produced before magistrate within 24 hours; to inform a relative; to free legal aid; to bail in bailable offences; medical examination.
X: C3 D4 3 | Explain the protections given by Article 20. | 20(1) – no ex post facto criminal law, no greater penalty; 20(2) – no double jeopardy; 20(3) – no self-incrimination.
X: C4 D4 3 | Explain the rights of victims in the criminal justice system. | Right to compensation under victim compensation schemes; information about progress; to engage a lawyer to assist the prosecution; to be heard in certain matters; protection and support; appeal against acquittal in some cases.
L: D4 | Explain the rights of the accused under the Constitution and criminal law. | Article 20 – ex post facto, double jeopardy, self-incrimination; Article 21 – fair and speedy trial; Article 22 – grounds, lawyer, 24 hours; presumption of innocence; legal aid; D.K. Basu guidelines.
"""),
]

CH10 = [ST(S + '10-st1', 'concept and evolution of human rights; UDHR', """
T: human rights | rights inherent to all human beings by virtue of being human, regardless of nationality, sex, religion or any other status
T: Universal Declaration of Human Rights | the declaration adopted by the UN General Assembly on 10 December 1948 setting out fundamental rights for all people
T: International Bill of Human Rights | the UDHR together with the International Covenant on Civil and Political Rights and the International Covenant on Economic, Social and Cultural Rights
T: first generation rights | civil and political rights such as the right to life, liberty and freedom of speech
T: second generation rights | economic, social and cultural rights such as the right to work, education and health
T: third generation rights | collective or solidarity rights such as the right to development and a healthy environment
Q: The UDHR was adopted on: | 10 December 1948 | 24 October 1945 | 26 January 1950 | 15 August 1947
Q: Human Rights Day is observed on: | 10 December | 24 October | 2 October | 26 November
Q: The two international covenants on human rights were adopted in: | 1966 | 1948 | 1993 | 1976
Q: Civil and political rights are called: | first generation rights | second generation rights | third generation rights | collective rights only
Q: The UDHR contains: | 30 articles | 17 articles | 100 articles | 51 articles
Q: The Magna Carta, an early document limiting royal power, was issued in England in: | 1215 | 1689 | 1789 | 1948
Y: 1948 | the adoption of the Universal Declaration of Human Rights
Y: 1966 | the adoption of the two International Covenants on human rights
Y: 1215 | the issue of the Magna Carta in England
S+: Human rights are universal, inalienable, indivisible and interdependent
S+: The UDHR is not a treaty in itself, but it has great moral and political force
S+: The ICCPR and ICESCR are binding on the States that ratify them
S+: Second generation rights generally require positive action by the State
S+: The right to development and the right to a healthy environment are examples of collective rights
S-: The UDHR was adopted in 1966 | It was adopted in 1948; the two covenants were adopted in 1966
S-: Human rights are granted only to citizens of a country | Human rights belong to all human beings by virtue of being human
S-: Human rights can be freely surrendered or sold | Human rights are inalienable
C: Human rights are called inalienable | they cannot be taken away or given up, as they belong to every person by virtue of being human
C: The UDHR is called the foundation of international human rights law | it set common standards later turned into binding covenants
C: Economic and social rights need positive State action | rights such as education and health require the State to provide resources
X: C2 D2 2 | Distinguish between first and second generation rights. | First – civil and political rights (life, liberty, speech), restrain the State; second – economic, social and cultural rights (work, education, health), need positive State action.
X: C3 D3 2 | What is the International Bill of Human Rights? | The UDHR (1948) together with the ICCPR and ICESCR (1966) and their protocols.
X: C3 D3 3 | Explain the characteristics of human rights. | Universal; inherent; inalienable; indivisible; interdependent; equal and non-discriminatory.
X: C3 D4 3 | Trace the evolution of human rights. | Magna Carta 1215; English Bill of Rights 1689; American and French declarations; UN Charter 1945; UDHR 1948; covenants 1966; later conventions.
X: C4 D4 3 | 'The UDHR is a milestone in the history of human rights.' Explain. | First global statement of rights; adopted 10 December 1948; 30 articles; civil, political, economic, social rights; basis for covenants and national constitutions.
L: D4 | Explain the concept, characteristics and evolution of human rights with reference to the UDHR. | Meaning; characteristics; generations of rights; Magna Carta to UN Charter; UDHR 1948; ICCPR and ICESCR 1966.
"""), ST(S + '10-st2', 'human rights under the Indian Constitution; Article 21', """
T: fundamental rights | the justiciable rights guaranteed in Part III of the Constitution and enforceable in courts
T: directive principles of state policy | the non-justiciable principles in Part IV of the Constitution that the State must apply in making laws
T: right to life and personal liberty | the right under Article 21 that no person shall be deprived of life or personal liberty except according to procedure established by law
T: right to privacy | the right declared a fundamental right under Article 21 in Justice K.S. Puttaswamy v Union of India (2017)
T: right to education | the fundamental right of children aged six to fourteen years to free and compulsory education under Article 21A
Q: The case which held that the procedure under Article 21 must be just, fair and reasonable is: | Maneka Gandhi v Union of India | A.K. Gopalan v State of Madras | Salomon v Salomon | Kesavananda Bharati v State of Kerala
Q: The right to privacy was declared a fundamental right in: | Justice K.S. Puttaswamy v Union of India | Vishaka v State of Rajasthan | Olga Tellis v Bombay Municipal Corporation | D.K. Basu v State of West Bengal
Q: Article 21A was added by the: | 86th Amendment (2002) | 42nd Amendment (1976) | 44th Amendment (1978) | 73rd Amendment (1992)
Q: The right to livelihood was linked to Article 21 in: | Olga Tellis v Bombay Municipal Corporation | Ashby v White | Rylands v Fletcher | Carlill v Carbolic Smoke Ball Co.
Q: Untouchability is abolished by: | Article 17 | Article 14 | Article 23 | Article 21
Q: Fundamental rights are contained in: | Part III of the Constitution | Part IV | Part IVA | Part XV
Y: 1978 | the Supreme Court's decision in Maneka Gandhi v Union of India
Y: 2017 | the Supreme Court's declaration of privacy as a fundamental right in the Puttaswamy case
S+: Fundamental rights are justiciable, while directive principles are not enforceable by courts
S+: The courts have read rights such as livelihood, shelter, health, privacy and a clean environment into Article 21
S+: Article 23 prohibits trafficking in human beings and forced labour
S+: Article 24 prohibits the employment of children below fourteen years in factories, mines and hazardous work
S+: Many rights in the UDHR are reflected in Part III and Part IV of the Indian Constitution
S-: Directive principles are enforceable in courts | They are not justiciable, though fundamental in governance
S-: Article 21 protects only against physical death | Courts have read the right to live with dignity, livelihood, privacy and more into it
S-: The right to education is a directive principle only | Article 21A makes it a fundamental right for children aged six to fourteen
C: Article 21 is called the heart of fundamental rights | courts have expanded it to include many rights needed for a dignified life
C: The Maneka Gandhi case is a landmark | it required that any procedure depriving liberty be just, fair and reasonable
C: Directive principles are not enforceable but still important | they guide the State in making laws for social and economic justice
X: C2 D2 2 | Distinguish between fundamental rights and directive principles. | Fundamental rights – Part III, justiciable, mostly restrain the State; directive principles – Part IV, non-justiciable, guide the State to secure socio-economic welfare.
X: C3 D3 2 | How did Maneka Gandhi v Union of India expand Article 21? | Held that procedure depriving life or liberty must be just, fair and reasonable, not arbitrary; linked Articles 14, 19 and 21.
X: C3 D3 3 | Name any three rights read into Article 21 by the courts. | Right to live with dignity; livelihood (Olga Tellis); privacy (Puttaswamy); speedy trial; free legal aid; clean environment; health; shelter.
X: C3 D4 3 | Explain how the Indian Constitution reflects the UDHR. | Civil and political rights in Part III – equality, freedom, life, against exploitation; socio-economic rights in Part IV – work, education, health; Article 21 expansion.
X: C4 D4 3 | 'Article 21 has become a source of many rights.' Explain. | Maneka Gandhi – fair procedure; Olga Tellis – livelihood; Puttaswamy – privacy; rights to health, environment, speedy trial, legal aid; Article 21A education.
L: D4 | Explain the protection of human rights under the Indian Constitution with reference to Article 21. | Part III and Part IV; Articles 14, 17, 19, 21, 23, 24; Maneka Gandhi; Olga Tellis; Puttaswamy; Article 21A.
"""), ST(S + '10-st3', 'rights of vulnerable groups', """
T: vulnerable groups | sections of society, such as women, children, Scheduled Castes and Tribes and persons with disabilities, who face a greater risk of rights violations
T: Vishaka guidelines | the guidelines laid down by the Supreme Court in 1997 to prevent sexual harassment of women at the workplace
T: Rights of Persons with Disabilities Act 2016 | the law that recognises 21 kinds of disabilities and secures equal rights and opportunities for persons with disabilities
T: SC and ST (Prevention of Atrocities) Act 1989 | the law that punishes atrocities against members of the Scheduled Castes and Scheduled Tribes and provides relief to victims
T: Protection of Women from Domestic Violence Act 2005 | the civil law that provides protection orders, residence and monetary relief to women facing domestic violence
Q: Guidelines against sexual harassment at the workplace were laid down in: | Vishaka v State of Rajasthan | Maneka Gandhi v Union of India | D.K. Basu v State of West Bengal | Hussainara Khatoon v State of Bihar
Q: The Rights of Persons with Disabilities Act was passed in: | 2016 | 1995 | 2005 | 2012
Q: The Sexual Harassment of Women at Workplace Act was passed in: | 2013 | 1997 | 2005 | 1961
Q: Transgender persons were recognised as a 'third gender' in: | NALSA v Union of India (2014) | Vishaka v State of Rajasthan | Olga Tellis v Bombay Municipal Corporation | Puttaswamy v Union of India
Q: The Protection of Children from Sexual Offences Act was enacted in: | 2012 | 2005 | 2016 | 1989
Q: The number of disabilities recognised by the Rights of Persons with Disabilities Act 2016 is: | 21 | 7 | 12 | 30
Y: 1997 | the Supreme Court's Vishaka guidelines on sexual harassment at the workplace
Y: 2013 | the enactment of the Sexual Harassment of Women at Workplace (Prevention, Prohibition and Redressal) Act
S+: Article 15(3) allows the State to make special provisions for women and children
S+: The Dowry Prohibition Act 1961 makes giving and taking dowry an offence
S+: The SC and ST (Prevention of Atrocities) Act provides for special courts for speedy trial
S+: The Rights of Persons with Disabilities Act 2016 replaced the Persons with Disabilities Act 1995
S+: In the Vishaka case the Supreme Court relied on the CEDAW convention in the absence of a domestic law
S-: The Rights of Persons with Disabilities Act recognises only seven disabilities | It recognises 21 kinds of disabilities
S-: The Vishaka guidelines were issued by Parliament | They were laid down by the Supreme Court in 1997
S-: Special provisions for women violate the right to equality | Article 15(3) expressly permits special provisions for women and children
C: Special laws protect vulnerable groups | general laws have not been enough to prevent discrimination and violence against them
C: The Supreme Court laid down the Vishaka guidelines | there was no law on sexual harassment at the workplace at that time
C: Special courts are set up under the Atrocities Act | speedy trial is needed to give justice to victims and deter offenders
X: C2 D2 2 | What were the Vishaka guidelines? | Guidelines laid down by the Supreme Court in 1997 to prevent and redress sexual harassment of women at the workplace; later replaced by the 2013 Act.
X: C3 D3 2 | Why are special laws needed for vulnerable groups? | They face discrimination, violence and exclusion; general laws inadequate; Constitution permits special provisions (Articles 15(3), 15(4), 46).
X: C3 D3 3 | Name any three laws protecting the rights of women in India. | Dowry Prohibition Act 1961; Protection of Women from Domestic Violence Act 2005; Sexual Harassment of Women at Workplace Act 2013; Maternity Benefit Act.
X: C3 D4 3 | Explain the main provisions of the Rights of Persons with Disabilities Act 2016. | Recognises 21 disabilities; non-discrimination; reservation in education and jobs; accessibility; free education for children with benchmark disabilities; penalties for offences.
X: C4 D4 3 | Explain the protection given to Scheduled Castes and Scheduled Tribes. | Article 17 abolishes untouchability; Article 46; reservations; Protection of Civil Rights Act 1955; SC and ST (Prevention of Atrocities) Act 1989 – offences, special courts, relief.
L: D4 | Explain the legal protection of the rights of women, SC/ST and persons with disabilities in India. | Constitutional provisions; Vishaka, POSH 2013, Domestic Violence Act 2005, Dowry Prohibition Act; Article 17, Atrocities Act 1989; RPwD Act 2016.
"""),
]

CH11 = [ST(S + '11-st1', 'common human rights violations', """
T: custodial violence | torture, ill-treatment or death of a person in the custody of the police or other authorities
T: human trafficking | the recruitment, transport or harbouring of persons by force, fraud or deception for exploitation
T: bonded labour | a system in which a person is forced to work to repay a debt, often for years or generations
T: discrimination | unfair treatment of a person on grounds such as caste, religion, sex or disability
Q: Trafficking in human beings and forced labour are prohibited by: | Article 23 | Article 17 | Article 21A | Article 300A
Q: The Bonded Labour System (Abolition) Act was passed in: | 1976 | 1956 | 1986 | 2005
Q: Guidelines to prevent custodial violence were laid down in: | D.K. Basu v State of West Bengal | Vishaka v State of Rajasthan | Salomon v Salomon | Olga Tellis v Bombay Municipal Corporation
Q: The Immoral Traffic (Prevention) Act was passed in: | 1956 | 1976 | 1993 | 2013
Q: Which of these is a human rights violation? | Torture in police custody | Arrest on a valid warrant | Grant of bail | Free legal aid
Y: 1976 | the enactment of the Bonded Labour System (Abolition) Act
S+: Custodial torture violates the right to life and dignity under Article 21
S+: The D.K. Basu guidelines require police to carry identification and prepare an arrest memo
S+: The D.K. Basu guidelines require a relative or friend of the arrested person to be informed of the arrest
S+: Trafficking is often linked to forced labour, sexual exploitation and child labour
S+: Discrimination on grounds of religion, race, caste, sex or place of birth is prohibited by Article 15
S-: Custodial violence is permitted to obtain confessions | It violates Article 21, and confessions to police are generally not admissible
S-: Bonded labour is legal if the worker owes money | Bonded labour is abolished and prohibited by Article 23 and the 1976 Act
S-: Human rights violations can be committed only by private persons | They are often committed by State agents such as police
C: The Supreme Court laid down guidelines on arrest in D.K. Basu | custodial violence and deaths in police custody were widespread
C: Bonded labour violates human rights | it denies the worker freedom of movement, choice of employment and dignity
C: Trafficking flourishes among the poor | poverty and lack of education make people easy targets of false promises of jobs
X: C2 D2 2 | What is custodial violence? | Torture, ill-treatment or death of a person in the custody of police or other authorities; violates Article 21.
X: C3 D3 2 | Why is bonded labour a human rights violation? | Forced work to repay a debt; denies freedom, dignity and choice of work; prohibited by Article 23 and the 1976 Act.
X: C3 D3 3 | State any three D.K. Basu guidelines on arrest. | Police to carry visible identification; arrest memo attested by a witness; inform a relative or friend; inform the arrested person of this right; medical examination; production before magistrate.
X: C3 D4 3 | Explain the causes and effects of human trafficking. | Causes – poverty, lack of education, unemployment, gender discrimination, demand for cheap labour; effects – exploitation, abuse, loss of liberty and health.
X: C4 D4 3 | 'Custodial violence is a crime against humanity.' Explain. | Violates Article 21 and dignity; abuse of State power; deaths in custody; D.K. Basu guidelines; NHRC reporting; compensation by courts.
L: D4 | Explain the common forms of human rights violations in India. | Custodial violence – D.K. Basu; trafficking – Article 23, ITPA 1956; bonded labour – 1976 Act; child labour – Article 24; discrimination – Articles 15, 17.
"""), ST(S + '11-st2', 'National and State Human Rights Commissions', """
T: National Human Rights Commission | the statutory body set up under the Protection of Human Rights Act 1993 to inquire into violations of human rights
T: State Human Rights Commission | the statutory body set up in a State under the Protection of Human Rights Act 1993 to inquire into violations in that State
T: Human Rights Courts | the Sessions Courts specified in each district under the Protection of Human Rights Act for speedy trial of offences arising from human rights violations
T: suo motu cognizance | action taken by a body on its own, without a complaint being filed
Q: The NHRC was set up under the: | Protection of Human Rights Act 1993 | Legal Services Authorities Act 1987 | Advocates Act 1961 | Commissions for Protection of Child Rights Act 2005
Q: The NHRC is a: | statutory body | constitutional body | non-governmental organisation | court of law
Q: The chairperson of the NHRC is a person who has been: | Chief Justice of India or a judge of the Supreme Court | a retired IAS officer | a Member of Parliament | a Governor
Q: The members of the NHRC are appointed by the: | President on the recommendation of a committee headed by the Prime Minister | Chief Justice of India | Parliament by vote | Home Secretary
Q: The NHRC generally cannot inquire into a matter after the expiry of: | one year from the date of the alleged act | ten years | one month | five years
Q: The recommendations of the NHRC are: | recommendatory and not binding | binding like a court decree | final with no follow-up | binding on Parliament
Y: 1993 | the enactment of the Protection of Human Rights Act
S+: The NHRC can inquire into violations suo motu or on a petition by a victim or any person on the victim's behalf
S+: The NHRC can intervene in court proceedings involving allegations of human rights violations
S+: The NHRC can visit jails and other institutions to study the living conditions of inmates
S+: The NHRC promotes human rights literacy and research
S+: The NHRC has the powers of a civil court while inquiring into complaints
S-: The NHRC can punish those guilty of violations | It can only recommend action; it cannot punish
S-: The NHRC is a constitutional body | It is a statutory body under the Protection of Human Rights Act 1993
S-: The NHRC can inquire into any matter regardless of when it occurred | It generally cannot inquire after one year from the act
C: The NHRC is called a watchdog of human rights | it inquires into violations and recommends relief and action
C: The NHRC's effectiveness is limited | its recommendations are not binding on the government
C: Human Rights Courts are set up | they provide speedy trial of offences arising from violations of human rights
X: C2 D2 2 | What is the National Human Rights Commission? | Statutory body set up under the Protection of Human Rights Act 1993 to inquire into and recommend action on violations of human rights.
X: C3 D3 2 | Why is the NHRC called a recommendatory body? | It cannot punish or enforce its findings; it recommends compensation, prosecution and other action to the government.
X: C3 D3 3 | State any three functions of the NHRC. | Inquire into violations suo motu or on petition; intervene in court proceedings; visit jails; review safeguards; study treaties; research; spread human rights literacy; encourage NGOs.
X: C3 D4 3 | Explain the composition and appointment of the NHRC. | Chairperson – former CJI or SC judge; members including judges and persons with human rights knowledge; ex officio members – chairpersons of national commissions; appointed by President on recommendation of committee headed by PM.
X: C4 D4 3 | 'The NHRC is a watchdog without teeth.' Examine. | Recommendatory powers; one-year limit; limited jurisdiction over armed forces; dependence on government; yet influence through inquiries, reports, public pressure, compensation recommendations.
L: D4 | Explain the composition, functions and powers of the National Human Rights Commission. | PHRA 1993; composition and appointment; functions; powers of civil court; limitations; State Human Rights Commissions; Human Rights Courts.
"""), ST(S + '11-st3', 'other commissions and complaint mechanisms', """
T: National Commission for Women | the statutory body set up in 1992 under the National Commission for Women Act 1990 to safeguard the rights of women
T: National Commission for Scheduled Castes | the constitutional body under Article 338 that investigates matters relating to safeguards for Scheduled Castes
T: National Commission for Protection of Child Rights | the statutory body set up under the Commissions for Protection of Child Rights Act 2005 to protect child rights
T: National Commission for Scheduled Tribes | the constitutional body under Article 338A that investigates matters relating to safeguards for Scheduled Tribes
Q: The National Commission for Scheduled Castes is provided under: | Article 338 | Article 338A | Article 39A | Article 323A
Q: The National Commission for Women was constituted under an Act passed in: | 1990 | 1993 | 2005 | 1987
Q: The NCPCR was set up under an Act passed in: | 2005 | 1990 | 1993 | 2012
Q: The National Commission for Scheduled Tribes is provided under: | Article 338A | Article 338 | Article 51 | Article 21A
Q: Which of these is a constitutional body? | National Commission for Scheduled Castes | National Commission for Women | National Human Rights Commission | NCPCR
M:commission: NCSC | Article 338
M:commission: NCST | Article 338A
M:commission: NCW | National Commission for Women Act 1990
M:commission: NCPCR | Commissions for Protection of Child Rights Act 2005
S+: The NCW reviews constitutional and legal safeguards for women and looks into complaints
S+: The 89th Amendment (2003) created separate national commissions for Scheduled Castes and Scheduled Tribes
S+: The NCPCR monitors the implementation of laws such as the Right to Education Act and POCSO Act
S+: A complaint to the NHRC can be made in writing, by post or online, and no fee is charged
S+: Complaints can be made in English, Hindi or any language in the Eighth Schedule
S-: The NCW is a constitutional body | It is a statutory body under the 1990 Act
S-: A fee must be paid to file a complaint with the NHRC | No fee is charged
S-: The NCSC is a statutory body | It is a constitutional body under Article 338
C: Separate commissions are needed for women, children and Scheduled Castes and Tribes | each group faces specific problems that need focused attention
C: Complaint procedures before the commissions must be simple and free | victims are often poor and cannot afford legal procedures
C: The NCPCR monitors the Right to Education Act | children's rights depend on effective implementation of such laws
X: C2 D2 2 | Distinguish between a constitutional and a statutory commission with examples. | Constitutional – created by the Constitution (NCSC, Article 338; NCST, Article 338A); statutory – created by a law (NHRC, NCW, NCPCR).
X: C3 D3 2 | How can a person file a complaint with the NHRC? | In writing, by post, fax, email or online portal; in English, Hindi or an Eighth Schedule language; no fee; with details of the violation.
X: C3 D3 3 | State any three functions of the National Commission for Women. | Review safeguards for women; recommend legal reforms; look into complaints and take suo motu notice; inspect jails and remand homes; research and awareness.
X: C3 D4 3 | Explain the role of the NCPCR. | Statutory under 2005 Act; protects child rights; examines safeguards; inquires into violations; monitors RTE Act and POCSO Act; research and awareness.
X: C4 D4 3 | 'India has a network of commissions to protect human rights.' Explain. | NHRC and SHRCs; NCW; NCSC (Article 338); NCST (Article 338A); NCPCR; National Commission for Minorities; complaint mechanisms; recommendatory nature.
L: D4 | Explain the role of national commissions and the procedure for filing complaints about human rights violations. | NCW, NCSC, NCST, NCPCR – basis and functions; NHRC complaint procedure – writing, language, no fee, online; limitations.
"""),
]

CH12 = [ST(S + '12-st1', 'meaning, nature and sources of international law', """
T: international law | the body of rules and principles that govern relations between States and other international actors
T: treaty | a written agreement between States governed by international law
T: international custom | a general practice of States accepted as law
T: pacta sunt servanda | the principle that every treaty in force is binding on the parties and must be performed in good faith
T: private international law | the rules that decide which country's law applies and which courts have jurisdiction in disputes with a foreign element
Q: The sources of international law are listed in: | Article 38 of the Statute of the ICJ | Article 51 of the Constitution of India | Article 2 of the UN Charter | Article 253 of the Constitution of India
Q: The term 'international law' was coined by: | Jeremy Bentham | Hugo Grotius | John Locke | Montesquieu
Q: The 'father of international law' is generally considered to be: | Hugo Grotius | Jeremy Bentham | John Austin | Woodrow Wilson
Q: Under Article 38, judicial decisions and the teachings of eminent publicists are: | subsidiary means for determining rules of law | primary sources | not sources at all | binding treaties
Q: The law of treaties is codified in the: | Vienna Convention on the Law of Treaties 1969 | Geneva Convention 1949 | Paris Agreement 2015 | Berne Convention 1886
Q: A general practice of States accepted as law is: | international custom | a treaty | a judicial decision | a resolution of a municipal body
M:source: International conventions | treaties establishing rules recognised by the parties
M:source: International custom | general practice accepted as law
M:source: General principles of law | principles recognised by civilised nations
M:source: Judicial decisions | subsidiary means for determining rules of law
S+: Article 38(1) of the ICJ Statute lists treaties, custom, general principles of law, and judicial decisions and teachings of publicists
S+: Public international law governs relations between States, while private international law deals with conflict of laws
S+: International law has no central legislature or police force, and enforcement depends largely on consent and cooperation
S+: Customary international law binds all States, including those that are not parties to a treaty on the subject
S+: Under the principle of pacta sunt servanda treaties must be performed in good faith
S-: International law has a world parliament that makes all its rules | There is no central legislature; rules come from treaties and custom
S-: Judicial decisions are a primary source under Article 38 | They are subsidiary means for determining rules of law
S-: Private international law governs relations between States | It deals with conflict of laws in private disputes with a foreign element
C: International law is sometimes called weak law | it lacks a central legislature and a strong enforcement machinery
C: States generally follow international law | they value reciprocity, reputation and peaceful relations
C: Treaties bind the States that are parties to them | under pacta sunt servanda a treaty in force must be performed in good faith
X: C2 D2 2 | Distinguish between public and private international law. | Public – rules governing relations between States and international organisations; private – rules on applicable law and jurisdiction in private disputes with a foreign element.
X: C3 D3 2 | What is pacta sunt servanda? | The principle that a treaty in force binds the parties and must be performed in good faith; codified in the Vienna Convention 1969.
X: C3 D3 3 | Explain the sources of international law under Article 38 of the ICJ Statute. | International conventions; international custom; general principles of law recognised by civilised nations; judicial decisions and teachings of publicists as subsidiary means.
X: C3 D4 3 | Explain the nature of international law. | Governs States and international organisations; based on consent; no central legislature, executive or compulsory court; enforcement by reciprocity, sanctions, UN.
X: C4 D4 3 | 'Is international law true law?' Discuss. | Austin – no sovereign command, so not law; others – States accept it as binding, treaties and custom, ICJ, UN Charter; generally obeyed; weak enforcement.
L: D4 | Explain the meaning, nature and sources of international law. | Definition; public and private; nature – consent-based, no central authority; sources under Article 38 – treaties, custom, general principles, judicial decisions and publicists.
"""), ST(S + '12-st2', 'international law and municipal law; Article 51', """
T: municipal law | the national or domestic law of a State
T: monism | the theory that international law and municipal law form a single legal system
T: dualism | the theory that international law and municipal law are separate systems, so a treaty needs domestic legislation to take effect
T: Article 51 | the Directive Principle that the State shall promote international peace and security and foster respect for international law and treaty obligations
T: Article 253 | the provision that empowers Parliament to make laws for implementing treaties and international agreements
Q: India generally follows the: | dualist approach | monist approach | theocratic approach | colonial approach
Q: Parliament can make laws to implement international treaties under: | Article 253 | Article 51 | Article 32 | Article 300A
Q: Fostering respect for international law and treaty obligations is a directive under: | Article 51 | Article 21 | Article 39A | Article 323B
Q: In India, treaties are entered into by the: | Union executive | State Legislatures | Supreme Court | Election Commission
Q: The Supreme Court used the CEDAW convention to frame guidelines in: | Vishaka v State of Rajasthan | Salomon v Salomon | Rylands v Fletcher | Kasturi Lal v State of U.P.
S+: Article 51 directs the State to encourage settlement of international disputes by arbitration
S+: In India a treaty does not automatically become part of domestic law unless Parliament legislates for it
S+: Indian courts interpret domestic laws in harmony with international obligations where there is no conflict
S+: Customary international law not inconsistent with domestic law is treated as part of Indian law by the courts
S+: Under monism, international law may prevail over national law in case of conflict
S-: In India every treaty automatically becomes enforceable domestic law | India follows dualism; Parliament must legislate under Article 253
S-: Article 51 is a fundamental right | It is a Directive Principle of State Policy
S-: State Legislatures make laws to implement treaties | Parliament has this power under Article 253, even on State subjects
C: Parliament can legislate on a State subject to implement a treaty | Article 253 gives it power to implement international agreements
C: Indian courts sometimes rely on international conventions | where domestic law is silent, conventions consistent with fundamental rights can be read into them
C: India needs legislation to give effect to treaties | it follows the dualist approach
X: C2 D2 2 | Distinguish between monism and dualism. | Monism – international and municipal law form one system, international law may prevail; dualism – separate systems, treaties need domestic legislation (India).
X: C3 D3 2 | What does Article 51 direct the State to do? | Promote international peace and security; maintain just and honourable relations; foster respect for international law and treaties; encourage settlement by arbitration.
X: C3 D3 3 | Explain how treaties are implemented in India. | Executive enters treaties (Article 73); dualist approach; Parliament legislates under Article 253, even on State subjects; courts interpret laws consistently with treaties.
X: C3 D4 3 | Explain the use of international law by Indian courts. | Vishaka – CEDAW used for guidelines; customary law read into domestic law if not inconsistent; harmonious interpretation; environmental principles from international law.
X: C4 D4 3 | 'India is dualist in theory but often monist in practice.' Explain. | Treaties need legislation (Article 253); but courts apply customary international law and conventions where law is silent (Vishaka); harmonious construction.
L: D4 | Explain the relationship between international law and municipal law with reference to India. | Monism and dualism; Article 51; Article 73 and 253; implementation of treaties; role of courts – Vishaka and customary law.
"""), ST(S + '12-st3', 'United Nations and the International Court of Justice', """
T: United Nations | the international organisation established in 1945 to maintain international peace and security and promote cooperation
T: International Court of Justice | the principal judicial organ of the United Nations, located at The Hague
T: contentious jurisdiction | the power of the ICJ to decide legal disputes between States that consent to its jurisdiction
T: advisory opinion | an opinion of the ICJ on a legal question referred by authorised UN organs or agencies
T: Security Council | the UN organ with primary responsibility for international peace and security, with five permanent members holding the veto
Q: The ICJ is located at: | The Hague | Geneva | New York | Vienna
Q: The number of judges of the ICJ is: | 15 | 9 | 21 | 5
Q: Judges of the ICJ are elected for a term of: | nine years | five years | six years | life
Q: Only the following can be parties in contentious cases before the ICJ: | States | individuals | private companies | NGOs
Q: The United Nations came into existence on: | 24 October 1945 | 10 December 1948 | 26 June 1919 | 1 January 1942
Q: The case between India and Pakistan decided by the ICJ in 2019 concerned: | Kulbhushan Jadhav | the Indus Waters Treaty | the Kashmir boundary | trade tariffs
Y: 1945 | the establishment of the United Nations
S+: The principal organs of the UN are the General Assembly, the Security Council, ECOSOC, the Trusteeship Council, the ICJ and the Secretariat
S+: Article 33 of the UN Charter lists negotiation, enquiry, mediation, conciliation, arbitration and judicial settlement as peaceful means
S+: ICJ judgments are final and binding on the parties, with no appeal
S+: The ICJ's jurisdiction in contentious cases depends on the consent of the States concerned
S+: The judges of the ICJ are elected by the General Assembly and the Security Council
S-: Individuals can file cases against States in the ICJ | Only States can be parties in contentious cases
S-: The ICJ is located at Geneva | It is located at The Hague
S-: Advisory opinions of the ICJ are binding judgments | Advisory opinions are generally not binding
C: The ICJ cannot hear a dispute against a State's will | its contentious jurisdiction depends on the consent of the States concerned
C: The UN Charter prefers peaceful settlement | the use of force threatens international peace and security
C: Permanent members have great influence in the Security Council | each of them can veto substantive decisions
X: C2 D2 2 | Distinguish between contentious and advisory jurisdiction of the ICJ. | Contentious – legal disputes between consenting States, binding judgments; advisory – opinions on legal questions referred by UN organs, generally not binding.
X: C3 D3 2 | Why is the ICJ's jurisdiction said to be based on consent? | States must accept jurisdiction by special agreement, treaty clause or optional clause declaration; no compulsory jurisdiction otherwise.
X: C3 D3 3 | Explain the peaceful means of dispute settlement under the UN Charter. | Article 33 – negotiation, enquiry, mediation, conciliation, arbitration, judicial settlement, regional arrangements; Security Council may call on parties.
X: C3 D4 3 | Explain the composition and jurisdiction of the ICJ. | 15 judges, nine-year terms, elected by GA and SC; The Hague; contentious jurisdiction between States by consent; advisory opinions; judgments final and binding.
X: C4 D4 3 | 'The ICJ has helped settle disputes but has limits.' Explain. | Settles legal disputes peacefully, e.g. Kulbhushan Jadhav case; limits – consent-based jurisdiction, only States, enforcement depends on Security Council.
L: D4 | Explain the role of the United Nations and the ICJ in the peaceful settlement of international disputes. | UN 1945, principal organs; Article 33 means; ICJ composition, jurisdiction, binding judgments, advisory opinions; Security Council role; limitations.
"""),
]

CH13 = [ST(S + '13-st1', 'legal profession: Advocates Act, Bar Council and ethics', """
T: advocate | a person whose name is entered on the roll of a State Bar Council under the Advocates Act 1961
T: Bar Council of India | the statutory body under the Advocates Act 1961 that regulates the legal profession and legal education in India
T: State Bar Council | the body under the Advocates Act that enrols advocates and takes disciplinary action against them for misconduct in the State
T: senior advocate | an advocate designated by the Supreme Court or a High Court on the basis of ability, standing at the Bar or special knowledge
T: professional misconduct | conduct of an advocate that violates the standards of professional ethics laid down by the Bar Council of India
T: Attorney General for India | the highest law officer of the Union, appointed by the President under Article 76
Q: The legal profession in India is regulated by the: | Advocates Act 1961 | Legal Services Authorities Act 1987 | Companies Act 2013 | Protection of Human Rights Act 1993
Q: An advocate is enrolled by the: | State Bar Council | Supreme Court | Ministry of Law | National Legal Services Authority
Q: The Attorney General for India is appointed under: | Article 76 | Article 165 | Article 124 | Article 39A
Q: The Advocate General of a State is appointed under: | Article 165 | Article 76 | Article 217 | Article 323A
Q: Which of these is prohibited for an advocate under the Bar Council rules? | Advertising or soliciting work | Appearing for a client | Advising a client | Drafting documents
Q: Disciplinary proceedings for professional misconduct are first decided by the: | disciplinary committee of the State Bar Council | Supreme Court | Ministry of Law | Lok Adalat
Y: 1961 | the enactment of the Advocates Act
S+: Advocates owe duties to the court, to their clients, to opponents and to fellow advocates
S+: An advocate must not disclose communications made by a client in confidence
S+: An advocate should not ordinarily refuse a brief within his field if the fee is proper
S+: The Bar Council of India lays down standards of professional conduct and promotes legal education
S+: An advocate entitled to practise may practise in all courts and tribunals throughout India
S-: Advocates may advertise their services like other businesses | Bar Council rules prohibit advocates from advertising or soliciting work
S-: An advocate is enrolled by the Supreme Court | Enrolment is by a State Bar Council
S-: The Bar Council of India is a non-statutory club | It is a statutory body under the Advocates Act 1961
C: Advocates must keep client communications confidential | clients must be able to disclose all facts freely to get proper advice
C: Advocates are called officers of the court | they owe a duty to assist the court in the administration of justice
C: Advocates may not advertise | law is a noble profession and not a trade or business
X: C2 D2 2 | What is the Bar Council of India? | Statutory body under the Advocates Act 1961 that lays down standards of professional conduct, safeguards advocates' rights and regulates legal education.
X: C3 D3 2 | Why are advocates called officers of the court? | They owe a duty to assist the court in administering justice; must not mislead the court; must maintain dignity and respect.
X: C3 D3 3 | State any three duties of an advocate towards the client. | Not refuse brief without good reason; maintain confidentiality; avoid conflict of interest; not withdraw without notice; fearlessly uphold client's interest; account for client's money.
X: C3 D4 3 | Explain the functions of the Bar Council of India. | Standards of professional conduct; procedure for disciplinary committees; safeguarding rights of advocates; promote law reform; regulate legal education and recognise law degrees; supervise State Bar Councils.
X: C4 D4 3 | 'Law is a profession, not a business.' Explain with reference to professional ethics. | Prohibition on advertising and soliciting; duty to court; confidentiality; no fee tied to results; duty to give legal aid; disciplinary action for misconduct.
L: D4 | Explain the regulation of the legal profession under the Advocates Act 1961 and the professional ethics of advocates. | Bar Council of India and State Bar Councils; enrolment; senior advocates; duties to court, client, opponent, colleagues; misconduct and disciplinary committees; law officers.
"""), ST(S + '13-st2', 'legal education and women in the legal profession', """
T: legal education | the education of persons in the principles, practices and theory of law, regulated in India by the Bar Council of India
T: five-year integrated LL.B. | a law degree programme taken after Class 12 that combines a bachelor's degree with law
T: National Law University | an autonomous law university set up by a State law to offer integrated law programmes
T: Legal Practitioners (Women) Act 1923 | the law that removed the bar on women entering the legal profession in India
Q: The first woman judge of the Supreme Court of India was: | Justice M. Fathima Beevi | Justice Leila Seth | Justice Anna Chandy | Justice Ruma Pal
Q: The first woman judge of a High Court in India was: | Justice Anna Chandy | Justice M. Fathima Beevi | Justice Indira Banerjee | Justice Sujata Manohar
Q: The first woman Chief Justice of a High Court in India was: | Justice Leila Seth | Justice Anna Chandy | Justice M. Fathima Beevi | Justice Gyan Sudha Misra
Q: A pioneer who was among the first women to practise law in India is: | Cornelia Sorabji | Sarojini Naidu | Annie Besant | Vijaya Lakshmi Pandit
Q: Women were permitted to enter the legal profession in India by a law passed in: | 1923 | 1961 | 1950 | 1987
Q: Legal education in India is regulated by the: | Bar Council of India | National Human Rights Commission | Election Commission | Law Commission of India
Y: 1923 | the passing of the Legal Practitioners (Women) Act
S+: The five-year integrated law degree is offered after Class 12 by National Law Universities and other institutions
S+: Admission to many National Law Universities is through the Common Law Admission Test (CLAT)
S+: Justice M. Fathima Beevi was appointed to the Supreme Court in 1989
S+: Women remain under-represented among judges of the higher judiciary
S+: Clinical legal education, moot courts and legal aid clinics give practical training to law students
S-: Women have been allowed to practise law in India since 1850 | Women were permitted by the Legal Practitioners (Women) Act 1923
S-: Justice Anna Chandy was the first woman judge of the Supreme Court | She was the first woman High Court judge; Justice Fathima Beevi was the first in the Supreme Court
S-: Legal education is regulated by the Election Commission | It is regulated by the Bar Council of India
C: The Legal Practitioners (Women) Act 1923 was passed | courts had earlier refused to enrol women as legal practitioners
C: National Law Universities changed legal education | they introduced five-year integrated programmes with practical and interdisciplinary training
C: Greater representation of women in the judiciary matters | it brings diverse perspectives and builds public confidence in justice
X: C2 D2 2 | What is the five-year integrated LL.B. programme? | A law degree taken after Class 12 combining a bachelor's degree (B.A., B.B.A., B.Com.) with law; offered by NLUs and other institutions.
X: C3 D3 2 | Why was the Legal Practitioners (Women) Act 1923 important? | It removed the bar on women entering the legal profession after courts had refused to enrol women such as Regina Guha.
X: C3 D3 3 | Name any three pioneering women in the Indian legal profession and their contribution. | Cornelia Sorabji – among first women lawyers; Anna Chandy – first woman HC judge; Fathima Beevi – first woman SC judge (1989); Leila Seth – first woman Chief Justice of a HC.
X: C3 D4 3 | Explain the main features of legal education in India today. | Regulated by BCI; three-year and five-year LL.B.; NLUs and CLAT; moot courts, internships, clinical education; LL.M. and research.
X: C4 D4 3 | 'Women have travelled a long way in the legal profession, but much remains.' Explain. | Early exclusion; 1923 Act; pioneers – Sorabji, Chandy, Fathima Beevi, Leila Seth; growing numbers; still under-represented in higher judiciary and senior positions.
L: D4 | Explain the development of legal education and the role of women in the legal profession in India. | BCI regulation; three-year and five-year degrees; NLUs and CLAT; practical training; women – 1923 Act, pioneers, present position.
"""), ST(S + '13-st3', 'free legal aid: Article 39A and the Legal Services Authorities Act', """
T: Article 39A | the Directive Principle requiring the State to secure equal justice and provide free legal aid so that no citizen is denied justice because of economic or other disabilities
T: National Legal Services Authority | the apex body under the Legal Services Authorities Act 1987 that lays down policies and schemes for legal services
T: free legal aid | legal services provided free of cost to eligible persons, including advice, representation and court fees
T: District Legal Services Authority | the body that implements legal services schemes and organises Lok Adalats in a district
T: legal literacy | awareness among people of their legal rights and the remedies available
Q: Article 39A was added by the: | 42nd Amendment (1976) | 44th Amendment (1978) | 86th Amendment (2002) | 73rd Amendment (1992)
Q: The patron-in-chief of NALSA is the: | Chief Justice of India | President of India | Prime Minister | Law Minister
Q: The Legal Services Authorities Act came into force on 9 November 1995, which is observed as: | National Legal Services Day | Human Rights Day | Law Day | Constitution Day
Q: Which of these persons is entitled to free legal aid under the Act? | A member of a Scheduled Caste | Any company | A wealthy businessman | A foreign diplomat
Q: The executive chairman of NALSA is usually the: | senior-most judge of the Supreme Court after the CJI | Attorney General | Chief Justice of a High Court | Law Secretary
Q: The right to free legal aid has been held to be part of: | Article 21 | Article 300A | Article 51 | Article 323A
Y: 1976 | the 42nd Amendment inserting Article 39A on free legal aid
Y: 1995 | the coming into force of the Legal Services Authorities Act on 9 November
S+: Women, children, members of Scheduled Castes and Tribes, persons with disabilities and persons in custody are entitled to free legal aid
S+: Victims of trafficking, mass disasters, ethnic violence and industrial workmen are entitled to free legal aid
S+: Legal services authorities exist at the national, State, district and taluk levels
S+: Legal services authorities organise Lok Adalats and legal literacy camps
S+: In Hussainara Khatoon v State of Bihar the Supreme Court held that free legal aid is an essential part of a fair trial under Article 21
S-: Article 39A is a fundamental right | It is a Directive Principle; the right to legal aid has been read into Article 21
S-: Free legal aid is available only to persons charged with murder | It is available to all eligible persons in civil and criminal matters
S-: The Prime Minister is the patron-in-chief of NALSA | The Chief Justice of India is its patron-in-chief
C: Free legal aid is necessary | poverty or other disability should not prevent any citizen from getting justice
C: Legal literacy is essential for access to justice | people cannot claim rights they do not know about
C: Legal aid is part of a fair trial | an accused who cannot afford a lawyer cannot defend himself effectively
X: C2 D2 2 | What does Article 39A provide? | Directive Principle (42nd Amendment, 1976) that the State shall secure equal justice and provide free legal aid so that no citizen is denied justice due to economic or other disabilities.
X: C3 D3 2 | Why is free legal aid called part of a fair trial? | An accused who cannot afford a lawyer cannot defend effectively; Supreme Court read legal aid into Article 21 (Hussainara Khatoon).
X: C3 D3 3 | State any three categories of persons entitled to free legal aid. | SC/ST members; victims of trafficking or begar; women and children; persons with disabilities; victims of mass disaster; industrial workmen; persons in custody; persons with low income.
X: C3 D4 3 | Explain the structure of legal services authorities in India. | NALSA – patron-in-chief CJI, executive chairman senior SC judge; State Legal Services Authorities; District Legal Services Authorities; Taluk Legal Services Committees; Supreme Court and High Court Legal Services Committees.
X: C4 D4 3 | 'Access to justice is meaningless without legal aid.' Explain. | Poverty, illiteracy, cost of litigation; Article 39A; Article 21 – fair trial; LSA Act 1987 – eligibility, authorities, Lok Adalats, legal literacy.
L: D4 | Explain the provisions for free legal aid in India under Article 39A and the Legal Services Authorities Act 1987. | Article 39A; Hussainara Khatoon; LSA Act – NALSA, SLSA, DLSA, taluk committees; eligibility; Lok Adalats; legal literacy; 9 November Legal Services Day.
L: D5 | Evaluate the working of the legal aid system in India. | Constitutional and statutory basis; achievements – Lok Adalats, panel lawyers, legal literacy, para-legal volunteers; problems – low awareness, quality of lawyers, funding; suggestions.
"""),
]

CHAPTERS = [(CH08, {}), (CH09, {}), (CH10, {}), (CH11, {}), (CH12, {}), (CH13, {})]
