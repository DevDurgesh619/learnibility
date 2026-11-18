"""CBSE class 11 Psychology: curated 'distinguish between' pairs and original case vignettes (case-based section).

extra(chapters) returns {subtopic id: [families]} for g12_hum_engine.families(..., extra).
Each vignette is (text, concept, explanation, kind label); vignettes are original and short.
The two generator helpers follow g12_psychology_c.py (copied, not imported, so the tables stay separate).
"""
import qbank
import g12_hum_engine as E

PAIRS = {
    '01-st1': [('mental processes', 'behaviour'), ('experience', 'behaviour')],
    '01-st2': [('structuralism', 'functionalism'), ('behaviourism', 'Gestalt psychology'), ('psychoanalysis', 'humanistic perspective')],
    '01-st4': [('clinical psychology', 'educational psychology'), ('health psychology', 'environmental psychology'),
               ('social psychology', 'cross-cultural psychology')],
    '02-st1': [('prediction', 'explanation'), ('description', 'control')],
    '02-st2': [('physiological data', 'psychological information'), ('demographic information', 'physical information')],
    '02-st3': [('reliability', 'validity'), ('experimental method', 'correlational research'), ('naturalistic observation', 'participant observation'),
               ('survey research', 'case study method')],
    '02-st4': [('informed consent', 'debriefing'), ('quantitative method', 'qualitative method')],
    '03-st1': [('development', 'growth'), ('plasticity', 'maturation')],
    '03-st2': [('microsystem', 'macrosystem'), ('exosystem', 'chronosystem')],
    '03-st3': [('sensorimotor stage', 'preoperational stage'), ('conservation', 'object permanence')],
    '03-st4': [('puberty', 'adolescence'), ('identity', 'identity confusion')],
    '04-st1': [('stimulus', 'sensation'), ('kinesthetic system', 'vestibular system')],
    '04-st2': [('filter theory', 'filter-attenuation theory'), ('divided attention', 'sustained attention')],
    '04-st3': [('perception', 'sensation'), ('principle of proximity', 'principle of similarity'), ('principle of closure', 'principle of continuity')],
    '04-st4': [('retinal disparity', 'convergence'), ('size constancy', 'shape constancy'), ('illusion', 'phi phenomenon')],
    '05-st1': [('learning', 'performance')],
    '05-st2': [('extinction', 'spontaneous recovery'), ('delayed conditioning', 'backward conditioning'),
               ('conditioned response', 'unconditioned response')],
    '05-st3': [('primary reinforcer', 'secondary reinforcer'), ('positive reinforcement', 'punishment'), ('shaping', 'schedule of reinforcement')],
    '05-st4': [('observational learning', 'insight learning'), ('paired-associate learning', 'free recall'), ('latent learning', 'cognitive map')],
    '05-st5': [('learning disability', 'dyslexia'), ('preparedness for learning', 'learning style')],
    '06-st1': [('encoding', 'retrieval'), ('storage', 'retrieval')],
    '06-st2': [('sensory memory', 'short-term memory'), ('short-term memory', 'long-term memory'), ('iconic memory', 'echoic memory')],
    '06-st3': [('explicit memory', 'implicit memory'), ('semantic processing', 'structural processing')],
    '06-st4': [('trace decay', 'retrieval failure'), ('constructive memory', 'serial reproduction')],
    '06-st5': [('first-letter technique', 'PQRST method'), ('mnemonics', 'PQRST method')],
    '07-st1': [('natural concept', 'artificial concept'), ('mental image', 'concept')],
    '07-st2': [('mental set', 'functional fixedness'), ('problem solving', 'decision making')],
    '07-st3': [('fluency', 'flexibility'), ('originality', 'elaboration'), ('incubation', 'illumination')],
    '07-st4': [('syntax', 'semantics'), ('holophrase', 'telegraphic speech'), ('babbling', 'holophrase')],
    '08-st1': [('drive', 'incentive'), ('need for affiliation', 'need for power')],
    '08-st2': [('safety needs', 'esteem needs'), ('physiological needs', 'self-actualisation')],
    '08-st3': [('Cannon-Bard theory', 'Schachter-Singer two-factor theory'), ('display rules', 'paralanguage')],
    '08-st4': [('self-awareness', 'self-monitoring'), ('self-monitoring', 'self-modification')],
}

