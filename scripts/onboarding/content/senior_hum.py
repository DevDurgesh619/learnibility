"""Senior (grades 11-12) slot banks for History, Political Science and Geography (Humanities stream).

Humanities syllabuses diverge most across boards, so many slots are board swaps (B(...)): CBSE teaches world and
Indian history, Constitution and physical geography; Cambridge teaches European/American history, Global Perspectives
(a skills subject, the Political Science slot) and hydrology; IB teaches historical skills, Global Politics and
population/climate geography. Skill-based slots (causation, sources, argument) are shared.
Economics for Humanities reuses the Commerce economics bank.
"""
from dsl import S, K

HIST10 = {'cbse': 'social-science', 'cambridge': 'history', 'ib': 'social-science'}
GEO10 = {'cbse': 'social-science', 'cambridge': 'geography', 'ib': 'social-science'}


def B(cbse, cambridge, ib):
    """Board swap: a different slot for each board."""
    return {'cbse': cbse, 'cambridge': cambridge, 'ib': ib}


def one(board, grade, subject, kw):
    return K(grade, {board: subject}, {board: kw})


# ================================================================ History, grade 11
HISTORY_PRE_G11 = [
    S(K(10, HIST10, {'cbse': 'depression', 'cambridge': 'depression|wall street', 'ib': 'depression'}), 'The Great Depression', [
        ('The Great Depression began with', 'the Wall Street Crash of 1929', ['the end of the First World War', 'the Russian Revolution',
                                                                               'the Treaty of Versailles'], 'Share prices collapsed in New York'),
    ]),
    S(K(10, HIST10, {'cbse': 'first world war', 'cambridge': 'schlieffen|first world war', 'ib': 'long-term causes|first world war'}),
      'The First World War', [
        ('The First World War broke out in', '1914', ['1905', '1919', '1939'], 'After the assassination at Sarajevo'),
        ('Why did the war lead to rising prices and hardship in colonies such as India?', 'Colonial economies were taxed and drained to pay for the war',
         ['Colonies stopped trading', 'Colonies won new land', 'Wages rose faster than prices'], 'War costs were passed on'),
    ]),
    B(S(one('cbse', 10, 'social-science', 'french revolution|idea of the nation'), 'The French Revolution and the idea of the nation', [
        ("The French Revolution's ideas of 'la patrie' and 'le citoyen' aimed to", 'create a sense of collective identity among the French people',
         ['restore the monarchy', 'divide France into kingdoms', 'end all trade'], 'A nation of equal citizens'),
        ('The Napoleonic Code of 1804', 'abolished privileges based on birth and established equality before the law',
         ['restored feudal dues', 'gave only nobles the vote', 'banned private property'], 'A civil code'),
        ('Why did people in conquered areas come to resent Napoleonic rule despite its reforms?', 'Higher taxes, censorship and forced conscription',
         ['The reforms were too generous', 'Napoleon ended the French Revolution', 'They were not allowed to trade'], 'Benefits came with burdens'),
    ]),
      S(K(10, {'cambridge': 'history', 'ib': 'social-science'}, {'cambridge': 'hitler|dominate germany', 'ib': 'rise of hitler|hitler'}), 'The rise of Hitler', [
        ('Hitler became Chancellor of Germany in', 'January 1933', ['1923', '1939', '1929'], 'Appointed by Hindenburg'),
        ('Which event helped the Nazis win support after 1929?', 'Mass unemployment during the Depression', ['The Treaty of Locarno', 'The Dawes Plan', 'Economic recovery'],
         'Desperate voters turned to extremes'),
        ('How did the Enabling Act of 1933 help Hitler become a dictator?', 'It let him pass laws without the Reichstag',
         ['It banned the Nazi party', 'It restored the Kaiser', 'It created free elections'], 'Legal route to dictatorship'),
    ]), None),
    S(K(10, HIST10, {'cbse': 'print', 'cambridge': 'propaganda|nazis control', 'ib': 'source evaluation|research|sources'}), 'Evaluating historical sources', [
        ('A diary written by a soldier during a battle is a', 'primary source', ['secondary source', 'textbook', 'encyclopaedia'], 'Created at the time'),
        ('Why should a government poster from wartime be used with care?', 'It was made to persuade, so it may be one-sided',
         ['It is always false', 'Posters cannot show history', 'It was made long after the war'], 'Purpose affects reliability'),
        ('Two eyewitnesses describe the same protest differently. What is the best way for a historian to proceed?',
         'Compare both with other evidence and consider who wrote each and why', ['Choose the longer account', 'Ignore both', 'Trust the earlier one only'],
         'Corroboration and provenance'),
    ]),
]
HISTORY_PRE_G11[2]['ib'] = HISTORY_PRE_G11[2]['cambridge']

