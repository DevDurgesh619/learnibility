"""IB MYP 5 Language and Literature (English) – ib-g10-english.

MYP 5 ends with the on-screen eAssessment (2 hours): Task 1 analysis and comparison of unseen texts, Task 2
creative writing from visual prompts. Work is assessed on criteria A Analysing, B Organising, C Producing text and
D Using language (each 0-8). The six mocks follow the eAssessment shape (see MOCK below).

Passages are ORIGINAL unless attributed. Brief public-domain quotations only: Shakespeare (Macbeth), Abraham Lincoln
(Gettysburg Address, 1863), Sojourner Truth (1851 speech as recorded by Frances Gage, 1863) and Percy Bysshe Shelley
("The Mask of Anarchy", 1819; "Ozymandias", 1818). Famous modern speeches and novels are referred to only in general
terms. Shared builders and the shared passage library: ib_myp_english_common.py.
"""
from __future__ import annotations

from _common import F, Registry, T, mcq  # noqa: F401
from ib_myp_english_common import (AUD_Q, CHAR_Q, CRIT_A, CRIT_ALL, CRIT_AN, CRIT_B, CRIT_CR, CRIT_OPEN, CRIT_W, DEV_Q,  # noqa: F401
                                   KCONV_Q, LIFE, LIT, MEDIA, MOOD_Q, NARR, NONLIT, PERSUADE, POV_Q, PROSE, PURP_Q, STRUCT_Q,
                                   STYLE, SUM_Q, THEME_Q, TONE_Q, VIS_Q, VISUAL, Kit, add_shared, mock_sections)

CONFIG = {'minutesPerMark': 1.5, 'mcqMinutes': 1.5}

# MYP 5 eAssessment-style mock: Task 1 analysis 30 marks (two short analyses + a 20-mark comparison); Task 2 creative
# writing (50 marks on the real paper) scaled to 30 because one item may carry at most 20 marks. 60 marks per mock.
MOCK = mock_sections(t1_chapters=[6, 12], t2_chapters=[10, 12])

R = Registry()
K = Kit(R)
add_shared(K)
P, pq, qa, para, write = K.P, K.pq, K.qa, K.para, K.write
GLOBAL = K.mock_templates()


def init(subject_id):
    pass


def templates(st):
    return R.build(st, STYLE) + GLOBAL


def H(key, **kw):
    R.facts(key, F(**kw))


# =============================================================================================
# Grade 10 passages – speeches
# =============================================================================================
P(id='speech_reef', kind='speech', title='speech by a 16-year-old student to a regional climate summit',
  text=("Delegates, I was born the year the reef first turned white. I am sixteen now, and I have watched it bleach four more times.\n"
        "You have heard the science. You have seen the graphs. You have nodded at the statistics.\n"
        "So let me ask you a simpler question: what will you tell my children when they ask what coral looked like?\n"
        "We do not need more promises. We need decisions – today, in this room, before the tide goes out on our future."),
  appeals='Ethos: the speaker\'s own life ("born the year the reef first turned white") gives her authority as a witness. Pathos: the image of her future children asking what coral looked like creates guilt and grief. Logos: the reference to science, graphs and statistics reminds delegates that the evidence is already settled.',
  context='Audience: adult delegates and decision-makers at a climate summit, who hold power the young speaker lacks. Purpose: to shame and persuade them to act now. Context: the speech belongs to a tradition of young climate activists addressing world leaders.',
  dev=[('tricolon with anaphora', 'You have heard the science. You have seen the graphs. You have nodded at the statistics.', 'the repeated "You have" builds a rhythm that piles up the delegates\' inaction, ending on the dismissive verb "nodded"', ['simile', 'onomatopoeia', 'oxymoron']),
       ('rhetorical question', 'what will you tell my children when they ask what coral looked like?', 'the unanswerable question forces delegates to imagine a future without coral and to feel personally responsible', ['statistic', 'simile', 'alliteration']),
       ('antithesis', 'We do not need more promises. We need decisions', 'the balanced contrast exposes the gap between words and action and makes the demand memorable', ['hyperbole', 'onomatopoeia', 'personification']),
       ('metaphor', 'before the tide goes out on our future', 'the sea image links her future to the ocean she is defending and suggests time is running out', ['simile', 'statistic', 'rhetorical question'])],
  struct=[('the move from personal anecdote to direct challenge to a final demand', 'the speech builds from a story that earns sympathy to an accusation and finally a call to action, so the audience is led step by step to the conclusion'),
          ('the short final paragraph', 'ending on "today, in this room" makes the demand immediate and specific')],
  tone='urgent and accusatory', tw=['light-hearted', 'neutral', 'nostalgic'], tonex='direct address, repetition and the challenge to "you" create urgency and blame.',
  aud='Adult delegates and policymakers at a climate summit, addressed directly as "Delegates" and "you".',
  purp='To persuade decision-makers to stop promising and start acting on climate change immediately.',
  vocab=[('bleach', 'lose colour and turn white (here, coral dying from heat stress)', ['grow quickly', 'be cleaned', 'move away'], 'it turns a scientific process into a visible, painful image of loss.')],
  theme='intergenerational responsibility for the environment',
  gq='How does the speaker use rhetoric to persuade her audience to act?',
  gqa='She opens with ethos – her own lifetime measured in bleaching events – which makes her a credible witness. The tricolon "You have heard ... seen ... nodded" builds a rhythm of inaction ending on the dismissive "nodded". A rhetorical question about her future children creates pathos and guilt, and the antithesis "We do not need more promises. We need decisions" crystallises her demand. The closing metaphor "before the tide goes out on our future" ties urgency to the ocean itself.',
  write=[('Write a 300-word response to this speech from the perspective of a delegate who agrees but faces economic pressure. Address the student directly.', 'Indicative content: respectful direct address; acknowledges her points; explains constraints honestly; proposes concrete action; rhetorical devices (e.g. antithesis, inclusive "we"); formal register.')],
  summary='A sixteen-year-old tells summit delegates that she has watched the reef bleach repeatedly, accuses them of inaction despite the evidence, and demands decisions today.')

P(id='speech_lincoln', kind='speech', title='extract from the Gettysburg Address (1863) by Abraham Lincoln',
  text=("Four score and seven years ago our fathers brought forth on this continent, a new nation, conceived in Liberty, and dedicated to the proposition that all men are created equal. ...\n"
        "But, in a larger sense, we can not dedicate—we can not consecrate—we can not hallow—this ground. ...\n"
        "It is rather for us to be here dedicated to the great task remaining before us ... that this nation, under God, shall have a new birth of freedom—and that government of the people, by the people, for the people, shall not perish from the earth."),
  appeals='Ethos: as President, Lincoln speaks for the nation and links himself to "our fathers", the founders. Pathos: the dead soldiers are honoured as having made the ground sacred, stirring grief and duty. Logos: he reasons from the founding "proposition that all men are created equal" to the conclusion that the war must be finished.',
  context='Context: delivered on 19 November 1863 at the dedication of a military cemetery at Gettysburg, Pennsylvania, during the American Civil War, months after a battle in which thousands died. Audience: a grieving crowd and, through newspapers, the whole Union. Purpose: to honour the dead and redefine the war as a struggle for equality and democracy.',
  dev=[('tricolon', 'we can not dedicate—we can not consecrate—we can not hallow—this ground', 'the three verbs rise in holiness, suggesting that the soldiers\' sacrifice has already made the ground sacred beyond any speech', ['simile', 'onomatopoeia', 'oxymoron']),
       ('tricolon with repetition', 'government of the people, by the people, for the people', 'the repeated "the people" places ordinary citizens at the heart of democracy and gives the ending a memorable rhythm', ['metaphor', 'hyperbole', 'rhetorical question']),
       ('formal, archaic register', 'Four score and seven years ago', 'the biblical counting ("score" = twenty) lends solemnity and links the nation\'s founding to scripture', ['slang', 'onomatopoeia', 'colloquial language']),
       ('extended metaphor of birth', 'brought forth ... conceived in Liberty ... a new birth of freedom', 'the nation is presented as a living thing that was born and can be reborn, giving hope after death', ['simile', 'statistic', 'alliteration'])],
  struct=[('the movement from past ("Four score ... ago") to present ("this ground") to future ("shall not perish")', 'the speech travels through time, turning mourning into a commitment for the future'),
          ('its brevity', 'at around 270 words in full, the speech\'s concision makes every phrase weighty and memorable')],
  tone='solemn and resolute', tw=['comic', 'casual', 'bitter'], tonex='formal, biblical language and the commitment "shall not perish" create solemn determination.',
  aud='A grieving crowd at the dedication of a soldiers\' cemetery and, through the press, the citizens of the Union.',
  purp='To honour the soldiers who died and to persuade listeners to dedicate themselves to finishing the war for freedom and democracy.',
  vocab=[('consecrate', 'make holy or sacred', ['build on', 'measure', 'forget'], 'it gives the battlefield a religious significance.'),
         ('perish', 'die or be destroyed', ['grow', 'be elected', 'travel'], 'the word raises the stakes to the survival of democracy itself.')],
  theme='sacrifice and the survival of democracy',
  gq='How does Lincoln use language and structure to give meaning to the soldiers\' deaths?',
  gqa='Lincoln moves from the nation\'s birth ("Four score and seven years ago") to the present battlefield and a future "new birth of freedom", so the deaths become part of a larger story. The rising tricolon "dedicate ... consecrate ... hallow" suggests the soldiers have already made the ground sacred, and the archaic, biblical register lends solemnity. The famous final tricolon "of the people, by the people, for the people" turns grief into a shared democratic duty.',
  summary='Lincoln recalls the nation\'s founding on equality, says the soldiers have made the ground sacred, and urges the living to finish their work so democracy survives.')

P(id='speech_truth', kind='speech', title='extract from Sojourner Truth\'s 1851 speech at a women\'s rights convention in Akron, Ohio, as recorded by Frances Gage in 1863',
  text=("That man over there says that women need to be helped into carriages, and lifted over ditches, and to have the best place everywhere. Nobody ever helps me into carriages, or over mud-puddles, or gives me any best place! And ain't I a woman?\n"
        "Look at me! Look at my arm! I have ploughed and planted, and gathered into barns, and no man could head me! And ain't I a woman?"),
  appeals='Ethos: Truth\'s authority comes from her own life as a formerly enslaved labourer ("Look at my arm!"). Pathos: the contrast between pampered white women and her own treatment provokes indignation. Logos: she refutes the opponent\'s claim with evidence from her own experience – if women are weak, how could she do a man\'s work?',
  context='Context: Sojourner Truth, who had escaped slavery, spoke at a women\'s rights convention in 1851. This famous version was published by Frances Gage twelve years later; an earlier 1851 newspaper report records different wording and no refrain, so historians treat Gage\'s text with caution. Audience: convention delegates, including men who opposed women\'s rights.',
  dev=[('refrain (epistrophe)', 'And ain\'t I a woman?', 'the repeated rhetorical question hammers home that Black women were excluded from society\'s idea of womanhood', ['simile', 'statistic', 'onomatopoeia']),
       ('refutation of an opponent', 'That man over there says that women need to be helped into carriages', 'she quotes the opposing argument and then demolishes it with her own experience', ['flashback', 'simile', 'personification']),
       ('imperatives and direct address', 'Look at me! Look at my arm!', 'the commands make her body the evidence and force the audience to confront her strength', ['euphemism', 'simile', 'understatement']),
       ('listing (polysyndeton)', 'I have ploughed and planted, and gathered into barns', 'the repeated "and" piles up her labour, proving she is as strong as any man', ['oxymoron', 'onomatopoeia', 'pun'])],
  struct=[('the pattern of claim, counter-evidence, refrain', 'each section ends with the same question, so the argument grows stronger with each repetition'),
          ('beginning with "That man over there"', 'opening by pointing at an opponent makes the speech feel spontaneous and confrontational')],
  tone='defiant', tw=['apologetic', 'detached', 'sentimental'], tonex='exclamations, commands and the challenging refrain create a bold, defiant tone.',
  aud='Delegates at an 1851 women\'s rights convention, including men who argued that women were too delicate for equal rights.',
  purp='To expose the hypocrisy of arguments that women are weak and to claim womanhood and rights for Black women.',
  vocab=[('head', 'do better than or beat (an older use)', ['injure', 'lead into a room', 'listen to'], 'it shows she matched or out-worked men in the fields.')],
  theme='intersection of race and gender in the fight for rights',
  gq='How does the speaker challenge her opponents\' view of women?',
  gqa='She begins by quoting "That man over there", then refutes his claim that women need to be "helped into carriages" with her own contrasting experience. The refrain "And ain\'t I a woman?" repeatedly forces the audience to admit that their idea of womanhood excludes Black women. Imperatives ("Look at my arm!") make her body the evidence, and the polysyndeton "ploughed and planted, and gathered" piles up proof of her strength. Readers should note that this wording comes from Gage\'s 1863 version.',
  summary='Truth contrasts the claim that women need help and protection with her own life of hard labour and repeatedly asks whether she, too, is not a woman.')

P(id='speech_captain', kind='speech', title='speech by a candidate for school captain to a Year 10 assembly',
  text=("Good morning, Year 10. I'm not going to promise you a swimming pool, a four-day week or free pizza on Fridays. (I asked. The answer was no.)\n"
        "What I will promise is this: a student council that actually meets, a suggestion box that someone actually opens, and a captain who actually listens.\n"
        "Last year, ninety of us signed the petition for water fountains on the top floor. Nothing happened. This year, let's make something happen.\n"
        "Vote Amira. Because \"actually\" is a promise I can keep."),
  appeals='Ethos: honesty and humour ("I asked. The answer was no.") make Amira seem trustworthy and down to earth. Logos: the petition statistic gives evidence that students have been ignored. Pathos: the inclusive "let\'s" invites shared frustration and hope.',
  context='Audience: Year 10 students, who are sceptical of empty election promises. Purpose: to win votes by contrasting realistic promises with unrealistic ones. Context: a school election where speeches are short and delivered live.',
  dev=[('humorous tricolon', 'a swimming pool, a four-day week or free pizza on Fridays', 'listing absurd promises mocks typical campaign speeches and wins laughter and goodwill', ['statistic', 'oxymoron', 'onomatopoeia']),
       ('repetition', 'a student council that actually meets, a suggestion box that someone actually opens, and a captain who actually listens', 'the repeated "actually" suggests previous promises were empty and makes hers seem sincere', ['simile', 'personification', 'flashback']),
       ('statistic as evidence', 'ninety of us signed the petition', 'a specific number proves the problem is real and widely felt', ['metaphor', 'rhetorical question', 'alliteration']),
       ('callback ending', 'Because "actually" is a promise I can keep.', 'returning to the key word makes the conclusion memorable and neat', ['cliffhanger', 'simile', 'onomatopoeia'])],
  struct=[('the move from humour to evidence to a call to action', 'humour wins attention, evidence earns trust and the imperative "Vote Amira" closes the deal')],
  tone='witty and sincere', tw=['furious', 'mournful', 'detached'], tonex='self-deprecating humour combined with realistic promises creates a likeable, sincere tone.',
  aud='Year 10 students at a school assembly, addressed as "Year 10" and included through "us" and "let\'s".',
  purp='To persuade fellow students to vote for Amira as school captain.',
  theme='trust and honesty in leadership',
  gq='How does the speaker try to win the trust of her audience?',
  gqa='Amira mocks typical empty promises with a humorous tricolon ("a swimming pool, a four-day week or free pizza") and the aside "(I asked. The answer was no.)", which makes her seem honest. The repeated "actually" implies earlier promises were empty while hers are realistic. The petition statistic gives logos, the inclusive "let\'s" builds solidarity, and the callback ending on "actually" makes her message memorable.',
  write=[('Write the opposing candidate\'s 250-word speech, delivered straight after Amira\'s. Use at least three rhetorical devices and respond to her points.', 'Indicative content: direct address to Year 10; acknowledges Amira; offers distinct promises; rhetorical devices (tricolon, rhetorical question, anecdote); clear call to action; register suited to peers.')],
  summary='Amira refuses to make unrealistic promises, pledges a council, suggestion box and captain that "actually" work, cites an ignored petition and asks for votes.')

P(id='speech_mayor', kind='speech', title='speech by a town mayor one week after a flood',
  text=("A week ago the river came into our homes without knocking. It took photographs, furniture, a school library and, for some of us, the feeling of being safe.\n"
        "But it did not take this town.\n"
        "I have seen teenagers carrying sandbags at midnight. I have seen a baker giving away every loaf. I have seen neighbours who had never spoken sharing one kettle on one camping stove.\n"
        "We will rebuild. Not because it is easy, but because it is ours."),
  appeals='Pathos: personification of the river and the list of losses evoke grief, while images of kindness evoke pride. Ethos: the mayor speaks as an eyewitness ("I have seen"). The speech uses little logos; its aim is to unite rather than to argue.',
  context='Audience: residents of a town recovering from a flood, many of whom have lost homes or belongings. Purpose: to comfort, unite and encourage recovery. Context: a speech delivered soon after a disaster, when people need hope and leadership.',
  dev=[('personification', 'the river came into our homes without knocking', 'the river becomes an intruder, making the disaster feel like a violation of home', ['simile', 'statistic', 'onomatopoeia']),
       ('anaphora', 'I have seen teenagers ... I have seen a baker ... I have seen neighbours', 'the repeated eyewitness phrase builds a montage of kindness and the mayor\'s credibility', ['oxymoron', 'flashback', 'pun']),
       ('one-line paragraph', 'But it did not take this town.', 'isolated after the list of losses, the line marks a turning point from grief to defiance', ['simile', 'rhetorical question', 'hyperbole']),
       ('antithesis', 'Not because it is easy, but because it is ours.', 'the balanced contrast turns difficulty into a reason for pride and ownership', ['alliteration', 'onomatopoeia', 'simile'])],
  struct=[('the shift from loss to community to resolve', 'the speech mirrors the town\'s emotional journey, from grief through pride to determination')],
  tone='consoling and resolute', tw=['sarcastic', 'neutral', 'panicked'], tonex='gentle images of loss give way to proud, determined statements.',
  aud='Residents of a flooded town, addressed through the inclusive "our" and "us".',
  purp='To comfort residents, celebrate their solidarity and commit the town to rebuilding.',
  vocab=[('rebuild', 'build again after damage or destruction', ['decorate', 'sell', 'move away from'], 'it is literal (houses) and figurative (community and confidence).')],
  theme='community resilience after disaster',
  gq='How does the mayor use language to move the audience from grief to hope?',
  gqa='Personification ("came into our homes without knocking") presents the flood as an intruder and the list of losses ends on the emotional "the feeling of being safe". The isolated line "But it did not take this town" marks a turning point. Anaphora ("I have seen ...") builds a montage of kindness that gives the mayor eyewitness ethos, and the closing antithesis "Not because it is easy, but because it is ours" turns hardship into pride.',
  summary='A mayor recalls what the flood took, insists it did not destroy the town, describes acts of kindness he has seen and promises that the town will rebuild.')

# =============================================================================================
# Coming-of-age extracts
# =============================================================================================
P(id='coa_shipyard', kind='prose', title='extract from a coming-of-age novel set in a shipbuilding town in 1980s Britain',
  text=("I was twelve the summer my father stopped going to the yard, though nobody used the word \"redundant\" in our house. He said he was \"between ships\".\n"
        "Every morning he still put on his work boots. He walked me to the bus stop, then kept walking – to the river, I found out later, where he stood for hours watching the empty cranes.\n"
        "I thought he was the bravest man in the world. I know now that bravery and pride can look exactly the same from the height of a twelve-year-old."),
  pov='Retrospective first-person narration: an adult narrator looks back on being twelve. The gap between what the child believed ("the bravest man in the world") and what the adult knows creates poignancy and dramatic irony.',
  retro='The adult narrator signals hindsight with "I found out later" and "I know now", so the reader sees both the child\'s innocent view and the adult\'s understanding of the father\'s shame.',
  context='Historical and social context: in 1980s Britain many shipyards and heavy industries closed, leaving whole communities unemployed. Men like the father often felt shame, and families avoided words like "redundant".',
  char='The father is proud and ashamed: he keeps up appearances by wearing work boots and using the euphemism "between ships". The narrator is protected and naive as a child but reflective as an adult.',
  dev=[('euphemism', '"between ships"', 'the father\'s phrase hides the painful truth of unemployment and shows his pride', ['hyperbole', 'onomatopoeia', 'oxymoron']),
       ('symbolism', 'the empty cranes', 'the idle cranes symbolise the death of the industry and the father\'s lost purpose', ['simile', 'statistic', 'alliteration']),
       ('reflective final sentence', 'bravery and pride can look exactly the same from the height of a twelve-year-old', 'the adult narrator re-reads the past, showing how growing up changes understanding', ['cliffhanger', 'rhetorical question', 'onomatopoeia'])],
  struct=[('the shift from past events to the present-tense reflection "I know now"', 'the final line reframes everything before it, turning a child\'s memory into an adult\'s insight')],
  tone='tender and rueful', tw=['comic', 'angry', 'triumphant'], tonex='affectionate memories are tinged with the adult\'s regretful understanding.',
  vocab=[('redundant', 'no longer employed because the job is no longer needed', ['repeated too often', 'very brave', 'retired with honour'], 'the family\'s avoidance of the word shows the shame attached to it.')],
  theme='growing up and seeing parents clearly',
  gq='How does the writer use a retrospective narrator to present the father?',
  gqa='The adult narrator looks back on being twelve, so the reader sees two views at once. The child accepts the euphemism "between ships" and the ritual of the work boots, but hindsight phrases ("I found out later", "I know now") reveal the father\'s hidden shame. The symbol of the "empty cranes" connects his loss to the collapse of the industry, and the final sentence, contrasting "bravery and pride", shows how growing up changes the narrator\'s understanding.',
  write=[('Rewrite the extract from the father\'s point of view, standing by the river (about 250 words).', 'Indicative content: first-person father; interior thoughts about shame and pride; the cranes as symbol; his decision to hide the truth from his child; consistent voice and period detail.')],
  summary='An adult recalls being twelve when his father lost his shipyard job; the father pretended to go to work but watched the empty cranes, and the narrator now sees pride where he once saw bravery.')

P(id='coa_results', kind='prose', title='extract from a young-adult novel about exam results day',
  text=("Mei read the email three times. A, A, B. The B sat at the end of the line like a stone in a shoe.\n"
        "Downstairs, her mother was already on the phone to Auntie Lin, laughing her company laugh. \"Of course she did well,\" she was saying. \"Mei always does well.\"\n"
        "Mei closed the laptop. She thought about the art portfolio hidden under her bed – the one nobody had asked to see – and, for the first time, she wondered whose results these really were."),
  pov='Third-person limited narration stays close to Mei\'s thoughts and perceptions, so the reader shares her private disappointment and doubt while the mother\'s public confidence is heard only from a distance.',
  char='Mei is dutiful but beginning to question the expectations placed on her; the hidden art portfolio reveals a secret identity. Her mother is proud and image-conscious ("her company laugh").',
  dev=[('simile', 'The B sat at the end of the line like a stone in a shoe', 'the small but painful image shows how one grade spoils her sense of success', ['metaphor', 'onomatopoeia', 'hyperbole']),
       ('characterising detail', 'her company laugh', 'the phrase suggests the mother performs happiness for others, hinting at pressure and appearances', ['alliteration', 'statistic', 'pun']),
       ('symbolism', 'the art portfolio hidden under her bed', 'the hidden portfolio symbolises the part of Mei\'s identity that her family has not seen', ['flashback', 'simile', 'onomatopoeia']),
       ('rhetorical final thought', 'she wondered whose results these really were', 'the question marks the start of Mei\'s growing independence, a key coming-of-age moment', ['cliffhanger', 'hyperbole', 'statistic'])],
  struct=[('the contrast between upstairs (Mei) and downstairs (her mother)', 'the physical separation mirrors the emotional gap between their views of success')],
  tone='quietly unsettled', tw=['jubilant', 'farcical', 'furious'], tonex='restrained description and an open question suggest growing unease.',
  theme='identity and parental expectations',
  gq='How does the writer present Mei\'s changing sense of identity?',
  gqa='Close third-person narration shares Mei\'s view: the simile "like a stone in a shoe" shows the pressure she feels over one grade. Her mother\'s "company laugh" and "Mei always does well" reveal expectations performed for others. The hidden art portfolio symbolises a self nobody has asked to see, and the closing thought "whose results these really were" marks the beginning of her independence.',
  write=[('Write Mei\'s diary entry that evening (about 250 words), in which she decides whether to show her mother the portfolio.', 'Indicative content: diary conventions; first-person reflective voice; conflicting feelings of duty and desire; reference to the portfolio and the phone call; a decision or open ending; informal but controlled register.')],
  summary='Mei receives good results with one B, hears her mother boasting on the phone and, thinking of her hidden art portfolio, wonders whose achievements they really are.')

P(id='coa_court', kind='prose', title='extract from a coming-of-age novel in which the narrator attends her brother\'s trial',
  text=("The courtroom was smaller than the ones on television, and quieter. Nobody shouted \"Objection!\".\n"
        "Danny sat in a suit that belonged to our uncle. The sleeves covered his hands. He looked about nine.\n"
        "When the lawyer called him \"the defendant\", I wanted to stand up and say his name. His name is Danny. He is scared of moths. He taught me to ride a bike.\n"
        "I didn't stand up. That was the day I learned that justice is a room where you are not allowed to speak."),
  pov='First-person narration by the younger sister gives an outsider\'s, emotional view of the legal process; the reader feels her powerlessness.',
  char='Danny is presented as vulnerable and childlike ("He looked about nine"), not as a criminal. The narrator is loving and protective but silenced.',
  dev=[('contrast with expectation', 'smaller than the ones on television, and quieter', 'the anticlimax shows that real justice is ordinary and intimidating rather than dramatic', ['simile', 'onomatopoeia', 'hyperbole']),
       ('telling detail', 'The sleeves covered his hands.', 'the oversized borrowed suit makes Danny look small and childlike, building sympathy', ['metaphor', 'statistic', 'rhetorical question']),
       ('list of short sentences', 'His name is Danny. He is scared of moths. He taught me to ride a bike.', 'the simple personal facts restore Danny\'s humanity against the label "the defendant"', ['oxymoron', 'alliteration', 'flashback']),
       ('metaphor', 'justice is a room where you are not allowed to speak', 'the final metaphor sums up her disillusionment: the system silences those who love the accused', ['simile', 'onomatopoeia', 'pun'])],
  struct=[('the closing generalisation "That was the day I learned"', 'the specific scene becomes a turning point in her understanding of the adult world')],
  tone='bitter and tender', tw=['triumphant', 'comic', 'indifferent'], tonex='love for Danny mixes with disillusionment at the system.',
  theme='justice, innocence and growing up',
  gq='How does the writer present the narrator\'s experience of justice?',
  gqa='The narrator\'s expectations are undercut ("smaller than the ones on television"), showing justice as quiet and intimidating. Details like the borrowed suit whose "sleeves covered his hands" make Danny vulnerable, and the list of short sentences ("He is scared of moths") restores his humanity against the cold label "the defendant". The closing metaphor "justice is a room where you are not allowed to speak" shows her loss of innocence and sense of powerlessness.',
  summary='At her brother Danny\'s trial, the narrator sees him small in a borrowed suit, wants to tell the court who he really is, stays silent, and learns that justice can silence people.')

P(id='coa_lake', kind='prose', title='extract from a novel that follows its main character from childhood to adolescence',
  text=("At eleven, Ama would not go past the jetty. The lake was too dark, and her grandmother had told her about the river spirit who collected disobedient children.\n"
        "At fourteen, she swam to the jetty and back every evening, counting strokes to keep the fear quiet.\n"
        "At sixteen, the summer her grandmother died, Ama swam out past the last buoy, turned on her back and floated, looking up at a sky that seemed, for the first time, to belong to her.\n"
        "She did not count."),
  char='Ama develops from a fearful child obeying her grandmother\'s stories to a confident young woman who claims her own freedom; the change is shown through her relationship with the lake.',
  pov='Third-person narration, moving through time in jumps, lets the reader watch Ama\'s development from outside while staying close to her feelings.',
  dev=[('time markers as structure', 'At eleven ... At fourteen ... At sixteen', 'the repeated pattern compresses years into a few lines and makes the stages of growing up clear', ['flashback', 'onomatopoeia', 'simile']),
       ('motif', 'counting strokes to keep the fear quiet', 'counting shows her controlling fear; when "She did not count" the motif marks her freedom', ['hyperbole', 'oxymoron', 'alliteration']),
       ('symbolism', 'swam out past the last buoy', 'the last buoy marks the limit of safety; passing it symbolises leaving childhood boundaries behind', ['simile', 'statistic', 'personification']),
       ('one-line paragraph', 'She did not count.', 'the short final line marks the climax of her development quietly but powerfully', ['rhetorical question', 'cliffhanger', 'simile'])],
  struct=[('the three-stage time structure', 'the repeated "At ..." pattern lets the reader track change across years in a very short space')],
  tone='quietly triumphant', tw=['menacing', 'comic', 'bitter'], tonex='calm description and the final freedom suggest a hard-won confidence.',
  vocab=[('buoy', 'a floating marker in water that shows a boundary or danger', ['a small boat', 'a fishing net', 'a wave'], 'it becomes a symbol of the limits Ama finally passes.')],
  theme='growing up as overcoming fear and claiming independence',
  gq='How does the writer show Ama\'s development across the extract?',
  gqa='The structure – "At eleven ... At fourteen ... At sixteen" – compresses Ama\'s growth into three stages. At first she obeys her grandmother\'s story about the river spirit; then she controls her fear by "counting strokes"; finally, after her grandmother\'s death, she swims "past the last buoy", symbolically leaving childhood limits behind. The sky that "seemed ... to belong to her" and the one-line ending "She did not count." show her new freedom.',
  summary='Ama goes from refusing to pass the jetty at eleven, to swimming there while counting strokes at fourteen, to swimming past the last buoy without counting at sixteen after her grandmother\'s death.')

# =============================================================================================
# Poetry of conflict and protest
# =============================================================================================
P(id='shelley_mask', kind='poem', title='final stanza of "The Mask of Anarchy" (1819) by Percy Bysshe Shelley',
  text=("Rise like Lions after slumber\n"
        "In unvanquishable number—\n"
        "Shake your chains to earth like dew\n"
        "Which in sleep had fallen on you—\n"
        "Ye are many—they are few."),
  context='Context: Shelley wrote the poem after the Peterloo Massacre (Manchester, August 1819), when cavalry charged a peaceful crowd demanding parliamentary reform, killing at least fifteen people. It was considered too radical to publish until 1832.',
  form='Form: rhyming couplets and a final triplet (slumber/number, dew/you/few) in a strong trochaic rhythm, giving the stanza the force of a chant or rallying cry.',
  persp='Perspective: Shelley speaks directly to ordinary working people, urging peaceful but determined resistance; he presents oppression as something that can be shaken off easily if people recognise their strength.',
  dev=[('simile', 'Rise like Lions after slumber', 'the people are compared to powerful, sleeping lions, suggesting their strength has only been dormant', ['metaphor', 'onomatopoeia', 'oxymoron']),
       ('simile', 'Shake your chains to earth like dew', 'comparing chains to light dew suggests oppression can be shaken off easily once people wake up', ['hyperbole', 'alliteration', 'pun']),
       ('antithesis', 'Ye are many—they are few.', 'the stark contrast makes the people\'s numerical power obvious and memorable', ['simile', 'personification', 'statistic']),
       ('imperatives', 'Rise ... Shake', 'the commands give the poem the urgency of a call to action', ['euphemism', 'onomatopoeia', 'flashback'])],
  struct=[('the closing antithesis', 'ending on "Ye are many—they are few" leaves the reader with a clear, chantable message')],
  tone='rousing', tw=['melancholy', 'resigned', 'whimsical'], tonex='imperatives, strong rhythm and images of lions create a rousing, defiant tone.',
  vocab=[('unvanquishable', 'impossible to defeat', ['very loud', 'unknown', 'tired'], 'it insists that the people, united, cannot be beaten.'),
         ('slumber', 'sleep', ['anger', 'hunger', 'battle'], 'it implies the people\'s power is only resting, not absent.')],
  theme='the power of ordinary people to resist oppression',
  gq='How does Shelley use language and form to inspire his readers to resist?',
  gqa='The imperatives "Rise" and "Shake" make the stanza a call to action. The simile "like Lions after slumber" presents the people as powerful but dormant, and the simile of chains like "dew" suggests oppression can be shaken off easily. Rhyming couplets and a strong rhythm give it the force of a chant, and the final antithesis "Ye are many—they are few" sums up the people\'s strength in numbers. Written after Peterloo (1819), the stanza turns a massacre into a rallying cry.',
  summary='Shelley urges ordinary people to rise like waking lions, shake off their chains like dew and remember that they are many and their oppressors few.')

P(id='ozymandias', kind='poem', title='final lines of the sonnet "Ozymandias" (1818) by Percy Bysshe Shelley',
  text=("And on the pedestal, these words appear:\n"
        "My name is Ozymandias, King of Kings;\n"
        "Look on my Works, ye Mighty, and despair!\n"
        "Nothing beside remains. Round the decay\n"
        "Of that colossal Wreck, boundless and bare\n"
        "The lone and level sands stretch far away."),
  form='Form: the lines come from a sonnet in iambic pentameter with an unusual, interlocking rhyme scheme; the volta turns from the tyrant\'s boast to the emptiness around it. Enjambement ("Round the decay / Of that colossal Wreck") makes the sands seem to stretch across the line break.',
  persp='Perspective: through the image of a ruined statue, Shelley mocks tyrants\' belief that their power will last; time and nature defeat all rulers.',
  context='Context: written in 1817–18, inspired by news of an ancient Egyptian statue (of Ramesses II, called Ozymandias by the Greeks) being brought to London; Shelley was a radical opponent of tyranny.',
  dev=[('irony', 'Look on my Works, ye Mighty, and despair! / Nothing beside remains.', 'the king\'s boast is undercut by the empty desert: the "Mighty" should despair not at his power but at its disappearance', ['simile', 'onomatopoeia', 'hyperbole only']),
       ('caesura', 'Nothing beside remains. Round the decay', 'the full stop mid-line creates a stark pause after the boast, like silence falling', ['enjambement', 'rhyme', 'refrain']),
       ('alliteration', 'boundless and bare / The lone and level sands', 'the repeated "b" and "l" sounds stretch out the line, echoing the endless empty desert', ['assonance only', 'onomatopoeia', 'oxymoron'])],
  struct=[('the turn from the inscription to the empty desert', 'the sudden shift from the tyrant\'s words to "Nothing beside remains" exposes the futility of power')],
  tone='ironic and contemplative', tw=['celebratory', 'panicked', 'romantic'], tonex='the gap between the boast and the bare sands creates quiet, mocking irony.',
  vocab=[('colossal', 'extremely large', ['ancient', 'broken', 'golden'], 'the size of the "Wreck" makes its ruin more striking.')],
  theme='the impermanence of power',
  gq='How does Shelley present the limits of a tyrant\'s power?',
  gqa='The inscription "Look on my Works, ye Mighty, and despair!" is a tyrant\'s boast, but the caesura and the blunt "Nothing beside remains" turn it into dramatic irony. Alliteration in "boundless and bare" and "lone and level sands" stretches the lines like the empty desert, and enjambement carries the reader across the wreck. The sonnet\'s turn from boast to emptiness shows that time defeats all rulers.',
  summary='A ruined statue\'s inscription boasts of a king\'s mighty works, but nothing is left around it except empty desert sand.')

P(id='poem_checkpoint', kind='poem', title='free-verse poem about a girl crossing a checkpoint on her way to school',
  text=("Every morning she shows them\n"
        "her bag:\n"
        "a pencil case, a maths book,\n"
        "an apple she will not eat until noon.\n"
        "\n"
        "They search it like a country\n"
        "they suspect of hiding something.\n"
        "\n"
        "She has learned to stand still,\n"
        "to look at the middle distance,\n"
        "to keep her homework dry\n"
        "and her anger folded\n"
        "small enough to fit\n"
        "between the pages."),
  form='Form: free verse with no regular rhyme or metre; short, uneven lines and enjambement ("shows them / her bag") create pauses that mimic the stop-start of the checkpoint and the girl\'s careful self-control.',
  persp='Perspective: a third-person observer presents an ordinary schoolgirl, so conflict is seen through its effect on daily life rather than through battles or politics. The poet\'s sympathy lies with her quiet endurance.',
  dev=[('list of ordinary objects', 'a pencil case, a maths book, / an apple she will not eat until noon', 'the harmless items highlight the absurdity of searching a child and humanise her', ['hyperbole', 'onomatopoeia', 'oxymoron']),
       ('simile', 'They search it like a country / they suspect of hiding something', 'the small bag stands for a whole people under suspicion, widening the poem\'s political meaning', ['metaphor', 'alliteration', 'pun']),
       ('metaphor', 'her anger folded / small enough to fit / between the pages', 'her anger is a hidden note, showing suppressed feeling and the discipline needed to survive', ['simile', 'statistic', 'personification']),
       ('enjambement', 'shows them / her bag', 'the line break creates a pause like a held breath at the checkpoint', ['caesura', 'rhyme', 'refrain'])],
  struct=[('the final stanza\'s list of learned behaviours ending on "between the pages"', 'the poem ends on a quiet image of suppressed anger, more powerful than an outburst')],
  tone='restrained and indignant', tw=['joyful', 'comic', 'nostalgic'], tonex='calm, plain description barely holds back anger at injustice.',
  vocab=[('middle distance', 'a point neither near nor far, where someone looks to avoid eye contact', ['the halfway point of a race', 'a measurement on a map', 'a type of camera shot only'], 'it shows how she protects herself by not engaging.')],
  theme='the effect of conflict on children\'s everyday lives',
  gq='How does the poet present the effect of conflict on an ordinary child?',
  gqa='The poet focuses on the ordinary: the list "a pencil case, a maths book, / an apple" makes the search seem absurd and the girl innocent. The simile "like a country / they suspect" widens her bag into a whole people under suspicion. Free verse and enjambement create stop-start rhythms like the checkpoint itself, and the final metaphor of anger "folded / small enough to fit / between the pages" shows the quiet discipline conflict forces on her.',
  summary='Each morning a schoolgirl has her bag searched at a checkpoint as if it were a suspect country; she has learned to stay still and fold her anger away.')

