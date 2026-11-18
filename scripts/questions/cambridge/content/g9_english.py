"""Cambridge IGCSE First Language English 0500 (grade 9): reading units.

Reading skills and strategies, comprehension (Paper 1 Q1), summary writing (Q2), writers' effects (Q3),
extended response to reading (Q4) and timed reading practice. Every source passage below is original
(24 passages, 120-230 words: short stories, descriptive writing, memoir, diary, travel writing, blog,
news, report, magazine feature, interview, speech, letter, leaflet, review, opinion article).

Each passage carries annotations (facts, inferences, vocabulary, phrases, word-level effects, imagery,
structural features, summary points, fact/opinion, viewpoint, an in-role task). Templates quote only the
sentences they need, so different items on the same passage do not become near-duplicates; whole
passages are quoted only by the summary, extended-response, evaluation and timed-practice tasks.
Open items carry a model answer and mark points; level-marked tasks give band descriptors and
indicative content. Reading objectives: R1 explicit meaning, R2 implicit meaning and attitudes,
R3 analyse/evaluate/develop ideas, R4 writers' effects, R5 select for a specific purpose.
"""
import os
import re
from types import SimpleNamespace

from ._lib import topic, mcq, compose, person, city, fmt  # noqa: F401
from core import MARKS

PROFILE = {'mark_scale': {'long': (2.5, 3)}, 'wordy': True}
CHAPTERS = {}


# =========================================================== helpers

def Q(s):
    if s.startswith('‘') and s.endswith('’') and s.count('‘') == 1:
        return s
    if '‘' in s:
        return '“' + s + '”'
    return '‘' + s + '’'


def cap(s):
    return s[:1].upper() + s[1:] if s else s


def low(s):
    return s[:1].lower() + s[1:] if s and not s[:2].isupper() else s


def dot(s):
    s = s.strip()
    return s if s[-1:] in '.!?’' else s + '.'


def mk(C, D, typ=None):
    m = MARKS.get((C, D), (2, 2))[0]
    sc = PROFILE['mark_scale'].get(typ)
    if sc:
        m = max(1, round(m * sc[0]))
    return m


def upto(m):
    return 'Mark points'


def bands(m):
    """Three level bands for m marks: (low, mid, high) as strings."""
    if m <= 2:
        return ('0', '1', str(m))
    a = max(1, round(m * 0.35))
    b = max(a + 1, round(m * 0.7))
    return (f'1–{a}', f'{a + 1}–{b}', f'{b + 1}–{m}' if b + 1 < m else str(m))


def wc(s):
    return len(re.findall(r"[\w’'-]+", s))


def split_sents(text):
    """Sentence splitter that does not split inside quoted speech (‘…’)."""
    out, start, depth, i, n = [], 0, 0, 0, len(text)
    while i < n:
        c = text[i]
        if c == '‘':
            depth += 1
        elif c == '’' and depth > 0 and not (text[i + 1:i + 2].isalpha()):
            depth -= 1
        if c in '.!?':
            j = i + 1
            if j < n and text[j] in '’”':
                if depth > 0:
                    depth -= 1
                j += 1
            if depth == 0 and j + 1 < n and text[j] == ' ' and (text[j + 1].isupper() or text[j + 1].isdigit() or text[j + 1] in '‘“'):
                out.append(text[start:j].strip())
                start = j + 1
            i = j
            continue
        i += 1
    out.append(text[start:].strip())
    return [x for x in out if x]


def sents(P):
    if not hasattr(P, '_s'):
        P._s = split_sents(P.text)
    return P._s


def span(P, loc):
    """(first, last) sentence indices covering loc (a loc may run across sentences)."""
    ss = sents(P)
    for i, s in enumerate(ss):
        if loc in s:
            return i, i
    for i in range(len(ss)):
        for j in range(i + 1, min(i + 4, len(ss))):
            if loc in ' '.join(ss[i:j + 1]):
                return i, j
    raise ValueError(f'{P.title}: {loc!r} not found')


def sidx(P, loc):
    return span(P, loc)[0]


def sent(P, loc):
    i, j = span(P, loc)
    return ' '.join(sents(P)[i:j + 1])


def ext(P, locs, pad=0):
    """Quote the sentences containing each loc (in text order), joined with an ellipsis across gaps."""
    ss = sents(P)
    idx = set()
    for l in locs:
        i, j = span(P, l)
        idx |= set(range(i, j + 1))
    idx = sorted(idx)
    if pad and idx:
        idx = sorted(set(idx) | {min(idx[-1] + 1, len(ss) - 1)})
    out, prev = [], None
    for i in idx:
        if prev is not None and i != prev + 1:
            out.append('…')
        out.append(ss[i])
        prev = i
    return ' '.join(out)


def src(P):
    return f'the {P.kind} {Q(P.title)}'


def a_kind(P):
    if P.kind == 'travel writing':
        return 'a piece of travel writing'
    return ('an ' if P.kind[0] in 'aeiou' else 'a ') + P.kind


def full(P):
    return f'Read the {P.kind} {Q(P.title)}: “{P.text}”'


ALL = []


def P(**kw):
    d = dict(facts=[], infer=[], vocab=[], phrase=[], effects=[], figs=[], struct=[], summary=None, fo=[], view=None, role=None, mood=None)
    d.update(kw)
    p = SimpleNamespace(**d)
    ALL.append(p)
    return p


# =========================================================== passages (all original)

P(title='The Night Ferry', kind='short story', fam='fiction', cat='fiction',
  audience='general readers of fiction', purpose='to entertain readers with a story', pshort='to entertain',
  gist='A young woman travelling alone on a night ferry feels anxious as the fog closes in, but tries to reassure herself.',
  mood='Mira’s anxiety and sense of isolation',
  text='The ferry left the harbour at nine, an hour late, because the captain refused to cast off until the last delivery van had rattled up the ramp. Mira found a seat on the open deck, her rucksack wedged between her ankles like a nervous dog. Within minutes the lights of the town had shrunk to a smudge, and then the fog swallowed them completely. The engine throbbed beneath her feet. Somewhere below, a child was crying and a radio crackled out a song she half remembered from her grandmother’s kitchen. Mira pulled her scarf tighter. She had told her mother she would be fine travelling alone; she had said it three times, as if repeating it would make it true. Now, with nothing but grey in every direction, she checked her ticket again. Island of Sela, arrival 08:55. Twelve hours. She could manage twelve hours. A deckhand passed, whistling, and nodded at her as though night crossings were the most ordinary thing in the world. For him, she supposed, they were.',
  facts=[('an hour late', 'Why did the ferry leave the harbour late?', 'The captain would not leave until the last delivery van had come on board.', ['The fog was too thick to sail.', 'Mira arrived late at the harbour.', 'The engine had broken down.']),
         ('arrival 08:55', 'At what time was the ferry due to arrive at the Island of Sela?', '08:55', ['09:00', '21:00', '06:40']),
         ('her rucksack wedged', 'Where did Mira keep her rucksack during the crossing?', 'Wedged between her ankles on the open deck.', ['On the seat beside her', 'In a locker below deck', 'In the captain’s cabin'])],
  infer=[('she had said it three times', 'What does this suggest about how Mira really felt about travelling alone?', 'She was anxious and was trying to convince herself, as well as her mother, that she would be all right.', ['She was bored of her mother’s questions.', 'She was calm and confident about the journey.', 'She was angry with her mother for worrying.'], 'repeating the reassurance shows doubt; ‘as if repeating it would make it true’ reveals it did not yet feel true'),
         ('For him, she supposed, they were.', 'What does this sentence suggest about the difference between Mira and the deckhand?', 'The crossing is routine and relaxed for him, but new and unsettling for her.', ['The deckhand is as frightened as Mira.', 'Mira has made the crossing many times before.', 'The deckhand dislikes his job.'], '‘For him’ implies that for her the crossing is anything but ordinary')],
  vocab=[('throbbed', 'beat or pulsed strongly and steadily', ['stopped suddenly', 'shone brightly', 'whispered quietly'], 'it describes an engine felt ‘beneath her feet’, so it is a regular vibration'),
         ('smudge', 'a blurred, unclear mark', ['a bright flash', 'a sharp outline', 'a loud noise'], 'the lights ‘had shrunk’ as the ferry moved away, so they became small and blurred')],
  phrase=[('the fog swallowed them completely', 'the fog hid the town’s lights so that they could no longer be seen at all'),
          ('as though night crossings were the most ordinary thing in the world', 'he behaved as if sailing at night was completely normal and nothing to worry about')],
  effects=[('swallowed', 'the fog is overwhelming and threatening', '‘Swallowed’ presents the fog as a huge mouth consuming the lights; it suggests the town disappears suddenly and completely, leaving Mira cut off and vulnerable.', 'hid'),
           ('rattled', 'a noisy, hurried, last-minute arrival', '‘Rattled’ suggests an old, noisy van bumping up the ramp at the last moment, making the departure feel chaotic rather than calm and orderly.', 'drove'),
           ('crackled', 'a weak, distant, broken sound', '‘Crackled’ suggests a poor signal and a faint, broken song, which matches the half-remembered memory of her grandmother and makes home seem far away.', 'played')],
  figs=[('her rucksack wedged between her ankles like a nervous dog', 'simile', 'the simile transfers Mira’s nervousness to the rucksack: a nervous dog presses close to its owner for comfort, suggesting she is clinging to familiar things for security.'),
        ('The engine throbbed beneath her feet', 'personification', 'the engine seems to have a pulse like a heartbeat, which mirrors Mira’s own tension and makes the ship feel alive and unsettling.')],
  struct=[('Twelve hours. She could manage twelve hours.', 'repetition', 'the short, repeated sentences sound like Mira talking herself into calm; they slow the pace at a moment of doubt.', ['short sentence']),
          ('Island of Sela, arrival 08:55.', 'minor sentence', 'the verbless sentence copies the words on the ticket, focusing the reader on how far she still has to go.', [])],
  role=('Imagine you are Mira. The morning after the crossing you write a journal entry.', ['what happened before and during the departure', 'your thoughts and feelings during the night', 'how you now feel about travelling alone'],
        [('an hour late', 'the late departure caused by the delivery van', 'the delay gave more time to worry; frustration before the journey even began'),
         ('the fog swallowed them completely', 'the town disappearing in the fog', 'feeling cut off from home and everything familiar'),
         ('she had said it three times', 'her repeated promises to her mother', 'she was more frightened than she admitted; perhaps she now feels guilty or proud'),
         ('A deckhand passed, whistling', 'the calm deckhand', 'his ease could have reassured her, or made her feel more like an outsider')],
        'Dear Journal, I am writing this on the quayside at Sela with salt still in my hair. Last night, when the fog swallowed the last lights of home, I honestly wondered whether I had made a terrible mistake…'))

P(title='The Last Mango Tree', kind='short story', fam='fiction', cat='fiction',
  audience='general readers of fiction', purpose='to entertain readers with a story', pshort='to entertain',
  gist='A grandfather says goodbye to the last tree on the orchard he has sold, and passes on a mango stone to his grandchild.',
  mood='Grandfather’s grief and love for the orchard',
  text='Grandfather walked the orchard every evening, even after the land had been sold. He moved slowly between the rows, touching each trunk as if he were taking attendance at a school register. Most of the trees were already gone; the developers had cleared the eastern field in a single week, and now orange flags fluttered where the guavas had been. Only the old mango by the well remained. ‘Planted it the year your mother was born,’ he told me, though I had heard the story a hundred times. Its bark was cracked like a dry riverbed, and its lowest branch dipped so close to the ground that I could sit on it without jumping. That evening he did not speak for a long while. He pressed his palm flat against the trunk and kept it there. Then he took out his pocket knife, cut a single green mango and handed it to me. ‘Keep the stone,’ he said. ‘Plant it somewhere they can’t reach.’',
  facts=[('in a single week', 'How long did it take the developers to clear the eastern field?', 'A single week.', ['A single day', 'A whole month', 'A year']),
         ('Only the old mango by the well remained.', 'Which tree was still standing, and where was it?', 'The old mango tree, beside the well.', ['A guava tree in the eastern field', 'A mango tree by the gate', 'A lime tree beside the house']),
         ('Planted it the year', 'When did Grandfather plant the mango tree?', 'In the year the narrator’s mother was born.', ['In the year the land was sold', 'In the year the narrator was born', 'Before the well was dug'])],
  infer=[('as if he were taking attendance', 'What does this suggest about Grandfather’s feelings for the trees?', 'He thinks of them as individuals he is responsible for and cares about, like a teacher with pupils.', ['He is counting them for the developers.', 'He finds the trees boring.', 'He is checking which ones to sell.'], 'touching ‘each trunk’ shows individual attention and care'),
         ('He pressed his palm flat against the trunk and kept it there.', 'What does this action suggest about Grandfather’s feelings at this moment?', 'He is grieving and saying a silent goodbye; he wants to stay connected to the tree for as long as he can.', ['He is testing whether the tree is strong.', 'He is tired and needs support.', 'He is angry with the tree.'], 'the silence ‘for a long while’ and the lingering touch suggest deep emotion he cannot put into words'),
         ('Plant it somewhere they can’t reach.', 'What does this suggest about Grandfather’s attitude to the developers?', 'He resents them and wants something of the orchard to survive beyond their control.', ['He admires the developers’ work.', 'He wants the narrator to sell the stone to them.', 'He has forgotten about the developers.'], '‘they’ refers to the developers; ‘can’t reach’ implies they destroy whatever they can get hold of')],
  vocab=[('developers', 'people or companies who buy land in order to build on it', ['farmers who grow fruit', 'photographers who develop film', 'teachers who develop pupils’ skills'], 'they ‘cleared’ the field and put up ‘orange flags’, which suggests construction'),
         ('fluttered', 'moved lightly and quickly in the wind', ['burned slowly', 'fell heavily', 'stood completely still'], 'flags are light and move in the breeze')],
  phrase=[('taking attendance at a school register', 'checking each tree one by one, as a teacher checks that every pupil is present'),
          ('somewhere they can’t reach', 'in a place where the developers cannot destroy it')],
  effects=[('cleared', 'quick, complete, business-like destruction', '‘Cleared’ is a neutral, business-like word that makes the destruction of a whole field of trees sound routine and quick; it contrasts with Grandfather’s slow, loving walk and shows how little the developers value the orchard.', 'cut down'),
           ('fluttered', 'careless, almost cheerful new ownership', '‘Fluttered’ is light and carefree, as if the bright orange flags are celebrating where living trees once stood, which makes the loss feel more painful.', 'hung')],
  figs=[('Its bark was cracked like a dry riverbed', 'simile', 'the simile compares the bark to a parched river, suggesting great age, endurance and thirst; the tree, like Grandfather, is old and has survived hardship.'),
        ('as if he were taking attendance at a school register', 'simile', 'comparing Grandfather to a teacher calling the register suggests care, responsibility and routine; it also makes the missing trees feel like absent pupils.')],
  struct=[('Only the old mango by the well remained.', 'short sentence', 'after the long sentence about the cleared field, the short sentence isolates the last tree, mirroring its isolation and making it the focus of the passage.', []),
          ('‘Plant it somewhere they can’t reach.’', 'ending / closing line', 'the passage ends on Grandfather’s instruction, leaving the reader with defiance and hope rather than only loss.', ['direct speech'])],
  role=('Imagine you are the narrator, now an adult. You write a letter to your grandfather telling him what happened to the mango stone.', ['your memories of the last evening in the orchard', 'what you understood about his feelings', 'what you did with the stone and why'],
        [('touching each trunk', 'Grandfather’s evening walk and touching the trees', 'you now understand he was saying goodbye to old friends'),
         ('orange flags fluttered', 'the cleared field and orange flags', 'anger or sadness at how quickly the land was destroyed'),
         ('He pressed his palm flat', 'his silent hand on the trunk', 'his grief, which he could not express in words'),
         ('Keep the stone', 'his instruction about the stone', 'a promise kept: the stone planted somewhere safe as a living memorial')],
        'Dear Grandfather, the stone you gave me that evening is now a tree taller than I am. I still remember the way you pressed your hand against the old mango, as if you were listening to it…'))

P(title='First Day at the Workshop', kind='short story', fam='fiction', cat='fiction',
  audience='general readers of fiction', purpose='to entertain readers with a story', pshort='to entertain',
  gist='A new apprentice works hard on the first day for a demanding carpenter and wins a tiny sign of approval.',
  mood='Mr Okafor’s strictness and the narrator’s determination',
  text='The workshop smelled of pine resin and hot glue, and every surface was furred with sawdust. Mr Okafor did not look up when I came in. He was planing the edge of a door, his whole body leaning into each stroke, and long pale curls of wood spiralled to the floor around his boots. ‘You’re late,’ he said. I was not late; I was ten minutes early. I said nothing. He pointed his chin at a broom propped in the corner, and I understood that this was my first lesson. I swept for an hour. By the time I had finished, my arms ached and the floor gleamed, but he only grunted and handed me a piece of sandpaper and a scrap of rough timber. ‘Smooth,’ he said. ‘Like glass.’ It took me until lunchtime. When he finally ran his thumb along the surface, he paused, and for the briefest moment the corner of his mouth lifted. It was not quite a smile. It was enough.',
  facts=[('ten minutes early', 'How early did the narrator actually arrive?', 'Ten minutes early.', ['Five minutes early', 'An hour early', 'Exactly on time']),
         ('I swept for an hour.', 'How long did the narrator spend sweeping?', 'An hour.', ['Ten minutes', 'Until lunchtime', 'All afternoon']),
         ('pine resin and hot glue', 'What two smells filled the workshop?', 'Pine resin and hot glue.', ['Paint and varnish', 'Sawdust and engine oil', 'Coffee and smoke'])],
  infer=[('‘You’re late,’ he said.', 'Why might Mr Okafor say ‘You’re late’ when the narrator was early?', 'He is testing the narrator, or setting very high, strict standards from the start.', ['He has misread the clock by accident.', 'He wants the narrator to go home.', 'He is making a friendly joke.'], 'the narrator stays silent and accepts the ‘first lesson’, suggesting it is a deliberate test of attitude'),
         ('It was enough.', 'What does ‘It was enough.’ suggest about the narrator’s feelings?', 'Even this tiny sign of approval makes the narrator feel proud and rewarded for a morning of hard work.', ['The narrator is disappointed and wants to leave.', 'The narrator is bored of sanding.', 'The narrator has had enough of Mr Okafor.'], 'the half-smile is ‘not quite a smile’, yet the narrator values it highly')],
  vocab=[('furred', 'covered with a soft, thick layer', ['scratched', 'freshly painted', 'polished'], 'it describes surfaces covered ‘with sawdust’'),
         ('grunted', 'made a short, low sound instead of speaking', ['shouted angrily', 'laughed loudly', 'sang quietly'], '‘but he only’ shows a minimal reaction rather than words of praise')],
  phrase=[('pointed his chin at a broom', 'he showed the narrator the broom with a small movement of his head instead of speaking'),
          ('the corner of his mouth lifted', 'he very nearly smiled')],
  effects=[('furred', 'a thick, soft layer built up over years', '‘Furred’ makes the sawdust sound like an animal’s coat, suggesting a thick, soft layer built up over years of work and creating a vivid, tactile picture of the workshop.', 'covered'),
           ('gleamed', 'shining cleanliness and pride', '‘Gleamed’ suggests the floor shines brightly, showing how thoroughly the narrator worked and hinting at pride, which makes Mr Okafor’s mere grunt feel all the more grudging.', 'was clean'),
           ('grunted', 'grudging, wordless acknowledgement', '‘Grunted’ is an animal-like, wordless sound; it suggests Mr Okafor gives the bare minimum of acknowledgement, emphasising his gruffness.', 'said thanks')],
  figs=[('‘Like glass.’', 'simile', 'the two-word simile sets an exacting standard: glass is perfectly smooth, so Mr Okafor expects flawless work.'),
        ('long pale curls of wood spiralled to the floor', 'visual imagery', 'the image of curls spiralling down shows the skill and rhythm of his planing, making his craftsmanship seem almost graceful.')],
  struct=[('It was not quite a smile. It was enough.', 'ending / closing line', 'two short sentences end the story quietly; the second reverses the first, showing how much the small reaction means.', ['short sentence']),
          ('‘Smooth,’ he said. ‘Like glass.’', 'direct speech', 'the clipped dialogue shows Mr Okafor as a man of very few words whose instructions are brief and demanding.', ['short sentence'])],
  role=('Imagine you are Mr Okafor. That evening you write a journal entry about your new apprentice’s first day.', ['why you treated the apprentice as you did', 'what you noticed about the apprentice’s work and attitude', 'your hopes or doubts for the future'],
        [('You’re late', 'telling the apprentice they were late', 'a deliberate test of whether they would argue or accept discipline'),
         ('I said nothing', 'the apprentice’s silence', 'a sign of patience and respect that impressed him'),
         ('I swept for an hour', 'the hour of sweeping', 'a lesson that a craftsman respects the workshop before touching wood'),
         ('ran his thumb along the surface', 'checking the sanded timber', 'quiet pride: the work was nearly as smooth as glass')],
        'The new one arrived ten minutes early. I told them they were late. They said nothing — good. Most of them argue, and the ones who argue never learn…'))

P(title='Stranded', kind='short story', fam='fiction', cat='fiction',
  audience='general readers of fiction', purpose='to entertain readers with a story', pshort='to entertain',
  gist='A brother and sister walking in the mountains are caught by a sudden storm and shelter under a rock overhang.',
  mood='the danger and violence of the storm',
  text='By three o’clock the sky over the ridge had turned the colour of a bruise. Kenji and his sister had been walking since dawn, and the hut they were aiming for was still two hours away. The first drops of rain were fat and slow, almost playful. Then the wind arrived. It came over the crest with a howl, snatching Aiko’s hat and flinging it into the valley before either of them could move. The path, which had been a friendly ribbon of gravel all morning, became a stream. Kenji’s boots filled with icy water. He could hear his own heartbeat louder than the thunder. ‘We go back,’ Aiko shouted, ‘to the overhang!’ He wanted to argue — they had come so far — but she was already turning, and he knew she was right. They stumbled downhill, clutching at roots and rocks, until the dark mouth of the overhang opened in front of them. Inside, it was dry and smelled of moss. They sat shoulder to shoulder, shaking, and listened to the mountain roar.',
  facts=[('still two hours away', 'How far away was the hut when the storm began?', 'Two hours’ walk away.', ['Ten minutes away', 'A whole day away', 'Just over the ridge']),
         ('snatching Aiko’s hat', 'What did the wind take from Aiko?', 'Her hat.', ['Her rucksack', 'Her map', 'Her walking pole']),
         ('to the overhang', 'Where did Aiko decide they should go?', 'Back to the overhang, a rock shelter.', ['On to the hut', 'Down into the valley', 'Up to the crest'])],
  infer=[('He wanted to argue', 'What does this sentence suggest about Kenji’s feelings about turning back?', 'He was frustrated and reluctant to give up after coming so far, but he accepted that his sister was right.', ['He was delighted to turn back.', 'He did not care what they did.', 'He was angry that Aiko had lost her hat.'], '‘they had come so far’ shows his reluctance; ‘he knew she was right’ shows acceptance'),
         ('They sat shoulder to shoulder', 'What does ‘shoulder to shoulder’ suggest about Kenji and Aiko at the end?', 'They are close and supporting each other, sharing comfort and relief after the danger.', ['They have fallen out and are ignoring each other.', 'They are preparing to fight.', 'They are competing for space.'], 'physical closeness after shared danger suggests unity and comfort')],
  vocab=[('crest', 'the top of a ridge or hill', ['the bottom of a valley', 'a type of tent', 'a mountain stream'], 'the wind ‘came over’ it from above'),
         ('overhang', 'a part of a rock that sticks out above, giving shelter', ['a deep lake', 'a wooden bridge', 'a steep path'], 'inside it ‘was dry’, so it must shelter them from the rain')],
  phrase=[('a friendly ribbon of gravel', 'a narrow path that had seemed easy and safe to walk on'),
          ('the colour of a bruise', 'a dark purple-grey colour that warns of a coming storm')],
  effects=[('snatching', 'a sudden, aggressive theft', '‘Snatching’ suggests a quick, rough, deliberate grab, as if the wind is a hostile thief; with ‘flinging’ it makes the wind seem violent and careless.', 'taking'),
           ('stumbled', 'exhaustion and loss of control', '‘Stumbled’ suggests tripping and nearly falling, showing how exhausted and frightened they are and how dangerous the path has become.', 'walked'),
           ('roar', 'the immense power of the storm', '‘Roar’ makes the mountain sound like a huge wild animal, emphasising the storm’s power and the smallness of the two walkers.', 'noise')],
  figs=[('the colour of a bruise', 'visual imagery', 'a bruise is dark purple and is caused by injury, so the image creates a threatening, painful atmosphere and foreshadows harm.'),
        ('a friendly ribbon of gravel', 'metaphor', 'calling the path a ‘friendly ribbon’ makes it seem harmless and decorative, which makes its sudden change into ‘a stream’ more shocking.'),
        ('the dark mouth of the overhang', 'metaphor', 'the ‘mouth’ suggests the rock could swallow them, yet it offers safety, adding a note of unease even at the moment of rescue.'),
        ('listened to the mountain roar', 'personification', 'the mountain becomes a living, roaring creature, emphasising its power and their vulnerability.')],
  struct=[('Then the wind arrived.', 'short sentence', 'after the gentle description of the rain, this short sentence marks a sudden turning point from calm to danger.', []),
          ('He wanted to argue — they had come so far — but she was already turning', 'dash / parenthesis', 'the dashes interrupt the sentence just as Kenji’s thoughts interrupt his action, showing his inner conflict.', []),
          ('‘We go back,’ Aiko shouted, ‘to the overhang!’', 'direct speech', 'Aiko’s short, shouted command shows her decisiveness and the urgency of the moment.', ['exclamation'])],
  role=('Imagine you are Aiko. After the storm you write a letter to the warden of the mountain hut.', ['what happened on the walk and during the storm', 'how you and Kenji kept safe', 'what advice the hut should give other walkers'],
        [('Kenji and his sister had been walking since dawn', 'walking since dawn and still two hours from the hut', 'perhaps they set out too ambitiously or too late in the season'),
         ('turned the colour of a bruise', 'the darkening sky at three o’clock', 'warning signs that walkers should be told to watch for'),
         ('We go back', 'the decision to turn back to the overhang', 'turning back is safer than pressing on; knowing where shelter is matters'),
         ('They sat shoulder to shoulder', 'sheltering together', 'staying together and keeping warm until the storm passed')],
        'Dear Warden, I am writing to tell you about the storm that caught my brother and me on the ridge path last Saturday, and to suggest some advice that might keep other walkers safe…'))

P(title='The Audition', kind='short story', fam='fiction', cat='fiction',
  audience='general readers of fiction', purpose='to entertain readers with a story', pshort='to entertain',
  gist='A nervous young violinist waits for his audition and calms himself by thinking of home.',
  mood='Tomás’s nerves and self-doubt',
  text='The corridor outside Room 4 was lined with plastic chairs, and on every chair sat someone more talented than Tomás. At least, that was how it felt. The girl beside him was tuning her cello with tiny, confident twists of the pegs, humming the note under her breath. Tomás held his violin case on his knees like a shield. He had practised the Bach every morning for six months, before school, before breakfast, before his little brothers were awake to complain. He knew every bar. But now his fingers felt like they belonged to somebody else — stiff, cold, clumsy. A door opened. A man with a clipboard read out a name that was not his, and the cellist rose and glided away. The silence she left behind was enormous. Tomás closed his eyes and pictured the kitchen at home, the grey light at six o’clock, his mother pretending to sleep through his scales. When the man returned and said ‘Tomás Ferreira?’, he was surprised to find that his hands had stopped shaking.',
  facts=[('every morning for six months', 'For how long had Tomás practised the Bach?', 'Every morning for six months.', ['Every evening for six weeks', 'Once a week for a year', 'Every morning for two months']),
         ('outside Room 4', 'Where were the candidates waiting?', 'In the corridor outside Room 4.', ['In the kitchen', 'In the music library', 'Outside Room 6']),
         ('tuning her cello', 'What was the girl beside Tomás doing?', 'Tuning her cello and humming the note.', ['Reading her music', 'Practising scales on a violin', 'Talking on her phone'])],
  infer=[('on every chair sat someone more talented than Tomás', 'What does this suggest about how Tomás sees himself?', 'He lacks confidence and compares himself unfavourably with everyone else.', ['He is sure he will win.', 'He thinks the others are lazy.', 'He is bored by the other musicians.'], '‘At least, that was how it felt’ shows this is his fear, not a fact'),
         ('his mother pretending to sleep through his scales', 'What does this detail suggest about Tomás’s mother?', 'She is patient and supportive; she puts up with the early-morning noise to encourage him.', ['She is a very heavy sleeper.', 'She dislikes music.', 'She is unaware that he practises.'], '‘pretending’ shows she is awake but chooses not to complain')],
  vocab=[('glided', 'moved smoothly and gracefully', ['ran clumsily', 'crawled slowly', 'stamped angrily'], 'it contrasts with Tomás’s ‘stiff, cold, clumsy’ fingers'),
         ('clumsy', 'awkward and badly controlled', ['skilful and quick', 'warm and soft', 'strong and steady'], 'it is listed with ‘stiff’ and ‘cold’, which all describe fingers that will not work properly')],
  phrase=[('like they belonged to somebody else', 'his fingers no longer felt as though he could control them'),
          ('The silence she left behind was enormous', 'after she left, the quiet felt huge and made him feel more alone and nervous')],
  effects=[('glided', 'effortless, graceful confidence', '‘Glided’ suggests smooth, effortless movement, as if the cellist floats; it emphasises her confidence and makes Tomás’s stiffness seem worse by contrast.', 'walked'),
           ('enormous', 'overwhelming, oppressive quiet', '‘Enormous’ makes the silence feel physically huge, as if it fills the corridor and presses on Tomás, conveying his rising anxiety.', 'noticeable'),
           ('confident', 'the cellist’s self-assurance', '‘Confident’ describes even her tiny movements, highlighting how at ease she is and sharpening Tomás’s sense of inferiority.', 'small')],
  figs=[('Tomás held his violin case on his knees like a shield', 'simile', 'a shield is held for protection in battle, so the simile suggests Tomás feels under attack and is hiding behind his instrument.'),
        ('his fingers felt like they belonged to somebody else', 'simile', 'the simile conveys a frightening loss of control: his own body no longer feels like his, at the moment he needs it most.')],
  struct=[('before school, before breakfast, before his little brothers were awake to complain', 'repetition', 'the repeated ‘before’ builds a sense of dedication and early-morning effort, emphasising how hard he has worked.', ['list of three']),
          ('A door opened.', 'short sentence', 'the short sentence creates a sudden, tense pause as the waiting is interrupted.', []),
          ('stiff, cold, clumsy', 'list of three', 'the three adjectives build up an impression of fingers that refuse to work, intensifying his fear.', ['dash / parenthesis'])],
  role=('Imagine you are Tomás’s mother. After the audition you write a letter to Tomás’s music teacher.', ['how Tomás prepared at home', 'how he seemed on the day of the audition', 'what you hope for him in the future'],
        [('every morning for six months', 'six months of early practice', 'his dedication and discipline at home'),
         ('pretending to sleep', 'listening to his scales', 'she was secretly proud and moved'),
         ('like a shield', 'his nerves on the day', 'she may have noticed his anxiety and wanted to reassure him'),
         ('his hands had stopped shaking', 'his calm at the end', 'pride that he found his own way to face his fear')],
        'Dear Mrs Silva, I am writing to thank you for all the help you have given Tomás. You may not know that he has practised every morning since March, before any of us were awake…'))

P(title='Market Morning', kind='descriptive piece', fam='fiction', cat='fiction',
  audience='general readers', purpose='to describe a place and create atmosphere', pshort='to describe',
  gist='A description of a busy street market from before dawn until the sleepy heat of noon.',
  mood='the energy and heat of the market',
  text='Before dawn the market is only shadows and voices. Then the first trader lifts her shutter with a clatter like a train, and the day begins. Within an hour the narrow lanes are crammed: baskets of glossy aubergines, pyramids of limes, buckets of silver fish still twitching in their shallow water. The air is thick with frying garlic and diesel. A boy weaves between the stalls with a tower of bread rolls balanced on his head, never once looking up. Old women haggle with the stallholders as if their lives depended on a few coins, then laugh and pay what was first asked. Scooters hiss and buzz along the edges like impatient insects. By noon the heat presses down like a hand, the shouting softens to murmurs and the traders doze beneath their awnings. The fish are gone. The limes are fewer. Only the flies remain busy, drawing lazy circles above the empty crates.',
  facts=[('a tower of bread rolls', 'What does the boy carry on his head?', 'A tower of bread rolls.', ['A basket of limes', 'A bucket of fish', 'A crate of aubergines']),
         ('the traders doze beneath their awnings', 'What do the traders do by noon?', 'They doze beneath their awnings.', ['They pack up and go home.', 'They start shouting louder.', 'They cook lunch for the shoppers.']),
         ('The air is thick with', 'Which two smells fill the air?', 'Frying garlic and diesel.', ['Fresh bread and limes', 'Fish and flowers', 'Smoke and coffee'])],
  infer=[('then laugh and pay what was first asked', 'What does this suggest about the old women’s haggling?', 'It is a social ritual or game they enjoy rather than a real attempt to save money.', ['They are very poor and desperate.', 'They are angry with the stallholders.', 'They always get a discount.'], 'they argue ‘as if their lives depended’ on it, then pay the original price and laugh'),
         ('never once looking up', 'What does ‘never once looking up’ suggest about the boy?', 'He is highly skilled and practised at carrying the bread; he does this every day.', ['He is shy of the traders.', 'He is lost.', 'He is about to drop the bread.'], 'balancing a ‘tower’ without looking shows routine expertise')],
  vocab=[('haggle', 'argue about the price before agreeing to buy', ['steal from', 'sell to', 'shout greetings at'], 'they argue over ‘a few coins’ and then ‘pay’'),
         ('awnings', 'sheets of material stretched out to give shade', ['wooden crates', 'metal shutters', 'market stalls on wheels'], 'traders doze ‘beneath’ them in the noon ‘heat’')],
  phrase=[('as if their lives depended on a few coins', 'arguing with great seriousness over a very small amount of money'),
          ('the shouting softens to murmurs', 'the loud noise of the market dies down to quiet talking')],
  effects=[('crammed', 'overcrowding and abundance', '‘Crammed’ suggests the lanes are packed so tightly that nothing more could fit, conveying the abundance and bustle of the market.', 'full'),
           ('twitching', 'freshness and unsettling life', '‘Twitching’ suggests the fish are still just alive, emphasising their freshness but also adding a vivid, slightly unsettling detail.', 'lying'),
           ('presses', 'heavy, oppressive heat', '‘Presses’ makes the heat a physical weight pushing down on the market, explaining why the energy drains away and everyone slows.', 'is')],
  figs=[('with a clatter like a train', 'simile', 'comparing the shutter to a train suggests a loud, long, metallic noise that shatters the quiet and launches the day.'),
        ('Scooters hiss and buzz along the edges', 'onomatopoeia', '‘hiss’ and ‘buzz’ imitate the engines’ sounds, so the reader hears the restless traffic around the market.'),
        ('like impatient insects', 'simile', 'the scooters are compared to insects that will not settle, suggesting constant irritating movement at the edges of the scene.'),
        ('the heat presses down like a hand', 'simile', 'the heat is a hand pressing down, a heavy physical force that makes the market slow and sleepy.'),
        ('Only the flies remain busy, drawing lazy circles', 'personification', 'the flies ‘drawing lazy circles’ are given human idleness, which captures the drowsy, finished mood of the afternoon.')],
  struct=[('Before dawn the market is only shadows and voices.', 'opening hook', 'the opening presents a mysterious, almost empty scene, so the description can build up the market’s energy from nothing.', []),
          ('The fish are gone. The limes are fewer.', 'short sentence', 'the short sentences slow the pace and show the market emptying, in contrast with the crowded lists earlier.', ['repetition']),
          ('baskets of glossy aubergines, pyramids of limes, buckets of silver fish', 'list of three', 'the list piles up goods to convey abundance and colour.', [])],
  role=('Imagine you are the boy who carries the bread rolls. You give a short talk to visitors on a walking tour of the market.', ['what the market is like at different times of the morning', 'what your own work involves', 'advice for visitors who want to enjoy the market'],
        [('Before dawn', 'the market before dawn', 'his early start and the quiet before the noise'),
         ('a tower of bread rolls', 'carrying bread on his head', 'years of practice; pride in his skill'),
         ('Old women haggle', 'the haggling old women', 'haggling is a friendly game, so visitors should join in with good humour'),
         ('By noon the heat presses down', 'the noon heat', 'come early, before the heat and before the best food has gone')],
        'Good morning, everyone, and welcome to the busiest street in the city! If you had come here at five o’clock, you would have seen nothing but shadows…'))

