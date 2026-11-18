"""IB MYP 3 Language and Literature (English) – ib-g8-english.

MYP 3 has no external exam: school-designed summative tasks are assessed on criteria A Analysing, B Organising,
C Producing text and D Using language (each 0-8). Mocks mirror the MYP 5 on-screen eAssessment so students practise
it early: Task 1 analysis and comparison of two extracts, Task 2 creative writing from visual prompts.

Item styles: C1 terminology and recognition (devices, text types, tone, language in context); C2 explain /
distinguish / correct a misconception; C3 reading, inference and writer's-effects questions on ORIGINAL short
passages written for this bank; C4 analytical paragraphs (PEE), comparison, directed writing and composition keyed
to criteria A-D. Myths are retold in our own words; the only quotations are brief public-domain lines (attributed).
Shared builders and the shared passage library: ib_myp_english_common.py.
"""
from __future__ import annotations

from _common import F, Registry, T, mcq  # noqa: F401
from ib_myp_english_common import (AUD_Q, CHAR_Q, CRIT_A, CRIT_ALL, CRIT_AN, CRIT_B, CRIT_CR, CRIT_OPEN, CRIT_W, DEV_Q,  # noqa: F401
                                   KCONV_Q, LIFE, LIT, MEDIA, MOOD_Q, NARR, NONLIT, PERSUADE, POV_Q, PROSE, PURP_Q, STRUCT_Q,
                                   STYLE, SUM_Q, THEME_Q, TONE_Q, VIS_Q, VISUAL, Kit, add_shared, mock_sections)

CONFIG = {'minutesPerMark': 1.5, 'mcqMinutes': 1.5}

# MYP 5 eAssessment-style mock (practised early): Task 1 analysis 30 marks; Task 2 creative writing (50 marks on the
# real paper) scaled to 30 because a single item may carry at most 20 marks. 6 items, 60 marks per mock.
MOCK = mock_sections(t1_chapters=[12, 2, 6], t2_chapters=[12, 6])

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
# Grade 8 passages (original; myths retold in our own words)
# =============================================================================================
P(id='pangu', kind='myth', title='retelling of the Chinese creation myth of Pangu',
  text=("In the beginning there was only a great egg, and inside it slept Pangu.\n"
        "For eighteen thousand years he grew, until one day he stretched and the egg cracked open. The light, clear parts floated up and became the sky; the heavy, dark parts sank and became the earth.\n"
        "Afraid they would join again, Pangu stood between them, pushing the sky higher each day.\n"
        "When at last he died, his breath became the wind, his voice the thunder, his eyes the sun and moon, and his blood the rivers."),
  myth_conv='It has a supernatural being (the giant Pangu), a time "in the beginning", huge time-scales (eighteen thousand years) and it explains how the natural world began – sky, earth, wind, thunder, sun, moon and rivers.',
  explains='How the sky and earth were separated and where natural features came from: Pangu\'s body became the wind, thunder, sun, moon and rivers.',
  culture='It suggests a belief that people and nature are connected: the world is literally made from a body, and creation comes from sacrifice and hard work.',
  dev=[('listing', 'his breath became the wind, his voice the thunder, his eyes the sun and moon', 'the list links each part of the body to part of nature, showing that the world is made from Pangu', ['simile', 'onomatopoeia', 'rhetorical question']),
       ('contrast', 'The light, clear parts floated up ... the heavy, dark parts sank', 'the opposites explain the order of the universe – sky above, earth below', ['simile', 'alliteration', 'hyperbole'])],
  struct=[('the chronological structure from egg to death', 'myths are often told in time order like oral stories, which makes them easy to remember and retell')],
  theme='creation and sacrifice', tone='solemn and wondrous', tw=['sarcastic', 'chatty', 'angry'], tonex='the grand scale and calm storytelling voice create wonder.',
  gq='How does the myth explain the creation of the world?',
  gqa='The myth explains creation through the actions and body of one supernatural being. Contrast ("light, clear parts floated up ... heavy, dark parts sank") explains the order of sky and earth; Pangu\'s effort to push the sky up shows creation as hard work; and the final list ("his breath became the wind...") turns his body into nature, suggesting people and the world are connected.',
  summary='Pangu grows inside a cosmic egg, cracks it open, separates sky and earth by holding them apart, and when he dies his body becomes the features of the natural world.')

P(id='rangi', kind='myth', title='retelling of the Maori creation story of Rangi and Papa',
  text=("Long ago, Ranginui the Sky Father and Papatūānuku the Earth Mother held each other so tightly that their children lived in darkness between them.\n"
        "The children argued. One wanted to kill their parents. Tāne, god of the forests, had a better idea.\n"
        "He lay on his back, pressed his feet against his father and pushed – slowly, for a very long time – until the sky rose and light flooded in.\n"
        "Rangi's tears for his lost wife still fall as rain, and Papa's sighs rise as morning mist."),
  myth_conv='It features gods (the Sky Father, Earth Mother and their children), conflict among supernatural beings, a heroic act by Tāne and explanations of natural events – daylight, rain and mist.',
  explains='Why there is light between earth and sky, and why it rains (Rangi\'s tears) and why mist rises (Papa\'s sighs).',
  culture='It values family love and the natural world: rain and mist are signs of the parents\' continuing love, and Tāne chooses a non-violent solution.',
  dev=[('personification', 'Rangi\'s tears for his lost wife still fall as rain', 'turning rain into tears gives weather an emotional explanation and makes nature feel alive and loving', ['statistic', 'onomatopoeia', 'oxymoron'])],
  theme='family and the origin of nature', tone='tender and solemn', tw=['comic', 'boastful', 'bitter'], tonex='the story of separated parents is told with sadness and respect.',
  summary='The Sky Father and Earth Mother held each other so tightly that their children lived in darkness; Tāne pushed them apart to let in light, and their grief still appears as rain and mist.')

P(id='manu', kind='myth', title='retelling of the Hindu flood story of Manu and the fish',
  text=("One morning, as Manu washed his hands in the river, a tiny fish swam into his palm. 'Protect me,' it begged, 'and one day I will save you.'\n"
        "Manu kept it in a jar, then a pond, then the sea, for it grew enormous. At last the fish warned him: 'A great flood is coming. Build a boat and take seeds of every plant.'\n"
        "When the waters rose, the fish – the god Vishnu in disguise – towed Manu's boat to a mountain top. From Manu, the world began again."),
  myth_conv='It includes a god in disguise (Vishnu as the fish), a warning, a test of kindness, a great flood and a new beginning for humanity.',
  explains='How humanity survived a great flood and began again through Manu, the first human of a new age.',
  culture='It values kindness to the smallest creatures: Manu\'s care for a tiny fish is rewarded with salvation.',
  dev=[('repetition / listing', 'in a jar, then a pond, then the sea', 'the growing list shows the fish growing and Manu\'s continued care', ['simile', 'onomatopoeia', 'oxymoron'])],
  theme='kindness rewarded and rebirth', tone='calm and wondrous', tw=['angry', 'mocking', 'chatty'], tonex='the calm voice presents miraculous events as natural.',
  summary='Manu protects a tiny fish that grows huge; it warns him of a flood, and when the waters rise the fish (Vishnu) tows his boat to safety so the world can begin again.')

P(id='deucalion', kind='myth', title='retelling of the Greek flood myth of Deucalion and Pyrrha',
  text=("Zeus looked down at humans and saw only cruelty, so he sent rain until the whole world drowned.\n"
        "Only Deucalion and his wife Pyrrha survived, floating in a wooden chest until it came to rest on Mount Parnassus.\n"
        "Alone and afraid, they prayed. A voice told them: 'Throw the bones of your mother over your shoulders.'\n"
        "Pyrrha was horrified – until Deucalion understood. Their mother was the Earth; her bones were stones. Every stone they threw became a person, and the world was full again."),
  myth_conv='It features a powerful god (Zeus) who punishes humanity, a flood, a riddle from a divine voice and the creation of new people.',
  explains='Why humans exist after a great flood: new people grew from stones thrown by Deucalion and Pyrrha.',
  culture='It shows Greek ideas that the gods punish wickedness and reward piety, and that humans are connected to the Earth ("Mother").',
  dev=[('riddle', '\'Throw the bones of your mother over your shoulders.\'', 'the puzzling instruction creates suspense and tests the characters\' wisdom', ['simile', 'onomatopoeia', 'statistic'])],
  theme='punishment, faith and rebirth', tone='dramatic and solemn', tw=['light-hearted', 'sarcastic', 'chatty'], tonex='divine anger and fear create drama; the ending brings hope.',
  summary='Zeus floods the world to punish human cruelty; Deucalion and Pyrrha survive, solve a riddle and throw stones that become new people.')

P(id='maui', kind='myth', title='retelling of the Polynesian story of Māui and the sun',
  text=("In the old days the sun raced across the sky so fast that there was never enough daylight to cook food or finish work.\n"
        "Māui's brothers laughed when he said he would slow it down. But Māui had a jawbone given to him by his grandmother, full of magic.\n"
        "With his brothers he wove ropes from flax, travelled east to the sun's pit and waited all night.\n"
        "When the sun rose, they snared it. Māui beat it with the jawbone until, weak and limping, it promised to travel slowly. And so we have long days."),
  myth_conv='It has a trickster hero with a magical object, a seemingly impossible task, a journey and a battle, and it explains a natural phenomenon (the length of the day).',
  explains='Why days are long enough for people to work and cook: Māui forced the sun to travel slowly.',
  hero='Ordinary world: days are too short. Call to adventure: Māui decides to slow the sun. Refusal/doubt: his brothers laugh. Mentor and gift: his grandmother\'s magic jawbone. Crossing the threshold: the journey east to the sun\'s pit. Ordeal: snaring and beating the sun. Return with the reward: longer days for everyone.',
  culture='It values cleverness, teamwork and the gifts of elders; Māui uses his grandmother\'s jawbone and his brothers\' help to benefit the whole community.',
  dev=[('personification', 'weak and limping, it promised to travel slowly', 'the sun is treated as a creature that can be defeated, making the cosmic task feel like a physical fight', ['simile', 'onomatopoeia', 'statistic'])],
  theme='courage and cleverness', tone='lively and heroic', tw=['gloomy', 'formal and scientific', 'sarcastic'], tonex='the bold quest and triumphant ending feel heroic.',
  gq='How does the story present Māui as a hero?',
  gqa='Māui is presented as a hero who defies doubt: his brothers laugh, but he acts. He has a mentor\'s gift (his grandmother\'s magic jawbone), plans carefully (weaving ropes, waiting all night) and wins through courage in the battle with the sun. The personified sun ("weak and limping") makes his victory dramatic, and the ending shows the reward benefits everyone ("And so we have long days").',
  write=[('Retell the Māui story as a short comic-strip script of four panels (describe each image and write the speech bubbles and captions).', 'Indicative content: four clearly described panels following the story (doubt, preparation, snaring, outcome); captions for narration; speech bubbles revealing character; visual choices (close-up of the jawbone, wide shot of the sun).')],
  summary='The sun moves too fast, so Māui, with his grandmother\'s magic jawbone and his brothers\' help, snares and beats it until it agrees to travel slowly, giving people long days.')

P(id='sundiata', kind='legend', title='retelling of the West African legend of Sundiata, the Lion King of Mali',
  text=("Sundiata was born in Niani, in the land of Mali, but he could not walk. For years other children mocked him and his mother wept.\n"
        "One day the queen insulted his mother because Sundiata could not bring her baobab leaves. That evening, Sundiata asked for an iron rod. Leaning on it, he pulled himself up – and the rod bent like a bow.\n"
        "He walked to the baobab tree, uprooted it and laid it at his mother's door.\n"
        "Years later, Sundiata would return from exile to defeat the sorcerer-king Soumaoro and found the Mali Empire."),
  myth_conv='As a legend it is linked to a real place and historical figure (Sundiata Keita, founder of the Mali Empire in the 13th century), but it includes superhuman deeds such as uprooting a baobab tree; it was passed down orally by griots.',
  hero='Ordinary world: Sundiata cannot walk and is mocked. Call to adventure: his mother is insulted. The challenge/threshold: he stands with the iron rod and uproots the baobab. Later stages: exile, return and the defeat of Soumaoro, which brings the reward of founding an empire.',
  culture='It values loyalty to one\'s mother, perseverance and the idea that a hero may rise from weakness; it also preserves the history of the Mali Empire through oral storytelling.',
  dev=[('simile', 'the rod bent like a bow', 'the image shows Sundiata\'s sudden, astonishing strength and hints that he will become a warrior', ['metaphor', 'onomatopoeia', 'personification']),
       ('foreshadowing', 'Years later, Sundiata would return from exile', 'the final sentence hints at a much larger story to come and shows that this is the start of a hero\'s journey', ['flashback', 'onomatopoeia', 'oxymoron'])],
  theme='rising from weakness to greatness', tone='admiring and heroic', tw=['mocking', 'cold', 'humorous'], tonex='the storyteller celebrates Sundiata\'s transformation.',
  gq='How does the legend show Sundiata changing from a weak child into a hero?',
  gqa='At first Sundiata is presented as powerless – he "could not walk" and is "mocked". The insult to his mother becomes his call to action. The simile "the rod bent like a bow" shows superhuman strength and hints he will be a warrior, and uprooting the baobab is an extraordinary deed done out of love. The foreshadowing of his return from exile shows this is the beginning of a hero\'s journey.',
  summary='Sundiata, who could not walk as a child, stands up with an iron rod after his mother is insulted, uproots a baobab tree for her, and later founds the Mali Empire.')

P(id='modern_myth', kind='myth', title='modern myth written by a Grade 8 student, "Why the City Never Sleeps"',
  text=("When the city was young, it slept every night like everyone else.\n"
        "But the Night Spirit was lonely. She drifted through empty streets, whispering to the closed shops.\n"
        "One night a baker's daughter, Ines, heard her crying. 'I'll keep you company,' Ines said, and she lit one lamp in her window.\n"
        "The Spirit was so grateful that she breathed light into every window, every street and every sign.\n"
        "And that is why the city never sleeps: it is keeping a lonely spirit company."),
  myth_conv='It copies the conventions of a traditional myth – "When the city was young", a spirit, a kind human, a gift and an ending that explains something ("And that is why...") – but applies them to a modern city.',
  explains='Why cities stay lit and busy at night: the city is keeping the lonely Night Spirit company.',
  dev=[('personification', 'whispering to the closed shops', 'the spirit seems alive and lonely, so readers sympathise with her', ['simile', 'statistic', 'hyperbole']),
       ('formulaic ending', 'And that is why the city never sleeps', 'the traditional "that is why" ending marks the story as an explanation myth', ['cliffhanger', 'flashback', 'oxymoron'])],
  theme='kindness and loneliness', tone='gentle and magical', tw=['sarcastic', 'aggressive', 'scientific'], tonex='simple storytelling and kindness create a gentle mood.',
  summary='A lonely Night Spirit is comforted by a baker\'s daughter who lights a lamp; in thanks, the Spirit lights every window, which is why the city never sleeps.')

P(id='treehouse', kind='prose', title='extract from a first-person novel about two friends',
  text=("Dev and I built the treehouse the summer we were ten. We nailed a sign to it: NO GROWN-UPS. NO GIRLS. NO EXCEPTIONS.\n"
        "Now we're thirteen and the sign is still there, faded and crooked, and Dev hasn't climbed up for months.\n"
        "Today I saw him at the bus stop with Marcus's crowd. He laughed at something Marcus said. I waved. He looked at his shoes.\n"
        "I went home and climbed the ladder alone. I took the sign down. Then I put it back up. I don't know why."),
  char='The narrator is lonely and hurt but loyal: he waves to Dev even when ignored and cannot bring himself to remove the sign, showing he hopes the friendship will return. Dev is embarrassed ("looked at his shoes") and drifting towards a new group.',
  pov='First-person narration by the abandoned friend: we only know his feelings and see Dev from the outside, so Dev\'s motives stay uncertain and we share the narrator\'s confusion.',
  theme='changing friendships as we grow up',
  message='Friendships can change painfully as people grow up; holding on to the past (the sign) can be comforting and sad at the same time.',
  dev=[('symbol', 'the sign is still there, faded and crooked', 'the old sign represents the childhood friendship, now faded like the bond between the boys', ['simile', 'onomatopoeia', 'statistic']),
       ('short sentences', 'I waved. He looked at his shoes.', 'the brief, flat sentences show the painful moment without explaining it, letting the reader feel the rejection', ['simile', 'rhetorical question', 'hyperbole']),
       ('contradictory actions', 'I took the sign down. Then I put it back up.', 'the reversal shows the narrator\'s mixed feelings – he wants to move on but cannot let go', ['metaphor', 'personification', 'alliteration'])],
  struct=[('the time shift from "the summer we were ten" to "Now we\'re thirteen"', 'the contrast between past and present shows how much the friendship has changed'),
          ('the ending "I don\'t know why."', 'the honest, unresolved ending shows the narrator\'s confusion and invites readers to interpret his feelings')],
  vocab=[('crooked', 'not straight; bent or twisted', ['dishonest', 'broken into pieces', 'brightly painted'], 'it suggests the friendship is now damaged and out of shape.')],
  qa=[('How long has it been since Dev climbed up to the treehouse?', 'Months.'),
      ('What does Dev\'s reaction at the bus stop suggest about his feelings?', 'He looks at his shoes, which suggests embarrassment or guilt: he does not want Marcus\'s crowd to see him with the narrator, but he does not want to be cruel.'),
      ('Why does the narrator put the sign back up?', 'He is not ready to accept that the friendship is over; the sign keeps his hope and memories alive.')],
  gq='How does the writer present the narrator\'s feelings about his changing friendship with Dev?',
  gqa='Point: the narrator is hurt but unwilling to let go. Evidence: "I waved. He looked at his shoes." Explanation: the short, flat sentences present the rejection without comment, making the hurt more powerful. The faded, crooked sign symbolises the damaged friendship, and the contradictory actions ("I took the sign down. Then I put it back up.") and the honest "I don\'t know why" show mixed feelings of loss and hope.',
  write=[('Rewrite the bus-stop scene (about 200 words) from Dev\'s point of view, showing why he looked at his shoes.', 'Indicative content: first person as Dev; consistent events (Marcus\'s crowd, the wave); inner conflict between wanting to fit in and guilt; realistic dialogue or thoughts; a hint about the treehouse.')],
  summary='The narrator and Dev built a treehouse as children, but now Dev ignores him to fit in with new friends; the narrator takes down their old sign, then puts it back up.')

P(id='twovoices', kind='prose', title='extract from a novel told by two narrators',
  text=("AMARA\nWhen the new boy sat in my seat on the bus, I didn't say anything. I just glared. He didn't even notice. Typical.\n\n"
        "TOMÁS\nI sat in the only empty seat. A girl glared at me like I'd stolen her kidney. I wanted to say sorry, but my English comes out wrong when I'm nervous, so I looked out of the window and counted lamp posts until my stop. Forty-three."),
  pov='Two first-person narrators give the same event from different sides: Amara thinks Tomás is rude ("He didn\'t even notice"), but Tomás reveals he did notice and was too nervous to speak. The reader knows more than either character (dramatic irony).',
  char='Amara is quick to judge and proud ("Typical."); Tomás is anxious, observant and self-conscious about his English, which he hides by counting lamp posts.',
  theme='misunderstanding and seeing others\' perspectives',
  message='We often misjudge people because we only see our own side; understanding another person\'s perspective can change how we see them.',
  dev=[('hyperbole / simile', 'like I\'d stolen her kidney', 'the comic exaggeration shows how fierce the glare felt to Tomás and adds humour', ['statistic', 'onomatopoeia', 'personification']),
       ('minor sentence', 'Typical.', 'the one-word judgement reveals Amara\'s quick assumption about the new boy', ['simile', 'rhetorical question', 'alliteration']),
       ('precise detail', 'counted lamp posts until my stop. Forty-three.', 'the exact number shows Tomás\'s anxiety and his need to focus on something safe', ['hyperbole', 'simile', 'oxymoron'])],
  struct=[('switching between two named narrators', 'the reader sees the same moment twice and realises that each character misreads the other')],
  qa=[('Why didn\'t Tomás apologise to Amara?', 'He was nervous and his English "comes out wrong" when he is nervous.'),
      ('What does the word "Typical." suggest about Amara?', 'That she has already judged the new boy negatively, perhaps assuming all new or different people are rude.')],
  gq='How does the writer use two narrators to show a misunderstanding?',
  gqa='Amara\'s section shows her judgement ("He didn\'t even notice. Typical."), but Tomás\'s section reveals the opposite: he noticed the glare ("like I\'d stolen her kidney") and wanted to apologise but was too nervous. Switching narrators creates dramatic irony, so the reader understands both sides, and the detail of counting lamp posts builds sympathy for Tomás.',
  summary='Amara is annoyed when a new boy takes her bus seat and thinks he is rude; Tomás, the new boy, noticed her glare but was too nervous about his English to apologise.')

P(id='bench', kind='prose', title='extract from a novel about a boy who eats lunch alone',
  text=("Every lunchtime Oliver ate on the bench behind the music block, where the wind smelled of old leaves and nobody came.\n"
        "He told his mum he had loads of friends. It was easier than the truth.\n"
        "On Tuesday, a tuba case appeared at the other end of the bench, followed by a tall girl with a sandwich.\n"
        "\"Is this your bench?\" she asked.\n"
        "\"It's nobody's bench,\" Oliver said.\n"
        "\"Good,\" said the girl, sitting down. \"Then it can be ours.\""),
  char='Oliver is lonely and hides it to protect his mother ("It was easier than the truth"); the girl is confident and friendly, turning his phrase "nobody\'s bench" into an invitation.',
  pov='Third-person limited narration follows Oliver closely, revealing his secret and his feelings, so the reader sympathises with his loneliness.',
  theme='loneliness and belonging', message='Belonging can start with a small act of welcome; places of loneliness can become places of friendship.',
  dev=[('sensory description', 'where the wind smelled of old leaves and nobody came', 'the faded, lonely setting reflects Oliver\'s isolation', ['statistic', 'onomatopoeia', 'oxymoron']),
       ('wordplay in dialogue', '"It\'s nobody\'s bench" ... "Then it can be ours."', 'the girl turns Oliver\'s lonely phrase into an offer of friendship', ['simile', 'personification', 'alliteration'])],
  struct=[('the shift "On Tuesday"', 'it breaks Oliver\'s lonely routine and introduces change')],
  qa=[('What lie does Oliver tell his mum?', 'That he has "loads of friends".'),
      ('What does the girl\'s final line suggest about her?', 'She is friendly and confident, and perhaps also looking for a friend; she turns the bench into a shared place.')],
  gq='How does the writer show the beginning of a friendship in this extract?',
  gqa='The setting ("where the wind smelled of old leaves and nobody came") reflects Oliver\'s loneliness, and his lie to his mum shows how hidden it is. The arrival of the tuba case breaks the routine, and the girl\'s wordplay ("Then it can be ours") turns his lonely phrase into an invitation, showing belonging can begin with a small act of welcome.',
  summary='Lonely Oliver eats lunch alone behind the music block and pretends to his mother that he has friends, until a girl with a tuba sits with him and says the bench can be theirs.')

P(id='limerick', kind='poem', title='limerick by a student poet',
  text=("A girl from the top of Peru\n"
        "Had a llama that sang in the zoo.\n"
        "When the crowd shouted, \"Stop!\"\n"
        "It hit a high top,\n"
        "And the keeper joined in with it too."),
  form='It is a limerick: five lines with an AABBA rhyme scheme (Peru/zoo/too; Stop/top), a bouncing rhythm with longer lines 1, 2 and 5 and shorter lines 3 and 4, and a humorous, absurd story.',
  sound='The AABBA rhyme scheme and the bouncy, galloping rhythm (anapaestic metre) make the poem fun to read aloud; the short third and fourth lines speed up towards the punchline.',
  dev=[('rhyme', 'Peru ... zoo ... too', 'the repeated sound ties the comic story together and makes the ending feel like a punchline', ['assonance', 'onomatopoeia', 'simile'])],
  tone='comic', tw=['tragic', 'serious', 'mournful'], tonex='the absurd singing llama and punchline make it light-hearted.',
  perform='Perform it with a lively, bouncing rhythm and comic timing: pause briefly before the last line and stress the rhyming words; a surprised facial expression on "the keeper joined in" helps the joke.',
  summary='A girl from Peru has a llama that sings in a zoo; when the crowd tells it to stop it sings higher, and the keeper joins in.')

P(id='ballad', kind='poem', title='ballad by a student poet, "The Ferryman\'s Daughter"',
  text=("The river ran both wide and black,\n"
        "The storm came down the hill;\n"
        "The ferryman went out at dusk\n"
        "And has not come back still.\n\n"
        "His daughter took the lantern down\n"
        "And walked into the rain;\n"
        "She called his name across the waves –\n"
        "She called and called again."),
  form='It is a ballad: it tells a story in four-line stanzas (quatrains) with an ABCB rhyme scheme (hill/still; rain/again), a regular alternating rhythm and repetition, like a song passed down orally.',
  sound='The ABCB rhyme and regular rhythm make it sound like a song; the repetition "She called and called again" echoes like a voice across the water and emphasises desperation.',
  dev=[('repetition', 'She called and called again', 'repeating "called" shows the daughter\'s desperate, unanswered search and creates a haunting, song-like effect', ['simile', 'statistic', 'oxymoron']),
       ('pathetic fallacy', 'The river ran both wide and black, / The storm came down the hill', 'the dark, wild setting reflects danger and creates a tense, tragic mood', ['hyperbole', 'onomatopoeia', 'alliteration'])],
  tone='tense and sorrowful', tw=['comic', 'cheerful', 'boastful'], tonex='the missing father and the storm create sorrow and suspense.',
  mood='A dark, tense, tragic mood is created by the "wide and black" river, the storm and the father who "has not come back".',
  perform='Read slowly with a steady rhythm, lower the voice for the dark setting, and let the repetition grow louder or more desperate on "called and called again"; in a choral reading, different voices could echo "called".',
  theme='loss and love',
  summary='A ferryman goes out in a storm and does not return; his daughter takes a lantern into the rain and calls his name across the river again and again.')

P(id='citynight', kind='poem', title='free verse poem by a student poet, "Lagos at Midnight"',
  text=("The city does not sleep;\n"
        "it hums,\n"
        "a generator heart\n"
        "beating under every street.\n"
        "Danfo buses honk like geese.\n"
        "A radio somewhere\n"
        "is singing to nobody,\n"
        "and the moon,\n"
        "tired of competing,\n"
        "hides behind the billboards."),
  form='It is free verse: there is no regular rhyme scheme or metre; line lengths vary freely, and line breaks are used for emphasis (e.g. "it hums," on its own line).',
  sound='Onomatopoeia ("hums", "honk") and the simile "honk like geese" recreate the city\'s noise; the short line "it hums," slows the reader down to hear the sound.',
  dev=[('metaphor', 'a generator heart / beating under every street', 'the city becomes a living body powered by generators, suggesting constant energy', ['simile', 'onomatopoeia', 'alliteration']),
       ('simile', 'Danfo buses honk like geese', 'the comparison is humorous and captures the chaotic noise of traffic', ['metaphor', 'personification', 'oxymoron']),
       ('personification', 'the moon, / tired of competing, / hides behind the billboards', 'the moon seems defeated by the city\'s artificial light, a playful way to show how bright Lagos is', ['simile', 'statistic', 'onomatopoeia']),
       ('onomatopoeia', 'hums', 'the word imitates the low, constant sound of the city', ['simile', 'metaphor', 'hyperbole'])],
  tone='energetic and affectionate', tw=['bitter', 'fearful', 'bored'], tonex='lively sound images and humour show love for the busy city.',
  mood='A lively, slightly lonely mood: the city is full of noise and energy, yet the radio "singing to nobody" hints at loneliness.',
  theme='city life',
  perform='Perform with varied pace: slow and quiet for "it hums," faster and louder for the honking buses, and a soft, playful voice for the hiding moon; spoken-word style suits it.',
  gq='How does the poet use imagery and sound to present Lagos at night?',
  gqa='The extended metaphor "a generator heart / beating" presents the city as a living body. Onomatopoeia ("hums", "honk") and the comic simile "like geese" recreate the noise. Free-verse line breaks isolate sounds, and personification of the moon "tired of competing" shows the city\'s overwhelming light, while the radio "singing to nobody" adds a hint of loneliness.',
  summary='The poet presents Lagos at midnight as alive and noisy – humming generators, honking buses and a radio – so bright that even the moon hides.')