P(id='poem_wall', kind='poem', title='sonnet about a city divided by a wall',
  text=("They built the wall the summer I was born,\n"
        "a seam of grey that stitched the city through;\n"
        "my mother's sister waved across the thorn\n"
        "of wire, and every year the distance grew.\n"
        "We learned the shapes of windows on that side,\n"
        "the radio songs we were not meant to hear,\n"
        "the names of streets where cousins lived and died\n"
        "so close, so far, a whisper and a year.\n"
        "But walls are only stone, and stone grows old;\n"
        "one night the crowd came singing with their hands,\n"
        "and pulled the grey apart, and through the cold\n"
        "two sisters met like strangers from two lands.\n"
        "  They held each other, laughing, wet with rain –\n"
        "  then, slowly, learned each other's names again."),
  form='Form: a Shakespearean-style sonnet – fourteen lines of iambic pentameter, three quatrains rhyming ABAB and a final couplet. The volta at line 9 ("But walls are only stone") turns from division to reunion, and the couplet resolves the poem with a bittersweet image.',
  persp='Perspective: a first-person speaker who grew up in a divided city presents conflict through the separation of a family, so political division becomes personal loss.',
  dev=[('metaphor', 'a seam of grey that stitched the city through', 'the wall is a scar or seam, suggesting the city is one body forcibly sewn apart', ['simile', 'onomatopoeia', 'hyperbole']),
       ('volta', 'But walls are only stone, and stone grows old', 'the turn shifts the poem from division to hope, as the wall is shown to be temporary', ['refrain', 'caesura', 'flashback']),
       ('antithesis', 'so close, so far', 'the contrast captures the painful paradox of relatives living nearby but out of reach', ['alliteration', 'statistic', 'pun']),
       ('simile', 'two sisters met like strangers from two lands', 'the reunion is bittersweet: the years apart have made family members into strangers', ['metaphor', 'personification', 'onomatopoeia'])],
  struct=[('the final rhyming couplet', 'the couplet\'s image of re-learning names shows that reunion does not erase the damage of division')],
  tone='elegiac and hopeful', tw=['angry', 'comic', 'detached'], tonex='memories of loss give way to a tender but bittersweet reunion.',
  vocab=[('seam', 'a line where two pieces of fabric are sewn together', ['a type of rock', 'a narrow street', 'a crack in ice'], 'it makes the city a garment cruelly stitched in two.')],
  theme='division and reconciliation',
  gq='How does the poet use the sonnet form to present division and reunion?',
  gqa='The three quatrains present division: the wall is a "seam of grey" that "stitched the city through", and the antithesis "so close, so far" captures the family\'s painful separation. The volta at line 9, "But walls are only stone", turns to hope as the crowd pulls the wall apart. The simile "like strangers from two lands" and the final couplet, in which the sisters "learned each other\'s names again", show that reunion cannot simply undo the years of division.',
  summary='A speaker recalls a wall that divided the city and her family; when crowds finally tear it down, her mother and aunt meet like strangers and get to know each other again.')

P(id='poem_chant', kind='poem', title='poem written to be performed at a youth protest march',
  text=("They told us to wait.\n"
        "We waited through three elections,\n"
        "two floods and one fire season\n"
        "that never really ended.\n"
        "\n"
        "They told us to be realistic.\n"
        "We are. We have done the maths.\n"
        "\n"
        "They told us we were too young to understand.\n"
        "We understand this:\n"
        "you can't negotiate with a thermometer.\n"
        "\n"
        "So we are done waiting.\n"
        "Look out of your windows.\n"
        "We are the weather now."),
  form='Form: free verse in short stanzas built on a repeated structure ("They told us ... We ..."), designed to be performed aloud; the pattern of accusation and reply gives it the rhythm of a chant.',
  persp='Perspective: a collective "we" of young protesters addresses adults in power ("you"), presenting the climate crisis as a conflict between generations.',
  dev=[('anaphora', 'They told us to wait. ... They told us to be realistic. ... They told us we were too young', 'the repeated opening lists adult excuses, each one rejected in turn', ['simile', 'onomatopoeia', 'oxymoron']),
       ('epigram', 'you can\'t negotiate with a thermometer', 'the witty, compressed line shows that physical facts cannot be argued away', ['simile', 'hyperbole', 'flashback']),
       ('metaphor', 'We are the weather now.', 'the young protesters become an unstoppable natural force, turning the threat back on those in power', ['simile', 'statistic', 'rhetorical question']),
       ('listing with numbers', 'three elections, / two floods and one fire season', 'the countdown measures years of waiting in disasters', ['alliteration', 'pun', 'oxymoron'])],
  struct=[('the call-and-response pattern of "They told us" and "We"', 'it dramatises the generational conflict and suits live performance')],
  tone='defiant', tw=['submissive', 'nostalgic', 'whimsical'], tonex='short declaratives and turned-back accusations create a confident, defiant tone.',
  aud='Fellow young protesters and the adults in power they are addressing ("Look out of your windows").',
  purp='To express young people\'s frustration and to warn those in power that young people will no longer wait.',
  theme='generational conflict and protest',
  gq='How does the poet create a voice of protest in this poem?',
  gqa='The anaphora "They told us ..." lists adult excuses, and each is answered by the collective "We", creating a call-and-response protest rhythm. Numbers ("three elections, / two floods") measure the years of waiting in disasters. The epigram "you can\'t negotiate with a thermometer" mocks political delay, and the final metaphor "We are the weather now" turns young people into an unstoppable force, giving the poem a defiant, threatening ending.',
  summary='Young protesters list the excuses adults gave them, reject each one, and declare that they have stopped waiting and are now a force like the weather.')

# =============================================================================================
# Macbeth (public domain)
# =============================================================================================
P(id='mac_witches', kind='drama', title='extract from Act 1 of Macbeth by William Shakespeare',
  text=("[Act 1, Scene 1. Thunder and lightning. Enter three WITCHES.]\n"
        "ALL: Fair is foul, and foul is fair:\n"
        "Hover through the fog and filthy air.\n"
        "[Act 1, Scene 3. After the witches greet Macbeth as future king.]\n"
        "BANQUO: But 'tis strange:\n"
        "And oftentimes, to win us to our harm,\n"
        "The instruments of darkness tell us truths,\n"
        "Win us with honest trifles, to betray's\n"
        "In deepest consequence."),
  tragic='Tragic genre: the witches introduce fate and temptation; their prophecy works on Macbeth\'s ambition, his hamartia, while Banquo\'s warning foreshadows how "honest trifles" will lead Macbeth to destruction.',
  staging='Stage directions ("Thunder and lightning") create a stormy, supernatural atmosphere from the very first moment; the witches could hover in smoke or speak in eerie unison to unsettle the audience.',
  motif='Motifs of darkness and confusion: "fog and filthy air" and "instruments of darkness" introduce the darkness that runs through the play, while "Fair is foul" sets up the inversion of good and evil.',
  dev=[('paradox and chiasmus', 'Fair is foul, and foul is fair', 'the reversed phrase suggests a world where appearances deceive and moral order is upside down', ['simile', 'onomatopoeia', 'hyperbole']),
       ('alliteration', 'fog and filthy air', 'the repeated "f" sounds create a hissing, ominous atmosphere', ['assonance only', 'pun', 'metaphor']),
       ('metaphor', 'The instruments of darkness tell us truths', 'the witches are tools of evil who use partial truths to trap people, foreshadowing Macbeth\'s fall', ['simile', 'statistic', 'oxymoron']),
       ('trochaic tetrameter', 'Fair is foul, and foul is fair', 'the chant-like rhythm, different from the nobles\' blank verse, marks the witches as unnatural', ['iambic pentameter', 'free verse', 'prose'])],
  struct=[('opening the play with the witches', 'beginning with the supernatural establishes fate, evil and confusion before we meet Macbeth')],
  tone='ominous', tw=['cheerful', 'romantic', 'comic'], tonex='thunder, chanting and Banquo\'s warning create a threatening, ominous tone.',
  vocab=[('trifles', 'things of little value or importance', ['weapons', 'prophecies of doom', 'large rewards'], 'Banquo warns that small truths are bait for a great betrayal.')],
  theme='appearance versus reality and the temptation of evil',
  gq='How does Shakespeare use the witches to establish the atmosphere and themes of the play?',
  gqa='The stage direction "Thunder and lightning" and the chant "Fair is foul, and foul is fair" create an unnatural, ominous atmosphere: the paradox inverts moral order and introduces the theme of appearance versus reality. Alliteration in "fog and filthy air" adds menace. Banquo\'s metaphor "instruments of darkness" and his warning that they "win us with honest trifles" foreshadow how the prophecy will exploit Macbeth\'s ambition, his tragic flaw.',
  summary='The witches chant that fair is foul in a storm; later Banquo warns that agents of evil tell small truths to lead people to their destruction.')

P(id='mac_aside', kind='drama', title='extract from Act 1, Scene 4 of Macbeth by William Shakespeare',
  text=("[DUNCAN has just named his son Malcolm heir to the throne, as Prince of Cumberland.]\n"
        "MACBETH [Aside]: The Prince of Cumberland! That is a step\n"
        "On which I must fall down, or else o'erleap,\n"
        "For in my way it lies. Stars, hide your fires;\n"
        "Let not light see my black and deep desires:\n"
        "The eye wink at the hand; yet let that be\n"
        "Which the eye fears, when it is done, to see."),
  dramatic='The aside lets Macbeth speak his secret thoughts to the audience while the other characters cannot hear. This creates dramatic irony: Duncan trusts Macbeth while we know he is thinking about murder.',
  tragic='Macbeth\'s hamartia – "vaulting" ambition – is revealed here: Malcolm\'s promotion becomes an obstacle to "o\'erleap", and he begins his moral fall.',
  motif='Light and darkness: "Stars, hide your fires; / Let not light see my black and deep desires" links evil to darkness; Macbeth wants to hide his desires even from heaven.',
  staging='The aside could be delivered downstage, away from Duncan, with lighting dimming on "Stars, hide your fires", so the audience becomes Macbeth\'s guilty confidant.',
  dev=[('aside', '[Aside]', 'the device shares Macbeth\'s murderous thoughts with the audience alone, creating dramatic irony', ['soliloquy', 'monologue to Duncan', 'chorus']),
       ('metaphor', 'That is a step / On which I must fall down, or else o\'erleap', 'Malcolm is an obstacle in Macbeth\'s path to the crown, showing his ambition', ['simile', 'onomatopoeia', 'pun']),
       ('apostrophe and imagery of light and dark', 'Stars, hide your fires; / Let not light see my black and deep desires', 'Macbeth calls on the stars to hide, linking his ambition to darkness and evil', ['simile', 'statistic', 'oxymoron']),
       ('rhyming couplet', 'desires ... fires', 'the neat rhyme seals Macbeth\'s dark resolve and marks the end of the thought', ['free verse', 'blank verse only', 'enjambement only'])],
  struct=[('placing the aside straight after Duncan honours his son', 'the contrast between public celebration and private plotting heightens tension and dramatic irony')],
  tone='secretive and sinister', tw=['joyful', 'loyal', 'carefree'], tonex='the hushed aside and imagery of darkness create a sinister tone.',
  theme='ambition and the concealment of evil',
  gq='How does Shakespeare use the aside to reveal Macbeth\'s ambition?',
  gqa='Because it is an aside, Macbeth\'s thoughts are shared only with the audience, creating dramatic irony as Duncan continues to trust him. The metaphor of Malcolm as a "step" he must "o\'erleap" shows his ambition – his hamartia – turning towards murder. His apostrophe "Stars, hide your fires" and the imagery of "black and deep desires" link ambition with darkness, while the rhyming couplet seals his dark resolve.',
  summary='When Duncan names Malcolm his heir, Macbeth secretly reveals that Malcolm is an obstacle to his ambition and asks the stars to hide his dark desires.')

P(id='mac_dagger', kind='drama', title='extract from Macbeth\'s soliloquy in Act 2, Scene 1 of Macbeth by William Shakespeare',
  text=("MACBETH: Is this a dagger which I see before me,\n"
        "The handle toward my hand? Come, let me clutch thee.\n"
        "I have thee not, and yet I see thee still.\n"
        "Art thou not, fatal vision, sensible\n"
        "To feeling as to sight? or art thou but\n"
        "A dagger of the mind, a false creation,\n"
        "Proceeding from the heat-oppressed brain?"),
  dramatic='As a soliloquy, the speech reveals Macbeth\'s inner conflict while he is alone on stage; the audience hears his fear and guilt before the murder of Duncan.',
  tragic='The hallucination shows Macbeth\'s conscience struggling with his ambition: a tragic hero who knows he is doing wrong but proceeds anyway.',
  motif='The dagger introduces the motif of blood and violence that will haunt Macbeth; the uncertainty about what is real links to the theme of appearance versus reality.',
  staging='Directors choose whether the audience sees the dagger (a projection or light) or only Macbeth\'s reaction; either choice shapes whether the vision seems supernatural or psychological.',
  dev=[('rhetorical questions', 'Is this a dagger which I see before me', 'the questions show Macbeth\'s confusion and inner turmoil', ['statistic', 'pun', 'simile']),
       ('apostrophe', 'Come, let me clutch thee', 'addressing the dagger directly shows how real the vision feels to him', ['aside', 'onomatopoeia', 'oxymoron']),
       ('metaphor', 'A dagger of the mind, a false creation', 'he wonders if the dagger is a product of his guilty imagination, showing his disturbed mind', ['simile', 'alliteration', 'hyperbole']),
       ('blank verse with enjambement', 'sensible / To feeling as to sight? or art thou but / A dagger of the mind', 'the run-on lines mimic his racing, uncontrolled thoughts', ['rhyming couplets', 'prose', 'trochaic chant'])],
  struct=[('its position just before the murder of Duncan', 'the soliloquy builds suspense and shows Macbeth\'s hesitation at the point of no return')],
  tone='feverish and uncertain', tw=['calm', 'triumphant', 'comic'], tonex='questions and broken lines express fear and confusion.',
  vocab=[('heat-oppressed', 'overheated and burdened, as if feverish', ['cold and calm', 'well-rested', 'religious'], 'it suggests his brain is sick with guilt and ambition.')],
  theme='guilt, ambition and the unreliable mind',
  gq='How does Shakespeare present Macbeth\'s state of mind before the murder?',
  gqa='In soliloquy, Macbeth is alone with his conscience. His rhetorical questions ("Is this a dagger ...?") and apostrophe ("Come, let me clutch thee") show he is unsure what is real. The metaphor "A dagger of the mind, a false creation" suggests guilt is already distorting his perception, and "heat-oppressed brain" implies fever. Enjambement mimics his racing thoughts, building suspense just before the point of no return.',
  summary='Alone before killing Duncan, Macbeth sees a dagger pointing towards him, tries to grasp it and wonders whether it is real or a product of his feverish mind.')

P(id='mac_blood', kind='drama', title='extract from Act 2, Scene 2 of Macbeth by William Shakespeare (just after Duncan\'s murder)',
  text=("MACBETH: Will all great Neptune's ocean wash this blood\n"
        "Clean from my hand? No, this my hand will rather\n"
        "The multitudinous seas incarnadine,\n"
        "Making the green one red.\n"
        "[Re-enter LADY MACBETH]\n"
        "LADY MACBETH: My hands are of your colour, but I shame\n"
        "To wear a heart so white. [Knocking within] I hear a knocking\n"
        "At the south entry. Retire we to our chamber.\n"
        "A little water clears us of this deed."),
  dramatic='Dramatic irony: Lady Macbeth\'s confident "A little water clears us of this deed" will be reversed in Act 5, when she sleepwalks, trying to wash away imaginary blood. The knocking within also builds tension.',
  motif='Blood symbolises guilt: Macbeth believes all the oceans could not wash it away, while Lady Macbeth dismisses it, a contrast the play later overturns.',
  staging='The offstage knocking ("Knocking within") is a sound effect that heightens panic; actors might freeze, then rush to hide their bloody hands.',
  tragic='Macbeth feels the weight of his crime immediately, showing the guilt that will destroy him; his tragedy is that he understands the horror of what he has done.',
  dev=[('hyperbole', 'this my hand will rather / The multitudinous seas incarnadine', 'Macbeth exaggerates that his bloody hand would turn all the oceans red, showing overwhelming guilt', ['understatement', 'simile', 'pun']),
       ('contrast of registers', 'The multitudinous seas incarnadine, / Making the green one red.', 'grand Latinate words are followed by plain monosyllables, as if Macbeth\'s grandeur collapses into simple horror', ['alliteration only', 'onomatopoeia', 'oxymoron']),
       ('colour imagery', 'My hands are of your colour, but I shame / To wear a heart so white', 'Lady Macbeth mocks her husband\'s "white" (cowardly) heart while sharing his blood-red guilt', ['simile', 'statistic', 'rhetorical question']),
       ('dramatic irony', 'A little water clears us of this deed.', 'the audience will later see her unable to wash away imagined blood, so her confidence is tragically mistaken', ['foreshadowing only by the chorus', 'comic relief', 'flashback'])],
  struct=[('the interruption of the knocking', 'the sound breaks the dialogue and brings the outside world crashing in, heightening fear of discovery')],
  tone='tense and guilt-ridden', tw=['relaxed', 'joyful', 'romantic'], tonex='Macbeth\'s horror and the knocking create panic and guilt.',
  vocab=[('incarnadine', 'turn blood-red (used as a verb)', ['make calm', 'flood', 'bless'], 'the rare, grand word magnifies the horror of his guilt.')],
  theme='guilt and its consequences',
  gq='How does Shakespeare present the Macbeths\' different reactions to the murder?',
  gqa='Macbeth\'s rhetorical question and hyperbole – his hand would "the multitudinous seas incarnadine" – show overwhelming guilt; the shift to the plain "Making the green one red" suggests collapse into simple horror. Lady Macbeth\'s colour imagery mocks his "heart so white" and her line "A little water clears us of this deed" shows practical confidence. The audience\'s later knowledge of her sleepwalking makes this dramatic irony, while the "knocking within" heightens fear of discovery.',
  summary='After the murder, Macbeth fears his bloody hand could stain the oceans red; Lady Macbeth scorns his fear, hears knocking and says a little water will clean them.')

P(id='mac_tomorrow', kind='drama', title='extract from Macbeth\'s soliloquy in Act 5, Scene 5 of Macbeth by William Shakespeare (after hearing of his wife\'s death)',
  text=("MACBETH: Tomorrow, and tomorrow, and tomorrow,\n"
        "Creeps in this petty pace from day to day,\n"
        "To the last syllable of recorded time;\n"
        "And all our yesterdays have lighted fools\n"
        "The way to dusty death. Out, out, brief candle!\n"
        "Life's but a walking shadow, a poor player\n"
        "That struts and frets his hour upon the stage\n"
        "And then is heard no more."),
  dramatic='As a soliloquy, it reveals Macbeth\'s despair and emptiness near the end; the audience sees the cost of his ambition.',
  tragic='Macbeth has gained everything his ambition wanted and found it meaningless; this is the tragic hero\'s recognition, which may produce pity (catharsis) in the audience.',
  motif='Light and darkness: "Out, out, brief candle!" makes life a candle about to be extinguished; theatre imagery ("a poor player") makes life a meaningless performance.',
  dev=[('repetition', 'Tomorrow, and tomorrow, and tomorrow', 'the slow, repeated word mimics the dragging monotony of time for Macbeth', ['tricolon of contrasting ideas', 'onomatopoeia', 'pun']),
       ('metaphor', 'Out, out, brief candle!', 'life is a fragile candle easily blown out, showing how quickly his wife\'s life and his own will end', ['simile', 'statistic', 'oxymoron']),
       ('extended theatrical metaphor', 'a poor player / That struts and frets his hour upon the stage', 'life is like a bad actor\'s brief performance, suggesting it is meaningless and quickly forgotten', ['simile', 'hyperbole', 'alliteration only']),
       ('alliteration', 'dusty death', 'the hard "d" sounds emphasise the bleak finality of death', ['assonance only', 'onomatopoeia', 'pun'])],
  struct=[('its placement after Lady Macbeth\'s death and before the final battle', 'it shows Macbeth emotionally dead before his physical death')],
  tone='despairing and nihilistic', tw=['hopeful', 'triumphant', 'playful'], tonex='slow rhythms and images of shadows and dust convey despair.',
  vocab=[('petty', 'small and unimportant', ['angry', 'quick', 'royal'], 'it shows Macbeth now finds each day trivial and meaningless.')],
  theme='the emptiness of ambition',
  gq='How does Shakespeare present Macbeth\'s view of life in this soliloquy?',
  gqa='The repetition "Tomorrow, and tomorrow, and tomorrow" and the verb "Creeps" convey the slow, meaningless passing of time. The metaphor "brief candle" presents life as fragile and easily extinguished, and alliteration in "dusty death" stresses bleak finality. The extended theatre metaphor – "a poor player / That struts and frets" – makes life a pointless performance. This is the tragic hero\'s recognition: his ambition has brought only emptiness, which evokes pity.',
  summary='After his wife\'s death, Macbeth reflects that time creeps on meaninglessly and that life is a brief candle and a poor actor\'s short performance.')

# =============================================================================================
# News, editorial and online texts
# =============================================================================================
P(id='stadium_a', kind='news', title='news report from a regional newspaper',
  text=("NEW STADIUM TO BRING 2,000 JOBS AND \"A NEW HEART\" TO RIVERSIDE\n"
        "Councillors last night approved plans for a £300 million stadium on the Riverside estate, promising thousands of jobs and a revived town centre.\n"
        "Council leader Priya Nair called the decision \"historic\". \"Riverside has waited decades for investment,\" she said.\n"
        "About 140 households will be relocated during construction. Local football fans celebrated outside the town hall."),
  framing='The report frames the stadium positively: the headline foregrounds jobs and "A NEW HEART", the council leader is quoted at length, and the relocation of 140 households is placed late and described neutrally ("relocated"). Residents who oppose the plan are not quoted.',
  newsval='News values: impact (jobs, investment), proximity (a local estate), prominence (the council leader) and positivity – a story of regeneration.',
  facts_op='Fact: "Councillors last night approved plans for a £300 million stadium." Opinion: the council leader calling the decision "historic" (a judgement, attributed to her).',
  dev=[('positive framing in the headline', '2,000 JOBS AND "A NEW HEART"', 'leading with jobs and a metaphor of renewal tells readers this is good news', ['negative framing', 'neutral summary only', 'pun']),
       ('euphemism', 'About 140 households will be relocated', 'the neutral verb "relocated" softens the reality of families losing their homes', ['hyperbole', 'simile', 'onomatopoeia']),
       ('selective quotation', 'Council leader Priya Nair called the decision "historic"', 'only the supporter\'s voice is quoted, giving her view authority', ['balanced quotation from both sides', 'statistic', 'rhetorical question'])],
  struct=[('the order of information (inverted pyramid)', 'positive details come first and the relocation comes near the end, so many readers will not register the cost')],
  tone='upbeat', tw=['outraged', 'mournful', 'sarcastic'], tonex='celebratory words ("historic", "celebrated") create a positive tone.',
  aud='Readers of a regional newspaper, including local residents and business owners.',
  purp='To report the council\'s decision, but in a way that presents it as good news for the town.',
  theme='regeneration and its costs',
  gq='How does this report present the stadium decision?',
  gqa='The headline frames the story positively, foregrounding "2,000 JOBS" and the metaphor "A NEW HEART". Only the council leader is quoted, calling the decision "historic", so her perspective dominates. The cost to residents is placed late and softened by the euphemism "relocated", while the image of celebrating fans ends the report on a positive note. Through selection and order, the report favours the council\'s view.',
  summary='A report says councillors approved a £300 million stadium promising 2,000 jobs, quotes the council leader\'s praise, and briefly notes that 140 households will be relocated.')

P(id='stadium_b', kind='news', title='news report from a community news website',
  text=("FAMILIES FACE EVICTION AS COUNCIL BACKS £300M STADIUM\n"
        "One hundred and forty families on the Riverside estate could lose their homes after councillors voted last night to build a stadium on the site.\n"
        "\"My children were born in this flat,\" said Joan Mensah, 62, who has lived on the estate for thirty years. \"Nobody asked us.\"\n"
        "The council claims the project will create 2,000 jobs. Campaigners say most will be temporary."),
  framing='The report frames the stadium negatively: the headline foregrounds "EVICTION" and families, a long-term resident is quoted emotionally, and the jobs figure is introduced with "claims" and immediately challenged by campaigners. The council leader is not quoted.',
  newsval='News values: human interest (a resident\'s story), negativity (eviction), proximity and conflict between residents and the council.',
  facts_op='Fact: "councillors voted last night to build a stadium on the site." Opinion: "Nobody asked us" (Joan Mensah\'s view) and the campaigners\' claim that most jobs will be temporary.',
  dev=[('negative framing in the headline', 'FAMILIES FACE EVICTION', 'leading with eviction and families makes readers sympathise with residents', ['positive framing', 'neutral summary only', 'pun']),
       ('emotive quotation', '"My children were born in this flat,"', 'a personal detail turns statistics into a human story and creates sympathy', ['statistic', 'euphemism', 'simile']),
       ('distancing verb', 'The council claims the project will create 2,000 jobs', '"claims" casts doubt on the council\'s figure, unlike a neutral "says"', ['hyperbole', 'onomatopoeia', 'metaphor'])],
  struct=[('ending with the campaigners\' challenge', 'the final word goes to critics, leaving readers doubtful about the benefits')],
  tone='critical and sympathetic', tw=['celebratory', 'comic', 'indifferent'], tonex='emotive quotation and words like "eviction" create a critical tone.',
  aud='Readers of a community news website, especially local residents concerned about the estate.',
  purp='To report the decision while highlighting its human cost and questioning the council\'s claims.',
  theme='regeneration and its costs',
  gq='How does this report present the stadium decision?',
  gqa='The headline frames the story negatively, foregrounding "EVICTION" and families. The emotive quotation from Joan Mensah ("My children were born in this flat") turns a number into a human story, and "Nobody asked us" suggests injustice. The council\'s jobs figure is introduced with the distancing verb "claims" and immediately challenged by campaigners, who get the last word. Through framing, selection and order, the report favours residents.',
  summary='A report says 140 families could lose their homes because of the stadium, quotes a long-term resident who was not consulted, and questions the council\'s jobs claim.')

P(id='editorial_curfew', kind='oped', title='newspaper editorial ("Our view") on a proposed curfew for under-16s',
  text=("OUR VIEW: A CURFEW WILL NOT MAKE OUR STREETS SAFER\n"
        "The council's plan to ban under-16s from the town centre after 9 p.m. may sound tough. It is also lazy.\n"
        "Police figures show that youth crime in the town fell by 12 per cent last year. The problem is not that teenagers are out; it is that there is nowhere for them to go. Two youth clubs have closed since 2022.\n"
        "Treat young people as suspects and they will behave like them. Fund the clubs instead."),
  facts_op='Facts: "youth crime in the town fell by 12 per cent last year"; "Two youth clubs have closed since 2022." Opinions: the plan "is also lazy"; "Treat young people as suspects and they will behave like them."',
  framing='The editorial frames the curfew as a lazy, counterproductive policy and young people as victims of cuts rather than as a threat.',
  dev=[('concession and rebuttal', 'may sound tough. It is also lazy.', 'the editorial briefly acknowledges the plan\'s appeal, then dismisses it sharply', ['simile', 'onomatopoeia', 'flashback']),
       ('statistical evidence', 'youth crime in the town fell by 12 per cent last year', 'a fact undermines the premise that a curfew is needed (logos)', ['hyperbole', 'anecdote', 'metaphor']),
       ('antithesis', 'The problem is not that teenagers are out; it is that there is nowhere for them to go.', 'the balanced sentence reframes the issue from behaviour to lack of facilities', ['simile', 'pun', 'oxymoron']),
       ('imperative', 'Fund the clubs instead.', 'the short command offers a clear alternative and ends with a call to action', ['rhetorical question', 'statistic', 'euphemism'])],
  struct=[('the move from criticism to evidence to an alternative proposal', 'the editorial does not only oppose but offers a solution, which strengthens its argument')],
  tone='forthright', tw=['hesitant', 'whimsical', 'neutral'], tonex='short, blunt sentences ("It is also lazy.") create a confident, forthright tone.',
  aud='Readers of the local newspaper, including parents, councillors and older residents worried about safety.',
  purp='To persuade readers and councillors to reject the curfew and fund youth clubs instead.',
  vocab=[('curfew', 'a rule that people must stay indoors or away from certain places after a set time', ['a type of fine', 'a youth club', 'a police patrol'], 'the word connotes control and suspicion.')],
  theme='how society treats young people',
  gq='How does the editorial argue against the curfew?',
  gqa='The editorial concedes the plan "may sound tough" before dismissing it as "lazy", a confident rebuttal. Statistical evidence – youth crime fell by 12 per cent and two clubs have closed – supports its argument with logos. The antithesis "The problem is not that teenagers are out; it is that there is nowhere for them to go" reframes the issue, and the closing imperative "Fund the clubs instead" offers an alternative. Opinions are presented forcefully but grounded in facts.',
  summary='A newspaper editorial argues that a proposed 9 p.m. curfew for under-16s is lazy, citing falling youth crime and closed youth clubs, and urges the council to fund clubs instead.')

P(id='viral_post', kind='social', title='social media post that was widely shared',
  text=("🚨SHARE BEFORE THEY DELETE THIS🚨\n"
        "My cousin works at the water company and says the city's tap water will be SWITCHED OFF for 3 DAYS from Monday!!! The government doesn't want you to know.\n"
        "Fill your baths NOW. Buy bottled water while you still can.\n"
        "Doctors are saying this is the worst crisis in 50 years. Wake up people!!!\n"
        "#WaterCrisis #TheyAreLying"),
  misinfo='Red flags: an anonymous second-hand source ("My cousin works at the water company"); vague authorities ("Doctors are saying"); urgency and fear ("SHARE BEFORE THEY DELETE THIS", "NOW"); conspiracy framing ("The government doesn\'t want you to know"); capital letters and multiple exclamation marks; no date, link or official source.',
  source='The post gives no verifiable source: no name, no link to the water company, no official statement. A reliable source would be the water company\'s own website or a reputable news outlet.',
  dev=[('appeal to fear and urgency', 'SHARE BEFORE THEY DELETE THIS', 'the warning pressures readers to share without checking, which is how misinformation spreads', ['understatement', 'simile', 'statistic from a named study']),
       ('anonymous second-hand source', 'My cousin works at the water company', 'the unverifiable claim gives false authority', ['named expert', 'official statement', 'peer-reviewed study']),
       ('vague appeal to authority', 'Doctors are saying', 'unnamed "doctors" sound authoritative but cannot be checked', ['statistic with source', 'direct quotation', 'metaphor']),
       ('conspiracy framing', 'The government doesn\'t want you to know.', 'it makes any denial seem like proof of a cover-up', ['balanced view', 'counterargument', 'simile'])],
  struct=[('typographical emphasis (capitals, emoji, exclamation marks)', 'visual alarm signals panic and encourages quick emotional sharing')],
  tone='alarmist', tw=['measured', 'reassuring', 'ironic'], tonex='capitals, emoji and urgent imperatives create an alarmist tone.',
  aud='Social media users in the city, who are urged to act and share immediately.',
  purp='To alarm readers and make them share the claim and stockpile water.',
  theme='misinformation and fear online',
  gq='How does the post try to persuade readers to believe and share it?',
  gqa='The post uses urgency ("SHARE BEFORE THEY DELETE THIS", "NOW") and fear to make readers act before thinking. Its sources are unverifiable – an anonymous "cousin" and unnamed "Doctors" – but they lend false authority. Conspiracy framing ("The government doesn\'t want you to know") makes denials seem like proof, and visual signals (capitals, emoji, exclamation marks) create alarm. These are classic red flags of misinformation.',
  summary='A post claims, citing a cousin and unnamed doctors, that the city\'s water will be cut off for three days and urges people to stockpile water and share before it is deleted.')

P(id='factcheck', kind='website', title='article from an independent fact-checking website',
  text=("FACT CHECK: Is the city's water being switched off for three days? FALSE\n"
        "A post shared more than 40,000 times claims that tap water will be cut off from Monday.\n"
        "We contacted the water company, which said in a written statement: \"There are no planned interruptions. Some streets in the north of the city will have reduced pressure for up to four hours on Tuesday during routine maintenance.\"\n"
        "We found no doctors or health bodies making the claims in the post.\n"
        "Verdict: FALSE. The post exaggerates a short, local maintenance notice."),
  source='The article is reliable because it names its source (the water company\'s written statement), quotes it directly, explains how it checked the claim, and distinguishes the real event (four hours of reduced pressure) from the exaggeration.',
  misinfo='It shows how misinformation often grows from a real but minor fact (local maintenance) that is exaggerated and stripped of context.',
  dev=[('clear verdict label', 'Verdict: FALSE', 'the label gives readers a quick, unambiguous answer', ['rhetorical question', 'pun', 'hyperbole']),
       ('direct quotation from a named source', 'the water company, which said in a written statement', 'a named, verifiable source provides authority and transparency', ['anonymous source', 'rumour', 'opinion']),
       ('precise detail', 'reduced pressure for up to four hours on Tuesday', 'exact facts contrast with the post\'s vague exaggeration', ['vague claim', 'emotive language', 'simile'])],
  struct=[('question headline, method, evidence, verdict', 'the clear structure models how to check a claim step by step')],
  tone='calm and objective', tw=['alarmist', 'sarcastic', 'emotional'], tonex='neutral, precise language contrasts with the panic of the viral post.',
  aud='Members of the public who have seen the viral post and want to know whether it is true.',
  purp='To check a viral claim, show the evidence and correct misinformation.',
  theme='truth and verification online',
  gq='How does the fact-check article establish that it is reliable?',
  gqa='The article sets out a clear structure – question, method, evidence, verdict. It names and directly quotes its source, the water company\'s written statement, and gives precise details ("up to four hours on Tuesday") that contrast with the viral post\'s vague panic. It explains what it checked ("We found no doctors ...") and its calm, objective tone and clear verdict label "FALSE" build trust.',
  summary='A fact-check finds that the viral water shut-off claim is false: the water company confirms only four hours of reduced pressure in some streets, and no doctors made the claims.')

# =============================================================================================
# Unseen comparison extracts (Task 1 practice)
# =============================================================================================
P(id='leaving_poem', kind='poem', title='poem about leaving home, from a contemporary anthology',
  text=("Departure Lounge\n"
        "\n"
        "My mother packed the spices first –\n"
        "cardamom, turmeric, a jar of chilli\n"
        "wrapped in a jumper like a sleeping child –\n"
        "as if a country could be carried\n"
        "in small glass jars.\n"
        "\n"
        "At the gate, she did not look back.\n"
        "I did. I am still\n"
        "looking."),
  form='Form: free verse in two stanzas; the enjambement and the final one-word line ("looking.") make the speaker\'s backward glance last beyond the poem.',
  persp='Perspective: the speaker, a child at the time, remembers emigrating; the contrast between the mother who "did not look back" and the speaker who is "still / looking" presents two ways of coping with displacement.',
  dev=[('simile', 'wrapped in a jumper like a sleeping child', 'the jar is protected like a baby, showing how precious home and its tastes are', ['metaphor', 'onomatopoeia', 'hyperbole']),
       ('metaphor (conceit)', 'as if a country could be carried / in small glass jars', 'the spices stand for the whole homeland, and the image is touching but impossible', ['simile', 'statistic', 'alliteration']),
       ('contrast and enjambement', 'she did not look back. / I did. I am still / looking.', 'the contrast and broken lines show the speaker\'s lasting attachment and grief', ['rhyming couplet', 'refrain', 'onomatopoeia'])],
  struct=[('the shift from past tense to the present "I am still / looking"', 'the ending reveals that the departure is not over for the speaker; it continues into the present')],
  tone='wistful', tw=['jubilant', 'angry', 'comic'], tonex='tender sensory details and the lingering final line create a wistful tone.',
  theme='migration, memory and belonging',
  gq='How does the poet present the experience of leaving home?',
  gqa='Leaving home is presented through sensory, domestic details: the spices are "wrapped in a jumper like a sleeping child", a simile that shows how precious the homeland\'s tastes are. The conceit "as if a country could be carried / in small glass jars" is touching but impossible. The contrast between the mother who "did not look back" and the speaker, and the shift into the present "I am still / looking", shows that for the speaker the departure has never ended.',
  summary='A speaker remembers her mother packing spices before they emigrated; the mother did not look back at the departure gate, but the speaker is still looking back.')

P(id='leaving_letter', kind='letter', title='letter written in 1962 by a young woman who had recently emigrated, to her sister',
  text=("Dear Nalini,\n"
        "The flat is small and the radiator knocks all night like a neighbour who wants to come in. At the factory they call me \"Nelly\" because they cannot say my name. I let them.\n"
        "I have found a shop that sells cardamom, but it tastes of the box it came in.\n"
        "Do not tell Amma I cry on the bus. Tell her I have a warm coat and that the English are polite. Both are true.\n"
        "Your loving sister,\nSaroja"),
  aud='Saroja\'s sister Nalini, who is still at home; the letter is private and intimate.',
  purp='To keep in touch with her sister, share honest feelings about her new life and protect their mother from worry.',
  context='Context: in the 1950s and 1960s many people from South Asia and the Caribbean emigrated to Britain to work in factories and services, often facing loneliness, unfamiliar food and having their names changed or mispronounced.',
  dev=[('simile', 'the radiator knocks all night like a neighbour who wants to come in', 'the strange noise becomes a lonely image of someone outside wanting company, reflecting her isolation', ['metaphor', 'onomatopoeia only', 'hyperbole']),
       ('short, resigned sentence', 'I let them.', 'the brief sentence shows her quietly accepting the loss of her name and identity', ['rhetorical question', 'exclamation', 'statistic']),
       ('sensory detail', 'it tastes of the box it came in', 'even familiar food is changed by displacement, showing that home cannot be fully recreated', ['simile', 'pun', 'alliteration']),
       ('irony', 'Tell her I have a warm coat and that the English are polite. Both are true.', 'she tells the truth but selects it to hide her unhappiness, showing her love and her loneliness', ['hyperbole', 'oxymoron', 'onomatopoeia'])],
  struct=[('letter conventions (salutation, sign-off)', 'the familiar form frames an intimate confession, making the reader feel they are reading something private')],
  tone='stoic and lonely', tw=['triumphant', 'angry', 'comic'], tonex='understated statements hide deep loneliness.',
  theme='migration, identity and loneliness',
  gq='How does the writer of the letter present her experience of a new country?',
  gqa='The simile of the radiator knocking "like a neighbour who wants to come in" conveys loneliness, and the short sentence "I let them" shows her quiet acceptance of losing her name. The sensory detail that cardamom "tastes of the box it came in" shows home cannot be recreated. Her instruction to tell their mother only selected truths ("Both are true") is ironic and loving, revealing hidden sadness beneath stoicism.',
  summary='Saroja writes to her sister about her small flat, being renamed "Nelly" at work and spices that taste wrong, and asks her not to tell their mother that she cries.')