P(title='Learning to Swim at Forty', kind='autobiography', fam='personal', cat='lnf',
  audience='adult readers of a magazine life-writing column', purpose='to recount and reflect on a personal experience', pshort='to recount and reflect',
  gist='The writer describes learning to swim at forty after years of avoiding the water, and the joy of finally floating.',
  mood='the writer’s fear turning to joy',
  text='I grew up three streets from the sea and never learned to swim. As a child I told everyone I preferred sandcastles; as a teenager I said swimming was boring; as an adult I simply stopped going to the beach. So when I signed up for beginners’ lessons at the age of forty, I expected to be laughed at. Instead, I found myself in the shallow end with a retired bus driver, two nurses and a nineteen-year-old student who was terrified of putting her face in the water. Our instructor, Hana, was half my age and endlessly patient. ‘Your body wants to float,’ she kept saying. ‘You just have to stop fighting it.’ For four weeks I fought it. I sank like a dropped spanner. Then, one wet Tuesday in March, I lay back, spread my arms and felt the water lift me as gently as a hand under a sleeping child. I stayed there, staring at the steamed-up ceiling, and laughed out loud. Nobody laughed at me. They clapped.',
  facts=[('three streets from the sea', 'How far from the sea did the writer grow up?', 'Three streets away.', ['Three kilometres away', 'Right on the beach', 'In a city far from the sea']),
         ('For four weeks I fought it.', 'For how long did the writer struggle before managing to float?', 'Four weeks.', ['Four days', 'One lesson', 'A whole year']),
         ('a retired bus driver, two nurses', 'Who else was in the beginners’ class?', 'A retired bus driver, two nurses and a nineteen-year-old student.', ['Only children', 'The writer’s family', 'Other swimming instructors'])],
  infer=[('I expected to be laughed at', 'What does this show about how the writer felt before the first lesson?', 'Embarrassed and self-conscious about being a beginner at forty.', ['Excited and confident.', 'Angry with the instructor.', 'Bored by the idea of swimming.'], 'the fear of mockery shows embarrassment about age and inability'),
         ('as a teenager I said swimming was boring', 'What do the writer’s excuses suggest about how they felt when younger?', 'They were ashamed of not being able to swim and hid it behind excuses.', ['They genuinely found swimming boring.', 'They were too busy with sport.', 'Their parents would not allow it.'], 'a different excuse at each age suggests a cover story rather than a real preference')],
  vocab=[('retired', 'no longer working, usually because of age', ['recently trained', 'very tired', 'part-time'], 'a ‘retired bus driver’ is an older person who used to drive buses'),
         ('steamed-up', 'covered with mist from warm, damp air', ['brightly painted', 'cracked and broken', 'very high'], 'indoor pools are warm and wet, so the ceiling is misty')],
  phrase=[('You just have to stop fighting it', 'you need to relax and trust the water instead of struggling against it'),
          ('endlessly patient', 'never losing her patience, however slow her pupils were')],
  effects=[('fought', 'tense, stubborn struggle', '‘Fought’ turns swimming into a battle, showing how tense the writer was and making the eventual relaxation feel like a victory.', 'tried'),
           ('lift', 'gentle, supportive power', '‘Lift’ suggests the water actively raises and supports the writer, turning it from an enemy into a helper.', 'hold'),
           ('terrified', 'extreme fear', '‘Terrified’ is stronger than ‘afraid’; it shows the class is full of real fear, so the writer is not alone.', 'unsure')],
  figs=[('I sank like a dropped spanner', 'simile', 'a spanner is heavy metal and sinks instantly; the humorous comparison mocks the writer’s own hopelessness.'),
        ('as gently as a hand under a sleeping child', 'simile', 'the image suggests tenderness, safety and trust: the water now supports the writer as a parent supports a child.')],
  struct=[('Nobody laughed at me. They clapped.', 'ending / closing line', 'the ending reverses the fear of being laughed at from the opening, giving a satisfying, circular twist.', ['short sentence']),
          ('As a child I told everyone I preferred sandcastles; as a teenager I said swimming was boring; as an adult I simply stopped going to the beach.', 'list of three', 'the three clauses, separated by semicolons, move through a lifetime of excuses and show how long the problem lasted.', ['repetition'])],
  summary=('the writer’s experience of the swimming lessons', [('expected to be laughed at', 'expected to be mocked as a forty-year-old beginner', 'feelings'),
                                                            ('Instead, I found myself in the shallow end', 'joined a mixed class of other nervous adults', 'events'),
                                                            ('endlessly patient', 'had a young, very patient instructor', 'events'),
                                                            ('For four weeks I fought it.', 'struggled and sank for a month', 'events'),
                                                            ('felt the water lift me', 'finally floated one day in March', 'events'),
                                                            ('laughed out loud', 'felt joy and was applauded, not mocked', 'feelings')], ('how the writer felt', 'what happened')),
  fo=[('I grew up three streets from the sea', 'fact'), ('Hana, was half my age', 'fact'), ('swimming was boring', 'opinion')],
  view=('self-mocking about past fears but warm and encouraging about learning as an adult', [('I sank like a dropped spanner', 'humour at the writer’s own expense'), ('Nobody laughed at me. They clapped.', 'the positive ending encourages others to try')]),
  role=('Imagine you are Hana, the instructor. You write a short article for the swimming club newsletter about this beginners’ class.', ['who joined the class and how they felt at first', 'the difficulties they faced', 'why other adults should not be afraid to learn'],
        [('a retired bus driver, two nurses', 'the mix of learners', 'adult beginners come from all walks of life'),
         ('terrified of putting her face in the water', 'the nervous student', 'fear is normal and can be overcome step by step'),
         ('For four weeks I fought it', 'four weeks of sinking', 'patience is needed; progress is not instant'),
         ('They clapped', 'the class clapping', 'a supportive group helps everyone succeed')],
        'Every September I meet a new group of adults standing at the edge of the shallow end, arms folded, convinced they will be the first person in history who cannot float…'))

P(title='Crossing the Salt Flats', kind='travel writing', fam='personal', cat='lnf',
  audience='readers of a travel magazine', purpose='to recount and reflect on a personal experience', pshort='to recount and reflect',
  gist='The writer crosses a vast salt plain and is moved, unexpectedly, by its silence and emptiness.',
  mood='the strangeness and vastness of the salt flats',
  text='Nothing prepares you for the whiteness. We left the last village at sunrise, and within twenty minutes the land had flattened into a blinding plain of salt that stretched to every horizon. Our driver, Luis, wore two pairs of sunglasses at once and still squinted. In the rainy season, he told us, a thin layer of water turns the flats into the world’s largest mirror, and the sky appears both above and below you. We had come in the dry season, so instead the ground was cracked into hexagons, each one rimmed with a crust of salt as neat as icing on a cake. At noon Luis stopped the jeep and switched off the engine. The silence was so complete that I could hear the blood moving in my ears. There were no birds, no insects, no wind — only an enormous, humming emptiness. I had travelled a long way to see a famous view. I had not expected to be moved by the absence of one.',
  facts=[('two pairs of sunglasses', 'How did Luis protect his eyes from the glare?', 'He wore two pairs of sunglasses at once.', ['He wore a wide hat.', 'He kept his eyes closed.', 'He drove with the windows covered.']),
         ('In the rainy season', 'What happens to the flats in the rainy season?', 'A thin layer of water turns them into a huge mirror that reflects the sky.', ['They flood too deeply to cross.', 'They turn green with grass.', 'They crack into hexagons.']),
         ('cracked into hexagons', 'What did the ground look like in the dry season?', 'It was cracked into hexagons, each edged with a crust of salt.', ['It was covered in a thin layer of water.', 'It was smooth and sandy.', 'It was full of rocks.'])],
  infer=[('I had not expected to be moved by the absence of one.', 'What does the final sentence suggest about the writer’s experience?', 'The emptiness and silence affected the writer more deeply than any famous view could have done.', ['The writer was disappointed by the trip.', 'The writer was bored by the silence.', 'The writer wished they had come in the rainy season.'], '‘moved’ shows emotion; ‘the absence of one’ means the lack of a view')],
  vocab=[('rimmed', 'edged around the border', ['filled to the top', 'hidden underneath', 'broken into pieces'], 'each hexagon has salt around its edge'),
         ('squinted', 'looked with eyes partly closed', ['laughed loudly', 'stared with wide eyes', 'wept'], 'he is facing a ‘blinding’ glare even with sunglasses')],
  phrase=[('the world’s largest mirror', 'a huge, perfectly reflective surface'),
          ('the absence of one', 'the lack of any view at all')],
  effects=[('blinding', 'overwhelming, painful brightness', '‘Blinding’ suggests the white is so intense it almost hurts, conveying the extreme, alien brightness of the landscape.', 'bright'),
           ('humming', 'a silence so deep it seems to make its own sound', '‘Humming’ paradoxically gives the silence a faint sound, suggesting it is so total that the writer becomes aware of tiny internal noises.', 'quiet')],
  figs=[('as neat as icing on a cake', 'simile', 'the homely image of icing makes the salt crust seem neat, decorative and surprisingly delicate.'),
        ('an enormous, humming emptiness', 'oxymoron', 'emptiness cannot really hum; the contradiction captures a silence so complete it feels like a presence.'),
        ('the world’s largest mirror', 'metaphor', 'the flooded flats become a mirror, suggesting perfect reflection and a dizzying sense of sky above and below.')],
  struct=[('Nothing prepares you for the whiteness.', 'opening hook', 'the short opening sentence addresses ‘you’ and creates intrigue about the strange whiteness to come.', ['short sentence']),
          ('There were no birds, no insects, no wind', 'list of three', 'the repeated ‘no’ strips away every sign of life, emphasising the total emptiness.', ['repetition', 'dash / parenthesis'])],
  summary=('what makes the salt flats an unusual place to visit', [('blinding plain of salt', 'a dazzling white plain stretches to every horizon', 'appearance'),
                                                                 ('world’s largest mirror', 'in the rainy season it reflects the sky like a vast mirror', 'appearance'),
                                                                 ('cracked into hexagons', 'in the dry season the ground forms salt-edged hexagons', 'appearance'),
                                                                 ('The silence was so complete', 'the silence is total', 'atmosphere'),
                                                                 ('no birds, no insects, no wind', 'there is no sign of life or movement', 'atmosphere'),
                                                                 ('moved by the absence', 'its emptiness is unexpectedly moving', 'atmosphere')], ('appearance', 'atmosphere')),
  fo=[('Our driver, Luis, wore two pairs of sunglasses at once', 'fact'), ('Nothing prepares you for the whiteness.', 'opinion')],
  view=('awed and reflective; the writer values emptiness over famous sights', [('Nothing prepares you', 'the writer is overwhelmed'), ('moved by the absence of one', 'the writer finds meaning in emptiness')]),
  role=('Imagine you are Luis, the driver. You write an entry for a travel guidebook advising visitors to the salt flats.', ['the best time of year to visit and why', 'what visitors will see and experience', 'how to stay safe and comfortable'],
        [('In the rainy season', 'the rainy-season mirror', 'visit in the rainy season for reflections, dry season for hexagons'),
         ('two pairs of sunglasses', 'the glare', 'bring strong sunglasses and sun protection'),
         ('cracked into hexagons', 'the dry-season ground', 'a different but equally striking sight'),
         ('The silence was so complete', 'the silence at noon', 'many visitors are moved by the stillness; switch off engines and listen')],
        'Visitors ask me every week: when should I come? My answer depends on what you want to see. Come in the rainy season and you will drive across the sky itself…'))

P(title='Turtle Hatchery Diary', kind='diary', fam='personal', cat='lnf',
  audience='the writer (a private diary)', purpose='to recount and reflect on a personal experience', pshort='to recount and reflect',
  gist='A volunteer records a day of beach patrols, egg rescue and a school talk at a turtle hatchery whose funding is ending.',
  mood='the volunteer’s dedication and worry',
  text='Tuesday 14 July. Up at 4.30 again for the beach patrol. Ines and I walked the full three kilometres with red torches — white light confuses the turtles — and found two new nests above the tide line. We marked each one with a numbered stake and logged the GPS position, as we have been taught. Nest 41 had been dug up by a dog during the night. Some eggs were cracked, and the rest lay scattered in the sand like abandoned golf balls. We rescued thirty-two and reburied them in the hatchery enclosure, which took nearly two hours. My back is aching as I write this. In the afternoon I gave the talk for visiting schoolchildren. Last week I mumbled; today they actually asked questions, and one girl wanted to know whether she could volunteer when she is older. I told her yes. I hope I was telling the truth: the project’s funding ends in December, and nobody knows what happens after that.',
  facts=[('the full three kilometres', 'How far did the volunteers walk on the beach patrol?', 'Three kilometres.', ['Four and a half kilometres', 'Thirty kilometres', 'One kilometre']),
         ('white light confuses the turtles', 'Why did the volunteers use red torches?', 'Because white light confuses the turtles.', ['Red torches are cheaper.', 'Red light attracts the turtles.', 'White torches were not allowed on the beach.']),
         ('We rescued thirty-two', 'How many eggs from Nest 41 did they rescue?', 'Thirty-two.', ['Forty-one', 'Two', 'Fourteen']),
         ('funding ends in December', 'When does the project’s funding end?', 'In December.', ['In July', 'Next week', 'In two years'])],
  infer=[('Last week I mumbled', 'What does this suggest about how the writer has changed?', 'They have grown in confidence as a speaker since last week.', ['They have lost interest in giving talks.', 'They are ill.', 'They dislike the schoolchildren.'], 'the contrast between mumbling and the children asking questions shows improvement'),
         ('I hope I was telling the truth', 'What does this suggest about the writer’s feelings about the project’s future?', 'They are worried and uncertain that the project may close and the girl may never be able to volunteer.', ['They are sure the project will continue.', 'They lied to the girl on purpose.', 'They want the project to end.'], '‘nobody knows what happens after that’ follows immediately')],
  vocab=[('enclosure', 'an area surrounded by a fence or barrier', ['a deep hole', 'a type of boat', 'an open beach'], 'eggs are reburied there for protection, away from dogs'),
         ('logged', 'recorded officially', ['cut down', 'forgot', 'hid'], 'they recorded the ‘GPS position’ ‘as we have been taught’')],
  phrase=[('above the tide line', 'higher up the beach than the sea reaches'),
          ('nobody knows what happens after that', 'the future of the project is completely uncertain')],
  effects=[('abandoned', 'neglect and vulnerability', '‘Abandoned’ suggests the eggs have been left with nobody to care for them, emphasising how exposed and vulnerable they are.', 'lying'),
           ('aching', 'physical cost of the work', '‘Aching’ conveys a lingering pain, showing how hard and physical the volunteers’ work is.', 'tired')],
  figs=[('like abandoned golf balls', 'simile', 'comparing the eggs to lost golf balls emphasises their smooth white shape and how carelessly they have been left exposed.')],
  struct=[('Tuesday 14 July.', 'minor sentence', 'the dated heading gives the entry immediacy and authenticity, like a real record of a day.', []),
          ('My back is aching as I write this.', 'present tense', 'the shift into the present tense brings the reader into the moment of writing and shows the physical cost of the work.', ['short sentence'])],
  summary=('the tasks the volunteers carry out', [('Up at 4.30 again for the beach patrol', 'patrol the beach before dawn', 'on the beach'),
                                                 ('with red torches', 'use red torches so as not to confuse turtles', 'on the beach'),
                                                 ('marked each one with a numbered stake', 'mark new nests with numbered stakes', 'on the beach'),
                                                 ('logged the GPS position', 'record each nest’s GPS position', 'on the beach'),
                                                 ('reburied them in the hatchery enclosure', 'rescue damaged nests and rebury eggs in the enclosure', 'on the beach'),
                                                 ('gave the talk for visiting schoolchildren', 'give talks to visiting schoolchildren', 'education')], ('on the beach', 'educating visitors')),
  fo=[('Nest 41 had been dug up by a dog', 'fact'), ('the project’s funding ends in December', 'fact'), ('I hope I was telling the truth', 'opinion')],
  view=('dedicated and proud of the work, but anxious about the future', [('as we have been taught', 'care and professionalism'), ('nobody knows what happens after that', 'anxiety about funding')]),
  role=('Imagine you are the volunteer. You write a letter to a local business asking it to help fund the hatchery after December.', ['what the volunteers do and why it matters', 'the problems the turtles face', 'what difference the money would make'],
        [('beach patrol', 'the early-morning patrols', 'dedication: volunteers give their time before dawn'),
         ('dug up by a dog', 'the damaged nest', 'turtles face threats from animals and people; the hatchery protects eggs'),
         ('visiting schoolchildren', 'the school talks', 'the project educates the next generation'),
         ('funding ends in December', 'the end of the funding', 'without money the work and the education will stop')],
        'Dear Manager, every morning at half past four, two volunteers walk three kilometres of your town’s beach in the dark. I am one of them, and I am writing to ask for your help…'))

P(title='My Grandmother’s Kitchen', kind='memoir', fam='personal', cat='lnf',
  audience='adult readers of a collection of family memories', purpose='to recount and reflect on a personal experience', pshort='to recount and reflect',
  gist='The writer remembers a grandmother who cooked by instinct and discovers, after her death, that she cooked for people rather than from recipes.',
  mood='the warmth and noise of the kitchen',
  text='My grandmother’s kitchen in Lagos was never quiet. The pressure cooker shrieked, the radio argued with itself, and somewhere a neighbour was always knocking at the back door with a bowl to borrow or a piece of news to share. She cooked without measuring anything. When I asked her how much pepper went into her stew, she looked at me as if I had asked how much air went into a song. ‘Enough,’ she said. ‘You will know.’ I did not know. For years my attempts were either bland or so fiery that my friends wept. It was only after she died, when I found her handwritten notebook hidden behind the rice tin, that I understood. There were no quantities in it at all — just names. ‘Pepper: as Mama Bisi likes it.’ ‘Salt: less for Uncle Femi.’ She had not been cooking from recipes. She had been cooking for people.',
  facts=[('hidden behind the rice tin', 'Where did the writer find the notebook?', 'Hidden behind the rice tin.', ['In a drawer by the cooker', 'Under the back door', 'Inside the pressure cooker']),
         ('kitchen in Lagos', 'In which city was the grandmother’s kitchen?', 'Lagos.', ['Accra', 'Nairobi', 'Cairo']),
         ('either bland or so fiery', 'What went wrong with the writer’s attempts at the stew?', 'They were either tasteless or far too spicy.', ['They always burned.', 'They were too salty.', 'They took too long to cook.'])],
  infer=[('as if I had asked how much air went into a song', 'What does this suggest about the grandmother’s attitude to cooking?', 'She saw cooking as an instinctive art, like music, not something to be measured.', ['She did not know how to cook stew.', 'She thought the question was rude.', 'She preferred singing to cooking.'], 'air in a song cannot be measured; the question seems meaningless to her'),
         ('She had been cooking for people.', 'What does the writer finally realise about her grandmother?', 'Her cooking was an act of love, shaped by the tastes of the people she fed.', ['She was a professional chef.', 'She kept her recipes secret to annoy the family.', 'She cooked only for herself.'], 'the notebook lists people’s preferences instead of quantities')],
  vocab=[('bland', 'without much flavour', ['very spicy', 'burnt', 'expensive'], 'it is the opposite of ‘so fiery’'),
         ('fiery', 'very hot and spicy', ['tasteless', 'cold', 'sweet'], 'it made ‘my friends wept’, so it was painfully hot')],
  phrase=[('the radio argued with itself', 'the radio was full of voices talking over each other'),
          ('You will know', 'you will learn to judge by instinct and experience')],
  effects=[('shrieked', 'loud, piercing noise and busy energy', '‘Shrieked’ suggests a high, piercing scream, conveying the noise and urgency of a busy kitchen and making it seem alive.', 'whistled'),
           ('wept', 'comic exaggeration of the spice', '‘Wept’ exaggerates the effect of the spice to comic effect, showing how badly the writer’s attempts went wrong.', 'coughed')],
  figs=[('The pressure cooker shrieked', 'personification', 'the cooker is given a human scream, making the kitchen seem crowded with lively, noisy characters.'),
        ('the radio argued with itself', 'personification', 'the radio seems to quarrel like a person, adding humour and suggesting constant chatter.'),
        ('as if I had asked how much air went into a song', 'simile', 'the comparison makes measuring pepper seem as absurd as measuring air in music, showing cooking as an art.')],
  struct=[('She had not been cooking from recipes. She had been cooking for people.', 'ending / closing line', 'the two balanced sentences contrast ‘recipes’ with ‘people’, delivering the writer’s realisation with emphasis.', ['repetition', 'contrast']),
          ('I did not know.', 'short sentence', 'the blunt short sentence after ‘You will know’ creates humour and shows the writer’s frustration.', [])],
  role=('Imagine you are the writer. At a family celebration you give a short speech about your grandmother.', ['what her kitchen was like', 'how she cooked and what she told you', 'what her notebook taught you'],
        [('never quiet', 'the noisy, busy kitchen', 'a place at the heart of the community, always open to neighbours'),
         ('without measuring anything', 'cooking by instinct', 'her skill came from years of practice and attention'),
         ('Enough', 'her advice ‘You will know’', 'she trusted you to learn by tasting and caring'),
         ('just names', 'the notebook of names', 'cooking is about love for the people you feed')],
        'Good evening, everyone. Most of you will remember the noise of Grandma’s kitchen before you remember her food: the shriek of the pressure cooker, the radio, the knock at the back door…'))

P(title='Town Votes to Close Main Street to Cars', kind='news article', fam='informative', cat='nonfiction',
  audience='readers of a local newspaper', purpose='to report news events', pshort='to inform',
  gist='A town has voted to ban private cars from its main street; supporters and a shop owner give opposing views.',
  text='Residents of Porto Velho voted on Saturday to close the town’s main street to private cars from next April, ending months of heated debate. The proposal, put forward by the town council, won 58 per cent of the vote on a turnout of 71 per cent. Under the plan, the 800-metre street will be open only to pedestrians, cyclists, buses and delivery vehicles before 10 a.m. Supporters argue that the change will cut pollution and bring shoppers back to the centre. ‘Our children will breathe cleaner air, and our cafés will finally have room for outdoor tables,’ said councillor Ana Ribeiro. Not everyone is convinced. Shop owner Felix Mendes, whose hardware store has traded on the street for thirty years, fears customers will simply drive to the out-of-town retail park instead. ‘People don’t carry paint tins on a bicycle,’ he said. The council has promised to build a 300-space car park on the edge of the centre and to review the scheme after one year.',
  facts=[('won 58 per cent of the vote', 'What percentage of voters supported the proposal?', '58 per cent.', ['71 per cent', '42 per cent', '30 per cent']),
         ('delivery vehicles before 10 a.m.', 'When will delivery vehicles be allowed on the street?', 'Before 10 a.m.', ['After 10 p.m.', 'At any time', 'Only at weekends']),
         ('300-space car park', 'What has the council promised to build?', 'A 300-space car park on the edge of the centre.', ['A new cycle lane', 'An 800-space car park in the centre', 'A retail park']),
         ('traded on the street for thirty years', 'How long has Felix Mendes’s hardware store traded on the street?', 'Thirty years.', ['Thirteen years', 'Three years', 'Seventy-one years'])],
  infer=[('People don’t carry paint tins on a bicycle', 'What does this comment suggest about Felix Mendes’s attitude to the plan?', 'He thinks it is impractical for shops selling heavy goods and will harm his business.', ['He is a keen cyclist.', 'He supports the plan fully.', 'He plans to sell bicycles.'], 'the example of heavy paint tins shows customers need cars'),
         ('ending months of heated debate', 'What does this phrase suggest about the town before the vote?', 'The issue had divided the town and caused strong, angry disagreement for a long time.', ['Everyone had agreed from the start.', 'Nobody was interested in the issue.', 'The debate had lasted only a day.'], '‘months’ shows length; ‘heated’ shows strong feeling')],
  vocab=[('turnout', 'the proportion of people entitled to vote who actually voted', ['the result of the vote', 'the number of cars on the street', 'a sudden change of plan'], 'it is given as a percentage ‘on a turnout of 71 per cent’'),
         ('pedestrians', 'people travelling on foot', ['bus drivers', 'shop owners', 'delivery drivers'], 'they are listed separately from ‘cyclists, buses and delivery vehicles’')],
  phrase=[('ending months of heated debate', 'bringing to a close a long period of angry disagreement'),
          ('Not everyone is convinced', 'some people still doubt that the plan is a good idea')],
  effects=[('heated', 'strong, angry feeling', '‘Heated’ suggests the arguments became hot-tempered, conveying how divisive the issue was.', 'long')],
  struct=[('Not everyone is convinced.', 'short sentence', 'the short sentence marks the turn from the supporters’ view to the critics’, giving the article balance.', []),
          ('Residents of Porto Velho voted on Saturday', 'opening hook', 'the opening sentence summarises who, what and when, as news reports do, so readers grasp the story at once.', [])],
  summary=('the arguments for and against closing the street to cars', [('cut pollution', 'it will reduce pollution', 'for'),
                                                                        ('bring shoppers back to the centre', 'it will attract shoppers back to the centre', 'for'),
                                                                        ('breathe cleaner air', 'children will have cleaner air', 'for'),
                                                                        ('room for outdoor tables', 'cafés will have space for outdoor seating', 'for'),
                                                                        ('drive to the out-of-town retail park', 'customers may go to the out-of-town retail park instead', 'against'),
                                                                        ('paint tins on a bicycle', 'shoppers cannot carry heavy goods without a car', 'against')], ('for', 'against')),
  fo=[('won 58 per cent of the vote', 'fact'), ('the 800-metre street will be open only to pedestrians', 'fact'), ('Our children will breathe cleaner air', 'opinion'), ('People don’t carry paint tins on a bicycle', 'opinion')],
  view=('balanced and neutral: the reporter presents both sides without taking a position', [('Supporters argue', 'reports supporters’ view as their argument'), ('Not everyone is convinced', 'introduces the opposing view'), ('review the scheme after one year', 'ends on a neutral fact')]),
  role=('Imagine you are Felix Mendes. You write a letter to the town council about the plan.', ['how the change will affect your shop and customers', 'your response to the supporters’ arguments', 'what the council should do to help businesses like yours'],
        [('thirty years', 'thirty years trading on the street', 'loyal service to the town; deep roots'),
         ('retail park', 'fear of losing customers to the retail park', 'shops in the centre may close'),
         ('cleaner air', 'the councillor’s claim about cleaner air', 'accept the benefit but question the cost to businesses'),
         ('300-space car park', 'the promised car park', 'demand that it is built before April and close to shops')],
        'Dear Councillors, my family has sold paint, nails and garden tools on Main Street for thirty years. I respect the result of Saturday’s vote, but I must explain what it will mean for shops like mine…'))

P(title='Canteen Food Waste Report', kind='report', fam='informative', cat='nonfiction',
  audience='the Head of Year 10', purpose='to present findings and make recommendations', pshort='to present findings',
  gist='A student survey finds large amounts of canteen food waste, explains the causes and recommends three solutions.',
  text='Report to the Head of Year 10: Canteen Food Waste. Purpose: This report presents the findings of a two-week survey of food waste in the school canteen and recommends ways to reduce it. Findings: Students threw away an average of 41 kilograms of food each day. The largest single source of waste was rice, which accounted for almost a third of the total, followed by cooked vegetables. Waste was highest on Fridays, when a quarter of students said they skipped lunch to leave early for sports fixtures. In a questionnaire completed by 212 students, the most common reasons given for leaving food were that portions were too large (46 per cent) and that meals went cold while students queued (31 per cent). Recommendations: First, students should be able to choose a small or regular portion. Second, a second serving counter should be opened at peak times to shorten queues. Finally, uneaten food that is safe to use should be offered to the local food bank, with which the school already has links.',
  facts=[('average of 41 kilograms', 'How much food was thrown away on average each day?', '41 kilograms.', ['14 kilograms', '212 kilograms', '46 kilograms']),
         ('The largest single source of waste was rice', 'Which food was the largest single source of waste?', 'Rice.', ['Cooked vegetables', 'Bread', 'Fruit']),
         ('completed by 212 students', 'How many students completed the questionnaire?', '212.', ['41', '46', '31']),
         ('portions were too large (46 per cent)', 'What percentage of students said portions were too large?', '46 per cent.', ['31 per cent', '25 per cent', '41 per cent'])],
  infer=[('with which the school already has links', 'Why might the writer mention that the school already has links with the food bank?', 'To show that the recommendation is practical and easy to put into action.', ['To show the food bank is unreliable.', 'To criticise the canteen staff.', 'To suggest closing the canteen.'], 'existing links mean no new arrangement is needed'),
         ('a quarter of students said they skipped lunch', 'What does the Friday finding suggest about the cause of waste on that day?', 'Food is cooked for more students than actually eat, because many leave early for sport.', ['Friday food tastes worse.', 'The canteen is closed on Fridays.', 'Students eat more on Fridays.'], 'waste is highest when fewer students eat')],
  vocab=[('accounted for', 'made up (a proportion of)', ['explained the reason for', 'paid for', 'counted out loud'], 'rice ‘accounted for almost a third of the total’'),
         ('fixtures', 'arranged sports matches or events', ['pieces of furniture', 'school lessons', 'canteen meals'], 'students ‘leave early for sports fixtures’')],
  phrase=[('at peak times', 'when the canteen is at its busiest'),
          ('safe to use', 'still fit to eat')],
  struct=[('Findings:', 'subheadings', 'subheadings such as ‘Purpose’, ‘Findings’ and ‘Recommendations’ organise the report so the reader can find key information quickly.', []),
          ('First, students should be able to choose a small or regular portion.', 'discourse marker', '‘First’, ‘Second’ and ‘Finally’ sequence the recommendations clearly, showing they are distinct, practical steps.', [])],
  summary=('the causes of canteen food waste and the solutions proposed', [('portions were too large', 'portions are too big', 'causes'),
                                                                         ('meals went cold while students queued', 'food goes cold during long queues', 'causes'),
                                                                         ('skipped lunch to leave early for sports fixtures', 'many students miss Friday lunch for sport', 'causes'),
                                                                         ('choose a small or regular portion', 'offer a choice of portion size', 'solutions'),
                                                                         ('a second serving counter', 'open a second counter at busy times', 'solutions'),
                                                                         ('offered to the local food bank', 'give safe leftovers to the food bank', 'solutions')], ('causes', 'solutions')),
  fo=[('Students threw away an average of 41 kilograms', 'fact'), ('Waste was highest on Fridays', 'fact'), ('students should be able to choose a small or regular portion', 'opinion')],
  view=('concerned but objective and practical', [('average of 41 kilograms', 'precise statistics show objectivity'), ('Recommendations:', 'focus on practical solutions')]),
  role=('Imagine you are the student who wrote the report. You give a speech in a Year 10 assembly to persuade students to waste less food.', ['what the survey found', 'why waste matters', 'what students can do'],
        [('41 kilograms', 'the daily waste figure', 'make it vivid: the weight of a student thrown away every day'),
         ('rice', 'rice as the biggest waste', 'ask for smaller portions if you will not finish'),
         ('skipped lunch', 'Friday sports fixtures', 'tell the canteen in advance; take a packed lunch'),
         ('food bank', 'the food bank recommendation', 'waste could feed local families instead')],
        'Good morning, Year 10. Every school day, we throw away forty-one kilograms of food. That is about the weight of one of you — binned, every single lunchtime…'))

P(title='Why I Gave Up My Smartphone for a Month', kind='blog', fam='personal', cat='nonfiction',
  audience='readers of a lifestyle blog, mostly young adults', purpose='to recount and reflect on a personal experience', pshort='to recount and reflect',
  gist='A blogger describes a month without a smartphone: a hard start, real benefits and a sensible compromise.',
  mood='the writer’s humour and honesty',
  text='Confession: I used to check my phone 140 times a day. I know because an app told me, which is a bit like a biscuit telling you that you eat too many biscuits. So in September I locked my smartphone in a drawer and bought a cheap old phone that could only make calls and send texts. The first week was horrible. I reached for my pocket constantly, like someone feeling for a missing tooth. I got lost twice without a map app, and I missed a friend’s party because the invitation was only on social media. But by week three something had shifted. I was reading actual books on the bus. I slept better — around forty minutes more a night, according to my very old-fashioned diary. Conversations with my flatmates lasted longer than a notification. Am I going back to a smartphone? Honestly, yes; I need it for work. But it now lives in the hallway at night, and the app that counts my checks says I am down to thirty-five. Progress, not perfection.',
  facts=[('140 times a day', 'How many times a day did the writer use to check the phone?', '140 times.', ['35 times', '40 times', '14 times']),
         ('around forty minutes more a night', 'How much extra sleep did the writer get?', 'About forty minutes more a night.', ['About four hours more', 'About fourteen minutes more', 'No extra sleep']),
         ('I am down to thirty-five', 'How many times a day does the writer now check the phone?', 'About thirty-five.', ['140', '40', 'None']),
         ('it now lives in the hallway at night', 'Where does the phone now stay at night?', 'In the hallway.', ['Locked in a drawer', 'Beside the bed', 'At work'])],
  infer=[('which is a bit like a biscuit telling you', 'What does this comparison suggest about the writer’s attitude to the app?', 'They find it ironic and slightly absurd that a phone app warned them about using the phone too much.', ['They think the app is scientific and reliable.', 'They are angry with biscuit companies.', 'They want to delete the app.'], 'a biscuit warning about biscuits is self-contradictory'),
         ('Honestly, yes; I need it for work.', 'What does this answer suggest about the writer?', 'They are honest and realistic rather than pretending the experiment changed everything.', ['They failed the experiment completely.', 'They hate their job.', 'They are lying to readers.'], '‘Honestly’ signals a frank admission')],
  vocab=[('shifted', 'changed', ['broken', 'disappeared', 'stayed the same'], '‘But by week three’ signals a contrast with the horrible first week'),
         ('notification', 'an alert that appears on a phone', ['a long letter', 'a phone call', 'a book'], 'conversations lasted ‘longer than’ it, so it must be very short')],
  phrase=[('lasted longer than a notification', 'conversations became longer and more meaningful than a quick phone alert'),
          ('Progress, not perfection', 'improving is what matters, even if the change is not complete')],
  effects=[('Confession', 'intimate, humorous honesty', '‘Confession’ makes the opening sound like admitting a guilty secret, creating an intimate, humorous tone that draws readers in.', 'Fact'),
           ('horrible', 'blunt, informal admission of difficulty', '‘Horrible’ is blunt and informal, showing honestly how hard the first week was and making the later benefits more believable.', 'difficult')],
  figs=[('like someone feeling for a missing tooth', 'simile', 'the habitual, slightly uncomfortable gesture conveys how automatic and hard to break the habit was.'),
        ('a bit like a biscuit telling you that you eat too many biscuits', 'simile', 'the absurd comparison mocks the irony of a phone app warning against phone use, creating humour.')],
  struct=[('Am I going back to a smartphone?', 'rhetorical question', 'the question anticipates what readers want to know and introduces the writer’s honest compromise.', []),
          ('Progress, not perfection.', 'ending / closing line', 'the short, memorable minor sentence sums up the message like a slogan.', ['minor sentence'])],
  summary=('the benefits and drawbacks of giving up a smartphone', [('reading actual books on the bus', 'read more books', 'benefits'),
                                                                   ('I slept better', 'slept longer', 'benefits'),
                                                                   ('Conversations with my flatmates lasted longer', 'had longer conversations with others', 'benefits'),
                                                                   ('I reached for my pocket constantly', 'felt a constant urge to check', 'drawbacks'),
                                                                   ('I got lost twice', 'got lost without maps', 'drawbacks'),
                                                                   ('missed a friend’s party', 'missed invitations sent online', 'drawbacks')], ('benefits', 'drawbacks')),
  fo=[('I used to check my phone 140 times a day', 'fact'), ('The first week was horrible.', 'opinion'), ('I am down to thirty-five', 'fact')],
  view=('positive but realistic: the writer values the experiment without rejecting smartphones', [('Honestly, yes; I need it for work.', 'admits going back'), ('Progress, not perfection.', 'values improvement over perfection')]),
  role=('Imagine you are one of the writer’s flatmates. You post a reply on the blog describing the month from your point of view.', ['how the writer behaved at the start', 'what changes you noticed', 'whether you would try the experiment yourself'],
        [('reached for my pocket constantly', 'the constant reaching for a missing phone', 'restless, irritable, perhaps comic to watch'),
         ('got lost twice', 'getting lost', 'phoning flatmates for directions'),
         ('Conversations with my flatmates', 'longer conversations', 'flatmates enjoyed the writer’s company more'),
         ('in the hallway', 'phone in the hallway', 'a habit the flatmate might copy')],
        'As the flatmate who had to listen to the drawer being opened and shut forty times on the first night, I feel I have earned the right to reply…'))

