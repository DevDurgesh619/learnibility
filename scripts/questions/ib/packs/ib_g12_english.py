"""IB DP English A: Language and Literature SL/HL – ib-g12-english (DP year 2).

Year 2: the Intertextuality area of exploration (allusion, parody, adaptation, genre), remaining literary
works (novel, short stories / poetry in translation, graphic novel or literary non-fiction), non-literary
bodies of work (adaptation across media, satire and parody, campaigns and public communication),
Paper 2 comparative essay preparation and writing, the HL essay, Paper 1 consolidation and final revision.

This pack reuses the passage library, question-frame helpers, Paper 1/Paper 2 mock templates and markbands
of ib_g11_english.py (loaded as a base module with a fresh registry) and adds year-2 passages: satirical
columns, cartoons, parody advertisements, campaign posters, charity appeals, a manifesto, screenplay and
shot-list extracts, graphic novel pages described in words, memoir, testimony, short stories, fan fiction,
reviews and poems. All passages are original unless attributed (brief public-domain quotations only).
"""
from __future__ import annotations

import importlib.util
import os

from _common import F, Registry, T, mcq

_spec = importlib.util.spec_from_file_location('_ib_g11_english_base', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ib_g11_english.py'))
base = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(base)

# Fresh registry: helpers in the base module look up R / PASS at call time, so rebinding base.R sends
# every registration below to this pack only (the year-1 content is not reused for year-2 subtopics).
R = Registry()
base.R = R
P, pq, pq_dev_mcq, pq_tone_mcq, pq_kind_mcq, pq_para = base.P, base.pq, base.pq_dev_mcq, base.pq_tone_mcq, base.pq_kind_mcq, base.pq_para
PASS, P2Q, NONLIT, LIT, VISUAL = base.PASS, base.P2Q, base.NONLIT, base.LIT, base.VISUAL
MARKBAND, P1_BANDS, P2_BANDS, CRIT_A, CRIT_B, CRIT_OPEN = base.MARKBAND, base.P1_BANDS, base.P2_BANDS, base.CRIT_A, base.CRIT_B, base.CRIT_OPEN
AUD_Q, PURP_Q, CTX_Q, DEV_Q, STRUCT_Q, READ_Q, VIS_Q, ISSUE_Q, CONCEPT_Q = (base.AUD_Q, base.PURP_Q, base.CTX_Q, base.DEV_Q, base.STRUCT_Q,
                                                                          base.READ_Q, base.VIS_Q, base.ISSUE_Q, base.CONCEPT_Q)
STYLE = base.STYLE

CONFIG = {'minutesPerMark': 2.5, 'mcqMinutes': 1.5}

# One mock = HL Paper 1 (two unseen non-literary texts, 20 marks each) + Paper 2 (30 marks) split into
# planning (2 x 5) and comparative analysis (2 x 10). 6 items, 70 marks per mock.
MOCK = [
    dict(section='Paper 1 – Guided textual analysis, Text 1 (criteria A–D)', count=1, c=['C4'], d=[4, 5], type='long', marks=20, style='p1', chapters=[12, 13]),
    dict(section='Paper 1 (HL) – Guided textual analysis, Text 2 (criteria A–D)', count=1, c=['C4'], d=[5, 4], type='long', marks=20, style='p1', chapters=[6, 7, 12]),
    dict(section='Paper 2 – Comparative essay part A: unpacking the question and comparative thesis', count=2, c=['C3', 'C4'], d=[3, 4], type='case', marks=5, style='p2a', chapters=[8, 9]),
    dict(section='Paper 2 – Comparative essay part B: comparative analysis of two literary works', count=2, c=['C4'], d=[4, 5], type='long', marks=10, style='p2b', chapters=[9, 13]),
]


def init(subject_id):
    pass


def templates(st):
    return R.build(st, STYLE) + base.GLOBAL


def H(key, **kw):
    R.facts(key, F(**kw))


# =============================================================================================
# Year-2 passages
# =============================================================================================
P(id='housing', kind='satire', title='satirical column from a news-parody website',
  text=("In a bold move hailed by absolutely everyone in the Cabinet, the government announced today that the housing crisis will henceforth be known as the 'housing opportunity'. "
        "'Language matters,' said the Minister, speaking from the second of his four homes. 'Young people aren't priced out – they're simply enjoying an extended stay with their parents, which is wonderful for family values.' "
        "A spokesperson confirmed that rents would remain the same, but would now feel more optimistic."),
  aud='Readers of a news-parody website who are frustrated with politicians, especially young renters.',
  purp='To ridicule governments that use euphemism and spin instead of policy to deal with the housing crisis.',
  ctx='Rising rents and house prices in many cities have left young adults living with parents; satire sites imitate news style to mock political communication.',
  tone='deadpan', tw=['earnest', 'sentimental', 'alarmed'], tonex='absurd claims reported with a straight face create deadpan irony.',
  dev=[('hyperbole', 'hailed by absolutely everyone in the Cabinet', 'the exaggerated praise, limited to the Cabinet itself, exposes self-congratulation', ['simile', 'onomatopoeia', 'statistic']),
       ('ironic juxtaposition', 'speaking from the second of his four homes', 'the detail undercuts the Minister\'s authority and exposes hypocrisy', ['simile', 'onomatopoeia', 'rhetorical question']),
       ('mock euphemism', "the 'housing opportunity'", 'the absurd rebranding parodies political spin that renames problems rather than solving them', ['statistic', 'onomatopoeia', 'simile']),
       ('bathos', 'rents would remain the same, but would now feel more optimistic', 'the anticlimax mocks the emptiness of the announcement', ['simile', 'onomatopoeia', 'anaphora'])],
  struct=[('the imitation of news-report structure (announcement, quotation, spokesperson)', 'the familiar format makes the absurd content feel plausible, which sharpens the satire')],
  satire='Target: governments that replace policy with spin. Methods: a deadpan news register, mock euphemism ("housing opportunity"), ironic detail (four homes), and bathos ("feel more optimistic"); incongruity between serious form and absurd content creates the humour.',
  gq='How does the writer use the conventions of news reporting to satirise politicians?',
  gqa=('Thesis: by imitating a neutral news report, the satire lets politicians condemn themselves. (1) Deadpan news structure. (2) Ironic details and quotations exposing hypocrisy. (3) Bathos in the closing line. Evaluation: humour invites agreement but may encourage cynicism rather than action.'),
  issue='Housing inequality and political spin.',
  concept=('representation', 'politicians are represented through their own euphemistic language.'),
  read='Young renters laugh in recognition; a government supporter may see unfair caricature.',
  field='politics, power and justice')

P(id='share', kind='satire', title='satirical news story from a parody website',
  text=("Local man Darren Cole, 41, has once again shown extraordinary courage by sharing a news article on social media without reading beyond the headline. "
        "'I didn't need to,' Cole explained. 'The headline already agreed with me.' Friends describe the gesture as 'very on brand'. "
        "At press time, Cole was furiously defending the article's second paragraph, which he believes says something it does not."),
  aud='Social media users who will recognise the behaviour, possibly in themselves.',
  purp='To mock the habit of sharing without reading and the confirmation bias behind it.',
  ctx='Studies of social media sharing suggest many links are shared without being opened; parody news sites spread this kind of satire on the same platforms.',
  tone='mock-heroic', tw=['tragic', 'reverent', 'bitter'], tonex='heroic diction applied to a trivial act is mock-heroic.',
  dev=[('mock-heroic diction', 'shown extraordinary courage', 'grand praise for a trivial act exposes its laziness', ['statistic', 'onomatopoeia', 'simile']),
       ('ironic quotation', "'The headline already agreed with me.'", 'the man\'s own words expose confirmation bias', ['simile', 'onomatopoeia', 'anaphora']),
       ('news cliché', 'At press time', 'the borrowed newspaper phrase heightens the parody of journalism', ['simile', 'onomatopoeia', 'rhetorical question'])],
  struct=[('the escalation to the final sentence', 'the joke builds to the absurd image of defending a paragraph he has not read')],
  satire='Target: confirmation bias and careless sharing. Methods: mock-heroic diction, an "everyman" figure, ironic self-incrimination in quotation, parody of news clichés; the reader is invited to recognise themselves.',
  misinfo='The satire exposes how misinformation spreads: people share headlines that confirm beliefs and defend claims they have not checked.',
  gq='How does the satire criticise the way people engage with news online?',
  gqa=('Thesis: the piece mocks confirmation bias by celebrating it. (1) Mock-heroic diction. (2) Self-incriminating quotation. (3) Parody of news clichés and escalating absurdity. Evaluation: the gentle target (an ordinary man) invites self-recognition rather than blame.'),
  issue='Misinformation and confirmation bias online.',
  concept=('communication', 'the satire exposes how communication online replaces reading with reacting.'),
  read='Readers may laugh at Darren or uncomfortably recognise themselves.',
  field='science, technology and the environment')

P(id='emperor', kind='cartoon', title='editorial cartoon, described in words',
  text=("[A technology billionaire stands on a vast stage wearing nothing but a branded lanyard, arms raised in triumph. A giant screen behind him reads 'REVOLUTIONARY'. "
        "Rows of investors in suits applaud wildly. In the front row a small child holds up a hand-written sign: 'IT'S JUST A PHONE.']"),
  aud='Newspaper readers sceptical of technology hype.',
  purp='To satirise the hype surrounding technology launches and the audience who applauds it.',
  ctx='Product launches by technology companies are staged as spectacular events; the cartoon relies on readers knowing Hans Christian Andersen\'s tale "The Emperor\'s New Clothes" (1837).',
  tone='satirical', tw=['admiring', 'neutral', 'nostalgic'], tonex='exaggeration and allusion make it satirical.',
  dev=[('allusion', "a small child holds up a hand-written sign: 'IT'S JUST A PHONE.'", 'it recalls the child in Andersen\'s tale who says the emperor has no clothes, casting the billionaire as a vain emperor and investors as courtiers', ['statistic', 'onomatopoeia', 'simile']),
       ('exaggeration', "wearing nothing but a branded lanyard", 'the near-naked figure visualises the emptiness of the hype', ['statistic', 'onomatopoeia', 'rhetorical question'])],
  struct=[('the contrast in scale between the giant screen and the small child', 'the tiny truth-teller against the huge display reverses power: the smallest figure is the wisest')],
  visual='The giant screen and arms raised connote spectacle and self-worship; the rows of suited investors form a uniform, uncritical mass; the child in the foreground is the viewer\'s point of identification.',
  satire='Target: technology hype and uncritical investors. Method: allusion to "The Emperor\'s New Clothes" transfers the tale\'s moral (vanity and collective self-deception) to the present.',
  intertext='The cartoon depends on intertextual knowledge of Andersen\'s "The Emperor\'s New Clothes": readers recognise the child\'s honesty and the crowd\'s pretence, so the cartoon\'s meaning comes from mapping the old story onto the new situation.',
  gq='How does the cartoon use an earlier story to criticise technology culture?',
  gqa=('Thesis: by retelling a fairy tale, the cartoon makes hype look like collective self-deception. (1) The near-naked billionaire. (2) Applauding investors as courtiers. (3) The child\'s sign as truth. Evaluation: the allusion works only for readers who know the tale.'),
  issue='Technology, hype and critical thinking.',
  concept=('transformation', 'a nineteenth-century fable is transformed into contemporary satire.'),
  read='Sceptics enjoy it; a technology enthusiast may think it dismisses real innovation.',
  field='science, technology and the environment')

P(id='scales', kind='cartoon', title='editorial cartoon, described in words',
  text=("[A pair of scales of justice. On one pan sits a tiny pile of coins labelled 'Fine for polluting the river'. On the other, a mountain of banknotes labelled 'Annual profit'. "
        "The scales tip violently towards the profit. A very small judge peers up at it and says: 'Well, that'll teach them.']"),
  aud='Readers concerned about corporate responsibility and environmental law.',
  purp='To criticise fines that are too small to change the behaviour of large companies.',
  ctx='Companies are sometimes fined amounts that are small relative to their profits, prompting debate about whether penalties deter pollution.',
  tone='sardonic', tw=['celebratory', 'reverent', 'tender'], tonex='the judge\'s line is sardonic.',
  dev=[('visual metaphor', 'scales of justice', 'the traditional symbol of fairness is shown tipping absurdly, suggesting justice is unbalanced by wealth', ['onomatopoeia', 'statistic', 'rhetorical question']),
       ('irony', "'Well, that'll teach them.'", 'the judge\'s confident words contradict the image, exposing the weakness of the penalty', ['statistic', 'simile', 'onomatopoeia'])],
  struct=[('the contrast in size between the coins and the banknotes', 'scale makes the disproportion instantly visible')],
  visual='Disproportionate size (tiny coins, mountain of notes, small judge) creates the argument visually; labels anchor the meaning.',
  satire='Target: weak corporate penalties and the legal system. Methods: visual metaphor (scales), exaggeration of scale and verbal irony.',
  gq='How does the cartoon communicate its criticism of the justice system?',
  gqa=('Thesis: the cartoon turns justice\'s own symbol against it. (1) The tipping scales. (2) Labels as anchorage. (3) The ironic caption. Evaluation: clear and instant, though it simplifies legal complexity.'),
  issue='Corporate power, pollution and justice.',
  concept=('representation', 'the law is represented as small and powerless before wealth.'),
  read='Environmental readers agree; a business reader may argue fines are only one consequence.',
  field='politics, power and justice')

P(id='wearonce', kind='parody', title='parody advertisement created by a student activist group (culture jamming)',
  text=("[Image: a glossy fashion-advert layout. A model in a neon crop top poses, smiling, in front of a landfill heaped with clothes.]\n"
        "WEAR IT ONCE. POST IT. BIN IT.\n"
        "New season, new you – every week.\n"
        "*Made by someone paid less in a month than this top costs in a day.\n"
        "#OutfitOfTheMinute"),
  aud='Young consumers of fast fashion who will recognise the conventions of fashion advertising and social media.',
  purp='To criticise fast fashion by exaggerating its own advertising conventions until their hidden costs are exposed.',
  ctx='Culture jamming groups produce parodies ("subvertising") of brands to challenge consumer culture; fast fashion has been criticised for waste and low wages.',
  tone='ironic', tw=['sincere', 'reverent', 'neutral'], tonex='the advert says what real adverts hide, creating irony.',
  dev=[('parody of a tricolon slogan', 'WEAR IT ONCE. POST IT. BIN IT.', 'the imperative tricolon mimics brand slogans but spells out the disposable cycle they encourage', ['simile', 'onomatopoeia', 'rhetorical question']),
       ('subverted small print', '*Made by someone paid less in a month than this top costs in a day.', 'the footnote convention, normally used to hide caveats, is used to expose exploitation', ['simile', 'onomatopoeia', 'anaphora']),
       ('parody hashtag', '#OutfitOfTheMinute', 'it exaggerates "outfit of the day" culture to mock ever-faster consumption', ['simile', 'statistic', 'onomatopoeia'])],
  struct=[('the glossy layout combined with a landfill background', 'the familiar format draws the viewer in before the background reveals the critique')],
  visual='The smiling model and neon colour imitate fashion advertising; the landfill behind her juxtaposes glamour and waste.',
  satire='Parody imitates fast-fashion advertising (layout, slogan, hashtag, small print) and exaggerates it, so the genre condemns itself; culture jamming turns the brand\'s language against consumption.',
  intertext='The text depends on the viewer recognising fashion-advert and Instagram conventions ("outfit of the day"); its meaning comes from the gap between the imitated genre and its subversion.',
  gq='How does the parody use the conventions of advertising to criticise fast fashion?',
  gqa=('Thesis: the parody makes advertising tell the truth. (1) The parody slogan. (2) Glossy image against landfill. (3) Subverted small print and hashtag. Evaluation: effective for media-literate youth, but risks being shared as a joke rather than prompting change.'),
  issue='Fast fashion, waste and labour exploitation.',
  concept=('transformation', 'advertising conventions are transformed into critique.'),
  read='Some will feel guilty and reconsider; others may enjoy the joke and keep shopping.',
  field='science, technology and the environment')

P(id='openjoy', kind='parody', title='altered ("subvertised") billboard for a fictional soft drink, described in words',
  text=("[Original billboard: a smiling teenager drinks from a red can of FIZZ. Slogan: 'OPEN JOY.']\n"
        "[Altered version: the word 'JOY' has been pasted over with 'DECAY' in matching lettering. A sticker beside the can reads: '35 g of sugar – that's about 9 teaspoons.' "
        "The teenager's smile has been left untouched.]"),
  aud='Passers-by, especially young people and parents, at a bus stop.',
  purp='To expose the health cost of sugary drinks by subverting the brand\'s own slogan.',
  ctx='Culture jammers alter real billboards in public spaces; public-health campaigns have targeted sugary drinks.',
  tone='subversive', tw=['flattering', 'neutral', 'nostalgic'], tonex='the altered slogan subverts the advert.',
  dev=[('wordplay', "'OPEN JOY' becomes 'OPEN DECAY'", 'replacing one word in matching lettering keeps the brand\'s voice while reversing its meaning (tooth decay)', ['simile', 'statistic', 'anaphora']),
       ('statistic', '35 g of sugar – that\'s about 9 teaspoons', 'a concrete household measure makes the abstract figure shocking', ['simile', 'onomatopoeia', 'oxymoron']),
       ('irony', "The teenager's smile has been left untouched", 'the unchanged smile now looks naïve, making the viewer see the original image differently', ['statistic', 'onomatopoeia', 'simile'])],
  struct=[('the minimal alteration', 'changing as little as possible makes the critique feel like the advert\'s own confession')],
  visual='Matching lettering makes the alteration look official; the red can and smile retain the advert\'s appeal so the subversion is jarring.',
  satire='Culture jamming: the alteration hijacks the brand\'s slogan and image to expose what the advert conceals (sugar and health).',
  intertext='The meaning depends on recognising the original advert; the altered text is in dialogue with it.',
  gq='How does the altered billboard turn the original advertisement against itself?',
  gqa=('Thesis: minimal alteration makes the brand speak against itself. (1) Wordplay in the slogan. (2) The concrete statistic. (3) The unchanged smile recontextualised. Evaluation: powerful but raises questions about defacing property.'),
  issue='Public health, advertising and young people.',
  concept=('transformation', 'the original advert is transformed into its own critique.'),
  read='Parents may approve; the brand would call it vandalism; teenagers may find it funny.',
  field='science, technology and the environment')

P(id='copy', kind='campaign', title='public-health campaign poster against smoking',
  text=("[Image: a close-up of a toddler's hand reaching for a cigarette packet on a coffee table.]\n"
        "Headline: 'They copy everything you do.'\n"
        "Below: 'Children who grow up with smokers are much more likely to start smoking themselves.'\n"
        "Call to action: 'Quit for them. Free support: QuitLine.'"),
  aud='Adult smokers who are parents or carers of young children.',
  purp='To persuade parents to quit smoking by appealing to their protective feelings towards their children.',
  ctx='Public-health services run anti-smoking campaigns; research links parental smoking with children taking up smoking.',
  tone='poignant', tw=['playful', 'triumphant', 'sarcastic'], tonex='the vulnerable child creates poignancy.',
  dev=[('direct address', "'They copy everything you do.'", 'the second-person "you" confronts the parent, making them responsible', ['simile', 'onomatopoeia', 'oxymoron']),
       ('imperative', "'Quit for them.'", 'the command reframes quitting as an act of love rather than self-denial', ['simile', 'statistic', 'onomatopoeia'])],
  struct=[('the move from image to headline to support line', 'emotion first, evidence second, practical help last')],
  visual='The close-up of a small hand creates vulnerability; the cigarette packet within reach creates tension; the domestic setting places the danger in the home.',
  ethics='The poster uses a child to provoke guilt; it avoids graphic images but could stigmatise parents who smoke; offering free support balances the guilt with help.',
  gq='How does the poster use the image of a child to persuade its audience?',
  gqa=('Thesis: the poster turns parental love into motivation. (1) Close-up of the hand. (2) Direct address and the verb "copy". (3) The imperative and offer of support. Evaluation: guilt can motivate but may alienate.'),
  issue='Public health and family responsibility.',
  concept=('communication', 'a single image communicates a risk faster than statistics.'),
  read='A parent may be moved to quit; another may feel judged and resentful.',
  field='science, technology and the environment')

P(id='drawing', kind='campaign', title='poster from a refugee-aid NGO campaign',
  text=("[Image: a child's crayon drawing of a house with a red roof and a yellow sun, pinned to the canvas wall of a tent. No people are shown.]\n"
        "'Home is a place she has only drawn.'\n"
        "'For three years, Leila has lived in a camp. With your help, her drawing can become an address.'\n"
        "Text HOME to donate."),
  aud='Potential donors who may be weary of images of suffering.',
  purp='To raise donations for refugee housing while preserving the dignity of the child.',
  ctx='Aid campaigns have been criticised for "poverty porn"; some NGOs now use images that avoid showing distressed faces.',
  tone='hopeful', tw=['menacing', 'flippant', 'despairing'], tonex='the drawing and "can become" suggest hope.',
  dev=[('metonymy', "a child's crayon drawing of a house", 'the drawing stands for the child\'s hopes, so she is present without being exposed', ['statistic', 'onomatopoeia', 'rhetorical question']),
       ('antithesis', "'her drawing can become an address'", 'the shift from imagined home to real address frames donation as making a dream concrete', ['simile', 'onomatopoeia', 'statistic'])],
  struct=[('the absence of people in the image', 'leaving the child unseen protects her dignity and lets the viewer imagine her')],
  visual='The bright drawing against the drab tent canvas contrasts hope and reality; the absence of faces avoids exploitation.',
  ethics='The campaign avoids exploitative images of suffering ("poverty porn") by showing the child\'s creativity rather than her body; it names her (Leila) to individualise her, but still positions the donor as the agent of change.',
  gq='How does the poster represent the refugee child, and with what ethical effects?',
  gqa=('Thesis: the poster seeks empathy without exploitation. (1) The drawing as metonymy. (2) Absence of faces. (3) The shift from drawing to address. Evaluation: more dignified than many appeals, though it still centres the donor.'),
  issue='Displacement, refugee rights and ethical representation.',
  concept=('representation', 'the refugee is represented through her imagination rather than her suffering.'),
  read='Donors may find it moving; some may find it too subtle to prompt action.',
  field='politics, power and justice')

P(id='amina', kind='appeal', title='direct-mail appeal letter from an international charity',
  text=("Dear Friend,\nThis is Amina. She is seven. Every morning she walks two hours to collect water that makes her sick.\n"
        "[Photograph: a thin girl with downcast eyes holds a yellow jerrycan.]\n"
        "For just 5 euros a month, you can change Amina's life forever.\nPlease don't turn the page."),
  aud='Potential donors in wealthy countries receiving the letter at home.',
  purp='To prompt an immediate monthly donation through pity and guilt.',
  ctx='Charity appeals compete for attention; critics describe such images as "poverty porn" that reinforce stereotypes of helplessness.',
  tone='pleading', tw=['jubilant', 'sarcastic', 'detached'], tonex='the final imperative makes the tone pleading.',
  dev=[('short declaratives', 'This is Amina. She is seven.', 'simple sentences personalise and create intimacy, as if introducing her', ['simile', 'onomatopoeia', 'oxymoron']),
       ('hyperbole', "change Amina's life forever", 'the exaggerated promise inflates the donor\'s power', ['simile', 'onomatopoeia', 'anaphora']),
       ('emotive imperative', "Please don't turn the page.", 'it makes turning the page feel like abandoning her', ['simile', 'statistic', 'onomatopoeia'])],
  struct=[('the generic greeting "Dear Friend"', 'it imitates personal correspondence to create intimacy with a stranger')],
  visual='Downcast eyes create an "offer" image of passive suffering; the yellow jerrycan is a recognisable symbol of water poverty.',
  ethics='The appeal individualises suffering effectively but represents Amina as helpless and the donor as saviour; the promise of changing her life "forever" for 5 euros oversimplifies poverty and denies her agency.',
  gq='How does the appeal attempt to persuade its readers, and what ethical questions does it raise?',
  gqa=('Thesis: the appeal is persuasive because it is reductive. (1) Personalisation through short sentences. (2) The passive, downcast image. (3) Hyperbole and guilt-inducing imperative. Evaluation: effective fundraising, but it risks stereotyping and a saviour narrative.'),
  issue='Ethics of representation in charity campaigns.',
  concept=('representation', 'the recipient is represented as passive; the donor as saviour.'),
  read='A donor may give; a reader from the region may find the representation demeaning.',
  field='politics, power and justice')

P(id='manifesto', kind='manifesto', title="extract from a youth climate movement's manifesto",
  text=("WE ARE NOT ASKING.\n1. We demand that our city ends approval of new fossil-fuel projects by 2030.\n"
        "2. We demand climate education in every school, in every subject.\n3. We demand a seat at every table where our future is decided.\n"
        "We are told to be patient. Patience is a luxury for those who will not live with the consequences. Join us."),
  aud='Young people who might join the movement, and city leaders who are the target of the demands.',
  purp='To state the movement\'s demands, assert its authority and recruit supporters.',
  ctx='Youth climate movements have used manifestos, strikes and speeches to pressure governments since the late 2010s.',
  tone='uncompromising', tw=['apologetic', 'tentative', 'whimsical'], tonex='"We demand" and "WE ARE NOT ASKING" are uncompromising.',
  dev=[('anaphora', 'We demand ... We demand ... We demand', 'repetition builds collective force and clarity', ['simile', 'onomatopoeia', 'oxymoron']),
       ('aphorism', 'Patience is a luxury for those who will not live with the consequences', 'the memorable generalisation reframes patience as privilege', ['simile', 'onomatopoeia', 'statistic']),
       ('capitalised declaration', 'WE ARE NOT ASKING.', 'the opening refuses the polite register of petitions', ['simile', 'statistic', 'onomatopoeia'])],
  struct=[('the numbered list of demands', 'numbering makes the demands precise, official and checkable'), ('the closing imperative "Join us."', 'it turns the reader from audience into member')],
  gq='How does the manifesto construct a powerful collective voice?',
  gqa=('Thesis: the manifesto replaces requests with demands. (1) Capitalised opening. (2) Numbered anaphoric demands. (3) Aphorism and imperative. Evaluation: forceful and clear, though its uncompromising tone may alienate moderates.'),
  issue='Climate justice and youth political participation.',
  concept=('identity', 'a collective generational identity is constructed through "we".'),
  read='Young readers may feel empowered; politicians may dismiss it as unrealistic.',
  field='politics, power and justice')

P(id='ramps', kind='speech', title='speech by a disability-rights activist at a rally outside a parliament',
  text=("They say we ask for special treatment. Ramps are not special. Captions are not special. A lift that works is not special. "
        "What is special is a parliament with three hundred steps and not one ramp to its public gallery. "
        "We have watched our laws being made from the pavement for long enough. Nothing about us, without us."),
  aud='Rally participants, passers-by, journalists and the legislators inside the building.',
  purp='To demand accessible democratic institutions and reject the framing of access as a special privilege.',
  ctx='Disability-rights movements have long campaigned for accessible public buildings; "Nothing about us without us" is a slogan widely used by the movement.',
  tone='defiant', tw=['grateful', 'resigned', 'whimsical'], tonex='repeated refusals create defiance.',
  dev=[('anaphora / epistrophe', 'Ramps are not special. Captions are not special. A lift that works is not special.', 'the repeated "not special" builds rhythm and dismantles the opponent\'s word', ['simile', 'onomatopoeia', 'oxymoron']),
       ('reversal', 'What is special is a parliament with three hundred steps', 'turning the word "special" against the institution exposes its exclusion', ['simile', 'onomatopoeia', 'rhetorical question']),
       ('slogan (intertextual)', 'Nothing about us, without us.', 'the movement\'s slogan links the speech to a wider history of disability activism', ['simile', 'onomatopoeia', 'statistic'])],
  struct=[('the move from listing to the image of watching laws "from the pavement"', 'the concrete image makes exclusion visible and physical')],
  gq='How does the speaker challenge the idea that access is "special treatment"?',
  gqa=('Thesis: the speaker reclaims the word "special". (1) Repetition of "not special". (2) Reversal onto the parliament. (3) The pavement image and the slogan. Evaluation: the speech is short and quotable, suited to media coverage.'),
  issue='Disability rights and access to democratic participation.',
  concept=('perspective', 'the speech presents the institution from the perspective of those excluded by it.'),
  read='Supporters find it empowering; some may find the tone confrontational.',
  intertext='The closing slogan "Nothing about us without us" is borrowed from the disability-rights movement, connecting the speech to a collective history of activism.',
  field='politics, power and justice')

P(id='screen_river', kind='script', title='screenplay adaptation of the opening of a novel (an original extract written for study)',
  text=("EXT. RIVERBANK – DAY\nSummer. The water is flat and silent. No boats. NINA (9) sits on an upturned crate, scratching marks into the wood with a stone. Fourteen marks.\n"
        "INT. FAMILY KITCHEN – DAY\nBlinds half-drawn. PAPA (40s) asleep at the table, still in factory overalls. MAMA (40s) stirs a pot, watching him.\n"
        "NINA (O.S.)\nFifteen?\nMAMA\n(sharp, not turning)\nNumbers are for people with jobs.\nNina's stone stops."),
  adapt='The novel\'s first-person child narration is lost; instead the film externalises Nina\'s counting as marks on a crate (a visual motif) and shows Papa in factory overalls, so the audience sees the job loss rather than inferring it from a naïve voice. Mama\'s remark becomes direct, sharp dialogue, and "Nina\'s stone stops" turns the child\'s reaction into a silent image.',
  filmlang='Scene headings move from exterior (the silent river) to interior (the dim kitchen), linking setting and mood; the off-screen voice ("O.S.") places Nina outside the adult space; half-drawn blinds create low light and concealment.',
  tone='melancholy', tw=['farcical', 'euphoric', 'triumphant'], tonex='silence and stillness create melancholy.',
  dev=[('visual motif', 'scratching marks into the wood with a stone. Fourteen marks.', 'the marks show the child\'s counting without narration', ['statistic', 'onomatopoeia', 'rhetorical question']),
       ('off-screen voice', 'NINA (O.S.)', 'hearing Nina without seeing her places her on the edge of the adults\' world', ['simile', 'statistic', 'oxymoron'])],
  struct=[('the cut from riverbank to kitchen', 'the edit connects the silent river with the silent house')],
  gq='How does the screenplay transform the novel\'s child narrator for the screen?',
  gqa=('Thesis: the screenplay replaces voice with image. (1) Counting as visual motif. (2) Setting and costume revealing job loss. (3) Direct dialogue and silent reaction. Evaluation: gains immediacy but loses the dramatic irony of a naïve narrator.'),
  issue='Unemployment and its effect on families.',
  concept=('transformation', 'narration is transformed into visual storytelling.'),
  read='Viewers see more directly; readers of the novel may miss the child\'s voice.',
  field='politics, power and justice')

P(id='shotlist', kind='script', title='shot list from a short film (an original extract written for study)',
  text=("SHOT 1 – Extreme long shot: a lone figure crosses a frozen lake at dawn.\nSHOT 2 – Low-angle medium shot: the figure (ELENA, 70s) stops; her breath clouds.\n"
        "SHOT 3 – Extreme close-up: a crack spreads across the ice beneath her boot. Sound: the crack amplified; the wind drops out.\n"
        "SHOT 4 – Cut to black. Silence."),
  filmlang='The extreme long shot makes Elena small and isolated in a vast landscape; the low angle gives her dignity and strength; the extreme close-up on the crack creates suspense; amplified sound and the sudden silence heighten tension; the cut to black withholds the outcome, creating an open ending.',
  adapt='If adapted from a written story, the film would replace description of Elena\'s thoughts with camera distance, angle and sound.',
  tone='suspenseful', tw=['comic', 'cheerful', 'relaxed'], tonex='the crack and silence build suspense.',
  dev=[('extreme long shot', 'a lone figure crosses a frozen lake at dawn', 'it isolates the character in a vast, dangerous landscape', ['simile', 'statistic', 'onomatopoeia']),
       ('sound design', 'the crack amplified; the wind drops out', 'manipulating sound focuses attention and creates dread', ['simile', 'statistic', 'anaphora']),
       ('cut to black', 'Cut to black. Silence.', 'withholding the image creates an open, unsettling ending', ['simile', 'statistic', 'onomatopoeia'])],
  struct=[('the progression from extreme long shot to extreme close-up', 'moving closer and closer builds tension and narrows attention to the danger')],
  gq='How does the shot list use film language to create tension?',
  gqa=('Thesis: the sequence narrows from landscape to crack to nothing. (1) Shot distances. (2) Angle and sound. (3) Cut to black. Evaluation: ambiguity invites interpretation (danger, death or metaphor for ageing).'),
  issue='Ageing, risk and isolation.',
  concept=('creativity', 'film language creates meaning without dialogue.'),
  read='Viewers may read literal danger or a metaphor for mortality.',
  field='art, creativity and the imagination')

P(id='arrivals', kind='graphic', title='page from a graphic memoir, described in words',
  text=("[Panel 1 – wide, full width: a crowded airport arrivals hall drawn in muted greys; a small girl clutches her mother's coat. Caption: 'Toronto, 1994. Everything was too loud.']\n"
        "[Panel 2 – small and square: close-up of the girl's wide eyes. No words.]\n"
        "[Panel 3 – tall and narrow: an immigration officer leans over the counter; his speech balloon is filled with jagged, unreadable scribbles.]\n"
        "[Panel 4: the mother's hand squeezes the girl's – the only panel in colour, a warm orange.]"),
  graphic='Panel size controls pace and emphasis: the wide establishing panel shows overwhelming space, the small square close-up isolates fear, the tall panel makes the officer loom; the unreadable speech balloon visualises the language barrier from the child\'s perspective; the gutters create silence between moments; colour appears only in the final panel to highlight comfort.',
  memory='The retrospective caption ("Everything was too loud") shows the adult memoirist recalling a child\'s sensations, combining past perception and present reflection.',
  tone='anxious', tw=['jubilant', 'sarcastic', 'detached'], tonex='crowding and unreadable speech create anxiety.',
  dev=[('unreadable speech balloon', 'his speech balloon is filled with jagged, unreadable scribbles', 'it shows what the child experiences – noise rather than language – placing the reader in her position', ['statistic', 'simile', 'rhetorical question']),
       ('selective colour', 'the only panel in colour, a warm orange', 'colour marks the emotional centre: the mother\'s comfort', ['statistic', 'onomatopoeia', 'anaphora'])],
  struct=[('the sequence from wide panel to close-up to tall panel', 'shifting panel shapes mimic the child\'s shifting perception and fear')],
  visual='Muted greys convey alienation; the officer\'s height in a tall panel suggests power; the warm orange in the final panel creates relief.',
  gq='How does the page use the resources of the graphic form to convey a child\'s experience of migration?',
  gqa=('Thesis: form puts the reader inside the child\'s perception. (1) Panel size and shape. (2) The unreadable balloon. (3) Selective colour. Evaluation: wordless panels communicate what prose would have to describe.'),
  issue='Migration, language barriers and belonging.',
  concept=('perspective', 'the visual form recreates a child\'s perspective.'),
  read='Migrant readers may recognise the experience; others gain empathy through the visual perspective.',
  field='culture, identity and community')

P(id='village', kind='graphic', title='two panels from a graphic novel about memory and displacement, described in words',
  text=("[Panel 1: a grandfather in a modern apartment tells a story to his granddaughter; clean lines and flat colours.]\n"
        "[Panel 2: the same scene, but the apartment walls dissolve into sketchy pencil lines of a 1950s village street; the gutter between the panels has been removed, so the two images bleed into each other.]\n"
        "Caption: 'He always said the village was still there, if you knew how to look.'"),
  graphic='Removing the gutter merges present and past, showing memory intruding on the present; the change in drawing style (clean lines versus sketchy pencil) marks the shift from reality to memory and suggests its fragility.',
  memory='The village exists now only in the grandfather\'s memory and the act of storytelling; the work represents the transmission of memory across generations, a common concern of trauma and displacement narratives.',
  tone='wistful', tw=['furious', 'comic', 'triumphant'], tonex='the dissolving village is wistful.',
  dev=[('removed gutter', 'the gutter between the panels has been removed', 'the merged panels show past and present coexisting in memory', ['statistic', 'onomatopoeia', 'rhetorical question']),
       ('change of drawing style', 'sketchy pencil lines of a 1950s village street', 'the unfinished style suggests memory\'s fragility', ['statistic', 'simile', 'onomatopoeia'])],
  struct=[('the caption placed across both panels', 'the words bridge the two time periods as the storytelling does')],
  visual='Clean modern lines contrast with pencil sketches; the dissolving walls visualise memory reclaiming space.',
  gq='How do the panels represent the relationship between memory and history?',
  gqa=('Thesis: the panels make memory a space the reader can enter. (1) Removed gutter. (2) Contrasting styles. (3) The caption. Evaluation: memory is presented as both vivid and fragile.'),
  issue='Displacement and the transmission of memory.',
  concept=('transformation', 'the present is transformed by memory.'),
  read='Some see nostalgia; others see the trauma of a lost place.',
  field='culture, identity and community')

P(id='yellow', kind='memoir', title='extract from a memoir (an original extract written for study)',
  text=("I remember the kitchen as yellow. My sister insists it was green, and she has the photographs to prove it. "
        "But I have kept it yellow for forty years, because yellow is the colour of the morning my father taught me to make bread, "
        "and I am not ready to give that morning back."),
  memory='The memoirist admits that her memory is factually wrong but emotionally true, showing that memoir constructs the self through selective, emotionally shaped memory rather than objective record.',
  tone='tender', tw=['hostile', 'clinical', 'mocking'], tonex='the loving memory is tender.',
  dev=[('contrast', 'I remember the kitchen as yellow. My sister insists it was green', 'the conflict between memory and evidence foregrounds the reliability of memoir', ['simile', 'onomatopoeia', 'statistic']),
       ('metaphor', 'I am not ready to give that morning back', 'treating a memory as a possession shows how the self clings to it', ['statistic', 'onomatopoeia', 'simile'])],
  struct=[('the move from fact (photographs) to feeling (the morning)', 'the paragraph concedes the truth and then defends the memory')],
  gq='How does the writer explore the relationship between memory and truth?',
  gqa=('Thesis: the memoir values emotional truth over fact. (1) Contrasting memories. (2) Photographs as evidence. (3) The metaphor of keeping the morning. Evaluation: honesty about unreliability increases the reader\'s trust.'),
  issue='Memory, truth and the construction of the self.',
  concept=('identity', 'identity is built from chosen memories.'),
  read='Readers may admire her honesty or question memoir\'s reliability.',
  field='art, creativity and the imagination')

P(id='diesel', kind='memoir', title='extract from oral testimony recorded for a museum archive (an original passage written for study)',
  text=("We left at night. I don't remember much – my mother's hand, the smell of diesel, someone singing very quietly. People ask me what I felt. "
        "I was six; I felt cold. The feelings came later, much later, when I had children of my own and saw them asleep."),
  memory='The testimony is fragmentary – sensory details rather than narrative – and shows that trauma may be understood only later; the speaker resists the audience\'s expectation of dramatic emotion.',
  tone='understated', tw=['melodramatic', 'jubilant', 'sarcastic'], tonex='plain statements create understatement.',
  dev=[('sensory fragments', "my mother's hand, the smell of diesel, someone singing very quietly", 'the list of sensations shows memory as fragments rather than story', ['simile', 'statistic', 'rhetorical question']),
       ('understatement', 'I was six; I felt cold.', 'the plain statement resists sensational expectations and conveys truthfulness', ['simile', 'onomatopoeia', 'oxymoron'])],
  struct=[('the delayed final sentence', 'emotion arrives only at the end, mirroring how understanding came later in life')],
  gq='How does the testimony convey the experience of trauma?',
  gqa=('Thesis: the testimony conveys trauma through what it cannot say. (1) Sensory fragments. (2) Understatement. (3) The delayed feelings. Evaluation: the restraint makes it credible and moving.'),
  issue='Displacement, trauma and memory.',
  concept=('perspective', 'the child\'s perspective then and the adult\'s now coexist.'),
  read='Listeners may expect drama; the testimony asks them to accept fragments.',
  field='politics, power and justice')

P(id='violin', kind='story', title='ending of a short story (an original extract written for study)',
  text=("For eleven years Mr Okafor had walked past the music shop on Calle Real without stopping. Today the violin in the window had a small handwritten sign: "
        "'Played by a beginner. Still learning.' He stood there until the shopkeeper came out, and then, to his own surprise, he went in."),
  story='The short story compresses eleven years into one sentence and builds to an epiphany: the sign\'s words ("Still learning") release Mr Okafor from a long-held fear; the ending is open – we do not know what he does inside.',
  tone='hopeful', tw=['bitter', 'menacing', 'despairing'], tonex='the final action is hopeful.',
  dev=[('compression', 'For eleven years Mr Okafor had walked past the music shop', 'a single sentence summarises years of habit, typical of short story economy', ['simile', 'onomatopoeia', 'rhetorical question']),
       ('epiphany', "'Played by a beginner. Still learning.'", 'the sign triggers a sudden insight that permits change', ['simile', 'statistic', 'onomatopoeia'])],
  struct=[('the open ending "he went in"', 'it stops at the threshold, leaving the reader to imagine the change')],
  gq='How does the writer use the short story form to present a moment of change?',
  gqa=('Thesis: compression and an open ending make a small act momentous. (1) Compressed time. (2) The sign as epiphany. (3) Ending at the threshold. Evaluation: restraint gives the reader space.'),
  issue='Fear, ageing and second chances.',
  concept=('transformation', 'a small moment transforms a habit of years.'),
  read='Some read hope; others wonder whether the change will last.',
  field='art, creativity and the imagination')

P(id='ferry', kind='story', title='ending of a short story (an original extract written for study)',
  text=("She read the text message twice, put the phone face down on the table and looked out at the harbour. The ferry was leaving in ten minutes. "
        "Her suitcase was already by the door. Somewhere a gull laughed. She picked up the phone again."),
  story='The story ends without revealing the message or her decision; the short sentences and the ambiguous final action create an open ending that leaves the reader to infer the conflict.',
  tone='tense', tw=['carefree', 'jovial', 'triumphant'], tonex='the countdown creates tension.',
  dev=[('personification', 'Somewhere a gull laughed.', 'the gull\'s mockery suggests the indifference or irony of the world', ['statistic', 'rhetorical question', 'anaphora']),
       ('short sentences', 'The ferry was leaving in ten minutes. Her suitcase was already by the door.', 'clipped statements create a countdown', ['simile', 'onomatopoeia', 'oxymoron'])],
  struct=[('the final sentence', 'returning to the phone suggests hesitation, keeping the ending open')],
  gq='How does the writer create an open ending?',
  gqa=('Thesis: withheld information makes the ending a question. (1) The unrevealed message. (2) Time pressure. (3) Ambiguous final action. Evaluation: openness invites engagement but may frustrate.'),
  issue='Choice, freedom and relationships.',
  concept=('perspective', 'the limited perspective withholds what matters most.'),
  read='Readers imagine different messages and decisions.',
  field='culture, identity and community')

P(id='charlotte', kind='fanfic', title="fan fiction based on Jane Austen's 'Pride and Prejudice' (an original extract written for study)",
  text=("Charlotte Lucas did not love Mr Collins. She had never expected to. What she loved, she discovered in the first week at Hunsford, was the small sitting room at the back of the parsonage, "
        "where he never came because the light was poor. There she read, and wrote letters to Elizabeth, and was, for two hours each afternoon, nobody's wife."),
  fanfic='The piece borrows Austen\'s characters and the detail, present in the novel, that Charlotte prefers a back room her husband avoids; it shifts focalisation from Elizabeth to Charlotte, giving a minor character inner life and reframing her pragmatic marriage as a search for private freedom.',
  intertext='It depends on the reader knowing Pride and Prejudice: Charlotte marries Mr Collins for security, and Austen\'s narrator views her mainly through Elizabeth\'s disappointment; the fan fiction answers back to that perspective.',
  tone='wry', tw=['hysterical', 'grief-stricken', 'triumphant'], tonex='understatement and irony recall Austen\'s wry tone.',
  dev=[('pastiche of Austen\'s irony', 'Charlotte Lucas did not love Mr Collins. She had never expected to.', 'the understated sentences imitate Austen\'s dry narrative voice', ['simile', 'onomatopoeia', 'statistic']),
       ('climactic phrase', "nobody's wife", 'the ending reveals the freedom Charlotte values', ['simile', 'statistic', 'onomatopoeia'])],
  struct=[('the shift from what she did not love to what she did', 'the structure turns a story of compromise into one of discovery')],
  gq='How does the fan fiction transform its source text?',
  gqa=('Thesis: the fan fiction gives a minor character the interiority the source denied her. (1) Shifted focalisation. (2) Pastiche of Austen\'s irony. (3) The private room as symbol of freedom. Evaluation: it rereads the original from a feminist perspective.'),
  issue='Women, marriage and economic security.',
  concept=('transformation', 'the source text is transformed by a new perspective.'),
  read='Austen readers may see a faithful extension or a modern feminist rewriting.',
  field='art, creativity and the imagination')

P(id='penelope', kind='poem', title="poem 'Penelope' (an original poem written for study)",
  text=("Penelope\n\nTwenty years I wove and unwove,\nand they called it faithfulness.\nNo one asked what I was making\nin the hours the loom stood still –\na self, thread by thread,\nthat no returning king could wear."),
  intertext='The poem rewrites Homer\'s Odyssey, in which Penelope weaves a shroud by day and unravels it by night to delay her suitors while Odysseus is away for twenty years; it gives her a voice and reinterprets the weaving as self-making rather than wifely loyalty.',
  imagery='Weaving becomes a metaphor for constructing a self; "no returning king could wear" turns the woven self into a garment that belongs to her, not to Odysseus.',
  speaker='Penelope speaks as a persona in a dramatic monologue, challenging how she has been represented ("they called it faithfulness").',
  form='Free verse with short lines; the dash marks a pause before the revelation of what she was making.',
  sound='Repetition ("wove and unwove", "thread by thread") mimics the rhythm of weaving.',
  tone='defiant', tw=['submissive', 'jubilant', 'comic'], tonex='Penelope rejects the label given to her.',
  dev=[('allusion', 'Twenty years I wove and unwove', 'it recalls the Odyssey, inviting comparison with the original Penelope', ['statistic', 'onomatopoeia', 'simile']),
       ('extended metaphor', 'a self, thread by thread', 'weaving becomes self-making', ['statistic', 'onomatopoeia', 'rhetorical question'])],
  struct=[('the final line', 'it overturns the reunion of the epic: the self she made is not for Odysseus')],
  gq='How does the poet transform the story of Penelope?',
  gqa=('Thesis: the poem turns a symbol of wifely patience into a story of self-making. (1) Allusion. (2) Persona. (3) Weaving metaphor and the final line. Evaluation: a feminist rewriting that answers the epic.'),
  issue='Gender, voice and the retelling of myths.',
  concept=('transformation', 'a classical story is transformed by a new perspective.'),
  read='Some read empowerment; others a sadder story of a life spent waiting.',
  field='art, creativity and the imagination')

P(id='tides', kind='poem', title='two short poems from the same (fictional) poetry collection',
  text=("Poem 1: 'Tide'\nMy father's boat goes out like a held breath;\nthe harbour waits, the water keeps its counsel.\n\n"
        "Poem 2: 'Tide (II)'\nNow the boat is a planter on the quay,\nfull of geraniums. The water still keeps its counsel,\nbut no one asks it anything."),
  motif='The recurring image of the boat and the water that "keeps its counsel" links the poems: in the first, the sea is a mysterious force that the family depends on; in the second, the boat has become decoration and the water is ignored, showing the end of a fishing way of life and the speaker\'s grief.',
  imagery='Simile "like a held breath" creates suspense and fear; the boat as "a planter ... full of geraniums" is a poignant image of obsolescence.',
  form='Both poems are short and unrhymed; the title "Tide (II)" signals a sequel and invites comparison.',
  tone='elegiac', tw=['jubilant', 'sarcastic', 'frantic'], tonex='the change in the boat is elegiac.',
  dev=[('simile', "My father's boat goes out like a held breath", 'it conveys anxiety and dependence on the sea', ['statistic', 'onomatopoeia', 'rhetorical question']),
       ('repetition across poems', 'the water keeps its counsel ... The water still keeps its counsel', 'the repeated phrase links the poems and shows what has and has not changed', ['statistic', 'onomatopoeia', 'simile'])],
  struct=[('the sequel title "Tide (II)"', 'it frames the second poem as a revisiting, emphasising change over time')],
  gq='How does the poet use recurring images across the two poems?',
  gqa=('Thesis: the recurring images measure loss. (1) The boat transformed. (2) The repeated phrase about the water. (3) The shift from fear to neglect. Evaluation: comparing poems reveals the collection\'s concern with vanishing livelihoods.'),
  issue='The decline of traditional livelihoods.',
  concept=('transformation', 'the community and its objects are transformed by economic change.'),
  read='Readers may focus on family grief or on social change.',
  field='culture, identity and community')

P(id='panther', kind='trans', title="first stanza of Rainer Maria Rilke's poem 'Der Panther' (1902) with an English translation written for study",
  text=("Original: Sein Blick ist vom Vorübergehn der Stäbe / so müd geworden, daß er nichts mehr hält. / Ihm ist, als ob es tausend Stäbe gäbe / und hinter tausend Stäben keine Welt.\n"
        "Translation: His gaze, from the passing of the bars, / has grown so tired that it holds nothing more. / It seems to him there are a thousand bars / and behind a thousand bars, no world."),
  trans='The translation keeps the repetition of "thousand bars" and the closing "no world", which preserves the trapped, circular feeling, but it gives up the original rhyme (Stäbe/gäbe, hält/Welt) and much of the rhythm; "holds nothing more" keeps the double sense of "hält" (holds/retains).',
  culture='Rilke wrote the poem after observing a panther in the Jardin des Plantes in Paris; it is an example of his "thing-poems" (Dinggedichte), which try to see an object from within.',
  imagery='The bars seem to multiply until they replace the world, an image of captivity that destroys perception.',
  tone='desolate', tw=['joyful', 'playful', 'smug'], tonex='the image of no world is desolate.',
  dev=[('repetition', 'tausend Stäbe / tausend Stäben (a thousand bars / a thousand bars)', 'repetition enacts the endless pacing and the multiplication of bars', ['simile', 'statistic', 'onomatopoeia'])],
  gq='How does the translation preserve or change the effect of the original?',
  gqa=('Thesis: the translation keeps the image but loses the music. (1) Repetition preserved. (2) Rhyme lost. (3) "holds" for "hält". Evaluation: the meaning travels better than the sound.'),
  issue='Captivity and freedom (animal and human).',
  concept=('perspective', 'the poem tries to see from the panther\'s perspective.'),
  read='Some read the poem about animals; others as a metaphor for human confinement.',
  field='art, creativity and the imagination')

P(id='eyre_review', kind='review', title='review of a film adaptation of a classic novel, from an arts website',
  text=("Three stars. The new adaptation of Jane Eyre is beautiful to look at and curiously cold to feel. Every candle-lit corridor is gorgeously framed; every gust of moorland wind arrives on cue. "
        "What is missing is Jane's voice – the furious, funny first person that makes the novel a confession rather than a costume drama. "
        "Without it, she becomes someone things happen to, rather than someone who tells us what they meant."),
  aud='Readers of an arts website, likely familiar with the novel and interested in film.',
  purp='To evaluate the adaptation and advise readers whether it is worth seeing.',
  ctx='Classic novels are frequently adapted for film and television; reviewers often judge adaptations by their fidelity to the source.',
  tone='measured', tw=['gushing', 'furious', 'indifferent'], tonex='balanced praise and criticism make it measured.',
  dev=[('antithesis', 'beautiful to look at and curiously cold to feel', 'the balanced contrast sums up the verdict: visual success, emotional failure', ['simile', 'onomatopoeia', 'statistic']),
       ('contrast of genres', 'a confession rather than a costume drama', 'it distinguishes the novel\'s intimate voice from the film\'s surface spectacle', ['simile', 'onomatopoeia', 'statistic'])],
  struct=[('the rating placed first', 'readers get the verdict immediately, a convention of reviews'), ('the closing sentence', 'it explains the cost of losing first-person narration in adaptation')],
  adapt='The reviewer argues that adaptation struggles to translate first-person narration: the film\'s visuals (framing, weather) replace Jane\'s voice, turning her from narrator into object of the camera.',
  gq='How does the reviewer evaluate the adaptation?',
  gqa=('Thesis: the reviewer praises the surface and mourns the lost voice. (1) Antithesis. (2) Praise of cinematography. (3) Argument about first-person narration. Evaluation: persuasive for readers who know the novel; it assumes fidelity is the measure.'),
  issue='Adaptation and the transformation of literary voice.',
  concept=('transformation', 'adaptation transforms narrative voice into images.'),
  read='Fans of the novel agree; film lovers may value the adaptation on its own terms.',
  field='art, creativity and the imagination')

P(id='bread_review', kind='review', title='restaurant review on a food blog',
  text=("Let's start with the bread, because the bread is the best thing here, and that is not entirely a compliment. "
        "The menu promises 'a journey through the Andes'; the journey, sadly, stops at the bread basket. The ceviche was tired, the service brisk to the point of rudeness, "
        "and the bill – 58 euros for two – arrived faster than the main course. Two stars. Go for the bread. Leave before the journey."),
  aud='Readers of a food blog deciding where to eat.',
  purp='To evaluate the restaurant honestly and entertain readers with wit.',
  ctx='Online reviews influence restaurant success; bloggers build a following through a distinctive voice.',
  tone='witty', tw=['reverent', 'tragic', 'neutral'], tonex='ironic praise and punchlines make it witty.',
  dev=[('ironic praise', 'the bread is the best thing here, and that is not entirely a compliment', 'apparent praise becomes criticism of everything else', ['simile', 'onomatopoeia', 'statistic']),
       ('extended metaphor', "'a journey through the Andes'; the journey, sadly, stops at the bread basket", 'the reviewer turns the menu\'s own metaphor against it', ['statistic', 'onomatopoeia', 'rhetorical question']),
       ('imperative', 'Go for the bread. Leave before the journey.', 'the closing advice is a memorable punchline', ['simile', 'statistic', 'onomatopoeia'])],
  struct=[('the rating placed near the end', 'the verdict comes after the evidence, followed by a witty recommendation')],
  gq='How does the reviewer use humour to evaluate the restaurant?',
  gqa=('Thesis: wit makes criticism entertaining and credible. (1) Ironic praise. (2) Turning the menu\'s metaphor. (3) The comic list and punchline. Evaluation: entertaining, though one visit may be unfair.'),
  issue='The power of online reviews over livelihoods.',
  concept=('perspective', 'the reviewer\'s personal perspective is presented as authoritative.'),
  read='Readers enjoy the wit; the restaurant owner may find it unfair.',
  field='beliefs, values and education')

P(id='sugar_museum', kind='brochure', title='leaflet for a city museum exhibition',
  text=("SUGAR, SILVER, SILENCE: Untold Stories of the Port\nFor three centuries, ships left this harbour carrying cloth and returned with sugar, silver – and fortunes built on enslaved labour. "
        "This exhibition tells the stories our grand buildings leave out.\nFree entry. Content guidance: contains descriptions of violence."),
  aud='Residents and tourists in a port city, including families and school groups.',
  purp='To attract visitors to an exhibition that confronts the city\'s involvement in colonial trade and slavery.',
  ctx='Many European port cities have begun to address their historical links to slavery in museums and public debate.',
  tone='sober', tw=['flippant', 'celebratory', 'whimsical'], tonex='serious subject and restraint create sobriety.',
  dev=[('alliterative tricolon', 'SUGAR, SILVER, SILENCE', 'the list moves from goods to the silence about their human cost', ['simile', 'onomatopoeia', 'rhetorical question']),
       ('dash for emphasis', 'sugar, silver – and fortunes built on enslaved labour', 'the dash isolates the uncomfortable truth', ['simile', 'onomatopoeia', 'statistic']),
       ('personification', 'the stories our grand buildings leave out', 'the buildings become storytellers that have omitted part of history', ['statistic', 'onomatopoeia', 'simile'])],
  struct=[('the content guidance at the end', 'it signals respect for visitors and the seriousness of the material')],
  gq='How does the leaflet present the city\'s history to its audience?',
  gqa=('Thesis: the leaflet invites visitors to hear what the city has silenced. (1) The title\'s tricolon. (2) The dash revealing enslaved labour. (3) Personified buildings. Evaluation: inclusive "our" implicates the city\'s residents.'),
  issue='Colonial history, slavery and public memory.',
  concept=('representation', 'the city\'s past is re-represented to include those left out.'),
  read='Some welcome honesty; others resist re-examining civic pride.',
  field='politics, power and justice')

P(id='scroll', kind='oped', title='opinion column in a weekend newspaper',
  text=("To scroll or not to scroll: that is the question every teenager answers two hundred times a day. "
        "Whether 'tis nobler to endure the slings and arrows of the group chat, or to take arms against a sea of notifications and, by switching off, end them. "
        "Most of us, adults included, choose the scroll. Hamlet at least had the excuse of a ghost."),
  aud='Adult newspaper readers, many of them parents, with some literary knowledge.',
  purp='To comment humorously on compulsive phone use while including adults in the criticism.',
  ctx='Debates about smartphone use are common; the column assumes readers know Hamlet\'s "To be, or not to be" soliloquy.',
  tone='playful', tw=['solemn', 'hostile', 'despairing'], tonex='the parody of Shakespeare is playful.',
  dev=[('allusion / parody', "To scroll or not to scroll: that is the question", 'rewriting Hamlet\'s famous line turns a trivial choice into mock-tragic dilemma', ['simile', 'statistic', 'onomatopoeia']),
       ('pastiche', "the slings and arrows of the group chat ... a sea of notifications", 'borrowing Shakespeare\'s images for digital life creates comic incongruity', ['statistic', 'onomatopoeia', 'rhetorical question']),
       ('punchline', 'Hamlet at least had the excuse of a ghost.', 'the closing joke deflates modern indecision', ['simile', 'statistic', 'onomatopoeia'])],
  struct=[('the turn to "Most of us, adults included"', 'it widens the target from teenagers to all readers')],
  intertext='The column parodies Hamlet\'s soliloquy ("To be, or not to be ... the slings and arrows of outrageous fortune ... take arms against a sea of troubles"); its humour depends on recognising the source.',
  gq='How does the writer use an earlier text to comment on contemporary behaviour?',
  gqa=('Thesis: Shakespearean parody makes phone use look absurdly tragic. (1) The opening allusion. (2) Pastiche of images. (3) The punchline and inclusive turn. Evaluation: witty for literate readers but excludes those who miss the allusion.'),
  issue='Technology and attention.',
  concept=('creativity', 'the writer creatively reuses a canonical text.'),
  read='Readers who know Hamlet enjoy the parody; others may find it elitist.',
  field='science, technology and the environment')

# Paper 2: more questions for year 2.
P2Q.extend([
    dict(q='In what ways do two works you have studied present the relationship between the individual and the state?',
         terms='"Individual and the state" requires showing power exercised by institutions on a person; "ways" asks for authorial methods.',
         works="George Orwell's Nineteen Eighty-Four and Marjane Satrapi's Persepolis – a dystopian novel and a graphic memoir of life under authoritarian rule.",
         thesis='Both works show the state invading private life, but Orwell imagines total control through surveillance and language, while Satrapi shows a child negotiating state power through humour, family and visual self-representation.',
         points=['surveillance and the body: the telescreen versus the veil', 'resistance: Winston\'s diary versus Marji\'s rebellious clothes and music', 'form: third-person dystopia versus first-person graphic memoir'],
         ev='Evaluate which work offers more space for resistance.'),
    dict(q='Compare how two works you have studied use the perspective of a child or young person.',
         terms='"Perspective of a child" means focalisation or narration through youth; "compare" requires similarity and difference.',
         works="Harper Lee's To Kill a Mockingbird and Marjane Satrapi's Persepolis – child narrators of injustice.",
         thesis='Both works use a child\'s eyes to expose adult injustice, but Lee\'s retrospective narrator Scout blends innocence with adult reflection, while Satrapi\'s drawn child self makes naïvety visible on the page.',
         points=['retrospective narration versus the visual child self', 'humour and innocence', 'growing awareness of injustice'],
         ev='Evaluate how the medium shapes the effect of the child\'s perspective.'),
    dict(q='How do two works you have studied explore the consequences of a single decision?',
         terms='"Consequences" require cause and effect across the work; "single decision" must be identified in each.',
         works="Shakespeare's Othello and Ian McEwan's Atonement – a jealous murder and a false accusation.",
         thesis='Both works trace catastrophe from one decision, but Shakespeare compresses the consequences into a tragedy driven by Iago\'s manipulation, whereas McEwan spreads them across decades and reveals that the narrative itself is Briony\'s attempt at atonement.',
         points=['the moment of decision', 'dramatic irony versus metafictional revelation', 'responsibility and guilt'],
         ev='Evaluate which work makes the reader complicit.'),
    dict(q='Discuss how two works you have studied present the tension between public and private selves.',
         terms='"Public and private selves" requires showing a gap between how characters appear and who they are.',
         works="Oscar Wilde's The Importance of Being Earnest and Henrik Ibsen's A Doll's House (in translation).",
         thesis='Both plays expose the masks demanded by respectable society, but Wilde treats double lives ("Bunburying") as farce, while Ibsen treats Nora\'s performance as a tragedy that must be ended.',
         points=['double identities (Jack/Ernest; Nora\'s secret loan)', 'comic versus serious tone', 'endings: comic reconciliation versus departure'],
         ev='Evaluate whether comedy weakens or sharpens the social critique.'),
])


# =============================================================================================
# helpers for year 2
# =============================================================================================
LOI = [
    dict(text="Margaret Atwood's The Handmaid's Tale", concept='perspective',
         loi='How does Atwood use the "Historical Notes" epilogue to question the reliability and authority of Offred\'s testimony?',
         weak='Is The Handmaid\'s Tale a feminist novel?',
         thesis='Atwood\'s epilogue reframes Offred\'s narrative as an academic artefact, exposing how male scholars reduce testimony to evidence and inviting the reader to resist that reduction.'),
    dict(text="Marjane Satrapi's Persepolis", concept='identity',
         loi='How does Satrapi use the visual representation of the veil to explore the construction of Marji\'s identity?',
         weak='What does Persepolis tell us about Iran?',
         thesis='Satrapi\'s repeated, stylised images of the veil turn a garment into a contested sign, tracing Marji\'s identity as something imposed, resisted and finally chosen.'),
    dict(text="Chinua Achebe's Things Fall Apart", concept='representation',
         loi='In what ways does Achebe\'s ending, narrated from the District Commissioner\'s perspective, critique colonial representations of Africa?',
         weak='Is Okonkwo a good person?',
         thesis='The sudden shift to the Commissioner\'s view, and his plan to reduce Okonkwo to "a reasonable paragraph", exposes how colonial writing erased the complexity the novel has shown.'),
    dict(text="Kazuo Ishiguro's Never Let Me Go", concept='communication',
         loi='How does Ishiguro\'s use of euphemistic language ("donations", "completing") shape the reader\'s response to the clones\' fate?',
         weak='Is cloning wrong?',
         thesis='Ishiguro\'s gentle euphemisms mirror the characters\' acceptance, so the reader experiences the horror through what the language refuses to say.'),
    dict(text="Art Spiegelman's Maus", concept='representation',
         loi='To what extent does Spiegelman\'s animal metaphor both reveal and question the racial categories of Nazi ideology?',
         weak='How does Maus show the Holocaust?',
         thesis='Spiegelman\'s mice and cats make Nazi categories visible in order to expose them, while moments where characters wear masks reveal the metaphor\'s limits.'),
    dict(text='a body of work of political cartoons on climate change', concept='perspective',
         loi='How do cartoonists use non-human perspectives (animals, the planet) to criticise political inaction on climate change?',
         weak='What do cartoons say about climate change?',
         thesis='By giving animals and the planet a voice, the cartoons reverse the usual human perspective and make political time-scales absurd.'),
    dict(text='a body of work of fast-fashion parody advertisements', concept='transformation',
         loi='How do parody advertisements transform the conventions of fashion advertising to expose the hidden costs of fast fashion?',
         weak='Why is fast fashion bad?',
         thesis='The parodies keep the visual grammar of glossy adverts but subvert slogans and small print, making the genre confess what it normally hides.'),
    dict(text="Carol Ann Duffy's The World's Wife", concept='creativity',
         loi='How does Duffy use humour and the dramatic monologue to rewrite the stories of famous men from their wives\' perspectives?',
         weak='Is Duffy a feminist poet?',
         thesis='Duffy\'s comic monologues reclaim the wives\' voices, turning canonical stories into sharp critiques of male self-mythology.'),
    dict(text="Henrik Ibsen's A Doll's House (in translation)", concept='identity',
         loi='How does Ibsen use stage props such as the macaroons, the Christmas tree and the letterbox to trace Nora\'s changing sense of self?',
         weak='Why does Nora leave?',
         thesis='Ibsen\'s props externalise Nora\'s hidden life, so the stripped tree and the locked letterbox chart her movement from performance to self-knowledge.'),
    dict(text='a body of work of public-health anti-smoking campaigns', concept='communication',
         loi='How have anti-smoking campaigns shifted from fear appeals to appeals to family responsibility, and to what effect?',
         weak='Do anti-smoking adverts work?',
         thesis='The campaigns move from shock imagery to images of children and family, replacing fear with guilt and love as motivators.'),
]


def loi_gen(keys, c, d, mode):
    keys = [keys] if isinstance(keys, str) else keys

    def fn(rng, slot):
        it = rng.choice(LOI)
        if mode == 'eval':
            stem = rng.choice([f'A student proposes this HL essay line of inquiry on {it["text"]}: "{it["weak"]}" Explain why it is weak and rewrite it as a focused line of inquiry linked to the concept of {it["concept"]}.',
                               f'Evaluate the suitability of this HL essay line of inquiry: "{it["weak"]}" (text: {it["text"]}). Suggest an improved version.'])
            ans = f'Weak: it is too broad, invites summary or opinion and does not focus on authorial choices or a course concept. Improved: "{it["loi"]}" (linked to {it["concept"]}).'
            m = 3 if slot.d <= 3 else 4
            ty = 'explain'
        elif mode == 'thesis':
            stem = rng.choice([f'HL essay line of inquiry: "{it["loi"]}"\nWrite a thesis statement for this essay and outline three sections that would develop it.',
                               f'For the HL essay question "{it["loi"]}", propose an arguable thesis and explain which evidence from {it["text"]} you would use.'])
            ans = f'Model thesis: {it["thesis"]} Sections should each analyse specific authorial choices in {it["text"]} that support the thesis, ending with evaluation.'
            m = 4 if slot.d <= 3 else 6
            ty = 'case'
        else:
            stem = rng.choice([f'Write the introduction (about 150 words) for an HL essay on {it["text"]} answering: "{it["loi"]}"',
                               f'Explain how the line of inquiry "{it["loi"]}" connects to the course concept of {it["concept"]}, and how you would structure a 1,200–1,500-word essay on it.'])
            ans = f'Indicative content: context of the work; clear statement of the line of inquiry; thesis such as "{it["thesis"]}"; outline of argument; link to {it["concept"]}. HL essay criteria (5 marks each): A knowledge, understanding and interpretation; B analysis and evaluation; C focus, organisation and development; D language.'
            m = 6 if slot.d <= 4 else 10
            ty = 'long'
        return dict(stem=stem, answer=ans, markingKey=ans, type=ty, marks=m)
    for k in keys:
        R.t.setdefault(k, []).append(T(c, d, fn, 'long' if mode == 'intro' else 'case', None, 'loi_' + mode))


def p2_gen(keys, c, d, mode):
    keys = [keys] if isinstance(keys, str) else keys

    def fn(rng, slot):
        it = rng.choice(P2Q)
        q = it['q']
        if mode == 'terms':
            stem = rng.choice([f'Paper 2 question: "{q}"\nIdentify the key terms of this question and explain what each requires of your answer.',
                               f'Unpack this Paper 2 question by explaining its command phrase and its key terms: "{q}"'])
            ans, m, ty = it['terms'], (3 if slot.d <= 3 else 4), 'explain'
        elif mode == 'works':
            stem = rng.choice([f'Paper 2 question: "{q}"\nSuggest two literary works you could use to answer this question and justify the pairing.',
                               f'Which two works would make a strong pairing for this Paper 2 question, and why? "{q}"'])
            ans, m, ty = f'Suggested pairing: {it["works"]} (any two studied works may be credited if the justification shows a point of comparison and contrast).', (3 if slot.d <= 3 else 4), 'case'
        elif mode == 'thesis':
            stem = rng.choice([f'Paper 2 question: "{q}"\nWrite a comparative thesis statement that answers the question.',
                               f'Write an arguable comparative thesis for the Paper 2 question: "{q}"'])
            ans, m, ty = f'Model thesis: {it["thesis"]} A strong thesis names both works, answers the question directly and states a similarity and a difference.', (3 if slot.d <= 3 else 4), 'case'
        elif mode == 'points':
            stem = rng.choice([f'Paper 2 question: "{q}"\nOutline three comparative points for an essay answering this question.',
                               f'Plan the body of a comparative essay for: "{q}" Give three integrated comparative points.'])
            ans, m, ty = 'Example points: ' + '; '.join(it['points']) + f'. {it["ev"]}', (4 if slot.d <= 3 else 6), 'case'
        else:
            stem = rng.choice([f'Write a comparative paragraph for an essay answering: "{q}" Analyse an authorial choice in each of two works.',
                               f'Paper 2 question: "{q}"\nWrite one integrated comparative paragraph that analyses and evaluates how both writers\' choices shape meaning.'])
            ans, m, ty = f'Indicative content (example pairing: {it["works"]}): {it["points"][0]}. {it["ev"]} {P2_BANDS}', (6 if slot.d <= 4 else 10), 'long'
        return dict(stem=stem, answer=ans, markingKey=ans + ' Any suitable studied works may be credited.', type=ty, marks=m)
    for k in keys:
        R.t.setdefault(k, []).append(T(c, d, fn, 'long' if mode == 'para' else 'case', None, 'p2_' + mode))


# =============================================================================================
# ch01 Intertextuality: connecting texts – key concepts
# =============================================================================================
INTER = {'cartoon', 'parody', 'oped', 'speech', 'poem', 'fanfic', 'satire'}
H('ch01-st1',
  terms=[('intertextuality', 'the ways in which texts refer to, borrow from, or are shaped by other texts, so that meaning arises from relationships between texts'),
         ('allusion', 'a brief, indirect reference to another text, person or event that the reader is expected to recognise'),
         ('pastiche', 'a work that imitates the style of another writer or genre, often affectionately, without the critical edge of parody'),
         ('parody', 'an imitation of a text or genre that exaggerates its features for comic or critical effect'),
         ('adaptation', 'the transformation of a text into a new form, medium or context, such as a novel into a film'),
         ('hypotext', 'the earlier source text on which a later text (the hypertext) is based'),
         ('quotation', 'the direct reproduction of words from another text, used to borrow authority or create new meaning')],
  facts=[('A cartoon shows a child holding a sign saying "IT\'S JUST A PHONE" as investors applaud a near-naked billionaire. The cartoon alludes to:', '"The Emperor\'s New Clothes" by Hans Christian Andersen', ['"Little Red Riding Hood"', 'Hamlet', 'The Odyssey'], 'The child who tells the truth about the emperor is the source.'),
         ('"To scroll or not to scroll: that is the question" is an example of:', 'Parody of a famous quotation', ['Pastiche of a genre', 'Adaptation into film', 'Direct quotation'], 'It imitates and alters Hamlet\'s line for comic effect.'),
         ('What is the main difference between parody and pastiche?', 'Parody mocks or criticises its source; pastiche imitates without critical intent', ['Pastiche is always longer', 'Parody never imitates style', 'There is no difference'], 'Critical intent distinguishes parody.')],
  why=[('Explain why allusion depends on the reader.', 'An allusion only works if the reader recognises the source; readers who miss it lose a layer of meaning, so allusion creates an implied, knowledgeable audience.'),
       ('Explain why intertextuality is useful for writers of non-literary texts such as adverts.', 'Borrowing familiar stories, phrases or images gives an advert instant meaning, emotional associations and humour with very few words.'),
       ('Explain how a parody can criticise its source and the world at the same time.', 'Exaggerating a source\'s conventions exposes their assumptions, and applying them to a new subject comments on that subject too.')],
  contrast=[('allusion', 'quotation', 'An allusion is an indirect reference the reader must recognise; a quotation reproduces the source\'s actual words, usually marked as borrowed.'),
            ('parody', 'adaptation', 'Parody imitates in order to mock or criticise; adaptation transforms a text into a new form or context, often seeking to preserve its meaning for a new audience.')],
  misc=[('Intertextuality only means quoting other books.', 'It includes allusion, parody, pastiche, adaptation, genre conventions and any way a text\'s meaning depends on other texts, including visual and non-literary ones.'),
        ('Readers who do not recognise an allusion cannot understand the text at all.', 'They can still read the surface meaning; they miss a layer of significance that the allusion adds.')],
  evaluate=[('All texts are intertextual.', ['every text uses inherited language, genres and conventions', 'readers interpret through other texts they know'], ['some texts make intertextuality central and others do not', 'the term loses precision if applied to everything'], 'In a broad sense all texts are intertextual, but analysis should focus on deliberate, meaningful connections.')],
  extended=[('Choose a text you have studied that alludes to an earlier work. Analyse how the allusion shapes meaning and evaluate how much the text depends on the reader recognising it.', 'Indicative content: identify the allusion and source; analyse the transfer of meaning; consider readers who miss it; evaluate.', 8, 'long')])
pq('ch01-st1', ('C2', 'C3', 'C4'), (1, 5), None, 'intertext', ['Identify the intertextual reference in this text and explain how it shapes meaning.',
                                                              'How does this text depend on the reader\'s knowledge of another text?',
                                                              'Analyse how the writer uses an earlier text or genre to create meaning.',
                                                              'Evaluate how effectively the text uses intertextuality for its audience.'], crit=CRIT_B)
pq_dev_mcq('ch01-st1', INTER)

H('ch01-st2',
  terms=[('genre', 'a category of texts sharing conventions of form, content and style, such as Gothic fiction, tragedy or the opinion column'),
         ('convention', 'an expected feature of a genre or text type, such as a happy ending in romantic comedy or a headline in a news report'),
         ('subversion', 'deliberately breaking or reversing the conventions of a genre to surprise or make a point'),
         ('hybrid genre', 'a text that combines conventions from two or more genres'),
         ('horizon of expectations', 'the set of assumptions a reader brings to a text based on genre and previous reading (Hans Robert Jauss)')],
  facts=[('A satirical article that imitates the structure of a news report is using:', 'The conventions of one genre to subvert its purpose', ['A hybrid of poetry and drama', 'A literal translation', 'Free verse'], 'Satire borrows news conventions for comic critique.'),
         ('A graphic memoir combines conventions of:', 'Comics and autobiography', ['Tragedy and epic', 'News and advertising', 'Sonnet and ballad'], 'It is a hybrid genre.')],
  why=[('Explain why writers subvert genre conventions.', 'Subversion surprises readers, exposes the assumptions built into conventions and creates new meanings – for example a fairy tale without a happy ending questioning moral simplicity.'),
       ('Explain how genre shapes a reader\'s expectations.', 'Readers anticipate certain events, tones and endings; writers can satisfy these expectations or exploit them for suspense, irony or surprise.'),
       ('Explain why non-literary texts also have genres.', 'Adverts, reviews and manifestos have recognisable conventions that audiences use to interpret purpose and tone quickly.')],
  contrast=[('following a convention', 'subverting a convention', 'Following a convention meets the reader\'s expectations; subverting it deliberately breaks them, often to make a critical or surprising point.')],
  misc=[('Following genre conventions makes a text unoriginal.', 'Writers can use conventions creatively; originality often lies in how conventions are combined, varied or subverted.')],
  evaluate=[('Genre is more important to the reader than to the writer.', ['readers use genre to interpret and choose texts', 'expectations shape reading'], ['writers choose genres to reach audiences', 'subversion requires the writer\'s awareness'], 'Genre is a shared contract: writers use it to shape meaning and readers to interpret it.')],
  extended=[('Write the opening of a story (about 250 words) that subverts the conventions of a fairy tale, then explain which conventions you subverted and why.', 'Indicative content: recognisable conventions (once upon a time, archetypes) and clear subversion; commentary on effect and purpose.', 8, 'long')])
pq('ch01-st2', ('C2', 'C3'), (1, 5), None, 'kconv', ['Identify the genre or text type of this extract and explain how it follows or subverts its conventions.',
                                                   'Explain how the writer uses the conventions of the text type here.',
                                                   'Which conventions does this text use, and how does it use them to create meaning?'], crit=CRIT_A)
pq('ch01-st2', ('C3', 'C4'), (2, 5), {'satire', 'parody'}, 'satire', ['Analyse how this text borrows the conventions of another genre and to what effect.',
                                                                     'Evaluate how the text uses genre conventions to criticise its target.'])

H('ch01-st3',
  terms=[('shared concept', 'one of the seven course concepts used as a lens to compare texts of different types'),
         ('comparative analysis', 'analysis that examines similarities and differences between texts in relation to a focus'),
         ('cross-genre comparison', 'comparison of texts from different genres or text types, such as a poem and an advertisement')],
  facts=[('Which pairing best suits a comparison through the concept of "representation"?', 'A novel and a news report that portray the same group of people', ['Two copies of the same poem', 'A dictionary and a thesaurus', 'A timetable and a menu'], 'Both texts construct an image of the same group.'),
         ('In comparative analysis, a strong comparison:', 'Integrates both texts around a shared focus', ['Analyses one text, then the other, without links', 'Lists similarities only', 'Summarises plots'], 'Integration shows comparison.')],
  why=[('Explain why comparing a literary and a non-literary text can be illuminating.', 'Different forms present the same issue differently – literature through complexity and voice, non-literary texts through direct persuasion – so comparison reveals how form shapes meaning.'),
       ('Explain why a shared concept helps structure a comparison.', 'A concept such as perspective gives a common question to ask of both texts, preventing two separate analyses.'),
       ('Explain why differences between texts can be as revealing as similarities.', 'Differences show what each form or context makes possible, sharpening understanding of both texts.')],
  contrast=[('an integrated comparison', 'a sequential comparison', 'An integrated comparison discusses both texts together point by point; a sequential comparison analyses one text and then the other, linking them later.')],
  misc=[('Texts of different genres cannot be meaningfully compared.', 'Comparison across genres is central to the course; a shared concept or issue makes it meaningful.')],
  evaluate=[('Non-literary texts present global issues more honestly than literary works.', ['they address the issue directly', 'they often use real data'], ['they persuade and simplify', 'literature explores complexity and ambiguity'], 'Neither is more honest; each is constructed for a purpose.')],
  extended=[('Compare how a literary work and a non-literary text you have studied engage with the concept of perspective.', 'Indicative content: define perspective; analyse each text; integrate comparison; evaluate.', 8, 'long')])
pq('ch01-st3', ('C3', 'C4'), (2, 5), None, 'concept', ['Explain how this text engages with the concept of {cname}, and suggest a literary work you could compare it with.',
                                                     'How could this text be compared with a literary work you have studied through the concept of {cname}?',
                                                     'Discuss how the concept of {cname} could link this text to a work of a different genre.'], crit=CRIT_OPEN)
pq('ch01-st3', 'C2', (2, 4), None, 'issue', ['Explain what global issue this text shares with a literary work you have studied.'], crit=CRIT_OPEN)


# =============================================================================================
# ch02 Literary work 4 – the novel
# =============================================================================================
PROSE = {'prose', 'story', 'fanfic', 'memoir'}
H('ch02-st1',
  terms=[('theme', 'a central idea or concern explored throughout a work, such as power, identity or loss'),
         ('thematic development', 'the way a work\'s treatment of a theme changes, deepens or complicates across its structure'),
         ('motif', 'a recurring element that develops a theme'),
         ('narrative arc', 'the overall shape of a story from exposition through climax to resolution')],
  facts=[('Tracing how a symbol changes from the beginning to the end of a novel is a way of analysing:', 'Thematic development', ['Metre', 'Typography', 'Lineation'], 'Changing symbols chart the development of themes.'),
         ('A theme is best expressed as:', 'A statement about an idea, e.g. "ambition corrupts trust"', ['A single word only, e.g. "ambition"', 'A plot summary', 'A list of characters'], 'A thematic statement makes an arguable claim.')],
  why=[('Explain why themes in a novel should be traced across the whole work rather than one passage.', 'Novels develop themes through change – events, character arcs and repeated motifs – so a single passage shows only one stage.'),
       ('Explain how a novel\'s ending can change the meaning of its themes.', 'Endings resolve or complicate earlier patterns; a tragic or open ending can reframe the theme in retrospect.'),
       ('Explain why expressing a theme as a statement is better than a single word.', 'A statement ("power corrupts those who fear weakness") is arguable and specific, guiding analysis better than a topic word.')],
  contrast=[('a theme', 'a subject', 'A subject is what the novel is about (war); a theme is what it suggests about the subject (war destroys the moral certainties of those who fight).')],
  misc=[('A novel has one theme that the author intends.', 'Novels usually explore several interconnected themes, and readers may interpret them differently.')],
  evaluate=[('Character is the main vehicle of theme in the novel.', ['characters\' choices dramatise ideas', 'readers connect to themes through people'], ['setting, structure and narrative voice also carry theme', 'motifs develop meaning independently'], 'Character is a central vehicle but works with structure, voice and motif.')],
  extended=[('Trace the development of one theme across a novel you have studied, referring to its opening, a central episode and its ending.', 'Indicative content: thematic statement; three stages; authorial methods; evaluation of development.', 8, 'long')])
pq('ch02-st1', ('C3', 'C4'), (2, 5), PROSE, 'issue', ['What thematic concern does this extract introduce, and how might a novel develop it?',
                                                     'Express a theme suggested by this extract as a statement and explain the evidence for it.'], crit=CRIT_OPEN)
pq('ch02-st1', ('C2', 'C3'), (1, 4), PROSE, 'symbol', ['Explain how a symbol in this extract could develop a theme across a whole novel.'])

H('ch02-st2',
  terms=[('unreliable narrator', 'a narrator whose account cannot be fully trusted because of bias, ignorance, self-deception or deception'),
         ('stream of consciousness', 'a technique that presents the continuous flow of a character\'s thoughts, impressions and memories'),
         ('fragmented time', 'a non-chronological narrative structure that moves between times, often reflecting memory or trauma'),
         ('metafiction', 'fiction that draws attention to its own status as fiction'),
         ('interior monologue', 'the direct presentation of a character\'s thoughts, often in the first person')],
  facts=[('Virginia Woolf\'s Mrs Dalloway is often studied as an example of:', 'Stream of consciousness', ['Epistolary form', 'Omniscient Victorian narration', 'Verse drama'], 'Woolf presents characters\' flowing thoughts.'),
         ('A narrator who says "I want to be clear that I did not take the money. I borrowed it" is likely:', 'Unreliable', ['Omniscient', 'Objective', 'A chorus'], 'Self-justification signals unreliability.')],
  why=[('Explain why modernist writers experimented with stream of consciousness.', 'They sought to represent how consciousness actually works – associative, fragmented, shaped by memory – rather than ordered external events.'),
       ('Explain how fragmented time can represent trauma.', 'Trauma disrupts memory; jumping between times mimics intrusive recollection and the difficulty of telling a coherent story.'),
       ('Explain how an unreliable narrator creates irony.', 'The gap between what the narrator says and what the reader infers creates dramatic irony and invites critical reading.')],
  contrast=[('stream of consciousness', 'interior monologue', 'Stream of consciousness is a broad technique presenting the flow of thought, often in fragmented syntax; interior monologue is a more ordered direct presentation of a character\'s thoughts.')],
  misc=[('Experimental narration is just a way of making novels difficult.', 'Experimental techniques serve meaning: they represent memory, trauma or subjectivity in ways conventional narration cannot.')],
  evaluate=[('Unreliable narrators make readers better readers.', ['they demand active inference', 'they train attention to clues'], ['some readers miss the unreliability', 'they can frustrate'], 'They reward and develop attentive reading, though their effect depends on the reader.')],
  extended=[('Write a 250-word passage in which an unreliable narrator recounts an event, then explain the clues you planted for the reader.', 'Indicative content: consistent voice; deliberate contradictions or omissions; commentary.', 8, 'long')])
pq('ch02-st2', ('C2', 'C3', 'C4'), (1, 5), {'prose', 'memoir'}, 'pov', ['How does the narrative voice in this extract shape the reader\'s trust?',
                                                                       'Analyse the narrative technique used in this extract.',
                                                                       'Explain whether the narrator in this extract can be trusted, using evidence.',
                                                                       'Evaluate how the narrative technique in this extract affects the reader.'])
pq('ch02-st2', ('C3', 'C4'), (2, 5), {'prose', 'memoir'}, 'time', ['How does the extract handle time, and to what effect?'])
pq('ch02-st2', 'C3', (2, 5), {'memoir'}, 'memory', ['How does the extract suggest that memory is unreliable or selective?'])

H('ch02-st3',
  terms=[('critical lens', 'a theoretical perspective used to interpret a text, such as feminist, Marxist or postcolonial criticism'),
         ('feminist criticism', 'an approach that examines how texts represent gender and power, and how they reinforce or challenge patriarchy'),
         ('Marxist criticism', 'an approach that examines how texts represent class, economic power and ideology'),
         ('postcolonial criticism', 'an approach that examines how texts represent colonisation, empire and their aftermath, and whose voices are heard'),
         ('ideology', 'a system of beliefs and values that shapes how people see the world, often presented as natural')],
  facts=[('Reading an extract about a domestic worker counting her wages for evidence of class power is applying:', 'A Marxist lens', ['A formalist lens', 'A biographical lens', 'A psychoanalytic lens only'], 'Class and economic power are Marxist concerns.'),
         ('Edward Said\'s Orientalism (1978) is associated with:', 'Postcolonial criticism', ['Feminist criticism', 'New Criticism', 'Reader-response theory'], 'Said analysed Western representations of the "East".')],
  why=[('Explain why applying a critical lens can deepen an interpretation.', 'A lens directs attention to patterns (gender, class, empire) a reader may overlook, revealing ideologies the text reflects or challenges.'),
       ('Explain why the same novel can be read through different lenses.', 'Novels contain many dimensions of power and identity; each lens foregrounds different ones, producing complementary interpretations.'),
       ('Explain why critical lenses should be used with textual evidence.', 'A lens is a way of reading, not a conclusion; claims must be supported by analysis of the text\'s choices.')],
  contrast=[('feminist criticism', 'Marxist criticism', 'Feminist criticism focuses on gender, patriarchy and the representation of women; Marxist criticism focuses on class, economic power and ideology. They intersect in readings of working-class women.'),
            ('postcolonial criticism', 'Marxist criticism', 'Postcolonial criticism examines empire, colonisation and cultural voice; Marxist criticism examines class and economic relations. Postcolonial critics often combine both.')],
  misc=[('A critical lens tells you what a text really means.', 'A lens offers one perspective; strong essays treat lenses as tools for argument, not as final answers.')],
  evaluate=[('Applying modern critical lenses to older novels is unfair to them.', ['older writers held different values', 'risk of anachronism'], ['lenses reveal what texts assume', 'texts live in present readings'], 'It is fair if done with awareness of context: the aim is understanding, not condemnation.')],
  extended=[('Interpret a novel you have studied through two critical lenses and evaluate which yields the richer reading.', 'Indicative content: define lenses; apply to specific episodes; compare insights; evaluation.', 8, 'long')])
pq('ch02-st3', ('C3', 'C4'), (2, 5), {'trans', 'prose', 'fanfic'}, 'power', ['Read this extract through a feminist or Marxist lens: what does it reveal about power?',
                                                                            'Apply a critical lens of your choice to this extract and explain what it reveals.',
                                                                            'Discuss how a Marxist and a feminist reading of this extract might differ.'], crit=CRIT_OPEN)
pq('ch02-st3', ('C3', 'C4'), (2, 5), None, 'gender', ['Apply a feminist lens to this text: how does it represent gender and power?'], crit=CRIT_OPEN)

H('ch02-st4',
  terms=[('retelling', 'a new version of an existing story, often from a different perspective or setting'),
         ('rewriting back', 'a postcolonial or feminist strategy of rewriting a canonical text to give voice to characters it marginalised'),
         ('revisionist fiction', 'fiction that reinterprets an earlier work or historical narrative'),
         ('canon', 'the body of works traditionally considered the most important in a literature')],
  facts=[('Jean Rhys\'s Wide Sargasso Sea (1966) rewrites which novel?', "Charlotte Brontë's Jane Eyre", ["Jane Austen's Emma", "Emily Brontë's Wuthering Heights", "Mary Shelley's Frankenstein"], 'It gives a voice and history to Bertha Mason, the "madwoman in the attic".'),
         ('A short piece that retells Pride and Prejudice from Charlotte Lucas\'s perspective is an example of:', 'A retelling from a marginalised perspective', ['A literal translation', 'A parody advertisement', 'An infographic'], 'It shifts focalisation to a minor character.')],
  why=[('Explain why writers rewrite canonical works.', 'Rewriting gives voice to characters the original marginalised, questions its values and shows how stories change with new perspectives.'),
       ('Explain why a retelling depends on the reader\'s knowledge of the source.', 'Much of its meaning lies in the differences from the original; recognising them reveals the critique.')],
  contrast=[('a retelling', 'an adaptation', 'A retelling creates a new version of a story, often changing perspective or meaning; an adaptation transfers a story to a new medium, often aiming to preserve it.')],
  apply=[('Jean Rhys\'s Wide Sargasso Sea tells the story of Antoinette (Bertha) before she arrives at Thornfield. Explain how this changes a reader\'s view of Jane Eyre.', 'It gives the "madwoman in the attic" a history, voice and Caribbean context, so Rochester appears more culpable and the original\'s colonial and racial assumptions become visible.', 4),
         ('Suggest how you would retell a key scene from a novel you have studied from the antagonist\'s point of view, and what the change would reveal.', 'Answers vary: credit a specific scene, a plausible antagonist perspective and a clear explanation of what is revealed about the original\'s values or blind spots.', 4),
         ('A poem retells a myth from the perspective of a woman silenced in the original. Identify two techniques the poet might use and their effects.', 'For example: first-person persona to give voice; allusion to specific details of the myth so readers recognise changes; ironic reframing of the original\'s praise (e.g. "faithfulness").', 3),
         ('Explain why a retelling might change the setting of its source to the present day.', 'Updating the setting tests whether the source\'s concerns still apply, makes it accessible and can expose how power or prejudice persists.', 3)],
  misc=[('Retellings are less original than the works they rewrite.', 'Retellings can be highly original, transforming perspective, form and meaning while engaging critically with the source.')],
  evaluate=[('A retelling can change how we read the original work.', ['Wide Sargasso Sea changes readings of Bertha', 'new perspectives reveal blind spots'], ['the original stands on its own', 'readers may resist reinterpretation'], 'Strong retellings permanently alter how many readers see the original.')],
  extended=[('Rewrite a scene from a novel you have studied from the perspective of a minor character, then explain what your retelling reveals.', 'Indicative content: consistent voice; meaningful shift; commentary on original\'s perspective.', 8, 'long')])
pq('ch02-st4', ('C2', 'C3', 'C4'), (1, 5), {'fanfic', 'poem'}, 'intertext', ['How does this text respond to an earlier work?',
                                                                            'Analyse what this retelling changes about its source and why.',
                                                                            'Evaluate what this rewriting reveals about the original text.'])
pq('ch02-st4', 'C3', (2, 4), {'fanfic'}, 'fanfic', ['Explain how this text transforms its source.'])
pq('ch02-st4', 'C3', (2, 4), {'cartoon', 'oped', 'speech', 'parody'}, 'intertext', ['Like a novel that rewrites an earlier work, this text responds to a source. Explain how it reworks that source.',
                                                                                  'Explain what this text borrows from an earlier text and what it changes.'])


# =============================================================================================
# ch03 Literary work 5 – poetry in translation or short stories
# =============================================================================================
H('ch03-st1',
  terms=[('body of poems', 'a collection or selection of poems by one poet studied as a single literary work'),
         ('recurring image', 'an image that appears in several poems, developing meaning across the collection'),
         ('sequence', 'a group of poems arranged to be read together, often developing a narrative or theme'),
         ('volta', 'a turn in thought within a poem')],
  facts=[('Two poems titled "Tide" and "Tide (II)" by the same poet invite readers to:', 'Compare how a recurring image changes', ['Ignore the first poem', 'Read them as translations', 'Treat them as unrelated'], 'The sequel title signals development.'),
         ('Studying a poet\'s recurring images across a collection helps to identify:', 'The poet\'s central preoccupations and their development', ['The poet\'s biography only', 'The metre of every poem', 'The publisher\'s choices'], 'Patterns reveal concerns.')],
  why=[('Explain why recurring images matter more in a collection than in a single poem.', 'Across a collection an image gathers associations and changes, revealing development in the poet\'s attitude.'),
       ('Explain why the order of poems in a collection can matter.', 'Sequence creates juxtapositions and narratives, so placement can change how individual poems are read.'),
       ('Explain why translated poetry may make recurring images more important to analyse than sound.', 'Images often survive translation better than rhyme and rhythm, so they are a more reliable focus.')],
  contrast=[('a single poem', 'a body of poems', 'A single poem is read on its own; a body of poems is read as one work, so patterns, development and contrasts across poems become significant.')],
  misc=[('Each poem in a collection should be analysed in isolation.', 'Poems in a collection speak to each other; analysis gains depth by tracing connections and contrasts.')],
  evaluate=[('A poet\'s recurring images reveal their deepest concerns.', ['repetition signals preoccupation', 'development shows change'], ['repetition can be stylistic habit', 'readers may over-read patterns'], 'Usually true if supported by context and development, not mere frequency.')],
  extended=[('Compare how a recurring image functions in two poems from a collection you have studied.', 'Indicative content: image identified; analysis in each; development; link to concerns.', 8, 'long')])
pq('ch03-st1', ('C2', 'C3', 'C4'), (1, 5), {'poem'}, 'motif', ['How does the recurring image connect the two poems?',
                                                             'Analyse how the image of the boat and the water develops across the poems.',
                                                             'Explain what changes between the two poems and what remains the same.',
                                                             'Evaluate how reading the poems together changes the meaning of each.'])
pq('ch03-st1', ('C2', 'C3'), (1, 5), {'poem'}, 'imagery', ['Analyse the imagery of this poem.', 'Explain the effect of one image in the poem.', 'How does figurative language shape the poem\'s meaning?'])
pq('ch03-st1', ('C3', 'C4'), (2, 5), {'trans'}, 'trans', ['How does the translation affect the imagery of the poem?', 'Evaluate what the translation preserves and what it loses.'])

H('ch03-st2',
  terms=[('marginalised voice', 'the perspective of a person or group excluded from power or mainstream representation'),
         ('persona', 'a constructed voice or character through which a poet or writer speaks'),
         ('testimony', 'a first-hand account of experience, especially of injustice or trauma'),
         ('subaltern', 'a person or group excluded from hegemonic power structures (Gayatri Spivak asked "Can the subaltern speak?")')],
  facts=[('Gayatri Chakravorty Spivak\'s essay "Can the Subaltern Speak?" is associated with:', 'Postcolonial criticism', ['Formalism', 'Romanticism', 'Structural linguistics'], 'It questions who can speak for the oppressed.'),
         ('A poem in which Penelope speaks back to the Odyssey gives voice to:', 'A character marginalised in the original narrative', ['The hero of the epic', 'The poet\'s publisher', 'An omniscient narrator'], 'Penelope\'s perspective is foregrounded.')],
  why=[('Explain why writers give voice to marginalised characters.', 'Voicing the marginalised challenges dominant narratives, creates empathy and reveals injustice from inside.'),
       ('Explain why speaking for others raises ethical questions.', 'Writers from outside a group may misrepresent or appropriate experiences; authenticity and respect become issues.'),
       ('Explain how form can enact marginalisation.', 'Fragmented syntax, silences or short lines can mirror being unheard, making the form part of the meaning.')],
  contrast=[('speaking for', 'speaking with', 'Speaking for represents others\' experience in one\'s own voice, risking appropriation; speaking with involves the marginalised in shaping their own representation.')],
  misc=[('Any text with a poor or oppressed character gives voice to the marginalised.', 'Presence is not voice; a text may depict marginalised people only through others\' eyes.')],
  evaluate=[('Literature can genuinely give voice to the voiceless.', ['testimony and persona create empathy', 'it preserves suppressed stories'], ['writers may speak over the marginalised', 'voice in a book is not political power'], 'It can amplify voices, especially when written by or with those affected, but it is not a substitute for political voice.')],
  extended=[('Analyse how a work you have studied presents the perspective of a marginalised character or speaker.', 'Indicative content: who is marginalised; methods of voice; reader positioning; ethical evaluation.', 8, 'long')])
pq('ch03-st2', ('C2', 'C3', 'C4'), (1, 5), {'poem', 'trans', 'memoir', 'fanfic'}, 'speaker', ['How does the text give voice to a marginalised perspective?',
                                                                                          'Analyse how the speaker\'s voice challenges how they have been represented.',
                                                                                          'Evaluate how effectively the text gives voice to someone previously unheard.'])
pq('ch03-st2', ('C3', 'C4'), (2, 5), {'trans', 'speech'}, 'power', ['How does the text present the perspective of someone with less power?'])
pq('ch03-st2', 'C3', (2, 5), {'speech'}, 'dev', DEV_Q)

H('ch03-st3',
  terms=[('epiphany', 'a sudden moment of insight or revelation for a character, associated with James Joyce\'s short stories'),
         ('compression', 'the short story\'s economy: suggesting much through few words, a small cast and a single situation'),
         ('open ending', 'an ending that leaves the outcome or meaning unresolved for the reader to consider'),
         ('in medias res', 'beginning in the middle of the action')],
  facts=[('James Joyce\'s idea of "epiphany" is most closely associated with the stories in which collection?', 'Dubliners', ['Ulysses', 'Finnegans Wake', 'A Portrait of the Artist as a Young Man only'], 'The stories in Dubliners (1914) often turn on moments of revelation.'),
         ('A short story that ends with "She picked up the phone again." without revealing her decision has:', 'An open ending', ['Full closure', 'A frame narrative', 'An epilogue'], 'The outcome is left unresolved.')],
  why=[('Explain why short stories often focus on a single moment.', 'Limited length favours intensity: a single moment can reveal a whole life through implication.'),
       ('Explain why open endings are common in short stories.', 'They trust the reader to complete meaning, leave the epiphany resonating and suit the form\'s emphasis on suggestion.'),
       ('Explain how compression affects characterisation in a short story.', 'Characters are revealed through telling details and actions rather than extended development, so every detail matters.')],
  contrast=[('a short story', 'a novel', 'A short story is compressed, usually focused on one situation and a few characters, and often ends with an epiphany or open ending; a novel has space for multiple plots, development and extended characterisation.')],
  misc=[('Short stories are simply shorter novels.', 'The short story has its own aesthetics – compression, implication, epiphany – distinct from the novel.')],
  evaluate=[('Open endings are a weakness in short stories.', ['readers may feel cheated', 'meaning may seem vague'], ['they invite active interpretation', 'they suit the form\'s compression'], 'Open endings are a strength when the story has prepared the reader to think beyond it.')],
  extended=[('Write a short story (about 400 words) that ends with an epiphany, then explain how you used compression.', 'Indicative content: single situation; telling details; clear epiphany; commentary.', 10, 'long')])
pq('ch03-st3', ('C2', 'C3', 'C4'), (1, 5), {'story'}, 'story', ['How does the writer use the short story form in this extract?',
                                                              'Analyse how the ending creates meaning.',
                                                              'Explain how the extract uses compression to suggest more than it states.',
                                                              'Evaluate the effectiveness of the ending of this short story.'])
pq('ch03-st3', 'C3', (1, 4), {'story'}, 'dev', DEV_Q)


# =============================================================================================
# ch04 Literary work 6 – graphic novel or literary non-fiction
# =============================================================================================
H('ch04-st1',
  terms=[('panel', 'a single framed image in a comic or graphic novel'),
         ('gutter', 'the space between panels, where the reader infers what happens between images (closure)'),
         ('closure', 'the reader\'s mental act of connecting separate panels into a continuous sequence (Scott McCloud)'),
         ('splash page', 'a full-page single panel used for dramatic effect'),
         ('speech balloon', 'the shape containing a character\'s words; its style can convey tone'),
         ('caption', 'text in a box conveying narration rather than speech')],
  facts=[('Scott McCloud\'s term for how readers fill in what happens in the gutter is:', 'Closure', ['Anchorage', 'Focalisation', 'Enjambment'], 'Understanding Comics (1993).'),
         ('A speech balloon filled with jagged scribbles most likely shows:', 'That the listener cannot understand the speech', ['A whisper', 'A song', 'A flashback'], 'It visualises incomprehension.'),
         ('Which graphic memoir uses animals – mice for Jews and cats for Nazis – to represent the Holocaust?', "Art Spiegelman's Maus", ["Marjane Satrapi's Persepolis", "Alison Bechdel's Fun Home", "Joe Sacco's Palestine"], 'Maus uses an animal metaphor.')],
  why=[('Explain why panel size can control pace in a graphic novel.', 'Large panels slow the reader and emphasise moments; small, repeated panels speed up action or create rhythm.'),
       ('Explain why the gutter is important in graphic narratives.', 'Readers must infer what happens between panels, so the gutter creates participation, ellipsis and sometimes shock.'),
       ('Explain why colour (or its absence) is a powerful choice in graphic novels.', 'Colour carries mood and symbolism; selective colour can focus attention on emotional moments.')],
  contrast=[('a caption', 'a speech balloon', 'A caption contains narration, often retrospective; a speech balloon contains a character\'s words in the moment.'),
            ('a panel', 'a gutter', 'A panel is a framed image; the gutter is the space between panels in which the reader infers action.')],
  apply=[('A graphic novelist wants to show a character\'s sudden shock. Suggest two layout choices and explain their effect.', 'For example: a sudden splash page after small panels to create impact; a wordless close-up panel; breaking the panel border; each controls pace and emphasis.', 3),
         ('Explain how leaving a wide gutter between two panels showing "before" and "after" a violent event can affect the reader.', 'The reader must imagine the event in the gutter (closure), which can be more disturbing than showing it and makes the reader complicit.', 3),
         ('Describe how a graphic novel could show the difference between a character\'s thoughts and speech.', 'Thought bubbles or captions for thoughts and speech balloons for speech; contrasting fonts or colours; a gap between what is said and shown creates irony.', 3),
         ('Persepolis is drawn in stark black and white. Suggest one effect of this choice on the representation of the Iranian revolution.', 'Black and white simplifies and stylises, universalising the experience, echoing the child\'s perspective and making violence bearable to look at while still shocking.', 3)],
  misc=[('Graphic novels are easier to read than prose novels.', 'They require visual literacy: readers decode panels, gutters, colour and the interplay of word and image.')],
  evaluate=[('The graphic form can represent experience more powerfully than prose.', ['images create immediacy', 'form can show perception directly'], ['prose offers interiority and nuance', 'images can simplify'], 'Each form has distinctive powers; the graphic form excels at perception and juxtaposition.')],
  extended=[('Describe in words a one-page graphic sequence (four to six panels) showing a moment of tension, and explain your choices of panel size, gutter and word–image relationship.', 'Indicative content: clear sequence; deliberate panel choices; commentary on pace and closure.', 8, 'long')])
pq('ch04-st1', ('C2', 'C3', 'C4'), (1, 5), {'graphic'}, 'graphic', ['How does the page use the resources of the graphic form?',
                                                                   'Analyse the relationship between words and images on this page.',
                                                                   'Explain how panel layout and colour shape the reader\'s experience.',
                                                                   'Evaluate how the graphic form conveys what words alone could not.'])
pq_dev_mcq('ch04-st1', {'graphic'})
pq('ch04-st1', 'C3', (2, 4), {'graphic'}, 'visual', VIS_Q)

H('ch04-st2',
  terms=[('memoir', 'a non-fiction narrative of the writer\'s own experiences, shaped by memory and reflection'),
         ('literary non-fiction', 'factual writing that uses literary techniques such as narrative, imagery and voice'),
         ('constructed self', 'the version of the writer presented in autobiographical writing, shaped by selection and narration'),
         ('autobiographical pact', 'the implied agreement that author, narrator and protagonist of an autobiography are the same person (Philippe Lejeune)')],
  facts=[('A memoirist admits her memory of a yellow kitchen is factually wrong but keeps it. This illustrates:', 'The difference between emotional and factual truth in memoir', ['Fabrication for profit', 'Objective reporting', 'Stream of consciousness'], 'Memoir constructs a self through memory.'),
         ('The idea of an "autobiographical pact" was developed by:', 'Philippe Lejeune', ['Roland Barthes', 'Aristotle', 'Edward Said'], 'Lejeune (1975).')],
  why=[('Explain why memoir is a constructed text even though it is non-fiction.', 'The writer selects, orders and shapes events and voice, so the self presented is a representation, not a transcript of life.'),
       ('Explain why memoirists often reflect on the unreliability of memory.', 'Admitting uncertainty builds trust and makes the text about how we remember, not only what happened.'),
       ('Explain why testimony can carry special authority.', 'First-hand witness gives credibility and moral weight, especially for events others deny or forget.')],
  contrast=[('memoir', 'autobiography', 'Autobiography usually covers a whole life chronologically; memoir focuses on particular experiences or themes and foregrounds memory and reflection.')],
  misc=[('Memoir is simply true and should not be analysed like fiction.', 'Memoir uses narrative and literary techniques and constructs a self; it can and should be analysed for its choices.')],
  evaluate=[('Memoirists have a duty to tell the factual truth.', ['readers trust the autobiographical pact', 'misrepresentation can harm others'], ['memory is inherently selective', 'emotional truth matters'], 'Memoirists owe honesty about what they know and do not know, even if perfect factual truth is impossible.')],
  extended=[('Write a memoir extract (about 300 words) about a vivid childhood memory, including a moment where you question your own memory.', 'Indicative content: retrospective voice; sensory detail; reflection on memory; controlled style.', 10, 'long')])
pq('ch04-st2', ('C2', 'C3', 'C4'), (1, 5), {'memoir', 'graphic'}, 'memory', ['How does the writer present memory in this extract?',
                                                                          'Analyse how the extract constructs the writer\'s self.',
                                                                          'Explain what the extract suggests about the reliability of memory.',
                                                                          'Evaluate how the extract balances truth and memory.'])
pq('ch04-st2', 'C3', (1, 4), {'memoir'}, 'dev', DEV_Q)

H('ch04-st3',
  terms=[('trauma narrative', 'a text that represents traumatic experience, often through fragmentation, repetition and silence'),
         ('postmemory', 'the relationship of the next generation to the traumatic experiences of their parents, known through stories and images (Marianne Hirsch)'),
         ('hybrid work', 'a work that combines forms or genres, such as graphic memoir or documentary fiction'),
         ('historiography', 'the study of how history is written and represented')],
  facts=[('Marianne Hirsch\'s term for the second generation\'s inherited memory of trauma is:', 'Postmemory', ['Intertextuality', 'Defamiliarisation', 'Catharsis'], 'Hirsch developed the term partly through Maus.'),
         ('Maus frames Vladek\'s Holocaust testimony with scenes of Art interviewing him. This structure mainly:', 'Shows the making of memory and its effect on the next generation', ['Removes the father\'s voice', 'Presents history without mediation', 'Turns the book into fiction'], 'The frame foregrounds transmission.')],
  why=[('Explain why trauma narratives often use fragmentation.', 'Trauma disrupts memory and resists coherent telling, so fragmented form mirrors the experience and its aftermath.'),
       ('Explain why hybrid forms suit representations of history.', 'Combining image and word, or fact and reflection, allows writers to show both events and the difficulty of representing them.'),
       ('Explain why some writers include their own process of research in works about history.', 'It acknowledges mediation, questions authority and shows history as constructed through sources and memory.')],
  contrast=[('history', 'memory', 'History is the documented, often institutional account of the past; memory is personal or collective recollection, selective and emotional. Hybrid works often explore the gap.')],
  misc=[('Representing trauma accurately means showing as much violence as possible.', 'Many works convey trauma through silence, ellipsis and understatement, which can be more truthful and ethical.')],
  evaluate=[('Some events are too traumatic to be represented in art.', ['art may trivialise suffering', 'aestheticising atrocity raises ethical problems'], ['representation preserves memory and testimony', 'works like Maus show it can be done responsibly'], 'Representation is possible and necessary, but demands ethical awareness of form and audience.')],
  extended=[('Analyse how a hybrid work you have studied represents history and trauma.', 'Indicative content: form; specific techniques; ethical considerations; evaluation.', 8, 'long')])
pq('ch04-st3', ('C2', 'C3', 'C4'), (1, 5), {'graphic', 'memoir'}, 'memory', ['How does the text represent the relationship between past and present?',
                                                                          'Analyse how the text conveys traumatic or displaced memory.',
                                                                          'Evaluate how the form of the text helps represent history.'])
pq('ch04-st3', ('C3', 'C4'), (2, 5), {'graphic', 'memoir', 'photo'}, 'gqa', ['Guiding question: {gq}\nWrite an analytical paragraph that answers the guiding question.'], crit=MARKBAND)


# =============================================================================================
# ch05 Non-literary body of work – adaptation across media
# =============================================================================================
H('ch05-st1',
  terms=[('fidelity criticism', 'judging an adaptation mainly by how faithful it is to its source'),
         ('transposition', 'an adaptation that keeps the story but moves it to a new medium with minimal change'),
         ('commentary', 'an adaptation that alters the source to comment on it or on the new context'),
         ('voice-over', 'narration heard over the images of a film, sometimes used to preserve a novel\'s narrator'),
         ('externalisation', 'showing inner thoughts or feelings through visible action, image or sound in performance media')],
  facts=[('A film critic who complains that an adaptation "is not like the book" is practising:', 'Fidelity criticism', ['Reader response', 'Postcolonial criticism', 'Formalism'], 'Judging by faithfulness to the source.'),
         ('Which technique can preserve a first-person narrator\'s voice in film?', 'Voice-over narration', ['A splash page', 'Enjambment', 'A standfirst'], 'Voice-over lets the narrator speak over the images.')],
  why=[('Explain why first-person narration is difficult to adapt for the screen.', 'Film shows from outside; a narrator\'s inner voice, irony and reflection must be externalised through images, performance or voice-over, which changes their effect.'),
       ('Explain why judging an adaptation only by fidelity is limited.', 'An adaptation is a new text for a new medium and audience; changes can be creative interpretations that reveal new meaning.'),
       ('Explain why adaptations often update their settings.', 'Moving a story to a new time or place makes it relevant to current audiences and comments on what has or has not changed.')],
  contrast=[('a novel', 'its film adaptation', 'A novel uses words, narration and the reader\'s imagination over many hours; a film uses images, sound, performance and editing in a limited time, so it must compress and externalise.')],
  misc=[('A good adaptation must include every scene from the book.', 'Adaptations select, compress and reinterpret; leaving out scenes can strengthen the new work.')],
  evaluate=[('An adaptation should be judged as a work in its own right, not as a version of its source.', ['each medium has its own strengths', 'audiences may not know the source'], ['adaptations invite comparison', 'changes carry meaning only in relation to the source'], 'Both perspectives matter: an adaptation is a new work that gains meaning from dialogue with its source.')],
  extended=[('Evaluate how a film or stage adaptation of a literary work you have studied transforms its source.', 'Indicative content: specific scenes compared; choices of film/stage language; effect on meaning; evaluation beyond fidelity.', 8, 'long')])
pq('ch05-st1', ('C2', 'C3', 'C4'), (1, 5), {'script', 'review'}, 'adapt', ['How does this text show the transformation of a story from page to screen?',
                                                                         'Analyse what is gained and lost in this adaptation.',
                                                                         'Explain how the screen version externalises what the written version expresses through narration.',
                                                                         'Evaluate the choices made in adapting this material for the screen.'])
pq('ch05-st1', 'C3', (2, 4), {'review'}, 'dev', DEV_Q)

H('ch05-st2',
  terms=[('shot type', 'the distance of the camera from its subject, e.g. extreme long shot, medium shot, close-up'),
         ('camera angle', 'the position of the camera relative to the subject, e.g. high angle (diminishing) or low angle (empowering)'),
         ('editing', 'the selection and arrangement of shots, including cuts, cross-cutting and montage'),
         ('diegetic sound', 'sound that exists within the world of the film, such as dialogue or a ringing phone'),
         ('non-diegetic sound', 'sound added for the audience, such as a score or voice-over'),
         ('mise-en-scène', 'everything placed in front of the camera: setting, props, costume, lighting and actors\' positions')],
  facts=[('A low-angle shot usually makes the subject appear:', 'Powerful or imposing', ['Weak or vulnerable', 'Distant and small', 'Out of focus'], 'Looking up at the subject gives it stature.'),
         ('A film\'s orchestral score that the characters cannot hear is:', 'Non-diegetic sound', ['Diegetic sound', 'Foley only', 'Mise-en-scène'], 'It exists only for the audience.'),
         ('An extreme long shot is mainly used to:', 'Establish setting and show the subject small within it', ['Show facial detail', 'Show an object in detail', 'Represent a character\'s thoughts'], 'It establishes space and scale.')],
  why=[('Explain why directors vary shot distance within a scene.', 'Moving between long shots and close-ups controls what the audience sees and feels – context, then emotion or detail – and builds tension.'),
       ('Explain how editing creates meaning.', 'Juxtaposing shots creates connections (the Kuleshov effect), controls pace and directs interpretation.'),
       ('Explain why sound design is as important as image.', 'Sound shapes mood, directs attention and can create tension through silence or amplification.')],
  contrast=[('diegetic sound', 'non-diegetic sound', 'Diegetic sound comes from within the story world (footsteps, dialogue); non-diegetic sound is added for the audience (score, narration).'),
            ('a high-angle shot', 'a low-angle shot', 'A high angle looks down, often making the subject seem vulnerable; a low angle looks up, often making it seem powerful.')],
  misc=[('Camera angles always have fixed meanings.', 'Conventions such as "low angle = power" are tendencies; context and combination determine meaning.')],
  evaluate=[('Sound matters more than image in creating tension in film.', ['silence and amplified sound create dread', 'scores manipulate emotion'], ['framing and editing control what is seen', 'images often carry key information'], 'They work together; tension usually comes from their combination.')],
  extended=[('Write a shot list (six shots) for the opening of a film adaptation of a poem or story you have studied, and justify each choice.', 'Indicative content: varied shot types, angles and sound; justification linked to meaning of the source.', 8, 'long')])
pq('ch05-st2', ('C2', 'C3', 'C4'), (1, 5), {'script'}, 'filmlang', ['Analyse how film language is used in this extract.',
                                                                   'Explain the effect of the shot types and sound in this extract.',
                                                                   'How do the camera and sound choices create meaning in this sequence?',
                                                                   'Evaluate how effectively the sequence uses film language to create tension or mood.'])
pq_dev_mcq('ch05-st2', {'script'})

H('ch05-st3',
  terms=[('fan fiction', 'stories written by fans using characters or worlds from existing texts, often shared online'),
         ('remix culture', 'a culture in which people create new works by combining and altering existing ones'),
         ('participatory culture', 'a culture in which audiences actively create and share content rather than only consuming it (Henry Jenkins)'),
         ('transformative work', 'a new work that adds new expression, meaning or purpose to the source')],
  facts=[('Henry Jenkins is associated with the idea of:', 'Participatory culture', ['The male gaze', 'The death of the author', 'Postmemory'], 'Jenkins studied fan communities.'),
         ('A story that imagines Charlotte Lucas\'s private life after her marriage in Pride and Prejudice is:', 'Fan fiction', ['A literal translation', 'A news report', 'An advertisement'], 'It extends a source text\'s characters.')],
  why=[('Explain why fan fiction is a form of intertextuality.', 'It depends on and responds to its source, reinterpreting characters and filling gaps the original leaves.'),
       ('Explain why fan fiction often focuses on minor characters.', 'Minor characters have gaps in their stories that fans can fill, often giving voice to perspectives the original neglected.'),
       ('Explain why remix culture challenges traditional ideas of authorship.', 'When many people rework texts, meaning is collaborative and the idea of a single original author becomes less central.')],
  contrast=[('fan fiction', 'parody', 'Fan fiction extends a source with affection or curiosity, often within its world; parody imitates in order to mock or criticise.')],
  misc=[('Fan fiction is just copying.', 'Transformative fan fiction changes perspective, genre or meaning and can offer serious reinterpretation of its source.')],
  evaluate=[('Fan fiction has as much literary value as published fiction.', ['it can be inventive and critical', 'it democratises writing'], ['quality varies widely', 'it depends on another author\'s creation'], 'Value depends on the individual work; the form itself is not inferior.')],
  extended=[('Write a short piece of fan fiction (about 300 words) that gives a minor character from a work you have studied a new perspective, then explain how it transforms the source.', 'Indicative content: recognisable source; consistent voice; clear transformation; commentary.', 10, 'long')])
pq('ch05-st3', ('C2', 'C3', 'C4'), (1, 5), {'fanfic', 'parody', 'poem'}, 'intertext', ['How does this text transform its source?',
                                                                                    'Analyse how the text relies on and changes an earlier work.',
                                                                                    'Evaluate this text as a transformative work.'])
pq('ch05-st3', 'C3', (2, 4), {'fanfic'}, 'fanfic', ['Explain how this fan fiction reinterprets its source.'])

H('ch05-st4',
  terms=[('comparative learner portfolio entry', 'a portfolio entry comparing a literary extract with its adaptation to explore transformation'),
         ('adaptation choice', 'a decision in adapting a text, such as cutting, adding, externalising or updating'),
         ('medium specificity', 'the idea that each medium has distinctive capacities that shape what it can express')],
  facts=[('In a learner portfolio entry comparing a novel extract and its film version, the most useful focus is:', 'How specific choices in each medium shape meaning', ['Which version the student enjoyed more', 'The actors\' biographies', 'The box-office figures'], 'Analysis of choices is central.'),
         ('A screenplay that shows a child scratching marks on a crate instead of a narrator saying "I counted the boats" is an example of:', 'Externalisation', ['Voice-over', 'Fidelity criticism', 'Free indirect discourse'], 'Inner action is made visible.')],
  why=[('Explain why comparing an extract with its adaptation is useful in the learner portfolio.', 'It reveals medium specificity and the interpretive choices of the adapter, preparing for discussion of transformation and intertextuality.'),
       ('Explain why the portfolio entry should include reflection as well as comparison.', 'Reflection on one\'s response to each version develops awareness of how form shapes reader and viewer experience.')],
  contrast=[('a literary extract', 'its screen version', 'The literary extract uses narration and the reader\'s imagination; the screen version uses image, sound and performance to make choices visible and concrete.')],
  misc=[('A portfolio comparison should decide which version is better.', 'It should analyse how each creates meaning; evaluation is welcome but should be based on analysis, not preference.')],
  apply=[('List three points you would include in a learner portfolio entry comparing a novel\'s opening with its film adaptation.', 'For example: how narration is replaced (voice-over or image); what is added or cut and why; how setting is visualised; a reflective question.', 3),
         ('In a portfolio entry, compare how a novel and its film might present the same moment of silence between two characters.', 'Novel: narration can describe each character\'s thoughts during the silence; film: actors\' expressions, framing (two-shot or shot/reverse shot), duration and sound design convey it; each medium creates different access to inner life.', 4),
         ('Explain why a film adaptation might add a scene that is not in the novel, and how you would comment on it in a portfolio entry.', 'Added scenes can externalise inner conflict, update context or clarify plot; the entry should analyse how the addition changes meaning and evaluate its effect.', 3),
         ('A stage version of a novel uses a narrator who addresses the audience directly. Explain the effect, compared with the novel.', 'It preserves the narrator\'s voice and irony but makes them a visible, physical presence, breaking the fourth wall and creating intimacy with the audience.', 3),
         ('A film cuts a novel\'s first-person narration entirely. Suggest two techniques the film might use instead and their effects.', 'Close-ups and performance to convey emotion; visual motifs or symbolic objects; editing (cross-cutting) to show connections; each externalises inner life.', 4)],
  evaluate=[('Learner portfolio comparisons of adaptations are more useful for the HL essay than for Paper 2.', ['the HL essay can focus on non-literary bodies of work', 'portfolio ideas can become lines of inquiry'], ['Paper 2 compares literary works and also benefits from thinking about form', 'skills transfer'], 'They are useful for both, though more directly for the HL essay and IO.')],
  extended=[('Write a learner portfolio entry (about 300 words) comparing a literary extract with its screen or stage adaptation.', 'Indicative content: specific choices; medium specificity; effect on meaning; reflection.', 8, 'long')])
pq('ch05-st4', 'C3', (2, 5), {'review'}, 'adapt', ['Use this review in a learner portfolio entry: what does it suggest about adapting first-person narration?',
                                                    'Note in your learner portfolio how this review evaluates the adaptation, and whether you agree.'])
pq('ch05-st4', ('C3', 'C4'), (2, 5), {'script'}, 'adapt', ['Write a learner portfolio entry comparing this screen version with a written version of the scene: what does each medium make possible?',
                                                          'In a learner portfolio note, record two adaptation choices in this extract and their effects.'])


# =============================================================================================
# ch06 Non-literary body of work – satire, parody and humour
# =============================================================================================
SAT = {'satire', 'cartoon', 'parody'}
H('ch06-st1',
  terms=[('satire', 'the use of humour, irony, exaggeration or ridicule to expose and criticise folly or vice, especially in politics and society'),
         ('irony', 'a gap between what is said and what is meant, or between expectation and reality'),
         ('incongruity', 'a mismatch between elements (e.g. serious form and trivial content) that produces humour'),
         ('Horatian satire', 'gentle, playful satire that mocks human folly with amusement'),
         ('Juvenalian satire', 'bitter, angry satire that attacks corruption and vice with contempt'),
         ('deadpan', 'humour delivered with a straight face, without signalling that it is a joke')],
  facts=[('Jonathan Swift\'s A Modest Proposal (1729) is a classic example of:', 'Juvenalian satire', ['Pastoral elegy', 'Horatian ode', 'Gothic romance'], 'Its savage irony attacks the treatment of the Irish poor.'),
         ('A satirical article reporting that a government will rename the housing crisis a "housing opportunity" mainly uses:', 'Exaggeration and mock euphemism', ['Pathetic fallacy', 'Stream of consciousness', 'Iambic pentameter'], 'It exaggerates political spin.')],
  why=[('Explain why satire often imitates serious genres such as news reports.', 'The serious form creates incongruity with absurd content and lets the target condemn itself in its own style.'),
       ('Explain why irony is central to satire.', 'Saying the opposite of what is meant invites the reader to see the truth the irony exposes, making them complicit in the critique.'),
       ('Explain why satire can fail with some audiences.', 'Readers who miss the irony may take it literally or agree with what is mocked, so satire depends on shared knowledge and values.')],
  contrast=[('Horatian satire', 'Juvenalian satire', 'Horatian satire is gentle and amused, mocking folly; Juvenalian satire is bitter and angry, attacking vice and corruption.'),
            ('satire', 'parody', 'Satire criticises a target (often social or political) through humour; parody imitates a specific text or genre. Parody is often a tool of satire.')],
  misc=[('Satire is just comedy and has no serious purpose.', 'Satire uses comedy to criticise and provoke change; its purpose is moral or political.')],
  evaluate=[('Satire changes nothing; it only makes people laugh.', ['audiences may enjoy satire without acting', 'it can breed cynicism'], ['satire has exposed hypocrisy and shifted opinion', 'it gives voice to dissent under repression'], 'Satire rarely causes change directly, but it shapes public attitudes and holds power to account.')],
  extended=[('Write a short satirical news article (about 250 words) on an issue in your school or community, then explain the satirical techniques you used.', 'Indicative content: clear target; irony, exaggeration, deadpan; news conventions; commentary.', 10, 'long')])
pq('ch06-st1', ('C2', 'C3', 'C4'), (1, 5), SAT, 'satire', ['Identify the target of the satire and explain the methods used.',
                                                         'How does the text use irony and exaggeration to criticise its target?',
                                                         'Analyse how incongruity creates humour in this text.',
                                                         'Evaluate how effective the satire is for its intended audience.'])
pq_tone_mcq('ch06-st1', SAT)
pq_dev_mcq('ch06-st1', SAT)

H('ch06-st2',
  terms=[('political cartoon', 'a drawing that comments on political events or figures, usually through caricature, symbolism and captions'),
         ('caricature', 'exaggeration of a person\'s features for comic or critical effect'),
         ('visual metaphor', 'an image that represents one thing in terms of another, such as scales for justice'),
         ('satirical journalism', 'journalism or parody news that uses humour to criticise public life'),
         ('label', 'a word written on part of a cartoon to identify what it represents (anchorage)')],
  facts=[('In a cartoon, writing "Annual profit" on a pile of banknotes is an example of:', 'A label used for anchorage', ['A gutter', 'Diegetic sound', 'Enjambment'], 'Labels fix the meaning of symbols.'),
         ('Why do political cartoons often rely on familiar symbols (scales, crowns, ships)?', 'Readers decode them instantly, so the cartoon can make its point in a single glance', ['They are required by law', 'They hide the cartoonist\'s view', 'They avoid any interpretation'], 'Shared symbols aid quick reading.')],
  why=[('Explain why studying cartoons as a body of work is valuable.', 'Patterns across cartoons reveal a cartoonist\'s or publication\'s stance, recurring symbols and changes over time.'),
       ('Explain why political cartoons are often controversial.', 'They exaggerate and simplify, target powerful people and can offend groups; their power lies in provocation.'),
       ('Explain how a cartoon can use an earlier story to make its point.', 'Allusion to a familiar story (e.g. a fable) transfers its moral to the present situation, adding meaning economically.')],
  contrast=[('a political cartoon', 'a satirical news article', 'A cartoon makes its point mainly through image, caricature and caption in a single glance; a satirical article uses written irony and parody of news style over several sentences.')],
  misc=[('Political cartoons are fair because they are only jokes.', 'Cartoons are persuasive arguments that simplify and exaggerate; they can be unfair and should be read critically.')],
  evaluate=[('Political cartoons are more powerful than written satire.', ['images are immediate and shareable', 'they cross language barriers'], ['writing can develop complex arguments', 'images can be misread'], 'Cartoons are more immediate; written satire can be more developed – power depends on context and audience.')],
  extended=[('Analyse how two cartoons from a body of work you have studied criticise the same target.', 'Indicative content: symbols, caricature, labels, captions; comparison; evaluation.', 8, 'long')])
pq('ch06-st2', ('C2', 'C3', 'C4'), (1, 5), {'cartoon'}, 'visual', VIS_Q + ['Evaluate how the cartoon uses visual exaggeration to make its argument.'])
pq('ch06-st2', ('C3', 'C4'), (2, 5), {'cartoon', 'satire'}, 'satire', ['Explain the target and the methods of this satirical text.', 'How does the text use humour to make a serious point?'])
pq_para('ch06-st2', {'cartoon', 'satire'})

H('ch06-st3',
  terms=[('parody advertising', 'imitation of an advertisement\'s style to criticise the product, brand or consumer culture'),
         ('culture jamming', 'activist practice of altering or parodying media and advertising to subvert their messages'),
         ('subvertising', 'altering an existing advertisement so that it criticises itself'),
         ('détournement', 'turning an existing image or text against its original meaning (a term from the Situationists)')],
  facts=[('Altering a soft-drink billboard to read "OPEN DECAY" is an example of:', 'Culture jamming (subvertising)', ['Product placement', 'Native advertising', 'Sponsorship'], 'It turns the advert against itself.'),
         ('Adbusters is a magazine associated with:', 'Culture jamming', ['Fashion advertising', 'Celebrity news', 'Sports journalism'], 'Adbusters popularised spoof ads.')],
  why=[('Explain why parody advertising keeps the visual style of the original.', 'Recognising the style is essential: the critique works by making the familiar format say what it usually hides.'),
       ('Explain why culture jamming is a form of intertextuality.', 'Its meaning depends on the viewer recognising the original advert and noticing the alteration.')],
  contrast=[('an advertisement', 'a parody advertisement', 'An advertisement uses persuasive conventions to sell; a parody advertisement imitates those conventions to criticise the product, brand or consumerism.')],
  misc=[('Parody adverts are just vandalism with no meaning.', 'They are deliberate texts that use intertextual techniques to critique advertising; legality aside, they communicate arguments.')],
  apply=[('Design (in words) a parody of a fast-food advert that criticises its health effects. Name two conventions you would imitate and how you would subvert them.', 'For example: imitate the glossy close-up and upbeat slogan; subvert by altering the slogan ("I\'m clogging it") and adding a mock nutrition footnote. Explanation of effect.', 4),
         ('Explain how a parody advert could backfire on the activists who made it.', 'It might give the brand free publicity, be enjoyed as a joke without changing behaviour, or alienate viewers who see it as preachy.', 3)],
  evaluate=[('Culture jamming is an effective way to challenge consumer culture.', ['it uses the brand\'s visibility', 'it provokes thought in public spaces'], ['it is easily co-opted by brands', 'audiences may enjoy it without changing behaviour'], 'It is effective at provoking reflection but limited in changing consumption.')],
  extended=[('Evaluate how a parody advertisement you have studied uses the conventions of its target genre to criticise it.', 'Indicative content: conventions imitated; subversions; effect; evaluation.', 8, 'long')])
pq('ch06-st3', ('C2', 'C3', 'C4'), (1, 5), {'parody'}, 'satire', ['How does the parody advertisement criticise its target?',
                                                                 'Analyse how the text imitates and subverts the conventions of advertising.',
                                                                 'Evaluate the effectiveness of this culture-jamming text.'])
pq('ch06-st3', ('C2', 'C3'), (1, 4), {'parody'}, 'dev', DEV_Q)
pq('ch06-st3', 'C3', (2, 5), {'parody'}, 'intertext', ['How does the meaning of this text depend on the original it imitates?'])


# =============================================================================================
# ch07 Non-literary body of work – campaigns and public communication
# =============================================================================================
CAMP = {'campaign', 'appeal', 'infographic', 'propaganda'}
H('ch07-st1',
  terms=[('public-health campaign', 'a coordinated set of texts designed to change health-related behaviour in a population'),
         ('fear appeal', 'a persuasive strategy that warns of negative consequences to motivate change'),
         ('cross-platform campaign', 'a campaign whose message is adapted for posters, social media, video and other platforms'),
         ('call to action', 'an instruction that tells the audience what to do'),
         ('behavioural nudge', 'a design feature that steers people towards a choice without forcing it')],
  facts=[('A campaign showing a toddler reaching for cigarettes with the line "They copy everything you do" mainly appeals to:', 'Parental responsibility and guilt', ['Fear of legal punishment', 'Humour', 'Scientific curiosity'], 'It uses love and guilt.'),
         ('Why do campaigns adapt messages across platforms?', 'Each platform has different audiences, formats and conventions', ['To confuse audiences', 'Because messages must change completely', 'To avoid a call to action'], 'Cross-platform campaigns tailor delivery.')],
  why=[('Explain why public-health campaigns combine emotional appeals with practical help.', 'Emotion motivates, but without a clear, achievable action (a helpline) motivation may produce anxiety rather than change.'),
       ('Explain why fear appeals can backfire.', 'Too much fear can cause audiences to avoid the message or feel helpless; fear works best with a clear solution.'),
       ('Explain why charities and NGOs study their campaigns as a body of work.', 'Comparing texts across platforms and years shows which strategies work and how representation changes.')],
  contrast=[('a commercial advertisement', 'a public-health campaign', 'A commercial advertisement aims to sell a product for profit; a public-health campaign aims to change behaviour for social benefit, though both use persuasive techniques.')],
  misc=[('Public-health campaigns simply inform people of facts.', 'They are persuasive texts that use emotional appeals, imagery and calls to action, not just information.')],
  evaluate=[('Emotional appeals are more effective than statistics in public campaigns.', ['emotion motivates action', 'stories are memorable'], ['statistics give credibility', 'emotion without evidence can be dismissed as manipulation'], 'The most effective campaigns combine emotional appeal with credible evidence and a clear action.')],
  extended=[('Design a cross-platform campaign (poster, social post and short video concept) to encourage teenagers to sleep more, and justify how each text suits its platform.', 'Indicative content: consistent message; platform-specific conventions; appeals; call to action.', 10, 'long')])
pq('ch07-st1', ('C2', 'C3', 'C4'), (1, 5), CAMP, 'purp', PURP_Q + ['Evaluate how effectively the campaign text moves its audience towards action.'])
pq('ch07-st1', ('C2', 'C3'), (1, 4), CAMP, 'aud', AUD_Q)
pq('ch07-st1', ('C3', 'C4'), (2, 5), CAMP, 'visual', VIS_Q)
pq_para('ch07-st1', CAMP)

H('ch07-st2',
  terms=[('poverty porn', 'imagery that exploits the suffering of poor people to provoke pity and donations, often reinforcing stereotypes'),
         ('white saviour narrative', 'a representation in which (usually Western) donors or outsiders rescue passive victims'),
         ('dignity', 'respect for the worth and agency of the people represented'),
         ('agency', 'the capacity of people to act for themselves'),
         ('informed consent', 'permission given by subjects who understand how their image or story will be used')],
  facts=[('A charity letter showing a child with downcast eyes and promising to "change her life forever" for 5 euros has been criticised as:', 'Poverty porn and a saviour narrative', ['Neutral reporting', 'Culture jamming', 'Fan fiction'], 'It reduces the child to passive suffering.'),
         ('A refugee campaign that shows a child\'s drawing instead of her face is trying to:', 'Preserve dignity while creating empathy', ['Hide the charity\'s logo', 'Use a fear appeal', 'Avoid any call to action'], 'It avoids exploitative imagery.')],
  why=[('Explain why the representation of beneficiaries in charity campaigns is an ethical issue.', 'Images shape how audiences see whole communities; portraying people as helpless can reinforce stereotypes and deny their agency, even if it raises money.'),
       ('Explain why some NGOs now avoid images of suffering.', 'They seek to respect dignity, obtain consent, avoid compassion fatigue and represent beneficiaries as active people.'),
       ('Explain how a campaign can position the donor as the hero.', 'Language such as "you can change her life" makes the donor the agent of change and the recipient passive.')],
  contrast=[('an image of suffering', 'an image of agency', 'An image of suffering shows people as victims to provoke pity; an image of agency shows them acting, creating or speaking, inviting respect and solidarity.')],
  misc=[('If a campaign raises more money, its representation must be acceptable.', 'Effectiveness does not justify representations that demean people or reinforce harmful stereotypes; ethics and effectiveness must both be considered.')],
  evaluate=[('Charities are justified in using shocking images if they save lives.', ['funds raised have real benefits', 'shock overcomes indifference'], ['it reinforces stereotypes', 'it can violate dignity and consent'], 'Shock may be effective, but ethical campaigns seek ways to motivate without exploitation.')],
  extended=[('Compare the ethics of representation in two campaign texts you have studied.', 'Indicative content: specific images and language; dignity, agency, consent; evaluation.', 8, 'long')])
pq('ch07-st2', ('C2', 'C3', 'C4'), (1, 5), {'campaign', 'appeal', 'photo', 'website'}, 'ethics', ['What ethical questions does this campaign text raise?',
                                                                                            'Analyse how the text represents the people it seeks to help.',
                                                                                            'Explain whether this text respects the dignity of its subject.',
                                                                                            'Evaluate the ethics of the representation in this text.'])
pq('ch07-st2', ('C3', 'C4'), (2, 5), {'campaign', 'appeal', 'photo'}, 'gqa', ['Guiding question: {gq}\nWrite an analytical paragraph that answers the guiding question.'], crit=MARKBAND)

H('ch07-st3',
  terms=[('manifesto', 'a public declaration of the beliefs, aims and demands of a group or movement'),
         ('social movement', 'a collective effort by people to bring about or resist social or political change'),
         ('collective voice', 'the use of "we" to speak on behalf of a group'),
         ('slogan', 'a short, memorable phrase expressing a movement\'s message')],
  facts=[('The slogan "Nothing about us without us" is most associated with:', 'The disability-rights movement', ['The Romantic poets', 'The fashion industry', 'Advertising agencies'], 'It demands that disabled people be involved in decisions about them.'),
         ('Numbering the demands in a manifesto mainly:', 'Makes them clear, official and checkable', ['Hides them from readers', 'Makes them poetic', 'Shows uncertainty'], 'Lists give precision.')],
  why=[('Explain why manifestos use the collective "we".', 'It constructs a unified group identity, gives authority through numbers and invites readers to join.'),
       ('Explain why speeches at rallies are often short and repetitive.', 'They must be heard outdoors by crowds and quoted by media, so short, rhythmic, repeated lines are memorable.'),
       ('Explain why social movements borrow earlier slogans and speeches.', 'Intertextual echoes link the movement to past struggles, giving legitimacy and a sense of history.')],
  contrast=[('a manifesto', 'a speech', 'A manifesto is a written declaration of a group\'s aims and demands; a speech is spoken to a live audience, using oral techniques such as repetition and direct address.')],
  misc=[('Manifestos are only political party documents.', 'Artists, activists and youth movements also write manifestos; the form is any public declaration of aims.')],
  evaluate=[('An uncompromising tone makes a manifesto more effective.', ['it shows conviction', 'it inspires supporters'], ['it alienates moderates and decision-makers', 'compromise may be necessary'], 'It energises the base but may limit wider persuasion.')],
  extended=[('Write a manifesto (about 250 words) for a student movement on an issue that matters to you, using at least four persuasive techniques.', 'Indicative content: collective voice; numbered demands; slogan; call to action; controlled register.', 10, 'long')])
pq('ch07-st3', ('C2', 'C3', 'C4'), (1, 5), {'manifesto', 'speech'}, 'dev', DEV_Q + ['Evaluate how "{quote}" contributes to the collective voice of the text.'])
pq('ch07-st3', ('C3', 'C4'), (2, 5), {'manifesto', 'speech'}, 'struct', STRUCT_Q)
pq('ch07-st3', 'C3', (2, 4), {'manifesto', 'speech'}, 'ctx', CTX_Q)


# =============================================================================================
# ch08 Paper 2: reading the questions and choosing works
# =============================================================================================
H('ch08-st1',
  terms=[('Paper 2', 'the comparative essay exam: 1 hour 45 minutes, four general questions, students answer one by comparing two literary works studied; 30 marks'),
         ('key term', 'a word or phrase in the question that defines its focus and must be interpreted and addressed'),
         ('command phrase', 'the part of a question that tells students what to do, such as "In what ways and to what effect" or "Compare"'),
         ('scope', 'the range of material and ideas a question covers, which a student must interpret precisely')],
  facts=[('How long is Paper 2?', '1 hour 45 minutes', ['1 hour 15 minutes', '2 hours 15 minutes', '45 minutes'], 'Paper 2 is 1 h 45 at SL and HL.'),
         ('How many questions does a student answer in Paper 2?', 'One, chosen from four', ['Two, chosen from four', 'All four', 'One, chosen from two'], 'Students write one comparative essay.'),
         ('How many marks is Paper 2 worth?', '30', ['20', '40', '25'], 'Criteria A 10, B 10, C 5, D 5.'),
         ('What weighting does Paper 2 carry at HL?', '25%', ['35%', '20%', '30%'], 'Paper 2 is 35% at SL and 25% at HL.')],
  why=[('Explain why the key terms of a Paper 2 question must be defined in the essay.', 'General questions use broad terms ("power", "resolution"); defining them in relation to the chosen works shows precise understanding and keeps the essay focused.'),
       ('Explain why "to what effect" matters in a Paper 2 question.', 'It requires students to go beyond identifying methods to evaluating their impact on meaning and audience (criterion B).'),
       ('Explain why Paper 2 questions are deliberately general.', 'They must be answerable with any combination of studied works, so students must adapt their knowledge to the question rather than reproduce prepared essays.')],
  contrast=[('"In what ways"', '"To what extent"', '"In what ways" asks for an analysis of methods; "to what extent" requires a judgement about degree, with arguments for and against.')],
  misc=[('Paper 2 questions refer to specific set texts.', 'Paper 2 questions are general; students apply them to any two literary works they have studied (but not those used in the IO or HL essay).'),
        ('You can answer Paper 2 using a non-literary body of work.', 'Paper 2 requires two literary works studied in the course.')],
  evaluate=[('Choosing the right question is the most important decision in Paper 2.', ['a well-matched question allows depth', 'mismatches force irrelevant answers'], ['knowledge of works matters most', 'good students can adapt to most questions'], 'Question choice is crucial, but it depends on secure knowledge of the works.')],
  extended=[('Choose a Paper 2-style question and explain in detail how you would interpret its key terms in relation to two works you have studied.', 'Indicative content: key terms defined; command phrase explained; how each work fits; potential comparisons.', 6, 'long')])
p2_gen('ch08-st1', ('C2', 'C3'), (1, 4), 'terms')
p2_gen('ch08-st1', 'C4', (3, 5), 'thesis')

H('ch08-st2',
  terms=[('pairing', 'the choice of two literary works to compare in Paper 2'),
         ('point of comparison', 'a shared aspect (theme, technique, context) that allows two works to be discussed together'),
         ('productive contrast', 'a difference between works that illuminates both, such as contrasting genres or perspectives')],
  facts=[('Which works may NOT be used in Paper 2?', 'Works used in the Individual Oral or HL essay', ['Works in translation', 'Works of poetry', 'Works studied in year 1'], 'Students may not reuse IO or HL essay works.'),
         ('A strong Paper 2 pairing typically offers:', 'Both a shared concern and a productive contrast in method or context', ['Two works with identical plots', 'Two works by the same author only', 'A literary and a non-literary text'], 'Similarity and difference drive comparison.')],
  why=[('Explain why contrasting forms (e.g. a play and a novel) can make a good pairing.', 'Different forms present similar concerns through different methods, giving rich material for comparing authorial choices.'),
       ('Explain why students should prepare more than one pairing.', 'Questions vary; flexible pairings let students choose the best fit rather than force a prepared pairing onto an unsuitable question.'),
       ('Explain why context can strengthen a pairing.', 'Works from different times or places reveal how context shapes the treatment of a shared concern.')],
  contrast=[('a similarity-based pairing', 'a contrast-based pairing', 'A similarity-based pairing chooses works with closely shared concerns; a contrast-based pairing chooses works that differ in form or context but meet on the question. Strong essays use both.')],
  misc=[('The best pairing uses the two works you like most.', 'The best pairing is the one that answers the question most fully with rich comparison, regardless of preference.')],
  apply=[('A Paper 2 question asks about the presentation of power. Explain how you would decide between pairing a tragedy with a dystopian novel or with a poetry collection.', 'Consider which pairing has clear examples of power in both, offers contrasting methods, and lets you analyse authorial choices in depth; justify a choice.', 4)],
  evaluate=[('Students should prepare fixed pairings before the exam.', ['saves time', 'allows deep preparation of comparisons'], ['questions may not suit prepared pairings', 'fixed pairings lead to pre-learned essays'], 'Prepare flexible pairings with several points of comparison rather than fixed essays.')],
  extended=[('For two works you have studied, list four possible Paper 2 question themes they could answer and explain one comparison for each.', 'Indicative content: plausible themes; specific comparison points; awareness of contrasts.', 6, 'long')])
p2_gen('ch08-st2', ('C3', 'C4'), (2, 5), 'works')
p2_gen('ch08-st2', 'C4', (3, 5), 'points')

H('ch08-st3',
  terms=[('key passage', 'a short, significant section of a work that can be used as evidence in several essays'),
         ('quotation bank', 'a set of short, memorable quotations organised by theme and technique for revision'),
         ('character map', 'a diagram showing relationships, development and functions of characters in a work'),
         ('theme map', 'a revision diagram connecting a work\'s themes to scenes, techniques and quotations')],
  facts=[('Paper 2 is a closed-book exam. This means students:', 'Cannot bring copies of the works into the exam', ['May bring annotated copies', 'May bring a one-page outline', 'May use the internet'], 'References must come from memory.'),
         ('The best quotations to memorise for Paper 2 are:', 'Short, flexible ones that can support several points', ['Whole pages of text', 'Only the first line of each work', 'Quotations from critics only'], 'Short quotations are easier to recall and analyse.')],
  why=[('Explain why short quotations are better for revision than long passages.', 'They are easier to remember, can be embedded in sentences and allow close analysis of specific words.'),
       ('Explain why revision should organise quotations by theme and technique.', 'Paper 2 questions are thematic or technique-based; organised notes allow quick retrieval for any question.'),
       ('Explain why paraphrase and precise reference to episodes are acceptable in Paper 2.', 'In a closed-book exam, accurate reference to specific moments shows knowledge even when exact words are not remembered.')],
  contrast=[('memorising quotations', 'understanding key passages', 'Memorising quotations provides exact evidence; understanding key passages provides context, structure and methods to discuss even without exact words.')],
  misc=[('You must quote exactly in Paper 2 to get good marks.', 'Accurate quotation helps, but precise reference to episodes and paraphrase are also credited; knowledge and analysis matter most.')],
  apply=[('Create a revision plan of five steps for preparing two works for Paper 2 in the final month.', 'For example: reread key passages; build quotation banks by theme; map characters and themes; practise timed plans for past-style questions; write and self-assess full essays.', 4),
         ('Select three short quotations (or precise references) from a work you have studied that could support essays on three different themes, and explain each choice.', 'Answers vary: credit short, accurate references each linked to a theme with a brief explanation of the technique.', 4)],
  evaluate=[('Memorising model essays is an effective way to prepare for Paper 2.', ['gives confidence', 'provides tested arguments'], ['questions are unpredictable', 'examiners reward responsiveness to the question'], 'Model essays help with structure but should not replace flexible understanding.')],
  extended=[('Produce a theme map for one literary work you have studied, connecting three themes to scenes, techniques and quotations.', 'Indicative content: accurate references; clear connections; technique labels.', 6, 'long')])
p2_gen('ch08-st3', 'C3', (2, 4), 'points')
p2_gen('ch08-st3', 'C2', (1, 3), 'terms')


# =============================================================================================
# ch09 Paper 2: writing the comparative essay
# =============================================================================================
H('ch09-st1',
  terms=[('comparative thesis', 'an arguable statement that answers the question and indicates a key similarity and difference between the two works'),
         ('criterion A (Paper 2)', 'Knowledge, understanding and interpretation (10 marks): knowledge of the works and interpretation of their implications in relation to the question'),
         ('nuance', 'qualification and subtlety in an argument, recognising complexity')],
  facts=[('Which is the strongest comparative thesis?', '"Both works expose the cost of conformity, but where Ibsen stages Nora\'s break as liberation, Fitzgerald frames Gatsby\'s dream as doomed nostalgia."', ['"Both works are about society."', '"A Doll\'s House is a play and The Great Gatsby is a novel."', '"I will compare two works in this essay."'], 'It answers the question with similarity and difference.'),
         ('How many marks is criterion A worth in Paper 2?', '10', ['5', '20', '15'], 'A and B are worth 10 each; C and D 5 each.')],
  why=[('Explain why a comparative thesis should include both similarity and difference.', 'Comparison means both; a thesis stating only similarity produces two parallel essays, while difference creates an argument about how each work handles the question.'),
       ('Explain why the thesis should use the language of the question.', 'Echoing key terms shows that the essay addresses the question directly and keeps the argument focused.')],
  contrast=[('a comparative thesis', 'a statement of intent', 'A comparative thesis makes an arguable claim about both works; a statement of intent merely announces what the essay will do ("I will compare...").')],
  misc=[('A thesis should be neutral so that the examiner does not disagree.', 'A thesis must be arguable; examiners reward a clear, supported position, not neutrality.')],
  evaluate=[('A complex thesis is always better than a simple one.', ['complexity shows insight', 'nuance earns higher bands'], ['complex theses can be unclear', 'clarity guides the essay'], 'The best thesis is clear first and nuanced second.')],
  extended=[('Write three different comparative theses for one Paper 2-style question, then evaluate which is strongest and why.', 'Indicative content: three arguable theses; evaluation by clarity, nuance and fit to question.', 6, 'long')])
p2_gen('ch09-st1', ('C3', 'C4'), (2, 5), 'thesis')
p2_gen('ch09-st1', 'C2', (1, 3), 'terms')

H('ch09-st2',
  terms=[('criterion B (Paper 2)', 'Analysis and evaluation (10 marks): analysis and evaluation of how the choices of each author shape meaning, with comparison and contrast'),
         ('authorial choice', 'a deliberate decision about form, structure, language, character or narrative technique'),
         ('integrated comparison', 'discussing both works within the same paragraph around a shared point'),
         ('comparative connective', 'a phrase that links works, such as "whereas", "similarly", "by contrast", "in a parallel way"')],
  facts=[('Which phrase best signals integrated comparison?', '"whereas"', ['"firstly"', '"in conclusion"', '"for example"'], '"Whereas" sets two works against each other.'),
         ('Criterion B in Paper 2 rewards:', 'Comparative analysis of how authorial choices shape meaning', ['Plot summary of both works', 'Biographical background', 'Quantity of quotations'], 'Analysis and evaluation of choices.')],
  why=[('Explain why comparing authorial choices is better than comparing plots.', 'Paper 2 assesses how meaning is created; comparing methods (e.g. narration versus stage directions) shows analysis rather than summary.'),
       ('Explain why form is a fruitful point of comparison in Paper 2.', 'Different forms make different choices possible, so comparing them reveals how each writer\'s method shapes meaning.')],
  contrast=[('integrated comparison', 'block comparison', 'Integrated comparison discusses both works within each paragraph; block comparison discusses one work in full and then the other. Integrated comparison usually scores higher for criteria B and C.')],
  misc=[('Comparing works means listing their similarities.', 'Comparison includes differences and evaluation of how each work\'s choices produce different effects.')],
  evaluate=[('It is impossible to compare authorial choices across different literary forms.', ['techniques differ (stage directions vs narration)', 'effects are medium-specific'], ['forms share functions (characterisation, perspective)', 'difference is itself comparable'], 'It is not only possible but productive: comparing how forms achieve similar functions is central to Paper 2.')],
  extended=[('Write two integrated comparative paragraphs comparing how two works you have studied present a central character\'s downfall.', 'Indicative content: integrated points; specific choices; comparative connectives; evaluation.', 10, 'long')])
p2_gen('ch09-st2', ('C3', 'C4'), (2, 5), 'para')
p2_gen('ch09-st2', 'C3', (2, 4), 'points')

H('ch09-st3',
  terms=[('criterion C (Paper 2)', 'Focus and organisation (5 marks): how well the essay maintains focus, is coherent and balances the two works'),
         ('balance', 'giving roughly equal, integrated attention to both works'),
         ('point-by-point structure', 'an essay organised by comparative points, each discussing both works')],
  facts=[('How many marks is criterion C worth in Paper 2?', '5', ['10', '20', '8'], 'C and D are worth 5 each.'),
         ('An essay that spends three-quarters of its length on one work will most likely lose marks in:', 'Criterion C (balance and organisation)', ['Criterion D only', 'No criterion', 'The IO'], 'Balance is part of focus and organisation.')],
  why=[('Explain why a point-by-point structure helps criterion C.', 'Organising each paragraph around a comparative point keeps both works in focus, ensures balance and builds the argument.'),
       ('Explain why the conclusion of a comparative essay should not introduce new works.', 'The conclusion should synthesise the comparison and answer the question; new material distracts from focus.')],
  contrast=[('a point-by-point structure', 'a text-by-text structure', 'A point-by-point structure discusses both works under each point; a text-by-text structure discusses one work then the other, often weakening comparison and balance.')],
  misc=[('Balance means writing exactly the same number of words about each work.', 'Balance means both works are discussed meaningfully and in relation to each other, not word-count equality.')],
  apply=[('Outline a five-paragraph point-by-point structure for a Paper 2 essay on how two works present isolation.', 'Introduction with thesis; three comparative points (e.g. setting, narrative voice, ending) each discussing both works; conclusion synthesising and evaluating.', 4)],
  evaluate=[('Point-by-point is always the best structure for a comparative essay.', ['ensures integration and balance', 'favoured by examiners'], ['can become formulaic', 'some arguments need a different shape'], 'It is usually the safest and most effective, but structure should serve the argument.')],
  extended=[('Rewrite the plan of a text-by-text comparative essay as a point-by-point plan, explaining the improvements.', 'Indicative content: original plan; new integrated plan; explanation for criteria B and C.', 6, 'long')])
p2_gen('ch09-st3', ('C3', 'C4'), (2, 5), 'points')

H('ch09-st4',
  terms=[('timed writing', 'writing a complete essay under exam time limits'),
         ('planning time', 'the minutes at the start of the exam spent choosing a question and outlining an answer'),
         ('criterion D (Paper 2)', 'Language (5 marks): clarity, variety and accuracy of language and appropriate register')],
  facts=[('In a 1 hour 45 minute Paper 2, a sensible planning time is about:', '15–20 minutes', ['1 hour', '2 minutes', '45 minutes'], 'Enough to choose a question and plan while leaving about 80 minutes to write.'),
         ('Which is the best use of the last five minutes of Paper 2?', 'Checking the conclusion answers the question and correcting errors', ['Starting a new essay', 'Rewriting the introduction completely', 'Adding a third work'], 'Final checks protect criteria C and D.')],
  why=[('Explain why practising timed essays matters for Paper 2.', 'Timed practice builds speed, planning habits and stamina, so students can produce a complete, balanced essay under pressure.'),
       ('Explain why a plan saves time in a timed essay.', 'Knowing the argument in advance prevents digressions and rewriting, and ensures balance and a conclusion.')],
  contrast=[('a planned essay', 'an unplanned essay', 'A planned essay follows a clear argument with balanced comparison; an unplanned essay often drifts, repeats and runs out of time before the conclusion.')],
  misc=[('Planning wastes valuable writing time in Paper 2.', 'A short plan improves focus, balance and organisation, usually making the writing faster and better.')],
  apply=[('Divide 105 minutes for Paper 2 into stages and justify the timing.', 'For example: 5 min reading questions and choosing; 12 min planning; 80 min writing (about 15–18 per section); 8 min checking. Justification of each stage.', 3),
         ('You have 20 minutes left and have only discussed one work in depth. What should you do?', 'Write a focused comparative section bringing in the second work on the strongest point, then a brief conclusion that answers the question; balance and conclusion matter more than finishing the original plan.', 3)],
  evaluate=[('Speed of writing is more important than quality of planning in Paper 2.', ['incomplete essays lose marks', 'more writing allows more analysis'], ['unfocused writing scores poorly', 'planning creates efficient writing'], 'Planning enables efficient, focused writing; both matter but planning comes first.')],
  extended=[('Write a full timed plan (in 15 minutes) for a Paper 2-style question, including thesis, three comparative points and evidence for each work.', 'Indicative content: arguable thesis; integrated points; specific evidence; realistic scope.', 6, 'long')])
p2_gen('ch09-st4', 'C4', (3, 5), 'para')
p2_gen('ch09-st4', ('C3', 'C4'), (2, 4), 'thesis')


# =============================================================================================
# ch10 HL essay: developing a line of inquiry
# =============================================================================================
H('ch10-st1',
  terms=[('HL essay', 'a 1,200–1,500-word formal essay on one literary work or non-literary body of work studied, developing a student-chosen line of inquiry; 20 marks, 20% of HL'),
         ('line of inquiry', 'the focused question or angle the HL essay investigates, linked to a course concept'),
         ('course concept', 'one of the seven concepts (identity, culture, creativity, communication, perspective, transformation, representation) that the line of inquiry may connect to')],
  facts=[('What is the required length of the HL essay?', '1,200–1,500 words', ['2,500–3,000 words', '800–1,000 words', '4,000 words'], 'The HL essay is 1,200–1,500 words.'),
         ('The HL essay is worth what percentage of the HL grade?', '20%', ['25%', '35%', '30%'], 'HL essay 20%.'),
         ('The HL essay may be written on:', 'One literary work or one non-literary text or body of work studied', ['Two works compared', 'Any book the student likes', 'Only works in translation'], 'It focuses on a single work or body of work.')],
  why=[('Explain why a line of inquiry should be narrow.', 'In 1,200–1,500 words, a narrow focus allows detailed analysis of authorial choices; a broad question leads to summary.'),
       ('Explain why linking the line of inquiry to a course concept helps.', 'The concept gives a conceptual lens and shows the essay engages with the course\'s key ideas.'),
       ('Explain why the HL essay must not use works from the IO or Paper 2.', 'Assessment rules require different works across components so each tests independent knowledge.')],
  contrast=[('a line of inquiry', 'a topic', 'A topic is a general area (the veil in Persepolis); a line of inquiry is a focused question about how authorial choices create meaning (how Satrapi\'s visual representation of the veil constructs Marji\'s identity).')],
  misc=[('The HL essay is a comparative essay.', 'The HL essay focuses on one work or body of work; comparison is the focus of Paper 2.')],
  evaluate=[('Students should choose an HL essay text they find difficult.', ['difficulty can lead to original insight', 'challenge shows ambition'], ['students write best about texts they understand well', 'difficulty can produce confusion'], 'Choose a text that genuinely interests the student and offers rich material, whatever its difficulty.')],
  extended=[('Propose a line of inquiry for an HL essay on a work you have studied, explain its link to a course concept and outline three sections.', 'Indicative content: focused question; concept; three analytical sections; feasibility.', 6, 'long')])
loi_gen('ch10-st1', ('C2', 'C3'), (1, 4), 'eval')
loi_gen('ch10-st1', 'C4', (3, 5), 'thesis')

H('ch10-st2',
  terms=[('learner portfolio', 'the student\'s collection of responses to texts that provides ideas, evidence and reflection for the HL essay'),
         ('exploratory writing', 'informal writing used to test ideas before committing to a line of inquiry'),
         ('reflection', 'considering how one\'s ideas and interpretations have developed')],
  facts=[('How can the learner portfolio best support the HL essay?', 'By recording observations, quotations and questions that can become a line of inquiry', ['By replacing the essay', 'By providing a ready-made essay', 'It cannot be used'], 'The portfolio develops ideas.'),
         ('Which portfolio entry is most useful for developing a line of inquiry?', 'A note questioning why a recurring image changes across a work', ['A plot summary of chapter one', 'A list of characters\' names', 'A copy of the blurb'], 'Questions drive inquiry.')],
  why=[('Explain why testing ideas in the learner portfolio improves the HL essay.', 'Exploratory entries reveal which ideas have enough evidence and depth before the student commits to a line of inquiry.'),
       ('Explain why a portfolio entry that asks a question is more useful than one that summarises.', 'Questions lead to investigation and argument; summaries only record content.')],
  contrast=[('a portfolio entry', 'an HL essay draft', 'A portfolio entry is informal, exploratory and unassessed; an HL essay draft is a formal, structured argument aimed at the criteria.')],
  misc=[('Ideas from the learner portfolio cannot be used in assessed work.', 'The portfolio is designed to feed assessed work; students develop its ideas (in their own words) for the HL essay.')],
  apply=[('Turn this portfolio note into a possible line of inquiry: "Weird how the green light keeps coming back in Gatsby."', 'Example: "How does Fitzgerald use the recurring image of the green light to trace the development and failure of Gatsby\'s dream?"', 3),
         ('Turn this portfolio note into a possible line of inquiry: "The cartoons always show politicians as tiny compared to disasters."', 'Example: "How do the cartoonists use scale and visual metaphor to represent political inaction on climate change?"', 3),
         ('Turn this portfolio note into a possible line of inquiry: "Nora lies a lot in Act 1."', 'Example: "How does Ibsen use Nora\'s small deceptions in Act 1 to reveal the performance demanded of her within marriage?"', 3)],
  evaluate=[('The learner portfolio is more valuable for the HL essay than for any other assessment.', ['the essay needs independent lines of inquiry', 'it is the only coursework essay'], ['the IO depends on portfolio connections', 'Paper 2 revision uses it'], 'It is particularly valuable for the HL essay but supports all components.')],
  extended=[('Write a reflective learner portfolio entry (about 300 words) tracing how your idea for an HL essay developed over several weeks.', 'Indicative content: initial idea; evidence explored; refinements; final line of inquiry; reflection.', 8, 'long')])
loi_gen('ch10-st2', ('C3', 'C4'), (2, 5), 'thesis')
loi_gen('ch10-st2', 'C2', (1, 3), 'eval')

H('ch10-st3',
  terms=[('secondary source', 'critical or contextual material about a text written by someone other than its author'),
         ('academic integrity', 'honesty in academic work: acknowledging all sources and submitting one\'s own work'),
         ('plagiarism', 'presenting someone else\'s words or ideas as one\'s own without acknowledgement'),
         ('collusion', 'supporting malpractice by another student, such as letting one\'s work be copied'),
         ('critical reading', 'evaluating a source\'s argument, evidence and reliability rather than simply accepting it')],
  facts=[('Are secondary sources required in the HL essay?', 'No – they are optional, but any used must be acknowledged', ['Yes – at least five are required', 'Yes – only peer-reviewed sources', 'They are forbidden'], 'Secondary sources are not required.'),
         ('Using an AI tool to write sections of the HL essay without acknowledgement is:', 'A breach of academic integrity', ['Acceptable if edited', 'Encouraged by the IB', 'Only an issue at SL'], 'Work must be the student\'s own and all sources acknowledged.')],
  why=[('Explain why secondary sources should support rather than replace the student\'s argument.', 'The HL essay assesses the student\'s own analysis; sources are useful to test or extend ideas but cannot substitute for personal interpretation.'),
       ('Explain why critical reading of secondary sources matters.', 'Critics disagree and may be outdated or biased; evaluating their arguments allows the student to engage with them rather than repeat them.'),
       ('Explain why acknowledging ideas, not only quotations, is necessary.', 'Paraphrased ideas are still someone else\'s work; failing to cite them is plagiarism.')],
  contrast=[('plagiarism', 'collusion', 'Plagiarism is presenting another person\'s work as one\'s own; collusion is helping another student commit malpractice, for example by allowing work to be copied.')],
  misc=[('If you change a few words, you do not need to cite a source.', 'Paraphrased ideas still require citation; changing words does not make an idea your own.')],
  evaluate=[('Using secondary sources makes an HL essay stronger.', ['they deepen context and show research', 'engaging with critics shows sophistication'], ['they may crowd out personal analysis', 'they are not required by the criteria'], 'Used critically and sparingly, sources can strengthen an essay; they are not essential.')],
  extended=[('Explain how you would use one secondary source critically in an HL essay, including how you would cite it.', 'Indicative content: source purpose; agreement/disagreement; integration; citation format.', 6, 'long')])
loi_gen('ch10-st3', 'C3', (2, 4), 'intro')
loi_gen('ch10-st3', 'C4', (3, 5), 'intro')


# =============================================================================================
# ch11 HL essay: drafting, referencing and final submission
# =============================================================================================
H('ch11-st1',
  terms=[('introduction', 'the opening section that presents the work, the line of inquiry and the thesis'),
         ('body section', 'a section that develops one stage of the argument with analysis of evidence'),
         ('conclusion', 'the final section that synthesises the argument and evaluates its significance'),
         ('HL essay criteria', 'A Knowledge, understanding and interpretation; B Analysis and evaluation; C Focus, organisation and development; D Language – 5 marks each, 20 total')],
  facts=[('How many marks is the HL essay worth?', '20', ['30', '40', '25'], 'Four criteria × 5 marks.'),
         ('What happens if an HL essay exceeds 1,500 words?', 'The examiner stops reading at 1,500 words', ['Nothing', 'It is awarded zero', 'It gains extra marks'], 'Material beyond the limit is not assessed.')],
  why=[('Explain why the HL essay thesis should appear early.', 'Stating the thesis in the introduction gives the reader the line of argument from the start and lets each section be judged against it (criterion C).'),
       ('Explain why each section of an HL essay needs a topic sentence linked to the line of inquiry.', 'Linking topic sentences show how each section answers the inquiry, maintaining focus and showing development.'),
       ('Explain why the HL essay should analyse rather than summarise.', 'The examiner knows the work; criterion B rewards analysis of authorial choices, while summary uses words without earning marks.'),
       ('Explain why counter-arguments or alternative readings can strengthen an HL essay.', 'Addressing other interpretations shows nuance and critical thinking, strengthening the thesis by testing it.'),
       ('Explain why each body section of the HL essay should advance the argument.', 'Criterion C rewards development; sections that build on each other show a coherent, progressing argument.'),
       ('Explain why the introduction should be concise.', 'With only 1,200–1,500 words, a short introduction leaves space for analysis, which carries most marks.')],
  contrast=[('a thesis', 'a line of inquiry', 'A line of inquiry is the question the essay investigates; the thesis is the essay\'s arguable answer to it.'),
            ('an argument-led structure', 'a chronological structure', 'An argument-led structure organises sections by stages of the thesis; a chronological structure follows the text\'s order, often leading to summary.')],
  misc=[('The HL essay needs a long introduction with the author\'s biography.', 'Biography is only relevant if it illuminates the line of inquiry; a concise introduction leaves room for analysis.'),
        ('An HL essay conclusion should just repeat the thesis.', 'A conclusion should synthesise how the sections answer the inquiry and evaluate the significance of the findings.'),
        ('The HL essay should cover as many aspects of the work as possible.', 'It should develop one focused line of inquiry in depth; breadth leads to superficial analysis.')],
  apply=[('Allocate 1,400 words across the sections of an HL essay and justify the allocation.', 'For example: introduction about 150; three body sections about 350 each; conclusion about 150; justification based on analysis weight.', 3)],
  evaluate=[('A strong conclusion can significantly raise an HL essay\'s mark.', ['it shows synthesis and evaluation', 'it leaves a final impression'], ['marks depend mainly on analysis in the body', 'a conclusion cannot rescue weak analysis'], 'A strong conclusion helps criteria C and B but cannot compensate for weak body sections.')],
  extended=[('Write a detailed plan for a 1,200–1,500-word HL essay, including thesis, section topics, evidence and word allocation.', 'Indicative content: focused thesis; argument-led sections; specific evidence; realistic word allocation.', 6, 'long')])
loi_gen('ch11-st1', ('C3', 'C4'), (2, 5), 'intro')
loi_gen('ch11-st1', 'C3', (2, 4), 'thesis')

H('ch11-st2',
  terms=[('MLA style', 'a referencing system (Modern Language Association) commonly used in literary studies, with in-text citations and a works-cited list'),
         ('in-text citation', 'a brief reference in the text, e.g. (Achebe 208), pointing to the full entry in the works cited'),
         ('works cited', 'the alphabetical list of sources at the end of an essay in MLA style'),
         ('embedded quotation', 'a quotation integrated grammatically into the student\'s sentence')],
  facts=[('Which is a correctly formatted MLA in-text citation for a quotation from page 208 of a novel by Achebe?', '(Achebe 208)', ['(Achebe, p. 208)', '[208 Achebe]', '(Things Fall Apart, 1958, 208)'], 'MLA uses author and page with no comma.'),
         ('In MLA style, the list of sources at the end of an essay is called:', 'Works Cited', ['Bibliography of Sources', 'References Used', 'Endnotes List'], 'MLA uses "Works Cited".')],
  why=[('Explain why embedded quotations are preferable to long block quotations in the HL essay.', 'They save words, allow close analysis of key words and keep the student\'s argument in control.'),
       ('Explain why consistent referencing matters.', 'It shows academic integrity and allows the reader to locate evidence; inconsistency suggests carelessness.')],
  contrast=[('an in-text citation', 'a works-cited entry', 'An in-text citation is a short reference within the essay (author and page); a works-cited entry gives full publication details at the end.')],
  misc=[('Quotations from the primary text do not need to be cited.', 'All quotations, including from the primary text, should be referenced so that the reader can locate them.')],
  apply=[('Rewrite this sentence with an embedded quotation and MLA citation: The narrator says that the women sat on one side. (page 54, author Roy)', 'Example: The narrator observes that the women "sat on one side" (Roy 54), a spatial division that mirrors the novel\'s social boundaries. (Credit any accurate embedding and citation format.)', 2),
         ('Format a works-cited entry in MLA style for: Chinua Achebe, Things Fall Apart, Penguin Classics, 2006.', 'Achebe, Chinua. Things Fall Apart. Penguin Classics, 2006. (Title in italics when typed.)', 2)],
  evaluate=[('Referencing style matters less than the quality of the analysis.', ['criteria reward analysis mostly', 'minor formatting errors rarely change bands'], ['referencing is part of academic integrity', 'poor referencing undermines credibility'], 'Analysis carries most marks, but correct referencing is essential for integrity and clarity.')],
  extended=[('Write a paragraph for an HL essay that integrates three embedded quotations with correct MLA citations and analyses each.', 'Indicative content: fluent embedding; accurate citations; analysis of each quotation.', 6, 'long')])
loi_gen('ch11-st2', 'C3', (2, 4), 'thesis')
loi_gen('ch11-st2', 'C4', (3, 5), 'intro')

H('ch11-st3',
  terms=[('draft', 'a complete version of the essay submitted for teacher feedback before the final version'),
         ('feedback', 'the teacher\'s general comments on the draft, given once under IB rules'),
         ('redrafting', 'revising the essay in response to feedback and self-assessment'),
         ('final submission', 'the authenticated final version sent for external assessment')],
  facts=[('How many times may a teacher give written feedback on a draft of the HL essay?', 'Once', ['Three times', 'Unlimited', 'Never'], 'Teachers may comment on one draft.'),
         ('Teacher feedback on the HL essay draft may:', 'Give general comments but not edit or correct the text', ['Rewrite weak paragraphs', 'Correct every error', 'Award a final mark'], 'Feedback must be general.')],
  why=[('Explain why self-assessment against criteria A–D is useful before redrafting.', 'It helps the student identify specific weaknesses (focus, analysis, language) and plan targeted revisions.'),
       ('Explain why redrafting should focus on the argument rather than only on surface errors.', 'Most marks depend on interpretation, analysis and organisation; fixing these has more impact than correcting typos.')],
  contrast=[('revising', 'proofreading', 'Revising changes content and structure to improve the argument; proofreading corrects surface errors in spelling, grammar and punctuation.')],
  misc=[('The teacher can correct the HL essay draft line by line.', 'IB rules allow only general feedback on one draft; teachers must not edit the work.')],
  apply=[('Teacher feedback says: "Your analysis is strong but your sections do not connect clearly to your line of inquiry." Which criterion is affected and what two revisions would you make?', 'Criterion C; add topic sentences that link each section to the line of inquiry and transitions showing how each section develops the argument; revise the conclusion to synthesise.', 3),
         ('A draft scores well on criterion D but often summarises the plot. Which criterion should the student target and how?', 'Criterion B (and A); replace summary with analysis of authorial choices and their effects, using short embedded quotations.', 3)],
  evaluate=[('The first draft of an HL essay matters more than the final draft.', ['feedback depends on a complete draft', 'early structure shapes the essay'], ['only the final version is assessed', 'major revisions are possible'], 'The first draft is crucial for useful feedback, but the final draft is what is assessed.')],
  extended=[('Write a redrafting plan for an HL essay draft, identifying three targets linked to specific criteria and the changes you would make.', 'Indicative content: targets linked to A–D; specific revisions; prioritisation.', 6, 'long')])
loi_gen('ch11-st3', 'C3', (2, 4), 'eval')
loi_gen('ch11-st3', 'C4', (3, 5), 'thesis')


# =============================================================================================
# ch12 Paper 1 consolidation: unseen non-literary texts
# =============================================================================================
UNF = {'blog', 'review', 'oped', 'brochure', 'satire', 'campaign', 'appeal', 'manifesto', 'parody', 'cartoon', 'infographic', 'website', 'social', 'ad', 'letter', 'speech'}
H('ch12-st1',
  terms=[('review', 'a text that evaluates a product, performance or work, usually with a rating and recommendation'),
         ('opinion column', 'a by-lined article presenting the writer\'s personal argument on a topical issue'),
         ('brochure', 'a promotional leaflet describing a place, organisation or service'),
         ('blog', 'an online journal or series of posts with a personal voice and interactive features')],
  facts=[('Which convention is most typical of a review?', 'An evaluative rating and recommendation', ['An inverted pyramid of facts', 'A numbered list of demands', 'A salutation and sign-off'], 'Reviews evaluate.'),
         ('A text that opens "To scroll or not to scroll: that is the question" and argues a personal view in a newspaper is most likely:', 'An opinion column', ['A news report', 'A brochure', 'A manifesto'], 'It is a by-lined argument with a hook.')],
  why=[('Explain why Paper 1 students should know the conventions of many text types.', 'Unseen texts can be any type; knowing conventions lets students recognise how the writer uses or subverts them quickly.'),
       ('Explain why unfamiliar text types should still be analysed through audience, purpose and context.', 'These questions apply to all texts, so they provide a reliable approach even when the type is new.'),
       ('Explain why reviews can be persuasive even though they appear to be evaluative.', 'Reviewers persuade readers to accept their judgement through voice, wit and selection of evidence.')],
  contrast=[('a review', 'an advertisement', 'A review evaluates a product or work independently (ideally) for readers; an advertisement promotes it on behalf of the producer.')],
  misc=[('Paper 1 only uses common text types such as adverts and speeches.', 'Paper 1 may use any non-literary text type, including reviews, brochures, blogs, infographics and cartoons.')],
  evaluate=[('Knowing text-type conventions is the most important preparation for Paper 1.', ['it speeds up recognition', 'conventions frame analysis'], ['close reading of language matters more', 'unseen texts often mix types'], 'Conventions are a useful starting point; close analysis of choices earns the marks.')],
  extended=[('Write a review (about 300 words) of a film adaptation of a novel you know, using the conventions of the review form.', 'Indicative content: rating; summary; evaluation of adaptation choices; recommendation; voice.', 10, 'long')])
pq_kind_mcq('ch12-st1', UNF)
pq('ch12-st1', ('C2', 'C3', 'C4'), (1, 5), UNF, ('aud', 'purp'), ['Identify the audience and purpose of this unseen text and support your answer.',
                                                               'How does the writer adapt this text to its audience and purpose?',
                                                               'Evaluate how effectively the text achieves its purpose for its audience.'], crit=CRIT_A)
pq('ch12-st1', ('C2', 'C3'), (1, 5), UNF, 'dev', DEV_Q)

H('ch12-st2',
  terms=[('HL Paper 1', 'two guided textual analyses of unseen non-literary passages in 2 hours 15 minutes, 40 marks (35%)'),
         ('time allocation', 'dividing exam time evenly between texts and stages'),
         ('stamina', 'the ability to sustain quality across two analyses')],
  facts=[('How long do HL students have for Paper 1?', '2 hours 15 minutes', ['1 hour 15 minutes', '1 hour 45 minutes', '3 hours'], 'HL Paper 1 is 2 h 15 for two texts.'),
         ('Roughly how much time should an HL student spend on each Paper 1 text?', 'About 65–70 minutes', ['About 30 minutes', 'About 2 hours', 'About 10 minutes'], 'Half of 135 minutes.')],
  why=[('Explain why HL students should write on the text they find harder first, or at least not run out of time on it.', 'Harder texts need more thinking time; leaving them until fatigue sets in risks a weaker second response.'),
       ('Explain why the two Paper 1 analyses should be treated as separate essays.', 'Each is marked out of 20 on its own criteria; comparing the texts is not required and wastes time.')],
  contrast=[('SL Paper 1', 'HL Paper 1', 'SL students choose one of two texts and write one analysis in 1 h 15; HL students write on both texts in 2 h 15. Both carry 35%.')],
  misc=[('In HL Paper 1, students must compare the two texts.', 'HL students write two separate analyses; no comparison is required.')],
  apply=[('Propose a minute-by-minute plan for HL Paper 1.', 'For example: 67 minutes per text – 15 reading/annotating/planning, 47 writing, 5 checking; brief pause between texts. Justification.', 3)],
  evaluate=[('It is better to write two solid analyses than one brilliant and one weak.', ['each is worth 20 marks', 'a very weak second response loses many marks'], ['an excellent response may earn more marks overall if the other is adequate', 'strengths vary'], 'Balance is usually safer: consistent quality across both maximises the total.')],
  extended=[('Reflect on a timed HL Paper 1 practice: how did you divide your time, and how would you change your approach?', 'Indicative content: specific timings; effects on quality; concrete changes.', 6, 'long')])
pq_para('ch12-st2', UNF, c=('C3', 'C4'), d=(3, 5), frames=[
    'Guiding question: {gq}\nYou have about 65 minutes for this text in HL Paper 1. Write your plan (thesis and paragraph outline) in the first 15 minutes.',
    'Guiding question: {gq}\nWrite the thesis and two body paragraphs of a timed guided analysis of this text.'])
pq('ch12-st2', 'C3', (2, 4), UNF, 'struct', STRUCT_Q)

H('ch12-st3',
  terms=[('moderation', 'checking that marks awarded match the agreed standard'),
         ('markband descriptor', 'a statement describing the qualities of work at a given level for a criterion'),
         ('benchmark', 'an agreed example of work at a particular mark, used for comparison')],
  facts=[('A Paper 1 response that is insightful and well supported but loosely organised is most likely to score:', 'High on A and B, lower on C', ['Low on every criterion', 'Full marks on C', 'Zero overall'], 'Criteria are independent.'),
         ('Which description fits the top band of Paper 1 criterion B?', 'Insightful and convincing analysis of textual features and authorial choices, with very good evaluation', ['Some analysis, mostly descriptive', 'Little analysis; mainly summary', 'Accurate spelling throughout'], 'Top band B descriptor.')],
  why=[('Explain why moderating your own response against markbands improves performance.', 'It reveals precisely which descriptors you meet and what the next band requires, turning feedback into targets.'),
       ('Explain why comparing your work with benchmark responses is useful.', 'Benchmarks make abstract descriptors concrete and show the difference between bands in practice.')],
  contrast=[('a holistic judgement', 'a criterion-based judgement', 'A holistic judgement gives an overall impression; a criterion-based judgement assesses each criterion separately, as IB markbands require.')],
  misc=[('A long Paper 1 response will always score higher.', 'Marks depend on the quality described in the bands; a concise, focused analysis can outscore a long, descriptive one.')],
  apply=[('A response identifies many devices but explains few effects, is well organised and clearly written. Estimate a mark for each criterion and justify.', 'For example: A 3, B 2, C 4, D 4 (13/20) – organised and clear but feature-spotting limits analysis.', 4),
         ('A response offers a perceptive interpretation and detailed analysis but has frequent language errors that sometimes obscure meaning. Estimate marks for B and D.', 'For example: B 4, D 2 – strong analysis, but language errors affecting clarity limit D.', 3)],
  evaluate=[('Students are able to moderate their own work as accurately as teachers.', ['clear descriptors help', 'practice improves accuracy'], ['students tend to over- or under-mark', 'expertise in standards takes time'], 'With practice and benchmarks students get closer, but teacher moderation remains more reliable.')],
  extended=[('Mark a sample paragraph of your own against all four Paper 1 criteria and write targets for each.', 'Indicative content: criterion-by-criterion marks; justification by descriptors; targets.', 6, 'long')])
pq('ch12-st3', ('C3', 'C4'), (2, 5), UNF, 'gqa', ['Guiding question: {gq}\nList what a top-band response for criteria A and B would include for this text.',
                                                 'Guiding question: {gq}\nA student writes: "The text uses many techniques to persuade the audience." Moderate this thesis against criterion C and rewrite it for the top band.'], crit=P1_BANDS)


# =============================================================================================
# ch13 Final revision: synthesising the three areas of exploration
# =============================================================================================
H('ch13-st1',
  terms=[('areas of exploration', 'the three organising areas of the course: Readers, writers and texts; Time and space; Intertextuality: connecting texts'),
         ('Theory of Knowledge (TOK) link', 'a connection between course content and questions about knowledge, such as how language shapes what we know'),
         ('knowledge question', 'an open, contestable question about knowledge, e.g. "To what extent does language determine what we can know?"')],
  facts=[('Which is a knowledge question suitable for a TOK link in English?', '"To what extent can a translation give us knowledge of a work written in another language?"', ['"Who wrote Macbeth?"', '"How many lines are in a sonnet?"', '"When was Persepolis published?"'], 'Knowledge questions are open and about knowledge.'),
         ('The three areas of exploration are:', 'Readers, writers and texts; Time and space; Intertextuality: connecting texts', ['Poetry; Prose; Drama', 'Paper 1; Paper 2; IO', 'Identity; Culture; Creativity'], 'They organise the course.')],
  why=[('Explain why connecting works across areas of exploration helps in Paper 2.', 'Seeing works through several areas (reader response, context, intertextuality) provides varied angles for comparison and richer interpretation.'),
       ('Explain how the study of language and literature raises TOK questions.', 'It shows that language shapes perception and knowledge, that interpretation varies with perspective and that texts construct rather than mirror reality.'),
       ('Explain why course concepts are useful for synthesis in final revision.', 'Concepts cut across works and areas, providing a framework to connect texts studied at different times.')],
  contrast=[('an area of exploration', 'a course concept', 'An area of exploration is a broad organising frame for study (e.g. Time and space); a course concept is a lens (e.g. representation) applied within and across areas.')],
  misc=[('Each work belongs to only one area of exploration.', 'Works are often studied in one area but can be explored through all three; synthesis connects them.')],
  evaluate=[('Language shapes what we can know.', ['vocabulary and framing influence perception', 'translation shows meaning is language-bound'], ['experience and perception exist beyond language', 'translation and paraphrase are possible'], 'Language strongly shapes knowledge but does not wholly determine it – a central TOK debate.')],
  extended=[('Write a revision synthesis connecting three works you have studied to one course concept and one TOK knowledge question.', 'Indicative content: specific works; concept applied; knowledge question explored; connections.', 8, 'long')])
pq('ch13-st1', ('C3', 'C4'), (2, 5), None, 'concept', ['Explain how this text could be connected to works from other areas of exploration through the concept of {cname}.',
                                                     'Suggest a TOK knowledge question raised by this text and explain the link.',
                                                     'Discuss how this text could be used to synthesise ideas across the course, using the concept of {cname}.'], crit=CRIT_OPEN)
pq('ch13-st1', 'C2', (1, 4), None, 'read', ['Explain how this text shows that meaning depends on the reader – a TOK link on language and knowledge.'], crit=CRIT_OPEN)

H('ch13-st2',
  terms=[('mock examination', 'a full practice exam taken under timed conditions'),
         ('exam conditions', 'silence, time limits and no notes or texts, as in the real exam'),
         ('closed-book', 'an exam in which texts may not be brought in (Paper 2)')],
  facts=[('In a full HL mock, the Paper 1 and Paper 2 times combined are:', '4 hours (2 h 15 + 1 h 45)', ['3 hours', '2 hours 30 minutes', '5 hours'], 'HL P1 2 h 15 plus P2 1 h 45.'),
         ('In SL, Paper 1 and Paper 2 together carry:', '70% (35% + 35%)', ['60%', '50%', '80%'], 'SL P1 35% and P2 35%; IO 30%.')],
  why=[('Explain why students should practise choosing a Paper 2 question quickly.', 'Spending too long choosing reduces planning and writing time; practice with past-style questions builds confident, fast decisions.'),
       ('Explain why answering both Paper 1 texts under timed conditions matters for HL students.', 'Fatigue and timing affect the second analysis; only full practice shows whether quality can be sustained.'),
       ('Explain why a mock should be followed by reflection rather than simply a mark.', 'Reflection turns the mark into specific, criterion-linked targets that guide the remaining revision.'),
       ('Explain why full mock exams are valuable even if students have practised individual skills.', 'They test stamina, timing and the integration of all skills under pressure, revealing weaknesses not visible in short tasks.'),
       ('Explain why students should review mocks against each criterion.', 'Criterion-by-criterion review shows where marks were lost and directs revision efficiently.')],
  contrast=[('Paper 1', 'Paper 2', 'Paper 1 is a guided analysis of unseen non-literary texts (SL one, HL two); Paper 2 is a closed-book comparative essay on two literary works studied, answering one of four general questions.'),
            ('practice under exam conditions', 'untimed practice', 'Exam-condition practice tests timing and recall; untimed practice develops depth and technique but can hide time-management problems.')],
  misc=[('Mock exams should be taken with notes so they feel less stressful.', 'Mocks are most useful under real conditions (closed-book Paper 2, timed Paper 1), so they test genuine readiness.'),
        ('A high mock result means no more revision is needed.', 'Results vary with texts and questions; continued practice keeps skills sharp and addresses remaining weaknesses.'),
        ('A poor mock result predicts a poor final grade.', 'Mocks are diagnostic; targeted revision after a mock often produces large improvements.')],
  apply=[('After a mock, a student scored P1: A 4, B 2, C 3, D 4 and P2: A 6, B 4, C 3, D 4. Identify the priority for revision and suggest two strategies.', 'Analysis and evaluation (criterion B) in both papers; strategies: practise explaining effects of fewer features in depth; write comparative paragraphs analysing authorial choices with evaluation.', 4)],
  evaluate=[('Doing many full mock exams is the best way to prepare in the final weeks.', ['builds stamina and timing', 'familiarity reduces anxiety'], ['without feedback, repetition reinforces errors', 'targeted skill practice may be more efficient'], 'A few mocks with careful review are better than many without reflection.')],
  extended=[('Write a reflection on a full mock (Paper 1 and Paper 2), identifying strengths and three targets with strategies.', 'Indicative content: specific evidence; criteria; actionable strategies.', 6, 'long')])
pq_para('ch13-st2', UNF, c='C4', d=(4, 5), frames=['Paper 1 practice under exam conditions. Guiding question: {gq}\nWrite a full guided textual analysis of the text.',
                                                   'Timed practice (about 65 minutes). Guiding question: {gq}\nWrite a complete guided analysis.'], crit=P1_BANDS)
p2_gen('ch13-st2', 'C4', (4, 5), 'para')
p2_gen('ch13-st2', 'C3', (2, 4), 'thesis')

H('ch13-st3',
  terms=[('error log', 'a record of recurring mistakes and the strategies to fix them'),
         ('weak criterion', 'the assessment criterion on which a student consistently scores lowest'),
         ('targeted revision', 'revision focused on specific weaknesses rather than general rereading')],
  facts=[('Which is the most effective revision response to repeated low marks on Paper 1 criterion C?', 'Practising thesis statements, paragraph plans and transitions', ['Memorising more device names', 'Rereading set texts', 'Writing longer answers'], 'C is focus and organisation.'),
         ('A student\'s essays are often marked down for informal phrasing. The weak criterion is:', 'Criterion D', ['Criterion A', 'Criterion B', 'Criterion C'], 'D assesses language.')],
  why=[('Explain why keeping an error log helps exam preparation.', 'It reveals patterns in mistakes, so students can target recurring problems instead of repeating them.'),
       ('Explain why targeted revision is more efficient than rereading.', 'It addresses specific skills linked to marks, while rereading often feels productive but changes little.')],
  contrast=[('active revision', 'passive revision', 'Active revision involves practice and retrieval (timed plans, self-testing); passive revision involves rereading and highlighting, which is less effective.')],
  misc=[('If you keep making the same mistake, you just need to try harder.', 'Recurring mistakes need a specific strategy – such as a checklist or model – not just more effort.')],
  apply=[('A student\'s Paper 2 essays often discuss one work much more than the other. Suggest two targeted strategies.', 'Plan each paragraph with both works; use comparative connectives in topic sentences; check balance at the planning stage.', 3),
         ('A student\'s Paper 1 analyses often begin with a long summary. Suggest two targeted strategies.', 'Start with a one-sentence context and thesis; practise analytical topic sentences; limit description to what supports analysis.', 3),
         ('A student loses marks on criterion A in the IO because she rarely refers to the whole works. Suggest two strategies.', 'Prepare two or three brief, specific references to other parts of each work; plan a "connection to the whole" section in the outline.', 3)],
  evaluate=[('Focusing on weaknesses is more important than developing strengths in the final weeks.', ['weak criteria offer the biggest gains', 'balance across criteria is needed'], ['strengths can be pushed into top bands', 'confidence matters'], 'Mostly target weaknesses, while maintaining strengths through practice.')],
  extended=[('Write an error log for your Paper 1 or Paper 2 practice, identifying three recurring problems, their criteria and strategies.', 'Indicative content: specific problems; criteria; concrete strategies and check-ins.', 6, 'long')])
pq('ch13-st3', 'C3', (2, 4), UNF, 'dev', ['A student wrote only the label "{device}" beside "{quote}". Rewrite the comment so that it would score well on criterion B.',
                                         'Improve this weak annotation: "\'{quote}\' – {device}." Add effect and link to purpose.'])
pq('ch13-st3', 'C4', (3, 5), UNF, 'gqa', ['Guiding question: {gq}\nA student\'s plan lists one device per paragraph. Revise it into an argument-led plan that would score higher on criterion C.'], crit=P1_BANDS)
