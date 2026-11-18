"""IB MYP 4 Language and Literature (English) – ib-g9-english.

MYP 4 has no external exam: school-designed summative tasks are assessed on criteria A Analysing, B Organising,
C Producing text and D Using language (each 0-8). Mocks mirror the MYP 5 on-screen eAssessment: Task 1 analysis
and comparison of two extracts, Task 2 creative writing from visual prompts.

Passages are ORIGINAL unless attributed. Brief public-domain quotations only: Shakespeare (Romeo and Juliet),
Edgar Allan Poe ("The Tell-Tale Heart", 1843), Wilfred Owen (d. 1918), Rupert Brooke (d. 1915), Jessie Pope
("Who's for the game?", 1915), Lewis Carroll and Isaac Watts. Set novels and films are referred to only in general
terms. Shared builders and the shared passage library: ib_myp_english_common.py.
"""
from __future__ import annotations

from _common import F, Registry, T, mcq  # noqa: F401
from ib_myp_english_common import (AUD_Q, CHAR_Q, CRIT_A, CRIT_ALL, CRIT_AN, CRIT_B, CRIT_CR, CRIT_OPEN, CRIT_W, DEV_Q,  # noqa: F401
                                   KCONV_Q, LIFE, LIT, MEDIA, MOOD_Q, NARR, NONLIT, PERSUADE, POV_Q, PROSE, PURP_Q, STRUCT_Q,
                                   STYLE, SUM_Q, THEME_Q, TONE_Q, VIS_Q, VISUAL, Kit, add_shared, mock_sections)

CONFIG = {'minutesPerMark': 1.5, 'mcqMinutes': 1.5}

# MYP 5 eAssessment-style mock: Task 1 analysis 30 marks; Task 2 creative writing (50 on the real paper) scaled to
# 30 because one item may carry at most 20 marks. 6 items, 60 marks per mock.
MOCK = mock_sections(t1_chapters=[11, 4, 1], t2_chapters=[12, 10])

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
# Grade 9 passages
# =============================================================================================
P(id='gothic_house', kind='story', title='opening of a Gothic short story',
  text=("Blackwater Hall had been empty for forty years, yet every night a candle burned in the highest window.\n"
        "I arrived in November, when the trees had given up their leaves and the fog lay on the moor like a shroud. The gates groaned open before I touched them.\n"
        "Inside, the air was colder than the night. Portraits lined the staircase – generations of pale Blackwaters – and every pair of painted eyes was turned, I swear, towards the door.\n"
        "Towards me."),
  gothic='Gothic conventions: an isolated, decaying mansion; a mysterious light in an empty house; a hostile natural setting (fog, bare trees, moor); hints of the supernatural (gates that open by themselves, watching portraits); a first-person narrator whose fear we share.',
  mood='A cold, oppressive and uncanny mood is created by the empty hall, the shroud-like fog, the groaning gates and the portraits whose eyes seem to follow the narrator.',
  uncanny='The familiar becomes strange: painted portraits seem to look at the narrator and gates open without being touched – ordinary objects behave impossibly.',
  dev=[('simile', 'the fog lay on the moor like a shroud', 'a shroud is a cloth wrapped round a corpse, so the simile links the landscape with death and foreshadows horror', ['metaphor', 'onomatopoeia', 'alliteration']),
       ('personification', 'the trees had given up their leaves', 'the trees seem to have surrendered, creating a hopeless, lifeless atmosphere', ['simile', 'hyperbole', 'oxymoron']),
       ('one-line paragraph', 'Towards me.', 'the short fragment isolates the narrator\'s terrifying realisation and ends the opening on a chilling note', ['rhetorical question', 'simile', 'onomatopoeia']),
       ('paradox / mystery', 'had been empty for forty years, yet every night a candle burned', 'the impossible situation hooks the reader with an unanswered question', ['simile', 'statistic', 'onomatopoeia'])],
  struct=[('the opening sentence\'s contradiction', 'it immediately sets up a mystery that drives the reader forward'),
          ('the narrowing focus from the moor to the hall to the portraits to "me"', 'the zoom from landscape to narrator increases claustrophobia and fear')],
  pov='First-person narration ("I swear") makes the reader share the narrator\'s fear, but the insistence "I swear" also hints that the narrator expects not to be believed.',
  tone='ominous', tw=['cheerful', 'comic', 'romantic'], tonex='images of death, cold and watching eyes create a threatening tone.',
  vocab=[('shroud', 'a cloth used to wrap a dead body', ['a thick blanket', 'a type of cloud', 'a cloak worn by a knight'], 'its link with death makes the fog sinister.')],
  theme='the past haunting the present',
  gq='How does the writer create a Gothic atmosphere in this opening?',
  gqa='The writer uses classic Gothic conventions: an isolated, decaying house and a hostile landscape. The simile "like a shroud" links the fog to death, personification ("given up their leaves") creates hopelessness, and supernatural hints (gates opening untouched, portraits\' eyes turned to the door) make the familiar uncanny. Structurally the focus narrows from moor to narrator, ending on the isolated "Towards me." to trap the reader in the narrator\'s fear.',
  write=[('Continue the story (about 300 words): the narrator climbs the staircase towards the lit window. Maintain the Gothic atmosphere.', 'Indicative content: consistent first-person voice; Gothic setting details; sensory description; pacing that slows on the stairs; supernatural hints; a cliffhanger or revelation.')],
  summary='The narrator arrives at Blackwater Hall, empty for forty years but with a candle burning nightly; the gates open by themselves and the portraits seem to watch the door.')

P(id='telltale', kind='story', title='opening of "The Tell-Tale Heart" (1843) by Edgar Allan Poe',
  text=("\"True!—nervous—very, very dreadfully nervous I had been and am; but why will you say that I am mad? The disease had sharpened my senses—not destroyed—not dulled them. Above all was the sense of hearing acute. I heard all things in the heaven and in the earth. I heard many things in hell. How, then, am I mad? Hearken! and observe how healthily—how calmly I can tell you the whole story.\""),
  pov='The first-person narrator is unreliable: he insists he is not mad, yet his frantic dashes, repetitions and claim to hear "things in hell" suggest the opposite. The reader learns to distrust him.',
  unreliable='Clues to unreliability: he protests too much ("why will you say that I am mad?"); his claims are impossible ("I heard all things in the heaven and in the earth"); his broken syntax and dashes contradict his claim to be "calm".',
  gothic='Gothic features: a disturbed mind, a confession, references to hell and the supernatural, and an intense, claustrophobic first-person voice.',
  dev=[('dashes and fragmented syntax', 'True!—nervous—very, very dreadfully nervous', 'the broken rhythm mimics an agitated mind and undermines the narrator\'s claim to sanity', ['simile', 'alliteration', 'onomatopoeia']),
       ('rhetorical question', 'How, then, am I mad?', 'the narrator tries to argue the reader into agreement, but the question reveals his desperation', ['simile', 'statistic', 'personification']),
       ('hyperbole', 'I heard all things in the heaven and in the earth. I heard many things in hell.', 'the impossible claim shows his distorted perception and introduces a supernatural, sinister note', ['simile', 'understatement', 'onomatopoeia']),
       ('direct address', 'Hearken! and observe', 'the narrator speaks directly to "you", making the reader a listener to a confession', ['metaphor', 'oxymoron', 'statistic'])],
  tone='frantic', tw=['calm', 'cheerful', 'detached'], tonex='dashes, exclamations and repetition create a frantic, unstable tone.',
  vocab=[('acute', 'sharp and very sensitive', ['mild', 'painful', 'angled'], 'it shows his belief that his senses are heightened, which later drives the story.'),
         ('Hearken', 'listen (an old-fashioned word)', ['hurry', 'remember', 'look away'])],
  theme='guilt and madness',
  gq='How does Poe present the narrator as unreliable in this opening?',
  gqa='The narrator protests his sanity too strongly: the opening "True!—nervous" and the repeated "very, very dreadfully" use dashes and repetition that mimic agitation. His rhetorical questions ("How, then, am I mad?") try to persuade the reader but reveal desperation, and the hyperbolic claim to hear "things in hell" exposes distorted perception. The direct address "Hearken!" makes us his audience, yet the contrast between his claim of calm and his frantic syntax teaches us not to trust him.',
  summary='The narrator insists he is not mad, claiming his illness has sharpened his senses so that he hears everything, even in hell, and offers to prove his sanity by calmly telling his story.')

P(id='mirror_story', kind='story', title='extract from a Gothic short story told by a teenage narrator',
  text=("My brother says I imagine things. He's probably right. I imagined the scratching behind the wallpaper. I imagined that the mirror in the hall shows the room as it was a hundred years ago – the gas lamps, the dark curtains, the woman in grey.\n"
        "Last night I imagined she turned round.\n"
        "This morning there were wet footprints on the stairs. Small ones. Bare.\n"
        "My brother says I must have walked in my sleep. I didn't tell him that my feet were dry."),
  pov='The first-person narrator seems unreliable at first ("He\'s probably right"), but the final detail – her dry feet – suggests she is telling the truth, so the reader must decide whom to trust.',
  unreliable='The narrator undermines herself by repeating "I imagined", which makes us doubt her; but the physical evidence (wet footprints, her dry feet) contradicts the brother\'s rational explanation.',
  gothic='Gothic features: an old house with secrets, a haunted mirror showing the past, a ghostly woman in grey, unexplained sounds and footprints, and the uncanny blending of past and present.',
  uncanny='The ordinary mirror shows the room as it was a century ago, and a reflection turns round – the familiar household object becomes impossible and threatening.',
  dev=[('repetition with irony', 'I imagined the scratching ... I imagined that the mirror ... Last night I imagined she turned round.', 'the repeated "imagined" seems to dismiss the events, but the growing horror makes the word ironic', ['simile', 'statistic', 'onomatopoeia']),
       ('short fragments', 'Small ones. Bare.', 'the fragments slow the reader and force attention onto each disturbing detail', ['simile', 'hyperbole', 'rhetorical question']),
       ('final twist', 'I didn\'t tell him that my feet were dry.', 'the last line overturns the rational explanation and confirms the supernatural', ['flashback', 'simile', 'alliteration'])],
  tone='quietly menacing', tw=['joyful', 'comic', 'angry'], tonex='calm, understated narration makes the horror creep up on the reader.',
  theme='the past intruding on the present',
  gq='How does the writer use the narrator to create uncertainty and fear?',
  gqa='The narrator undermines herself – "He\'s probably right" and the repeated "I imagined" – so we first doubt her. Yet the details escalate (scratching, the mirror showing the past, the woman turning), and fragments ("Small ones. Bare.") slow the pace. The final line about her dry feet overturns the brother\'s explanation: the "unreliable" narrator may be the only one telling the truth, which is more frightening.',
  summary='A girl who says she imagines things describes a mirror that shows the past and a woman in grey who turns round; wet bare footprints appear, and her own feet were dry.')

P(id='bus_1955', kind='prose', title='extract from a novel set in Alabama in 1955',
  text=("The bus was crowded and hot. Ruth sat in the middle section with her mother, behind the painted line, where coloured passengers were allowed to sit if no white passenger needed the seat.\n"
        "At the third stop a man got on. There was nowhere for him to sit.\n"
        "The driver looked in the mirror. \"Y'all better make it light on yourselves,\" he said.\n"
        "Ruth felt her mother's hand tighten on hers. Three people stood up. Her mother did not.\n"
        "Ruth had never heard silence so loud."),
  context='Historical context: in 1955 Montgomery, Alabama, segregation laws forced Black passengers to give up seats to white passengers; Rosa Parks\'s refusal that December sparked the Montgomery Bus Boycott. The extract shows how ordinary journeys involved daily humiliation and courageous resistance.',
  char='Ruth\'s mother is quietly courageous: she stays seated despite the threat. Ruth is a child observer who senses danger through her mother\'s tightening hand and the "loud" silence.',
  pov='Third-person limited through the child Ruth, so the reader experiences the tension through her senses and partial understanding, which makes the injustice more striking.',
  symbol='The painted line on the bus symbolises segregation – an arbitrary but enforced division between people.',
  dev=[('oxymoron', 'silence so loud', 'the contradiction shows how tense and charged the moment is – everyone is waiting to see what happens', ['simile', 'onomatopoeia', 'alliteration']),
       ('contrast in short sentences', 'Three people stood up. Her mother did not.', 'the short, balanced sentences isolate the mother\'s act of resistance and make it powerful', ['simile', 'hyperbole', 'rhetorical question']),
       ('euphemistic threat', '"Y\'all better make it light on yourselves,"', 'the driver\'s casual phrase hides a threat, showing how injustice was normalised', ['simile', 'statistic', 'personification'])],
  struct=[('ending on Ruth\'s perception of silence', 'the climax is left unresolved, so the reader shares the frozen moment of danger')],
  theme='injustice and quiet resistance',
  gq='How does the writer use a child\'s perspective to present injustice in this extract?',
  gqa='Seen through Ruth, the injustice is shown rather than explained: the "painted line" symbolises segregation, and the driver\'s casual threat reveals how prejudice was normalised. Ruth senses danger physically ("her mother\'s hand tighten"), and the contrast "Three people stood up. Her mother did not." isolates the act of resistance. The oxymoron "silence so loud" captures the tension a child feels but cannot fully name; the historical context of Montgomery in 1955 makes the mother\'s courage resonate with real resistance.',
  summary='In segregated Alabama in 1955, a bus driver orders Black passengers to give up seats for a white man; three stand, but Ruth\'s mother stays seated, and the bus falls silent.')

P(id='soweto_1976', kind='prose', title='extract from a novel set in Soweto, South Africa, in 1976',
  text=("The new rule came on a Monday: half our subjects would now be taught in Afrikaans. Mathematics. Geography. A language most of our teachers barely spoke.\n"
        "Thabo tore the notice from the classroom door. \"They want to teach us in the language of the people who made the pass laws,\" he said.\n"
        "I said nothing. I was fourteen and I wanted to pass my exams.\n"
        "By June I was marching beside him, holding a cardboard sign: WE ARE NOT AFRAID. My hands were shaking so much the letters blurred."),
  context='Historical context: in 1976 the apartheid government ordered that Afrikaans be used to teach some subjects in Black schools; on 16 June 1976 thousands of Soweto students protested, and police opened fire. The extract shows how education became a site of resistance.',
  char='The narrator changes from cautious and self-focused ("I wanted to pass my exams") to politically active, though still frightened (shaking hands). Thabo is defiant and outspoken.',
  pov='First-person retrospective narration lets the reader follow the narrator\'s change of perspective from silence to protest.',
  symbol='The cardboard sign "WE ARE NOT AFRAID" symbolises collective courage, while the narrator\'s shaking hands show that courage exists alongside fear.',
  dev=[('irony', 'WE ARE NOT AFRAID. My hands were shaking so much the letters blurred.', 'the gap between the sign\'s words and his shaking hands shows that courage means acting despite fear', ['simile', 'onomatopoeia', 'alliteration']),
       ('listing in fragments', 'Mathematics. Geography. A language most of our teachers barely spoke.', 'the short fragments stress the shock and absurdity of the new rule', ['simile', 'hyperbole', 'personification'])],
  struct=[('the time jump from Monday to June', 'compressing months into a paragraph break shows how quickly the narrator\'s perspective changes')],
  theme='education, language and resistance',
  gq='How does the writer show the narrator\'s changing perspective?',
  gqa='At first the narrator is passive ("I said nothing") and focused on exams, contrasting with Thabo\'s defiance. The time jump "By June" shows rapid change, and the image of marching with the sign "WE ARE NOT AFRAID" while his hands shake uses irony to show courage alongside fear. The 1976 Soweto context gives the personal change historical weight.',
  summary='When Afrikaans is imposed in their school in 1976, Thabo protests while the narrator stays silent; by June the narrator, frightened but determined, joins the march.')

P(id='newcountry_class', kind='prose', title='extract from a contemporary novel about a refugee student in Berlin',
  text=("On the first day, the teacher wrote my name on the board wrong. Nobody corrected her, so I didn't either.\n"
        "Now, six months later, everyone calls me Sami instead of Samir, and I answer to it like a dog answers to a whistle.\n"
        "In history we studied walls – the Berlin Wall, how it divided families. Lena put up her hand and said, \"At least that's all in the past.\"\n"
        "I thought of my uncle, still on the other side of a border, still waiting. I didn't put up my hand."),
  char='Samir is quiet, observant and wounded: he accepts the wrong name to fit in but feels diminished ("like a dog answers to a whistle"), and he keeps his painful knowledge to himself.',
  pov='First-person narration reveals Samir\'s private thoughts that classmates never hear, creating dramatic irony when Lena says divisions are "in the past".',
  symbol='Walls and borders recur as a motif: the Berlin Wall in the lesson echoes the border that still separates Samir from his uncle, connecting history to the present.',
  context='Contemporary context: Germany received many refugees in the 2010s; the setting in Berlin, a city once divided by a wall, makes the theme of borders especially resonant.',
  dev=[('simile', 'like a dog answers to a whistle', 'the degrading comparison shows how the mispronounced name makes him feel controlled and less than human', ['metaphor', 'onomatopoeia', 'alliteration']),
       ('dramatic irony', '"At least that\'s all in the past."', 'the reader knows Samir\'s family is still divided, so Lena\'s innocent comment is painfully wrong', ['simile', 'statistic', 'hyperbole']),
       ('parallel endings', 'Nobody corrected her, so I didn\'t either. ... I didn\'t put up my hand.', 'the repeated silence frames the extract and shows Samir hiding his identity and pain', ['simile', 'personification', 'onomatopoeia'])],
  theme='identity, belonging and the persistence of borders',
  gq='How does the writer present Samir\'s experience of belonging and not belonging?',
  gqa='Samir\'s acceptance of the wrong name shows a desire to fit in, but the simile "like a dog answers to a whistle" reveals the cost to his identity. The motif of walls connects the Berlin Wall lesson to his uncle\'s border, and Lena\'s comment creates dramatic irony. The repeated silences frame the extract, showing that he belongs on the surface but keeps his real self hidden.',
  summary='Samir, a refugee student in Berlin, accepts a wrong version of his name; when a classmate says divided families are in the past, he thinks of his uncle stuck at a border and says nothing.')

P(id='rj_prologue', kind='drama', title='extract from the Prologue of Romeo and Juliet by William Shakespeare (c. 1595)',
  text=("CHORUS:\nTwo households, both alike in dignity,\n"
        "In fair Verona, where we lay our scene,\n"
        "From ancient grudge break to new mutiny,\n"
        "Where civil blood makes civil hands unclean.\n"
        "From forth the fatal loins of these two foes\n"
        "A pair of star-cross'd lovers take their life;"),
  shakes='The Prologue is a sonnet (14 lines of iambic pentameter rhyming ABAB CDCD EFEF GG) spoken by the Chorus. It tells the audience the outcome in advance, creating dramatic irony: we watch the lovers knowing they will die.',
  context='Elizabethan audiences believed in fate and the influence of the stars; "star-cross\'d" suggests the lovers are doomed by destiny. Plays were performed at open-air theatres such as the Globe, where the Chorus would address a mixed audience directly.',
  dev=[('oxymoron / wordplay', 'civil blood makes civil hands unclean', '"civil" means both "of citizens" and "polite", so the repetition shows how a civilised city is stained by violence', ['simile', 'onomatopoeia', 'personification']),
       ('compound adjective / imagery of fate', 'star-cross\'d lovers', 'it suggests the stars (fate) are against the lovers, foreshadowing tragedy', ['onomatopoeia', 'simile', 'hyperbole']),
       ('alliteration', 'From forth the fatal loins of these two foes', 'the repeated "f" sounds stress fate and enmity, making the line ominous', ['assonance', 'onomatopoeia', 'simile'])],
  metre='The lines are in iambic pentameter: five pairs of unstressed-stressed syllables ("Two HOUSE-holds, BOTH a-LIKE in DIG-ni-TY"), giving a formal, rhythmic voice suited to a Chorus introducing a tragedy.',
  struct=[('revealing the ending in the Prologue', 'it creates dramatic irony and shifts the audience\'s interest from what happens to how and why it happens')],
  tone='solemn and foreboding', tw=['playful', 'sarcastic', 'joyful'], tonex='words like "grudge", "blood" and "fatal" create a solemn, ominous tone.',
  theme='fate, conflict and love',
  gq='How does Shakespeare use the Prologue to prepare the audience for a tragedy?',
  gqa='The Prologue is a formal sonnet in iambic pentameter spoken by the Chorus, which signals a serious, structured story. It reveals the outcome, creating dramatic irony. Wordplay on "civil" shows violence corrupting a civilised city, alliteration in "fatal ... foes" stresses doom, and "star-cross\'d lovers" draws on Elizabethan beliefs about fate, telling the audience the lovers are destined to die.',
  summary='The Chorus tells the audience that two equally respected families in Verona have an old feud that has turned violent, and that a pair of doomed lovers will be born from them.')

P(id='rj_balcony', kind='drama', title='extract from Act 2 Scene 2 of Romeo and Juliet by William Shakespeare',
  text=("ROMEO:\nBut, soft! what light through yonder window breaks?\n"
        "It is the east, and Juliet is the sun.\n"
        "Arise, fair sun, and kill the envious moon,\n"
        "Who is already sick and pale with grief,\n"
        "That thou her maid art far more fair than she:"),
  shakes='Romeo speaks in blank verse (unrhymed iambic pentameter), the form Shakespeare uses for noble characters and serious emotion; here it gives his feelings an elevated, poetic quality.',
  context='Elizabethan audiences would recognise the conventions of love poetry (praising a beloved with images of light and heavenly bodies). The scene was staged in daylight at the Globe, so the language had to create the night and the light of Juliet.',
  dev=[('metaphor', 'Juliet is the sun', 'Romeo presents Juliet as the centre of his world, a source of light and warmth', ['simile', 'onomatopoeia', 'oxymoron']),
       ('personification', 'kill the envious moon, / Who is already sick and pale with grief', 'the moon is jealous of Juliet\'s beauty, which exaggerates her radiance', ['simile', 'alliteration', 'pun']),
       ('rhetorical question', 'what light through yonder window breaks?', 'it creates wonder and draws the audience\'s attention to Juliet\'s appearance', ['simile', 'statistic', 'pun'])],
  metre='Blank verse – unrhymed iambic pentameter ("It IS the EAST, and JU-liet IS the SUN") – gives Romeo\'s speech a dignified, heartbeat-like rhythm.',
  irony='Dramatic irony: the audience knows from the Prologue that this love will end in death, so Romeo\'s images of light and life are poignant.',
  tone='adoring', tw=['bitter', 'mocking', 'fearful'], tonex='images of light and heavenly beauty create an adoring tone.',
  theme='love and light',
  gq='How does Shakespeare use imagery to present Romeo\'s feelings for Juliet?',
  gqa='The extended metaphor of Juliet as the sun ("It is the east, and Juliet is the sun") presents her as the centre of Romeo\'s world. Personification of the "envious moon ... sick and pale with grief" exaggerates her beauty, and the rhetorical question creates wonder. Blank verse elevates his emotion, and the audience\'s knowledge of the tragic ending (dramatic irony) makes the imagery of light and life poignant.',
  summary='Romeo sees Juliet at her window and compares her to the sun rising, saying she outshines the jealous moon.')

P(id='rj_fight', kind='drama', title='extract from Act 3 Scene 1 of Romeo and Juliet by William Shakespeare',
  text=("(TYBALT, under ROMEO's arm, stabs MERCUTIO, and flies with his followers.)\n"
        "MERCUTIO: I am hurt.\nA plague o' both your houses! I am sped.\n"
        "ROMEO: Courage, man; the hurt cannot be much.\n"
        "MERCUTIO: No, 'tis not so deep as a well, nor so wide as a church-door; but 'tis enough, 'twill serve: ask for me to-morrow, and you shall find me a grave man."),
  shakes='This is the play\'s turning point: Mercutio\'s death turns the comedy-like first half into tragedy, leading Romeo to kill Tybalt and be banished. Mercutio speaks in prose rather than verse, matching his witty, informal character.',
  context='Elizabethan audiences enjoyed sword fights on stage; the line "A plague o\' both your houses!" would have had extra force at a time when outbreaks of plague often closed London\'s theatres.',
  dev=[('pun', 'you shall find me a grave man', '"grave" means both "serious" and "in a grave", so Mercutio jokes even as he dies, which makes his death more shocking and poignant', ['simile', 'alliteration', 'metaphor']),
       ('curse / repetition', 'A plague o\' both your houses!', 'Mercutio blames both families, and the curse foreshadows the tragedy that follows', ['simile', 'onomatopoeia', 'oxymoron']),
       ('dramatic irony', 'Courage, man; the hurt cannot be much.', 'the audience, and Mercutio, know the wound is fatal while Romeo does not, increasing the tension', ['metaphor', 'pun', 'alliteration'])],
  struct=[('Mercutio\'s death at the centre of the play', 'it is the turning point (peripeteia) that shifts the play from romance to tragedy')],
  irony='Romeo\'s reassurance that "the hurt cannot be much" is dramatically ironic, because Mercutio knows he is dying.',
  tone='darkly witty', tw=['joyful', 'calm', 'romantic'], tonex='Mercutio\'s jokes in the face of death mix humour with bitterness.',
  theme='violence and the consequences of the feud',
  gq='How does Shakespeare make Mercutio\'s death a turning point in the play?',
  gqa='The stage direction shows Tybalt striking "under Romeo\'s arm", so Romeo\'s attempt at peace causes the death. Mercutio\'s curse "A plague o\' both your houses!" blames both families and foreshadows tragedy. His dying pun ("a grave man") keeps his wit to the end, making the loss poignant. Romeo\'s ironic reassurance increases tension, and the death drives Romeo to revenge, turning the play from romance to tragedy.',
  summary='Tybalt stabs Mercutio under Romeo\'s arm; Mercutio curses both families and jokes that tomorrow he will be "a grave man" before dying.')