VIG = {
    '01-st1': [
        ("Before a speech, Kiran's palms sweat and her heart beats fast, though she looks calm and smiles at the audience.",
         'covert behaviour', "covert behaviours are internal responses, such as a racing heart, that others cannot directly observe", 'kind of behaviour'),
        ("Two friends watch the same film; one finds it frightening and the other finds it funny.",
         'experience', "experience is subjective awareness, known directly only to the experiencer and shaped by internal and external conditions", 'aspect studied by psychology'),
        ("A patient who learns to stay calm and positive during treatment recovers faster than expected, and his immune markers improve.",
         'psychoneuroimmunology', "it studies how the mind, nervous system and immune system interact, showing the role of the mind in health", 'field of study'),
    ],
    '01-st2': [
        ("In a laboratory, trained observers look at a coloured light and report the separate sensations and feelings they experience.",
         'structuralism (introspection)', "structuralists used introspection to break conscious experience into its basic elements", 'school of psychology'),
        ("A researcher refuses to talk about 'feelings' and studies only how often a rat presses a lever when food is given.",
         'behaviourism', "behaviourists studied only observable and measurable behaviour, rejecting introspection", 'school of psychology'),
        ("A psychologist says a melody is heard as a tune, not as separate notes, because the whole is more than its parts.",
         'Gestalt psychology', "Gestalt psychologists held that perception is of organised wholes that are more than the sum of their parts", 'school of psychology'),
    ],
    '01-st3': [
        ("A student project traces how a university in Bengal set up India's first psychology laboratory in 1915 and its first department of psychology in 1916.",
         'Calcutta University', "modern psychology in India began at Calcutta University, with the first laboratory in 1915 and department in 1916", 'institution'),
        ("A historian notes that, long before modern laboratories, Indian thinkers wrote at length about consciousness, the self and mind-body relations.",
         'Indian philosophical tradition', "Indian philosophical traditions discussed consciousness, self and mental processes long before modern psychology", 'source of psychological ideas'),
        ("A pioneer of Indian psychology who worked in psychoanalysis set up an association for its study in 1922.",
         'Girindrasekhar Bose and the Indian Psychoanalytic Association', "Bose worked in psychoanalysis and founded the Indian Psychoanalytic Association in 1922", 'pioneer'),
    ],
    '01-st4': [
        ("A psychologist in a hospital interviews a patient with severe anxiety, makes a diagnosis and plans therapy.",
         'clinical psychology', "clinical psychology deals with the causes, diagnosis and treatment of psychological disorders", 'branch of psychology'),
        ("A psychologist studies why people in crowded, noisy flats feel more irritable and helps plan better housing.",
         'environmental psychology', "environmental psychology studies the interaction between people and their physical environment", 'branch of psychology'),
        ("A firm hires a psychologist to design selection tests and training programmes for new employees.",
         'industrial or organisational psychology', "it deals with workplace behaviour such as selection, training and motivation of workers", 'branch of psychology'),
    ],
    '02-st1': [
        ("A researcher states before her study: 'Students who sleep eight hours will score higher in a memory test than those who sleep four hours.'",
         'hypothesis', "a hypothesis is a tentative answer to a research question stating a relationship between variables", 'research concept'),
        ("A team designs a programme to reduce bullying in schools after finding its causes.",
         'control', "control is the goal of making a behaviour happen, reducing it or enhancing it", 'goal of psychological enquiry'),
        ("After her study fails to support the theory she began with, a researcher changes the theory and plans a new study.",
         'revising research conclusions', "the last step of research revises the theory in the light of findings, leading to new research", 'step in scientific research'),
    ],
    '02-st2': [
        ("A researcher records each participant's age, gender, education and birth order on the first page of the form.",
         'demographic information', "demographic information is personal data such as age, gender, education and occupation", 'type of data'),
        ("During a stressful task, electrodes record a volunteer's heart rate and EEG.",
         'physiological data', "physiological data are measures of biological functions such as heart rate, blood pressure and EEG", 'type of data'),
        ("The same answer 'I am fine' meant very different things when given at a party and at a funeral.",
         'relative, context-dependent nature of psychological data', "psychological data depend on the context, the people involved and the time", 'feature of psychological data'),
    ],
    '02-st3': [
        ("A psychologist joins a village youth club for six months to understand how its members make decisions, without telling them she is studying them at first.",
         'participant observation', "the observer becomes a member of the group being observed", 'method'),
        ("One group of students studies with music and another in silence, everything else kept the same, and their test scores are compared.",
         'experimental method', "the independent variable (music) is manipulated and its effect on the dependent variable (scores) is measured under control", 'method'),
        ("A researcher finds that the more hours students spend on their phones, the lower their marks, without changing anything herself.",
         'negative correlation', "correlational research studies relationships without manipulation; here one variable rises as the other falls", 'research finding'),
    ],
    '02-st4': [
        ("After a study, the researcher explains to participants the real aim of the task and makes sure none of them feels upset.",
         'debriefing', "debriefing tells participants the real purpose after the study and returns them to their normal state", 'ethical procedure'),
        ("Before an interview, participants are told what the study involves and sign a form agreeing to take part.",
         'informed consent', "participants agree to take part after understanding what the study involves", 'ethical principle'),
        ("A researcher analyses diaries of migrant workers for themes of loneliness and hope, without converting them into numbers.",
         'qualitative analysis', "qualitative methods analyse descriptions and meanings rather than numbers", 'method of analysis'),
    ],
    '03-st1': [
        ("Identical twins raised in different homes grow to different heights; the better-fed twin is taller.",
         'interaction of heredity and environment', "genes give the potential, but the environment influences how it is expressed in the phenotype", 'concept'),
        ("A 70-year-old woman learns to use a smartphone and starts an online class.",
         'plasticity (life-span perspective)', "development is plastic and lifelong; capacity for change remains throughout life", 'principle of development'),
        ("Babies all over the world sit before they stand and stand before they walk, at roughly similar ages.",
         'maturation', "maturation is orderly change dictated largely by the genetic blueprint", 'developmental process'),
    ],
    '03-st2': [
        ("Aarav's mother is under heavy stress at her office, and she has less time and patience for him at home.",
         'exosystem', "the exosystem includes settings, like a parent's workplace, that affect the child without the child taking part", 'level of the ecological system'),
        ("Riya's parents meet her teachers regularly and work together to help her with mathematics.",
         'mesosystem', "the mesosystem is the set of relations among the parts of the child's microsystem", 'level of the ecological system'),
        ("A child's development is affected by the divorce of her parents when she is eight.",
         'chronosystem', "the chronosystem includes life events and changes over time that affect development", 'level of the ecological system'),
    ],
    '03-st3': [
        ("A ten-month-old baby lifts a cloth to find the toy his mother hid under it.",
         'object permanence', "the infant understands that objects exist even when not seen, which develops in the sensorimotor stage", 'cognitive achievement'),
        ("A four-year-old covers her eyes and says, 'You can't see me now.'",
         'egocentrism', "the preoperational child cannot take another person's point of view", 'feature of thought'),
        ("A nine-year-old says that a ball of clay rolled into a sausage still has the same amount of clay because 'you can roll it back'.",
         'conservation (concrete operational stage)', "the child understands that quantity stays the same despite change in shape, using reversibility", 'cognitive achievement'),
    ],
    '03-st4': [
        ("A fifteen-year-old refuses to go to school with a small pimple because she is sure everyone will stare at it.",
         'imaginary audience', "the adolescent believes others are as concerned with his or her appearance and behaviour as he or she is", 'feature of adolescent thinking'),
        ("A teenager drives fast without a helmet, saying accidents happen only to other people.",
         'personal fable', "the adolescent believes his or her experiences are unique and that he or she is invulnerable", 'feature of adolescent thinking'),
        ("A seventeen-year-old keeps changing his mind about career, values and friends and says he does not know who he really is.",
         'identity confusion', "according to Erikson, failure to develop a clear sense of self in adolescence leads to identity confusion", 'concept'),
    ],
    '04-st1': [
        ("A dog responds to a whistle that no person in the room can hear.",
         'functional limitation of sense organs', "each sense organ responds only to a limited range of stimuli, outside which stimuli are not sensed", 'concept'),
        ("A gymnast knows the exact position of her legs during a flip without looking at them.",
         'kinesthetic system', "it gives information about the position and movement of body parts", 'sense'),
        ("On entering a room with a strong smell of paint, Rohan notices it at once but no longer smells it after twenty minutes.",
         'sensory adaptation', "sensitivity to a constant stimulus decreases over time", 'process'),
    ],
    '04-st2': [
        ("In a noisy party, Neha hears her own name mentioned in a conversation across the room.",
         'selective attention (filter-attenuation)', "unattended messages are weakened, not blocked, so important words such as one's name can still be noticed", 'attentional process'),
        ("A radar operator must watch the screen for hours to spot a rare signal.",
         'sustained attention (vigilance)', "sustained attention is the ability to maintain attention on a task for a long period", 'attentional process'),
        ("An experienced tailor stitches a shirt while chatting with a customer.",
         'divided attention', "two tasks can be done together when one has become automatic through practice", 'attentional process'),
    ],
    '04-st3': [
        ("A doctor reads a patient's untidy handwriting on a prescription because she expects certain medicine names.",
         'top-down processing', "recognition starts from the whole and expectations, which guide identification of the parts", 'perceptual process'),
        ("Seeing a row of dots arranged in pairs, a child says there are pairs rather than single dots.",
         'principle of proximity', "objects close together are perceived as belonging together", 'Gestalt principle'),
        ("A logo made of a broken outline of a panda is easily seen as a panda.",
         'principle of closure', "we tend to perceive incomplete figures as complete", 'Gestalt principle'),
    ],
    '04-st4': [
        ("In a painting, a road grows narrower towards the horizon and seems to go far into the distance.",
         'linear perspective (monocular cue)', "parallel lines appear to converge with distance, a monocular cue to depth", 'depth cue'),
        ("As a friend walks away down the corridor, Meena does not think he is getting smaller.",
         'size constancy', "the perceived size stays the same despite a smaller retinal image with distance", 'perceptual constancy'),
        ("Lights on a festival board flash one after another and seem to run around the board.",
         'phi phenomenon', "stationary lights flashed in quick succession produce an illusion of movement", 'illusion'),
    ],
    '04-st5': [
        ("Children from a city of rectangular buildings are found to be more taken in by the Muller-Lyer illusion than children from a village of round huts.",
         'carpentered-world hypothesis', "people raised among straight lines and right angles read angles as depth cues and are more susceptible to the illusion", 'explanation'),
        ("A man who has lived all his life in a dense forest sees distant buffaloes across an open plain and thinks they are insects.",
         'cultural and ecological influence on size constancy', "people who rarely see distant objects may not develop size constancy for far objects", 'socio-cultural influence'),
        ("People shown the same simple drawing in two communities interpret its depth differently, depending on how familiar they are with pictures.",
         'socio-cultural influence on picture perception', "perception of depth in pictures depends partly on experience and culture", 'socio-cultural influence'),
    ],
    '05-st1': [
        ("After running a race, Arjun walks slowly for an hour; the next day he is back to his normal pace.",
         'temporary change due to fatigue, not learning', "learning is a relatively permanent change produced by experience; fatigue changes are temporary", 'concept'),
        ("A student knows the answer well but, too nervous in the exam, writes nothing.",
         'difference between learning and performance', "learning is inferred from performance, which may not always show what was learnt", 'concept'),
        ("A child learns to tie shoelaces after many attempts and can do it for years after.",
         'learning as a relatively permanent change through experience', "learning involves experience and produces a relatively permanent change in behaviour", 'concept'),
    ],
    '05-st2': [
        ("A puppy runs to the kitchen whenever it hears the rattle of its food bowl.",
         'classical conditioning', "the rattle (CS) paired with food (US) comes to produce an anticipatory response (CR)", 'type of learning'),
        ("After being stung once, a boy now fears not only bees but also wasps and flies.",
         'stimulus generalisation', "responses spread to stimuli similar to the conditioned stimulus", 'process in conditioning'),
        ("A dog stops salivating to a bell that is never followed by food, but salivates again to the bell after a week's rest.",
         'spontaneous recovery', "an extinguished response reappears after a lapse of time", 'process in conditioning'),
    ],
    '05-st3': [
        ("Raju starts wearing his seatbelt as soon as he enters the car so that the annoying beep stops.",
         'negative reinforcement', "a response is strengthened because it removes an unpleasant stimulus", 'type of consequence'),
        ("A trainer teaches a dolphin to jump through a hoop by rewarding it first for swimming near the hoop, then for touching it, and finally for jumping through.",
         'shaping', "successive approximations to the desired response are reinforced", 'operant technique'),
        ("A man keeps buying lottery tickets for years although he wins only now and then, after an unpredictable number of tickets.",
         'variable ratio schedule', "reinforcement after a varying number of responses produces high, steady responding resistant to extinction", 'schedule of reinforcement'),
    ],
    '05-st4': [
        ("After watching her elder sister being praised for setting the table, a little girl starts setting it too.",
         'observational learning', "learning occurs by watching a model and the consequences of the model's behaviour", 'type of learning'),
        ("A chimpanzee sits quietly for a while, then suddenly joins two sticks to pull in a banana kept out of reach.",
         'insight learning', "the solution appears suddenly after the learner perceives the relationships in the problem", 'type of learning'),
        ("A boy who often travelled with his father finds his way to a new shop at once when asked, though he had never been asked to go there alone.",
         'latent learning (cognitive map)', "learning occurs without reinforcement and shows when an incentive appears", 'type of learning'),
    ],
    '05-st5': [
        ("A bright girl of eight reads very slowly, confuses 'b' and 'd' and skips lines, though she is very good at explaining stories told to her.",
         'learning disability (dyslexia)', "a learning disability is a difficulty in specific abilities such as reading, not due to low intelligence", 'condition'),
        ("Manav studies astronomy late into the night just because he finds the stars fascinating.",
         'intrinsic motivation', "learning for the interest and satisfaction in the activity itself", 'factor facilitating learning'),
        ("A rat learns to avoid a food that made it sick after just one pairing, but cannot easily learn to link the sickness with a light.",
         'preparedness for learning', "species are biologically better equipped to learn some associations than others", 'factor in learning'),
    ],
    '06-st1': [
        ("Asha cannot recall the name of the guest she was introduced to because she was busy on her phone at that moment.",
         'encoding failure', "information not attended to and registered is never encoded, so it cannot be stored or retrieved", 'memory process'),
        ("Ravi is sure he knows his old roll number but cannot bring it to mind during a conversation.",
         'retrieval', "retrieval is bringing stored information out for use; here it fails though the memory is stored", 'memory process'),
        ("A student reads her notes and links each idea to an example so that it gets a meaning in her mind.",
         'encoding', "encoding is recording information and giving it a meaning", 'memory process'),
    ],
    '06-st2': [
        ("Sanjay repeats a phone number aloud until he finishes dialling it, and forgets it a minute later.",
         'maintenance rehearsal in short-term memory', "repetition keeps information in short-term memory, which is lost quickly without it", 'memory process'),
        ("Kavya remembers a 10-digit number as 98-765-43-210 instead of ten separate digits.",
         'chunking', "grouping items into meaningful units increases the capacity of short-term memory", 'memory strategy'),
        ("While doing a sum in her head, Leela holds the carried-over numbers and adds the next digits at the same time.",
         'working memory', "working memory holds and manipulates information during a task, controlled by the central executive", 'memory system'),
    ],
    '06-st3': [
        ("Rahul remembers his tenth birthday party, who came and what gift he got.",
         'episodic memory', "episodic memory stores personal life experiences tied to time and place", 'type of long-term memory'),
        ("Asked about Earth's distance from the Sun, Sara gives the answer but cannot say when she learnt it.",
         'semantic memory', "semantic memory stores general knowledge not tied to the time and place of learning", 'type of long-term memory'),
        ("A student who thinks about the meaning of each new word remembers more of them than one who only notes how they are spelt.",
         'semantic level of processing', "processing for meaning is the deepest level and gives better retention (Craik and Lockhart)", 'concept'),
    ],
    '06-st4': [
        ("After moving to a new house, Neel keeps giving his old address when asked, and finds it hard to learn the new one.",
         'proactive interference', "earlier learning interferes with the recall of later learning", 'cause of forgetting'),
        ("A witness who expects robbers to look rough describes a neatly dressed thief as 'shabby'.",
         'constructive memory', "memory is reconstructed using schemas and expectations rather than copied", 'feature of memory'),
        ("Mira forgets her friend's surname but recalls it at once on seeing the friend's brother.",
         'retrieval failure (cue-dependent forgetting)', "the information is stored but needs a suitable retrieval cue to be accessed", 'cause of forgetting'),
    ],
    '06-st5': [
        ("To remember a shopping list, Tara imagines bread on her doormat, eggs on the sofa and milk in the bathroom.",
         'method of loci', "items are placed as images in familiar locations in a known order", 'mnemonic'),
        ("A student remembers the order of planets with a sentence whose words begin with the first letters of the planets.",
         'first-letter technique', "first letters of items are combined into a word or sentence as a cue", 'mnemonic'),
        ("Before reading a chapter, Anil skims it, writes questions, reads to answer them, recites the answers and then tests himself.",
         'PQRST method', "Preview, Question, Read, Self-recitation and Test improve study and retention", 'study method'),
    ],
    '07-st1': [
        ("Asked to think of a 'fruit', most children in a class think of an apple or a mango rather than a fig.",
         'prototype', "a prototype is the most typical example of a concept", 'element of thinking'),
        ("Before leaving home, Neha pictures the route to her friend's house in her mind and decides where to turn.",
         'mental image', "a mental image is a representation of a sensory experience used in thinking", 'building block of thought'),
        ("A child learns that cats, dogs and cows all belong to the group 'animals'.",
         'concept', "a concept is a mental representation of a category of things sharing common features", 'building block of thought'),
    ],
    '07-st2': [
        ("Needing to tighten a screw and having no screwdriver, Arun does not think of using the coin in his pocket.",
         'functional fixedness', "objects are seen only in terms of their usual function, which blocks problem solving", 'obstacle to problem solving'),
        ("After observing that every metal she heated expanded, a student concludes that all metals expand on heating.",
         'inductive reasoning', "a general conclusion is drawn from specific observations", 'type of reasoning'),
        ("Weighing fees, distance and courses, Divya chooses one of three colleges that have offered her admission.",
         'decision making', "decision making is choosing one option from several alternatives after evaluating them", 'thinking process'),
    ],
    '07-st3': [
        ("Asked for uses of a newspaper, Raghav lists wrapping, a paper boat, a fan, a hat, kindling and a drum cover.",
         'divergent thinking (fluency and flexibility)', "producing many and varied ideas shows divergent thinking abilities", 'type of thinking'),
        ("After weeks of failing to solve a design problem, an engineer leaves it aside; the answer suddenly comes to him while walking.",
         'incubation and illumination', "ideas develop while the problem is set aside, then the solution suddenly appears", 'stages of creative thinking'),
        ("In a team meeting, all ideas are written down without comment, and only later are they judged.",
         'brainstorming', "ideas are generated freely and judgement is postponed, encouraging creative ideas", 'creative strategy'),
    ],
    '07-st4': [
        ("A one-year-old points to the door and says 'out', meaning 'I want to go out'.",
         'holophrase', "a single word is used to express a whole thought", 'stage of language development'),
        ("A two-year-old says 'Mummy go office', leaving out the small words.",
         'telegraphic speech', "early speech uses two or three essential words, leaving out small words", 'stage of language development'),
        ("A three-year-old says 'I runned fast', using a grammar rule no adult taught her.",
         'innate language capacity (Chomsky)', "children apply rules creatively, which supports an innate language acquisition device", 'view of language development'),
    ],
    '08-st1': [
        ("After a long walk in the sun, Ramesh feels a strong urge to drink water and goes looking for a tap.",
         'motivational cycle (need, drive, goal)', "a need (water deficit) creates a drive that leads to behaviour until the goal is reached", 'concept'),
        ("Zara sets high standards for herself, prefers moderately difficult tasks and works hard to excel.",
         'need for achievement', "it is the need to meet standards of excellence", 'psychosocial motive'),
        ("A new student in a hostel spends his time making friends and joining group activities.",
         'need for affiliation', "it is the need to seek the company of others and establish relationships", 'psychosocial motive'),
    ],
    '08-st2': [
        ("After an earthquake, a family's first concern is food and water, and then a safe place to sleep.",
         'lower needs in the hierarchy of needs', "physiological and safety needs are basic and must be met before higher needs become important (Maslow)", 'concept'),
        ("A successful doctor leaves a well-paid post to serve in a remote village, saying he wants to become all he can be.",
         'self-actualisation', "it is the highest need in Maslow's hierarchy, to realise one's full potential", 'level of need'),
        ("Meera works hard for an award because she wants recognition and respect from her colleagues.",
         'esteem needs', "esteem needs include the need for respect, recognition and a positive self-image", 'level of need'),
    ],
    '08-st3': [
        ("Seeing a snake, Raju's heart pounds and he starts running; only then does he feel afraid.",
         'James-Lange theory', "it holds that perception of bodily changes following a stimulus produces the emotion", 'theory of emotion'),
        ("Two volunteers are given the same arousing drug; one sitting with a cheerful person feels happy, the other sitting with an angry person feels irritated.",
         'Schachter-Singer two-factor theory', "emotion depends on physiological arousal and the cognitive label given to it", 'theory of emotion'),
        ("At a family function, a girl hides her disappointment with a smile because showing it would be rude.",
         'display rules', "display rules are cultural norms about how and when emotions should be expressed", 'concept'),
    ],
    '08-st4': [
        ("Before replying to a rude message, Kabir notices that he is angry and asks himself why.",
         'self-awareness', "being aware of one's own emotions is the first step in managing them", 'technique for managing emotions'),
        ("After failing a test, Priya sees it as a chance to learn how to prepare better rather than as proof that she is weak.",
         'perceptual reinterpretation', "seeing a problem in a different light reduces negative emotion", 'technique for managing emotions'),
        ("Every weekend Rohit teaches children in a slum and says it makes him feel cheerful and useful.",
         'community service', "helping others enhances positive emotions and a sense of worth", 'way to enhance positive emotions'),
    ],
}


