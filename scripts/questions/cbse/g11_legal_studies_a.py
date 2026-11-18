"""CBSE class 11 Legal Studies (074), chapters 1-6: fact tables for g12_hum_engine.

Only well-established facts are used: constitutional articles, statutes with their years, and leading cases whose
holdings are settled. Criminal statutes are named with their 2023 replacements where relevant."""
from g12_hum_engine import ST

S = 'cbse-g11-legal-studies-ch'

CH01 = [ST(S + '01-st1', 'the state and its elements', """
T: state | a politically organised community of people living in a definite territory, with a government and sovereignty
T: population | the people who live in a state; no state can exist without people
T: territory | the definite area of land, water and air space over which a state exercises its authority
T: government | the agency through which the will of the state is formulated, expressed and carried out
T: sovereignty | the supreme power of the state, internally over all persons and associations and externally free from outside control
Q: Which of the following is NOT an essential element of a state? | A written constitution | Population | Territory | Sovereignty
Q: Which element distinguishes a state from all other associations? | Sovereignty | Population | Government | Territory
Q: The agency through which the will of the state is expressed and carried out is the: | government | nation | society | territory
Q: Which article of the Indian Constitution declares that India, that is Bharat, shall be a Union of States? | Article 1 | Article 12 | Article 14 | Article 368
Q: For the purposes of Part III (Fundamental Rights), the term 'State' is defined in: | Article 12 | Article 1 | Article 36 | Article 51A
Q: The territory of a state includes: | land, inland waters, territorial waters and the air space above them | land only | land and rivers only | only the land within its capital
S+: Population, territory, government and sovereignty are the four essential elements of a state
S+: A state may have a small or a large population; there is no fixed minimum size
S+: Government is the machinery of the state; governments may change but the state continues
S+: Sovereignty is the element that distinguishes a state from other associations such as a club or a trade union
S+: Article 12 of the Indian Constitution defines 'State' to include the Government and Parliament of India, State Governments and Legislatures, and local and other authorities
S+: The territory of a state includes its land, waters and the air space above them
S-: A state can exist without a definite territory | A definite territory is an essential element of a state
S-: Government and state are the same thing | Government is only the agency of the state; governments change while the state continues
S-: A state must have a population of at least one million | There is no fixed minimum population for a state
S-: A province of a federation is a sovereign state | A province or unit of a federation lacks sovereignty
C: A trade union is not a state | it lacks sovereignty, which only the state possesses
C: The state is called a permanent institution while governments are temporary | governments change through elections or other means, but the state with its people, territory and sovereignty continues
C: Government is described as the machinery of the state | it is through the government that the will of the state is formulated, expressed and enforced
X: C2 D2 2 | Name the four essential elements of a state. | Population, territory, government and sovereignty.
X: C3 D3 3 | Distinguish between state and government. | State is permanent, abstract, has all four elements and sovereignty; government is temporary, concrete, only one element and the agency of the state; government can be changed, the state continues.
X: C4 D4 3 | 'Sovereignty is the soul of the state.' Explain with reference to the elements of the state. | Without sovereignty a community is not a state (e.g. a province or a club); sovereignty gives supreme internal authority and external independence; other elements are necessary but not distinctive.
L: D4 | Explain the meaning of state and discuss its four essential elements with examples. | Meaning; population (no fixed size); territory (land, water, air space); government (agency, forms vary); sovereignty (internal and external, distinctive element); Article 12 definition for Fundamental Rights; difference from government.
"""), ST(S + '01-st2', 'theories of the origin of the state', """
T: divine origin theory | the theory that the state was created by God and the ruler is God's representative, answerable only to God
T: force theory | the theory that the state originated through the subjugation of the weak by the strong
T: social contract theory | the theory that the state arose from an agreement among individuals who left the state of nature
T: evolutionary (historical) theory | the theory that the state is the product of gradual growth through kinship, religion, property and political consciousness
T: state of nature | the condition of human beings before the creation of the state, as imagined by social contract thinkers
T: general will | Rousseau's idea of the collective will of the community aimed at the common good
Q: Who wrote 'Leviathan' (1651)? | Thomas Hobbes | John Locke | Jean-Jacques Rousseau | Montesquieu
Q: Who wrote 'Two Treatises of Government'? | John Locke | Thomas Hobbes | Jean-Jacques Rousseau | Jean Bodin
Q: 'The Social Contract' (1762) was written by: | Jean-Jacques Rousseau | Thomas Hobbes | John Locke | Montesquieu
Q: According to Hobbes, life in the state of nature was: | solitary, poor, nasty, brutish and short | peaceful and happy | governed by the general will | based on natural rights to property
Q: Which thinker held that individuals keep their natural rights to life, liberty and property even after forming the state? | John Locke | Thomas Hobbes | Jean Bodin | Jean-Jacques Rousseau
Q: The idea of the 'general will' is associated with: | Rousseau | Hobbes | Locke | Austin
Q: Which theory of the origin of the state is generally accepted as the most satisfactory? | Evolutionary (historical) theory | Divine origin theory | Force theory | Social contract theory
M:thinker: Thomas Hobbes | Leviathan
M:thinker: John Locke | Two Treatises of Government
M:thinker: Jean-Jacques Rousseau | The Social Contract
M:thinker: Montesquieu | The Spirit of the Laws
S+: Hobbes argued that people surrendered all their rights to an absolute sovereign to escape the insecurity of the state of nature
S+: Locke believed in a limited government and the right of the people to resist a government that violates their natural rights
S+: Rousseau located sovereignty in the people as a whole, expressed through the general will
S+: The divine origin theory was used to justify the absolute power of kings
S+: According to the evolutionary theory, kinship, religion, property and political consciousness helped the state to grow
S+: The force theory explains the role of war and conquest in forming states, but force alone cannot keep a state together
S-: Hobbes favoured a limited government with a right to revolt | Hobbes favoured an absolute sovereign; it was Locke who supported limited government and resistance
S-: Locke wrote 'Leviathan' | Leviathan was written by Thomas Hobbes; Locke wrote Two Treatises of Government
S-: The evolutionary theory holds that the state was created suddenly by a contract | It holds that the state grew gradually over a long period
S-: Rousseau placed sovereignty in a single ruler | Rousseau placed sovereignty in the people, expressed through the general will
C: Hobbes supported an absolute sovereign | he thought that life in the state of nature was insecure and only a powerful ruler could ensure peace and order
C: The social contract theory is criticised as unhistorical | there is no historical evidence that people ever came together and signed a contract to create the state
C: The divine origin theory lost support in modern times | it justified absolute and irresponsible rule, and the growth of democracy and secular thought rejected rule by divine right
C: The evolutionary theory is considered the most satisfactory | it explains the state as the result of gradual growth through several factors rather than a single event
X: C2 D2 2 | Compare the views of Hobbes and Locke on the state of nature. | Hobbes: war of all against all, life solitary, poor, nasty, brutish and short; Locke: a state of peace and goodwill governed by natural law but lacking an impartial judge.
X: C3 D3 3 | Explain the main features of the social contract theory as given by Rousseau. | State of nature idyllic at first; growth of property and inequality; people form a contract and surrender rights to the community; general will is sovereign; popular sovereignty.
X: C4 D4 3 | Evaluate the social contract theory as an explanation of the origin of the state. | Merits: stresses consent and the people as the basis of authority, influenced democracy and revolutions; limits: unhistorical, state of nature imaginary, the state is not a voluntary club; evolutionary theory more satisfactory.
L: D4 | Discuss the social contract theories of Hobbes, Locke and Rousseau. | State of nature in each; nature and parties of the contract; resulting sovereign – absolute (Hobbes), limited government and natural rights (Locke), general will and popular sovereignty (Rousseau); criticism; contribution to democracy.
"""), ST(S + '01-st3', 'state, nation and society', """
T: nation | a people bound together by a sense of unity based on common history, culture, language or aspirations
T: society | the wider web of social relationships among people, of which the state is only one part
T: nation-state | a state whose people largely share a sense of being one nation
T: association | a group of people organised for a particular purpose, such as a trade union or a club
Q: Which of the following is primarily a psychological and cultural unity? | Nation | State | Government | Territory
Q: Which of the following is wider in scope and older in origin than the state? | Society | Government | Legislature | Constitution
Q: Membership of which of the following is compulsory for every person living in its territory? | The state | A trade union | A political party | A club
Q: Which of these is essential for a state but not for a nation? | Sovereignty | Common culture | Sense of unity | Common history
S+: A nation may exist without being a state, and one state may contain several nationalities
S+: The state is a political organisation, while the nation is a cultural and psychological unity
S+: Society existed before the state and is wider than it
S+: The state uses coercion and law, while society regulates behaviour mainly through customs and conventions
S+: Membership of the state is compulsory, whereas membership of most associations is voluntary
S-: Every nation is necessarily a sovereign state | A nation may exist without sovereignty, as many nations did under colonial rule
S-: Society and the state are identical in scope | Society is wider and older than the state
S-: Membership of the state is voluntary | Membership of the state is compulsory for those living in its territory
C: Many nations existed under colonial rule without being states | they had a common culture and sense of unity but lacked sovereignty
C: The state can punish those who break its laws but a club can only expel its members | the state alone possesses sovereignty and coercive power
C: Society is considered wider than the state | it covers all social relationships, while the state regulates only the external, political aspects of life
X: C2 D2 2 | Give two differences between state and nation. | State is political, needs sovereignty and territory; nation is cultural and psychological, may lack sovereignty; one state may have many nationalities.
X: C3 D3 3 | Distinguish between state and society. | Society older and wider; state political and sovereign; state uses coercion and law, society customs; state has definite territory, society need not; membership of state compulsory.
L: D4 | Distinguish the state from (a) the nation and (b) society, with suitable examples. | Nation – cultural unity, may lack sovereignty, one state many nations; society – wider, older, voluntary associations, customs vs law; state – sovereign, territorial, coercive, compulsory membership.
"""), ST(S + '01-st4', 'sovereignty', """
T: internal sovereignty | the supreme authority of the state over all persons and associations within its territory
T: external sovereignty | the independence of the state from control by any other state
T: monistic theory of sovereignty | the view that sovereignty is absolute, indivisible and located in a determinate authority, as stated by Austin
T: pluralistic theory of sovereignty | the view that sovereignty is shared between the state and other associations in society
T: popular sovereignty | the idea that ultimate authority rests with the people
T: legal sovereignty | the authority that makes the final law of the state, such as a sovereign parliament
Q: Who is regarded as the father of the modern theory of sovereignty? | Jean Bodin | John Austin | Harold Laski | Thomas Hobbes
Q: The monistic theory of sovereignty in its legal form is associated with: | John Austin | Harold Laski | Leon Duguit | Rousseau
Q: Which of the following thinkers is associated with the pluralistic theory of sovereignty? | Harold Laski | John Austin | Jean Bodin | Thomas Hobbes
Q: Freedom from control by any foreign power is called: | external sovereignty | internal sovereignty | legal sovereignty | popular sovereignty
Q: The idea that ultimate power rests with the people is called: | popular sovereignty | de facto sovereignty | legal sovereignty | titular sovereignty
Q: The Preamble of the Indian Constitution declares India to be a: | Sovereign Socialist Secular Democratic Republic | Socialist Unitary Republic | Federal Monarchy | Sovereign Theocratic State
S+: Internal sovereignty means the state's supremacy over all individuals and associations within its territory
S+: External sovereignty means that the state is free from the control of other states
S+: According to Austin, the sovereign is a determinate human superior who receives habitual obedience from the bulk of society and is not in the habit of obeying any other superior
S+: Pluralists argue that associations such as churches, trade unions and professional bodies also command loyalty, so sovereignty is shared
S+: Jean Bodin defined sovereignty as supreme power over citizens and subjects, unrestrained by law
S+: In India, sovereignty ultimately rests with the people, as the Preamble begins with 'We, the people of India'
S-: According to the monistic theory, sovereignty is divided among many associations | That is the pluralist view; monists hold sovereignty to be absolute and indivisible
S-: External sovereignty refers to the supremacy of the state over associations within it | That is internal sovereignty; external sovereignty is freedom from foreign control
S-: Harold Laski was a supporter of Austin's monistic theory | Laski was a leading pluralist critic of the monistic theory
C: Pluralists criticised the monistic theory of sovereignty | in modern society many associations command people's loyalty, and the state cannot be absolute over them
C: A colony is not regarded as a sovereign state | it lacks external sovereignty because it is controlled by a foreign power
C: Membership of international organisations is said to limit external sovereignty in practice | states accept obligations under treaties and international law
X: C2 D2 2 | Distinguish between internal and external sovereignty. | Internal – supremacy over all persons and associations within the state; external – independence from control by other states.
X: C3 D3 3 | State Austin's theory of sovereignty and give two criticisms of it. | Sovereign – determinate human superior, habitual obedience, not obeying another, absolute and indivisible; criticisms – ignores customs and popular will, sovereignty divided in federations, pluralist criticism.
X: C4 D4 3 | Is the monistic theory of sovereignty valid in a federal democracy like India? Give arguments. | Powers divided by the Constitution between Union and States, judicial review limits Parliament, sovereignty rests with the people; so legal sovereignty is not absolute or indivisible; yet the state remains supreme over associations.
L: D5 | Compare the monistic and pluralistic theories of sovereignty. Which is more relevant today? | Monistic – Bodin, Hobbes, Austin; absolute, indivisible, determinate; pluralistic – Laski, Figgis, Duguit; associations share loyalty; criticism of each; modern democracies, federalism, international law; balanced conclusion.
""")]