P(id='owen_dulce', kind='poem', title='opening of "Dulce et Decorum Est" by Wilfred Owen (written 1917, published 1920)',
  text=("Bent double, like old beggars under sacks,\n"
        "Knock-kneed, coughing like hags, we cursed through sludge,\n"
        "Till on the haunting flares we turned our backs,\n"
        "And towards our distant rest began to trudge.\n"
        "Men marched asleep. Many had lost their boots,\n"
        "But limped on, blood-shod. All went lame; all blind;"),
  context='Owen was a British officer who fought on the Western Front and was killed in November 1918. He wrote to expose the reality of trench warfare and to challenge patriotic propaganda; the title quotes the Latin poet Horace: "it is sweet and fitting [to die for one\'s country]".',
  persp='Protest: Owen presents war from the soldier\'s point of view as degrading, exhausting and inhuman, directly contradicting the heroic images of propaganda.',
  dev=[('simile', 'like old beggars under sacks', 'young soldiers are compared to old beggars, showing how war has stripped them of youth, strength and dignity', ['metaphor', 'onomatopoeia', 'personification']),
       ('simile', 'coughing like hags', 'the comparison to old women shows how illness and gas have destroyed the men\'s health', ['metaphor', 'alliteration', 'hyperbole']),
       ('compound adjective / metaphor', 'blood-shod', 'instead of shoes, the soldiers\' feet are covered in blood, a shocking image of suffering', ['simile', 'onomatopoeia', 'pun']),
       ('hyperbole', 'All went lame; all blind', 'the exaggeration stresses total exhaustion and the loss of control', ['simile', 'personification', 'onomatopoeia'])],
  struct=[('the slow, heavy rhythm and caesuras (e.g. "Men marched asleep. Many had lost their boots,")', 'the pauses mid-line slow the reader down, mimicking the soldiers\' exhausted trudge')],
  tone='bitter and grim', tw=['patriotic', 'cheerful', 'romantic'], tonex='degrading images of soldiers create a bitter, grim tone.',
  theme='the reality of war versus propaganda',
  gq='How does Owen use imagery to present the reality of war in this opening?',
  gqa='Owen presents soldiers not as heroes but as broken men: the similes "like old beggars under sacks" and "coughing like hags" age and degrade them, and "blood-shod" replaces boots with blood. Hyperbole ("All went lame; all blind") stresses total exhaustion, and the heavy rhythm with caesuras mimics their trudge. Written from a soldier\'s perspective, the imagery protests against the heroic language of propaganda.',
  summary='Owen describes exhausted soldiers leaving the front line, bent like old beggars, coughing, bootless and bleeding, marching half-asleep towards rest.')

P(id='owen_anthem', kind='poem', title='opening of "Anthem for Doomed Youth" by Wilfred Owen (1917)',
  text=("What passing-bells for these who die as cattle?\n"
        "— Only the monstrous anger of the guns.\n"
        "Only the stuttering rifles' rapid rattle\n"
        "Can patter out their hasty orisons."),
  context='Written in 1917 while Owen was recovering at Craiglockhart hospital, the poem contrasts the funerals soldiers deserve with the anonymous deaths of the Western Front. It is a sonnet, a form traditionally used for love poetry, here turned to grief.',
  persp='Protest and mourning: Owen suggests that soldiers are slaughtered without dignity and that the only "funeral" they get is the noise of the guns.',
  dev=[('rhetorical question', 'What passing-bells for these who die as cattle?', 'the question challenges the reader and suggests soldiers receive no proper funeral', ['simile', 'statistic', 'pun']),
       ('simile', 'who die as cattle', 'comparing soldiers to animals in a slaughterhouse shows that their deaths are mass, anonymous and undignified', ['metaphor', 'personification', 'hyperbole']),
       ('onomatopoeia and alliteration', 'stuttering rifles\' rapid rattle', 'the repeated "r" and "t" sounds imitate machine-gun fire, replacing funeral prayers with noise', ['simile', 'oxymoron', 'pun']),
       ('personification', 'the monstrous anger of the guns', 'the guns become furious monsters, showing the inhuman power of modern weapons', ['simile', 'statistic', 'onomatopoeia'])],
  form='It is a sonnet (14 lines), a form usually associated with love; Owen uses it ironically to mourn.',
  tone='angry and mournful', tw=['joyful', 'patriotic', 'playful'], tonex='bitter questions and harsh sounds express anger and grief.',
  theme='death without dignity in war',
  summary='Owen asks what funeral bells there are for soldiers who die like cattle, answering that only the guns and rifles "pray" for them.')

P(id='pope_game', kind='poem', title='opening of "Who\'s for the Game?" by Jessie Pope (1915)',
  text=("Who's for the game, the biggest that's played,\n"
        "The red crashing game of a fight?\n"
        "Who'll grip and tackle the job unafraid?\n"
        "And who thinks he'd rather sit tight?"),
  context='Jessie Pope wrote patriotic recruiting verse for British newspapers early in the First World War, when the army relied on volunteers. Owen originally addressed "Dulce et Decorum Est" to her as a reply.',
  persp='Propaganda: war is presented as an exciting sport ("the game"), and young men who do not volunteer are shamed as cowards.',
  dev=[('extended metaphor', 'Who\'s for the game, the biggest that\'s played', 'presenting war as a sporting game makes it seem fun, heroic and safe', ['simile', 'onomatopoeia', 'personification']),
       ('rhetorical questions', 'Who\'ll grip and tackle the job unafraid? / And who thinks he\'d rather sit tight?', 'the questions put pressure on readers, implying that real men volunteer and cowards stay home', ['statistic', 'simile', 'hyperbole']),
       ('euphemism', 'The red crashing game of a fight', 'violent death is softened into a colourful, noisy game', ['statistic', 'pun', 'oxymoron'])],
  struct=[('the bouncy, regular rhythm and rhyme (played/unafraid; fight/tight)', 'the jaunty, song-like form makes war sound cheerful and easy to remember')],
  tone='cheerful and challenging', tw=['mournful', 'bitter', 'despairing'], tonex='the jaunty rhythm and sporting language make war sound exciting.',
  theme='patriotism and pressure to fight',
  summary='Pope asks young men who will join "the game" of war, presenting it as exciting sport and implying that those who stay at home are cowards.')

P(id='brooke_soldier', kind='poem', title='opening of "The Soldier" by Rupert Brooke (1914)',
  text=("If I should die, think only this of me:\n"
        "That there's some corner of a foreign field\n"
        "That is for ever England. There shall be\n"
        "In that rich earth a richer dust concealed;"),
  context='Brooke wrote the sonnet at the start of the war, before the full horror of the trenches was known; he died in 1915 on the way to Gallipoli. The poem was widely used to encourage patriotic feeling.',
  persp='Patriotic idealism: death abroad is presented as noble and peaceful – the soldier\'s body makes foreign soil part of England.',
  dev=[('euphemism', 'If I should die', 'the conditional softens death and makes it seem calm and acceptable', ['simile', 'onomatopoeia', 'hyperbole']),
       ('metaphor', 'some corner of a foreign field / That is for ever England', 'the soldier\'s grave turns foreign land into England, presenting death as a gift to the nation', ['simile', 'personification', 'onomatopoeia']),
       ('comparative / wordplay', 'In that rich earth a richer dust concealed', 'the body (dust) is "richer" than the soil because it is English, showing pride and idealism', ['simile', 'oxymoron', 'onomatopoeia'])],
  form='It is a sonnet, a form linked with love, used here to express love of country.',
  tone='calm and patriotic', tw=['bitter', 'horrified', 'sarcastic'], tonex='gentle, idealised language makes death peaceful and noble.',
  theme='patriotism and sacrifice',
  summary='Brooke\'s speaker asks to be remembered as making a corner of foreign land "for ever England" if he dies, because his English body enriches the earth.')

P(id='daddy_poster', kind='propaganda', title='First World War recruitment poster (Britain, 1915), described in words',
  text=("[Image: a comfortable armchair in a home after the war. A father sits looking uneasy and guilty. His small daughter, on his lap, points to a history book; his son plays with toy soldiers on the floor.]\n"
        "[Caption in large letters: \"Daddy, what did YOU do in the Great War?\"]"),
  persp='Propaganda: the poster uses guilt and shame to pressure men to enlist, imagining a future in which their children judge them.',
  aud='British men of fighting age in 1915, especially fathers who had not yet volunteered.',
  purp='To persuade men to enlist by making them imagine future shame in front of their children.',
  visual='The father\'s guilty expression and averted gaze, the innocent daughter\'s pointing finger and the son\'s toy soldiers (playing at the war his father avoided) create emotional pressure; the domestic setting brings the war into the home.',
  dev=[('rhetorical question', '"Daddy, what did YOU do in the Great War?"', 'the child\'s question forces the viewer to imagine having no proud answer', ['statistic', 'simile', 'onomatopoeia']),
       ('emphasis (capitalised pronoun)', 'YOU', 'the capitals point directly at the viewer, making the accusation personal', ['simile', 'personification', 'alliteration'])],
  tone='accusing', tw=['celebratory', 'humorous', 'neutral'], tonex='the child\'s innocent question becomes a pointed accusation.',
  gq='How does the poster use image and language to persuade men to enlist?',
  gqa='The poster imagines a peaceful future: a child\'s innocent rhetorical question, with the capitalised "YOU", makes the viewer the accused. The father\'s guilty, averted gaze models the shame the viewer should fear, the son\'s toy soldiers show the war becoming a heroic story, and the domestic setting turns family love into pressure. It manipulates emotion (guilt, pride) rather than giving information.',
  summary='The poster shows a guilty-looking father whose daughter asks what he did in the Great War, implying that men who do not enlist will be ashamed in front of their children.')

P(id='screen_rain', kind='script', title='extract from an original film script',
  text=("EXT. MUMBAI ROOFTOP – NIGHT\n"
        "Rain lashes the concrete. Neon signs bleed colour into puddles.\n"
        "CLOSE-UP: ARJUN (16), soaked, clutching a crumpled acceptance letter.\n"
        "WIDE SHOT: the city stretches to the horizon; Arjun is tiny at the edge of the roof.\n"
        "SOUND: traffic below fades. Only rain. Then – his phone buzzes.\n"
        "INSERT – PHONE SCREEN: \"Dad: Come home. We'll talk.\"\n"
        "Arjun looks at the letter, then at the city. Slowly, he folds the letter into his pocket.\n"
        "CUT TO BLACK."),
  film='Camera: the close-up on the letter shows its importance to Arjun; the wide shot makes him tiny against the vast city, showing how small and alone he feels; the insert shot puts the father\'s message in front of the audience. Sound: the fading traffic leaves only rain, isolating Arjun; the buzz breaks the silence. Editing: the cut to black ends on suspense.',
  mise='Mise-en-scène: night, rain and neon "bleeding" colour create a melancholy but beautiful atmosphere; Arjun is soaked and at the roof\'s edge, which suggests vulnerability and a turning point.',
  dev=[('close-up', 'CLOSE-UP: ARJUN (16), soaked, clutching a crumpled acceptance letter.', 'it focuses the audience on the letter and Arjun\'s emotion, signalling that the letter matters', ['wide shot', 'tracking shot', 'aerial shot']),
       ('wide shot', 'WIDE SHOT: the city stretches to the horizon; Arjun is tiny', 'the contrast in scale shows his isolation and the size of his decision', ['close-up', 'over-the-shoulder shot', 'insert']),
       ('sound bridge / silence', 'traffic below fades. Only rain. Then – his phone buzzes.', 'removing background noise isolates Arjun, so the buzz becomes startling and important', ['montage', 'voice-over', 'flashback'])],
  struct=[('ending with "CUT TO BLACK"', 'the abrupt end leaves the decision unresolved, creating suspense and inviting interpretation')],
  theme='family conflict and ambition',
  gq='How does the script use camera and sound to present Arjun\'s situation?',
  gqa='The close-up on the crumpled acceptance letter tells us it is central, while the wide shot shrinks Arjun against the city, showing isolation. Sound narrows from traffic to rain, so the phone\'s buzz is startling; the insert shot reveals the father\'s message. Mise-en-scène (rain, neon "bleeding" into puddles, the roof\'s edge) creates a melancholy, tense mood, and the cut to black leaves his choice unresolved.',
  summary='On a rainy Mumbai rooftop, Arjun holds an acceptance letter; his father texts asking him to come home to talk, and Arjun puts the letter in his pocket before the scene cuts to black.')

P(id='trailer', kind='script', title='description of a horror film trailer',
  text=("0:00 – Black screen. A child's music box plays slowly.\n"
        "0:05 – Bright, sunny shots: a family moves into a farmhouse. Upbeat guitar.\n"
        "0:15 – The music box again, louder. Quick cuts: a door swinging shut; a shadow on the stairs; the daughter staring at a wall.\n"
        "0:25 – Silence. Close-up: the daughter turns to camera. \"She says we can stay... if we're quiet.\"\n"
        "0:28 – A crash of sound. Title: HUSH. In cinemas October."),
  film='Editing moves from slow, sunny shots to rapid quick cuts, increasing pace and anxiety. Sound shifts from upbeat guitar to a distorted music box, then sudden silence and a crash (a jump scare). The close-up of the daughter speaking to camera breaks the fourth wall and unsettles the viewer.',
  genre='Horror conventions: an isolated house, a creepy child, a music box, shadows, silence before a jump scare; the trailer raises questions (who is "she"?) without answering them, to make audiences want to see the film.',
  aud='Teenagers and adults who enjoy horror films; the October release date links to Halloween.',
  dev=[('contrast in sound', 'A child\'s music box plays slowly ... Upbeat guitar', 'the innocent sounds become sinister by contrast, building unease', ['voice-over', 'montage', 'aerial shot']),
       ('quick cuts', 'Quick cuts: a door swinging shut; a shadow on the stairs', 'rapid editing increases the pace and makes the viewer anxious', ['long take', 'slow motion', 'freeze frame']),
       ('direct address to camera', 'the daughter turns to camera', 'breaking the fourth wall makes the audience feel watched and implicated', ['tracking shot', 'wide shot', 'cross-cutting'])],
  struct=[('the movement from calm to chaos', 'the trailer sets up normality and then disrupts it, mirroring a horror plot and building to a jump scare')],
  gq='How does the trailer use sound and editing to attract its target audience?',
  gqa='The trailer begins with innocent sounds (a music box, upbeat guitar) and sunny shots, then corrupts them: the music box returns louder over quick cuts of shadows and doors, increasing pace and anxiety. Sudden silence and the daughter\'s direct address to camera unsettle the viewer, and a crash creates a jump scare. Horror conventions and an unanswered question ("She says...") hook horror fans, and the October date ties it to Halloween.',
  summary='The trailer moves from a happy family moving into a farmhouse to creepy music, shadows and a daughter warning that "she" lets them stay if they are quiet, ending with a crash and the title.')

P(id='filmreview', kind='review', title='film review on a student film blog',
  text=("Tidewater (12A) ★★★★☆\n"
        "Director Ana Moreno's debut follows two sisters in a Chilean fishing village as the sea swallows their town, house by house.\n"
        "The cinematography is breathtaking: long, wide shots of grey water make the people look painfully small, while handheld close-ups during the storm put you right in the boat.\n"
        "The script stumbles in the middle – a romance subplot goes nowhere – but the final ten minutes, almost silent, left our whole row in tears.\n"
        "Verdict: a quiet film about a loud problem. Bring tissues."),
  aud='Students and young film fans who read a film blog; the age rating and casual verdict ("Bring tissues") suit them.',
  purp='To evaluate the film and recommend it, while giving a balanced view of strengths and weaknesses.',
  dev=[('technical film vocabulary', 'long, wide shots ... handheld close-ups', 'precise terms show the reviewer\'s expertise and explain how the film creates its effects', ['simile', 'onomatopoeia', 'rhetorical question']),
       ('antithesis', 'a quiet film about a loud problem', 'the paradox sums up the film\'s style and its urgent subject memorably', ['simile', 'onomatopoeia', 'statistic']),
       ('personal response', 'left our whole row in tears', 'the reaction of real viewers is evidence of the film\'s emotional power', ['statistic', 'pun', 'alliteration'])],
  struct=[('the rating, summary, strengths, weakness and verdict', 'the conventional structure of a review gives a quick judgement and then justifies it')],
  tone='admiring but balanced', tw=['hostile', 'indifferent', 'sarcastic'], tonex='enthusiastic praise is tempered by honest criticism.',
  gq='How does the reviewer make the review informative and persuasive?',
  gqa='The star rating and verdict give a quick judgement, and the spoiler-free summary informs. Technical vocabulary (wide shots, handheld close-ups) explains how the film creates effects and builds the reviewer\'s credibility. Honest criticism of the subplot adds balance, while personal response ("our whole row in tears") and the antithetical verdict persuade readers to watch.',
  write=[('Write a review (about 300 words) of a film you have seen recently, using film vocabulary to explain at least two techniques.', 'Indicative content: rating; spoiler-free summary; analysis of camera, sound or mise-en-scène with film terms; one weakness; personal response; verdict for a specific audience.')],
  summary='The reviewer praises Tidewater, about two sisters in a Chilean village swallowed by the sea, for its cinematography and moving ending, though the middle romance subplot is weak.')

P(id='oped_vote16', kind='oped', title='opinion column in a youth news magazine',
  text=("Let Us Vote at 16\n"
        "At 16 I can work, pay tax on my wages and, in some countries, join the army. But I can't vote for the people who decide how that tax is spent.\n"
        "Critics say teenagers are too immature. Yet Austria has let 16-year-olds vote in national elections since 2007, and studies there found young voters were just as informed as older first-time voters.\n"
        "Climate, housing, education – the decisions made today will shape our lives for longer than anyone's.\n"
        "We are not asking for a favour. We are asking for a voice."),
  claim='Claim: the voting age should be lowered to 16. Evidence: 16-year-olds can work and pay tax; Austria\'s experience since 2007 suggests young voters are well informed. Counterargument: critics say teenagers are immature. Rebuttal: the Austrian studies, and the point that young people will live longest with today\'s decisions.',
  aud='Young readers and adults who influence policy; the magazine is aimed at young people, but the argument also addresses critics.',
  purp='To persuade readers that 16-year-olds should be allowed to vote.',
  dev=[('logos (evidence)', 'Austria has let 16-year-olds vote in national elections since 2007', 'a real example provides evidence that the policy works', ['pathos', 'ethos', 'hyperbole']),
       ('ethos (personal authority)', 'At 16 I can work, pay tax', 'speaking from experience as a 16-year-old gives the writer credibility', ['logos', 'statistic', 'simile']),
       ('counterargument and rebuttal', 'Critics say teenagers are too immature. Yet...', 'acknowledging and answering the main objection makes the argument fair and stronger', ['simile', 'onomatopoeia', 'alliteration']),
       ('antithesis', 'We are not asking for a favour. We are asking for a voice.', 'the parallel contrast reframes voting as a right, ending memorably', ['simile', 'statistic', 'personification'])],
  struct=[('claim – evidence – counterargument – rebuttal – conclusion', 'the classic argument structure makes the reasoning clear and persuasive')],
  tone='confident and reasonable', tw=['hysterical', 'comic', 'resigned'], tonex='calm evidence and a firm conclusion create confidence.',
  gq='How does the writer construct a persuasive argument for votes at 16?',
  gqa='The writer opens with an appeal to fairness and personal ethos (working and paying tax at 16). The counterargument about immaturity is rebutted with logos – Austria\'s experience since 2007 – and the tricolon "Climate, housing, education" stresses what is at stake. The antithesis "not asking for a favour ... asking for a voice" reframes voting as a right.',
  write=[('Write a response column (about 300 words) arguing that the voting age should stay at 18, addressing at least two of this writer\'s points.', 'Indicative content: clear claim; evidence (e.g. brain development, political pressure on young people); counterargument (acknowledge Austria) and rebuttal; rhetorical appeals; conclusion.')],
  summary='The writer argues that 16-year-olds should vote because they can work and pay tax, Austria\'s example shows they are well informed, and they will live longest with today\'s decisions.')

P(id='oped_homework', kind='oped', title='opinion column by a teacher in a school newsletter',
  text=("Less Homework, Better Learning?\n"
        "I have set homework for twenty years. I now think I set too much.\n"
        "Research from several countries suggests that, for students your age, the benefits of homework level off after about an hour or two a night. Beyond that, sleep, exercise and family time matter more.\n"
        "Some parents worry that less homework means lower standards. I understand. But a tired student who copies answers at midnight learns nothing.\n"
        "So this term, my classes will get less homework – and better homework."),
  claim='Claim: students should get less but better homework. Evidence: research showing benefits level off after one to two hours. Counterargument: parents fear lower standards. Rebuttal: an exhausted student copying answers learns nothing.',
  aud='Students and parents reading the school newsletter.',
  purp='To persuade readers that reducing homework can improve learning, and to explain the writer\'s new policy.',
  dev=[('ethos (experience and honesty)', 'I have set homework for twenty years. I now think I set too much.', 'admitting a change of mind after long experience makes the writer credible and honest', ['logos', 'statistic', 'simile']),
       ('logos', 'the benefits of homework level off after about an hour or two a night', 'research evidence supports the claim logically', ['pathos', 'hyperbole', 'simile']),
       ('pathos (emotive image)', 'a tired student who copies answers at midnight learns nothing', 'the vivid image appeals to the reader\'s sympathy and common sense', ['statistic', 'pun', 'oxymoron'])],
  tone='thoughtful and reasonable', tw=['angry', 'mocking', 'despairing'], tonex='honest reflection and calm evidence create a reasonable tone.',
  summary='A teacher argues that research shows homework benefits level off after one to two hours, so his classes will get less but better homework, despite some parents\' worries.')

P(id='story_seoul', kind='story', title='extract from a short story set in Seoul',
  text=("At 11 p.m. the hagwon let us out. The street was bright as noon with study cafés and convenience stores. My mother was waiting in the car with a kimbap roll and the question she asks every night: \"How did you do?\"\n"
        "\"Ninety-two,\" I said.\n"
        "She smiled, but I saw her eyes go to the number on Ji-woo's mother's car sticker: SEOUL NATIONAL UNIVERSITY.\n"
        "I ate the kimbap. It tasted of seaweed and expectation."),
  culture='Cultural setting: the story reflects the intense academic competition in South Korea, where many students attend hagwon (private cram schools) late into the night to prepare for university entrance; family honour and parental sacrifice are linked to results.',
  pov='First-person narration by the student lets readers feel the pressure from inside – the narrator notices her mother\'s glance and silently interprets it.',
  identity='The narrator\'s identity is shaped by her family\'s expectations and her culture\'s focus on success; her score becomes part of who she is.',
  dev=[('simile', 'bright as noon', 'the late-night street lit like daytime shows how study dominates life, even at night', ['metaphor', 'personification', 'onomatopoeia']),
       ('zeugma / unusual pairing', 'It tasted of seaweed and expectation.', 'joining a real taste with an abstract feeling shows that even food is flavoured by pressure', ['simile', 'onomatopoeia', 'alliteration']),
       ('symbol', 'the number on Ji-woo\'s mother\'s car sticker: SEOUL NATIONAL UNIVERSITY', 'the sticker symbolises status and comparison between families', ['simile', 'hyperbole', 'rhetorical question'])],
  theme='pressure, family and success',
  gq='How does the writer present the pressure on the narrator?',
  gqa='The cultural setting – hagwon finishing at 11 p.m., a street "bright as noon" – shows study dominating life. The mother\'s nightly question and her glance at the university sticker reveal comparison, interpreted silently by the first-person narrator. The final line "It tasted of seaweed and expectation" turns even a caring act (bringing food) into a reminder of pressure.',
  summary='After cram school at 11 p.m., a student tells her mother she scored 92; her mother smiles but glances at another family\'s university sticker, and the kimbap tastes of expectation.')

P(id='story_market_oaxaca', kind='story', title='extract from a short story set in Oaxaca, Mexico, told in the second person',
  text=("You wake before the roosters because your grandmother is already grinding corn. You help her carry the baskets to the market, past the church and the bakery where Don Félix waves with floury hands.\n"
        "You speak Zapotec with her and Spanish with the customers and English with the tourists who ask to take your photo.\n"
        "By noon you are three people. On the bus home, your grandmother falls asleep on your shoulder, and you are only one: hers."),
  culture='Cultural setting: a market in Oaxaca with Zapotec traditions (grinding corn by hand, Indigenous language) meeting Spanish-speaking customers and international tourists.',
  pov='Second-person narration ("you") places the reader inside the narrator\'s life, making the experience immediate and inviting us to imagine living between three languages.',
  identity='The narrator moves between languages and roles – "By noon you are three people" – but feels most herself in her bond with her grandmother: "you are only one: hers."',
  dev=[('second-person narration', 'You wake before the roosters', 'it makes the reader experience the routine as if it were their own', ['first-person narration', 'omniscient narration', 'dramatic monologue']),
       ('tricolon / listing of languages', 'Zapotec with her and Spanish with the customers and English with the tourists', 'the list shows the narrator switching identities across the day', ['simile', 'onomatopoeia', 'oxymoron']),
       ('metaphor', 'By noon you are three people.', 'the narrator\'s different languages become different selves, showing a divided identity', ['simile', 'statistic', 'personification'])],
  theme='identity and belonging across languages',
  gq='How does the writer use second-person narration to explore identity?',
  gqa='Second-person narration makes the reader live the narrator\'s day. The list of three languages shows her shifting between identities, and the metaphor "By noon you are three people" captures the strain of switching. The ending contrasts this with "you are only one: hers", suggesting that her truest identity lies in her family and Zapotec heritage.',
  summary='A girl helps her grandmother at a market in Oaxaca, speaking Zapotec, Spanish and English; she feels like three people, but on the bus home she is simply her grandmother\'s.')

P(id='story_lagos_rain', kind='story', title='extract from a short story set in Lagos',
  text=("When the rains came, Mama said the city became honest. 'Lagos cannot hide her potholes under water,' she said, 'and people cannot hide their hearts under umbrellas.'\n"
        "That evening the road outside our compound turned into a brown river. Mr Adeyemi from next door, who had not spoken to us since the argument about the generator, waded across carrying a sack of rice above his head.\n"
        "'Your roof is leaking,' he said. 'Mine is not. Come.'\n"
        "We spent the night in his parlour, two families, one candle, nobody mentioning the generator."),
  culture='Cultural setting: a Lagos compound in the rainy season, with shared generators, neighbours who know each other\'s business, and community hospitality in a crisis.',
  pov='First-person narration by a child observer, who records Mama\'s wisdom and the neighbours\' reconciliation.',
  identity='The story suggests that community identity is stronger than individual quarrels; in a crisis, neighbours become one household ("two families, one candle").',
  dev=[('personification', 'the city became honest', 'the city is given a human quality, suggesting that crises reveal true character', ['simile', 'onomatopoeia', 'statistic']),
       ('metaphor', 'turned into a brown river', 'the flooded road becomes a river, showing the power of the rain', ['simile', 'alliteration', 'hyperbole']),
       ('understatement', 'nobody mentioning the generator', 'leaving the old argument unspoken shows forgiveness gently, without sentimentality', ['hyperbole', 'simile', 'rhetorical question'])],
  theme='community and reconciliation',
  summary='During heavy rains in Lagos, a neighbour who had quarrelled with the narrator\'s family invites them to shelter in his dry house, and the old argument is quietly forgotten.')