HISTORY_CUR_G11 = [
    B(S(one('cbse', 11, 'history', 'writing|cuneiform'), 'Mesopotamia: cities and writing', [
        ('The earliest writing in Mesopotamia was', 'cuneiform on clay tablets', ['Brahmi on palm leaves', 'hieroglyphs on papyrus', 'Latin on parchment'],
         'Wedge-shaped signs'),
        ('Why did cities first develop in southern Mesopotamia?', 'Fertile river plains produced surplus food that supported non-farmers',
         ['It had large forests', 'It was rich in stone and metal', 'It was isolated from trade'], 'Agricultural surplus'),
        ('Why was writing first used mainly for keeping records?', 'Temples and traders needed to record goods, rations and transactions',
         ['To write novels', 'To print newspapers', 'To teach every citizen'], 'Administration and trade'),
    ]),
      S(one('cambridge', 11, 'history', 'causes of the french revolution'), 'Causes of the French Revolution', [
        ('The Third Estate in pre-revolutionary France was made up of', 'commoners: peasants, workers and the bourgeoisie', ['the clergy', 'the nobility', 'the royal family'],
         'About 97% of the population'),
        ('Why did Louis XVI call the Estates-General in 1789?', 'The crown was bankrupt and needed new taxes', ['To declare war on Britain', 'To abolish the monarchy',
                                                                                                             'To crown his son'], 'Financial crisis'),
        ('How did the ideas of the Enlightenment contribute to the Revolution?', 'They questioned absolute monarchy and privilege and promoted rights and reason',
         ['They supported divine right', 'They praised feudalism', 'They had no influence'], 'Rousseau, Montesquieu, Voltaire'),
    ]),
      S(one('ib', 11, 'history', 'six key concepts|causation'), 'Historical concepts: causation and consequence', [
        ('Which is an example of a long-term cause?', 'decades of economic inequality', ['an assassination on one day', 'a single speech', 'a sudden storm'],
         'Develops over a long period'),
        ('A trigger (immediate cause) is', 'the event that sets off a crisis that was already building', ['the most important cause always', 'a consequence',
                                                                                                           'a long-term trend'], 'The spark'),
        ('Why do historians usually rank causes rather than list them?', 'To judge which causes mattered most and how they interacted',
         ['Because only one cause exists', 'To make history shorter', 'Because causes never interact'], 'Weighing significance'),
    ])),
    B(S(one('cbse', 11, 'history', 'political history of the roman|roman'), 'The Roman Empire', [
        ('The Roman Empire was centred on the', 'Mediterranean', ['Pacific Ocean', 'Indian Ocean', 'Baltic Sea'], 'It stretched across three continents'),
        ('Which emperor made Christianity an official religion of the empire?', 'Constantine', ['Augustus', 'Nero', 'Julius Caesar'], '4th century CE'),
        ('Why did the third-century crisis weaken the empire?', 'Invasions, civil wars and rapid changes of emperors strained the economy and army',
         ['The empire grew too peaceful', 'Trade stopped entirely', 'All provinces became independent'], 'Pressure on several fronts'),
    ]),
      S(one('cambridge', 11, 'history', 'napoleon'), 'Napoleon Bonaparte', [
        ('Napoleon became Emperor of France in', '1804', ['1789', '1815', '1793'], 'He crowned himself'),
        ('Which of Napoleon\'s reforms lasted long after his fall?', 'The Napoleonic Code', ['The Continental System', 'The invasion of Russia', 'The Hundred Days'],
         'Basis of French civil law'),
        ('How far did Napoleon preserve the ideals of the Revolution?', 'He kept legal equality and merit but ended political liberty',
         ['He restored the old privileges fully', 'He extended democracy', 'He abolished all revolutionary laws'], 'A mixed legacy'),
    ]),
      S(one('ib', 11, 'history', 'origin, purpose|source analysis'), 'Source analysis: origin, purpose and content (OPVL)', [
        ('In OPVL, the "O" stands for', 'origin', ['opinion', 'outcome', 'objective'], 'Who made it, when and where'),
        ('A government press release about a riot has limited value because', 'its purpose may be to defend the government\'s actions',
         ['it was written in prose', 'it is a primary source', 'it is too recent'], 'Purpose shapes content'),
        ("A memoir written 40 years after events by a participant. What is one value and one limitation?",
         'Value: insider knowledge; limitation: memory and hindsight may distort it', ['Value: always accurate; limitation: none',
                                                                                       'Value: neutral; limitation: too short', 'No value at all'],
         'Balance origin and purpose'),
    ])),
    B(S(one('cbse', 11, 'history', 'genghis|mongol'), 'The Mongols and Genghis Khan', [
        ('Genghis Khan united the', 'Mongol tribes', ['Roman provinces', 'Chinese dynasties', 'Turkish sultanates'], 'In 1206'),
        ("What was the 'yasa'?", 'the code of laws attributed to Genghis Khan', ['a Mongol horse', 'a type of tent', 'a trade route'],
         'Legal and military code'),
        ('Why were the Mongols able to rule such a vast empire?', 'Disciplined mobile armies, a fast messenger system and use of local administrators',
         ['They had the largest navy', 'They avoided all battles', 'They converted every subject'], 'Organisation and adaptability'),
    ]),
      S(one('cambridge', 11, 'history', 'causes of the industrial revolution|industrial revolution'), 'The Industrial Revolution in Britain', [
        ('The Industrial Revolution began in', 'Britain', ['Russia', 'Italy', 'India'], 'From the mid-18th century'),
        ("Which invention powered factories and railways?", 'the steam engine', ['the telephone', 'the internal combustion engine only', 'the light bulb'],
         'Watt improved it'),
        ('Why did rapid urbanisation lead to public health problems?', 'Overcrowded housing lacked clean water and sewers', ['Cities had too many doctors',
                                                                                                                              'Factories were in the countryside', 'People ate more fruit'],
         'Cholera and typhoid spread'),
    ]),
      S(one('ib', 11, 'history', 'colonial legacy|rwanda'), 'Rwanda: causes of the conflict', [
        ('Before independence, Rwanda was ruled by', 'Belgium', ['France', 'Britain', 'Germany after 1945'], 'From 1916'),
        ('How did colonial identity cards affect Rwandan society?', 'They fixed Hutu and Tutsi as rigid ethnic categories', ['They ended ethnic divisions',
                                                                                                                              'They gave everyone equal status', 'They were never used'],
         'Divide and rule'),
        ('What role did radio station RTLM play in 1994?', 'It spread propaganda that encouraged violence against Tutsi', ['It called for peace', 'It reported neutral news only',
                                                                                                                         'It was banned before 1994'], 'Media and incitement'),
    ])),
    B(S(one('cbse', 11, 'history', 'three orders|feudalism'), 'The Three Orders: feudal society', [
        ('Feudalism in medieval Europe was based on', 'land held in return for service', ['factory wages', 'elected parliaments', 'stock markets'],
         'Lords, vassals and serfs'),
        ('The three orders of medieval society were', 'clergy, nobility and peasantry', ['kings, merchants and soldiers', 'priests, traders and artisans',
                                                                                          'nobles, guilds and slaves'], 'Those who pray, fight and work'),
        ('Why did the Black Death help weaken serfdom?', 'Labour shortages let surviving peasants demand better terms', ['More serfs were born', 'Lords became richer',
                                                                                                                           'The Church banned farming'], 'Scarcity of workers'),
    ]),
      S(one('cambridge', 11, 'history', 'italian unification|unification'), 'Liberalism, nationalism and unification', [
        ('Who led the Red Shirts in Italian unification?', 'Garibaldi', ['Bismarck', 'Mazzini only', 'Napoleon III'], 'Expedition of the Thousand'),
        ("Cavour's main strategy for unifying Italy was", 'diplomacy and alliances with stronger powers such as France', ['peasant revolt', 'a revolution in Rome',
                                                                                                                            'isolation from Europe'], 'Realpolitik'),
        ('How far was German unification driven by nationalism rather than Prussian power?', 'Prussian wars and Bismarck\'s Realpolitik mattered more than popular nationalism',
         ['Only popular nationalism mattered', 'Austria unified Germany', 'It happened without war'], 'Blood and iron'),
    ]),
      S(one('ib', 11, 'history', 'kosovo|yugoslavia'), 'Kosovo: causes and course of the conflict', [
        ('Kosovo was part of which state before 1999?', 'Yugoslavia (Serbia)', ['Albania', 'Greece', 'Bulgaria'], 'An autonomous province'),
        ("Why did Milošević's revocation of Kosovo's autonomy in 1989 raise tensions?", 'It removed self-rule from the Albanian majority',
         ['It gave Kosovo independence', 'It united Kosovo with Albania', 'It had no effect'], 'Serbian nationalism'),
        ('Why did NATO intervene in 1999 without UN Security Council approval?', 'Russia was expected to veto action, and NATO cited humanitarian grounds',
         ['The UN asked NATO to', 'Kosovo invaded NATO', 'Serbia requested help'], 'Contested legality'),
    ])),
]

# ================================================================ History, grade 12
HISTORY_PRE_G12 = [
    S(K(11, 'history', {'cbse': 'crisis of the 14th|third-century crisis', 'cambridge': 'causes of the french revolution', 'ib': 'causation'}),
      'Causation in history', [
        ('Which best describes a "short-term cause"?', 'A factor that develops just before an event and brings it closer',
         ['A factor from centuries earlier', 'A result of the event', 'An unrelated event'], 'Close in time'),
    ]),
    S(K(11, 'history', {'cbse': 'revival of italian|renaissance|humanis', 'cambridge': 'economic effects|industrial', 'ib': 'change and continuity|turning points'}),
      'Change, continuity and turning points', [
        ('A turning point in history is', 'an event after which things change significantly', ['an event with no effects', 'a period with no change', 'a date of birth'],
         'Marks a shift'),
        ('Which is an example of continuity?', 'Most people continued to work on the land after a new king took power', ['A revolution overthrew the king',
                                                                                                                              'Factories replaced workshops', 'A new religion spread rapidly'],
         'Things staying the same'),
    ]),
    S(K(11, 'history', {'cbse': 'sources and the political|sources', 'cambridge': 'how far unification|nationalism', 'ib': 'origin, purpose|source analysis'}),
      'Reliability of sources', [
        ('A source that agrees with other independent evidence is said to be', 'corroborated', ['biased', 'secondary', 'anachronistic'], 'Cross-checked'),
        ('Why might a court chronicle praising a king be unreliable?', 'It was written to please the ruler', ['It is too old to read', 'It is a primary source',
                                                                                                                'Chronicles are always false'], 'Patronage'),
        ('A source is biased. Can it still be useful to a historian?', 'Yes, it reveals the attitudes and purposes of its author', ['No, it must be discarded',
                                                                                                                                       'Only if it is short', 'Only if it is a photograph'],
         'Bias is itself evidence'),
    ]),
    S(K(11, 'history', {'cbse': 'humanist view of history|humanis', 'cambridge': 'how far', 'ib': 'perspectives and significance|why historians disagree'}),
      'Historical interpretation', [
        ('An interpretation in history is', "a historian's explanation or judgement about the past", ['a list of dates', 'a primary source', 'a map'],
         'Arguments built on evidence'),
        ('Why do historians writing in different periods often interpret the same event differently?', 'They ask new questions and use new evidence shaped by their own times',
         ['The event changes', 'Older historians lied', 'Evidence never changes'], 'Context of the historian'),
        ('Historian A blames one leader for a war; Historian B blames long-term rivalries. Which approaches are these?', 'Intentionalist (individual) versus structural',
         ['Both structural', 'Both economic', 'Primary versus secondary'], 'Agency versus structure'),
    ]),
]