P(title='The Return of the Urban Beekeeper', kind='magazine article', fam='informative', cat='nonfiction',
  audience='general readers of a weekend magazine', purpose='to inform readers about a topic', pshort='to inform',
  gist='An urban beekeeper explains why city honey is good, and why hive numbers must be managed to protect wild bees.',
  text='On the flat roof of a bank in central Toronto, eighty thousand bees are hard at work. Their keeper, Grace Lin, climbs a fire escape every Thursday to check the six hives, which produce around 150 jars of honey a year. ‘People expect city honey to taste of exhaust fumes,’ she laughs. ‘In fact, it’s often better than country honey.’ The reason is variety. While farmland bees may feed on a single crop for weeks, city bees forage in parks, gardens, balconies and roadside verges, collecting nectar from hundreds of different plants. Urban beekeeping has boomed over the past decade, but not all experts are delighted. Some ecologists warn that too many honeybee hives in a small area can leave too little food for wild bees, which are often more important pollinators. Lin agrees that numbers must be managed. She now spends as much time planting wildflowers on rooftops as she does tending her hives. ‘A beehive without flowers,’ she says, ‘is just a box of hungry insects.’',
  facts=[('eighty thousand bees', 'How many bees live on the roof?', 'Eighty thousand.', ['Eight thousand', 'One hundred and fifty', 'Six hundred']),
         ('every Thursday', 'How often does Grace Lin check the hives?', 'Every Thursday (once a week).', ['Every day', 'Once a month', 'Every weekend']),
         ('around 150 jars of honey a year', 'How much honey do the hives produce?', 'Around 150 jars a year.', ['Around 15 jars a year', 'Around 150 jars a month', 'Around 80 jars a year'])],
  infer=[('she laughs', 'What does ‘she laughs’ suggest about how Grace Lin responds to people’s expectations?', 'She is amused and confident, used to correcting this mistaken idea.', ['She is offended by the question.', 'She agrees city honey tastes bad.', 'She is nervous about being interviewed.'], 'laughing shows she is relaxed and sure of her answer'),
         ('Lin agrees that numbers must be managed.', 'What does this suggest about Grace Lin’s attitude to the experts’ criticism?', 'She is open-minded and responsible; she accepts valid criticism and acts on it.', ['She ignores the experts.', 'She plans to give up beekeeping.', 'She is angry with ecologists.'], 'she agrees and then plants wildflowers')],
  vocab=[('forage', 'search widely for food', ['sleep through winter', 'build nests', 'attack intruders'], 'bees ‘forage’ in many places, ‘collecting nectar’'),
         ('verges', 'strips of grass at the edge of a road', ['tall buildings', 'river banks', 'flower shops'], 'they are ‘roadside’'),
         ('pollinators', 'creatures that carry pollen between flowers so plants can reproduce', ['animals that eat honey', 'people who keep bees', 'insects that damage crops'], 'wild bees are described as ‘more important’ ones in an ecology context')],
  phrase=[('has boomed over the past decade', 'has grown very quickly in popularity over the last ten years'),
          ('numbers must be managed', 'the number of hives must be controlled')],
  effects=[('boomed', 'rapid, explosive growth', '‘Boomed’ suggests sudden, explosive growth, emphasising how fashionable urban beekeeping has become.', 'grown'),
           ('hungry', 'need and potential harm', '‘Hungry’ stresses the bees’ need for food and hints at the danger to wild bees if there are no flowers.', 'many')],
  figs=[('is just a box of hungry insects', 'metaphor', 'reducing a hive to ‘a box of hungry insects’ strips away its romance and makes her point about flowers memorable.')],
  struct=[('On the flat roof of a bank in central Toronto', 'opening hook', 'the article opens with a surprising image of bees on a bank roof, hooking the reader’s curiosity.', []),
          ('The reason is variety.', 'short sentence', 'the short sentence answers the puzzle of why city honey is good, clearly introducing the explanation.', []),
          ('‘A beehive without flowers,’ she says, ‘is just a box of hungry insects.’', 'ending / closing line', 'ending on Lin’s vivid quotation leaves readers with her key message.', ['direct speech'])],
  summary=('the benefits of urban beekeeping and the concerns about it', [('around 150 jars of honey', 'it produces a large amount of honey', 'benefits'),
                                                                         ('often better than country honey', 'city honey can taste better', 'benefits'),
                                                                         ('hundreds of different plants', 'city bees feed on a wide variety of plants', 'benefits'),
                                                                         ('too little food for wild bees', 'too many hives can starve wild bees', 'concerns'),
                                                                         ('more important pollinators', 'wild bees matter more for pollination', 'concerns'),
                                                                         ('planting wildflowers on rooftops', 'keepers can plant wildflowers to provide food', 'concerns')], ('benefits', 'concerns')),
  fo=[('produce around 150 jars of honey a year', 'fact'), ('it’s often better than country honey', 'opinion'), ('climbs a fire escape every Thursday', 'fact')],
  view=('broadly positive about urban beekeeping but balanced', [('not all experts are delighted', 'includes criticism'), ('Lin agrees that numbers must be managed', 'shows a responsible response')]),
  role=('Imagine you are Grace Lin. You give a talk to residents encouraging them to plant wildflowers on balconies and rooftops.', ['what your bees do in the city', 'the problem experts have warned about', 'how residents can help'],
        [('eighty thousand bees', 'the rooftop hives', 'the city is already home to many bees'),
         ('hundreds of different plants', 'bees forage widely', 'every balcony counts as a food source'),
         ('too little food for wild bees', 'wild bees at risk', 'more flowers support both wild and honeybees'),
         ('planting wildflowers on rooftops', 'her own planting', 'practical steps and an example to follow')],
        'Good evening. Above your heads, on the roof of the bank on King Street, eighty thousand of my bees are asleep. Tomorrow they will be looking for breakfast — and I need your help to feed them…'))

P(title='Speech to the Youth Climate Forum', kind='speech', fam='persuasive', cat='nonfiction',
  audience='young people at a climate forum', purpose='to persuade readers to take action', pshort='to persuade',
  gist='A student explains how a school eco-club noticed lost trees, proved their cooling effect and planted saplings for the future.',
  text='Friends, I want to begin with a number: eleven. That is how many trees stood in our school playground when my mother was a pupil there. Today there is one. The others were cut down, one by one, for a car park, a new science block and a wider gate. Nobody meant any harm. Nobody stopped to count. And that, I believe, is how we lose most things — not in a single disaster, but in small decisions that nobody notices. Last year our eco-club decided to notice. We measured the playground at midday in June: 41 degrees on the tarmac, 29 in the shade of that one remaining tree. Twelve degrees. Think about that the next time someone tells you trees are decoration. So we raised money, we wrote to the council, and in November we planted twenty saplings. Some will die. Most will grow. In twenty years, a pupil you will never meet will sit in their shade and not even think about it. That is exactly the point.',
  facts=[('begin with a number: eleven', 'How many trees were in the playground when the speaker’s mother was a pupil?', 'Eleven.', ['One', 'Twelve', 'Twenty']),
         ('41 degrees on the tarmac', 'What temperature did the club record on the tarmac?', '41 degrees.', ['29 degrees', '12 degrees', '21 degrees']),
         ('we planted twenty saplings', 'How many saplings did the club plant?', 'Twenty.', ['Eleven', 'Twelve', 'One']),
         ('for a car park, a new science block and a wider gate', 'Why were the trees cut down?', 'For a car park, a new science block and a wider gate.', ['Because they were diseased', 'To make room for a sports field', 'Because a storm damaged them'])],
  infer=[('Nobody meant any harm.', 'What does this suggest about the speaker’s attitude to the people who cut down the trees?', 'The speaker does not blame them; the loss came from thoughtlessness rather than bad intentions.', ['The speaker is furious with them.', 'The speaker thinks they were right.', 'The speaker does not know who they were.'], '‘Nobody stopped to count’ shows carelessness, not malice'),
         ('a pupil you will never meet will sit in their shade and not even think about it', 'What does the speaker suggest is the real reward for planting trees?', 'Helping future people who will benefit without knowing it; the action is unselfish.', ['Being thanked publicly.', 'Winning a prize.', 'Having shade for themselves next summer.'], '‘That is exactly the point’ shows the unnoticed benefit is the aim')],
  vocab=[('saplings', 'young trees', ['tree stumps', 'fallen leaves', 'gardeners'], 'they were ‘planted’ and ‘Some will die. Most will grow.’'),
         ('tarmac', 'a hard black material used to surface roads and playgrounds', ['grass', 'a type of tree', 'a shaded area'], 'it is contrasted with ‘the shade’ and is very hot')],
  phrase=[('small decisions that nobody notices', 'minor choices that seem unimportant at the time'),
          ('trees are decoration', 'trees are only there to look nice')],
  effects=[('notice', 'deliberate attention', 'repeating ‘notice’ from the previous sentence turns it into an active choice, presenting the eco-club as the opposite of the careless decision-makers.', 'act')],
  struct=[('I want to begin with a number: eleven.', 'opening hook', 'opening with a single striking number grabs attention and makes the audience wonder what it means.', []),
          ('Twelve degrees.', 'minor sentence', 'the verbless sentence isolates the difference in temperature, giving the key evidence maximum emphasis.', ['short sentence']),
          ('we raised money, we wrote to the council, and in November we planted twenty saplings', 'list of three', 'the list of actions shows determination and suggests that ordinary people can make a difference.', ['repetition']),
          ('Some will die. Most will grow.', 'contrast', 'the balanced short sentences are honest about failure but end on hope.', ['short sentence'])],
  summary=('what the eco-club did and why', [('decided to notice', 'they paid attention to tree loss', 'actions'),
                                           ('We measured the playground', 'they measured playground temperatures', 'actions'),
                                           ('29 in the shade', 'shade was twelve degrees cooler', 'reasons'),
                                           ('we raised money', 'raised money', 'actions'),
                                           ('we wrote to the council', 'contacted the council', 'actions'),
                                           ('planted twenty saplings', 'planted twenty young trees', 'actions'),
                                           ('a pupil you will never meet will sit in their shade', 'to benefit future pupils', 'reasons')], ('actions', 'reasons')),
  fo=[('41 degrees on the tarmac', 'fact'), ('that, I believe, is how we lose most things', 'opinion'), ('in November we planted twenty saplings', 'fact')],
  view=('passionate but reasonable and hopeful', [('Nobody meant any harm', 'fair, not blaming'), ('Twelve degrees', 'uses evidence'), ('That is exactly the point', 'confident conclusion')]),
  role=('Imagine you are a member of the eco-club. You write a letter to the local council asking it to plant trees in other playgrounds.', ['what happened to the trees in your playground', 'the evidence you collected', 'what you want the council to do'],
        [('eleven', 'eleven trees reduced to one', 'loss through small decisions over a generation'),
         ('41 degrees on the tarmac', 'the temperature measurements', 'trees keep children cool and safe'),
         ('we raised money', 'the club’s fundraising', 'young people are willing to help; the council should match it'),
         ('a pupil you will never meet', 'future pupils', 'planting now is an investment for the future')],
        'Dear Councillors, when my mother attended Hillside School, eleven trees shaded its playground. Today one remains. I am writing on behalf of our eco-club to ask you to help other schools before they lose theirs…'))

P(title='Protect Our Night Sky', kind='letter to a newspaper', fam='persuasive', cat='nonfiction',
  audience='readers and editor of a local newspaper', purpose='to persuade readers to take action', pshort='to persuade',
  gist='An astronomer argues that new park floodlights cause light pollution and proposes motion-sensor lighting.',
  text='Dear Editor, I am writing in response to your article last week celebrating the new floodlights at Riverside Park. I understand why many readers welcomed them; nobody wants to walk through a dark park feeling unsafe. However, I would ask the council to think again about how the lights are used. The floodlights now stay on until 2 a.m., seven nights a week, even though the park closes at ten. As a member of the town’s astronomy club for over twenty years, I have watched our night sky disappear. Where I once could trace the Milky Way from my garden, I now see perhaps a dozen stars. Light pollution is not merely a hobby problem for people like me. It disturbs the sleep of nearby residents, confuses migrating birds and wastes a great deal of public money. A simple solution exists: motion-sensor lighting, which switches on only when someone is present. Other towns have done it. Surely ours can too. Yours faithfully, Dr Mei Tanaka',
  facts=[('stay on until 2 a.m.', 'Until what time do the floodlights stay on?', 'Until 2 a.m.', ['Until ten o’clock', 'Until midnight', 'All night until dawn']),
         ('the park closes at ten', 'When does the park close?', 'At ten o’clock.', ['At 2 a.m.', 'At midnight', 'At sunset']),
         ('for over twenty years', 'How long has the writer belonged to the astronomy club?', 'Over twenty years.', ['Over two years', 'About a dozen years', 'Since last week']),
         ('motion-sensor lighting', 'What solution does the writer propose?', 'Motion-sensor lighting that switches on only when someone is present.', ['Removing all lights from the park', 'Closing the park permanently', 'Brighter floodlights'])],
  infer=[('I understand why many readers welcomed them', 'Why does the writer begin by acknowledging other readers’ views?', 'To appear fair and reasonable, so that readers are more willing to accept her argument.', ['Because she agrees with them completely.', 'Because she wants the article withdrawn.', 'Because she is afraid of the dark.'], 'the concession is followed by ‘However’'),
         ('not merely a hobby problem', 'Why does the writer say light pollution is ‘not merely a hobby problem’?', 'She expects readers to dismiss her as a stargazer, so she widens the issue to show it affects everyone.', ['She wants more people to join the club.', 'She thinks astronomy is unimportant.', 'She is giving up her hobby.'], 'she then lists effects on residents, birds and money')],
  vocab=[('migrating', 'moving from one region to another with the seasons', ['nesting', 'singing', 'feeding'], 'it describes birds that are ‘confused’ by lights at night'),
         ('merely', 'only or just', ['mainly', 'never', 'seriously'], 'the writer is arguing that the problem is bigger than a hobby')],
  phrase=[('think again', 'reconsider the decision'),
          ('not merely a hobby problem', 'not only an issue for people who enjoy stargazing')],
  effects=[('disappear', 'gradual, total loss', '‘Disappear’ suggests something valuable vanishing completely before her eyes over years, conveying a strong sense of loss.', 'change'),
           ('Surely', 'confident, challenging appeal', '‘Surely’ assumes the reader must agree, challenging the town to match others and ending the letter on a confident note.', 'Perhaps')],
  struct=[('Surely ours can too.', 'ending / closing line', 'the short final sentence appeals to civic pride, implying it would be shameful for the town to fall behind others.', ['short sentence']),
          ('It disturbs the sleep of nearby residents, confuses migrating birds and wastes a great deal of public money.', 'list of three', 'the list of three effects widens the problem to people, wildlife and money, making the case seem overwhelming.', []),
          ('However, I would ask the council to think again', 'discourse marker', '‘However’ turns from the concession to her main argument, signalling a polite but firm disagreement.', [])],
  summary=('the problems caused by the floodlights and the solution suggested', [('stay on until 2 a.m.', 'lights stay on four hours after the park closes', 'problems'),
                                                                                ('I now see perhaps a dozen stars', 'they hide the stars', 'problems'),
                                                                                ('disturbs the sleep of nearby residents', 'they keep residents awake', 'problems'),
                                                                                ('confuses migrating birds', 'they confuse migrating birds', 'problems'),
                                                                                ('wastes a great deal of public money', 'they waste public money', 'problems'),
                                                                                ('motion-sensor lighting', 'use motion-sensor lights that come on only when needed', 'solution')], ('problems', 'solution')),
  fo=[('The floodlights now stay on until 2 a.m.', 'fact'), ('Surely ours can too.', 'opinion'), ('nobody wants to walk through a dark park feeling unsafe', 'opinion'), ('the park closes at ten', 'fact')],
  view=('concerned and firm, but polite and reasonable', [('I understand why many readers welcomed them', 'concedes the other side'), ('A simple solution exists', 'constructive rather than just critical'), ('Surely ours can too', 'confident appeal')]),
  role=('Imagine you are the council’s parks officer. You write a reply to Dr Tanaka’s letter for the newspaper.', ['why the floodlights were installed', 'your response to each of her concerns', 'what the council will now do'],
        [('feeling unsafe', 'safety concerns', 'residents asked for lighting after incidents in the park'),
         ('until 2 a.m.', 'the late switch-off', 'admit the timing could be reviewed'),
         ('confuses migrating birds', 'the effect on birds', 'agree to consult wildlife experts'),
         ('motion-sensor lighting', 'motion sensors', 'promise a trial or explain costs')],
        'Dear Editor, I would like to thank Dr Tanaka for her thoughtful letter about the floodlights at Riverside Park. The lights were installed for a simple reason: residents told us they did not feel safe…'))

P(title='Visiting the Coral Reef Responsibly', kind='leaflet', fam='informative', cat='nonfiction',
  audience='tourists visiting a marine park', purpose='to give instructions and advice', pshort='to advise',
  gist='A marine park leaflet gives visitors rules for protecting the reef and its wildlife.',
  text='Welcome to Blue Lagoon Marine Park! Our reef is home to more than 300 species of fish and some of the oldest corals in the region. Help us keep it that way by following these simple guidelines. Never stand on or touch the coral. It may look like rock, but it is a living animal, and a single touch can damage its delicate outer layer. Use reef-safe sun cream. Many ordinary sun creams contain chemicals that bleach coral; ask at the visitor centre for approved brands. Keep your distance from turtles and rays — at least three metres — and never chase or feed them. Take all litter home with you, especially plastic bags, which turtles easily mistake for jellyfish. Finally, book your snorkelling trip with a licensed guide. Licensed boats use fixed moorings, so they never drop anchors onto the reef. Remember: take only photographs, leave only bubbles!',
  facts=[('more than 300 species of fish', 'How many species of fish live on the reef?', 'More than 300.', ['Exactly 30', 'Fewer than 100', 'More than 3,000']),
         ('at least three metres', 'How far away should visitors keep from turtles and rays?', 'At least three metres.', ['At least thirty metres', 'At least one metre', 'At least three kilometres']),
         ('which turtles easily mistake for jellyfish', 'Why are plastic bags especially harmful?', 'Turtles mistake them for jellyfish and may eat them.', ['They bleach the coral.', 'They block the moorings.', 'They frighten the fish.']),
         ('Licensed boats use fixed moorings', 'Why should visitors book with a licensed guide?', 'Licensed boats use fixed moorings, so they never drop anchors onto the reef.', ['Licensed guides are cheaper.', 'Licensed boats are faster.', 'Licensed guides let you feed the turtles.'])],
  infer=[('Help us keep it that way', 'What does ‘Help us’ suggest about how the writers want visitors to see themselves?', 'As partners who share responsibility for protecting the reef.', ['As customers who must obey or be fined.', 'As experts on coral.', 'As people who are not welcome.'], '‘us’ includes visitors in the park’s mission'),
         ('It may look like rock, but it is a living animal', 'Why do the writers explain that coral is a living animal?', 'Visitors may think coral is rock and harmless to touch, so the writers correct this to make them take care.', ['To make visitors afraid of coral.', 'To encourage people to collect coral.', 'To show that coral can move.'], '‘may look like rock, but’ corrects a likely misunderstanding')],
  vocab=[('delicate', 'easily damaged', ['very strong', 'brightly coloured', 'dangerous'], '‘a single touch can damage’ it'),
         ('moorings', 'fixed places where boats can be tied up', ['fishing nets', 'snorkels', 'diving lessons'], 'they mean boats ‘never drop anchors’'),
         ('bleach', 'turn white by removing colour', ['feed', 'repair', 'hide'], 'chemicals harm the coral, and bleached coral loses colour')],
  phrase=[('keep it that way', 'protect the reef so it stays as healthy and varied as it is now'),
          ('leave only bubbles', 'leave no trace of your visit')],
  effects=[('living animal', 'a creature that can be hurt', 'calling coral a ‘living animal’ makes it a creature that can be hurt, prompting more care than ‘rock’ would.', 'part of the reef')],
  struct=[('Never stand on or touch the coral.', 'imperative', 'the imperative gives a direct, unmistakable instruction, which suits a leaflet of rules.', ['short sentence']),
          ('Remember: take only photographs, leave only bubbles!', 'ending / closing line', 'the closing slogan uses balanced phrases and an exclamation to make the message memorable.', ['exclamation', 'imperative']),
          ('Welcome to Blue Lagoon Marine Park!', 'opening hook', 'the friendly exclamation welcomes visitors before the rules, creating a positive tone.', ['exclamation'])],
  summary=('how visitors can protect the reef and its wildlife', [('Never stand on or touch the coral.', 'do not touch or stand on coral', 'the reef'),
                                                                 ('Use reef-safe sun cream.', 'use reef-safe sun cream', 'the reef'),
                                                                 ('Keep your distance from turtles and rays', 'stay three metres from turtles and rays', 'wildlife'),
                                                                 ('never chase or feed them', 'do not chase or feed animals', 'wildlife'),
                                                                 ('Take all litter home with you', 'take litter, especially plastic, home', 'wildlife'),
                                                                 ('book your snorkelling trip with a licensed guide', 'use licensed guides whose boats do not anchor on the reef', 'the reef')], ('protecting the coral', 'protecting the animals')),
  fo=[('Our reef is home to more than 300 species of fish', 'fact'), ('these simple guidelines', 'opinion'), ('Licensed boats use fixed moorings', 'fact')],
  view=('friendly but firm; the writers care deeply about the reef', [('Help us keep it that way', 'inclusive and friendly'), ('Never stand on or touch the coral.', 'firm imperatives')]),
  role=('Imagine you are a licensed snorkelling guide. You write a short report for the park manager after a busy week.', ['how visitors behaved on the reef', 'any problems you saw', 'your recommendations'],
        [('touch the coral', 'visitors touching coral', 'some still stand on coral; more briefing needed'),
         ('reef-safe sun cream', 'sun cream', 'sell approved brands on boats'),
         ('chase or feed them', 'chasing turtles', 'stricter distance rules or warnings'),
         ('plastic bags', 'litter', 'more bins at the jetty')],
        'Report to the Park Manager. Purpose: to summarise visitor behaviour on the reef during the week of 3–9 March and recommend improvements…'))

P(title='Review: The Floating Museum', kind='review', fam='persuasive', cat='nonfiction',
  audience='readers of a city culture guide', purpose='to evaluate and recommend', pshort='to review',
  gist='A reviewer praises a museum in a converted ship for its dramatic lower deck, but criticises its dull upper deck and expensive café.',
  text='Housed in a converted cargo ship moored in Lisbon’s harbour, the new Museum of the Sea promises ‘an unforgettable voyage through five centuries of ocean history’. For the most part, it delivers. The lower deck is the star attraction: a dimly lit gallery where a full-size whale skeleton hangs above visitors’ heads, slowly revolving as if still swimming. Children around me gasped; one small boy refused to leave. The interactive navigation room, where you can steer a virtual ship through a storm, is equally gripping, although the queue on the Saturday I visited lasted forty minutes. Less successful is the upper deck, which is crammed with glass cases of maps and instruments labelled in tiny print. After the drama below, it feels like reading a textbook in a cupboard. The café, meanwhile, is overpriced: eight euros for a sandwich and a juice. Overall, though, this is a bold, imaginative museum that deserves its crowds. Go early, go hungry for wonder — and bring your own lunch.',
  facts=[('lasted forty minutes', 'How long was the queue for the navigation room?', 'Forty minutes.', ['Fourteen minutes', 'Four hours', 'Five minutes']),
         ('eight euros for a sandwich and a juice', 'How much did a sandwich and a juice cost in the café?', 'Eight euros.', ['Five euros', 'Eighteen euros', 'Four euros']),
         ('Housed in a converted cargo ship', 'Where is the museum housed?', 'In a converted cargo ship moored in Lisbon’s harbour.', ['In an old lighthouse', 'In a warehouse by the river', 'In a former navy base']),
         ('five centuries of ocean history', 'How many centuries of history does the museum promise to cover?', 'Five centuries.', ['Four centuries', 'Fifty years', 'Ten centuries'])],
  infer=[('one small boy refused to leave', 'What does this detail suggest about the lower deck?', 'It is so exciting that it completely captivates children.', ['It is too frightening for children.', 'It has no exit signs.', 'Children get lost there.'], 'refusing to leave shows strong enjoyment'),
         ('and bring your own lunch', 'What does the final piece of advice suggest about the reviewer’s view of the café?', 'The café is not worth the money, so visitors should avoid it.', ['The café is the best part of the museum.', 'Food is not allowed in the museum.', 'The café is closed at weekends.'], 'it echoes the earlier complaint that the café is ‘overpriced’')],
  vocab=[('gripping', 'very exciting and holding your attention', ['frightening and painful', 'boring and slow', 'confusing'], 'it is ‘equally’ exciting as the whale gallery'),
         ('overpriced', 'too expensive for what it is', ['very cheap', 'good value', 'free of charge'], 'eight euros for a sandwich and a juice'),
         ('moored', 'tied up and kept in one place', ['sunk', 'sailing at sea', 'being repaired'], 'the ship is in a harbour, not at sea')],
  phrase=[('For the most part, it delivers', 'it mostly lives up to its promise'),
          ('go hungry for wonder', 'arrive eager to be amazed')],
  effects=[('star attraction', 'the most impressive highlight', '‘Star attraction’ borrows the language of shows to present the lower deck as the highlight everyone comes to see.', 'main room'),
           ('crammed', 'cluttered overcrowding', '‘Crammed’ suggests too many cases squeezed into too little space, conveying a cluttered, uninviting room.', 'filled')],
  figs=[('like reading a textbook in a cupboard', 'simile', 'the simile suggests something dull, cramped and dark, contrasting sharply with the drama of the lower deck.'),
        ('as if still swimming', 'simile', 'the slowly turning skeleton seems alive, creating wonder and explaining the children’s gasps.')],
  struct=[('Less successful is the upper deck', 'contrast', 'inverting the sentence to begin with ‘Less successful’ marks a clear turn from praise to criticism.', []),
          ('Go early, go hungry for wonder — and bring your own lunch.', 'ending / closing line', 'the imperatives give practical advice; the dash sets up a humorous final jab at the café.', ['imperative', 'repetition', 'dash / parenthesis'])],
  summary=('the strengths and weaknesses of the museum', [('a full-size whale skeleton hangs', 'a dramatic revolving whale skeleton', 'strengths'),
                                                         ('steer a virtual ship through a storm', 'an exciting interactive navigation room', 'strengths'),
                                                         ('bold, imaginative museum', 'a bold, imaginative museum overall', 'strengths'),
                                                         ('the queue on the Saturday I visited lasted forty minutes', 'long queues at weekends', 'weaknesses'),
                                                         ('labelled in tiny print', 'a dull, cluttered upper deck with tiny labels', 'weaknesses'),
                                                         ('The café, meanwhile, is overpriced', 'an overpriced café', 'weaknesses')], ('strengths', 'weaknesses')),
  fo=[('eight euros for a sandwich and a juice', 'fact'), ('this is a bold, imaginative museum that deserves its crowds', 'opinion'), ('Housed in a converted cargo ship', 'fact')],
  view=('broadly enthusiastic, with honest reservations', [('For the most part, it delivers', 'positive overall'), ('Less successful is the upper deck', 'balanced criticism'), ('deserves its crowds', 'recommends it')]),
  role=('Imagine you are the director of the Museum of the Sea. You write a letter replying to the review.', ['thanks for the praise', 'your response to the criticisms', 'changes you will make'],
        [('star attraction', 'praise for the lower deck', 'pride in the whale gallery'),
         ('lasted forty minutes', 'queues', 'timed tickets to reduce waiting'),
         ('tiny print', 'the upper deck', 'redesign with larger labels and interactive screens'),
         ('overpriced', 'café prices', 'introduce a cheaper family menu')],
        'Dear Editor, on behalf of everyone at the Museum of the Sea, thank you for your generous review. We were delighted that our whale made the children gasp…'))

P(title='The Mountain Rescue Volunteer', kind='interview', fam='informative', cat='nonfiction',
  audience='readers of a regional magazine', purpose='to inform readers about a person', pshort='to inform',
  gist='A profile of an unpaid mountain rescue volunteer who explains common hiking mistakes and why he keeps helping.',
  text='Sipho Ndlovu has been called out 212 times in eleven years with the Drakensberg mountain rescue team, and he still keeps his boots by the front door. ‘The phone can ring at three in the morning,’ he says. ‘You have perhaps ten minutes to be in the truck.’ Like the rest of the team, he is an unpaid volunteer; by day he teaches mathematics at a local secondary school. Most call-outs, he explains, are not dramatic falls but simple mistakes: hikers who set off too late, who underestimate how quickly the weather changes, or who rely on a phone battery that dies on the mountain. The worst night he remembers was a search for two teenagers in thick cloud. ‘We found them at dawn, cold and frightened but alive. I have never been so tired or so happy.’ Asked why he continues, he shrugs. ‘Someone came for my father once, years ago. I suppose I am paying it back.’',
  facts=[('212 times in eleven years', 'How many times has Sipho been called out, and over how long?', '212 times in eleven years.', ['112 times in twelve years', '21 times in two years', '212 times in one year']),
         ('perhaps ten minutes to be in the truck', 'How long do volunteers have to reach the truck after a call?', 'About ten minutes.', ['About an hour', 'About three minutes', 'About thirty minutes']),
         ('teaches mathematics', 'What is Sipho’s paid job?', 'He teaches mathematics at a local secondary school.', ['He is a paid rescue officer.', 'He is a mountain guide.', 'He is a doctor.']),
         ('We found them at dawn', 'When were the two teenagers found?', 'At dawn.', ['At three in the morning', 'At midday', 'After two days'])],
  infer=[('he still keeps his boots by the front door', 'What does this detail suggest about Sipho’s commitment?', 'He is always ready to go and is still fully committed after many years.', ['He is untidy.', 'He is planning to quit.', 'He has nowhere else to keep them.'], '‘still’ after eleven years and 212 call-outs'),
         ('I suppose I am paying it back', 'What does this suggest about Sipho’s reason for volunteering?', 'Gratitude: he wants to repay the help his father once received by helping others.', ['He is paid well for it.', 'He enjoys the danger.', 'He was ordered to volunteer.'], '‘Someone came for my father once’')],
  vocab=[('underestimate', 'think something is smaller or less serious than it really is', ['measure exactly', 'fear greatly', 'ignore completely'], 'hikers are surprised by ‘how quickly the weather changes’'),
         ('unpaid', 'not receiving money for work', ['badly trained', 'part-time', 'retired'], 'he has a separate job ‘by day’')],
  phrase=[('paying it back', 'repaying a kindness by helping others in turn'),
          ('set off too late', 'start their walk too late in the day')],
  effects=[('dies', 'sudden, total loss of a lifeline', '‘Dies’ makes the battery seem like a lifeline that fails at the worst moment, stressing how dangerous relying on it is.', 'runs low')],
  struct=[('‘The phone can ring at three in the morning,’ he says.', 'direct speech', 'quoting Sipho brings his own voice into the article, making it vivid and authentic.', []),
          ('I have never been so tired or so happy.', 'contrast', 'pairing ‘tired’ with ‘happy’ shows the exhausting but deeply rewarding nature of rescue work.', ['direct speech'])],
  summary=('the common mistakes that lead to rescues and what volunteering involves', [('set off too late', 'hikers start too late', 'mistakes'),
                                                                                       ('underestimate how quickly the weather changes', 'they underestimate sudden weather changes', 'mistakes'),
                                                                                       ('rely on a phone battery', 'they rely on phones whose batteries fail', 'mistakes'),
                                                                                       ('ring at three in the morning', 'volunteers are called at any hour', 'volunteering'),
                                                                                       ('ten minutes to be in the truck', 'they must be ready within minutes', 'volunteering'),
                                                                                       ('he is an unpaid volunteer', 'they are unpaid and have other jobs', 'volunteering')], ('hikers’ mistakes', 'what volunteering involves')),
  fo=[('called out 212 times in eleven years', 'fact'), ('I have never been so tired or so happy', 'opinion'), ('by day he teaches mathematics', 'fact')],
  view=('admiring and respectful of Sipho', [('he still keeps his boots by the front door', 'shows dedication'), ('he shrugs', 'presents him as modest')]),
  role=('Imagine you are one of the two teenagers who were rescued. You write a letter of thanks to Sipho.', ['what happened on the night you were lost', 'how you felt when the team found you', 'what you have learned and will do differently'],
        [('thick cloud', 'lost in thick cloud', 'fear and disorientation; perhaps set off too late'),
         ('at dawn', 'found at dawn', 'relief and gratitude after a long, cold night'),
         ('unpaid volunteer', 'learning he is unpaid', 'deeper gratitude that he gave his night freely'),
         ('paying it back', 'his reason for volunteering', 'a wish to pay the kindness forward too')],
        'Dear Mr Ndlovu, I am not sure you will remember me — you have helped so many people — but I will never forget the moment your torch found us in the cloud…'))