P(id='spokenword', kind='poem', title='spoken-word poem performed by a 14-year-old at a youth festival in London',
  text=("They call us the screen generation.\n"
        "Screen – like something you hide behind.\n"
        "Screen – like something you sieve the truth through.\n"
        "But I am not a screen.\n"
        "I am a voice\n"
        "and I am LOUD,\n"
        "and I have been waiting fourteen years\n"
        "for you to hear me say it:\n"
        "we see more than you think."),
  form='It is a spoken-word poem written in free verse for performance: it uses repetition, direct address and changes in volume (capitals on "LOUD") to work on a live audience.',
  sound='The repetition of "Screen –" and the rising rhythm of the final lines build intensity; the capitalised "LOUD" tells the performer to raise their voice.',
  dev=[('pun / wordplay', 'Screen – like something you hide behind. / Screen – like something you sieve the truth through.', 'the poet plays on different meanings of "screen", criticising how adults label young people', ['simile', 'statistic', 'onomatopoeia']),
       ('anaphora', 'Screen – ... / Screen – ...', 'the repeated word at the start of lines builds rhythm and emphasis for a live audience', ['simile', 'hyperbole', 'personification']),
       ('direct address', 'for you to hear me say it', 'speaking directly to "you" (adults) makes the poem a challenge to the audience', ['simile', 'statistic', 'onomatopoeia'])],
  tone='defiant', tw=['tender', 'melancholy', 'sleepy'], tonex='the poet rejects a label and insists on being heard.',
  perform='Spoken-word performance: build volume from a calm opening to a shout on "LOUD", pause before the final line, make eye contact on "you" and use a gesture (pointing to the eyes) on "we see more than you think".',
  theme='identity and being heard',
  summary='The young poet rejects the label "screen generation", plays on the word "screen" and insists that young people have a loud voice and see more than adults think.')

P(id='charity_video', kind='ad', title='storyboard description of a 30-second charity video advertisement',
  text=("SHOT 1 (close-up): A girl's feet in torn sandals walk along a dry riverbed. Sound: wind, no music.\n"
        "SHOT 2 (wide shot): She carries a yellow jerrycan towards a distant well. Caption: \"Amina walks 6 km for water. Every day.\"\n"
        "SHOT 3 (close-up): Water pours from a new tap; Amina laughs. Music begins – soft piano.\n"
        "SHOT 4: Text on screen: \"£25 can bring clean water to a child for life.\"\n"
        "VOICE-OVER: \"Amina's walk can end today.\" Logo and website."),
  aud='Viewers in wealthy countries who might donate; the price in pounds and the request for money show the target audience.',
  purp='To persuade viewers to donate £25 by showing the hardship of collecting water and the change a donation can make.',
  video='Camera shots move from close-up on tired feet (hardship, empathy) to a wide shot showing the long distance, then a close-up of the laughing face. Sound changes from wind and silence (emptiness) to piano music when the tap appears, signalling hope. Captions give the facts and the donation request.',
  tone='moving and hopeful', tw=['comic', 'angry', 'indifferent'], tonex='silence and hardship give way to music and laughter.',
  dev=[('statistic', '"Amina walks 6 km for water. Every day."', 'a specific distance makes the hardship concrete, and the short sentence "Every day." stresses that it never stops', ['simile', 'oxymoron', 'onomatopoeia']),
       ('emotive voice-over', '"Amina\'s walk can end today."', 'it gives viewers the power to change one named child\'s life immediately', ['statistic', 'hyperbole', 'alliteration'])],
  struct=[('the before-and-after structure (dry riverbed to running tap)', 'it shows the problem and then the solution, so the donation feels effective')],
  visual='The yellow jerrycan stands out against the dry landscape and becomes a symbol of the burden; the close-up of Amina\'s laughing face makes the solution personal and joyful.',
  read='Some viewers will be moved to donate; others may question whether one child\'s story oversimplifies a complex problem or presents people as helpless.',
  gq='How does the video advertisement use camera shots, sound and words to persuade viewers to donate?',
  gqa='Close-ups of torn sandals build empathy, and the wide shot shows the 6 km distance; the caption "Every day." stresses the endless hardship. The shift from wind and silence to piano music when the tap appears signals hope, and the close-up of Amina laughing makes the change personal. The voice-over "Amina\'s walk can end today" and the price give viewers a simple, immediate action.',
  summary='A short charity video shows a girl walking 6 km for water each day, then laughing at a new tap, and asks viewers to donate £25 for clean water.')

P(id='bike_letter', kind='letter', title='persuasive letter from a student to her head teacher in Copenhagen',
  text=("Dear Ms Larsen,\n"
        "I am writing on behalf of the Grade 8 class to propose a covered bike shelter for our school.\n"
        "At present, 140 students cycle to school, but there are only 40 spaces. Bikes are left in the rain and two were stolen last month.\n"
        "A shelter would keep bikes safe, encourage more students to cycle, and support our city's aim to be carbon-neutral by 2025.\n"
        "Surely a school that teaches us about climate change should make the green choice the easy choice?\n"
        "Yours sincerely,\nFreja Nielsen, Grade 8B"),
  aud='The head teacher, who has the power to approve the shelter; the formal salutation and respectful tone suit her.',
  purp='To persuade the head teacher to build a covered bike shelter.',
  tone='formal and reasonable', tw=['rude', 'playful', 'desperate'], tonex='polite language and evidence make the case calm and convincing.',
  dev=[('statistics', '140 students cycle to school, but there are only 40 spaces', 'the contrast between the numbers proves the problem logically', ['simile', 'onomatopoeia', 'metaphor']),
       ('tricolon', 'keep bikes safe, encourage more students to cycle, and support our city\'s aim', 'three benefits make the proposal seem strong and well thought out', ['simile', 'oxymoron', 'onomatopoeia']),
       ('rhetorical question', 'Surely a school that teaches us about climate change should make the green choice the easy choice?', 'it challenges the head teacher to act on the school\'s own values', ['statistic', 'simile', 'hyperbole'])],
  struct=[('problem – solution – benefits – challenge', 'the logical order makes the letter persuasive and easy to follow')],
  gq='How does Freja make her letter persuasive?',
  gqa='Freja opens with a clear purpose and speaks "on behalf of the Grade 8 class", giving her authority. Statistics (140 cyclists, 40 spaces, two thefts) prove the problem, a tricolon of benefits presents the solution, and the closing rhetorical question uses the school\'s own values to make refusing difficult, all in a polite formal register.',
  write=[('Write a persuasive leaflet (about 200 words) for students, encouraging them to cycle or walk to school.', 'Indicative content: heading and subheadings; facts or statistics; bullet points of benefits; persuasive devices (rhetorical question, direct address, rule of three); call to action; layout features.')],
  summary='Freja asks her head teacher for a covered bike shelter because 140 students cycle but there are only 40 spaces; it would protect bikes, encourage cycling and support the city\'s climate goal.')

P(id='market_scene', kind='drama', title='extract from a comic playscript set in a market in Marrakech',
  text=("A busy market stall piled with lanterns. YOUSSEF (14) is minding the stall for his uncle. A TOURIST approaches, holding a map upside down.\n"
        "TOURIST: (loudly, slowly) HOW. MUCH. IS. THIS?\n"
        "YOUSSEF: (in perfect English) It's two hundred dirhams. Also, your map is upside down.\n"
        "TOURIST: (turns the map, embarrassed) Oh! You speak English!\n"
        "YOUSSEF: And French. And Arabic. And a bit of Spanish. (He grins.) For you, a special price: one hundred and ninety.\n"
        "(The TOURIST laughs. UNCLE HASSAN appears behind the lanterns, shaking his head.)"),
  char='Youssef is confident, witty and multilingual; he gently corrects the tourist\'s assumption and shows his skill as a salesman. The tourist is well-meaning but makes assumptions about the local boy.',
  staging='Set: a crowded stall of hanging lanterns, perhaps lit with warm coloured lights. Costume: casual clothes for Youssef, a sunhat and backpack for the tourist. Blocking: the tourist leans in too close when speaking loudly; Youssef stays relaxed behind the stall; Uncle Hassan appears upstage behind the lanterns for comic effect.',
  dev=[('stage direction for delivery', '(loudly, slowly) HOW. MUCH. IS. THIS?', 'the direction and full stops show the tourist assumes Youssef cannot understand English, setting up the comedy', ['soliloquy', 'aside', 'monologue']),
       ('comic reversal', '(in perfect English) ... Also, your map is upside down.', 'the twist overturns the tourist\'s stereotype and makes Youssef the clever one', ['dramatic irony', 'monologue', 'flashback']),
       ('listing in dialogue', 'And French. And Arabic. And a bit of Spanish.', 'the growing list shows Youssef\'s confidence and humour', ['simile', 'onomatopoeia', 'oxymoron'])],
  tone='comic and good-natured', tw=['tragic', 'menacing', 'mournful'], tonex='gentle humour comes from the tourist\'s mistake and Youssef\'s wit.',
  theme='stereotypes and cultural assumptions',
  gq='How does the playwright use dialogue and stage directions to create comedy and character?',
  gqa='The stage direction "(loudly, slowly)" and the full stops in "HOW. MUCH. IS. THIS?" show the tourist\'s assumption; the reversal "(in perfect English)" and the upside-down map overturn it. Youssef\'s listed languages and cheeky "special price" reveal his wit, and Uncle Hassan shaking his head adds a final visual joke.',
  summary='A tourist speaks loudly and slowly to Youssef at his uncle\'s market stall, but Youssef replies in perfect English, points out the upside-down map and jokes about a special price.')

P(id='audition', kind='drama', title='extract from a playscript about a school talent show',
  text=("Backstage. Dim light. PRIYA paces, muttering lines. JAKE sits on an amp, eating crisps.\n"
        "PRIYA: What if I forget the words? What if my voice cracks? What if everyone laughs?\n"
        "JAKE: (crunching) What if you're brilliant?\n"
        "PRIYA: (stops pacing) That's... not helpful.\n"
        "JAKE: (standing, serious for once) Priya. You sang in the lift on the way here. Three people clapped. One was the lift man.\n"
        "(Offstage, a voice calls: 'Priya Shah!' PRIYA freezes. JAKE gives her a thumbs up. She walks into the light.)"),
  char='Priya is anxious and self-doubting (repeated "What if..." questions, pacing); Jake seems careless (eating crisps on an amp) but is a loyal, funny friend who becomes "serious for once" to encourage her.',
  staging='Lighting: dim backstage light contrasted with a bright stage light that Priya walks into at the end. Sound: the offstage voice calling her name. Blocking: Priya paces while Jake stays still, showing their contrasting moods; she finally walks out of the dim area into the light.',
  dev=[('anaphora (repeated questions)', 'What if I forget the words? What if my voice cracks? What if everyone laughs?', 'the repeated questions show Priya\'s rising panic', ['simile', 'statistic', 'onomatopoeia']),
       ('comic reversal of the pattern', 'What if you\'re brilliant?', 'Jake turns Priya\'s worried pattern into encouragement, which is funny and kind', ['flashback', 'soliloquy', 'oxymoron']),
       ('symbolic stage direction', 'She walks into the light.', 'moving from dim backstage into the light symbolises Priya overcoming her fear', ['aside', 'monologue', 'hyperbole'])],
  tone='comic and encouraging', tw=['sinister', 'angry', 'despairing'], tonex='Jake\'s jokes ease Priya\'s nerves and lead to an uplifting end.',
  theme='friendship and courage',
  gq='How does the playwright present the friendship between Priya and Jake?',
  gqa='Priya\'s anaphoric "What if..." questions show her panic, and Jake\'s crunching reply "What if you\'re brilliant?" turns the pattern into encouragement. The stage direction "serious for once" reveals that his humour hides real care, and his anecdote about the lift is funny but reassuring. The final stage directions (thumbs up; "She walks into the light") show his support helping her overcome fear.',
  summary='Backstage, Priya panics before singing in a talent show; her friend Jake jokes and then seriously encourages her, and she walks out on stage.')

P(id='attic', kind='story', title='extract from a suspense story',
  text=("The attic door had been locked for as long as Leila could remember. 'Nothing up there but dust,' Gran always said.\n"
        "So why, tonight, was there a light under it?\n"
        "Leila climbed the stairs. Each step creaked. Each creak sounded like a warning.\n"
        "She reached for the handle. It was warm.\n"
        "Behind the door, something was humming – a tune she knew. The tune her mother used to sing.\n"
        "Her mother had been gone for six years."),
  suspense='Suspense is built through a mystery (a light under a locked door), a rhetorical question, slow pacing with short sentences on the stairs, unsettling sensory details (creaking steps, a warm handle) and a final revelation that creates a cliffhanger.',
  mood='A tense, eerie mood: darkness, the creaking stairs "like a warning", the warm handle and the familiar humming create unease.',
  setting='The setting is a dark house at night with a locked attic – a classic suspense location that hides secrets.',
  foreshadow='Gran\'s comment "Nothing up there but dust" foreshadows a secret in the attic, and the mother\'s tune hints at a link between the mystery and Leila\'s missing mother.',
  dev=[('rhetorical question', 'So why, tonight, was there a light under it?', 'it voices Leila\'s curiosity and pulls the reader into the mystery', ['simile', 'statistic', 'onomatopoeia']),
       ('simile', 'Each creak sounded like a warning', 'the ordinary noise becomes threatening, increasing tension', ['metaphor', 'onomatopoeia', 'oxymoron']),
       ('short sentences', 'She reached for the handle. It was warm.', 'brief sentences slow the action and focus on an unsettling detail', ['simile', 'hyperbole', 'rhetorical question']),
       ('cliffhanger', 'Her mother had been gone for six years.', 'the final revelation shocks the reader and leaves the mystery unresolved', ['flashback', 'simile', 'alliteration'])],
  struct=[('the one-sentence final paragraph', 'isolating the revelation gives it maximum impact and creates a cliffhanger'),
          ('the slow climb up the stairs', 'stretching a short action over several sentences delays the discovery and increases suspense')],
  tone='tense and mysterious', tw=['cheerful', 'comic', 'boastful'], tonex='short sentences and eerie details create tension.',
  theme='loss and mystery',
  gq='How does the writer build suspense in this extract?',
  gqa='The writer builds suspense through mystery and pacing. The rhetorical question "So why, tonight, was there a light under it?" draws the reader in; the simile "Each creak sounded like a warning" makes ordinary sounds threatening; short sentences ("It was warm.") slow the climb and focus on unsettling details; and the final isolated sentence about Leila\'s mother creates a shocking cliffhanger.',
  write=[('Write the next paragraph (about 200 words): what does Leila find when she opens the door? Keep the suspense and include a twist.', 'Indicative content: consistent setting and mood; slow pacing at the moment of opening; sensory detail; a twist that links to the mother (e.g. a recording, a sibling, a memory) rather than a cliché; a final line that resolves or deepens the mystery.')],
  summary='Leila sees a light under the locked attic door, climbs the creaking stairs and hears someone humming her mother\'s tune – but her mother has been gone for six years.')

P(id='lift', kind='story', title='extract from a short story set in a tower block in Hong Kong',
  text=("The lift stopped between the 23rd and 24th floors with a soft clunk.\n"
        "The lights dimmed to emergency orange. Kenji pressed the alarm. Nothing.\n"
        "'Don't worry,' said the old woman in the corner. 'It happens every Tuesday.'\n"
        "It was Wednesday.\n"
        "Kenji looked at her properly for the first time. Her umbrella was dripping, though it hadn't rained all week. And in the mirrored wall, where her reflection should have been, there was only an umbrella, dripping, all by itself."),
  suspense='Tension grows from a realistic problem (a stuck lift) to the uncanny: the old woman\'s wrong day, the dripping umbrella on a dry week and finally the missing reflection – each detail more unsettling than the last.',
  twist='The twist is that the old woman has no reflection, suggesting she is a ghost; earlier clues (the wrong day, the dripping umbrella) prepare for it.',
  mood='The emergency orange light, silence after the alarm and confined space create a claustrophobic, eerie mood.',
  setting='A lift stuck between floors in a tower block – a small, enclosed modern setting with no escape, which intensifies fear.',
  dev=[('one-line paragraph', 'It was Wednesday.', 'the short paragraph undercuts the woman\'s reassurance and signals that something is wrong', ['simile', 'statistic', 'onomatopoeia']),
       ('onomatopoeia', 'a soft clunk', 'the quiet sound makes the moment realistic and slightly ominous', ['simile', 'metaphor', 'alliteration']),
       ('colour imagery', 'emergency orange', 'the unnatural light creates an uneasy atmosphere', ['onomatopoeia', 'oxymoron', 'statistic'])],
  struct=[('clues placed before the twist', 'details such as the dripping umbrella prepare the reader, so the missing reflection is shocking but makes sense'),
          ('ending on the image of the umbrella in the mirror', 'the final image reveals the twist without explaining it, leaving the reader to realise the truth')],
  tone='eerie', tw=['joyful', 'romantic', 'sarcastic'], tonex='ordinary details become strange and frightening.',
  theme='the supernatural in everyday life',
  gq='How does the writer create tension and surprise in this extract?',
  gqa='Tension starts with a realistic problem (the "soft clunk", emergency orange light, a dead alarm). The one-line paragraph "It was Wednesday." undercuts the woman\'s reassurance. Clues build: the umbrella drips though it has not rained. The final image – a reflection showing only the umbrella – delivers the twist that she is a ghost without stating it.',
  summary='Kenji is trapped in a stuck lift with an old woman who says it happens every Tuesday – but it is Wednesday, her umbrella is wet in a dry week, and she has no reflection.')

P(id='footsteps', kind='story', title='extract from a short story with a twist ending',
  text=("Every night that week, Sam heard footsteps following her home from the bus stop. Every night she walked faster. Every night she didn't look back.\n"
        "On Friday she couldn't bear it. At the corner she spun round, fists raised.\n"
        "A small boy in a yellow raincoat stopped dead. He was holding out her purse.\n"
        "'You dropped it on Monday,' he whispered. 'I've been trying to catch up.'"),
  suspense='Suspense builds through repetition ("Every night..."), Sam\'s fear and her refusal to look back; the turning point on Friday raises the tension to a climax.',
  twist='The follower is not a threat but a small boy returning her purse; the twist reverses the reader\'s expectations and shows how fear can make us misjudge others.',
  dev=[('anaphora (repetition)', 'Every night that week ... Every night she walked faster. Every night she didn\'t look back.', 'the repetition builds dread and shows the fear growing night after night', ['simile', 'statistic', 'onomatopoeia']),
       ('contrast', 'fists raised. / A small boy in a yellow raincoat', 'the aggressive pose contrasts with the harmless child, making the twist comic and touching', ['simile', 'personification', 'onomatopoeia'])],
  struct=[('the twist in the final line', 'it reveals the innocent truth and makes the reader rethink the whole story')],
  tone='tense then touching', tw=['comic throughout', 'angry', 'boastful'], tonex='fear builds and is released by a gentle surprise.',
  theme='fear and misjudgement',
  summary='Sam is frightened by footsteps following her home every night; when she finally turns to confront them, it is a small boy trying to return the purse she dropped.')

P(id='wangari', kind='bio', title='short biography of the environmental activist Wangari Maathai',
  text=("Wangari Maathai was born in 1940 in a village in central Kenya, where she fetched water from a stream lined with fig trees.\n"
        "In 1971 she became the first woman in East and Central Africa to earn a doctorate. But she noticed that the streams of her childhood were drying up as forests were cut down.\n"
        "In 1977 she founded the Green Belt Movement, paying rural women to plant trees. Together they planted tens of millions.\n"
        "In 2004 she became the first African woman to win the Nobel Peace Prize."),
  context='Historical context: Kenya in the 1970s faced deforestation and women had few opportunities; Maathai connected environmental damage with poverty and women\'s rights. Personal context: her childhood memory of the stream shows why she cared about trees.',
  features='It is a biography: a third-person account of a real person\'s life in chronological order, using dates (1940, 1971, 1977, 2004), facts and achievements, with a detail from her childhood to give personal interest.',
  dev=[('chronological dates', 'In 1971 ... In 1977 ... In 2004', 'dates organise the life story clearly and show steady achievement', ['simile', 'flashback', 'onomatopoeia']),
       ('superlative / "first"', 'the first African woman to win the Nobel Peace Prize', 'it stresses how groundbreaking her achievements were', ['simile', 'hyperbole', 'oxymoron'])],
  struct=[('the link between the childhood stream and the later drying streams', 'it connects her personal memory to her life\'s work, showing why she acted')],
  qa=[('What did the Green Belt Movement pay rural women to do?', 'Plant trees.'),
      ('Why did Maathai become concerned about the environment?', 'She noticed the streams of her childhood drying up as forests were cut down.'),
      ('In what year did she win the Nobel Peace Prize?', '2004.')],
  gq='How does the biographer present Wangari Maathai as an inspiring figure?',
  gqa='The biography moves chronologically through a series of "firsts" (first woman in the region with a doctorate; first African woman to win the Nobel Peace Prize), showing her as a pioneer. The opening childhood detail of the stream lined with fig trees links her memories to her later concern, and the scale of "tens of millions" of trees shows the impact of ordinary women working together under her leadership.',
  summary='Wangari Maathai, born in Kenya in 1940, became the region\'s first female doctorate holder, founded the Green Belt Movement in 1977 to plant trees with rural women, and won the Nobel Peace Prize in 2004.')

P(id='owens', kind='bio', title='short biography of the athlete Jesse Owens',
  text=("Jesse Owens was born in Alabama in 1913, the grandson of enslaved people. His family moved north to Ohio, where a school coach noticed how fast he ran.\n"
        "In 1936 the Olympic Games were held in Berlin. Germany's Nazi government wanted the Games to show that its idea of racial superiority was true.\n"
        "Owens won four gold medals – in the 100 metres, 200 metres, long jump and relay.\n"
        "Yet when he returned to the United States, he still faced segregation. 'I wasn't invited to shake hands with the President,' he later said."),
  context='Historical context: the 1936 Berlin Olympics were used as propaganda by the Nazi government; at the same time, Black Americans faced segregation in the United States. This context shows that Owens\'s victories challenged racism abroad while he still suffered it at home.',
  features='It is a biography: third-person, chronological, factual (dates, places, medal events), with a quotation from Owens himself as evidence.',
  dev=[('contrast / irony', 'Yet when he returned to the United States, he still faced segregation', 'the word "Yet" reveals the irony that a national hero was still treated unequally at home', ['simile', 'onomatopoeia', 'alliteration']),
       ('quotation from the subject', '\'I wasn\'t invited to shake hands with the President,\'', 'his own words give evidence of injustice and a personal voice', ['statistic', 'metaphor', 'hyperbole'])],
  qa=[('In which four events did Owens win gold medals in 1936?', 'The 100 metres, 200 metres, long jump and relay.'),
      ('What did the Nazi government hope the 1936 Games would show?', 'That its idea of racial superiority was true.')],
  gq='How does the biographer use context to make Owens\'s achievements more meaningful?',
  gqa='The biographer begins with his family history (grandson of enslaved people) and places the 1936 Games in their Nazi propaganda context, so his four gold medals become a challenge to racist ideas. The ironic turn "Yet ... he still faced segregation" and his own quotation show that his achievement did not free him from racism at home.',
  summary='Jesse Owens, grandson of enslaved people, won four gold medals at the 1936 Berlin Olympics, challenging Nazi racial ideas, yet still faced segregation in the United States.')

P(id='cricket_autobio', kind='autobio', title='extract from the autobiography of a cricket coach who grew up in Colombo',
  text=("I learned to bat with a coconut-palm branch and a tennis ball wrapped in electrical tape. Our pitch was the lane behind my uncle's shop, and the stumps were a stack of bricks.\n"
        "The rules were simple: hit the shop window and you were out – and you also had to explain it to my uncle.\n"
        "I was eleven when I hit the window. I still remember the sound: not a crash, but a tiny, terrible click.\n"
        "My uncle didn't shout. He handed me a broom and said, 'Now you learn to sweep, then you learn to aim.' I have been coaching young players with that sentence for thirty years."),
  features='It is autobiography: a first-person account of the writer\'s own life, told by an older narrator looking back, combining specific childhood memories with reflection on how they shaped him.',
  context='Personal and cultural context: growing up in Colombo, playing street cricket with improvised equipment, shows the passion for cricket in Sri Lanka and a childhood without expensive resources; the uncle represents a respected older generation.',
  dev=[('specific sensory detail', 'not a crash, but a tiny, terrible click', 'the surprising quietness of the sound captures the moment of dread vividly and memorably', ['simile', 'statistic', 'rhetorical question']),
       ('humorous rule', 'hit the shop window and you were out – and you also had to explain it to my uncle', 'humour brings the street game to life and foreshadows the incident', ['metaphor', 'onomatopoeia', 'oxymoron']),
       ('reflection linking past and present', 'I have been coaching young players with that sentence for thirty years', 'the adult narrator shows the lasting lesson of the anecdote', ['flashforward', 'simile', 'statistic'])],
  struct=[('anecdote followed by reflection', 'the small story leads to a lesson that explains the writer\'s adult life')],
  gq='How does the writer make this childhood memory vivid and meaningful?',
  gqa='Specific details – the coconut-palm bat, the taped ball, the stack of bricks – recreate the improvised street game. The humorous rule foreshadows the incident, and the unexpected sound "a tiny, terrible click" captures his dread. The uncle\'s calm words become a lesson, and the final reflection links the anecdote to thirty years of coaching.',
  write=[('Write an autobiographical anecdote (about 250 words) about a mistake that taught you something, ending with a sentence of reflection.', 'Indicative content: first person; specific setting and sensory detail; a clear moment of crisis; dialogue; reflection on what was learned and how it matters now.')],
  summary='A coach recalls playing street cricket as a boy in Colombo with improvised equipment; when he broke his uncle\'s shop window, his uncle calmly taught him to sweep and then to aim – a lesson he still uses.')

P(id='skate_a', kind='news', title='report in a local newspaper about a new skatepark (Report A)',
  text=("YOUTH CELEBRATE AS SKATEPARK FINALLY OPENS\n"
        "Hundreds of young people cheered on Saturday as Riverside Skatepark opened after a three-year campaign by local teenagers.\n"
        "\"This is ours. We fought for it,\" said Lina Osei, 15, who collected 2,000 signatures.\n"
        "The council spent €180,000 on the park, which includes ramps, a bowl and free lessons for beginners.\n"
        "Councillor Mark Dubois called it \"an investment in our young people\"."),
  bias='Report A is positive towards the skatepark: the headline uses "Celebrate" and "Finally", quotations come only from supporters (Lina Osei and a councillor), and the cost is presented as an "investment".',
  facts_op='Fact: "The council spent €180,000 on the park". Opinion: "an investment in our young people" (Councillor Dubois\'s judgement).',
  dev=[('loaded words in the headline', 'CELEBRATE AS SKATEPARK FINALLY OPENS', '"Celebrate" and "Finally" present the opening as a long-awaited victory', ['simile', 'onomatopoeia', 'oxymoron']),
       ('selected quotation', '"This is ours. We fought for it,"', 'quoting a young campaigner makes readers sympathise with the teenagers', ['statistic', 'hyperbole', 'alliteration'])],
  struct=[('the lead paragraph', 'it gives who, what, when and why in one sentence: young people, the opening, Saturday, after a campaign')],
  summary='A skatepark opened after a three-year youth campaign; teenagers celebrated, and a councillor praised the €180,000 cost as an investment in young people.')