_CAM_IB_HIST12 = [
    S(K(12, 'history', {'cambridge': 'march on rome|rise of fascism', 'ib': 'german and italian expansion|italian'}), "Mussolini and Fascist Italy", [
        ('Mussolini came to power in Italy in', '1922', ['1918', '1933', '1940'], 'After the March on Rome'),
        ('Why did many Italians support Fascism after the First World War?', 'Anger over the "mutilated victory", economic crisis and fear of communism',
         ['Italy had gained many colonies', 'The economy was booming', 'There was no unrest'], 'Post-war grievances'),
        ('Why did Mussolini invade Abyssinia in 1935?', 'To build an empire, gain prestige and avenge the defeat at Adwa', ['To help the League of Nations',
                                                                                                                                'To defend Italy from attack', 'To end slavery'],
         'Imperial ambitions'),
    ]),
    S(K(12, 'history', {'cambridge': 'great turn|collectivisation', 'ib': 'single-party|authoritarian|stalin'}), "Stalin's USSR", [
        ('Stalin\'s rapid industrialisation programme was organised through', 'Five-Year Plans', ['the New Economic Policy', 'the Marshall Plan', 'perestroika'],
         'State targets'),
        ('The Great Terror of the 1930s involved', 'show trials and mass purges of suspected opponents', ['free elections', 'release of political prisoners',
                                                                                                           'the end of the secret police'], 'NKVD repression'),
        ('Why is collectivisation often judged a failure even though it supplied grain to cities?', 'It caused famine and millions of deaths, and farm output fell',
         ['It made peasants rich', 'It was voluntary', 'It increased private farming'], 'Human cost and low productivity'),
    ]),
    S(K(12, 'history', {'cambridge': "hitler's foreign policy|foreign policy", 'ib': 'appeasement|munich'}), 'Appeasement and the road to war', [
        ('The Munich Agreement of 1938 allowed Germany to take', 'the Sudetenland', ['Poland', 'Austria', 'the Rhineland'], 'From Czechoslovakia'),
        ('Why did Britain follow a policy of appeasement?', 'Fear of another war, military unreadiness and some sympathy for German grievances',
         ['Britain wanted Germany to rule Europe', 'Britain had no army', 'The USA ordered it'], 'Several motives'),
        ('Why did the Nazi-Soviet Pact of 1939 make war more likely?', 'It freed Hitler to invade Poland without fearing a war on two fronts',
         ['It united Britain and the USSR', 'It ended German rearmament', 'It returned land to Poland'], 'Removed a deterrent'),
    ]),
    S(K(12, 'history', {'cambridge': 'interpretation|historian', 'ib': 'comparing and contrasting|origin, purpose|opvl'}), 'Comparing sources and interpretations', [
        ('When comparing two sources, you should look for', 'points of agreement and disagreement', ['only the longer source', 'the date only', 'spelling errors'],
         'Compare and contrast'),
        ('A cartoon from a British newspaper in 1938 mocks Hitler. What should you consider first about its purpose?', 'Whether it aims to criticise appeasement or Hitler for a British audience',
         ['How long it took to draw', 'The colour of the ink', 'Whether Hitler saw it'], 'Audience and message'),
        ("What does 'synthesis' mean in a source-based essay?", 'Combining evidence from sources with your own knowledge into an argument',
         ['Copying the sources', 'Summarising one source', 'Listing dates'], 'Integration'),
    ]),
]

HISTORY_CUR_G12 = [
    B(S(one('cbse', 12, 'history', 'mohenjodaro|harappan|planned urban'), 'The Harappan Civilisation', [
        ('Which Harappan city had a citadel and a lower town?', 'Mohenjodaro', ['Pataliputra', 'Hampi', 'Taxila'], 'Planned layout'),
        ('Harappan seals were most likely used for', 'trade, to mark goods', ['coins', 'wedding rings', 'temple bells'], 'Sealing packages'),
        ('Why do historians still debate how the Harappan civilisation ended?', 'The script is undeciphered and the evidence points to several possible causes',
         ['It ended in one recorded battle', 'Written records explain it clearly', 'It never ended'], 'Climate, rivers, trade decline'),
    ]), _CAM_IB_HIST12[0], _CAM_IB_HIST12[0]),
    B(S(one('cbse', 12, 'history', "ashoka|mauryas"), 'The Mauryas and Ashoka', [
        ('Ashoka\'s inscriptions were mainly written in', 'Brahmi script in Prakrit', ['Devanagari in Hindi', 'Persian', 'Greek only'], 'Deciphered by James Prinsep'),
        ("Ashoka's 'dhamma' was", 'a moral code of tolerance, non-violence and respect', ['a tax system', 'a military strategy', 'a temple'], 'After the Kalinga war'),
        ('Why are Ashoka\'s inscriptions useful but not fully reliable sources?', 'They present the ruler\'s own view of his achievements', ['They are forgeries',
                                                                                                                                            'They are written in English', 'They are too recent'],
         'Royal self-presentation'),
    ]), _CAM_IB_HIST12[1], _CAM_IB_HIST12[1]),
    B(S(one('cbse', 12, 'history', 'mahabharata|varna|kinship'), 'Kinship, caste and class in early societies', [
        ('The varna order divided society into', 'four groups', ['two classes', 'seven castes', 'ten tribes'], 'Brahmanas, kshatriyas, vaishyas, shudras'),
        ('Why did scholars prepare a critical edition of the Mahabharata?', 'To compare many manuscripts and identify the common text', ['To translate it into English only',
                                                                                                                                         'To write a new story', 'To remove all versions'],
         'Many regional versions existed'),
        ('Why do historians treat Brahmanical texts on social norms with caution?', 'They describe ideals prescribed by an elite, not always actual practice',
         ['They are fiction', 'They were written by foreigners', 'They have no dates'], 'Prescriptive versus descriptive'),
    ]), _CAM_IB_HIST12[2], _CAM_IB_HIST12[2]),
    B(S(one('cbse', 12, 'history', 'sanchi|stupa|buddh'), 'Thinkers, beliefs and buildings: Buddhism and Sanchi', [
        ('Stupas were built to hold', 'relics associated with the Buddha', ['royal treasure', 'grain', 'weapons'], 'Sacred mounds'),
        ('The Buddha taught that suffering can be ended by', 'following the Eightfold Path', ['performing large sacrifices', 'caste duties alone', 'pilgrimage to Mecca'],
         'The Middle Way'),
        ('Why did Buddhism spread widely among traders and townspeople?', 'It rejected rigid ritual and welcomed people of all varnas', ['It demanded costly sacrifices',
                                                                                                                                          'It was taught only in Sanskrit', 'It banned trade'],
         'Accessible ethics'),
    ]), _CAM_IB_HIST12[3], _CAM_IB_HIST12[3]),
]

# ================================================================ Political Science, grade 11
POLSCI_PRE_G11 = [
    S(K(10, HIST10, {'cbse': 'power-sharing|power sharing', 'cambridge': 'weimar|constitution', 'ib': 'governance|power'}), 'Sharing and limiting power', [
        ('Dividing power between the legislature, executive and judiciary is called', 'separation of powers', ['federalism', 'monarchy', 'coalition'],
         'Checks and balances'),
    ]),
    S(K(10, HIST10, {'cbse': 'outcomes of democracy|democracy', 'cambridge': 'consolidation|dominate germany', 'ib': 'political ideologies|ideolog'}),
      'Democracy and dictatorship', [
        ('In a dictatorship, power is held by', 'one person or a small group without free elections', ['all citizens equally', 'independent courts', 'the media'],
         'No accountability'),
        ('Why is a free press important in a democracy?', 'It informs citizens and holds the government to account', ['It writes the laws', 'It chooses the judges',
                                                                                                                         'It runs elections'], 'Accountability'),
    ]),
    S(K(10, HIST10, {'cbse': 'political parties', 'cambridge': 'elections|depression, elections', 'ib': 'citizenship|governance'}), 'Parties and elections', [
        ('A political party mainly aims to', 'win elections and form a government', ['run businesses', 'write the constitution alone', 'appoint judges'],
         'Seeking power'),
        ('A coalition government is formed when', 'no single party has a majority, so parties share power', ['one party wins all seats', 'the army takes over',
                                                                                                             'elections are cancelled'], 'Combining seats'),
        ('Why can proportional representation lead to many coalition governments?', 'Small parties win seats in proportion to votes, so one party rarely has a majority',
         ['It bans small parties', 'It gives all seats to the largest party', 'It removes voting'], 'Fragmented seats'),
    ]),
    S(K(10, HIST10, {'cbse': 'gender, religion|caste', 'cambridge': 'persecution|minorities', 'ib': 'human rights'}), 'Rights and discrimination', [
        ('Equal treatment of all citizens regardless of religion, caste or gender is', 'equality before the law', ['privilege', 'sedition', 'censorship'],
         'A fundamental principle'),
        ('Which is an example of discrimination?', 'Refusing a job to someone because of their religion', ['Hiring the best-qualified candidate',
                                                                                                              'Paying equal wages', 'Holding free elections'],
         'Unfair treatment of a group'),
        ('Why do democracies protect minority rights even against majority votes?', 'Majority rule must not become oppression of minorities',
         ['Minorities always win elections', 'Majorities never vote', 'Rights are only for majorities'], 'Liberal democracy'),
    ]),
]