P(id='satire_school', kind='satire', title='satirical article from a student humour website',
  text=("SCHOOL BANS THINKING TO IMPROVE TEST SCORES\n"
        "Greenfield Academy has announced a ban on independent thought, after research showed that students who think 'take too long' to fill in multiple-choice answers.\n"
        "\"Curiosity is a distraction,\" said Head of Results Ms Graves. \"Our students don't need to understand. They need to tick.\"\n"
        "Questions will now be permitted only on Fridays, between 2:14 and 2:16 p.m.\n"
        "Parents have welcomed the news. \"My son used to ask 'Why?' all the time,\" said one father. \"Now he just says 'Which box?'\""),
  satire='The article satirises schools that focus on test scores rather than real learning. It uses an absurd premise (banning thinking), mock-serious news conventions, ironic quotations and exaggeration (questions allowed for two minutes a week) to criticise exam culture.',
  dev=[('irony', '"Curiosity is a distraction,"', 'the head of results says the opposite of what a school should value, exposing the absurdity of exam-focused education', ['simile', 'onomatopoeia', 'alliteration']),
       ('exaggeration (hyperbole)', 'Questions will now be permitted only on Fridays, between 2:14 and 2:16 p.m.', 'the ridiculously precise, tiny time slot mocks how little room real learning is given', ['understatement', 'simile', 'personification']),
       ('parody of news conventions', 'SCHOOL BANS THINKING TO IMPROVE TEST SCORES', 'imitating a serious headline makes the absurd idea seem official, which is what makes it funny', ['simile', 'statistic', 'onomatopoeia']),
       ('telling name', 'Ms Graves', 'the name suggests death and gloom, hinting that the school is killing curiosity', ['pun on an animal', 'onomatopoeia', 'alliteration'])],
  target='The target of the satire is education systems and schools that value test results over curiosity and understanding.',
  tone='mock-serious', tw=['sincere and angry', 'tragic', 'romantic'], tonex='the straight-faced news style presents an absurd idea as normal.',
  gq='How does the writer use satire to criticise exam-focused schools?',
  gqa='The article parodies news conventions – a serious headline, quotations from officials and parents – to present an absurd premise as normal. Irony ("Curiosity is a distraction") and the telling name "Ms Graves" expose values that kill learning; exaggeration (two minutes of questions a week) mocks how little space real thinking is given. The father\'s quotation ("Which box?") shows the result: students who no longer ask why.',
  write=[('Write a short satirical news article (about 250 words) about an issue in your school or community, using exaggeration, irony and news conventions.', 'Indicative content: a mock-serious headline; an absurd but recognisable premise; ironic quotations; exaggeration; a clear target; consistent deadpan tone.')],
  summary='A satirical article reports that a school has banned independent thought to raise test scores, allowing questions for only two minutes a week, mocking exam-focused education.')

P(id='cartoon_phones', kind='cartoon', title='political cartoon described in words',
  text=("[Image: a family of four sits around a dinner table. Each person is staring at a glowing phone. A huge smartphone sits in the father's chair at the head of the table, wearing his tie. Caption: \"Who's in charge here?\"]"),
  satire='The cartoon satirises families\' dependence on phones: by placing a giant phone in the head-of-the-table chair wearing a tie, it suggests technology has replaced the parent as the authority in the home.',
  visual='Visual exaggeration (the giant phone, the glowing screens lighting every face) and symbolism (the head of the table and the tie represent authority) make the point instantly; the caption\'s question invites viewers to recognise themselves.',
  dev=[('visual metaphor / symbolism', 'A huge smartphone sits in the father\'s chair ... wearing his tie', 'the phone literally takes the parent\'s place, showing technology as the new authority', ['onomatopoeia', 'statistic', 'alliteration']),
       ('rhetorical question in the caption', '"Who\'s in charge here?"', 'the question prompts viewers to reflect on their own habits', ['simile', 'pun', 'statistic'])],
  target='The target is the way smartphones dominate family life and replace conversation and parental authority.',
  tone='humorous but critical', tw=['celebratory', 'neutral', 'tragic'], tonex='the absurd image is funny but makes a serious point.',
  summary='A cartoon shows a family staring at phones while a giant phone sits in the father\'s chair wearing his tie, asking "Who\'s in charge here?"')

P(id='parody_ad', kind='satire', title='parody advertisement from a student magazine',
  text=("[Image: a glossy bottle labelled PERFECT™ on a pink background with sparkles.]\n"
        "TIRED OF BEING YOURSELF?\n"
        "Introducing PERFECT™ – the filter you can drink!\n"
        "✓ Removes freckles, opinions and personality\n"
        "✓ Makes you look exactly like everyone else on your feed\n"
        "✓ Side effects may include: loss of self, endless scrolling, and spending all your money\n"
        "Because you're worth nothing... until you're PERFECT™."),
  satire='It parodies beauty and social-media advertising by copying its conventions (glossy product shot, ticked benefit list, trademark, slogan) but exaggerating them to expose how such adverts sell insecurity and conformity.',
  intertext='It alludes to famous cosmetics slogans of the "because you\'re worth it" type, twisting the phrase to "Because you\'re worth nothing... until you\'re PERFECT™" to reveal the message hidden in real adverts.',
  dev=[('parody of a slogan', 'Because you\'re worth nothing... until you\'re PERFECT™.', 'twisting a well-known slogan exposes how adverts make people feel inadequate', ['simile', 'onomatopoeia', 'statistic']),
       ('ironic list of benefits', 'Removes freckles, opinions and personality', 'the list moves from appearance to identity, showing that beauty culture erases individuality', ['simile', 'personification', 'onomatopoeia']),
       ('rhetorical question', 'TIRED OF BEING YOURSELF?', 'it parodies the "problem" questions of real adverts, revealing that the problem is invented', ['statistic', 'simile', 'alliteration'])],
  target='The target is beauty and social-media culture that sells conformity and insecurity to young people.',
  tone='sarcastic', tw=['sincere', 'mournful', 'neutral'], tonex='the ironic adoption of advertising language mocks its message.',
  gq='How does the parody use the conventions of advertising to criticise beauty culture?',
  gqa='The parody copies real advertising conventions – a glossy product shot, a problem question, ticked benefits, a trademark and a slogan – so readers recognise the genre. Exaggeration exposes the hidden message: the ticked list moves from freckles to "opinions and personality", and the side effects list loss of self. The twisted slogan "Because you\'re worth nothing... until you\'re PERFECT™" alludes to real cosmetic slogans and reveals how they sell insecurity.',
  summary='A mock advert for a drinkable filter called PERFECT™ promises to remove freckles, opinions and personality, mocking beauty and social-media advertising.')

P(id='carroll', kind='poem', title='"How Doth the Little Crocodile" by Lewis Carroll (1865), a parody of Isaac Watts\'s "How doth the little busy bee" (1715)',
  text=("How doth the little crocodile\n"
        "Improve his shining tail,\n"
        "And pour the waters of the Nile\n"
        "On every golden scale!\n\n"
        "How cheerfully he seems to grin,\n"
        "How neatly spreads his claws,\n"
        "And welcomes little fishes in\n"
        "With gently smiling jaws!"),
  intertext='Carroll\'s poem parodies Isaac Watts\'s moral poem for children, which begins "How doth the little busy bee / Improve each shining hour" and praises hard work. Carroll keeps the form and opening but replaces the virtuous bee with a crocodile that "welcomes" fish into its jaws, mocking the preachy moral verse Victorian children had to memorise.',
  satire='The humour comes from the contrast between the polite, moral tone of the original and the sinister crocodile; "gently smiling jaws" makes a predator seem kind, turning moral lessons into a joke.',
  dev=[('irony', 'welcomes little fishes in / With gently smiling jaws!', 'the gentle words describe a crocodile eating fish, so the polite tone is comically sinister', ['simile', 'onomatopoeia', 'statistic']),
       ('parody (imitation of form)', 'How doth the little crocodile', 'echoing Watts\'s opening line signals the original and sets up the comic substitution', ['allusion to Shakespeare', 'onomatopoeia', 'simile'])],
  tone='playfully sinister', tw=['solemn', 'angry', 'tragic'], tonex='a sweet, polite tone describes a predator.',
  theme='parody of moral lessons',
  summary='Carroll describes a crocodile cheerfully polishing its scales and "welcoming" fish into its smiling jaws, parodying a moral poem about a hard-working bee.')

P(id='feature_rickshaw', kind='feature', title='feature article from a weekend newspaper magazine',
  text=("The Last Rickshaw Painter of Dhaka\n"
        "In a workshop no bigger than a parked car, Rafiqul Islam dips a brush thinner than an eyelash into crimson paint. Behind him, a hundred rickshaw panels lean against the wall – film stars, tigers, peacocks, the Taj Mahal.\n"
        "\"Forty years ago there were hundreds of us,\" he says, without looking up. \"Now the machines print stickers. Faster. Cheaper. Dead.\"\n"
        "He finishes the tiger's eye. It seems to blink."),
  feature_vs='It is a feature, not hard news: it opens with a descriptive scene rather than a lead, focuses on one person (human interest), uses sensory detail and quotation, and ends on a reflective image rather than the latest facts.',
  dev=[('descriptive scene-setting opening', 'In a workshop no bigger than a parked car', 'the vivid detail draws readers into the scene like a story', ['inverted pyramid', 'statistic', 'rhetorical question']),
       ('tricolon in quotation', '"Faster. Cheaper. Dead."', 'the three blunt words show the painter\'s bitterness about machine printing; "Dead" ends with shocking finality', ['simile', 'onomatopoeia', 'alliteration']),
       ('hyperbole / simile', 'a brush thinner than an eyelash', 'the exaggeration shows the delicacy and skill of his craft', ['metaphor', 'personification', 'onomatopoeia']),
       ('personification in the ending', 'It seems to blink.', 'the painted tiger comes alive, celebrating the artist\'s skill in a final memorable image', ['simile', 'statistic', 'alliteration'])],
  struct=[('ending on an image rather than a fact', 'the reflective close leaves readers with a feeling of wonder and loss, typical of features')],
  aud='Weekend magazine readers interested in culture and people; the leisurely, descriptive style suits readers with time to read.',
  purp='To inform readers about a disappearing traditional craft and make them care about it through one person\'s story.',
  gq='How does the writer use the conventions of a feature article to engage readers?',
  gqa='Instead of a news lead, the feature opens with a descriptive scene ("a workshop no bigger than a parked car") and sensory detail (a brush "thinner than an eyelash"), focusing on one person for human interest. His quotation "Faster. Cheaper. Dead." gives voice and emotion to a wider change, and the closing image of the tiger that "seems to blink" celebrates his craft and leaves a reflective, poignant ending.',
  write=[('Write the opening of a feature article (about 250 words) about a person in your community who keeps a tradition alive.', 'Indicative content: a descriptive opening scene; human-interest focus; sensory detail; direct quotation; background context; a reflective ending; headline.')],
  summary='A feature profiles Rafiqul Islam, one of Dhaka\'s last hand-painters of rickshaw art, whose craft is being replaced by machine-printed stickers.')

P(id='protest_a', kind='news', title='report of a climate protest (Report A, from a national newspaper)',
  text=("STUDENTS BRING CITY TO STANDSTILL\n"
        "Thousands of school pupils skipped lessons on Friday to block the main bridge into the city, causing traffic delays of up to two hours.\n"
        "Police said three people were arrested for public disorder.\n"
        "\"My son should be in maths, not in the road,\" said commuter Peter Hale.\n"
        "Organisers claimed 12,000 attended, though police estimated 5,000."),
  represent='Report A represents the protesters as disruptive: the headline emphasises the "standstill", the opening focuses on skipped lessons and traffic, it reports arrests, quotes only an annoyed commuter and gives the police estimate the last word.',
  facts_op='Fact: "Police said three people were arrested." Opinion: "My son should be in maths, not in the road" (a commuter\'s judgement). Note the disputed numbers: organisers claimed 12,000, police estimated 5,000.',
  dev=[('framing headline', 'STUDENTS BRING CITY TO STANDSTILL', 'the headline frames the protest as a problem for the city rather than about climate', ['simile', 'pun', 'onomatopoeia']),
       ('selective quotation', '"My son should be in maths, not in the road,"', 'quoting only a critic makes the protest seem irresponsible', ['statistic', 'alliteration', 'hyperbole'])],
  summary='Report A says thousands of pupils skipped school and blocked a bridge, causing delays and three arrests, quoting an annoyed commuter.')

P(id='protest_b', kind='news', title='report of a climate protest (Report B, from a youth news website)',
  text=("12,000 YOUNG PEOPLE DEMAND CLIMATE ACTION\n"
        "Up to 12,000 students marched peacefully across the main bridge on Friday, calling on the government to meet its emissions targets.\n"
        "\"We're missing one day of school. Our future is missing a plan,\" said organiser Amara Diallo, 16.\n"
        "Scientists from the city university joined the march.\n"
        "Police reported three arrests."),
  represent='Report B represents the protesters as responsible and purposeful: the headline uses the organisers\' number and "demand climate action", it stresses "peacefully" and the government\'s targets, quotes a young organiser and scientists\' support, and mentions arrests only briefly at the end.',
  facts_op='Fact: "Police reported three arrests." Opinion: "Our future is missing a plan" (the organiser\'s view). The figure "Up to 12,000" adopts the organisers\' claim.',
  dev=[('framing headline', '12,000 YOUNG PEOPLE DEMAND CLIMATE ACTION', 'using the higher figure and the cause foregrounds the protest\'s size and purpose', ['simile', 'pun', 'onomatopoeia']),
       ('antithesis in quotation', '"We\'re missing one day of school. Our future is missing a plan,"', 'the balanced contrast makes the protesters\' case memorable and reasonable', ['simile', 'alliteration', 'statistic'])],
  summary='Report B says up to 12,000 students marched peacefully to demand climate action, quoting a young organiser and noting scientists\' support and three arrests.')

P(id='scifi_memory', kind='story', title='extract from a science-fiction short story',
  text=("In 2087 you could sell your memories. Most people sold the boring ones first – queues, commutes, tax forms. The MemoryBank paid well for those; rich people used them to feel ordinary.\n"
        "Lin sold her seventh birthday to pay the rent.\n"
        "Afterwards she found a photo of herself in a paper crown, laughing, and felt nothing at all. Not sadness. Not even curiosity.\n"
        "That was the part the advertisements never mentioned: you didn't miss what you sold. You just became a little less."),
  scifi='Science-fiction conventions: a future date (2087), an invented technology (selling memories), a corporation (MemoryBank) and a "what if?" premise used to explore human values.',
  world='World-building is economical: a date, a technology and a market (rich people buy boring memories to "feel ordinary") suggest a whole unequal society in a few sentences.',
  ethics='The story questions whether everything should be for sale and suggests that poverty forces people to trade their identity; it explores the human cost of technology and inequality.',
  dev=[('irony', 'rich people used them to feel ordinary', 'it is ironic that the rich buy ordinary experiences while the poor sell precious ones, exposing inequality', ['simile', 'onomatopoeia', 'alliteration']),
       ('short, devastating sentence', 'Lin sold her seventh birthday to pay the rent.', 'the plain statement makes the loss shocking by treating it as routine', ['simile', 'rhetorical question', 'hyperbole']),
       ('metaphor', 'You just became a little less.', 'losing memories is presented as losing part of the self', ['simile', 'statistic', 'personification'])],
  theme='technology, inequality and identity',
  gq='How does the writer use a science-fiction premise to explore what makes us human?',
  gqa='The futuristic premise – selling memories in 2087 – is built economically through a date, a corporation and a market, and the irony that the rich buy "boring" memories exposes inequality. The flat sentence about Lin selling her seventh birthday makes poverty\'s cost routine, and the photo she feels "nothing" about shows memory as the basis of feeling. The final metaphor ("a little less") suggests identity itself is being sold.',
  write=[('Write the opening of your own speculative short story (about 300 words) based on a "what if?" question about technology.', 'Indicative content: a clear speculative premise; economical world-building (date, technology, society); a character affected by the technology; a hint of the ethical question; a hook.')],
  summary='In 2087 people can sell memories; Lin sells her seventh birthday to pay rent and afterwards feels nothing when she sees a photo of it, realising sellers become "a little less".')

P(id='scifi_mars', kind='story', title='extract from a science-fiction story set on Mars',
  text=("The first child born on Mars turned twelve today. Her name is Hope, which everyone agrees was a bit much.\n"
        "She has never felt rain. She has never seen a dog. When she watches old Earth films, she asks why people walk outside without helmets, as if it were the most dangerous thing in the world.\n"
        "Tonight she stood at the dome window and pointed at a small blue dot. \"Is that really where we're from?\" she asked.\n"
        "Nobody knew how to tell her that it was no longer safe to go back."),
  scifi='Conventions: a future colony on Mars, domes and helmets, Earth seen from space, and a hint of a catastrophe on Earth – a speculative setting used to explore belonging and loss.',
  world='World-building through absence: Hope has never felt rain or seen a dog, and she thinks walking without a helmet is dangerous – her normal life tells us how different the world is.',
  ethics='The story raises questions about humanity\'s treatment of Earth and what it means to belong to a home you cannot return to.',
  dev=[('ironic name', 'Her name is Hope, which everyone agrees was a bit much.', 'the gently humorous comment shows the settlers\' optimism and its weight on one child', ['simile', 'onomatopoeia', 'statistic']),
       ('dramatic irony / reversal', 'as if it were the most dangerous thing in the world', 'what is normal for readers is strange for Hope, showing how her world has reversed our assumptions', ['simile', 'hyperbole', 'alliteration']),
       ('foreshadowing / revelation', 'it was no longer safe to go back', 'the final line reveals a disaster on Earth, turning curiosity into tragedy', ['flashback', 'simile', 'onomatopoeia'])],
  theme='home, belonging and environmental loss',
  summary='Hope, the first child born on Mars, has never felt rain or seen a dog; when she asks if the blue dot is really home, nobody can tell her it is no longer safe to return.')

K.pair('owen_dulce', 'pope_game', 'Compare how the two poets present war and the soldier\'s experience.',
       'Text A (Owen, protest) shows the reality of war through degrading similes ("like old beggars under sacks", "coughing like hags") and the shocking "blood-shod"; the heavy rhythm and caesuras mimic exhaustion. Text B (Pope, propaganda) presents war as a "game" with a jaunty rhythm and regular rhyme, using rhetorical questions to shame men who "sit tight". '
       'Owen writes from first-hand experience to expose suffering; Pope writes from home to recruit. The contrast in form (heavy, broken rhythm vs bouncing song-like verse) mirrors their opposing perspectives; historically Owen\'s poem was a direct reply to writers like Pope.',
       sim='both poems address the experience of young men going to war and try to change how readers think about it.',
       diff='Text A uses grim similes and a slow rhythm to expose suffering, whereas Text B uses a sporting metaphor and a jaunty rhythm to make war sound exciting.')
K.pair('brooke_soldier', 'owen_anthem', 'Compare how the two sonnets present death in war.',
       'Both are sonnets, but they use the form differently. Text A (Brooke, 1914) idealises death: the euphemism "If I should die" and the metaphor of a "corner of a foreign field / That is for ever England" make death noble and peaceful. Text B (Owen, 1917) protests: the simile "die as cattle" and the onomatopoeic "stuttering rifles\' rapid rattle" show anonymous, undignified slaughter. '
       'Brooke wrote before the trenches; Owen wrote from experience. Brooke\'s calm, patriotic tone contrasts with Owen\'s anger and grief.',
       sim='both are sonnets about soldiers dying in a foreign land and how they are remembered.',
       diff='Text A presents death as calm and patriotic, whereas Text B presents it as anonymous slaughter with no proper funeral.')
K.pair('gothic_house', 'mirror_story', 'Compare how the two writers create a sense of the uncanny.',
       'Both use first-person narrators in old houses where ordinary objects behave impossibly – portraits that watch, a mirror that shows the past. Text A builds atmosphere through a hostile setting (fog "like a shroud") and a narrowing focus that ends on "Towards me." Text B uses an apparently unreliable narrator ("I imagined") whose final detail (dry feet) confirms the supernatural. '
       'Text A is dramatic and descriptive; Text B is understated and conversational, making the horror creep up more quietly.',
       sim='both use a first-person narrator in an old house where familiar objects (portraits, a mirror) behave impossibly.',
       diff='Text A builds fear through dramatic Gothic description, whereas Text B uses a calm, self-doubting narrator and a quiet twist.')
K.pair('protest_a', 'protest_b', 'Compare how the two reports represent the same protest.',
       'Both report the same basic facts (a march on the main bridge on Friday, three arrests), but they represent it differently. Report A\'s headline ("BRING CITY TO STANDSTILL") and focus on skipped lessons, traffic and a critical commuter frame the students as disruptive; it ends with the lower police estimate. '
       'Report B\'s headline uses the organisers\' figure and the cause ("DEMAND CLIMATE ACTION"), stresses "peacefully", quotes a young organiser and mentions scientists, placing the arrests last. Selection, order, quotation and numbers create bias in both.',
       sim='both report that a protest took place on the main bridge on Friday and that three people were arrested.',
       diff='Report A presents the students as disruptive by quoting an annoyed commuter, whereas Report B presents them as peaceful and purposeful by quoting a young organiser.')
K.pair('bus_1955', 'soweto_1976', 'Compare how the two extracts present young people\'s experience of injustice and resistance.',
       'Both use a young perspective on historical injustice – segregation in 1955 Alabama, apartheid education in 1976 Soweto. Text A uses third-person limited narration through a child who observes her mother\'s silent resistance ("Her mother did not.") and senses tension ("silence so loud"). '
       'Text B uses a first-person teenager who changes from silence to protest, with the ironic image of shaking hands holding "WE ARE NOT AFRAID". Text A shows resistance as a quiet act by an adult; Text B shows collective youth protest.',
       sim='both present historical injustice through a young person\'s eyes and show an act of courageous resistance.',
       diff='in Text A a child watches her mother resist quietly, whereas in Text B the teenage narrator himself joins a mass protest.')
K.pair('scifi_memory', 'scifi_mars', 'Compare how the two science-fiction extracts use imagined futures to explore human concerns.',
       'Both use economical world-building and a final revelation. Text A imagines a technology (selling memories) that exposes inequality and the link between memory and identity, ending with the metaphor "a little less". Text B imagines a Mars colony whose child has never felt rain, using reversal of our norms and ending with the revelation that Earth is unsafe. '
       'Text A focuses on economic injustice; Text B on environmental loss and belonging. Both suggest the future may cost us what makes us human.',
       sim='both use a futuristic setting and a final line that reveals a hidden cost of the future.',
       diff='Text A explores inequality through a technology that sells memories, whereas Text B explores environmental loss through a child who cannot return to Earth.')
K.pair('satire_school', 'parody_ad', 'Compare how the two texts use humour to criticise aspects of young people\'s lives.',
       'Both are satirical: they imitate a genre (a news report; a beauty advert) and exaggerate it to expose a target – exam culture and beauty/social-media culture. Text A uses deadpan irony ("Curiosity is a distraction"), absurd precision (2:14–2:16 p.m.) and a telling name (Ms Graves). Text B uses an ironic benefit list ("Removes freckles, opinions and personality") and a twisted slogan. '
       'Text A targets institutions; Text B targets the media industry that sells insecurity.',
       sim='both imitate a familiar genre and exaggerate it so that readers laugh at, and question, its values.',
       diff='Text A mocks schools that value test scores, whereas Text B mocks advertising that sells young people insecurity.')


# =============================================================================================
# ch01 Gothic and Horror Fiction
# =============================================================================================
GOTH = {'story'}
GIDS = ['gothic_house', 'telltale', 'mirror_story', 'attic', 'lift']
H('ch01-st1',
  terms=[('Gothic fiction', 'a genre that combines horror, mystery and romance, typically set in old, isolated buildings and exploring fear, the supernatural and hidden secrets'),
         ('the uncanny', 'the unsettling feeling when something familiar becomes strange or frightening (a portrait that watches, a reflection that moves)'),
         ('pathetic fallacy', 'when weather or nature reflects human emotions or the mood of a scene'),
         ('the supernatural', 'events or beings beyond the laws of nature, such as ghosts, curses or impossible occurrences'),
         ('foreboding', 'a feeling that something bad is going to happen')],
  facts=[('Which setting is most typical of Gothic fiction?', 'A crumbling mansion on a fog-covered moor', ['A sunny beach resort', 'A modern open-plan office', 'A busy sports stadium'], 'Isolated, decaying buildings are classic Gothic settings.'),
         ('Which novel is often described as a founding work of Gothic fiction?', 'The Castle of Otranto (Horace Walpole, 1764)', ['Pride and Prejudice', 'Treasure Island', 'Animal Farm'], 'Walpole\'s novel established many Gothic conventions.'),
         ('A portrait whose eyes seem to follow a character is an example of:', 'the uncanny', ['comic relief', 'a flashback', 'a red herring only'], 'A familiar object behaves strangely.'),
         ('Who wrote Frankenstein (1818), a key Gothic novel?', 'Mary Shelley', ['Charles Dickens', 'Jane Austen', 'Edgar Allan Poe'], 'Shelley wrote Frankenstein aged 18–19.')],
  why=[('Explain why Gothic stories are often set in isolated, old buildings.', 'Isolation removes help and escape, while old buildings suggest hidden secrets and the past haunting the present, creating fear and mystery.'),
       ('Explain why the uncanny is more disturbing than an obvious monster.', 'When familiar things become strange, readers feel that even safe, everyday spaces are not to be trusted, which unsettles them deeply.'),
       ('Explain why Gothic writers use pathetic fallacy.', 'Storms, fog and darkness reflect fear and foreboding, building atmosphere and preparing readers for terrible events.')],
  contrast=[('Gothic fiction', 'modern horror', 'Gothic fiction relies on atmosphere, suspense and the uncanny in old settings, often hinting at the supernatural; modern horror may be set anywhere and often shows violence or monsters more explicitly.'),
            ('suspense', 'terror vs horror', 'Suspense is the build-up of uncertainty; in Gothic theory, "terror" is the anticipation of something dreadful, while "horror" is the shock of seeing it.')],
  misc=[('Gothic stories must include a ghost.', 'Many Gothic stories only hint at the supernatural or explain it rationally; atmosphere, secrets and fear matter more than ghosts.'),
        ('Gothic fiction is only about scaring readers.', 'Gothic fiction also explores serious ideas – guilt, madness, the past, social fears – through its frightening atmosphere.')],
  apply=[('List four Gothic conventions you could include in a story set in an old lighthouse.', 'Any four: isolation; a storm (pathetic fallacy); a mysterious light or sound; a secret from the past; a ghost or uncanny object; a frightened first-person narrator.', 4),
         ('Rewrite this sentence to make it Gothic: "The house was old."', 'E.g. "The house crouched at the end of the lane, its windows black and blind, its roof sagging like a broken spine." Credit personification, dark imagery, foreboding.', 2)],
  evaluate=[('Gothic fiction is still effective for modern teenage readers.', ['fear and mystery are universal', 'modern horror films and games borrow Gothic conventions'], ['old-fashioned settings and language can feel distant', 'readers are used to faster, more explicit horror'], 'Gothic remains effective because its psychological fear and the uncanny still unsettle readers, even if some conventions are updated.')],
  extended=[('Choose a Gothic text you have studied. Analyse how it uses setting and the supernatural to create fear.', 'Indicative content: specific Gothic setting details; supernatural hints; the uncanny; language analysis with quotations; effect on the reader. Criteria A and B.', 8, 'long')])