P(id='skate_b', kind='news', title='report in a local newspaper about a new skatepark (Report B)',
  text=("RESIDENTS FEAR NOISE AS €180,000 SKATEPARK OPENS\n"
        "Residents near Riverside Park have complained about noise and litter after a new skatepark opened on Saturday.\n"
        "\"We can't hear our own television,\" said retired teacher Joan Price, 72. \"And who's paying for this? We are.\"\n"
        "The council spent €180,000 on the facility despite cuts to street lighting this year.\n"
        "Young people, who campaigned for the park, were not available for comment."),
  bias='Report B is negative: the headline foregrounds "fear", "noise" and the cost, the only quotation is from a resident who complains, and the line about cuts to street lighting suggests the money was wasted; young people\'s views are missing.',
  facts_op='Fact: "The council spent €180,000 on the facility". Opinion: "We can\'t hear our own television" (an exaggerated complaint) and the implied judgement that the money should have gone elsewhere.',
  dev=[('loaded words in the headline', 'RESIDENTS FEAR NOISE', '"Fear" and "noise" frame the skatepark as a threat to the community', ['simile', 'onomatopoeia', 'oxymoron']),
       ('omission', 'Young people ... were not available for comment', 'leaving out the teenagers\' voice makes the report one-sided', ['simile', 'alliteration', 'hyperbole'])],
  summary='Residents complain about noise and the €180,000 cost of the new skatepark, which was built despite cuts to street lighting; young campaigners were not quoted.')

P(id='headlines', kind='news', title='set of newspaper headlines',
  text=("1. \"PURR-FECT ENDING: CAT FOUND AFTER 3 WEEKS UP CRANE\"\n"
        "2. \"Mayor's Mega Mall Madness\"\n"
        "3. \"Thugs Trash Park in Night of Shame\"\n"
        "4. \"Students Spark Clean-Up Revolution\"\n"
        "5. \"Heatwave: 40°C Recorded in Seville\""),
  headline='Headline 1 uses a pun ("PURR-FECT") for humour; headline 2 uses alliteration ("Mayor\'s Mega Mall Madness") and the loaded word "Madness" to mock a decision; headline 3 uses loaded words ("Thugs", "Shame") to condemn; headline 4 uses a positive metaphor ("Spark ... Revolution"); headline 5 is neutral and factual.',
  dev=[('pun', 'PURR-FECT ENDING', 'the play on "perfect" and a cat\'s purr makes a light-hearted story fun and eye-catching', ['alliteration', 'statistic', 'loaded language']),
       ('alliteration', 'Mayor\'s Mega Mall Madness', 'the repeated "m" sound makes the headline memorable and mocking', ['pun', 'simile', 'onomatopoeia']),
       ('loaded words', 'Thugs Trash Park in Night of Shame', 'emotive words judge the people responsible and make readers angry', ['pun', 'neutral language', 'simile']),
       ('metaphor', 'Students Spark Clean-Up Revolution', 'the image of a spark starting a revolution makes a small action seem exciting and powerful', ['pun', 'onomatopoeia', 'statistic']),
       ('neutral, factual language', 'Heatwave: 40°C Recorded in Seville', 'a precise figure and no opinion words give information without judgement', ['pun', 'loaded language', 'alliteration'])],
  summary='Five headlines show different language choices: a pun, alliteration, loaded words, a metaphor and neutral factual reporting.')

P(id='comic_rooftop', kind='comic', title='graphic novel page described in words',
  text=("PANEL 1 (wide, from above): Two tiny figures on a rooftop at sunset; the whole city spreads beneath them. Caption: \"The last night before Kofi moved away.\"\n"
        "PANEL 2 (medium shot): Kofi and Ama sit side by side, legs dangling. No words.\n"
        "PANEL 3 (close-up): Ama's hand holds out a paper aeroplane. Speech bubble: \"Promise you'll write.\"\n"
        "PANEL 4 (extreme close-up, all colour drained to grey): Kofi's eyes, wet. Tiny speech bubble: \"Every day.\""),
  panels='The page moves from a wide, distant establishing shot to an extreme close-up, drawing the reader closer to the characters\' emotions. The silent second panel uses the gutter and lack of words to show a pause full of feeling, and the caption gives context the images cannot.',
  visual='Shot distance shrinks from wide (the city, small figures) to extreme close-up (Kofi\'s eyes), increasing intimacy. The high angle in panel 1 makes the friends look small against change. Colour shifts from sunset warmth to grey in the last panel, showing sadness. The tiny speech bubble suggests Kofi speaks quietly.',
  dev=[('caption', '"The last night before Kofi moved away."', 'the narrator\'s caption explains the situation and makes every image feel sad and important', ['speech bubble', 'sound effect', 'thought bubble']),
       ('silent panel', 'PANEL 2 ... No words.', 'the absence of words shows a quiet, emotional moment and slows the reader down', ['sound effect', 'caption', 'splash page']),
       ('symbolic object', 'a paper aeroplane', 'the aeroplane symbolises the distance and the letters that will keep the friendship alive', ['caption', 'sound effect', 'gutter'])],
  theme='friendship and saying goodbye',
  gq='How does the graphic novel page use visual techniques to present the friends\' goodbye?',
  gqa='The page moves from a wide, high-angle shot (small figures against a huge city, showing how big the change is) to an extreme close-up of Kofi\'s wet eyes, drawing the reader into his emotion. The silent second panel slows the pace; the paper aeroplane symbolises distance and future letters; and the drain of colour to grey with a tiny speech bubble shows quiet sadness.',
  summary='On the night before Kofi moves away, he and Ama sit on a rooftop; she gives him a paper aeroplane and asks him to write, and he tearfully promises to write every day.')

P(id='comic_ghostbus', kind='comic', title='graphic novel page described in words',
  text=("PANEL 1 (low angle): A double-decker bus looms out of thick fog, headlights glaring. Sound effect in jagged letters: \"SKREEEE!\"\n"
        "PANEL 2 (medium shot): Nia, 13, steps aboard. The bus is empty. Caption: \"The 11:45. The last bus. Or so I thought.\"\n"
        "PANEL 3 (over-the-shoulder shot): The driver's reflection in the mirror – he has no face.\n"
        "PANEL 4 (wide, tilted frame): The bus speeds away. Every window now has a passenger staring out."),
  panels='The four panels build a horror sequence: arrival, entering, discovery and a final shock. The gutters between panels force the reader to imagine what happens in between (when did the passengers appear?), which adds to the fear.',
  visual='The low angle in panel 1 makes the bus loom threateningly; the jagged "SKREEEE!" sound effect adds noise and alarm. The over-the-shoulder shot lets the reader discover the faceless driver with Nia. The tilted (Dutch angle) frame in panel 4 makes the world feel unbalanced and wrong.',
  dev=[('sound effect (onomatopoeia)', '"SKREEEE!"', 'the jagged lettering imitates screeching brakes and startles the reader', ['caption', 'thought bubble', 'speech bubble']),
       ('caption with foreshadowing', '"The last bus. Or so I thought."', 'Nia\'s retrospective narration hints that something strange is coming', ['sound effect', 'speech bubble', 'splash page']),
       ('tilted frame', 'PANEL 4 (wide, tilted frame)', 'the angled frame creates unease, showing that the normal world has been turned upside down', ['caption', 'sound effect', 'gutter'])],
  theme='the supernatural and fear',
  gq='How does the page use panels and visual techniques to build suspense?',
  gqa='The low-angle first panel and jagged sound effect make the bus threatening. The caption "Or so I thought" foreshadows danger. The over-the-shoulder third panel lets the reader discover the faceless driver alongside Nia, and the gutter before panel 4 leaves us to imagine how the passengers appeared, with the tilted frame making the final image feel wrong.',
  summary='Nia boards the empty last bus in the fog, sees that the driver has no face, and as the bus speeds away every window suddenly has a passenger staring out.')

P(id='speech_ocean', kind='speech', title='speech by a 14-year-old to a regional youth climate conference in Fiji',
  text=("Bula, everyone. My name is Losana, and my island is disappearing.\n"
        "Not in a hundred years. Now. Last year, the sea came into my grandmother's kitchen. Twice.\n"
        "Some people say: you are just a child, what can you do? I say: I am a child, and that is exactly why I am here. Because it is my future you are spending.\n"
        "So I ask you three things: listen to islands, cut emissions, and fund the walls that keep the sea out of kitchens.\n"
        "Vinaka vakalevu – thank you."),
  speechstruct='Hook: a shocking personal statement ("my island is disappearing"). Argument: the evidence of the sea in her grandmother\'s kitchen, a counterargument ("you are just a child") and rebuttal. Conclusion: three clear demands and a polite thank-you in Fijian.',
  aud='Delegates at a youth climate conference, including adults with power to act; she addresses them directly ("it is my future you are spending").',
  purp='To persuade the audience to listen to island nations and act on climate change by cutting emissions and funding sea walls.',
  tone='urgent and determined', tw=['playful', 'bored', 'sarcastic'], tonex='personal evidence and direct challenges create urgency.',
  dev=[('shocking opening', 'my island is disappearing', 'the dramatic hook grabs attention immediately and makes the issue personal', ['statistic', 'simile', 'onomatopoeia']),
       ('short sentences', 'Not in a hundred years. Now.', 'the short sentences correct the audience\'s assumption and stress urgency', ['simile', 'oxymoron', 'alliteration']),
       ('counterargument and rebuttal', 'Some people say: you are just a child ... I say: I am a child, and that is exactly why I am here.', 'she turns a criticism into her strongest argument', ['simile', 'statistic', 'onomatopoeia']),
       ('tricolon of demands', 'listen to islands, cut emissions, and fund the walls', 'three clear actions make the conclusion memorable', ['simile', 'personification', 'onomatopoeia'])],
  delivery='Speak slowly and clearly on the hook, pause after "Now.", make eye contact with the delegates on "it is my future you are spending", count the three demands on her fingers, and soften her voice for the closing thank-you.',
  questions='Good questions for Losana: "What is your community already doing to adapt?", "Which of your three demands is most urgent, and why?", "How can young people in other countries support islands like yours?"',
  gq='How does Losana make her speech powerful for her audience?',
  gqa='She opens with a shocking personal hook and short sentences ("Not in a hundred years. Now.") that stress urgency. The concrete image of the sea in her grandmother\'s kitchen gives emotional evidence. She anticipates the objection "you are just a child" and rebuts it, and finishes with a memorable tricolon of demands, using Fijian greetings to frame the speech with her identity.',
  summary='Losana, 14, tells delegates her island is already flooding and asks them to listen to islands, cut emissions and fund sea walls.')

P(id='speech_award', kind='speech', title='acceptance speech by a student winning a school writing award',
  text=("Thank you. I genuinely did not prepare this, because I genuinely did not think I would win. (Laughter.)\n"
        "Two years ago, Ms Ferreira handed back my first story with one comment: 'More you, please.' I didn't understand. I thought stories had to sound like books.\n"
        "This story is about my little brother, our noisy flat and the day he lost his first tooth in a mango. It is the most 'me' thing I have ever written.\n"
        "So thank you, Ms Ferreira. And thank you, mango."),
  speechstruct='Hook: humorous honesty that he did not prepare. Body: an anecdote about a teacher\'s comment and what the story is about. Conclusion: thanks to the teacher and a comic callback ("thank you, mango").',
  aud='An audience of students, teachers and parents at an awards ceremony.',
  purp='To thank his teacher and share what he learned about writing in his own voice, while entertaining the audience.',
  tone='modest and humorous', tw=['arrogant', 'furious', 'formal and cold'], tonex='self-deprecating jokes and gratitude create warmth.',
  dev=[('self-deprecating humour', 'I genuinely did not prepare this, because I genuinely did not think I would win', 'the modest joke wins the audience over immediately', ['statistic', 'simile', 'personification']),
       ('quotation in an anecdote', '\'More you, please.\'', 'the teacher\'s short comment becomes the central lesson of the speech', ['simile', 'statistic', 'hyperbole']),
       ('callback humour', 'And thank you, mango.', 'returning to the funny detail ends on a laugh and a memorable image', ['flashback', 'statistic', 'oxymoron'])],
  delivery='Relaxed posture and a smile on the opening joke; pause for the laughter; turn towards Ms Ferreira when thanking her; slow down for "More you, please"; deliver the final line with comic timing.',
  questions='Good questions: "How did you find your own voice?", "What advice would you give a younger writer?", "Why did you choose to write about your brother?"',
  summary='An award-winning student thanks his teacher, whose comment "More you, please" taught him to write in his own voice, and jokes about his story of his brother\'s tooth lost in a mango.')

P(id='podcast_qa', kind='interview', title='transcript of the question-and-answer session after a student talk on food waste',
  text=("SPEAKER (Hana, 13): ...so one third of all food produced is wasted. Any questions?\n"
        "STUDENT 1: Yeah, but what can we actually do?\n"
        "HANA: Good question! Plan meals, use leftovers, and our canteen could donate unsold food.\n"
        "STUDENT 2: You said 'one third'. Where is that number from?\n"
        "HANA: The UN Food and Agriculture Organization. I should have said that – thank you.\n"
        "STUDENT 3: I disagree. Isn't the real problem supermarkets, not families?\n"
        "HANA: Both matter. Supermarkets waste a lot, but in many countries households waste even more."),
  questions='Student 1 asks a practical, open question about solutions; Student 2 asks a source/evidence question, which tests the reliability of the statistic; Student 3 challenges the argument respectfully with a counterpoint, which pushes the speaker to give a balanced answer.',
  dev=[('open question', '"what can we actually do?"', 'it invites the speaker to give practical solutions', ['closed question', 'rhetorical question', 'statement']),
       ('question about evidence', '"Where is that number from?"', 'it checks the reliability of the speaker\'s statistic', ['rhetorical question', 'leading question', 'compliment'])],
  struct=[('the order of questions from practical to evidence to challenge', 'the session moves from understanding to testing and debating the speaker\'s ideas')],
  gq='How do the listeners\' questions help to develop and test the speaker\'s ideas?',
  gqa='Student 1\'s open question leads Hana to suggest practical solutions; Student 2\'s request for a source makes her credit the UN FAO and strengthens her evidence; Student 3\'s respectful challenge pushes her to give a balanced response (both supermarkets and households). Hana responds positively ("Good question!", "thank you"), showing good listening on both sides.',
  summary='After Hana\'s talk on food waste, students ask what they can do, where her statistic comes from, and whether supermarkets are the real problem; she answers each one.')

K.pair('manu', 'deucalion', 'Compare how the two myths present the flood and the survival of humanity.',
       'Both myths include a great flood, a chosen survivor and a new beginning for humanity. In Text A the god Vishnu saves Manu as a reward for kindness to a tiny fish, so the flood is a natural disaster and survival comes from compassion; in Text B Zeus sends the flood as a punishment for human cruelty, and survival requires solving a riddle. '
       'Text A uses repetition ("in a jar, then a pond, then the sea") to show growing care; Text B uses a riddle ("the bones of your mother") and a revelation. Both suggest a close link between humans and the natural world – seeds of every plant in Text A, people born from Earth\'s stones in Text B.',
       sim='both include a warning or message from a god, a boat or chest that survives the flood, and a new beginning for humanity.',
       diff='in Text A the flood is survived because Manu was kind to a fish, whereas in Text B the flood is Zeus\'s punishment and survival depends on solving a riddle.')
K.pair('pangu', 'rangi', 'Compare how the two creation myths explain the separation of the sky and the earth.',
       'In both myths the sky and earth were once joined and a powerful being pushes them apart. Text A (Chinese) presents one giant, Pangu, whose own body becomes nature after his death (sacrifice); Text B (Maori) presents a family – the Sky Father and Earth Mother – separated by their son Tāne. '
       'Text A emphasises effort and transformation (a list of body parts becoming nature); Text B emphasises love and loss through personification (rain as tears, mist as sighs). Both explain natural features and show that people and nature are connected.',
       sim='both explain how the sky and earth were separated by a powerful being who pushes them apart.',
       diff='Text A focuses on one giant whose body becomes nature, while Text B tells a family story in which rain and mist show the parents\' grief.')
K.pair('attic', 'storm_drama', 'Compare how the writers build suspense in a story extract and a playscript extract.',
       'Both use dark settings, unexplained sounds and a sudden ending. Text A (story) builds suspense through narration: a rhetorical question, the simile "like a warning", short sentences and a final one-line revelation (a cliffhanger). '
       'Text B (playscript) relies on stage directions (rain, flickering lights, three knocks), dialogue and comic relief ("a very polite wind"), ending with a blackout. The story can show Leila\'s thoughts; the playscript must show fear through action and sound for a live audience.',
       sim='both create suspense with a dark setting, a mysterious sound (humming; three knocks) and an unresolved ending.',
       diff='Text A builds suspense through narration and the character\'s thoughts, whereas Text B uses stage directions, sound and lighting for an audience.')
K.pair('skate_a', 'skate_b', 'Compare how the two reports present the opening of the skatepark.',
       'Both report the same facts (opening on Saturday, €180,000 cost) but select and frame them differently. Text A\'s headline ("Celebrate", "Finally") and quotations from a teenage campaigner and a councillor present the park as a victory and "an investment". '
       'Text B\'s headline foregrounds "fear", "noise" and the cost, quotes only a complaining resident, links the cost to cuts in street lighting and omits young people. The comparison shows how word choice, quotation and omission create bias.',
       sim='both include the same fact that the council spent €180,000 and that the park opened on Saturday.',
       diff='Text A quotes only supporters and celebrates the opening, while Text B quotes only a resident who complains and leaves out young people.')
K.pair('wangari', 'owens', 'Compare how the two biographies present people who overcame challenges.',
       'Both are chronological, third-person biographies using dates and achievements. Text A presents Maathai\'s achievements as a series of "firsts" and links her childhood memories to her environmental work. Text B places Owens\'s victories in the context of Nazi propaganda and American segregation, using irony ("Yet...") and his own quotation to show injustice. '
       'Maathai changed her society; Owens challenged racism abroad but still faced it at home.',
       sim='both use dates and "firsts" or medals to present a person who achieved something remarkable despite difficulties.',
       diff='Text A links Maathai\'s childhood to her work for change, whereas Text B uses irony to show that Owens\'s success did not free him from racism at home.')
K.pair('treehouse', 'comic_rooftop', 'Compare how the two texts present friendships under pressure.',
       'Both show a friendship changing: Text A through a first-person narrator\'s painful observations (short sentences, the symbolic faded sign); Text B through images (shot distance shrinking to an extreme close-up, a silent panel, colour draining to grey). '
       'In Text A the friendship fades because one friend wants to fit in; in Text B distance separates friends who want to stay close, and the paper aeroplane offers hope.',
       sim='both use a symbolic object – the faded sign and the paper aeroplane – to represent the friendship.',
       diff='in Text A one friend is drifting away by choice, whereas in Text B the friends are separated by a move but promise to stay in touch.')


# =============================================================================================
# Grammar data for chapter 10 (Criterion D)
# =============================================================================================
SENT = [
    ('The bus was late.', 'simple'), ('Mina laughed at the joke.', 'simple'), ('Rain fell all night over the village.', 'simple'),
    ('The volcano rumbled, and the villagers ran.', 'compound'), ('I wanted to go, but my bike had a flat tyre.', 'compound'),
    ('You can take the train, or you can walk along the canal.', 'compound'), ('The shop was closed, so we went home.', 'compound'),
    ('Although it was raining, the match continued.', 'complex'), ('When the bell rang, everyone rushed outside.', 'complex'),
    ('The boy who found the wallet handed it in.', 'complex'), ('Because she practised every day, Aiko won the competition.', 'complex'),
    ('If you finish early, you can read quietly.', 'complex'),
    ('Although he was tired, Omar finished his essay, and then he went to bed.', 'compound-complex'),
    ('When the storm ended, the children went outside, but the streets were flooded.', 'compound-complex'),
]
TYPE_WRONG = {'simple': ['compound', 'complex', 'compound-complex'], 'compound': ['simple', 'complex', 'compound-complex'],
              'complex': ['simple', 'compound', 'compound-complex'], 'compound-complex': ['simple', 'compound', 'complex']}
TYPE_WHY = {'simple': 'it has one independent clause (one subject-verb unit)',
            'compound': 'it joins two independent clauses with a coordinating conjunction (and, but, or, so)',
            'complex': 'it has one independent clause and at least one dependent (subordinate) clause, introduced by a word such as although, when, because, if or who',
            'compound-complex': 'it has at least two independent clauses and at least one dependent clause'}
COMBINE = [
    ('The film was long. We enjoyed it.', 'although', 'Although the film was long, we enjoyed it.'),
    ('The power went out. We lit candles.', 'when', 'When the power went out, we lit candles.'),
    ('Sara missed the bus. She overslept.', 'because', 'Sara missed the bus because she overslept.'),
    ('It stops raining. We will play outside.', 'if', 'If it stops raining, we will play outside.'),
    ('The dog barked. The postman arrived.', 'as soon as', 'The dog barked as soon as the postman arrived.'),
    ('My cousin lives in Nairobi. She is visiting us.', 'who', 'My cousin, who lives in Nairobi, is visiting us.'),
    ('The test was difficult. Most students passed.', 'even though', 'Even though the test was difficult, most students passed.'),
    ('The team trained hard. They won the final.', 'so', 'The team trained hard, so they won the final.'),
]
PUNCT = [
    ('its the dogs bowl', "It's the dog's bowl.", 'apostrophes: "it\'s" = it is; "dog\'s" shows possession (one dog)'),
    ('the childrens coats were wet', "The children's coats were wet.", 'apostrophe for possession with a plural that does not end in s: children\'s'),
    ('we visited paris rome and madrid', 'We visited Paris, Rome and Madrid.', 'commas separate items in a list; capital letters for proper nouns'),
    ('where are you going asked mum', '"Where are you going?" asked Mum.', 'speech marks around spoken words; the question mark goes inside the speech marks'),
    ('i love football its my favourite sport', "I love football; it's my favourite sport.", 'a semicolon joins two closely related independent clauses; "it\'s" = it is'),
    ('after the match we went for pizza', 'After the match, we went for pizza.', 'a comma after an introductory phrase'),
    ('the girls bikes were stolen (more than one girl)', "The girls' bikes were stolen.", 'plural possession: the apostrophe goes after the s'),
    ('stop shouted the guard', '"Stop!" shouted the guard.', 'speech marks and an exclamation mark inside them'),
    ('my brother who is twelve plays the drums', 'My brother, who is twelve, plays the drums.', 'commas around extra (non-essential) information'),
    ('the weather was awful we stayed inside', 'The weather was awful; we stayed inside.', 'a semicolon (or a full stop) prevents a comma splice between two independent clauses'),
]
REGISTER = [
    ('Hey Mr Tan, can u let me off homework cos I was ill?', 'Dear Mr Tan, Could I please have an extension for my homework, as I was unwell?'),
    ('The new park is well good and loads of kids go there.', 'The new park is excellent and is popular with many young people.'),
    ('We need to sort out the rubbish problem ASAP.', 'We need to address the problem of litter as soon as possible.'),
    ('Gonna be late, sorry!!', 'I apologise, but I will be arriving late.'),
    ('The trip was a total disaster, lol.', 'Unfortunately, the trip did not go as planned.'),
    ('Loads of people reckon the canteen food is rubbish.', 'Many students believe that the quality of canteen food is poor.'),
]
CONNECT = [
    ('The weather was cold. ___, we went swimming.', 'Nevertheless', ['Because', 'Similarly', 'For example'], 'contrast: the swimming happened despite the cold'),
    ('Exercise improves fitness. ___, it can boost your mood.', 'Furthermore', ['However', 'Therefore', 'Instead'], 'addition: a second benefit'),
    ('He did not revise. ___, he failed the test.', 'As a result', ['Moreover', 'However', 'In contrast'], 'cause and effect'),
    ('Many animals are endangered. ___, the snow leopard has fewer than 7,000 left in the wild.', 'For example', ['However', 'Finally', 'Therefore'], 'an example of the general point'),
    ('First, mix the flour and water. ___, knead the dough.', 'Next', ['However', 'In conclusion', 'Similarly'], 'sequence'),
    ('Text A is cheerful. ___, Text B is gloomy.', 'In contrast', ['Similarly', 'Therefore', 'Furthermore'], 'comparison showing difference'),
]
PROOF = [
    ('Yesterday me and my freind goes to the beach. We seen a dolphin, it was amazing.', 'Yesterday my friend and I went to the beach. We saw a dolphin; it was amazing.', '"me and my freind" → "my friend and I" (subject pronoun, spelling); "goes" → "went" (tense); "seen" → "saw"; comma splice → semicolon or full stop'),
    ('Their going to the museum tomorow, there teacher said its free.', 'They\'re going to the museum tomorrow; their teacher said it\'s free.', 'their/they\'re/there confusion; spelling of "tomorrow"; comma splice; "its" → "it\'s"'),
    ('The team played good but they lost there last match becuase of the rain.', 'The team played well, but they lost their last match because of the rain.', '"good" → "well" (adverb); comma before "but"; "there" → "their"; spelling of "because"'),
    ('Every students in the class have finished they\'re project.', 'Every student in the class has finished their project.', '"Every students" → "Every student"; subject-verb agreement "has"; "they\'re" → "their"'),
    ('I could of won the race if I would of trained harder', 'I could have won the race if I had trained harder.', '"could of" → "could have"; "would of trained" → "had trained" (correct conditional); missing full stop'),
]