POLSCI_CUR_G11 = [
    B(S(one('cbse', 11, 'political-science', 'why do we need a constitution|constitution'), 'Why we need a constitution', [
        ('A constitution is', 'the basic set of rules that establishes and limits government', ['a list of political parties', 'a budget', 'a court judgment'],
         'Supreme law'),
        ('The Indian Constitution was drafted by the', 'Constituent Assembly', ['Lok Sabha of 1952', 'British Parliament', 'Supreme Court'], '1946-49'),
        ('Why must a constitution limit the powers of government?', 'To protect citizens from abuse of power by those who rule', ['To make government weak forever',
                                                                                                                                    'To let one party rule', 'To avoid elections'],
         'Limited government'),
    ]),
      S(one('cambridge', 11, 'political-science', 'what makes an issue global|global issue'), 'What makes an issue global', [
        ('An issue is global when', 'it affects people across many countries and needs international cooperation', ['it happens in one village only',
                                                                                                                       'it is in the news once', 'it concerns one family'],
         'Scale and interconnection'),
        ('Which is a global issue?', 'climate change', ['a local school timetable', 'a family budget', 'a town fair'], 'Affects all nations'),
        ('Why is it useful to look at a global issue at local, national and global levels?', 'Causes and solutions can differ at each level',
         ['Only the global level matters', 'Local views are irrelevant', 'It makes the issue disappear'], 'Multi-scale analysis'),
    ]),
      S(one('ib', 11, 'political-science', 'forms of power|power'), 'Power: hard, soft and smart', [
        ('Using military threats or force to get what a state wants is', 'hard power', ['soft power', 'smart power', 'legitimacy'], 'Coercion'),
        ('Which is an example of soft power?', 'A country\'s films and culture being admired abroad', ['Economic sanctions', 'Invading a neighbour', 'Building nuclear weapons'],
         'Attraction (Nye)'),
        ('Why might a state combine aid programmes with military alliances?', 'Smart power mixes attraction and coercion to achieve goals', ['It must by UN law',
                                                                                                                                               'Aid replaces armies', 'It has no other choice'],
         'Smart power'),
    ])),
    B(S(one('cbse', 11, 'political-science', 'fundamental rights'), 'Fundamental Rights', [
        ('Which is a Fundamental Right in the Indian Constitution?', 'Right to Equality', ['Right to Property', 'Right to Vote at 16', 'Right to Free Housing'],
         'Articles 14-18'),
        ('The Right to Constitutional Remedies lets citizens', 'go to court if their Fundamental Rights are violated', ['change the Constitution', 'avoid taxes', 'elect judges'],
         'Ambedkar called it the heart of the Constitution'),
        ('How do Directive Principles differ from Fundamental Rights?', 'They guide state policy but cannot be enforced in court', ['They are enforceable rights',
                                                                                                                                     'They apply only to children', 'They were removed in 1950'],
         'Non-justiciable'),
    ]),
      S(one('cambridge', 11, 'political-science', 'perspective'), 'Identifying perspectives', [
        ('A perspective is', 'a viewpoint on an issue shaped by values and experience', ['a fact', 'a statistic', 'a source title'], 'A way of seeing'),
        ('A farmer and a factory owner disagree about a new dam. Why?', 'They are affected differently and hold different interests', ['One must be lying',
                                                                                                                                          'Dams affect everyone the same', 'They read different news'],
         'Interests shape views'),
        ('Why should you consider perspectives you disagree with when analysing an issue?', 'It gives a fuller understanding and tests your own reasoning',
         ['It wastes time', 'It always changes your mind', 'Other views are always wrong'], 'Balanced judgement'),
    ]),
      S(one('ib', 11, 'political-science', 'westphalian|sovereignty'), 'Sovereignty and the state', [
        ('Sovereignty means', 'supreme authority of a state over its territory', ['membership of the UN', 'a strong economy', 'having a king'], 'Westphalian principle'),
        ('Which challenges state sovereignty from above?', 'binding rules of supranational bodies such as the EU', ['local elections', 'a national anthem', 'a census'],
         'Pooling sovereignty'),
        ('Why is Taiwan described as having contested statehood?', 'It governs itself but is not widely recognised as a sovereign state',
         ['It has no government', 'It is a UN member', 'It has no territory'], 'Recognition matters'),
    ])),
    B(S(one('cbse', 11, 'political-science', 'fptp|system of election'), 'Election and representation', [
        ('India elects the Lok Sabha using', 'first past the post', ['proportional representation', 'a lottery', 'indirect election only'], 'Plurality in each constituency'),
        ('Reserved constituencies exist to', 'ensure representation of Scheduled Castes and Tribes', ['give seats to the richest', 'stop women voting', 'favour one party'],
         'Social justice'),
        ('Why did India choose FPTP rather than proportional representation?', 'It is simple for voters and tends to produce stable governments',
         ['It is used nowhere else', 'It gives exact proportionality', 'It removes constituencies'], 'Simplicity and stability'),
    ]),
      S(one('cambridge', 11, 'political-science', 'components of an argument|claims'), 'Analysing arguments: claims, reasons and evidence', [
        ('In an argument, a reason is', 'a statement given to support a claim', ['the conclusion', 'a question', 'an unrelated fact'], 'Why to believe the claim'),
        ("'Cities should ban cars because air pollution causes asthma.' What is the claim?", 'Cities should ban cars', ['Air pollution causes asthma', 'Asthma is common',
                                                                                                                       'Cars are fast'], 'What the writer wants you to accept'),
        ("What is the hidden assumption in 'We should cut the school day because students are tired'?", 'Shorter days will make students less tired',
         ['Students are tired', 'School days exist', 'Teachers agree'], 'An unstated link'),
    ]),
      S(one('ib', 11, 'political-science', 'weber|legitimacy'), 'Legitimacy', [
        ('Legitimacy is', 'the acceptance of an authority\'s right to rule', ['military strength', 'the size of territory', 'wealth'], 'Rightful power'),
        ("According to Weber, which is a source of legitimacy?", 'charismatic authority', ['economic sanctions', 'propaganda only', 'hard power'],
         'Traditional, charismatic, legal-rational'),
        ('A government wins a flawed election but delivers rapid growth. How might it claim legitimacy?', 'Through performance legitimacy, despite weak procedural legitimacy',
         ['Through divine right', 'It cannot claim any', 'Through charisma alone'], 'Output versus input legitimacy'),
    ])),
    B(S(one('cbse', 11, 'political-science', 'parliamentary and presiden|executive'), 'The executive', [
        ('In India, the real executive power lies with the', 'Prime Minister and Council of Ministers', ['President alone', 'Chief Justice', 'Election Commission'],
         'Parliamentary system'),
        ('In a presidential system such as the USA, the President is', 'both head of state and head of government', ['chosen by parliament', 'a ceremonial figure only',
                                                                                                                      'a judge'], 'Separate election'),
        ('Why is the civil service called the permanent executive?', 'Officials stay in office while elected ministers change', ['They are elected for life',
                                                                                                                                  'They make all laws', 'They cannot be removed ever'],
         'Continuity'),
    ]),
      S(one('cambridge', 11, 'political-science', 'credibility'), 'Evaluating sources and evidence', [
        ('A vested interest means', 'a source gains from a particular outcome', ['the source is an expert', 'the source is recent', 'the source is anonymous'],
         'Possible bias'),
        ('Which is usually the most credible source on vaccine safety?', 'a peer-reviewed medical study', ['a celebrity post', 'an anonymous blog', 'a product advert'],
         'Expertise and review'),
        ('A study funded by a sugar company finds sugar harmless. What should you do?', 'Check whether independent studies reach the same finding',
         ['Accept it fully', 'Reject all studies on sugar', 'Ignore funding'], 'Corroborate'),
    ]),
      S(one('ib', 11, 'political-science', 'interdependence and globalization|global governance'), 'Interdependence and global governance', [
        ('Which organisation is central to global governance?', 'the United Nations', ['a national parliament', 'a city council', 'a football club'], 'Since 1945'),
        ('Interdependence means', 'states rely on each other economically and politically', ['states are fully isolated', 'only one state matters', 'trade has stopped'],
         'Mutual dependence'),
        ('Why is collective action on climate change hard?', 'Each state may free-ride, hoping others will bear the costs', ['All states agree instantly', 'It is cheap',
                                                                                                                                  'No state emits carbon'], 'Collective action problem'),
    ])),
]