# =============================================================================================
# Stories from around the world (translated-literature style)
# =============================================================================================
P(id='tr_kyoto', kind='story', title='extract from a short story set in Kyoto, Japan, which keeps some Japanese words, as many translations do',
  text=("On the last night of Obon, Grandmother gave Haruto a paper lantern and a pen. \"Write his name,\" she said.\n"
        "Haruto wrote OJIICHAN in careful letters, because he could not remember his grandfather's face, only the smell of his pipe.\n"
        "At the river the lanterns drifted away in hundreds, each one a small, swaying light. Haruto watched his until he could not tell it from the others.\n"
        "\"Now he knows the way back,\" Grandmother said. \"And we know the way to let go.\""),
  culture='Cultural context: Obon is a Japanese Buddhist festival honouring ancestors\' spirits; on its last night floating lanterns (tōrō nagashi) guide the spirits back. Keeping words such as "Obon" and "Ojiichan" (grandfather) preserves cultural meaning that translation might lose.',
  symbol='The lanterns symbolise the spirits of the dead and the act of letting go; when Haruto cannot distinguish his lantern from the others, it suggests individual grief joining a shared tradition.',
  epiphany='Epiphany: Grandmother\'s final words reveal that the ritual is as much for the living, learning to let go, as for the dead.',
  conflict='Inner conflict: Haruto wants to honour a grandfather he can barely remember, and must learn to grieve and let go.',
  dev=[('retained cultural terms', 'Obon ... OJIICHAN', 'keeping the Japanese words preserves cultural meaning and reminds readers they are entering another culture', ['slang', 'pun', 'onomatopoeia']),
       ('sensory detail', 'only the smell of his pipe', 'a single sense memory shows how faint but precious his memory of his grandfather is', ['simile', 'statistic', 'hyperbole']),
       ('symbolism', 'Haruto watched his until he could not tell it from the others', 'losing sight of his lantern among hundreds suggests personal grief merging with a communal tradition', ['flashback', 'oxymoron', 'alliteration']),
       ('parallel structure', '"Now he knows the way back ... And we know the way to let go."', 'the balanced lines show that the ritual serves both the dead and the living', ['rhetorical question', 'hyperbole', 'onomatopoeia'])],
  struct=[('ending on Grandmother\'s words', 'the final line provides the story\'s epiphany and turns description into meaning')],
  tone='gentle and reflective', tw=['comic', 'tense', 'bitter'], tonex='quiet sensory images and calm dialogue create a gentle, reflective tone.',
  theme='grief, memory and tradition',
  gq='How does the writer use the lantern ceremony to explore grief?',
  gqa='Retained terms like "Obon" and "OJIICHAN" situate the story in Japanese culture and its ancestor rituals. Haruto\'s memory survives only as "the smell of his pipe", showing faint but precious grief. The lanterns symbolise spirits; as Haruto loses sight of his among hundreds, private grief merges into shared tradition. Grandmother\'s parallel final lines provide an epiphany: the ritual teaches the living "the way to let go".',
  summary='On the last night of Obon, Haruto writes his barely remembered grandfather\'s name on a lantern and sets it on the river, and his grandmother explains that the ritual helps the living let go.')

P(id='tr_cairo', kind='story', title='extract from a short story set in Cairo, Egypt',
  text=("Every evening Karim's uncle climbed to the roof to fly his pigeons. He whistled, waved a long stick with a rag tied to it, and the flock rose over the satellite dishes and the washing lines.\n"
        "\"Why do they always come back?\" Karim asked.\n"
        "His uncle shrugged. \"Because this is where they are fed. Freedom is a big sky, ya Karim. But it is not dinner.\"\n"
        "That autumn, when Karim's visa letter came, he climbed to the roof alone and stood a long time, watching the birds circle and return, circle and return."),
  culture='Cultural context: rooftop pigeon-keeping is a long tradition in Cairo; the setting of satellite dishes and washing lines shows crowded city life. The phrase "ya Karim" (an Arabic form of address) keeps the uncle\'s voice.',
  symbol='The pigeons symbolise the tension between freedom and belonging: they fly far but always return home. Karim, about to emigrate, sees his own choice in their flight.',
  epiphany='Epiphany: on receiving his visa letter, Karim understands his uncle\'s words – he too will need to balance freedom with the pull of home.',
  conflict='Inner conflict: Karim is torn between the opportunity of leaving and his attachment to home and family.',
  dev=[('symbolism', 'the flock rose over the satellite dishes and the washing lines', 'the pigeons rising over everyday city life suggest the possibility of escape', ['simile', 'statistic', 'onomatopoeia']),
       ('aphorism', 'Freedom is a big sky, ya Karim. But it is not dinner.', 'the uncle\'s wise, humorous saying expresses the story\'s central tension between freedom and security', ['simile', 'hyperbole', 'oxymoron']),
       ('repetition', 'circle and return, circle and return', 'the repeated phrase mimics the birds\' flight and Karim\'s thoughts going round and round', ['alliteration', 'pun', 'flashback'])],
  struct=[('the time jump to "That autumn"', 'moving from a remembered conversation to the visa letter shows how the uncle\'s words gain new meaning')],
  tone='bittersweet', tw=['farcical', 'furious', 'triumphant'], tonex='warm family detail mixes with the sadness of leaving.',
  theme='freedom, home and migration',
  gq='How does the writer use the pigeons as a symbol?',
  gqa='The pigeons rising "over the satellite dishes and the washing lines" suggest escape from crowded daily life, yet they always return. The uncle\'s aphorism "Freedom is a big sky ... But it is not dinner" makes them symbols of the tension between freedom and belonging. When Karim receives his visa letter, he watches them "circle and return, circle and return", and the repetition shows him seeing his own dilemma in their flight.',
  summary='Karim\'s uncle flies pigeons from a Cairo rooftop and explains that they return because home feeds them; when Karim\'s visa arrives, he watches them circle and return.')

P(id='tr_valparaiso', kind='story', title='extract from a short story set in Valparaíso, Chile',
  text=("For twenty years my father kept the key in his wallet, behind his London bus pass. A small brass key to a blue door on Cerro Alegre.\n"
        "\"Why keep it?\" I asked once. \"The house is probably gone.\"\n"
        "He didn't answer.\n"
        "When we finally went back, the door was green. A café now. My father stood outside for a long time, then took out the key, kissed it and slipped it into the café's tip jar.\n"
        "\"There,\" he said, in Spanish. \"Now it is home again.\""),
  culture='Cultural context: Valparaíso\'s hills (cerros) are known for their brightly painted houses; many Chileans went into exile in the 1970s and 1980s during the military dictatorship. The father\'s return after twenty years suggests such an exile.',
  symbol='The key symbolises the father\'s lost home and his hope of return; by giving it away he accepts that the past cannot be recovered but can still be honoured.',
  epiphany='Epiphany: the father\'s act shows that "home" is not the building but his relationship with the place; letting go allows him to reconnect.',
  conflict='Conflict: the father\'s loyalty to the past versus the reality that the house has changed.',
  dev=[('symbolism', 'A small brass key to a blue door', 'the key is a symbol of exile, memory and the hope of return', ['simile', 'hyperbole', 'onomatopoeia']),
       ('juxtaposition', 'behind his London bus pass', 'placing the key beside his London pass shows his two lives, past and present, side by side', ['alliteration', 'pun', 'statistic']),
       ('silence', 'He didn\'t answer.', 'the one-line paragraph suggests feelings too deep or painful to express', ['rhetorical question', 'exclamation', 'simile']),
       ('change of colour', 'the door was green. A café now.', 'the changed colour and fragments show how the past has been replaced, shocking narrator and reader', ['metaphor', 'flashback', 'oxymoron'])],
  struct=[('the twenty-year time span compressed into a few lines', 'the narrator\'s summary focuses attention on the moment of return and the father\'s gesture')],
  tone='poignant', tw=['comic', 'angry', 'detached'], tonex='restrained narration and a quiet gesture create a poignant tone.',
  theme='exile, memory and letting go',
  gq='How does the writer use the key to explore the idea of home?',
  gqa='The "small brass key" kept "behind his London bus pass" juxtaposes the father\'s two lives and symbolises exile and hope of return. His silence when asked why he keeps it shows emotion too deep to express. The fragments "the door was green. A café now." reveal the past has been replaced, yet he kisses the key and gives it to the café: an epiphany in which home is honoured by letting go. "Now it is home again" redefines home as a relationship, not a building.',
  summary='A father keeps the key to his old house in Valparaíso for twenty years; when they return and find it is now a café, he gives the key away and says it is home again.')

# =============================================================================================
# Dystopian fiction
# =============================================================================================
P(id='dys_harmony', kind='prose', title='opening of a dystopian novel',
  text=("Nobody in Unity Sector had been sad for eleven years. It was against the law.\n"
        "Each morning, Citizen 4471 – her friends had once called her Lena – pressed her wrist to the scanner at the factory gate. The band glowed green: Harmony Score 92. Acceptable.\n"
        "Above the gate, the screen showed the Director's smiling face and the words of the day: A HAPPY CITIZEN IS A SAFE CITIZEN.\n"
        "Lena smiled back. She had practised in the mirror. It hardly hurt at all."),
  dystopia='Dystopian conventions: a controlling state (Unity Sector, the Director); surveillance technology (wrist scanners); loss of individuality (Citizen 4471 instead of Lena); propaganda slogans; enforced emotions; a protagonist who conforms outwardly but feels inner resistance.',
  control='Control through language: the slogan "A HAPPY CITIZEN IS A SAFE CITIZEN" equates emotion with safety, and words like "Harmony Score" and "Acceptable" make surveillance sound positive.',
  dev=[('opening hook with irony', 'Nobody in Unity Sector had been sad for eleven years. It was against the law.', 'the first sentence sounds utopian, but the second reveals that happiness is enforced, establishing the dystopia', ['simile', 'onomatopoeia', 'hyperbole']),
       ('naming', 'Citizen 4471 – her friends had once called her Lena', 'replacing a name with a number shows the state erasing individuality; "once" suggests a lost past', ['metaphor', 'alliteration', 'pun']),
       ('propaganda slogan', 'A HAPPY CITIZEN IS A SAFE CITIZEN', 'the slogan links emotion to safety, implying unhappy citizens are dangerous', ['rhetorical question', 'simile', 'understatement']),
       ('understatement', 'It hardly hurt at all.', 'the casual final line reveals the pain of forced smiling and hints at Lena\'s hidden resistance', ['hyperbole', 'onomatopoeia', 'exclamation'])],
  struct=[('ending on Lena\'s practised smile', 'the opening closes on a detail of inner resistance, setting up the conflict between the individual and the state')],
  tone='chillingly calm', tw=['joyful', 'comic', 'romantic'], tonex='flat, matter-of-fact narration makes the oppression more disturbing.',
  theme='enforced conformity and the loss of individuality',
  gq='How does the writer establish a dystopian world in this opening?',
  gqa='The opening hook ironically presents enforced happiness: "Nobody ... had been sad ... It was against the law." The number "Citizen 4471" replacing "Lena" shows loss of individuality, and the wrist scanner and "Harmony Score" reveal surveillance. The slogan "A HAPPY CITIZEN IS A SAFE CITIZEN" shows propaganda controlling emotion. The understated final line "It hardly hurt at all" hints at Lena\'s hidden pain and future rebellion.',
  write=[('Continue the opening (about 300 words): Lena\'s Harmony Score suddenly drops. Maintain the dystopian conventions and calm, chilling tone.', 'Indicative content: consistent close third person; surveillance consequences; propaganda language; tension through pacing; hints of resistance; controlled, chilling tone.')],
  summary='In Unity Sector, where sadness is illegal, Citizen 4471 – once Lena – scans her wrist for a Harmony Score, sees the Director\'s slogan and forces a practised smile.')

P(id='dys_ministry', kind='prose', title='extract from a dystopian novel in which a government department controls vocabulary',
  text=("The Ministry of Clear Speech published the new dictionary every January. This year it was thinner again.\n"
        "\"Protest\" had become \"unhelpful noise\". \"Prison\" was now a \"Calm Centre\". The word \"why\" had been reclassified as \"impolite\" and was no longer taught in schools.\n"
        "Jonah's little sister could not understand the old books on Grandad's shelf. \"What is freedom?\" she asked, sounding it out.\n"
        "Jonah opened his mouth and found he did not have the words to tell her."),
  control='Language as control: by removing and renaming words ("Prison" becomes "Calm Centre"; "why" is "impolite"), the Ministry limits what people can think and question. Jonah\'s inability to explain "freedom" shows that losing words means losing ideas.',
  dystopia='Dystopian conventions: an authoritarian state with an Orwellian-sounding ministry; censorship of language and books; a younger generation raised without key concepts; a protagonist who senses something has been lost.',
  dev=[('euphemism (state-controlled language)', '"Prison" was now a "Calm Centre"', 'the renaming disguises oppression as kindness, like the language of propaganda', ['hyperbole', 'onomatopoeia', 'simile']),
       ('ironic name', 'The Ministry of Clear Speech', 'the ministry does the opposite of what its name says, making speech less clear', ['simile', 'statistic', 'alliteration']),
       ('symbolism', 'This year it was thinner again.', 'the shrinking dictionary symbolises the narrowing of thought and freedom', ['flashback', 'onomatopoeia', 'pun']),
       ('ironic ending', 'found he did not have the words to tell her', 'Jonah himself has been affected: the system has succeeded in limiting his thought', ['cliffhanger only', 'simile', 'rhetorical question'])],
  struct=[('moving from the Ministry\'s policy to one family', 'the shift from state to personal shows the human cost of language control')],
  tone='quietly ominous', tw=['cheerful', 'farcical', 'triumphant'], tonex='matter-of-fact statements about censorship build a quiet sense of menace.',
  vocab=[('reclassified', 'officially put into a different category', ['spelled differently', 'translated', 'forgotten naturally'], 'the bureaucratic word makes censorship sound neutral and routine.')],
  theme='language, power and freedom of thought',
  gq='How does the writer show language being used as a tool of control?',
  gqa='The ironically named "Ministry of Clear Speech" shrinks the dictionary each year, a symbol of narrowing thought. Euphemisms – "Prison" as a "Calm Centre", "Protest" as "unhelpful noise" – disguise oppression, and the banning of "why" prevents questioning. The little sister sounding out "freedom" shows a generation losing concepts, and Jonah\'s discovery that he "did not have the words" reveals that the control has already reached him.',
  summary='A ministry removes and renames words each year; when Jonah\'s sister asks what freedom is, he finds he cannot explain it.')

P(id='dys_escape', kind='prose', title='extract from the climax of a dystopian novel',
  text=("The siren started at 02:14.\n"
        "Lena ran. Past the dormitories, past the dark canteen, past the statue of the Director with its stone smile. Her breath tore at her throat.\n"
        "The fence. Three metres. Wire at the top.\n"
        "Behind her: boots, torches, a voice through a speaker calmly reminding all citizens to remain in their beds for their own safety.\n"
        "She climbed. The wire bit her palms.\n"
        "She did not look down. She did not look back.\n"
        "She jumped."),
  dystopia='Dystopian conventions: the protagonist\'s rebellion and escape; surveillance and pursuit; the calm, controlling voice of the state contrasting with violence.',
  dev=[('short sentences and fragments', 'The fence. Three metres. Wire at the top.', 'the clipped fragments mimic Lena\'s rapid perception and breathlessness, speeding the pace', ['long descriptive sentence', 'simile', 'rhetorical question']),
       ('tricolon with anaphora', 'Past the dormitories, past the dark canteen, past the statue', 'the repeated "past" creates a sense of rushing movement', ['onomatopoeia', 'oxymoron', 'flashback']),
       ('juxtaposition', 'a voice through a speaker calmly reminding all citizens to remain in their beds for their own safety', 'the calm voice contrasts with the chase, exposing the sinister politeness of the regime', ['simile', 'statistic', 'pun']),
       ('one-word final paragraph', 'She jumped.', 'the abrupt ending creates a cliffhanger at the climax', ['circular ending', 'flashback', 'epilogue'])],
  struct=[('the precise time "02:14" as an opening', 'it creates urgency and a sense of a countdown')],
  tone='breathless and tense', tw=['relaxed', 'nostalgic', 'humorous'], tonex='fragments, short paragraphs and verbs of action create breathless tension.',
  theme='rebellion against oppression',
  gq='How does the writer use structure and pacing to create tension in this climax?',
  gqa='The extract opens with a precise time, "02:14", creating urgency. Short sentences and fragments ("The fence. Three metres.") mimic Lena\'s breathless perception, while the anaphora "Past ... past ... past" builds rushing momentum. The calm speaker voice is juxtaposed with the chase, exposing the regime\'s sinister politeness. Increasingly short paragraphs accelerate the pace to the one-line cliffhanger "She jumped."',
  summary='At 02:14 a siren sounds and Lena runs through the compound, climbs the wire fence as guards approach and jumps.')

P(id='dys_tree', kind='prose', title='opening of a dystopian short story',
  text=("The last tree in the city stood in a glass case in Victory Square, guarded by two soldiers and a sign: DO NOT BREATHE ON THE EXHIBIT.\n"
        "Children came on school trips to look at it. They were told it had been saved by the Council, who had also, the teachers explained, saved everyone from the dangerous old days when trees grew wherever they liked.\n"
        "Nadia, aged twelve, pressed her nose to the glass and saw something no one else had noticed.\n"
        "A new leaf."),
  dystopia='Dystopian conventions: environmental collapse; a state that rewrites history ("saved everyone from the dangerous old days"); education as propaganda; a child protagonist who notices something hopeful and subversive.',
  control='The teachers\' explanation rewrites history so that the Council appears as a saviour; nature itself is presented as dangerous and must be controlled.',
  dev=[('absurd sign', 'DO NOT BREATHE ON THE EXHIBIT', 'the ridiculous instruction shows how rare and controlled nature has become, mixing humour with horror', ['simile', 'onomatopoeia', 'metaphor']),
       ('irony', 'saved everyone from the dangerous old days when trees grew wherever they liked', 'freedom and nature are presented as dangerous, revealing the regime\'s propaganda', ['hyperbole only', 'simile', 'pun']),
       ('one-line paragraph', 'A new leaf.', 'the short final line is a symbol of hope and possible rebellion; "a new leaf" also suggests a fresh start', ['cliffhanger with dialogue', 'flashback', 'statistic'])],
  struct=[('ending on a small, hopeful discovery', 'the opening raises a question – what will Nadia do? – and hints that nature and resistance can survive')],
  tone='satirical yet hopeful', tw=['despairing', 'jubilant', 'neutral'], tonex='absurd details and propaganda create dark humour, but the ending offers hope.',
  theme='nature, control and hope',
  gq='How does the writer use the tree to present the dystopian world and a sense of hope?',
  gqa='The tree in a "glass case" guarded by soldiers, with the absurd sign "DO NOT BREATHE ON THE EXHIBIT", shows how rare and controlled nature has become. Irony in the teachers\' claim that the Council saved everyone from "the dangerous old days" exposes propaganda that rewrites history. Nadia\'s discovery of "A new leaf", isolated in a one-line paragraph, symbolises hope and suggests resistance can grow, with a pun on turning over a new leaf.',
  summary='The city\'s last tree is kept in a guarded glass case and used for propaganda on school trips, but twelve-year-old Nadia notices it has grown a new leaf.')

# =============================================================================================
# Advertising and visual texts (images described in words)
# =============================================================================================
P(id='ad_runner', kind='ad', title='magazine advertisement for running shoes (the image is described in words)',
  text=("[Image: a black-and-white photograph of a young woman running alone up a steep, rain-soaked street at dawn. Only her shoes are in colour – bright orange. She is shot from a low angle, so she appears to tower over the city.]\n"
        "Slogan (large, white, top left): YOUR ONLY RIVAL IS YESTERDAY.\n"
        "Small text (bottom right): Olympic 1500 m finalist Zara Kimani trains in Vela Pulse. Built for every kind of morning.\n"
        "Logo: VELA"),
  visual='Visual grammar: the selective colour makes the orange shoes the most salient element; the low-angle shot makes the runner powerful; the rain and empty street suggest determination; the slogan is placed top left, where readers start, and the logo bottom right, where they finish.',
  persuade='Persuasive techniques: an aspirational slogan; celebrity endorsement (an Olympic finalist); the implied promise that the shoes help you improve; targeting young, ambitious runners.',
  dev=[('slogan with personification', 'YOUR ONLY RIVAL IS YESTERDAY', 'the slogan turns running into a battle with your past self, appealing to self-improvement', ['simile', 'onomatopoeia', 'statistic']),
       ('endorsement', 'Olympic 1500 m finalist Zara Kimani trains in Vela Pulse', 'a respected athlete transfers her credibility to the product', ['testimonial from an ordinary customer', 'statistic', 'pun']),
       ('selective colour (salience)', 'Only her shoes are in colour – bright orange', 'colour draws the eye straight to the product in an otherwise grey image', ['symmetry', 'close-up of the logo', 'cartoon style']),
       ('low-angle shot', 'shot from a low angle, so she appears to tower over the city', 'the angle makes the runner seem powerful and heroic, an image the viewer is invited to share', ['high-angle shot', 'bird\'s-eye view', 'long shot of the crowd'])],
  struct=[('the Z-pattern layout from slogan to image to logo', 'the reader\'s eye moves from the message through the image to the brand, ending on the name they should remember')],
  tone='inspirational', tw=['humorous', 'nostalgic', 'menacing'], tonex='the heroic image and slogan create an inspiring, aspirational tone.',
  aud='Young, ambitious runners and people who want to see themselves as determined and disciplined.',
  purp='To sell Vela running shoes by associating them with determination, self-improvement and elite performance.',
  theme='self-improvement and aspiration',
  gq='How does the advertisement use visual and verbal techniques to persuade its audience?',
  gqa='Selective colour makes the orange shoes the most salient element in a black-and-white image, and the low-angle shot makes the runner seem heroic. The rain and empty street suggest determination. The slogan "YOUR ONLY RIVAL IS YESTERDAY" appeals to self-improvement, and the endorsement by an Olympic finalist transfers credibility to the product. The layout leads the eye from slogan to image to the VELA logo, so the brand is the final thing remembered.',
  summary='A black-and-white advert shows a runner in bright orange shoes on a rainy street at dawn, with the slogan "Your only rival is yesterday" and an Olympic athlete\'s endorsement.')

P(id='ad_parody', kind='satire', title='parody advertisement from a school satirical magazine (the image is described in words)',
  text=("[Image: a dramatic close-up of a tired student with dark eyes, lit like a perfume model, holding a tiny bottle labelled EXAM. Gold sparkles drift around her. In the background, a pile of textbooks glows like treasure.]\n"
        "Slogan (elegant gold script): EAU DE EXAM. Because you're worth… a B+.\n"
        "Small text: The scent of revision, panic and cold toast at 2 a.m. Now with notes of highlighter.\n"
        "Warning: may cause sudden memories of the periodic table."),
  intertext='Intertextuality: the text imitates the conventions of luxury perfume adverts – dramatic close-up, glamorous lighting, gold script, a French product name and a famous-sounding slogan – and twists them to mock exam pressure.',
  persuade='It borrows persuasive techniques (aspirational slogan, glamour, sensory description of "notes") but turns them upside down to make readers laugh at the idea that exam stress is glamorous.',
  dev=[('parody of a slogan', 'Because you\'re worth… a B+.', 'the familiar beauty-advert promise collapses into a disappointing grade, creating bathos and humour', ['simile', 'statistic', 'alliteration']),
       ('bathos', 'The scent of revision, panic and cold toast at 2 a.m.', 'the luxurious "scent" language describes unglamorous exam stress, which is funny and recognisable', ['euphemism', 'onomatopoeia', 'oxymoron']),
       ('mock-French name', 'EAU DE EXAM', 'the French phrase imitates perfume branding, making the parody instantly recognisable', ['acronym', 'rhetorical question', 'simile']),
       ('mock warning', 'Warning: may cause sudden memories of the periodic table.', 'imitating legal small print adds absurd humour', ['real safety information', 'testimonial', 'statistic'])],
  struct=[('copying the layout of a luxury advert', 'the familiar structure makes the parody recognisable and the twists funnier')],
  tone='satirical', tw=['solemn', 'menacing', 'sentimental'], tonex='mock-glamour and bathos create a playful, satirical tone.',
  aud='Students who read the school magazine and recognise both perfume adverts and exam stress.',
  purp='To entertain and to satirise both exam pressure and the glamorous promises of advertising.',
  theme='exam pressure and the false promises of advertising',
  gq='How does the parody use the conventions of advertising to create humour and make a point?',
  gqa='The text copies the conventions of a perfume advert – dramatic close-up, gold sparkles, elegant script and the mock-French name "EAU DE EXAM". It parodies a famous-sounding slogan with bathos: "Because you\'re worth… a B+." Luxury "notes" become "revision, panic and cold toast at 2 a.m.", and a mock legal warning adds absurdity. The humour exposes both exam stress and the unrealistic glamour advertising sells.',
  summary='A parody perfume advert called "Eau de Exam" shows a tired student lit like a model, with a slogan promising a B+ and a scent of revision, panic and cold toast.')

P(id='campaign_water', kind='poster', title='poster from a multimodal campaign by a youth climate group (the image is described in words)',
  text=("[Image: a single drop of water falling from a tap. Inside the drop, reflected upside down, is a cracked, dry riverbed. The background is pale blue, almost white.]\n"
        "Headline (bold, dark blue): EVERY DROP HAS A HISTORY.\n"
        "Body text: It takes 2,700 litres of water to make one cotton T-shirt. Before you buy, ask: do I need it?\n"
        "Call to action: Join the #OneShirtChallenge – wear one T-shirt for a week and post your photo.\n"
        "Logo: Youth for Water (bottom centre)"),
  visual='Visual grammar: the drop is the salient central image; the reflected dry riverbed inside it creates a striking visual metaphor linking everyday water use to drought; the pale background and plenty of white space focus attention.',
  campaign='Multimodal campaign: the poster works with social media (the hashtag challenge) so the audience moves from seeing the message to acting and spreading it; the photo challenge makes participants into campaigners.',
  persuade='Persuasive techniques: a shocking statistic (2,700 litres), a rhetorical question addressed to "you", a participatory call to action and a hashtag.',
  dev=[('visual metaphor', 'Inside the drop, reflected upside down, is a cracked, dry riverbed', 'the image links one drop of water to drought elsewhere, making an abstract idea visible', ['simile', 'onomatopoeia', 'alliteration']),
       ('statistic', 'It takes 2,700 litres of water to make one cotton T-shirt', 'the surprising number makes the hidden cost of clothes concrete (logos)', ['anecdote', 'hyperbole', 'endorsement']),
       ('direct address and question', 'Before you buy, ask: do I need it?', 'the question invites readers to reflect on their own habits', ['imperative only', 'pun', 'flashback']),
       ('participatory call to action', 'Join the #OneShirtChallenge', 'the hashtag challenge turns the audience into active, visible participants', ['logo', 'statistic', 'slogan only'])],
  struct=[('the movement from image to headline to statistic to action', 'the poster leads the viewer from emotional impact to evidence to something they can do')],
  tone='thought-provoking', tw=['flippant', 'aggressive', 'nostalgic'], tonex='the restrained design and question encourage reflection rather than guilt.',
  aud='Teenagers and young adults who buy clothes and use social media.',
  purp='To raise awareness of the water used to make clothing and to persuade young people to buy less and join an online challenge.',
  theme='hidden environmental costs of consumption',
  gq='How do the visual and verbal elements of the poster work together to persuade?',
  gqa='The salient image of a water drop containing a reflected dry riverbed is a visual metaphor linking everyday water to drought, and the white space keeps the focus on it. The headline "EVERY DROP HAS A HISTORY" invites curiosity, the statistic "2,700 litres" provides logos, and the question "do I need it?" addresses readers personally. The hashtag call to action extends the campaign onto social media, turning viewers into participants.',
  summary='A campaign poster shows a water drop reflecting a dry riverbed, states that a T-shirt takes 2,700 litres of water to make, and invites young people to join a one-shirt challenge online.')

P(id='ad_phone', kind='ad', title='billboard advertisement for a smartphone (the image is described in words)',
  text=("[Image: a vast white space. In the exact centre, a thin black phone stands upright, casting a long soft shadow. Nothing else.]\n"
        "Text (small, grey, beneath the phone): Less. But better.\n"
        "Bottom corner: NOVA 9. From 1 March."),
  visual='Visual grammar: minimalism – huge white space, a single centred object and small grey text – makes the phone salient and suggests luxury, simplicity and confidence. The long shadow adds elegance and drama.',
  persuade='Persuasive techniques: minimal copy and a short aphoristic slogan suggest a brand so confident it does not need to explain; the release date creates anticipation.',
  dev=[('white space (minimalism)', 'a vast white space ... Nothing else.', 'the emptiness makes the phone the only point of focus and suggests luxury and calm', ['clutter', 'collage', 'bright colour clash']),
       ('central placement (salience)', 'In the exact centre, a thin black phone stands upright', 'centring and contrast (black on white) make the product dominant', ['rule of thirds', 'background placement', 'cropping']),
       ('aphoristic slogan', 'Less. But better.', 'the two short fragments imply quality over quantity and match the minimal design', ['rhetorical question', 'statistic', 'onomatopoeia'])],
  struct=[('the date at the bottom', 'ending on "From 1 March" creates anticipation and a call to action')],
  tone='cool and confident', tw=['desperate', 'chatty', 'humorous'], tonex='minimal design and understated words create a cool, confident tone.',
  aud='Adults and older teenagers who value design and status and can afford premium technology.',
  purp='To build desire and anticipation for a new smartphone by presenting it as elegant and premium.',
  theme='luxury and simplicity as status',
  gq='How does the billboard use minimalism to persuade?',
  gqa='The vast white space and the single phone "in the exact centre" make the product salient and suggest luxury and calm. The black-on-white contrast and long shadow add drama. The aphoristic slogan "Less. But better." matches the minimal design and implies quality, while the brand\'s confidence in saying so little suggests status. The release date "From 1 March" creates anticipation.',
  summary='A minimalist billboard shows a single black phone centred in white space with the words "Less. But better." and a release date.')

# =============================================================================================
# Memoir, personal essay and travel writing
# =============================================================================================
P(id='memoir_tailor', kind='memoir', title='extract from a memoir about the writer\'s grandfather',
  text=("My grandfather's tailor's shop in Leicester smelled of steam and chalk. I spent every Saturday of my childhood under his cutting table, collecting the coloured threads that fell like slow rain.\n"
        "He measured everyone the same way: the bus driver, the bride, the man who came in once a year to have his only suit taken in a little further.\n"
        "I did not understand, then, that he was measuring the whole neighbourhood – its weddings, its funerals, its slow thinning. I understand it now, every time I sew on a button and get it wrong."),
  memoir='Memoir conventions: a first-person adult narrator recalls real childhood experiences; specific sensory details ("steam and chalk"); a focus on a relationship; and reflection that interprets the past ("I did not understand, then ... I understand it now").',
  reflect='Reflection: the narrator realises that the grandfather\'s measuring recorded the life of a community; the humble final detail (getting a button wrong) shows lasting love and loss.',
  dev=[('sensory detail', 'smelled of steam and chalk', 'specific smells recreate the shop vividly and show how strongly the memory has lasted', ['simile', 'statistic', 'onomatopoeia']),
       ('simile', 'coloured threads that fell like slow rain', 'the gentle image captures a child\'s wonder and the slow pace of those Saturdays', ['metaphor', 'hyperbole', 'oxymoron']),
       ('telling detail', 'the man who came in once a year to have his only suit taken in a little further', 'the man\'s shrinking body quietly suggests ageing and poverty, deepening the portrait of the community', ['euphemism', 'pun', 'flashback']),
       ('extended metaphor', 'he was measuring the whole neighbourhood – its weddings, its funerals, its slow thinning', 'the grandfather\'s work becomes a record of the community\'s life and decline', ['simile', 'onomatopoeia', 'alliteration'])],
  struct=[('the shift from past memories to present reflection', 'the final sentences reinterpret the childhood scenes and show what they mean to the adult writer')],
  tone='affectionate and elegiac', tw=['angry', 'comic', 'detached'], tonex='warm sensory memories are touched with loss.',
  theme='memory, family and community',
  gq='How does the writer use memoir conventions to present her grandfather?',
  gqa='The adult narrator recreates childhood through sensory detail – "steam and chalk" – and the simile of threads that "fell like slow rain" conveys wonder. Telling details, like the man whose "only suit" is taken in further, sketch the community. Reflection ("I did not understand, then ... I understand it now") turns memory into meaning: the extended metaphor of "measuring the whole neighbourhood" shows the grandfather recording lives and loss, and the final image of a badly sewn button expresses enduring love.',
  summary='A writer remembers Saturdays in her grandfather\'s tailor\'s shop and realises that by measuring his customers he was recording the life and decline of the neighbourhood.')

P(id='essay_stammer', kind='memoir', title='extract from a personal essay by a young writer',
  text=("For most of my life, my name has been the hardest word I know.\n"
        "\"Th-\" I would begin, and the room would wait, and the wait would fill with kind faces trying not to look kind. Teachers finished my sentences. Friends ordered for me.\n"
        "At fifteen I joined the debate club, mostly by accident. The first time I spoke, I stammered for eleven seconds – I know, because someone timed it.\n"
        "Then I finished my argument. We won.\n"
        "I still stammer. I have simply stopped apologising for the time it takes me to be heard."),
  memoir='Personal essay conventions: a first-person voice exploring an experience to reach an insight; honest, specific detail; a reflective conclusion that addresses a wider idea (being heard).',
  reflect='Reflection: the writer redefines success not as curing the stammer but as refusing to apologise for it; the final sentence moves from personal experience to a general claim about being heard.',
  dev=[('paradox / hook', 'my name has been the hardest word I know', 'the surprising opening grabs attention and immediately introduces the stammer', ['simile', 'onomatopoeia', 'statistic']),
       ('paradox', 'kind faces trying not to look kind', 'the phrase captures how even sympathy can feel uncomfortable and patronising', ['hyperbole', 'alliteration', 'pun']),
       ('precise detail', 'I stammered for eleven seconds – I know, because someone timed it', 'the exact number and wry aside show the cruelty she faced with dry humour', ['euphemism', 'simile', 'flashback']),
       ('short sentences', 'Then I finished my argument. We won.', 'the plain sentences deliver the triumph without fuss, matching the writer\'s calm confidence', ['rhetorical question', 'long periodic sentence', 'onomatopoeia'])],
  struct=[('ending on a present-tense reflection', 'the final sentence turns the story into a statement of identity and self-acceptance')],
  tone='candid and quietly defiant', tw=['self-pitying', 'farcical', 'bitter'], tonex='honest detail, dry humour and calm statements create a candid, quietly defiant tone.',
  aud='General readers, including young people who have struggled to be heard.',
  purp='To reflect on living with a stammer and to challenge the idea that fluent speech is required to be heard.',
  theme='voice, identity and self-acceptance',
  gq='How does the writer present her experience of stammering?',
  gqa='The paradoxical hook "my name has been the hardest word I know" introduces the stammer powerfully. The phrase "kind faces trying not to look kind" captures uncomfortable sympathy, and the lists of teachers and friends speaking for her show lost agency. The precise "eleven seconds" and wry aside reveal cruelty with dry humour. Short sentences ("We won.") deliver triumph calmly, and the present-tense ending reframes success as self-acceptance: she has "stopped apologising".',
  write=[('Write a personal essay (about 400 words) about a moment when you had to find your voice. End with a reflection that connects your experience to a wider idea.', 'Indicative content: first-person reflective voice; a specific, vividly told moment; honest detail; a structure that moves from experience to insight; a concluding reflection on a wider idea; controlled, varied style.')],
  summary='A young writer describes years of others speaking for her because of her stammer, joining a debate club, stammering for eleven seconds and winning, and refusing to apologise for needing time.')

P(id='travel_hanoi', kind='travel', title='extract from a travel article about Hanoi, Vietnam',
  text=("The guidebook had promised me \"timeless Old Quarter charm\". What I found at seven in the morning was Mrs Thu, who has sold phở from the same corner for thirty-one years, scrolling the football scores on her phone while her broth simmered.\n"
        "I had come looking for an unchanging, exotic past. Hanoi was busy being a modern city, and it was not waiting for me.\n"
        "Mrs Thu handed me a bowl and a pair of chopsticks. \"Too much photo,\" she said, nodding at my camera. \"Eat first.\" She was right."),
  represent='Representation of place and culture: the writer questions the guidebook\'s clichéd image ("timeless ... charm") and the tourist\'s wish for an "exotic past", presenting Hanoi instead as a modern city and Mrs Thu as a named individual with her own voice and authority.',
  dev=[('contrast with a cliché', '"timeless Old Quarter charm" ... scrolling the football scores on her phone', 'the contrast punctures the stereotype of an unchanging Asia and shows a real, modern person', ['simile', 'onomatopoeia', 'hyperbole']),
       ('self-critical reflection', 'I had come looking for an unchanging, exotic past.', 'the writer admits his own bias, encouraging readers to question their expectations', ['boast', 'statistic', 'pun']),
       ('giving the local person a voice', '"Too much photo," she said ... "Eat first."', 'Mrs Thu\'s words correct the tourist, giving her authority rather than making her a background figure', ['silence', 'stereotype', 'euphemism']),
       ('specific detail', 'who has sold phở from the same corner for thirty-one years', 'precise details present Mrs Thu as an individual with a history, not as scenery', ['vague generalisation', 'simile', 'onomatopoeia'])],
  struct=[('ending on "She was right."', 'the short final sentence shows the traveller learning from the local person, reversing the usual power of the travel writer')],
  tone='self-deprecating and respectful', tw=['arrogant', 'mournful', 'furious'], tonex='the writer gently mocks his own expectations and respects Mrs Thu\'s view.',
  aud='Readers of a travel magazine or website, possibly planning a trip.',
  purp='To describe Hanoi while challenging stereotyped, exoticised representations of the city.',
  theme='representation of place and culture in travel writing',
  gq='How does the writer challenge stereotypical representations of Hanoi?',
  gqa='The writer sets the guidebook\'s cliché "timeless Old Quarter charm" against Mrs Thu "scrolling the football scores on her phone", puncturing the stereotype of an unchanging past. He admits his own bias ("I had come looking for an unchanging, exotic past"), and presents Mrs Thu with specific detail (thirty-one years on the same corner) and her own voice ("Too much photo ... Eat first."). The final "She was right" gives the local person authority over the traveller.',
  summary='A travel writer expecting a timeless, exotic Hanoi meets Mrs Thu, a phở seller checking football scores, who tells him to stop photographing and eat; he admits she was right.')