pq('ch01-st1', ('C2', 'C3', 'C4'), (1, 5), None, 'gothic', ['Identify three Gothic conventions in this extract and explain how each creates fear.',
                                                         'How does this extract use the conventions of Gothic fiction?',
                                                         'Explain which features of this extract are typical of the Gothic genre.'], ids=GIDS, crit=CRIT_A)
pq('ch01-st1', ('C2', 'C3'), (1, 4), None, 'uncanny', ['Explain how the writer makes something familiar seem strange or threatening.',
                                                    'Find an example of the uncanny in the extract and explain its effect.'], ids=GIDS, crit=CRIT_B)
pq('ch01-st1', ('C2', 'C3'), (1, 4), None, 'mood', MOOD_Q, ids=GIDS + ['storm_drama'], crit=CRIT_B)
K.dev_mcq('ch01-st1', None, ids=GIDS)
K.vocab('ch01-st1', ids=GIDS)

H('ch01-st2',
  terms=[('tension', 'a feeling of strain and anxious anticipation built up in the reader'),
         ('fragment (minor sentence)', 'an incomplete sentence used for effect, such as "Towards me."'),
         ('syntax', 'the arrangement of words and phrases in a sentence'),
         ('delay', 'holding back key information to keep the reader in suspense'),
         ('rhythm (in prose)', 'the pattern created by sentence lengths and punctuation, which can speed up or slow down reading')],
  facts=[('Which sentence structure most increases tension at a climax?', 'A series of short sentences and fragments', ['One very long sentence with many commas describing scenery', 'A list of dates', 'A paragraph of dialogue about the weather'], 'Short sentences heighten tension.'),
         ('"Small ones. Bare." What is the effect of these fragments?', 'They slow the reader down and focus on disturbing details', ['They speed up a happy scene', 'They summarise the plot', 'They introduce a new character'], 'Fragments isolate details.'),
         ('A long, flowing sentence before a short one is often used to:', 'build up and then release tension with a shock', ['make the reader bored', 'show that nothing is happening', 'give a list of characters'], 'Contrast in sentence length creates impact.')],
  why=[('Explain why writers vary sentence length to control pace.', 'Long sentences can build atmosphere or a sense of rushing, while short ones create abrupt stops and emphasis; varying them controls the reader\'s heartbeat.'),
       ('Explain why a one-line paragraph can be powerful.', 'White space isolates the line, forcing the reader to pause on it, which gives a revelation or shock maximum impact.'),
       ('Explain why dashes can create tension in first-person narration.', 'Dashes break up the flow like gasps or interruptions, showing a nervous or panicked mind (as in Poe\'s narrator).')],
  contrast=[('pace', 'tension', 'Pace is how fast the story seems to move; tension is the anxious feeling in the reader. Slowing the pace at a key moment can increase tension.')],
  misc=[('Short sentences always make writing exciting.', 'Overused, short sentences become choppy; they work best in contrast with longer sentences at key moments.')],
  apply=[('Rewrite this sentence as three short sentences or fragments to build tension: "She slowly opened the door and saw that the room was empty except for a chair that was rocking by itself."', 'E.g. "She opened the door. Slowly. The room was empty – except for a chair. Rocking. By itself." Credit fragments and delay of the key detail.', 3),
         ('Write a paragraph of four sentences in which a long sentence builds suspense and a short final sentence delivers a shock.', 'Any paragraph showing deliberate contrast in sentence length ending on a short shocking sentence.', 3)],
  evaluate=[('Sentence structure creates more tension than vocabulary.', ['rhythm controls pace and shock', 'fragments and white space create pauses'], ['vivid, threatening words create fear', 'tension comes from both together'], 'Sentence structure and vocabulary work together, but structure is often what turns frightening words into a heart-stopping moment.')],
  extended=[('Analyse how a writer uses sentence structure to create tension in a Gothic or horror extract you have read.', 'Indicative content: identifies sentence lengths, fragments, punctuation and paragraphing with quotations; explains effects on pace and tension; organised argument. Criteria A and B.', 8, 'long')])
pq('ch01-st2', ('C2', 'C3', 'C4'), (1, 5), None, 'dev', ['Analyse how the writer uses sentence structure in "{quote}" to create tension.',
                                                      'Explain how "{quote}" controls the pace of the extract.',
                                                      'How does the writer\'s syntax in "{quote}" affect the reader?'], ids=GIDS + ['bus_1955', 'storm_drama'], crit=CRIT_B)
pq('ch01-st2', ('C2', 'C3'), (1, 4), None, 'struct', STRUCT_Q, ids=GIDS, crit=CRIT_B)
para('ch01-st2', None, ids=GIDS, c='C4', d=(3, 5), frames=['{gq} Focus on sentence structure and pacing.',
                                                          'Write an analytical paragraph explaining how sentence structure and pacing create tension in this extract.'])

H('ch01-st3',
  terms=[('unreliable narrator', 'a narrator whose account cannot be fully trusted because of madness, bias, ignorance or deception'),
         ('first-person narration', 'narration by a character using "I", limiting the reader to that character\'s perspective'),
         ('dramatic irony', 'when the reader understands more than the narrator or characters'),
         ('confession', 'a narrative in which the narrator admits to wrongdoing, common in Gothic tales')],
  facts=[('Which clue most strongly suggests a narrator is unreliable?', 'He insists he is sane while describing impossible things', ['He gives the date', 'He describes the weather', 'He uses past tense'], 'Contradiction reveals unreliability.'),
         ('"The Tell-Tale Heart" (1843) was written by:', 'Edgar Allan Poe', ['Mary Shelley', 'Bram Stoker', 'Charles Dickens'], 'Poe is famous for unreliable narrators.'),
         ('Why does Poe\'s narrator say "why will you say that I am mad?"', 'He is trying to convince the reader of his sanity, which makes us suspect him', ['He is asking a doctor for help', 'He is joking with a friend', 'He is reading a letter aloud'], 'Protesting too much undermines him.')],
  why=[('Explain why Gothic writers often use unreliable narrators.', 'If the reader cannot trust the narrator, they cannot be sure what is real, which increases fear and ambiguity – is the ghost real, or is the narrator mad?'),
       ('Explain why an unreliable narrator makes the reader work harder.', 'The reader must read between the lines, comparing what the narrator says with clues that contradict it, becoming a detective.')],
  contrast=[('a reliable narrator', 'an unreliable narrator', 'A reliable narrator gives an account the reader can trust; an unreliable narrator\'s account is distorted by madness, bias, lies or limited understanding, so the reader must question it.')],
  misc=[('An unreliable narrator is always lying on purpose.', 'Narrators may be unreliable because they are mad, young, biased, mistaken or self-deceiving, not only because they lie.')],
  apply=[('Write two sentences in the voice of an unreliable narrator who insists they are calm but clearly is not.', 'E.g. "I am perfectly calm—perfectly! I simply checked the lock seventeen times because locks, you know, can change their minds." Credit contradiction between claim and evidence.', 2),
         ('Identify two clues in the mirror story that make the narrator seem unreliable and one clue that suggests she is telling the truth.', 'Unreliable: "He\'s probably right"; repeated "I imagined". Truth: her feet were dry although there were wet footprints.', 3)],
  evaluate=[('An unreliable narrator makes a story more frightening than a reliable one.', ['uncertainty about reality creates dread', 'the reader is trapped inside a disturbed mind'], ['a trustworthy narrator can make the reader believe the horror is real', 'too much uncertainty can confuse'], 'Unreliable narrators often heighten fear through ambiguity, but a reliable narrator can be equally frightening when we trust their account of horror.')])
pq('ch01-st3', ('C2', 'C3', 'C4'), (1, 5), None, 'unreliable', ['What clues suggest that the narrator cannot be fully trusted?',
                                                             'Explain how the writer presents the narrator as unreliable.',
                                                             'To what extent should the reader trust this narrator? Refer to the text.'], ids=['telltale', 'mirror_story'], crit=CRIT_B)
pq('ch01-st3', ('C2', 'C3'), (1, 4), None, 'pov', POV_Q, ids=['telltale', 'mirror_story', 'gothic_house'], crit=CRIT_B)
para('ch01-st3', None, ids=['telltale', 'mirror_story'], c='C4', d=(3, 5))
K.vocab('ch01-st3', ids=['telltale', 'gothic_house'])
K.tone_mcq('ch01-st3', None, ids=['telltale', 'mirror_story', 'gothic_house'])

H('ch01-st4',
  terms=[('opening hook', 'a first line or paragraph designed to grab the reader\'s attention and raise questions'),
         ('in medias res', 'starting a story in the middle of the action'),
         ('atmosphere', 'the overall feeling of a scene, created through setting, description and pace')],
  facts=[('Which is the strongest opening line for a Gothic story?', '"The house had been empty for forty years, yet every night a candle burned in the highest window."', ['"I went to a house."', '"Gothic stories are scary."', '"It was a nice day and nothing happened."'], 'It sets a mystery and Gothic setting immediately.'),
         ('Which detail would best create foreboding in a Gothic opening?', 'A raven watching from a broken gate', ['A bright rainbow', 'A cheerful postman', 'A new car'], 'Ominous symbols create foreboding.')],
  why=[('Explain why a Gothic opening should create questions rather than answer them.', 'Unanswered questions (who lights the candle?) create suspense and make readers continue.'),
       ('Explain why sensory detail is important in a Gothic opening.', 'Cold air, groaning gates and the smell of damp immerse the reader in the atmosphere and make fear physical.')],
  contrast=[('a descriptive opening', 'an in medias res opening', 'A descriptive opening builds atmosphere slowly through setting; an in medias res opening drops the reader into action and explains later.')],
  misc=[('A Gothic opening must reveal the monster immediately.', 'Gothic openings usually delay revelation, using hints and atmosphere to build dread.'),
        ('More adjectives always make a Gothic opening better.', 'Precise, well-chosen details and strong verbs are more effective than piling up adjectives.')],
  apply=[('Write the first two sentences of a Gothic story set in an abandoned school.', 'Credit Gothic conventions (isolation, decay, a mystery, foreboding) and a hook. 1 mark for atmosphere, 1 for hook.', 2),
         ('Improve this opening by adding pathetic fallacy and a mystery: "I arrived at the old hotel."', 'E.g. "I arrived at the old hotel as the storm broke, and the receptionist said my room had been booked for me – forty years ago." Credit weather reflecting mood and an intriguing mystery.', 2)],
  evaluate=[('A Gothic opening should focus on atmosphere rather than character.', ['atmosphere defines the genre', 'setting creates dread'], ['readers need a character to care about', 'the narrator\'s fear makes atmosphere matter'], 'The best Gothic openings combine both: atmosphere creates dread, and a character\'s reactions make the reader feel it.')],
  extended=[('Write the opening (about 400 words) of a Gothic short story. Use setting, the uncanny and varied sentence structure to create tension.', 'Indicative content: Gothic setting; the uncanny; foreboding; first-person or close third narrator; varied sentences and fragments; a hook or cliffhanger. Criteria B, C, D.', 12, 'long')])
write('ch01-st4', ids=['gothic_house'])
K.prompts('ch01-st4', 'open', c=('C3', 'C4'), d=(2, 5))
K.prompts('ch01-st4', 'one', c='C4', d=(3, 5))
pq('ch01-st4', 'C3', (2, 4), None, 'struct', ['Explain how {feature} makes this an effective opening, and how you could use the same technique in your own Gothic opening.'], ids=GIDS, crit=CRIT_B)


# =============================================================================================
# ch02 Novel Study: Prejudice and Social Justice
# =============================================================================================
NOVEL = ['bus_1955', 'soweto_1976', 'newcountry_class']
H('ch02-st1',
  terms=[('historical context', 'the time, place and events in which a novel is set or written, which shape its meaning'),
         ('segregation', 'the enforced separation of people by race, as under the "Jim Crow" laws in the southern United States'),
         ('apartheid', 'the system of racial segregation and discrimination enforced by law in South Africa from 1948 to the early 1990s'),
         ('prejudice', 'an unfair opinion formed about a person or group without knowledge or reason'),
         ('social justice', 'fair and equal rights, opportunities and treatment for all people in society')],
  facts=[('In which year did the Montgomery Bus Boycott begin?', '1955', ['1919', '1968', '1989'], 'It began in December 1955 after Rosa Parks\'s arrest.'),
         ('What did students in Soweto protest against on 16 June 1976?', 'Being taught some subjects in Afrikaans', ['A ban on football', 'The end of apartheid', 'School uniforms'], 'The Soweto Uprising began as a protest against Afrikaans-medium instruction.'),
         ('Which novel, set in 1930s Alabama, explores racial prejudice through the eyes of a child narrator, Scout?', 'To Kill a Mockingbird (Harper Lee)', ['Animal Farm', 'The Hunger Games', 'Lord of the Flies'], 'Lee\'s novel is widely studied for its treatment of prejudice.')],
  why=[('Explain why knowing the historical context of a novel changes how we read it.', 'Context reveals the laws, attitudes and dangers characters faced, so their choices – like staying seated on a bus – gain meaning and courage.'),
       ('Explain why writers often set novels about prejudice in the past.', 'Historical settings let readers see injustice clearly with hindsight, and invite comparison with prejudice that still exists today.'),
       ('Explain why a novel can teach readers about history differently from a textbook.', 'A novel gives an emotional, personal perspective on events, helping readers understand how injustice felt to individuals.')],
  contrast=[('the context of setting', 'the context of writing', 'The context of setting is the time and place in which the story happens; the context of writing is when and where the author wrote it. They may differ (e.g. a novel written in 2010 about 1955).')],
  misc=[('Context is only important for history lessons, not for English.', 'Context shapes a text\'s meaning, language and reception; understanding it is part of analysing a novel (criterion A).'),
        ('Novels about prejudice in the past have nothing to say about today.', 'They often invite readers to recognise similar attitudes and injustices in the present.')],
  apply=[('Explain how the historical context of 1955 Alabama makes the mother\'s action in the bus extract significant.', 'Segregation laws required Black passengers to give up seats; refusing risked arrest or violence, so her staying seated is a courageous act of resistance, echoing Rosa Parks.', 3),
         ('Write two sentences explaining how the 1976 setting shapes the meaning of the Soweto extract.', 'The apartheid government\'s order to teach in Afrikaans turned education into a symbol of oppression, so the narrator\'s decision to march shows a young person joining a historic resistance.', 3)],
  evaluate=[('A novel about prejudice cannot be understood without knowing its historical context.', ['context explains laws and dangers', 'readers may misread characters\' choices'], ['universal emotions of fear and courage are understandable anyway', 'good novels provide context within the story'], 'Context greatly deepens understanding, but powerful novels also communicate universal experiences that readers can grasp before researching the history.')],
  extended=[('Choose a novel you have studied that deals with prejudice. Explain how its historical and social context shapes its meaning, with reference to two key moments.', 'Indicative content: accurate context; two specific moments with evidence; explanation of how context gives them meaning; organised response. Criteria A and B.', 8, 'long')])
pq('ch02-st1', ('C2', 'C3', 'C4'), (1, 5), None, 'context', ['Explain how the historical or social context of this extract shapes its meaning.',
                                                          'How does knowing the context help you understand the characters\' actions?',
                                                          'Identify one detail that reflects the context of the extract and explain its significance.'], ids=NOVEL + ['nobel_mum'], crit=CRIT_A)
para('ch02-st1', None, ids=NOVEL, c='C4', d=(3, 5))
K.dev_mcq('ch02-st1', None, ids=NOVEL)
K.tone_mcq('ch02-st1', None, ids=['bus_1955', 'telltale', 'pope_game', 'owen_dulce'])

H('ch02-st2',
  terms=[('character development (arc)', 'the way a character changes over the course of a story'),
         ('protagonist', 'the main character of a story'),
         ('static character', 'a character who does not change significantly'),
         ('dynamic character', 'a character who changes in an important way'),
         ('epiphany', 'a sudden moment of realisation that changes a character\'s understanding')],
  facts=[('In the Soweto extract, how does the narrator change?', 'From staying silent to joining the protest', ['From brave to cowardly', 'From student to teacher', 'He does not change'], 'He becomes politically active.'),
         ('A character who changes significantly is called:', 'dynamic', ['static', 'flat', 'minor'], 'Dynamic characters develop.'),
         ('Which moment best shows a turning point in a protagonist\'s perspective?', 'The narrator sees a friend treated unfairly and decides to speak out', ['The narrator eats breakfast', 'The narrator describes the weather', 'The narrator lists his subjects'], 'Turning points change perspective.')],
  why=[('Explain why writers show a protagonist\'s perspective changing.', 'A changing perspective lets readers grow with the character and models how people can recognise and challenge injustice.'),
       ('Explain why a child narrator\'s perspective is effective in a novel about prejudice.', 'A child sees injustice with fresh eyes and asks simple questions, exposing how unreasonable adult prejudice is.')],
  contrast=[('a static character', 'a dynamic character', 'A static character stays essentially the same throughout; a dynamic character changes in values, understanding or behaviour, often because of key events.')],
  misc=[('A character\'s development happens in one moment.', 'Development is usually gradual, shown through several events, though an epiphany can mark a turning point.')],
  apply=[('Track a character\'s development: write one sentence each about how the narrator of the Soweto extract feels at the start, at the turning point and at the end.', 'Start: cautious, focused on exams ("I said nothing"). Turning point: the new rule and Thabo\'s protest. End: marching with the sign, afraid but determined.', 3),
         ('Explain what Samir\'s silence at the end of the Berlin extract reveals about his development.', 'He has learned to hide his identity and pain in order to fit in; he has not yet found a way to share his perspective, suggesting his journey towards belonging is incomplete.', 2)],
  evaluate=[('Readers learn most about injustice from characters who change.', ['change shows how understanding develops', 'readers identify with growth'], ['static characters can show how deeply prejudice is rooted', 'victims\' unchanging resilience can be powerful'], 'Changing characters model growth, but static characters can reveal the stubbornness of prejudice; both teach readers.')],
  extended=[('Analyse how a protagonist\'s perspective changes in a novel you have studied, referring to at least two key moments.', 'Indicative content: initial perspective; two moments that cause change with quotations; final perspective; analysis of how the writer shows the change (narration, dialogue, symbol). Criteria A and B.', 8, 'long')])
pq('ch02-st2', ('C2', 'C3', 'C4'), (1, 5), None, 'char', CHAR_Q + ['How does the main character change, or begin to change, in this extract?'], ids=NOVEL, crit=CRIT_A)
pq('ch02-st2', ('C2', 'C3'), (1, 4), None, 'pov', POV_Q, ids=NOVEL, crit=CRIT_B)
para('ch02-st2', None, ids=NOVEL, c='C4', d=(3, 5), frames=['{gq} Comment on how the character\'s perspective is presented.'])
K.vocab('ch02-st2', ids=NOVEL + ['newgirl', 'treehouse'])

H('ch02-st3',
  terms=[('symbol', 'an object, colour, place or action that represents a larger idea'),
         ('motif', 'a recurring image, idea or symbol that develops a theme across a text'),
         ('allegory', 'a story in which characters and events represent ideas, such as political or moral issues')],
  facts=[('In the bus extract, what does the painted line most clearly symbolise?', 'Segregation', ['Friendship', 'Freedom', 'Wealth'], 'The line divides passengers by race.'),
         ('What is the difference between a symbol and a motif?', 'A motif recurs across a text; a symbol may appear once or recur', ['A symbol is always a colour', 'A motif is only in poetry', 'There is no difference'], 'Motifs are recurring patterns.'),
         ('In the Berlin extract, walls and borders recur. This is an example of:', 'a motif', ['a pun', 'a statistic', 'an anecdote'], 'Recurring images form a motif.')],
  why=[('Explain why writers use symbols to explore prejudice.', 'Symbols make abstract ideas (segregation, division) visible and memorable, allowing writers to criticise injustice without stating it directly.'),
       ('Explain how a motif can develop a theme across a novel.', 'Each time a motif reappears it gains new associations, deepening the theme (e.g. walls in history and in a refugee\'s life).')],
  contrast=[('a symbol', 'a metaphor', 'A metaphor is a direct comparison within a sentence; a symbol is an object or image in the story world that stands for an idea throughout.')],
  misc=[('Every object in a novel is a symbol.', 'Only objects given emphasis, repetition or significance function as symbols; over-reading every detail weakens analysis.')],
  apply=[('Identify a symbol in the Soweto extract and explain what it represents.', 'The cardboard sign "WE ARE NOT AFRAID" represents collective courage; the shaking hands show that courage exists alongside fear.', 2),
         ('Suggest a symbol a writer could use in a novel about a family divided by a border, and explain its meaning.', 'E.g. a broken phone line or an empty chair at the table, representing the absent relative and the family\'s incompleteness.', 2)],
  evaluate=[('Symbols are more powerful than direct statements in novels about injustice.', ['they engage readers to interpret', 'they are memorable and layered'], ['direct statements can be clear and urgent', 'some readers may miss symbols'], 'Symbols often create deeper, lasting impact, but direct moments of testimony are also powerful; the best novels combine both.')])
pq('ch02-st3', ('C2', 'C3', 'C4'), (1, 5), None, 'symbol', ['Identify a symbol or motif in this extract and explain what it represents.',
                                                         'How does the writer use symbolism to develop a theme?',
                                                         'Analyse the significance of one recurring image or object in the extract.'], ids=NOVEL + ['nobel_mum', 'treehouse'], crit=CRIT_B)
pq('ch02-st3', ('C2', 'C3'), (1, 4), None, 'theme', THEME_Q, ids=NOVEL + ['bench', 'treehouse'], crit=CRIT_OPEN)

H('ch02-st4',
  terms=[('thesis statement', 'a sentence, usually in the introduction, that states the main argument of an essay'),
         ('PEEL paragraph', 'a paragraph with a Point, Evidence, Explanation and Link back to the question or thesis'),
         ('embedded quotation', 'a short quotation built smoothly into your own sentence'),
         ('literary present tense', 'the convention of writing about literature in the present tense ("the narrator says")')],
  facts=[('Which is the strongest thesis for an essay on prejudice in a novel?', 'The writer uses a child\'s perspective and symbolism to show how prejudice is normalised and how ordinary people resist it.', ['The novel is about prejudice.', 'I liked the novel a lot.', 'Prejudice is bad.'], 'A thesis is specific and arguable.'),
         ('What does the "L" in PEEL stand for?', 'Link', ['Language', 'List', 'Length'], 'Link back to the question or thesis.'),
         ('Which tense should normally be used to analyse a novel?', 'The present tense', ['The future tense', 'The past perfect only', 'Any tense randomly'], 'Literary present: "Ruth notices..."')],
  why=[('Explain why an analytical essay needs a clear thesis.', 'It gives the essay a direction and argument; every paragraph can then support it, which shows organisation (criterion B).'),
       ('Explain why linking back to the question is important at the end of each paragraph.', 'It keeps the essay focused and shows how each point answers the question, rather than drifting into retelling.')],
  contrast=[('a thesis statement', 'a topic sentence', 'A thesis states the argument of the whole essay; a topic sentence states the main point of one paragraph, supporting the thesis.')],
  misc=[('An analytical essay should retell the plot so the examiner knows what happens.', 'The examiner knows the plot; analysis explains how and why the writer creates meaning, using brief references.'),
        ('A conclusion should introduce a brand-new argument.', 'A conclusion should draw the argument together and may reflect on wider significance, not start a new point.')],
  apply=[('Write a thesis statement for the essay question: "How does the writer present injustice in the bus extract?"', 'E.g. "Through a child\'s limited perspective, a symbolic painted line and a single act of quiet defiance, the writer presents injustice as both normalised and resistible." Credit specificity and argument.', 2),
         ('Write a PEEL paragraph on how the writer of the Berlin extract presents Samir\'s identity, using the quotation "like a dog answers to a whistle".', 'Point: Samir\'s identity is diminished by trying to fit in. Evidence: the simile. Explanation: comparing himself to a dog shows he feels controlled and less than human. Link: the writer suggests belonging at the cost of identity is not true belonging.', 4, 'long')],
  evaluate=[('A good analytical essay should have exactly five paragraphs.', ['a clear, simple structure helps organisation', 'it ensures introduction, body and conclusion'], ['the argument should determine the structure', 'rigid formulas can limit depth'], 'Structure should serve the argument; five paragraphs can work, but strong essays adapt their organisation to the question.')],
  extended=[('Write an analytical essay (about 600 words): "How does a novel you have studied present prejudice and resistance to it?"', 'Indicative content: clear thesis; three or four PEEL paragraphs with embedded quotations; analysis of narrative perspective, symbolism and character; context; conclusion. Criteria A, B, D.', 12, 'long'),
            ('Write the introduction and first body paragraph of an essay on how a writer uses symbolism in a novel you have studied.', 'Indicative content: context-setting opening; thesis; topic sentence; embedded evidence; analysis of the symbol; link. Criteria A, B.', 8, 'long')])