# =============================================================================================
# ch01 Myths, Legends and the Hero's Journey
# =============================================================================================
MYTH = {'myth', 'legend'}
H('ch01-st1',
  terms=[('myth', 'a traditional story, often sacred to a culture, involving gods or supernatural beings, that explains the origins of the world, nature or customs'),
         ('legend', 'a traditional story about a hero or event linked to a real place or historical time, with exaggerated or supernatural elements'),
         ('origin (explanation) myth', 'a myth that explains how something began – the world, a natural feature, an animal or a custom'),
         ('oral tradition', 'the passing down of stories by word of mouth from one generation to the next, before or alongside writing'),
         ('pantheon', 'all the gods of a particular culture or religion, such as the Greek or Norse gods')],
  facts=[('Which feature most clearly distinguishes a legend from a myth?', 'It is linked to a real place or historical figure', ['It has a happy ending', 'It is always written in verse', 'It contains no supernatural events'], 'Legends such as Sundiata or King Arthur are rooted in history; myths usually happen in a timeless past among gods.'),
         ('Why do many myths end with a phrase such as "And that is why..."?', 'Because they explain the origin of something in nature or society', ['Because they were written for children', 'Because they are fables with a moral', 'Because they are based on scientific evidence'], 'Origin myths explain why the world is as it is.'),
         ('In the Polynesian story, what does Māui do to the sun?', 'He snares it and forces it to travel more slowly', ['He steals it and hides it in a cave', 'He marries it', 'He turns it into the moon'], 'The story explains the length of the day.'),
         ('Who are the griots of West Africa?', 'Storytellers, historians and musicians who preserve history and legends orally', ['Gods of the forest', 'Kings of the Mali Empire', 'Writers of the first printed books'], 'Griots have passed down the legend of Sundiata for centuries.')],
  why=[('Explain why myths often include gods or supernatural beings.', 'Myths explain things people could not explain scientifically, such as thunder or the sun, so powerful beings provide causes and make the world seem ordered and meaningful.'),
       ('Explain why myths were usually passed down orally.', 'Many cultures told stories before writing was common; repetition, patterns and memorable images made myths easy to remember, perform and share across generations.'),
       ('Explain why myths can tell us about the values of the culture that created them.', 'The heroes, rewards and punishments in a myth show what a culture admired or feared – for example, the Manu story rewards kindness, and the Greek flood punishes cruelty.')],
  contrast=[('a myth', 'a legend', 'A myth usually takes place in a timeless past and involves gods explaining the origins of the world; a legend is rooted in a real place or historical person (such as Sundiata of Mali) but includes exaggerated or supernatural deeds.'),
            ('a myth', 'a fable', 'A myth explains origins or beliefs through gods and heroes; a fable is a short story, often with animals, that teaches a clear moral lesson.')],
  misc=[('Myths are just lies, so they have no value.', 'Myths are not meant as factual reports; they express a culture\'s beliefs, values and ways of understanding the world, and they still shape literature, film and language today.'),
        ('A legend is always completely true.', 'A legend is linked to real people or places, but its events are often exaggerated or supernatural, so it mixes history with imagination.')],
  apply=[('Name the natural feature that each of these mythical explanations is about: (a) Rangi\'s tears; (b) Papa\'s sighs; (c) Pangu\'s blood.', '(a) rain; (b) morning mist; (c) rivers.', 3),
         ('Write two sentences explaining one convention of myths, using an example from any myth you know.', 'For example: Myths often explain how something in nature began. In the Māori story, rain is explained as the tears of the Sky Father for the Earth Mother.', 2)],
  evaluate=[('Myths are still relevant to teenagers today.', ['modern films and books (superhero stories, fantasy) use mythical heroes and quests', 'myths explore universal themes like courage, family and loss'], ['science now explains nature', 'some myths reflect old-fashioned values'], 'Myths remain relevant because their patterns and themes still shape stories and help us explore what it means to be human, even if we no longer read them as explanations of nature.')],
  extended=[('Choose a myth or legend you know. Explain how it shows three conventions of the genre, using evidence.', 'Indicative content: identifies three conventions (supernatural beings, explanation of origins, a hero\'s quest or test, oral storytelling features); supports each with a specific detail; explains what each reveals about the culture.', 6, 'long')])
K.kind_mcq('ch01-st1', MYTH)
pq('ch01-st1', ('C2', 'C3'), (1, 4), MYTH, 'myth_conv', ['Identify two conventions of myths or legends in this text and explain how each is used.',
                                                    'How can you tell that this text is a myth or legend? Refer to two features.',
                                                    'Explain which features of this text are typical of traditional stories.'], crit=CRIT_A)
pq('ch01-st1', 'C3', (1, 4), MYTH, 'explains', ['What does this myth explain about the natural world or society?',
                                                'Identify what this story explains and how it explains it.'], crit=CRIT_A)
pq('ch01-st1', ('C3', 'C4'), (2, 5), MYTH, 'culture', ['What does this story suggest about the values of the culture that created it?',
                                                     'Explain what this myth or legend reveals about the beliefs of the people who told it.'], crit=CRIT_OPEN)
K.dev_mcq('ch01-st1', MYTH)

H('ch01-st2',
  terms=[('hero\'s journey', 'a common story pattern, described by Joseph Campbell, in which a hero leaves the ordinary world, faces tests and returns transformed with a reward'),
         ('call to adventure', 'the stage of the hero\'s journey when the hero is given a challenge or problem that disrupts the ordinary world'),
         ('mentor', 'a wise guide who helps the hero, often with advice or a magical gift'),
         ('threshold', 'the point at which the hero leaves the familiar world and enters the unknown'),
         ('ordeal', 'the hero\'s greatest test or crisis, often a battle or a moment close to death')],
  facts=[('In the hero\'s journey, what usually comes immediately after the call to adventure?', 'The refusal of the call (doubt or fear)', ['The return with the reward', 'The final battle', 'Meeting the hero\'s children'], 'Heroes often hesitate before accepting the challenge.'),
         ('In the Māui story, who plays the role of the mentor?', 'His grandmother, who gives him the magic jawbone', ['His brothers', 'The sun', 'The chief of the village'], 'The mentor gives a gift that helps the hero.'),
         ('Which stage of the hero\'s journey is the final one?', 'The return with the reward (elixir)', ['The call to adventure', 'Meeting the mentor', 'Crossing the threshold'], 'The hero returns home changed and brings something that benefits others.')],
  why=[('Explain why the hero\'s journey is found in stories from many different cultures.', 'It reflects universal human experiences – facing challenges, growing up and returning changed – so storytellers everywhere have used similar patterns.'),
       ('Explain why heroes often refuse the call to adventure at first.', 'The hesitation shows that the hero is human and afraid, which makes the later courage more impressive and lets readers identify with them.'),
       ('Explain why the hero usually returns home at the end of the journey.', 'The return shows that the hero has changed and brings back a reward (knowledge, a gift, safety) that benefits the community, giving the journey its purpose.')],
  contrast=[('the ordinary world', 'the special world', 'The ordinary world is the hero\'s normal life at the start of the story; the special world is the unfamiliar, dangerous place the hero enters after crossing the threshold, where the tests happen.')],
  misc=[('Every story must follow all twelve stages of the hero\'s journey in exact order.', 'The hero\'s journey is a flexible pattern; many stories skip, combine or reorder stages.'),
        ('The mentor is always an old man with a beard.', 'A mentor can be anyone – a grandmother (Māui), a friend, an animal or even a voice – who guides the hero.')],
  apply=[('Put these stages of the hero\'s journey in order: ordeal; call to adventure; return with the reward; meeting the mentor; ordinary world.', 'Ordinary world – call to adventure – meeting the mentor – ordeal – return with the reward.', 3),
         ('Choose a film or novel you know. Identify the call to adventure, the mentor and the ordeal.', 'Any valid example, e.g. in a superhero film: the call is discovering a power or threat; the mentor is a teacher figure; the ordeal is the final battle. 1 mark per correctly identified stage with a specific detail.', 3),
         ('Map the legend of Sundiata onto three stages of the hero\'s journey.', 'Ordinary world: he cannot walk and is mocked. Call/threshold: his mother is insulted and he stands with the iron rod. Later ordeal and return: exile, defeat of Soumaoro and founding of the Mali Empire.', 3)],
  evaluate=[('The hero\'s journey makes stories predictable.', ['readers recognise stages and can guess what happens', 'many blockbuster films feel similar'], ['the pattern is flexible and writers vary it', 'familiar patterns satisfy readers while characters and settings make stories fresh'], 'The pattern can feel predictable if used mechanically, but skilled writers use it as a framework and surprise readers within it.')],
  extended=[('Plan a hero\'s journey story set in your own town: list six stages with one sentence for each.', 'Indicative content: six clearly named stages in a logical order (ordinary world, call, refusal, mentor, ordeal, return); a consistent hero and setting; a reward that changes the hero or community.', 6, 'long')])
pq('ch01-st2', ('C3', 'C4'), (2, 5), MYTH, 'hero', ['Identify three stages of the hero\'s journey in this story, with evidence for each.',
                                                  'How does this story follow the pattern of the hero\'s journey? Refer to specific events.',
                                                  'Map the events of this text onto stages of the hero\'s journey.'], crit=CRIT_A)
para('ch01-st2', MYTH, frames=['{gq}\nWrite a PEE paragraph (point, evidence, explanation) that answers the question.',
                              'Answer in about 200 words: {gq} Refer closely to the text.'])
pq('ch01-st2', 'C2', (1, 3), MYTH, 'tone', TONE_Q, crit=CRIT_B)

H('ch01-st3',
  terms=[('creation myth', 'a myth that explains how the world, the universe or people came into being'),
         ('flood myth', 'a myth in which a great flood destroys the world and a chosen survivor allows life to begin again'),
         ('archetype', 'a typical character, situation or symbol that appears in stories across many cultures, such as the hero, the flood or the wise mentor'),
         ('motif', 'a recurring element or idea in stories, such as water, light or a journey')],
  facts=[('Which of these is a flood myth from Hindu tradition?', 'The story of Manu and the fish', ['The story of Pangu', 'The story of Māui and the sun', 'The story of Rangi and Papa'], 'Vishnu, as a fish, saves Manu from the flood.'),
         ('In the Greek flood myth, how are new people created?', 'From stones thrown over the shoulders of Deucalion and Pyrrha', ['From the bones of animals', 'From clay shaped by Zeus', 'From seeds carried on a boat'], 'The "bones of your mother" are the stones of the Earth.'),
         ('What do the creation myths of Pangu and of Rangi and Papa have in common?', 'Sky and earth were once joined and are pushed apart', ['Both begin with a flood', 'Both are set in Greece', 'Both have no gods'], 'Separation of sky and earth is a shared archetype.')],
  why=[('Explain why flood myths appear in many different cultures.', 'Many early civilisations lived near rivers and coasts and experienced devastating floods; the flood story also expresses the idea of cleansing and a new beginning.'),
       ('Explain why comparing myths across cultures is useful.', 'It reveals shared human questions (how did the world begin?) and different cultural values, such as whether the flood is a punishment or a natural disaster.')],
  contrast=[('the Greek flood myth', 'the Hindu flood myth of Manu', 'In the Greek myth, Zeus sends the flood to punish human cruelty and survivors must solve a riddle; in the Manu story, the flood is a coming disaster and Manu is saved because he was kind to a small fish.')],
  misc=[('Cultures with similar myths must have copied each other.', 'Similar myths can develop independently because people everywhere face similar experiences (floods, darkness, the sky) and ask similar questions.')],
  apply=[('Complete the comparison: "In the Pangu myth, the world is made from ______, whereas in the Māori story, rain and mist are explained as ______."', 'Pangu\'s body (breath, voice, eyes, blood); the tears and sighs of the separated Sky Father and Earth Mother.', 2),
         ('Write a topic sentence for a paragraph comparing two flood myths, using a comparative connective.', 'For example: "Whereas the Greek flood is a punishment from Zeus, the flood in the Manu story is survived through kindness, showing different ideas about why disaster comes."', 2)],
  evaluate=[('The similarities between myths from different cultures are more important than the differences.', ['shared archetypes show universal human concerns', 'similarities connect cultures'], ['differences reveal each culture\'s distinct values and landscape', 'ignoring differences can erase cultural identity'], 'Both matter: similarities show what humans share, while differences show what makes each culture unique; a good comparison explores both.')])
K.compare('ch01-st3', d=(3, 5), only=['manu', 'pangu'])
K.compare_short('ch01-st3', c='C3', d=(2, 4), only=['manu', 'pangu'])
pq('ch01-st3', 'C3', (1, 4), MYTH, 'explains', ['Explain what this myth explains and compare it briefly with another myth you know.',
                                                'What question about the world does this myth answer?'], crit=CRIT_A)
pq('ch01-st3', 'C2', (2, 4), MYTH, 'culture', ['Explain one value of the culture that created this myth.'], crit=CRIT_OPEN)

H('ch01-st4',
  terms=[('modern myth', 'a new story written today that uses the conventions of traditional myths to explain something in the modern world'),
         ('narrative voice', 'the "voice" telling a story; myths often use a third-person storyteller\'s voice'),
         ('formulaic opening', 'a traditional story opening such as "Long ago..." or "In the beginning..." that signals the genre')],
  facts=[('Which opening sentence best suits a modern myth?', '"Long ago, when the internet was young, the Signal Spirit lived in the clouds."', ['"The Wi-Fi was slow today, so I complained."', '"Scientists have measured internet speeds."', '"Click here to improve your Wi-Fi."'], 'It uses a formulaic myth opening and a supernatural being.'),
         ('Which ending best shows the conventions of an origin myth?', '"And that is why phones grow warm when you hold them for too long."', ['"Then I went to bed."', '"The end. Please like and subscribe."', '"Nobody knows what happened next."'], 'Origin myths end by explaining something.')],
  why=[('Explain why a writer might use the hero\'s journey when writing a modern myth.', 'It gives a clear, satisfying structure (call, test, return) that readers recognise, so the writer can focus on making the setting and hero original.'),
       ('Explain why modern myths often explain technology or city life.', 'Writers use the old form to make familiar modern things seem magical and to comment on how they affect our lives.')],
  contrast=[('a traditional myth', 'a modern myth', 'A traditional myth was passed down orally within a culture and expresses its sacred beliefs; a modern myth is written by an individual today, borrowing myth conventions to explain or comment on something in the modern world.'),
            ('a formulaic opening', 'a narrative hook', 'A formulaic opening ("Long ago...") signals the genre through tradition; a narrative hook grabs attention through surprise or mystery. A modern myth can combine both.')],
  misc=[('A modern myth does not need any supernatural elements.', 'Supernatural beings or forces are a key convention of myth; without them it is simply a realistic story.'),
        ('A modern myth must be set in ancient times.', 'A modern myth applies traditional conventions to the present – cities, technology, school life – which is what makes it modern.'),
        ('The "And that is why..." ending is too childish for a modern myth.', 'The explanatory ending is a defining convention of origin myths; writers can use it playfully or seriously to give the story its purpose.')],
  apply=[('Write the opening two sentences of a modern myth that explains why traffic lights are red, amber and green.', 'Indicative: formulaic opening ("Long ago, when cities were young..."); a supernatural being or force; a hint of the problem. 1 mark for genre conventions, 1 for imaginative idea.', 2),
         ('Plan a modern myth explaining why phones need charging every night: name the hero, the supernatural being, the challenge and the explanation at the end.', 'Any coherent plan: a hero (e.g. a girl who stays up too late), a being (e.g. the Battery Spirit), a challenge or bargain, and an ending ("And that is why...").', 4)],
  evaluate=[('Modern myths are less meaningful than traditional myths.', ['traditional myths carry centuries of cultural belief', 'modern myths can feel like jokes'], ['modern myths comment on our world and values', 'all myths were once new'], 'Modern myths can be just as meaningful when they explore real modern concerns (loneliness, technology) through the myth form.')],
  extended=[('Write a modern myth (about 400 words) that explains a feature of your town or city, using the stages of the hero\'s journey.', 'Indicative content: formulaic opening; supernatural being; a hero with a call and a test; the hero\'s journey structure; vivid description; an "And that is why..." ending. Criteria B, C, D.', 12, 'long'),
            ('Write a modern myth that explains why teenagers need more sleep than adults. Use at least two conventions of traditional myths.', 'Indicative content: a creative explanation involving supernatural beings; myth conventions (formulaic opening, a test, an explanatory ending); an engaging storytelling voice. Criteria C and D.', 8, 'long')])
pq('ch01-st4', 'C3', (2, 4), None, 'myth_conv', ['Identify two myth conventions that this writer uses, and suggest one more convention you would add if you rewrote it.'], ids=['modern_myth', 'pangu', 'maui'], crit=CRIT_A)
write('ch01-st4', ids=['maui'])
K.prompts('ch01-st4', 'one', c='C4', d=(3, 5))
K.prompts('ch01-st4', 'open', c='C3', d=(2, 4))


# =============================================================================================
# ch02 Novel Study: Friendship and Belonging
# =============================================================================================
NOV = {'prose'}
H('ch02-st1',
  terms=[('characterisation', 'the methods a writer uses to create and reveal a character: actions, speech, thoughts, appearance and others\' reactions'),
         ('inference', 'a conclusion the reader works out from clues in the text, rather than from something stated directly'),
         ('direct characterisation', 'when the narrator tells the reader directly what a character is like (e.g. "She was shy")'),
         ('indirect characterisation', 'when the reader infers what a character is like from what they say, do and think')],
  facts=[('"Mei clutched the timetable she had folded so many times it was soft as cloth." What can we infer about Mei?', 'She is nervous', ['She is angry', 'She is bored', 'She is careless'], 'The repeated folding suggests anxiety.'),
         ('Which is an example of indirect characterisation?', '"He looked at his shoes when I waved."', ['"He was embarrassed."', '"He was a kind boy."', '"She was very shy."'], 'The action lets readers infer embarrassment.'),
         ('Which question helps you infer a character\'s feelings from a line of dialogue?', 'What does the way they speak suggest about how they feel?', ['How many words are in the line?', 'What colour is the character\'s hair?', 'Who published the novel?'], 'Inference uses clues in speech and action.')],
  why=[('Explain why writers often show a character\'s feelings through actions rather than stating them.', 'Showing invites readers to infer and makes characters feel real; readers become more involved when they work out feelings themselves.'),
       ('Explain why a character\'s thoughts are a useful clue to their personality.', 'Thoughts reveal what a character may hide from others, such as fear or kindness, giving the reader private knowledge.'),
       ('Explain why other characters\' reactions help us understand a character.', 'How others treat a character (laughing, welcoming, ignoring) shows how they are seen and can contrast with how they see themselves.')],
  contrast=[('direct characterisation', 'indirect characterisation', 'Direct characterisation tells the reader what a character is like ("She was brave"); indirect characterisation shows it through speech, actions and thoughts, so the reader infers it.')],
  misc=[('A character\'s personality can only be known if the narrator tells us.', 'Readers infer personality from actions, speech, thoughts and others\' reactions; most characterisation is indirect.'),
        ('If a character says they are fine, the reader should believe them.', 'Characters can hide feelings; their actions or the narrator\'s details may contradict their words, and readers should look for these clues.')],
  apply=[('Read this sentence: "Oliver told his mum he had loads of friends. It was easier than the truth." What can you infer about Oliver? Give one reason.', 'He is lonely (he has few or no friends) and wants to protect his mum from worrying; "easier than the truth" shows he hides his feelings.', 2),
         ('Write a sentence that shows (does not tell) that a character is excited.', 'Any sentence showing excitement through action or speech, e.g. "Ravi bounced on his toes, checking the clock for the tenth time." No marks for "Ravi was excited."', 2)],
  evaluate=[('Readers learn more about a character from what they do than from what they say.', ['actions can reveal hidden feelings (Dev looking at his shoes)', 'characters may lie in speech'], ['dialogue reveals voice, humour and relationships (Zara\'s chatter)', 'speech and action together are most revealing'], 'Actions are often more revealing because they can contradict words, but the best understanding comes from comparing both.')],
  extended=[('Choose a character from a novel you have studied. Explain how the writer reveals their personality through actions, speech and thoughts, with one quotation for each.', 'Indicative content: three methods with a short quotation each; inference about personality; effect on the reader. Criterion A and B.', 8, 'long')])
pq('ch02-st1', ('C3', 'C4'), (1, 5), NOV, 'char', CHAR_Q, crit=CRIT_A)
qa('ch02-st1', 'C3', (1, 4), NOV)
para('ch02-st1', NOV, c='C4', d=(3, 5))
K.vocab('ch02-st1', d=(1, 3), kinds=NOV)
K.vocab_explain('ch02-st1', c='C2', d=(2, 4), kinds=NOV)

H('ch02-st2',
  terms=[('first-person narration', 'a story told by a character using "I", so the reader sees events through that character\'s eyes'),
         ('third-person narration', 'a story told by a narrator outside the action using "he", "she" and "they"'),
         ('multiple narrators', 'a novel in which different characters take turns to tell the story, giving different points of view'),
         ('dramatic irony', 'when the reader knows something that a character does not'),
         ('unreliable narrator', 'a narrator whose account the reader cannot fully trust because of bias, limited knowledge or dishonesty')],
  facts=[('Which sentence is written in the first person?', '"I climbed the ladder alone."', ['"He climbed the ladder alone."', '"They climbed the ladder."', '"The ladder was climbed."'], 'First person uses "I".'),
         ('What is one effect of using two narrators to describe the same event?', 'The reader sees both sides and may realise each character misunderstands the other', ['The story becomes shorter', 'The reader learns nothing about feelings', 'It removes all dialogue'], 'Multiple narrators can create dramatic irony.'),
         ('Which is a limitation of first-person narration?', 'The reader only knows what the narrator knows or chooses to tell', ['The reader knows every character\'s thoughts', 'It cannot include dialogue', 'It must be in the past tense'], 'A single viewpoint limits information.')],
  why=[('Explain why a writer might choose first-person narration for a story about friendship.', 'It lets readers share the narrator\'s private feelings (hurt, loyalty, confusion) directly, creating sympathy and intimacy.'),
       ('Explain why a first-person narrator may not give the full truth about other characters.', 'They only see others from the outside and may be biased by their own feelings, so readers must infer what others really think.'),
       ('Explain how multiple narrators can create dramatic irony.', 'When each narrator reveals private thoughts, the reader knows things the other characters do not, so we watch misunderstandings unfold.')],
  contrast=[('first-person narration', 'third-person narration', 'First-person narration ("I") gives one character\'s inner view and voice; third-person narration ("he/she") comes from outside and may show one or several characters\' thoughts with more distance.')],
  misc=[('A first-person narrator is always the author.', 'The narrator is a character created by the author; their views, age and experiences may be very different from the author\'s.')],
  apply=[('Rewrite this sentence in the first person: "Mei stood at the door, her cheeks burning."', '"I stood at the door, my cheeks burning."', 1),
         ('Rewrite this first-person sentence in the third person: "I waved, but he looked at his shoes."', '"He waved, but Dev looked at his shoes." (or "The narrator waved..."). Any correct third-person version.', 1)],
  evaluate=[('First-person narration is the best way to make readers care about a character.', ['it gives direct access to feelings', 'the voice feels personal and honest'], ['third-person can show several characters and more context', 'a limited view may confuse readers'], 'First person creates strong intimacy, but third-person limited can be equally powerful while allowing wider perspective; the best choice depends on the story.')])
pq('ch02-st2', ('C2', 'C3'), (1, 4), NOV, 'pov', POV_Q, crit=CRIT_B)
pq('ch02-st2', 'C4', (3, 5), None, 'pov', ['Explain how the narrative perspective controls what the reader knows, and how the extract would change if told by another character.'], ids=['twovoices', 'treehouse', 'bench'], typ='long', crit=CRIT_AN)
write('ch02-st2', ids=['treehouse'])
K.dev_mcq('ch02-st2', NOV)

H('ch02-st3',
  terms=[('theme', 'a central idea or message explored in a text, such as friendship, belonging or growing up'),
         ('message', 'what the writer seems to want readers to think, learn or feel about a theme'),
         ('symbol', 'an object, person or place that represents a bigger idea (e.g. a faded sign representing a fading friendship)')],
  facts=[('Which is a theme rather than a plot event?', 'Belonging', ['Mei arrives at school', 'Dev waits at the bus stop', 'Oliver eats lunch'], 'A theme is an idea, not an event.'),
         ('How is a theme different from the subject of a story?', 'A theme is what the story says about its subject', ['A theme is the title', 'A theme is the setting', 'A theme is the first sentence'], 'Friendship is a subject; "friendships can change as we grow" is a theme statement.')],
  why=[('Explain why it is better to write a theme as a statement rather than a single word.', 'A single word ("friendship") only names a topic; a statement ("friendships can change painfully as we grow up") shows what the text says about it.'),
       ('Explain how a symbol can help to develop a theme.', 'A symbol gives a concrete image for an abstract idea; for example, the faded treehouse sign makes the theme of a fading friendship visible.')],
  contrast=[('a theme', 'a moral', 'A theme is an idea a text explores, often with complexity; a moral is a direct lesson the reader is told to learn, as in a fable.')],
  misc=[('A story can only have one theme.', 'Most stories explore several connected themes, such as friendship, identity and growing up.')],
  apply=[('Write a theme statement (one sentence) for a story about a new student who finds a friend through a shared hobby.', 'For example: "Shared interests can help people overcome loneliness and feel they belong." 1 mark for a statement, 1 for relevance.', 2),
         ('Identify a symbol in a story you have read and explain what it represents.', 'Any valid symbol with explanation (e.g. the paper aeroplane in a goodbye scene represents distance and the hope of staying in touch).', 2)],
  evaluate=[('The theme of a novel is whatever the reader thinks it is.', ['readers bring their own experiences', 'many themes can be valid'], ['interpretations must be supported by evidence in the text', 'the writer\'s choices guide meaning'], 'Readers can find different themes, but a convincing theme must be supported by evidence from the text.')])
pq('ch02-st3', ('C2', 'C3'), (1, 4), NOV, 'theme', THEME_Q, crit=CRIT_OPEN)
pq('ch02-st3', ('C3', 'C4'), (2, 5), NOV, 'message', ['What message about friendship or belonging does this extract suggest? Support your answer with evidence.',
                                                    'Explain what the writer might want readers to learn from this extract.'], crit=CRIT_OPEN)
pq('ch02-st3', 'C3', (2, 4), NOV, 'struct', STRUCT_Q, crit=CRIT_B)

H('ch02-st4',
  terms=[('PEE paragraph', 'an analytical paragraph that makes a Point, gives Evidence (a quotation) and Explains how the evidence supports the point'),
         ('embedded quotation', 'a short quotation built smoothly into your own sentence'),
         ('analysis', 'explaining how and why a writer\'s choices create meaning and effects, not just what happens'),
         ('topic sentence', 'the first sentence of a paragraph, which states its main point')],
  facts=[('Which sentence is the best "Point" for a PEE paragraph about Mei?', 'The writer presents Mei as anxious on her first day.', ['Mei goes to school.', '"Twenty-eight faces turned."', 'This shows a lot.'], 'A point is an arguable claim about the text.'),
         ('Which is an example of an embedded quotation?', 'Mei\'s timetable is "soft as cloth", showing how often she has folded it.', ['Quotation: "soft as cloth".', 'The writer uses a quotation.', '"Soft as cloth." This is a simile.'], 'The quotation is part of the student\'s sentence.'),
         ('What should the Explanation in a PEE paragraph do?', 'Explain how the evidence supports the point and its effect on the reader', ['Repeat the quotation', 'Retell the next event', 'Give the page number only'], 'Explanation is where analysis happens.')],
  why=[('Explain why retelling the story is not the same as analysing it.', 'Retelling describes what happens; analysis explains how the writer\'s choices (words, structure, techniques) create meaning and affect the reader.'),
       ('Explain why short quotations are usually better than long ones.', 'Short, precise quotations focus on the exact words being analysed and can be embedded smoothly, showing close reading.')],
  contrast=[('evidence', 'explanation', 'Evidence is the quotation or reference from the text; explanation is the writer\'s own analysis of what the evidence shows and how it affects the reader.')],
  misc=[('A PEE paragraph is complete once you have included a quotation.', 'The quotation must be explained: the analysis of word choice and effect is what earns marks.'),
        ('The more quotations you include, the better your paragraph.', 'One or two well-chosen, well-explained quotations are better than many unexplained ones.')],
  apply=[('Label the three parts of this paragraph as Point, Evidence or Explanation: (1) "The writer shows that the narrator feels rejected." (2) "When he waves, Dev \'looked at his shoes\'." (3) "This suggests Dev is embarrassed to be seen with him, which hurts the narrator."', '(1) Point; (2) Evidence; (3) Explanation.', 3),
         ('Improve this weak explanation: "This quotation shows he is sad." Quotation: "I took the sign down. Then I put it back up."', 'For example: "The contradictory actions show that the narrator cannot decide whether to give up on the friendship; he wants to move on but still hopes, which makes his sadness complex." Credit reference to specific words and effect.', 3),
         ('Write a PEE paragraph about how the writer presents Thabo in the missing-dog story, using the quotation "He thought about his mother\'s empty purse."', 'Point: Thabo is tempted by the reward because his family is poor. Evidence: the quotation. Explanation: the image of the "empty purse" shows financial need, making his kind choice more meaningful. Criteria A and B.', 4, 'long')],
  evaluate=[('The PEE structure makes all student writing sound the same.', ['it can become formulaic', 'strong writers vary their structure'], ['it guarantees evidence and explanation', 'it is a foundation that can be developed (PEEL, extended explanation)'], 'PEE is a useful foundation, especially in MYP 3, but writers should develop it by embedding evidence and linking ideas.')])