CH02 = [ST(S + '02-st1', 'forms of government', """
T: monarchy | a form of government in which supreme power is held by one person, usually by hereditary right
T: aristocracy | rule by a few persons, chosen for their ability or rank, in the interest of all
T: democracy | government in which power rests with the people, who rule directly or through elected representatives
T: unitary government | a system in which all powers are concentrated in a central government and local units derive their powers from it
T: federal government | a system in which powers are divided by the constitution between a central government and units
T: constitutional monarchy | a monarchy in which the monarch is a nominal head and real power lies with elected representatives
Q: Aristotle's classification treats tyranny as the perverted form of: | monarchy | aristocracy | democracy | oligarchy
Q: In Aristotle's classification, oligarchy is the perverted form of: | aristocracy | monarchy | polity | tyranny
Q: Which country is a classic example of a unitary state with a constitutional monarchy? | The United Kingdom | The United States of America | Switzerland | Australia
Q: Which country is the classic example of a federal government with a presidential system? | The United States of America | The United Kingdom | France | Japan
Q: Direct democracy, where citizens vote directly on laws, is practised in some cantons of: | Switzerland | India | Canada | Japan
Q: The Indian Constitution describes India as a: | Union of States | Confederation of States | Federation of Provinces | Unitary Republic
S+: In a federal system powers are divided between the centre and the units by a written constitution
S+: In a unitary system the central government may create or abolish local units
S+: The United Kingdom has a constitutional monarchy in which the monarch reigns but does not rule
S+: In a representative democracy the people govern through elected representatives
S+: Aristotle classified governments by the number of rulers and by whether they ruled for the common good
S-: In a unitary government powers are divided by the constitution between the centre and the units | That is a feature of a federal government
S-: The United States is a unitary state | The United States is a federation
S-: In a constitutional monarchy the monarch exercises real executive power | Real power lies with the elected government; the monarch is a nominal head
C: Federalism is suited to large countries with diversity | it allows regional units to manage their own affairs while the centre handles common national matters
C: A unitary government can act quickly and uniformly | power is concentrated in the central government
C: Indirect democracy is common in modern states | large populations make it impossible for all citizens to meet and decide every law directly
X: C2 D2 2 | Distinguish between unitary and federal governments. | Unitary – power concentrated in the centre, units derive power from it; federal – division of powers by a written constitution, often with a supreme judiciary.
X: C3 D3 3 | Explain Aristotle's classification of governments. | Basis – number of rulers and aim; rule of one: monarchy/tyranny; few: aristocracy/oligarchy; many: polity/democracy (perverted form).
L: D4 | Explain the different forms of government with examples. | Monarchy (absolute, constitutional – UK), aristocracy, democracy (direct – Swiss cantons; representative); unitary (UK) and federal (USA, India – 'Union of States'); merits and demerits.
"""), ST(S + '02-st2', 'parliamentary and presidential systems', """
T: parliamentary system | a system in which the executive is drawn from the legislature and remains responsible to it
T: presidential system | a system in which the executive head is elected separately for a fixed term and is not responsible to the legislature
T: collective responsibility | the principle that the Council of Ministers stands or falls together before the legislature
T: nominal executive | the head of state in whose name the government is run but who does not exercise real power
T: real executive | the body that actually exercises executive power, such as the Prime Minister and Council of Ministers
T: no-confidence motion | a motion in the legislature which, if passed, forces the government to resign in a parliamentary system
Q: Under which article is the Council of Ministers collectively responsible to the House of the People? | Article 75(3) | Article 74(1) | Article 53 | Article 368
Q: Which of the following is a feature of the presidential system? | Fixed tenure of the executive | Collective responsibility to the legislature | Dual executive | Ministers must be members of the legislature
Q: In India, the real executive power is exercised by: | the Prime Minister and the Council of Ministers | the President acting alone | the Chief Justice of India | the Speaker of the Lok Sabha
Q: In the USA, the President can be removed from office before the end of the term only by: | impeachment | a no-confidence motion | a referendum | dissolution of Congress
Q: India adopted the parliamentary system largely on the model of: | the United Kingdom | the United States | Switzerland | France
S+: In a parliamentary system there is a nominal head of state and a real executive headed by the Prime Minister
S+: In India the Council of Ministers is collectively responsible to the Lok Sabha
S+: In a presidential system the President is both head of state and head of government
S+: In the USA the members of the Cabinet are not members of Congress
S+: A parliamentary government can be removed by a vote of no confidence in the lower House
S+: The presidential system gives stability because the executive has a fixed term
S-: In the presidential system the executive is collectively responsible to the legislature | The executive has a fixed term and is not responsible to the legislature
S-: The President of India is the real executive | The President is the nominal head; real power lies with the Council of Ministers
S-: In India ministers need not be members of Parliament for any length of time | A minister who is not a member must become one within six months
C: The parliamentary system ensures responsible government | the executive must keep the confidence of the elected legislature and answer to it
C: The presidential system is said to be more stable | the President has a fixed term and cannot be removed by a vote of no confidence
C: The President of India is called a nominal executive | under Article 74 the President acts on the aid and advice of the Council of Ministers
X: C2 D2 2 | State two features of the parliamentary system. | Nominal and real executive; executive drawn from legislature; collective responsibility; Prime Minister's leadership; government removable by no-confidence.
X: C3 D3 3 | Compare the parliamentary and presidential systems on three points. | Executive drawn from vs separate from legislature; responsible vs fixed term; dual vs single executive; fusion vs separation of powers; examples India/UK vs USA.
X: C4 D4 3 | Why did the framers of the Indian Constitution prefer the parliamentary system to the presidential system? | Familiarity with British practice; responsibility preferred to stability; daily accountability through questions and motions; suited to a diverse society; avoids deadlock between executive and legislature.
L: D4 | Distinguish between the parliamentary and the presidential forms of government. Which suits India better and why? | Features of each with examples (UK/India, USA); responsibility vs stability; fusion vs separation; merits and demerits; Constituent Assembly's choice and reasons.
"""), ST(S + '02-st3', 'organs of government', """
T: legislature | the organ of government that makes laws, controls finance and holds the executive accountable
T: executive | the organ of government that implements laws and runs the administration
T: judiciary | the organ of government that interprets laws, settles disputes and protects rights
T: judicial review | the power of courts to examine the constitutional validity of laws and executive actions
T: bicameral legislature | a legislature with two houses
Q: Under Article 79, the Parliament of India consists of: | the President and the two Houses | the Lok Sabha only | the Lok Sabha and the Rajya Sabha only | the Prime Minister and the two Houses
Q: Under Article 53, the executive power of the Union is vested in the: | President | Prime Minister | Parliament | Supreme Court
Q: The Supreme Court of India is established under: | Article 124 | Article 214 | Article 79 | Article 53
Q: Which organ of government interprets the law and settles disputes? | The judiciary | The legislature | The executive | The Election Commission
Q: The Rajya Sabha is also called the: | Council of States | House of the People | Legislative Assembly | Union Cabinet
Q: Which is the main function of the legislature? | Making laws | Interpreting laws | Executing laws | Conducting elections
S+: The legislature makes laws, passes the budget and controls the executive
S+: The executive implements laws and conducts the day-to-day administration
S+: The judiciary interprets the Constitution and laws and protects the rights of citizens
S+: The Parliament of India is bicameral, consisting of the Lok Sabha and the Rajya Sabha along with the President
S+: The Indian judiciary has the power of judicial review over laws and executive actions
S-: The executive is the organ that interprets laws | Interpretation of laws is the function of the judiciary
S-: Under Article 53 the executive power of the Union is vested in the Prime Minister | It is vested in the President, who acts on ministerial advice
S-: The Parliament of India consists only of the Lok Sabha and the Rajya Sabha | Under Article 79 it also includes the President
C: The legislature is said to control the executive in India | ministers answer questions, motions are moved, and the budget needs the legislature's approval
C: An independent judiciary is essential in a democracy | it protects rights and keeps the other organs within the limits of the Constitution
C: The President is a part of Parliament in India | a Bill becomes law only after the President's assent, and the President summons and prorogues the Houses
X: C2 D2 2 | State two functions of the judiciary. | Interpreting laws and the Constitution; settling disputes; protecting rights; judicial review; advisory role.
X: C3 D3 3 | Explain three ways in which the legislature controls the executive in India. | Question Hour; motions (adjournment, no-confidence); budget and financial control; committees; debates.
L: D4 | Describe the functions of the three organs of government with reference to India. | Legislature – Article 79, law-making, budget, control of executive; executive – Article 53, President and Council of Ministers, administration, ordinances; judiciary – Article 124, interpretation, judicial review, rights, writs.
""")]