para('ch02-st4', None, ids=NOVEL + ['newgirl', 'treehouse', 'bench'], c=('C3', 'C4'), d=(2, 5),
     frames=['{gq}\nWrite a PEEL paragraph that answers the question, with at least one embedded quotation.',
             'Write a thesis statement and one analytical paragraph in response to: {gq}',
             'Essay question: {gq} Write the introduction (with a thesis) and your first body paragraph.'])


# =============================================================================================
# ch03 Shakespeare: Romeo and Juliet
# =============================================================================================
RJ = ['rj_prologue', 'rj_balcony', 'rj_fight']
H('ch03-st1',
  terms=[('the Globe', 'the open-air London theatre where many of Shakespeare\'s plays were performed, built in 1599'),
         ('groundlings', 'audience members who paid a penny to stand in the yard in front of the stage'),
         ('Elizabethan', 'relating to the reign of Elizabeth I (1558–1603)'),
         ('patriarchy', 'a social system in which men hold power, including fathers\' authority over daughters\' marriages'),
         ('fate', 'the idea that events are predetermined by a power beyond human control, often linked to the stars')],
  facts=[('Who played female roles on the Elizabethan stage?', 'Boy actors', ['Women', 'The playwright himself', 'Puppets'], 'Women did not act on the public stage in Elizabethan England.'),
         ('Where is Romeo and Juliet set?', 'Verona, Italy', ['London', 'Athens', 'Venice'], '"In fair Verona, where we lay our scene."'),
         ('Why did many Elizabethans believe "star-cross\'d lovers" were doomed?', 'Many believed the stars and fate controlled human lives', ['They thought astronomy was a crime', 'Stars were a symbol of luck only in comedies', 'The phrase meant the lovers were famous'], 'Astrology and fate were widely believed.'),
         ('Approximately when was Romeo and Juliet written?', 'Around 1595', ['Around 1495', 'Around 1695', 'Around 1795'], 'It is an early Shakespeare tragedy, c. 1594–96.')],
  why=[('Explain why the Elizabethan audience\'s beliefs about fate matter to Romeo and Juliet.', 'Many believed destiny was written in the stars, so the Prologue\'s "star-cross\'d" lovers would seem genuinely doomed, increasing tragic tension.'),
       ('Explain why Juliet\'s defiance of her father would shock an Elizabethan audience.', 'In a patriarchal society, daughters were expected to obey fathers in marriage; Juliet\'s refusal challenges social order.'),
       ('Explain why Shakespeare\'s language had to create setting and time of day.', 'Plays were performed in daylight with few props, so words like "what light through yonder window breaks" had to make the audience imagine night and place.')],
  contrast=[('an Elizabethan audience', 'a modern audience', 'An Elizabethan audience might accept fate, arranged marriage and duels as part of life; a modern audience may see the tragedy as caused by adult hatred, impulsive choices and lack of communication.')],
  misc=[('Shakespeare\'s plays were written only for wealthy people.', 'The Globe\'s audience included groundlings who paid a penny to stand, so plays had to appeal to all classes with action, humour and spectacle.')],
  apply=[('Explain how a groundling and a wealthy spectator might each enjoy the fight scene in Act 3 Scene 1.', 'Groundlings would enjoy the sword fight and Mercutio\'s jokes; wealthy spectators might appreciate the wordplay (the "grave man" pun) and the tragic turning point.', 2)],
  evaluate=[('Romeo and Juliet is more about fate than about the characters\' own choices.', ['the Prologue calls them "star-cross\'d"', 'coincidences such as the undelivered letter'], ['Romeo kills Tybalt in anger', 'the feud and rushed marriage are human decisions'], 'Shakespeare balances the two: fate frames the story, but characters\' impulsive choices and the adults\' hatred cause the tragedy.')])
pq('ch03-st1', ('C2', 'C3', 'C4'), (1, 5), None, 'context', ['Explain how the Elizabethan context helps us understand this extract.',
                                                          'How might an Elizabethan audience have responded to this extract differently from a modern audience?'], ids=RJ, crit=CRIT_A)
K.kind_mcq('ch03-st1', None, ids=RJ + ['storm_drama', 'screen_rain'])
K.dev_mcq('ch03-st1', None, ids=RJ)

H('ch03-st2',
  terms=[('iambic pentameter', 'a line of ten syllables in five iambs (unstressed-stressed pairs): "but SOFT, what LIGHT through YON-der WIN-dow BREAKS"'),
         ('blank verse', 'unrhymed iambic pentameter, used by Shakespeare for noble characters and serious speech'),
         ('sonnet', 'a 14-line poem; the Shakespearean sonnet rhymes ABAB CDCD EFEF GG and ends with a couplet'),
         ('pun', 'a play on words with two meanings, such as Mercutio\'s "grave man"'),
         ('prose (in drama)', 'speech without metre, often used by servants, comic characters or in informal moments')],
  facts=[('How many syllables are in a line of iambic pentameter?', 'Ten', ['Eight', 'Twelve', 'Fourteen'], 'Five iambs of two syllables.'),
         ('The Prologue to Romeo and Juliet is written as:', 'a sonnet', ['a limerick', 'free verse', 'a haiku'], '14 lines ending with a rhyming couplet.'),
         ('"Ask for me to-morrow, and you shall find me a grave man." What device is this?', 'A pun', ['A simile', 'Onomatopoeia', 'Alliteration'], '"Grave" = serious / in a grave.'),
         ('When Romeo and Juliet first meet, their dialogue forms:', 'a shared sonnet', ['a limerick', 'a ballad', 'a list of insults'], 'Their first 14 lines together form a sonnet, linking them through love poetry.')],
  why=[('Explain why Shakespeare uses iambic pentameter for many of his characters.', 'Its rhythm resembles a heartbeat and natural speech while sounding elevated, giving dignity to noble characters and serious emotions.'),
       ('Explain why Shakespeare makes Romeo and Juliet\'s first conversation a sonnet.', 'The sonnet is the form of love poetry, so sharing one shows their instant connection and harmony.'),
       ('Explain why Mercutio speaks in prose when he is dying.', 'Prose suits his witty, informal character; breaking from verse makes his speech feel raw and natural even as he dies.')],
  contrast=[('verse', 'prose', 'In Shakespeare, verse (usually iambic pentameter) is used for noble or emotional speech; prose is used for comic, informal or lower-status characters and moments, or to show a character\'s breakdown.')],
  misc=[('Shakespeare\'s plays are written entirely in rhyme.', 'Most of the verse is unrhymed blank verse; rhyme is used in sonnets, couplets at the ends of scenes, and special moments.'),
        ('Iambic pentameter means every line rhymes.', 'Iambic pentameter refers to rhythm (five unstressed-stressed pairs), not rhyme.')],
  apply=[('Mark the stressed syllables in "It is the east, and Juliet is the sun."', 'it IS the EAST and JU-liet IS the SUN – five stresses (iambic pentameter).', 2),
         ('Explain the double meaning of "civil" in "Where civil blood makes civil hands unclean."', '"Civil" means relating to citizens (civil war, civil blood) and polite/civilised; the repetition shows citizens\' blood staining supposedly civilised hands.', 2)],
  evaluate=[('Shakespeare\'s language is a barrier for modern students.', ['old vocabulary and syntax', 'puns that are hard to understand'], ['performance and context make meaning clear', 'many phrases are still used today', 'the imagery remains powerful'], 'The language is challenging but rewarding; performance, glosses and close reading reveal how its rhythm and imagery still create meaning.')],
  extended=[('Analyse how Shakespeare uses language and verse form in one key scene of Romeo and Juliet you have studied.', 'Indicative content: identifies blank verse/prose/sonnet use; imagery and wordplay with quotations; explains effects on character and audience; organised analysis. Criteria A and B.', 8, 'long')])
pq('ch03-st2', ('C2', 'C3', 'C4'), (1, 5), None, 'dev', DEV_Q, ids=RJ, crit=CRIT_B)
pq('ch03-st2', ('C2', 'C3'), (1, 4), None, 'metre', ['Explain the metre of this extract and its effect.',
                                                   'How does Shakespeare\'s use of verse contribute to the effect of this extract?'], ids=['rj_prologue', 'rj_balcony'], crit=CRIT_B)
para('ch03-st2', None, ids=RJ, c='C4', d=(3, 5))
K.vocab('ch03-st2', ids=RJ + ['telltale'])

H('ch03-st3',
  terms=[('prologue', 'an introduction to a play, spoken by the Chorus in Romeo and Juliet, that summarises the story'),
         ('dramatic irony', 'when the audience knows something the characters do not'),
         ('turning point (peripeteia)', 'a moment that reverses the direction of the action, such as Mercutio\'s death'),
         ('climax', 'the moment of greatest tension in a play'),
         ('tragedy', 'a play in which the main characters suffer and usually die, often because of a flaw or fate')],
  facts=[('Which event is the main turning point of Romeo and Juliet?', 'The deaths of Mercutio and Tybalt in Act 3 Scene 1', ['The Capulet party', 'The Prologue', 'The Nurse\'s speech about Juliet\'s childhood'], 'From this point the play becomes tragic.'),
         ('Why does the Prologue create dramatic irony?', 'It tells the audience that the lovers will die', ['It hides the ending', 'It introduces a comic subplot', 'It is spoken by Romeo'], 'The audience watches knowing the outcome.'),
         ('How many acts are there in Romeo and Juliet?', 'Five', ['Three', 'Two', 'Seven'], 'Shakespeare\'s plays are divided into five acts.')],
  why=[('Explain why Shakespeare tells the audience the ending in the Prologue.', 'It creates dramatic irony and shifts interest from what happens to how and why, making every hopeful moment painful.'),
       ('Explain why Mercutio\'s death changes the mood of the play.', 'It removes the play\'s main source of comedy and provokes Romeo\'s revenge, turning romance into tragedy.')],
  contrast=[('dramatic irony', 'situational irony', 'Dramatic irony is when the audience knows more than the characters (we know the lovers will die); situational irony is when the outcome is the opposite of what is expected (Romeo\'s attempt at peace leads to Mercutio\'s death).')],
  misc=[('Knowing the ending ruins the suspense of Romeo and Juliet.', 'Dramatic irony creates a different suspense – the audience hopes for an escape it knows will not come.')],
  apply=[('Identify the dramatic irony in Romeo\'s line "Courage, man; the hurt cannot be much."', 'The audience (and Mercutio) know the wound is fatal, while Romeo believes it is minor, so his reassurance is painfully mistaken.', 2),
         ('Explain why Act 3 Scene 1 is called the turning point of the play.', 'Mercutio\'s and Tybalt\'s deaths lead to Romeo\'s banishment, separating the lovers and setting off the chain of events that ends in their deaths.', 3)],
  evaluate=[('Mercutio\'s death is the most important moment in the play.', ['it turns comedy into tragedy', 'it causes Romeo\'s banishment'], ['the lovers\' meeting or the final deaths are equally crucial', 'the Prologue shapes the whole play'], 'Mercutio\'s death is the structural turning point, though its importance depends on the events it connects – the love before and the tragedy after.')])
pq('ch03-st3', ('C2', 'C3', 'C4'), (1, 5), None, 'struct', STRUCT_Q, ids=RJ, crit=CRIT_B)
pq('ch03-st3', ('C2', 'C3'), (1, 4), None, 'irony', ['Explain how dramatic irony works in this extract.',
                                                   'What does the audience know that the characters do not, and what is the effect?'], ids=['rj_balcony', 'rj_fight'], crit=CRIT_B)
para('ch03-st3', None, ids=['rj_fight', 'rj_prologue'], c='C4', d=(3, 5))

H('ch03-st4',
  terms=[('film adaptation', 'a film version of a literary text, which interprets it through visual and sound choices'),
         ('interpretation', 'a particular understanding of a text, shown through choices of setting, casting, cutting and style'),
         ('setting (in adaptation)', 'the time and place in which a director chooses to stage the story, which may differ from the original'),
         ('mise-en-scène', 'everything placed in the frame: set, costume, lighting, props and actors\' positions')],
  facts=[('Baz Luhrmann\'s 1996 film of Romeo and Juliet is set in:', 'a modern city called Verona Beach, with guns instead of swords', ['Elizabethan London', 'a spaceship', 'ancient Rome'], 'Luhrmann updated the setting but kept Shakespeare\'s language.'),
         ('Franco Zeffirelli\'s 1968 film is known for:', 'period costumes and Italian Renaissance locations', ['a modern Miami setting', 'animated characters', 'a happy ending'], 'Zeffirelli used a traditional setting.'),
         ('What does Luhrmann\'s film do with Shakespeare\'s original dialogue?', 'Keeps much of the original language in a modern setting', ['Translates it all into modern slang', 'Removes all dialogue', 'Turns it into songs'], 'The contrast is part of its interpretation.')],
  why=[('Explain why a director might set Romeo and Juliet in the modern world.', 'A modern setting (gangs, guns, media) makes the feud and youth violence feel relevant to contemporary audiences.'),
       ('Explain why comparing two adaptations deepens understanding of a scene.', 'Different choices of setting, casting, music and cutting reveal different interpretations, showing that the text can mean different things.')],
  contrast=[('a traditional adaptation', 'a modernised adaptation', 'A traditional adaptation keeps the original period and setting (Zeffirelli\'s Renaissance Verona); a modernised one moves the story to a contemporary setting (Luhrmann\'s Verona Beach) to highlight its relevance.')],
  misc=[('A film adaptation should copy the play exactly.', 'Adaptations interpret; cutting lines, changing settings and adding music are choices that create new meaning.')],
  apply=[('Suggest how a director could film the balcony scene to emphasise danger as well as romance. Describe two choices.', 'E.g. cut to guards patrolling below; use a swimming pool or high wall setting with security lights; tense music under the dialogue. Credit choices linked to meaning.', 4),
         ('Explain how setting the fight scene on a hot, crowded beach (as in some modern versions) might affect the audience.', 'Heat and crowds build tension and suggest violence about to erupt; a public setting makes the feud seem dangerous to everyone.', 2)],
  evaluate=[('Modern film adaptations make Shakespeare more accessible than stage performances.', ['familiar settings and visuals', 'music and editing guide emotion'], ['live theatre preserves the language and atmosphere', 'heavy cuts may lose meaning'], 'Modern films can open Shakespeare to new audiences, but they offer one interpretation; comparing them with the text and stage versions gives the fullest understanding.')],
  extended=[('Compare how two film adaptations of Romeo and Juliet present one key scene. Analyse setting, camera, sound and performance, and explain which interpretation you find more effective.', 'Indicative content: two named adaptations; specific choices of setting, camera, sound and acting; analysis of different interpretations; justified judgement. Criteria A and B.', 12, 'long')])
pq('ch03-st4', ('C3', 'C4'), (2, 5), None, 'struct', ['Imagine you are directing a film of this extract. Describe two camera or sound choices that would bring out its meaning, and explain why.',
                                                    'How might a modern film adaptation stage this extract differently from a traditional one? Give two examples.'], ids=RJ, crit=CRIT_OPEN)
pq('ch03-st4', 'C2', (1, 3), None, 'film', ['Explain how camera and sound choices in this script create meaning.'], ids=['screen_rain', 'trailer'], crit=CRIT_B)


# =============================================================================================
# ch04 War Poetry
# =============================================================================================
WAR = ['owen_dulce', 'owen_anthem', 'pope_game', 'brooke_soldier']
H('ch04-st1',
  terms=[('war poetry', 'poetry written about the experience of war, especially by soldier-poets of the First World War'),
         ('the Western Front', 'the line of trenches across Belgium and France where much of the First World War was fought'),
         ('caesura', 'a pause in the middle of a line of poetry, often marked by punctuation'),
         ('tone', 'the attitude of the poet towards the subject, shown through word choice and rhythm'),
         ('imagery', 'language that creates vivid pictures and sensations in the reader\'s mind')],
  facts=[('Wilfred Owen\'s "Dulce et Decorum Est" takes its title from a poem by:', 'Horace, a Roman poet', ['Shakespeare', 'Rupert Brooke', 'Jessie Pope'], 'Horace wrote "Dulce et decorum est pro patria mori".'),
         ('When was Wilfred Owen killed?', 'November 1918, a week before the Armistice', ['1914', '1916', '1939'], 'He died on 4 November 1918.'),
         ('Which poet, who served in the trenches and met Owen at Craiglockhart hospital, also wrote bitter protest poetry?', 'Siegfried Sassoon', ['Rupert Brooke', 'Jessie Pope', 'Lewis Carroll'], 'Sassoon encouraged Owen\'s writing.'),
         ('"Bent double, like old beggars under sacks" – what is the tone?', 'Bitter and grim', ['Joyful', 'Patriotic', 'Comic'], 'The image degrades the soldiers.')],
  why=[('Explain why Owen compares young soldiers to "old beggars" and "hags".', 'The similes show how war has destroyed their youth, health and dignity, contradicting heroic images of soldiers.'),
       ('Explain why caesuras are effective in Owen\'s poetry.', 'Mid-line pauses break the rhythm, slowing the reader and mimicking the soldiers\' exhausted, halting movement.'),
       ('Explain why the soldier-poets\' first-hand experience gives their poetry authority.', 'They witnessed the trenches directly, so their images of suffering carry credibility that challenged propaganda written by people at home.')],
  contrast=[('imagery', 'tone', 'Imagery is the vivid sensory picture created by words ("blood-shod"); tone is the poet\'s attitude (bitter, patriotic) which the imagery helps to create.')],
  misc=[('All First World War poetry was anti-war.', 'Early war poetry, such as Brooke\'s and Pope\'s, was often patriotic; protest poetry grew as the reality of the trenches became known.')],
  apply=[('Explain the effect of the compound "blood-shod" in "Dulce et Decorum Est".', 'Instead of shoes, the soldiers\' feet are covered in blood; the shocking image shows extreme suffering and loss of basic dignity.', 2),
         ('Identify two words in "Anthem for Doomed Youth" that create a harsh sound and explain the effect.', 'E.g. "stuttering", "rattle" (or "rapid") – repeated "t" and "r" sounds imitate gunfire, replacing funeral prayers with violent noise.', 2)],
  evaluate=[('Imagery is the most powerful tool in Owen\'s war poetry.', ['similes and metaphors make suffering vivid', 'images stay in the reader\'s memory'], ['rhythm, sound and irony (the title) are equally powerful', 'his first-hand perspective gives authority'], 'Imagery is central, but its power comes from combination with rhythm, sound and the ironic contrast with patriotic language.')],
  extended=[('Analyse how Owen uses imagery and tone to present the reality of war in one poem you have studied.', 'Indicative content: specific images with quotations; tone; sound and rhythm; context; effect on reader. Criteria A and B.', 8, 'long')])
pq('ch04-st1', ('C2', 'C3', 'C4'), (1, 5), None, 'dev', DEV_Q, ids=WAR, crit=CRIT_B)
pq('ch04-st1', ('C2', 'C3'), (1, 4), None, 'tone', TONE_Q, ids=WAR, crit=CRIT_B)
para('ch04-st1', None, ids=['owen_dulce'], c='C4', d=(3, 5), frames=['{gq}', 'Write an analytical paragraph: {gq} Comment on imagery and tone.',
                                                                     'Answer in about 300 words: {gq} Refer to sound and rhythm as well as imagery.'])
K.dev_mcq('ch04-st1', None, ids=WAR)
K.tone_mcq('ch04-st1', None, ids=WAR)

H('ch04-st2',
  terms=[('propaganda', 'information, often biased or misleading, used to promote a political cause or point of view'),
         ('protest poetry', 'poetry that challenges authority or criticises injustice, such as war'),
         ('recruitment', 'persuading people to join the armed forces'),
         ('euphemism', 'a mild word or phrase used instead of a harsh one (e.g. "If I should die")'),
         ('jingoism', 'extreme, aggressive patriotism')],
  facts=[('Jessie Pope\'s "Who\'s for the Game?" presents war as:', 'a sporting game', ['a nightmare', 'a prison', 'a funeral'], 'The extended metaphor makes war seem fun.'),
         ('The poster "Daddy, what did YOU do in the Great War?" uses which emotion to persuade?', 'Guilt and shame', ['Humour', 'Boredom', 'Calm'], 'It imagines future shame.'),
         ('Owen originally addressed "Dulce et Decorum Est" to:', 'Jessie Pope', ['Rupert Brooke', 'the King', 'his mother'], 'An early draft was dedicated "To Jessie Pope etc."')],
  why=[('Explain why recruitment propaganda presented war as a game or adventure.', 'Making war seem exciting and safe encouraged young men to volunteer and hid the danger.'),
       ('Explain why propaganda often uses shame.', 'Fear of being seen as a coward by family and society was a powerful pressure that could override personal fear of fighting.'),
       ('Explain why protest poets used shocking images.', 'Graphic images forced civilians to confront the reality hidden by propaganda and challenged the idea that dying for one\'s country is glorious.')],
  contrast=[('propaganda', 'protest', 'Propaganda promotes a cause, often by simplifying or hiding the truth (war as a "game"); protest challenges authority by exposing suffering and questioning official messages.')],
  misc=[('Propaganda always contains lies.', 'Propaganda can use true facts selectively; its aim is to persuade, often by appealing to emotion rather than presenting a full picture.')],
  apply=[('Identify two persuasive techniques in "Who\'s for the Game?" and explain their effect on young men in 1915.', 'Extended sporting metaphor – makes war seem fun; rhetorical questions – put pressure on readers and imply cowardice ("rather sit tight"). Also accept jaunty rhythm.', 4),
         ('Rewrite the line "Who\'s for the game, the biggest that\'s played" from the perspective of a soldier in the trenches in 1917.', 'Any rewriting that exposes reality with a bitter tone, e.g. "Who\'s for the mud, the gas and the rats?" Credit perspective shift.', 2)],
  evaluate=[('Propaganda poetry has no literary value.', ['it simplifies and manipulates', 'its purpose is persuasion, not truth'], ['it is skilfully crafted (rhythm, metaphor)', 'it is valuable evidence of historical attitudes'], 'Propaganda poetry may be morally questionable, but it has historical and technical value, and studying it sharpens understanding of protest poetry.')],
  extended=[('"Propaganda and protest are two sides of the same coin: both try to persuade." Discuss with reference to two war texts.', 'Indicative content: defines propaganda and protest; analyses persuasive techniques in each (e.g. Pope and Owen); considers differences in honesty and perspective; judgement. Criteria A and B.', 12, 'long')])
pq('ch04-st2', ('C2', 'C3', 'C4'), (1, 5), None, 'persp', ['Is this text propaganda or protest? Justify your answer with reference to the text.',
                                                        'Explain the perspective on war presented in this text.',
                                                        'How does the writer try to shape the reader\'s attitude to war?'], ids=WAR + ['daddy_poster'], crit=CRIT_OPEN)
pq('ch04-st2', ('C2', 'C3'), (1, 4), None, 'visual', VIS_Q, ids=['daddy_poster', 'fastfashion_poster'], crit=CRIT_B)
para('ch04-st2', None, ids=['daddy_poster'], c='C4', d=(3, 5))
K.compare_short('ch04-st2', c='C3', d=(2, 4), only=['owen_dulce', 'brooke_soldier'])

H('ch04-st3',
  terms=[('comparative analysis', 'an analysis that examines similarities and differences between two texts'),
         ('comparative connective', 'a word or phrase that signals comparison, such as similarly, whereas, in contrast, likewise'),
         ('form', 'the overall shape and type of a poem (sonnet, ballad, free verse)'),
         ('message', 'the main idea or attitude that a poem communicates')],
  facts=[('Which connective signals a difference?', 'Whereas', ['Similarly', 'Likewise', 'Also'], '"Whereas" introduces contrast.'),
         ('Both "The Soldier" and "Anthem for Doomed Youth" are:', 'sonnets', ['limericks', 'ballads', 'free verse'], 'Both use the 14-line form, to opposite effect.'),
         ('When comparing two poems, a strong paragraph should:', 'discuss both poems and link them with comparative connectives', ['discuss only one poem', 'list techniques without explanation', 'retell both poems'], 'Integrated comparison is strongest.')],
  why=[('Explain why it is effective to compare poems that use the same form differently.', 'Shared form highlights contrasting attitudes – a love-poem form used for patriotic idealism by Brooke and for angry grief by Owen.'),
       ('Explain why an integrated comparison is better than writing about each poem separately.', 'Discussing both together in each paragraph shows direct links and differences, demonstrating comparison rather than two separate analyses (criterion B).')],
  contrast=[('an integrated comparison', 'a block comparison', 'An integrated comparison discusses both texts in each paragraph, point by point; a block comparison writes about one text fully and then the other, which risks losing the comparison.')],
  misc=[('Comparison means only finding differences.', 'Comparison includes similarities and differences; strong answers explore both and explain their significance.')],
  apply=[('Write a comparative topic sentence about the tone of "The Soldier" and "Dulce et Decorum Est".', 'E.g. "Whereas Brooke\'s tone is calm and patriotic, Owen\'s is bitter and grim, reflecting their different experiences of war."', 2),
         ('Complete the comparison: "Both poets write about death in war; however, Brooke ______, while Owen ______."', 'E.g. Brooke presents death as a noble gift to England; Owen presents it as anonymous slaughter "as cattle".', 2)],
  evaluate=[('Comparing poems from opposite perspectives is more useful than comparing poems with the same view.', ['contrast reveals techniques clearly', 'it shows how context shapes attitude'], ['similar poems reveal subtle differences in method', 'shared perspectives show a common experience'], 'Opposing perspectives often make comparison vivid, but comparing similar poems trains closer attention to subtle choices; both are valuable.')])