para('ch02-st4', NOV | {'story', 'poem'}, c='C4', d=(2, 5), frames=['{gq}\nWrite one PEE paragraph (point, evidence, explanation) that answers this question.',
                                                                     'Write a PEE paragraph in response to this question: {gq} Embed at least one short quotation.',
                                                                     'Write two linked PEE paragraphs (about 250 words) that answer: {gq}'])
pq('ch02-st4', 'C3', (2, 4), NOV, 'dev', ['Write a PEE paragraph explaining the effect of "{quote}".',
                                         'Explain, in point-evidence-explanation form, why the writer uses the {device} "{quote}".'], crit=CRIT_B)


# =============================================================================================
# ch03 Poetry: The Power of Imagery
# =============================================================================================
POEM = {'poem'}
H('ch03-st1',
  terms=[('simile', 'a comparison using "like" or "as" (e.g. "honk like geese")'),
         ('metaphor', 'a comparison that says one thing is another (e.g. "Her hands are maps")'),
         ('personification', 'giving human qualities to something non-human (e.g. "the street holds its breath")'),
         ('imagery', 'descriptive language that appeals to the senses and creates pictures in the reader\'s mind'),
         ('extended metaphor', 'a metaphor that is continued over several lines or a whole poem')],
  facts=[('"I wandered lonely as a cloud" (William Wordsworth). Which device is used?', 'Simile', ['Metaphor', 'Onomatopoeia', 'Alliteration'], 'It compares the speaker to a cloud using "as".'),
         ('"The moon, tired of competing, hides behind the billboards." Which device is used?', 'Personification', ['Simile', 'Rhyme', 'Statistic'], 'The moon is given human feelings and actions.'),
         ('"Her hands are maps of seventy years." Which device is used?', 'Metaphor', ['Simile', 'Personification', 'Onomatopoeia'], 'The hands are said to BE maps.'),
         ('"He clasps the crag with crooked hands" (Alfred, Lord Tennyson, "The Eagle"). Which TWO devices are used?', 'Alliteration and personification', ['Simile and rhyme', 'Onomatopoeia and metaphor', 'Hyperbole and simile'], 'The repeated hard "c" sound is alliteration; the eagle\'s claws are called "hands" (personification).')],
  why=[('Explain why poets use metaphors rather than plain description.', 'Metaphors create surprising connections that make readers see something in a new way and pack a lot of meaning into few words.'),
       ('Explain why personification can make a setting feel alive.', 'Giving human actions or feelings to places or objects makes them seem to act and feel, creating mood and emotional connection.'),
       ('Explain why an extended metaphor can be more powerful than a single metaphor.', 'Developing one comparison across a poem builds layers of meaning and gives the poem unity, as with the hands-as-maps image that returns in "every border folded into her palms".')],
  contrast=[('a simile', 'a metaphor', 'A simile compares using "like" or "as" ("honk like geese"); a metaphor states that one thing is another ("a generator heart"), which is usually a stronger, more direct comparison.')],
  misc=[('Any sentence with "like" in it is a simile.', '"Like" must introduce a comparison; "I like pizza" uses "like" as a verb and is not a simile.'),
        ('Personification means describing a person.', 'Personification gives human qualities to something that is not human, such as the moon or a street.')],
  apply=[('Write a simile and a metaphor to describe a busy school corridor.', 'Any valid pair, e.g. simile: "Students poured through the corridor like a river in flood." Metaphor: "The corridor was a beehive at the bell." 1 mark each.', 2),
         ('Turn this plain sentence into personification: "The wind was strong."', 'For example: "The wind shoved the door and howled through the letterbox." Credit any human action or feeling given to the wind.', 1),
         ('Identify the device in each: (a) "The classroom was a zoo." (b) "The leaves danced in the wind." (c) "As quiet as a held breath."', '(a) metaphor; (b) personification; (c) simile.', 3)],
  evaluate=[('Figurative language makes poetry harder to understand, so it should be used sparingly.', ['too many images can confuse', 'plain language can be powerful'], ['images make abstract feelings concrete', 'readers remember vivid images'], 'Figurative language usually makes poems more vivid and memorable; the skill is choosing precise images rather than piling them up.')])
K.dev_mcq('ch03-st1', POEM | {'prose', 'story'})
pq('ch03-st1', ('C2', 'C3'), (1, 4), POEM, 'dev', DEV_Q, crit=CRIT_B)
para('ch03-st1', POEM, c='C4', d=(3, 5))
write('ch03-st1', ids=['grandmother_kitchen'])

H('ch03-st2',
  terms=[('rhyme', 'the repetition of the same sound at the end of words, often at the end of lines'),
         ('rhythm', 'the pattern of stressed and unstressed syllables in a line, which creates a beat'),
         ('alliteration', 'the repetition of the same consonant sound at the start of nearby words'),
         ('onomatopoeia', 'a word that imitates the sound it describes, such as "honk", "hum" or "splash"'),
         ('assonance', 'the repetition of vowel sounds in nearby words')],
  facts=[('"Tyger Tyger, burning bright" (William Blake). Which sound device is most obvious?', 'Alliteration', ['Onomatopoeia', 'Assonance only', 'Free verse'], 'The repeated "T" and "b" sounds are alliteration.'),
         ('Which word is an example of onomatopoeia?', 'Sizzle', ['Bright', 'Gentle', 'Tall'], '"Sizzle" imitates the sound it describes.'),
         ('A poem rhymes AABBA. Which form is this most likely to be?', 'A limerick', ['A haiku', 'A sonnet', 'Free verse'], 'Limericks have five lines rhyming AABBA.')],
  why=[('Explain why poets use rhythm and rhyme.', 'They make poems musical and memorable, help them be performed aloud, and can link important words or create humour.'),
       ('Explain why onomatopoeia is effective in a poem about a city.', 'Sound words such as "hum" and "honk" let the reader hear the city, making the description vivid and immersive.')],
  contrast=[('alliteration', 'assonance', 'Alliteration repeats consonant sounds at the start of words ("crooked crag"); assonance repeats vowel sounds inside words ("the light of the fire is a sight").')],
  misc=[('All poems must rhyme.', 'Many poems, including free verse and most haiku, do not rhyme; poets choose whether rhyme suits their purpose.'),
        ('Alliteration means words start with the same letter.', 'Alliteration is about the same sound: "cat" and "kite" alliterate, but "city" and "cat" do not.')],
  apply=[('Write a line of poetry about rain that includes onomatopoeia and alliteration.', 'Any line with both, e.g. "Pitter-patter, puddles plop on the path." 1 mark each device.', 2),
         ('Identify the rhyme scheme: "The river ran both wide and black, / The storm came down the hill; / The ferryman went out at dusk / And has not come back still."', 'ABCB (hill/still rhyme).', 1)],
  evaluate=[('Sound devices matter more when a poem is read aloud than when it is read silently.', ['rhythm and rhyme are heard', 'spoken word depends on sound'], ['readers "hear" sounds in their heads', 'sound devices also link ideas on the page'], 'Sound devices are strongest aloud, but they shape meaning and mood even when a poem is read silently.')])
pq('ch03-st2', ('C2', 'C3'), (1, 4), POEM, 'sound', ['Explain how the poet uses sound in this poem and the effect created.',
                                                   'Identify two sound devices in the poem and explain their effect on the reader.',
                                                   'How do rhythm and sound help to create the mood of the poem?'], crit=CRIT_B)
pq('ch03-st2', 'C2', (1, 3), POEM, 'tone', TONE_Q, crit=CRIT_B)
K.tone_mcq('ch03-st2', POEM)

H('ch03-st3',
  terms=[('haiku', 'a Japanese poetic form of three lines with 5, 7 and 5 syllables, usually capturing a moment in nature'),
         ('limerick', 'a humorous five-line poem with an AABBA rhyme scheme and a bouncing rhythm'),
         ('ballad', 'a poem that tells a story, usually in four-line stanzas with a regular rhythm and rhyme, often with repetition'),
         ('free verse', 'poetry with no regular rhyme scheme or metre'),
         ('stanza', 'a group of lines forming a unit in a poem, like a paragraph in prose')],
  facts=[('How many syllables does a traditional haiku have?', '17 (5-7-5)', ['14', '10', '20'], 'Three lines of 5, 7 and 5 syllables.'),
         ('Which form tells a story in quatrains, like a song?', 'A ballad', ['A haiku', 'A limerick', 'A cinquain'], 'Ballads are narrative poems originally sung.'),
         ('Which form has no regular rhyme or metre?', 'Free verse', ['A limerick', 'A sonnet', 'A ballad'], 'Free verse uses line breaks rather than fixed patterns.'),
         ('How many lines does a sonnet have?', '14', ['5', '3', '8'], 'Sonnets have 14 lines.')],
  why=[('Explain why the haiku form suits poems about single moments in nature.', 'Its short, strict form forces precision and captures a single image, like a snapshot.'),
       ('Explain why limericks are usually humorous.', 'Their bouncing rhythm, quick AABBA rhymes and punchline last line suit comic, absurd stories.'),
       ('Explain why a poet might choose free verse.', 'Without fixed rhyme and metre, the poet can shape lines to match natural speech and emphasise words through line breaks.')],
  contrast=[('a ballad', 'free verse', 'A ballad tells a story with regular stanzas, rhythm and rhyme; free verse has no fixed rhyme or metre and may not tell a story.')],
  misc=[('A haiku must always rhyme.', 'Traditional haiku do not rhyme; they focus on syllable count and a precise image.')],
  apply=[('Write a haiku (5-7-5) about your journey to school.', 'Three lines with 5, 7 and 5 syllables (allow minor variation); a precise image. 1 mark for form, 1 for imagery.', 2),
         ('Count the syllables in "First fat drops of rain" and say whether it fits the first line of a haiku.', '5 syllables (First-fat-drops-of-rain), so it fits.', 1),
         ('Write a limerick about a teacher or a pet with the AABBA rhyme scheme.', 'Five lines; AABBA rhyme; bouncing rhythm; humorous ending. 1 for rhyme scheme, 1 for rhythm, 1 for humour.', 3)],
  evaluate=[('Strict poetic forms limit a poet\'s creativity.', ['rules restrict word choice', 'free verse allows more freedom'], ['constraints push poets to be inventive', 'form can add meaning (e.g. a ballad\'s song-like repetition)'], 'Forms can both limit and inspire; many poets find that constraints sharpen their creativity.')])
pq('ch03-st3', ('C1', 'C2'), (1, 3), POEM, 'form', ['Identify the form of this poem and describe two of its features.',
                                                  'What poetic form is used here? Give two pieces of evidence.'], crit=CRIT_A)
pq('ch03-st3', ('C3', 'C4'), (2, 5), POEM, 'form', ['Explain how the form of this poem suits its subject and purpose.',
                                                  'How does the poet\'s choice of form contribute to the effect of the poem?'], crit=CRIT_B)
write('ch03-st3', ids=['rain_haiku'])

H('ch03-st4',
  terms=[('spoken word', 'poetry written to be performed aloud, often using rhythm, repetition and direct address'),
         ('choral reading', 'reading a poem aloud as a group, with lines shared between solo voices and the whole group'),
         ('pace', 'the speed at which a poem is read aloud'),
         ('emphasis (stress)', 'saying certain words more strongly to highlight their importance'),
         ('projection', 'making the voice carry clearly to the whole audience')],
  facts=[('Which performance choice best suits the line "and I am LOUD"?', 'Raising the volume on "LOUD"', ['Whispering the whole line', 'Reading it as fast as possible', 'Skipping it'], 'The capitals signal volume.'),
         ('In a choral reading, why might a group speak a repeated line together?', 'To give it extra power and emphasis', ['To save time', 'Because solos are not allowed', 'To hide mistakes'], 'Combined voices emphasise refrains.')],
  why=[('Explain why pauses are important when performing poetry.', 'Pauses give the audience time to absorb an image or idea, create suspense and emphasise the line that follows.'),
       ('Explain why spoken-word poets often use repetition.', 'Listeners cannot reread, so repetition helps them follow and remember key ideas and builds rhythm and intensity.')],
  contrast=[('reading a poem silently', 'performing it aloud', 'Reading silently lets the reader go at their own pace and reread; performance uses voice, pace, volume and gesture to interpret the poem for an audience in real time.')],
  misc=[('Performing a poem well just means reading it loudly.', 'Good performance varies volume, pace and tone to match the meaning, uses pauses, eye contact and gesture.')],
  apply=[('Plan a performance of the first four lines of a poem you know: mark one pause, one word to stress and one gesture, and explain each choice.', 'Any valid plan with reasons linked to meaning (e.g. pause after a key image to let it sink in).', 3)],
  evaluate=[('A poem is not complete until it is performed.', ['poetry began as an oral art', 'performance brings rhythm and emotion to life'], ['many poems are designed for the page (layout, visual effects)', 'silent reading allows close analysis'], 'Some poems (spoken word) depend on performance, while others are written for the page; performance adds interpretation but is not essential to all poems.')])
pq('ch03-st4', ('C3', 'C4'), (1, 5), POEM, 'perform', ['Explain how you would perform this poem aloud, referring to pace, volume, pauses and gesture.',
                                                      'Plan a choral reading of this poem for a group of four: which lines would be solo and which group, and why?',
                                                      'How should this poem be performed to bring out its meaning? Justify your choices with reference to the text.'], crit=CRIT_OPEN)
pq('ch03-st4', 'C2', (1, 3), POEM, 'sound', ['Explain how the sound of this poem would help a listener to understand it.'], crit=CRIT_B)


# =============================================================================================
# ch04 Persuasion and Advertising
# =============================================================================================
PERS = PERSUADE | {'poster'}
H('ch04-st1',
  terms=[('purpose', 'what a text is trying to do: for example to persuade, inform, entertain, advise or explain'),
         ('target audience', 'the specific group of people a text is aimed at'),
         ('demographic', 'a group defined by characteristics such as age, gender, income or interests'),
         ('call to action', 'an instruction telling the audience what to do next (e.g. "Sign up by Friday")')],
  facts=[('An advert appears in a teen sports magazine and uses hashtags. Who is the most likely target audience?', 'Teenagers who play sport', ['Retired business owners', 'Young children under five', 'Scientists'], 'Placement and features suggest the audience.'),
         ('What is the main purpose of a leaflet that says "Sign up at the eco-club table by Friday!"?', 'To persuade', ['To entertain', 'To narrate', 'To describe a setting'], 'It asks readers to act.'),
         ('Which feature best identifies a text\'s audience?', 'Where it appears and how it addresses readers', ['The number of paragraphs', 'The font size only', 'The date it was printed'], 'Context and language reveal audience.')],
  why=[('Explain why advertisers must identify their target audience before writing.', 'Language, images and placement must appeal to the specific interests, values and age of the audience to persuade them.'),
       ('Explain why a text can have more than one purpose.', 'A text may entertain to keep attention while persuading (e.g. a funny advert) or inform while persuading (a leaflet with facts).')],
  contrast=[('purpose', 'audience', 'Purpose is what the text aims to do (persuade, inform); audience is who it is for. Writers adapt their choices to achieve the purpose for that audience.')],
  misc=[('Everyone who reads a text is its target audience.', 'Many people may read a text, but the target audience is the specific group the writer designed it for.')],
  apply=[('Suggest the target audience and purpose of an advert for a new energy drink that shows skateboarders and uses slang.', 'Audience: teenagers or young adults interested in extreme sports. Purpose: to persuade them to buy the drink by associating it with excitement and youth culture.', 2),
         ('Rewrite the slogan "Buy our cereal" for (a) young children and (b) health-conscious parents.', '(a) e.g. "Crunchy, munchy fun in every bowl!" (b) e.g. "Wholegrain goodness to start their day right." 1 mark each for audience-appropriate language.', 2)],
  evaluate=[('Advertisers aimed at teenagers are more manipulative than those aimed at adults.', ['teenagers are influenced by peer pressure and social media', 'adverts use insecurities about image'], ['adult adverts also exploit fears (health, status)', 'many teenagers are media-literate and critical'], 'All advertising seeks to influence; teenagers may be especially targeted through social media, so media literacy matters for every audience.')])
pq('ch04-st1', ('C2', 'C3'), (1, 4), PERS, 'aud', AUD_Q, crit=CRIT_A)
pq('ch04-st1', ('C2', 'C3'), (1, 4), PERS, 'purp', PURP_Q, crit=CRIT_A)
K.kind_mcq('ch04-st1', PERS)

H('ch04-st2',
  terms=[('rhetorical question', 'a question asked for effect, not for an answer, to make the audience think'),
         ('emotive language', 'words chosen to make the audience feel strong emotions such as pity, guilt or anger'),
         ('statistic', 'a number or percentage used as evidence to make an argument seem factual and convincing'),
         ('repetition', 'using a word or phrase more than once for emphasis'),
         ('rule of three (tricolon)', 'a list of three words, phrases or ideas that makes a point memorable')],
  facts=[('"Do I need it? Will I wear it 30 times?" Which technique is used?', 'Rhetorical questions', ['Statistics', 'Onomatopoeia', 'Simile'], 'The questions make readers think rather than answer aloud.'),
         ('"Fill it. Carry it. Keep it." Which technique is used?', 'Rule of three', ['Statistic', 'Alliteration', 'Onomatopoeia'], 'Three short parallel commands.'),
         ('"About 900 plastic cups every week." Which technique is used?', 'Statistic', ['Emotive language', 'Rhetorical question', 'Personification'], 'A number used as evidence.'),
         ('Which phrase uses emotive language?', '"Amina\'s walk can end today."', ['"The well is 6 km away."', '"Our logo is blue."', '"Visit our website."'], 'It appeals to the viewer\'s feelings about a named child.')],
  why=[('Explain why statistics make persuasive texts more convincing.', 'Numbers seem objective and factual, so they make claims appear proven and reliable (logos).'),
       ('Explain why emotive language can be effective in a charity advert.', 'It makes the audience feel pity or guilt, motivating them to act, often more strongly than facts alone.'),
       ('Explain why the rule of three is common in slogans.', 'Three items create a satisfying rhythm and are easy to remember, so the message sticks.')],
  contrast=[('emotive language', 'statistics', 'Emotive language persuades through feelings (pathos); statistics persuade through apparent facts and logic (logos). Strong persuasion often combines both.')],
  misc=[('A rhetorical question expects the audience to answer.', 'A rhetorical question is asked for effect; the answer is implied, and it makes the audience think or agree.'),
        ('Statistics in adverts are always true and complete.', 'Statistics can be selected, rounded or presented without context; readers should check sources.')],
  apply=[('Write a persuasive sentence for a campaign to save a local park that uses emotive language and a statistic.', 'Any sentence using both, e.g. "Over 3,000 children play in Green Park every week – will we really let bulldozers destroy their only green space?" 1 mark each.', 2),
         ('Identify the technique in each: (a) "Small changes. Big difference." (b) "What can YOU do?" (c) "Every minute counts."', '(a) antithesis/contrast; (b) rhetorical question with direct address; (c) emotive language/urgency (accept hyperbole).', 3)],
  evaluate=[('Emotive language is more persuasive than facts.', ['feelings drive action', 'charity adverts rely on pathos'], ['facts build trust and credibility', 'too much emotion can feel manipulative'], 'The most persuasive texts combine emotion with evidence; emotion motivates, facts make the action seem justified.')],
  extended=[('Choose a persuasive text you have seen. Analyse how it uses three persuasive techniques and evaluate which is most effective.', 'Indicative content: three techniques with quotations; explanation of effect on the audience; reasoned judgement. Criteria A and B.', 8, 'long')])
K.dev_mcq('ch04-st2', PERS)
pq('ch04-st2', ('C2', 'C3'), (1, 4), PERS, 'dev', DEV_Q, crit=CRIT_B)
para('ch04-st2', PERS, c='C4', d=(3, 5))
pq('ch04-st2', 'C3', (2, 4), PERS, 'struct', STRUCT_Q, crit=CRIT_B)

H('ch04-st3',
  terms=[('slogan', 'a short, memorable phrase associated with a brand or campaign'),
         ('logo', 'a symbol or design that identifies a brand or organisation'),
         ('close-up', 'a camera shot that shows a face or object in detail, often to create emotion'),
         ('voice-over', 'a voice heard over the images in a video, not spoken by a character on screen'),
         ('connotation', 'the ideas and feelings associated with a word, colour or image beyond its literal meaning')],
  facts=[('In a video advert, why might the director use a close-up of a child\'s face?', 'To create an emotional connection with the viewer', ['To show the whole landscape', 'To hide the child\'s feelings', 'To make the advert shorter'], 'Close-ups reveal emotion.'),
         ('What does the colour green often connote in advertising?', 'Nature, health or environmental friendliness', ['Danger', 'Luxury', 'Mourning'], 'Green is linked to nature and eco-friendliness.'),
         ('What is the effect of music starting at the moment of a solution in a charity video?', 'It signals hope and change', ['It shows danger', 'It confuses the viewer', 'It replaces the call to action'], 'Sound changes mark emotional turning points.')],
  why=[('Explain why images are often more important than words in advertisements.', 'Images are processed instantly and create emotion and associations (connotations) that words alone cannot, so they grab attention quickly.'),
       ('Explain why video adverts use changes in sound and music.', 'Sound shapes the viewer\'s feelings – silence can suggest emptiness or hardship, while music can signal hope – guiding the emotional response.')],
  contrast=[('a print advertisement', 'a video advertisement', 'A print advert relies on a single image, layout and text that readers can study; a video advert uses moving images, camera shots, sound, music and time to tell a mini-story.')],
  misc=[('Colours in adverts are chosen randomly.', 'Advertisers choose colours deliberately for their connotations (green for nature, red for urgency or passion, gold for luxury).')],
  apply=[('Describe two camera shots you would use in a 20-second video advert for a reusable bottle and explain why.', 'Any two valid shots with reasons, e.g. a close-up of plastic bottles in the sea (shock), a wide shot of a clean beach with a person drinking from the bottle (solution).', 4)],
  evaluate=[('Video advertisements are more persuasive than print advertisements.', ['movement, music and story create strong emotion', 'they reach audiences online'], ['print adverts can be studied and remembered', 'viewers can skip video adverts'], 'Video often has more emotional power, but well-designed print adverts can be equally persuasive, depending on audience and placement.')])
pq('ch04-st3', ('C2', 'C3', 'C4'), (1, 5), VISUAL | {'ad'}, 'visual', VIS_Q, crit=CRIT_B)
pq('ch04-st3', ('C3', 'C4'), (2, 5), None, 'video', ['Analyse how camera shots and sound are used to persuade viewers in this video advertisement.',
                                                  'Explain how the storyboard creates an emotional journey for the viewer.'], ids=['charity_video'], crit=CRIT_B)
para('ch04-st3', {'ad', 'poster'}, c='C4', d=(3, 5))

H('ch04-st4',
  terms=[('persuasive letter', 'a formal letter written to convince a specific reader to take action or change their view'),
         ('leaflet', 'a short printed text, often folded, that informs or persuades using headings, bullet points and images'),
         ('formal register', 'language suited to official or serious situations, avoiding slang and contractions'),
         ('counterargument', 'an opposing point that a writer acknowledges and then answers (rebuts)')],
  facts=[('Which is the best opening for a formal persuasive letter to a head teacher?', '"Dear Ms Larsen, I am writing to propose a covered bike shelter."', ['"Hey Miss, guess what?"', '"Bikes are cool."', '"To whoever reads this."'], 'Formal salutation and clear purpose.'),
         ('Which sign-off is correct when you know the person\'s name?', 'Yours sincerely', ['Yours faithfully', 'Cheers', 'See ya'], 'Use "Yours sincerely" with a named recipient.'),
         ('Which feature is most typical of a leaflet?', 'Headings and bullet points', ['Stage directions', 'Chapters', 'Rhyming couplets'], 'Leaflets are designed to be scanned.')],
  why=[('Explain why a persuasive letter should include a counterargument.', 'Addressing an objection shows fairness and strengthens the case by answering doubts before the reader raises them.'),
       ('Explain why leaflets use bullet points and headings.', 'They make information easy to scan quickly, so busy readers can find the key points.')],
  contrast=[('a persuasive letter', 'a leaflet', 'A persuasive letter addresses one specific reader in continuous formal paragraphs; a leaflet addresses a wider audience using headings, bullet points and images for quick reading.')],
  misc=[('Persuasive writing should only include your own opinion.', 'Effective persuasion supports opinions with evidence, examples and statistics and addresses counterarguments.')],
  apply=[('Write the opening paragraph of a persuasive letter to your local council asking for a pedestrian crossing outside your school.', 'Formal salutation; clear statement of purpose; one piece of evidence or a reason; formal register. 1 mark each.', 4),
         ('List four features you would include in a leaflet persuading students to join a debate club.', 'Any four: a catchy heading; subheadings; bullet-point benefits; a quotation from a member; an image; meeting details; a call to action.', 4)],
  evaluate=[('A polite letter is more persuasive than an angry one.', ['politeness builds respect and trust', 'angry letters can be dismissed'], ['strong feelings can show urgency', 'some issues require forceful language'], 'A firm but polite tone is usually more persuasive, because it keeps the reader listening while still showing that the issue matters.')],
  extended=[('Write a persuasive letter (about 300 words) to your head teacher arguing for a change you would like to see at school.', 'Indicative content: letter conventions; clear purpose; at least two arguments with evidence; a counterargument and rebuttal; persuasive techniques; formal register; call to action. Criteria B, C, D.', 12, 'long'),
            ('Design and write a one-page leaflet (about 250 words) persuading students in your school to reduce food waste.', 'Indicative content: heading; subheadings; facts/statistics; bullet-point actions; persuasive devices; call to action; layout notes. Criteria B, C, D.', 12, 'long')])
write('ch04-st4', kinds=PERS)
write('ch04-st4', c='C3', d=(2, 4), ids=['plasticfree', 'library_letter', 'bike_letter'])
pq('ch04-st4', 'C3', (1, 4), {'letter', 'leaflet'}, 'kconv', ['Identify two conventions of a persuasive letter or leaflet in this text and explain why the writer uses them.',
                                                           'Which features of this text could you borrow for your own persuasive writing? Explain two.'], crit=CRIT_A)
pq('ch04-st4', 'C3', (2, 4), {'letter', 'leaflet'}, 'struct', ['Explain how {feature} helps to make this persuasive text effective.',
                                                           'How does the organisation of this text help it persuade? Refer to {feature}.'], crit=CRIT_B)