P(id='travel_atacama', kind='travel', title='extract from a travel blog about the Atacama Desert, Chile',
  text=("At four in the morning, in the driest desert on Earth, I lay on a frozen ground sheet and watched the Milky Way rise like smoke from behind the volcano.\n"
        "Our guide, Rodrigo, whose grandmother herded llamas on these salt flats, pointed out the dark shapes between the stars. \"Other people see constellations,\" he said. \"My people saw a llama, a fox, a toad – in the dark spaces.\"\n"
        "I have looked at the night sky my whole life. That night was the first time I had been taught how to see it."),
  represent='Representation of culture: the local guide is presented as an expert with ancestral knowledge (the Andean "dark constellations"), and the writer acknowledges learning a new way of seeing rather than presenting the place only as a spectacle.',
  dev=[('simile', 'watched the Milky Way rise like smoke from behind the volcano', 'the image makes the stars seem alive and mysterious, conveying awe', ['metaphor', 'hyperbole', 'onomatopoeia']),
       ('superlative', 'the driest desert on Earth', 'the extreme fact sets the scene as remarkable and remote', ['understatement', 'rhetorical question', 'pun']),
       ('quotation of a local voice', '"My people saw a llama, a fox, a toad – in the dark spaces."', 'Rodrigo\'s words show a different cultural way of reading the sky, giving him authority', ['statistic', 'stereotype', 'euphemism']),
       ('reflective ending', 'That night was the first time I had been taught how to see it.', 'the writer\'s reflection shows humility and the value of local knowledge', ['cliffhanger', 'boast', 'flashback'])],
  struct=[('the movement from spectacle to a local voice to reflection', 'the extract shifts the focus from scenery to people and knowledge')],
  tone='awed and humble', tw=['bored', 'arrogant', 'sarcastic'], tonex='wonder at the sky and respect for Rodrigo create an awed, humble tone.',
  aud='Readers of a travel blog interested in adventurous, meaningful travel.',
  purp='To recreate the experience of stargazing in the Atacama and to share what the writer learned from a local guide.',
  theme='learning to see a place through local knowledge',
  gq='How does the writer present the Atacama and its people?',
  gqa='The superlative "the driest desert on Earth" and the simile of the Milky Way rising "like smoke" create awe. Rodrigo is introduced through his heritage (a grandmother who herded llamas) and quoted directly about Andean "dark" constellations, giving him expertise. The reflective ending – "the first time I had been taught how to see it" – shows the writer\'s humility, presenting the place through the knowledge of its people rather than as mere scenery.',
  summary='A travel blogger stargazing in the Atacama learns from guide Rodrigo how his ancestors saw animals in the dark spaces between stars, and feels taught to see the sky anew.')

# =============================================================================================
# Model narrative (show not tell, dialogue)
# =============================================================================================
P(id='model_car', kind='story', title='extract from a short story in which two siblings argue',
  text=("\"You can't sell it,\" Leo said. \"It's Dad's.\"\n"
        "\"It was Dad's.\" Mira didn't look up from the laptop. \"Now it's a car that needs new brakes.\"\n"
        "Leo picked at the peeling sticker on the fridge – a football club Dad had supported, badly, for forty years.\n"
        "\"He sang in that car,\" Leo said.\n"
        "Mira's typing stopped. For a long moment there was only the hum of the fridge.\n"
        "\"I know,\" she said. \"I know he did.\""),
  show='Show, not tell: the writer never says "they were grieving". Grief is shown through the shift from "It\'s" to "It was", Leo picking at the sticker, Mira\'s typing stopping and the silence filled by the fridge\'s hum.',
  dialogue='Dialogue reveals character and conflict: Leo speaks emotionally, Mira practically, and the subtext is their shared grief for their father. The repeated "I know" shows Mira finally letting her feelings through.',
  dev=[('correction in dialogue', '"It was Dad\'s."', 'changing the tense shows Mira forcing herself to accept their father\'s death', ['simile', 'onomatopoeia', 'hyperbole']),
       ('telling action', 'Leo picked at the peeling sticker on the fridge', 'the small, nervous action shows Leo\'s distress without stating it', ['flashback', 'pun', 'statistic']),
       ('silence and sound', 'For a long moment there was only the hum of the fridge.', 'the pause slows the pace and lets emotion fill the gap between words', ['exclamation', 'rhetorical question', 'alliteration']),
       ('repetition', '"I know," she said. "I know he did."', 'the repetition shows Mira\'s practical mask slipping', ['simile', 'oxymoron', 'onomatopoeia'])],
  struct=[('the turning point when Mira\'s typing stops', 'the change in action marks the emotional climax of the scene')],
  tone='tender and restrained', tw=['comic', 'angry', 'triumphant'], tonex='understated dialogue and small actions create a restrained, tender tone.',
  theme='grief and how people show it differently',
  gq='How does the writer use dialogue and action to show, rather than tell, the siblings\' feelings?',
  gqa='The writer never names the emotion. Mira\'s correction "It was Dad\'s" shows her forcing acceptance, while Leo\'s nervous picking at the sticker shows distress. The detail that Dad supported the club "badly, for forty years" adds affectionate humour. When Mira\'s typing stops and "there was only the hum of the fridge", the silence lets grief fill the scene, and the repeated "I know" shows her practical mask slipping. Subtext carries the meaning.',
  write=[('Rewrite the scene from Mira\'s point of view in the first person (about 250 words), keeping the subtext: do not use the words "sad" or "grief".', 'Indicative content: first-person Mira; practical surface thoughts; hints of suppressed grief through action and sensory detail; correctly punctuated dialogue; subtext rather than statement.')],
  summary='Leo objects to Mira selling their late father\'s car; she insists practically that it needs brakes until he says their father sang in it, and she admits she knows.')

# =============================================================================================
# Pairs for comparison (Task 1 style)
# =============================================================================================
K.pair('speech_reef', 'speech_lincoln', 'Compare how the two speakers use rhetoric to inspire their audiences to act.',
       'Both speakers address powerful audiences at a moment of crisis and turn the past into a call for future action. Lincoln uses a solemn, biblical register ("Four score and seven years ago"), a rising tricolon ("dedicate ... consecrate ... hallow") and the democratic tricolon "of the people, by the people, for the people" to give soldiers\' deaths meaning. The student uses personal ethos ("born the year the reef first turned white"), an accusatory tricolon ("You have heard ... seen ... nodded"), a rhetorical question about her children and antithesis ("not ... promises ... decisions"). Whereas Lincoln unites his audience with inclusive "we", she divides "you" from "us" to shame delegates into action; both end with a memorable image of the future.',
       sim='both use tricolon and a focus on the future to persuade their audience to commit to a cause.',
       diff='Lincoln\'s tone is solemn and unifying ("we"), whereas the student\'s is urgent and accusatory ("you").')
K.pair('speech_truth', 'speech_reef', 'Compare how the two speakers challenge the people who hold power over them.',
       'Both speakers are outsiders challenging powerful audiences. Truth refutes "That man over there" with her own experience, uses imperatives ("Look at my arm!") and the refrain "And ain\'t I a woman?" to expose hypocrisy. The student uses her lifetime of reef bleaching as ethos, a tricolon of inaction ("heard ... seen ... nodded") and the rhetorical question about her children. Both use personal experience as evidence and repetition for emphasis; however, Truth\'s defiance is direct and confrontational, while the student\'s is controlled and formal, ending with a demand for "decisions". Context matters: Truth, a formerly enslaved woman in 1851, risked far more by speaking.',
       sim='both use personal experience as evidence and repetition to challenge a powerful audience.',
       diff='Truth confronts a named opponent with a defiant refrain, whereas the student addresses delegates formally and demands specific action.')
K.pair('speech_lincoln', 'speech_mayor', 'Compare how the two speeches respond to loss and look to the future.',
       'Both speeches are given soon after tragedy and move from grief to resolve. Lincoln honours the dead with a solemn, biblical register, a rising tricolon ("dedicate ... consecrate ... hallow") and an extended metaphor of birth, ending with democracy that "shall not perish". The mayor personifies the flood as an intruder ("without knocking"), lists losses, then uses anaphora ("I have seen ...") to celebrate community, ending with antithesis: "Not because it is easy, but because it is ours." Lincoln gives national, abstract meaning to sacrifice, whereas the mayor focuses on local, concrete kindness; both use inclusive pronouns to unite listeners.',
       sim='both move from grief to determination and use inclusive "we/our" to unite their audience.',
       diff='Lincoln gives deaths an abstract national meaning, whereas the mayor celebrates concrete, local acts of kindness.')
K.pair('stadium_a', 'stadium_b', 'Compare how the two reports present the same council decision.',
       'Both report the same facts (a £300m stadium, 2,000 jobs, 140 households), but framing differs. Text A\'s headline foregrounds "2,000 JOBS AND \'A NEW HEART\'", quotes only the council leader and softens the cost with the euphemism "relocated", ending with celebrating fans. Text B\'s headline foregrounds "FAMILIES FACE EVICTION", quotes a 62-year-old resident ("Nobody asked us"), introduces the jobs figure with the distancing "claims" and gives critics the last word. Selection, order and word choice create opposite representations of the same event.',
       sim='both report the same core facts – the vote, the £300m cost, 2,000 jobs and 140 households.',
       diff='Text A frames the decision as regeneration through the council leader\'s voice, whereas Text B frames it as eviction through a resident\'s voice.')
K.pair('viral_post', 'factcheck', 'Compare how the two texts try to convince readers that they are telling the truth.',
       'Both texts address the same claim and want readers\' trust, but use opposite methods. The viral post relies on urgency and fear ("SHARE BEFORE THEY DELETE THIS"), anonymous or vague sources ("My cousin", "Doctors are saying"), conspiracy framing and visual alarm (capitals, emoji). The fact-check uses a calm structure (question, method, evidence, verdict), a named source quoted directly, precise details ("up to four hours on Tuesday") and a clear label. Whereas the post asks readers to act before thinking, the fact-check models how to check before sharing.',
       sim='both address the same claim and present themselves as revealing the truth to the public.',
       diff='the post relies on fear and unverifiable sources, whereas the fact-check uses named sources, precise evidence and a calm tone.')
K.pair('leaving_poem', 'leaving_letter', 'Compare how the two texts present the experience of leaving home.',
       'Both texts use spices and small domestic details to represent home and loss. In the poem, spices are "wrapped in a jumper like a sleeping child", and the conceit "as if a country could be carried / in small glass jars" shows the impossibility of carrying home. In the letter, cardamom "tastes of the box it came in", showing home cannot be recreated. The poem uses free verse, enjambement and a lingering final word ("looking") to show grief continuing into the present; the letter uses intimate address, understated sentences ("I let them.") and selective truth to protect her mother. The poem looks back years later; the letter is written in the raw present of arrival.',
       sim='both use spices and domestic details to show that home cannot be fully carried to a new place.',
       diff='the poem looks back from the present with lasting grief, whereas the letter speaks from the immediate loneliness of arrival and hides pain from family.')
K.pair('shelley_mask', 'poem_chant', 'Compare how the two poems use language and form to create a voice of protest.',
       'Both poems address people in power through a collective voice and use repetition and memorable endings. Shelley uses imperatives ("Rise", "Shake"), similes of lions and dew, rhyming couplets and a chant-like rhythm, ending with the antithesis "Ye are many—they are few". The modern poem uses free verse and anaphora ("They told us ..."), each answered by "We", an epigram ("you can\'t negotiate with a thermometer") and the closing metaphor "We are the weather now". Shelley addresses the oppressed and urges them to rise; the modern poem speaks as the protesters, directly confronting adults. Contexts differ: Peterloo in 1819 and today\'s climate protests.',
       sim='both use a collective voice, repetition and a memorable, chantable final line to inspire resistance.',
       diff='Shelley uses rhyme and regular rhythm to address the oppressed, whereas the modern poem uses free verse to confront those in power directly.')
K.pair('poem_checkpoint', 'poem_wall', 'Compare how the two poems present the effects of division and conflict on ordinary people.',
       'Both poems present conflict through its effect on daily and family life rather than battles. "Checkpoint" uses free verse, a list of school objects and the simile "like a country / they suspect" to show a child treated as a threat; her anger is "folded / small enough to fit / between the pages". The sonnet uses the metaphor of a "seam of grey" stitching the city and the antithesis "so close, so far", with a volta ("But walls are only stone") leading to reunion. "Checkpoint" ends with suppressed anger in an ongoing situation; the sonnet ends with a bittersweet resolution, as sisters "learned each other\'s names again". Free verse suits ongoing tension, while the sonnet\'s ordered form suits a story with an ending.',
       sim='both show political division through its effect on ordinary people, using everyday details.',
       diff='"Checkpoint" ends with suppressed anger in an unresolved situation, whereas the sonnet moves through a volta to a bittersweet reunion.')
K.pair('coa_shipyard', 'memoir_tailor', 'Compare how the two writers look back on a parent or grandparent\'s working life.',
       'Both texts use adult narrators looking back on childhood to reinterpret a relative\'s work. The novel extract uses the euphemism "between ships", the symbol of "empty cranes" and the closing reflection that "bravery and pride can look exactly the same" to reveal the father\'s shame after redundancy. The memoir uses sensory detail ("steam and chalk"), the simile of threads like "slow rain" and the metaphor of "measuring the whole neighbourhood" to celebrate the grandfather\'s role. Both shift from past to present ("I know now"; "I understand it now"); however, the novel exposes hidden pain linked to industrial decline, while the memoir expresses affectionate elegy for a community.',
       sim='both use retrospective adult narrators who reinterpret childhood memories of a relative\'s work.',
       diff='the novel reveals hidden shame after job loss, whereas the memoir affectionately celebrates the grandfather\'s place in his community.')
K.pair('tr_cairo', 'tr_valparaiso', 'Compare how the two stories use a symbol to explore the idea of home.',
       'Both stories use a single object or image – pigeons and a key – to explore the pull between leaving and belonging. In the Cairo story, pigeons that always return, and the uncle\'s aphorism "Freedom is a big sky ... But it is not dinner", help Karim face emigration; the repetition "circle and return" ends the story with his uncertainty. In the Valparaíso story, the key "behind his London bus pass" symbolises exile; when the father gives it away, he finds an epiphany: "Now it is home again." The first story looks forward to leaving with unresolved feelings, whereas the second looks back after return and achieves resolution.',
       sim='both use a central symbol to explore the tension between leaving and belonging.',
       diff='the Cairo story ends unresolved as Karim prepares to leave, whereas the Valparaíso story ends with the father\'s resolution after returning.')
K.pair('dys_harmony', 'dys_ministry', 'Compare how the two dystopian extracts show a state controlling its citizens.',
       'Both extracts present authoritarian states that control people through language and erase individuality. Text A uses surveillance (wrist scanners, "Harmony Score 92"), a number replacing a name and the slogan "A HAPPY CITIZEN IS A SAFE CITIZEN" to show emotions controlled. Text B shows control through vocabulary: euphemisms ("Prison" becomes "Calm Centre"), the shrinking dictionary and the banning of "why". Both end on a quiet personal moment – Lena\'s practised smile, Jonah lacking words – but Text A hints at resistance, whereas Text B suggests the control has already succeeded.',
       sim='both use euphemistic, state-controlled language and end on a quiet personal moment that reveals the cost of control.',
       diff='Text A controls emotion through surveillance and hints at resistance, whereas Text B controls thought through vocabulary and suggests the control has succeeded.')
K.pair('ad_runner', 'ad_parody', 'Compare how the two texts use the conventions of advertising for different purposes.',
       'Both texts use advertising conventions – a striking image, a slogan, small print and a product name – but for opposite purposes. Text A sincerely persuades: selective colour makes the shoes salient, a low-angle shot makes the runner heroic, and the slogan "YOUR ONLY RIVAL IS YESTERDAY" and an Olympic endorsement promise self-improvement. Text B parodies perfume adverts: glamorous lighting on a tired student, the mock-French "EAU DE EXAM" and the bathetic slogan "Because you\'re worth… a B+." mock both exam stress and advertising glamour. Text A sells aspiration; Text B satirises it.',
       sim='both use a dramatic image, a slogan and small print – the conventions of advertising.',
       diff='Text A uses them sincerely to sell aspiration, whereas Text B parodies them to mock exam pressure and advertising\'s promises.')
K.pair('travel_hanoi', 'travel_atacama', 'Compare how the two travel writers represent the places and people they encounter.',
       'Both writers avoid presenting the place as mere scenery and give local people a voice. In Hanoi, the writer contrasts the guidebook cliché "timeless Old Quarter charm" with Mrs Thu checking football scores, admits his own bias and lets her correct him ("Eat first"). In the Atacama, the writer uses awe-filled imagery (the Milky Way "like smoke") and quotes Rodrigo\'s ancestral knowledge of the dark constellations. Both end with humble reflection ("She was right"; "taught how to see it"), but the Hanoi writer is self-mocking and challenges stereotypes directly, whereas the Atacama writer is awed and celebrates cultural knowledge.',
       sim='both give a local person a direct voice and end with the writer\'s humble reflection.',
       diff='the Hanoi writer mocks his own stereotyped expectations, whereas the Atacama writer expresses awe and celebrates ancestral knowledge.')
K.pair('mac_dagger', 'mac_tomorrow', 'Compare how Shakespeare presents Macbeth\'s state of mind in these two soliloquies.',
       'Both soliloquies reveal Macbeth\'s inner life through questions, imagery and the flexibility of blank verse. Before the murder (Text A), rhetorical questions ("Is this a dagger ...?"), apostrophe and the metaphor "A dagger of the mind" show a feverish, guilty imagination; enjambement mimics racing thoughts. Near the end (Text B), the slow repetition "Tomorrow, and tomorrow, and tomorrow", the metaphor "brief candle" and the theatre metaphor "a poor player" show despair. Text A presents a man on the edge of crime, full of fear; Text B presents a man emptied by its consequences – the tragic arc from temptation to recognition.',
       sim='both are soliloquies that use questions, metaphor and blank verse to reveal Macbeth\'s disturbed mind.',
       diff='Text A shows feverish fear before the murder, whereas Text B shows numb despair after its consequences.')
K.pair('essay_stammer', 'speech_captain', 'Compare how the two writers present the challenge of speaking to others.',
       'Both texts are about being heard, and both use humour and short sentences. The personal essay reflects on stammering: the paradoxical hook "my name has been the hardest word I know", the phrase "kind faces trying not to look kind" and the precise "eleven seconds" reveal struggle; the ending redefines success as refusing to apologise. The speech performs confident speaking: a humorous tricolon of impossible promises, the repeated "actually" and a petition statistic win trust. The essay is reflective and personal, written to be read; the speech is persuasive and public, written to be heard.',
       sim='both use humour and short, plain sentences to show the importance of being heard.',
       diff='the essay reflects privately on the struggle to speak, whereas the speech is a public, persuasive performance.')


# =============================================================================================
# ch01 Speeches and Rhetoric
# =============================================================================================
SP = ['speech_reef', 'speech_lincoln', 'speech_truth', 'speech_captain', 'speech_mayor', 'phonesfree']
H('ch01-st1',
  terms=[('ethos', 'an appeal to the speaker\'s credibility, character or authority'),
         ('pathos', 'an appeal to the audience\'s emotions, such as pity, guilt, pride or fear'),
         ('logos', 'an appeal to logic and reason through evidence, statistics and argument'),
         ('rhetoric', 'the art of using language effectively to persuade or influence an audience'),
         ('kairos', 'the right or opportune moment for an argument; using timing and context to persuade')],
  facts=[('Which ancient Greek thinker described ethos, pathos and logos in his "Rhetoric"?', 'Aristotle', ['Homer', 'Pythagoras', 'Archimedes'], 'Aristotle analysed the three modes of persuasion.'),
         ('"I was born the year the reef first turned white." Which appeal does this mainly use?', 'Ethos – the speaker\'s personal authority as a witness', ['Logos – statistical proof', 'Kairos – a deadline', 'None – it is purely descriptive'], 'Her life gives her credibility.'),
         ('"Police figures show youth crime fell by 12 per cent." Which appeal is this?', 'Logos', ['Pathos', 'Ethos', 'Bathos'], 'Statistics appeal to reason.'),
         ('Which line from a speech appeals most strongly to pathos?', '"What will you tell my children when they ask what coral looked like?"', ['"The report was published on Monday."', '"There are three main proposals."', '"I have chaired this committee for ten years."'], 'It evokes guilt and grief.')],
  why=[('Explain why the most effective speeches combine ethos, pathos and logos.', 'Each appeal reaches the audience differently: ethos earns trust, logos provides reasons and pathos moves people to act; relying on one alone can seem untrustworthy, cold or manipulative.'),
       ('Explain why a young speaker might rely on ethos from personal experience rather than expertise.', 'Without professional authority, a young speaker can still be credible as a witness to how a problem affects their life and future.'),
       ('Explain why too much pathos can weaken a speech.', 'Audiences may feel manipulated if emotion replaces evidence, especially sceptical or expert listeners.')],
  contrast=[('ethos', 'logos', 'Ethos persuades through who the speaker is (credibility, character); logos persuades through what is argued (evidence, reasoning).'),
            ('pathos', 'bathos', 'Pathos genuinely evokes strong emotion; bathos is an anticlimax from the serious to the trivial, often for comic effect.')],
  misc=[('Logos means using long words to sound logical.', 'Logos is about evidence and reasoning – statistics, facts, cause and effect – not complex vocabulary.'),
        ('Ethos only comes from being famous or an expert.', 'Ethos can come from personal experience, honesty, humility or shared identity with the audience.')],
  apply=[('Write one sentence for a speech about school lunches that uses each appeal: ethos, pathos and logos.', 'E.g. Ethos: "As someone who has eaten school lunch every day for five years..."; Pathos: "No child should spend the afternoon too hungry to think."; Logos: "Seventy per cent of students surveyed skip lunch because of cost." Credit one per appeal.', 3),
         ('Identify the main appeal in each line: (a) "Look at my arm!" (b) "of the people, by the people, for the people" (c) "ninety of us signed the petition".', '(a) ethos/pathos – her body as evidence and emotional challenge; (b) pathos/ethos – stirring democratic ideal; (c) logos – a statistic.', 3)],
  evaluate=[('Pathos is the most powerful of the three appeals.', ['emotion moves people to act', 'memorable images stay with audiences'], ['without evidence, emotion can seem manipulative', 'ethos is needed for the audience to trust the speaker'], 'Pathos is often decisive, but it works best when supported by credible ethos and convincing logos.')],
  extended=[('Choose a famous speech you have studied. Analyse how the speaker uses ethos, pathos and logos to persuade the audience.', 'Indicative content: examples of each appeal with quotation; effect on the original audience; links to context; evaluation of which appeal is most effective. Criteria A and B.', 8, 'long')])
pq('ch01-st1', ('C2', 'C3', 'C4'), (1, 5), None, 'appeals', ['Identify how the speaker uses ethos, pathos and logos in this speech.',
                                                         'Which rhetorical appeal is most important in this speech? Explain with evidence.',
                                                         'Analyse how the speaker combines different rhetorical appeals to persuade the audience.'], ids=SP, crit=CRIT_A)
pq('ch01-st1', ('C2', 'C3'), (1, 4), None, 'aud', AUD_Q, ids=SP, crit=CRIT_A)
pq('ch01-st1', 'C3', (2, 4), None, 'dev', ['Which appeal – ethos, pathos or logos – does "{quote}" use? Explain how it persuades the audience.'], ids=SP, crit=CRIT_B)
K.dev_mcq('ch01-st1', ids=SP)
K.kind_mcq('ch01-st1', ids=SP + ['uniform', 'library_letter', 'editorial_curfew'])

H('ch01-st2',
  terms=[('anaphora', 'repetition of a word or phrase at the start of successive clauses or sentences ("I have seen ... I have seen ...")'),
         ('tricolon (rule of three)', 'a series of three parallel words, phrases or clauses'),
         ('antithesis', 'the placing of contrasting ideas side by side in balanced phrases ("not because it is easy, but because it is ours")'),
         ('rhetorical question', 'a question asked for effect rather than to get an answer'),
         ('epistrophe', 'repetition of a word or phrase at the end of successive clauses'),
         ('direct address', 'speaking directly to the audience using "you"')],
  facts=[('"We do not need more promises. We need decisions." This is an example of:', 'antithesis', ['anaphora', 'onomatopoeia', 'euphemism'], 'Contrasting ideas are balanced.'),
         ('"I have seen teenagers ... I have seen a baker ... I have seen neighbours" uses:', 'anaphora', ['antithesis', 'epistrophe', 'alliteration'], 'Repetition at the start of clauses.'),
         ('"government of the people, by the people, for the people" is a famous example of:', 'tricolon', ['oxymoron', 'simile', 'litotes'], 'Three parallel phrases.'),
         ('The refrain "And ain\'t I a woman?" at the end of sections is an example of:', 'epistrophe / refrain', ['anaphora', 'tricolon', 'simile'], 'Repetition at the end of sections.')],
  why=[('Explain why speeches use more repetition than written essays.', 'Listeners cannot reread, so repetition helps them follow and remember key ideas and creates a rhythm that is powerful when heard.'),
       ('Explain why the tricolon is so common in speeches.', 'Three items feel complete and rhythmic; the pattern is easy to remember and the third item can carry extra emphasis.'),
       ('Explain why antithesis makes a point memorable.', 'Balanced contrasts sharpen the difference between two ideas, often in a neat, quotable form.')],
  contrast=[('anaphora', 'epistrophe', 'Anaphora repeats words at the start of clauses; epistrophe repeats them at the end.'),
            ('a rhetorical question', 'a hypophora', 'A rhetorical question expects no answer; hypophora is when the speaker asks a question and then answers it.')],
  misc=[('Naming a rhetorical device is enough for a good analysis.', 'Analysis must explain how the device works and what effect it has on the audience in context.'),
        ('Every list of three is an effective tricolon.', 'A tricolon is effective when the items are parallel, purposeful and build towards a climax.')],
  apply=[('Write a sentence about protecting a local park that uses anaphora and a tricolon.', 'E.g. "We will protect its trees, we will protect its birds, we will protect the place where our children learn to play." Credit repeated opening and three parallel parts.', 2),
         ('Rewrite "Recycling is important and we should do it" as an antithesis.', 'E.g. "Recycling is not a chore we owe the council; it is a gift we owe our children." Credit balanced contrast.', 2)],
  evaluate=[('Rhetorical devices make speeches manipulative.', ['devices can stir emotion without evidence', 'they can disguise weak arguments'], ['devices help audiences follow and remember', 'they can serve honest, important causes'], 'Devices are tools: they can manipulate or clarify, so audiences should judge the argument they serve.')],
  extended=[('Analyse how rhetorical devices are used in a speech you have studied to persuade its audience.', 'Indicative content: identifies anaphora, tricolon, antithesis, rhetorical questions with quotations; explains effects on listeners; links to purpose and context; organised argument. Criteria A and B.', 8, 'long')])
pq('ch01-st2', ('C2', 'C3', 'C4'), (1, 5), None, 'dev', DEV_Q + ['Analyse how the rhetorical device in "{quote}" affects listeners hearing the speech aloud.'], ids=SP, crit=CRIT_B)
pq('ch01-st2', ('C2', 'C3'), (1, 4), None, 'struct', STRUCT_Q, ids=SP, crit=CRIT_B)
para('ch01-st2', None, ids=SP, c='C4', d=(3, 5), frames=['{gq} Focus on at least three rhetorical devices.',
                                                        'Write an analytical response (about 250 words) explaining how rhetorical devices make this speech persuasive.'])
K.dev_mcq('ch01-st2', ids=SP)
K.vocab('ch01-st2', ids=SP)

H('ch01-st3',
  terms=[('audience', 'the people a speech is addressed to, including those listening live and those reading or watching later'),
         ('purpose', 'what a speaker wants to achieve: to persuade, inspire, inform, console or entertain'),
         ('context', 'the circumstances of a speech: time, place, occasion, events and the speaker\'s situation'),
         ('occasion', 'the specific event at which a speech is delivered, such as a dedication, a rally or an assembly'),
         ('register', 'the level of formality of language, chosen to suit audience and occasion')],
  facts=[('Lincoln\'s Gettysburg Address was delivered in November 1863 at:', 'the dedication of a military cemetery during the American Civil War', ['his first inauguration', 'the end of the Second World War', 'a women\'s rights convention'], 'It honoured soldiers killed at Gettysburg.'),
         ('Sojourner Truth\'s famous speech (1851) was given at:', 'a women\'s rights convention in Akron, Ohio', ['the White House', 'a Civil War battlefield', 'a London theatre'], 'It addressed women\'s rights.'),
         ('Why is the 1863 text of Sojourner Truth\'s speech treated with caution by historians?', 'It was published by Frances Gage twelve years later and differs from an 1851 newspaper report', ['It was written in French', 'It was banned for 100 years', 'Truth wrote it herself in 1900'], 'Versions differ.'),
         ('Which register suits a speech at a memorial service?', 'Formal and solemn', ['Slang and jokes', 'Text-message abbreviations', 'Technical jargon only'], 'Register must suit the occasion.')],
  why=[('Explain why knowing the context of a speech helps you analyse it.', 'Context explains why the speaker chose certain words, what the audience already felt and what was at stake, so effects can be judged accurately.'),
       ('Explain why a speech can have more than one audience.', 'Speakers address the live crowd but also wider audiences who read reports or watch recordings, sometimes including opponents or future generations.'),
       ('Explain why speakers adapt register to their audience.', 'The right level of formality builds trust and shows respect for the occasion; the wrong register can alienate listeners.')],
  contrast=[('the immediate audience', 'the wider audience', 'The immediate audience hears the speech live; the wider audience encounters it later through media, and may have different views.'),
            ('purpose', 'context', 'Purpose is what the speaker aims to achieve; context is the situation in which the speech is given.')],
  misc=[('Context means a summary of the speaker\'s biography.', 'Context is relevant only when linked to how it shapes the speech\'s language, purpose and audience response.'),
        ('A speech has only one purpose.', 'Many speeches combine purposes, e.g. to console and to inspire, or to entertain and to persuade.')],
  apply=[('Suggest how the mayor\'s flood speech would need to change if delivered to government ministers asking for funding.', 'E.g. more logos (cost of damage, numbers affected), a more formal register, specific requests, less emphasis on local anecdotes; still some pathos to show human impact.', 3),
         ('Identify the audience, purpose and context of a school captain election speech.', 'Audience: fellow students (and teachers); purpose: to win votes; context: a short, live assembly speech in a school election, where students are sceptical of empty promises.', 3)],
  evaluate=[('A great speech can be understood without knowing its context.', ['universal themes and devices still move readers', 'many famous lines are quoted out of context'], ['context explains choices and stakes', 'misreading is likely without it'], 'Great speeches can move later audiences, but their full meaning depends on understanding their original context.')],
  extended=[('Analyse how a speaker adapts language to audience, purpose and context in a speech you have studied.', 'Indicative content: identifies audience, purpose and context; links specific choices (register, devices, appeals) to these; considers the wider audience. Criteria A and B.', 8, 'long')])
pq('ch01-st3', ('C2', 'C3', 'C4'), (1, 5), None, 'context', ['Explain how the audience, purpose and context of this speech shape its language.',
                                                         'How does the context of this speech help explain the speaker\'s choices?',
                                                         'Identify the audience and purpose of this speech and explain how the speaker adapts to them.'], ids=SP, crit=CRIT_A)
pq('ch01-st3', ('C2', 'C3'), (1, 4), None, 'purp', PURP_Q, ids=SP, crit=CRIT_A)
pq('ch01-st3', ('C2', 'C3'), (1, 3), None, 'tone', TONE_Q, ids=SP, crit=CRIT_A)
K.tone_mcq('ch01-st3', ids=SP)

H('ch01-st4',
  terms=[('hook', 'an opening designed to grab the audience\'s attention: an anecdote, question, shocking fact or quotation'),
         ('call to action', 'a direct request for the audience to do something specific'),
         ('signposting', 'phrases that guide listeners through the structure ("First...", "But here is the real problem...")'),
         ('delivery', 'how a speech is performed: pace, pause, volume, eye contact and gesture'),
         ('peroration', 'the final, climactic section of a speech, designed to inspire')],
  facts=[('Which is the strongest hook for a speech on food waste?', '"Last night, this school threw away 300 uneaten lunches."', ['"Today I am going to talk about food waste."', '"Hello, my name is Sam."', '"Food is a thing that people eat."'], 'A specific shocking fact grabs attention.'),
         ('Why should speech-writers include pauses in delivery?', 'To let key points sink in and to create emphasis', ['To fill time', 'To remember the next line', 'Because the audience asked'], 'Pauses create emphasis.'),
         ('Which is the clearest call to action?', '"Sign the petition at the library before Friday."', ['"Someone should do something."', '"Think about it."', '"Thanks for listening."'], 'It is specific and actionable.')],
  why=[('Explain why a speech should end with a call to action.', 'It turns agreement into action and leaves the audience with a clear, memorable instruction.'),
       ('Explain why signposting is more important in speeches than in essays.', 'Listeners cannot see paragraphs or reread, so spoken signposts help them follow the structure.'),
       ('Explain why a personal anecdote can be an effective opening.', 'A short story makes the topic human and relatable, builds ethos and engages emotion before the argument begins.')],
  contrast=[('writing a speech', 'writing an essay', 'A speech is written for the ear, using direct address, repetition, signposting and shorter sentences; an essay is written for the eye and can be more complex and detailed.')],
  misc=[('Speaking faster makes a speech more exciting.', 'Varying pace and using pauses is more effective; rushing makes speeches hard to follow.'),
        ('A speech should include every point you can think of.', 'Effective speeches focus on a few strong points, developed and repeated, because listeners remember little detail.')],
  apply=[('Write the opening hook (two or three sentences) for a speech persuading your school to ban single-use plastic.', 'Credit an anecdote, shocking fact or question that grabs attention and introduces the topic; direct address.', 2),
         ('Write a peroration (about 60 words) for a speech asking Year 10 to volunteer at a food bank, using a tricolon and a call to action.', 'Credit an emotive climax, a tricolon, inclusive language and a specific call to action.', 3)],
  evaluate=[('Delivery matters more than content in a speech.', ['confident delivery engages and convinces', 'pauses and tone add meaning'], ['weak arguments are exposed eventually', 'written speeches are judged on content'], 'Delivery can make or break a speech, but it works best in service of strong, well-organised content.')],
  extended=[('Write a persuasive speech (400–500 words) to be delivered to your school\'s leadership team, arguing for a change you believe in. Use a hook, a clear structure, rhetorical devices and a call to action.', 'Indicative content: direct address; a hook; signposted structure; ethos, pathos and logos; at least three rhetorical devices; counterargument; peroration with call to action; appropriate formal register. Criteria B, C, D.', 12, 'long')])
write('ch01-st4', ids=SP + ['uniform'])
pq('ch01-st4', ('C3', 'C4'), (2, 5), None, 'struct', ['Explain how {feature} makes this speech effective, and how you would use the same technique in your own speech.'], ids=SP, crit=CRIT_B)
pq('ch01-st4', 'C3', (2, 4), None, 'dev', ['Imagine you are delivering this speech. Explain how you would perform the line "{quote}" (pace, pause, emphasis) and why.'], ids=SP, crit=CRIT_OPEN)
para('ch01-st4', None, ids=SP, c='C4', d=(3, 5), frames=['{gq} Then suggest one way the speech could be improved for a teenage audience.'])


# =============================================================================================
# ch02 Coming-of-Age Novel Study
# =============================================================================================
COA = ['coa_shipyard', 'coa_results', 'coa_court', 'coa_lake', 'newgirl']
H('ch02-st1',
  terms=[('characterisation', 'the methods a writer uses to create and develop a character: actions, speech, thoughts, appearance and others\' reactions'),
         ('dynamic character', 'a character who changes significantly during the story'),
         ('static character', 'a character who stays essentially the same'),
         ('coming-of-age novel (Bildungsroman)', 'a novel that follows a young person\'s psychological and moral growth into adulthood'),
         ('foil', 'a character whose contrasting qualities highlight those of another')],
  facts=[('A novel that follows a young person\'s growth into adulthood is called a:', 'Bildungsroman', ['tragedy', 'satire', 'epic'], 'German for "novel of formation".'),
         ('In the lake extract, Ama is best described as:', 'a dynamic character', ['a static character', 'a foil only', 'an unreliable narrator'], 'She changes across time.'),
         ('Which is an example of indirect characterisation?', 'Showing a character hiding an art portfolio under her bed', ['Stating "Mei was secretly artistic"', 'Listing her age', 'Giving her name'], 'Indirect characterisation shows through action.'),
         ('Which coming-of-age novel is narrated by Scout Finch, looking back on her childhood?', 'To Kill a Mockingbird', ['Frankenstein', 'Macbeth', 'Nineteen Eighty-Four'], 'Scout narrates retrospectively.')],
  why=[('Explain why writers use indirect characterisation.', 'Showing through action and speech lets readers infer character for themselves, which is more engaging and convincing than being told.'),
       ('Explain why character development is central to the coming-of-age genre.', 'The genre is about growing up, so the main character\'s change in understanding, values or identity is the core of the story.'),
       ('Explain why writers often use a turning point to show character development.', 'A key event forces the character to make a choice or see differently, making change visible and believable.')],
  contrast=[('direct characterisation', 'indirect characterisation', 'Direct characterisation tells the reader what a character is like; indirect characterisation shows it through actions, speech, thoughts and others\' reactions.'),
            ('a dynamic character', 'a static character', 'A dynamic character changes in an important way; a static character remains essentially the same.')],
  misc=[('A character must change dramatically to be dynamic.', 'Change can be subtle – a new understanding or a small act of independence can mark development.')],
  apply=[('Write two sentences of indirect characterisation that show a teenager is nervous about starting at a new school, without using the word "nervous".', 'E.g. "Jas checked the timetable for the fourth time, though she already knew it by heart. Her sandwich went back home uneaten." Credit action/detail revealing feeling.', 2),
         ('Trace Ama\'s development across the lake extract in three stages, with a quotation for each.', 'At eleven: fearful, obeys grandmother ("would not go past the jetty"); fourteen: controls fear ("counting strokes"); sixteen: free ("swam out past the last buoy", "She did not count").', 3)],
  evaluate=[('A coming-of-age story needs a dramatic event to show growth.', ['trials, deaths and conflicts force change', 'turning points make growth visible'], ['quiet moments of realisation can be just as powerful', 'growth can be gradual'], 'Dramatic events often trigger growth, but subtle, everyday moments can show development equally well.')],
  extended=[('Analyse how a writer presents the development of a central character in a coming-of-age novel you have studied.', 'Indicative content: stages of development; direct and indirect characterisation with evidence; turning points; links to themes; organised analysis. Criteria A and B.', 8, 'long')])