P(title='Should Homework Be Banned?', kind='opinion article', fam='persuasive', cat='nonfiction',
  audience='parents and teachers reading a newspaper', purpose='to persuade readers to take action', pshort='to persuade',
  gist='The writer argues not for banning homework but for setting less, better homework, using research and emotive language.',
  text='Every evening, in millions of homes, the same battle is fought over the kitchen table. Parents nag, children sulk, and a worksheet on fractions somehow takes two hours. It is time we asked whether homework is worth the misery. The evidence is far less clear than many teachers assume. Research suggests that for primary pupils homework makes little difference to achievement, while for older students modest amounts — around an hour a night — can help. Beyond that, the benefits fall away and stress rises. Yet many teenagers report three or more hours a night, squeezed in between sport, chores and part-time jobs. I am not arguing for banning homework altogether. Reading for pleasure, practising a musical instrument or revising for a test are valuable habits. What I object to is busywork: tasks set because a timetable says so, not because anyone will learn from them. Schools should set less homework, set it better and, above all, explain why it matters. Our children’s evenings are not an extension of the school day.',
  facts=[('around an hour a night', 'According to the research, how much homework can help older students?', 'Around an hour a night.', ['Three or more hours a night', 'Two hours a week', 'None at all']),
         ('three or more hours a night', 'How much homework do many teenagers report doing?', 'Three or more hours a night.', ['Around an hour a night', 'Two hours a week', 'Thirty minutes a night']),
         ('somehow takes two hours', 'How long does the worksheet on fractions take?', 'Two hours.', ['Twenty minutes', 'One hour', 'Three hours'])],
  infer=[('Parents nag, children sulk', 'What impression does this create of homework time at home?', 'It is tense and unhappy, a regular source of conflict within families.', ['It is a calm, enjoyable family time.', 'Parents and children rarely talk.', 'Children enjoy working with their parents.'], '‘nag’ and ‘sulk’ suggest irritation on both sides'),
         ('I am not arguing for banning homework altogether.', 'Why does the writer include this sentence?', 'To appear reasonable and avoid seeming extreme, which makes the argument more persuasive to teachers and parents.', ['To change sides in the argument.', 'To show the writer is confused.', 'To agree that homework should be banned.'], 'it is a concession before the main proposal')],
  vocab=[('busywork', 'tasks that keep people occupied without any real purpose', ['challenging project work', 'paid part-time work', 'housework'], 'it is defined as tasks set ‘not because anyone will learn from them’'),
         ('modest', 'moderate; not large', ['huge', 'boastful', 'compulsory'], 'it is explained as ‘around an hour a night’')],
  phrase=[('the benefits fall away', 'the advantages disappear'),
          ('an extension of the school day', 'simply more school time')],
  effects=[('battle', 'conflict and hostility', '‘Battle’ turns homework into a war fought nightly, exaggerating the conflict to make readers feel its emotional cost.', 'discussion'),
           ('misery', 'deep unhappiness', '‘Misery’ is strongly emotive; it suggests homework causes real suffering, pushing readers to question it.', 'effort'),
           ('squeezed', 'pressure and lack of time', '‘Squeezed’ suggests homework is forced into too small a space between other duties, conveying pressure on teenagers’ time.', 'done')],
  figs=[('the same battle is fought over the kitchen table', 'metaphor', 'the metaphor presents homework as warfare in ordinary homes, making the problem seem widespread and destructive.')],
  struct=[('I am not arguing for banning homework altogether.', 'contrast', 'the concession turns the argument, distinguishing valuable homework from ‘busywork’ and making the writer seem fair.', []),
          ('set less homework, set it better and, above all, explain why it matters', 'list of three', 'the list of three builds to the most important demand, flagged by ‘above all’.', ['repetition']),
          ('Every evening, in millions of homes, the same battle is fought over the kitchen table.', 'opening hook', 'opening with a familiar domestic scene draws parents in by making the problem universal.', [])],
  summary=('the writer’s arguments against too much homework and the changes proposed', [('makes little difference to achievement', 'it barely helps younger pupils', 'arguments'),
                                                                                         ('the benefits fall away and stress rises', 'beyond an hour it adds stress without benefit', 'arguments'),
                                                                                         ('three or more hours a night', 'teenagers have far too much', 'arguments'),
                                                                                         ('What I object to is busywork', 'much of it is pointless busywork', 'arguments'),
                                                                                         ('Schools should set less homework', 'schools should set less', 'changes'),
                                                                                         ('explain why it matters', 'schools should explain its purpose', 'changes')], ('arguments', 'proposals')),
  fo=[('many teenagers report three or more hours a night', 'fact'), ('It is time we asked whether homework is worth the misery.', 'opinion'), ('Our children’s evenings are not an extension of the school day.', 'opinion')],
  view=('critical of excessive, pointless homework but not of all homework', [('The evidence is far less clear', 'uses research to challenge assumptions'), ('I am not arguing for banning', 'measured position'), ('the same battle', 'emotive language')]),
  role=('Imagine you are a teacher who disagrees with the writer. You write an article for the same newspaper in reply.', ['which of the writer’s points you accept', 'which points you challenge and why', 'what good homework looks like'],
        [('can help', 'research that modest homework helps', 'agree on quantity; argue for quality'),
         ('battle', 'the emotive picture of family conflict', 'challenge it as exaggerated'),
         ('busywork', 'busywork', 'agree pointless tasks should go; defend practice and revision'),
         ('explain why it matters', 'explaining purpose', 'teachers can explain; parents can support routines')],
        'Last week your columnist described homework as a nightly battle. As a teacher of twenty years, I recognise the picture — but I do not accept the conclusion…'))

P(title='Flood Recovery in the River District', kind='news article', fam='informative', cat='nonfiction',
  audience='readers of a regional newspaper', purpose='to report news events', pshort='to inform',
  gist='Three months after a flood, some homes and the bridge are repaired, but the school and many shops remain closed.',
  text='Three months after the River Kali burst its banks, recovery in the River District is uneven. Of the 1,400 homes flooded, around 900 have been repaired and reoccupied. The remaining families are still living with relatives or in temporary housing at the sports centre. The main road bridge, which was closed after cracks were found in its supports, reopened last week following emergency repairs costing 2.3 million dollars. However, the district’s only secondary school remains shut, and around 600 students are being taught in shifts at a primary school four kilometres away. Local businesses have been hit hard. A survey by the traders’ association found that one in five shops has not reopened, and many owners say their insurance did not cover flood damage. Engineers have recommended raising the flood wall by one metre and restoring wetlands upstream to slow the water in future. The regional government says it will publish its decision by the end of the year.',
  facts=[('around 900 have been repaired', 'How many flooded homes have been repaired and reoccupied?', 'Around 900.', ['1,400', '500', '600']),
         ('costing 2.3 million dollars', 'How much did the emergency bridge repairs cost?', '2.3 million dollars.', ['3.2 million dollars', '23 million dollars', '2.3 thousand dollars']),
         ('around 600 students are being taught in shifts', 'How many secondary students are being taught in shifts?', 'Around 600.', ['Around 900', 'Around 1,400', 'Around 60']),
         ('one in five shops has not reopened', 'What proportion of shops has not reopened?', 'One in five.', ['One in two', 'Four in five', 'One in fifty'])],
  infer=[('The regional government says it will publish its decision by the end of the year.', 'What might the writer imply by ending the report with this sentence?', 'That long-term flood protection is still uncertain and decisions are slow, leaving residents at risk.', ['That the problem has been completely solved.', 'That the government has already built the wall.', 'That nobody cares about the flood.'], 'it ends on an unresolved future decision'),
         ('many owners say their insurance did not cover flood damage', 'What does this suggest about why some shops have not reopened?', 'The owners cannot afford the repairs without insurance money.', ['The owners have retired.', 'The shops were never damaged.', 'Customers have moved to a new town.'], 'no insurance payout means no money for repairs')],
  vocab=[('uneven', 'not the same everywhere; better in some places than others', ['finished', 'impossible', 'very fast'], 'some homes are repaired while the school ‘remains shut’'),
         ('reoccupied', 'lived in again', ['sold', 'demolished', 'abandoned'], 'families have returned to repaired homes'),
         ('upstream', 'further up a river, towards its source', ['under the bridge', 'in the town centre', 'at the sea'], 'wetlands there would ‘slow the water’ before it arrives')],
  phrase=[('burst its banks', 'overflowed and flooded the land around it'),
          ('hit hard', 'badly affected')],
  struct=[('However, the district’s only secondary school remains shut', 'discourse marker', '‘However’ turns from progress to problems, structuring the report as a balance of good and bad news.', []),
          ('Three months after the River Kali burst its banks, recovery in the River District is uneven.', 'opening hook', 'the opening sentence summarises the whole story — time, event and the key judgement ‘uneven’.', [])],
  summary=('the progress made since the flood and the problems that remain', [('around 900 have been repaired', 'about 900 homes repaired and lived in again', 'progress'),
                                                                             ('reopened last week', 'the main bridge has reopened', 'progress'),
                                                                             ('still living with relatives or in temporary housing', 'hundreds of families still displaced', 'problems'),
                                                                             ('only secondary school remains shut', 'the secondary school is still closed', 'problems'),
                                                                             ('taught in shifts', 'students taught in shifts far away', 'problems'),
                                                                             ('one in five shops has not reopened', 'a fifth of shops still shut', 'problems')], ('progress', 'problems')),
  fo=[('Of the 1,400 homes flooded, around 900 have been repaired', 'fact'), ('recovery in the River District is uneven', 'opinion'), ('reopened last week following emergency repairs', 'fact')],
  view=('largely neutral and factual, with a quiet note of concern', [('uneven', 'a judgement summarising mixed progress'), ('hit hard', 'sympathy for businesses'), ('by the end of the year', 'ends on uncertainty')]),
  role=('Imagine you are one of the students being taught in shifts. You write a letter to the regional government.', ['how the flood and school closure have affected you', 'what daily life is like now', 'what you want the government to decide and why'],
        [('taught in shifts', 'lessons in shifts', 'less teaching time; exam worries'),
         ('four kilometres away', 'travelling four kilometres', 'long journeys, cost and tiredness'),
         ('temporary housing at the sports centre', 'families in temporary housing', 'no quiet place to study'),
         ('raising the flood wall', 'engineers’ recommendations', 'urge a quick decision so it never happens again')],
        'Dear Minister, my name is Amara and I am in Year 10 at River District Secondary School — or I was, until the River Kali came through our classrooms three months ago…'))

P(title='The Lighthouse Keeper’s Last Winter', kind='biography', fam='personal', cat='lnf',
  audience='general readers of a local history collection', purpose='to recount and reflect on a personal experience', pshort='to recount and reflect',
  gist='A tribute to a lighthouse keeper who served for thirty-one years before being replaced by a machine, and never lost her sense of duty.',
  mood='Elena’s dignity and the sadness of her departure',
  text='For thirty-one years, Elena Petrova kept the light at Cape Morrow burning. Every evening she climbed the 117 iron steps of the tower, wound the clockwork that turned the great lens, and wrote the weather in a leather logbook in her small, upright handwriting. In 1998 the lighthouse was automated, and a machine in a grey metal box took over her duties. She was given a clock, a certificate and three weeks to leave. Her final logbook entry survives. Most days she recorded only wind direction and visibility, but on her last night she wrote a single extra line: ‘Light shown. All ships safe. Keeper going home.’ Villagers remember her walking down the cliff path the next morning without looking back, her suitcase in one hand and a geranium in a pot in the other. She lived another nineteen years in a flat overlooking the harbour. Neighbours said she still woke at dusk, every evening, and stood at the window until she saw the beam.',
  facts=[('the 117 iron steps', 'How many steps did Elena climb each evening?', '117.', ['31', '19', '98']),
         ('In 1998 the lighthouse was automated', 'In which year was the lighthouse automated?', '1998.', ['1989', '2017', '1931']),
         ('three weeks to leave', 'How long was Elena given to leave?', 'Three weeks.', ['Three months', 'Thirty-one days', 'One night']),
         ('another nineteen years', 'How long did Elena live after leaving the lighthouse?', 'Nineteen years.', ['Thirty-one years', 'Nine years', 'Three years'])],
  infer=[('without looking back', 'What does ‘without looking back’ suggest about how Elena felt when she left?', 'She was dignified and determined not to show her sadness, or to let regret slow her down.', ['She was glad to escape the lighthouse.', 'She was angry with the villagers.', 'She had forgotten something.'], 'thirty-one years of service make indifference unlikely; she is controlling her emotion'),
         ('stood at the window until she saw the beam', 'What does this suggest about Elena after she retired?', 'Her sense of duty and her bond with the lighthouse never left her.', ['She was afraid of the dark.', 'She disliked her new flat.', 'She wanted to get her job back.'], 'she repeats her old routine ‘every evening’')],
  vocab=[('automated', 'operated by machines rather than people', ['repainted', 'closed down', 'rebuilt'], 'a ‘machine in a grey metal box took over’'),
         ('visibility', 'how far you can see, depending on the weather', ['the height of the tower', 'the number of ships', 'the brightness of the lamp'], 'it is recorded with ‘wind direction’ as weather information')],
  phrase=[('took over her duties', 'did the work that she used to do'),
          ('kept the light at Cape Morrow burning', 'made sure the lighthouse shone every night')],
  effects=[('grey metal box', 'cold, impersonal replacement', '‘Grey metal box’ is drab and impersonal, contrasting with Elena’s warm, human care and making the replacement seem soulless.', 'new system'),
           ('upright', 'disciplined, principled character', '‘Upright’ describes her handwriting but also suggests an honest, disciplined personality.', 'neat')],
  figs=[('a machine in a grey metal box took over her duties', 'visual imagery', 'the dull grey box is a bleak image that makes thirty-one years of human care seem replaced by something lifeless.')],
  struct=[('Light shown. All ships safe. Keeper going home.', 'minor sentence', 'the clipped, verbless phrases mimic a log entry, yet ‘going home’ carries quiet emotion, so the restraint makes it moving.', ['short sentence', 'list of three', 'direct speech']),
          ('She was given a clock, a certificate and three weeks to leave.', 'list of three', 'the list builds to the blunt ‘three weeks to leave’, emphasising how meagre and cold her reward was.', []),
          ('stood at the window until she saw the beam', 'ending / closing line', 'the ending returns to the light, showing that her sense of duty outlived her job.', [])],
  summary=('Elena’s duties as keeper and how her working life ended', [('climbed the 117 iron steps', 'climbed the tower every evening', 'duties'),
                                                                     ('wound the clockwork', 'wound the clockwork that turned the lens', 'duties'),
                                                                     ('wrote the weather in a leather logbook', 'recorded the weather in a logbook', 'duties'),
                                                                     ('the lighthouse was automated', 'the lighthouse was automated in 1998', 'ending'),
                                                                     ('a clock, a certificate', 'she received a clock and certificate', 'ending'),
                                                                     ('three weeks to leave', 'she had only three weeks to leave', 'ending')], ('duties', 'how it ended')),
  fo=[('In 1998 the lighthouse was automated', 'fact'), ('She lived another nineteen years', 'fact')],
  view=('admiring and sympathetic towards Elena; quietly critical of how she was treated', [('three weeks to leave', 'a cold farewell'), ('small, upright handwriting', 'respect for her character')]),
  role=('Imagine you are one of Elena’s neighbours. You give a short speech at the unveiling of a plaque in her memory.', ['her work at the lighthouse', 'how she left and how she lived afterwards', 'why the village should remember her'],
        [('thirty-one years', 'thirty-one years of service', 'loyalty and reliability; ships kept safe'),
         ('All ships safe', 'her final logbook line', 'quiet pride; her work mattered'),
         ('without looking back', 'leaving with dignity', 'strength of character'),
         ('until she saw the beam', 'watching the beam from her flat', 'a lifelong bond with the light and the sea')],
        'Friends and neighbours, every evening for nineteen years I saw a light come on in the window above the harbour, a few minutes before the lighthouse beam. That was Elena…'))

P(title='The Power Cut', kind='short story', fam='fiction', cat='fiction',
  audience='general readers of fiction', purpose='to entertain readers with a story', pshort='to entertain',
  gist='During an evening power cut a family gathers by candlelight and rediscovers each other.',
  mood='the strange darkness and the family’s closeness',
  text='The lights died at 7.14, halfway through dinner. For a moment nobody moved. Then my little sister laughed, a high nervous sound, and Dad’s chair scraped back as he went to find the torch he swore was in the drawer by the sink. It was not. Outside, the whole street had vanished; even the streetlamps were blind. I had never seen our neighbourhood so dark. Without the hum of the fridge and the murmur of the television, the house seemed to hold its breath. We found three candles in the end, stubby and half-melted from someone’s birthday cake, and set them in a saucer in the middle of the table. In their wobbling light my parents’ faces looked younger, softer. Mum told a story about a storm in her village when she was a girl, a story I had never heard before. Nobody reached for a phone. When the power returned at 9.02, flooding the room with harsh white light, I was almost disappointed.',
  facts=[('The lights died at 7.14', 'At what time did the power cut begin?', '7.14.', ['9.02', '7.40', 'Midnight']),
         ('We found three candles', 'How many candles did the family find?', 'Three.', ['Two', 'Five', 'One']),
         ('the power returned at 9.02', 'When did the power return?', '9.02.', ['7.14', '9.20', 'The next morning']),
         ('set them in a saucer', 'Where did they put the candles?', 'In a saucer in the middle of the table.', ['On the windowsill', 'In the drawer by the sink', 'On the birthday cake'])],
  infer=[('I was almost disappointed', 'What does this suggest about the narrator’s feelings about the power cut?', 'The narrator enjoyed the closeness and calm it brought and was sorry to see it end.', ['The narrator was frightened throughout.', 'The narrator was bored without the television.', 'The narrator was angry with Dad.'], '‘almost disappointed’ when normal life returned'),
         ('the torch he swore was in the drawer', 'What does this detail suggest about Dad?', 'He is confident but wrong; it gently mocks him and adds humour.', ['He is organised and always prepared.', 'He hid the torch on purpose.', 'He is frightened of the dark.'], '‘It was not.’ follows immediately')],
  vocab=[('stubby', 'short and thick', ['tall and elegant', 'brightly coloured', 'brand new'], 'they are ‘half-melted’ leftovers from a cake'),
         ('wobbling', 'moving unsteadily from side to side', ['completely still', 'very bright', 'quickly fading'], 'candlelight flickers and moves')],
  phrase=[('even the streetlamps were blind', 'not even the streetlights were working'),
          ('Nobody reached for a phone', 'nobody used their phone')],
  effects=[('died', 'sudden, final ending', '‘Died’ makes the power cut sound sudden and final, as if the house itself has lost its life.', 'went out'),
           ('harsh', 'unwelcome, glaring intrusion', '‘Harsh’ makes the returning electric light feel unpleasant and intrusive, unlike the gentle candlelight.', 'bright'),
           ('flooding', 'overwhelming rush', '‘Flooding’ suggests the light rushes in and overwhelms the room, washing away the intimate mood.', 'filling')],
  figs=[('the house seemed to hold its breath', 'personification', 'the house becomes a living thing holding its breath, creating suspense and a hushed, expectant silence.'),
        ('even the streetlamps were blind', 'personification', 'describing the lamps as ‘blind’ gives them human eyes, emphasising the total darkness.')],
  struct=[('It was not.', 'short sentence', 'the three-word sentence undercuts Dad’s confidence, creating humour through anticlimax.', []),
          ('The lights died at 7.14, halfway through dinner.', 'opening hook', 'the story begins at the moment of disruption, with a precise time that is echoed at the end (9.02), framing the episode.', []),
          ('When the power returned at 9.02', 'ending / closing line', 'the closing time frames the episode; ‘almost disappointed’ reveals how much it meant.', [])],
  role=('Imagine you are Mum. Later that night you write a diary entry about the power cut.', ['what happened when the lights went out', 'what the evening by candlelight was like', 'your thoughts about family life'],
        [('Dad’s chair scraped back', 'Dad searching for the torch', 'affectionate amusement at his confidence'),
         ('three candles', 'the birthday-cake candles', 'making do; memories of the birthday'),
         ('a story about a storm in her village', 'telling the storm story', 'surprise that her children had never heard it; memories of childhood'),
         ('Nobody reached for a phone', 'no phones', 'wish for more evenings like this')],
        'What an evening. At quarter past seven the lights went, and for two hours we were a family from my mother’s time: four faces round three stubby candles…'))

P(title='Street Food Fridays', kind='blog', fam='personal', cat='nonfiction',
  audience='readers of a food and travel blog', purpose='to recount and reflect on a personal experience', pshort='to recount and reflect',
  gist='A food blogger celebrates a weekly street-food market in Colombo, while admitting its litter problem.',
  mood='the writer’s enthusiasm for the market',
  text='Every Friday at six, the car park behind Colombo’s old railway station turns into the best restaurant in the city. No tables, no menus, no reservations — just thirty-odd stalls, a few strings of coloured bulbs and a crowd that grows until you can barely move. My first stop is always Ravi’s kottu stall, where two flat-topped grills clatter like a drum band as he chops roti, egg and vegetables together with a pair of steel blades. A plate costs less than a bus ticket. Next, I queue for hoppers: crisp, bowl-shaped pancakes with a soft egg at the centre. I have burned my fingers on them every single week and I regret nothing. Not everything is perfect. There are not enough bins, and by nine the ground is littered with paper plates. But the council has promised more bins from next month, and the traders now run a tidy-up rota. Come hungry, bring cash, and wear shoes you don’t mind ruining.',
  facts=[('Every Friday at six', 'When does the market open?', 'Every Friday at six.', ['Every Saturday at nine', 'Every evening at six', 'Every Friday at nine']),
         ('just thirty-odd stalls', 'About how many stalls are there?', 'About thirty.', ['About three', 'About three hundred', 'About thirteen']),
         ('A plate costs less than a bus ticket.', 'How does the writer describe the price of Ravi’s kottu?', 'A plate costs less than a bus ticket.', ['It costs more than a restaurant meal.', 'It is free on Fridays.', 'It costs the same as a taxi.']),
         ('more bins from next month', 'What has the council promised?', 'More bins from next month.', ['A new car park', 'Tables and menus', 'A ban on paper plates'])],
  infer=[('I have burned my fingers on them every single week and I regret nothing', 'What does this suggest about the writer’s feelings about hoppers?', 'They love them so much that the pain is worth it; it shows enthusiasm and humour.', ['They want the stall to cool the hoppers.', 'They will stop buying hoppers.', 'They are complaining about the stallholder.'], '‘I regret nothing’ shows the pleasure outweighs the pain'),
         ('wear shoes you don’t mind ruining', 'What does this advice suggest about the market at the end of the evening?', 'It gets messy and dirty underfoot, probably because of litter and spilt food.', ['It has a strict dress code.', 'It is held on a beach.', 'It is very formal.'], 'the ground is ‘littered with paper plates’ by nine')],
  vocab=[('reservations', 'bookings made in advance for a table', ['complaints', 'doubts', 'discounts'], 'listed with ‘tables’ and ‘menus’ as things a restaurant would have'),
         ('rota', 'a schedule showing who does a job and when, in turn', ['a type of flatbread', 'a fine for dropping litter', 'a cleaning machine'], 'the traders take turns to tidy up')],
  phrase=[('the best restaurant in the city', 'the finest place to eat in the whole city'),
          ('wear shoes you don’t mind ruining', 'wear old shoes because they may get dirty or damaged')],
  effects=[('clatter', 'loud, rhythmic, energetic noise', '‘Clatter’ suggests a loud, metallic, rhythmic noise, conveying the energy and showmanship of Ravi’s cooking.', 'sound'),
           ('littered', 'messy neglect', '‘Littered’ suggests rubbish scattered carelessly everywhere, giving an honest, unglamorous picture of the market.', 'covered')],
  figs=[('clatter like a drum band', 'simile', 'comparing the grills to a drum band makes the cooking seem like a lively musical performance.'),
        ('turns into the best restaurant in the city', 'hyperbole', 'the exaggerated claim that a car park is the city’s best restaurant expresses the writer’s enthusiasm and surprises the reader.')],
  struct=[('No tables, no menus, no reservations', 'list of three', 'the repeated ‘no’ lists what is missing, which paradoxically makes the market sound more authentic and exciting.', ['repetition', 'dash / parenthesis']),
          ('Not everything is perfect.', 'short sentence', 'the short sentence signals a turn from praise to criticism, making the blog seem honest and balanced.', []),
          ('Come hungry, bring cash, and wear shoes you don’t mind ruining.', 'imperative', 'the closing imperatives speak directly to readers, giving practical advice with a humorous final twist.', ['list of three', 'ending / closing line'])],
  summary=('what makes Street Food Fridays appealing and the problems it faces', [('a few strings of coloured bulbs', 'a lively, colourful atmosphere', 'appeal'),
                                                                                ('clatter like a drum band', 'cooking is a lively performance', 'appeal'),
                                                                                ('less than a bus ticket', 'food is very cheap', 'appeal'),
                                                                                ('crisp, bowl-shaped pancakes', 'delicious local dishes such as hoppers', 'appeal'),
                                                                                ('a crowd that grows until you can barely move', 'it becomes extremely crowded', 'problems'),
                                                                                ('There are not enough bins', 'there are too few bins, so litter builds up', 'problems')], ('appeal', 'problems')),
  fo=[('Every Friday at six', 'fact'), ('the best restaurant in the city', 'opinion'), ('the traders now run a tidy-up rota', 'fact')],
  view=('enthusiastic but honest about problems', [('the best restaurant in the city', 'enthusiasm'), ('Not everything is perfect.', 'honesty')]),
  role=('Imagine you are a council officer. You write a short report on Street Food Fridays for the council’s planning committee.', ['what the market offers the city', 'the problems that need attention', 'your recommendations'],
        [('thirty-odd stalls', 'the number of stalls and crowds', 'popular; brings visitors and income'),
         ('less than a bus ticket', 'cheap food', 'affordable for residents'),
         ('littered with paper plates', 'litter', 'more bins; reusable plates'),
         ('tidy-up rota', 'the traders’ rota', 'support and formalise the rota')],
        'Report to the Planning Committee: Street Food Fridays, Old Railway Station Car Park. Purpose: to assess the weekly market and recommend action on waste…'))

P(title='The Bus to Kathmandu', kind='travel writing', fam='personal', cat='lnf',
  audience='readers of a travel magazine', purpose='to recount and reflect on a personal experience', pshort='to recount and reflect',
  gist='A traveller endures a crowded, frightening mountain bus journey, softened by the kindness of fellow passengers.',
  mood='the discomfort and danger of the journey',
  text='The bus was supposed to leave at seven. It left at nine, after the driver had finished his tea, his second tea and a long conversation with a man selling oranges. Every seat was taken, and the aisle was soon packed with sacks of rice, a crate of hens and a schoolboy who fell asleep standing up. The road climbed in hairpin bends, and on the outside of each bend there was nothing at all — no barrier, no verge, only a sheer drop to a river that glittered like a thread of tin far below. I gripped the seat in front so hard my knuckles turned white. The woman beside me noticed. Without a word, she broke a piece from her bread and pressed it into my hand, then pointed out of the window at a line of snow peaks that had appeared above the clouds. For a moment I forgot to be afraid. We arrived eleven hours later, stiff, dusty and somehow friends.',
  facts=[('It left at nine', 'At what time did the bus actually leave?', 'Nine o’clock.', ['Seven o’clock', 'Eleven o’clock', 'Midday']),
         ('sacks of rice, a crate of hens', 'What was packed into the aisle?', 'Sacks of rice, a crate of hens and a sleeping schoolboy.', ['Suitcases and bicycles', 'Oranges and tea', 'Goats and baskets of fish']),
         ('We arrived eleven hours later', 'How long did the journey take?', 'Eleven hours.', ['Seven hours', 'Nine hours', 'Two days'])],
  infer=[('after the driver had finished his tea, his second tea', 'What does this suggest about the driver’s attitude to the timetable?', 'He is relaxed and unhurried; timetables matter little to him.', ['He is anxious to leave on time.', 'He is ill.', 'He is waiting for the police.'], 'the list of leisurely activities explains a two-hour delay'),
         ('Without a word, she broke a piece from her bread', 'What does this action suggest about the woman beside the writer?', 'She is kind and perceptive; she sees the writer’s fear and offers comfort without fuss.', ['She is hungry and sharing by mistake.', 'She is annoyed with the writer.', 'She wants to sell the bread.'], '‘The woman beside me noticed’ the white knuckles')],
  vocab=[('hairpin', 'very sharply curved, turning back on itself', ['narrow and straight', 'flat and wide', 'slippery'], 'the road ‘climbed’ in bends like the shape of a hairpin'),
         ('sheer', 'extremely steep, almost vertical', ['gentle', 'grassy', 'shallow'], 'there was ‘nothing at all’ on the outside of the bend')],
  phrase=[('somehow friends', 'friends, in a way that is hard to explain, after sharing the journey'),
          ('I forgot to be afraid', 'for a short time my fear left me')],
  effects=[('packed', 'crushing overcrowding', '‘Packed’ suggests the aisle is filled to bursting, conveying the discomfort and chaos of the bus.', 'filled'),
           ('gripped', 'tense, fearful clinging', '‘Gripped’ suggests a tight, desperate hold, showing the writer’s terror on the mountain road.', 'held')],
  figs=[('a river that glittered like a thread of tin far below', 'simile', 'the river looks as thin as a metal thread, emphasising the terrifying height of the road above it.'),
        ('my knuckles turned white', 'visual imagery', 'the image of white knuckles shows physical tension and fear without stating it.')],
  struct=[('It left at nine', 'short sentence', 'the blunt second sentence undercuts the first, creating humour about the delay.', []),
          ('no barrier, no verge, only a sheer drop', 'list of three', 'the list removes every safety feature one by one, building to the terrifying ‘sheer drop’.', ['repetition', 'dash / parenthesis']),
          ('We arrived eleven hours later, stiff, dusty and somehow friends.', 'ending / closing line', 'the list ends unexpectedly on ‘friends’, shifting the focus from hardship to human connection.', ['list of three'])],
  summary=('the difficulties of the journey and the moments that made it bearable', [('It left at nine', 'the bus left two hours late', 'difficulties'),
                                                                                      ('the aisle was soon packed', 'it was extremely overcrowded', 'difficulties'),
                                                                                      ('only a sheer drop', 'the road ran along terrifying unprotected drops', 'difficulties'),
                                                                                      ('eleven hours later', 'the journey was very long', 'difficulties'),
                                                                                      ('pressed it into my hand', 'a stranger shared her bread', 'comforts'),
                                                                                      ('a line of snow peaks', 'beautiful mountain views', 'comforts')], ('difficulties', 'comforts')),
  fo=[('We arrived eleven hours later', 'fact'), ('somehow friends', 'opinion')],
  view=('humorous about hardship and grateful for kindness', [('his second tea', 'gentle humour'), ('somehow friends', 'warmth towards fellow passengers')]),
  role=('Imagine you are the woman who sat beside the writer. You tell a friend about the journey in a letter.', ['what the bus and the road were like', 'what you noticed about the traveller', 'why you helped and how the journey ended'],
        [('It left at nine', 'the late departure', 'a familiar delay to a local passenger'),
         ('my knuckles turned white', 'the traveller’s fear', 'she noticed the gripping hands'),
         ('broke a piece from her bread', 'sharing bread', 'simple kindness to a frightened stranger'),
         ('a line of snow peaks', 'showing the peaks', 'wanting the visitor to see the beauty, not only the danger')],
        'Dear Sunita, you will laugh, but on the Tuesday bus I shared my bread with a foreigner who was holding the seat in front as if it were a lifeboat…'))

# =========================================================== sanity check on annotations

def _check():
    for p in ALL:
        sents(p)
        for f in p.facts:
            sidx(p, f[0])
        for f in p.infer:
            sidx(p, f[0])
        for v in p.vocab:
            sidx(p, v[0])
        for x in p.phrase:
            sidx(p, x[0])
        for x in p.effects:
            sidx(p, x[0])
        for x in p.figs:
            sidx(p, x[0])
        for x in p.struct:
            sidx(p, x[0])
        if p.summary:
            for x in p.summary[1]:
                sidx(p, x[0])
        for x in p.fo:
            sidx(p, x[0])
        if p.view:
            for x in p.view[1]:
                sidx(p, x[0])
        if p.role:
            for x in p.role[2]:
                sidx(p, x[0])
        n = wc(p.text)
        assert 100 <= n <= 260, (p.title, n)


_check()


# =========================================================== shared tables

STRICT = bool(os.environ.get('QB_STRICT'))


def add(t, C, D, typ=None):
    """Register a template; data gaps (no suitable passage) return None instead of raising."""
    def deco(fn):
        def safe(r, D_):
            try:
                return fn(r, D_)
            except (ValueError, IndexError, KeyError, AttributeError, TypeError, ZeroDivisionError):
                if STRICT:
                    raise
                return None
        safe.__name__ = fn.__name__
        t.add(C, D, typ)(safe)
        return fn
    return deco


def pool(field, cats=None, need=1):
    return [p for p in ALL if len(getattr(p, field) or []) >= need and (cats is None or p.cat in cats)]


SUMP = [p for p in ALL if p.summary]
NARR = ('fiction', 'lnf')
NONF = ('nonfiction',)

SUPER = {'fiction': 'A', 'personal': 'A', 'informative': 'B', 'persuasive': 'B'}
KINDS = sorted({p.kind for p in ALL})
KIND_FEATS = {
    'short story': ['third- or first-person narration of events', 'characters, dialogue and a setting', 'descriptive language and imagery to create mood', 'tension built towards a turning point'],
    'descriptive piece': ['sensory detail (sights, sounds, smells)', 'present-tense description of a place', 'imagery such as similes and personification', 'structure based on shifts in time or focus'],
    'autobiography': ['first-person account of the writer’s own life', 'reflection on feelings and what was learned', 'anecdotes and humour', 'a mix of past events and present reflection'],
    'memoir': ['first-person memories of people and places', 'reflection on what the memory means now', 'vivid sensory details', 'quoted speech of remembered people'],
    'biography': ['third-person account of a real person’s life', 'dates and factual details', 'a reflective, admiring tone', 'selected anecdotes that reveal character'],
    'travel writing': ['first-person account of a journey', 'vivid description of an unfamiliar place', 'reflection on the experience', 'details of local people and customs'],
    'diary': ['a date heading', 'first-person, informal private voice', 'recount of the day’s events', 'personal reflections and worries'],
    'blog': ['informal, chatty first-person voice', 'direct address to readers', 'humour and personal anecdote', 'practical tips or opinions'],
    'news article': ['an opening that summarises who, what, when and where', 'facts and figures', 'quotations from people involved', 'a formal, mostly neutral third-person style'],
    'report': ['a title and subheadings', 'formal, impersonal language', 'statistics and findings', 'numbered or sequenced recommendations'],
    'magazine article': ['an engaging opening hook', 'expert or interviewee quotations', 'informative content with a lively tone', 'a memorable ending'],
    'interview': ['direct quotations from the interviewee', 'background facts about the person', 'a mix of reported and direct speech', 'an admiring or curious tone'],
    'leaflet': ['imperative instructions', 'a friendly welcome', 'short, clear sections of advice', 'a memorable slogan'],
    'speech': ['direct address to the audience (e.g. ‘Friends’)', 'rhetorical devices such as lists of three and repetition', 'short sentences for emphasis', 'a call to action'],
    'letter to a newspaper': ['‘Dear Editor’ and a formal sign-off', 'reference to a previous article', 'a polite but firm argument', 'a proposed solution'],
    'review': ['evaluation of strengths and weaknesses', 'first-person opinion', 'specific details such as prices and waiting times', 'an overall verdict and recommendation'],
    'opinion article': ['a clear viewpoint', 'evidence such as research findings', 'emotive language', 'a concession and counter-argument'],
}
PURPOSES = {'to entertain readers with a story': 1, 'to describe a place and create atmosphere': 1, 'to recount and reflect on a personal experience': 1,
            'to report news events': 2, 'to inform readers about a topic': 2, 'to inform readers about a person': 2, 'to present findings and make recommendations': 2,
            'to persuade readers to take action': 3, 'to evaluate and recommend': 3, 'to give instructions and advice': 3}

DEVICES = ['simile', 'metaphor', 'personification', 'onomatopoeia', 'alliteration', 'hyperbole', 'oxymoron', 'visual imagery']
DEV_CLASH = {'metaphor': {'personification', 'visual imagery', 'hyperbole'}, 'personification': {'metaphor', 'visual imagery'}, 'simile': {'visual imagery'},
             'visual imagery': {'metaphor', 'simile', 'personification'}, 'hyperbole': {'metaphor'}, 'oxymoron': {'personification', 'visual imagery', 'metaphor'},
             'onomatopoeia': {'personification', 'alliteration'}}