K.compare('ch04-st3', d=(3, 5), only=['owen_dulce', 'brooke_soldier', 'grandmother_kitchen'])
K.compare_short('ch04-st3', c='C3', d=(2, 4), only=['owen_dulce', 'brooke_soldier', 'grandmother_kitchen'])
pq('ch04-st3', 'C3', (2, 4), None, 'persp', ['Summarise the poet\'s perspective on war in one sentence, then explain how one image supports it.'], ids=WAR, crit=CRIT_A)
pq('ch04-st3', 'C2', (1, 3), None, 'form', ['Identify the form of this poem and explain why the poet\'s use of it is significant.'], ids=['owen_anthem', 'brooke_soldier'], crit=CRIT_B)


# =============================================================================================
# ch05 Film and Moving Image
# =============================================================================================
FILM = ['screen_rain', 'trailer']
H('ch05-st1',
  terms=[('close-up', 'a shot that shows a face or object in detail, revealing emotion or significance'),
         ('wide (long) shot', 'a shot that shows a whole setting and a figure\'s place within it'),
         ('high angle / low angle', 'a shot looking down on (high) or up at (low) a subject, making it seem weak or powerful'),
         ('tracking shot', 'a shot in which the camera moves alongside or follows the action'),
         ('cut', 'an instant change from one shot to another; the rhythm of cuts controls pace')],
  facts=[('Which shot best shows a character\'s isolation in a vast landscape?', 'A wide shot', ['An extreme close-up of an eye', 'An insert of a phone screen', 'A two-shot'], 'Wide shots show scale.'),
         ('What is the usual effect of rapid cuts in a trailer?', 'They increase pace and excitement or anxiety', ['They slow the film down', 'They make it romantic', 'They remove sound'], 'Fast editing builds energy.'),
         ('A low-angle shot of a villain usually makes them seem:', 'powerful and threatening', ['weak and small', 'friendly', 'far away'], 'Looking up gives dominance.')],
  why=[('Explain why directors vary shot distance.', 'Different distances control what the audience sees and feels – wide shots establish context, close-ups create intimacy and reveal emotion.'),
       ('Explain why editing pace matters.', 'Long takes create calm or tension through stillness, while rapid cuts create energy, confusion or fear.')],
  contrast=[('a close-up', 'a wide shot', 'A close-up isolates a face or object to show emotion or importance; a wide shot shows the whole setting and the character\'s position within it, often suggesting isolation or scale.')],
  misc=[('Camera angles are chosen just to make films look good.', 'Angles create meaning: a high angle can make a character seem vulnerable, a low angle powerful.')],
  apply=[('Describe the shot you would use to show (a) a nervous student before an exam and (b) a huge crowd at a concert, explaining each.', '(a) close-up of hands or face to show nerves; (b) wide or aerial shot to show scale and energy. 1 mark each shot, 1 each reason.', 4)],
  evaluate=[('Camera work matters more than dialogue in film.', ['film is a visual medium', 'images show emotion without words'], ['dialogue reveals character and plot', 'sound and performance matter too'], 'Camera work is central to film\'s meaning, but it works with dialogue, sound and performance; the strongest scenes combine them.')])
pq('ch05-st1', ('C2', 'C3', 'C4'), (1, 5), None, 'film', ['Analyse how camera shots and editing are used in this extract.',
                                                        'Explain how two camera choices in this extract create meaning.',
                                                        'How do the shots chosen guide the audience\'s emotions?'], ids=FILM, crit=CRIT_B)
K.dev_mcq('ch05-st1', None, ids=FILM)
pq('ch05-st1', ('C2', 'C3'), (1, 4), None, 'dev', DEV_Q, ids=FILM, crit=CRIT_B)
para('ch05-st1', None, ids=FILM, c='C4', d=(3, 5))

H('ch05-st2',
  terms=[('diegetic sound', 'sound that exists in the world of the film, which characters can hear (dialogue, a phone buzzing, rain)'),
         ('non-diegetic sound', 'sound added for the audience only, such as background music or a voice-over'),
         ('mise-en-scène', 'everything placed in the frame: setting, props, costume, lighting, make-up and actors\' positions'),
         ('lighting (high-key / low-key)', 'high-key lighting is bright and even; low-key lighting has strong shadows and darkness'),
         ('sound bridge', 'sound from one scene that continues into the next, linking them')],
  facts=[('A phone buzzing that the character hears is:', 'diegetic sound', ['non-diegetic sound', 'a voice-over', 'a soundtrack only'], 'It exists in the story world.'),
         ('Low-key lighting is most typical of which genre?', 'Horror or thriller', ['Romantic comedy', 'Children\'s cartoons', 'Cooking shows'], 'Shadows create suspense.'),
         ('Which is part of mise-en-scène?', 'The character\'s costume', ['The film\'s budget', 'The cinema\'s seating', 'The release date'], 'Mise-en-scène is what appears in the frame.')],
  why=[('Explain why silence can be effective in a film.', 'Removing sound focuses attention and builds tension, so the next sound (a buzz, a crash) becomes startling and important.'),
       ('Explain why directors use non-diegetic music.', 'Music tells the audience how to feel – hope, fear, sadness – even when characters do not know what is coming.'),
       ('Explain how mise-en-scène can reveal character.', 'Costume, props and setting signal personality, status and emotion – a soaked boy at the edge of a roof suggests vulnerability and a turning point.')],
  contrast=[('diegetic sound', 'non-diegetic sound', 'Diegetic sound comes from within the story world and characters can hear it; non-diegetic sound (soundtrack, voice-over) is added for the audience only.')],
  misc=[('Music in films is just background decoration.', 'Music shapes emotional response, signals genre and can foreshadow events.')],
  apply=[('Suggest diegetic and non-diegetic sound for a scene where a girl waits alone at a bus stop at night, and explain each.', 'Diegetic: distant traffic, a flickering streetlight buzz – realism and loneliness; non-diegetic: slow, low strings – unease or sadness. Credit links to mood.', 4),
         ('Describe the mise-en-scène you would use for the opening of a horror film set in a school.', 'E.g. empty corridor, flickering lights (low-key), a single schoolbag on the floor, lockers half open. Credit purposeful choices.', 3)],
  evaluate=[('Sound is more important than image in creating fear in horror films.', ['music and silence manipulate emotion', 'jump scares rely on sound'], ['dark images and framing create dread', 'sound without image loses meaning'], 'Sound often triggers fear, but it works with mise-en-scène and camera; together they create horror.')])
pq('ch05-st2', ('C2', 'C3', 'C4'), (1, 5), None, 'film', ['Analyse how sound is used in this extract and its effect on the audience.',
                                                        'Explain how sound and silence build tension in the extract.'], ids=FILM, crit=CRIT_B)
pq('ch05-st2', ('C2', 'C3'), (1, 4), None, 'mise', ['Analyse the mise-en-scène of this extract and what it suggests.',
                                                  'How do setting, lighting and costume create meaning in this script?'], ids=['screen_rain'], crit=CRIT_B)
pq('ch05-st2', ('C3', 'C4'), (2, 5), None, 'struct', STRUCT_Q, ids=FILM, crit=CRIT_B)

H('ch05-st3',
  terms=[('film genre', 'a category of film with recognisable conventions, such as horror, romance, science fiction or action'),
         ('conventions', 'typical features audiences expect in a genre (e.g. a creepy house and jump scares in horror)'),
         ('target audience', 'the specific group of viewers a film or trailer is designed for'),
         ('trailer', 'a short promotional video that advertises a film by showing selected highlights')],
  facts=[('Which is a convention of the horror genre?', 'A jump scare after silence', ['A wedding ending', 'A song-and-dance number', 'A courtroom verdict'], 'Jump scares are typical of horror.'),
         ('Why is a horror film often released in October?', 'To link with Halloween', ['Because cinemas are closed in summer', 'Because it is the only month for trailers', 'To avoid young audiences'], 'Release timing targets audiences.'),
         ('Why do trailers usually avoid revealing the ending?', 'To create curiosity and make audiences buy tickets', ['Because endings are not filmed yet', 'Because it is illegal', 'To make the trailer longer'], 'Trailers raise questions.')],
  why=[('Explain why trailers follow genre conventions.', 'Recognisable conventions tell audiences immediately what kind of experience to expect, attracting fans of that genre.'),
       ('Explain why some films subvert genre conventions.', 'Breaking expectations surprises audiences and can make a familiar genre feel fresh or comment on it.')],
  contrast=[('following conventions', 'subverting conventions', 'Following conventions meets audience expectations (a haunted house in horror); subverting them deliberately breaks expectations (a ghost who is friendly) for surprise or comment.')],
  misc=[('A film can belong to only one genre.', 'Many films are hybrids (romantic comedy, science-fiction horror), combining conventions of more than one genre.')],
  apply=[('List four conventions you would include in a trailer for a science-fiction film aimed at teenagers.', 'Any four: futuristic setting; technology or space; a young hero; a threat to humanity; special effects; dramatic music; a tagline; a release date.', 4)],
  evaluate=[('Genre conventions make films predictable.', ['audiences can guess what will happen', 'repetitive formulas'], ['conventions create satisfying expectations', 'skilful films play with them'], 'Conventions can feel predictable, but they also give pleasure and a framework that inventive films build on or subvert.')])
pq('ch05-st3', ('C2', 'C3', 'C4'), (1, 5), None, 'genre', ['Identify the genre conventions in this trailer and explain how they attract the target audience.',
                                                         'How does the trailer use genre to create audience expectations?'], ids=['trailer'], crit=CRIT_B)
pq('ch05-st3', ('C2', 'C3'), (1, 4), None, 'aud', AUD_Q, ids=['trailer', 'filmreview'], crit=CRIT_A)
para('ch05-st3', None, ids=['trailer'], c='C4', d=(3, 5))

H('ch05-st4',
  terms=[('film review', 'an evaluative article about a film, combining a brief summary, analysis and a verdict'),
         ('verdict', 'the reviewer\'s overall judgement, often with a star rating'),
         ('spoiler', 'information that reveals important plot twists or the ending')],
  facts=[('Which is a convention of a film review?', 'A star rating and verdict', ['Stage directions', 'A rhyme scheme', 'A lead paragraph with who/what/where/when only'], 'Reviews evaluate.'),
         ('Why should a review avoid spoilers?', 'So readers can still enjoy the film', ['Because reviews must be short', 'Because directors forbid it', 'To confuse readers'], 'Spoilers ruin surprises.')],
  why=[('Explain why using film vocabulary improves a review.', 'Terms like "handheld close-ups" explain precisely how a film creates effects and build the reviewer\'s credibility.'),
       ('Explain why a good review includes a weakness.', 'Balance shows fairness and makes the praise more believable.')],
  contrast=[('a review', 'a summary', 'A summary retells what happens; a review evaluates how well the film works, using evidence and a verdict.')],
  misc=[('A review is just the reviewer\'s opinion, so evidence is unnecessary.', 'A strong review supports its opinions with specific evidence from the film (scenes, techniques, performances).')],
  apply=[('Write the verdict (two sentences) for a review of a film you recently watched, including a recommendation for a specific audience.', 'E.g. "A gripping, beautifully shot thriller that falters only in its final act. Perfect for fans of mysteries who don\'t mind a few jumps." Credit evaluation and audience.', 2)],
  evaluate=[('Star ratings are the most useful part of a film review.', ['quick, easy to compare', 'many readers only check stars'], ['ratings lack explanation', 'the analysis helps readers judge whether they will like it'], 'Ratings are a useful summary, but the reasoning and evidence are what make a review valuable.')],
  extended=[('Write a film review (about 400 words) of a film you have seen, using film terminology and the conventions of a review.', 'Indicative content: headline and rating; spoiler-free summary; analysis of camera, sound or mise-en-scène with film terms; strengths and a weakness; verdict for a target audience. Criteria B, C, D.', 12, 'long')])
write('ch05-st4', ids=['filmreview', 'bookreview'])
pq('ch05-st4', ('C2', 'C3', 'C4'), (1, 5), None, 'dev', DEV_Q, ids=['filmreview', 'bookreview'], crit=CRIT_B)
para('ch05-st4', None, ids=['filmreview', 'bookreview'], c='C4', d=(3, 5))
pq('ch05-st4', 'C3', (1, 4), None, 'struct', STRUCT_Q, ids=['filmreview', 'bookreview'], crit=CRIT_B)
K.kind_mcq('ch05-st4', None, ids=['filmreview', 'bookreview', 'trailer', 'screen_rain'])


# =============================================================================================
# ch06 Argument and Persuasion: Essays and Opinion Pieces
# =============================================================================================
ARG = ['oped_vote16', 'oped_homework', 'uniform', 'phonesfree', 'library_letter']
H('ch06-st1',
  terms=[('claim', 'the main point or position an argument sets out to prove'),
         ('evidence', 'facts, statistics, examples, expert opinion or anecdotes that support a claim'),
         ('counterargument', 'an opposing point of view that the writer acknowledges'),
         ('rebuttal', 'the writer\'s response that shows why the counterargument is weaker'),
         ('reasoning', 'the explanation of how the evidence supports the claim')],
  facts=[('In "Let Us Vote at 16", which sentence is the counterargument?', '"Critics say teenagers are too immature."', ['"Let Us Vote at 16"', '"We are asking for a voice."', '"At 16 I can work"'], 'It states the opposing view.'),
         ('Which is the strongest type of evidence for a claim about health?', 'Results from a reliable scientific study', ['A rumour on social media', 'A personal feeling', 'A slogan'], 'Reliable research is strongest.'),
         ('What does a rebuttal do?', 'Shows why an opposing argument is weaker', ['Repeats the claim', 'Introduces the topic', 'Lists sources'], 'It answers the counterargument.')],
  why=[('Explain why including a counterargument can make an argument stronger.', 'It shows the writer has considered other views and allows them to answer objections before the reader raises them, building trust.'),
       ('Explain why evidence alone is not enough.', 'Reasoning must explain how the evidence supports the claim; otherwise readers may not see the connection.'),
       ('Explain why anecdotes are useful but limited as evidence.', 'They make arguments vivid and emotional, but one example may not represent the wider picture, so they work best with data.')],
  contrast=[('a claim', 'evidence', 'A claim is the position being argued ("the voting age should be 16"); evidence is the support for it (Austria\'s experience since 2007).'),
            ('a counterargument', 'a rebuttal', 'A counterargument states the opposing view; a rebuttal answers it, showing why it is weaker or wrong.')],
  misc=[('Mentioning the other side weakens your argument.', 'Acknowledging and rebutting the other side strengthens your argument by showing fairness and anticipating objections.'),
        ('The more statistics you use, the more persuasive your argument.', 'Too many statistics can overwhelm; well-chosen evidence, clearly explained, is more persuasive.')],
  apply=[('Write a claim, one piece of evidence, a counterargument and a rebuttal for the topic "Schools should start at 10 a.m."', 'Claim: schools should start at 10 a.m. Evidence: research on teenage sleep cycles. Counterargument: it would disrupt parents\' work schedules. Rebuttal: flexible drop-off schemes and improved learning outweigh the inconvenience. 1 mark each.', 4),
         ('Identify the claim, evidence, counterargument and rebuttal in "Less Homework, Better Learning?"', 'Claim: less but better homework. Evidence: research that benefits level off after 1–2 hours. Counterargument: parents worry about standards. Rebuttal: a tired student copying answers learns nothing.', 4)],
  evaluate=[('An argument with emotional appeal is more effective than one based on logic.', ['emotion motivates action', 'stories are memorable'], ['logic builds trust and withstands scrutiny', 'emotional manipulation can backfire'], 'The most effective arguments combine sound logic with emotional engagement, adapted to the audience.')],
  extended=[('Write an argumentative essay (about 500 words): "Social media does more harm than good to teenagers."', 'Indicative content: clear claim; two or three arguments with varied evidence; counterargument and rebuttal; logical structure with connectives; conclusion. Criteria B, C, D.', 12, 'long')])
pq('ch06-st1', ('C2', 'C3', 'C4'), (1, 5), None, 'claim', ['Identify the claim, evidence, counterargument and rebuttal in this text.',
                                                         'How does the writer construct the argument? Refer to its claim, evidence and counterargument.',
                                                         'Evaluate how convincing the writer\'s evidence is.'], ids=['oped_vote16', 'oped_homework'], crit=CRIT_A)
pq('ch06-st1', ('C2', 'C3'), (1, 4), None, 'struct', STRUCT_Q, ids=ARG, crit=CRIT_B)
para('ch06-st1', None, ids=ARG, c='C4', d=(3, 5))
write('ch06-st1', ids=['oped_vote16'])

H('ch06-st2',
  terms=[('ethos', 'an appeal to the speaker\'s or writer\'s credibility, character or authority'),
         ('pathos', 'an appeal to the audience\'s emotions'),
         ('logos', 'an appeal to logic and reason, using facts, statistics and evidence'),
         ('rhetoric', 'the art of persuasive speaking or writing'),
         ('Aristotle', 'the ancient Greek philosopher who described the three rhetorical appeals')],
  facts=[('"I have set homework for twenty years." Which appeal is this?', 'Ethos', ['Pathos', 'Logos', 'Kairos only'], 'Experience builds credibility.'),
         ('"A tired student who copies answers at midnight learns nothing." This appeals mainly to:', 'pathos', ['logos', 'ethos', 'none'], 'It creates a sympathetic image.'),
         ('"Austria has let 16-year-olds vote since 2007." This appeals mainly to:', 'logos', ['pathos', 'ethos', 'irony'], 'It uses factual evidence.')],
  why=[('Explain why effective arguments often combine ethos, pathos and logos.', 'Each appeal persuades a different part of the audience: credibility builds trust, emotion motivates and logic convinces; together they are more powerful.'),
       ('Explain why ethos matters for a young writer arguing about votes at 16.', 'Speaking from personal experience (working and paying tax) gives the writer authority on the issue.')],
  contrast=[('pathos', 'logos', 'Pathos persuades through emotion (images of suffering, hope); logos persuades through reason and evidence (statistics, logical consequences).')],
  misc=[('Pathos is a dishonest way to persuade.', 'Emotional appeals are legitimate when they are relevant and truthful; they become manipulative only when they distort or replace evidence.')],
  apply=[('Write one sentence using each appeal (ethos, pathos, logos) to persuade students to join a litter-picking club.', 'Ethos: "As captain of the eco-club for two years, I have seen what we can achieve." Pathos: "Imagine a turtle tangled in a crisp packet you dropped." Logos: "Last term we collected 400 kg of litter in four hours."', 3)],
  evaluate=[('Logos is the most important rhetorical appeal.', ['evidence makes an argument credible', 'it withstands scrutiny'], ['audiences act on emotion', 'without ethos the evidence may not be trusted'], 'Logos is essential, but its impact depends on the speaker\'s credibility and on emotional engagement; the appeals work best together.')])
pq('ch06-st2', ('C2', 'C3', 'C4'), (1, 5), None, 'dev', ['Identify the rhetorical appeal used in "{quote}" and explain its effect.',
                                                       'Explain whether "{quote}" appeals mainly to ethos, pathos or logos, and why.',
                                                       'Analyse how the writer uses "{quote}" to persuade the audience.'], ids=ARG, crit=CRIT_B)
K.dev_mcq('ch06-st2', None, ids=['oped_vote16', 'oped_homework'])
para('ch06-st2', None, ids=['oped_vote16', 'phonesfree', 'uniform'], c='C4', d=(3, 5), frames=['{gq} Refer to ethos, pathos and logos in your answer.'])

H('ch06-st3',
  terms=[('opinion column', 'a regular article in which a writer argues a personal view on a topical issue'),
         ('by-line', 'the line giving the writer\'s name'),
         ('hook', 'an opening designed to grab attention'),
         ('call to action', 'a closing request for readers to do something')],
  facts=[('Which is the best headline for an opinion column?', '"Why Our School Needs a Four-Day Week"', ['"Some Information"', '"Article 3"', '"A Report on Weather"'], 'It signals a clear stance.'),
         ('How does an opinion column differ from a news report?', 'It argues the writer\'s personal view', ['It must be neutral', 'It contains no evidence', 'It is always written in the third person'], 'Columns are subjective.')],
  why=[('Explain why opinion columns often begin with an anecdote.', 'An anecdote hooks readers emotionally and makes the issue personal before the argument begins.'),
       ('Explain why a column for a school magazine should consider its audience carefully.', 'Students, teachers and parents have different concerns; addressing them appropriately (tone, examples) makes the argument more persuasive.')],
  contrast=[('an opinion column', 'an editorial', 'An opinion column expresses an individual writer\'s view under their name; an editorial expresses the official view of the publication.')],
  misc=[('Opinion columns do not need evidence because they are opinions.', 'Effective columns support opinions with evidence, examples and reasoning to persuade readers.')],
  apply=[('Write a hook (two sentences) for an opinion column arguing that schools should teach cooking.', 'E.g. "Last week my friend tried to boil an egg in the microwave. It exploded – and so did my belief that we\'re ready for adult life." Credit an engaging, relevant hook.', 2)],
  evaluate=[('Humour makes an opinion column more persuasive.', ['it engages and disarms readers', 'it makes the writer likeable'], ['it can trivialise serious issues', 'jokes may alienate some readers'], 'Humour can be very persuasive when it supports, rather than replaces, a serious argument, as in the uniform column.')],
  extended=[('Write an opinion column (about 400 words) for your school magazine on an issue that matters to students.', 'Indicative content: headline and by-line; hook; clear claim; evidence and anecdote; counterargument and rebuttal; rhetorical appeals; memorable ending or call to action. Criteria B, C, D.', 12, 'long')])
write('ch06-st3', ids=ARG)
pq('ch06-st3', ('C2', 'C3'), (1, 4), None, 'kconv', KCONV_Q, ids=['oped_vote16', 'oped_homework', 'uniform'], crit=CRIT_A)
pq('ch06-st3', 'C3', (1, 4), None, 'aud', AUD_Q, ids=ARG, crit=CRIT_A)
K.tone_mcq('ch06-st3', None, ids=ARG)


# =============================================================================================
# ch07 Short Stories from Diverse Cultures
# =============================================================================================
CULT = ['story_seoul', 'story_market_oaxaca', 'story_lagos_rain', 'newcountry_class', 'lostdog']
H('ch07-st1',
  terms=[('cultural setting', 'the customs, beliefs, language and daily life of the community in which a story is set'),
         ('values', 'the principles and beliefs a community considers important, such as family honour, education or hospitality'),
         ('code-switching', 'moving between languages or ways of speaking depending on the situation'),
         ('loan words', 'words from another language used in a text, such as "hagwon" or "kimbap"')],
  facts=[('In the Seoul story, what is a hagwon?', 'A private after-school cram school', ['A traditional meal', 'A university', 'A type of bus'], 'Hagwon are private academies.'),
         ('Why might a writer leave words like "kimbap" untranslated?', 'To keep the story rooted in its culture and give authenticity', ['Because they forgot the English word', 'To confuse readers', 'Because it is a spelling mistake'], 'Untranslated words convey culture.'),
         ('Which value is most central in the Lagos rain story?', 'Community and hospitality in a crisis', ['Academic competition', 'Wealth and status', 'Military honour'], 'Neighbours shelter together.')],
  why=[('Explain why reading stories from different cultures is valuable.', 'They show different values and ways of life, build empathy and help readers recognise both shared human experiences and cultural differences.'),
       ('Explain why cultural details (food, language, places) matter in a short story.', 'Specific details make the setting authentic and reveal values – a kimbap roll handed over after cram school shows care and expectation.')],
  contrast=[('cultural setting', 'physical setting', 'Physical setting is the place and time (a Seoul street at 11 p.m.); cultural setting is the values, customs and expectations of the community (academic pressure, family honour).')],
  misc=[('Stories from other cultures are only about differences.', 'They often explore universal experiences – family, pressure, belonging – in a specific cultural context.')],
  apply=[('Identify two details that reveal cultural values in the Seoul story and explain what each suggests.', 'Hagwon until 11 p.m. – the importance of education; the university car sticker – status and family comparison.', 4)],
  evaluate=[('Readers need to share a culture to fully understand a story set in it.', ['insiders recognise subtle details and values', 'outsiders may misread'], ['good stories communicate universal emotions', 'outsiders can learn and empathise'], 'Insiders may notice more, but well-written stories allow outsiders to understand and empathise; reading across cultures broadens perspective.')])
pq('ch07-st1', ('C2', 'C3', 'C4'), (1, 5), None, 'culture', ['Explain how the cultural setting shapes the story.',
                                                          'What values of the community are revealed in this extract? Support your answer with evidence.',
                                                          'How does the writer create a sense of cultural setting?'], ids=CULT[:3], crit=CRIT_A)
para('ch07-st1', None, ids=CULT[:3], c='C4', d=(3, 5))
K.dev_mcq('ch07-st1', None, ids=CULT[:3])
pq('ch07-st1', ('C2', 'C3'), (1, 4), None, 'dev', DEV_Q, ids=CULT[:3], crit=CRIT_B)

H('ch07-st2',
  terms=[('first-person narration', 'narration by a character using "I"'),
         ('second-person narration', 'narration using "you", placing the reader in the story'),
         ('third-person limited', 'narration using "he/she" that follows one character\'s thoughts'),
         ('third-person omniscient', 'narration using "he/she" by an all-knowing narrator who can enter any character\'s mind')],
  facts=[('"You wake before the roosters because your grandmother is already grinding corn." This is:', 'second-person narration', ['first-person narration', 'third-person omniscient', 'a stage direction'], '"You" addresses the reader as the character.'),
         ('Which narration lets the reader know every character\'s thoughts?', 'Third-person omniscient', ['First person', 'Third-person limited', 'Second person'], 'Omniscient narrators know all.'),
         ('A limitation of first-person narration is that:', 'the reader only knows what the narrator perceives', ['it cannot show feelings', 'it must be in the future tense', 'it has no dialogue'], 'The perspective is limited.')],
  why=[('Explain why a writer might choose second-person narration.', 'It makes the reader experience events as if they were the character, creating immediacy and empathy.'),
       ('Explain why third-person omniscient narration can create dramatic irony.', 'The narrator can reveal what several characters think, so the reader knows more than any one character.')],
  contrast=[('third-person limited', 'third-person omniscient', 'Third-person limited follows one character\'s thoughts closely; omniscient can move between many characters\' minds and comment on events.')],
  misc=[('Second-person narration is just for instructions.', 'In fiction, second person can create intimacy and immediacy, placing the reader inside the character\'s experience.')],
  apply=[('Rewrite the first sentence of the Oaxaca story in the first person and explain how the effect changes.', '"I wake before the roosters because my grandmother is already grinding corn." The reader now observes the narrator\'s experience rather than living it; it feels more personal to the character but less immediate for the reader.', 3),
         ('Rewrite "I ate the kimbap. It tasted of seaweed and expectation." in third-person limited.', '"She ate the kimbap. It tasted of seaweed and expectation." Credit consistent pronoun and preserved effect.', 1)],
  evaluate=[('First-person narration is the best choice for stories about identity.', ['inner thoughts reveal identity', 'the voice expresses culture and language'], ['second person can involve readers more', 'third person can show how others see the character'], 'First person is powerful for identity, but second and third person offer other insights; the best choice depends on what the story explores.')])