CH03 = [ST(S + '03-st1', 'the doctrine of separation of powers', """
T: separation of powers | the doctrine that the legislative, executive and judicial powers of government should be exercised by separate organs
T: tyranny | arbitrary and oppressive rule that results when all powers are concentrated in the same hands
T: checks and balances | the arrangement by which each organ of government can limit the powers of the others
Q: The doctrine of separation of powers was systematically stated by Montesquieu in: | The Spirit of the Laws | Leviathan | The Social Contract | Two Treatises of Government
Q: The book 'The Spirit of the Laws' was published in: | 1748 | 1651 | 1762 | 1789
Q: Montesquieu was a political thinker from: | France | England | Germany | the United States
Q: According to Montesquieu, the main purpose of separating powers is to protect: | liberty | the monarchy | the church | property only
Y: 1748 | the publication of Montesquieu's 'The Spirit of the Laws'
S+: Montesquieu argued that when legislative and executive powers are united in the same person there can be no liberty
S+: The doctrine aims to prevent tyranny by ensuring that no organ becomes all-powerful
S+: The doctrine has three elements: separate persons, separate functions and no control of one organ by another
S+: No modern state follows the doctrine of separation of powers in its absolute or rigid form
S-: Separation of powers was first stated by John Austin | It was systematically stated by Montesquieu in The Spirit of the Laws (1748)
S-: The doctrine means that all powers should be given to the legislature | It requires the powers to be divided among separate organs
S-: Strict separation of powers is followed in every democracy | No modern state follows it rigidly
C: Montesquieu favoured separation of powers | he believed that concentration of powers in the same hands would end liberty and lead to tyranny
C: A rigid separation of powers is not practical | the organs of government are interdependent and need to cooperate for effective government
C: The doctrine is linked with the rule of law | separate and independent organs prevent any authority from acting arbitrarily
X: C2 D2 2 | What is meant by the doctrine of separation of powers? | The three functions of government – legislative, executive and judicial – should be exercised by separate organs, none controlling another.
X: C3 D3 3 | Explain the three elements of Montesquieu's doctrine. | Same person should not form part of more than one organ; one organ should not interfere with another; one organ should not exercise the functions of another.
L: D4 | Explain the doctrine of separation of powers as given by Montesquieu. Discuss its merits and limitations. | Meaning and elements; The Spirit of the Laws 1748; liberty and prevention of tyranny; merits – efficiency, accountability, independent judiciary; limitations – rigid separation impossible, interdependence, need for checks and balances.
"""), ST(S + '03-st2', 'separation of powers in the USA and the UK', """
T: presidential veto | the power of the US President to refuse assent to a bill passed by Congress
T: impeachment | the process by which the legislature can remove the head of state or a judge for serious misconduct
T: fusion of powers | the close link between the legislature and the executive in a parliamentary system, as in the UK
Q: In which case did the US Supreme Court first assert the power of judicial review (1803)? | Marbury v Madison | Brown v Board of Education | Roe v Wade | Dred Scott v Sandford
Q: In the USA, treaties made by the President require the approval of: | two-thirds of the Senate present | the House of Representatives only | the Supreme Court | a referendum
Q: The Supreme Court of the United Kingdom was created by the: | Constitutional Reform Act 2005 | Magna Carta 1215 | Bill of Rights 1689 | Parliament Act 1911
Q: In the UK, the Prime Minister and the Cabinet are: | members of Parliament | appointed from outside Parliament only | elected separately by the people | judges of the Supreme Court
Q: Which country's constitution is said to follow separation of powers most closely? | The United States of America | The United Kingdom | India | Japan
Y: 1803 | the decision in Marbury v Madison establishing judicial review in the USA
Y: 2005 | the Constitutional Reform Act creating the Supreme Court of the United Kingdom
S+: The US Constitution vests legislative power in Congress, executive power in the President and judicial power in the Supreme Court
S+: The US President can veto a bill, but Congress can override the veto by a two-thirds majority in both Houses
S+: In the USA, appointments of judges and senior officials by the President need the consent of the Senate
S+: In the UK there is a fusion of legislative and executive powers because ministers are members of Parliament
S+: The Constitutional Reform Act 2005 separated the highest court of the UK from the House of Lords
S-: In the USA, the members of the Cabinet sit in Congress | US Cabinet members are not members of Congress
S-: The UK follows a strict separation of legislative and executive powers | The UK has a fusion of legislative and executive powers
S-: The US President cannot be removed before the end of the term | The President can be removed by impeachment
C: The US system is described as one of separation of powers with checks and balances | each organ is separate but has some power to check the others, such as the veto, Senate approval and judicial review
C: The UK system is described as a fusion of powers | the executive is drawn from Parliament and depends on its confidence
C: The Constitutional Reform Act 2005 strengthened judicial independence in the UK | it moved the highest appellate court out of the House of Lords into a separate Supreme Court
X: C2 D2 2 | Give two examples of checks and balances in the US Constitution. | Presidential veto and its override; Senate approval of appointments and treaties; impeachment; judicial review (Marbury v Madison, 1803).
X: C3 D3 3 | Why is the British system called a fusion of powers? | Ministers are members of Parliament; the Cabinet leads the legislature; the government depends on the confidence of the House of Commons; until 2009 the highest court sat in the House of Lords.
L: D4 | Compare the working of separation of powers in the USA and the UK. | USA – Articles of the Constitution, separate organs, fixed term, checks and balances (veto, Senate, impeachment, judicial review); UK – fusion of legislature and executive, parliamentary sovereignty, Constitutional Reform Act 2005, independent judiciary.
"""), ST(S + '03-st3', 'separation of powers under the Indian Constitution', """
T: basic structure doctrine | the principle that Parliament may amend the Constitution but cannot destroy its basic features
T: functional separation | the division of the main functions among the organs without a rigid wall between them
T: ordinance | a temporary law made by the President (Article 123) or a Governor (Article 213) when the legislature is not in session
Q: Which Directive Principle asks the State to separate the judiciary from the executive in the public services? | Article 50 | Article 44 | Article 39A | Article 48
Q: The basic structure doctrine was laid down in: | Kesavananda Bharati v State of Kerala (1973) | Golaknath v State of Punjab (1967) | Maneka Gandhi v Union of India (1978) | A.K. Gopalan v State of Madras (1950)
Q: In Kesavananda Bharati v State of Kerala, the Supreme Court bench consisted of: | 13 judges | 5 judges | 7 judges | 9 judges
Q: In which case did the Supreme Court apply the basic structure doctrine to strike down a constitutional amendment relating to the election of the Prime Minister? | Indira Nehru Gandhi v Raj Narain (1975) | Kesavananda Bharati v State of Kerala (1973) | Minerva Mills v Union of India (1980) | S.R. Bommai v Union of India (1994)
Q: The President of India can issue ordinances under: | Article 123 | Article 213 | Article 352 | Article 356
Q: Which body exercises the power of judicial review in India? | The Supreme Court and the High Courts | Parliament | The President | The Election Commission
Y: 1973 | the Kesavananda Bharati judgment laying down the basic structure doctrine
Y: 1975 | the Supreme Court's decision in Indira Nehru Gandhi v Raj Narain
S+: The Indian Constitution does not adopt the doctrine of separation of powers in its rigid sense but recognises a functional separation
S+: In India the executive is part of the legislature, since ministers must be members of Parliament
S+: The executive exercises legislative power through ordinances and delegated legislation
S+: The judiciary can strike down laws and executive actions that violate the Constitution
S+: Separation of powers has been recognised by the Supreme Court as part of the basic structure of the Constitution
S+: In Indira Nehru Gandhi v Raj Narain, the Court held that free and fair elections and judicial review are part of the basic structure
S-: The Indian Constitution follows a rigid separation of powers like the USA | It follows a functional separation with overlapping functions
S-: The basic structure doctrine was first laid down in Golaknath's case | It was laid down in Kesavananda Bharati v State of Kerala (1973)
S-: Parliament can amend any part of the Constitution, including its basic structure | After Kesavananda Bharati, Parliament cannot destroy the basic structure
C: The Indian system is described as having a functional separation of powers | the organs have distinct main functions, but they overlap through ordinances, delegated legislation and judicial review
C: Judicial review is regarded as a check on the legislature in India | courts can declare laws void if they violate Fundamental Rights or the basic structure
C: Indira Nehru Gandhi v Raj Narain is important for separation of powers | the Court held that Parliament could not take away the judiciary's role in deciding an election dispute
X: C2 D2 2 | Give two examples of overlap of functions between the organs of government in India. | Ordinances by President/Governor; delegated legislation by the executive; ministers as members of Parliament; judges making rules; Parliament's power of impeachment.
X: C3 D3 3 | What was decided in Kesavananda Bharati v State of Kerala (1973)? | 13-judge bench; Parliament can amend any part of the Constitution under Article 368 but cannot alter its basic structure; separation of powers, judicial review, federalism, secularism among basic features.
X: C4 D4 3 | 'The Indian Constitution has not adopted the doctrine of separation of powers in its absolute rigidity.' Examine. | Article 50; distinct functions of organs; overlaps – parliamentary executive, ordinances, delegated legislation, judicial rule-making; checks – judicial review, impeachment, accountability; basic structure protection.
L: D5 | Discuss the position of separation of powers under the Indian Constitution with reference to Kesavananda Bharati and Indira Nehru Gandhi v Raj Narain. | Functional separation; Article 50; checks and balances; overlaps; Kesavananda Bharati (1973) – basic structure; Indira Gandhi v Raj Narain (1975) – election dispute, judicial review and free and fair elections; separation of powers as basic feature.
""")]