DEV_DEF = {
    'simile': 'a comparison using ‘like’ or ‘as’', 'metaphor': 'a comparison that says one thing is another', 'personification': 'giving human qualities to something non-human',
    'onomatopoeia': 'a word that imitates the sound it describes', 'alliteration': 'repetition of the same initial consonant sound in nearby words',
    'hyperbole': 'deliberate exaggeration for effect', 'oxymoron': 'two contradictory ideas placed together', 'visual imagery': 'language that creates a vivid picture in the reader’s mind'}

STYPES_POOL = ['rhetorical question', 'direct speech', 'subheadings', 'dash / parenthesis', 'list of three', 'imperative', 'exclamation', 'discourse marker']

STOP = set('the a an and or but of to in on at by for with from as into that this these those was were is are be been had has have his her their its our my your '
           'he she they it we you i me him them us who which what when where then than there here not no nor so if only just even very more most some any all each '
           'every one two three would could should will can may might must did does do also too about after before over under while within without'.split())


def content_words(sentence, exclude):
    ex = {w.lower() for w in re.findall(r"[A-Za-z’'-]+", exclude)}
    out = []
    for w in re.findall(r"[A-Za-z’'-]+", sentence):
        lw = w.lower().strip('’\'-')
        if len(lw) < 4 or lw in STOP or lw in ex or w[0].isupper() or '’' in w or lw in [o.lower() for o in out]:
            continue
        out.append(w)
    return out


def alliterative(s):
    ws = [w.lower() for w in re.findall(r'[A-Za-z]+', s) if w.lower() not in STOP]
    return any(a[0] == b[0] and a[0] not in 'aeiou' for a, b in zip(ws, ws[1:]))


def struct_has(loc, ftype, also):
    has = {ftype, *also}
    if '?' in loc:
        has.add('rhetorical question')
    if '‘' in loc:
        has.add('direct speech')
    if '—' in loc or '(' in loc:
        has.add('dash / parenthesis')
    if '!' in loc:
        has.add('exclamation')
    if loc.count(',') >= 2:
        has.add('list of three')
    if re.match(r'(However|First|Finally|Then|But|So|Next|Instead|Overall)\b', loc):
        has.add('discourse marker')
    return has


def lead(r, P, what='sentence'):
    return r.choice([f'Read this {what} from {src(P)}:', f'In {src(P)}, the writer writes:', f'Look at this {what}, taken from {src(P)}:',
                     f'The following {what} comes from {src(P)}:'])


def lead_x(r, P):
    return r.choice([f'Read this extract from {src(P)}:', f'Here is part of {src(P)}:', f'The following lines are taken from {src(P)}:', f'Re-read these sentences from {src(P)}:'])


def fact_part(P, f, verb='State'):
    loc, q, a, _ = f
    return lambda r: (q, a, f'{a} [1]')


def infer_part(P, it, m=2):
    loc, q, a, _, ev = it
    return lambda r: (f'{q} Use evidence from the text to support your answer.' if m >= 2 else q,
                      f'{a} Evidence: {Q(loc)} – {ev}.' if m >= 2 else a,
                      (f'1 mark: {low(a)} 1 mark: supporting evidence, e.g. {Q(loc)} ({ev})' + (' 1 mark: developed explanation of how the evidence shows this' if m >= 3 else '') + f' [{m}]') if m >= 2 else f'{a} [1]')


def phrase_part(P, it, m=2):
    ph, own = it
    return lambda r: (f'Explain, using your own words, what the writer means by {Q(ph)}.', cap(own) + '.',
                      f'{cap(own)}; ' + ('1 mark for each clear element of the meaning, in own words; repeating the original words gains no credit' if m >= 2 else 'own words required') + f' [{m}]')


def vocab_part(P, it):
    w, mean, _, clue = it
    return lambda r: (f'Give the meaning of {Q(w)} as it is used in the text.', cap(mean) + '.', f'{cap(mean)} (accept close synonyms that fit the context) [1]')


def effect_part(P, it, m=2):
    ph, sug, ana, plain = it
    return lambda r: (f'Explain the effect of the word {Q(ph)}.', ana,
                      f'1 mark: meaning in context ({sug}); 1 mark: connotation/effect on the reader' + ('; 1 mark: link to the wider impression created' if m >= 3 else '') + f'. Indicative: {ana} [{m}]')


def fig_part(P, it, m=2):
    ph, dev, ana = it
    return lambda r: (f'Identify the technique used in {Q(ph)} and explain its effect.', f'{cap(dev)}: {ana}',
                      f'1 mark: {dev}; ' + ('1 mark' if m == 2 else f'{m - 1} marks') + f' for explaining the effect, e.g. {ana} [{m}]')


def struct_part(P, it, m=2, named=True):
    loc, ft, eff, also = it
    return lambda r: (f'Explain the effect of the {ft} in {Q(loc)}.' if named else f'Explain the effect of this feature in {Q(loc)}.', cap(eff),
                      f'1 mark: identifies how the {ft} works here; ' + ('1 mark' if m == 2 else f'{m - 1} marks') + f' for its effect on pace, emphasis or meaning: {eff} [{m}]')


def level_key(m, task, top, mid, lowb, ind):
    lo_, mi_, hi_ = bands(m)
    return (f'Level-marked out of {m} ({task}). Top band ({hi_}): {top} Middle band ({mi_}): {mid} Lower band ({lo_}): {lowb} Indicative content: {ind}')


def rw_key(m, task, reading_top, ind, split=0.5):
    """Reading + writing split, as for Paper 1 summary and extended response."""
    a = max(1, round(m * split))
    b = m - a
    ra, rb, rc = bands(a)
    wa, wb, wcx = bands(b)
    return (f'Level-marked out of {m} ({task}): Reading {a} marks, Writing {b} marks. '
            f'Reading – top band ({rc}): {reading_top}; middle band ({rb}): relevant ideas with some development or selection; lower band ({ra}): few relevant ideas, often lifted or repeated. '
            f'Writing – top band ({wcx}): fluent, well organised, own words, register and form fully suited to the task; middle band ({wb}): clear and mostly accurate, some own words; lower band ({wa}): lifted phrases, weak organisation or frequent errors. '
            f'Indicative content: {ind}')


MODEL = {
    'Learning to Swim at Forty': 'When the writer finally signed up for lessons at forty, they feared being mocked. Instead they joined a mixed group of nervous adult beginners taught by a young, very patient instructor. For a month they struggled and kept sinking, but one day in March they managed to float. The experience brought joy rather than embarrassment: the writer laughed with delight, and the other learners applauded.',
    'Crossing the Salt Flats': 'The salt flats are unusual first because of how they look: a dazzling white plain stretches to every horizon. In the wet season a film of water reflects the sky like an enormous mirror, while in the dry season the ground splits into neat, salt-edged hexagons. Their atmosphere is just as striking. The silence is total, with no wildlife or wind, and this emptiness can be surprisingly moving.',
    'Turtle Hatchery Diary': 'Much of the volunteers’ work happens on the beach. They patrol before dawn, using red torches so that the turtles are not confused, mark each new nest with a numbered stake and record its GPS position. When a nest is disturbed, they rescue the surviving eggs and rebury them inside the protected enclosure. They also educate visitors by giving talks to school groups.',
    'Town Votes to Close Main Street to Cars': 'Supporters believe that banning cars will reduce pollution, giving children cleaner air, and will draw shoppers back into the town centre. Cafés would also gain space for outdoor seating. However, opponents fear that customers will simply drive to the out-of-town retail park instead, since people cannot easily carry heavy purchases without a car.',
    'Canteen Food Waste Report': 'The survey identified three main causes of waste: portions are too large, food goes cold while students wait in long queues, and many students miss lunch on Fridays to attend sports matches. To tackle this, the report recommends offering a choice of portion size, opening a second serving counter at busy times and donating safe leftover food to the local food bank.',
    'Why I Gave Up My Smartphone for a Month': 'Giving up a smartphone had clear benefits: the writer read more books, slept for longer and had fuller conversations with flatmates. There were also drawbacks. At first the writer constantly felt the urge to check the phone, got lost without a map app and missed a party because the invitation was only online.',
    'The Return of the Urban Beekeeper': 'Urban beekeeping has benefits: rooftop hives can produce plenty of honey, and because city bees feed on a wide variety of plants, their honey often tastes better than country honey. However, experts are concerned that too many hives can leave too little food for wild bees, which are often more important pollinators. Keepers can reduce this risk by limiting hive numbers and planting wildflowers.',
    'Speech to the Youth Climate Forum': 'Concerned that the school’s trees had been lost through small, unnoticed decisions, the eco-club decided to pay attention. They measured temperatures in the playground and found that the shade of the last tree was twelve degrees cooler than the tarmac. They then raised money, contacted the council and planted twenty young trees, so that future pupils would benefit from shade.',
    'Protect Our Night Sky': 'The floodlights stay on until 2 a.m., four hours after the park closes. As a result, the stars are hidden, nearby residents’ sleep is disturbed, migrating birds are confused and public money is wasted. The writer proposes motion-sensor lighting, which would come on only when someone is actually in the park.',
    'Visiting the Coral Reef Responsibly': 'To protect the coral, visitors should never touch or stand on it, should use only reef-safe sun cream and should book trips with licensed guides, whose boats moor rather than anchor on the reef. To protect the animals, they should keep at least three metres from turtles and rays, never chase or feed them, and take all litter, especially plastic bags, home.',
    'Review: The Floating Museum': 'The museum’s strengths include a dramatic, slowly revolving whale skeleton and an exciting interactive room where visitors steer a virtual ship; overall it is bold and imaginative. Its weaknesses are long weekend queues, a dull and cluttered upper deck with labels that are hard to read, and an expensive café.',
    'The Mountain Rescue Volunteer': 'Most rescues result from simple mistakes: hikers start too late, underestimate how fast the weather can change or depend on phones whose batteries run out. Volunteering is demanding. Team members can be called at any hour, must be ready to leave within minutes and receive no pay, fitting the work around other jobs.',
    'Should Homework Be Banned?': 'The writer argues that homework barely helps younger pupils and that, beyond about an hour a night, older students gain little while stress increases. Many teenagers do far more than this, and much of it is pointless busywork. Schools should therefore set less homework, make it more purposeful and explain to students why it matters.',
    'Flood Recovery in the River District': 'Some progress has been made: about 900 of the 1,400 flooded homes are repaired and occupied again, and the main bridge has reopened. However, serious problems remain. Many families are still living with relatives or in temporary housing, the only secondary school is closed, its students are taught in shifts some distance away, and a fifth of shops are still shut.',
    'The Lighthouse Keeper’s Last Winter': 'Each evening Elena climbed the tower, wound the mechanism that turned the lens and recorded the weather in a logbook. Her working life ended abruptly when the lighthouse was automated in 1998: her reward was a clock and a certificate, and she was given only three weeks to move out.',
    'Street Food Fridays': 'The market appeals because of its lively, colourful atmosphere, the theatrical cooking at stalls such as Ravi’s, its very cheap food and delicious local dishes like hoppers. However, it becomes extremely crowded, and with too few bins, litter quickly builds up.',
    'The Bus to Kathmandu': 'The journey was difficult: the bus left two hours late, was severely overcrowded and took eleven hours along a mountain road with frightening, unprotected drops. Two things made it bearable: a kind passenger who shared her bread with the anxious writer, and the beautiful view of snow-covered peaks.',
}
for _p in SUMP:
    assert _p.title in MODEL, _p.title

CONTRAST = {('for', 'against'), ('benefits', 'drawbacks'), ('strengths', 'weaknesses'), ('progress', 'problems'), ('benefits', 'concerns'), ('appeal', 'problems'), ('difficulties', 'comforts'), ('problems', 'solution')}


def groups(P):
    keys = list(dict.fromkeys(x[2] for x in P.summary[1]))
    return list(zip(P.summary[2], keys))


def points(P, group=None):
    return [x for x in P.summary[1] if group is None or x[2] == group]


# sentences that are not summary points but are close enough to the focus to be arguable: never offered as 'irrelevant'
NEAR_REL = {
    'Learning to Swim at Forty': ['stop fighting it', 'dropped spanner', 'Your body wants to float'],
    'Crossing the Salt Flats': ['two pairs of sunglasses', 'Nothing prepares you'],
    'Turtle Hatchery Diary': ['dug up by a dog', 'Some eggs were cracked'],
    'Why I Gave Up My Smartphone for a Month': ['down to thirty-five', 'something had shifted'],
    'The Return of the Urban Beekeeper': ['not all experts are delighted', 'numbers must be managed', 'box of hungry insects'],
    'Speech to the Youth Climate Forum': ['The others were cut down', 'how we lose most things', 'That is how many trees stood'],
    'Protect Our Night Sky': ['watched our night sky disappear', 'not merely a hobby problem'],
    'Visiting the Coral Reef Responsibly': ['ask at the visitor centre', 'fixed moorings', 'living animal'],
    'Review: The Floating Museum': ['refused to leave', 'textbook in a cupboard', 'For the most part', 'bring your own lunch'],
    'The Mountain Rescue Volunteer': ['two teenagers in thick cloud', 'called out 212 times'],
    'Should Homework Be Banned?': ['far less clear', 'Parents nag', 'worth the misery', 'extension of the school day'],
    'Flood Recovery in the River District': ['hit hard'],
    'The Lighthouse Keeper’s Last Winter': ['kept the light at Cape Morrow', 'wind direction and visibility'],
    'Street Food Fridays': ['regret nothing', 'more bins from next month', 'best restaurant in the city', 'wear shoes'],
    'The Bus to Kathmandu': ['knuckles turned white', 'forgot to be afraid', 'supposed to leave at seven'],
}


def nonpoint_sents(P):
    pts = set()
    for x in P.summary[1]:
        i, j = span(P, x[0])
        pts |= set(range(i, j + 1))
    ex = NEAR_REL.get(P.title, [])
    return [s for i, s in enumerate(sents(P)) if i not in pts and wc(s) >= 6 and not any(e in s for e in ex)]


def plist(items):
    return ' '.join(f'({i}) {cap(x)}' + ('' if x.endswith('.') else '.') for i, x in enumerate(items, 1))


# =========================================================== 1 Reading skills and strategies

# ---------------------------------------------------------------- 1.1 skimming and scanning
t11 = topic('Skimming for gist and scanning for specific detail', 'skimming for gist and scanning for specific detail', 'skimming', 'scanning')
t11.fixed('C1', (1, 2), [
    ('What is skimming?', 'Reading quickly to get the overall gist of a text', 'Skimming = fast reading for the general idea, using titles, headings and the first and last sentences of paragraphs.',
     ['Reading every word slowly to analyse language', 'Searching for one specific detail such as a date', 'Reading a text aloud to check fluency']),
    ('What is scanning?', 'Searching a text quickly for a specific piece of information', 'Scanning = looking for particular details (names, numbers, key words) without reading everything.',
     ['Reading the whole text closely for implied meanings', 'Summarising a text in your own words', 'Reading only the conclusion']),
    ('Which parts of a non-fiction text are most useful when skimming for gist?', 'The title, subheadings and the first sentence of each paragraph', 'Headings and topic sentences carry the main ideas.',
     ['Only the last word of each paragraph', 'Every adjective in the text', 'The punctuation marks']),
    ('What does ‘gist’ mean?', 'The general meaning or main point of a text', 'Gist = the overall sense, not the detail.', ['The most difficult word in a text', 'The writer’s name and date', 'A quotation used as evidence']),
    ('A topic sentence is usually', 'the sentence that states the main idea of a paragraph', 'Often the first sentence of a paragraph; reading topic sentences is an efficient way to skim.',
     ['the shortest sentence in the text', 'a sentence containing dialogue', 'the sentence with the most commas']),
    ('When scanning for a number, such as a price, what should your eyes look for?', 'Figures and the key word from the question', 'Scan for the shape of the information (digits, capitals) and the question’s key word.',
     ['Long descriptive sentences', 'Adjectives and adverbs', 'The first word of every line only']),
])
STRAT = [('deciding quickly whether an article is relevant to your project', 'skimming'), ('getting a general idea of a passage before answering any questions', 'skimming'),
         ('finding out in a minute what a leaflet is broadly about', 'skimming'), ('checking the overall argument of a letter before reading it closely', 'skimming'),
         ('identifying the main topic of each paragraph in a long report', 'skimming'),
         ('finding the date of an event in a news report', 'scanning'), ('locating the price of a ticket in a review', 'scanning'), ('finding the name of the person quoted in an article', 'scanning'),
         ('finding how many students took part in a survey', 'scanning'), ('locating a key word from the question in a long passage', 'scanning'), ('finding the time a ferry was due to arrive', 'scanning'),
         ('explaining how a writer’s word choice creates an effect', 'close reading'), ('working out what a character’s action suggests about their feelings', 'close reading'),
         ('analysing the connotations of a metaphor', 'close reading'), ('evaluating how convincing a writer’s argument is', 'close reading')]
STRAT_OPTS = ['skimming', 'scanning', 'close reading', 'reading aloud']


@add(t11, 'C1', (1, 2, 3))
def t11_strategy(r, D):
    task, s = r.choice(STRAT)
    opts, ans = mcq(r, s, [x for x in STRAT_OPTS if x != s])
    stem = r.choice([f'Which reading strategy is most suitable for {task}?', f'A student needs to do the following: {task}. Which strategy should they use?',
                     f'In the exam your task involves {task}. Which reading approach is most efficient?'])
    why = {'skimming': 'skimming gives the general idea quickly', 'scanning': 'scanning locates a specific detail without reading everything',
           'close reading': 'this needs careful, detailed reading of the language, not just locating information'}[s]
    return {'stem': stem, 'options': opts, 'answer': ans, 'key': f'{cap(s)}: {why}.'}


t11.fixed('C2', (2, 3), [
    ('Explain the difference between skimming and scanning, giving an example of when you would use each in Paper 1.', 'Skimming is reading quickly for the overall gist, e.g. a first read of the passage to see what it is about; scanning is searching for a particular detail, e.g. finding a time or number needed for a one-mark question.',
     '1 mark: skimming = gist; 1 mark: scanning = specific detail; up to 1 further mark for appropriate exam examples. [3]'),
    ('Explain why it is useful to skim the whole passage before answering the first question.', 'Skimming first gives an overview of the content, structure and text type, so you know where to look for answers and can understand details in context; it also prevents misreading the purpose.',
     '1 mark: overview / knowing where information is; 1 mark: context helps interpret details or saves time later. [2]'),
    ('Explain why you should underline the key words in a question before scanning the passage.', 'Key words tell you exactly what information is needed (e.g. a reason, a time, a feeling), so you scan for the right detail and do not copy irrelevant material.',
     '1 mark: focuses the search; 1 mark: avoids irrelevant or wrong information. [2]'),
    ('Explain why scanning alone is not enough to answer a question beginning ‘What does this suggest about…?’', 'Scanning finds where the relevant words are, but ‘suggest’ asks for an inference; you must read the surrounding text closely and interpret what is implied.',
     '1 mark: scanning only locates; 1 mark: inference needs close reading of implied meaning. [2]'),
])


@add(t11, 'C2', (1, 2, 3, 4), 'explain')
def t11_gist(r, D):
    P = r.choice(ALL)
    ss = sents(P)
    m = max(2, mk('C2', D))
    stem = r.choice([f'You skim {src(P)}. It begins: {Q(ss[0])} and ends: {Q(ss[-1])} Explain what the gist of the whole text is likely to be, and how these sentences helped you.',
                     f'Here are the first and last sentences of {src(P)}. First: {Q(ss[0])} Last: {Q(ss[-1])} Using only these, explain what you think the text is mainly about.'])
    return {'stem': stem, 'answer': f'{P.gist} The opening sets up the situation/topic and the ending shows its outcome or main message.',
            'key': f'{upto(m)}: 1 mark for a reasonable statement of the gist ({P.gist}); further mark(s) for explaining how the opening and closing sentences signal topic, situation or conclusion.', 'marks': m}


@add(t11, 'C3', (1, 2, 3, 4, 5), 'short')
def t11_scan(r, D):
    P = r.choice(pool('facts', need=2))
    k = 1 if D <= 2 else min(len(P.facts), 2 if D == 3 else 3)
    fs = r.sample(P.facts, k)
    intro = r.choice([f'Scan this extract from {src(P)} to answer the questions.', f'Scan the following lines from {src(P)}.', f'Use scanning to find the answers in this part of {src(P)}.']) + f' “{ext(P, [f[0] for f in fs], pad=D >= 3)}”'
    parts = [fact_part(P, f) for f in fs]
    if D >= 4:
        parts.append(lambda r: ('Identify the type of text this extract comes from.', cap(P.kind) + '.', f'{P.kind} [1]'))
        parts.append(lambda r: ('Name the key word or phrase you scanned for to answer the first question, and explain why it helped.', f'A key word from the question, e.g. {Q(fs[0][0])}, which leads directly to the answer.', 'any appropriate key word linked to the question; 1 mark for the explanation [2]'))
    return compose(r, intro, parts, k=(len(parts),) if D <= 3 else (k + 1, k + 2), type_='short')


@add(t11, 'C4', (2, 3, 4, 5), 'multi_step')
def t11_full(r, D):
    P = r.choice(pool('facts', need=2))
    fs = r.sample(P.facts, 2)
    inf = r.choice(P.infer) if P.infer else None
    parts = [lambda r: ('Skim the text and state its gist in one sentence.', P.gist, f'1 mark: main topic or situation; 1 mark: outcome or main point – {P.gist} [2]'),
             fact_part(P, fs[0]), fact_part(P, fs[1]),
             lambda r: ('Identify the type of text and give two features from the text that helped you identify it while skimming.', f'{cap(P.kind)}: {KIND_FEATS[P.kind][0]}; {KIND_FEATS[P.kind][1]}.', f'1 mark: {P.kind}; 1 mark each for two relevant features with reference to the text [3]')]
    if inf:
        parts.append(lambda r: (f'Explain why you would need to read closely, rather than scan, to answer this question, and then answer it: {inf[1]}',
                                f'It asks for an inference, not a stated fact. {inf[2]}', f'1 mark: recognises it requires inference/implied meaning; 1 mark: {low(inf[2])} 1 mark: evidence, e.g. {Q(inf[0])} [3]'))
    return compose(r, full(P), parts, k=(3, 4, 5) if D >= 4 else (3, 4), type_='multi_step')


# ---------------------------------------------------------------- 1.2 audience, purpose, text type
t12 = topic('Identifying audience, purpose and text type', 'identifying audience, purpose and text type', 'audience purpose')
t12.fixed('C1', (1, 2), [
    ('Which feature is most typical of a news article?', 'An opening sentence that summarises who, what, when and where', 'News articles open with the key facts.', ['A ‘Dear Sir or Madam’ greeting', 'Rhyming lines', 'A list of instructions in the imperative']),
    ('Which feature is most typical of a formal report?', 'Subheadings such as ‘Findings’ and ‘Recommendations’', 'Reports are organised under headings and use impersonal language.', ['Dialogue between characters', 'Slang and abbreviations', 'A dated diary heading']),
    ('Which feature is most typical of a speech?', 'Direct address to the listeners and rhetorical devices', 'Speeches address an audience directly (e.g. ‘Friends’) and use repetition and lists.', ['Footnotes and a bibliography', 'Subheadings and bullet-pointed data', 'A headline and by-line']),
    ('What does ‘audience’ mean when analysing a text?', 'The people the text is written for', 'Audience = intended readers or listeners.', ['The writer of the text', 'The place where the text is set', 'The main character']),
    ('A leaflet tells visitors ‘Never touch the coral.’ What is its main purpose?', 'To instruct and advise', 'Imperatives give instructions/advice.', ['To entertain with a story', 'To report a news event', 'To review a product']),
    ('Which of these most clearly shows that a text is a diary?', 'A date heading and a private first-person voice', 'Diaries are dated and personal.', ['Quotations from experts', 'A star rating', 'Numbered recommendations']),
])


@add(t12, 'C1', (1, 2, 3))
def t12_kind(r, D):
    P = r.choice(ALL)
    ss = sents(P)
    i = 0 if D <= 1 else r.randrange(0, max(1, len(ss) - 2))
    x = ' '.join(ss[i:i + 2])
    other = sorted({p.kind for p in ALL if SUPER[p.fam] != SUPER[P.fam]})
    opts, ans = mcq(r, P.kind, other)
    stem = r.choice([f'Read this extract: “{x}” Which text type is it most likely to come from?', f'“{x}” From which type of text is this extract most likely taken?'])
    return {'stem': stem, 'options': opts, 'answer': ans, 'key': f'{cap(P.kind)}: e.g. {KIND_FEATS[P.kind][0]}; {KIND_FEATS[P.kind][1]}.'}


@add(t12, 'C1', (1, 2, 3))
def t12_purpose(r, D):
    P = r.choice(ALL)
    g = PURPOSES[P.purpose]
    ss = sents(P)
    i = r.randrange(0, max(1, len(ss) - 2))
    x = ' '.join(ss[i:i + 2])
    opts, ans = mcq(r, P.purpose, [k for k, v in PURPOSES.items() if v != g])
    return {'stem': r.choice([f'These lines come from {a_kind(P)}: “{x}” What is the main purpose of the text?', f'What is the main purpose of the text that contains these lines? “{x}”']),
            'options': opts, 'answer': ans, 'key': f'{cap(P.purpose)}: typical of {a_kind(P)} for {P.audience}.'}


@add(t12, 'C2', (1, 2, 3, 4), 'explain')
def t12_ap(r, D):
    P = r.choice(ALL)
    ss = sents(P)
    i = r.randrange(0, max(1, len(ss) - 2))
    x = ' '.join(ss[i:i + 2])
    m = max(2, mk('C2', D))
    feat = r.choice(KIND_FEATS[P.kind])
    return {'stem': r.choice([f'Read these lines from {a_kind(P)}: “{x}” Identify the likely audience and purpose, and explain how one feature of the writing shows this.',
                              f'“{x}” These lines are from {a_kind(P)}. Explain who the text is written for and why, referring to one feature of its style.']),
            'answer': f'Audience: {P.audience}. Purpose: {P.purpose}. Feature: {feat}, which suits this audience and purpose.',
            'key': f'{upto(m)}: 1 mark audience ({P.audience}); 1 mark purpose ({P.purpose}); 1 mark for a relevant feature with brief explanation (e.g. {feat}).', 'marks': m}


@add(t12, 'C3', (1, 2, 3, 4, 5), 'short')
def t12_parts(r, D):
    P = r.choice(ALL)
    ss = sents(P)
    i = r.randrange(0, max(1, len(ss) - 3))
    x = ' '.join(ss[i:i + 3])
    f1, f2 = r.sample(KIND_FEATS[P.kind], 2)
    parts = [lambda r: ('Identify the text type.', cap(P.kind) + '.', f'{P.kind} [1]'),
             lambda r: ('Identify the intended audience.', cap(P.audience) + '.', f'{P.audience} (accept reasonable equivalents) [1]'),
             lambda r: ('State the main purpose of the text.', cap(P.purpose) + '.', f'{P.purpose} [1]'),
             lambda r: ('Give two features typical of this text type, supporting one with a quotation from the extract.', f'{cap(f1)}; {f2}.', f'1 mark per relevant feature; quotation must support the feature [2]'),
             lambda r: ('Explain how the register (level of formality) suits the audience.', f'The register suits {P.audience}: ' + ('formal and impersonal' if P.fam == 'informative' else 'personal and engaging' if SUPER[P.fam] == 'A' else 'direct and persuasive') + '.', 'identifies register; links to audience [2]')]
    return compose(r, f'Read this extract from {src(P)}: “{x}”', parts, k=(2, 3) if D <= 3 else (3, 4), type_='short')


@add(t12, 'C4', (2, 3, 4, 5), 'multi_step')
def t12_compare(r, D):
    A = r.choice(ALL)
    B = r.choice([p for p in ALL if SUPER[p.fam] != SUPER[A.fam]])
    xa = ' '.join(sents(A)[:2])
    xb = ' '.join(sents(B)[:2])
    intro = f'Extract A is from {src(A)}: “{xa}” Extract B is from {src(B)}: “{xb}”'
    parts = [lambda r: ('Identify the text type and purpose of Extract A.', f'{cap(A.kind)}; {A.purpose}.', '1 mark type; 1 mark purpose [2]'),
             lambda r: ('Identify the text type and purpose of Extract B.', f'{cap(B.kind)}; {B.purpose}.', '1 mark type; 1 mark purpose [2]'),
             lambda r: ('Compare how each extract engages its audience, using a short quotation from each.', f'A ({A.audience}) uses {KIND_FEATS[A.kind][0]}; B ({B.audience}) uses {KIND_FEATS[B.kind][0]}.',
                        '1 mark per supported point about each text; 1 mark for a clear comparison [3]'),
             lambda r: ('Suggest which extract would suit a reader looking for factual information, and justify your choice.', ('A' if SUPER[A.fam] == 'B' else 'B') + ': its purpose is to inform/persuade with facts rather than tell a personal story.', 'choice + justification linked to purpose [2]')]
    return compose(r, intro, parts, k=(3, 4), type_='multi_step')


# ---------------------------------------------------------------- 1.3 vocabulary from context
t13 = topic('Working out meaning of unfamiliar vocabulary from context', 'working out meaning of unfamiliar vocabulary from context', 'vocabulary context')
t13.fixed('C1', (1, 2), [
    ('In ‘unpaid’, what does the prefix ‘un-’ mean?', 'not', '‘un-’ = not; unpaid = not paid.', ['again', 'before', 'too much']),
    ('In ‘reoccupied’, what does the prefix ‘re-’ mean?', 'again', '‘re-’ = again; reoccupied = lived in again.', ['not', 'under', 'against']),
    ('In ‘underestimate’, what does ‘under-’ suggest?', 'too little', 'to underestimate = to judge something as smaller or less serious than it is.', ['too much', 'beneath the ground', 'exactly right']),
    ('In ‘overpriced’, what does ‘over-’ suggest?', 'too much', 'overpriced = priced too high.', ['above the building', 'finished', 'not at all']),
    ('What is the best first step when you meet an unfamiliar word in an exam passage?', 'Re-read the sentence and look at the words around it for clues', 'Context clues (synonyms, contrasts, examples) usually reveal meaning.', ['Skip the whole paragraph', 'Guess the first meaning that comes to mind', 'Assume it is a spelling mistake']),
    ('A writer says the soup was ‘bland, not fiery’. What kind of context clue helps you work out ‘bland’?', 'A contrast with an opposite word', '‘not fiery’ signals the opposite meaning.', ['A definition in brackets', 'A list of examples', 'A footnote']),
])


@add(t13, 'C1', (1, 2, 3))
def t13_mcq(r, D):
    P = r.choice(pool('vocab'))
    w, mean, dis, clue = r.choice(P.vocab)
    opts, ans = mcq(r, mean, dis)
    return {'stem': f'{lead(r, P)} {Q(sent(P, w))} What does {Q(w)} most nearly mean here?', 'options': opts, 'answer': ans, 'key': f'{cap(mean)}: {clue}.'}


t13.fixed('C2', (2, 3), [
    ('Explain two strategies you can use to work out the meaning of an unfamiliar word in a passage.', 'Use context: read the words and sentences around it for synonyms, contrasts or examples; use word structure: break it into prefix, root and suffix (e.g. un-paid).',
     '1 mark each for two distinct, explained strategies (context clues; word parts; substitution test; knowledge of related words). [2]'),
    ('Explain why you should test your guessed meaning by substituting it back into the sentence.', 'If the substitute makes sense and keeps the meaning of the sentence, the guess is probably right; if not, the context shows you need a different meaning.',
     '1 mark: substitution checks sense; 1 mark: reveals wrong guesses / multiple meanings. [2]'),
    ('Explain why a dictionary meaning is not always enough in a Paper 1 vocabulary question.', 'Many words have several meanings, and the question asks for the meaning in this context; you must choose the sense that fits the sentence.',
     '1 mark: words have multiple meanings; 1 mark: meaning in context is required. [2]'),
])


@add(t13, 'C2', (1, 2, 3, 4), 'explain')
def t13_clue(r, D):
    P = r.choice(pool('vocab'))
    w, mean, dis, clue = r.choice(P.vocab)
    m = max(2, mk('C2', D))
    return {'stem': r.choice([f'Explain how the context helps you work out the meaning of {Q(w)} in this sentence from {src(P)}: {Q(sent(P, w))}',
                              f'A reader does not know the word {Q(w)}. Using the surrounding words in {Q(sent(P, w))} (from {src(P)}), explain how they could work out what it means.']),
            'answer': f'{Q(w)} means {mean}. Context clue: {clue}.', 'key': f'{upto(m)}: 1 mark for an accurate meaning ({mean}); 1 mark for identifying the clue in the context ({clue}).', 'marks': m}


@add(t13, 'C3', (1, 2, 3, 4, 5), 'short')
def t13_parts(r, D):
    P = r.choice(pool('vocab', need=2))
    vs = P.vocab[:]
    intro = f'{lead_x(r, P)} “{ext(P, [v[0] for v in vs])}”'
    parts = []
    for v in vs:
        parts.append(vocab_part(P, v))
        parts.append((lambda v: lambda r: (f'Identify the clue in the surrounding words that helps you understand {Q(v[0])}.', cap(v[3]) + '.', f'{v[3]} [1]'))(v))
    if D >= 4:
        parts.append((lambda v: lambda r: (f'Suggest a word that could replace {Q(v[0])} without changing the meaning, and explain why it fits.', f'A synonym meaning {v[1]}.', 'synonym that fits the sentence; brief justification [2]'))(vs[0]))
    return compose(r, intro, parts, k=(2, 3) if D <= 3 else (4, 5), type_='short')


@add(t13, 'C4', (2, 3, 4, 5), 'multi_step')
def t13_wrong(r, D):
    P = r.choice(pool('vocab', need=2))
    v1, v2 = r.sample(P.vocab, 2)
    g1, g2 = r.choice(v1[2]), r.choice(v2[2])
    intro = f'In {src(P)}, a student meets two unfamiliar words: {Q(sent(P, v1[0]))} and {Q(sent(P, v2[0]))} The student guesses that {Q(v1[0])} means ‘{g1}’ and {Q(v2[0])} means ‘{g2}’.'
    parts = [lambda r: (f'Using the context, explain why the guess for {Q(v1[0])} is wrong and give the correct meaning.', f'It means {v1[1]}; {v1[3]}, so ‘{g1}’ does not fit.', f'1 mark: correct meaning; 1 mark: explanation using context [2]'),
             lambda r: (f'Using the context, explain why the guess for {Q(v2[0])} is wrong and give the correct meaning.', f'It means {v2[1]}; {v2[3]}, so ‘{g2}’ does not fit.', f'1 mark: correct meaning; 1 mark: explanation using context [2]'),
             lambda r: ('Describe a strategy the student could have used to avoid these mistakes.', 'Substitute the guessed meaning back into the sentence and check it makes sense with the surrounding clues; look for contrasts, examples or synonyms nearby.', 'any valid, explained strategy [2]'),
             lambda r: ('Explain why working out vocabulary in context matters for later questions on the passage.', 'Misunderstanding a key word can lead to wrong inferences and weak analysis of the writer’s effects.', 'link to inference or language questions [1]')]
    return compose(r, intro, parts, k=(3, 4), type_='multi_step')