# ================================================================ Political Science, grade 12
POLSCI_PRE_G12 = [
    S(K(11, 'political-science', {'cbse': 'constitution', 'cambridge': 'global issue|what makes', 'ib': 'westphalian|sovereignty'}), 'Authority and the state', [
        ('A state is usually defined by territory, population, government and', 'sovereignty', ['a flag only', 'a football team', 'a stock market'], 'Four elements'),
    ]),
    S(K(11, 'political-science', {'cbse': 'fundamental rights|rights', 'cambridge': 'perspective', 'ib': 'weber|legitimacy|human rights'}), 'Rights and perspectives', [
        ('Human rights are', 'rights everyone has simply because they are human', ['rights only citizens earn', 'privileges given by kings', 'rules of a club'],
         'Universal'),
        ('Why might people from different cultures prioritise different rights?', 'Values such as community and individual freedom are weighted differently',
         ['Rights are identical everywhere', 'Some people have no rights', 'Rights cannot be discussed'], 'Universalism versus relativism'),
    ]),
    S(K(11, 'political-science', {'cbse': 'electoral reforms|election', 'cambridge': 'components of an argument|argument', 'ib': 'political issue'}),
      'Evaluating claims', [
        ('Which piece of evidence is strongest?', 'data from a large, representative survey', ['one person\'s opinion', 'a rumour', 'an advert'], 'Representative data'),
        ("'Turnout fell after the new voting law, so the law caused it.' What is the flaw?", 'It assumes correlation proves causation',
         ['It uses data', 'It is too short', 'It mentions a law'], 'Other factors may explain it'),
        ('Why is a counter-argument useful in an essay?', 'Answering it strengthens your conclusion', ['It weakens your position', 'It is not allowed', 'It replaces evidence'],
         'Rebuttal'),
    ]),
    S(K(11, 'political-science', {'cbse': 'executive', 'cambridge': 'credibility|evidence', 'ib': 'forms of power|power'}), 'Power and accountability', [
        ('Holding leaders answerable for their actions is', 'accountability', ['sovereignty', 'anarchy', 'propaganda'], 'Answerability'),
        ('Which institution most directly checks the executive in a parliamentary democracy?', 'the legislature', ['the army', 'the stock exchange', 'the media alone'],
         'Questions, votes, committees'),
        ('Why can concentrated power be dangerous even under a popular leader?', 'Without checks, it can be abused and is hard to remove', ['Popular leaders never err',
                                                                                                                                              'Concentration always improves policy', 'Checks slow nothing'],
         'Lord Acton'),
    ]),
]

_CBSE_IB_POL12 = [
    S(K(12, 'political-science', {'cbse': 'principal organs|un', 'ib': 'third-party|peacekeeping'}), 'The UN and peacekeeping', [
        ('The UN body with permanent members holding a veto is the', 'Security Council', ['General Assembly', 'WHO', 'International Court only'], 'P5'),
        ('UN peacekeepers are usually deployed', 'with the consent of the parties to monitor a ceasefire', ['to conquer territory', 'to collect taxes', 'only in Europe'],
         'Consent and impartiality'),
        ('Why is the veto criticised by many states?', 'Five states can block action even when most members support it', ['It gives every state equal power',
                                                                                                                            'It is rarely used', 'It applies to the General Assembly'],
         'Unequal power'),
    ]),
    S(K(12, 'political-science', {'cbse': 'traditional security|security', 'ib': 'types of conflict|causes of conflict'}), 'Security and conflict', [
        ('A war between two states is an', 'interstate conflict', ['intrastate conflict', 'civil disobedience', 'election'], 'Between states'),
        ('Non-traditional security threats include', 'pandemics and climate change', ['only foreign armies', 'border posts', 'military parades'], 'Human security'),
        ('What is the security dilemma?', 'One state\'s defensive build-up makes others feel less secure, leading to arms races',
         ['States always trust each other', 'Security has no costs', 'Only small states arm'], 'Spiral of insecurity'),
    ]),
    S(K(12, 'political-science', {'cbse': 'non-traditional|human security', 'ib': 'negative and positive peace|non-violence|defining peace'}), 'Peace and human security', [
        ('Positive peace means', 'the presence of justice and conditions that prevent violence', ['simply no war', 'military victory', 'a ceasefire only'], 'Galtung'),
        ('Structural violence refers to', 'harm caused by unjust social systems such as poverty', ['a bombing', 'a street fight', 'a duel'], 'Indirect harm'),
        ('Why did Gandhi\'s non-violent methods put pressure on the British?', 'They exposed the injustice of colonial rule and made it costly to maintain',
         ['They used force', 'They avoided public attention', 'They relied on foreign armies'], 'Moral and economic pressure'),
    ]),
]

POLSCI_CUR_G12 = [
    B(_CBSE_IB_POL12[0], S(one('cambridge', 12, 'political-science', 'research question'), 'Choosing a research question', [
        ('A good research question should be', 'focused enough to allow depth and debate', ['as broad as possible', 'answerable with yes or no only', 'unrelated to evidence'],
         'Manageable scope'),
        ('Which is the best research question?', 'To what extent has microfinance reduced poverty among women in Bangladesh since 2000?',
         ['Is poverty bad?', 'What is money?', 'Tell me about Bangladesh.'], 'Specific, debatable, researchable'),
        ('Why should a research question permit different perspectives?', 'So the report can weigh evidence and reach a supported judgement',
         ['So it can be answered in one line', 'To avoid using sources', 'Because opinions are facts'], 'Debate is needed'),
    ]), _CBSE_IB_POL12[0]),
    B(_CBSE_IB_POL12[1], S(one('cambridge', 12, 'political-science', 'primary research methods'), 'Research methods', [
        ('An interview you conduct yourself is', 'primary research', ['secondary research', 'a literature review', 'a citation'], 'First-hand data'),
        ('Why might an online survey give a biased sample?', 'Only people with internet access and interest will respond', ['Online surveys are always random',
                                                                                                                                'Everyone responds', 'It is secondary data'],
         'Self-selection'),
        ('Why combine qualitative interviews with quantitative surveys?', 'Numbers show patterns while interviews explain reasons', ['It doubles the word count',
                                                                                                                                     'Interviews replace data', 'Surveys cannot be analysed'],
         'Mixed methods'),
    ]), _CBSE_IB_POL12[1]),
    B(_CBSE_IB_POL12[2], S(one('cambridge', 12, 'political-science', 'evaluating methods|credibility, reli'), 'Evaluating methods and data', [
        ('Reliability of a method means', 'it would give similar results if repeated', ['it is expensive', 'it is new', 'it agrees with you'], 'Consistency'),
        ('A study of 20 students claims to show the views of all teenagers. What is the main weakness?', 'The sample is too small and not representative',
         ['It uses students', 'It has a title', 'It has numbers'], 'Generalisation'),
        ('Why should a researcher acknowledge the limitations of their own method?', 'It shows critical awareness and lets readers judge the conclusions',
         ['It hides errors', 'It is optional decoration', 'It lowers the grade'], 'Reflective practice'),
    ]), _CBSE_IB_POL12[2]),
    B(S(one('cbse', 12, 'political-science', 'soviet system|gorbachev|bipolarity'), 'The end of bipolarity', [
        ('The Soviet Union broke up in', '1991', ['1945', '1989 only', '2001'], 'Into 15 republics'),
        ("Gorbachev's reforms of 'glasnost' meant", 'openness and freer discussion', ['military expansion', 'closing borders', 'more censorship'], 'Political opening'),
        ('Why did the end of the Cold War make the world "unipolar"?', 'The USA was left as the only superpower', ['Many equal powers emerged', 'China became the sole power',
                                                                                                                     'Europe united into one state'], 'One pole'),
    ]),
      S(one('cambridge', 12, 'political-science', 'referencing|sustained argument|structuring'), 'Writing the research report', [
        ('A bibliography lists', 'the sources used in the report', ['the chapters of the report', 'the author\'s opinions', 'the marks awarded'], 'References'),
        ('Why must sources be referenced?', 'To credit authors and let readers check the evidence', ['To make the report longer', 'Because quotes are illegal', 'To hide the sources'],
         'Academic honesty'),
        ('A strong conclusion in a research report should', 'answer the question with a judgement supported by the evidence', ['introduce new topics', 'repeat the introduction word for word',
                                                                                                                                  'avoid any judgement'], 'Supported answer'),
    ]),
      S(one('ib', 12, 'political-science', 'nature of borders|borders'), 'Borders', [
        ('A border that exists mainly in trade rules and visas rather than on the ground is', 'a virtual or economic border', ['a natural border', 'a river',
                                                                                                                                 'a mountain range'], 'Not physical'),
        ('Why are many border disputes linked to colonial history?', 'Colonial powers drew borders without regard for local communities', ['Borders were chosen by referendum',
                                                                                                                                              'Colonies had no borders', 'Colonial maps were exact'],
         'Arbitrary lines'),
        ('How can tighter border controls create a humanitarian challenge?', 'Refugees fleeing danger may be left stranded or pushed back', ['They end all migration',
                                                                                                                                              'They make travel easier', 'They have no effect'],
         'Rights of asylum seekers'),
    ])),
]