CH04 = [ST(S + '04-st1', 'the making of the Constitution and the Preamble', """
T: Constituent Assembly | the body that framed the Constitution of India between 1946 and 1949
T: Objectives Resolution | the resolution moved by Jawaharlal Nehru in December 1946 setting out the ideals of the Constitution, which became the basis of the Preamble
T: Preamble | the introduction to the Constitution that states its source of authority, its objectives and the nature of the Indian state
T: Drafting Committee | the committee of the Constituent Assembly, chaired by Dr B.R. Ambedkar, that prepared the draft Constitution
Q: The Constituent Assembly held its first meeting on: | 9 December 1946 | 15 August 1947 | 26 November 1949 | 26 January 1950
Q: Who was elected the permanent President of the Constituent Assembly? | Dr Rajendra Prasad | Dr B.R. Ambedkar | Jawaharlal Nehru | Sardar Vallabhbhai Patel
Q: Who chaired the Drafting Committee of the Constituent Assembly? | Dr B.R. Ambedkar | Dr Rajendra Prasad | Jawaharlal Nehru | Maulana Abul Kalam Azad
Q: The Constitution of India was adopted on: | 26 November 1949 | 26 January 1950 | 15 August 1947 | 9 December 1946
Q: The Constitution of India came into force on: | 26 January 1950 | 26 November 1949 | 15 August 1947 | 26 January 1949
Q: The words 'socialist', 'secular' and 'integrity' were added to the Preamble by the: | 42nd Amendment, 1976 | 44th Amendment, 1978 | 1st Amendment, 1951 | 86th Amendment, 2002
Q: The Objectives Resolution was moved in the Constituent Assembly by: | Jawaharlal Nehru | Dr B.R. Ambedkar | Dr Rajendra Prasad | Sardar Vallabhbhai Patel
Q: In which case did the Supreme Court hold that the Preamble is a part of the Constitution? | Kesavananda Bharati v State of Kerala | Berubari Union case | Golaknath v State of Punjab | Maneka Gandhi v Union of India
Y: 1946 | the first meeting of the Constituent Assembly
Y: 1949 | the adoption of the Constitution of India by the Constituent Assembly
Y: 1950 | the Constitution of India coming into force
Y: 1976 | the addition of 'socialist', 'secular' and 'integrity' to the Preamble
S+: The Preamble begins with the words 'We, the people of India', showing that the people are the source of authority
S+: The Preamble declares India to be a Sovereign Socialist Secular Democratic Republic
S+: The Preamble aims to secure justice, liberty, equality and fraternity for all citizens
S+: The Constitution was adopted on 26 November 1949 and came into force on 26 January 1950
S+: Dr B.R. Ambedkar chaired the Drafting Committee of the Constituent Assembly
S+: The Preamble has been amended only once, by the 42nd Amendment in 1976
S-: The Constitution came into force on 26 November 1949 | It was adopted on 26 November 1949 and came into force on 26 January 1950
S-: The word 'secular' was part of the Preamble from 1950 | It was added by the 42nd Amendment in 1976
S-: Jawaharlal Nehru was the President of the Constituent Assembly | Dr Rajendra Prasad was its President
S-: The Supreme Court has held that the Preamble can never be considered part of the Constitution | In Kesavananda Bharati the Court held that the Preamble is part of the Constitution
C: The Preamble is called the key to the Constitution | it states the objectives and philosophy that guide the interpretation of the Constitution
C: 26 January 1950 was chosen as the date of commencement | on 26 January 1930 the Indian National Congress had resolved for Purna Swaraj
C: The Preamble shows that the people of India are the source of the Constitution's authority | it begins with 'We, the people of India … give to ourselves this Constitution'
X: C2 D2 2 | Name the four objectives that the Preamble aims to secure for all citizens. | Justice (social, economic and political); liberty of thought, expression, belief, faith and worship; equality of status and opportunity; fraternity assuring the dignity of the individual and the unity and integrity of the Nation.
X: C3 D3 3 | Explain the meaning of 'Sovereign', 'Secular' and 'Republic' as used in the Preamble. | Sovereign – free from external control, independent; Secular – no state religion, equal respect for all religions; Republic – elected head of state, no hereditary ruler.
L: D4 | Describe the making of the Indian Constitution and explain the significance of the Preamble. | Constituent Assembly (first met 9 Dec 1946), Objectives Resolution, Rajendra Prasad, Ambedkar and Drafting Committee; adopted 26 Nov 1949, in force 26 Jan 1950; Preamble – source, nature of state, objectives; 42nd Amendment; Kesavananda Bharati on its status.
"""), ST(S + '04-st2', 'salient features of the Indian Constitution', """
T: written constitution | a constitution contained in a single formal document
T: federal system with a unitary bias | a federation in which the Union is given more powers, especially in emergencies, than the States
T: secularism | the principle that the State has no religion of its own and treats all religions equally
T: universal adult franchise | the right of every adult citizen to vote without discrimination of caste, religion, sex or property
T: single citizenship | the system in which all Indians are citizens of India only and not of separate States
T: independent judiciary | a judiciary free from the control of the legislature and the executive
Q: At the time of its adoption, the Constitution of India had: | 395 articles, 22 parts and 8 schedules | 448 articles, 25 parts and 12 schedules | 300 articles and 10 schedules | 250 articles and 5 schedules
Q: The division of legislative powers between the Union and the States is given in the: | Seventh Schedule | First Schedule | Tenth Schedule | Eighth Schedule
Q: Residuary powers of legislation in India belong to: | Parliament | the State Legislatures | both equally | the President alone
Q: The voting age in India was reduced from 21 to 18 years by the: | 61st Amendment | 42nd Amendment | 44th Amendment | 73rd Amendment
Q: Which of the following is a unitary feature of the Indian Constitution? | Single citizenship | Division of powers | Written constitution | Bicameral legislature
Q: Which of the following is a federal feature of the Indian Constitution? | Division of powers between the Union and the States | Single citizenship | All-India services | Emergency provisions
S+: The Constitution of India is the lengthiest written constitution in the world
S+: The Seventh Schedule contains the Union List, the State List and the Concurrent List
S+: India has a single integrated judiciary with the Supreme Court at the top
S+: During a national emergency the federal structure can work like a unitary one
S+: The Constitution is partly rigid and partly flexible, since some provisions can be amended by a simple majority and others need special procedures
S+: India has universal adult franchise, giving every citizen of 18 years and above the right to vote
S-: India has dual citizenship – of the Union and of the States | India has single citizenship
S-: Residuary powers in India belong to the States | Residuary powers belong to Parliament (Article 248)
S-: The Constitution of India is unwritten like that of the UK | India has a written constitution
S-: India has separate Supreme Courts for each State | India has one integrated judiciary with the Supreme Court at the top and High Courts in the States
C: The Indian federation is said to have a unitary bias | the Union has more powers, residuary powers, emergency powers, single citizenship and all-India services
C: The Indian Constitution is very lengthy | it covers the structure of both the Union and the States, Fundamental Rights, Directive Principles and many detailed provisions for a diverse country
C: India is described as a secular state | the State has no official religion and guarantees freedom of religion to all
X: C2 D2 2 | State any two unitary features of the Indian Constitution. | Single citizenship; strong centre and residuary powers; emergency provisions; all-India services; integrated judiciary; Parliament's power to change State boundaries (Article 3).
X: C3 D3 3 | Explain why the Indian Constitution is called partly rigid and partly flexible. | Some provisions amended by simple majority; others by special majority under Article 368; federal provisions also need ratification by half the States.
X: C4 D4 3 | 'India is a quasi-federal state.' Examine this statement. | Federal features – division of powers, written constitution, independent judiciary, bicameralism; unitary features – strong centre, single citizenship, emergencies, Governors, all-India services; Union of States; cooperative federalism.
L: D4 | Explain any five salient features of the Indian Constitution. | Lengthy written constitution (395 articles originally); federal with unitary bias; parliamentary government; secularism; Fundamental Rights and Directive Principles; independent judiciary and judicial review; universal adult franchise; single citizenship; rigid and flexible.
"""), ST(S + '04-st3', 'Fundamental Rights and constitutional remedies', """
T: Fundamental Rights | the basic rights guaranteed in Part III of the Constitution that are enforceable by courts
T: writ | a formal written order of a court commanding a person or authority to do or not to do something
T: habeas corpus | the writ by which a court orders a person who has been detained to be produced before it, to examine whether the detention is legal
T: mandamus | the writ by which a court commands a public authority to perform a public duty
T: certiorari | the writ by which a higher court quashes the order of a lower court or tribunal made without or in excess of jurisdiction
T: quo warranto | the writ by which a court asks a person by what authority he holds a public office
T: prohibition | the writ by which a higher court stops a lower court or tribunal from continuing a case beyond its jurisdiction
Q: Fundamental Rights are contained in which part of the Constitution? | Part III | Part IV | Part IVA | Part V
Q: Which article was described by Dr B.R. Ambedkar as the 'heart and soul' of the Constitution? | Article 32 | Article 14 | Article 21 | Article 19
Q: The right to property was removed from the list of Fundamental Rights by the: | 44th Amendment, 1978 | 42nd Amendment, 1976 | 1st Amendment, 1951 | 86th Amendment, 2002
Q: The right to education (Article 21A) was inserted by the: | 86th Amendment, 2002 | 42nd Amendment, 1976 | 44th Amendment, 1978 | 73rd Amendment, 1992
Q: Untouchability is abolished by: | Article 17 | Article 14 | Article 21 | Article 25
Q: Which article protects life and personal liberty? | Article 21 | Article 19 | Article 22 | Article 32
Q: Which writ is issued to release a person who has been illegally detained? | Habeas corpus | Mandamus | Quo warranto | Certiorari
Q: In which case did the Supreme Court hold that the procedure for depriving a person of life or liberty must be just, fair and reasonable? | Maneka Gandhi v Union of India (1978) | A.K. Gopalan v State of Madras (1950) | Kesavananda Bharati v State of Kerala (1973) | Shankari Prasad v Union of India (1951)
Q: High Courts can issue writs under: | Article 226 | Article 32 | Article 141 | Article 368
M:right: Right to equality | Articles 14 to 18
M:right: Right to freedom | Articles 19 to 22
M:right: Right against exploitation | Articles 23 and 24
M:right: Right to freedom of religion | Articles 25 to 28
M:right: Cultural and educational rights | Articles 29 and 30
M:right: Right to constitutional remedies | Article 32
M:writ: habeas corpus | produce the detained person before the court
M:writ: mandamus | command a public authority to perform its public duty
M:writ: quo warranto | ask by what authority a person holds a public office
M:writ: certiorari | quash an order passed without or in excess of jurisdiction
M:writ: prohibition | stop a lower court from exceeding its jurisdiction
S+: Fundamental Rights are justiciable, meaning a person can go to court if they are violated
S+: Under Article 32 a person can directly approach the Supreme Court for the enforcement of Fundamental Rights
S+: The jurisdiction of High Courts under Article 226 is wider than that of the Supreme Court under Article 32, as High Courts can issue writs for other purposes also
S+: Fundamental Rights are not absolute; reasonable restrictions can be placed on many of them
S+: Article 24 prohibits the employment of children below fourteen years in factories, mines or other hazardous employment
S+: After the 44th Amendment, the right to property is a constitutional right under Article 300A
S-: Fundamental Rights are contained in Part IV of the Constitution | They are in Part III; Part IV contains the Directive Principles
S-: Mandamus is issued to release a person from illegal detention | That is habeas corpus; mandamus commands performance of a public duty
S-: The right to property is still a Fundamental Right | It was removed by the 44th Amendment (1978) and is now a constitutional right under Article 300A
S-: Only the Supreme Court can issue writs in India | High Courts can also issue writs under Article 226
C: Article 32 is called the heart and soul of the Constitution | it makes Fundamental Rights real by giving a guaranteed remedy before the Supreme Court
C: Fundamental Rights are subject to reasonable restrictions | individual freedom has to be balanced with public order, morality, security of the State and the rights of others
C: Maneka Gandhi v Union of India widened Article 21 | the Court held that any procedure depriving a person of liberty must be just, fair and reasonable, not arbitrary
X: C2 D2 2 | Name any four writs that the Supreme Court can issue. | Habeas corpus, mandamus, prohibition, certiorari, quo warranto (any four).
X: C3 D3 3 | Distinguish between the writ jurisdiction of the Supreme Court and that of the High Courts. | SC under Article 32 – only for Fundamental Rights, itself a Fundamental Right; HCs under Article 226 – for Fundamental Rights and for any other purpose, wider in scope; territorial limits.
X: C4 D4 3 | Explain the significance of Maneka Gandhi v Union of India (1978) for Article 21. | Passport impounded; Court held procedure must be just, fair and reasonable; linked Articles 14, 19 and 21; overturned narrow view of A.K. Gopalan; led to wide interpretation of life and liberty.
L: D4 | Explain the Fundamental Rights guaranteed by the Constitution and the remedies available for their violation. | Six groups with articles (14–18, 19–22, 23–24, 25–28, 29–30, 32); justiciable, reasonable restrictions; 44th and 86th Amendments; writs and their uses; Articles 32 and 226; Maneka Gandhi.
"""), ST(S + '04-st4', 'Directive Principles of State Policy and Fundamental Duties', """
T: Directive Principles of State Policy | the guidelines in Part IV of the Constitution that the State must apply in making laws, though they are not enforceable by courts
T: Fundamental Duties | the duties of citizens listed in Article 51A, added by the 42nd Amendment
T: non-justiciable | not enforceable in a court of law
T: welfare state | a state that works actively to promote the economic and social well-being of its people
Q: The Directive Principles of State Policy are contained in: | Part IV (Articles 36 to 51) | Part III (Articles 12 to 35) | Part IVA (Article 51A) | Part V
Q: The idea of Directive Principles was borrowed from the Constitution of: | Ireland | the USA | the USSR | Canada
Q: Fundamental Duties were added to the Constitution by the: | 42nd Amendment, 1976 | 44th Amendment, 1978 | 86th Amendment, 2002 | 1st Amendment, 1951
Q: Fundamental Duties were added on the recommendation of the: | Swaran Singh Committee | Sarkaria Commission | Kothari Commission | Mandal Commission
Q: Which article directs the State to endeavour to secure a Uniform Civil Code? | Article 44 | Article 40 | Article 45 | Article 50
Q: Which article directs the State to organise village panchayats? | Article 40 | Article 44 | Article 48 | Article 51
Q: Equal justice and free legal aid are provided for in: | Article 39A | Article 21A | Article 14 | Article 51A
Q: The duty of parents or guardians to provide opportunities for education to their child aged 6 to 14 years was added by the: | 86th Amendment, 2002 | 42nd Amendment, 1976 | 44th Amendment, 1978 | 61st Amendment, 1988
M:article: Article 40 | organisation of village panchayats
M:article: Article 44 | Uniform Civil Code
M:article: Article 39A | equal justice and free legal aid
M:article: Article 50 | separation of judiciary from executive
M:article: Article 51 | promotion of international peace and security
M:article: Article 51A | Fundamental Duties of citizens
S+: Article 37 declares that the Directive Principles are not enforceable by any court but are fundamental in the governance of the country
S+: The Directive Principles aim at establishing a welfare state and social and economic democracy
S+: Fundamental Duties are contained in Part IVA, Article 51A
S+: There are now eleven Fundamental Duties; the eleventh was added by the 86th Amendment in 2002
S+: Respecting the Constitution, the National Flag and the National Anthem is a Fundamental Duty
S+: In Minerva Mills v Union of India (1980) the Supreme Court held that the balance between Fundamental Rights and Directive Principles is part of the basic structure
S-: Directive Principles can be enforced in a court of law | Article 37 makes them non-justiciable
S-: Fundamental Duties were part of the original Constitution of 1950 | They were added by the 42nd Amendment in 1976
S-: Article 40 deals with the Uniform Civil Code | Article 40 deals with village panchayats; Article 44 deals with the Uniform Civil Code
S-: There are ten Fundamental Duties at present | There are eleven; the eleventh was added in 2002
C: Directive Principles are made non-justiciable | the newly independent State did not have enough resources to implement all of them immediately
C: Directive Principles are still important even though courts cannot enforce them | they are fundamental in governance and guide the legislature and executive in making policies and laws
C: Fundamental Duties were added to the Constitution | rights must be balanced with duties so that citizens also contribute to the nation
X: C2 D2 2 | Give two differences between Fundamental Rights and Directive Principles. | FRs justiciable, DPSPs not (Article 37); FRs negative restrictions on the State, DPSPs positive directions; FRs aim at political democracy, DPSPs at social and economic democracy.
X: C3 D3 3 | Explain any three Directive Principles with their articles. | Article 39A free legal aid; Article 40 village panchayats; Article 44 Uniform Civil Code; Article 45 early childhood care; Article 48 agriculture and animal husbandry; Article 50 separation of judiciary; Article 51 international peace.
L: D4 | Discuss the nature and importance of the Directive Principles of State Policy and Fundamental Duties. | Part IV, Irish origin, Article 37 non-justiciable, welfare state, examples; relation with FRs, Minerva Mills balance; Part IVA, Article 51A, 42nd Amendment, Swaran Singh Committee, eleven duties, 86th Amendment.
"""), ST(S + '04-st5', 'amendment of the Constitution', """
T: amendment | a formal change in the text of the Constitution
T: special majority | a majority of the total membership of a House and at least two-thirds of the members present and voting
T: ratification by States | approval of an amendment by the legislatures of at least half of the States, needed for amendments affecting the federal structure
Q: The procedure for amendment of the Constitution is given in: | Article 368 | Article 356 | Article 352 | Article 123
Q: An amendment that affects the representation of States in Parliament requires: | special majority in Parliament and ratification by at least half of the State Legislatures | a simple majority in Parliament | a referendum of the people | the approval of the Supreme Court
Q: Which amendment made it obligatory for the President to give assent to a Constitution Amendment Bill? | 24th Amendment, 1971 | 42nd Amendment, 1976 | 44th Amendment, 1978 | 1st Amendment, 1951
Q: In which case did the Supreme Court hold that Parliament could not amend Fundamental Rights (later overruled)? | Golaknath v State of Punjab (1967) | Shankari Prasad v Union of India (1951) | Kesavananda Bharati v State of Kerala (1973) | Minerva Mills v Union of India (1980)
Q: A Constitution Amendment Bill can be introduced in: | either House of Parliament | the Lok Sabha only | the Rajya Sabha only | a State Legislature
Q: In case of a deadlock over a Constitution Amendment Bill between the two Houses: | there is no provision for a joint sitting | a joint sitting is held | the President decides | the Supreme Court decides
Y: 1967 | the Golaknath judgment on the amendment of Fundamental Rights
Y: 1971 | the 24th Amendment affirming Parliament's power to amend any part of the Constitution
S+: Some provisions, such as the formation of new States under Article 3, can be changed by a simple majority and are not deemed amendments under Article 368
S+: Most amendments need a special majority in each House of Parliament
S+: Amendments affecting the federal structure also need ratification by the legislatures of at least half of the States
S+: After Kesavananda Bharati, Parliament can amend any part of the Constitution but cannot destroy its basic structure
S+: There is no provision for a joint sitting of the two Houses on a Constitution Amendment Bill
S-: A Constitution Amendment Bill can be introduced only in the Lok Sabha | It can be introduced in either House of Parliament
S-: The President can withhold assent from a Constitution Amendment Bill | After the 24th Amendment the President must give assent
S-: Every amendment needs ratification by all the States | Only amendments affecting federal provisions need ratification by at least half of the States
S-: Golaknath's case is still the law on amending Fundamental Rights | It was overruled in Kesavananda Bharati (1973)
C: The amendment procedure in India is described as a blend of rigidity and flexibility | some provisions need only a simple majority, others a special majority, and federal provisions also need ratification by States
C: Ratification by States is required for some amendments | these provisions affect the federal structure and the interests of the States
C: The basic structure doctrine limits the amending power | the Supreme Court held that the power to amend does not include the power to destroy the Constitution's essential features
X: C2 D2 2 | What is meant by special majority under Article 368? | Majority of the total membership of each House and not less than two-thirds of members present and voting.
X: C3 D3 3 | Explain the three methods of amending the Indian Constitution. | Simple majority (outside Article 368, e.g. Article 3); special majority under Article 368; special majority plus ratification by half the State Legislatures for federal provisions.
X: C4 D4 3 | Trace the debate on Parliament's power to amend Fundamental Rights from Shankari Prasad to Kesavananda Bharati. | Shankari Prasad 1951 – amendment allowed; Golaknath 1967 – FRs cannot be amended; 24th Amendment 1971; Kesavananda Bharati 1973 – power to amend but not the basic structure; Minerva Mills 1980.
L: D4 | Explain the procedure for amendment of the Indian Constitution under Article 368. Discuss the limits on the amending power. | Introduction in either House, special majority, no joint sitting, ratification for federal provisions, President's assent (24th Amendment); simple majority provisions; limits – basic structure (Kesavananda Bharati), Minerva Mills.
""")]