# ---------------------------------------------------------------- 1.4 annotating and selecting
t14 = topic('Annotating and selecting relevant material from a text', 'annotating and selecting relevant material from a text', 'annotating selecting')
t14.fixed('C1', (1, 2), [
    ('What is the main purpose of annotating a passage in the exam?', 'To mark the material relevant to a specific question so it can be used efficiently', 'Annotation is targeted at the task, not general highlighting.', ['To decorate the passage', 'To copy the passage neatly', 'To count the words in the passage']),
    ('Which annotation is most useful when preparing a summary on ‘the causes of waste’?', 'Underlining each separate cause and numbering it in the margin', 'Numbering separate points helps avoid repetition and count content.', ['Highlighting every sentence', 'Circling all the adjectives', 'Writing ‘good’ next to each paragraph']),
    ('Why should you annotate only what is relevant to the question?', 'Highlighting everything makes it impossible to select the key points', 'Selective annotation keeps the focus.', ['Because examiners mark your annotations', 'Because annotations count towards the word limit', 'Because the passage cannot be read again']),
    ('A margin note such as ‘cause 3 – queues’ is useful because it', 'reduces a detail to a short point in your own words', 'Short own-word labels prepare for summary writing.', ['copies the original wording exactly', 'adds a new idea not in the text', 'shows the writer’s opinion']),
])


@add(t14, 'C1', (1, 2, 3))
def t14_mcq(r, D):
    P = r.choice(SUMP)
    pt = r.choice(points(P))
    ok = sent(P, pt[0])
    bad = [s for s in nonpoint_sents(P) if s != ok]
    opts, ans = mcq(r, ok, bad)
    return {'stem': f'You are annotating {src(P)} for a task on {P.summary[0]}. Which sentence should you underline?', 'options': opts, 'answer': ans,
            'key': f'Relevant: it shows that {pt[1]}.'}


t14.fixed('C2', (2, 3), [
    ('Explain why highlighting almost the whole passage is an ineffective way to annotate.', 'If everything is highlighted, nothing stands out; you still have to reread to find the relevant points, wasting time and risking irrelevant material.',
     '1 mark: loss of focus/nothing stands out; 1 mark: wastes time or leads to irrelevance. [2]'),
    ('Explain how numbering points in the margin helps when answering a question that asks for a set number of ideas.', 'Numbering lets you check you have enough distinct points, avoid repeating the same idea and plan the order of your answer.',
     '1 mark: counting/coverage; 1 mark: avoids repetition or helps ordering. [2]'),
    ('Explain why you should annotate with the question’s focus in mind rather than simply marking interesting language.', 'Different questions need different material; interesting language may be irrelevant to, say, a summary of causes, so annotation must serve the task.',
     '1 mark: task determines relevance; 1 mark: example of irrelevant but interesting material. [2]'),
])


@add(t14, 'C2', (1, 2, 3, 4), 'explain')
def t14_why(r, D):
    P = r.choice(SUMP)
    pt = r.choice(points(P))
    m = max(2, mk('C2', D))
    return {'stem': r.choice([f'Explain why this sentence from {src(P)} should be annotated for a task on {P.summary[0]}, and write a brief margin note for it: {Q(sent(P, pt[0]))}',
                              f'A student underlines {Q(sent(P, pt[0]))} in {src(P)} when preparing to write about {P.summary[0]}. Explain why this is a good choice and suggest a short margin label.']),
            'answer': f'It is relevant because it shows that {pt[1]}. Margin note: “{pt[1]}”.', 'key': f'{upto(m)}: 1 mark: links the sentence to the focus ({P.summary[0]}); 1 mark: concise own-words note, e.g. “{pt[1]}”.', 'marks': m}