def distinguish(chapters):
    out = {}
    for subs, _ in chapters:
        terms = {t: m for sb in subs for t, m in sb.T}
        for sb in subs:
            pairs = PAIRS.get(sb.sid.split('-ch')[-1], [])
            if not pairs:
                continue
            for a, b in pairs:
                assert a in terms and b in terms, (sb.sid, a, b)
            d = E.deck([((a, terms[a]), (b, terms[b])) for a, b in pairs])

            def gen(r, d=d):
                (a, ma), (b, mb) = d(r)
                ans = f"{E.cap(a)}: {E.end(ma)} {E.cap(b)}: {E.end(mb)}"
                return {'stem': f"Distinguish between '{a}' and '{b}'.", 'answer': ans,
                        'key': f"2 marks: 1 mark for explaining '{a}' ({E.end(ma)}) and 1 mark for '{b}' ({E.end(mb)}), "
                               f"with the contrast between them made clear.", 'marks': 2, 'minutes': 3}
            out.setdefault(sb.sid, []).append(qbank.F('C2', 'D2', 'explain', gen, marks=2, minutes=3))
    return out


def vignettes(chapters):
    out = {}
    for subs, _ in chapters:
        for sb in subs:
            vs = VIG[sb.sid.split('-ch')[-1]]
            d = E.deck(vs)

            def one(r, d=d):
                text, concept, expl, kind = d(r)
                return {'stem': f"Read the case and answer. {text} Identify the {kind} illustrated.",
                        'answer': E.cap(concept) + '.',
                        'key': f"1 mark: {concept}.", 'marks': 1, 'minutes': 2}

            def two(r, d=d):
                text, concept, expl, kind = d(r)
                return {'stem': f"Read the case and answer. {text} Name the {kind} shown here and explain it briefly.",
                        'answer': f"{E.cap(concept)}: {E.end(expl)}",
                        'key': f"2 marks: 1 mark for naming it ({concept}); 1 mark for the explanation ({expl}).",
                        'marks': 2, 'minutes': 4}
            out.setdefault(sb.sid, []).extend([
                qbank.F('C3', 'D3', 'case', one, marks=1, minutes=2, kinds=('case1',), gap='G7'),
                qbank.F('C4', 'D3', 'case', two, marks=2, minutes=4, kinds=('case2',), gap='G7')])
    return out


def extra(chapters):
    out = distinguish(chapters)
    for sid, fs in vignettes(chapters).items():
        out.setdefault(sid, []).extend(fs)
    return out