pq('ch02-st1', ('C2', 'C3', 'C4'), (1, 5), None, 'char', CHAR_Q + ['How does the writer show that the character is changing or growing up?'], ids=COA, crit=CRIT_A)
pq('ch02-st1', ('C2', 'C3'), (1, 4), None, 'dev', ['Explain what "{quote}" reveals about the character.', 'How does "{quote}" help to characterise the people in this extract?'], ids=COA, crit=CRIT_B)
para('ch02-st1', None, ids=COA, c='C4', d=(3, 5))
K.vocab('ch02-st1', ids=COA)

H('ch02-st2',
  terms=[('retrospective narrator', 'a narrator who looks back on past events from a later point in life, often with greater understanding'),
         ('limited narrator', 'a narrator, often third person, whose knowledge is restricted to one character\'s perceptions and thoughts'),
         ('narrative voice', 'the distinctive personality, tone and language of the narrator'),
         ('dramatic irony', 'when the reader understands more than a character does'),
         ('free indirect discourse', 'third-person narration that takes on a character\'s thoughts and voice without quotation marks')],
  facts=[('"I know now that bravery and pride can look exactly the same" is a sign of:', 'a retrospective narrator', ['an omniscient narrator', 'a second-person narrator', 'a stage direction'], '"I know now" shows hindsight.'),
         ('The results-day extract is narrated in:', 'third-person limited', ['first person', 'second person', 'third-person omniscient'], 'It stays close to Mei only.'),
         ('A retrospective narrator often creates:', 'a gap between the child\'s understanding and the adult\'s', ['a list of facts', 'stage directions', 'a rhyme scheme'], 'Hindsight creates a double perspective.')],
  why=[('Explain why a writer might choose a retrospective first-person narrator for a coming-of-age novel.', 'The adult narrator can recreate a child\'s experience while adding hindsight, so readers see both innocence and later understanding.'),
       ('Explain why third-person limited narration suits a story about a character\'s private doubts.', 'It keeps readers close to one character\'s thoughts while allowing some distance, so we share her doubts but also see her situation clearly.'),
       ('Explain why a child narrator can make injustice more striking.', 'A child describes events without adult explanations or excuses, so the injustice appears raw and obvious to the reader.')],
  contrast=[('a retrospective narrator', 'a present-tense narrator', 'A retrospective narrator looks back with hindsight; a present-tense narrator experiences events as they happen, without later knowledge.'),
            ('third-person limited', 'third-person omniscient', 'Limited narration follows one character\'s perspective; omniscient narration can enter many minds and comment freely.')],
  misc=[('First-person narrators are always reliable because they were there.', 'First-person narrators are limited by memory, bias and age; retrospective narrators may also reinterpret the past.')],
  apply=[('Rewrite this sentence to show a retrospective narrator\'s hindsight: "My mother told me we were going on holiday."', 'E.g. "My mother told me we were going on holiday; it would be years before I understood that we were never coming back." Credit a clear hindsight signal.', 2),
         ('Rewrite the first two sentences of the courtroom extract in third-person limited narration.', 'E.g. "The courtroom was smaller than the ones on television, and quieter, she noticed. Nobody shouted \'Objection!\'." Credit consistent third person staying close to the sister\'s perceptions.', 2)],
  evaluate=[('A retrospective narrator is the best choice for a coming-of-age novel.', ['hindsight adds reflection and meaning', 'it shows growth explicitly'], ['present-tense or limited narration creates immediacy and suspense', 'hindsight can remove uncertainty'], 'Retrospective narration suits reflective novels, but immediate or limited narration can create more tension and intimacy.')],
  extended=[('Analyse how the narrative voice shapes the reader\'s response in a coming-of-age novel you have studied.', 'Indicative content: identifies narrative perspective; analyses hindsight, limitation or dramatic irony with evidence; effect on reader; links to theme. Criteria A and B.', 8, 'long')])
pq('ch02-st2', ('C2', 'C3', 'C4'), (1, 5), None, 'pov', POV_Q, ids=COA + ['coa_court'], crit=CRIT_A)
pq('ch02-st2', ('C2', 'C3'), (1, 4), None, 'retro', ['How does the writer show that the narrator is looking back on past events?', 'Explain the effect of the gap between the child\'s view and the adult narrator\'s view.'], ids=['coa_shipyard'], crit=CRIT_A)
pq('ch02-st2', 'C3', (2, 4), None, 'dev', ['How does "{quote}" reveal the narrator\'s perspective?'], ids=COA, crit=CRIT_B)
para('ch02-st2', None, ids=['coa_shipyard', 'coa_results', 'coa_court'], c='C4', d=(3, 5), frames=['{gq} Focus on how the narrative voice shapes the reader\'s response.'])

H('ch02-st3',
  terms=[('historical context', 'the time and events in which a novel is set or written'),
         ('social context', 'the social conditions, attitudes and structures (class, gender, race, work) that shape characters\' lives'),
         ('deindustrialisation', 'the decline of heavy industries such as shipbuilding, coal and steel, causing unemployment in whole communities'),
         ('setting', 'the time and place of a story, including its social atmosphere')],
  facts=[('In 1980s Britain, many communities were affected by:', 'the closure of shipyards, mines and factories', ['the invention of the printing press', 'the abolition of the monarchy', 'the First World War'], 'Deindustrialisation caused mass unemployment.'),
         ('The euphemism "between ships" in the shipyard extract reflects:', 'the shame attached to unemployment in the father\'s community', ['the father\'s love of sailing', 'a holiday', 'a naval battle'], 'Social context explains the euphemism.'),
         ('Which question best uses context in analysis?', '"How does the 1980s setting help explain the father\'s silence?"', ['"What year was the author born?"', '"How many pages is the novel?"', '"What is the author\'s favourite food?"'], 'Context must explain the text.')],
  why=[('Explain why understanding social context can change how we judge a character.', 'Context reveals the pressures and values a character lives with, so behaviour that seems strange (like hiding unemployment) becomes understandable.'),
       ('Explain why writers set coming-of-age stories at moments of social change.', 'Personal change mirrors social change, so a young person\'s growth can reflect wider shifts in their community or country.')],
  contrast=[('the context of setting', 'the context of writing', 'The context of setting is the time the story takes place; the context of writing is when the author wrote it – they may be decades apart.')],
  misc=[('Context paragraphs should list historical facts.', 'Context is only useful when it explains specific choices or meanings in the text.')],
  apply=[('Explain how the 1980s setting helps the reader understand the father in the shipyard extract.', 'Closures caused mass unemployment and shame; the father\'s euphemism, work boots and visits to the empty cranes show his pride and loss of identity in that context.', 3),
         ('Suggest how Danny\'s trial in the courtroom extract might be read differently by a reader who has experienced the justice system and one who has not.', 'One may recognise the intimidation and silencing; the other may see the court as fair and be shocked by the narrator\'s view. Credit two reasoned readings.', 3)],
  evaluate=[('A novel\'s historical context matters less than its universal themes.', ['themes like growing up are timeless', 'readers relate to feelings, not dates'], ['context shapes characters\' choices and meanings', 'ignoring context can lead to misreading'], 'Universal themes make novels last, but context explains how those themes are shaped in a specific time and place.')],
  extended=[('Explain how the historical and social context of a novel you have studied shapes its characters and themes.', 'Indicative content: relevant context; specific links to characters\' choices and themes; textual evidence; avoids bolted-on history. Criteria A and B.', 8, 'long')])
pq('ch02-st3', ('C2', 'C3', 'C4'), (1, 5), None, 'context', ['How does the historical or social context help you understand this extract?',
                                                         'Explain how the setting in time and place shapes the characters\' experiences.'], ids=['coa_shipyard', 'nobel_mum', 'leaving_letter', 'tr_valparaiso'], crit=CRIT_A)
pq('ch02-st3', ('C2', 'C3'), (1, 4), None, 'theme', THEME_Q, ids=COA, crit=CRIT_OPEN)
pq('ch02-st3', 'C3', (2, 4), None, 'char', ['Explain how the social pressures of the character\'s world shape their behaviour in this extract.'], ids=COA, crit=CRIT_A)
K.tone_mcq('ch02-st3', ids=COA)

H('ch02-st4',
  terms=[('theme', 'a central idea explored in a text, such as identity, justice or growing up'),
         ('identity', 'a person\'s sense of who they are, shaped by family, culture, choices and experiences'),
         ('justice', 'fairness in the way people are treated, by individuals and by institutions'),
         ('loss of innocence', 'the moment a young character realises a hard truth about the adult world'),
         ('motif', 'a recurring image, object or idea that develops a theme')],
  facts=[('"That was the day I learned that justice is a room where you are not allowed to speak" shows:', 'loss of innocence', ['comic relief', 'a flashback to childhood joy', 'a foil'], 'The narrator learns a hard truth.'),
         ('Mei\'s hidden art portfolio most clearly develops the theme of:', 'identity and expectations', ['war', 'the supernatural', 'travel'], 'It symbolises her hidden self.'),
         ('Which statement is a theme rather than a topic?', '"Growing up means seeing parents as flawed human beings."', ['"Parents"', '"Shipyards"', '"A lake"'], 'A theme is an idea about a topic.')],
  why=[('Explain why the theme of justice is common in coming-of-age novels.', 'Young people often first discover unfairness as they grow up; facing injustice tests their values and marks their entry into the adult world.'),
       ('Explain why writers use symbols to develop themes of identity.', 'Objects like a hidden portfolio or a buoy make abstract ideas concrete and memorable for readers.')],
  contrast=[('a topic', 'a theme', 'A topic is a subject (family); a theme is the idea the text explores about it (growing up means seeing parents clearly).')],
  misc=[('A text has only one theme.', 'Most texts explore several connected themes, such as identity, justice and growing up.')],
  apply=[('Write a thematic statement (one sentence) for the courtroom extract.', 'E.g. "The extract suggests that growing up means discovering that institutions can silence the people who love the accused." Credit an idea, not a topic.', 2),
         ('Choose two extracts and explain how each develops the theme of growing up.', 'E.g. lake – overcoming fear and claiming freedom (passing the buoy); results – questioning parental expectations (hidden portfolio). Credit two developed, supported links.', 3)],
  evaluate=[('Coming-of-age stories are mainly about loss rather than gain.', ['loss of innocence and certainty', 'characters lose childhood comforts'], ['characters gain independence, insight and identity', 'loss and gain are linked'], 'Coming-of-age stories usually show both: losing innocence is the price of gaining understanding and independence.')],
  extended=[('Explore how a coming-of-age novel you have studied presents the themes of identity and justice.', 'Indicative content: thematic statements; analysis of characters, symbols and events with evidence; links between themes; context. Criteria A and B.', 8, 'long')])
pq('ch02-st4', ('C2', 'C3', 'C4'), (1, 5), None, 'theme', THEME_Q + ['Explain how this extract explores the idea of growing up.'], ids=COA + ['tr_cairo', 'essay_stammer'], crit=CRIT_OPEN)
pq('ch02-st4', ('C2', 'C3'), (1, 4), None, 'dev', ['How does "{quote}" contribute to a theme of identity, justice or growing up?'], ids=COA, crit=CRIT_B)
para('ch02-st4', None, ids=COA, c='C4', d=(3, 5), frames=['{gq} Link your analysis to the themes of identity, justice or growing up.'])
write('ch02-st4', ids=COA)


# =============================================================================================
# ch03 Poetry of Conflict and Protest
# =============================================================================================
POEMS = ['shelley_mask', 'ozymandias', 'poem_checkpoint', 'poem_wall', 'poem_chant', 'leaving_poem']
H('ch03-st1',
  terms=[('sonnet', 'a fourteen-line poem, usually in iambic pentameter, with a set rhyme scheme and a volta (turn)'),
         ('volta', 'the turn in a sonnet where the argument or mood shifts'),
         ('free verse', 'poetry without regular rhyme or metre'),
         ('iambic pentameter', 'a line of ten syllables in five iambs (da-DUM), e.g. "They BUILT the WALL the SUMmer I was BORN"'),
         ('enjambement', 'when a sentence runs on from one line to the next without punctuation'),
         ('caesura', 'a pause in the middle of a line, usually marked by punctuation')],
  facts=[('How many lines does a sonnet have?', '14', ['10', '12', '16'], 'A sonnet has fourteen lines.'),
         ('A Shakespearean sonnet ends with:', 'a rhyming couplet', ['a single unrhymed line', 'a refrain', 'a haiku'], 'Three quatrains and a couplet.'),
         ('"Checkpoint", with no regular rhyme or metre, is written in:', 'free verse', ['iambic pentameter', 'ballad metre', 'terza rima'], 'It has no fixed pattern.'),
         ('"Nothing beside remains. Round the decay" contains:', 'a caesura', ['a refrain', 'a rhyming couplet', 'onomatopoeia'], 'The full stop creates a mid-line pause.')],
  why=[('Explain why a poet might use the sonnet form to write about conflict.', 'The ordered, traditional form can contrast with chaos, and its volta can dramatise a turn from conflict to hope, or from boast to ruin.'),
       ('Explain why free verse suits poems about ongoing conflict.', 'Its irregular lines can mimic disruption, stop-start rhythms and voices that do not fit neat patterns, reflecting unresolved situations.'),
       ('Explain why enjambement can create tension.', 'Running lines on delays meaning and creates momentum or a held breath across the line break.')],
  contrast=[('enjambement', 'caesura', 'Enjambement runs a sentence over a line break; caesura is a pause within a line.'),
            ('a Petrarchan sonnet', 'a Shakespearean sonnet', 'A Petrarchan sonnet has an octave and a sestet with the volta at line 9; a Shakespearean sonnet has three quatrains and a final couplet, with the turn often at line 9 or in the couplet.')],
  misc=[('Form is just decoration in poetry.', 'Form shapes meaning: rhyme, metre and line breaks control pace, emphasis and mood.'),
        ('Free verse has no structure.', 'Free verse uses deliberate line breaks, stanza shapes and repetition to create structure without regular rhyme or metre.')],
  apply=[('Mark the stressed syllables in "They built the wall the summer I was born" and name the metre.', 'they BUILT the WALL the SUMmer I was BORN – iambic pentameter (five iambs).', 2),
         ('Identify the volta in the sonnet about the divided city and explain its effect.', 'Line 9, "But walls are only stone, and stone grows old" – shifts from division to hope and reunion.', 2)],
  evaluate=[('Traditional forms like the sonnet are less suitable than free verse for modern protest poetry.', ['free verse feels immediate and natural', 'protest resists rules'], ['sonnets\' order can contrast powerfully with chaos', 'the volta can dramatise change'], 'Both can work; the best choice depends on whether the poet wants order to contrast with chaos or form to mirror disruption.')],
  extended=[('Analyse how a poet uses form, structure and metre to convey ideas about conflict or protest in a poem you have studied.', 'Indicative content: identifies form, rhyme, metre, line breaks and stanza structure with examples; explains how each shapes meaning; organised analysis. Criteria A and B.', 8, 'long')])
pq('ch03-st1', ('C2', 'C3', 'C4'), (1, 5), None, 'form', ['Explain how the form of this poem contributes to its meaning.',
                                                      'Analyse how the poet uses structure and line breaks for effect.',
                                                      'Identify the form of this poem and explain why the poet might have chosen it.'], ids=POEMS, crit=CRIT_A)
pq('ch03-st1', ('C2', 'C3'), (1, 4), None, 'struct', STRUCT_Q, ids=POEMS, crit=CRIT_B)
K.dev_mcq('ch03-st1', ids=POEMS)

H('ch03-st2',
  terms=[('imagery', 'descriptive language that appeals to the senses and creates pictures in the reader\'s mind'),
         ('metaphor', 'a direct comparison that says one thing is another'),
         ('simile', 'a comparison using "like" or "as"'),
         ('alliteration', 'repetition of initial consonant sounds in nearby words'),
         ('assonance', 'repetition of vowel sounds in nearby words'),
         ('sibilance', 'repetition of "s" and "sh" sounds')],
  facts=[('"Rise like Lions after slumber" is an example of:', 'a simile', ['a metaphor', 'onomatopoeia', 'personification only'], 'It uses "like".'),
         ('"a seam of grey that stitched the city through" is an example of:', 'a metaphor', ['a simile', 'alliteration only', 'a rhetorical question'], 'The wall is described as a seam.'),
         ('"The lone and level sands stretch far away" uses:', 'alliteration', ['onomatopoeia', 'oxymoron', 'a simile'], 'Repeated "l" sounds.'),
         ('"Hover through the fog and filthy air" uses which sound device?', 'Alliteration', ['Assonance only', 'Rhyme only', 'Onomatopoeia'], 'Repeated "f" sounds.')],
  why=[('Explain why poets about conflict often focus on small, concrete images.', 'Concrete details (a pencil case, an apple) make large, abstract conflicts personal and believable, creating empathy.'),
       ('Explain why sound devices matter in protest poetry.', 'Protest poems are often performed aloud; alliteration, rhythm and repetition make lines memorable, chantable and forceful.'),
       ('Explain why a metaphor can be more powerful than a simile.', 'A metaphor states that one thing is another, creating a stronger, more direct identification than the comparison "like".')],
  contrast=[('a simile', 'a metaphor', 'A simile compares using "like" or "as"; a metaphor says one thing is another.'),
            ('alliteration', 'assonance', 'Alliteration repeats consonant sounds at the start of words; assonance repeats vowel sounds within words.')],
  misc=[('Alliteration always creates a soft effect.', 'The effect depends on the sounds: hard "d" or "b" sounds can sound harsh; "s" sounds can be soothing or sinister.')],
  apply=[('Write a metaphor and a simile describing a border fence, each suggesting a different feeling.', 'E.g. metaphor: "The fence is a scar across the valley" (pain); simile: "The fence glittered like a necklace of knives" (danger). Credit two different effects.', 2),
         ('Explain the effect of the alliteration in "boundless and bare / The lone and level sands".', 'The "b" and "l" sounds slow and stretch the lines, echoing the endless, empty desert and the disappearance of power.', 2)],
  evaluate=[('Imagery is more important than sound in poetry about conflict.', ['images make conflict visible and personal', 'they create empathy'], ['sound creates mood and memorability', 'protest poems are performed'], 'Imagery and sound work together; imagery makes us see conflict, sound makes us feel and remember it.')],
  extended=[('Analyse how a poet uses imagery and sound to present conflict or protest in a poem you have studied.', 'Indicative content: identifies imagery (simile, metaphor, symbol) and sound devices with quotation; explains effects; links to message. Criteria A and B.', 8, 'long')])
pq('ch03-st2', ('C2', 'C3', 'C4'), (1, 5), None, 'dev', DEV_Q + ['Analyse the imagery in "{quote}" and explain what it suggests about conflict.'], ids=POEMS, crit=CRIT_B)
pq('ch03-st2', ('C2', 'C3'), (1, 4), None, 'tone', TONE_Q, ids=POEMS, crit=CRIT_A)
para('ch03-st2', None, ids=POEMS, c='C4', d=(3, 5), frames=['{gq} Focus on imagery and sound.'])
K.vocab('ch03-st2', ids=POEMS)

H('ch03-st3',
  terms=[('tone', 'the attitude of the poet or speaker towards the subject or audience'),
         ('perspective', 'the point of view from which a poem presents its subject'),
         ('protest poetry', 'poetry that criticises injustice, oppression or war and calls for change'),
         ('speaker', 'the voice in a poem, which may not be the poet'),
         ('irony', 'a gap between what is said and what is meant, or between expectation and reality')],
  facts=[('Shelley wrote "The Mask of Anarchy" in response to:', 'the Peterloo Massacre of 1819', ['the Battle of Waterloo', 'the French Revolution of 1789', 'the First World War'], 'Cavalry attacked a peaceful reform meeting in Manchester.'),
         ('The tone of "Ye are many—they are few" is best described as:', 'rousing', ['melancholy', 'resigned', 'playful'], 'It rallies the people.'),
         ('"Ozymandias" mainly presents a perspective on:', 'the impermanence of tyrants\' power', ['the joy of travel', 'romantic love', 'childhood'], 'The ruined statue mocks power.'),
         ('The collective "we" in a protest poem creates:', 'a sense of solidarity and shared purpose', ['an unreliable narrator', 'a sonnet', 'comic relief'], 'It speaks for a group.')],
  why=[('Explain why the speaker of a protest poem may use "we" rather than "I".', '"We" presents the protest as collective, giving it strength in numbers and including the reader.'),
       ('Explain why some protest poems use a restrained tone rather than an angry one.', 'Restraint can make injustice seem more shocking, as readers feel the anger the speaker holds back.'),
       ('Explain why irony is useful in poems criticising power.', 'Irony exposes the gap between what the powerful claim and the reality, as in "Look on my Works ... Nothing beside remains."')],
  contrast=[('tone', 'mood', 'Tone is the speaker\'s attitude; mood is the feeling created in the reader.'),
            ('the poet', 'the speaker', 'The poet is the writer; the speaker is the voice in the poem, which may be a persona.')],
  misc=[('Protest poetry is always angry.', 'Protest poems can be restrained, ironic, mournful or hopeful; tone is chosen for effect.')],
  apply=[('Identify the tone of "Checkpoint" and quote two details that create it.', 'Restrained/indignant: "She has learned to stand still"; "her anger folded / small enough to fit".', 3),
         ('Explain the perspective of "Ozymandias" on tyranny in two sentences.', 'The poem suggests that tyrants\' power is temporary; time and nature destroy even the mightiest rulers, making their boasts ironic.', 2)],
  evaluate=[('Poetry can change the world.', ['poems inspire movements and are quoted at protests', 'they create empathy'], ['laws and actions change the world, not words alone', 'many readers never see protest poems'], 'Poetry rarely changes events alone, but it can shape feelings and memory and inspire people who do.')],
  extended=[('Analyse how the poet presents a perspective on conflict or protest in a poem you have studied, focusing on tone.', 'Indicative content: identifies speaker, perspective and tone with evidence; analyses language and form that create tone; links to context. Criteria A and B.', 8, 'long')])
pq('ch03-st3', ('C2', 'C3', 'C4'), (1, 5), None, 'persp', ['What is the poet\'s perspective on conflict or protest? Support your answer with evidence.',
                                                       'Explain how the poem presents a particular attitude towards power or conflict.'], ids=POEMS, crit=CRIT_A)
pq('ch03-st3', ('C2', 'C3'), (1, 4), None, 'tone', TONE_Q, ids=POEMS, crit=CRIT_A)
pq('ch03-st3', ('C2', 'C3'), (1, 4), None, 'context', ['How does knowing the context help you understand the poem\'s perspective?'], ids=['shelley_mask', 'ozymandias'], crit=CRIT_A)
K.tone_mcq('ch03-st3', ids=POEMS)

H('ch03-st4',
  terms=[('comparative thesis', 'a statement summarising the key similarity and difference between two texts'),
         ('point of comparison', 'an aspect such as theme, form, imagery or tone used to compare'),
         ('comparative connectives', 'words that link texts: both, similarly, likewise, whereas, however, in contrast'),
         ('integrated comparison', 'discussing both texts within each paragraph')],
  facts=[('Which is the best comparative thesis on "Checkpoint" and the wall sonnet?', '"Both poems show division through ordinary lives, but whereas \'Checkpoint\' ends in suppressed anger, the sonnet moves to a bittersweet reunion."', ['"Both are poems."', '"I like the sonnet more."', '"\'Checkpoint\' is about a girl."'], 'It states similarity and difference.'),
         ('Which connective signals contrast?', 'Whereas', ['Similarly', 'Likewise', 'Both'], '"Whereas" contrasts.'),
         ('Which point of comparison is most useful for two protest poems?', 'How each uses repetition and a collective voice', ['The number of words in each', 'The font size', 'The poets\' birthdays'], 'It compares methods.')],
  why=[('Explain why comparing form is valuable when comparing two poems.', 'Form choices (sonnet vs free verse) shape meaning differently, so comparing them reveals how each poet\'s method supports their message.'),
       ('Explain why a comparative essay should discuss both texts in each paragraph.', 'Integrated comparison keeps the relationship between the texts in focus and avoids two separate analyses.')],
  contrast=[('a similarity', 'a difference', 'A similarity is a shared feature; a difference is a contrast. Strong comparisons explain why each matters for meaning.')],
  misc=[('Comparison means finding as many differences as possible.', 'Strong comparison explores significant similarities and differences and explains their effects.')],
  apply=[('Write a comparative topic sentence on the endings of "Checkpoint" and the wall sonnet.', 'E.g. "While \'Checkpoint\' ends with anger \'folded\' away in an unresolved situation, the sonnet closes with a couplet of bittersweet reunion."', 2),
         ('List three points of comparison for Shelley\'s stanza and the modern protest poem.', 'E.g. collective voice/address; repetition and imperatives; form (rhyme vs free verse); final lines; context (1819 vs climate protest).', 3)],
  evaluate=[('Comparing poems from different centuries is less useful than comparing modern poems.', ['shared context makes comparison easier', 'modern language is accessible'], ['different contexts reveal how protest has changed', 'similarities across time show universal concerns'], 'Comparing across centuries can be especially revealing, as it shows both continuity and change in how poets protest.')])
K.compare('ch03-st4', c='C4', d=(3, 5), frames=['{q}', '{q} Consider form, imagery and tone.'], only=POEMS + ['grandmother_kitchen'])
K.compare_short('ch03-st4', c=('C2', 'C3'), d=(1, 4), only=POEMS + ['grandmother_kitchen'])
pq('ch03-st4', ('C2', 'C3'), (1, 4), None, 'form', ['Explain how the form of this poem shapes its meaning, and suggest how a poem on a similar theme might use a different form.'], ids=POEMS, crit=CRIT_A)


# =============================================================================================
# ch04 Shakespeare: Macbeth
# =============================================================================================
MAC = ['mac_witches', 'mac_aside', 'mac_dagger', 'mac_blood', 'mac_tomorrow']
H('ch04-st1',
  terms=[('tragedy', 'a drama in which a protagonist of high status falls from fortune to disaster, usually through a flaw, ending in death'),
         ('tragic hero', 'a noble protagonist whose downfall is caused by a flaw or error of judgement'),
         ('hamartia', 'the tragic hero\'s fatal flaw or error (Macbeth\'s ambition)'),
         ('catharsis', 'the release of pity and fear the audience feels at a tragedy\'s end'),
         ('hubris', 'excessive pride or self-confidence that leads to downfall'),
         ('anagnorisis', 'the moment of recognition when the tragic hero understands the truth of his situation')],
  facts=[('Macbeth\'s hamartia is usually identified as:', 'his ambition', ['his kindness', 'his cowardice in battle', 'his loyalty to Duncan'], 'Ambition drives his fall.'),
         ('Which Greek philosopher defined tragedy and catharsis in the "Poetics"?', 'Aristotle', ['Plato', 'Socrates', 'Sophocles'], 'Aristotle\'s Poetics.'),
         ('At the start of the play, Macbeth is:', 'a brave, respected general praised by Duncan', ['a murderer in hiding', 'the king of Scotland', 'a witch'], 'A tragic hero begins high.'),
         ('Which speech shows Macbeth\'s despairing recognition near the end?', '"Tomorrow, and tomorrow, and tomorrow"', ['"Fair is foul, and foul is fair"', '"Is this a dagger which I see before me"', '"Out, damned spot!"'], 'It shows his emptiness.')],
  why=[('Explain why a tragic hero must begin with high status.', 'The fall is greater and more shocking from a height, and it affects a whole kingdom, not only one person.'),
       ('Explain why the audience feels pity for Macbeth despite his crimes.', 'He knows what he is doing is wrong, suffers guilt and ends in despair; his potential for greatness makes his waste tragic.'),
       ('Explain why the witches do not simply make Macbeth a murderer.', 'They only predict; Macbeth\'s own ambition chooses murder, which keeps him responsible and makes the tragedy moral rather than fated.')],
  contrast=[('hamartia', 'hubris', 'Hamartia is the fatal flaw or error; hubris is a specific kind of flaw – excessive pride.'),
            ('fate', 'free will', 'Fate suggests events are predestined (the prophecies); free will means characters choose (Macbeth decides to kill). Macbeth explores both.')],
  misc=[('Macbeth is simply a villain.', 'He is a tragic hero: initially noble, tormented by conscience and destroyed by his own flaw, which evokes pity as well as horror.')],
  apply=[('Outline Macbeth\'s journey as a tragic hero in four stages, with a key moment for each.', 'E.g. noble general praised by Duncan; temptation by prophecy and Lady Macbeth; murder and descent into tyranny; despair and death ("Tomorrow, and tomorrow...").', 4),
         ('Explain how "Tomorrow, and tomorrow, and tomorrow" could produce catharsis in an audience.', 'It shows Macbeth\'s emptiness and recognition of life\'s meaninglessness; the audience feels pity at his waste and fear at the consequences of ambition, releasing those emotions.', 3)],
  evaluate=[('Lady Macbeth is more responsible than Macbeth for Duncan\'s murder.', ['she plans and pressures him', 'she questions his manhood'], ['Macbeth already thinks of murder in his aside', 'he chooses and continues killing alone'], 'Lady Macbeth drives the first murder, but Macbeth\'s own ambition and later choices make him ultimately responsible.')],
  extended=[('To what extent is Macbeth a tragic hero? Refer to the play\'s structure and key speeches.', 'Indicative content: Aristotelian features (status, hamartia, fall, recognition, catharsis); evidence from key moments; consideration of villainy vs tragedy; balanced judgement. Criteria A and B.', 8, 'long')])
pq('ch04-st1', ('C2', 'C3', 'C4'), (1, 5), None, 'tragic', ['How does this extract present Macbeth as a tragic hero?',
                                                        'Explain how this extract contributes to the tragic pattern of the play.',
                                                        'What does this extract reveal about the role of ambition, fate or guilt in the tragedy?'], ids=MAC, crit=CRIT_A)
pq('ch04-st1', ('C2', 'C3'), (1, 4), None, 'theme', THEME_Q, ids=MAC, crit=CRIT_OPEN)
para('ch04-st1', None, ids=MAC, c='C4', d=(3, 5), frames=['{gq} Link your answer to Macbeth as a tragedy.'])
K.dev_mcq('ch04-st1', ids=MAC)

H('ch04-st2',
  terms=[('soliloquy', 'a speech in which a character alone on stage speaks their thoughts aloud'),
         ('aside', 'a short remark spoken to the audience (or to oneself) that other characters on stage cannot hear'),
         ('dramatic irony', 'when the audience knows something characters do not'),
         ('stage directions', 'instructions in the script about actions, sounds and entrances, e.g. [Knocking within]'),
         ('foreshadowing', 'hints of what will happen later in the play')],
  facts=[('"Is this a dagger which I see before me" is spoken by Macbeth alone on stage. It is a:', 'soliloquy', ['aside', 'prologue', 'dialogue'], 'He is alone.'),
         ('"Stars, hide your fires" is spoken as an aside. This means:', 'other characters on stage cannot hear it', ['it is sung', 'it is cut from performances', 'all characters respond to it'], 'An aside is private.'),
         ('"A little water clears us of this deed" is ironic because:', 'Lady Macbeth later sleepwalks trying to wash away imagined blood', ['water is scarce in Scotland', 'Macbeth is a sailor', 'it is a joke'], 'Dramatic irony.'),
         ('"[Knocking within]" is an example of:', 'a stage direction creating sound', ['a soliloquy', 'an aside', 'a rhyming couplet'], 'It is an offstage sound effect.')],
  why=[('Explain why Shakespeare gives Macbeth so many soliloquies.', 'They reveal his conscience and inner conflict, so the audience understands and partly sympathises with him even as he commits crimes.'),
       ('Explain why dramatic irony creates tension.', 'The audience knows the danger or truth that characters do not, so they watch anxiously for the consequences.'),
       ('Explain why the knocking after Duncan\'s murder is dramatically effective.', 'The sound interrupts the Macbeths\' panic, raising fear of discovery and bringing the outside world into the scene.')],
  contrast=[('a soliloquy', 'an aside', 'A soliloquy is a longer speech by a character alone on stage; an aside is a brief remark to the audience while others are present but cannot hear.'),
            ('dramatic irony', 'verbal irony', 'Dramatic irony is when the audience knows more than characters; verbal irony is when a speaker says something different from what they mean.')],
  misc=[('A soliloquy is a conversation with the audience.', 'A soliloquy is a character thinking aloud; the audience overhears it rather than taking part.')],
  apply=[('Explain how a director might stage Macbeth\'s aside "Stars, hide your fires" to make the dramatic irony clear.', 'E.g. Macbeth steps downstage, lights dim on him while Duncan and the court freeze or continue celebrating in the background, so the audience alone hears his dark thoughts.', 3),
         ('Identify an example of foreshadowing in the witches\' scene and explain what it hints at.', '"The instruments of darkness tell us truths ... to betray\'s / In deepest consequence" – hints that the prophecies will lead Macbeth to destruction.', 2)],
  evaluate=[('Soliloquies make the audience sympathise with Macbeth too much.', ['we share his fear and guilt', 'we understand his motives'], ['they also reveal his dark desires', 'sympathy makes the tragedy more painful, not less'], 'Soliloquies create complex responses – sympathy and horror – which is essential to tragedy.')],
  extended=[('Analyse how Shakespeare uses dramatic devices (soliloquy, aside, dramatic irony, stage directions) to create tension in Macbeth.', 'Indicative content: examples of each device with quotation; explanation of effect on audience; staging considerations; organised analysis. Criteria A and B.', 8, 'long')])
pq('ch04-st2', ('C2', 'C3', 'C4'), (1, 5), None, 'dramatic', ['Identify the dramatic device used in this extract and explain its effect on the audience.',
                                                           'How does Shakespeare use dramatic irony or soliloquy in this extract?',
                                                           'Explain how this extract creates tension for the audience.'], ids=MAC, crit=CRIT_A)
pq('ch04-st2', ('C2', 'C3'), (1, 4), None, 'staging', ['How might this extract be staged to create tension? Refer to the text.',
                                                    'Explain how stage directions or staging choices contribute to the dramatic effect.'], ids=MAC + ['storm_drama'], crit=CRIT_OPEN)
pq('ch04-st2', 'C3', (2, 4), None, 'dev', ['Explain how "{quote}" creates dramatic effect on stage.'], ids=MAC, crit=CRIT_B)
para('ch04-st2', None, ids=MAC, c='C4', d=(3, 5), frames=['{gq} Refer to dramatic devices in your answer.'])

H('ch04-st3',
  terms=[('blank verse', 'unrhymed iambic pentameter, used by Shakespeare\'s noble characters'),
         ('motif', 'a recurring image or idea, such as blood or darkness in Macbeth'),
         ('apostrophe', 'addressing someone absent or something inanimate, e.g. "Stars, hide your fires"'),
         ('trochaic tetrameter', 'a line of four trochees (DUM-da), used for the witches\' chants'),
         ('imagery', 'language that creates pictures, often developed into patterns across a play')],
  facts=[('Most of Macbeth\'s speeches are written in:', 'blank verse', ['rhyming couplets throughout', 'prose', 'free verse'], 'Unrhymed iambic pentameter.'),
         ('The witches speak in a different rhythm from the nobles. This is:', 'trochaic tetrameter', ['iambic pentameter', 'prose', 'blank verse'], 'Their chant marks them as unnatural.'),
         ('"Will all great Neptune\'s ocean wash this blood / Clean from my hand?" develops the motif of:', 'blood as guilt', ['light as hope', 'birds as freedom', 'clothing as disguise'], 'Blood symbolises guilt.'),
         ('"Let not light see my black and deep desires" develops the motif of:', 'light and darkness', ['sleep', 'clothing', 'weather'], 'Darkness links to evil.')],
  why=[('Explain why the motif of blood develops across Macbeth.', 'Blood moves from a sign of heroism in battle to a symbol of guilt that cannot be washed away, tracing Macbeth\'s moral fall.'),
       ('Explain why Shakespeare gives the witches a different metre.', 'The chanting trochaic rhythm sets them apart from human characters, making them sound unnatural and spell-like.'),
       ('Explain why darkness is linked with evil in Macbeth.', 'Characters call on darkness to hide their crimes from heaven and conscience; the imagery shows evil needs concealment.')],
  contrast=[('blank verse', 'prose', 'Blank verse is unrhymed iambic pentameter, used for noble or serious speech; prose has no metre and is often used for lower-status characters, madness or comedy.')],
  misc=[('Shakespeare\'s characters always speak in rhyme.', 'Most of Macbeth is blank verse (unrhymed); rhyme is used for the witches, scene endings and moments of resolve.')],
  apply=[('Trace the motif of blood through two extracts and explain how its meaning develops.', 'E.g. "this blood / Clean from my hand" – overwhelming guilt; Lady Macbeth\'s "A little water clears us" – dismissive, later reversed in her sleepwalking. Credit development of meaning.', 3),
         ('Explain why "Stars, hide your fires; / Let not light see my black and deep desires" ends with a rhyming couplet.', 'The rhyme seals his dark resolve, giving the moment emphasis and finality within a scene otherwise in blank verse.', 2)],
  evaluate=[('Shakespeare\'s imagery is the most powerful element of Macbeth.', ['motifs of blood and darkness shape the whole play', 'images stay in the audience\'s minds'], ['character and plot drive the tragedy', 'staging and performance matter'], 'Imagery is central, giving the play its atmosphere and moral meaning, but it works through character, plot and performance.')],
  extended=[('Analyse how Shakespeare uses language and imagery of blood and darkness in Macbeth.', 'Indicative content: tracks the motifs across scenes; close analysis of quotations; metre (blank verse, trochaic chant); links to themes of guilt and evil. Criteria A and B.', 8, 'long')])
pq('ch04-st3', ('C2', 'C3', 'C4'), (1, 5), None, 'motif', ['Explain how this extract develops the motifs of blood or darkness.',
                                                       'How does Shakespeare\'s imagery in this extract connect to the play\'s wider themes?'], ids=MAC, crit=CRIT_A)
pq('ch04-st3', ('C2', 'C3', 'C4'), (1, 5), None, 'dev', DEV_Q, ids=MAC, crit=CRIT_B)
K.vocab('ch04-st3', ids=MAC)
K.tone_mcq('ch04-st3', ids=MAC)