pq('ch07-st2', ('C2', 'C3', 'C4'), (1, 5), None, 'pov', POV_Q, ids=CULT + ['twovoices', 'bench'], crit=CRIT_B)
para('ch07-st2', None, ids=['story_market_oaxaca'], c='C4', d=(3, 5))

H('ch07-st3',
  terms=[('identity', 'a person\'s sense of who they are, shaped by family, culture, language, place and experience'),
         ('belonging', 'the feeling of being accepted and at home in a group or place'),
         ('diaspora', 'people living outside their ancestral homeland'),
         ('heritage', 'traditions, language and culture passed down through generations')],
  facts=[('"By noon you are three people." This metaphor suggests the narrator:', 'has different identities in different languages and roles', ['has two sisters', 'is lost in the market', 'is tired of work'], 'Code-switching creates multiple selves.'),
         ('Samir accepting the name "Sami" shows:', 'a sacrifice of identity in order to fit in', ['pride in his new name', 'that he has forgotten his family', 'that the teacher is kind'], 'He feels diminished.')],
  why=[('Explain why language is closely connected to identity in many stories.', 'The languages we speak carry family history and culture; switching or losing a language can feel like gaining or losing part of oneself.'),
       ('Explain why stories about belonging often involve outsiders.', 'An outsider\'s perspective makes the rules of belonging visible and lets readers feel what exclusion is like.')],
  contrast=[('identity', 'belonging', 'Identity is a person\'s sense of who they are; belonging is the feeling of being accepted by a group. A character can have a strong identity but not belong, or belong by hiding their identity.')],
  misc=[('Belonging means becoming exactly like everyone else.', 'True belonging allows people to be accepted as they are; stories often show the cost of belonging by hiding one\'s identity.')],
  apply=[('Compare how the Oaxaca and Berlin extracts present identity in one or two sentences.', 'E.g. "Both narrators move between languages, but while the Oaxaca narrator finds her true self with her grandmother, Samir hides his identity in silence to fit in."', 2)],
  evaluate=[('It is possible to belong to more than one culture.', ['many people live between languages and traditions', 'the Oaxaca narrator moves between three'], ['people may feel they fully belong nowhere', 'pressure to choose one identity'], 'Many people do belong to several cultures, though this can involve tension; stories show both the richness and the strain of multiple identities.')],
  extended=[('Write a short story (about 500 words) about a character who moves between two cultures or languages, showing a moment of belonging or exclusion.', 'Indicative content: a clear narrative perspective; cultural details; a turning point related to identity; symbolism or motif; controlled structure; accurate language. Criteria B, C, D.', 12, 'long'),
            ('Compare how two short stories you have read present identity and belonging across cultures.', 'Indicative content: two stories; techniques (narration, symbol, language) with evidence; similarities and differences; comparative connectives. Criteria A and B.', 10, 'long')])
pq('ch07-st3', ('C2', 'C3', 'C4'), (1, 5), None, 'identity', ['How does the writer explore identity in this extract?',
                                                           'Explain how the character\'s sense of belonging is presented.',
                                                           'What does this extract suggest about identity and culture? Support your answer with evidence.'], ids=['story_seoul', 'story_market_oaxaca', 'story_lagos_rain'], crit=CRIT_OPEN)
pq('ch07-st3', ('C2', 'C3'), (1, 4), None, 'theme', THEME_Q, ids=CULT, crit=CRIT_OPEN)
para('ch07-st3', None, ids=['newcountry_class', 'story_market_oaxaca', 'story_seoul'], c='C4', d=(3, 5))


# =============================================================================================
# ch08 Satire and Humour
# =============================================================================================
SAT = ['satire_school', 'cartoon_phones', 'parody_ad', 'carroll']
H('ch08-st1',
  terms=[('irony', 'saying or showing the opposite of what is meant or expected'),
         ('verbal irony', 'when a speaker says the opposite of what they mean'),
         ('exaggeration (hyperbole)', 'extreme overstatement for effect'),
         ('understatement', 'deliberately presenting something as less important than it is'),
         ('deadpan', 'a serious, expressionless delivery of something absurd, which increases the humour')],
  facts=[('"Curiosity is a distraction," says the Head of Results. This is an example of:', 'irony', ['onomatopoeia', 'a simile', 'a statistic'], 'A school should value curiosity, so the statement is ironic.'),
         ('"Questions will now be permitted only on Fridays, between 2:14 and 2:16 p.m." This uses:', 'exaggeration', ['understatement', 'personification', 'alliteration'], 'The tiny time slot is absurdly exaggerated.'),
         ('"We spent the night ... nobody mentioning the generator." This is:', 'understatement', ['hyperbole', 'sarcasm', 'onomatopoeia'], 'Forgiveness is shown by saying very little.')],
  why=[('Explain why satirists use a deadpan, serious tone.', 'Presenting absurd ideas as normal makes readers notice the absurdity themselves, which is funnier and more critical.'),
       ('Explain why exaggeration is effective in satire.', 'Pushing a real tendency to an extreme reveals its flaws more clearly – banning thinking exposes a focus on test scores.'),
       ('Explain why understatement can be powerful.', 'Saying less than expected makes readers fill in the meaning, which can make emotion or criticism more striking.')],
  contrast=[('irony', 'sarcasm', 'Irony is a gap between what is said and what is meant or expected; sarcasm is a sharper, often mocking form of verbal irony aimed at a person.'),
            ('exaggeration', 'understatement', 'Exaggeration makes something seem bigger or more extreme than it is; understatement makes it seem smaller or less important. Both create irony.')],
  misc=[('Irony just means a coincidence.', 'Irony is a gap between appearance and reality, or words and meaning; a coincidence is not necessarily ironic.')],
  apply=[('Write an ironic sentence about a school that claims to be "eco-friendly" but prints every email.', 'E.g. "Our eco-friendly school proudly printed 10,000 copies of its new paperless policy." Credit a clear gap between claim and reality.', 2),
         ('Identify the irony in "rich people used them to feel ordinary" from the memory story.', 'The rich buy ordinary, boring memories while the poor sell precious ones, reversing what we expect and exposing inequality.', 2)],
  evaluate=[('Irony is too subtle to be an effective way of criticising society.', ['some readers miss it', 'it can be misread as support'], ['it engages readers to think', 'it exposes hypocrisy memorably'], 'Irony risks being misunderstood, but when signalled clearly it is a powerful, memorable form of criticism.')])
pq('ch08-st1', ('C2', 'C3', 'C4'), (1, 5), None, 'dev', DEV_Q, ids=SAT + ['scifi_memory'], crit=CRIT_B)
K.dev_mcq('ch08-st1', None, ids=SAT)
K.tone_mcq('ch08-st1', None, ids=SAT)
para('ch08-st1', None, ids=['satire_school', 'parody_ad'], c='C4', d=(3, 5))

H('ch08-st2',
  terms=[('satire', 'the use of humour, irony and exaggeration to criticise people, institutions or society'),
         ('target', 'the person, group or idea a satire criticises'),
         ('political cartoon', 'a drawing that comments on current events or society, often using caricature and symbols'),
         ('caricature', 'an exaggerated picture of a person or type for comic effect'),
         ('sketch', 'a short comic scene performed on stage, television or online')],
  facts=[('What is the target of the "School Bans Thinking" article?', 'Schools that value test scores over learning', ['Students who are lazy', 'Parents who travel', 'Science teachers'], 'It mocks exam-focused education.'),
         ('In the cartoon, why is the giant phone wearing a tie?', 'To show it has taken the parent\'s authority', ['Because it is a formal dinner', 'To show the phone is broken', 'To advertise ties'], 'The tie symbolises authority.'),
         ('Which is the main purpose of satire?', 'To criticise through humour', ['To inform neutrally', 'To tell a love story', 'To sell a product'], 'Satire criticises.')],
  why=[('Explain why satire uses humour rather than direct criticism.', 'Humour makes criticism entertaining and memorable, lowers the audience\'s defences and can expose powerful people safely.'),
       ('Explain why cartoons are effective for satire.', 'A single exaggerated image communicates a criticism instantly and can be understood across languages.')],
  contrast=[('satire', 'comedy', 'Comedy aims mainly to entertain; satire uses comedy to criticise a target and encourage change.')],
  misc=[('Satire is just making fun of people.', 'Satire has a serious purpose: it criticises behaviour, institutions or ideas to provoke thought or reform.')],
  apply=[('Describe a satirical cartoon you could draw about too much homework. Explain the target and one visual technique.', 'E.g. a student buried under a mountain of worksheets with only a hand visible, a teacher adding more; target: excessive homework; technique: exaggeration/visual metaphor.', 3),
         ('Explain what the caption "Who\'s in charge here?" adds to the cartoon.', 'It turns the image into a question, inviting viewers to recognise that phones now control family life and to reflect on their own habits.', 2)],
  evaluate=[('Satire can change people\'s behaviour.', ['it exposes hypocrisy and makes people think', 'historical satire has influenced public debate'], ['audiences may laugh without changing', 'people often enjoy satire that confirms their views'], 'Satire can raise awareness and shift attitudes, but it rarely changes behaviour on its own; its power lies in starting conversations.')])
pq('ch08-st2', ('C2', 'C3', 'C4'), (1, 5), None, 'satire', ['Explain how this text uses satire, and identify its target.',
                                                         'What is being criticised in this text, and how does the writer or artist make it funny?',
                                                         'Analyse the satirical techniques used in this text.'], ids=SAT, crit=CRIT_B)
pq('ch08-st2', ('C2', 'C3'), (1, 4), None, 'target', ['Identify the target of the satire and explain how you can tell.'], ids=SAT, crit=CRIT_A)
pq('ch08-st2', ('C2', 'C3'), (1, 4), None, 'visual', VIS_Q, ids=['cartoon_phones', 'parody_ad'], crit=CRIT_B)
write('ch08-st2', ids=['satire_school'])

H('ch08-st3',
  terms=[('parody', 'an imitation of a text, genre or style, exaggerated for comic or critical effect'),
         ('intertextuality', 'the relationship between texts, when one text refers to, borrows from or transforms another'),
         ('allusion', 'a brief reference to another text, person or event'),
         ('pastiche', 'an imitation that celebrates rather than mocks its source')],
  facts=[('Lewis Carroll\'s "How Doth the Little Crocodile" parodies a poem by:', 'Isaac Watts', ['William Shakespeare', 'Wilfred Owen', 'Rupert Brooke'], 'Watts wrote "How doth the little busy bee".'),
         ('Which is an example of intertextuality?', 'A parody advert that twists a famous slogan', ['A news report of a fire', 'A shopping list', 'A timetable'], 'It depends on another text.'),
         ('What is the difference between parody and pastiche?', 'Parody mocks its source; pastiche imitates it affectionately', ['They are the same', 'Pastiche is always about food', 'Parody must rhyme'], 'Purpose differs.')],
  why=[('Explain why parody relies on the audience recognising the original.', 'The humour comes from the gap between the original and the changed version; without recognition, the joke and the criticism are lost.'),
       ('Explain why Carroll chose to parody a moral poem for children.', 'Victorian children had to memorise preachy verse; replacing a virtuous bee with a grinning crocodile mocks such moralising and delights readers who knew the original.')],
  contrast=[('parody', 'allusion', 'A parody imitates the form and style of a whole text to mock it; an allusion is a brief reference to another text without imitating it.')],
  misc=[('Parody is the same as copying.', 'Parody transforms its source for a new purpose – usually humour or criticism – and depends on deliberate changes.')],
  apply=[('Write two lines parodying "Twinkle, twinkle, little star" to comment on social media.', 'E.g. "Scroll, scroll, little thumb, / How I wonder where you\'re from." Credit recognisable original structure and a satirical point.', 2),
         ('Explain how the slogan "Because you\'re worth nothing... until you\'re PERFECT™" uses intertextuality.', 'It alludes to a famous cosmetics slogan and twists it, revealing the hidden message that adverts make people feel inadequate.', 2)],
  evaluate=[('Parody is a lazy form of creativity because it borrows from others.', ['it relies on existing texts', 'it may not create original ideas'], ['transforming a source requires skill and insight', 'many classics are parodies or rewritings'], 'Parody is a sophisticated creative form: it requires understanding the original and transforming it purposefully.')],
  extended=[('Write a parody (about 250 words) of a well-known text type – an advert, a news report or a nursery rhyme – to criticise an aspect of modern life. Then explain your target and techniques in a short commentary.', 'Indicative content: recognisable imitation of conventions; exaggeration and irony; clear target; commentary explaining choices. Criteria C and D; commentary A.', 12, 'long')])
pq('ch08-st3', ('C2', 'C3', 'C4'), (1, 5), None, 'intertext', ['Explain how this text uses parody or intertextual reference.',
                                                            'What original text or genre does this parody, and what is the effect of the changes?',
                                                            'How does the writer rely on the reader\'s knowledge of another text?'], ids=['carroll', 'parody_ad'], crit=CRIT_B)
para('ch08-st3', None, ids=['parody_ad'], c='C4', d=(3, 5))
K.compare('ch08-st3', c='C4', d=(4, 5), only=['satire_school'])


# =============================================================================================
# ch09 Journalism: Features, Interviews and Investigative Writing
# =============================================================================================
JOUR = ['feature_rickshaw', 'interview_chef', 'protest_a', 'protest_b', 'turtles', 'floodnews']
H('ch09-st1',
  terms=[('hard news', 'reporting of recent, important events, focusing on facts and following the inverted pyramid'),
         ('feature article', 'a longer article exploring a topic, person or trend in depth, using description, human interest and a personal style'),
         ('human interest', 'focus on people\'s experiences and emotions to engage readers'),
         ('angle', 'the particular focus or perspective a journalist takes on a story')],
  facts=[('Which opening is typical of a feature rather than hard news?', '"In a workshop no bigger than a parked car, Rafiqul dips a brush into crimson paint."', ['"Police arrested three people on Friday."', '"A fire broke out at 3 a.m. at a factory."', '"The council voted 7–2 to close the library."'], 'Features open with scenes.'),
         ('Which is a feature of hard news?', 'The inverted pyramid', ['A reflective ending', 'Long sensory description', 'First-person anecdotes'], 'Hard news puts key facts first.')],
  why=[('Explain why feature articles often end with an image rather than a fact.', 'Features aim to leave readers with a feeling or reflection; a final image lingers and makes the piece memorable.'),
       ('Explain why features focus on individuals.', 'Telling a wider story through one person\'s experience creates human interest and empathy.')],
  contrast=[('hard news', 'a feature article', 'Hard news reports recent events quickly and objectively using the inverted pyramid; a feature explores a topic in depth with description, human interest, quotation and a more personal, reflective style.')],
  misc=[('Feature articles do not need facts.', 'Features combine description and storytelling with researched facts, context and quotations.')],
  apply=[('Rewrite the opening of the turtle hatching news report as the opening of a feature article.', 'E.g. "At 2 a.m. on Watamu Beach, Amani Mwangi is on her knees in the sand, counting tiny shadows racing for the sea." Credit scene-setting, human focus and sensory detail.', 3)],
  evaluate=[('Feature articles are more valuable than hard news.', ['they give depth and context', 'they build empathy'], ['hard news informs quickly about urgent events', 'features can be subjective'], 'Both are valuable for different purposes: hard news informs quickly, features deepen understanding.')])
pq('ch09-st1', ('C2', 'C3', 'C4'), (1, 5), None, 'feature_vs', ['How can you tell that this is a feature article rather than hard news? Refer to the text.',
                                                             'Explain how this feature article differs from a news report.'], ids=['feature_rickshaw'], crit=CRIT_A)
pq('ch09-st1', ('C2', 'C3'), (1, 4), None, 'dev', DEV_Q, ids=['feature_rickshaw', 'turtles', 'floodnews'], crit=CRIT_B)
K.kind_mcq('ch09-st1', None, ids=['feature_rickshaw', 'turtles', 'floodnews', 'interview_chef', 'filmreview'])
para('ch09-st1', None, ids=['feature_rickshaw'], c='C4', d=(3, 5))
write('ch09-st1', ids=['feature_rickshaw'])

H('ch09-st2',
  terms=[('open question', 'a question that invites a detailed answer, often beginning with how, why or what'),
         ('follow-up question', 'a question that responds to the interviewee\'s answer to explore it further'),
         ('Q&A format', 'a write-up that prints questions and answers in turn'),
         ('direct quotation', 'the exact words of the interviewee, in quotation marks')],
  facts=[('Which is the best open question for an interview with a young chef?', '"How did your grandmother influence the way you cook?"', ['"Do you like cooking?"', '"Is your stall open on Saturdays?"', '"Are you 16?"'], 'It invites a detailed answer.'),
         ('Why does an interview write-up often begin with an introduction?', 'To explain who the interviewee is and why readers should care', ['To list every question', 'To give the interviewer\'s address', 'To summarise the ending'], 'It frames the interview.')],
  why=[('Explain why follow-up questions are important in an interview.', 'They explore interesting answers more deeply and show active listening, producing richer material.'),
       ('Explain why interviewers prepare questions in advance.', 'Research and planning ensure relevant, purposeful questions and a logical order.')],
  contrast=[('a Q&A interview', 'a profile written in prose', 'A Q&A prints questions and answers directly; a prose profile weaves quotations into the journalist\'s own description and narrative.')],
  misc=[('A good interview just lets the interviewee talk with no plan.', 'Good interviews are planned with researched questions but stay flexible for follow-ups.')],
  apply=[('Write five interview questions (with at least three open questions) for a student who has started a successful school club.', 'Credit open questions (how/why/what), a logical order, a follow-up possibility and one question about challenges or advice.', 5),
         ('Turn this answer into a sentence of a prose profile with a direct quotation: "Q: Advice for other teens? A: Start small. Burn things. Try again."', 'E.g. "Her advice for other teenagers is simple: \'Start small. Burn things. Try again.\'"', 2)],
  evaluate=[('The interviewer is as important as the interviewee.', ['questions shape answers', 'editing shapes the final text'], ['readers want the interviewee\'s voice', 'interviewers should not dominate'], 'The interviewer shapes the interview through questions and editing, but should foreground the interviewee\'s voice.')],
  extended=[('Interview a family member or friend about a significant experience and write it up as a feature (about 400 words) with an introduction and quotations.', 'Indicative content: introduction framing the person; a clear angle; open-question material; embedded quotations; descriptive detail; reflective ending. Criteria B, C, D.', 12, 'long')])
pq('ch09-st2', ('C2', 'C3', 'C4'), (1, 5), None, 'struct', STRUCT_Q, ids=['interview_chef', 'podcast_qa'] if False else ['interview_chef'], crit=CRIT_B)
qa('ch09-st2', 'C3', (1, 4), None, ids=['interview_chef'])
write('ch09-st2', ids=['interview_chef'])
pq('ch09-st2', ('C2', 'C3'), (1, 4), None, 'dev', DEV_Q, ids=['interview_chef', 'feature_rickshaw'], crit=CRIT_B)
para('ch09-st2', None, ids=['interview_chef'], c='C4', d=(3, 5))

H('ch09-st3',
  terms=[('representation', 'the way the media presents people, groups or events, which constructs a version of reality'),
         ('framing', 'how a story is presented – the angle, headline and emphasis – which shapes how readers interpret it'),
         ('selection and omission', 'the choice of what to include and what to leave out of a report'),
         ('bias', 'a one-sided presentation that favours a particular view'),
         ('agenda', 'the underlying aims or interests of a publication')],
  facts=[('Report A quotes only an annoyed commuter. This shows:', 'selective quotation that creates bias', ['balanced reporting', 'a neutral headline', 'an interview'], 'Choosing whom to quote shapes the story.'),
         ('Report B uses the organisers\' figure of 12,000 in its headline. This is an example of:', 'framing', ['onomatopoeia', 'a lead paragraph only', 'a feature'], 'Choice of figure frames the protest.'),
         ('What do both protest reports agree on?', 'There were three arrests', ['The exact number of protesters', 'Whether the protest was peaceful', 'Who should be quoted'], 'Both mention three arrests.')],
  why=[('Explain why the same event can be represented differently by different publications.', 'Publications have different audiences and agendas; selection, headlines, quotations and order frame the event to suit them.'),
       ('Explain why the order of information affects representation.', 'Readers give most weight to the headline and opening; placing arrests first or last changes the impression of a protest.'),
       ('Explain why media literacy matters for teenagers.', 'Recognising framing and bias helps young people compare sources and form their own judgements rather than accepting one representation.')],
  contrast=[('representation', 'reality', 'Reality is the event itself; representation is a constructed version shaped by selection, framing and language. Every report is a representation.')],
  misc=[('If a report contains only true facts, it represents the event fairly.', 'True facts can still be selected and arranged to create a one-sided representation.'),
        ('Youth news sites are always more biased than national newspapers.', 'Any outlet can be biased; readers should analyse each report\'s selection, framing and language.')],
  apply=[('Rewrite the headline "STUDENTS BRING CITY TO STANDSTILL" so that it is more neutral.', 'E.g. "Thousands of Students March Across Main Bridge in Climate Protest". Credit removal of loaded framing.', 2),
         ('List three choices that make Report A represent the protest negatively.', 'Headline about "standstill"; focus on skipped lessons and traffic; only a critic quoted; police estimate given last. Any three.', 3)],
  evaluate=[('Bias in the news is unavoidable, so readers should not worry about it.', ['all reporting involves selection', 'perfect neutrality is impossible'], ['some reports are far more balanced than others', 'bias can mislead and polarise'], 'Some bias is unavoidable, which is exactly why readers should compare sources and analyse framing.')],
  extended=[('Compare how two news reports represent the same event. Analyse headlines, selection of facts, quotations and language, and evaluate which is more balanced.', 'Indicative content: specific comparison of headlines, quotations, order and word choice; analysis of effects; reasoned judgement. Criteria A and B.', 12, 'long')])
K.compare('ch09-st3', d=(3, 5), only=['protest_a', 'bus_1955'])
K.compare_short('ch09-st3', c='C3', d=(2, 4), only=['protest_a'])
pq('ch09-st3', ('C2', 'C3', 'C4'), (1, 5), None, 'represent', ['How does this report represent the protesters? Refer to headline, quotations and word choice.',
                                                            'Analyse how the report frames the event.',
                                                            'Is this report balanced? Explain with reference to the text.'], ids=['protest_a', 'protest_b', 'skate_a', 'skate_b'] if False else ['protest_a', 'protest_b'], crit=CRIT_B)
pq('ch09-st3', ('C2', 'C3'), (1, 4), None, 'facts_op', ['Identify one fact and one opinion in this report and explain the difference.'], ids=['protest_a', 'protest_b', 'turtles', 'floodnews'], crit=CRIT_A)


# =============================================================================================
# ch10 Science Fiction and Speculative Futures
# =============================================================================================
SF = ['scifi_memory', 'scifi_mars', 'robotdog']
H('ch10-st1',
  terms=[('science fiction', 'a genre that imagines the effects of science and technology on society, often set in the future or on other worlds'),
         ('speculative fiction', 'fiction that asks "what if?" about alternative realities, including science fiction, dystopia and fantasy'),
         ('world-building', 'the creation of a believable imaginary world, including its technology, society, rules and history'),
         ('novum', 'the new invention or idea at the heart of a science-fiction story (e.g. selling memories)')],
  facts=[('Which detail is most typical of science fiction?', 'An invented technology in a future society', ['A talking fox who teaches a moral', 'A knight on a quest for a dragon', 'A detective in Victorian London'], 'Science fiction centres on science and technology.'),
         ('Who wrote "The War of the Worlds" (1898), an early science-fiction novel?', 'H. G. Wells', ['Edgar Allan Poe', 'Lewis Carroll', 'Wilfred Owen'], 'Wells is a founding figure of the genre.'),
         ('In the memory story, what is the "novum"?', 'The ability to sell memories', ['The rent', 'A paper crown', 'The year 2087 alone'], 'The new technology drives the story.')],
  why=[('Explain why science-fiction writers often reveal their world gradually.', 'Gradual details let readers discover the world through characters\' normal lives, which is more natural and intriguing than long explanations.'),
       ('Explain why science fiction often comments on the present.', 'Imagined futures exaggerate current trends (inequality, technology, climate) so readers can see them more clearly.')],
  contrast=[('science fiction', 'fantasy', 'Science fiction explains its strange elements through science and technology (possible in theory); fantasy uses magic and the supernatural.')],
  misc=[('Science fiction is only about aliens and spaceships.', 'Much science fiction focuses on human questions – memory, inequality, belonging – using technology as a starting point.')],
  apply=[('Write three sentences that build a science-fiction world through a character\'s everyday routine, without explaining the technology directly.', 'Credit details that imply a different world (e.g. "Mira scanned her breakfast for its carbon score before her mother would let her eat it.").', 3),
         ('Identify two pieces of world-building in the Mars extract and explain what each suggests.', 'Hope has never felt rain – Mars has no weather; walking without helmets seems dangerous to her – the colony depends on technology to survive.', 4)],
  evaluate=[('Good world-building matters more than characters in science fiction.', ['the world makes the genre distinctive', 'readers enjoy exploring new worlds'], ['readers need characters to care about', 'world-building is most effective through characters\' experience'], 'Strong science fiction needs both; the best world-building is revealed through characters whose lives make the world meaningful.')])
pq('ch10-st1', ('C2', 'C3', 'C4'), (1, 5), None, 'scifi', ['Identify the science-fiction conventions in this extract and explain their effect.',
                                                         'How can you tell that this is science fiction? Refer to two features.'], ids=SF[:2], crit=CRIT_A)
pq('ch10-st1', ('C2', 'C3'), (1, 4), None, 'world', ['Explain how the writer builds a believable world in very few words.',
                                                   'How does the writer reveal the world of the story through details?'], ids=SF[:2], crit=CRIT_B)