# ================================================================ Geography, grade 11
GEOGRAPHY_PRE_G11 = [
    S(K(10, GEO10, {'cbse': 'resources|resource', 'cambridge': 'resources|energy', 'ib': 'sustainab|climate'}), 'Resources and sustainable development', [
        ('Sustainable development means', 'meeting present needs without harming the ability of future generations to meet theirs',
         ['using all resources now', 'stopping all development', 'only protecting forests'], 'Brundtland definition'),
    ]),
    S(K(10, GEO10, {'cbse': 'agriculture|cropping', 'cambridge': 'agriculture', 'ib': 'globalisation'}), 'Agriculture and farming systems', [
        ('Farming mainly to feed the farmer\'s own family is', 'subsistence farming', ['commercial farming', 'plantation farming', 'agribusiness'], 'Self-consumption'),
        ('Why is irrigation important for farming in areas with a seasonal monsoon?', 'It supplies water during the dry months', ['It stops rain', 'It removes soil',
                                                                                                                                    'It cools the air'], 'Reliable water'),
    ]),
    S(K(10, GEO10, {'cbse': 'water', 'cambridge': 'water|resources', 'ib': 'climate|sustainab'}), 'Water scarcity', [
        ('Water scarcity can be caused by', 'over-use and pollution as well as low rainfall', ['only by deserts', 'too many rivers', 'cold weather alone'], 'Physical and human causes'),
        ('Rainwater harvesting helps by', 'collecting and storing rain for later use or recharging groundwater', ['stopping rain', 'polluting rivers', 'increasing floods'],
         'Local solution'),
        ('Why can large dams be controversial?', 'They provide water and power but can displace people and harm ecosystems', ['They have no benefits', 'They always increase rainfall',
                                                                                                                                 'They never affect people'], 'Costs and benefits'),
    ]),
    B(S(one('cbse', 10, 'social-science', 'manufacturing|industr'), 'Manufacturing industries', [
        ('Which is an agro-based industry?', 'cotton textiles', ['iron and steel', 'cement', 'aluminium smelting'], 'Raw material from farms'),
        ('Iron and steel plants are often located near coalfields and iron ore because', 'raw materials are heavy and costly to transport', ['markets are always there',
                                                                                                                                                'labour is free', 'the land is flat'],
         'Weight-losing industry'),
        ('How can industries reduce environmental damage?', 'Treat waste water and use cleaner technology', ['Release waste into rivers', 'Burn more coal', 'Locate in forests'],
         'Pollution control'),
    ]),
      S(K(10, {'cambridge': 'geography'}, {'cambridge': 'migration'}), 'Migration', [
        ('Moving from the countryside to a city is', 'rural-to-urban migration', ['international migration', 'emigration', 'counter-urbanisation'], 'Internal movement'),
        ('Which is a pull factor of a city?', 'better job opportunities', ['drought', 'conflict', 'lack of schools'], 'Attracts migrants'),
        ('Why can migration benefit the source country?', 'Migrants send remittances home', ['It always reduces income', 'It increases unemployment at home', 'Nobody returns'],
         'Money transfers'),
    ]),
      S(K(10, {'ib': 'social-science'}, {'ib': 'population|migration'}), 'Population and migration', [
        ('Moving from the countryside to a city is', 'rural-to-urban migration', ['international migration', 'emigration', 'counter-urbanisation'], 'Internal movement'),
        ('Which is a pull factor of a city?', 'better job opportunities', ['drought', 'conflict', 'lack of schools'], 'Attracts migrants'),
        ('Why can migration benefit the source country?', 'Migrants send remittances home', ['It always reduces income', 'It increases unemployment at home', 'Nobody returns'],
         'Money transfers'),
    ])),
]

_GEO11_POP = S(one('ib', 11, 'geography', 'population distribution|distribution'), 'Population distribution and change', [
    ('Population density is', 'the number of people per square kilometre', ['the total population', 'the birth rate', 'the area of a country'], 'People per area'),
    ('In stage 2 of the demographic transition model,', 'death rates fall while birth rates stay high', ['both rates are low', 'birth rates fall first', 'population falls'],
     'Rapid growth'),
    ('Why do some countries reach stage 5 of the DTM with a shrinking population?', 'Birth rates fall below death rates as people have fewer children',
     ['Death rates rise sharply', 'Migration stops', 'Life expectancy falls'], 'Low fertility'),
])

GEOGRAPHY_CUR_G11 = [
    B(S(one('cbse', 11, 'geography', 'plate tectonics|earthquake'), 'Earthquakes and plate tectonics', [
        ('The point inside the Earth where an earthquake starts is the', 'focus (hypocentre)', ['epicentre', 'crater', 'fault scarp'], 'Directly above it is the epicentre'),
        ('Which seismic waves cannot travel through liquids?', 'S waves', ['P waves', 'surface waves', 'all waves'], 'This shows the outer core is liquid'),
        ('Why does the shadow zone of P and S waves tell us about the Earth\'s interior?', 'Waves bend or stop at boundaries between layers of different state',
         ['Waves never change speed', 'The Earth is hollow', 'Waves travel only on the surface'], 'Refraction at the core'),
    ]),
      S(one('cambridge', 11, 'geography', 'inputs, outputs|drainage basin'), 'The drainage basin system', [
        ('Precipitation is an', 'input to the drainage basin', ['output', 'store', 'transfer only'], 'Water enters the system'),
        ('Water soaking into the soil is', 'infiltration', ['percolation', 'evaporation', 'interception'], 'Surface to soil'),
        ('Why does urbanisation increase surface runoff?', 'Impermeable surfaces stop infiltration', ['Cities have more trees', 'It reduces rainfall', 'Soil absorbs more'],
         'Concrete and tarmac'),
    ]), _GEO11_POP),
    B(S(one('cbse', 11, 'geography', 'weathering'), 'Weathering and geomorphic processes', [
        ('The breakdown of rocks in place without movement is', 'weathering', ['erosion', 'deposition', 'transportation'], 'In situ'),
        ('Freeze-thaw weathering is most common in', 'cold climates where temperatures move around 0 °C', ['hot deserts only', 'tropical rainforests', 'deep oceans'],
         'Water expands as it freezes'),
        ('Why is chemical weathering faster in hot, humid regions?', 'Heat and moisture speed up chemical reactions', ['There is no water', 'Rocks are softer by law',
                                                                                                                           'Cold slows nothing'], 'Reaction rates'),
    ]), S(one('cambridge', 11, 'geography', 'storm hydrograph|hydrograph'), 'Storm hydrographs', [
        ('The time between peak rainfall and peak discharge is the', 'lag time', ['base flow', 'rising limb', 'bankfull'], 'On a hydrograph'),
        ('Which factor gives a short lag time?', 'steep slopes and impermeable rock', ['dense forest', 'deep permeable soil', 'gentle slopes'], 'Fast runoff'),
        ('Why does deforestation make floods more likely?', 'Less interception and infiltration send water to rivers faster', ['Trees cause rain', 'Soil becomes deeper',
                                                                                                                                   'Rivers widen'], 'Flashier hydrograph'),
    ]), S(one('ib', 11, 'geography', 'pyramids|dependency'), 'Population structure', [
        ('A population pyramid shows', 'the age and sex structure of a population', ['rainfall over a year', 'the height of mountains', 'GDP growth'], 'Age-sex graph'),
        ('The dependency ratio compares', 'dependants (young and old) with the working-age population', ['men with women', 'cities with villages', 'births with deaths only'],
         'Economic burden'),
        ('What challenges does an ageing population create?', 'Higher pension and health costs with fewer workers to pay taxes', ['More schools needed', 'Too many young workers',
                                                                                                                                       'Rising birth rates'], 'Greying society'),
    ])),
    B(S(one('cbse', 11, 'geography', 'drainage|river'), 'Rivers and drainage', [
        ('A river system with its tributaries forms a', 'drainage basin', ['delta only', 'watershed line', 'plateau'], 'Area drained'),
        ('A meander is', 'a bend in a river', ['a waterfall', 'a lake', 'a delta'], 'Formed by erosion and deposition'),
        ('Why are Himalayan rivers perennial while many peninsular rivers are seasonal?', 'Himalayan rivers are fed by glaciers as well as rain', ['They have no tributaries',
                                                                                                                                                       'Peninsular rivers are glacier-fed', 'They flow uphill'],
         'Snowmelt'),
    ]), S(one('cambridge', 11, 'geography', 'meanders|river landforms|channel processes'), 'River channel processes and landforms', [
        ('Erosion by rocks carried in the river scraping the bed is', 'abrasion', ['solution', 'attrition', 'hydraulic action'], 'Sandpaper effect'),
        ('On a meander, erosion is greatest on the', 'outer bank', ['inner bank', 'river bed only', 'floodplain'], 'Fastest flow'),
        ('Why do levees form along some rivers?', 'Coarse sediment is deposited near the channel when the river floods', ['Humans always build them', 'Erosion raises the banks',
                                                                                                                             'Wind piles sand'], 'Natural embankments'),
    ]), S(one('ib', 11, 'geography', 'migration'), 'Migration and its impacts', [
        ('People forced to leave their country because of persecution are', 'refugees', ['economic migrants', 'tourists', 'commuters'], 'Protected by international law'),
        ('Brain drain means', 'skilled workers leaving a country', ['students failing exams', 'water draining from fields', 'people moving to villages'], 'Loss of talent'),
        ('How can international migration help host countries?', 'Migrants fill labour shortages and pay taxes', ['It always raises unemployment', 'It reduces the workforce',
                                                                                                                  'It ends trade'], 'Economic contribution'),
    ])),
    S(K(11, 'geography', {'cbse': 'heat budget|insolation|atmosphere', 'cambridge': 'energy budget', 'ib': 'energy balance|atmospheric system'}),
      'Atmospheric energy and the greenhouse effect', [
        ('Incoming solar radiation is called', 'insolation', ['albedo', 'convection', 'condensation'], 'Incoming sunlight'),
        ('Albedo is', 'the proportion of sunlight reflected by a surface', ['the temperature of the air', 'a type of cloud', 'rainfall intensity'], 'Reflectivity'),
        ('Why does melting Arctic sea ice speed up warming?', 'Darker ocean absorbs more sunlight than reflective ice', ['Ice makes heat', 'Oceans reflect more', 'It cools the air'],
         'Positive feedback'),
    ]),
]