def chunk(r, P, D):
    ss = sents(P)
    n = min(len(ss), 3 + D // 2 + r.randint(0, 1))
    for _ in range(10):
        i = r.randint(0, len(ss) - n)
        ids = set(range(i, i + n))
        got = [x for x in points(P) if span(P, x[0])[0] in ids]
        if len(got) >= 2:
            return ' '.join(ss[i:i + n]), got
    return None, None


@add(t14, 'C3', (1, 2, 3, 4, 5), 'short')
def t14_select(r, D):
    P = r.choice(SUMP)
    x, got = chunk(r, P, D)
    if not x:
        return None
    m = len(got) + (1 if D >= 4 else 0)
    extra = ' Then group your points under two headings.' if D >= 4 else ''
    return {'stem': f'Annotate this extract from {src(P)} for a task on {P.summary[0]}. List each relevant point in a short note of your own.{extra} “{x}”',
            'answer': '; '.join(cap(g[1]) for g in got) + '.' + (f' Headings: {P.summary[2][0]} / {P.summary[2][1]}.' if D >= 4 else ''),
            'key': f'1 mark per relevant point (max {len(got)}): ' + '; '.join(g[1] for g in got) + ('. 1 mark for sensible grouping.' if D >= 4 else '.') + ' No credit for copied irrelevant detail.', 'marks': m}


@add(t14, 'C4', (2, 3, 4, 5), 'multi_step')
def t14_full(r, D):
    P = r.choice(SUMP)
    n = min(len(points(P)), 3 + D // 2)
    bad = nonpoint_sents(P)
    parts = [lambda r: (f'Select {n} separate details relevant to {P.summary[0]}, writing each as a short note.', '; '.join(cap(x[1]) for x in points(P)) + '.', f'1 mark per relevant, distinct point up to {n} [{n}]'),
             lambda r: (f'Sort the relevant details in the text under two headings: ‘{P.summary[2][0]}’ and ‘{P.summary[2][1]}’.', '; '.join(f'{h}: ' + ', '.join(x[1] for x in points(P, k)) for h, k in groups(P)) + '.', 'accurate grouping [2]')]
    if bad:
        b = r.choice(bad)
        parts.append(lambda r: (f'Explain why you would not annotate this sentence for the task: {Q(b)}', f'It does not give information about {P.summary[0]}; it adds background, description or an example rather than a key point.', '1 mark: not relevant to the focus; 1 mark: explains what kind of material it is [2]'))
    return compose(r, full(P), parts, k=(len(parts),), type_='multi_step')


CHAPTERS[1] = [t11, t12, t13, t14]


# =========================================================== 2 Comprehension (Paper 1 Question 1)

# ---------------------------------------------------------------- 2.1 explicit meaning
t21 = topic('Explicit meaning: retrieving facts and details accurately', 'explicit meaning: retrieving facts and details accurately', 'explicit meaning retrieving')
t21.fixed('C1', (1, 2), [
    ('A question asks you to ‘Identify’ a detail from the passage. What does the examiner expect?', 'A brief, accurate detail taken from the text', '‘Identify’ = pick out; no explanation needed.', ['A long explanation of the writer’s feelings', 'Your own opinion on the topic', 'An analysis of language']),
    ('A one-mark question asks ‘When did the ferry leave?’ Which answer is best?', 'At nine, an hour late', 'Precise and relevant.', ['The ferry left the harbour at nine, an hour late, because the captain refused to cast off until the last van had rattled up the ramp', 'Late', 'In the evening, I think, when it was foggy and Mira was nervous']),
    ('Which of these is the most common reason for losing marks on retrieval questions?', 'Copying too much text so that the correct detail is buried among wrong details', 'Over-copying can include incorrect material that cancels the answer.', ['Writing in pen', 'Answering in a complete sentence', 'Using the exact name from the text']),
    ('Explicit information is', 'stated directly in the text', 'Explicit = stated; implicit = suggested.', ['hinted at but never stated', 'the reader’s own opinion', 'only found in the title']),
])


@add(t21, 'C1', (1, 2, 3))
def t21_mcq(r, D):
    P = r.choice(pool('facts'))
    loc, q, a, dis = r.choice(P.facts)
    opts, ans = mcq(r, a, dis)
    return {'stem': f'{lead(r, P)} {Q(sent(P, loc))} {q}', 'options': opts, 'answer': ans, 'key': f'{a} The detail is stated explicitly in the sentence.'}


t21.fixed('C2', (2, 3), [
    ('Explain why you should check the line or paragraph reference in a retrieval question before answering.', 'The answer must come from the specified part of the text; a similar detail elsewhere may be wrong or not credited.',
     '1 mark: answers must be located in the given section; 1 mark: details elsewhere may be different or not accepted. [2]'),
    ('Explain why answering a retrieval question in a few precise words can be better than copying a whole sentence.', 'A precise answer shows you have identified exactly what is asked; copying a sentence may include incorrect or irrelevant details that cancel the mark.',
     '1 mark: precision shows understanding; 1 mark: over-copying risks contradiction. [2]'),
])


@add(t21, 'C2', (1, 2, 3, 4), 'explain')
def t21_error(r, D):
    P = r.choice(pool('facts'))
    loc, q, a, dis = r.choice(P.facts)
    wrong = r.choice(dis)
    m = max(2, mk('C2', D))
    return {'stem': f'Question on {src(P)}: “{q}” A student answered: ‘{wrong}’. Using this sentence from the text, explain why the answer is wrong and give the correct answer: {Q(sent(P, loc))}',
            'answer': f'The sentence states that the answer is: {a} The student’s answer is not what the text says (it misreads or confuses the detail).',
            'key': f'{upto(m)}: 1 mark: correct answer ({a}); 1 mark: explains that the text states this explicitly and the student’s answer is not supported.', 'marks': m}


@add(t21, 'C3', (1, 2, 3, 4, 5), 'short')
def t21_parts(r, D):
    P = r.choice(pool('facts', need=2))
    k = min(len(P.facts), 2 + (D >= 3) + (D >= 5))
    fs = r.sample(P.facts, k)
    intro = r.choice([f'Answer the questions using only this extract from {src(P)}.', f'Read this part of {src(P)} and answer the questions that follow.']) + f' “{ext(P, [f[0] for f in fs])}”'
    parts = [fact_part(P, f) for f in fs]
    if D >= 4 and P.phrase:
        parts.append(phrase_part(P, r.choice(P.phrase)))
    return compose(r, intro, parts, k=(len(parts),), type_='short')


@add(t21, 'C4', (2, 3, 4, 5), 'multi_step')
def t21_full(r, D):
    P = r.choice(pool('facts', need=2))
    parts = [fact_part(P, f) for f in P.facts]
    if P.infer:
        parts.append(infer_part(P, P.infer[0], 2))
    if P.phrase:
        parts.append(phrase_part(P, P.phrase[0]))
    return compose(r, full(P) + ' Answer the questions.', parts, k=(4, 5), type_='multi_step')


# ---------------------------------------------------------------- 2.2 implicit meaning
t22 = topic('Implicit meaning: inferring thoughts, feelings and attitudes', 'implicit meaning: inferring thoughts, feelings and attitudes', 'implicit meaning inferring')
t22.fixed('C1', (1, 2), [
    ('What does it mean to ‘infer’ from a text?', 'To work out something that is suggested but not stated directly', 'Inference = reading between the lines using evidence.', ['To copy the main point word for word', 'To count the number of paragraphs', 'To give your own unrelated opinion']),
    ('Which question is asking for an inference?', 'What does his silence suggest about how he feels?', '‘suggest’ signals implied meaning.', ['At what time did he arrive?', 'How many steps are in the tower?', 'Where was the notebook found?']),
    ('A strong inference answer should', 'state the implied meaning and support it with evidence from the text', 'Point + evidence + explanation.', ['retell the story in order', 'use as many quotations as possible without comment', 'avoid referring to the text']),
    ('A character ‘slammed the door without a word’. What is the most likely inference?', 'The character is angry', 'The action implies the feeling.', ['The character is calm and happy', 'The door was broken', 'The character is very polite']),
])


@add(t22, 'C1', (1, 2, 3))
def t22_mcq(r, D):
    P = r.choice(pool('infer'))
    loc, q, a, dis, ev = r.choice(P.infer)
    opts, ans = mcq(r, a, dis)
    return {'stem': f'{lead(r, P)} {Q(sent(P, loc))} {q}', 'options': opts, 'answer': ans, 'key': f'{a} Evidence: {ev}.'}


@add(t22, 'C2', (1, 2, 3, 4), 'explain')
def t22_explain(r, D):
    P = r.choice(pool('infer'))
    loc, q, a, dis, ev = r.choice(P.infer)
    m = max(2, mk('C2', D))
    return {'stem': r.choice([f'{lead(r, P)} {Q(sent(P, loc))} {q} Support your answer with evidence.', f'{q} Refer to this sentence from {src(P)} in your answer: {Q(sent(P, loc))}']),
            'answer': f'{a} Evidence: {Q(loc)} – {ev}.', 'key': f'{upto(m)}: 1 mark: valid inference ({low(a)}); 1 mark: relevant evidence with explanation ({ev}). Answers that only retell the text gain no credit.', 'marks': m}


t22.fixed('C2', (2, 3), [
    ('Explain the difference between explicit and implicit meaning, using an example of your own.', 'Explicit meaning is stated directly (e.g. ‘She was angry’); implicit meaning is suggested (e.g. ‘She slammed the door’ implies anger).',
     '1 mark: explicit = stated; 1 mark: implicit = suggested; 1 mark: apt example. [3]'),
    ('Explain why an inference must be supported by evidence from the text.', 'Without evidence, the answer is just a guess or personal opinion; evidence shows the inference is grounded in what the writer has written.',
     '1 mark: inference must be grounded; 1 mark: evidence shows how the meaning is suggested. [2]'),
])


@add(t22, 'C3', (1, 2, 3, 4, 5), 'short')
def t22_parts(r, D):
    P = r.choice(pool('infer', need=2) if D >= 3 else pool('infer'))
    its = r.sample(P.infer, 2) if len(P.infer) >= 2 else P.infer[:]
    m = 3 if D >= 4 else 2
    intro = f'{lead_x(r, P)} “{ext(P, [i[0] for i in its])}”'
    parts = [infer_part(P, i, m) for i in its]
    if P.facts:
        parts.insert(0, fact_part(P, r.choice(P.facts)))
    return compose(r, intro, parts, k=(len(parts) - 1, len(parts)) if D <= 2 else (len(parts),), type_='short')


@add(t22, 'C4', (2, 3, 4, 5), 'multi_step')
def t22_extended(r, D):
    P = r.choice(pool('infer', need=2))
    m = mk('C4', D)
    focus = r.choice(['thoughts and feelings', 'attitudes', 'state of mind'])
    x = ext(P, [i[0] for i in P.infer], pad=1)
    pts = ' '.join(f'{cap(i[2])} ({Q(i[0])}: {i[4]}).' for i in P.infer)
    return {'stem': f'Read this extract from {src(P)}: “{x}” Explain what the writer suggests about the {focus} of the people in this extract. Support each point with evidence and explain how the evidence suggests it.',
            'answer': pts, 'key': f'{upto(m)}: 1 mark per valid inference (max 2) and 1 mark per supporting quotation with explanation. Indicative: {pts}', 'marks': m, 'type': 'multi_step'}


# ---------------------------------------------------------------- 2.3 own words
t23 = topic('Explaining words and phrases in own words', 'explaining words and phrases in own words', 'own words')
t23.fixed('C1', (1, 2), [
    ('A question says ‘Using your own words, explain…’. Which answer would gain credit?', 'One that rephrases the meaning without repeating the key words of the text', 'Own words = paraphrase; repetition of key words earns nothing.', ['One that copies the phrase in quotation marks', 'One that gives a dictionary page number', 'One that explains how the phrase sounds']),
    ('Why do ‘own words’ questions reward paraphrase?', 'Paraphrase shows you understand the meaning rather than just locating the words', 'It tests understanding (R1).', ['Because quotations are not allowed anywhere in the exam', 'Because shorter answers are always better', 'Because the examiner cannot read quotations']),
    ('Which is the best own-words explanation of ‘burst its banks’?', 'overflowed and flooded the land around it', 'Meaning without repeating ‘burst’ or ‘banks’.', ['burst its banks', 'the banks were burst', 'the river had banks']),
])


@add(t23, 'C1', (1, 2, 3))
def t23_mcq(r, D):
    P = r.choice(pool('vocab'))
    w, mean, dis, clue = r.choice(P.vocab)
    opts, ans = mcq(r, mean, dis)
    return {'stem': f'Which of the following is closest in meaning to {Q(w)} as it is used in this sentence from {src(P)}? {Q(sent(P, w))}', 'options': opts, 'answer': ans, 'key': f'{cap(mean)}: {clue}.'}


@add(t23, 'C2', (1, 2, 3, 4), 'explain')
def t23_explain(r, D):
    P = r.choice(pool('phrase'))
    ph, own = r.choice(P.phrase)
    m = max(2, mk('C2', D))
    return {'stem': r.choice([f'Explain, using your own words, what the writer means by {Q(ph)} in this sentence from {src(P)}: {Q(sent(P, ph))}',
                              f'{lead(r, P)} {Q(sent(P, ph))} Using your own words, explain the meaning of {Q(ph)}.']),
            'answer': cap(own) + '.', 'key': f'{upto(m)}: accurate meaning in own words – {own}. Repeating the key words of the phrase gains no credit.', 'marks': m}


@add(t23, 'C3', (1, 2, 3, 4, 5), 'short')
def t23_parts(r, D):
    P = r.choice(pool('phrase', need=2))
    intro = f'{lead_x(r, P)} “{ext(P, [p[0] for p in P.phrase] + ([P.vocab[0][0]] if P.vocab else []))}” Use your own words in each answer.'
    parts = [phrase_part(P, p) for p in P.phrase]
    if P.vocab:
        parts.append(vocab_part(P, P.vocab[0]))
    return compose(r, intro, parts, k=(2,) if D <= 2 else (len(parts),), type_='short')


@add(t23, 'C4', (2, 3, 4, 5), 'multi_step')
def t23_students(r, D):
    P = r.choice(pool('phrase', need=2))
    (p1, o1), (p2, o2) = r.sample(P.phrase, 2)
    intro = f'In {src(P)}, the writer uses the phrase {Q(p1)}. Two students explained it. Student A wrote: ‘It means that {p1}.’ Student B wrote: ‘{cap(o1)}.’'
    parts = [lambda r: ('Explain which answer would gain credit, and why.', 'Student B: A simply repeats the writer’s words, so shows no understanding; B explains the meaning in their own words.', '1 mark: B; 1 mark: A repeats/lifts the key words [2]'),
             lambda r: (f'Using your own words, explain what the writer means by {Q(p2)}.', cap(o2) + '.', f'{o2} [2]'),
             lambda r: ('Give one piece of advice to Student A for answering ‘own words’ questions.', 'Work out the meaning, then express it with different words (synonyms), keeping the same sense; check no key word from the phrase is repeated.', 'any sensible, specific advice [1]')]
    if P.vocab:
        parts.append(vocab_part(P, P.vocab[0]))
    return compose(r, intro, parts, k=(3, 4), type_='multi_step')


# ---------------------------------------------------------------- 2.4 mark allocation
t24 = topic('Answering short-answer questions to mark allocation', 'answering short-answer questions to mark allocation', 'mark allocation')
t24.fixed('C1', (1, 2), [
    ('A question is followed by [2] and asks ‘Give two reasons…’. How many separate points should your answer contain?', 'Two', 'One mark per distinct reason.', ['One', 'Three', 'As many as possible']),
    ('A 1-mark retrieval question needs', 'one precise detail', 'Keep it short and accurate.', ['a paragraph of explanation', 'two quotations and an analysis', 'a summary of the passage']),
    ('A 3-mark inference question is most likely to reward', 'a point, supporting evidence and a developed explanation', 'Each element earns credit.', ['one word', 'copying the whole paragraph', 'a list of unrelated quotations']),
    ('What is the best guide to how much to write for a short-answer question?', 'The number of marks shown and the space provided', 'Marks signal the number of points expected.', ['The length of the passage', 'The number of questions on the paper', 'How confident you feel']),
])


@add(t24, 'C1', (1, 2, 3))
def t24_count(r, D):
    P = r.choice(pool('infer'))
    if r.random() < 0.5 and P.facts:
        q, n = r.choice(P.facts)[1], 1
    else:
        q, n = r.choice(P.infer)[1] + ' Support your answer with evidence.', r.choice([2, 3])
    words = {1: '1 point (one precise detail)', 2: '2 points (an inference plus supporting evidence)', 3: '3 points (inference, evidence and developed explanation)', 4: '4 points'}
    opts, ans = mcq(r, words[n], [v for k, v in words.items() if k != n])
    return {'stem': f'A question on {src(P)} reads: “{q}” [{n}] How many distinct creditworthy points should a good answer contain?', 'options': opts, 'answer': ans,
            'key': f'{n} mark(s) → {words[n]}.'}


@add(t24, 'C2', (1, 2, 3, 4), 'explain')
def t24_copy(r, D):
    P = r.choice(pool('infer'))
    loc, q, a, dis, ev = r.choice(P.infer)
    m = max(2, mk('C2', D))
    return {'stem': f'Question on {src(P)}: “{q}” [2] A student answered only by copying: {Q(sent(P, loc))} Explain why this would not gain both marks, and write an answer that would.',
            'answer': f'Copying the sentence locates the evidence but does not state the inference or explain it. Better: {a} This is shown by {Q(loc.rstrip("."))}, because {ev}.',
            'key': f'{upto(m)}: 1 mark: copying ≠ explaining the implied meaning; 1 mark: improved answer with inference + evidence ({low(a).rstrip(".")}).', 'marks': m}


@add(t24, 'C3', (1, 2, 3, 4, 5), 'short')
def t24_set(r, D):
    P = r.choice(pool('infer'))
    parts = []
    if P.facts:
        f = r.choice(P.facts)
        parts.append(lambda r: (f'{f[1]} [1]', f[2], f'{f[2]} [1]'))
    i = r.choice(P.infer)
    m = 3 if D >= 4 else 2
    ip = infer_part(P, i, m)
    parts.append(lambda r: (lambda t: (t[0] + f' [{m}]', t[1], t[2]))(ip(r)))
    if P.phrase:
        ph = r.choice(P.phrase)
        pp = phrase_part(P, ph)
        parts.append(lambda r: (lambda t: (t[0] + ' [2]', t[1], t[2]))(pp(r)))
    locs = [i[0]] + ([f[0]] if P.facts else []) + ([ph[0]] if P.phrase else [])
    intro = f'Answer each question about this extract from {src(P)}, making as many points as the marks indicate. “{ext(P, locs)}”'
    return compose(r, intro, parts, k=(2,) if D <= 2 else (len(parts),), type_='short')


@add(t24, 'C4', (2, 3, 4, 5), 'multi_step')
def t24_compare(r, D):
    P = r.choice(pool('infer'))
    loc, q, a, dis, ev = r.choice(P.infer)
    intro = (f'This 3-mark question is about {src(P)}: “{q}” [3] Answer A: ‘{a}’ Answer B: ‘{a} This is shown when the writer says {Q(loc)}, which suggests this because {ev}.’')
    parts = [lambda r: ('Award a mark out of 3 to each answer and justify your decisions.', 'A: 1/3 – a valid inference but no evidence or explanation. B: 3/3 – inference, apt evidence and developed explanation.', '1 mark each for a justified mark for A and B [2]'),
             lambda r: ('Explain what Answer A needs to do to reach full marks.', 'Add a short, relevant quotation and explain how it shows the inference.', 'evidence + explanation [2]'),
             lambda r: ('Explain how the mark allocation should guide the length of an answer in the exam.', 'Roughly one creditworthy point per mark; write enough to cover each mark but no more, to save time for later questions.', 'one point per mark; time management [2]')]
    if P.facts:
        f = r.choice(P.facts)
        parts.append(lambda r: (f'Answer this 1-mark question as concisely as possible: {f[1]}', f[2], f'{f[2]} [1]'))
    return compose(r, intro, parts, k=(3, 4), type_='multi_step')


CHAPTERS[2] = [t21, t22, t23, t24]


# =========================================================== 3 Summary writing (Paper 1 Question 2)

def summary_key(m, P, words):
    return rw_key(m, f'summary of {P.summary[0]}, no more than {words} words',
                  'a wide range of relevant points, clearly selected and expressed concisely',
                  '; '.join(x[1] for x in P.summary[1]) + '. Writing: concise, organised, own words, no examples, quotations or comment.')


# ---------------------------------------------------------------- 3.1 selecting points
t31 = topic('Selecting relevant points for a summary focus', 'selecting relevant points for a summary focus', 'summary relevant points')
t31.fixed('C1', (1, 2), [
    ('In a summary, which of these should usually be left out?', 'Examples, quotations, repetition and your own opinions', 'A summary records the key points only.', ['The main points relevant to the focus', 'Points from the second half of the text', 'Linking words between points']),
    ('What should you do first when you read a summary question?', 'Underline the focus of the question so you know what to select', 'The focus determines relevance.', ['Start writing immediately', 'Count the words in the passage', 'Copy the first paragraph']),
    ('A summary question asks about ‘the problems’ caused by something. A sentence describes how it was invented. This sentence is', 'irrelevant to the focus', 'Background is not a problem.', ['the most important point', 'needed as an introduction', 'a useful quotation to include']),
    ('Why should each summary point be distinct?', 'Repeating the same idea in different words earns no extra credit', 'One mark per distinct point.', ['Because longer summaries score more', 'Because the examiner counts every sentence', 'Because repetition improves style']),
])


@add(t31, 'C1', (1, 2, 3))
def t31_mcq(r, D):
    P = r.choice(SUMP)
    pt = r.choice(points(P))
    ok = sent(P, pt[0])
    opts, ans = mcq(r, ok, [s for s in nonpoint_sents(P) if s != ok])
    return {'stem': f'You are writing a summary of {P.summary[0]}, based on {src(P)}. Which of these sentences contains a relevant point?', 'options': opts, 'answer': ans,
            'key': f'It gives the point that {pt[1]}; the other sentences do not address the focus.'}


@add(t31, 'C2', (1, 2, 3, 4), 'explain')
def t31_two(r, D):
    P = r.choice(SUMP)
    good = r.sample(points(P), 2)
    gs = [sent(P, g[0]) for g in good]
    if gs[0] == gs[1]:
        return None
    bad = [s for s in nonpoint_sents(P) if s not in gs]
    if len(bad) < 2:
        return None
    opts = gs + r.sample(bad, 2)
    r.shuffle(opts)
    lab = 'ABCD'
    right = [lab[opts.index(g)] for g in gs]
    m = max(2, mk('C2', D))
    stem = f'Which two of these sentences from {src(P)} contain points relevant to a summary of {P.summary[0]}? Explain your choice briefly. ' + ' '.join(f'{lab[i]}: {Q(o)}' for i, o in enumerate(opts))
    return {'stem': stem, 'answer': f'{right[0]} and {right[1]}: they show that {good[0][1]} and that {good[1][1]}. The others give background or description, not points about the focus.',
            'key': f'{upto(m)}: 1 mark for identifying both {right[0]} and {right[1]}; 1 mark for explaining their relevance to {P.summary[0]}.', 'marks': m}


t31.fixed('C2', (2, 3), [
    ('Explain why a summary should not include the writer’s examples or quotations.', 'Examples and quotations illustrate a point but are not points themselves; including them wastes words and suggests lifting rather than selecting.',
     '1 mark: they illustrate rather than add new points; 1 mark: waste words within the limit / show lifting. [2]'),
    ('Explain how you can check that a point is relevant to the summary focus.', 'Ask whether it directly answers the focus question (e.g. is it a cause? a benefit?); if it only sets the scene or gives opinion, leave it out.',
     '1 mark: test against the focus; 1 mark: identify background/opinion as irrelevant. [2]'),
])


@add(t31, 'C3', (1, 2, 3, 4, 5), 'short')
def t31_list(r, D):
    P = r.choice(SUMP)
    x, got = chunk(r, P, D + 1)
    if not x:
        return None
    return {'stem': r.choice([f'List the points in this extract from {src(P)} that are relevant to a summary of {P.summary[0]}. Write each point in your own words. “{x}”',
                              f'From this part of {src(P)}, select the points you would include in a summary of {P.summary[0]}. Use your own words. “{x}”']),
            'answer': '; '.join(cap(g[1]) for g in got) + '.', 'key': f'1 mark per relevant point in own words (max {len(got)}): ' + '; '.join(g[1] for g in got) + '. Do not credit lifted or irrelevant material.', 'marks': len(got)}


@add(t31, 'C4', (2, 3, 4, 5), 'long')
def t31_summary(r, D):
    P = r.choice(SUMP)
    words = {2: 80, 3: 100, 4: 120, 5: 120}.get(D, 80)
    m = mk('C4', D, 'long')
    return {'stem': f'{full(P)} Write a summary of {P.summary[0]}, as described in the text. You must use continuous writing (not note form) and use your own words as far as possible. Your summary should be no more than {words} words.',
            'answer': 'Model summary: ' + MODEL[P.title], 'key': summary_key(m, P, words), 'marks': m, 'type': 'long'}


# ---------------------------------------------------------------- 3.2 organising
t32 = topic('Organising and grouping points logically', 'organising and grouping points logically', 'organising grouping')
t32.fixed('C1', (1, 2), [
    ('Which connective best introduces a contrasting point in a summary?', 'However,', 'Contrast connective.', ['Furthermore,', 'For example,', 'Similarly,']),
    ('Why is it helpful to group related points before writing a summary?', 'It produces a logical, cohesive paragraph rather than a random list', 'Grouping improves organisation (W2).', ['It makes the summary longer', 'It allows you to copy whole sentences', 'It removes the need for a word limit']),
    ('A summary on ‘benefits and drawbacks’ is best organised by', 'dealing with the benefits together and then the drawbacks', 'Group by category.', ['following the order of the passage exactly, mixing the two', 'starting with your own opinion', 'listing the drawbacks twice']),
    ('Which connective best adds a further point of the same kind?', 'In addition,', 'Addition connective.', ['On the other hand,', 'Despite this,', 'In contrast,']),
])


@add(t32, 'C1', (1, 2, 3))
def t32_conn(r, D):
    P = r.choice(SUMP)
    gs = groups(P)
    keys = (gs[0][1], gs[1][1])
    if r.random() < 0.5 and keys in CONTRAST:
        a = r.choice(points(P, keys[0]))
        b = r.choice(points(P, keys[1]))
        ans, ds, why = 'However,', ['Furthermore,', 'For example,', 'Similarly,'], 'the second point contrasts with the first'
    else:
        k = r.choice(keys)
        pts = points(P, k)
        if len(pts) < 2:
            return None
        a, b = r.sample(pts, 2)
        ans, ds, why = 'In addition,', ['However,', 'For example,', 'In conclusion,'], 'both points belong to the same group, so the second adds to the first'
    opts, ans = mcq(r, ans, ds)
    return {'stem': f'In a summary of {P.summary[0]} ({src(P)}), which connective best links these two points? ‘{cap(a[1])}.’ ___ ‘{b[1]}.’', 'options': opts, 'answer': ans, 'key': f'{ans} – {why}.'}


@add(t32, 'C2', (1, 2, 3, 4), 'explain')
def t32_sort(r, D):
    P = r.choice(SUMP)
    pts = points(P)[:]
    r.shuffle(pts)
    n = min(len(pts), 4 + (D >= 3))
    pts = pts[:n]
    m = max(2, mk('C2', D))
    (h1, k1), (h2, k2) = groups(P)
    return {'stem': f'Sort these summary points from {src(P)} into two groups, ‘{h1}’ and ‘{h2}’, and explain how grouping them will improve the summary. {plist([x[1] for x in pts])}',
            'answer': f'{cap(h1)}: ' + ', '.join(f'({i})' for i, x in enumerate(pts, 1) if x[2] == k1) + f'. {cap(h2)}: ' + ', '.join(f'({i})' for i, x in enumerate(pts, 1) if x[2] == k2) + '. Grouping lets each part of the summary deal with one aspect, so it is logical and avoids jumping between ideas.',
            'key': f'{upto(m)}: accurate grouping (1 mark, or 2 at higher tariffs); 1 mark for explaining that grouping gives a logical, cohesive structure.', 'marks': m}


@add(t32, 'C3', (1, 2, 3, 4, 5), 'short')
def t32_order(r, D):
    P = r.choice(SUMP)
    pts = points(P)[:]
    r.shuffle(pts)
    m = max(2, mk('C3', D))
    (h1, k1), (h2, k2) = groups(P)
    return {'stem': f'These notes for a summary of {P.summary[0]} ({src(P)}) are in a random order: {plist([x[1] for x in pts])} Arrange them into a logical order, group them, and write the summary as a short paragraph using suitable connectives.',
            'answer': f'Order: {h1} first, then {h2}. Model paragraph: {MODEL[P.title]}',
            'key': f'{upto(m)}: logical grouping ({h1} / {h2}); appropriate connectives (e.g. ‘In addition’, ‘However’); all points included in own words; continuous prose.', 'marks': m}


@add(t32, 'C4', (2, 3, 4, 5), 'long')
def t32_notes(r, D):
    P = r.choice(SUMP)
    pts = points(P)[:]
    r.shuffle(pts)
    words = {2: 70, 3: 80, 4: 100, 5: 120}.get(D, 70)
    m = mk('C4', D, 'long')
    return {'stem': f'A student has made these notes on {P.summary[0]} from {src(P)}: {plist([x[1] for x in pts])} Using the notes, write a summary of {P.summary[0]} in continuous prose, organising the points logically. Write no more than {words} words.',
            'answer': 'Model summary: ' + MODEL[P.title], 'key': rw_key(m, f'organised summary from notes, {words} words', 'all points included, logically grouped and linked', '; '.join(x[1] for x in P.summary[1]) + '. Writing: grouped by ' + ' / '.join(h for h, _ in groups(P)) + ', linked with connectives, concise.'),
            'marks': m, 'type': 'long'}


# ---------------------------------------------------------------- 3.3 concise, own words
t33 = topic('Writing concisely in own words within a word limit', 'writing concisely in own words within a word limit', 'concisely word limit')
t33.fixed('C1', (1, 2), [
    ('What is ‘lifting’ in summary writing?', 'Copying phrases or sentences directly from the passage', 'Lifting shows less understanding and is penalised in the writing marks.', ['Removing irrelevant points', 'Using connectives', 'Writing within the word limit']),
    ('Which technique best helps you stay within a word limit?', 'Combining related points into one sentence and cutting examples', 'Concision.', ['Adding an introduction about the writer', 'Repeating key points for emphasis', 'Using long quotations']),
    ('Which sentence is most concise?', 'Portions are too large.', 'Says the point in the fewest words.', ['It is really quite important to say that the portions are, in many cases, too large.', 'As the report clearly tells us, portions are too large, which is a problem.', 'Basically, what the text is saying is that portions are too large.']),
    ('What happens if your summary goes far beyond the word limit?', 'You lose the benefit of concision and may lose writing marks', 'Over-length summaries are penalised for lack of concision.', ['You gain extra content marks', 'Nothing – word limits are guidance only', 'The examiner reads only the first sentence']),
])


def padded(r, pt):
    return r.choice([f'{cap(pt)}, which is something that the writer mentions and explains in quite a lot of detail in the text.',
                     f'{cap(pt)} – this is basically what the writer is really trying to say in this part of the passage.',
                     f'{cap(pt)}, and this is an important point that the text makes very clearly indeed.'])


@add(t33, 'C1', (1, 2, 3))
def t33_best(r, D):
    P = r.choice(SUMP)
    pt = r.choice(points(P))
    other = [x for x in points(P) if x[2] != pt[2]]
    if not other:
        return None
    right = cap(pt[1]) + '.'
    opts, ans = mcq(r, right, [sent(P, pt[0]), padded(r, pt[1]), cap(r.choice(other)[1]) + '.'])
    return {'stem': f'Which is the most concise, own-words summary point for this sentence from {src(P)}? {Q(sent(P, pt[0]))}', 'options': opts, 'answer': ans,
            'key': f'{right} The other options copy the text, pad with unnecessary words, or give a different point.'}


@add(t33, 'C2', (1, 2, 3, 4), 'explain')
def t33_why(r, D):
    P = r.choice(SUMP)
    pt = r.choice(points(P))
    kind = r.choice(['lift', 'pad', 'opinion'])
    s = {'lift': sent(P, pt[0]), 'pad': padded(r, pt[1]), 'opinion': f'{cap(pt[1])}, which I think is a brilliant point and very true.'}[kind]
    why = {'lift': 'it copies the original sentence, so it is lifted and not in the student’s own words; it may also include unnecessary detail',
           'pad': 'it uses many unnecessary words before the point, wasting the word limit',
           'opinion': 'it adds the student’s own opinion, which does not belong in a summary'}[kind]
    m = max(2, mk('C2', D))
    return {'stem': f'A student writing a summary of {P.summary[0]} ({src(P)}) wrote: ‘{s}’ Explain why this sentence would lose marks, and rewrite it.',
            'answer': f'It loses marks because {why}. Rewrite: {cap(pt[1])}.', 'key': f'{upto(m)}: 1 mark: identifies the fault ({kind}: {why}); 1 mark: concise own-words rewrite – {pt[1]}.', 'marks': m}


@add(t33, 'C3', (1, 2, 3, 4, 5), 'short')
def t33_rewrite(r, D):
    P = r.choice(SUMP)
    n = 1 if D <= 2 else 2 if D <= 4 else 3
    pts = r.sample(points(P), n)
    if len({sent(P, p[0]) for p in pts}) < n:
        return None
    lim = max(6, max(wc(p[1]) for p in pts) + 3)
    q = ' '.join(f'({i}) {Q(sent(P, p[0]))}' for i, p in enumerate(pts, 1)) if n > 1 else Q(sent(P, pts[0][0]))
    stem = (f'Rewrite {"each of these sentences" if n > 1 else "this sentence"} from {src(P)} as a concise summary point about {P.summary[0]}, in your own words and using no more than {lim} words {"each" if n > 1 else ""}: {q}').replace('  ', ' ').replace(' :', ':')
    return {'stem': stem, 'answer': ' '.join(f'({i}) {cap(p[1])}.' for i, p in enumerate(pts, 1)) if n > 1 else cap(pts[0][1]) + '.',
            'key': f'Per sentence: 1 mark for the accurate point, 1 mark for concise own words within {lim} words. Points: ' + '; '.join(p[1] for p in pts) + '.', 'marks': 2 * n}


@add(t33, 'C4', (2, 3, 4, 5), 'multi_step')
def t33_draft(r, D):
    P = r.choice(SUMP)
    pts = r.sample(points(P), min(4, len(points(P))))
    pts.sort(key=lambda x: sidx(P, x[0]))
    bad = nonpoint_sents(P)
    if not bad:
        return None
    b = r.choice(bad)
    draft = ' '.join(dict.fromkeys([sent(P, p[0]) for p in pts[:2]] + [b] + [sent(P, p[0]) for p in pts[2:]]))
    lim = sum(wc(p[1]) for p in pts) + 12
    intro = f'A student’s draft summary of {P.summary[0]}, based on {src(P)}, reads: “{draft}”'
    parts = [lambda r: ('Identify one sentence in the draft that is irrelevant to the focus.', Q(b), f'{b} [1]'),
             lambda r: ('Explain two other weaknesses of the draft.', 'It lifts whole sentences from the text instead of using own words, and it is not concise (it includes examples and detail).', '1 mark each: lifting; lack of concision; no linking/organisation [2]'),
             lambda r: (f'Rewrite the relevant content as a concise summary in your own words, in no more than {lim} words.', ' '.join(cap(p[1]) + '.' for p in pts), f'1 mark per point retained in own words; concise and within {lim} words [{len(pts) + 1}]')]
    return compose(r, intro, parts, k=(3,), type_='multi_step')


CHAPTERS[3] = [t31, t32, t33]


# =========================================================== 4 Writers' effects (Paper 1 Question 3)

def q3_key(m, mood, items):
    ind = ' '.join(f'{Q(a)} – {b}' for a, b in items)
    return level_key(m, f'language task: how the writer conveys {mood}',
                     'a wide range of well-chosen words and phrases, including imagery, with precise explanation of meaning in context and of connotations and effects; analysis is developed, not just identified.',
                     'relevant choices with some explanation of meaning and effect, but some comments are general or partly descriptive.',
                     'some relevant selection, with explanations that are general (e.g. ‘makes it interesting’) or that repeat the words.',
                     ind)


# ---------------------------------------------------------------- 4.1 selecting powerful words
t41 = topic('Selecting powerful words and phrases from a text', 'selecting powerful words and phrases from a text', 'powerful words')
t41.fixed('C1', (1, 2), [
    ('In a language question, what makes a word ‘powerful’?', 'It carries strong meaning or associations that create a clear effect', 'Powerful = precise, vivid, connotative.', ['It is the longest word in the sentence', 'It is a common everyday word', 'It appears in the title']),
    ('Which kind of choice is usually most rewarding to analyse in Question 3?', 'Specific words and short phrases, including imagery', 'Short, precise selections allow focused analysis.', ['Whole paragraphs copied out', 'Words such as ‘the’ and ‘and’', 'Proper names of people']),
    ('Which word in ‘The wind snatched her hat’ is most powerful?', 'snatched', '‘snatched’ suggests a sudden, aggressive grab.', ['wind', 'her', 'hat']),
    ('How many words should a typical selection for analysis contain?', 'Usually one to six words', 'Short quotations keep analysis precise.', ['A whole paragraph', 'At least two sentences', 'Exactly ten words']),
])


@add(t41, 'C1', (1, 2, 3))
def t41_mcq(r, D):
    P = r.choice(pool('effects'))
    ph, sug, ana, plain = r.choice(P.effects)
    s = sent(P, ph)
    others = ' '.join([e[0] for e in P.effects if e[0] != ph] + [f[0] for f in P.figs])
    ds = content_words(s, ph + ' ' + others)
    if len(ds) < 3:
        return None
    opts, ans = mcq(r, ph, ds)
    return {'stem': f'{lead(r, P)} {Q(s)} Which word most strongly suggests {sug}?', 'options': opts, 'answer': ans, 'key': f'{Q(ph)}: {ana}'}


@add(t41, 'C2', (1, 2, 3, 4), 'explain')
def t41_plain(r, D):
    P = r.choice(pool('effects'))
    ph, sug, ana, plain = r.choice(P.effects)
    m = max(2, mk('C2', D))
    return {'stem': r.choice([f'Explain why {Q(ph)} is more effective than {Q(plain)} would be in this sentence from {src(P)}: {Q(sent(P, ph))}',
                              f'In {src(P)} the writer chose {Q(ph)} rather than a plainer word such as {Q(plain)}: {Q(sent(P, ph))} Explain the effect of this choice.']),
            'answer': f'{ana} {Q(plain)} would simply state the fact without these associations.',
            'key': f'{upto(m)}: 1 mark: meaning in context ({sug}); 1 mark: effect/connotation beyond the plain word; further mark for a developed link to the passage. Indicative: {ana}', 'marks': m}


t41.fixed('C2', (2, 3), [
    ('Explain why ‘The writer uses a good word to describe the storm’ would gain few marks in a language question.', 'It does not identify the word, explain its meaning in context or analyse its connotations and effect; ‘good’ is vague.',
     '1 mark: no specific selection; 1 mark: no explanation of meaning/effect. [2]'),
    ('Explain why choosing a short, precise quotation is better than copying a whole sentence when analysing language.', 'A short quotation pinpoints the exact word whose effect you are explaining, so the analysis is focused; a whole sentence hides which word matters.',
     '1 mark: focus on precise words; 1 mark: allows detailed analysis of connotation. [2]'),
])


@add(t41, 'C3', (1, 2, 3, 4, 5), 'short')
def t41_pick(r, D):
    P = r.choice([p for p in ALL if len(p.effects) + len(p.figs) >= 2 and p.effects])
    e = r.choice(P.effects)
    others = [x for x in P.effects if x is not e] + [(f[0], f[1], f[2], None) for f in P.figs]
    o = r.choice(others)
    intro = f'{lead_x(r, P)} “{ext(P, [e[0], o[0]])}”'
    m2 = 3 if D >= 4 else 2
    parts = [lambda r: (f'Identify one word in the extract that suggests {e[1]}.', Q(e[0]), f'{e[0]} [1]'),
             effect_part(P, e, m2),
             lambda r: (f'Explain the effect of {Q(o[0])}.', o[2], f'meaning and effect explained: {o[2]} [{m2}]')]
    return compose(r, intro, parts, k=(2,) if D <= 2 else (3,), type_='short')


@add(t41, 'C4', (2, 3, 4, 5), 'long')
def t41_q3(r, D):
    P = r.choice([p for p in ALL if p.mood and len(p.effects) >= 2])
    items = [(e[0], e[2]) for e in P.effects] + [(f[0], f[2]) for f in P.figs[:1]]
    x = ext(P, [i[0] for i in items])
    m = mk('C4', D, 'long')
    return {'stem': f'Re-read these sentences from {src(P)}: “{x}” Explain how the writer uses language to convey {P.mood}. Select powerful words and phrases, including imagery, and explain how they create effects.',
            'answer': 'Model points: ' + ' '.join(f'{Q(a)}: {b}' for a, b in items), 'key': q3_key(m, P.mood, items), 'marks': m, 'type': 'long'}


# ---------------------------------------------------------------- 4.2 connotations
t42 = topic('Explaining connotations and effects of vocabulary choices', 'explaining connotations and effects of vocabulary choices', 'connotations')
t42.fixed('C1', (1, 2), [
    ('What is a connotation?', 'An idea or feeling associated with a word beyond its literal meaning', 'Connotation vs denotation.', ['The dictionary definition of a word', 'The number of syllables in a word', 'A word that sounds like another']),
    ('Which word has the most negative connotations for a crowd?', 'mob', '‘mob’ suggests disorder and threat.', ['gathering', 'audience', 'group']),
    ('Which word has the most positive connotations for a home?', 'haven', '‘haven’ suggests safety and comfort.', ['building', 'property', 'unit']),
    ('‘Slender’ and ‘skinny’ have a similar meaning. How do their connotations differ?', '‘Slender’ is approving; ‘skinny’ can suggest unhealthy thinness', 'Same denotation, different connotations.', ['They are identical in every way', '‘Skinny’ is more formal', '‘Slender’ means very large']),
])


@add(t42, 'C1', (1, 2, 3))
def t42_mcq(r, D):
    P = r.choice(pool('effects'))
    ph, sug, ana, plain = r.choice(P.effects)
    ds = [e[1] for p in ALL for e in p.effects if e[0] != ph and e[1] != sug]
    opts, ans = mcq(r, sug, ds)
    return {'stem': f'{lead(r, P)} {Q(sent(P, ph))} What does the word {Q(ph)} suggest here?', 'options': opts, 'answer': ans, 'key': ana}


@add(t42, 'C2', (1, 2, 3, 4), 'explain')
def t42_explain(r, D):
    P = r.choice(pool('effects'))
    ph, sug, ana, plain = r.choice(P.effects)
    m = max(2, mk('C2', D))
    return {'stem': r.choice([f'Explain the connotations of {Q(ph)} in this sentence from {src(P)}: {Q(sent(P, ph))}', f'{lead(r, P)} {Q(sent(P, ph))} What does {Q(ph)} suggest, and what effect does it have on the reader?']),
            'answer': ana, 'key': f'{upto(m)}: 1 mark: meaning in context; 1 mark: connotation ({sug}); further mark: effect on reader or link to wider impression. Indicative: {ana}', 'marks': m}


@add(t42, 'C3', (1, 2, 3, 4, 5), 'short')
def t42_parts(r, D):
    P = r.choice(pool('effects', need=2))
    es = r.sample(P.effects, min(len(P.effects), 2 if D <= 3 else 3))
    intro = f'{lead_x(r, P)} “{ext(P, [e[0] for e in es])}”'
    m = 3 if D >= 5 else 2
    return compose(r, intro, [effect_part(P, e, m) for e in es], k=(len(es),) if D >= 3 else (1, 2), type_='short')


@add(t42, 'C4', (2, 3, 4, 5), 'multi_step')
def t42_critique(r, D):
    P = r.choice(pool('effects', need=2))
    e1, e2 = r.sample(P.effects, 2)
    weak = r.choice(['The writer uses a good word that makes it more interesting for the reader.', 'This word is effective because it describes what is happening.', f'The word {e1[0]} is a verb and it makes you want to read on.'])
    intro = f'In {src(P)} the writer writes: {Q(sent(P, e1[0]))} A student commented on {Q(e1[0])}: ‘{weak}’'
    parts = [lambda r: ('Explain why the student’s comment would gain few marks.', 'It is general: it does not explain the meaning of the word in context or its connotations, and the comment could apply to any word.', '1 mark: no meaning/connotation; 1 mark: generic comment [2]'),
             lambda r: (f'Write a better analysis of {Q(e1[0])}.', e1[2], f'meaning in context; connotation ({e1[1]}); effect [3]'),
             lambda r: (f'Explain the connotations of {Q(e2[0])} in {Q(sent(P, e2[0]))}, and how it adds to the same impression.', e2[2], f'connotation ({e2[1]}); link to overall impression [2]')]
    return compose(r, intro, parts, k=(3,), type_='multi_step')


# ---------------------------------------------------------------- 4.3 figurative language, imagery and sound
t43 = topic('Analysing figurative language, imagery and sound', 'analysing figurative language, imagery and sound', 'figurative imagery')
t43.fixed('C1', (1, 2), [(f'What is {"an" if d[0] in "aeiou" else "a"} {d}?' if d != 'visual imagery' else 'What is visual imagery?', cap(DEV_DEF[d]), f'{cap(d)}: {DEV_DEF[d]}.', [cap(DEV_DEF[x]) for x in DEVICES if x != d][:5])
                         for d in ['simile', 'metaphor', 'personification', 'onomatopoeia', 'oxymoron', 'hyperbole']])


@add(t43, 'C1', (1, 2, 3))
def t43_device(r, D):
    P = r.choice(pool('figs'))
    ph, dev, ana = r.choice(P.figs)
    bad = {dev} | DEV_CLASH.get(dev, set())
    if alliterative(ph):
        bad.add('alliteration')
    if re.search(r'\b(like|as)\b', ph) and dev != 'simile':
        bad.add('simile')
    opts, ans = mcq(r, dev, [d for d in DEVICES if d not in bad])
    return {'stem': f'{lead(r, P)} {Q(sent(P, ph))} Which technique is used in {Q(ph)}?', 'options': opts, 'answer': ans, 'key': f'{cap(dev)}: {ana}'}


@add(t43, 'C2', (1, 2, 3, 4), 'explain')
def t43_explain(r, D):
    P = r.choice(pool('figs'))
    ph, dev, ana = r.choice(P.figs)
    m = max(2, mk('C2', D))
    return {'stem': r.choice([f'Explain the effect of the {dev} {Q(ph)} in {src(P)}.', f'In {src(P)}, the writer writes {Q(ph)}. Explain what this {dev} suggests and why it is effective.']),
            'answer': cap(ana), 'key': f'{upto(m)}: 1 mark: what is being compared or described and what it suggests; 1 mark: effect on the reader; further mark: link to mood or meaning of the passage. Indicative: {ana}', 'marks': m}


@add(t43, 'C3', (1, 2, 3, 4, 5), 'short')
def t43_parts(r, D):
    P = r.choice(pool('figs', need=2) if D >= 3 else pool('figs'))
    fs = r.sample(P.figs, min(len(P.figs), 1 if D <= 2 else 2))
    intro = f'{lead_x(r, P)} “{ext(P, [f[0] for f in fs])}”'
    parts = [fig_part(P, f, 3 if D >= 4 else 2) for f in fs]
    if P.mood and D >= 3:
        parts.append(lambda r: (f'Explain how the imagery in the extract helps to convey {P.mood}.', f'Together the images ({", ".join(Q(f[0]) for f in fs)}) build {P.mood}.', 'clear link between images and overall effect [2]'))
    return compose(r, intro, parts, k=(len(parts),), type_='short')


@add(t43, 'C4', (2, 3, 4, 5), 'long')
def t43_imagery(r, D):
    P = r.choice([p for p in pool('figs', need=2) if p.mood])
    items = [(f[0], f'{f[1]}: {f[2]}') for f in P.figs]
    x = ext(P, [f[0] for f in P.figs])
    m = mk('C4', D, 'long')
    return {'stem': f'Read this extract from {src(P)}: “{x}” Explain how the writer uses imagery and sound to create {P.mood}. Refer closely to specific words and phrases and explain their effects.',
            'answer': 'Model points: ' + ' '.join(f'{Q(a)} ({b})' for a, b in items), 'key': q3_key(m, P.mood, items), 'marks': m, 'type': 'long'}


# ---------------------------------------------------------------- 4.4 structure and sentence forms
t44 = topic('Analysing structure and sentence forms for effect', 'analysing structure and sentence forms for effect', 'structure sentence forms')
t44.fixed('C1', (1, 2), [
    ('What is a minor sentence?', 'A sentence without a main verb, used for effect', 'E.g. ‘Twelve degrees.’', ['A sentence with two main clauses', 'A very long descriptive sentence', 'A sentence in brackets']),
    ('What is the usual effect of a very short sentence after several long ones?', 'It creates emphasis or a sudden change of pace', 'Contrast in length draws attention.', ['It makes the writing less clear', 'It always signals the end of the text', 'It shows the writer is unsure']),
    ('A text opens with a surprising detail to catch the reader’s interest. This is called', 'an opening hook', 'Hook = attention-grabbing opening.', ['a conclusion', 'a subheading', 'a footnote']),
    ('What is a ‘list of three’ (tricolon) usually used for?', 'To build emphasis and a memorable rhythm', 'Three items feel complete and persuasive.', ['To confuse the reader', 'To introduce a quotation', 'To mark a change of speaker']),
    ('A circular structure is one in which', 'the ending returns to an idea or image from the opening', 'Circularity gives a sense of completion or change.', ['every paragraph is the same length', 'the events are told in reverse', 'the text has no ending']),
])


@add(t44, 'C1', (1, 2, 3))
def t44_mcq(r, D):
    P = r.choice(pool('struct'))
    loc, ft, eff, also = r.choice(P.struct)
    if ft not in STYPES_POOL + ['short sentence', 'minor sentence', 'repetition', 'contrast', 'opening hook', 'ending / closing line', 'present tense']:
        return None
    has = struct_has(loc, ft, also)
    if {'short sentence', 'minor sentence'} & has:
        has |= {'short sentence', 'minor sentence'}
    pool_ = [x for x in STYPES_POOL if x not in has]
    opts, ans = mcq(r, ft, pool_)
    return {'stem': f'{lead(r, P, "extract")} {Q(loc)} Which structural or sentence feature is most clearly used here?', 'options': opts, 'answer': ans, 'key': f'{cap(ft)}: {eff}'}


@add(t44, 'C2', (1, 2, 3, 4), 'explain')
def t44_explain(r, D):
    P = r.choice(pool('struct'))
    loc, ft, eff, also = r.choice(P.struct)
    m = max(2, mk('C2', D))
    return {'stem': r.choice([f'Explain the effect of the {ft} in this part of {src(P)}: {Q(loc)}', f'{lead(r, P, "extract")} {Q(loc)} Why has the writer used a {ft} here?']),
            'answer': cap(eff), 'key': f'{upto(m)}: 1 mark: identifies how the {ft} works; 1 mark: effect on pace, emphasis or meaning; further mark: link to the purpose or mood of the text. Indicative: {eff}', 'marks': m}


@add(t44, 'C3', (1, 2, 3, 4, 5), 'short')
def t44_parts(r, D):
    P = r.choice(pool('struct', need=2))
    ss = r.sample(P.struct, 2)
    intro = f'{lead_x(r, P)} “{ext(P, [s[0] for s in ss])}”'
    m = 3 if D >= 4 else 2
    parts = [lambda r: (f'Identify the sentence feature used in {Q(ss[0][0])}.', cap(ss[0][1]) + '.', f'{ss[0][1]} [1]'), struct_part(P, ss[0], m, named=False), struct_part(P, ss[1], m)]
    return compose(r, intro, parts, k=(2,) if D <= 2 else (3,), type_='short')


@add(t44, 'C4', (2, 3, 4, 5), 'long')
def t44_whole(r, D):
    P = r.choice(pool('struct', need=2))
    items = [(s[0], f'{s[1]}: {s[2]}') for s in P.struct]
    m = mk('C4', D, 'long')
    aim = P.mood or P.purpose.replace('to ', '', 1)
    return {'stem': f'{full(P)} Explain how the writer uses structure and sentence forms to {"convey " + P.mood if P.mood else "achieve the purpose of the text (" + P.purpose + ")"}. Consider the opening, changes of focus or pace, sentence lengths and the ending.',
            'answer': 'Model points: ' + ' '.join(f'{Q(a)}: {dot(b)}' for a, b in items),
            'key': level_key(m, f'structure and sentence forms: {aim}', 'precise identification of structural choices across the whole text, with developed explanation of their effects on pace, emphasis and the reader’s response.',
                             'relevant structural features identified with some explanation of effect.', 'features named or described with little explanation.', ' '.join(f'{Q(a)} – {dot(b)}' for a, b in items)),
            'marks': m, 'type': 'long'}


CHAPTERS[4] = [t41, t42, t43, t44]


# =========================================================== 5 Extended response to reading (Paper 1 Question 4)

ROLEP = [p for p in ALL if p.role]
FORM_FEATS = {
    'journal': ('a private, reflective first-person voice exploring thoughts and feelings', 'an honest, informal tone and references to the time of writing'),
    'guide': ('practical advice organised clearly for visitors', 'second-person address and an informative, enthusiastic tone'),
    'blog': ('an informal, conversational first-person voice', 'direct engagement with the original post and its readers'),
    'speech': ('direct address to the listeners, e.g. “Good evening, everyone”', 'rhetorical devices such as questions, repetition and a call to action'),
    'report': ('a title, subheadings and an impersonal, formal tone', 'findings followed by clear recommendations'),
    'article': ('a headline and an engaging opening paragraph', 'a lively but controlled voice suited to the publication’s readers'),
    'letter': ('an opening such as “Dear …” and a suitable sign-off', 'a clear purpose stated early and a register suited to the recipient'),
}


def form_of(task):
    t = task.lower()
    for k, rx in [('journal', r'journal|diary'), ('guide', r'guidebook'), ('blog', r'\bblog\b'), ('speech', r'speech|\btalk\b'), ('report', r'\breport\b'), ('article', r'article'), ('letter', r'letter')]:
        if re.search(rx, t):
            return k
    return 'letter'


def who(task):
    m = re.match(r'Imagine you are ([^.]+)\.', task)
    return m.group(1) if m else 'the character'


def role_task(P):
    task, bullets, ideas, model = P.role
    return f'{task} In your {form_of(task)}, you should write about: ' + '; '.join(bullets) + '.'


def role_key(m, P):
    task, bullets, ideas, model = P.role
    f = form_of(task)
    ind = ' '.join(f'{cap(i[1])} → {i[2]}.' for i in ideas)
    return rw_key(m, f'extended response in role ({f})', 'ideas from the passage are thoroughly used, developed and extended with convincing inferences; all three bullets addressed; a consistent, convincing voice',
                  f'{ind} Form: {FORM_FEATS[f][0]}; {FORM_FEATS[f][1]}.')


# ---------------------------------------------------------------- 5.1 writing in role
t51 = topic('Writing in role: letter, speech, journal or report based on a text', 'writing in role: letter, speech, journal or report based on a text', 'writing in role')
t51.fixed('C1', (1, 2), [
    ('You are writing a formal letter to someone whose name you do not know. Which sign-off is correct?', 'Yours faithfully', '‘Dear Sir or Madam … Yours faithfully’; ‘Dear Mr X … Yours sincerely’.', ['Yours sincerely', 'Love from', 'See you soon']),
    ('Which feature is most important in a speech written in role?', 'Direct address to the audience', 'Speeches are spoken to listeners.', ['Subheadings', 'A dated heading', 'Footnotes']),
    ('A journal entry written in role should mainly', 'reveal the character’s private thoughts and feelings', 'Journals are reflective and personal.', ['list statistics under headings', 'address a large audience', 'give instructions to visitors']),
    ('In Question 4, what does writing ‘in role’ mean?', 'Writing as a character or person from the passage, using their viewpoint and voice', 'You adopt the given persona.', ['Writing as yourself giving opinions about the passage', 'Writing a summary of the passage', 'Writing a story with new characters']),
    ('Which register suits a report written for a manager?', 'Formal and objective', 'Reports are formal and impersonal.', ['Chatty and full of slang', 'Poetic and rhyming', 'Angry and exaggerated']),
    ('Why must you address all three bullet points in an extended response task?', 'The bullets define the content the reading marks reward', 'Missing a bullet limits the reading mark.', ['Because each bullet must be a separate paragraph of exactly equal length', 'Because they tell you the word count', 'Because they are only suggestions and can be ignored']),
])


@add(t51, 'C1', (1, 2, 3))
def t51_form(r, D):
    P = r.choice(ROLEP)
    f = form_of(P.role[0])
    opts, ans = mcq(r, cap(FORM_FEATS[f][0]), [cap(v[0]) for k, v in FORM_FEATS.items() if k != f and not (f in ('journal', 'blog') and k in ('journal', 'blog'))])
    return {'stem': f'Based on {src(P)}, you are given this task: “{P.role[0]}” Which feature would be most appropriate in your response?', 'options': opts, 'answer': ans,
            'key': f'The task asks for a {f}: {FORM_FEATS[f][0]}.'}


BAD_OPEN = [
    ('Imagine you are a parks officer replying formally to a letter in a newspaper.', 'Hiya Mei, chill out about the lights, they’re fine!', 'The register is far too informal and dismissive for a public reply to a serious letter.', 'Dear Editor, I would like to thank Dr Tanaka for her thoughtful letter about the floodlights.'),
    ('Imagine you are a student giving a speech in assembly.', 'In this speech I will talk about food waste. Firstly food waste. Secondly also food waste.', 'It announces the topic mechanically and repeats itself; there is no engaging address to the audience.', 'Good morning, Year 10. Every school day we throw away forty-one kilograms of food.'),
    ('Imagine you are a character writing a private journal entry about a frightening night.', 'Report on the Night Crossing. Findings: the ferry was late.', 'It uses report conventions; a journal should be personal and reflective.', 'I am writing this on the quayside with salt still in my hair. Last night I really thought I had made a mistake.'),
    ('Imagine you are a business owner writing to the town council.', 'The plan is rubbish and everyone knows it.', 'It is rude, vague and unsupported; a formal letter needs a polite, reasoned opening.', 'Dear Councillors, I respect the result of Saturday’s vote, but I must explain what it will mean for shops like mine.'),
    ('Imagine you are a volunteer writing to ask a local business for funding.', 'Give us money please.', 'It is blunt, informal and gives no context or reason; it would not persuade a business manager.', 'Dear Manager, every morning at half past four, two volunteers walk three kilometres of your town’s beach in the dark.'),
    ('Imagine you are a rescued teenager writing a letter of thanks to a rescue volunteer.', 'To whom it may concern, this letter is to formally notify you of the rescue.', 'It is cold and impersonal; a thank-you letter should be warm and sincere.', 'Dear Mr Ndlovu, I will never forget the moment your torch found us in the cloud.'),
]


@add(t51, 'C2', (1, 2, 3, 4), 'explain')
def t51_bad(r, D):
    task, bad, why, good = r.choice(BAD_OPEN)
    m = max(2, mk('C2', D))
    return {'stem': f'Task: {task} A student begins: ‘{bad}’ Explain what is wrong with this opening and suggest a better one.',
            'answer': f'{why} Better: ‘{good}’', 'key': f'{upto(m)}: 1 mark: identifies the problem of form/register/voice; 1 mark: improved opening that suits the role and audience.', 'marks': m}


@add(t51, 'C2', (1, 2, 3, 4), 'explain')
def t51_feats(r, D):
    P = r.choice(ROLEP)
    f = form_of(P.role[0])
    m = max(2, mk('C2', D))
    return {'stem': f'Explain two features you should include when responding to this task based on {src(P)}: “{role_task(P)}”',
            'answer': f'{cap(FORM_FEATS[f][0])}; {FORM_FEATS[f][1]}. The voice should be that of {who(P.role[0])}, using details from the passage.',
            'key': f'{upto(m)}: 1 mark per relevant, explained feature of a {f} in role (e.g. {FORM_FEATS[f][0]}); 1 mark for linking voice to {who(P.role[0])}.', 'marks': m}


@add(t51, 'C3', (1, 2, 3, 4, 5), 'short')
def t51_plan(r, D):
    P = r.choice(ROLEP)
    ideas = P.role[2]
    n = 2 if D <= 2 else 3 if D <= 4 else 4
    sel = sorted(r.sample(ideas, n), key=lambda i: sidx(P, i[0]))
    return {'stem': f'Task: “{P.role[0]}” These sentences come from {src(P)}: “{ext(P, [i[0] for i in sel])}” Explain how you would use each detail in your response, developing it from the point of view of {who(P.role[0])}.',
            'answer': ' '.join(f'{cap(i[1])}: {i[2]}.' for i in sel), 'key': f'1 mark per detail identified and 1 mark per detail developed in role (max {2 * n}): ' + '; '.join(f'{i[1]} → {i[2]}' for i in sel) + '.', 'marks': 2 * n}


@add(t51, 'C4', (2, 3, 4, 5), 'long')
def t51_task(r, D):
    P = r.choice(ROLEP)
    m = mk('C4', D, 'long')
    words = {2: '200–250', 3: '250–300', 4: '250–350', 5: '250–350'}.get(D, '200–250')
    return {'stem': f'{full(P)} {role_task(P)} Base your answer on what you have read, but be careful to use your own words. Write about {words} words.',
            'answer': 'Model opening: ' + P.role[3] + ' The response then develops: ' + '; '.join(f'{i[1]} ({i[2]})' for i in P.role[2]) + '.', 'key': role_key(m, P), 'marks': m, 'type': 'long'}


# ---------------------------------------------------------------- 5.2 developing ideas
t52 = topic('Developing and extending ideas from the passage with evidence', 'developing and extending ideas from the passage with evidence', 'developing extending ideas')
t52.fixed('C1', (1, 2), [
    ('In an extended response, what does it mean to ‘develop’ an idea from the passage?', 'To go beyond what is stated by inferring causes, feelings or consequences that fit the text', 'Development = plausible extension grounded in the text.', ['To copy the idea in the writer’s words', 'To invent events unconnected to the text', 'To repeat the idea several times']),
    ('Which response best develops the detail ‘the bus left two hours late’ in role?', 'For us locals a late bus is normal, but I could see the visitor’s patience draining with every glass of tea.', 'It infers a viewpoint and feelings from the detail.', ['The bus left two hours late.', 'The bus was late. It was late.', 'There was a bus.']),
    ('Developed ideas should always be', 'consistent with the evidence in the passage', 'Extensions must be plausible and grounded.', ['completely new and unrelated', 'as dramatic as possible', 'copied from the final paragraph']),
    ('Which assessment objective is most clearly rewarded when you extend and develop ideas from a text?', 'R3', 'R3: analyse, evaluate and develop facts, ideas and opinions.', ['R1', 'R4', 'R5']),
])


@add(t52, 'C1', (1, 2, 3))
def t52_mcq(r, D):
    P = r.choice(ROLEP)
    loc, idea, dev = r.choice(P.role[2])
    other = r.choice([q for q in ROLEP if q is not P]).role[2][0][2]
    opts, ans = mcq(r, cap(dev) + '.', [f'Mention {idea}.', cap(sent(P, loc)), cap(other) + '.'])
    return {'stem': f'Task: “{P.role[0]}” Which is the best development of the detail about {idea} from {src(P)}?', 'options': opts, 'answer': ans,
            'key': f'{cap(dev)} – it extends the detail with a plausible inference; the others only repeat the text or are unrelated.'}


@add(t52, 'C2', (1, 2, 3, 4), 'explain')
def t52_repeat(r, D):
    P = r.choice(ROLEP)
    loc, idea, dev = r.choice(P.role[2])
    m = max(2, mk('C2', D))
    return {'stem': f'Task: “{P.role[0]}” A student’s response includes this sentence copied from {src(P)}: {Q(sent(P, loc))} Explain why this only repeats the passage, and suggest how the student could develop the idea.',
            'answer': f'It retells the text without interpreting it, so it shows little R3 development. Development: {dev}.',
            'key': f'{upto(m)}: 1 mark: recognises repetition/lifting; 1 mark: plausible development ({dev}); further mark for linking it to the role and purpose.', 'marks': m}


@add(t52, 'C3', (1, 2, 3, 4, 5), 'explain')
def t52_extend(r, D):
    P = r.choice(ROLEP)
    n = 1 if D <= 2 else 2
    sel = r.sample(P.role[2], n)
    m = max(2, mk('C3', D))
    stem = (f'Writing as {who(P.role[0])}, develop {"each of these details" if n > 1 else "this detail"} from {src(P)} into two or three sentences that infer thoughts, feelings or consequences: '
            + ' '.join(Q(sent(P, i[0])) for i in sel))
    return {'stem': stem, 'answer': ' '.join(f'Detail: {i[1]}. Developed in role: {i[2]}.' for i in sel),
            'key': f'{upto(m)}: credit plausible inference grounded in the detail, written in role; indicative: ' + '; '.join(f'{i[1]} → {i[2]}' for i in sel) + '. No credit for copying.', 'marks': m}


@add(t52, 'C4', (2, 3, 4, 5), 'multi_step')
def t52_plan(r, D):
    P = r.choice(ROLEP)
    task, bullets, ideas, model = P.role
    sel = r.sample(ideas, 2)
    intro = f'Task based on {src(P)}: “{role_task(P)}” Relevant lines: “{ext(P, [i[0] for i in ideas])}”'
    parts = [lambda r: ('Identify two details from the lines that you could use in your response, and state which bullet point each would support.', f'{cap(sel[0][1])}; {sel[1][1]} (each linked to a suitable bullet).', '1 mark per relevant detail linked to a bullet [2]'),
             lambda r: ('For each detail, explain how you would develop it beyond what the text states.', f'{cap(sel[0][2])}; {sel[1][2]}.', '2 marks per developed, plausible extension [4]'),
             lambda r: ('Explain why developed ideas are rewarded more highly than repeated ones.', 'R3 rewards developing and evaluating ideas; repetition only shows basic understanding (R1).', 'link to R3 [2]')]
    return compose(r, intro, parts, k=(3,), type_='multi_step')


# ---------------------------------------------------------------- 5.3 voice and register
t53 = topic('Adapting voice, register and form to the task', 'adapting voice, register and form to the task', 'voice register')
REG = [
    ('the town council', 'formal', 'I would ask the council to reconsider how long the floodlights remain on each night.', ['Your floodlights are seriously messing up our sky, sort it out!', 'Lights bad. Stars gone. Fix it.', 'Hey council, the lights are well annoying lol.'], 'polite modal ‘would ask’, precise vocabulary, no slang'),
    ('the Head of Year', 'formal', 'Many students are unhappy with the quality of the food and the length of the queues.', ['The canteen food is gross and the queues are mad long.', 'Food = bad, queues = worse!!!', 'Honestly, who even eats that stuff?'], 'measured, impersonal phrasing suitable for a staff reader'),
    ('readers of a newspaper', 'formal', 'A significant number of residents believe the new plan is flawed.', ['Loads of people reckon the new plan is rubbish.', 'The plan stinks, obviously.', 'Like, nobody wants this plan, yeah?'], 'precise quantity and neutral judgement rather than slang'),
    ('a museum director', 'formal', 'The café’s prices seem high for what is offered.', ['Your café is a total rip-off.', 'The café is daylight robbery, mate.', 'Eight euros?! Are you joking?'], 'tactful, evaluative language'),
    ('a business manager', 'formal', 'Your support would allow us to continue protecting the turtles after December.', ['Give us some cash so the turtles don’t die, yeah?', 'Money. Now. For turtles.', 'Pls fund us, thx.'], 'courteous conditional ‘would allow’ and a clear purpose'),
    ('school governors', 'formal', 'Homework is causing considerable stress for many students and their families.', ['Basically, homework is doing everyone’s heads in.', 'Homework = misery, end of.', 'We all hate homework, obviously.'], 'formal vocabulary (‘considerable’) and no idiom'),
    ('a mountain hut warden', 'formal', 'The weather changed suddenly and we were in real danger.', ['The weather went totally crazy and we nearly got wiped out.', 'Storm! Scary! Help!', 'It was like, the worst ever, honestly.'], 'clear, factual account without exaggerated slang'),
    ('a government minister', 'formal', 'I urge you to reopen our school as quickly as possible.', ['You lot need to hurry up and fix our school.', 'School. Fix. Now.', 'Come on, just sort the school out, will you?'], 'respectful but forceful ‘I urge you’'),
    ('a close friend, in a letter', 'informal', 'You won’t believe the journey I’ve just had — it was awful!', ['I am writing to inform you that the journey was extremely unpleasant.', 'Please find enclosed a report on the journey.', 'It is with regret that I report the journey was unsatisfactory.'], 'contractions, exclamation and a chatty tone suit a friend'),
    ('your own private journal', 'informal', 'I really lost my nerve today, and I hate admitting it.', ['It is with regret that I report my failure to remain calm.', 'Findings: nerve lost. Recommendation: remain calm.', 'Dear Sir, I wish to record that I was nervous.'], 'honest, personal first-person voice'),
    ('young readers of a lifestyle blog', 'informal', 'Let’s be honest: we all spend way too long on our phones.', ['One must consider the detrimental impact of excessive device usage.', 'Device usage statistics are presented below.', 'Readers are advised that phone usage is excessive.'], 'inclusive ‘we’, conversational ‘way too long’'),
    ('Year 10 students in an assembly', 'informal', 'So here’s my challenge to all of you: take only what you’ll actually eat.', ['It is recommended that pupils reduce the quantity of discarded food.', 'Food waste reduction measures are required.', 'Pupils are hereby instructed to waste less.'], 'direct address and a friendly challenge suit a peer audience'),
]
t53.fixed('C1', (1, 2), [
    ('What does ‘register’ mean?', 'The level of formality of language, chosen to suit the audience and purpose', 'Register = formality.', ['The list of students in a class', 'The speed of reading', 'The number of paragraphs']),
    ('Which is the most formal sentence?', 'I would be grateful if you could reconsider the decision.', 'Polite conditional, no contractions.', ['Can you just change your mind?', 'Change it, please!', 'You gotta rethink this.']),
    ('A speech to classmates can be less formal than a report to a manager because', 'the audience is made up of peers and the purpose is to engage them', 'Audience shapes register.', ['speeches never use standard English', 'reports are always informal', 'peers do not understand formal language']),
    ('‘Voice’ in an extended response means', 'the distinctive personality and viewpoint of the person you are writing as', 'Voice = persona’s character in the writing.', ['how loudly the text is read', 'the use of the passive voice only', 'the number of quotations used']),
])


@add(t53, 'C1', (1, 2, 3))
def t53_mcq(r, D):
    aud, reg, right, wrongs, why = r.choice(REG)
    opts, ans = mcq(r, right, wrongs)
    return {'stem': r.choice([f'Which version is most appropriate for {aud}?', f'You are writing for {aud}. Which sentence has the most suitable register?']), 'options': opts, 'answer': ans, 'key': f'{right} – {why} ({reg} register).'}


@add(t53, 'C2', (1, 2, 3, 4), 'explain')
def t53_rewrite(r, D):
    aud, reg, right, wrongs, why = r.choice(REG)
    w = wrongs[0]
    m = max(2, mk('C2', D))
    return {'stem': r.choice([f'Rewrite this sentence so that it suits {aud}, and explain one change you made: ‘{w}’', f'A student writing for {aud} wrote: ‘{w}’ Rewrite it in an appropriate register and explain your choices.']),
            'answer': f'‘{right}’ – {why}.', 'key': f'{upto(m)}: 1 mark: meaning kept in an appropriate {reg} register; 1 mark: explanation of a specific change (e.g. {why}).', 'marks': m}


@add(t53, 'C3', (1, 2, 3, 4, 5), 'short')
def t53_two(r, D):
    a, b = r.sample(REG, 2)
    parts = [lambda r: (f'Rewrite ‘{a[3][0]}’ for {a[0]}.', a[2], f'appropriate {a[1]} register, meaning kept [2]'),
             lambda r: (f'Rewrite ‘{b[3][0]}’ for {b[0]}.', b[2], f'appropriate {b[1]} register, meaning kept [2]'),
             lambda r: ('Explain how the intended audience shaped the choices you made when rewriting.', f'For {a[0]}: {a[4]}. For {b[0]}: {b[4]}.', 'specific choice of vocabulary or tone linked to the audience [2]')]
    if D <= 2:
        parts = parts[:1] + parts[2:]
    return compose(r, 'Rewrite each sentence in a register suited to the audience named, keeping its meaning.', parts, k=(len(parts),), type_='short')


@add(t53, 'C4', (2, 3, 4, 5), 'long')
def t53_open(r, D):
    P = r.choice(ROLEP)
    f = form_of(P.role[0])
    m = mk('C4', D, 'long')
    return {'stem': f'Based on {src(P)}, write the opening paragraph (about 100–150 words) of your response to this task: “{role_task(P)}” Then explain three choices you made to create an appropriate voice and register for {who(P.role[0])}.',
            'answer': f'Model opening: {P.role[3]} Choices: {FORM_FEATS[f][0]}; {FORM_FEATS[f][1]}; vocabulary and viewpoint that reflect {who(P.role[0])}.',
            'key': level_key(m, f'voice and register in a {f}', f'a convincing, consistent voice for {who(P.role[0])}; form and register fully suited; ideas from the passage woven in; three precise, well-explained choices.',
                             'appropriate voice and register for most of the paragraph; choices explained in general terms.', 'register insecure or inconsistent; explanations vague or missing.',
                             f'{FORM_FEATS[f][0]}; {FORM_FEATS[f][1]}; details such as ' + ', '.join(i[1] for i in P.role[2][:2]) + '.'), 'marks': m, 'type': 'long'}


# ---------------------------------------------------------------- 5.4 evaluating viewpoints
t54 = topic('Evaluating viewpoints and attitudes in a text', 'evaluating viewpoints and attitudes in a text', 'viewpoints attitudes')
VIEWP = [p for p in ALL if p.view and len([x for x in p.fo if x[1] == 'opinion']) >= 1 and len([x for x in p.fo if x[1] == 'fact']) >= 1]
t54.fixed('C1', (1, 2), [
    ('Which is an opinion?', 'The museum deserves its crowds.', 'A judgement that can be disagreed with.', ['The museum is in a converted cargo ship.', 'The queue lasted forty minutes.', 'A sandwich and a juice cost eight euros.']),
    ('What is bias?', 'A one-sided presentation that favours one viewpoint', 'Bias = unbalanced selection or language.', ['A balanced weighing of both sides', 'A list of facts with no opinions', 'A type of summary']),
    ('Which technique most often signals a writer’s attitude?', 'Emotive word choices', 'Loaded vocabulary reveals attitude.', ['Page numbers', 'Paragraph indentation', 'The font used']),
    ('When evaluating a viewpoint, you should consider', 'how well the evidence supports the writer’s claims', 'Evaluate = judge strength and support.', ['only whether you like the writer', 'the length of the article', 'how many paragraphs it has']),
])


@add(t54, 'C1', (1, 2, 3))
def t54_fo(r, D):
    P = r.choice(VIEWP)
    op = r.choice([x for x in P.fo if x[1] == 'opinion'])[0]
    facts = []
    for f in [x[0] for x in P.fo if x[1] == 'fact'] + [f[0] for f in P.facts]:
        if not any(f.lower() in g.lower() or g.lower() in f.lower() for g in facts + [op]):
            facts.append(f)
    opts, ans = mcq(r, cap(op), [cap(f) for f in facts])
    return {'stem': f'Which of these extracts from {src(P)} expresses an opinion rather than a fact?', 'options': opts, 'answer': ans, 'key': f'{Q(op)} is a judgement that could be disputed; the others can be checked or verified.'}


@add(t54, 'C2', (1, 2, 3, 4), 'explain')
def t54_att(r, D):
    P = r.choice(VIEWP)
    loc, how = r.choice(P.view[1])
    m = max(2, mk('C2', D))
    return {'stem': r.choice([f'What is the writer’s attitude in {src(P)}? Explain with reference to: {Q(sent(P, loc))}', f'{lead(r, P)} {Q(sent(P, loc))} What does this reveal about the writer’s viewpoint?']),
            'answer': f'The writer is {P.view[0]}. The words {Q(loc)} show this ({how}).', 'key': f'{upto(m)}: 1 mark: attitude ({P.view[0]}); 1 mark: explanation of how the quotation shows it ({how}).', 'marks': m}


@add(t54, 'C3', (1, 2, 3, 4, 5), 'short')
def t54_parts(r, D):
    P = r.choice(VIEWP)
    fa = r.choice([x for x in P.fo if x[1] == 'fact'])
    op = r.choice([x for x in P.fo if x[1] == 'opinion'])
    vl, how = r.choice(P.view[1])
    intro = f'{lead_x(r, P)} “{ext(P, [fa[0], op[0], vl])}”'
    parts = [lambda r: ('Identify one fact from the extract.', Q(fa[0]), f'{fa[0]} (any verifiable statement) [1]'),
             lambda r: ('Identify one opinion from the extract.', Q(op[0]), f'{op[0]} (any judgement) [1]'),
             lambda r: ('Explain how the writer uses a fact to support their viewpoint.', f'{cap(fa[0])} gives verifiable support, making the writer’s view seem reasonable and evidence-based.', 'fact linked to view [2]'),
             lambda r: ('Summarise the writer’s overall attitude, with a brief reference to the text.', f'{cap(P.view[0])}: {how} ({Q(vl)}).', f'attitude + evidence [2]')]
    return compose(r, intro, parts, k=(2, 3) if D <= 3 else (4,), type_='short')


@add(t54, 'C4', (2, 3, 4, 5), 'long')
def t54_eval(r, D):
    P = r.choice(VIEWP)
    m = mk('C4', D, 'long')
    ev = ' '.join(f'{Q(l)} – {h}.' for l, h in P.view[1])
    facts = '; '.join(x[0] for x in P.fo if x[1] == 'fact')
    ops = '; '.join(x[0] for x in P.fo if x[1] == 'opinion')
    return {'stem': f'{full(P)} How convincingly does the writer present their views? In your answer, identify the main viewpoint and attitudes; evaluate how well they are supported by facts, examples and language; and reach your own reasoned judgement.',
            'answer': f'Viewpoint: {P.view[0]}. Support: facts such as {facts}. Opinions: {ops}. Methods: {ev} Judgement: e.g. largely convincing because claims are backed by specific details, though some statements are opinion rather than evidence.',
            'key': level_key(m, 'evaluating viewpoints (R3)', 'clear grasp of viewpoint and attitudes; evaluation distinguishes fact from opinion and judges the strength of evidence and the effect of language; a sustained, well-supported judgement.',
                             'identifies viewpoint and some methods with some evaluation; judgement partly supported.', 'mainly retells the content; little evaluation.', f'{P.view[0]}; facts: {facts}; opinions: {ops}; {ev}'),
            'marks': m, 'type': 'long'}


CHAPTERS[5] = [t51, t52, t53, t54]


# =========================================================== 6 Reading practice and exam technique

def tmins(m):
    return f'{int(round(m * 1.5))} minutes'


def practice_parts(P, D):
    """(loc, part) pairs covering every Paper 1 Question 1/3 skill for passage P."""
    out = [(f[0], fact_part(P, f)) for f in P.facts[:2]]
    if P.infer:
        out.append((P.infer[-1][0], infer_part(P, P.infer[-1], 3 if D >= 4 else 2)))
    if P.phrase:
        out.append((P.phrase[-1][0], phrase_part(P, P.phrase[-1])))
    if P.vocab:
        out.append((P.vocab[-1][0], vocab_part(P, P.vocab[-1])))
    if P.effects:
        out.append((P.effects[-1][0], effect_part(P, P.effects[-1], 3 if D >= 4 else 2)))
    if P.figs:
        out.append((P.figs[-1][0], fig_part(P, P.figs[-1])))
    if P.struct:
        out.append((P.struct[-1][0], struct_part(P, P.struct[-1])))
    return out


def practice_c3(cats):
    def fn(r, D):
        P = r.choice([p for p in ALL if p.cat in cats])
        pp = practice_parts(P, D)
        sel = r.sample(pp, min(len(pp), 2 if D <= 2 else 3))
        sel.sort(key=lambda x: sidx(P, x[0]))
        x = ext(P, [l for l, _ in sel])
        q = compose(r, f'Timed practice ({{T}}) on {src(P)}. Extract: “{x}”', [f for _, f in sel], k=(len(sel),))
        if not q:
            return None
        q['stem'] = q['stem'].replace('{T}', tmins(q['marks']))
        q['type'] = 'short'
        return q
    return fn


def practice_c4(cats, label):
    def fn(r, D):
        P = r.choice([p for p in ALL if p.cat in cats])
        parts = [f for _, f in practice_parts(P, D)]
        if P.summary:
            parts.append(lambda r: (f'Using your own words, list three points the text makes about {P.summary[0]}.', '; '.join(cap(x[1]) for x in P.summary[1][:3]) + '.', '1 mark per point in own words [3]'))
        q = compose(r, f'Timed practice on {label}: allow about {{T}}. {full(P)}', parts, k=(4, 5) if D >= 4 else (3, 4), type_='multi_step')
        if q:
            q['stem'] = q['stem'].replace('{T}', tmins(q['marks']))
        return q
    return fn


# ---------------------------------------------------------------- 6.1 fiction and literary non-fiction
t61 = topic('Timed practice on fiction and literary non-fiction passages', 'timed practice on fiction and literary non-fiction passages', 'fiction literary non-fiction')
t61.fixed('C1', (1, 2), [
    ('In a fiction passage, which details usually reveal a character’s feelings most effectively?', 'Their actions, speech and reactions', 'Show, don’t tell: inference from behaviour.', ['The page number', 'The title only', 'The number of paragraphs']),
    ('Literary non-fiction differs from a short story because it', 'describes real experiences, often using literary techniques', 'E.g. memoir, travel writing.', ['is always written in the future tense', 'never uses imagery', 'contains only statistics']),
    ('Before answering questions on a fiction passage, you should first', 'read the whole passage to understand the situation and characters', 'Skim then read closely.', ['answer the last question first', 'count the dialogue lines', 'read only the first paragraph']),
    ('Which question type is most likely to appear on a fiction passage?', 'What does the character’s action suggest about how they feel?', 'Inference on character is typical.', ['What are the report’s recommendations?', 'Which subheading introduces the findings?', 'What statistics are given?']),
])


@add(t61, 'C1', (1, 2, 3))
def t61_mcq(r, D):
    P = r.choice([p for p in pool('infer') if p.cat in NARR])
    loc, q, a, dis, ev = r.choice(P.infer)
    opts, ans = mcq(r, a, dis)
    return {'stem': f'Timed practice (1 minute): in {src(P)}, {Q(sent(P, loc))} {q}', 'options': opts, 'answer': ans, 'key': f'{a} ({ev}).'}


@add(t61, 'C2', (1, 2, 3, 4), 'explain')
def t61_c2(r, D):
    P = r.choice([p for p in pool('effects') if p.cat in NARR])
    ph, sug, ana, plain = r.choice(P.effects)
    m = max(2, mk('C2', D))
    return {'stem': f'Timed practice ({tmins(m)}): in {src(P)} the writer writes {Q(sent(P, ph))} What does {Q(ph)} suggest, and why is it more effective than {Q(plain)}?',
            'answer': ana, 'key': f'{upto(m)}: meaning in context ({sug}); effect beyond the plain alternative. Indicative: {ana}', 'marks': m}


add(t61, 'C3', (1, 2, 3, 4, 5), 'short')(practice_c3(NARR))
add(t61, 'C4', (2, 3, 4, 5), 'multi_step')(practice_c4(NARR, 'a fiction or literary non-fiction passage'))


# ---------------------------------------------------------------- 6.2 non-fiction
t62 = topic('Timed practice on non-fiction: articles, reports and blogs', 'timed practice on non-fiction: articles, reports and blogs', 'non-fiction articles reports blogs')
t62.fixed('C1', (1, 2), [
    ('When reading a report under timed conditions, which features help you find information fastest?', 'Subheadings and topic sentences', 'They signpost content.', ['Adjectives', 'Quotation marks', 'Commas']),
    ('A blog differs from a report mainly because a blog', 'uses a personal, informal voice', 'Blogs are conversational.', ['always contains numbered recommendations', 'is written in the third person only', 'never expresses opinions']),
    ('In a news article, where are the key facts usually found?', 'In the opening sentence or paragraph', 'News leads with the key facts.', ['In the final quotation only', 'In the headline’s punctuation', 'In a footnote']),
    ('Why is it important to distinguish fact from opinion when reading articles?', 'To judge how far the writer’s claims are supported', 'Evaluating viewpoints (R3).', ['Because opinions are always wrong', 'Because facts never appear in articles', 'Because examiners only ask about facts']),
])


@add(t62, 'C1', (1, 2, 3))
def t62_mcq(r, D):
    P = r.choice([p for p in pool('facts') if p.cat in NONF])
    loc, q, a, dis = r.choice(P.facts)
    opts, ans = mcq(r, a, dis)
    return {'stem': f'Timed practice (1 minute) on the {P.kind} {Q(P.title)}: {Q(sent(P, loc))} {q}', 'options': opts, 'answer': ans, 'key': a}


@add(t62, 'C2', (1, 2, 3, 4), 'explain')
def t62_c2(r, D):
    P = r.choice([p for p in VIEWP if p.cat in NONF])
    op = r.choice([x for x in P.fo if x[1] == 'opinion'])[0]
    m = max(2, mk('C2', D))
    return {'stem': f'Timed practice ({tmins(m)}): in {src(P)} the writer states {Q(sent(P, op))} Explain whether {Q(op)} is a fact or an opinion, and how it contributes to the writer’s viewpoint.',
            'answer': f'It is an opinion – a judgement that could be disputed. It reveals the attitude that the writer is {P.view[0]}.', 'key': f'{upto(m)}: 1 mark: opinion with reason; 1 mark: link to viewpoint ({P.view[0]}).', 'marks': m}


add(t62, 'C3', (1, 2, 3, 4, 5), 'short')(practice_c3(NONF))
add(t62, 'C4', (2, 3, 4, 5), 'multi_step')(practice_c4(NONF, 'a non-fiction text'))


# ---------------------------------------------------------------- 6.3 planning time and marks
t63 = topic('Planning time and marks across the four Paper 1 questions', 'planning time and marks across the four paper 1 questions', 'planning time marks')
PAPER = 'Paper 1 (Reading) lasts 2 hours and carries 80 marks: four compulsory questions of 20 marks each (comprehension, summary, language task, extended response).'
t63.fixed('C1', (1, 2), [
    ('How long is Paper 1 (Reading) in this course?', '2 hours', PAPER, ['1 hour 30 minutes', '2 hours 30 minutes', '1 hour']),
    ('How many marks does Paper 1 carry in total?', '80', PAPER, ['40', '50', '100']),
    ('If all four Paper 1 questions carry equal marks, how many marks is each worth?', '20', '80 ÷ 4 = 20.', ['10', '25', '40']),
    ('Roughly how many minutes per mark does a 2-hour, 80-mark paper allow?', '1.5 minutes', '120 ÷ 80 = 1.5 minutes per mark.', ['1 minute', '2 minutes', '0.5 minutes']),
    ('Which question in Paper 1 is mainly a test of writers’ effects (R4)?', 'The language task (Question 3)', 'Q3 analyses language.', ['The summary (Question 2)', 'The comprehension questions (Question 1)', 'None of them']),
])


@add(t63, 'C1', (1, 2, 3))
def t63_rate(r, D):
    T, M = r.choice([(120, 80), (90, 60), (120, 60), (105, 70), (100, 80), (135, 90), (80, 80), (75, 50), (120, 96), (60, 40)])
    v = T / M
    opts, ans = mcq(r, f'{fmt(v)} minutes', [f'{fmt(x)} minutes' for x in (M / T, v * 2, v / 2, v + 1, v + 0.5, T - M) if abs(x - v) > 1e-9 and x > 0])
    return {'stem': f'A reading paper lasts {T} minutes and carries {M} marks. If time is spread evenly, how many minutes should be spent per mark?', 'options': opts, 'answer': ans,
            'key': f'{T} ÷ {M} = {fmt(v)} minutes per mark.'}


t63.fixed('C2', (2, 3), [
    ('Explain why it is unwise to spend 50 minutes on the first 20-mark question of a 2-hour, 80-mark paper.', 'The fair share is about 30 minutes; overrunning leaves too little time for the later questions, where easy marks may be lost.',
     '1 mark: fair share ≈ 30 min (20 × 1.5); 1 mark: consequence for later questions. [2]'),
    ('Explain why you should leave a few minutes at the end of Paper 1 to check your answers.', 'Checking lets you correct errors, confirm word limits and complete unfinished points, which can recover marks cheaply.',
     '1 mark: correcting errors/word count; 1 mark: marks gained for little time. [2]'),
    ('Explain how the marks for each part of Question 1 should guide your time.', 'Spend time in proportion to marks: a 1-mark retrieval needs seconds; a 3-mark inference needs a developed answer; this keeps time balanced.',
     '1 mark: proportional time; 1 mark: example. [2]'),
])


@add(t63, 'C2', (1, 2, 3, 4), 'explain')
def t63_over(r, D):
    T, M, n = 120, 80, 4
    q = r.choice([1, 2, 3, 4])
    x = r.choice([40, 45, 50, 55])
    fair = T / n
    left = T - x
    m = max(2, mk('C2', D))
    return {'stem': f'{PAPER} A student spends {x} minutes on Question {q}. Explain the problem this creates, using a calculation.',
            'answer': f'Fair share per question ≈ {T} ÷ {n} = {fmt(fair)} minutes, so the student has overrun by {fmt(x - fair)} minutes and has only {left} minutes for the other {n - 1} questions (≈ {fmt(left / (n - 1))} minutes each instead of {fmt(fair)}).',
            'key': f'{upto(m)}: 1 mark: fair share {fmt(fair)} min; 1 mark: remaining {left} min ÷ {n - 1} = {fmt(left / (n - 1))} min; further mark: consequence (rushed later answers).', 'marks': m}


@add(t63, 'C3', (1, 2, 3, 4, 5), 'numerical')
def t63_plan(r, D):
    T = 120
    R = r.choice([10, 15, 20])
    K = r.choice([0, 5, 10]) if D >= 2 else 0
    marks = r.choice([(20, 20, 20, 20), (15, 25, 20, 20), (20, 15, 25, 20), (25, 20, 15, 20)]) if D >= 3 else (20, 20, 20, 20)
    A = T - R - K
    per = A / 80
    alloc = [int(mm * per + 0.5) for mm in marks]
    intro = f'A student plans their time for Paper 1 ({T} minutes, 80 marks). They allow {R} minutes to read the passages' + (f' and {K} minutes at the end to check.' if K else '.') + f' The four questions carry {marks[0]}, {marks[1]}, {marks[2]} and {marks[3]} marks.'
    parts = [lambda r: ('Calculate the time available for writing answers.', f'{A} minutes', f'{T} − {R}' + (f' − {K}' if K else '') + f' = {A} [1]'),
             lambda r: ('Calculate the time available per mark.', f'{fmt(per)} minutes', f'{A} ÷ 80 = {fmt(per)} min per mark [1]'),
             lambda r: ('Calculate, to the nearest minute, how long the student should spend on each question.', ', '.join(f'Q{i + 1}: {a} min' for i, a in enumerate(alloc)), 'marks × time per mark, e.g. ' + f'{marks[0]} × {fmt(per)} ≈ {alloc[0]} [2]'),
             lambda r: ('Explain why the student should still move on if a question is unfinished when its time is up.', 'Later questions carry marks that are easier to gain at the start of an answer than the last marks of an overrun one.', 'diminishing returns / later marks [1]')]
    return compose(r, intro, parts, k=(2,) if D <= 1 else (3,) if D <= 3 else (4,), type_='numerical')


@add(t63, 'C4', (2, 3, 4, 5), 'multi_step')
def t63_rescue(r, D):
    T, R = 120, r.choice([10, 15])
    x = r.choice([38, 40, 42, 45])
    used = R + x
    left = T - used
    per = left / 60
    a2 = int(20 * per + 0.5)
    intro = f'{PAPER} A student read the passages for {R} minutes and then spent {x} minutes on Question 1. There are {left} minutes left for Questions 2, 3 and 4 (20 marks each).'
    parts = [lambda r: ('Calculate the time per mark the student now has for the remaining questions.', f'{fmt(per)} minutes per mark', f'{left} ÷ 60 = {fmt(per)} [2]'),
             lambda r: ('Calculate, to the nearest minute, the time for each remaining question.', f'about {a2} minutes each', f'20 × {fmt(per)} ≈ {a2} [1]'),
             lambda r: ('Compare this with the time they would have had with an even plan, and explain the effect.', f'An even plan gives ({T} − {R}) ÷ 80 = {fmt((T - R) / 80)} min per mark, i.e. {int(20 * (T - R) / 80 + 0.5)} min per question; they now have {a2 - int(20 * (T - R) / 80 + 0.5)} minutes per question less, so later answers may be rushed or incomplete.', 'calculation + consequence [2]'),
             lambda r: ('Suggest and justify a strategy for the remaining time.', 'Plan the summary and extended response briefly, cover every bullet or focus point at least briefly, and stick strictly to the new time per question; partial answers to all questions earn more than a perfect answer to one.', 'sensible, justified strategy [2]')]
    return compose(r, intro, parts, k=(3, 4), type_='multi_step')


# ---------------------------------------------------------------- 6.4 self-assessment R1–R5
t64 = topic('Self-assessment against R1–R5 reading objectives', 'self-assessment against r1–r5 reading objectives', 'self-assessment reading objectives')
ROBJ = {'R1': 'demonstrate understanding of explicit meanings', 'R2': 'demonstrate understanding of implicit meanings and attitudes',
        'R3': 'analyse, evaluate and develop facts, ideas and opinions, using appropriate support from the text', 'R4': 'demonstrate understanding of how writers achieve effects and influence readers',
        'R5': 'select and use information for specific purposes'}
QMAP = {1: ('comprehension', 'R1, R2'), 2: ('summary', 'R1, R5'), 3: ('language task', 'R4'), 4: ('extended response', 'R1, R2, R3')}
TASK_R = [('Give two details from the passage that show the market was busy.', 'R1'), ('Identify the time at which the ferry left.', 'R1'), ('Using your own words, explain what the writer means by ‘burst its banks’.', 'R1'),
          ('What does Grandfather’s silence suggest about his feelings?', 'R2'), ('What can you infer about Sipho from the fact that he keeps his boots by the front door?', 'R2'), ('Explain what the writer’s attitude to the floodlights is.', 'R2'),
          ('Explain how the writer uses language to convey the danger of the storm.', 'R4'), ('Explain the effect of the simile ‘like a shield’.', 'R4'), ('Analyse the effect of the short sentence ‘Then the wind arrived.’', 'R4'),
          ('Write a summary of the benefits of urban beekeeping.', 'R5'), ('Select the points relevant to the causes of canteen food waste.', 'R5'), ('Select details about the volunteers’ tasks for a summary.', 'R5'),
          ('Evaluate how convincingly the writer argues that homework should be reduced.', 'R3'), ('Writing as the flatmate, develop and comment on the blogger’s claims about smartphones.', 'R3'),
          ('Develop the idea that the eco-club’s action will benefit future pupils, in a speech written in role.', 'R3')]


@add(t64, 'C1', (1, 2, 3))
def t64_task(r, D):
    task, R = r.choice(TASK_R)
    opts, ans = mcq(r, R, [x for x in ROBJ if x != R])
    return {'stem': f'Which reading objective is mainly tested by this task? “{task}”', 'options': opts, 'answer': ans, 'key': f'{R}: {ROBJ[R]}.'}


@add(t64, 'C1', (1, 2, 3))
def t64_def(r, D):
    R = r.choice(list(ROBJ))
    opts, ans = mcq(r, cap(ROBJ[R]), [cap(v) for k, v in ROBJ.items() if k != R])
    return {'stem': f'What does reading objective {R} require you to do?', 'options': opts, 'answer': ans, 'key': f'{R}: {ROBJ[R]}.'}


SELF = [('My summary was 210 words long and included three examples and two quotations.', 'R5', 'selection for a specific purpose was weak: examples and quotations were included instead of key points (also concision in writing).', 'Select only points that answer the focus; cut examples; keep within the word limit.'),
        ('For ‘What does this suggest about her feelings?’ I copied the sentence and wrote “this shows she is sad.”', 'R2', 'the inference is undeveloped and unsupported by explanation of the evidence.', 'State the inference precisely and explain how the quoted words suggest it.'),
        ('In the language task I wrote that every word “makes the reader want to read on”.', 'R4', 'comments on effect are generic and do not explain meaning or connotation.', 'Explain the meaning in context, the connotations and the specific effect of each choice.'),
        ('In my letter in role I retold the passage in order and did not add anything.', 'R3', 'ideas were not developed or evaluated.', 'Infer motives, feelings and consequences from details and comment on them in role.'),
        ('I wrote that the ferry left at seven, but the passage says nine.', 'R1', 'explicit information was misread.', 'Scan carefully for the key word and check the detail before writing it.'),
        ('I lost marks on own-words questions because I repeated the writer’s phrases.', 'R1', 'understanding of explicit meaning was not shown in own words.', 'Paraphrase the meaning using synonyms and check no key word is repeated.'),
        ('I said the writer of the opinion article was neutral, but my teacher said she was strongly critical.', 'R2', 'the writer’s attitude was misjudged.', 'Look for emotive language and concessions to judge attitude.'),
        ('In my evaluation I just agreed with the writer without discussing the evidence.', 'R3', 'evaluation was missing.', 'Judge how well facts and examples support each claim before giving your view.')]


@add(t64, 'C2', (1, 2, 3, 4), 'explain')
def t64_self(r, D):
    s, R, why, fix = r.choice(SELF)
    m = max(2, mk('C2', D))
    return {'stem': r.choice([f'A student writes in their self-assessment: ‘{s}’ Which reading objective (R1–R5) do they most need to improve, and why?', f'‘{s}’ Identify the reading objective this comment shows weakness in, explain the problem and suggest a target.']),
            'answer': f'{R} ({ROBJ[R]}): {why} Target: {fix}', 'key': f'{upto(m)}: 1 mark: {R}; 1 mark: explanation ({why}); further mark: specific target ({fix}).', 'marks': m}


@add(t64, 'C3', (1, 2, 3, 4, 5), 'numerical')
def t64_scores(r, D):
    sc = [r.randint(8, 18) for _ in range(4)]
    lo = min(range(4), key=lambda i: (sc[i], i))
    if sc.count(sc[lo]) > 1:
        sc[lo] -= 1
    tot = sum(sc)
    pct = [round(100 * s / 20) for s in sc]
    name, objs = QMAP[lo + 1]
    intro = f'In a practice Paper 1 (four questions, 20 marks each), a student scored: Q1 comprehension {sc[0]}/20, Q2 summary {sc[1]}/20, Q3 language task {sc[2]}/20, Q4 extended response {sc[3]}/20.'
    parts = [lambda r: ('Calculate the total mark and the overall percentage.', f'{tot}/80 = {fmt(100 * tot / 80, 1)}%', f'{"+".join(map(str, sc))} = {tot}; {tot} ÷ 80 × 100 = {fmt(100 * tot / 80, 1)}% [2]'),
             lambda r: ('Calculate the percentage for each question.', ', '.join(f'Q{i + 1} {p}%' for i, p in enumerate(pct)), 'each mark ÷ 20 × 100 [1]'),
             lambda r: ('Identify the weakest question and the reading objectives it mainly tests.', f'Q{lo + 1} ({name}): {objs}', f'Q{lo + 1}; {objs} [1]'),
             lambda r: ('Suggest one specific target to improve that question.', {1: 'Answer to the mark allocation: point + evidence for inference questions; precise detail for retrieval.', 2: 'Select only points on the focus and write them concisely in own words.',
                                                                                3: 'Choose precise words/images and explain meaning, connotation and effect.', 4: 'Cover all bullets and develop ideas from the passage in a convincing voice.'}[lo + 1], 'specific, relevant target [1]'),
             lambda r: ('How many more marks would the student need to reach 60/80?', f'{max(0, 60 - tot)} marks', f'60 − {tot} = {max(0, 60 - tot)} [1]')]
    return compose(r, intro, parts, k=(2,) if D <= 1 else (3,) if D <= 3 else (4, 5), type_='numerical')


@add(t64, 'C4', (2, 3, 4, 5), 'multi_step')
def t64_profile(r, D):
    a = r.randint(4, 9)    # Q1 retrieval /10 (R1)
    b = r.randint(2, 8)    # Q1 inference /10 (R2)
    c = r.randint(4, 9)    # Q2 content /10 (R5)
    d = r.randint(3, 9)    # Q3 /20 (R4) halved below
    d2 = d * 2
    e = r.randint(3, 9)    # Q4 reading /10 (R3)
    vals = {'R1 (Q1 retrieval)': a * 10, 'R2 (Q1 inference)': b * 10, 'R5 (Q2 summary content)': c * 10, 'R4 (Q3 language)': round(100 * d2 / 20), 'R3 (Q4 reading)': e * 10}
    srt = sorted(vals.items(), key=lambda kv: (kv[1], kv[0]))
    intro = (f'A student’s Paper 1 marks are broken down by objective: Q1 retrieval {a}/10 (R1), Q1 inference {b}/10 (R2), Q2 summary content {c}/10 (R5), Q3 language task {d2}/20 (R4), Q4 reading {e}/10 (R3).')
    parts = [lambda r: ('Convert each score to a percentage.', ', '.join(f'{k} {v}%' for k, v in vals.items()), 'all five correct [2]'),
             lambda r: ('Identify the two weakest objectives.', f'{srt[0][0]} and {srt[1][0]}', f'{srt[0][0]}; {srt[1][0]} [1]'),
             lambda r: ('For each of the two weakest objectives, set a specific target and describe one practice activity.', f'{srt[0][0].split()[0]}: {ROBJ[srt[0][0].split()[0]]} – targeted practice with model answers; {srt[1][0].split()[0]}: {ROBJ[srt[1][0].split()[0]]} – timed practice and self-marking against the mark scheme.',
                        '1 mark per relevant target + 1 per suitable activity [4]'),
             lambda r: ('Evaluate whether the student should spend more revision time on Question 3 or Question 1, using the figures.', 'Compare the R4 percentage with the average of R1 and R2: the lower area, with more marks available, should get more time.', 'uses figures; reasoned judgement [2]')]
    return compose(r, intro, parts, k=(3, 4), type_='multi_step')


CHAPTERS[6] = [t61, t62, t63, t64]


def _fixed_marks():
    """Fixed open items carry their tariff in a trailing [n]; make the item marks match it."""
    for ts in CHAPTERS.values():
        for t in ts:
            for tp in t.templates:
                if tp.name != 'fixed':
                    continue

                def g(r, D, f=tp.fn):
                    q = f(r, D)
                    mm = re.findall(r'\[(\d+)\]', q['key'])
                    if mm and not q.get('options'):
                        q['marks'] = int(mm[-1])
                    return q
                tp.fn = g


_fixed_marks()