# =============================================================================================
# ch05 Drama: Reading and Performing Playscripts
# =============================================================================================
DRAMA = {'drama'}
H('ch05-st1',
  terms=[('playscript', 'the written text of a play, including character names, dialogue and stage directions'),
         ('stage directions', 'instructions in a playscript, usually in brackets or italics, about movement, setting, lighting, sound and how lines are spoken'),
         ('act', 'a major section of a play, made up of scenes'),
         ('scene', 'a smaller section of a play, usually in one place and time'),
         ('dialogue', 'the words spoken by characters to each other')],
  facts=[('In a playscript, where do the character\'s name and lines appear?', 'The name appears before each speech, followed by the lines', ['Inside speech marks in a paragraph', 'Only in the stage directions', 'At the end of the play'], 'Playscripts do not use speech marks.'),
         ('What is the purpose of stage directions?', 'To tell actors and directors how to stage the play', ['To give the audience the answers', 'To list the cast\'s phone numbers', 'To replace the dialogue'], 'They guide performance.'),
         ('Which is a stage direction?', '(The lights go out. Blackout.)', ['ANA: Did you hear that?', '"Stop!" she said.', 'Chapter One'], 'It is in brackets and describes lighting.')],
  why=[('Explain why playscripts do not use speech marks.', 'Every spoken line is already shown by the character\'s name and layout, so speech marks are unnecessary; the format makes lines easy for actors to find.'),
       ('Explain why stage directions are important even though the audience does not hear them.', 'They shape what the audience sees and feels – movement, lighting, sound and tone of voice – so they carry meaning in performance.')],
  contrast=[('a playscript', 'a novel', 'A playscript is written to be performed, using dialogue and stage directions; a novel is written to be read, using a narrator who can describe thoughts and settings directly.')],
  misc=[('Stage directions are optional details that can be ignored.', 'Stage directions often carry vital meaning (a knock, a blackout, a character\'s tone) that changes how scenes are understood.')],
  apply=[('Rewrite this prose as a playscript: "Leo whispered nervously, \'Is someone there?\' Then the door creaked open."', 'LEO: (nervously, whispering) Is someone there?\n(The door creaks open.) – 1 mark for name and colon format, 1 for stage directions in brackets.', 2),
         ('Add two stage directions to this line to show the character is furious: "MAYA: I can\'t believe you did that."', 'For example: MAYA: (slamming her bag down, shouting) I can\'t believe you did that! (She storms to the door.) Credit any directions showing anger.', 2)],
  evaluate=[('A playscript is incomplete until it is performed.', ['plays are written for performance', 'acting and staging add meaning'], ['readers can imagine the performance', 'scripts can be analysed as literature'], 'A playscript is designed for performance, so it is fully realised on stage, but careful readers can still interpret it richly on the page.')])
pq('ch05-st1', ('C2', 'C3'), (1, 4), DRAMA, 'kconv', KCONV_Q, crit=CRIT_A)
K.kind_mcq('ch05-st1', DRAMA | {'prose', 'story', 'script'})
write('ch05-st1', ids=['storm_drama'])
K.dev_mcq('ch05-st1', DRAMA)

H('ch05-st2',
  terms=[('characterisation (in drama)', 'how a playwright reveals character through dialogue, action, stage directions and other characters\' reactions'),
         ('subtext', 'the meaning or feeling beneath what a character actually says'),
         ('comic relief', 'a humorous moment that releases tension in a serious or frightening scene'),
         ('conflict', 'a struggle between characters or within a character, which drives a play forward')],
  facts=[('"LUCAS: (forcing a laugh) OK. That\'s... a very polite wind." What does the stage direction suggest?', 'Lucas is scared but pretending not to be', ['Lucas finds the wind genuinely funny', 'Lucas is angry with Ana', 'Lucas is bored'], '"Forcing" shows the laugh is not real.'),
         ('What is subtext?', 'The meaning beneath the words a character says', ['The title of a scene', 'A list of characters', 'The set design'], 'Characters often mean more than they say.')],
  why=[('Explain why playwrights rely on dialogue to reveal character.', 'There is usually no narrator, so what characters say – and how – is the main way the audience learns about them.'),
       ('Explain why contrasting characters are useful in a scene.', 'Contrast (anxious Priya, relaxed Jake) highlights each character\'s traits and creates conflict or humour.')],
  contrast=[('dialogue', 'stage directions', 'Dialogue is what characters say aloud; stage directions describe actions, tone and staging that show character without words.')],
  misc=[('In drama, a character\'s personality is only shown through what they say.', 'Actions, movement, tone of voice, pauses and others\' reactions – often in stage directions – reveal character just as much.')],
  apply=[('Write a short dialogue (four lines) between two characters that shows one is jealous of the other without using the word "jealous".', 'Any dialogue in playscript format with subtext showing jealousy (e.g. sarcastic compliments, a stage direction such as "(looking away)"). Format 1, subtext 2.', 3),
         ('Explain what the stage direction "(standing, serious for once)" reveals about Jake.', 'That he is usually jokey, but he genuinely cares about Priya and becomes serious to support her.', 2)],
  evaluate=[('Stage directions reveal more about a character than dialogue.', ['actions show hidden feelings ("forcing a laugh")', 'directions can contradict words'], ['dialogue gives voice, humour and relationships', 'actors interpret both together'], 'Both are essential; stage directions often reveal subtext that dialogue hides, so the richest understanding comes from reading them together.')],
  extended=[('Choose a character from a play you have studied. Analyse how the playwright uses dialogue and stage directions to present them.', 'Indicative content: specific lines and directions; inferences about character; effect on the audience; comment on subtext. Criteria A and B.', 8, 'long')])
pq('ch05-st2', ('C2', 'C3', 'C4'), (1, 5), DRAMA, 'char', CHAR_Q, crit=CRIT_A)
pq('ch05-st2', ('C2', 'C3'), (1, 4), DRAMA, 'dev', DEV_Q, crit=CRIT_B)
para('ch05-st2', DRAMA, c='C4', d=(3, 5))
pq('ch05-st2', 'C2', (1, 3), DRAMA, 'tone', TONE_Q, crit=CRIT_B)

H('ch05-st3',
  terms=[('set', 'the scenery and furniture on stage that show where a scene takes place'),
         ('blocking', 'the planned movements and positions of actors on stage'),
         ('lighting', 'the use of stage lights to show time, mood and focus'),
         ('costume', 'the clothes actors wear to show character, period and status'),
         ('upstage / downstage', 'upstage is the back of the stage, furthest from the audience; downstage is the front')],
  facts=[('Which lighting choice would best create suspense?', 'Flickering, dim lights', ['Bright, steady white light', 'Coloured disco lights', 'No change at all'], 'Unstable light creates unease.'),
         ('What does "blackout" mean in a playscript?', 'All stage lights are switched off at once', ['Actors wear black', 'The curtain stays open', 'The audience leaves'], 'A blackout often ends a scene suddenly.')],
  why=[('Explain why a director might place a character upstage behind others.', 'It can make the character seem distant, mysterious or less powerful, or allow a surprise entrance (like Uncle Hassan behind the lanterns).'),
       ('Explain how costume can reveal character.', 'Clothes signal age, status, personality and culture – a tourist\'s sunhat and backpack immediately show they are a visitor.')],
  contrast=[('lighting', 'sound', 'Lighting controls what the audience sees and the mood visually (darkness, colour); sound controls what they hear (rain, knocks, music) to build atmosphere and signal events.')],
  misc=[('Staging choices are decoration and do not change the meaning of a scene.', 'Set, lighting, costume and blocking shape mood, focus and how the audience interprets characters and events.')],
  apply=[('Suggest a lighting and a sound effect for a scene in which two friends say goodbye at a train station at night, and explain each.', 'Any valid choices with reasons, e.g. a single cold spotlight to isolate them (loneliness); a distant train whistle to signal departure.', 4),
         ('Describe how you would block (position and move) two actors in a scene where one character is trying to apologise and the other refuses to listen.', 'For example: the apologiser moves towards the other, who turns away and crosses to the other side of the stage; distance shows refusal. Credit purposeful positions linked to meaning.', 3)],
  evaluate=[('A simple set is often more effective than a detailed one.', ['the audience\'s imagination fills gaps', 'focus stays on actors'], ['detailed sets create a believable world', 'some plays need realism'], 'A simple set can be very effective if lighting and acting carry meaning, but the best choice depends on the play\'s style.')])
pq('ch05-st3', ('C3', 'C4'), (1, 5), DRAMA, 'staging', ['Suggest staging choices (set, lighting, sound, costume or blocking) for this extract and explain how each would create meaning.',
                                                     'As a director, how would you stage this extract? Justify two choices with reference to the text.',
                                                     'Explain how lighting and blocking could help the audience understand the characters in this scene.'], crit=CRIT_OPEN)
pq('ch05-st3', 'C2', (1, 3), DRAMA, 'struct', STRUCT_Q, crit=CRIT_B)


# =============================================================================================
# ch06 Short Stories: Suspense and Mystery
# =============================================================================================
SUSP = {'story'}
H('ch06-st1',
  terms=[('suspense', 'a feeling of anxious uncertainty about what will happen next'),
         ('pacing', 'the speed at which a story moves, controlled by sentence length, detail and paragraphing'),
         ('foreshadowing', 'hints or clues about what will happen later in a story'),
         ('cliffhanger', 'an ending (of a chapter or story) that leaves the reader in suspense'),
         ('red herring', 'a false clue that misleads the reader')],
  facts=[('Which technique most directly slows the pace at a tense moment?', 'Short sentences describing small actions', ['A long summary of several days', 'A list of characters\' names', 'A flashback to a holiday'], 'Short sentences stretch time and build tension.'),
         ('"Nothing up there but dust," Gran always said. This line is an example of:', 'foreshadowing', ['onomatopoeia', 'a cliffhanger', 'a simile'], 'It hints that the attic hides a secret.'),
         ('What is a cliffhanger?', 'An ending that leaves a question unanswered', ['A happy ending', 'A description of a cliff', 'A list of clues'], 'Cliffhangers keep readers wanting more.')],
  why=[('Explain why writers use short sentences at moments of tension.', 'Short sentences slow the reader down, focus on each detail and mimic a character\'s quickened heartbeat, increasing suspense.'),
       ('Explain why foreshadowing makes a twist ending satisfying.', 'Hints placed earlier mean the twist surprises the reader but also makes sense when they look back.'),
       ('Explain why withholding information builds suspense.', 'When readers do not know what is behind the door or who is following, they keep reading to find out.')],
  contrast=[('suspense', 'surprise', 'Suspense is a lasting feeling of anxious expectation built over time; surprise is a sudden, unexpected moment. A twist ending gives surprise after a build-up of suspense.')],
  misc=[('Suspense means lots of action and violence.', 'Suspense comes from uncertainty and anticipation; quiet details such as a warm door handle can be more suspenseful than action.')],
  apply=[('Rewrite this sentence to build more suspense: "Ravi opened the door and saw a figure."', 'For example: "Ravi\'s fingers closed round the handle. Cold. He pushed. The door groaned. In the darkness, something moved." Credit short sentences, sensory detail and delay.', 3),
         ('Write a one-line cliffhanger to end a chapter in which a girl finds a message on her phone from an unknown number.', 'For example: "The message said: I can see you." Credit lines that leave a strong question.', 2)],
  evaluate=[('A suspense story must end with a twist.', ['twists surprise and satisfy readers', 'they make readers rethink the story'], ['a predictable twist can disappoint', 'open endings or realistic resolutions can also be powerful'], 'Twists can be effective if well foreshadowed, but suspense can also end with an open or quiet resolution; the ending should fit the story.')],
  extended=[('Analyse how the writer of a suspense story you have read uses pacing and foreshadowing to keep the reader in suspense.', 'Indicative content: identifies pacing techniques (sentence length, delay) and foreshadowing with quotations; explains effects; organised analysis. Criteria A and B.', 8, 'long')])
pq('ch06-st1', ('C2', 'C3', 'C4'), (1, 5), SUSP, 'suspense', ['How does the writer build suspense in this extract?',
                                                           'Explain two techniques the writer uses to keep the reader in suspense.',
                                                           'Analyse how pacing is used to create tension in the extract.'], crit=CRIT_B)
pq('ch06-st1', ('C2', 'C3'), (1, 4), SUSP, 'dev', DEV_Q, crit=CRIT_B)
para('ch06-st1', SUSP, c='C4', d=(3, 5))
pq('ch06-st1', 'C3', (2, 4), SUSP, 'struct', STRUCT_Q, crit=CRIT_B)
K.dev_mcq('ch06-st1', SUSP)

H('ch06-st2',
  terms=[('setting', 'the time and place in which a story happens'),
         ('atmosphere (mood)', 'the feeling created for the reader by a description or scene'),
         ('sensory description', 'description that appeals to the five senses: sight, sound, smell, touch and taste'),
         ('pathetic fallacy', 'when the weather or setting reflects the characters\' feelings or the mood of the story')],
  facts=[('"The lights dimmed to emergency orange." Which sense does this appeal to?', 'Sight', ['Taste', 'Smell', 'Touch'], 'It describes colour and light.'),
         ('"The rain hammered on the roof as Ana\'s heart raced." This is an example of:', 'pathetic fallacy', ['onomatopoeia only', 'a flashback', 'a rhetorical question'], 'The stormy weather reflects her fear.'),
         ('Which detail best creates an eerie atmosphere?', 'A door handle that is warm to the touch in a cold, empty house', ['A sunny beach with ice cream', 'A busy classroom at lunchtime', 'A birthday cake with candles'], 'Unexpected sensory details create unease.')],
  why=[('Explain why writers use more than one sense in descriptions of setting.', 'Appealing to several senses immerses the reader in the scene and makes it feel real.'),
       ('Explain why confined settings (lifts, attics) are common in suspense stories.', 'They trap characters with no escape, increasing fear and tension.')],
  contrast=[('setting', 'atmosphere', 'Setting is where and when a story takes place; atmosphere is the feeling the description of that setting creates for the reader.')],
  misc=[('Setting is just background information.', 'Setting creates atmosphere, reflects characters\' feelings and can drive the plot (a stuck lift, a storm).')],
  apply=[('Write two sentences describing an abandoned railway station at night, using at least two senses.', 'Any vivid description using two senses (e.g. sound of dripping water, smell of rust). 1 mark each sense, 1 for atmosphere.', 3),
         ('Change the mood of this sentence from cheerful to threatening: "The sun shone on the playground and children laughed."', 'For example: "Clouds smothered the sun; on the empty playground, a swing creaked by itself." Credit vocabulary and imagery that create threat.', 2)],
  evaluate=[('Description of setting slows a story down too much.', ['readers may skip long description', 'action keeps pace'], ['setting creates mood that makes events frightening', 'well-chosen details can be brief'], 'Overlong description can slow a story, but precise sensory details build the atmosphere that suspense depends on.')])
pq('ch06-st2', ('C2', 'C3', 'C4'), (1, 5), SUSP | {'prose'}, 'mood', MOOD_Q, crit=CRIT_B)
pq('ch06-st2', ('C2', 'C3'), (1, 4), SUSP, 'setting', ['Explain how the setting contributes to the suspense in this extract.',
                                                     'Why is this setting effective for a suspense story?'], crit=CRIT_B)
K.prompts('ch06-st2', 'open', c=('C3', 'C4'), d=(2, 5))

H('ch06-st3',
  terms=[('twist', 'an unexpected development, often at the end of a story, that changes the reader\'s understanding'),
         ('narrative hook', 'an opening that grabs the reader\'s attention'),
         ('climax', 'the most intense point of a story, usually just before the resolution'),
         ('resolution', 'the part of the story after the climax where the outcome is revealed')],
  facts=[('Which opening sentence is the strongest hook for a suspense story?', '"The phone rang at 3 a.m. – from my own number."', ['"I woke up and had breakfast."', '"This is a story about my week."', '"It was a normal day."'], 'An intriguing mystery hooks readers.'),
         ('What makes a twist ending satisfying rather than confusing?', 'Clues earlier in the story that make sense in hindsight', ['Introducing a completely new character at the end', 'Explaining nothing', 'Ending in the middle of a sentence'], 'Fair clues make twists work.')],
  why=[('Explain why writers plan the twist before writing the opening.', 'Knowing the twist lets them plant clues and red herrings from the start, so the ending is surprising but believable.'),
       ('Explain why "it was all a dream" is often a weak twist.', 'It cancels the story\'s events and stakes, making the reader feel cheated rather than surprised.')],
  contrast=[('the climax', 'the resolution', 'The climax is the moment of greatest tension (spinning round to face the follower); the resolution reveals the outcome (it is a boy with her purse).')],
  misc=[('A good twist should have no clues so that nobody can guess it.', 'Fair clues are needed so the twist makes sense; the skill is hiding them in plain sight.')],
  apply=[('Plan a suspense story with a twist: write one sentence each for the hook, two clues, the climax and the twist.', 'Any coherent plan with a hook, two clues that point to the twist, a climax and a twist that recontextualises the story.', 5),
         ('Identify the clues that prepare for the twist in the lift story (the old woman with no reflection).', 'She says it happens every Tuesday when it is Wednesday; her umbrella is dripping although it has not rained all week.', 2)],
  evaluate=[('A twist ending is more important than a strong opening.', ['the ending is what readers remember', 'a twist rewards attention'], ['readers stop if the opening does not hook them', 'the build-up creates the suspense the twist depends on'], 'Both matter: a strong opening keeps readers reading, and a fair twist rewards them; one without the other weakens the story.')],
  extended=[('Write a suspense story (400–500 words) with a twist ending. Build tension through pacing and setting.', 'Indicative content: hook; sensory setting; pacing (short sentences at climax); foreshadowing; a fair twist; controlled paragraphing. Criteria B, C, D.', 12, 'long')])
pq('ch06-st3', ('C3', 'C4'), (2, 5), SUSP, 'twist', ['Explain how the writer prepares the reader for the twist in this extract.',
                                                   'How does the twist change the reader\'s understanding of the story?'], crit=CRIT_B)
write('ch06-st3', kinds=SUSP)
K.prompts('ch06-st3', 'one', c='C4', d=(3, 5))
K.prompts('ch06-st3', 'plan', c='C3', d=(2, 4))


# =============================================================================================
# ch07 Life Writing: Autobiography and Biography
# =============================================================================================
LW = {'memoir', 'autobio', 'bio', 'diary'}
H('ch07-st1',
  terms=[('autobiography', 'an account of a person\'s life written by that person, usually covering a long period'),
         ('biography', 'an account of a person\'s life written by someone else, in the third person'),
         ('memoir', 'a first-person account focusing on particular memories or a period of the writer\'s life, with reflection'),
         ('anecdote', 'a short, interesting story about a real incident'),
         ('reflection', 'the writer\'s thoughts about what an experience meant or taught them')],
  facts=[('A text about Wangari Maathai written in the third person by a journalist is:', 'a biography', ['an autobiography', 'a memoir', 'a diary'], 'Biography is written by someone else.'),
         ('Which feature is most typical of a memoir?', 'Reflection on what memories mean', ['Stage directions', 'A rhyme scheme', 'A headline and lead'], 'Memoirs combine memory and reflection.'),
         ('Which pronoun is typical of autobiography?', 'I', ['He', 'They', 'You'], 'Autobiography is first person.')],
  why=[('Explain why biographers use dates and quotations.', 'Dates organise the life clearly and quotations provide evidence and the subject\'s own voice, making the account reliable.'),
       ('Explain why memoirs include reflection, not just events.', 'Reflection shows what experiences meant and how they changed the writer, giving the memoir depth and connecting with readers.')],
  contrast=[('autobiography', 'memoir', 'An autobiography usually covers a whole life in chronological order; a memoir focuses on selected memories or one period and emphasises reflection and feeling.'),
            ('biography', 'autobiography', 'A biography is written by someone else in the third person and relies on research; an autobiography is written by the subject in the first person from personal memory.')],
  misc=[('Life writing is always completely objective.', 'Life writers select, shape and interpret events; memory is imperfect and biographers choose which facts to include.')],
  apply=[('Identify whether each text is autobiography, biography or memoir: (a) "Jesse Owens was born in Alabama in 1913..." (b) "I was nine when we arrived in Oslo..." with reflection on belonging.', '(a) biography; (b) memoir.', 2)],
  evaluate=[('Autobiography is more truthful than biography.', ['the writer lived the events', 'it gives direct access to feelings'], ['writers may hide or flatter themselves', 'biographers can check sources and be more objective'], 'Each has strengths and limits: autobiography offers inner truth but may be biased; biography offers research and distance but cannot fully know the subject\'s feelings.')])
K.kind_mcq('ch07-st1', LW)
pq('ch07-st1', ('C2', 'C3'), (1, 4), LW, 'kconv', KCONV_Q, crit=CRIT_A)
pq('ch07-st1', ('C2', 'C3'), (1, 4), None, 'features', ['Identify the type of life writing and explain two features that show this.',
                                                      'What features of biography or autobiography are used in this extract?'], ids=['wangari', 'owens', 'cricket_autobio'], crit=CRIT_A)
pq('ch07-st1', 'C3', (2, 4), LW, 'dev', DEV_Q, crit=CRIT_B)
para('ch07-st1', LW, c='C4', d=(3, 5))

H('ch07-st2',
  terms=[('historical context', 'the events, values and conditions of the time in which a life was lived or a text was written'),
         ('personal context', 'the individual circumstances – family, place, experiences – that shaped a person'),
         ('segregation', 'the enforced separation of people by race, as in parts of the United States until the 1960s'),
         ('perspective', 'the point of view from which events are seen and told')],
  facts=[('Why is the context of the 1936 Berlin Olympics important to Jesse Owens\'s story?', 'The Nazi government wanted the Games to show racial superiority, which his victories challenged', ['It was the first Olympics ever held', 'It took place in Alabama', 'Owens was the Nazi team\'s coach'], 'Context gives his medals extra meaning.'),
         ('Which detail gives personal context in the Wangari Maathai biography?', 'She fetched water from a stream lined with fig trees as a child', ['She won the Nobel Peace Prize in 2004', 'Kenya is in East Africa', 'The Green Belt Movement was founded in 1977'], 'The childhood memory is personal context.')],
  why=[('Explain why understanding historical context changes how we read a life story.', 'Context shows the obstacles a person faced and why their actions mattered; Owens\'s medals mean more when we know about Nazi propaganda and segregation.'),
       ('Explain why a memoir written by an adult about childhood shows two perspectives.', 'It combines the child\'s experience at the time with the adult\'s later reflection and understanding.')],
  contrast=[('historical context', 'personal context', 'Historical context is the wider situation of the time (wars, laws, social attitudes); personal context is the individual\'s own circumstances (family, childhood, experiences).')],
  misc=[('Context is just extra information and does not affect meaning.', 'Context shapes meaning: the same achievement can be ordinary or extraordinary depending on the barriers of the time.')],
  apply=[('Write two sentences explaining how the historical context of Jesse Owens\'s life makes his achievement more significant.', 'For example: "The Nazis wanted the 1936 Games to prove their racist ideas, so Owens\'s four gold medals directly challenged them. Yet he returned to segregation in the USA, showing that his success did not end racism at home."', 3)],
  evaluate=[('You cannot understand a life story without knowing its historical context.', ['context explains obstacles and choices', 'readers may misjudge actions without it'], ['personal feelings and universal experiences can be understood without context', 'texts often provide the context needed'], 'Context deepens understanding significantly, though some aspects (emotions, relationships) can be appreciated without detailed historical knowledge.')])
pq('ch07-st2', ('C2', 'C3', 'C4'), (1, 5), None, 'context', ['Explain how the context of this text helps the reader understand its significance.',
                                                           'How does the writer use historical or personal context in this extract?',
                                                           'Identify one piece of context in the text and explain why it matters.'], ids=['wangari', 'owens', 'cricket_autobio', 'nobel_mum'], crit=CRIT_A)
qa('ch07-st2', 'C3', (1, 4), None, ids=['wangari', 'owens'])
para('ch07-st2', None, ids=['wangari', 'owens', 'nobel_mum'], c='C4', d=(3, 5))
pq('ch07-st2', 'C3', (1, 4), None, 'dev', ['Explain how the {device} "{quote}" helps the reader understand the subject\'s life.',
                                           'What does "{quote}" suggest about the person\'s experience? Explain the writer\'s choice.'], ids=['wangari', 'owens', 'cricket_autobio', 'nobel_mum'], crit=CRIT_B)
pq('ch07-st2', 'C3', (2, 4), None, 'summary', ['Summarise the key events of this life story in no more than 50 words.',
                                              'In three bullet points, summarise what this text tells us about the person\'s life.'], ids=['wangari', 'owens', 'cricket_autobio', 'nobel_mum'], crit=CRIT_A)

H('ch07-st3',
  terms=[('autobiographical anecdote', 'a short, true story from the writer\'s own life, told to entertain or make a point'),
         ('retrospective narrator', 'a narrator looking back on past events from a later point in time'),
         ('show, don\'t tell', 'revealing feelings through details, actions and senses rather than stating them')],
  facts=[('Which sentence best "shows" nervousness in an anecdote?', '"My hands shook so much that the paper rattled."', ['"I was nervous."', '"It was a day."', '"Nerves are common."'], 'A physical detail shows the feeling.'),
         ('What usually ends an effective autobiographical anecdote?', 'A reflection on what the experience meant', ['A list of dates', 'A rhetorical question to the teacher', 'A new unrelated story'], 'Reflection gives the anecdote a point.')],
  why=[('Explain why a small, specific memory often makes a better anecdote than a whole holiday.', 'A focused moment allows vivid detail and a clear turning point, whereas a long summary becomes a list of events.'),
       ('Explain why dialogue is useful in autobiographical writing.', 'Remembered words (like the uncle\'s lesson) bring people to life and can capture the key message of the experience.')],
  misc=[('An anecdote must be about something dramatic to be interesting.', 'Small, everyday moments (breaking a window, a sound) can be powerful if told with vivid detail and reflection.')],
  apply=[('Rewrite this "telling" sentence to "show" the feeling: "I was scared on my first day."', 'E.g. "My fingers wouldn\'t stop twisting the strap of my bag, and the corridor seemed a mile long." Credit concrete physical or sensory detail.', 2),
         ('Turn this list of events into the opening of an anecdote with a hook: "I went to the beach. I lost my phone. I found it later."', 'E.g. "The sea had my phone, and it wasn\'t giving it back." Credit a hook that raises a question and a focused moment.', 2),
         ('Write a line of remembered dialogue that captures an important lesson from an adult in your life, and one sentence explaining why it stayed with you.', 'Any plausible quotation plus reflection, e.g. "\'Nobody is born knowing,\' my grandfather said – I still hear it before every exam."', 2),
         ('Write the first two sentences of an anecdote about a time you got lost, using a specific sensory detail.', 'Any first-person opening with a specific setting and sensory detail. 1 mark for focus, 1 for sensory detail.', 2),
         ('Write a one-sentence reflection to end an anecdote about losing a race.', 'For example: "I didn\'t win that day, but I learned that finishing matters more than first place." Credit a sentence that shows learning.', 1)],
  evaluate=[('Autobiographical writing should always tell the exact truth.', ['readers expect honesty', 'invented details mislead'], ['memory is imperfect, so some reconstruction is inevitable', 'shaping events can reveal emotional truth'], 'Life writing should be honest about real events, but writers inevitably shape memories; the key is emotional and factual honesty rather than perfect recall.')],
  extended=[('Write an autobiographical anecdote (about 400 words) about a moment that changed how you saw yourself or someone else.', 'Indicative content: first person; a focused incident; sensory detail; dialogue; a turning point; reflection. Criteria B, C, D.', 12, 'long')])
write('ch07-st3', kinds=LW)
write('ch07-st3', c='C3', d=(2, 4), ids=['hiking_diary', 'nobel_mum', 'cricket_autobio'])
qa('ch07-st3', 'C3', (1, 3), None, ids=['hiking_diary'])
pq('ch07-st3', 'C3', (1, 4), LW, 'dev', ['The writer uses {device}: "{quote}". Explain its effect and write your own sentence using the same technique for an anecdote about your first day at school.', 'How could you use the technique in "{quote}" in your own autobiographical writing? Explain its effect and give an example.'], crit=CRIT_B)
pq('ch07-st3', 'C2', (1, 3), LW, 'struct', STRUCT_Q, crit=CRIT_B)