CH05 = [ST(S + '05-st1', 'meaning of law, morality and justice', """
T: law | a body of rules of conduct recognised and enforced by the State, with a sanction for their breach
T: sanction | the penalty or consequence that follows the breach of a law
T: morality | principles of right and wrong conduct based on conscience, religion or social values, not enforced by the State
T: justice | giving every person their due; fairness in the making and applying of laws
Q: Who defined law as 'the body of principles recognised and applied by the State in the administration of justice'? | Salmond | Austin | Savigny | Roscoe Pound
Q: Who defined law as the command of the sovereign backed by a sanction? | John Austin | Salmond | Savigny | Henry Maine
Q: Which of the following is enforced by the State? | Law | Morality | Etiquette | Fashion
Q: Laws are concerned mainly with: | external conduct of persons | inner thoughts and motives only | religious beliefs only | personal tastes
S+: Laws are enforced by the State through courts and sanctions, while morals are enforced by conscience and social pressure
S+: Law regulates mainly external conduct, while morality also concerns inner motives
S+: Many legal rules, such as those against murder and theft, also have a moral basis
S+: The aim of law is to secure justice in society
S+: An immoral act is not necessarily illegal, and an illegal act need not be immoral
S-: Every moral rule is also a law | Many moral rules, such as telling the truth in daily life, are not enforced as law
S-: Morality is enforced by courts through punishment | Morality is enforced by conscience and social disapproval, not by courts
S-: Law and justice always mean the same thing | Justice is an ideal; a particular law may sometimes be unjust and need reform
C: Law and morality are closely related | many laws are based on moral values, and morality influences the making and reform of laws
C: Laws must be backed by sanctions | without the threat of a penalty, people may not obey rules that go against their interests
C: Unjust laws are reformed or struck down in a democracy | the aim of law is justice, and courts and legislatures correct laws that are unfair
X: C2 D2 2 | Give two differences between law and morality. | Law enforced by State with sanctions, morality by conscience/society; law governs external acts, morality also motives; law is definite and uniform, morality varies.
X: C3 D3 3 | Explain the relationship between law and justice. | Justice is the aim of law; laws are the means; unjust laws reformed; courts interpret in light of justice, equity and good conscience; Preamble's ideal of justice.
L: D4 | Define law and explain its relationship with morality and justice. | Definitions – Austin, Salmond; features – rules, State, sanction; law and morality – similarities and differences, examples; law and justice – aim, reform, Preamble.
"""), ST(S + '05-st2', 'schools of jurisprudence', """
T: natural law school | the school that holds that law is based on reason and universal moral principles higher than man-made law
T: positivist (analytical) school | the school that studies law as it is, as laid down by the sovereign, separate from morality
T: historical school | the school that holds that law grows from the customs and spirit of the people
T: sociological school | the school that studies law in relation to society and its role in balancing social interests
T: Volksgeist | Savigny's term for the common spirit or consciousness of a people, from which law develops
T: social engineering | Roscoe Pound's idea that law is a tool for balancing competing interests in society
Q: The command theory of law is associated with: | John Austin | Savigny | Roscoe Pound | Thomas Aquinas
Q: The concept of 'Volksgeist' was given by: | Savigny | Austin | Bentham | Kelsen
Q: 'The movement of progressive societies has hitherto been a movement from status to contract' – who said this? | Henry Maine | John Austin | Roscoe Pound | Hans Kelsen
Q: The idea of law as 'social engineering' is associated with: | Roscoe Pound | Savigny | Austin | Henry Maine
Q: The 'Pure Theory of Law' with the idea of a Grundnorm was given by: | Hans Kelsen | H.L.A. Hart | Savigny | Roscoe Pound
Q: Which school holds that an unjust law is not a true law? | Natural law school | Positivist school | Historical school | Realist school
M:jurist: John Austin | command theory of law
M:jurist: Savigny | Volksgeist
M:jurist: Roscoe Pound | social engineering
M:jurist: Hans Kelsen | Grundnorm
M:jurist: Henry Maine | status to contract
S+: Natural law thinkers believe that there are universal principles of justice that man-made laws should follow
S+: Austin defined law as a command of the sovereign enforced by a sanction
S+: Savigny believed that law is found and not made, as it grows from the spirit of the people
S+: The sociological school sees law as a means of balancing competing interests in society
S+: Positivists separate law as it is from law as it ought to be
S-: Austin was the founder of the historical school | Austin belonged to the analytical (positivist) school; Savigny is linked with the historical school
S-: Savigny held that law is consciously made by the legislature | He held that law is found in the people's spirit, not made
S-: Roscoe Pound gave the command theory of law | The command theory is Austin's; Pound is known for social engineering
C: The positivist school is criticised for ignoring morality | it treats any command of the sovereign as law even if it is unjust
C: Savigny opposed hasty codification of law | he believed that law grows slowly from the customs and spirit of the people
C: The sociological school became influential in modern welfare states | it treats law as a tool to meet social needs and balance interests
X: C2 D2 2 | State the main idea of the historical school of jurisprudence. | Law grows from the customs and Volksgeist of the people; it is found, not made (Savigny); Henry Maine – status to contract.
X: C3 D3 3 | Explain Austin's command theory and give two criticisms. | Law is a command of the sovereign backed by sanction; criticisms – ignores customs and international law, does not fit constitutional limits on sovereigns, ignores morality and permissive laws.
X: C4 D4 3 | Which school of jurisprudence best explains the role of public interest litigation in India? Give reasons. | Sociological school – law as social engineering, courts balancing interests; also natural law ideas of justice; positivism less suitable.
L: D4 | Explain the natural law, positivist, historical and sociological schools of jurisprudence. | Natural law – reason, higher law; positivist – Austin, Kelsen, separation of law and morals; historical – Savigny, Volksgeist, Maine; sociological – Pound, social engineering; evaluation.
"""), ST(S + '05-st3', 'purpose and functions of law', """
T: social control | the regulation of individual behaviour in society to maintain order
T: rule of law | the principle that everyone, including the government, is subject to the law, and no one is above it
T: dispute resolution | the settlement of conflicts between persons or groups through courts and other legal processes
Q: Which of the following is a primary function of law in society? | Maintaining order and resolving disputes | Promoting a particular religion | Fixing the prices of all goods | Deciding people's personal tastes
Q: The principle that no one is above the law is called the: | rule of law | doctrine of precedent | separation of powers | doctrine of equity
Q: Laws against untouchability and dowry are examples of law used as an instrument of: | social change | punishment only | foreign policy | taxation
S+: Law maintains order by laying down rules of conduct and penalties for their breach
S+: Law protects the rights and liberties of individuals
S+: Law provides peaceful methods for settling disputes
S+: Law can be an instrument of social change, as in the abolition of untouchability under Article 17
S+: The rule of law means that the government also acts according to law
S-: The only function of law is to punish criminals | Law also protects rights, resolves disputes and brings about social change
S-: Under the rule of law, ministers are above the law | Under the rule of law, everyone including the government is subject to law
C: Law is necessary in society | without rules and sanctions there would be disorder and conflict
C: Law is described as an instrument of social change | legislation such as the abolition of untouchability and dowry prohibition changes harmful social practices
C: The rule of law protects citizens from arbitrary government | the government can act only according to law and courts can review its actions
X: C2 D2 2 | Mention any two functions of law in society. | Maintaining order; protecting rights; settling disputes; bringing social change; securing justice.
X: C3 D3 3 | Explain how law acts as an instrument of social change with two Indian examples. | Article 17 abolishing untouchability; Dowry Prohibition Act 1961; Prohibition of Child Marriage Act 2006; RTE Act 2009; changes behaviour and attitudes.
L: D4 | Discuss the purposes and functions of law in a democratic society. | Order, rights, justice, dispute resolution, social control, social change, rule of law; examples from Indian laws.
""")]