# ================================================================ Geography, grade 12
GEOGRAPHY_PRE_G12 = [
    S(K(11, 'geography', {'cbse': 'heat budget|insolation|atmosphere', 'cambridge': 'energy budget', 'ib': 'greenhouse|energy balance'}), 'The greenhouse effect', [
        ('Which gas contributes most to the enhanced greenhouse effect from human activity?', 'carbon dioxide', ['oxygen', 'nitrogen', 'argon'], 'From burning fossil fuels'),
    ]),
    B(S(one('cbse', 11, 'geography', 'drainage|river'), 'Rivers and drainage', [
        ('The line separating two drainage basins is a', 'watershed', ['tributary', 'confluence', 'meander'], 'High ground'),
        ('Why do deltas form at some river mouths?', 'The river slows and deposits sediment faster than the sea removes it', ['The river speeds up', 'Waves build them',
                                                                                                                                 'Glaciers deposit them'], 'Loss of energy'),
    ]), S(one('cambridge', 11, 'geography', 'storm hydrograph|hydrograph'), 'Rivers and hydrographs', [
        ('The time between peak rainfall and peak discharge is the', 'lag time', ['base flow', 'rising limb', 'bankfull'], 'On a hydrograph'),
        ('Why does urbanisation shorten lag time?', 'Impermeable surfaces and drains send water to rivers faster', ['Cities absorb more water', 'It rains less in cities',
                                                                                                                       'Rivers are longer in cities'], 'Rapid runoff'),
    ]), S(one('ib', 11, 'geography', 'threat multiplier|impacts on people|sea-level'), 'Consequences of climate change', [
        ('Rising sea levels are caused mainly by', 'melting land ice and thermal expansion of seawater', ['more rivers', 'earthquakes', 'deforestation alone'], 'Warming oceans'),
        ('Why are low-income coastal communities often most vulnerable to climate change?', 'They have fewer resources to adapt or recover', ['They emit the most carbon',
                                                                                                                                                'They live on high ground', 'They are always insured'],
         'Vulnerability'),
    ])),
    B(S(one('cbse', 11, 'geography', 'structure of the earth|interior'), 'The interior of the Earth', [
        ('The outermost solid layer of the Earth is the', 'crust', ['mantle', 'outer core', 'inner core'], 'Thinnest layer'),
        ('Which layer of the Earth is liquid?', 'outer core', ['inner core', 'crust', 'lithosphere'], 'Shown by S-wave shadow'),
        ('Why do we rely on indirect evidence to study the Earth\'s interior?', 'The deepest drilling reaches only a tiny fraction of the depth', ['Interior is visible',
                                                                                                                                                    'Volcanoes show the core', 'Maps show it'],
         'Seismic waves, meteorites, gravity'),
    ]), S(one('cambridge', 11, 'geography', 'demographic transition|population'), 'Population change', [
        ('Natural increase is', 'birth rate minus death rate', ['immigration minus emigration', 'total population', 'death rate minus birth rate'], 'Excludes migration'),
        ('In stage 3 of the DTM,', 'birth rates fall while death rates are low', ['both rates are high', 'death rates rise', 'population falls'], 'Growth slows'),
        ('Why might an anti-natalist policy be introduced?', 'To slow rapid population growth that strains resources', ['To increase births', 'To attract migrants',
                                                                                                                          'To raise death rates'], 'Population control'),
    ]), S(one('ib', 11, 'geography', 'demographic transition|population policies'), 'Population change and policies', [
        ('Natural increase is', 'birth rate minus death rate', ['immigration minus emigration', 'total population', 'death rate minus birth rate'], 'Excludes migration'),
        ('A pro-natalist policy aims to', 'encourage people to have more children', ['reduce births', 'expel migrants', 'raise death rates'], 'Boost fertility'),
        ('Why might a country with an ageing population encourage immigration?', 'Young migrants add workers and taxpayers', ['To reduce the workforce', 'To raise the median age',
                                                                                                                               'To lower tax revenue'], 'Labour supply'),
    ])),
    B(S(one('cbse', 11, 'geography', 'soil formation|mass movement'), 'Soils and mass movement', [
        ('The parent rock from which soil forms is the', 'parent material', ['humus', 'topsoil', 'subsoil'], 'Weathered bedrock'),
        ('A landslide is a type of', 'mass movement', ['weathering', 'deposition by wind', 'glaciation'], 'Downslope movement'),
        ('Why do landslides increase after deforestation on steep slopes?', 'Roots no longer bind the soil, and more water saturates it', ['Trees cause landslides',
                                                                                                                                             'Soil becomes drier', 'Slopes get gentler'],
         'Slope instability'),
    ]), S(one('cambridge', 11, 'geography', 'rural-urban migration|types of migration'), 'Migration', [
        ('Which is a push factor?', 'civil war', ['better schools', 'higher wages', 'a safe environment'], 'Drives people away'),
        ('Internal migration means moving', 'within the same country', ['to another continent', 'across oceans only', 'to space'], 'Within borders'),
        ('Why can rural-urban migration create problems in the countryside?', 'Young adults leave, leaving an ageing population and fewer workers', ['Villages grow quickly',
                                                                                                                                                       'Farms get more labour', 'Birth rates rise'],
         'Rural depopulation'),
    ]), S(one('ib', 11, 'geography', 'international migration|migration'), 'Migration', [
        ('Which is a push factor?', 'civil war', ['better schools', 'higher wages', 'a safe environment'], 'Drives people away'),
        ('Remittances are', 'money sent home by migrants', ['taxes paid by migrants', 'visas', 'airline tickets'], 'Financial flows'),
        ('Why can brain drain slow development in a source country?', 'It loses skilled doctors, engineers and teachers', ['It gains workers', 'It improves hospitals',
                                                                                                                             'It increases taxes'], 'Human capital loss'),
    ])),
]