K.dev_mcq('ch10-st1', None, ids=SF[:2])
para('ch10-st1', None, ids=SF[:2], c='C4', d=(3, 5))

H('ch10-st2',
  terms=[('ethics', 'questions about what is morally right or wrong'),
         ('the human condition', 'the essential experiences of being human – identity, memory, love, mortality, belonging'),
         ('cautionary tale', 'a story that warns readers about a danger'),
         ('artificial intelligence', 'computer systems designed to perform tasks that normally require human intelligence')],
  facts=[('What ethical question does the memory story raise?', 'Should people be allowed to sell parts of their identity?', ['Should Mars be colonised by 2087?', 'Is kimbap healthy?', 'Should schools ban phones?'], 'The story questions selling memories.'),
         ('Which story is often called the first science-fiction novel and explores the ethics of creating life?', 'Frankenstein (Mary Shelley, 1818)', ['Romeo and Juliet', 'Treasure Island', 'Oliver Twist'], 'Frankenstein asks what responsibility creators have.')],
  why=[('Explain why science fiction is useful for exploring ethical questions.', 'Imagined technologies create situations not yet possible, letting readers test moral questions before they happen.'),
       ('Explain why many science-fiction stories are cautionary tales.', 'By showing the harmful consequences of unchecked technology or power, they warn readers about present-day trends.')],
  contrast=[('a cautionary tale', 'a utopian story', 'A cautionary tale warns of dangers (e.g. technology that erodes identity); a utopian story imagines an ideal society.')],
  misc=[('Science fiction always presents technology as bad.', 'Science fiction explores both the benefits and dangers of technology; many stories are hopeful or balanced.')],
  apply=[('Explain how the robot-pet advertisement and the memory story both raise questions about technology and what it means to be human.', 'The robot pet replaces human companionship; the memory market turns identity into a product. Both ask whether technology can replace things that make us human – relationships and memories.', 3)],
  evaluate=[('Science fiction teaches us more about the present than the future.', ['it exaggerates current trends', 'its fears reflect its own time'], ['some works predict real technologies', 'it imagines genuinely new possibilities'], 'Science fiction speaks to both, but its greatest value is often in helping readers see present choices more clearly.')],
  extended=[('"Science fiction is a warning, not a prediction." Discuss with reference to at least one science-fiction text you have read.', 'Indicative content: defines the claim; analyses how a text warns (technology, ethics, human cost); considers predictive elements; judgement. Criteria A and B.', 12, 'long')])
pq('ch10-st2', ('C2', 'C3', 'C4'), (1, 5), None, 'ethics', ['What ethical question does this extract raise? Support your answer with evidence.',
                                                         'How does the writer use technology to explore what it means to be human?',
                                                         'Explain the warning this extract might be giving its readers.'], ids=SF[:2], crit=CRIT_OPEN)
pq('ch10-st2', ('C2', 'C3'), (1, 4), None, 'theme', THEME_Q, ids=SF[:2], crit=CRIT_OPEN)
pq('ch10-st2', 'C3', (2, 4), None, 'read', ['How might different readers respond to this advertisement? Explain two possible readings.'], ids=['robotdog'], crit=CRIT_OPEN)

H('ch10-st3',
  terms=[('speculative premise', 'the "what if?" idea at the centre of a speculative story'),
         ('exposition', 'background information the reader needs to understand the story'),
         ('show, don\'t tell (world-building)', 'revealing the rules of a world through characters\' actions and details rather than explanation')],
  facts=[('Which is the best "what if?" premise for a speculative story?', '"What if everyone\'s lifespan was displayed on their wrist from birth?"', ['"What if I went to school?"', '"What if it rained?"', '"What if my friend was late?"'], 'It imagines a world-changing idea.'),
         ('Which opening reveals the world most effectively?', '"Lin sold her seventh birthday to pay the rent."', ['"In the future, technology lets people sell memories. This is how it works..."', '"Science fiction is a genre."', '"There was a girl."'], 'It shows the world through action.')],
  why=[('Explain why a speculative story should focus on one premise.', 'A single strong idea can be explored deeply in a short story; too many inventions confuse readers.'),
       ('Explain why long exposition can weaken a speculative story.', 'Explaining everything slows the pace; readers engage more when they infer the world from details.')],
  misc=[('A speculative story must be set hundreds of years in the future.', 'Speculative stories can be set in the near future or an alternative present; what matters is the "what if?" premise.')],
  apply=[('Write a "what if?" premise and a one-sentence opening that shows the world through a character.', 'E.g. Premise: "What if dreams could be recorded and sold?" Opening: "Amira\'s best nightmare paid for her school trip." Credit premise + showing.', 2),
         ('Plan a speculative short story: premise, protagonist, conflict, a detail of world-building and an ending that reveals a cost.', 'Any coherent plan with all five elements; the ending should link to an ethical or human cost.', 5)],
  evaluate=[('A speculative story is more effective if the technology is explained scientifically.', ['explanation makes it believable', 'readers enjoy detail'], ['human consequences matter more than mechanics', 'over-explanation slows the story'], 'Some plausibility helps, but focusing on human consequences is usually more effective than technical explanation.')],
  extended=[('Write a speculative short story (about 500 words) based on a "what if?" question about technology, society or the environment.', 'Indicative content: clear premise; economical world-building; protagonist with a conflict; ethical question; deliberate structure with a revealing ending; accurate, varied language. Criteria B, C, D.', 12, 'long')])
write('ch10-st3', ids=['scifi_memory'])
K.prompts('ch10-st3', 'one', c='C4', d=(3, 5))
K.prompts('ch10-st3', 'plan', c='C3', d=(2, 4))
pq('ch10-st3', 'C3', (2, 4), None, 'world', ['Identify how the writer builds the world in this extract, and use the same technique in a sentence of your own speculative story.'], ids=SF[:2], crit=CRIT_B)


# =============================================================================================
# ch11 Comparative Analysis Skills (MYP 5 eAssessment Task 1 style)
# =============================================================================================
H('ch11-st1',
  terms=[('annotation', 'notes and highlights on a text identifying features, effects and links'),
         ('unseen extract', 'a passage you have not studied before'),
         ('first reading / second reading', 'a first reading for overall meaning, then a second for close analysis of language and structure'),
         ('point of comparison', 'a shared aspect (theme, technique, tone) used to compare two texts')],
  facts=[('What should you look for first when annotating two unseen extracts?', 'The purpose, audience and overall meaning of each', ['The number of commas', 'The font size', 'The author\'s birthday'], 'Understand before analysing.'),
         ('Which annotation is most useful for comparison?', '"Both use first person – A for fear, B for defiance."', ['"Nice word."', '"Long sentence."', '"Text A."'], 'It links the texts.')],
  why=[('Explain why annotating both texts for the same features helps comparison.', 'Looking for the same features (tone, imagery, structure) in both makes it easy to see similarities and differences.'),
       ('Explain why you should annotate effects, not just techniques.', 'The effect on the reader is what you will analyse; noting it while annotating saves time and keeps the focus on meaning.')],
  contrast=[('annotating', 'summarising', 'Annotating identifies features and their effects in the text; summarising restates the main content in your own words.')],
  misc=[('You should annotate every word in an unseen extract.', 'Select the most significant features linked to the question; over-annotating wastes time and hides key points.')],
  apply=[('Write three annotations comparing the openings of the Gothic house extract and the mirror story.', 'E.g. both first person; A uses dramatic setting (fog "like a shroud"), B uses a casual voice ("He\'s probably right"); both end on a chilling short line. Credit comparative links.', 3)],
  evaluate=[('Planning time in a comparison task is wasted time.', ['writing time is limited', 'some students think better while writing'], ['planning ensures balanced, organised comparison', 'it prevents running out of points'], 'Brief, focused planning improves organisation (criterion B) and usually saves time overall.')],
  extended=[('Annotate two unseen extracts on a shared theme and write a comparative plan with a thesis and three points of comparison.', 'Indicative content: annotations on both texts; thesis linking them; three points of comparison each with evidence from both texts. Criteria A and B.', 8, 'long')])
K.compare_short('ch11-st1', c=('C2', 'C3'), d=(1, 4))
K.compare('ch11-st1', c='C4', d=(3, 5), frames=['{q} First list three annotations for each text, then write a comparative paragraph.', '{q}'])
pq('ch11-st1', ('C2', 'C3'), (1, 4), LIT, 'struct', STRUCT_Q, crit=CRIT_B)
K.dev_mcq('ch11-st1', LIT)
K.vocab('ch11-st1', kinds=None)

H('ch11-st2',
  terms=[('comparative connective', 'a word or phrase that links ideas across texts: similarly, likewise, both, whereas, however, in contrast, on the other hand'),
         ('point-by-point structure', 'organising a comparison so that each paragraph discusses one point in both texts'),
         ('block structure', 'writing about one text fully, then the other'),
         ('comparative thesis', 'a statement of the main similarity and difference between the texts')],
  facts=[('Which connective signals similarity?', 'Likewise', ['Whereas', 'However', 'In contrast'], '"Likewise" shows similarity.'),
         ('Which structure usually produces the strongest comparison?', 'Point-by-point (integrated)', ['Writing only about Text A', 'Block structure with no links', 'A list of quotations'], 'Integrated comparison sustains links.'),
         ('Which is a comparative thesis?', '"Both texts present war\'s impact on young men, but whereas Pope glorifies it, Owen exposes its horror."', ['"Text A is a poem."', '"I prefer Text B."', '"Text B was written in 1917."'], 'It states similarity and difference.')],
  why=[('Explain why comparative connectives are important.', 'They make the relationships between the texts explicit, showing the examiner that you are comparing rather than writing two separate analyses.'),
       ('Explain why a point-by-point structure is often more effective than block structure.', 'It keeps both texts in view throughout, so similarities and differences are analysed directly in each paragraph.')],
  contrast=[('point-by-point structure', 'block structure', 'Point-by-point discusses both texts within each paragraph around a shared point; block structure discusses all of Text A, then all of Text B, with comparison mainly at the end.')],
  misc=[('Using "both" at the start of every sentence makes a comparison effective.', 'Effective comparison varies connectives and analyses why the similarity or difference matters.')],
  apply=[('Rewrite these two sentences as one comparative sentence: "Text A uses a sporting metaphor. Text B uses similes of old beggars."', 'E.g. "Whereas Text A presents war through a sporting metaphor, Text B degrades soldiers with similes of \'old beggars\', revealing opposite attitudes."', 2),
         ('Organise these points into a point-by-point plan: tone of both poems; imagery in both poems; form of both poems.', 'Para 1: tone – Pope jaunty vs Owen bitter; Para 2: imagery – game metaphor vs degrading similes; Para 3: form – bouncing rhyme vs heavy rhythm and caesuras.', 3)],
  evaluate=[('Similarities between texts are less interesting than differences.', ['differences reveal contrasting perspectives', 'contrast is vivid'], ['similarities can reveal shared methods or contexts', 'similarities make differences meaningful'], 'Both matter: similarities establish common ground that makes differences significant.')])
K.compare('ch11-st2', c='C4', d=(3, 5), frames=['{q} Use a point-by-point structure and at least four different comparative connectives.',
                                                '{q} Begin with a comparative thesis.'])
K.compare_short('ch11-st2', c=('C2', 'C3'), d=(1, 4))
para('ch11-st2', LIT, c='C3', d=(2, 4), frames=['{gq} Write a topic sentence for a comparative paragraph that could link this text to another text you know on a similar theme.'])

H('ch11-st3',
  terms=[('effect on the reader', 'the thoughts or feelings a writer\'s choice creates in the reader'),
         ('audience response', 'how a particular audience might react to a text, influenced by its context and values'),
         ('tentative language', 'phrases such as "perhaps", "this may suggest" that show awareness of more than one interpretation')],
  facts=[('Which sentence best comments on effect?', '"The fragment \'Towards me.\' makes the reader feel trapped with the narrator."', ['"There is a fragment."', '"The text has 70 words."', '"The writer is good."'], 'It explains the reader\'s response.'),
         ('Why use tentative language such as "perhaps"?', 'To show awareness that texts can be interpreted in more than one way', ['To show you are unsure of the answer', 'Because it is required in every sentence', 'To make your answer longer'], 'It signals thoughtful interpretation.')],
  why=[('Explain why different audiences might respond differently to the same text.', 'Readers bring different experiences, values and contexts; a 1915 reader of Pope might feel patriotic, a modern reader may feel uneasy.'),
       ('Explain why commenting on effect is essential in analysis.', 'Criterion A asks how choices create meaning and effects; naming a technique without effect shows little understanding.')],
  contrast=[('the intended effect', 'the actual response', 'The intended effect is what the writer seems to want readers to feel; the actual response may differ depending on the reader\'s context and values.')],
  misc=[('"It makes the reader want to read on" is a strong comment on effect.', 'It is too general; strong comments explain the specific feeling or thought created and why.')],
  apply=[('Improve this comment on effect: "The simile makes it more interesting." Quotation: "like old beggars under sacks".', 'E.g. "The simile shocks the reader by ageing and degrading young soldiers, making us question the heroic image of war we may have been taught."', 2),
         ('Explain how a reader in 1915 and a reader today might respond differently to the Daddy recruitment poster.', '1915: guilt, pressure to enlist and patriotic duty; today: awareness of manipulation and the horror of the war, so the poster may seem disturbing.', 3)],
  evaluate=[('A text means whatever the reader feels it means.', ['readers bring personal contexts', 'responses vary legitimately'], ['interpretations need textual evidence', 'writers\' choices guide meaning'], 'Reader response is important, but convincing interpretations are grounded in the text\'s evidence and context.')])
pq('ch11-st3', ('C2', 'C3', 'C4'), (1, 5), LIT, 'dev', ['Explain the effect of "{quote}" on the reader, and how a different reader might respond.',
                                                    'How does "{quote}" shape the reader\'s response to the text?'], crit=CRIT_B)
pq('ch11-st3', ('C3', 'C4'), (2, 5), None, 'read', ['Suggest how two different audiences might respond to this text, explaining why.'], ids=['robotdog'], crit=CRIT_OPEN)
pq('ch11-st3', ('C3', 'C4'), (2, 5), None, 'persp', ['How might a reader in 1915 and a reader today respond differently to this text? Refer to specific details.'], ids=WAR + ['daddy_poster'], crit=CRIT_OPEN)
K.compare('ch11-st3', c='C4', d=(4, 5), frames=['{q} In your answer, comment on the effect each text has on its audience.'])


# =============================================================================================
# ch12 Creative Writing from Visual Prompts and Timed Practice
# =============================================================================================
H('ch12-st1',
  terms=[('visual prompt', 'an image used as a stimulus for creative writing'),
         ('mood', 'the feeling an image or piece of writing creates'),
         ('perspective', 'whose point of view the piece is told from'),
         ('subtext (in an image)', 'what an image suggests beyond what it literally shows')],
  facts=[('When interpreting an image prompt, what should you consider first?', 'The mood, possible stories and perspectives it suggests', ['The camera that took it', 'Its file size', 'How many colours it has'], 'Interpretation drives creativity.'),
         ('Which response to an image of an empty swing in fog is most original?', 'A story told by the swing itself, waiting for a child who has grown up', ['"There is a swing. It is foggy."', 'A list of playground equipment', 'A weather report'], 'An unusual perspective shows insight.')],
  why=[('Explain why it is useful to brainstorm several story ideas from one image.', 'The first idea is often the most obvious; generating several lets the writer choose the most original and developed.'),
       ('Explain why the perspective you choose matters.', 'Perspective shapes what the reader knows and feels; an unusual viewpoint can transform a simple image.')],
  contrast=[('the literal content of an image', 'its suggested meaning', 'The literal content is what is shown (a swing, fog); the suggested meaning is what it implies (absence, memory, loss).')],
  misc=[('You must use every detail in the image.', 'Use the details that serve your idea; the image is a starting point, not a checklist.'),
        ('The mood of your piece must match the image exactly.', 'You can work with or against the image\'s mood – contrast can be powerful (a happy memory in a bleak setting).')],
  apply=[('Look at this image: a moving van outside a block of flats at dawn; a child presses a hand against the van\'s window. Suggest three perspectives you could write from and the story each would tell.', 'E.g. the child leaving (loss, hope); a friend watching from a balcony (abandonment); the van driver (an outsider noticing the moment). Credit three distinct perspectives with stories.', 3)],
  evaluate=[('The best creative responses to images ignore the obvious interpretation.', ['originality is rewarded', 'unexpected angles engage readers'], ['an obvious idea, well executed, can be powerful', 'forced originality can feel artificial'], 'Originality helps, but execution matters most; a familiar idea told with insight and control can outperform a strange but weak one.')])
K.prompts('ch12-st1', 'interpret', c=('C2', 'C3'), d=(1, 4))
K.prompts('ch12-st1', 'plan', c=('C3', 'C4'), d=(2, 5))
K.prompts('ch12-st1', 'open', c='C4', d=(3, 5))

H('ch12-st2',
  terms=[('dialogue', 'characters\' spoken words, used to reveal character, move the plot and vary pace'),
         ('description', 'language that creates a vivid picture of setting, character or action'),
         ('narrative structure', 'the shape of a story: exposition, rising action, climax, resolution'),
         ('flashback', 'a scene that interrupts the present to show an earlier event'),
         ('circular structure', 'a story that ends where it began, often with a changed meaning')],
  facts=[('In a 400–600 word story, how many main characters is usually best?', 'One or two', ['Six or more', 'None', 'Ten'], 'Short pieces need focus.'),
         ('Which is correctly punctuated dialogue?', '"I\'m not going," she said.', ['"I\'m not going" she said.', 'I\'m not going, "she said."', '"I\'m not going." She said.'], 'Comma inside speech marks before the reporting clause.'),
         ('What is a circular structure?', 'A story that ends where it began', ['A story with no ending', 'A story told backwards', 'A story with many narrators'], 'Returning to the opening shows change.')],
  why=[('Explain why dialogue should be used sparingly in a short piece.', 'Too much dialogue can slow the story; a few well-chosen lines reveal character and conflict efficiently.'),
       ('Explain why a flashback can be effective in a short story.', 'It reveals important background or motivation at a key moment, adding depth without a long chronological build-up.'),
       ('Explain why a word limit affects structural choices.', 'With limited words, writers must focus on one key moment and choose a structure (e.g. in medias res, circular) that maximises impact.')],
  contrast=[('a linear structure', 'a non-linear structure', 'A linear structure tells events in chronological order; a non-linear structure uses flashbacks, flash-forwards or fragmented order for effect.')],
  misc=[('A short story needs lots of plot events to be interesting.', 'Short stories work best focused on one key moment or change, developed in depth.')],
  apply=[('Write a short exchange of dialogue (four lines) that reveals tension between two siblings, correctly punctuated.', 'Credit correct speech punctuation, new line for each speaker and subtext revealing tension.', 3),
         ('Plan a 500-word story using a circular structure, inspired by an image of a lighthouse in a storm.', 'E.g. opens and closes with the beam sweeping the sea; middle: the keeper\'s rescue attempt; the final image changes meaning (the boat is now safe, or the keeper is gone). Credit circularity and changed meaning.', 3)],
  evaluate=[('Description is more important than dialogue in creative writing.', ['description builds setting and mood', 'examiners reward vivid language'], ['dialogue reveals character and creates pace', 'balance is key'], 'Both are important; a balanced piece uses description for atmosphere and dialogue for character and conflict.')],
  extended=[('Write a narrative of 400–600 words inspired by an image of a robot vacuum cleaner stuck against a door in a dark flat. Use a deliberate structure and at least one passage of dialogue.', 'Indicative content: an imaginative interpretation; consistent perspective; deliberate structure (e.g. circular, in medias res); purposeful dialogue; vivid description; accurate punctuation of speech. Criteria B, C, D.', 16, 'long')])
K.prompts('ch12-st2', 'write', c='C4', d=(3, 5))
K.prompts('ch12-st2', 'one', c=('C3', 'C4'), d=(2, 5))
pq('ch12-st2', ('C2', 'C3'), (1, 4), PROSE, 'struct', ['Explain how {feature} shapes this narrative, and how you could use a similar structural choice in your own writing.'], crit=CRIT_B)

R.mcqs('ch12-st3', 'C1', (1, 3), [
    ('Which MYP criterion assesses insight, imagination and stylistic choices?', 'Criterion C: Producing text', ['Criterion A: Analysing', 'Criterion B: Organising', 'Criterion D: Using language'], 'Criterion C covers creativity and style.'),
    ('Which criterion assesses vocabulary, register and accuracy?', 'Criterion D: Using language', ['Criterion A: Analysing', 'Criterion B: Organising', 'Criterion C: Producing text'], 'Criterion D covers language use.'),
    ('In the MYP 5 eAssessment, how long is the Language and literature on-screen exam?', '2 hours', ['45 minutes', '4 hours', '30 minutes'], 'The exam lasts 2 hours.'),
    ('What is the recommended length of the Task 2 creative piece in the MYP 5 eAssessment?', '400–600 words', ['50–100 words', '1,500–2,000 words', '3,000 words'], 'Task 2 asks for 400–600 words.'),
    ('In timed writing, when should you plan?', 'Briefly before writing, using a few minutes', ['Never', 'After writing', 'For half of the time'], 'A short plan improves organisation.'),
])
H('ch12-st3',
  terms=[('self-assessment', 'judging your own work against the assessment criteria to identify strengths and targets'),
         ('timed writing', 'writing a response within a fixed time, as in an exam'),
         ('proofreading', 'checking for errors in spelling, punctuation and grammar'),
         ('target', 'a specific, achievable goal for improvement')],
  why=[('Explain why practising timed writing improves exam performance.', 'It builds speed, helps students judge how long planning, writing and checking take, and reduces anxiety.'),
       ('Explain why self-assessment against the criteria is useful.', 'It helps students understand what each band requires and identify specific targets for improvement.')],
  contrast=[('a strength', 'a target', 'A strength is what the writing already does well (e.g. vivid sensory detail); a target is a specific improvement to make next time (e.g. vary sentence openings).')],
  misc=[('Proofreading is not worth the time in an exam.', 'Even a few minutes of proofreading can correct errors that lower criterion D marks.'),
        ('A vague target such as "write better" helps improvement.', 'Effective targets are specific and linked to criteria (e.g. "use at least three different sentence structures for effect").')],
  apply=[('Write two specific targets for a student whose story has a strong idea but lots of comma splices and a rushed ending.', 'E.g. (D) "Use full stops or semicolons between independent clauses"; (B) "Plan the ending in advance and give it at least one paragraph."', 2),
         ('Plan how you would divide 60 minutes for a creative writing task of 400–600 words.', 'E.g. 5–8 minutes interpreting the prompt and planning; 40–45 minutes writing; 5–10 minutes proofreading and editing.', 3),
         ('Proofread and correct: "Its been raining all day, me and Sam was stuck inside, we was bored."', '"It\'s been raining all day; Sam and I were stuck inside and we were bored." – it\'s; comma splices; "Sam and I"; "were".', 4)],
  evaluate=[('Timed practice is the best way to prepare for the eAssessment.', ['it builds exam stamina and timing', 'it mirrors real conditions'], ['skills must first be developed without time pressure', 'feedback and reflection matter as much'], 'Timed practice is essential near the exam, but it works best combined with untimed skill-building and feedback.')],
  extended=[('Under timed conditions (45 minutes), write a piece of 400–600 words inspired by an image of a hospital corridor at 3 a.m. Then write a short self-assessment against criteria B, C and D.', 'Indicative content: a focused, imaginative piece with deliberate structure and style; accurate language; a self-assessment identifying one strength and one target per criterion. Criteria B, C, D.', 16, 'long')])
write('ch12-st3', kinds=None)
K.prompts('ch12-st3', 'write', c='C4', d=(3, 5))

# --- extra C2/C3 coverage for thinner cells ---
pq('ch03-st4', 'C3', (2, 4), None, 'dev', ['A director wants to film this extract. Pick one technique in "{quote}" and explain how a camera shot or sound effect could bring out the same effect.',
   'Explain what a film adaptation might gain or lose when it shows, rather than tells, the moment in "{quote}".'], ids=RJ, crit=CRIT_OPEN)
pq('ch05-st4', 'C3', (2, 4), None, 'aud', AUD_Q, ids=['filmreview', 'bookreview', 'trailer'], crit=CRIT_B)
pq('ch06-st2', 'C3', (2, 4), None, 'purp', PURP_Q, ids=ARG, crit=CRIT_B)
pq('ch07-st3', 'C3', (2, 4), None, 'dev', ['Explain how "{quote}" suggests something about the character\'s sense of belonging.',
   'How does the detail "{quote}" connect the character to a place or culture?'], ids=CULT, crit=CRIT_A)
pq('ch08-st3', 'C3', (2, 4), None, 'tone', TONE_Q, ids=SAT, crit=CRIT_A)
pq('ch10-st1', 'C3', (2, 4), None, 'dev', DEV_Q, ids=SF, crit=CRIT_B)
pq('ch10-st2', 'C3', (2, 4), None, 'dev', ['Explain how "{quote}" makes the reader think about the effect of technology on people.',
   'What does "{quote}" suggest about the relationship between humans and machines?'], ids=SF, crit=CRIT_A)
pq('ch10-st3', 'C2', (1, 3), None, 'dev', DEV_Q, ids=SF + GIDS[:3], crit=CRIT_B)
pq('ch10-st3', 'C2', (1, 3), None, 'world', ['Name one detail the writer uses to show the reader that this world is different from ours.',
   'Explain how one small detail in this extract builds the setting.'], ids=SF, crit=CRIT_B)
pq('ch12-st3', 'C3', (2, 4), LIT | NONLIT, 'dev', ['You have 10 minutes. Write one analytical paragraph (point, evidence, explanation) about "{quote}", then say which criterion it most clearly meets.',
   'Annotate "{quote}" with two techniques and their effects, then rate your annotation against criterion A (0-8) with a reason.'], crit=CRIT_ALL)
pq('ch07-st3', 'C3', (2, 4), None, 'char', CHAR_Q, ids=CULT + NOVEL, crit=CRIT_A)
pq('ch07-st2', ('C3', 'C4'), (2, 5), None, 'pov', POV_Q, ids=CULT + GIDS + SF[:2], crit=CRIT_A)