H('ch04-st4',
  terms=[('interpretation', 'a director\'s or actor\'s particular reading of a scene, expressed through performance choices'),
         ('blocking', 'the planned movement and positioning of actors on stage'),
         ('proxemics', 'the use of space and distance between characters to show relationships'),
         ('subtext', 'meaning beneath the words, which actors can reveal through tone and gesture')],
  facts=[('In staging the dagger soliloquy, showing a real projected dagger suggests:', 'a supernatural vision', ['a comic interpretation', 'a cut scene', 'that Macbeth is not present'], 'Showing it implies it is real.'),
         ('Placing Macbeth far from Lady Macbeth in the final act would use:', 'proxemics to show their separation', ['a soliloquy', 'iambic pentameter', 'an aside'], 'Distance shows relationship.'),
         ('Which choice would best create tension during "[Knocking within]"?', 'Freezing the actors, then a sudden rush to hide their hands', ['Adding a cheerful song', 'Turning on all the lights', 'Having the actors laugh'], 'It heightens fear.')],
  why=[('Explain why the same scene can be performed in very different ways.', 'Scripts leave gaps – tone, movement, pauses – so directors and actors interpret meaning differently, emphasising different aspects.'),
       ('Explain why the delivery of "Tomorrow, and tomorrow, and tomorrow" matters.', 'A slow, flat delivery suggests numb despair; a bitter or broken one suggests anguish – each shapes the audience\'s sympathy.')],
  contrast=[('a supernatural interpretation', 'a psychological interpretation', 'A supernatural interpretation presents visions and witches as real; a psychological interpretation presents them as products of Macbeth\'s guilty mind.')],
  misc=[('There is one correct way to perform a Shakespeare scene.', 'Many interpretations are valid if they are supported by the text.')],
  apply=[('Write three staging notes for the witches\' opening scene (lighting, sound, movement) and explain the effect of each.', 'E.g. flickering green light (unnatural); low thunder and whispered chanting (menace); witches moving in circles through fog (disorientation). Credit three choices with effects.', 3),
         ('Write director\'s notes for an actor delivering "Is this a dagger which I see before me" (voice, gesture, movement).', 'E.g. hushed, uncertain voice; reaching out then recoiling; eyes fixed on an empty point; pauses at "I have thee not". Credit choices justified by the text.', 3)],
  evaluate=[('Macbeth is better experienced in performance than read on the page.', ['staging, sound and acting bring it alive', 'it was written to be performed'], ['reading allows close analysis of language', 'readers imagine their own interpretation'], 'Performance reveals the play\'s power, but reading uncovers detail; both deepen understanding.')],
  extended=[('Choose a key scene from Macbeth. Explain how you would direct it to bring out its meaning, justifying each choice with reference to the text.', 'Indicative content: clear interpretation; choices on voice, movement, proxemics, lighting and sound; justification with quotation; awareness of alternative interpretations. Criteria A, B and C.', 8, 'long')])
pq('ch04-st4', ('C2', 'C3', 'C4'), (1, 5), None, 'staging', ['You are directing this extract. Describe two staging choices and explain how they bring out its meaning.',
                                                         'How might an actor perform this extract to convey the character\'s state of mind?'], ids=MAC, crit=CRIT_OPEN)
pq('ch04-st4', ('C3', 'C4'), (2, 5), None, 'dev', ['Explain how an actor could deliver "{quote}" and why that choice suits the meaning of the line.'], ids=MAC, crit=CRIT_OPEN)
pq('ch04-st4', 'C4', (3, 5), None, 'staging', ['Write director\'s notes (about 250 words) for a performance of this extract, covering voice, movement, lighting and sound. Justify each choice from the text.',
                                              'Explain how you would stage this extract for a modern audience, and how your choices would shape its meaning.'], typ='long', ids=MAC, crit=CRIT_OPEN)


# =============================================================================================
# ch05 News Media, Bias and Misinformation
# =============================================================================================
NEWS = ['stadium_a', 'stadium_b', 'editorial_curfew', 'viral_post', 'factcheck', 'turtles', 'floodnews']
H('ch05-st1',
  terms=[('news values', 'the criteria journalists use to decide what is newsworthy: impact, proximity, prominence, conflict, human interest, novelty and timeliness'),
         ('inverted pyramid', 'a news structure that puts the most important information first and less important details later'),
         ('lead (lede)', 'the opening paragraph of a news report, answering who, what, where, when (and often why)'),
         ('headline', 'the title of a news story, designed to summarise and attract attention'),
         ('attribution', 'stating the source of information or quotations ("said the council leader")')],
  facts=[('Which structure places the most important information first?', 'The inverted pyramid', ['Chronological order', 'Circular structure', 'Flashback structure'], 'Key facts come first.'),
         ('A story about a local estate is newsworthy partly because of:', 'proximity', ['novelty only', 'celebrity', 'none – local stories are never news'], 'Proximity – it affects local readers.'),
         ('The lead paragraph of a news report should answer:', 'who, what, where and when', ['only why', 'what the journalist thinks', 'the reader\'s opinion'], 'The 5 Ws.'),
         ('Quoting the council leader brings which news value?', 'Prominence', ['Novelty', 'Weather', 'Humour'], 'Important people are newsworthy.')],
  why=[('Explain why news reports use the inverted pyramid.', 'Readers often skim; putting the most important facts first means they get the essentials even if they stop early, and editors can cut from the bottom.'),
       ('Explain why conflict is a strong news value.', 'Disagreement creates drama and stakes, which attracts readers\' attention.'),
       ('Explain why attribution is important in news reports.', 'It shows where information comes from, allowing readers to judge reliability and separating facts from the reporter\'s opinion.')],
  contrast=[('hard news', 'soft news', 'Hard news covers urgent, important events (politics, disasters); soft news covers lighter human-interest stories (lifestyle, entertainment).')],
  misc=[('News values guarantee that the most important stories are reported.', 'News values also favour drama, celebrity and conflict, so some important but undramatic issues are under-reported.')],
  apply=[('Write the headline and lead paragraph of a news report about your school opening a new library.', 'Credit a concise headline and a lead answering who, what, where, when (and why) in a neutral, factual register.', 3),
         ('Identify three news values in the stadium story.', 'Impact (2,000 jobs, 140 homes); proximity (local estate); conflict (residents vs council); prominence (council leader).', 3)],
  evaluate=[('News values make journalism less objective.', ['they favour drama and conflict', 'they shape which stories are told'], ['they help readers find relevant stories', 'they are necessary choices, not lies'], 'News values inevitably shape coverage; readers should be aware of them rather than expect total objectivity.')],
  extended=[('Write a news report (about 300 words) on a recent event at your school, using the inverted pyramid and at least two attributed quotations.', 'Indicative content: headline; lead with 5 Ws; inverted-pyramid order; attributed quotations from at least two sources; neutral register; accurate punctuation of quotations. Criteria B, C, D.', 8, 'long')])
pq('ch05-st1', ('C2', 'C3', 'C4'), (1, 5), None, 'newsval', ['Identify the news values that make this story newsworthy and explain each.',
                                                         'Why might an editor choose to publish this story? Refer to news values.'], ids=['stadium_a', 'stadium_b'], crit=CRIT_A)
pq('ch05-st1', ('C2', 'C3'), (1, 4), None, 'struct', STRUCT_Q, ids=NEWS, crit=CRIT_B)
pq('ch05-st1', ('C2', 'C3'), (1, 4), None, 'kconv', KCONV_Q, ids=NEWS, crit=CRIT_A)
K.kind_mcq('ch05-st1', ids=NEWS)

H('ch05-st2',
  terms=[('bias', 'an unfair preference for one side or view, shown through selection, language or emphasis'),
         ('framing', 'the way a story is presented – what is emphasised, included or left out – which shapes how readers understand it'),
         ('representation', 'how people, places or events are portrayed in the media'),
         ('selection and omission', 'choosing which facts, voices and images to include or leave out'),
         ('loaded language', 'words with strong positive or negative connotations')],
  facts=[('"FAMILIES FACE EVICTION" and "A NEW HEART" frame the same story:', 'negatively and positively', ['in exactly the same way', 'neutrally', 'humorously'], 'Framing shapes meaning.'),
         ('Describing residents as "relocated" rather than "evicted" is an example of:', 'euphemism softening the impact', ['hyperbole', 'onomatopoeia', 'a pun'], 'A gentler word hides the reality.'),
         ('Which is a sign of bias in a report?', 'Only one side is quoted', ['Both sides are quoted', 'Sources are named', 'Facts are dated'], 'Omission of a side reveals bias.'),
         ('Using "claims" rather than "says" before a statement suggests:', 'doubt about the statement', ['strong agreement', 'neutrality', 'that it is a joke'], '"Claims" distances the writer.')],
  why=[('Explain why two reports can use the same facts but give different impressions.', 'Selection, order, headline, word choice and whose voices are quoted frame the facts differently.'),
       ('Explain why the order of information matters in a biased report.', 'Readers remember the headline and opening most; placing inconvenient facts late reduces their impact.'),
       ('Explain why readers should compare several sources on the same event.', 'Each source frames events differently; comparison reveals omissions and bias and gives a fuller picture.')],
  contrast=[('bias', 'framing', 'Bias is an unfair preference for one side; framing is the way any story is presented. All stories are framed, but not all framing is biased.'),
            ('representation', 'reality', 'Representation is a constructed version of people or events; reality is more complex than any single representation.')],
  misc=[('A report that contains only facts cannot be biased.', 'Bias can come from which facts are selected, the order they appear in and which voices are quoted.')],
  apply=[('Rewrite the stadium headline "FAMILIES FACE EVICTION AS COUNCIL BACKS £300M STADIUM" so that it is as neutral as possible.', 'E.g. "Council approves £300m stadium; 140 households to move." Credit removal of loaded language and balance.', 2),
         ('Identify two techniques of framing in one stadium report and explain their effect.', 'E.g. Text B: headline foregrounds "EVICTION"; emotive quotation from Joan Mensah; "claims" casts doubt; critics given last word. Credit two techniques with effects.', 3)],
  evaluate=[('Completely unbiased journalism is impossible.', ['every report involves selection', 'journalists have perspectives'], ['professional standards reduce bias', 'balance and attribution are achievable'], 'Total neutrality is impossible because selection is unavoidable, but fairness and balance are realistic goals.')],
  extended=[('Compare how two news reports represent the same event, analysing framing, language and selection.', 'Indicative content: headlines; leads; quotations chosen; loaded language; order; omissions; effect on readers; comparative structure. Criteria A and B.', 8, 'long')])
pq('ch05-st2', ('C2', 'C3', 'C4'), (1, 5), None, 'framing', ['How does this report frame the event? Refer to headline, quotations and word choice.',
                                                         'Identify evidence of bias or framing in this text and explain its effect on readers.',
                                                         'Whose perspective does this text favour? Support your answer with evidence.'], ids=['stadium_a', 'stadium_b', 'editorial_curfew'], crit=CRIT_A)
K.compare_short('ch05-st2', c=('C2', 'C3'), d=(1, 4), only=NEWS)
pq('ch05-st2', ('C2', 'C3'), (1, 4), None, 'dev', ['Explain how the word choice in "{quote}" shapes the reader\'s view of the event.'], ids=['stadium_a', 'stadium_b', 'floodnews', 'turtles'], crit=CRIT_B)
para('ch05-st2', None, ids=['stadium_a', 'stadium_b'], c='C4', d=(3, 5), frames=['{gq} Analyse framing, selection and word choice.'])

H('ch05-st3',
  terms=[('fact', 'a statement that can be checked and proved true or false'),
         ('opinion', 'a statement of belief, feeling or judgement that cannot be proved'),
         ('editorial', 'an article expressing the official opinion of a newspaper ("Our view")'),
         ('concession', 'admitting a point on the other side before rebutting it'),
         ('rebuttal', 'arguing against an opposing point')],
  facts=[('"Youth crime in the town fell by 12 per cent last year" is:', 'a fact (checkable)', ['an opinion', 'a rhetorical question', 'a metaphor'], 'It can be checked against police figures.'),
         ('"It is also lazy" in the curfew editorial is:', 'an opinion', ['a fact', 'a statistic', 'a quotation'], 'It is a judgement.'),
         ('An editorial differs from a news report because it:', 'expresses the newspaper\'s opinion', ['must be neutral', 'never uses evidence', 'is always about sport'], 'It argues a position.'),
         ('"The plan may sound tough. It is also lazy." This shows:', 'concession followed by rebuttal', ['a flashback', 'a neutral summary', 'a statistic'], 'It admits then rejects.')],
  why=[('Explain why editorials use facts as well as opinions.', 'Facts make opinions convincing and harder to dismiss, giving the argument logos.'),
       ('Explain why a concession can strengthen an argument.', 'Acknowledging the other side shows fairness and confidence, making the rebuttal more persuasive.'),
       ('Explain why readers should separate fact from opinion.', 'Opinions can be presented as if they were facts; separating them helps readers judge an argument fairly.')],
  contrast=[('a news report', 'an editorial', 'A news report aims to inform with facts and attributed quotations; an editorial argues the newspaper\'s opinion using evidence and persuasive techniques.'),
            ('a fact', 'an opinion', 'A fact can be verified; an opinion is a judgement that can be argued but not proved.')],
  misc=[('Opinions are worthless in journalism.', 'Opinion pieces are valuable when clearly labelled, well-argued and based on evidence.')],
  apply=[('Identify two facts and two opinions in the curfew editorial.', 'Facts: youth crime fell 12 per cent; two clubs closed since 2022. Opinions: "It is also lazy"; "Treat young people as suspects and they will behave like them."', 4),
         ('Write a two-sentence concession and rebuttal for an editorial supporting longer school holidays.', 'E.g. "Critics argue that longer holidays harm learning. Yet research shows rested students return more focused, and holidays offer time for family, work and rest." Credit concession and rebuttal.', 2)],
  evaluate=[('Newspapers should not publish editorials because they influence readers.', ['opinion can mislead', 'readers may confuse it with news'], ['clear labelling allows informed debate', 'editorials hold power to account'], 'Editorials are legitimate if clearly labelled and well-evidenced; readers need media literacy to evaluate them.')],
  extended=[('Write an editorial (about 350 words) for your school newspaper on a current issue. Combine facts and opinions, include a concession and rebuttal, and end with a clear call to action.', 'Indicative content: headline ("Our view"); clear stance; facts and evidence; opinions; concession and rebuttal; persuasive devices; call to action; formal register. Criteria B, C, D.', 12, 'long')])
pq('ch05-st3', ('C2', 'C3', 'C4'), (1, 5), None, 'facts_op', ['Identify one fact and one opinion in the text, and explain how the writer uses each.',
                                                          'How does the writer combine fact and opinion to persuade?'], ids=['editorial_curfew', 'stadium_a', 'stadium_b', 'turtles', 'floodnews'], crit=CRIT_A)
pq('ch05-st3', ('C2', 'C3'), (1, 4), None, 'purp', PURP_Q, ids=['editorial_curfew', 'uniform'], crit=CRIT_A)
pq('ch05-st3', 'C3', (2, 4), None, 'dev', DEV_Q, ids=['editorial_curfew', 'uniform'], crit=CRIT_B)
para('ch05-st3', None, ids=['editorial_curfew', 'uniform'], c='C4', d=(3, 5))
write('ch05-st3', ids=['editorial_curfew', 'uniform'])

H('ch05-st4',
  terms=[('misinformation', 'false or misleading information shared without intent to deceive'),
         ('disinformation', 'false information deliberately created and spread to deceive'),
         ('source evaluation', 'judging a source\'s reliability by its author, evidence, purpose, date and corroboration'),
         ('lateral reading', 'checking a claim by opening other tabs to see what independent sources say about it'),
         ('corroboration', 'confirmation of a claim by other independent, reliable sources')],
  facts=[('Which is a red flag for misinformation?', 'An anonymous second-hand source ("My cousin says...")', ['A named official statement', 'A link to a reputable news site', 'A date and author'], 'Unverifiable sources are a warning sign.'),
         ('"SHARE BEFORE THEY DELETE THIS" is designed to:', 'make readers share before checking', ['encourage careful research', 'cite a source', 'calm readers'], 'Urgency bypasses thinking.'),
         ('Checking what other independent sites say about a source is called:', 'lateral reading', ['vertical reading', 'skimming', 'proofreading'], 'Read across, not down.'),
         ('False information deliberately spread to deceive is:', 'disinformation', ['misinformation', 'satire', 'an editorial'], 'Intent distinguishes them.')],
  why=[('Explain why misinformation spreads faster than corrections.', 'It is usually emotional, surprising and urgent, so people share it quickly; corrections are calmer and less exciting.'),
       ('Explain why conspiracy framing makes misinformation hard to correct.', 'If a post claims "they don\'t want you to know", official denials can seem like proof of a cover-up.'),
       ('Explain why fact-checkers name and quote their sources.', 'Transparency allows readers to verify claims themselves and builds trust.')],
  contrast=[('misinformation', 'disinformation', 'Misinformation is false information shared without intent to deceive; disinformation is deliberately created to deceive.'),
            ('a reliable source', 'an unreliable source', 'A reliable source is transparent about authorship and evidence, accurate and corroborated; an unreliable source is anonymous, emotional and unverifiable.')],
  misc=[('If many people share something, it must be true.', 'Popularity is not evidence; false claims often spread faster than true ones.'),
        ('Fact-checking is only for journalists.', 'Everyone can check claims using lateral reading, official sources and reverse image searches before sharing.')],
  apply=[('List four red flags in the viral water post.', 'Any four: anonymous cousin; unnamed "doctors"; urgency ("SHARE BEFORE THEY DELETE THIS"); conspiracy claim; capitals and exclamation marks; no date, link or official source.', 4),
         ('Describe three steps you would take to check the viral post before sharing it.', 'E.g. check the water company\'s website; search reputable news sites; look for a fact-check; check the date and origin of the post.', 3)],
  evaluate=[('Social media companies, not users, should be responsible for stopping misinformation.', ['platforms profit from engagement', 'they can remove false content at scale'], ['users choose what to share', 'over-removal threatens free speech'], 'Responsibility is shared: platforms should limit harmful misinformation, but users need media literacy to judge what they share.')],
  extended=[('Write a guide (about 350 words) for Year 7 students on how to spot misinformation online, using examples.', 'Indicative content: clear title and subheadings; explanation of red flags; practical steps (lateral reading, checking sources); examples; accessible register for younger readers; call to action. Criteria B, C, D.', 8, 'long')])
pq('ch05-st4', ('C2', 'C3', 'C4'), (1, 5), None, 'misinfo', ['Identify the features that suggest this text may be misinformation, or explain how it corrects misinformation.',
                                                         'How does this text try to make readers believe it? Evaluate how reliable it is.'], ids=['viral_post', 'factcheck'], crit=CRIT_A)
pq('ch05-st4', ('C2', 'C3'), (1, 4), None, 'source', ['How reliable is this text as a source? Explain with reference to its evidence.',
                                                   'Explain how a reader could check whether this text is reliable.'], ids=['viral_post', 'factcheck'], crit=CRIT_A)
pq('ch05-st4', ('C2', 'C3'), (1, 4), None, 'dev', DEV_Q, ids=['viral_post', 'factcheck'], crit=CRIT_B)
K.compare('ch05-st4', c='C4', d=(4, 5), frames=['{q} Evaluate which text is more reliable and why.'], only=['viral_post'])
K.tone_mcq('ch05-st4', ids=['viral_post', 'factcheck', 'stadium_a', 'stadium_b'])


# =============================================================================================
# ch06 Comparative Analysis of Literary and Non-Literary Texts (eAssessment Task 1)
# =============================================================================================
H('ch06-st1',
  terms=[('unseen extract', 'a text you have not studied before, as in the eAssessment'),
         ('annotation', 'notes on a text that identify features, their effects and links to purpose'),
         ('GAP (genre, audience, purpose)', 'a checklist for a first reading of any text'),
         ('first reading / close reading', 'a first reading for overall meaning, then a close reading for language, structure and technique'),
         ('literary text', 'an imaginative text such as a poem, story or play'),
         ('non-literary text', 'a functional or persuasive text such as a speech, article, advertisement or letter')],
  facts=[('On first reading an unseen extract, what should you identify first?', 'Its genre, audience and purpose (GAP)', ['Every comma', 'The word count', 'The font'], 'GAP orients analysis.'),
         ('Which annotation is most useful?', '"Simile \'like a sleeping child\' – shows spices as precious, links home to family"', ['"Simile"', '"Nice"', '"Line 3"'], 'It names, quotes and explains.'),
         ('In the eAssessment, which kind of text pairing is common in Task 1?', 'A literary and a non-literary text on a shared theme', ['Two identical texts', 'Only poems', 'Only advertisements'], 'Task 1 compares different text types.'),
         ('Which of these is a non-literary text?', 'A fact-checking article', ['A sonnet', 'A short story', 'A playscript'], 'It is functional.')],
  why=[('Explain why you should annotate for purpose and effect, not just features.', 'Criterion A rewards explaining how choices create meaning; annotations that record effects save time when writing.'),
       ('Explain why a first reading for overall meaning comes before close analysis.', 'Understanding the whole text\'s purpose and argument guides which details are significant.'),
       ('Explain why annotating structure as well as language is important.', 'Structure (openings, shifts, endings) shapes meaning and is often overlooked, so it can add depth to analysis.')],
  contrast=[('annotation', 'summary', 'Annotation identifies features and their effects; summary restates content in your own words.'),
            ('a literary text', 'a non-literary text', 'A literary text is imaginative and aesthetic (poem, story); a non-literary text has a practical or persuasive purpose (article, speech, advert).')],
  misc=[('You should annotate every line of an unseen extract.', 'Select significant features linked to the question; over-annotating wastes time.')],
  apply=[('Annotate the letter from 1962 with three features, each with an effect.', 'E.g. simile "radiator knocks ... like a neighbour" – loneliness; "I let them." – quiet acceptance of lost identity; irony "Both are true." – protects mother, reveals sadness.', 3),
         ('Apply GAP to the fact-check article.', 'Genre: online fact-check article; audience: members of the public who saw the viral post; purpose: to check the claim and correct misinformation.', 3)],
  evaluate=[('Annotation is less important than writing time in the exam.', ['writing earns the marks', 'time is short'], ['annotation organises ideas and finds evidence', 'it prevents weak, unplanned answers'], 'Brief, focused annotation is a wise investment; it improves both analysis and organisation.')],
  extended=[('Annotate an unseen literary extract and write an analytical response (about 300 words) on how the writer creates meaning.', 'Indicative content: GAP identified; annotated features with effects; analytical paragraphs with embedded quotations; structure and language analysed; clear organisation. Criteria A, B, D.', 8, 'long')])
pq('ch06-st1', ('C2', 'C3', 'C4'), (1, 5), LIT | NONLIT | LIFE, 'dev', ['Annotate "{quote}": name the technique, then explain its effect and how it links to the purpose of the text.',
                                                                  'Write an annotation for "{quote}" that you could use in a Task 1 response.'], crit=CRIT_B)
pq('ch06-st1', ('C2', 'C3'), (1, 4), None, 'purp', PURP_Q + ['Apply GAP (genre, audience, purpose) to this text, giving evidence for each.'], ids=['leaving_letter', 'factcheck', 'campaign_water', 'travel_hanoi', 'speech_mayor', 'editorial_curfew'], crit=CRIT_A)
pq('ch06-st1', ('C2', 'C3'), (1, 4), LIT | LIFE, 'struct', STRUCT_Q, crit=CRIT_B)
pq('ch06-st1', 'C3', (2, 4), NONLIT, 'kconv', KCONV_Q, crit=CRIT_A)
para('ch06-st1', LIT | LIFE, c='C4', d=(3, 5), frames=['{gq} Write an analytical response of about 250 words, as in Task 1.'])
K.vocab('ch06-st1', kinds=LIT | NONLIT | LIFE)
K.dev_mcq('ch06-st1', kinds=LIT | NONLIT | LIFE)

H('ch06-st2',
  terms=[('comparative thesis', 'a central claim that states how two texts are similar and different in relation to the question'),
         ('controlling idea', 'the main argument that every paragraph supports'),
         ('nuance', 'a subtle distinction that makes an argument more precise ("both ... but in different ways")'),
         ('shared focus', 'the common theme or purpose that justifies comparing the texts')],
  facts=[('Which is the strongest comparative thesis?', '"Both texts use spices to represent home, but whereas the poem looks back with lasting grief, the letter hides fresh loneliness from family."', ['"Both texts are about leaving home."', '"Text A is a poem and Text B is a letter."', '"I think Text A is better."'], 'It states similarity, difference and significance.'),
         ('A comparative thesis should appear:', 'in the introduction, guiding the whole response', ['only in the conclusion', 'nowhere', 'in a footnote'], 'It sets the direction.'),
         ('Which word signals nuance in a thesis?', '"Whereas"', ['"Also"', '"And"', '"Then"'], 'It introduces a qualified contrast.')],
  why=[('Explain why a comparative thesis should include both a similarity and a difference.', 'It shows a balanced understanding of the texts\' relationship and gives a clear structure for the essay.'),
       ('Explain why a thesis should go beyond "both texts are about X".', 'A strong thesis explains how and why the texts differ in method or perspective, which is what criterion A rewards.'),
       ('Explain why the thesis should answer the question directly.', 'Relevance to the question keeps the analysis focused and helps the examiner follow the argument (criterion B).')],
  contrast=[('a topic statement', 'a thesis', 'A topic statement says what the texts are about; a thesis makes an arguable claim about how and why they present it.')],
  misc=[('A thesis must claim the texts are completely different.', 'The best theses identify meaningful similarities and differences and the reasons for them.')],
  apply=[('Write a comparative thesis for the two stadium reports.', 'E.g. "Both reports convey the same facts, but whereas Text A frames the stadium as regeneration through the council\'s voice, Text B frames it as eviction through a resident\'s." Credit similarity, difference and method.', 2),
         ('Improve this thesis: "Both poems are about protest."', 'E.g. "Both poems use a collective voice to protest, but Shelley rallies the oppressed with rhyme and simile, whereas the modern poem confronts adults with free verse and turned-back accusations." Credit precision and method.', 2)],
  evaluate=[('A thesis should be decided before reading the texts closely.', ['it saves time', 'it gives focus'], ['it may ignore key evidence', 'it should emerge from annotation'], 'A provisional thesis can guide reading, but it should be refined after close annotation so it reflects the evidence.')],
  extended=[('Read two texts on a shared theme. Write a comparative introduction with a clear thesis and an outline of your three main points.', 'Indicative content: introduces both texts (type, purpose); precise thesis with similarity and difference; three points of comparison previewed. Criteria A and B.', 6, 'long')])
K.compare_short('ch06-st2', c=('C2', 'C3'), d=(1, 4))
K.compare('ch06-st2', c=('C3', 'C4'), d=(3, 5), frames=['{q} Begin with a comparative thesis that states one key similarity and one key difference.',
                                                         'Write a comparative introduction (about 120 words) for this question, ending with a thesis. {q}'])
para('ch06-st2', LIT | NONLIT | LIFE, c='C3', d=(2, 4), frames=['{gq} Write a one-sentence thesis that answers this question, then explain which two pieces of evidence you would use to support it.'])

H('ch06-st3',
  terms=[('point-by-point (integrated) structure', 'each paragraph compares both texts on one point'),
         ('block structure', 'discussing one text fully, then the other'),
         ('comparative connectives', 'similarly, likewise, both, whereas, while, in contrast, conversely, however'),
         ('topic sentence', 'the opening sentence of a paragraph, stating its comparative point'),
         ('conclusion', 'a final paragraph that returns to the thesis and evaluates the significance of the comparison')],
  facts=[('Which structure usually produces the most sustained comparison?', 'Point-by-point', ['Block', 'Random', 'Chronological summary'], 'It keeps both texts in view.'),
         ('Which connective introduces a similarity?', 'Similarly', ['Conversely', 'Whereas', 'In contrast'], '"Similarly" shows likeness.'),
         ('A good comparative topic sentence:', 'states a point about both texts', ['quotes Text A only', 'summarises the plot', 'introduces a new text'], 'It frames the paragraph.'),
         ('Which connective introduces a contrast?', 'Conversely', ['Likewise', 'Equally', 'Also'], '"Conversely" signals opposition.')],
  why=[('Explain why a point-by-point structure is often more effective than block structure.', 'It compares directly within paragraphs, so similarities and differences are analysed rather than left for the reader to infer.'),
       ('Explain why paragraph topic sentences should be comparative.', 'They signal the comparison immediately, keep the argument focused and help criterion B (organisation).'),
       ('Explain why the conclusion should do more than repeat the introduction.', 'It should evaluate the significance of the comparison – what it reveals about the texts\' purposes or contexts.')],
  contrast=[('point-by-point structure', 'block structure', 'Point-by-point compares both texts on each point within paragraphs; block structure discusses each text separately, with comparison mostly at the end.')],
  misc=[('Block structure always fails.', 'Block structure can work if the second block constantly links back to the first, but it risks becoming two separate essays.')],
  apply=[('Plan a point-by-point comparison of the two dystopian extracts with three paragraphs.', 'E.g. P1: control through language (slogan vs renamed words); P2: loss of individuality (Citizen 4471 vs lost concepts); P3: endings (Lena\'s smile vs Jonah\'s silence). Credit three comparative points.', 3),
         ('Use three different comparative connectives to link points about the two travel extracts.', 'E.g. "Both writers give local people a voice; however, the Hanoi writer mocks his own expectations, whereas the Atacama writer is awed. Similarly, both end in reflection." Credit three accurate connectives.', 3)],
  evaluate=[('Using many comparative connectives guarantees a high mark for organisation.', ['connectives signal comparison', 'they help the reader follow'], ['connectives without real analysis are superficial', 'logical structure matters more'], 'Connectives help, but criterion B rewards a logical, purposeful structure; connectives must link genuine comparative ideas.')],
  extended=[('Write a full comparative essay (about 500 words) on two texts, using a point-by-point structure, comparative topic sentences and a conclusion.', 'Indicative content: introduction with thesis; three point-by-point paragraphs with comparative topic sentences, evidence from both texts and analysis; varied connectives; evaluative conclusion. Criteria A, B, D.', 12, 'long')])
K.compare('ch06-st3', c='C4', d=(3, 5), frames=['{q} Use a point-by-point structure with comparative topic sentences.',
                                                '{q} Write two comparative paragraphs, each with a comparative topic sentence and evidence from both texts.'])
K.compare_short('ch06-st3', c=('C2', 'C3'), d=(1, 4))

H('ch06-st4',
  terms=[('embedded quotation', 'a short quotation woven into the grammar of your own sentence'),
         ('effect on the reader', 'the thoughts, feelings or responses a choice creates'),
         ('zooming in', 'analysing a single word or phrase within a quotation for its connotations'),
         ('connotation', 'the associations a word carries beyond its literal meaning'),
         ('tentative language', 'phrases such as "perhaps", "this may suggest" that show awareness of more than one reading')],
  facts=[('Which sentence embeds a quotation correctly?', 'The poet describes the wall as "a seam of grey", suggesting a city sewn apart.', ['"A seam of grey." This is a metaphor.', 'The poet says a quote "a seam of grey".', 'Quote: a seam of grey'], 'It flows within the sentence.'),
         ('Which is the best comment on effect?', '"The euphemism \'relocated\' softens the reality, so readers may overlook the families\' loss."', ['"It is a good word."', '"It makes you want to read on."', '"There is a word."'], 'It explains the reader\'s response.'),
         ('Zooming in on the verb "nodded" in "You have nodded at the statistics" reveals:', 'that delegates acknowledged evidence without acting', ['that they were asleep', 'that they disagreed', 'that statistics are wrong'], '"Nodded" suggests passive agreement.')],
  why=[('Explain why short, embedded quotations are better than long ones.', 'They focus on the key words to be analysed and keep the argument flowing.'),
       ('Explain why zooming in on single words strengthens analysis.', 'Single words carry connotations; analysing them shows close reading and precise understanding of effect.'),
       ('Explain why tentative language can strengthen analysis.', 'It shows awareness that texts are open to interpretation, which is a sign of perceptive, mature analysis.')],
  contrast=[('identifying a technique', 'analysing its effect', 'Identifying names the device; analysing explains how it shapes meaning and the reader\'s response in context.')],
  misc=[('"It makes the reader want to read on" is a precise comment on effect.', 'It is too general; strong comments name the specific thought or feeling created and explain why.')],
  apply=[('Improve this analysis: "Lincoln uses a tricolon \'dedicate, consecrate, hallow\'. This is effective."', 'E.g. "Lincoln\'s rising tricolon \'dedicate ... consecrate ... hallow\' moves towards ever holier verbs, suggesting the soldiers\' sacrifice has made the ground sacred beyond any speech." Credit embedding and explanation.', 3),
         ('Zoom in on one word in "her anger folded / small enough to fit / between the pages" and explain its connotations.', 'E.g. "folded" connotes neatness, concealment and control – anger made small and hidden, like a note in a book.', 2)],
  evaluate=[('Commenting on effect is more important than identifying techniques.', ['marks reward understanding of meaning', 'technique-spotting without effect earns little'], ['accurate terminology shows knowledge', 'effects need precise identification'], 'Both matter, but effect is the goal; terminology is a tool for explaining it precisely.')],
  extended=[('Write two analytical paragraphs on a text, each with at least two embedded quotations, zooming in on key words and commenting on their effects.', 'Indicative content: clear points; embedded, short quotations; zooming in on connotations; precise effects; tentative alternative readings. Criteria A and D.', 8, 'long')])
pq('ch06-st4', ('C2', 'C3', 'C4'), (1, 5), LIT | NONLIT | LIFE, 'dev', ['Write an analytical sentence that embeds part of "{quote}" and explains its effect on the reader.',
                                                                  'Zoom in on one word in "{quote}" and explain its connotations and effect.',
                                                                  'How does "{quote}" affect the reader? Offer two possible interpretations.'], crit=CRIT_B)
para('ch06-st4', LIT | NONLIT | LIFE, c='C4', d=(3, 5), frames=['{gq} Embed at least three short quotations and zoom in on key words.'])
K.compare('ch06-st4', c='C4', d=(4, 5), frames=['{q} Embed short quotations from both texts and explain their effects on the reader.'])


# =============================================================================================
# ch07 World Literature: Short Stories in Translation
# =============================================================================================
TR = ['tr_kyoto', 'tr_cairo', 'tr_valparaiso']
STORY = TR + ['lostdog', 'coa_court', 'model_car']
H('ch07-st1',
  terms=[('setting', 'the time, place and social environment of a story'),
         ('conflict', 'the central struggle: internal (within a character) or external (with another person, society or nature)'),
         ('epiphany', 'a sudden moment of insight or realisation for a character'),
         ('climax', 'the turning point of highest tension'),
         ('open ending', 'an ending that leaves questions unresolved for the reader')],
  facts=[('Which term was popularised by James Joyce for a character\'s sudden moment of insight?', 'Epiphany', ['Catharsis', 'Hubris', 'Denouement'], 'Joyce used "epiphany" for such moments.'),
         ('Karim being torn between leaving and staying is an example of:', 'internal conflict', ['external conflict with nature', 'comic relief', 'a flashback'], 'The struggle is within him.'),
         ('Grandmother\'s line "And we know the way to let go" provides:', 'an epiphany', ['a cliffhanger', 'an inciting incident only', 'a red herring'], 'It reveals the story\'s meaning.'),
         ('A short story usually focuses on:', 'a single situation or turning point', ['a whole lifetime in detail', 'dozens of characters', 'many unrelated plots'], 'Short stories are compressed.')],
  why=[('Explain why short stories often end with an epiphany.', 'An epiphany gives a brief story depth and meaning, turning a small moment into an insight the reader shares.'),
       ('Explain why setting is especially important in stories from other cultures.', 'Setting carries cultural practices and values that shape characters\' choices, helping readers understand their world.'),
       ('Explain why short stories often use open endings.', 'Open endings invite readers to reflect and continue the story in their minds, which suits the compressed form.')],
  contrast=[('internal conflict', 'external conflict', 'Internal conflict is a struggle within a character\'s mind; external conflict is with another person, society or nature.'),
            ('a climax', 'an epiphany', 'A climax is the point of highest tension in the plot; an epiphany is a moment of realisation, which may or may not coincide with the climax.')],
  misc=[('Every short story needs a dramatic climax.', 'Many short stories build to a quiet epiphany or small gesture rather than a dramatic event.')],
  apply=[('Identify the setting, conflict and epiphany in the Valparaíso story.', 'Setting: Valparaíso hills, after twenty years of exile; conflict: father\'s loyalty to the past vs the changed house; epiphany: giving away the key – "Now it is home again."', 3),
         ('Write an epiphany sentence for a story about a teenager who has spent a year angry at a parent for moving the family to a new country.', 'E.g. "Watching her mother practise the new language at the bus stop, lips moving silently, Ana realised that she was not the only one who was afraid." Credit sudden realisation.', 2)],
  evaluate=[('An epiphany is the most important element of a short story.', ['it gives the story meaning', 'it is memorable'], ['setting and conflict create the epiphany', 'some stories deliberately avoid resolution'], 'Epiphanies often give stories their meaning, but they depend on setting and conflict, and some stories deliberately withhold them.')],
  extended=[('Analyse how a short story you have studied uses setting, conflict and epiphany to explore its theme.', 'Indicative content: setting and its cultural significance; internal/external conflict; the epiphany and its effect; quotation and analysis; links to theme. Criteria A and B.', 8, 'long')])
pq('ch07-st1', ('C2', 'C3', 'C4'), (1, 5), None, 'epiphany', ['Identify the moment of epiphany in this extract and explain its significance.',
                                                          'How does the ending of this extract change the reader\'s understanding of the story?'], ids=TR, crit=CRIT_A)
pq('ch07-st1', ('C2', 'C3'), (1, 4), None, 'conflict', ['Identify the conflict in this extract and explain how it is developed.',
                                                     'Is the main conflict internal or external? Explain with evidence.'], ids=TR, crit=CRIT_A)
pq('ch07-st1', ('C2', 'C3'), (1, 4), None, 'struct', STRUCT_Q, ids=STORY, crit=CRIT_B)
K.dev_mcq('ch07-st1', ids=STORY)
para('ch07-st1', None, ids=TR, c='C4', d=(3, 5))