GEOGRAPHY_CUR_G12 = [
    B(S(one('cbse', 12, 'geography', 'population distribution|density'), 'World population distribution and density', [
        ('Which region of the world is very sparsely populated?', 'the Sahara Desert', ['the Ganga plain', 'eastern China', 'western Europe'], 'Harsh climate'),
        ('Population density is highest where there is', 'fertile land, water and jobs', ['steep mountains', 'ice sheets', 'deserts'], 'Favourable factors'),
        ('Why is the Ganga plain one of the most densely populated regions?', 'Fertile alluvial soil and water support intensive farming and cities',
         ['It is very cold', 'It has no rivers', 'It is mountainous'], 'Physical and human factors'),
    ]), S(one('cambridge', 12, 'geography', 'itcz|causes of tropical climates|tropical climates'), 'Tropical climates', [
        ('The ITCZ is a zone of', 'low pressure where trade winds meet', ['high pressure and drought', 'polar winds', 'cold ocean currents'], 'Intertropical Convergence Zone'),
        ('Humid tropical climates have', 'high temperatures and rainfall all year', ['cold winters', 'little rain', 'snow in summer'], 'Equatorial climate'),
        ('Why do savanna regions have a wet and a dry season?', 'The ITCZ migrates north and south with the seasons', ['They are near the poles', 'Oceans freeze',
                                                                                                                       'Mountains block all rain'], 'Seasonal shift'),
    ]), S(one('ib', 12, 'geography', 'volcanic processes|volcano'), 'Volcanic hazards', [
        ('A volcano formed by layers of ash and lava is a', 'composite (strato) volcano', ['shield volcano', 'fold mountain', 'rift valley'], 'Steep sides'),
        ('Pyroclastic flows are dangerous because they', 'are fast-moving clouds of very hot gas and ash', ['move very slowly', 'are cold', 'are only water'], 'Lethal'),
        ('Why do explosive eruptions occur at destructive boundaries?', 'Viscous, gas-rich magma traps pressure until it bursts', ['Magma is very runny', 'There is no gas',
                                                                                                                                       'Plates move apart'], 'Silica-rich magma'),
    ])),
    B(S(one('cbse', 12, 'geography', 'human development index|human development'), 'Human development', [
        ('The Human Development Index combines', 'health, education and income', ['only income', 'only population', 'only exports'], 'UNDP'),
        ('The concept of human development focuses on', 'expanding people\'s choices and capabilities', ['only economic growth', 'military power', 'land area'],
         'Mahbub ul Haq'),
        ('Why can a country have high GDP but a low HDI?', 'Income is unequally shared and spending on health and education is low', ['HDI ignores health',
                                                                                                                                        'GDP includes education', 'HDI measures only exports'],
         'Growth is not development'),
    ]), S(one('cambridge', 12, 'geography', 'weathering in humid|deep weathering|tropical landforms'), 'Weathering and landforms in the tropics', [
        ('Chemical weathering is rapid in humid tropics because of', 'high temperatures and abundant moisture', ['freezing nights', 'low rainfall', 'strong winds'], 'Fast reactions'),
        ('A tor is', 'an exposed outcrop of weathered granite', ['a sand dune', 'a coral reef', 'a river terrace'], 'Granite landform'),
        ('Why can deep weathering profiles reach tens of metres in the tropics?', 'Long periods of warm, wet conditions without glaciation', ['Frequent glaciers',
                                                                                                                                                'Very dry climate', 'Young rocks only'],
         'Time and climate'),
    ]), S(one('ib', 12, 'geography', 'earthquake processes|earthquake'), 'Earthquake hazards', [
        ('The magnitude of an earthquake measures', 'the energy released', ['the damage caused', 'the number of deaths', 'the depth of the sea'], 'Moment magnitude scale'),
        ('Liquefaction happens when', 'shaking makes saturated soil behave like a liquid', ['lava cools', 'rain stops', 'rocks melt'], 'Secondary hazard'),
        ('Why can a smaller earthquake cause more deaths than a larger one?', 'Building quality, population density and preparedness differ', ['Smaller quakes release more energy',
                                                                                                                                                  'Deaths depend only on magnitude', 'Larger quakes are always deeper'],
         'Vulnerability'),
    ])),
    B(S(one('cbse', 12, 'geography', 'types of agriculture|agriculture'), 'Primary activities: agriculture', [
        ('Growing a single cash crop on a large estate is', 'plantation agriculture', ['shifting cultivation', 'nomadic herding', 'subsistence farming'], 'Tea, rubber, coffee'),
        ('Shifting cultivation involves', 'clearing land, farming it for a few years, then moving on', ['farming the same plot forever', 'growing crops in greenhouses',
                                                                                                         'fishing'], 'Slash and burn'),
        ('Why is intensive subsistence farming common in monsoon Asia?', 'High population density and small farms need high yields per hectare',
         ['Land is abundant', 'Few people live there', 'Rainfall is very low'], 'Labour-intensive'),
    ]), S(one('cambridge', 12, 'geography', 'tropical rainforest|rainforest'), 'Tropical rainforest ecosystems', [
        ('The tallest trees that rise above the canopy are', 'emergents', ['understorey', 'shrub layer', 'leaf litter'], 'Top layer'),
        ('Most nutrients in a tropical rainforest are stored in the', 'biomass', ['soil', 'rock', 'atmosphere'], 'Rapid recycling'),
        ('Why do soils become infertile soon after rainforest is cleared?', 'Heavy rain leaches nutrients once the biomass is removed', ['Rain adds nutrients',
                                                                                                                                          'Soil becomes thicker', 'Trees stole the nutrients'],
         'Nutrient cycle broken'),
    ]), S(one('ib', 12, 'geography', 'hazard risk equation|vulnerability'), 'Hazard risk and vulnerability', [
        ('Risk is often expressed as', 'hazard x vulnerability', ['hazard ÷ population', 'magnitude + depth', 'wealth x area'], 'Risk equation'),
        ('Which group is often most vulnerable in a disaster?', 'the elderly and poor', ['wealthy adults', 'tourists in hotels', 'government officials'], 'Fewer resources'),
        ('Why might people continue living near an active volcano?', 'Fertile soils, jobs and attachment to home outweigh perceived risk', ['They cannot see it',
                                                                                                                                              'Volcanoes are always safe', 'Law forbids moving'],
         'Hazard perception'),
    ])),
    B(S(one('cbse', 12, 'geography', 'manufacturing|secondary'), 'Secondary activities: manufacturing', [
        ('Manufacturing converts', 'raw materials into finished goods', ['goods into services', 'money into land', 'water into rain'], 'Adds value'),
        ('Footloose industries are', 'not tied to raw material locations', ['always near coal', 'only in villages', 'banned in cities'], 'Electronics, software'),
        ('Why do high-tech industries cluster near universities?', 'They need skilled workers and research links', ['Universities give free land', 'They need iron ore',
                                                                                                                       'They avoid skilled labour'], 'Knowledge economy'),
    ]), S(one('cambridge', 12, 'geography', 'waves|coastal processes'), 'Coastal processes', [
        ('Waves that build up beaches are', 'constructive waves', ['destructive waves', 'tsunamis only', 'tidal bores'], 'Strong swash'),
        ('Longshore drift moves sediment', 'along the coast', ['out to sea only', 'inland', 'into the sky'], 'Swash at an angle'),
        ('Why can building groynes on one beach increase erosion further along the coast?', 'They trap sediment, starving beaches down-drift',
         ['They add sand everywhere', 'They stop waves', 'They raise sea level'], 'Sediment budget'),
    ]), S(one('ib', 12, 'geography', 'pre-event management|resilience'), 'Building resilience to hazards', [
        ('A hazard map shows', 'areas at risk from a hazard', ['road traffic only', 'school locations only', 'rainfall totals'], 'Planning tool'),
        ('Which is a pre-event strategy?', 'earthquake-resistant building codes', ['emergency rescue', 'rebuilding homes', 'insurance payouts'], 'Before the event'),
        ('Why is community preparedness often as important as technology?', 'People who know what to do act faster and save lives', ['Technology always fails',
                                                                                                                                       'Communities cause hazards', 'Preparedness is costly'],
         'Human response'),
    ])),
]