CH06 = [ST(S + '06-st1', 'public, private, substantive and procedural law', """
T: public law | law governing the relationship between the State and individuals, such as constitutional, administrative and criminal law
T: private law | law governing relationships between private persons, such as the law of contract, property and family
T: substantive law | law that defines rights and duties, such as the law of contract or the law of crimes
T: procedural law | law that lays down the procedure for enforcing rights and duties in courts
Q: Which of the following is an example of procedural law? | The Code of Civil Procedure, 1908 | The Indian Contract Act, 1872 | The Transfer of Property Act, 1882 | The Hindu Marriage Act, 1955
Q: Which of the following is an example of substantive law? | The Indian Contract Act, 1872 | The Code of Civil Procedure, 1908 | The Limitation Act, 1963 | The Bharatiya Nagarik Suraksha Sanhita, 2023
Q: Constitutional law and administrative law are branches of: | public law | private law | equity | customary law
Q: The law of contract is a branch of: | private law | public law | international law | constitutional law
Q: The Bharatiya Nyaya Sanhita, 2023, which replaced the Indian Penal Code, 1860, is an example of: | substantive criminal law | procedural civil law | international law | private law
Q: The Bharatiya Sakshya Adhiniyam, 2023, which replaced the Indian Evidence Act, 1872, deals with: | rules of evidence | the law of contract | the law of marriage | taxation
S+: Public law deals with matters in which the State is directly concerned
S+: Private law deals with the rights and duties of individuals towards one another
S+: Substantive law tells us what our rights and duties are, while procedural law tells us how to enforce them
S+: Criminal law is a part of public law because a crime is treated as a wrong against society
S+: The Code of Civil Procedure, 1908 lays down the procedure for civil suits
S-: The Code of Civil Procedure is a substantive law | It is a procedural law
S-: Criminal law is a branch of private law | Criminal law is part of public law
S-: The law of contract is part of public law | It is part of private law
C: Criminal law is classified as public law | crimes are regarded as wrongs against society, and the State prosecutes the offender
C: Procedural law is as important as substantive law | rights have little value unless there is a procedure to enforce them in courts
C: The law of contract is part of private law | it deals with agreements and obligations between private persons
X: C2 D2 2 | Distinguish between substantive law and procedural law with one example each. | Substantive defines rights and duties (Indian Contract Act 1872); procedural lays down methods of enforcement (Code of Civil Procedure 1908).
X: C3 D3 3 | Explain the difference between public law and private law with examples. | Public – State and individual: constitutional, administrative, criminal; private – between individuals: contract, property, family, torts; State as a party vs private parties.
L: D4 | Explain the classification of law into public and private law and into substantive and procedural law, with examples. | Definitions; examples – Constitution, administrative law, criminal law (BNS 2023); contract (1872), property (1882), family laws; procedural – CPC 1908, BNSS 2023, BSA 2023; significance.
"""), ST(S + '06-st2', 'civil and criminal law', """
T: civil law | the law dealing with disputes between private parties about rights, such as property, contract and family matters
T: criminal law | the law dealing with offences against society, which are punished by the State
T: plaintiff | the person who files a civil suit
T: accused | the person charged with committing an offence
T: damages | money compensation awarded by a court for a civil wrong
Q: In a civil case, the person who files the suit is called the: | plaintiff | accused | prosecutor | respondent in a criminal appeal
Q: Criminal cases are usually filed in the name of: | the State | the victim's family only | the accused | the judge
Q: The standard of proof in a criminal case is: | proof beyond reasonable doubt | preponderance of probabilities | prima facie evidence only | the plaintiff's statement
Q: Which of the following is a typical remedy in a civil case? | Damages or injunction | Imprisonment | Death penalty | Fine paid to the State only
Q: A dispute about the breach of a sale agreement for a flat is a: | civil matter | criminal matter | constitutional matter only | international dispute
S+: In civil cases the aim is to restore the rights of the aggrieved party, usually through damages, injunction or specific performance
S+: In criminal cases the aim is to punish the offender through imprisonment, fine or other punishment
S+: A criminal case is prosecuted by the State because a crime is regarded as a wrong against society
S+: The standard of proof is higher in criminal cases (beyond reasonable doubt) than in civil cases (preponderance of probabilities)
S+: The same act, such as a road accident caused by rash driving, can give rise to both civil and criminal proceedings
S-: In a criminal case the person who files the case is called the plaintiff | In a civil case the party is the plaintiff; in a criminal case the State prosecutes the accused
S-: Imprisonment is a normal remedy in civil cases | Civil remedies are damages, injunction, specific performance and the like; imprisonment is a criminal punishment
S-: The standard of proof is the same in civil and criminal cases | Criminal cases need proof beyond reasonable doubt; civil cases need a preponderance of probabilities
C: Criminal cases require proof beyond reasonable doubt | conviction can take away a person's liberty, so the law guards strongly against punishing the innocent
C: The State is a party in every criminal case | the prosecution is conducted in the name of the State by a public prosecutor, since the whole community is harmed by a crime
C: A road accident can lead to both a civil and a criminal case | the driver may be punished for rash driving and may also have to pay compensation to the victim
X: C2 D2 2 | Give two differences between civil and criminal law. | Nature (private wrong vs offence against society); parties (plaintiff/defendant vs State/accused); remedy (compensation vs punishment); standard of proof.
X: C3 D3 3 | Explain, with an example, how the same act can lead to both civil and criminal liability. | Rash driving causing injury – criminal prosecution by the State for the offence and a civil claim for compensation by the victim; different aims, procedures and standards of proof.
L: D4 | Distinguish between civil law and criminal law on the basis of nature, parties, procedure, standard of proof and remedies, with examples. | Civil – private disputes, plaintiff v defendant, suit, preponderance, damages/injunction; criminal – offences, State v accused, FIR and trial, beyond reasonable doubt, punishment; examples.
"""), ST(S + '06-st3', 'municipal and international law; constitutional and statutory law', """
T: municipal law | the national or domestic law of a state that applies within its territory
T: international law | the body of rules that governs relations between states and international organisations
T: constitutional law | the supreme law that lays down the structure and powers of the organs of government and the rights of citizens
T: statutory law | law made by a legislature in the form of Acts
T: treaty | a written agreement between states that is binding under international law
Q: Which article of the Constitution asks the State to foster respect for international law and treaty obligations? | Article 51 | Article 44 | Article 21 | Article 368
Q: Parliament can make laws to implement international treaties and agreements under: | Article 253 | Article 123 | Article 32 | Article 50
Q: An Act passed by Parliament is an example of: | statutory law | constitutional law | international law | customary international law
Q: Which law is supreme in India? | The Constitution of India | Acts of Parliament | State laws | International treaties
Q: The Indian Contract Act, 1872 is an example of: | municipal (national) law | international law | constitutional law | canon law
S+: Municipal law is enforced by the courts and the government of a state within its territory
S+: International law governs relations among states and is based on treaties, customs and general principles
S+: The Constitution is the supreme law in India, and any law inconsistent with it can be declared void
S+: Statutory law is made by Parliament or State Legislatures within the limits of the Constitution
S+: In Vishaka v State of Rajasthan (1997) the Supreme Court relied on an international convention to frame guidelines where there was no domestic law
S-: International law is enforced in the same way as municipal law by a world police | International law lacks a central enforcing authority like a national government
S-: An ordinary Act of Parliament is superior to the Constitution | The Constitution is supreme; Acts must conform to it
S-: Article 253 deals with the amendment of the Constitution | Article 253 gives Parliament power to implement treaties; amendment is under Article 368
C: International law is sometimes called weak law | there is no central legislature or police to enforce it, and it depends largely on the consent of states
C: Statutory laws must conform to the Constitution | the Constitution is the supreme law and courts can strike down laws that violate it
C: Indian courts have used international conventions in some cases | where there is no domestic law, conventions consistent with Fundamental Rights can be read into them, as in Vishaka
X: C2 D2 2 | Distinguish between municipal law and international law. | Municipal – within a state, made and enforced by its organs; international – between states, based on treaties and customs, lacks central enforcement.
X: C3 D3 3 | Explain the difference between constitutional law and statutory law. | Constitutional – supreme, structure of government and rights, special amendment procedure; statutory – Acts of legislatures, ordinary procedure, subordinate to the Constitution, can be struck down.
L: D4 | Explain municipal and international law, and constitutional and statutory law, with Indian examples. | Definitions; Articles 51 and 253; Vishaka (1997); Constitution as supreme law; Acts as statutory law; judicial review.
"""), ST(S + '06-st4', 'common law and equity', """
T: common law | the body of law developed in England by the decisions of royal courts and applied uniformly across the country
T: equity | rules developed by the Court of Chancery to give justice where the common law was rigid or gave no remedy
T: injunction | an equitable remedy by which a court orders a person to do or not to do a particular act
T: specific performance | an equitable remedy by which a court orders a party to perform the contract itself rather than pay damages
T: trust | an equitable arrangement in which property is held by one person for the benefit of another
Q: Equity was developed in England by the: | Court of Chancery | Court of King's Bench | House of Commons | Privy Council
Q: Which maxim of equity means that a person seeking relief must have behaved fairly? | He who comes into equity must come with clean hands | Equity follows the law | Delay defeats equity | Equity acts in personam
Q: Which of the following is an equitable remedy? | Injunction | Imprisonment | Fine | Death penalty
Q: In India, equitable remedies like specific performance and injunctions are mainly provided by the: | Specific Relief Act, 1963 | Indian Contract Act, 1872 | Code of Civil Procedure, 1908 | Indian Trusts Act, 1882
Q: The maxim 'delay defeats equity' means that: | a person who sleeps over his rights may lose the equitable remedy | equity always prefers delay | delay is a crime | equity cannot be delayed
S+: The common law was developed by judges through decisions in individual cases
S+: Equity grew because the common law was rigid and often gave only money damages
S+: Equitable remedies are discretionary and are granted by the court according to the facts
S+: 'He who seeks equity must do equity' is a maxim of equity
S+: Indian law absorbed many principles of equity through statutes such as the Specific Relief Act and the Indian Trusts Act
S-: Equity was developed by Parliament through statutes | Equity was developed by the Court of Chancery
S-: Equitable remedies must always be granted as a matter of right | Equitable remedies are discretionary
S-: Imprisonment is an equitable remedy | Equitable remedies include injunction, specific performance and rescission; imprisonment is a criminal penalty
C: Equity developed alongside the common law | the common law was rigid, formal and often provided only damages, which did not always give justice
C: An injunction is called an equitable remedy | it was developed by the Court of Chancery and is granted at the discretion of the court
C: A person who delays unreasonably may be refused an equitable remedy | equity helps the vigilant and not those who sleep over their rights
X: C2 D2 2 | Name two maxims of equity and explain one. | He who seeks equity must do equity; he who comes into equity must come with clean hands; delay defeats equity; equity follows the law; equity acts in personam (explain one).
X: C3 D3 3 | Why did equity develop in England? | Rigidity and formalism of common law; limited writs and remedies (only damages); petitions to the King and Lord Chancellor; Court of Chancery applied conscience and fairness.
L: D4 | Explain the origin of common law and equity and the main maxims of equity. How has Indian law adopted equity? | Royal courts and judge-made law; rigidity; Chancery; maxims; remedies – injunction, specific performance, trusts; Indian statutes – Specific Relief Act 1963, Indian Trusts Act 1882; 'justice, equity and good conscience'.
""")]

CHAPTERS = [(CH01, {'chapter_topic': 'the concept of state'}), (CH02, {'chapter_topic': 'forms and organs of government'}),
            (CH03, {'chapter_topic': 'separation of powers'}), (CH04, {'chapter_topic': 'the Indian Constitution'}),
            (CH05, {'chapter_topic': 'the nature and meaning of law'}), (CH06, {'chapter_topic': 'the classification of laws'})]