H('ch07-st2',
  terms=[('translated literature', 'literature originally written in one language and rendered into another'),
         ('culture-specific item', 'a word, custom or reference with no exact equivalent in another culture (e.g. "Obon")'),
         ('foreignisation', 'a translation approach that keeps the source culture visible, for example by retaining original words'),
         ('domestication', 'a translation approach that adapts the text to the target culture so it reads smoothly'),
         ('cultural context', 'the beliefs, customs and history that shape a text\'s meaning')],
  facts=[('Keeping the word "Obon" in an English text is an example of:', 'foreignisation', ['domestication', 'a pun', 'a malapropism'], 'The source culture stays visible.'),
         ('Obon is:', 'a Japanese Buddhist festival honouring ancestors\' spirits', ['a Chinese New Year dish', 'a Korean sport', 'a type of lantern only used at weddings'], 'Lanterns guide spirits.'),
         ('Replacing a culture-specific food with a familiar English one is:', 'domestication', ['foreignisation', 'transliteration', 'onomatopoeia'], 'It adapts to the reader\'s culture.'),
         ('Many Chileans went into exile in the 1970s and 1980s because of:', 'the military dictatorship', ['a volcanic eruption', 'the Olympic Games', 'a football tournament'], 'Political repression drove many into exile.')],
  why=[('Explain why translators sometimes keep words from the original language.', 'Some words carry cultural meanings with no exact English equivalent; keeping them preserves meaning and reminds readers of the source culture.'),
       ('Explain why reading translated literature broadens readers\' perspectives.', 'It shows how people in other cultures experience universal concerns – grief, home, family – in different ways.'),
       ('Explain why cultural context is needed to understand the lantern ceremony in the Kyoto story.', 'Knowing that the lanterns guide ancestors\' spirits explains the ritual\'s meaning and Grandmother\'s final words.')],
  contrast=[('foreignisation', 'domestication', 'Foreignisation keeps the source culture visible (retaining words and customs); domestication adapts the text to feel familiar to the target audience.')],
  misc=[('A translation is exactly the same text in a different language.', 'Every translation involves choices about meaning, tone and culture; no translation is a perfect copy.')],
  apply=[('Identify two culture-specific items in the Cairo or Kyoto story and explain what each adds.', 'E.g. Cairo: rooftop pigeon-keeping (tradition, city life), "ya Karim" (intimate Arabic address). Kyoto: Obon (ancestor festival), "Ojiichan" (affectionate family term).', 3),
         ('Explain one advantage and one disadvantage of domesticating the word "phở" as "noodle soup" in an English text.', 'Advantage: easier for readers; disadvantage: loses the specific dish and its cultural associations.', 2)],
  evaluate=[('Translated literature can never be fully understood by readers from another culture.', ['cultural references and wordplay are lost', 'context is unfamiliar'], ['universal emotions cross cultures', 'translators and notes bridge gaps'], 'Some nuance is always lost, but translated literature still communicates powerfully, especially when readers learn about its context.')],
  extended=[('Explore how a short story from another culture you have studied presents its cultural context, and how this shapes meaning for an English-speaking reader.', 'Indicative content: cultural context; culture-specific items; how translation choices affect meaning; universal and specific themes; evidence. Criteria A and B.', 8, 'long')])
pq('ch07-st2', ('C2', 'C3', 'C4'), (1, 5), None, 'culture', ['How does this extract present its cultural context? Refer to specific details.',
                                                         'Explain how culture-specific words or customs shape the meaning of the extract.',
                                                         'What would an English-speaking reader need to know to understand this extract fully? Explain.'], ids=TR + ['travel_hanoi', 'travel_atacama'], crit=CRIT_A)
pq('ch07-st2', ('C2', 'C3'), (1, 4), None, 'theme', THEME_Q, ids=TR, crit=CRIT_OPEN)
pq('ch07-st2', 'C3', (2, 4), None, 'dev', ['Explain how "{quote}" reflects the cultural setting of the story.'], ids=TR, crit=CRIT_B)
K.vocab('ch07-st2', ids=TR + ['travel_hanoi'])

H('ch07-st3',
  terms=[('symbol', 'an object, person or image that represents a larger idea'),
         ('motif', 'a recurring element (image, object, phrase) that develops a theme'),
         ('extended symbol', 'a symbol developed across a whole text'),
         ('universal symbol', 'a symbol with similar meanings across many cultures (light for hope, a key for home)'),
         ('culture-specific symbol', 'a symbol whose meaning depends on a particular culture (Obon lanterns)')],
  facts=[('In the Valparaíso story, the key symbolises:', 'the lost home and the hope of return', ['wealth', 'a new job', 'a prison'], 'The key represents exile and memory.'),
         ('The pigeons in the Cairo story symbolise:', 'the tension between freedom and belonging', ['war', 'wealth', 'illness'], 'They fly but always return.'),
         ('Counting strokes in the lake extract is best described as:', 'a motif', ['a flashback', 'a pun', 'a stage direction'], 'It recurs and changes meaning.'),
         ('A symbol whose meaning depends on a particular culture is:', 'culture-specific', ['universal', 'literal', 'onomatopoeic'], 'E.g. Obon lanterns.')],
  why=[('Explain why writers use symbols rather than stating ideas directly.', 'Symbols make abstract ideas concrete and memorable and allow readers to discover meaning for themselves.'),
       ('Explain why a motif can show a character\'s development.', 'When a recurring element changes – Ama stops counting – the change marks the character\'s growth.'),
       ('Explain why the same symbol can mean different things in different cultures.', 'Symbols draw on cultural associations; a colour or animal may signal luck in one culture and death in another.')],
  contrast=[('a symbol', 'a motif', 'A symbol is an image representing an idea; a motif is a recurring element (which may be a symbol) that develops a theme through repetition.')],
  misc=[('Every object in a story is a symbol.', 'Symbols are emphasised, repeated or placed at key moments; ordinary details are not automatically symbolic.')],
  apply=[('Explain how the key in the Valparaíso story changes meaning by the end.', 'At first it represents exile and longing for return; when given away, it represents acceptance and a new idea of home as relationship rather than building.', 3),
         ('Invent a symbol for a story about a family that has emigrated, and explain what it represents.', 'E.g. a grandmother\'s sewing tin brought from home – memory, continuity, the work of mending a broken life. Credit a concrete object and clear meaning.', 2)],
  evaluate=[('Symbols are more effective when readers have to work out their meaning.', ['active interpretation engages readers', 'subtlety rewards rereading'], ['obscure symbols may be missed', 'some clarity helps all readers'], 'Symbols work best when they are suggestive but grounded in clear textual emphasis.')],
  extended=[('Analyse how a writer uses symbolism and motif in a short story you have studied.', 'Indicative content: identifies key symbol/motif; how it develops across the story; cultural associations; links to theme; quotation and analysis. Criteria A and B.', 8, 'long')])
pq('ch07-st3', ('C2', 'C3', 'C4'), (1, 5), None, 'symbol', ['Identify a symbol in this extract and explain what it represents.',
                                                        'How does the writer develop a symbol to explore the story\'s theme?',
                                                        'Explain how the meaning of the central symbol changes during the extract.'], ids=TR + ['coa_lake', 'coa_results', 'coa_shipyard'], crit=CRIT_A)
pq('ch07-st3', ('C2', 'C3'), (1, 4), None, 'dev', ['Explain how "{quote}" works as a symbol or motif.'], ids=TR + ['coa_lake', 'dys_tree'], crit=CRIT_B)
K.compare('ch07-st3', c='C4', d=(3, 5), frames=['{q}', '{q} Focus on symbolism and imagery.'], only=TR + ['coa_shipyard', 'leaving_poem', 'grandmother_kitchen'])
para('ch07-st3', None, ids=TR + ['coa_lake'], c='C4', d=(3, 5), frames=['{gq} Focus on symbol and motif.'])


# =============================================================================================
# ch08 Dystopian Fiction
# =============================================================================================
DYS = ['dys_harmony', 'dys_ministry', 'dys_escape', 'dys_tree']
H('ch08-st1',
  terms=[('dystopia', 'an imagined society that is oppressive, frightening or dehumanising, often presented as a warning'),
         ('utopia', 'an imagined perfect society'),
         ('totalitarian state', 'a government that controls every aspect of public and private life'),
         ('surveillance', 'close monitoring of people\'s behaviour, often by the state'),
         ('conformity', 'behaving according to the rules and expectations of a group or state')],
  facts=[('Which novel by George Orwell (1949) introduced "Big Brother" and "Newspeak"?', 'Nineteen Eighty-Four', ['Animal Farm', 'Brave New World', 'Fahrenheit 451'], 'Orwell\'s novel is the classic dystopia.'),
         ('In which dystopian novel are books burned by "firemen"?', 'Fahrenheit 451 (Ray Bradbury)', ['The Hunger Games', 'Macbeth', 'Lord of the Flies'], 'Bradbury\'s firemen burn books.'),
         ('The word "utopia" was coined by:', 'Thomas More (1516)', ['William Shakespeare', 'George Orwell', 'Aldous Huxley'], 'More\'s "Utopia" means "no place".'),
         ('Which is a typical convention of dystopian fiction?', 'A protagonist who begins to question the system', ['A happy, carefree society with no problems', 'A talking animal guide', 'A historical battle'], 'Questioning drives the plot.')],
  why=[('Explain why dystopian fiction is often described as a warning.', 'It exaggerates current trends (surveillance, censorship, environmental collapse) to show where they might lead, urging readers to resist them.'),
       ('Explain why dystopian societies often appear perfect on the surface.', 'Presenting control as harmony shows how oppression can be disguised, making it more chilling and realistic.'),
       ('Explain why dystopian protagonists are often ordinary people.', 'Readers identify with them, and their awakening shows that anyone can resist.')],
  contrast=[('utopia', 'dystopia', 'A utopia is an ideal society; a dystopia is an oppressive one, often disguised as a utopia.')],
  misc=[('Dystopian fiction is about the future, so it is unrelated to the present.', 'Dystopias are usually critiques of present-day trends, projected into the future.')],
  apply=[('List four dystopian conventions in the Unity Sector opening, with evidence.', 'Controlling state (the Director); surveillance (wrist scanner, Harmony Score); loss of individuality (Citizen 4471); propaganda slogan ("A HAPPY CITIZEN..."); enforced emotion (sadness illegal).', 4),
         ('Suggest a present-day trend that could inspire a dystopian story, and describe the society it might create.', 'E.g. constant social-media ratings – a society where your score decides your job and home; credit a clear trend and an extrapolated society.', 2)],
  evaluate=[('Dystopian fiction is more relevant today than ever.', ['surveillance technology and misinformation are growing', 'climate change raises survival fears'], ['every generation has felt dystopias were relevant', 'exaggeration can distort real issues'], 'Dystopias remain relevant because they adapt to each era\'s fears; today\'s technology gives them particular urgency.')],
  extended=[('Analyse how a dystopian text you have studied uses its conventions to warn readers about the present.', 'Indicative content: identifies conventions; links to real-world concerns; analysis of language and structure; evaluation of the warning\'s effectiveness. Criteria A and B.', 8, 'long')])
pq('ch08-st1', ('C2', 'C3', 'C4'), (1, 5), None, 'dystopia', ['Identify the dystopian conventions in this extract and explain their effect.',
                                                          'How does the writer establish a dystopian world here?',
                                                          'What warning about the real world might this extract contain?'], ids=DYS, crit=CRIT_A)
pq('ch08-st1', ('C2', 'C3'), (1, 4), None, 'tone', TONE_Q, ids=DYS, crit=CRIT_A)
K.dev_mcq('ch08-st1', ids=DYS)
para('ch08-st1', None, ids=DYS, c='C4', d=(3, 5))

H('ch08-st2',
  terms=[('propaganda', 'information, often biased or misleading, used to promote a political cause or view'),
         ('Newspeak', 'Orwell\'s invented language in Nineteen Eighty-Four, designed to limit thought by reducing vocabulary'),
         ('euphemism', 'a mild word replacing a harsh one ("Calm Centre" for "prison")'),
         ('doublethink', 'Orwell\'s term for holding two contradictory beliefs at once'),
         ('slogan', 'a short, memorable phrase used in propaganda or advertising')],
  facts=[('"Prison" renamed as "Calm Centre" is an example of:', 'euphemism', ['hyperbole', 'alliteration', 'onomatopoeia'], 'It softens a harsh reality.'),
         ('In Nineteen Eighty-Four, Newspeak was designed to:', 'make dissenting thought impossible by removing words', ['teach foreign languages', 'make poetry more beautiful', 'help children spell'], 'Fewer words, fewer thoughts.'),
         ('"WAR IS PEACE" from Nineteen Eighty-Four is an example of:', 'doublethink/paradox in propaganda', ['a simile', 'a statistic', 'a pun'], 'Contradiction accepted as truth.'),
         ('"A HAPPY CITIZEN IS A SAFE CITIZEN" is a:', 'propaganda slogan', ['news headline', 'stage direction', 'haiku'], 'It promotes the state\'s message.')],
  why=[('Explain why dystopian regimes control language.', 'If people lack words for ideas like freedom or protest, they struggle to think or organise against the regime.'),
       ('Explain why euphemism is a powerful tool of control.', 'It disguises cruelty as kindness, making oppression seem acceptable or even caring.'),
       ('Explain why slogans are effective propaganda.', 'They are short, repeated and memorable, so they shape beliefs without argument.')],
  contrast=[('propaganda', 'persuasion', 'Persuasion presents arguments that can be weighed; propaganda manipulates, often through repetition, emotion and distortion, to serve power.')],
  misc=[('Language control only happens in fiction.', 'Real governments and organisations use euphemism and propaganda ("collateral damage", "enhanced interrogation"); dystopias exaggerate real practices.')],
  apply=[('Invent two euphemisms a dystopian government might use and explain what each hides.', 'E.g. "Re-education holidays" (forced labour camps); "Voluntary silence days" (bans on speech). Credit clear euphemism and hidden reality.', 2),
         ('Explain how the Ministry of Clear Speech\'s actions limit thought, using two examples.', 'Removing "why" prevents questioning; renaming "Protest" as "unhelpful noise" makes protest seem pointless; Jonah cannot explain "freedom".', 3)],
  evaluate=[('Controlling language is the most effective form of control in dystopian fiction.', ['it shapes thought itself', 'it works invisibly'], ['violence and surveillance are more immediate', 'people resist through other means'], 'Language control is especially insidious because it shapes thought, but it usually works alongside surveillance and force.')],
  extended=[('Analyse how a dystopian text you have studied presents language as a tool of control.', 'Indicative content: propaganda, euphemism, slogans and censorship with evidence; effects on characters; links to real-world parallels. Criteria A and B.', 8, 'long')])
pq('ch08-st2', ('C2', 'C3', 'C4'), (1, 5), None, 'control', ['How does the extract show language being used to control people?',
                                                         'Explain how propaganda or euphemism is used in this extract.'], ids=DYS + ['viral_post'], crit=CRIT_A)
pq('ch08-st2', ('C2', 'C3'), (1, 4), None, 'dev', ['Explain how the language in "{quote}" works as propaganda or control.'], ids=['dys_harmony', 'dys_ministry', 'dys_tree'], crit=CRIT_B)
K.vocab('ch08-st2', ids=DYS)
K.compare('ch08-st2', c='C4', d=(4, 5), frames=['{q} Consider how language is used to shape what people think.'], only=['dys_harmony', 'stadium_a', 'viral_post', 'ad_runner', 'speech_reef', 'speech_lincoln', 'speech_truth'])

H('ch08-st3',
  terms=[('pacing', 'the speed at which a narrative moves, controlled by sentence length, paragraphing and detail'),
         ('exposition', 'the opening section that introduces setting and characters'),
         ('rising action', 'events that build tension towards the climax'),
         ('cliffhanger', 'an ending that leaves the reader in suspense'),
         ('time markers', 'words or phrases that show when events happen and control the reader\'s sense of time')],
  facts=[('"The fence. Three metres. Wire at the top." speeds up the pace through:', 'fragments', ['long descriptive sentences', 'dialogue', 'a flashback'], 'Fragments speed the pace.'),
         ('"She jumped." as a final line is an example of:', 'a cliffhanger', ['a resolution', 'exposition', 'a flashback'], 'It leaves suspense.'),
         ('Which choice would slow the pace before a climax?', 'Detailed description of a single moment', ['A series of one-word sentences', 'Skipping ahead a year', 'Removing all description'], 'Detail slows time.'),
         ('"02:14" at the start of the escape scene is a:', 'time marker creating urgency', ['symbol of freedom', 'flashback', 'rhetorical question'], 'Precise time adds urgency.')],
  why=[('Explain why writers vary pace in an extended narrative.', 'Changes in pace control tension and give readers moments to absorb detail before action accelerates.'),
       ('Explain why paragraph length matters for pacing.', 'Short paragraphs create speed and emphasis; longer ones slow the reader and build atmosphere.'),
       ('Explain why a writer might end a chapter on a cliffhanger.', 'It creates suspense and makes the reader continue, especially in longer narratives.')],
  contrast=[('a fast pace', 'a slow pace', 'A fast pace uses short sentences, fragments, verbs of action and little description; a slow pace uses longer sentences, detail and reflection.'),
            ('story time', 'discourse time', 'Story time is how long events take; discourse time is how long the narrative spends describing them.')],
  misc=[('Fast pacing is always better.', 'Constant speed exhausts readers; contrast with slower moments makes the climax effective.')],
  apply=[('Rewrite this sentence to create a fast pace: "Lena ran quickly through the dark compound past many buildings until she reached the high fence, which had wire at the top."', 'E.g. "Lena ran. Past the dormitories. Past the canteen. The fence. Three metres. Wire." Credit fragments and short sentences.', 2),
         ('Outline a five-stage structure for a dystopian short story about a girl who discovers a hidden library.', 'Exposition (controlled society); inciting incident (finds the library); rising action (reads, is noticed); climax (confrontation or escape); resolution/open ending. Credit five clear stages.', 3)],
  evaluate=[('Structure matters more than language in creating tension.', ['pacing and order control suspense', 'cliffhangers drive reading'], ['vivid language makes danger real', 'both work together'], 'Structure creates the shape of tension, but language makes each moment vivid; the best writing combines them.')],
  extended=[('Analyse how a writer uses structure and pacing to create tension in a dystopian narrative you have studied.', 'Indicative content: overall structure; sentence and paragraph length; time markers; climax and cliffhanger; quotations and effects. Criteria A and B.', 8, 'long')])
pq('ch08-st3', ('C2', 'C3', 'C4'), (1, 5), None, 'struct', STRUCT_Q + ['How does the writer control the pace of this extract?'], ids=DYS + ['coa_lake', 'tr_valparaiso'], crit=CRIT_B)
pq('ch08-st3', ('C2', 'C3', 'C4'), (1, 5), None, 'dev', ['Analyse how sentence structure in "{quote}" affects the pace of the narrative.'], ids=DYS + ['coa_lake'], crit=CRIT_B)
para('ch08-st3', None, ids=['dys_escape', 'dys_harmony', 'coa_lake'], c='C4', d=(3, 5), frames=['{gq} Focus on structure and pacing.'])

H('ch08-st4',
  terms=[('world-building', 'creating a believable imagined world through details of society, technology, rules and history'),
         ('in medias res', 'starting in the middle of the action'),
         ('show, don\'t tell', 'revealing the world through details and actions rather than explanation'),
         ('hook', 'an opening that raises questions and makes the reader want to continue')],
  facts=[('Which is the most effective dystopian opening line?', '"Nobody in Unity Sector had been sad for eleven years. It was against the law."', ['"This is a story about a bad government."', '"Once upon a time there was a city."', '"The future was not nice."'], 'It hooks with irony and world-building.'),
         ('Revealing a society\'s rules through a sign ("DO NOT BREATHE ON THE EXHIBIT") is an example of:', 'show, don\'t tell', ['info-dumping', 'a flashback', 'an epilogue'], 'Details reveal the world.'),
         ('Too much explanation of a dystopian world in the opening is called:', 'info-dumping', ['foreshadowing', 'pathetic fallacy', 'a volta'], 'It slows the opening.')],
  why=[('Explain why dystopian openings often reveal the world gradually.', 'Gradual details create mystery and let readers piece together the society, which is more engaging than an explanation.'),
       ('Explain why a small, ordinary detail can make a dystopian world believable.', 'Everyday details (a wrist scanner at the factory gate) make the society feel lived-in and real.')],
  contrast=[('world-building through detail', 'world-building through explanation', 'Detail lets readers infer the world from objects, rules and actions; explanation tells them directly, which can be dull.')],
  misc=[('A dystopian opening must explain the history of the society.', 'Effective openings hint at history and leave readers curious; explanation can come later or not at all.')],
  apply=[('Write the first two sentences of a dystopian story set in a city where music is banned.', 'Credit a hook, world-building through detail and a hint of the protagonist\'s resistance.', 2),
         ('Rewrite this opening to show rather than tell: "In the future the government watched everyone all the time."', 'E.g. "The camera above Jas\'s bed blinked green as she woke, the way it had every morning of her life." Credit concrete detail revealing surveillance.', 2)],
  evaluate=[('A dystopian opening should start with action rather than description.', ['action hooks quickly', 'in medias res creates suspense'], ['description builds the world', 'quiet openings can be chilling'], 'Either can work; what matters is that the opening hooks the reader and reveals the world efficiently.')],
  extended=[('Write the opening (400–500 words) of a dystopian story. Build the world through detail, introduce a protagonist and end with a hook.', 'Indicative content: dystopian conventions; world-building through detail; a protagonist with hints of resistance; controlled pacing; a hook or cliffhanger; varied, accurate language. Criteria B, C, D.', 12, 'long')])
write('ch08-st4', ids=['dys_harmony'])
K.prompts('ch08-st4', 'open', c=('C3', 'C4'), d=(2, 5))
pq('ch08-st4', ('C3', 'C4'), (2, 5), None, 'dystopia', ['Explain how this extract builds a dystopian world, then write the first sentence of your own dystopian opening using one of the same techniques.'], ids=DYS, crit=CRIT_B)
pq('ch08-st4', 'C3', (2, 4), None, 'dev', ['Explain how "{quote}" hooks the reader, and how you could use a similar technique in a dystopian opening.'], ids=['dys_harmony', 'dys_tree', 'dys_ministry'], crit=CRIT_B)


# =============================================================================================
# ch09 Advertising and Visual Texts
# =============================================================================================
ADS = ['ad_runner', 'ad_parody', 'campaign_water', 'ad_phone', 'trainers', 'robotdog', 'fastfashion_poster', 'museum_site']
H('ch09-st1',
  terms=[('salience', 'the quality of standing out; the element that first draws the eye'),
         ('framing (visual)', 'what is included in the image and how it is cropped'),
         ('camera angle', 'the angle from which an image is taken: low (makes subjects powerful), high (makes them vulnerable), eye level'),
         ('typography', 'the style, size and arrangement of lettering'),
         ('colour connotation', 'the associations a colour carries (red – danger or passion; green – nature)'),
         ('white space', 'empty areas of a design that focus attention and suggest simplicity')],
  facts=[('A low-angle shot usually makes the subject appear:', 'powerful', ['weak', 'distant', 'comic'], 'Looking up suggests power.'),
         ('In the running-shoe advert, the orange shoes in a black-and-white photo show:', 'salience through selective colour', ['white space', 'a high-angle shot', 'a pun'], 'Colour draws the eye.'),
         ('In Western layouts, readers typically scan:', 'from top left to bottom right', ['from bottom right to top left', 'from the centre outwards only', 'randomly'], 'This is why logos often sit bottom right.'),
         ('Large white space around a single product suggests:', 'luxury and simplicity', ['cheapness', 'urgency', 'danger'], 'Minimalism connotes premium quality.')],
  why=[('Explain why advertisers place logos in the bottom right of a design.', 'Readers often finish scanning there, so the brand is the last thing they see and remember.'),
       ('Explain why colour choices are important in visual texts.', 'Colours carry connotations and draw attention, shaping mood and meaning before any words are read.'),
       ('Explain why typography matters in an advertisement.', 'The style of lettering suggests personality – elegant script for luxury, bold capitals for urgency – reinforcing the message.')],
  contrast=[('a low-angle shot', 'a high-angle shot', 'A low angle looks up at the subject, making it powerful; a high angle looks down, making it vulnerable or small.'),
            ('salience', 'white space', 'Salience is what stands out; white space is empty area that helps create salience by removing distractions.')],
  misc=[('Visual analysis means describing what is in the picture.', 'Visual analysis explains how choices such as colour, angle, layout and typography create meaning and persuade.')],
  apply=[('Analyse two visual choices in the smartphone billboard and their effects.', 'E.g. white space (luxury, focus); central placement and black-on-white contrast (salience); small grey text (understated confidence). Credit two choices with effects.', 3),
         ('Describe how you would design a poster for a school charity run, naming three visual choices and their intended effects.', 'E.g. low-angle photo of runners (heroic); bright school colours (identity, energy); bold slogan top left and logo bottom right (reading path). Credit three choices with effects.', 3)],
  evaluate=[('Images persuade more than words in advertising.', ['images are processed instantly', 'they create emotional associations'], ['slogans anchor meaning', 'words give information and calls to action'], 'Images often make the first impact, but words anchor their meaning; effective adverts combine both.')],
  extended=[('Analyse how a visual text (advertisement, poster or web page) you have studied uses visual grammar to create meaning.', 'Indicative content: salience, framing, angle, colour, typography, layout; how image and text interact; effect on target audience. Criteria A and B.', 8, 'long')])
pq('ch09-st1', ('C2', 'C3', 'C4'), (1, 5), None, 'visual', VIS_Q + ['Explain how salience, colour or layout guide the viewer\'s eye in this text.'], ids=ADS, crit=CRIT_A)
pq('ch09-st1', ('C2', 'C3'), (1, 4), None, 'dev', ['Explain how the choice in "{quote}" contributes to the text\'s message.'], ids=['ad_runner', 'ad_phone', 'campaign_water'], crit=CRIT_B)
K.dev_mcq('ch09-st1', ids=['ad_runner', 'ad_phone', 'campaign_water'])
para('ch09-st1', None, ids=ADS, c='C4', d=(3, 5), frames=['{gq} Refer to visual grammar (salience, framing, colour, typography, layout).'])

H('ch09-st2',
  terms=[('target audience', 'the specific group an advertisement aims to persuade'),
         ('slogan', 'a short, memorable phrase associated with a brand'),
         ('endorsement', 'support for a product from a celebrity or expert'),
         ('aspirational advertising', 'advertising that links a product to an ideal lifestyle or self-image'),
         ('call to action', 'an instruction to the audience to buy, join or act'),
         ('unique selling point (USP)', 'the feature that makes a product different from competitors')],
  facts=[('An Olympic athlete appearing in a shoe advert is an example of:', 'endorsement', ['a testimonial from a customer', 'a statistic', 'a pun'], 'A respected figure transfers credibility.'),
         ('"YOUR ONLY RIVAL IS YESTERDAY" appeals mainly to:', 'self-improvement and aspiration', ['fear of danger', 'saving money', 'nostalgia'], 'It suggests becoming better.'),
         ('"Join the #OneShirtChallenge" is a:', 'call to action', ['slogan only', 'statistic', 'disclaimer'], 'It asks the audience to act.'),
         ('Who is the most likely target audience for the running-shoe advert?', 'Young, ambitious runners', ['Retired people who dislike exercise', 'Young children', 'Car buyers'], 'Imagery and endorsement target them.')],
  why=[('Explain why advertisers use celebrity endorsement.', 'Audiences transfer their admiration and trust from the celebrity to the product, hoping to share the celebrity\'s qualities.'),
       ('Explain why aspirational advertising is effective.', 'It sells a feeling or identity rather than just a product, appealing to people\'s desire to become their ideal selves.'),
       ('Explain why slogans are kept short.', 'Short slogans are memorable and easily repeated, so they stay associated with the brand.')],
  contrast=[('endorsement', 'testimonial', 'Endorsement uses a celebrity or expert; a testimonial uses an ordinary customer\'s account of the product.')],
  misc=[('Adverts only persuade people to buy products.', 'Adverts and campaigns also persuade people to change behaviour, support causes or adopt values.')],
  apply=[('Identify the target audience of the water campaign poster and two techniques aimed at it.', 'Teenagers/young adults: hashtag challenge (social media); statistic about T-shirts (clothes they buy); direct question "do I need it?".', 3),
         ('Write a slogan and a call to action for an advert selling a reusable water bottle to teenagers.', 'E.g. slogan "Refill. Rethink. Repeat."; call to action "Grab yours in the canteen from Monday." Credit memorable slogan and specific call to action.', 2)],
  evaluate=[('Advertising aimed at teenagers should be more strictly regulated.', ['teenagers are vulnerable to pressure on body image and status', 'social media advertising is hard to spot'], ['teenagers can learn media literacy', 'over-regulation limits useful information'], 'Some regulation is justified, especially on harmful products and hidden ads, but media literacy is also essential.')],
  extended=[('Analyse how an advertisement you have studied uses persuasive techniques to appeal to its target audience.', 'Indicative content: target audience; slogan, endorsement, aspiration, call to action; visual and verbal techniques with evidence; effects. Criteria A and B.', 8, 'long')])
pq('ch09-st2', ('C2', 'C3', 'C4'), (1, 5), None, 'persuade', ['Identify the persuasive techniques used in this text and explain how they appeal to the target audience.',
                                                          'How does this text persuade its audience? Refer to slogan, image and any endorsement.'], ids=ADS, crit=CRIT_A)
pq('ch09-st2', ('C2', 'C3'), (1, 4), None, 'aud', AUD_Q, ids=ADS, crit=CRIT_A)
pq('ch09-st2', ('C2', 'C3'), (1, 4), None, 'purp', PURP_Q, ids=ADS, crit=CRIT_A)
K.tone_mcq('ch09-st2', ids=ADS)
K.kind_mcq('ch09-st2', ids=ADS + ['viral_post', 'factcheck'])

H('ch09-st3',
  terms=[('intertextuality', 'the way a text refers to, borrows from or echoes another text'),
         ('parody', 'an imitation of a text\'s style or conventions for comic or critical effect'),
         ('pastiche', 'an imitation that celebrates rather than mocks its source'),
         ('allusion', 'a brief reference to another text, person or event'),
         ('bathos', 'an anticlimax from the elevated to the ordinary, often for comic effect')],
  facts=[('"EAU DE EXAM" imitates the conventions of:', 'luxury perfume adverts', ['news reports', 'war poetry', 'recipes'], 'It borrows perfume branding.'),
         ('"Because you\'re worth… a B+." creates humour through:', 'bathos', ['pathos', 'alliteration', 'statistics'], 'The grand promise collapses.'),
         ('An imitation that mocks its source is a:', 'parody', ['pastiche', 'translation', 'summary'], 'Parody criticises or mocks.'),
         ('A brief reference to another text is an:', 'allusion', ['aside', 'epiphany', 'anagram'], 'Allusions are brief references.')],
  why=[('Explain why media texts use intertextuality.', 'Recognising a reference creates pleasure and a sense of shared knowledge, and borrowed associations add meaning quickly.'),
       ('Explain why parody can be an effective form of criticism.', 'By exaggerating a text\'s conventions, parody exposes their absurdity or hidden values, making audiences laugh and think.')],
  contrast=[('parody', 'pastiche', 'Parody imitates in order to mock or criticise; pastiche imitates in a celebratory or neutral way.')],
  misc=[('Intertextuality is the same as copying.', 'Intertextuality transforms or comments on its source, creating new meaning.')],
  apply=[('Identify two conventions of luxury adverts that "Eau de Exam" parodies and explain how each is twisted.', 'E.g. glamorous lighting/close-up applied to a tired student; perfume "notes" become "revision, panic and cold toast"; mock-French name; legal small print becomes an absurd warning.', 3),
         ('Plan a parody of a sports-drink advert that criticises the pressure on teenagers to be constantly productive.', 'Credit identification of conventions (heroic athlete, energetic slogan, endorsement) and a clear critical twist.', 3)],
  evaluate=[('Parody adverts are more persuasive than serious campaigns.', ['humour is memorable and shareable', 'it disarms audiences'], ['humour can trivialise serious issues', 'audiences may miss the point'], 'Parody can be very effective for engagement, but serious campaigns may suit issues that need sober reflection.')],
  extended=[('Analyse how a media text you have studied uses intertextuality or parody to create meaning.', 'Indicative content: identifies source conventions; how they are borrowed or twisted; effect on audience; purpose of the parody. Criteria A and B.', 8, 'long')])
pq('ch09-st3', ('C2', 'C3', 'C4'), (1, 5), None, 'intertext', ['Explain how this text uses intertextuality or parody.',
                                                           'Which conventions does this text borrow, and how does it change them?'], ids=['ad_parody'], crit=CRIT_A)
pq('ch09-st3', ('C2', 'C3', 'C4'), (1, 5), None, 'dev', ['Explain how "{quote}" uses parody or bathos to create humour and make a point.'], ids=['ad_parody'], crit=CRIT_B)
pq('ch09-st3', ('C2', 'C3'), (1, 4), None, 'tone', TONE_Q, ids=['ad_parody', 'dys_tree', 'speech_captain'], crit=CRIT_A)
K.compare('ch09-st3', c='C4', d=(3, 5), frames=['{q} Consider how each text uses or transforms familiar conventions.'], only=['ad_runner', 'trainers', 'fastfashion_poster', 'lostdog', 'viral_post'])
para('ch09-st3', None, ids=['ad_parody'], c='C4', d=(3, 5))

H('ch09-st4',
  terms=[('multimodal text', 'a text that combines two or more modes: written words, images, sound, video, layout'),
         ('campaign', 'a coordinated series of texts across platforms with a shared message and goal'),
         ('platform', 'the medium where a text appears (poster, website, social media, video)'),
         ('brand identity', 'consistent visual and verbal features (logo, colours, slogan) that make a campaign recognisable'),
         ('engagement', 'how actively an audience responds: sharing, commenting, participating')],
  facts=[('A campaign that combines a poster, a hashtag challenge and a video is:', 'multimodal and multi-platform', ['monomodal', 'a single print advert', 'a news report'], 'It uses several modes and platforms.'),
         ('Why does the water campaign use a hashtag?', 'To encourage participation and spread the message on social media', ['To make the poster longer', 'To hide the logo', 'Because hashtags are required by law'], 'Hashtags drive engagement.'),
         ('Consistent colours and a logo across a campaign create:', 'brand identity', ['bias', 'pathos only', 'irony'], 'Recognition across texts.')],
  why=[('Explain why campaigns use several platforms.', 'Different platforms reach different audiences and do different jobs: posters raise awareness, social media drives participation, video builds emotion.'),
       ('Explain why participatory calls to action are effective with young audiences.', 'Taking part (posting a photo) makes the audience invested and turns them into campaigners who spread the message.'),
       ('Explain why a consistent brand identity matters across a campaign.', 'Consistency makes each text instantly recognisable and reinforces the message every time it is seen.')],
  contrast=[('a single advertisement', 'a campaign', 'A single advert is one text; a campaign coordinates many texts across platforms over time towards a shared goal.')],
  misc=[('A multimodal campaign just repeats the same poster everywhere.', 'Effective campaigns adapt content to each platform while keeping a consistent message and identity.')],
  apply=[('Design a three-part multimodal campaign to reduce food waste in your school: describe a poster, a social media post and a short video.', 'Credit consistent message and identity; poster with salient image and slogan; social post with call to action/hashtag; video with narrative or emotional appeal; clear target audience.', 4),
         ('Write the text for an Instagram post that extends the water campaign, with a caption, a hashtag and a call to action.', 'Credit concise, informal register; link to "Every drop has a history"; hashtag; clear call to action.', 2)],
  evaluate=[('Social media is the most important platform for a youth campaign.', ['it reaches young people directly', 'it enables participation and sharing'], ['posters and school events reach everyone', 'online messages can be lost in noise'], 'Social media is vital for engagement, but the most effective campaigns combine online and offline platforms.')],
  extended=[('Create a pitch (about 400 words) for a multimodal campaign on an issue that matters to teenagers. Describe at least three texts across different platforms and justify your choices.', 'Indicative content: clear goal and target audience; consistent slogan and brand identity; three platform-specific texts with visual and verbal choices; justification of persuasive techniques; organised, persuasive register. Criteria B, C, D.', 12, 'long')])
pq('ch09-st4', ('C2', 'C3', 'C4'), (1, 5), None, 'campaign', ['Explain how this text works as part of a multimodal campaign.',
                                                          'How does this text try to turn its audience into participants?'], ids=['campaign_water'], crit=CRIT_A)
pq('ch09-st4', ('C3', 'C4'), (2, 5), None, 'visual', ['Using this text as a model, describe a second text for the same campaign on a different platform, explaining your visual and verbal choices.'], ids=ADS, crit=CRIT_W)
pq('ch09-st4', ('C2', 'C3'), (1, 4), None, 'persuade', ['Explain which persuasive techniques in this text could be reused in a social media campaign, and why.'], ids=ADS, crit=CRIT_A)
write('ch09-st4', ids=['trainers', 'plasticfree', 'phonesfree'])


# =============================================================================================
# ch10 Creative Writing from Visual Prompts (eAssessment Task 2)
# =============================================================================================
H('ch10-st1',
  terms=[('visual prompt', 'an image used as a stimulus for creative writing, as in eAssessment Task 2'),
         ('literal reading', 'what an image actually shows'),
         ('inferential reading', 'what an image suggests about story, character, mood or theme'),
         ('perspective', 'whose point of view a piece is told from – a person in the image, an object, an outsider'),
         ('mood', 'the feeling an image or piece of writing creates')],
  facts=[('In eAssessment Task 2, students usually choose from:', 'three visual prompts', ['one essay title', 'ten poems', 'a set novel'], 'Three images are offered.'),
         ('Which response to an image of an empty swing in fog is most imaginative?', 'A story told by the swing, waiting for a child who has grown up', ['"There is a swing. It is foggy."', 'A list of playground equipment', 'A weather forecast'], 'An unusual perspective shows insight.'),
         ('Working out what an image suggests rather than shows is:', 'inferential reading', ['literal reading', 'skimming', 'proofreading'], 'Inference goes beyond the literal.')],
  why=[('Explain why brainstorming several ideas from an image is useful.', 'The first idea is often obvious; generating several allows the writer to choose the most original and developed.'),
       ('Explain why an unusual perspective can make a response stand out.', 'It shows insight and imagination (criterion C) and makes a familiar image feel new.'),
       ('Explain why the image should be a starting point, not a checklist.', 'Trying to describe every detail produces lists; selecting details that serve a story creates focus and depth.')],
  contrast=[('a literal reading', 'an inferential reading', 'A literal reading describes what is shown; an inferential reading interprets what it suggests about story, character and feeling.')],
  misc=[('You must describe the image accurately for high marks.', 'Task 2 rewards imaginative, insightful responses; the image is a stimulus, not a subject to describe exactly.'),
        ('The mood of your piece must match the image.', 'Writing against the image\'s mood – a joyful memory in a bleak setting – can be powerful.')],
  apply=[('An image shows a suitcase left on an empty railway platform at dusk. Give one literal and three inferential readings.', 'Literal: a suitcase alone on a platform at dusk. Inferential: someone left in a hurry; someone is waiting to return; a refugee\'s only possessions; a decision not to leave. Credit three distinct inferences.', 3),
         ('Suggest three different perspectives from which you could write about an image of a lighthouse in a storm, with the story each would tell.', 'E.g. the keeper (duty and isolation); a sailor in the storm (fear, hope); the lighthouse itself (centuries of watching). Credit three perspectives with stories.', 3)],
  evaluate=[('The best Task 2 responses ignore the obvious interpretation of the image.', ['originality is rewarded', 'unexpected angles engage readers'], ['an obvious idea, well executed, can be powerful', 'forced originality can feel artificial'], 'Originality helps, but control and insight matter most; a familiar idea told with skill can outperform a strange but weak one.')])