# =============================================================================================
# ch08 News and Media Literacy
# =============================================================================================
NEWS = {'news'}
H('ch08-st1',
  terms=[('headline', 'the title of a news report, designed to summarise the story and catch attention'),
         ('lead (lede)', 'the first paragraph of a news report, which answers the key questions who, what, where, when (and often why)'),
         ('inverted pyramid', 'the structure of a news report, with the most important information first and less important details later'),
         ('standfirst', 'a short summary under the headline that introduces the story'),
         ('attribution', 'stating who said or provided information, e.g. "said volunteer Amani Mwangi"')],
  facts=[('Which questions should the lead paragraph of a news report answer?', 'Who, what, where and when', ['How long the report is', 'What the reader should buy', 'Who the editor is'], 'The lead gives the key facts.'),
         ('Why do news reports use the inverted pyramid?', 'So readers get the most important facts first', ['So the ending is a surprise', 'To make reports longer', 'To hide the main story'], 'Readers who stop early still know the main points.'),
         ('Which is an example of attribution?', '"said rescue coordinator Imran Shah"', ['"A free app"', '"this week"', '"RECORD TURTLE HATCHING"'], 'It names the source.')],
  why=[('Explain why news reports include quotations from witnesses and experts.', 'They provide evidence, human interest and authority, and let the journalist report opinions without stating them personally.'),
       ('Explain why news reports are usually written in the third person.', 'It creates a sense of objectivity and distance, presenting events as facts rather than personal views.')],
  contrast=[('a news report', 'a feature article', 'A news report gives the key facts of a recent event quickly using the inverted pyramid; a feature article explores a topic in more depth with description, human interest and a more personal style.')],
  misc=[('The most exciting part of a news story should be saved for the end.', 'News uses the inverted pyramid: the most important facts come first; suspense is for stories, not reports.')],
  apply=[('Write a lead paragraph (one or two sentences) for a news report about your school winning a robotics competition.', 'Answers who, what, where, when (and why/how) concisely in the third person, e.g. "Students from Riverside International School won the national junior robotics championship in Kuala Lumpur on Saturday with a robot that sorts recycling." 1 mark per key element (max 4).', 4),
         ('Put these parts of a news report in inverted-pyramid order: (a) background on previous competitions; (b) the result and who won; (c) a quotation from the team captain.', '(b) result – (c) quotation – (a) background.', 2)],
  evaluate=[('The inverted pyramid is outdated in the age of online news.', ['online readers scroll and skim', 'some sites prefer storytelling openings'], ['skimming readers need key facts first', 'it suits headlines and notifications'], 'The inverted pyramid remains useful because online readers often read only the opening, though features and longer pieces use other structures.')],
  extended=[('Write a news report (about 250 words) on a real or imagined event at your school, using the conventions of news writing.', 'Indicative content: headline; lead with who/what/where/when; inverted pyramid; attributed quotations; third person; neutral tone. Criteria B, C, D.', 10, 'long')])
pq('ch08-st1', ('C2', 'C3'), (1, 4), NEWS, 'struct', STRUCT_Q, crit=CRIT_B)
qa('ch08-st1', 'C3', (1, 3), NEWS)
pq('ch08-st1', ('C2', 'C3'), (1, 4), NEWS, 'kconv', KCONV_Q, crit=CRIT_A)
pq('ch08-st1', 'C3', (2, 4), NEWS, 'summary', SUM_Q, crit=CRIT_A)

H('ch08-st2',
  terms=[('fact', 'a statement that can be checked and proved true or false'),
         ('opinion', 'a statement of belief, feeling or judgement that cannot be proved'),
         ('bias', 'an unfair preference for one side, shown through what is included, left out or how it is described'),
         ('omission', 'leaving out information or viewpoints, which can make a report one-sided'),
         ('loaded language', 'words with strong positive or negative connotations that influence the reader')],
  facts=[('Which statement is a fact?', '"The council spent €180,000 on the park."', ['"The park is a waste of money."', '"It is an investment in our young people."', '"Skateboarders are noisy."'], 'It can be checked.'),
         ('Report B quotes only a resident who complains and leaves out young people. This is an example of:', 'bias through omission', ['balanced reporting', 'onomatopoeia', 'a lead paragraph'], 'Leaving out one side creates bias.'),
         ('Which word in a headline is most loaded?', '"Thugs"', ['"Park"', '"Saturday"', '"Opens"'], '"Thugs" carries a strong negative judgement.')],
  why=[('Explain why two reports of the same event can give very different impressions.', 'Journalists choose which facts, quotations and words to include and in what order, so selection and framing create different impressions even with the same facts.'),
       ('Explain why readers should look for who is quoted in a report.', 'If only one side is quoted, the report may be biased; balanced reports include different viewpoints.'),
       ('Explain why an opinion inside quotation marks can still create bias.', 'Although attributed to someone else, the journalist chose to include it, so it still shapes the reader\'s view.')],
  contrast=[('fact', 'opinion', 'A fact can be verified (a cost, a date); an opinion is a judgement that can be argued with ("a waste of money"). Opinions can be supported by facts but are not facts themselves.'),
            ('bias', 'opinion', 'An opinion is a single judgement; bias is a pattern of unfair selection or presentation that favours one side across a text.')],
  misc=[('If a report contains only facts, it cannot be biased.', 'Bias can come from which facts are chosen, how they are ordered and what is left out, even when every statement is true.'),
        ('Numbers in news reports are always neutral.', 'Numbers can be framed to create impressions, e.g. putting "€180,000" in a headline beside "fear" suggests waste.')],
  apply=[('Label each statement F (fact) or O (opinion): (a) "Lina Osei collected 2,000 signatures." (b) "The skatepark is the best thing to happen to our town." (c) "The park includes a bowl and ramps."', '(a) F; (b) O; (c) F.', 3),
         ('Rewrite this biased sentence neutrally: "Selfish teenagers have ruined the peace of our once-quiet park."', 'For example: "Some residents say noise has increased since the skatepark opened." Credit removal of loaded words and attribution.', 2)],
  evaluate=[('It is impossible for any news report to be completely unbiased.', ['journalists must select information', 'word choice always has connotations'], ['professional standards aim for balance', 'quoting several sides reduces bias'], 'Complete neutrality is very difficult because selection is unavoidable, but reports can be more or less balanced; readers should compare sources.')],
  extended=[('Compare how two reports of the same event present it differently. Analyse headline, quotations and word choice.', 'Indicative content: identifies differences in headline language, choice of quotations, omission and framing of facts; explains effects on reader; judges which is more balanced. Criteria A and B.', 8, 'long')])
pq('ch08-st2', ('C2', 'C3'), (1, 4), NEWS, 'facts_op', ['Identify one fact and one opinion in the text.',
                                                     'Find one statement that can be proved and one that cannot. Explain the difference.',
                                                     'Separate fact from opinion in this report, giving one example of each.'], crit=CRIT_A)
pq('ch08-st2', ('C3', 'C4'), (2, 5), None, 'bias', ['Is this report biased? Explain your answer with reference to the headline, quotations and word choice.',
                                                  'Analyse how the report favours one side of the story.'], ids=['skate_a', 'skate_b'], crit=CRIT_B)
K.compare_short('ch08-st2', c='C3', d=(2, 4), only=['skate_a'])
K.compare('ch08-st2', c='C4', d=(4, 5), only=['skate_a'])

H('ch08-st3',
  terms=[('pun', 'a play on words that uses a word with two meanings or words that sound alike, often for humour'),
         ('alliteration (in headlines)', 'repeating initial consonant sounds to make headlines memorable'),
         ('connotation', 'the feelings or associations a word carries beyond its dictionary meaning'),
         ('tabloid', 'a newspaper style using short, dramatic stories and attention-grabbing headlines'),
         ('broadsheet', 'a newspaper style associated with longer, more serious reporting and more neutral headlines')],
  facts=[('"PURR-FECT ENDING" is an example of:', 'a pun', ['a statistic', 'an omission', 'a lead'], 'It plays on "perfect" and "purr".'),
         ('Which headline is most neutral?', '"Heatwave: 40°C Recorded in Seville"', ['"Thugs Trash Park in Night of Shame"', '"Mayor\'s Mega Mall Madness"', '"Hero Teen Saves Town"'], 'It reports a fact without judgement.'),
         ('Why do headlines often omit small words like "the" and "a"?', 'To save space and create impact', ['Because they are grammatically wrong', 'To confuse readers', 'Because editors dislike articles'], 'Headlinese is compressed.')],
  why=[('Explain why tabloid headlines often use puns.', 'Puns are witty and eye-catching, making readers stop and remember the story, especially for light-hearted news.'),
       ('Explain why loaded words in headlines can be powerful.', 'They tell readers how to feel before they read the story, shaping opinion through connotation.')],
  contrast=[('a pun', 'alliteration', 'A pun plays on meanings or sounds of words ("PURR-FECT"); alliteration repeats initial consonant sounds ("Mayor\'s Mega Mall Madness"). Both make headlines memorable in different ways.')],
  misc=[('Headlines are just summaries and do not try to persuade.', 'Headline language (loaded words, puns, emphasis) frames how readers understand and feel about a story.')],
  apply=[('Write a headline using a pun for a story about a local bakery winning an award.', 'Any pun, e.g. "Baker Rises to the Top" or "Bread-y for Glory". 1 mark for a clear pun, 1 for relevance.', 2),
         ('Write two headlines for the same story – a skatepark opening – one positive and one negative, using loaded words.', 'E.g. positive "Teens Triumph as Skatepark Opens"; negative "Noise Nightmare as Skatepark Opens". 1 mark each.', 2)],
  evaluate=[('Clever headlines are more important than accurate ones.', ['clever headlines attract readers', 'competition for clicks'], ['misleading headlines damage trust', 'many readers only read the headline'], 'Accuracy matters more, because many readers never read beyond the headline; wit is valuable only when it does not mislead.')])
K.dev_mcq('ch08-st3', None, ids=['headlines', 'skate_a', 'skate_b', 'turtles', 'floodnews'])
pq('ch08-st3', ('C2', 'C3'), (1, 4), None, 'dev', ['Explain the effect of the language used in "{quote}".',
                                                 'What does the choice of words in "{quote}" suggest about the newspaper\'s attitude?',
                                                 'Identify the technique in "{quote}" and explain why a headline writer might use it.'], ids=['headlines', 'skate_a', 'skate_b'], crit=CRIT_B)
pq('ch08-st3', ('C3', 'C4'), (2, 5), None, 'headline', ['Compare the language choices in these headlines. Which is most neutral and which is most loaded?',
                                                      'Explain how each headline uses language to attract readers or influence opinion.'], ids=['headlines'], crit=CRIT_B)


# =============================================================================================
# ch09 Graphic Novels and Visual Storytelling
# =============================================================================================
COMIC = {'comic'}
H('ch09-st1',
  terms=[('panel', 'a single frame or box in a comic or graphic novel showing one moment'),
         ('gutter', 'the space between panels, where the reader imagines what happens between moments'),
         ('speech bubble', 'a shape containing a character\'s spoken words, with a tail pointing to the speaker'),
         ('caption', 'a box of text, often narration, giving context, time or a narrator\'s thoughts'),
         ('splash page', 'a full-page single image used for dramatic impact')],
  facts=[('What is the gutter in a graphic novel?', 'The space between panels', ['The title page', 'A type of speech bubble', 'The colour of the background'], 'Readers fill the gap with imagination.'),
         ('Which feature usually shows a narrator\'s words?', 'A caption box', ['A speech bubble', 'A sound effect', 'A thought bubble'], 'Captions give narration.'),
         ('A jagged "SKREEEE!" in large letters is an example of:', 'a sound effect (onomatopoeia)', ['a caption', 'a gutter', 'a splash page'], 'Sound effects show noise visually.')],
  why=[('Explain why the gutter is important in comics.', 'Readers imagine the action between panels (closure), which involves them actively and can create suspense or humour.'),
       ('Explain why a silent panel can be powerful.', 'Without words, the reader slows down and focuses on expression and image, often showing strong emotion.')],
  contrast=[('a speech bubble', 'a caption', 'A speech bubble contains a character\'s spoken words and points to the speaker; a caption is a box, usually narration or context, not spoken aloud by a character in the scene.')],
  misc=[('Graphic novels are just picture books for younger readers.', 'Graphic novels tell complex stories for all ages, combining images and words in sophisticated ways.')],
  apply=[('Describe two panels showing a character receiving bad news: state the shot and what the speech bubble or caption says.', 'Any two coherent panels, e.g. Panel 1 medium shot of a girl reading a phone, caption "Then the message came."; Panel 2 close-up of her face, no words. Credit purposeful choices.', 4)],
  evaluate=[('Graphic novels require less reading skill than prose novels.', ['images give information quickly', 'less text'], ['readers must interpret images, panels, gutters and text together', 'visual literacy is complex'], 'Graphic novels demand different skills – visual and verbal reading at once – rather than fewer skills.')])
pq('ch09-st1', ('C2', 'C3', 'C4'), (1, 5), COMIC, 'panels', ['Explain how the sequence of panels tells the story on this page.',
                                                          'How does the writer use panels, captions and gutters to control the reader\'s experience?',
                                                          'Analyse the effect of the silent or wordless moments on this page.'], crit=CRIT_B)
K.dev_mcq('ch09-st1', COMIC)
pq('ch09-st1', ('C2', 'C3'), (1, 4), COMIC, 'dev', ['Explain the effect of the {device} in this page.', 'Why might the creator have used a {device} here?'], crit=CRIT_B)

H('ch09-st2',
  terms=[('shot distance', 'how close the "camera" is to the subject: extreme close-up, close-up, medium shot, wide (long) shot'),
         ('camera angle', 'the position from which a subject is viewed: high angle (looking down), low angle (looking up), eye level'),
         ('framing', 'what is included in a panel and how it is arranged, including tilted (Dutch) frames'),
         ('colour palette', 'the range of colours used, which creates mood (warm, cold, muted)')],
  facts=[('What is the usual effect of a low-angle shot?', 'It makes the subject look powerful or threatening', ['It makes the subject look small and weak', 'It shows a wide landscape', 'It hides the subject'], 'Looking up makes things loom.'),
         ('Why might an artist drain colour to grey in a final panel?', 'To show sadness or loss', ['To save ink', 'To show a happy ending', 'To make it look like daytime'], 'Muted colour suggests sorrow.'),
         ('Which shot best shows a character\'s emotion?', 'A close-up of the face', ['A wide shot of a city', 'A high-angle view of a crowd', 'An empty panel'], 'Close-ups reveal expression.')],
  why=[('Explain why artists vary shot distance across a page.', 'Moving from wide to close shots controls focus and emotion – wide shots set the scene, close-ups intensify feeling.'),
       ('Explain why a tilted frame creates unease.', 'The unbalanced angle makes the world look wrong or unstable, matching a disturbing moment.')],
  contrast=[('a high-angle shot', 'a low-angle shot', 'A high-angle shot looks down on a subject, making it seem small or vulnerable; a low-angle shot looks up, making it seem powerful or threatening.')],
  misc=[('Colour in a graphic novel is just decoration.', 'Colour creates mood and meaning, such as warm sunset tones for nostalgia or grey for sadness.')],
  apply=[('Describe the shot distance and angle you would use to show (a) a character feeling lonely in a big city and (b) a bully looming over a victim, explaining each.', '(a) a wide, high-angle shot making the character tiny against buildings; (b) a low-angle shot from the victim\'s viewpoint so the bully looms. 1 mark each choice, 1 each reason.', 4),
         ('Choose a shot distance and angle for a panel showing a hero facing a giant robot, and explain your choice.', 'E.g. a low-angle wide shot from behind the hero, making the robot loom and the hero look brave but small. Credit choice + reason.', 2),
         ('Describe the colour palette you would use for a panel showing a happy memory, and why.', 'E.g. warm golden tones and soft edges to suggest warmth and nostalgia.', 2)],
  evaluate=[('In graphic novels, images matter more than words.', ['images carry setting, emotion and action', 'silent panels show power of images'], ['words give voice, narration and humour', 'meaning comes from the interplay'], 'Images often carry the most information, but the strongest pages combine images and words so that each adds something the other cannot.')])
pq('ch09-st2', ('C2', 'C3', 'C4'), (1, 5), COMIC, 'visual', ['Analyse how shot distance, angle and colour are used on this page and their effects.',
                                                          'Explain how two visual techniques on this page create mood.',
                                                          'How does the artist use framing and colour to guide the reader\'s emotions?'], crit=CRIT_B)
para('ch09-st2', COMIC, c='C4', d=(3, 5))
pq('ch09-st2', 'C3', (1, 4), COMIC, 'dev', ['Explain how the {device} on this page contributes to its mood.',
                                          'How does "{quote}" work with the image to affect the reader?'], crit=CRIT_B)
pq('ch09-st2', 'C3', (2, 4), COMIC, 'theme', ['Explain how the visual choices on this page help to present the theme of {theme}.'], crit=CRIT_B)

H('ch09-st3',
  terms=[('adaptation', 'a new version of a text in a different form or medium, such as a story turned into a comic or film'),
         ('storyboard', 'a sequence of sketches or descriptions planning each shot or panel'),
         ('thumbnail', 'a small, rough sketch used to plan the layout of panels')],
  facts=[('When adapting a story into a comic, what usually happens to long descriptions?', 'They are shown in images rather than words', ['They are copied into speech bubbles', 'They are removed and the story is changed', 'They are put in a footnote'], 'Comics show rather than tell.'),
         ('What is the first step in adapting a scene into a comic strip?', 'Identifying the key moments to show in each panel', ['Colouring the final panel', 'Writing the title in bubble letters', 'Choosing a font'], 'Planning the sequence comes first.')],
  why=[('Explain why adapting a story into a comic requires cutting words.', 'Images show setting, action and emotion, so description and some dialogue become unnecessary; captions are kept short.'),
       ('Explain why sound effects are useful when adapting a suspense story into a comic.', 'Written sounds (a creak, a knock) can be shown as lettering inside the image, recreating the tension that narration created in the story.'),
       ('Explain why the adapter must decide how many panels to use for a moment.', 'More panels slow time and build tension; fewer panels speed the action, so panel count controls pacing.')],
  contrast=[('a storyboard', 'a finished comic page', 'A storyboard is a rough plan of shots or panels used to organise a sequence; a finished comic page has final artwork, lettering, colour and layout for readers.'),
            ('narration in a story', 'captions in a comic', 'A story\'s narrator can describe at length; a comic\'s captions must be brief, because images carry most of the description.')],
  misc=[('An adaptation should copy every line of the original text.', 'Adaptations select and transform; they must use the strengths of the new medium, so many words become images.'),
        ('A character\'s thoughts cannot be shown in a comic.', 'Thoughts can be shown through thought bubbles, captions, facial expressions in close-up, or symbolic images.'),
        ('Every sentence of the story needs its own panel.', 'Adapters choose key moments; some sentences become one panel, others are cut, and some moments are stretched across several panels for pacing.')],
  apply=[('Adapt this sentence into two comic panels: "Thabo crouched. The dog looked at him. He looked at the poster."', 'Panel 1: medium shot of Thabo crouching to the muddy dog, eye level. Panel 2: over-the-shoulder shot from Thabo towards the poster on the lamppost. Credit shot choices and minimal text.', 3),
         ('Explain which part of the attic extract you would show as a silent panel, and why.', 'E.g. the close-up of Leila\'s hand on the warm handle, with no words, to slow the pace and build suspense.', 2)],
  evaluate=[('A comic-strip adaptation is always simpler than the original story.', ['text is cut', 'inner thoughts are harder to show'], ['images add new layers of meaning', 'panel layout and colour create complexity'], 'Adaptations are different rather than simpler; they lose some narration but gain visual meaning.')],
  extended=[('Adapt a scene from a short story you have read into a six-panel comic strip. For each panel, describe the image (shot, angle, colour) and write any captions or speech bubbles. Then explain two of your choices.', 'Indicative content: six clearly described panels following the scene; varied shots and angles; minimal, purposeful text; explanation linking choices to mood and pacing. Criteria B, C, D.', 12, 'long')])
write('ch09-st3', ids=['maui'])
pq('ch09-st3', ('C3', 'C4'), (2, 5), SUSP | {'prose'}, 'summary', ['Plan a four-panel comic strip adaptation of this extract. For each panel, describe the shot and write one caption or speech bubble.',
                                                                 'Adapt this extract into a short comic: describe three panels, explaining how each shot creates the mood of the original.'], typ='long', crit=CRIT_CR)


# =============================================================================================
# ch10 Language Conventions: Grammar, Punctuation and Style (Criterion D)
# =============================================================================================
@R.add('ch10-st1', 'C1', (1, 3), 'mcq')
def sent_type_mcq(rng, slot):
    s, t = rng.choice(SENT)
    q = rng.choice([f'What type of sentence is this? "{s}"', f'"{s}" This sentence is:', f'Identify the sentence type: "{s}"'])
    return mcq(rng, q, t, TYPE_WRONG[t], f'It is {t}: {TYPE_WHY[t]}.')


@R.add('ch10-st1', 'C3', (1, 4), 'short')
def combine(rng, slot):
    a, conj, ans = rng.choice(COMBINE)
    q = rng.choice([f'Combine these sentences into one using "{conj}": {a}', f'Join the two simple sentences with "{conj}" to make one sentence: {a}'])
    return dict(stem=q, answer=ans, markingKey=f'{ans} 1 mark for correct use of "{conj}"; 1 mark for correct punctuation (a comma after an opening subordinate clause).', type='short', marks=2)


@R.add('ch10-st1', 'C2', (2, 4), 'explain')
def sent_explain(rng, slot):
    s, t = rng.choice([x for x in SENT if x[1] != 'simple'])
    return dict(stem=f'Explain why "{s}" is a {t} sentence.', answer=f'It is {t} because {TYPE_WHY[t]}.', type='explain', marks=2,
                markingKey=f'It is {t} because {TYPE_WHY[t]}. 1 mark for identifying the clauses, 1 for the joining word or structure.')


H('ch10-st1',
  terms=[('clause', 'a group of words containing a subject and a verb'),
         ('independent (main) clause', 'a clause that makes sense on its own as a sentence'),
         ('dependent (subordinate) clause', 'a clause that cannot stand alone, often starting with although, because, when, if or who'),
         ('coordinating conjunction', 'a joining word (for, and, nor, but, or, yet, so) that links two independent clauses'),
         ('subordinating conjunction', 'a word such as although, because, when, if or unless that introduces a dependent clause')],
  why=[('Explain why writers vary sentence types.', 'Variety keeps writing interesting, controls pace (short sentences for impact, longer complex ones for detail) and shows relationships between ideas.'),
       ('Explain why a short simple sentence can be effective after several long sentences.', 'The contrast makes it stand out, adding emphasis, shock or tension.')],
  contrast=[('a compound sentence', 'a complex sentence', 'A compound sentence joins two equal independent clauses with a coordinating conjunction (and, but, so); a complex sentence has an independent clause and a dependent clause introduced by a subordinating conjunction (although, because, when).')],
  misc=[('Long sentences are always better because they sound more sophisticated.', 'Effective writing varies sentence length; long sentences can become confusing, while short ones create emphasis.'),
        ('A complex sentence is any sentence that is hard to understand.', 'In grammar, a complex sentence specifically contains a main clause and at least one subordinate clause.')],
  evaluate=[('Short sentences are a sign of weak writing.', ['too many short sentences can feel choppy', 'complex ideas need complex sentences'], ['short sentences create tension and emphasis', 'skilled writers use them deliberately'], 'Short sentences are weak only when overused or accidental; used deliberately, they are a powerful stylistic tool.')],
  extended=[('Write a paragraph (about 120 words) describing the moment before an exam begins. Use at least one simple, one compound and one complex sentence, and label each.', 'Indicative content: three correctly constructed and labelled sentence types; deliberate effects (e.g. a short simple sentence for tension); accurate punctuation. Criterion D.', 6, 'long')])
pq('ch10-st1', ('C3', 'C4'), (2, 5), SUSP | {'prose'}, 'dev', ['Analyse how the writer uses sentence length and structure in this extract, with reference to "{quote}".',
                                                              'Explain how sentence types help to create the effect of the extract, using "{quote}" as one example.'], crit=CRIT_B)

R.mcqs('ch10-st2', 'C1', (1, 3), [
    ('Which sentence uses the apostrophe correctly?', "The dog's bowl is empty.", ["The dogs' bowl is empty (one dog).", 'The dog\'s are barking.', 'Its\' bowl is empty.'], 'One dog owns the bowl: dog\'s.'),
    ('Which sentence is punctuated correctly?', '"Where are you going?" asked Mum.', ['"Where are you going"? asked Mum.', 'Where are you going? "asked Mum."', '"Where are you going." asked Mum?'], 'The question mark goes inside the speech marks.'),
    ('Which sentence uses a semicolon correctly?', 'I love football; it is my favourite sport.', ['I love; football it is my favourite sport.', 'I love football; and it is my favourite.', 'I; love football.'], 'A semicolon joins two related independent clauses.'),
    ('Which sentence is a comma splice?', 'The weather was awful, we stayed inside.', ['The weather was awful, so we stayed inside.', 'The weather was awful; we stayed inside.', 'Because the weather was awful, we stayed inside.'], 'Two independent clauses joined only by a comma.'),
    ('Which is correct?', "It's raining, and the cat has hurt its paw.", ["Its raining, and the cat has hurt it's paw.", "It's raining, and the cat has hurt it's paw.", "Its raining, and the cat has hurt its paw."], "It's = it is; its = belonging to it."),
    ('Where should the comma go? "After the match we went for pizza."', 'After "match"', ['After "we"', 'After "went"', 'No comma is possible'], 'A comma follows an introductory phrase.'),
    ('Which shows possession by more than one girl?', "The girls' bikes", ["The girl's bikes", 'The girls bikes', "The girls's bikes"], 'Plural possessive: apostrophe after the s.'),
])


@R.add('ch10-st2', 'C3', (1, 4), 'short')
def punct_fix(rng, slot):
    bad, good, rule = rng.choice(PUNCT)
    q = rng.choice([f'Rewrite this sentence with correct punctuation and capital letters: {bad}', f'Correct the punctuation in: {bad}'])
    return dict(stem=q, answer=good, markingKey=f'{good} Rule: {rule}. 1 mark per correction (max 2).', type='short', marks=2)


@R.add('ch10-st2', 'C2', (2, 4), 'explain')
def punct_rule(rng, slot):
    bad, good, rule = rng.choice(PUNCT)
    return dict(stem=f'The corrected sentence is: {good} Explain the punctuation rule that has been applied.', answer=cap_(rule) + '.', type='explain', marks=2,
                markingKey=f'{cap_(rule)}. 1 mark for naming the rule, 1 for explaining it.')


def cap_(s):
    return s[0].upper() + s[1:]