K.prompts('ch10-st1', 'interpret', c=('C2', 'C3'), d=(1, 4))
K.prompts('ch10-st1', 'plan', c=('C3', 'C4'), d=(2, 5))
K.prompts('ch10-st1', 'open', c='C4', d=(3, 5))

H('ch10-st2',
  terms=[('show, don\'t tell', 'revealing feelings and character through action, detail and dialogue rather than stating them'),
         ('subtext', 'meaning beneath the surface of dialogue or action'),
         ('dialogue tag', 'the phrase identifying the speaker ("she said")'),
         ('pacing', 'the speed of a narrative, controlled by sentence length, detail and scene choice'),
         ('sensory detail', 'description that appeals to sight, sound, smell, taste or touch')],
  facts=[('Which sentence shows rather than tells?', '"Leo picked at the peeling sticker on the fridge."', ['"Leo was sad."', '"Leo felt upset about his dad."', '"Leo was very emotional."'], 'Action implies feeling.'),
         ('Which is correctly punctuated dialogue?', '"You can\'t sell it," Leo said.', ['"You can\'t sell it" Leo said.', '"You can\'t sell it." Leo said.', 'You can\'t sell it, "Leo said."'], 'Comma inside speech marks before the tag.'),
         ('A new speaker in dialogue should:', 'start on a new line', ['share the same paragraph', 'be written in capitals', 'have no speech marks'], 'New speaker, new line.'),
         ('"For a long moment there was only the hum of the fridge." What does this do to the pace?', 'Slows it, creating a charged pause', ['Speeds it up', 'Has no effect', 'Ends the story'], 'Silence slows time.')],
  why=[('Explain why showing is often more powerful than telling.', 'Readers infer emotions from details and actions, which involves them actively and feels more convincing than being told.'),
       ('Explain why dialogue should contain subtext.', 'People rarely say exactly what they feel; subtext makes dialogue realistic and lets readers sense deeper tensions.'),
       ('Explain why a writer might slow the pace at the most emotional moment.', 'Slowing down – with a pause, a sensory detail or silence – gives the moment weight and lets the reader feel it.')],
  contrast=[('showing', 'telling', 'Showing reveals through detail, action and dialogue ("her hands shook"); telling states directly ("she was nervous").'),
            ('dialogue', 'reported speech', 'Dialogue gives characters\' exact words in speech marks; reported speech summarises what was said ("He said that he was tired").')],
  misc=[('Good stories use a lot of dialogue.', 'Dialogue should be purposeful and limited in short pieces; a few lines with subtext are more effective than long exchanges.'),
        ('Showing means adding as many adjectives as possible.', 'Showing relies on precise actions and telling details, not piles of adjectives.')],
  apply=[('Rewrite "Sam was terrified of the exam" to show rather than tell.', 'E.g. "Sam read the first question three times. The words slid away. Under the desk, his knee would not stop bouncing." Credit action/detail implying fear.', 2),
         ('Write four lines of dialogue between two friends in which one is hiding bad news. Use correct punctuation and subtext.', 'Credit correct speech punctuation, new line per speaker and subtext (evasion, changing the subject, short answers).', 3)],
  evaluate=[('Dialogue is the most effective way to reveal character.', ['speech reveals voice and relationships', 'subtext adds depth'], ['actions and thoughts can reveal more', 'too much dialogue slows short pieces'], 'Dialogue is powerful, but it works best combined with action and detail that show what characters cannot say.')],
  extended=[('Write a narrative of 400–600 words in which a character receives unexpected news. Show the character\'s feelings through action, detail and dialogue, and control the pace at the key moment.', 'Indicative content: showing not telling; purposeful dialogue with subtext; varied pacing (slowing at the climax); sensory detail; correctly punctuated speech; deliberate structure. Criteria B, C, D.', 16, 'long')])
pq('ch10-st2', ('C2', 'C3', 'C4'), (1, 5), None, 'show', ['How does the writer show, rather than tell, the characters\' feelings?',
                                                      'Find two examples of showing rather than telling and explain their effect.'], ids=['model_car'], crit=CRIT_A)
pq('ch10-st2', ('C2', 'C3', 'C4'), (1, 5), None, 'dialogue', ['How does the writer use dialogue to reveal character and conflict?',
                                                          'Explain how subtext works in the dialogue of this extract.'], ids=['model_car'], crit=CRIT_A)
pq('ch10-st2', ('C2', 'C3'), (1, 4), None, 'dev', ['Explain how "{quote}" shows a character\'s feelings without stating them.', 'How does "{quote}" control the pace of the narrative?'], ids=['model_car', 'coa_court', 'coa_results', 'tr_valparaiso', 'dys_escape'], crit=CRIT_B)
write('ch10-st2', ids=['model_car', 'coa_results'])
K.prompts('ch10-st2', 'one', c=('C3', 'C4'), d=(2, 5))
K.prompts('ch10-st2', 'write', c='C4', d=(4, 5))

H('ch10-st3',
  terms=[('form', 'the type of text: story, diary entry, letter, speech, monologue, blog'),
         ('register', 'the level of formality of language, chosen for audience and purpose'),
         ('conventions', 'the features expected in a form (a diary\'s date and private voice; a letter\'s salutation and sign-off)'),
         ('dramatic monologue', 'a piece in which a single character speaks to a silent listener, revealing themselves'),
         ('voice', 'the distinctive personality of the narrator or speaker')],
  facts=[('Which form best suits a private, honest reflection on a single day?', 'A diary entry', ['A news report', 'An advertisement', 'An encyclopedia entry'], 'Diaries are personal and immediate.'),
         ('Which feature is a convention of a letter?', 'A salutation and sign-off', ['A headline and lead', 'Stage directions', 'A slogan and logo'], 'Letters open and close formally.'),
         ('A speech written for Task 2 should include:', 'direct address and devices for the ear', ['footnotes', 'a bibliography', 'stage directions only'], 'Speeches are written to be heard.'),
         ('Which register suits a letter of apology to a head teacher?', 'Formal', ['Slang', 'Text-speak', 'Comic'], 'Register suits the audience.')],
  why=[('Explain why choosing a form is part of creative insight in Task 2.', 'The form shapes voice, structure and audience; an unexpected form (a letter from the swing) can transform an image.'),
       ('Explain why register must be consistent within a piece.', 'Sudden shifts in formality break the voice and confuse the reader unless done deliberately for effect.'),
       ('Explain why a diary entry can create intimacy.', 'The private first-person voice and present feelings make the reader feel trusted with secrets.')],
  contrast=[('a story', 'a diary entry', 'A story is usually narrated for readers and shaped by plot; a diary entry is private, dated and reflective, written as if for the writer alone.'),
            ('formal register', 'informal register', 'Formal register uses complete sentences, precise vocabulary and no slang; informal register is conversational, with contractions and colloquial words.')],
  misc=[('Stories are always the best choice for Task 2.', 'Letters, diaries, speeches or monologues can show insight and control if their conventions are used purposefully.')],
  apply=[('An image shows an old man feeding pigeons alone in a square. Suggest three forms you could use and what each would allow you to do.', 'E.g. diary (his loneliness, private memories); letter to his late wife (intimacy, history); speech at the council meeting to save the square (persuasion). Credit three forms with purposes.', 3),
         ('Rewrite this sentence in a formal register for a letter to a newspaper: "Honestly, the new bus timetable is a total joke and nobody can get to school on time."', 'E.g. "The new bus timetable has made it very difficult for students to arrive at school on time." Credit formal vocabulary and removal of slang.', 2)],
  evaluate=[('Unusual forms score higher in creative writing than stories.', ['they show originality', 'they stand out to examiners'], ['a well-crafted story can show equal insight', 'unusual forms done poorly lose marks'], 'Form should be chosen for purpose; an unusual form helps only if its conventions are used with control.')],
  extended=[('Choose ONE form (diary, letter, speech or dramatic monologue) and write a piece of 400–600 words inspired by an image of a child\'s handprint in wet cement outside a house that is being demolished. Explain your choice of form in one sentence at the end.', 'Indicative content: form conventions used purposefully; consistent voice and register; imaginative interpretation of the image; deliberate structure; accurate language; a justified choice of form. Criteria B, C, D.', 16, 'long')])
K.prompts('ch10-st3', 'plan', c=('C3', 'C4'), d=(2, 5))
K.prompts('ch10-st3', 'one', c='C4', d=(3, 5))
pq('ch10-st3', ('C2', 'C3'), (1, 4), None, 'kconv', KCONV_Q, ids=['leaving_letter', 'hiking_diary', 'speech_captain', 'speech_mayor', 'essay_stammer', 'library_letter'], crit=CRIT_A)
write('ch10-st3', ids=['speech_reef', 'coa_shipyard', 'essay_stammer', 'model_car'])
K.kind_mcq('ch10-st3', ids=['leaving_letter', 'hiking_diary', 'speech_captain', 'essay_stammer', 'model_car', 'poem_chant'])

PROOF10 = [
    ('The flat was silent, the only sound was the clock ticking on the wall.', 'The flat was silent; the only sound was the clock ticking on the wall.', 'comma splice – two independent clauses joined only by a comma; use a semicolon or full stop'),
    ('"Where are you going" asked Mum. "Out" I said.', '"Where are you going?" asked Mum.\n"Out," I said.', 'question mark inside the speech marks; comma before the closing speech mark; new line for a new speaker'),
    ('Each of the students have brought their own torch.', 'Each of the students has brought their own torch.', 'subject–verb agreement: "each" is singular, so "has"'),
    ('Running down the street, the rain soaked my coat.', 'Running down the street, I was soaked by the rain.', 'dangling modifier – the rain was not running; the subject must be the person running'),
    ('Me and Leo should of stayed at home.', 'Leo and I should have stayed at home.', '"Me and Leo" as subject → "Leo and I"; "should of" → "should have"'),
    ('Its the moment the dog lifts it\'s head that I remember.', 'It\'s the moment the dog lifts its head that I remember.', '"it\'s" = it is; "its" = possessive with no apostrophe'),
    ('The crowd were silent, they waited, nobody moved.', 'The crowd was silent. They waited. Nobody moved.', 'comma splices replaced with full stops; short sentences for tension'),
    ('Despite the rain. We decided to walk to the station.', 'Despite the rain, we decided to walk to the station.', 'sentence fragment joined to its main clause with a comma'),
    ('She walked slowly, carefully, and quiet across the ice.', 'She walked slowly, carefully and quietly across the ice.', 'parallel structure: three adverbs ("quietly"); no comma needed before "and" in British style'),
    ('Who\'s phone is ringing.', 'Whose phone is ringing?', '"whose" (possessive) not "who\'s" (who is); question mark'),
]
STYLE10 = [
    ('It was a very very dark night and it was very cold and I was very scared.', 'The night was black and bitter, and fear crept along my spine.', 'repetition of "very" and "and" replaced by precise vocabulary and imagery'),
    ('She said she was sad. She said she wanted to go home. She said she missed her mum.', '"I want to go home," she whispered. "I miss Mum."', 'repetitive reported speech replaced by dialogue that shows emotion'),
    ('The thing was big and nice and had lots of good stuff in it.', 'The market sprawled across the square, its stalls heaped with mangoes, spices and bolts of bright cloth.', 'vague nouns and adjectives ("thing", "nice", "stuff") replaced by precise, concrete detail'),
    ('Suddenly, suddenly the door opened suddenly.', 'The door swung open.', 'redundant repetition of "suddenly" removed; a strong verb ("swung") does the work'),
    ('I walked into the room. I saw a table. I saw a chair. I sat down.', 'I walked into the room, past an empty table, and sank into the only chair.', 'choppy, repetitive sentences combined for flow, with a stronger verb ("sank")'),
]


@R.add('ch10-st4', 'C3', (1, 4), 'short')
def proof10(rng, slot):
    bad, good, rule = rng.choice(PROOF10)
    q = rng.choice([f'Proofread and correct the following sentence: {bad}', f'Identify and correct the error(s) in: {bad}'])
    return dict(stem=q, answer=good, markingKey=f'{good} Error: {rule}. 1 mark for the correction; 1 mark for identifying the error.', type='short', marks=2)


@R.add('ch10-st4', 'C2', (2, 4), 'explain')
def proof10_explain(rng, slot):
    bad, good, rule = rng.choice(PROOF10)
    return dict(stem=f'A student wrote: {bad}\nThe corrected version is: {good}\nExplain the rule that has been applied.', answer=rule[0].upper() + rule[1:] + '.', type='explain', marks=2,
                markingKey=f'{rule}. 1 mark for naming the error, 1 for explaining the rule.')


@R.add('ch10-st4', ('C3', 'C4'), (2, 5), 'short')
def style10(rng, slot):
    bad, good, why = rng.choice(STYLE10)
    q = rng.choice([f'Edit this sentence to improve its style for a creative piece: {bad}', f'Rewrite the following to make it more precise and effective: {bad}'])
    return dict(stem=q, answer=f'E.g. {good}', markingKey=f'Example: {good} ({why}). Credit any edit that removes repetition or vagueness and uses precise vocabulary and varied structure (criterion D).', type='short', marks=3)


H('ch10-st4',
  terms=[('proofreading', 'checking a finished text for errors in spelling, punctuation and grammar'),
         ('editing', 'revising a text to improve clarity, style and effect'),
         ('comma splice', 'joining two independent clauses with only a comma'),
         ('dangling modifier', 'a phrase that does not logically describe the subject of the sentence ("Running down the street, the rain soaked me")'),
         ('subject–verb agreement', 'the verb must match its subject in number ("each has", "they have")'),
         ('Criterion D', 'the MYP criterion for using language: vocabulary, sentence structures, register, accuracy')],
  facts=[('"The flat was silent, the only sound was the clock" contains:', 'a comma splice', ['a dangling modifier', 'correct punctuation', 'a fragment'], 'Two main clauses joined by a comma.'),
         ('Which is correct?', 'Each of the students has a torch.', ['Each of the students have a torch.', 'Each of the student have a torch.', 'Each of the students having a torch.'], '"Each" is singular.'),
         ('Which is correct?', 'The dog lifted its head.', ['The dog lifted it\'s head.', 'The dog lifted its\' head.', 'The dog lifted it is head.'], 'Possessive "its" has no apostrophe.'),
         ('Which MYP criterion assesses accuracy of grammar, spelling and punctuation?', 'Criterion D: Using language', ['Criterion A: Analysing', 'Criterion B: Organising', 'Criterion C: Producing text'], 'Criterion D covers language use.')],
  why=[('Explain why you should leave time to proofread in the eAssessment.', 'Errors in punctuation and grammar can lower criterion D marks; a few minutes of checking can correct many of them.'),
       ('Explain why editing for style is different from proofreading.', 'Proofreading fixes errors; editing improves effect – cutting repetition, choosing precise words, varying sentences.'),
       ('Explain why comma splices are a problem.', 'They blur the boundary between complete thoughts, making writing harder to follow and showing weak control of sentence structure.')],
  contrast=[('proofreading', 'editing', 'Proofreading corrects errors of accuracy; editing revises content and style for clarity and effect.'),
            ('a deliberate fragment', 'an accidental fragment', 'A deliberate fragment is used for effect ("She jumped."); an accidental fragment is an incomplete sentence that should be joined to a main clause.')],
  misc=[('Spell-check catches all errors.', 'Spell-check misses homophones (their/there), missing words and grammar errors; careful proofreading is needed.'),
        ('Fragments are always wrong.', 'Fragments can be used deliberately for effect in creative writing; accidental fragments are errors.')],
  apply=[('Proofread this passage and correct four errors: "Their was a knock at the door, I opened it. Standing on the step, the wind blew my hair. "Who are you" I asked."', '"There was a knock at the door. I opened it. Standing on the step, I felt the wind blow my hair. \'Who are you?\' I asked." – there/their; comma splice; dangling modifier; question mark inside speech marks.', 4),
         ('Edit this sentence for style and accuracy: "The sky was really really dark and the rain was falling down very hard."', 'E.g. "Rain hammered from a sky as dark as wet slate." Credit precise verb, imagery and removal of repetition.', 2)],
  evaluate=[('Accuracy matters more than creativity in Task 2.', ['frequent errors obscure meaning', 'criterion D rewards control'], ['criterion C rewards insight and imagination', 'a few errors in an original piece cost little'], 'Both are assessed; accuracy should support creativity, so writers need time to create and to proofread.')],
  extended=[('Write a 300-word piece inspired by an image, then annotate three edits you would make to improve its accuracy and style, explaining each.', 'Indicative content: a controlled creative piece; three specific edits (accuracy and style) with explanations linked to criterion D. Criteria C and D.', 8, 'long')])


# =============================================================================================
# ch11 Memoir, Personal Essay and Travel Writing
# =============================================================================================
LIFEW = ['memoir_tailor', 'essay_stammer', 'travel_hanoi', 'travel_atacama', 'nobel_mum', 'hiking_diary']
H('ch11-st1',
  terms=[('memoir', 'a non-fiction account of the writer\'s own experiences, focused on particular memories and their meaning'),
         ('personal essay', 'a short non-fiction piece that explores an experience to reach a wider insight'),
         ('reflection', 'the writer\'s thoughtful interpretation of what an experience meant'),
         ('narrating self / experiencing self', 'the older writer telling the story and the younger self who lived it'),
         ('anecdote', 'a short, vivid personal story used to illustrate a point')],
  facts=[('How does a memoir differ from an autobiography?', 'A memoir focuses on particular memories and their meaning; an autobiography usually covers a whole life', ['A memoir is always fiction', 'A memoir is written by someone else', 'There is no difference'], 'Memoir is selective and reflective.'),
         ('"I did not understand, then ... I understand it now" shows:', 'reflection by the narrating self', ['a flashback in a novel', 'a stage direction', 'a news lead'], 'The older self interprets the past.'),
         ('A personal essay typically ends with:', 'a reflection that connects the experience to a wider idea', ['a list of sources', 'a headline', 'a call to buy'], 'Insight is the goal.')],
  why=[('Explain why memoirs use specific sensory details.', 'Precise details ("steam and chalk") make memories vivid and convincing, and show the reader why they lasted.'),
       ('Explain why reflection is essential in memoir and personal essays.', 'Without reflection, a memoir is just a sequence of events; reflection shows what the experience meant and why it matters to readers.'),
       ('Explain why memoirists are not simply objective reporters of the past.', 'Memory is selective and shaped by later understanding, so memoir is an interpretation, not a record.')],
  contrast=[('memoir', 'autobiography', 'Memoir focuses on selected experiences and their meaning; autobiography covers the writer\'s life more fully and chronologically.'),
            ('the narrating self', 'the experiencing self', 'The narrating self is the older writer looking back; the experiencing self is the younger person living the events.')],
  misc=[('Memoir must include every detail exactly as it happened.', 'Memoir selects and shapes memories for meaning; writers should be honest but cannot recall everything exactly.')],
  apply=[('Identify two memoir conventions in the tailor\'s shop extract, with evidence.', 'Sensory detail ("steam and chalk"); reflection ("I did not understand, then ... I understand it now"); focus on a relationship (grandfather); first-person adult narrator.', 2),
         ('Rewrite this flat sentence with a sensory detail and a reflection: "I used to visit my aunt\'s farm every summer."', 'E.g. "Every summer I woke at my aunt\'s farm to the smell of hay and diesel; only later did I realise those weeks were the only time my mother laughed." Credit sense detail and reflection.', 2)],
  evaluate=[('Memoirs are less truthful than biographies.', ['memory is selective and biased', 'writers shape events for meaning'], ['memoirs reveal emotional truth', 'biographies also interpret evidence'], 'Memoirs offer subjective, emotional truth rather than objective record; both forms interpret the past.')],
  extended=[('Analyse how the writer of a memoir or personal essay you have studied uses detail and reflection to create meaning.', 'Indicative content: sensory and telling detail; narrating vs experiencing self; reflection; structure; links to wider themes. Criteria A and B.', 8, 'long')])
pq('ch11-st1', ('C2', 'C3', 'C4'), (1, 5), None, 'memoir', ['Identify the conventions of memoir or personal essay in this extract and explain their effect.',
                                                        'How does the writer use reflection to give meaning to the experience?'], ids=['memoir_tailor', 'essay_stammer'], crit=CRIT_A)
pq('ch11-st1', ('C2', 'C3'), (1, 4), None, 'dev', DEV_Q, ids=LIFEW, crit=CRIT_B)
pq('ch11-st1', ('C2', 'C3'), (1, 4), None, 'tone', TONE_Q, ids=LIFEW, crit=CRIT_A)
K.dev_mcq('ch11-st1', ids=LIFEW)
K.kind_mcq('ch11-st1', ids=LIFEW + ['coa_shipyard', 'leaving_letter'])

H('ch11-st2',
  terms=[('travel writing', 'non-fiction that describes places and the writer\'s experiences of them'),
         ('representation of place', 'how a text portrays a place and its people'),
         ('exoticism', 'presenting a culture as strange, mysterious or timeless for the entertainment of outsiders'),
         ('the "tourist gaze"', 'the way outsiders look at and judge a place according to their own expectations'),
         ('local voice', 'the direct words and perspectives of people who live in the place')],
  facts=[('The guidebook phrase "timeless Old Quarter charm" is an example of:', 'a clichéd, exoticising representation', ['a statistic', 'an objective fact', 'a pun'], 'It presents Hanoi as unchanging.'),
         ('Which choice gives local people more authority in travel writing?', 'Quoting them directly and naming them', ['Describing them only as part of the scenery', 'Leaving them out', 'Generalising about "the locals"'], 'Names and voices give agency.'),
         ('"The driest desert on Earth" is an example of:', 'a superlative', ['a simile', 'an understatement', 'a rhetorical question'], 'It uses the -est form.')],
  why=[('Explain why travel writers should be careful about stereotypes.', 'Stereotypes reduce people and places to clichés, misinform readers and can be disrespectful.'),
       ('Explain why admitting your own expectations can strengthen travel writing.', 'It shows honesty and invites readers to question their own assumptions, as in the Hanoi extract.'),
       ('Explain why sensory description is central to travel writing.', 'It transports readers to a place they may never visit, making the experience vivid.')],
  contrast=[('exoticism', 'respectful representation', 'Exoticism makes a place seem strange and timeless for outsiders; respectful representation shows it as complex and modern, with local voices.')],
  misc=[('Travel writing is just a description of beautiful places.', 'Travel writing also reflects on culture, people, the writer\'s perspective and questions of representation.')],
  apply=[('Rewrite this exoticising sentence to represent the place respectfully: "The mysterious natives of the old market haggled in strange tongues."', 'E.g. "In the market, Mr Okafor and his daughter sold yams and joked with customers in Igbo and English." Credit specific, named people and non-exoticising language.', 2),
         ('Identify two ways the Atacama extract gives authority to local knowledge.', 'Rodrigo is named and his heritage given; he is quoted directly about the dark constellations; the writer says he was "taught how to see".', 2)],
  evaluate=[('Travel writers can never represent another culture fairly.', ['outsiders bring biases', 'short visits give partial views'], ['honest reflection and local voices help', 'outsiders can notice what insiders take for granted'], 'Perfect representation is impossible, but self-awareness, specificity and local voices allow fair, respectful travel writing.')],
  extended=[('Analyse how a travel writer you have studied represents a place and its people.', 'Indicative content: sensory description; representation of people; local voices; stereotypes challenged or reinforced; the writer\'s perspective and reflection. Criteria A and B.', 8, 'long')])
pq('ch11-st2', ('C2', 'C3', 'C4'), (1, 5), None, 'represent', ['How does the writer represent the place and its people?',
                                                           'Does the writer challenge or reinforce stereotypes? Explain with evidence.'], ids=['travel_hanoi', 'travel_atacama'], crit=CRIT_A)
pq('ch11-st2', ('C2', 'C3'), (1, 4), None, 'aud', AUD_Q, ids=['travel_hanoi', 'travel_atacama', 'volcano'], crit=CRIT_A)
pq('ch11-st2', ('C2', 'C3'), (1, 4), None, 'purp', PURP_Q, ids=['travel_hanoi', 'travel_atacama', 'volcano'], crit=CRIT_A)
K.vocab('ch11-st2', ids=LIFEW + ['volcano'])
para('ch11-st2', None, ids=['travel_hanoi', 'travel_atacama', 'volcano'], c='C4', d=(3, 5))

H('ch11-st3',
  terms=[('reflective writing', 'writing that explores an experience and what the writer learned from it'),
         ('epiphany (in non-fiction)', 'the moment the writer realises the significance of an experience'),
         ('honesty', 'a candid voice that admits mistakes, doubts and complex feelings'),
         ('universal significance', 'the way a personal experience connects to ideas other readers share')],
  facts=[('Which ending best suits a reflective personal piece?', '"I still stammer. I have simply stopped apologising for the time it takes me to be heard."', ['"The end."', '"That is what happened."', '"Thanks for reading."'], 'It reflects and generalises.'),
         ('A reflective piece should move from:', 'a specific experience to a wider insight', ['a list of facts to a summary', 'a headline to a quotation', 'a question to a statistic'], 'Experience leads to insight.'),
         ('Which detail is most vivid for a reflective piece about a first job?', '"The fryer hissed every time I dropped a basket, and so did my manager."', ['"It was a job."', '"I worked there."', '"It was okay."'], 'Specific detail with wit.')],
  why=[('Explain why reflective pieces need specific moments rather than general summaries.', 'Specific moments let readers experience events and make reflection earned and convincing.'),
       ('Explain why honesty about mixed feelings strengthens reflective writing.', 'Admitting complexity makes the voice authentic and relatable.')],
  contrast=[('recounting', 'reflecting', 'Recounting tells what happened; reflecting explores what it meant and why it matters.')],
  misc=[('A reflective piece must end with a moral lesson.', 'Reflection can be open, uncertain or ironic; it does not have to preach.')],
  apply=[('Write a reflective final sentence for a piece about losing a football final.', 'E.g. "We lost 3–1, but walking home in our muddy kit, laughing, I understood that I had never really played for the trophy." Credit insight beyond the event.', 2),
         ('Plan a reflective personal piece in three parts about a moment you changed your mind about someone.', 'E.g. opening scene (first impression); turning point (the moment of change); reflection (what it taught you about judging others). Credit three purposeful stages.', 3)],
  evaluate=[('Reflective writing is more valuable when it is about dramatic experiences.', ['dramatic events engage readers', 'they create clear change'], ['ordinary moments can reveal deep insight', 'honest reflection matters more than drama'], 'Reflection, not drama, gives such writing value; small moments can carry great significance.')],
  extended=[('Write a reflective personal piece (400–600 words) about a place that mattered to you as a child. Use sensory detail, a clear structure and a final reflection.', 'Indicative content: specific sensory memories; narrating vs experiencing self; a turning point or realisation; reflective conclusion with wider significance; varied, accurate language. Criteria B, C, D.', 16, 'long')])
write('ch11-st3', ids=['essay_stammer', 'coa_shipyard', 'nobel_mum', 'hiking_diary'])
pq('ch11-st3', ('C3', 'C4'), (2, 5), None, 'reflect', ['Explain how the writer turns a personal experience into a wider reflection, then write a reflective final sentence for a piece of your own on a similar experience.'], ids=['memoir_tailor', 'essay_stammer'], crit=CRIT_W)
pq('ch11-st3', ('C2', 'C3'), (1, 4), None, 'struct', STRUCT_Q, ids=LIFEW, crit=CRIT_B)
K.prompts('ch11-st3', 'one', c='C4', d=(3, 5))


# =============================================================================================
# ch12 eAssessment Preparation and Timed Practice
# =============================================================================================
R.mcqs('ch12-st1', 'C1', (1, 3), [
    ('How long is the MYP Language and literature on-screen eAssessment?', '2 hours', ['45 minutes', '4 hours', '30 minutes'], 'The examination lasts 2 hours.'),
    ('Which criterion assesses insight, imagination and stylistic choices?', 'Criterion C: Producing text', ['Criterion A: Analysing', 'Criterion B: Organising', 'Criterion D: Using language'], 'C covers creativity and style.'),
    ('Which criterion assesses analysis of content, context, language and structure?', 'Criterion A: Analysing', ['Criterion B: Organising', 'Criterion C: Producing text', 'Criterion D: Using language'], 'A covers analysis.'),
    ('Which criterion assesses structure, logical organisation and referencing?', 'Criterion B: Organising', ['Criterion A: Analysing', 'Criterion C: Producing text', 'Criterion D: Using language'], 'B covers organisation.'),
    ('What is the maximum level for each MYP criterion?', '8', ['5', '10', '20'], 'Each criterion is marked 0-8.'),
    ('The eAssessment is completed:', 'on screen, typed by the student', ['by hand on paper only', 'orally', 'as a group project'], 'It is an on-screen exam.'),
])
H('ch12-st1',
  terms=[('Criterion A: Analysing', 'explaining content, context, language, structure, technique and style and their effects, and justifying opinions with evidence'),
         ('Criterion B: Organising', 'using a clear, logical structure suited to the task and connecting ideas purposefully'),
         ('Criterion C: Producing text', 'showing insight, imagination and personal engagement, and making deliberate stylistic choices'),
         ('Criterion D: Using language', 'using varied, accurate vocabulary, sentence structures, register and conventions'),
         ('level descriptor', 'the description of performance at each band (1-2, 3-4, 5-6, 7-8)'),
         ('best-fit judgement', 'choosing the band whose descriptor best matches the work overall')],
  why=[('Explain why it is useful to know which criteria each task assesses.', 'Students can focus their effort on what is rewarded – analysis and organisation in Task 1, creativity and language in Task 2.'),
       ('Explain why markers use best-fit judgement.', 'Work rarely matches one descriptor exactly; best fit balances strengths and weaknesses to find the most accurate level.'),
       ('Explain why typing the eAssessment affects how students should plan.', 'On-screen writing is easy to edit, so students can restructure, but they must still plan and leave time to proofread.')],
  contrast=[('criterion A', 'criterion C', 'A rewards analysing others\' texts; C rewards producing your own text with insight and imagination.'),
            ('criterion B', 'criterion D', 'B is about structure and organisation; D is about vocabulary, sentences, register and accuracy.')],
  misc=[('Criterion D is only about spelling.', 'Criterion D covers vocabulary range, sentence variety, register, punctuation and grammar.'),
        ('Long answers always score higher.', 'Quality of analysis, organisation and language matters more than length; focused answers often score higher.')],
  apply=[('A student\'s comparison analyses both texts well but has no paragraphs and few connectives. Which criterion is weakest, and what is one target?', 'Criterion B (Organising). Target: use point-by-point paragraphs with comparative topic sentences and connectives.', 2),
         ('Match each to its criterion: (a) a vivid, original idea; (b) accurate semicolons; (c) a clear thesis and logical paragraphs; (d) explaining the effect of a metaphor.', '(a) C; (b) D; (c) B; (d) A.', 4)],
  evaluate=[('Knowing the criteria matters more than practising writing.', ['criteria show what to aim for', 'they help self-assessment'], ['skills improve only through practice', 'criteria without practice are abstract'], 'Knowing the criteria guides practice, but improvement comes from writing, feedback and reflection.')])
pq('ch12-st1', ('C2', 'C3'), (1, 4), LIT | NONLIT | LIFE, 'dev', ['A student wrote: "The writer uses a technique in \'{quote}\'." Using criterion A, explain why this would score low and rewrite it to reach a higher band.'], crit=CRIT_ALL)
K.prompts('ch12-st1', 'interpret', c='C3', d=(2, 4))

H('ch12-st2',
  terms=[('timed comparison', 'writing a comparative analysis of two unseen texts within a fixed time'),
         ('time allocation', 'dividing exam time between reading, annotating, planning, writing and checking'),
         ('comparative thesis', 'a central claim stating the key similarity and difference'),
         ('balanced coverage', 'giving roughly equal attention to both texts')],
  facts=[('In a 60-minute Task 1 comparison, roughly how long should you spend reading and annotating?', 'About 10–15 minutes', ['1 minute', '45 minutes', 'None'], 'Allow time to understand both texts.'),
         ('Which is the best way to begin a timed comparison?', 'An introduction that names both texts and states a comparative thesis', ['A long biography of the authors', 'A summary of Text A only', 'A list of quotations'], 'Thesis first.'),
         ('Why should you leave a few minutes at the end?', 'To proofread and check comparison is sustained', ['To start a new essay', 'To rewrite everything', 'To read a new text'], 'Checking improves accuracy.')],
  why=[('Explain why balanced coverage of both texts matters in Task 1.', 'The task is comparative; focusing on one text weakens analysis and organisation.'),
       ('Explain why planning is especially important under timed conditions.', 'A short plan prevents running out of ideas or time and keeps the essay focused and organised.')],
  contrast=[('a timed response', 'an untimed response', 'A timed response must prioritise key points and efficient structure; an untimed response can explore more detail and be redrafted.')],
  misc=[('In a timed exam you should write as much as possible about everything.', 'Selective, focused analysis of key features in both texts scores better than covering everything superficially.')],
  apply=[('Plan how you would divide 60 minutes for a Task 1 comparative analysis.', 'E.g. 12 minutes reading/annotating both texts; 5 minutes planning thesis and points; 38 minutes writing; 5 minutes proofreading.', 3)],
  evaluate=[('Timed practice is the best preparation for Task 1.', ['builds speed and confidence', 'reveals timing problems'], ['untimed practice develops depth first', 'feedback matters as much'], 'Timed practice is essential near the exam, combined with untimed skill-building and feedback.')])
K.compare('ch12-st2', c='C4', d=(3, 5), frames=['Timed practice (40 minutes). {q} Write a comparative analysis of both texts.',
                                                'Timed practice: spend 10 minutes annotating, then 30 minutes writing. {q}'], marks=None)
K.compare_short('ch12-st2', c=('C2', 'C3'), d=(1, 4))
para('ch12-st2', LIT | NONLIT | LIFE, c=('C3', 'C4'), d=(3, 5), frames=['Timed practice (15 minutes): {gq}', 'In 15 minutes, write one analytical paragraph that answers this question: {gq}'])

H('ch12-st3',
  terms=[('three visual prompts', 'the images offered in Task 2, from which students choose one'),
         ('planning time', 'a few minutes spent choosing a prompt, form, perspective and structure before writing'),
         ('self-assessment', 'judging your own work against criteria B, C and D to identify strengths and targets'),
         ('target', 'a specific, achievable goal for improvement')],
  facts=[('In Task 2, how many visual prompts do you choose from?', 'Three', ['One', 'Five', 'Ten'], 'Students choose one of three images.'),
         ('Which criteria are most relevant to Task 2 creative writing?', 'B, C and D', ['A only', 'A and B only', 'None'], 'Organising, producing text and using language.'),
         ('Which is the most useful target after a Task 2 practice?', '"Vary sentence openings and use at least two short sentences for impact at the climax."', ['"Write better."', '"Be more creative."', '"Use more words."'], 'Specific and actionable.')],
  why=[('Explain why choosing quickly between the three prompts matters.', 'Spending too long choosing reduces writing time; a quick, confident choice with a clear idea is better.'),
       ('Explain why self-assessment after timed writing improves performance.', 'It helps students see what each band requires and set specific targets for the next attempt.')],
  contrast=[('a strength', 'a target', 'A strength is what the writing already does well; a target is a specific improvement for next time.')],
  misc=[('Proofreading is not worth the time in the exam.', 'A few minutes of proofreading can correct errors that would lower criterion D marks.')],
  apply=[('Plan how you would divide 60 minutes for Task 2.', 'E.g. 5 minutes choosing a prompt and brainstorming; 5 minutes planning form, perspective and structure; 40–45 minutes writing; 5 minutes proofreading.', 3),
         ('Write two specific targets for a student whose story has an original idea but a rushed ending and frequent comma splices.', 'E.g. (B) "Plan the ending and give it a full paragraph"; (D) "Use full stops or semicolons between independent clauses."', 2)],
  evaluate=[('Students should prepare a story in advance and adapt it to whichever prompt appears.', ['it reduces stress', 'it ensures a polished piece'], ['responses may not fit the prompt', 'criterion C rewards genuine engagement with the image'], 'Practising techniques is wise, but a memorised story risks irrelevance; it is better to prepare skills and respond freshly to the prompt.')],
  extended=[('Under timed conditions (50 minutes), write a 400–600 word piece inspired by an image of a lit window in an otherwise dark tower block. Then write a short self-assessment against criteria B, C and D.', 'Indicative content: an imaginative interpretation; deliberate form, perspective and structure; varied, accurate language; a self-assessment naming a strength and a target for each criterion. Criteria B, C, D.', 16, 'long')])
K.prompts('ch12-st3', 'write', c='C4', d=(3, 5))
K.prompts('ch12-st3', 'plan', c=('C3', 'C4'), d=(2, 5))
K.prompts('ch12-st3', 'interpret', c=('C2', 'C3'), d=(1, 4))

# --- extra C3 coverage for thinner cells ---
pq('ch07-st3', 'C3', (2, 4), None, 'theme', ['Explain how the central symbol of this extract connects to its theme of {theme}.',
                                            'How does one image in this extract carry meaning beyond its literal sense?'], ids=TR + ['coa_lake', 'dys_tree'], crit=CRIT_OPEN)
pq('ch09-st3', 'C3', (2, 4), None, 'persuade', ['Explain how this text borrows the persuasive techniques of a real advert and turns them against advertising.'], ids=['ad_parody'], crit=CRIT_A)
pq('ch09-st3', 'C3', (2, 4), None, 'aud', AUD_Q, ids=['ad_parody'], crit=CRIT_A)
pq('ch09-st3', 'C3', (2, 4), None, 'purp', PURP_Q, ids=['ad_parody'], crit=CRIT_A)