H('ch10-st2',
  terms=[('apostrophe of possession', 'an apostrophe showing that something belongs to someone (the girl\'s bag; the girls\' bags)'),
         ('apostrophe of omission (contraction)', 'an apostrophe showing missing letters (it\'s = it is; don\'t = do not)'),
         ('semicolon', 'a punctuation mark (;) that joins two closely related independent clauses or separates items in a complex list'),
         ('comma splice', 'the error of joining two independent clauses with only a comma'),
         ('speech marks (inverted commas)', 'punctuation marks placed around the exact words spoken')],
  why=[('Explain why punctuation matters for clarity.', 'Punctuation shows where ideas begin and end and how they relate, preventing misreading (e.g. "Let\'s eat, Grandma" vs "Let\'s eat Grandma").'),
       ('Explain why "its" and "it\'s" are often confused.', 'Both sound the same, but "it\'s" means "it is" (omission) while "its" is a possessive pronoun that, like "his", has no apostrophe.')],
  contrast=[('a semicolon', 'a comma', 'A semicolon can join two complete sentences that are closely related; a comma cannot do this on its own (that would be a comma splice) but separates list items, clauses with a conjunction or introductory phrases.')],
  misc=[('You add an apostrophe whenever a word ends in s.', 'Apostrophes show possession or omission only; plurals such as "the dogs are barking" need no apostrophe.')],
  evaluate=[('Punctuation errors do not matter as long as the reader understands.', ['meaning often survives small errors', 'informal texts are relaxed'], ['errors can change meaning or confuse', 'accuracy affects credibility and criterion D marks'], 'Accuracy matters because errors can confuse readers and weaken the writer\'s authority, especially in formal writing.')])

R.mcqs('ch10-st3', 'C1', (1, 3), [
    ('Which sentence is written in a formal register?', 'I would be grateful if you could reply at your earliest convenience.', ['Get back to me ASAP, yeah?', 'Reply soon, lol.', 'Hit me up when you can.'], 'Formal register avoids slang and contractions.'),
    ('Which word is most formal?', 'Request', ['Ask for', 'Beg', 'Nag'], '"Request" suits formal writing.'),
    ('Which audience would most need a formal register?', 'A letter to a government minister', ['A text to your best friend', 'A birthday card for your brother', 'A group chat about football'], 'Official audiences expect formality.'),
    ('Which is an example of slang?', '"That film was sick!"', ['"That film was excellent."', '"The film received positive reviews."', '"The film was screened on Friday."'], '"Sick" is informal slang meaning very good.'),
])


@R.add('ch10-st3', 'C3', (1, 4), 'short')
def reg_rewrite(rng, slot):
    inf, form = rng.choice(REGISTER)
    if rng.random() < 0.5:
        q = f'Rewrite this sentence in a formal register: "{inf}"'
        return dict(stem=q, answer=form, markingKey=f'For example: {form} 1 mark for removing slang/abbreviations, 1 for formal vocabulary and accurate punctuation.', type='short', marks=2)
    q = f'Rewrite this formal sentence in an informal register for a message to a friend: "{form}"'
    return dict(stem=q, answer=inf, markingKey=f'For example: {inf} Credit any natural informal version (contractions, colloquial vocabulary).', type='short', marks=2)


H('ch10-st3',
  terms=[('register', 'the level of formality of language, chosen to suit the audience, purpose and situation'),
         ('formal register', 'language for serious or official situations: standard vocabulary, no slang, few contractions'),
         ('informal register', 'relaxed, conversational language for friends and casual situations, which may include slang and contractions'),
         ('slang', 'very informal words used by particular groups, such as "sick" meaning excellent'),
         ('jargon', 'specialist vocabulary used by a particular profession or group')],
  why=[('Explain why choosing the right register is important.', 'The wrong register can confuse, offend or weaken a message: slang in a letter to a councillor seems disrespectful, while very formal language in a text to a friend sounds cold.'),
       ('Explain why a speech to classmates might mix formal and informal language.', 'A mix can sound respectful but relatable, helping the speaker connect with peers while being taken seriously.')],
  contrast=[('formal register', 'informal register', 'Formal register uses standard vocabulary, full forms and polite structures for official audiences; informal register uses everyday language, contractions and sometimes slang for friends.')],
  misc=[('Formal writing means using the longest words possible.', 'Formal writing should be clear and precise; unnecessarily long words can make writing confusing.')],
  apply=[('Identify three features that make this sentence informal and rewrite it formally: "Hiya! Can\'t make the meeting cos I\'ve got footy, sorry!!"', 'Features: greeting "Hiya", contraction "Can\'t", abbreviation "cos", slang "footy", double exclamation marks. Formal: "I am sorry, but I am unable to attend the meeting because I have football practice."', 4)],
  evaluate=[('Texting and social media are damaging young people\'s ability to write formally.', ['abbreviations creep into school work', 'less practice of long formal writing'], ['young people switch registers skilfully (code-switching)', 'digital writing builds fluency and creativity'], 'Most young people can switch registers when taught to; the key is awareness of audience and purpose rather than avoiding informal writing.')])
pq('ch10-st3', ('C2', 'C3'), (1, 4), NONLIT, 'tone', ['Describe the register of this text and explain why it suits its audience.',
                                                     'Is the language of this text formal or informal? Give two examples and explain the effect.'], crit=CRIT_B)
K.vocab('ch10-st3', d=(1, 3))

R.mcqs('ch10-st4', 'C1', (1, 3), [(q.replace('___', '______'), a, w, f'"{a}" shows {why}.') for q, a, w, why in CONNECT])


@R.add('ch10-st4', 'C3', (1, 4), 'short')
def connective_fill(rng, slot):
    q, a, w, why = rng.choice(CONNECT)
    return dict(stem=f'Choose a suitable connective to fill the gap and explain your choice: "{q}"', answer=f'{a} (or a similar connective) – it shows {why}.',
                markingKey=f'{a} or a suitable alternative showing {why} (1); explanation of the relationship (1).', type='short', marks=2)


H('ch10-st4',
  terms=[('topic sentence', 'the sentence, usually first, that states the main idea of a paragraph'),
         ('cohesion', 'the way ideas in a text are linked so that it flows logically'),
         ('connective (discourse marker)', 'a word or phrase that links ideas, such as however, furthermore, as a result'),
         ('paragraph', 'a group of sentences about one main idea; a new paragraph starts with a change of time, place, topic or speaker')],
  why=[('Explain why writers start a new paragraph.', 'A new paragraph signals a change of time, place, topic or speaker, helping readers follow the structure.'),
       ('Explain why connectives improve an argument.', 'They show the relationships between ideas (addition, contrast, cause and effect), making the reasoning clear and logical.')],
  contrast=[('a topic sentence', 'a concluding sentence', 'A topic sentence introduces a paragraph\'s main idea; a concluding sentence sums it up or links to the next paragraph.')],
  misc=[('A paragraph must always be exactly five sentences long.', 'Paragraph length depends on purpose; a one-sentence paragraph can create emphasis, and analytical paragraphs may be longer.'),
        ('Using "and then" between every sentence makes writing cohesive.', 'Repetitive "and then" is weak; varied connectives show precise relationships between ideas.')],
  apply=[('Write a topic sentence for a paragraph arguing that schools should have longer lunch breaks.', 'For example: "Longer lunch breaks would improve students\' concentration in afternoon lessons." Credit a clear, arguable main idea.', 1),
         ('Reorder these sentences into a cohesive paragraph and add one connective: (a) This wastes thousands of cups a year. (b) Our canteen uses plastic cups. (c) We should switch to reusable cups.', '(b) Our canteen uses plastic cups. (a) This wastes thousands of cups a year. (c) Therefore, we should switch to reusable cups.', 3)],
  evaluate=[('Connectives are the most important tool for cohesion.', ['they signal relationships clearly', 'they guide the reader'], ['pronouns, repetition of key words and logical order also create cohesion', 'overusing connectives feels mechanical'], 'Connectives are important, but cohesion also depends on logical order, topic sentences and reference words; good writers use a range.')],
  extended=[('Write three linked paragraphs (about 250 words) arguing for or against homework at weekends. Underline each topic sentence and use at least four different connectives.', 'Indicative content: clear topic sentences; one idea per paragraph; varied connectives (addition, contrast, cause); a logical progression; accurate punctuation. Criteria B and D.', 10, 'long')])


# =============================================================================================
# ch11 Speeches and Oral Presentations
# =============================================================================================
SPEECH = {'speech'}
H('ch11-st1',
  terms=[('hook', 'an opening that grabs the audience\'s attention, such as a question, a shocking fact or a story'),
         ('anecdote', 'a short personal story used to engage an audience and illustrate a point'),
         ('call to action', 'a closing instruction telling the audience what to do'),
         ('counterargument', 'an opposing view that the speaker acknowledges and answers'),
         ('signposting', 'phrases that guide listeners through a speech, such as "First...", "My second point is..."')],
  facts=[('Which is the strongest hook for a speech about plastic pollution?', '"By 2050, there could be more plastic in the sea than fish, by weight."', ['"Today I will talk about plastic."', '"My speech is about the sea."', '"Hello, my name is Sam."'], 'A shocking statistic grabs attention.'),
         ('Why do speeches use signposting phrases such as "Firstly" and "Finally"?', 'Listeners cannot reread, so signposts help them follow the structure', ['To make the speech longer', 'Because it is required by law', 'To confuse the audience'], 'Signposting helps listeners.'),
         ('Which ending best concludes a persuasive speech?', 'A clear call to action', ['A new unrelated topic', 'A list of sources', 'An apology for the speech'], 'Speeches end with what the audience should do.')],
  why=[('Explain why a speech needs a strong hook.', 'Listeners decide quickly whether to pay attention; a hook creates curiosity or emotion so they keep listening.'),
       ('Explain why speakers often include a counterargument.', 'Answering objections shows fairness and confidence and removes doubts that might stop the audience agreeing.')],
  contrast=[('a speech', 'an essay', 'A speech is written for listeners, using direct address, repetition, signposting and a strong ending; an essay is written to be read, using paragraphs, formal analysis and references.')],
  misc=[('A speech is just an essay read aloud.', 'Speeches are designed for the ear: shorter sentences, repetition, direct address and signposting help listeners follow.')],
  apply=[('Write a hook for a speech persuading your class to volunteer at an animal shelter.', 'Any effective hook (question, statistic, anecdote), e.g. "Every night, 40 dogs in our city fall asleep waiting for someone who never comes." Credit engagement and relevance.', 2),
         ('Plan a three-part structure (hook, two arguments with evidence, conclusion) for a two-minute speech on why sport should be compulsory.', 'Any coherent plan with a hook, two supported arguments, a counterargument (optional) and a call to action.', 4)],
  evaluate=[('The ending of a speech matters more than the opening.', ['audiences remember the last words', 'the call to action drives change'], ['without a hook the audience stops listening', 'both frame the message'], 'Both are crucial: the hook earns attention and the ending turns it into action; a strong speech links them.')],
  extended=[('Write a persuasive speech (about 350 words) for a school assembly on a cause you care about.', 'Indicative content: hook; clear structure with signposting; evidence and anecdote; counterargument and rebuttal; rhetorical devices; call to action; spoken register. Criteria B, C, D.', 12, 'long')])
pq('ch11-st1', ('C2', 'C3', 'C4'), (1, 5), SPEECH, 'speechstruct', ['Identify the hook, the main argument and the conclusion of this speech and explain how each works.',
                                                                 'How is this speech structured to persuade its audience?',
                                                                 'Explain how the opening and ending of the speech are designed to affect the audience.'], crit=CRIT_B)
pq('ch11-st1', ('C2', 'C3'), (1, 4), SPEECH, 'dev', DEV_Q, crit=CRIT_B)
para('ch11-st1', SPEECH, c='C4', d=(3, 5))
K.dev_mcq('ch11-st1', SPEECH)

H('ch11-st2',
  terms=[('eye contact', 'looking at members of the audience to engage them and build trust'),
         ('gesture', 'a movement of the hands or body that supports what the speaker says'),
         ('intonation', 'the rise and fall of the voice'),
         ('pace', 'the speed of speaking'),
         ('pause', 'a deliberate silence used for emphasis or to let an idea sink in')],
  facts=[('Why should a speaker pause after an important statistic?', 'To let the audience absorb it', ['To find their place in their notes', 'To end the speech', 'To show they are bored'], 'Pauses give impact.'),
         ('Which delivery choice shows confidence?', 'Steady eye contact and an upright posture', ['Reading with eyes down', 'Speaking very fast', 'Hiding behind the lectern'], 'Body language communicates confidence.')],
  why=[('Explain why eye contact makes a speech more persuasive.', 'It makes each listener feel personally addressed and shows the speaker is sincere and confident.'),
       ('Explain why varying pace and volume is important.', 'A monotone voice loses attention; changes in pace and volume highlight key points and convey emotion.')],
  contrast=[('verbal communication', 'non-verbal communication', 'Verbal communication is the words and how they are spoken (tone, pace, volume); non-verbal communication is body language – eye contact, gesture, posture and facial expression.')],
  misc=[('Good speakers memorise every word and never look at notes.', 'Many effective speakers use brief cue cards; the key is natural delivery and eye contact rather than perfect memorisation.')],
  apply=[('A speaker reads her whole speech quickly with her eyes on her notes. Give two specific improvements and explain their effect.', 'E.g. slow down and pause after key points so the audience can absorb them; look up and make eye contact at the start and end of each paragraph to engage listeners.', 4),
         ('Mark up this line for delivery, showing one pause (/) and one stressed word (CAPITALS): "We cannot wait for someone else to save our planet."', 'E.g. "We cannot WAIT / for someone else to save our planet." Credit sensible choices with a reason.', 2),
         ('Give three pieces of advice to a nervous classmate about delivering a speech.', 'Any three valid tips: practise aloud; use cue cards; breathe and pause; make eye contact with friendly faces; vary pace; stand still and upright.', 3)],
  evaluate=[('How a speech is delivered matters more than what it says.', ['poor delivery loses the audience', 'confident delivery persuades'], ['strong content gives the speech substance', 'audiences notice empty rhetoric'], 'Delivery and content work together: great delivery cannot save weak ideas for long, and strong ideas need effective delivery to be heard.')])
pq('ch11-st2', ('C3', 'C4'), (1, 5), SPEECH, 'delivery', ['Explain how the speaker should deliver this speech, referring to voice, eye contact and gesture.',
                                                        'Annotate this speech for delivery: where should the speaker pause, stress words or gesture? Justify two choices.',
                                                        'How could non-verbal communication strengthen this speech? Refer to specific lines.'], crit=CRIT_OPEN)
pq('ch11-st2', 'C2', (1, 3), SPEECH, 'tone', TONE_Q, crit=CRIT_B)
pq('ch11-st2', 'C3', (1, 4), SPEECH, 'dev', ['How would you deliver the line "{quote}"? Describe your voice, pace and one gesture, and explain why.',
                                           'Explain how a speaker could use pauses and emphasis to make "{quote}" more powerful.'], crit=CRIT_OPEN)

H('ch11-st3',
  terms=[('active listening', 'listening attentively, showing interest and thinking about what is said in order to respond'),
         ('open question', 'a question that invites a detailed answer (e.g. "How could we...?")'),
         ('closed question', 'a question that can be answered with yes, no or a short fact'),
         ('constructive feedback', 'comments that identify strengths and suggest specific improvements respectfully')],
  facts=[('Which is an open question?', '"How could the canteen reduce food waste?"', ['"Do you like the canteen?"', '"Is food waste bad?"', '"Did you finish your talk?"'], 'Open questions invite explanation.'),
         ('Which response shows respectful disagreement?', '"I see your point, but isn\'t the real problem supermarkets?"', ['"That\'s stupid."', '"You\'re wrong."', '"Whatever."'], 'It acknowledges, then challenges.')],
  why=[('Explain why asking a speaker for the source of a statistic is a useful question.', 'It tests whether the evidence is reliable and helps the audience judge the argument.'),
       ('Explain why active listening matters in a discussion.', 'It shows respect, helps listeners understand the argument fully and leads to relevant, thoughtful responses.')],
  contrast=[('an open question', 'a closed question', 'An open question invites a detailed answer ("Why...?", "How...?"); a closed question can be answered with yes/no or one fact.')],
  misc=[('Questioning a speaker is rude.', 'Respectful questions show engagement and help test and develop ideas; tone and wording keep them polite.')],
  apply=[('Write two open questions you could ask a speaker who has argued that school should start later.', 'E.g. "What evidence is there that later start times improve grades?"; "How would a later start affect after-school activities?" 1 mark each.', 2),
         ('Turn this closed question into an open one: "Do you think recycling is important?"', 'E.g. "Why do you think recycling is important, and what could our school do better?"', 1)],
  evaluate=[('The audience\'s questions are as important as the speech itself.', ['questions test evidence and reveal weaknesses', 'they turn a talk into dialogue'], ['the speech sets out the ideas', 'poor questions can distract'], 'Good questions make a speech more valuable by testing and extending ideas, but they depend on a clear speech to respond to.')])
pq('ch11-st3', ('C3', 'C4'), (1, 5), SPEECH, 'questions', ['Write three questions you would ask this speaker afterwards: one to clarify, one about evidence and one to challenge respectfully.',
                                                         'Suggest two questions an audience member could ask to test this speaker\'s argument, explaining why each is useful.'], crit=CRIT_OPEN)
pq('ch11-st3', ('C2', 'C3'), (1, 4), None, 'questions', ['Analyse the questions the listeners ask in this transcript: what does each type of question achieve?',
                                                       'Explain how the speaker responds to each question and what this shows about good listening.'], ids=['podcast_qa'], crit=CRIT_B)
para('ch11-st3', None, ids=['podcast_qa'], c='C4', d=(3, 5))
K.dev_mcq('ch11-st3', None, ids=['podcast_qa'])


# =============================================================================================
# ch12 Analysis and Creative Writing Practice (MYP 5 eAssessment style)
# =============================================================================================
H('ch12-st1',
  terms=[('unseen extract', 'a passage you have not studied before, analysed under timed conditions'),
         ('annotation', 'notes and highlights on a text identifying features and their effects'),
         ('effect on the reader', 'how a writer\'s choice makes the reader think or feel'),
         ('structure', 'how a text is organised: its order, openings and endings, shifts in focus and paragraphing')],
  facts=[('When analysing an unseen extract, what should you do first?', 'Read the question and the whole extract carefully', ['Start writing immediately', 'Count the words', 'Look only at the last line'], 'Understanding comes before analysis.'),
         ('Which comment shows analysis of structure?', '"The final one-line paragraph isolates the revelation, creating a cliffhanger."', ['"There is a simile in line 3."', '"The story is about a girl."', '"I liked it."'], 'It explains how organisation creates effect.'),
         ('Which is the best way to refer to evidence in an analysis?', 'A short embedded quotation', ['Copying the whole paragraph', 'Retelling the plot', 'Giving no evidence'], 'Short quotations focus analysis.')],
  why=[('Explain why it is important to analyse structure as well as language.', 'Structure (order, shifts, endings) shapes how meaning unfolds and how readers feel, so ignoring it misses half of the writer\'s choices.'),
       ('Explain why you should comment on effect rather than just naming techniques.', 'Criterion A rewards explaining how choices create meaning and affect the reader; naming a technique alone shows little understanding.')],
  contrast=[('language analysis', 'structure analysis', 'Language analysis looks at word-level and sentence-level choices (imagery, word choice, sentence types); structure analysis looks at how the whole text is organised (openings, shifts, pacing, endings).')],
  misc=[('Feature-spotting (listing techniques) earns high marks.', 'High marks require explaining the effects of choices and linking them to the writer\'s purpose, with evidence.')],
  apply=[('Write three annotations you would make on the opening of the attic extract: one on language, one on structure and one on effect.', 'E.g. language: rhetorical question draws reader in; structure: slow climb up the stairs delays discovery; effect: reader shares Leila\'s fear and curiosity.', 3)],
  evaluate=[('Analysing an unseen text is harder than analysing a studied text.', ['no prior knowledge or notes', 'time pressure'], ['fresh reading can be more personal', 'the same skills apply'], 'It is more demanding under time pressure, but strong analytical skills transfer to any text; practice reduces the difficulty.')],
  extended=[('Write a full analysis (about 400 words) of an unseen extract of your choice, covering language, structure and effect on the reader.', 'Indicative content: clear thesis; analysis of language and structure with embedded quotations; explanation of effects; logical organisation; accurate terminology. Criteria A, B, D.', 12, 'long')])
para('ch12-st1', LIT | LIFE, c=('C3', 'C4'), d=(2, 5), frames=['Read the extract carefully. {gq} Analyse the writer\'s use of language and structure.',
                                                               'Unseen analysis. {gq} Write about 300 words, using evidence and explaining effects on the reader.',
                                                               '{gq}\nIn your answer, comment on language, structure and the effect on the reader.'])
para('ch12-st1', NONLIT, c='C4', d=(3, 5), frames=['Unseen text analysis. {gq} Refer to language, layout or structure, and the intended audience.'])
pq('ch12-st1', ('C2', 'C3'), (1, 4), LIT, 'struct', STRUCT_Q, crit=CRIT_B)
K.vocab('ch12-st1', d=(1, 3))
K.vocab_explain('ch12-st1', c=('C2', 'C3'), d=(2, 4))
K.tone_mcq('ch12-st1', None)
qa('ch12-st1', 'C3', (1, 4), None)

H('ch12-st2',
  terms=[('visual prompt', 'an image used as a starting point for creative writing'),
         ('perspective (in creative writing)', 'the point of view from which the piece is told'),
         ('show, don\'t tell', 'revealing emotions and ideas through specific details, actions and senses rather than stating them'),
         ('narrative arc', 'the shape of a story: opening, rising action, climax and resolution')],
  facts=[('What is the most effective way to use a visual prompt?', 'Use it as a starting point and develop an original idea beyond the literal image', ['Describe every object in the image in order', 'Ignore the image completely', 'Write about how the photo was taken'], 'Examiners reward imaginative interpretation.'),
         ('Which choice adds originality to a story based on an image of an empty swing?', 'Telling it from the point of view of the swing', ['Writing "There was a swing"', 'Listing the colours in the image', 'Copying a film plot'], 'An unusual perspective creates originality.')],
  why=[('Explain why choosing an unusual perspective can improve a creative piece.', 'It makes a familiar image fresh and shows insight and imagination (criterion C).'),
       ('Explain why sensory detail is important in writing inspired by an image.', 'An image shows only sight; adding sound, smell, touch and taste brings the scene to life and immerses the reader.'),
       ('Explain why a creative piece should have a turning point.', 'A turning point creates change and tension, giving the piece shape and purpose rather than a static description.'),
       ('Explain why a clear structure matters in a 400–600 word piece.', 'Limited space means every section must build towards a turning point and ending; a clear arc keeps the piece focused (criterion B).')],
  contrast=[('a literal response to an image', 'an imaginative response to an image', 'A literal response simply describes what the image shows; an imaginative response uses the image as a springboard for a story, character or idea that goes beyond it.'),
            ('first-person narration', 'second-person narration', 'First person ("I") lets the reader share one character\'s thoughts; second person ("you") places the reader inside the story, which can feel immediate and unsettling.')],
  misc=[('Creative writing from a prompt should describe exactly what is in the picture.', 'The image is a stimulus; strong responses build a story, character or idea that goes beyond literal description.'),
        ('A creative piece must have a happy ending.', 'Endings should fit the story; open, bittersweet or surprising endings can be more powerful.'),
        ('Using lots of long, unusual words always improves creative writing.', 'Precise, well-chosen vocabulary matters more than difficult words; overloading sentences can obscure meaning.')],
  apply=[('Look at this image: a cracked smartphone screen lit up in the dark, showing 47 unread messages. Write three possible story ideas, each from a different perspective.', 'Any three distinct ideas with perspectives (e.g. first person – a teen whose secret has been leaked; second person – "you" deciding whether to reply; third person – a parent finding the phone).', 3)],
  evaluate=[('It is better to write a story than a diary entry or letter in response to a visual prompt.', ['stories allow plot and character development', 'examiners expect narrative'], ['diaries and letters can be intimate and original', 'any form can show creativity'], 'Any form can succeed if it suits the idea and shows control; the best choice is the one that lets the writer show insight and style.')])
K.prompts('ch12-st2', 'interpret', c='C3', d=(2, 4))
K.prompts('ch12-st2', 'plan', c=('C3', 'C4'), d=(2, 4))
K.prompts('ch12-st2', 'write', c='C4', d=(3, 5))
K.prompts('ch12-st2', 'open', c=('C3', 'C4'), d=(2, 4))

R.mcqs('ch12-st3', 'C1', (1, 3), [
    ('Which MYP criterion assesses accurate grammar, spelling and punctuation?', 'Criterion D: Using language', ['Criterion A: Analysing', 'Criterion B: Organising', 'Criterion C: Producing text'], 'Criterion D covers accuracy, vocabulary and register.'),
    ('Which MYP criterion assesses the structure and organisation of your response?', 'Criterion B: Organising', ['Criterion A: Analysing', 'Criterion C: Producing text', 'Criterion D: Using language'], 'Criterion B covers structure and referencing.'),
    ('Which MYP criterion assesses imagination and stylistic choices in creative writing?', 'Criterion C: Producing text', ['Criterion A: Analysing', 'Criterion B: Organising', 'Criterion D: Using language'], 'Criterion C rewards insight, imagination and deliberate choices.'),
    ('Each MYP Language and literature criterion is marked out of:', '8', ['10', '5', '20'], 'Each criterion has a maximum of 8.'),
    ('What is the best use of the last five minutes of a timed writing task?', 'Proofreading for errors and clarity', ['Starting a new paragraph', 'Rewriting the title', 'Counting words'], 'Proofreading improves criterion D.'),
])


@R.add('ch12-st3', 'C3', (1, 4), 'short')
def proofread(rng, slot):
    bad, good, errs = rng.choice(PROOF)
    q = rng.choice([f'Proofread and correct this passage: "{bad}"', f'Find and correct the errors in this sentence (criterion D): "{bad}"'])
    return dict(stem=q, answer=good, markingKey=f'{good} Errors: {errs}. 1 mark per error corrected (max 4).', type='short', marks=4 if slot.d >= 3 else 3)


H('ch12-st3',
  terms=[('planning', 'deciding on content, structure and purpose before writing, e.g. with a spider diagram or outline'),
         ('drafting', 'writing a first version, focusing on ideas and structure'),
         ('proofreading', 'checking for errors in spelling, punctuation and grammar'),
         ('editing', 'improving a draft\'s content, structure and style, not just correcting errors'),
         ('success criteria', 'a checklist of what a good response must include, often based on the assessment criteria')],
  why=[('Explain why planning saves time in a timed task.', 'A plan sets out structure and key points in advance, so writing flows logically and the writer does not run out of ideas or time.'),
       ('Explain why editing is different from proofreading.', 'Editing improves ideas, structure and style (criteria B and C); proofreading corrects surface errors (criterion D). Both are needed.')],
  contrast=[('editing', 'proofreading', 'Editing changes content, organisation and style to improve a draft; proofreading checks for surface errors such as spelling, punctuation and grammar.')],
  misc=[('If your ideas are good, spelling and punctuation do not affect your mark.', 'Criterion D (Using language) assesses accuracy, so frequent errors lower the mark even when ideas are strong.')],
  apply=[('Create a five-point success-criteria checklist for a persuasive letter, linked to criteria B, C and D.', 'E.g. (B) letter conventions and logical paragraphs; (B) connectives; (C) at least two persuasive techniques with evidence; (C) clear purpose and call to action; (D) formal register and accurate punctuation.', 5),
         ('A student\'s paragraph is mostly retelling the plot. Give two pieces of advice to improve it against criterion A.', 'E.g. start with an analytical point about the writer\'s choice; embed a short quotation and explain its effect on the reader rather than what happens.', 2)],
  evaluate=[('Self-assessment against the criteria is as useful as teacher feedback.', ['it develops independence', 'students understand what is required'], ['students may misjudge their work', 'teachers notice patterns students miss'], 'Self-assessment is valuable when combined with teacher feedback; together they build understanding of the criteria.')])
write('ch12-st3', kinds=None)
