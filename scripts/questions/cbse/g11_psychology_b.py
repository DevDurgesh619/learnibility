"""CBSE class 11 Psychology (chapters 5-8): fact tables for g12_hum_engine (NCERT Introduction to Psychology)."""
from g12_hum_engine import ST

S = 'cbse-g11-psychology-ch'

CH05 = [ST(S + '05-st1', 'nature of learning and paradigms of learning', """
T: learning | any relatively permanent change in behaviour or behavioural potential produced by experience
T: performance | the observed behaviour of a person, from which learning is inferred
T: paradigm of learning | a distinct type or method of learning, such as classical conditioning, operant conditioning or observational learning
Q: Learning is best defined as a relatively permanent change in behaviour produced by: | experience | fatigue | drugs | maturation
Q: Which of these is NOT an example of learning? | Changes in behaviour due to fatigue | Learning to ride a bicycle | Learning a poem | Learning to fear a dog after a bite
Q: Learning is said to be an inferred process because it is judged from: | performance | heredity | reflexes | maturation
Q: Which of these is a paradigm of learning? | Operant conditioning | Maturation | Fatigue | Growth
M:paradigm: Classical conditioning | learning by association of two stimuli
M:paradigm: Operant conditioning | learning from the consequences of behaviour
M:paradigm: Observational learning | learning by watching a model
M:paradigm: Cognitive learning | learning through insight and understanding
M:paradigm: Skill learning | learning a smooth sequence of responses through practice
S+: Learning always involves some kind of experience
S+: Behavioural changes due to learning are relatively permanent
S+: Changes due to fatigue, habituation, drugs or maturation are not learning
S+: Learning is an inferred process and is different from performance
S+: Learning paradigms include classical and operant conditioning, observational, cognitive, verbal, concept and skill learning
S-: Changes in behaviour due to drugs are an example of learning | Such changes are temporary and are not learning
S-: Learning and performance are the same | Learning is inferred from performance, which may not always reflect what has been learnt
S-: Changes due to maturation are a kind of learning | Maturation is due to biological growth, not experience
C: Learning is called an inferred process | it cannot be observed directly and is judged from changes in performance
C: Changes in behaviour due to fatigue are not learning | they are temporary and not produced by experience
X: C2 D2 2 | Define learning. Why are changes due to fatigue not considered learning? | Relatively permanent change in behaviour due to experience; fatigue changes are temporary and not due to experience.
X: C2 D2 2 | Distinguish between learning and performance. | Learning – relatively permanent change in behavioural potential, inferred; performance – observed behaviour from which learning is inferred.
X: C3 D3 3 | Explain any three features of the learning process. | Always involves experience; relatively permanent changes; inferred process distinct from performance; excludes fatigue, drugs, maturation.
X: C3 D4 4 | Name and briefly explain any four paradigms of learning. | Classical conditioning; operant conditioning; observational learning; cognitive learning; verbal learning; concept learning; skill learning (any four).
L: D4 | Explain the nature of learning and describe the different paradigms of learning. | Definition; features – experience, permanence, inferred; not fatigue or maturation; paradigms – classical, operant, observational, cognitive, verbal, concept, skill learning.
"""), ST(S + '05-st2', 'classical conditioning', """
T: classical conditioning | learning in which a neutral stimulus comes to elicit a response after being paired with a stimulus that naturally produces it
T: unconditioned stimulus | a stimulus that naturally produces a response without any learning, such as food
T: unconditioned response | the natural, unlearnt response to an unconditioned stimulus, such as salivation to food
T: conditioned stimulus | an originally neutral stimulus that comes to produce a response after pairing, such as the sound of a bell
T: conditioned response | the learnt response to the conditioned stimulus
T: extinction | the disappearance of a learnt response when reinforcement is withdrawn
T: spontaneous recovery | the reappearance of an extinguished response after a lapse of time
T: stimulus generalisation | the tendency to respond to stimuli similar to the conditioned stimulus
T: stimulus discrimination | the learnt ability to respond to the conditioned stimulus but not to similar stimuli
T: delayed conditioning | the arrangement in which the conditioned stimulus begins before the unconditioned stimulus and lasts until it appears
T: backward conditioning | the arrangement in which the unconditioned stimulus is presented before the conditioned stimulus
Q: Classical conditioning was first studied by: | Ivan Pavlov | B.F. Skinner | Albert Bandura | Wolfgang Kohler
Q: In Pavlov's experiment, the sound of the bell after conditioning was the: | conditioned stimulus | unconditioned stimulus | unconditioned response | reinforcer
Q: In Pavlov's experiment, salivation to food was the: | unconditioned response | conditioned response | conditioned stimulus | neutral stimulus
Q: The most effective time arrangement in classical conditioning is: | delayed conditioning | backward conditioning | trace conditioning | simultaneous conditioning
Q: The least effective arrangement in classical conditioning is: | backward conditioning | delayed conditioning | simultaneous conditioning | trace conditioning
Q: A child conditioned to fear a white rat also fears a white rabbit. This is: | stimulus generalisation | discrimination | extinction | spontaneous recovery
Q: The reappearance of an extinguished conditioned response after some time is: | spontaneous recovery | generalisation | discrimination | shaping
M:conditioning: Unconditioned stimulus | food in Pavlov's experiment
M:conditioning: Unconditioned response | salivation to food
M:conditioning: Conditioned stimulus | sound of the bell
M:conditioning: Conditioned response | salivation to the bell
M:time relation: Simultaneous conditioning | CS and US presented together
M:time relation: Delayed conditioning | CS begins first and lasts until US appears
M:time relation: Trace conditioning | CS ends before the US begins
M:time relation: Backward conditioning | US presented before CS
S+: In classical conditioning, the conditioned stimulus comes to signal the occurrence of the unconditioned stimulus
S+: The time relation between the conditioned and unconditioned stimulus affects the speed of conditioning
S+: Aversive unconditioned stimuli, such as electric shock, usually produce faster conditioning than appetitive ones
S+: The more intense the conditioned stimulus, the fewer the trials needed for conditioning
S+: Many fears and phobias are acquired through classical conditioning
S-: In Pavlov's experiment, food was the conditioned stimulus | Food was the unconditioned stimulus; the bell was the conditioned stimulus
S-: Backward conditioning is the most effective arrangement | Delayed conditioning is the most effective; backward conditioning is the least effective
S-: Extinction means the learnt response is permanently erased | An extinguished response can reappear through spontaneous recovery
C: A child may become afraid of the doctor's clinic | the clinic has been paired with the pain of injections, which is an unconditioned stimulus
C: Delayed conditioning is the most effective arrangement | the conditioned stimulus reliably signals that the unconditioned stimulus is about to come
C: An extinguished response may reappear after a rest | extinction weakens the response without erasing the learnt association completely
X: C2 D2 2 | Distinguish between unconditioned and conditioned stimulus, with examples from Pavlov's experiment. | Unconditioned – naturally produces response, e.g. food; conditioned – originally neutral, produces response after pairing, e.g. bell.
X: C2 D2 2 | Distinguish between stimulus generalisation and discrimination. | Generalisation – responding to stimuli similar to the CS; discrimination – responding only to the CS and not to similar stimuli.
X: C3 D3 3 | Describe Pavlov's experiment on classical conditioning. | Dog in harness; food (US) produces salivation (UR); bell (CS) paired with food; after pairings bell alone produces salivation (CR).
X: C3 D3 3 | Explain the time relations between stimuli in classical conditioning. | Simultaneous; delayed – most effective; trace; backward – least effective; meaning of each.
X: C3 D4 4 | Explain the determinants of classical conditioning. | Time relations between stimuli; type of unconditioned stimulus – appetitive or aversive; intensity of conditioned stimulus; examples.
X: C4 D4 4 | Riya feels nervous whenever she smells the antiseptic of a hospital, where she once had a painful operation. Explain this using classical conditioning and suggest how the fear may be reduced. | US – pain; UR – fear; CS – smell; CR – nervousness; generalisation; extinction by repeated exposure to the smell without pain.
L: D4 | Describe classical conditioning with the help of Pavlov's experiment. Explain the key processes of extinction, spontaneous recovery, generalisation and discrimination. | US, UR, CS, CR; pairing; acquisition; extinction; spontaneous recovery; generalisation; discrimination; examples from daily life.
L: D5 | Discuss the determinants of classical conditioning and its applications in everyday life. | Time relations – simultaneous, delayed, trace, backward; type of US; intensity of CS; applications – fears, phobias, advertising, emotional reactions; extinction in therapy.
"""), ST(S + '05-st3', 'operant conditioning', """
T: operant conditioning | learning in which the probability of a voluntary behaviour is changed by its consequences
T: operant | a voluntary behaviour emitted by an organism that operates on the environment
T: reinforcement | any event that increases the probability of a response
T: positive reinforcement | strengthening a response by presenting a pleasant stimulus after it
T: negative reinforcement | strengthening a response by removing or avoiding an unpleasant stimulus after it
T: punishment | an aversive stimulus that decreases the probability of a response
T: primary reinforcer | a reinforcer that satisfies a biological need, such as food or water
T: secondary reinforcer | a reinforcer that acquires value by association with primary reinforcers, such as money or praise
T: shaping | reinforcing successive approximations to the desired response
T: schedule of reinforcement | the arrangement of when and how often reinforcement is given
T: partial reinforcement effect | the finding that responses learnt under partial reinforcement are more resistant to extinction
Q: Operant conditioning was first studied by: | B.F. Skinner | Ivan Pavlov | Albert Bandura | Edward Tolman
Q: Removing a headache by taking a pill, which makes pill-taking more likely, is an example of: | negative reinforcement | positive reinforcement | punishment | extinction
Q: Which reinforcer satisfies a biological need? | Food | Money | Praise | Grades
Q: Reinforcing successive approximations to a desired behaviour is called: | shaping | chaining | extinction | generalisation
Q: A salesperson paid for every tenth sale is on a: | fixed ratio schedule | fixed interval schedule | variable interval schedule | continuous schedule
Q: Gambling machines that pay out after an unpredictable number of plays use a: | variable ratio schedule | fixed ratio schedule | fixed interval schedule | continuous schedule
Q: Responses learnt under partial reinforcement are: | more resistant to extinction | extinguished faster | never learnt | the same as reflexes
Q: Money, praise and grades are examples of: | secondary reinforcers | primary reinforcers | punishments | unconditioned stimuli
M:schedule: Fixed ratio | reinforcement after a fixed number of responses
M:schedule: Variable ratio | reinforcement after a varying number of responses
M:schedule: Fixed interval | reinforcement for the first response after a fixed time
M:schedule: Variable interval | reinforcement after varying amounts of time
M:consequence: Positive reinforcement | praise given for finishing homework
M:consequence: Negative reinforcement | putting on a seatbelt to stop the warning beep
M:consequence: Punishment | a fine for parking in the wrong place
S+: Skinner used rats and pigeons in a box to study operant conditioning
S+: Both positive and negative reinforcement increase the probability of a response
S+: Punishment decreases the probability of a response
S+: Delayed reinforcement is less effective than immediate reinforcement
S+: Escape and avoidance learning are based on negative reinforcement
S+: Complex behaviours can be learnt through shaping and chaining
S-: Negative reinforcement is the same as punishment | Negative reinforcement increases a response by removing an unpleasant stimulus; punishment decreases a response
S-: Continuous reinforcement makes responses most resistant to extinction | Partial reinforcement makes responses more resistant to extinction
S-: Food is a secondary reinforcer | Food is a primary reinforcer; money and praise are secondary reinforcers
C: Negative reinforcement increases a response | removing an unpleasant stimulus after the response makes it more likely in future
C: Gamblers keep playing even after many losses | variable ratio reinforcement produces responses that are very resistant to extinction
C: Immediate praise works better than praise given weeks later | delayed reinforcement is less effective than immediate reinforcement
X: C2 D2 2 | Distinguish between positive and negative reinforcement. | Positive – presenting a pleasant stimulus to strengthen a response; negative – removing an unpleasant stimulus to strengthen a response.
X: C2 D2 2 | How is negative reinforcement different from punishment? | Negative reinforcement increases a response by removing an aversive stimulus; punishment decreases a response by an aversive consequence.
X: C2 D2 2 | Distinguish between primary and secondary reinforcers. | Primary – satisfy biological needs, e.g. food, water; secondary – acquire value through association, e.g. money, praise.
X: C3 D3 3 | Describe Skinner's experiment on operant conditioning. | Hungry rat in Skinner box; lever press delivers food pellet; accidental press reinforced; rate of pressing rises; operant learnt through consequences.
X: C3 D3 3 | Explain the four schedules of partial reinforcement with examples. | Fixed ratio; variable ratio; fixed interval; variable interval – meaning and example of each; partial reinforcement effect.
X: C3 D4 4 | Compare classical and operant conditioning. | Classical – involuntary responses, S-S association, Pavlov; operant – voluntary behaviour, consequences, Skinner; reinforcement role; examples; both show extinction and generalisation.
X: C4 D4 4 | A parent wants her son to keep his room tidy. Suggest how she can use operant conditioning principles. | Positive reinforcement with praise or token; shaping – reward small steps; immediate reinforcement; then partial schedule; avoid harsh punishment.
L: D4 | Explain operant conditioning. Describe the types of reinforcement and the schedules of reinforcement. | Skinner box; operant; positive, negative reinforcement; punishment; primary and secondary reinforcers; continuous and partial schedules – FR, VR, FI, VI; partial reinforcement effect; delayed reinforcement; shaping and chaining.
L: D5 | Compare classical and operant conditioning, and discuss the applications of operant conditioning in education and daily life. | Differences in nature of response, association, role of learner; applications – classroom praise, token economy, shaping skills, habit formation; limits of punishment.
"""), ST(S + '05-st4', 'observational, cognitive, verbal, concept and skill learning', """
T: observational learning | learning by observing the behaviour of others and its consequences, also called social learning or modelling
T: insight learning | learning in which a solution appears suddenly after the learner perceives the relationships in a problem
T: latent learning | learning that occurs but is not shown in behaviour until there is an incentive to show it
T: cognitive map | a mental representation of the layout of an environment
T: verbal learning | learning of words and verbal material, studied with methods such as paired-associate, serial and free recall learning
T: paired-associate learning | a method of verbal learning in which a person learns pairs of words so that the first word recalls the second
T: serial learning | a method of verbal learning in which a list of items must be learnt in the order of presentation
T: free recall | a method of verbal learning in which items can be recalled in any order
T: concept learning | learning a mental category of objects or events that share common features
T: skill | the ability to perform a complex task smoothly and efficiently
T: transfer of learning | the effect of earlier learning on later learning, which may be positive, negative or zero
Q: The study in which children imitated aggression towards a doll after watching a film was conducted by: | Albert Bandura | B.F. Skinner | Wolfgang Kohler | Ivan Pavlov
Q: Kohler's experiments with chimpanzees demonstrated: | insight learning | latent learning | classical conditioning | serial learning
Q: Tolman's experiments with rats in a maze demonstrated: | latent learning | insight learning | operant conditioning | observational learning
Q: The use of nonsense syllables to study verbal learning was started by: | Hermann Ebbinghaus | Edward Tolman | Albert Bandura | Jean Piaget
Q: In which method of verbal learning can items be recalled in any order? | Free recall | Serial learning | Paired-associate learning | Recognition
Q: The three phases of skill learning are cognitive, associative and: | autonomous | concrete | latent | operant
Q: When learning to drive a car makes it easier to learn to drive a truck, it shows: | positive transfer | negative transfer | zero transfer | extinction
M:learning: Observational learning | Bandura's study of children copying aggression
M:learning: Insight learning | Kohler's chimpanzees reaching bananas with sticks
M:learning: Latent learning | Tolman's rats forming a cognitive map of a maze
M:learning: Verbal learning | Ebbinghaus's nonsense syllables
M:verbal method: Paired-associate learning | learning pairs of words
M:verbal method: Serial learning | recalling items in the order presented
M:verbal method: Free recall | recalling items in any order
S+: In Bandura's study, children who saw the model rewarded for aggression showed the most aggression
S+: In insight learning the solution comes suddenly and can be applied to similar problems
S+: Latent learning shows that learning can occur without reinforcement
S+: Skill learning passes through cognitive, associative and autonomous phases
S+: In the autonomous phase of skill learning, the skill becomes automatic and needs little attention
S+: Concepts may be artificial, with clearly defined features, or natural, with fuzzy boundaries
S-: Tolman's experiments demonstrated insight learning | Tolman's experiments demonstrated latent learning; Kohler's demonstrated insight learning
S-: In free recall, items must be recalled in the order presented | That is serial learning; in free recall items can be recalled in any order
S-: Observational learning requires direct reinforcement of the learner | It occurs by watching a model and the consequences of the model's behaviour
C: Children copy the behaviour of characters they see on television | people learn by observing models and the consequences of their behaviour
C: Tolman's rats ran the maze quickly once food was introduced | they had already formed a cognitive map of the maze through latent learning
C: An expert typist can talk while typing | in the autonomous phase a skill becomes automatic and needs little attention
X: C2 D2 2 | What is observational learning? Give an example. | Learning by watching a model and the consequences of the model's behaviour; e.g. a child imitating a parent's style of greeting.
X: C2 D2 2 | Distinguish between insight learning and latent learning. | Insight – sudden solution after perceiving relations (Kohler); latent – learning without reinforcement, shown later when an incentive appears (Tolman).
X: C2 D2 2 | Distinguish between serial learning and free recall. | Serial – items recalled in the order presented; free recall – items recalled in any order.
X: C3 D3 3 | Describe Bandura's experiment on observational learning. | Children saw a film of a model hitting a doll; three groups – model rewarded, punished, no consequence; children who saw reward most aggressive; learning by observation.
X: C3 D3 3 | Explain the three phases of skill learning. | Cognitive – understand instructions, many errors; associative – errors decrease, practice; autonomous – automatic, little attention needed (Fitts).
X: C3 D4 4 | Describe Kohler's study of insight learning in chimpanzees. | Chimpanzee in cage with bananas out of reach and sticks; after failed attempts, sudden solution joining sticks; insight – perceiving relations; transfer to similar problems.
X: C4 D4 4 | 'Not all learning is shown immediately in behaviour.' Explain with reference to latent learning. | Tolman's rats; group without reward explored maze; when food introduced, ran as fast as rewarded rats; cognitive map; learning versus performance.
L: D4 | Describe observational learning and cognitive learning (insight and latent learning) with experiments. | Bandura – modelling, consequences to model; Kohler – insight, sudden solution, transfer; Tolman – latent learning, cognitive map; learning versus performance.
L: D5 | Explain verbal learning, concept learning and skill learning, and discuss the transfer of learning. | Ebbinghaus nonsense syllables; paired-associate, serial, free recall; concepts – artificial and natural; skills – cognitive, associative, autonomous phases; positive, negative and zero transfer.
"""), ST(S + '05-st5', 'factors facilitating learning and learning disabilities', """
T: intrinsic motivation | the motivation to learn because the activity is interesting or satisfying in itself
T: extrinsic motivation | the motivation to learn in order to gain an external reward or avoid punishment
T: preparedness for learning | the idea that members of a species are biologically better equipped to learn some associations than others
T: learning disability | a general term for a heterogeneous group of disorders shown as difficulties in acquiring and using listening, speaking, reading, writing, reasoning or mathematical abilities
T: dyslexia | a learning disability marked by difficulty in reading
T: learning style | a learner's consistent way of responding to and using stimuli in learning
Q: Learning because the subject itself interests you shows: | intrinsic motivation | extrinsic motivation | negative reinforcement | punishment
Q: Studying only to get a prize shows: | extrinsic motivation | intrinsic motivation | preparedness | insight
Q: A learning disability marked by difficulty in reading is: | dyslexia | dyscalculia | dysgraphia | ADHD
Q: The idea that species are biologically better equipped to learn some associations is called: | preparedness for learning | learning style | transfer of learning | extinction
Q: Learning disabilities are usually first noticed: | when the child begins school learning | only in old age | only at birth | only after adolescence
M:motivation: Intrinsic motivation | learning for its own interest
M:motivation: Extrinsic motivation | learning for a reward
S+: Responses learnt under partial reinforcement last longer than those learnt under continuous reinforcement
S+: Motivation, whether intrinsic or extrinsic, facilitates learning
S+: Children with learning disabilities may have difficulty in writing letters and words, reading and following instructions
S+: Children with learning disabilities may show poor spatial orientation and motor coordination
S+: Learning disabilities can be remedied through suitable intervention and teaching methods
S+: Learning disabilities are not the result of intellectual disability or sensory impairment alone
S-: Children with learning disabilities always have low intelligence | Many children with learning disabilities have normal intelligence
S-: Learning disabilities cannot be helped by any intervention | Suitable remedial teaching and intervention can help
S-: Extrinsic motivation is learning for the joy of the activity | That is intrinsic motivation; extrinsic is learning for external rewards
C: A child with a learning disability may do poorly in school despite normal intelligence | learning disabilities affect specific abilities such as reading and writing
C: Partial reinforcement facilitates lasting learning | responses learnt under partial reinforcement are more resistant to extinction
C: Different students prefer different ways of studying | each learner has a learning style for responding to and using stimuli
X: C2 D2 2 | Distinguish between intrinsic and extrinsic motivation in learning. | Intrinsic – learning for interest and satisfaction in the activity; extrinsic – learning for external reward or to avoid punishment.
X: C2 D2 2 | What is a learning disability? | Heterogeneous group of disorders – difficulty in listening, speaking, reading, writing, reasoning or mathematics; not due to low intelligence alone.
X: C3 D3 3 | Explain any three factors that facilitate learning. | Continuous versus partial reinforcement; motivation – intrinsic, extrinsic; preparedness for learning; learning styles (any three).
X: C3 D4 4 | Describe any four symptoms of learning disabilities. | Difficulty in writing letters and words; reading – dyslexia; poor spatial orientation; attention problems; poor motor coordination; difficulty following instructions; poor memory for sequences (any four).
X: C4 D4 4 | A bright Class 3 student keeps reversing letters and reads very slowly. What may be the problem, and how can teachers help? | Possible learning disability – dyslexia; not low intelligence; early identification; remedial teaching, multi-sensory methods, patience, reinforcement of progress.
L: D4 | Explain the factors that facilitate learning and describe the symptoms of learning disabilities. | Reinforcement schedules; motivation; preparedness; learning styles; learning disabilities – meaning, symptoms, normal intelligence, remedial help.
"""), ]

CH06 = [ST(S + '06-st1', 'nature of memory: encoding, storage and retrieval', """
T: memory | the process of retaining and retrieving information over a period of time
T: encoding | the first stage of memory, in which information is recorded and registered and given a meaning
T: storage | the stage of memory in which encoded information is retained over a period of time
T: retrieval | the stage of memory in which stored information is brought out for use
Q: The process in which information is registered and given meaning is called: | encoding | storage | retrieval | forgetting
Q: Bringing stored information back to awareness for use is: | retrieval | encoding | storage | rehearsal
Q: The three stages of memory are encoding, storage and: | retrieval | perception | attention | forgetting
Q: Memory failure can occur at: | any of the three stages | only the encoding stage | only the storage stage | only the retrieval stage
M:stage: Encoding | registering information and giving it meaning
M:stage: Storage | retaining information over time
M:stage: Retrieval | bringing information out for use
S+: Memory involves retaining information over a period of time and retrieving it when needed
S+: Information has to be encoded before it can be stored
S+: Failure in any one of the three stages leads to memory failure
S+: Retrieval depends on how well the information was encoded and stored
S-: Retrieval is the first stage of memory | Encoding is the first stage; retrieval is the last
S-: Memory failure can happen only at the retrieval stage | It can happen at the encoding, storage or retrieval stage
C: We may fail to remember a name we never paid attention to | information that is not encoded cannot be stored or retrieved
C: Memory is called a process | it involves the stages of encoding, storage and retrieval
X: C2 D2 2 | Name and explain the three stages of memory. | Encoding – registering and giving meaning; storage – retaining over time; retrieval – bringing out for use.
X: C3 D3 3 | Explain why memory failure can occur at any of the three stages, with examples. | Encoding failure – not attended; storage failure – information decays; retrieval failure – stored but cannot be accessed, e.g. tip of tongue.
X: C3 D4 4 | Explain the nature of memory with reference to encoding, storage and retrieval. | Definition; encoding – registering and meaning; storage – retention; retrieval – use; interdependence; failure at any stage.
L: D4 | Explain the nature of memory and the processes of encoding, storage and retrieval. | Definition; three stages with examples; dependence of each on the earlier; memory failure at each stage; implications for study.
"""), ST(S + '06-st2', 'information processing model of memory', """
T: stage model of memory | Atkinson and Shiffrin's 1968 model of memory with three separate systems: sensory, short-term and long-term memory
T: sensory memory | the memory system with a large capacity that holds sensory information for a very brief period, less than a second
T: iconic memory | the visual sensory memory
T: echoic memory | the auditory sensory memory
T: short-term memory | the memory system that holds a small amount of information, about seven items, for a brief period unless rehearsed
T: long-term memory | the permanent store of memory, with unlimited capacity, holding information from a few minutes to a lifetime
T: maintenance rehearsal | silently repeating information to keep it in short-term memory
T: elaborative rehearsal | relating new information to existing information in memory, which helps transfer to long-term memory
T: chunking | grouping items into meaningful units to increase the capacity of short-term memory
T: working memory | Baddeley's model of short-term memory as a system that holds and manipulates information, with a phonological loop, a visuo-spatial sketchpad and a central executive
Q: The stage model of memory was proposed by: | Atkinson and Shiffrin | Craik and Lockhart | Baddeley | Bartlett
Q: The capacity of short-term memory is about: | 7 plus or minus 2 items | 20 plus or minus 2 items | unlimited | 2 items
Q: Information in short-term memory is mainly encoded: | acoustically | semantically only | visually only | by touch
Q: Visual sensory memory is called: | iconic memory | echoic memory | episodic memory | procedural memory
Q: The component of working memory that controls attention and coordinates the other parts is the: | central executive | phonological loop | visuo-spatial sketchpad | sensory register
Q: Grouping the digits 1, 9, 4, 7 as the year 1947 is an example of: | chunking | maintenance rehearsal | decay | interference
Q: The model of working memory was proposed by: | Alan Baddeley | Endel Tulving | Atkinson and Shiffrin | Hermann Ebbinghaus
Q: The memory system with unlimited capacity is: | long-term memory | short-term memory | sensory memory | iconic memory
M:memory system: Sensory memory | large capacity, lasts less than a second
M:memory system: Short-term memory | about seven items, lost quickly without rehearsal
M:memory system: Long-term memory | unlimited capacity, relatively permanent
M:working memory: Phonological loop | holds sounds and words for a short time
M:working memory: Visuo-spatial sketchpad | holds visual and spatial information
M:working memory: Central executive | coordinates the other components and controls attention
S+: In the stage model, information passes from sensory memory to short-term memory and then to long-term memory
S+: Attention transfers information from sensory memory to short-term memory
S+: Information in short-term memory is lost quickly unless it is rehearsed
S+: Information in long-term memory is mainly encoded semantically, in terms of meaning
S+: Elaborative rehearsal helps transfer information to long-term memory
S+: Working memory not only stores information but also manipulates it
S-: Sensory memory has a very small capacity | Sensory memory has a large capacity but very short duration
S-: Short-term memory has unlimited capacity | Short-term memory holds about seven items; long-term memory is unlimited
S-: Maintenance rehearsal is the best way to transfer information to long-term memory | Elaborative rehearsal, which relates new information to old, is better
C: A telephone number is forgotten soon after dialling | information in short-term memory fades quickly unless it is rehearsed
C: Chunking improves short-term memory | grouping items into meaningful units allows more information to be held within its limited capacity
C: Working memory was proposed as an alternative to short-term memory | short-term memory was found to be not a single store but a system that also processes information
X: C2 D2 2 | Distinguish between maintenance rehearsal and elaborative rehearsal. | Maintenance – repeating information to keep it in STM; elaborative – relating it to existing knowledge, helps transfer to LTM.
X: C2 D2 2 | What is chunking? Give an example. | Grouping items into meaningful units to increase STM capacity, e.g. 1-9-4-7 remembered as 1947.
X: C3 D3 3 | Compare sensory memory, short-term memory and long-term memory. | Sensory – large capacity, less than a second; STM – about 7 items, brief, acoustic; LTM – unlimited, permanent, semantic.
X: C3 D3 3 | Explain the three components of working memory. | Baddeley; phonological loop – sounds and words; visuo-spatial sketchpad – visual and spatial information; central executive – controls and coordinates.
X: C3 D4 4 | Describe the stage model of memory. | Atkinson and Shiffrin 1968; sensory memory – large, very brief; attention to STM – 7±2, acoustic, rehearsal; LTM – unlimited, semantic; flow of information.
X: C4 D4 4 | 'Short-term memory is not just a store but a work-space.' Explain with reference to working memory. | Baddeley; holds and manipulates information during tasks such as mental arithmetic and reading; three components; limits of the stage model's STM.
L: D4 | Describe the information processing (stage) model of memory with reference to sensory, short-term and long-term memory. | Atkinson and Shiffrin; sensory memory – icon and echo; STM – capacity, duration, acoustic coding, rehearsal, chunking; LTM – unlimited, semantic; transfer.
L: D5 | Critically examine the stage model of memory and explain how the idea of working memory modified it. | Stage model – three stores, sequential flow; criticisms – STM not a single store; Baddeley's working memory – phonological loop, visuo-spatial sketchpad, central executive; levels of processing as alternative.
"""), ST(S + '06-st3', 'levels of processing and types of long-term memory', """
T: levels of processing | Craik and Lockhart's 1972 view that how well information is remembered depends on how deeply it is processed
T: semantic processing | the deepest level of processing, in which the meaning of information is analysed
T: structural processing | the shallowest level of processing, based on the physical features of information
T: declarative memory | long-term memory for facts, names, dates and events, which can be put into words
T: procedural memory | long-term memory for skills and how to do things, which is hard to put into words
T: episodic memory | declarative memory of personal life experiences
T: semantic memory | declarative memory of general knowledge, facts and the meanings of words
T: explicit memory | memory that is consciously and deliberately recalled
T: implicit memory | memory of which a person is not consciously aware
Q: The levels of processing view was proposed by: | Craik and Lockhart | Atkinson and Shiffrin | Baddeley | Tulving
Q: Remembering your first day at school is an example of: | episodic memory | semantic memory | procedural memory | sensory memory
Q: Knowing that Delhi is the capital of India is an example of: | semantic memory | episodic memory | procedural memory | implicit memory
Q: Knowing how to ride a bicycle is an example of: | procedural memory | episodic memory | semantic memory | iconic memory
Q: The distinction between episodic and semantic memory was made by: | Endel Tulving | Frederic Bartlett | Hermann Ebbinghaus | Alan Baddeley
Q: According to the levels of processing view, the deepest level is processing of: | meaning | physical features | sound | colour
Q: Typing without thinking where each key is shows: | implicit memory | episodic memory | explicit semantic memory | sensory memory
M:LTM type: Episodic memory | one's own life experiences
M:LTM type: Semantic memory | general knowledge and word meanings
M:LTM type: Procedural memory | skills such as swimming
M:level: Structural processing | physical features such as the shape of letters
M:level: Phonetic processing | the sound of a word
M:level: Semantic processing | the meaning of a word
S+: Information processed for meaning is retained longer than information processed for physical features
S+: Long-term memory is divided into declarative and procedural memory
S+: Declarative memory includes episodic and semantic memory
S+: Episodic memories are often emotional and personally significant
S+: Semantic memory is not tied to the time and place where it was learnt
S-: Structural processing is the deepest level of processing | Semantic processing of meaning is the deepest level
S-: Knowing how to swim is a semantic memory | It is a procedural memory
S-: Procedural memories are easy to put into words | Procedural memories are hard to describe; declarative memories can be put into words
C: Students remember more when they think about the meaning of a lesson | semantic processing is a deeper level of processing that gives better retention
C: We cannot easily explain how we ride a bicycle | procedural memory stores skills that are not easily put into words
C: We remember facts without remembering where we learnt them | semantic memory is not tied to the time and place of learning
X: C2 D2 2 | Distinguish between episodic and semantic memory. | Episodic – personal life experiences, linked to time and place; semantic – general knowledge, facts and meanings.
X: C2 D2 2 | Distinguish between declarative and procedural memory. | Declarative – facts and events that can be put into words; procedural – skills and how to do things, hard to describe.
X: C3 D3 3 | Explain the levels of processing view of memory. | Craik and Lockhart 1972; structural – physical features, shallow; phonetic – sound; semantic – meaning, deepest; deeper processing, better retention.
X: C3 D4 4 | Classify the types of long-term memory with examples. | Declarative – episodic (personal events), semantic (facts); procedural (skills); explicit and implicit memory; examples.
X: C4 D4 4 | Two students read the same chapter: one reads it aloud repeatedly, the other relates each idea to examples. Who is likely to remember better and why? | Second – semantic, deeper processing, elaborative rehearsal; first – shallow, phonetic processing; levels of processing view.
L: D4 | Explain the levels of processing view and describe the types of long-term memory. | Craik and Lockhart – structural, phonetic, semantic levels; depth and retention; declarative – episodic and semantic; procedural; explicit and implicit memory; examples.
"""), ST(S + '06-st4', 'knowledge representation, constructive memory and forgetting', """
T: schema | a mental structure that organises knowledge and guides how information is interpreted and remembered
T: hierarchical network model | Collins and Quillian's model in which knowledge is stored as concepts linked in a hierarchy
T: constructive memory | the view that remembering is a process of reconstruction influenced by schemas, beliefs and expectations
T: serial reproduction | Bartlett's method in which a person recalls material repeatedly over intervals, showing how memory changes
T: forgetting | the inability to recall information that was learnt earlier
T: trace decay | the view that forgetting occurs because memory traces fade with disuse over time
T: interference | the view that forgetting occurs because different learnings compete with each other
T: proactive interference | interference in which earlier learning interferes with the recall of later learning
T: retroactive interference | interference in which later learning interferes with the recall of earlier learning
T: retrieval failure | forgetting that occurs because the right retrieval cues are absent or inappropriate
Q: The study of memory as a constructive process using serial reproduction was done by: | Frederic Bartlett | Hermann Ebbinghaus | Craik and Lockhart | Atkinson and Shiffrin
Q: The forgetting curve was first plotted by: | Hermann Ebbinghaus | Frederic Bartlett | Endel Tulving | Alan Baddeley
Q: According to Ebbinghaus's forgetting curve, forgetting is: | rapid at first and then slows down | slow at first and then rapid | constant over time | absent in the first hour
Q: Learning a new phone number makes you forget your old one. This is: | retroactive interference | proactive interference | trace decay | repression
Q: Your old habit of driving on the left makes it hard to learn to drive on the right abroad. This shows: | proactive interference | retroactive interference | retrieval failure | trace decay
Q: Being sure you know a name but not being able to recall it at the moment shows: | retrieval failure | trace decay | encoding failure | proactive interference
Q: The hierarchical network model of knowledge representation was proposed by: | Collins and Quillian | Craik and Lockhart | Atkinson and Shiffrin | Baddeley
M:cause of forgetting: Trace decay | memory traces fading with disuse
M:cause of forgetting: Proactive interference | old learning disrupting new learning
M:cause of forgetting: Retroactive interference | new learning disrupting old learning
M:cause of forgetting: Retrieval failure | absence of suitable retrieval cues
S+: Knowledge in long-term memory is organised in the form of concepts, categories and schemas
S+: Bartlett showed that people change material while recalling it to fit their schemas
S+: Memory is not a copy of the past but a reconstruction
S+: Ebbinghaus used nonsense syllables to study forgetting
S+: Interference theory explains forgetting by competition between different learnings
S+: According to retrieval failure theory, information may be available in memory but not accessible
S-: Memory is an exact copy of past events | Bartlett showed memory is a constructive process
S-: Proactive interference is when new learning disrupts old learning | That is retroactive interference; proactive is old learning disrupting new learning
S-: According to Ebbinghaus, forgetting is slow at first and rapid later | Forgetting is rapid at first and slows down later
C: Eyewitness accounts may be inaccurate | memory is reconstructed using schemas and expectations rather than copied
C: Studying similar subjects one after another may lead to forgetting | similar learnings interfere with each other
C: A forgotten name may be recalled when we meet a related person | retrieval failure is overcome when suitable retrieval cues are present
X: C2 D2 2 | Distinguish between proactive and retroactive interference. | Proactive – earlier learning interferes with recall of later learning; retroactive – later learning interferes with recall of earlier learning.
X: C2 D2 2 | What did Bartlett mean by memory as a constructive process? | Remembering is reconstruction influenced by schemas, beliefs and expectations; serial reproduction showed changes in recalled material.
X: C3 D3 3 | Explain the three causes of forgetting. | Trace decay – fading with disuse; interference – proactive and retroactive; retrieval failure – absence of suitable cues, tip of tongue.
X: C3 D3 3 | Describe Ebbinghaus's forgetting curve. | Nonsense syllables; relearning; forgetting rapid in first hours, then slows and levels off; shows most forgetting soon after learning.
X: C3 D4 4 | Explain how knowledge is represented and organised in memory. | Concepts and categories; prototypes; schemas; hierarchical network model of Collins and Quillian; organisation helps retrieval.
X: C4 D4 4 | Evaluate trace decay theory as an explanation of forgetting. | Traces fade with disuse; but forgetting depends more on what happens between learning and recall; sleep studies show less forgetting; interference and retrieval failure explain better.
L: D4 | What is forgetting? Explain the nature and causes of forgetting. | Definition; Ebbinghaus's curve; trace decay; interference – proactive, retroactive; retrieval failure – availability and accessibility, cues; examples.
L: D5 | Explain how knowledge is represented in memory and why memory is considered a constructive process. | Concepts, categories, schemas; hierarchical network; Bartlett's serial reproduction; errors in recall shaped by schemas; implications for eyewitness testimony.
"""), ST(S + '06-st5', 'enhancing memory', """
T: mnemonics | strategies or devices that help improve memory
T: keyword method | a mnemonic in which a familiar word that sounds like a new word is linked to it through an image
T: method of loci | a mnemonic in which items are placed as images in familiar locations in a known order
T: first-letter technique | a mnemonic in which the first letters of items are combined into a word or sentence, such as VIBGYOR
T: PQRST method | a study method involving Preview, Question, Read, Self-recitation and Test
Q: Remembering the colours of the rainbow as VIBGYOR uses the: | first-letter technique | method of loci | keyword method | chunking
Q: Imagining items placed along a familiar route in your house is the: | method of loci | keyword method | first-letter technique | PQRST method
Q: In the PQRST method, 'S' stands for: | Self-recitation | Summary | Search | Storage
Q: Mnemonics that use mental images include the keyword method and the: | method of loci | first-letter technique | chunking | PQRST method
M:mnemonic: Keyword method | linking a new word to a similar-sounding familiar word
M:mnemonic: Method of loci | placing images in familiar locations
M:mnemonic: First-letter technique | acronyms such as VIBGYOR
M:mnemonic: Chunking | grouping items into larger units
S+: Mnemonics may use images or organisation of material
S+: Processing information deeply, in terms of meaning, improves memory
S+: Minimising interference by spacing study of similar subjects helps memory
S+: Providing oneself with retrieval cues during learning helps later recall
S+: The PQRST method helps students study textbook material effectively
S-: The method of loci uses the first letters of words | That is the first-letter technique; the method of loci places images in familiar locations
S-: Studying similar subjects back to back improves memory | It increases interference; spacing similar subjects helps
C: The first-letter technique helps in remembering lists | combining first letters gives an organised cue for recalling all the items
C: The method of loci aids recall | each item is linked to a familiar location that serves as a retrieval cue
C: Self-recitation improves retention | recalling material actively strengthens encoding and provides retrieval practice
X: C2 D2 2 | Distinguish between the keyword method and the method of loci. | Keyword – link new word to similar-sounding familiar word by an image; loci – place items as images in familiar locations in order.
X: C2 D2 2 | What does PQRST stand for in the study method? | Preview, Question, Read, Self-recitation, Test.
X: C3 D3 3 | Explain any three strategies for improving memory other than mnemonics. | Deep, semantic processing; minimise interference; give enough retrieval cues; distributed practice; PQRST (any three).
X: C3 D4 4 | Describe mnemonics using images and using organisation. | Images – keyword method, method of loci; organisation – chunking, first-letter technique; examples of each.
X: C4 D4 4 | Suggest a study plan for a student who forgets lessons quickly, using principles of memory. | PQRST; semantic processing; spacing study, minimise interference; mnemonics; retrieval cues; self-testing.
L: D4 | Describe the techniques of enhancing memory. | Mnemonics using images – keyword, loci; using organisation – chunking, first-letter; other strategies – deep processing, minimising interference, retrieval cues; PQRST method.
"""), ]

CH07 = [ST(S + '07-st1', 'nature of thinking and its building blocks', """
T: thinking | a higher mental process through which we manipulate and analyse acquired or existing information
T: mental image | a mental representation of a sensory experience, which can be used to think about things
T: concept | a mental representation of a category, referring to a class of objects, ideas or events that share common properties
T: prototype | the best or most typical example of a concept
T: natural concept | a concept formed from everyday experience, whose features are not clearly defined
T: artificial concept | a concept with clearly defined rules and features, such as a square
Q: Thinking is described as a: | higher mental process | reflex | sensory process | motor response
Q: The two building blocks of thought are mental images and: | concepts | reflexes | stimuli | sensations
Q: For most people a sparrow is a more typical example of 'bird' than an ostrich. The sparrow is a: | prototype | schema | mental set | heuristic
Q: A concept such as 'square', whose features are clearly defined, is a: | artificial concept | natural concept | prototype | mental image
M:building block: Mental image | a picture of your house in your mind
M:building block: Concept | the category 'fruit'
M:building block: Prototype | the most typical member of a category
S+: Thinking is the base of all cognitive activities
S+: Thinking is mostly goal-directed
S+: Thinking involves manipulation and analysis of information received from the environment
S+: Concepts help us organise knowledge so that it can be retrieved quickly
S+: Mental images are used in thinking about objects that are not present
S-: Thinking deals only with objects that are physically present | Thinking uses mental images and concepts of objects not present
S-: A prototype is the least typical member of a category | A prototype is the most typical example of a concept
C: Concepts make thinking efficient | they group similar objects and events so that we need not treat each one as new
C: An architect can plan a building before it is built | thinking uses mental images to represent objects not physically present
X: C2 D2 2 | What is thinking? Name its two building blocks. | Higher mental process manipulating and analysing information; building blocks – mental images and concepts.
X: C2 D2 2 | Distinguish between a concept and a prototype. | Concept – mental representation of a category; prototype – most typical example of the concept.
X: C3 D3 3 | Explain the role of concepts in thinking. | Mental categories; organise knowledge; quick retrieval; prototypes; natural and artificial concepts; efficient thinking.
X: C3 D4 4 | Explain the nature of thinking and its building blocks. | Higher mental process; goal-directed; manipulation of information; mental images; concepts and prototypes; examples.
L: D4 | Describe the nature of thinking and explain the role of mental images and concepts as its building blocks. | Definition; goal-directed; internal representation; mental images; concepts – natural, artificial, prototypes; organisation of knowledge.
"""), ST(S + '07-st2', 'problem solving, reasoning and decision making', """
T: problem solving | thinking that is directed towards the solution of a specific problem by moving from an initial state to a goal state
T: mental set | a tendency to solve problems by following already tried mental operations or steps
T: functional fixedness | the tendency to think of objects only in terms of their usual functions, which hinders problem solving
T: deductive reasoning | reasoning that begins with a general assumption and draws a specific conclusion from it
T: inductive reasoning | reasoning that draws a general conclusion from specific facts or observations
T: analogical reasoning | reasoning that solves a problem by using a similar problem whose solution is known
T: decision making | choosing one option from among several alternatives
T: judgement | the process of drawing conclusions, forming opinions and evaluating objects or events on the basis of information
Q: Solving a new problem in the same way as earlier problems, even when a simpler method exists, shows: | mental set | insight | creativity | inductive reasoning
Q: Failing to see that a coin can be used as a screwdriver shows: | functional fixedness | mental set only | divergent thinking | deductive reasoning
Q: Concluding that all crows are black after seeing many black crows is: | inductive reasoning | deductive reasoning | analogical reasoning | judgement
Q: 'All humans are mortal; Ravi is human; so Ravi is mortal' is an example of: | deductive reasoning | inductive reasoning | analogical reasoning | brainstorming
Q: Choosing which college to join from several offers is an example of: | decision making | perception | mental imagery | sensation
Q: Which of these is an obstacle to problem solving? | Lack of motivation | Brainstorming | Incubation | Flexibility
M:reasoning: Deductive reasoning | general assumption to specific conclusion
M:reasoning: Inductive reasoning | specific observations to general conclusion
M:reasoning: Analogical reasoning | using a similar solved problem
M:obstacle: Mental set | sticking to earlier tried methods
M:obstacle: Functional fixedness | seeing objects only in their usual use
M:obstacle: Lack of motivation | giving up easily after failure
S+: Problem solving is goal-directed thinking
S+: Mental set and lack of motivation are obstacles to problem solving
S+: Deductive reasoning goes from the general to the particular
S+: Inductive reasoning goes from particular facts to general conclusions
S+: Judgement and decision making are interrelated processes
S+: Decision making involves evaluating alternatives in terms of their costs and benefits
S-: Inductive reasoning goes from a general rule to a particular case | That is deductive reasoning; inductive goes from particular facts to a general conclusion
S-: Mental set always helps in solving new problems | Mental set may hinder solving problems that need new methods
S-: Decision making and judgement are unrelated | They are interrelated; decisions are based on judgements
C: A person may fail to solve a problem that needs a new method | mental set makes people stick to methods that worked before
C: Scientists often use inductive reasoning | they draw general conclusions from many specific observations
C: Experienced doctors make faster diagnoses | they use knowledge of similar earlier cases, as in analogical reasoning
X: C2 D2 2 | Distinguish between deductive and inductive reasoning, with an example of each. | Deductive – general to specific, e.g. syllogism; inductive – specific observations to general conclusion, e.g. all crows seen are black.
X: C2 D2 2 | Distinguish between judgement and decision making. | Judgement – forming opinions and evaluating on available information; decision making – choosing among alternatives, based on judgements.
X: C3 D3 3 | Explain any three obstacles to problem solving. | Mental set; functional fixedness; lack of motivation; meaning and examples.
X: C3 D4 4 | Describe the process of reasoning and its types. | Deductive; inductive; analogical; examples; errors in reasoning; role in problem solving.
X: C4 D4 4 | A student keeps using a long method for a sum and does not try the shortcut the teacher shows. Explain this and suggest how to overcome it. | Mental set; earlier success reinforces old method; overcome by awareness, practising new methods, seeing problem afresh, motivation.
L: D4 | Explain problem solving and the obstacles to it. Describe the different types of reasoning. | Initial state to goal state; obstacles – mental set, functional fixedness, lack of motivation; deductive, inductive, analogical reasoning; examples.
L: D5 | Discuss judgement and decision making, and how reasoning helps in solving real-life problems. | Judgement on information; decision making among alternatives; costs and benefits; role of reasoning; errors and biases; examples from daily life.
"""), ST(S + '07-st3', 'creative thinking', """
T: creative thinking | thinking that produces ideas, objects or solutions that are novel and appropriate
T: divergent thinking | open-ended thinking that produces many different answers to a problem
T: convergent thinking | thinking that leads to one correct answer to a problem
T: fluency | the ability to produce many ideas for a task or problem
T: flexibility | the ability to think of varied ideas and look at a problem from different angles
T: originality | the ability to produce ideas that are rare or unusual
T: elaboration | the ability to go into the details of an idea and work out its implications
T: incubation | the stage of creative thinking in which one stops working on the problem consciously while ideas develop
T: illumination | the stage of creative thinking in which the solution suddenly appears, the 'aha' experience
T: brainstorming | a group technique in which ideas are freely generated without being judged, developed by Alex Osborn
Q: Thinking of many unusual uses for a brick is an example of: | divergent thinking | convergent thinking | deductive reasoning | mental set
Q: Solving a multiple-choice question with one correct answer needs: | convergent thinking | divergent thinking | incubation | elaboration
Q: The stage of creative thinking in which the solution suddenly appears is: | illumination | preparation | incubation | verification
Q: The last stage of creative thinking, in which the solution is tested, is: | verification | illumination | incubation | preparation
Q: The ability to produce many ideas is called: | fluency | flexibility | originality | elaboration
Q: Brainstorming was developed by: | Alex Osborn | Jean Piaget | Albert Bandura | Ivan Pavlov
M:creative stage: Preparation | understanding the problem and gathering information
M:creative stage: Incubation | setting the problem aside while ideas develop
M:creative stage: Illumination | sudden appearance of a solution
M:creative stage: Verification | testing and checking the solution
M:divergent ability: Fluency | producing many ideas
M:divergent ability: Flexibility | producing varied kinds of ideas
M:divergent ability: Originality | producing unusual ideas
M:divergent ability: Elaboration | working out the details of an idea
S+: Creative thinking involves both divergent and convergent thinking
S+: Creative thinking passes through preparation, incubation, illumination and verification
S+: Barriers to creative thinking may be habitual, perceptual, motivational, emotional or cultural
S+: In brainstorming, criticism of ideas is avoided until many ideas have been produced
S+: Fear of failure and negative thinking are barriers to creative thinking
S-: Convergent thinking produces many possible answers | Divergent thinking produces many answers; convergent thinking leads to one correct answer
S-: Illumination is the first stage of creative thinking | Preparation is the first stage; illumination is the third
S-: Ideas should be criticised immediately during brainstorming | Judgement is postponed until many ideas are generated
C: Brainstorming helps creative thinking | postponing criticism encourages free and unusual ideas
C: A solution often comes after a break from the problem | during incubation ideas develop without conscious effort
C: Fear of failure blocks creativity | it stops people from taking risks and trying unusual ideas
X: C2 D2 2 | Distinguish between divergent and convergent thinking. | Divergent – open-ended, many answers; convergent – one correct answer.
X: C2 D2 2 | Name the four abilities of divergent thinking. | Fluency, flexibility, originality and elaboration.
X: C3 D3 3 | Explain any three barriers to creative thinking. | Habitual – rigid habits; perceptual – fixed ways of seeing; motivational and emotional – fear of failure, low motivation; cultural – conformity, tradition (any three).
X: C3 D4 4 | Describe the four stages of the creative thinking process. | Preparation; incubation; illumination; verification – meaning and example of each.
X: C4 D4 4 | Suggest four strategies a school can use to develop students' creative thinking. | Brainstorming; encourage questions and multiple answers; reward originality; reduce fear of failure; feedback; time for incubation; varied experiences.
L: D4 | What is creative thinking? Describe its stages and the abilities involved in divergent thinking. | Novelty and appropriateness; preparation, incubation, illumination, verification; fluency, flexibility, originality, elaboration; convergent thinking also needed.
L: D5 | Discuss the barriers to creative thinking and suggest strategies to enhance it. | Habitual, perceptual, motivational, emotional, cultural barriers; strategies – brainstorming, awareness of habits, positive thinking, feedback, risk taking, incubation; examples.
"""), ST(S + '07-st4', 'thought and language; development and use of language', """
T: language | a system of symbols organised by rules, used to communicate with others
T: linguistic relativity hypothesis | Benjamin Lee Whorf's view that language determines the content and ways of thinking
T: babbling | the stage of language development, around six months, in which infants produce repeated sound combinations such as 'ba-ba'
T: holophrase | a single word used by a young child to express a whole thought
T: telegraphic speech | early speech of children with two or three words, leaving out small words
T: phoneme | the smallest unit of sound in a language
T: morpheme | the smallest unit of language that carries meaning
T: syntax | the rules for combining words into sentences
T: semantics | the meaning of words and sentences in a language
T: language acquisition device | Noam Chomsky's idea of an innate mechanism that helps children learn language
T: bilingualism | the use of two languages by a person
Q: The linguistic relativity hypothesis was proposed by: | Benjamin Lee Whorf | Jean Piaget | Lev Vygotsky | Noam Chomsky
Q: The view that thought and language have different origins and merge at about two years was given by: | Lev Vygotsky | Benjamin Lee Whorf | B.F. Skinner | Noam Chomsky
Q: The view that thought develops first and language reflects it was held by: | Jean Piaget | Benjamin Lee Whorf | B.F. Skinner | Albert Bandura
Q: The language acquisition device was proposed by: | Noam Chomsky | B.F. Skinner | Jean Piaget | Benjamin Lee Whorf
Q: The smallest meaningful unit of language is a: | morpheme | phoneme | syntax | sentence
Q: Skinner explained language development through: | imitation and reinforcement | an innate device | insight | maturation alone
Q: A child saying 'milk' to mean 'I want milk' is using a: | holophrase | telegraphic sentence | phoneme | morpheme only
M:view: Benjamin Lee Whorf | language determines thought
M:view: Jean Piaget | thought determines language
M:view: Lev Vygotsky | thought and language have different origins and merge around two years
M:view: Noam Chomsky | innate language acquisition device
M:view: B.F. Skinner | language learnt by imitation and reinforcement
M:component: Phoneme | smallest unit of sound
M:component: Morpheme | smallest unit of meaning
M:component: Syntax | rules for combining words into sentences
M:component: Semantics | meaning of words and sentences
S+: Language development begins with crying and cooing, followed by babbling
S+: Children's first words usually appear around their first birthday
S+: Telegraphic speech leaves out small words but conveys meaning
S+: Chomsky held that children are born with an innate capacity for language
S+: Vygotsky held that thought and language develop separately at first and merge at about two years
S+: Many people in India are bilingual or multilingual
S-: Chomsky explained language through reinforcement and imitation | Skinner explained it by reinforcement; Chomsky proposed an innate language acquisition device
S-: A phoneme is the smallest unit of meaning | A phoneme is the smallest unit of sound; a morpheme is the smallest unit of meaning
S-: Whorf held that thought determines language | Whorf held that language determines thought; Piaget held that thought determines language
C: Children all over the world pass through similar stages of language development | according to Chomsky, they are born with an innate language acquisition device
C: Children often say things like 'I goed' | they apply rules of grammar they have learnt, which cannot be explained by imitation alone
C: Children use the language of their parents | according to Skinner, language is learnt through imitation and reinforcement
X: C2 D2 2 | Distinguish between a phoneme and a morpheme. | Phoneme – smallest unit of sound; morpheme – smallest unit of meaning.
X: C2 D2 2 | What is the linguistic relativity hypothesis? | Whorf's view that language determines content and ways of thinking; speakers of different languages think differently.
X: C3 D3 3 | Explain the three views on the relationship between thought and language. | Whorf – language determines thought; Piaget – thought determines language; Vygotsky – different origins, merge at about two years.
X: C3 D4 4 | Describe the stages of language development in children. | Crying, cooing; babbling around six months; first words around one year, holophrases; two-word and telegraphic speech; rapid vocabulary growth; grammar.
X: C4 D4 4 | Compare Skinner's and Chomsky's views of language development. | Skinner – imitation, reinforcement, environment; Chomsky – innate language acquisition device, universal stages, creative rule use; evidence such as overgeneralisation; both partly right.
L: D4 | Explain the relationship between thought and language. Describe the development of language in children. | Whorf, Piaget, Vygotsky views; components – phonemes, morphemes, syntax, semantics; stages – crying, cooing, babbling, first words, telegraphic speech; theories of Skinner and Chomsky.
"""), ]

CH08 = [ST(S + '08-st1', 'nature of motivation and biological and psychosocial motives', """
T: motivation | the process that energises and directs behaviour towards a goal
T: motivational cycle | the sequence in which a need gives rise to a drive, which leads to activity that ends when the goal is reached
T: need | a lack or deficit of some necessity, which creates a state of tension
T: drive | the state of tension or arousal produced by a need, which energises behaviour
T: incentive | an external object or goal that satisfies a need and attracts behaviour
T: homeostasis | the tendency of the body to maintain a balanced, stable internal state
T: need for achievement | the need to meet standards of excellence and succeed, measured with the Thematic Apperception Test
T: need for affiliation | the need to seek the company of others and establish relationships
T: need for power | the need to influence or control others and the environment, studied by David McClelland
T: curiosity | the motive to seek novel experiences and information
Q: The word 'motivation' comes from the Latin word 'movere', meaning: | to move | to feel | to think | to see
Q: In the motivational cycle, a need gives rise to a: | drive | goal | reflex | concept
Q: The tendency of the body to maintain a stable internal state is called: | homeostasis | motivation | arousal | adaptation
Q: The need to meet standards of excellence is called: | need for achievement | need for affiliation | need for power | curiosity
Q: The Thematic Apperception Test is commonly used to measure: | need for achievement | intelligence | reaction time | memory span
Q: Hunger and thirst are examples of: | biological motives | psychosocial motives | incentives | goals
Q: Need for power has been studied in detail by: | David McClelland | Abraham Maslow | B.F. Skinner | Jean Piaget
M:motive: Need for achievement | striving to meet standards of excellence
M:motive: Need for affiliation | seeking the company of others
M:motive: Need for power | influencing or controlling others
M:motive: Curiosity | seeking new experiences and information
S+: Motivation energises and directs behaviour towards a goal
S+: The motivational cycle includes need, drive, instrumental response and goal attainment
S+: Biological motives are based on physiological needs of the body such as hunger and thirst
S+: Psychosocial motives are learnt through interaction with the social environment
S+: People high in need for achievement prefer tasks of moderate difficulty
S+: The hypothalamus plays an important role in hunger and thirst
S-: Psychosocial motives are entirely inborn | Psychosocial motives are learnt through social interaction
S-: People high in need for achievement prefer very easy tasks | They prefer tasks of moderate difficulty and challenge
S-: In the motivational cycle the goal comes before the need | The cycle begins with a need, which produces a drive towards a goal
C: Hunger is called a biological motive | it is based on the physiological need of the body for food
C: Motives cannot be observed directly | they are inferred from behaviour directed towards goals
C: People seek friends when they are anxious | the need for affiliation is aroused when people feel threatened or alone
X: C2 D2 2 | Distinguish between need and drive. | Need – lack or deficit of a necessity; drive – state of tension or arousal produced by the need that energises behaviour.
X: C2 D2 2 | Distinguish between biological and psychosocial motives, with one example each. | Biological – physiological needs, e.g. hunger, thirst; psychosocial – learnt in social interaction, e.g. need for achievement, affiliation.
X: C3 D3 3 | Explain the motivational cycle with an example. | Need – deficit; drive – tension; instrumental response – activity; goal – satisfies need; relief, cycle repeats; e.g. hunger and eating.
X: C3 D3 3 | Explain any three psychosocial motives. | Need for affiliation; need for power; need for achievement; curiosity and exploration (any three).
X: C3 D4 4 | Explain the biological bases of hunger and thirst. | Hunger – stomach contractions, blood glucose, hormones, hypothalamus; thirst – dryness of mouth, water loss from cells; homeostasis.
X: C4 D4 4 | Riya chooses moderately difficult tasks, sets high standards and works hard to succeed. Which motive does she show? Explain its features. | Need for achievement; standards of excellence; preference for moderate difficulty; persistence; learnt in childhood; measured with TAT.
L: D4 | Explain the nature of motivation. Describe the biological and psychosocial motives. | Definition; motivational cycle; biological motives – hunger, thirst, homeostasis, hypothalamus; psychosocial – affiliation, power, achievement, curiosity and exploration.
"""), ST(S + '08-st2', "Maslow's hierarchy of needs", """
T: hierarchy of needs | Abraham Maslow's arrangement of human needs in levels, from basic physiological needs to self-actualisation
T: physiological needs | the most basic needs in Maslow's hierarchy, such as food, water and sleep
T: safety needs | the needs for physical and psychological security and protection from danger
T: belongingness and love needs | the needs to be loved, to belong and to have relationships with others
T: esteem needs | the needs for respect, recognition and a positive self-image
T: self-actualisation | the highest need in Maslow's hierarchy, to realise one's full potential
Q: The hierarchy of needs was proposed by: | Abraham Maslow | David McClelland | Carl Rogers | Sigmund Freud
Q: The most basic needs in Maslow's hierarchy are: | physiological needs | safety needs | esteem needs | self-actualisation needs
Q: The highest need in Maslow's hierarchy is: | self-actualisation | esteem | safety | belongingness and love
Q: The need for respect and recognition belongs to: | esteem needs | safety needs | physiological needs | belongingness needs
Q: In Maslow's hierarchy, the need that comes just after physiological needs is: | safety | esteem | self-actualisation | belongingness and love
M:Maslow level: Physiological needs | food, water and sleep
M:Maslow level: Safety needs | protection from danger and security
M:Maslow level: Belongingness and love needs | friendship and acceptance
M:Maslow level: Esteem needs | respect and recognition
M:Maslow level: Self-actualisation | realising one's full potential
S+: According to Maslow, lower-level needs generally have to be satisfied before higher-level needs become important
S+: Self-actualised people are self-aware, creative, spontaneous and socially responsive
S+: Maslow's theory is a humanistic view of motivation
S+: Few people reach the level of self-actualisation
S-: Self-actualisation is the most basic need in Maslow's hierarchy | Physiological needs are the most basic; self-actualisation is the highest
S-: Esteem needs come before safety needs in Maslow's hierarchy | Safety needs come before belongingness and esteem needs
S-: Maslow's theory is a behaviourist theory | It is a humanistic theory of motivation
C: A starving person is unlikely to be concerned with esteem | according to Maslow, lower-level needs must be satisfied before higher ones become important
C: Maslow's theory is called humanistic | it stresses the human urge to grow and realise one's potential
X: C2 D2 2 | Name the five levels of Maslow's hierarchy of needs in order. | Physiological, safety, belongingness and love, esteem, self-actualisation.
X: C2 D2 2 | What is self-actualisation? State two features of self-actualised people. | Realising one's full potential; self-aware, creative, spontaneous, open to novelty, socially responsive (any two).
X: C3 D3 3 | Explain Maslow's hierarchy of needs with examples. | Five levels with examples; lower needs before higher; humanistic view; self-actualisation as highest need.
X: C3 D4 4 | Evaluate Maslow's hierarchy of needs. | Strengths – humanistic, explains growth, wide use in education and work; limits – order may vary, people may seek higher needs despite unmet lower needs, cultural differences.
X: C4 D4 4 | A poor artist continues to paint even when he cannot afford regular meals. Does this support or challenge Maslow's theory? Explain. | Challenges strict hierarchy – self-actualisation sought despite unmet physiological needs; Maslow said 'generally', order can vary; individual differences.
L: D4 | Describe Maslow's hierarchy of needs. Explain the characteristics of self-actualised people. | Five levels from physiological to self-actualisation; lower before higher; self-actualised – self-aware, creative, spontaneous, socially responsive; humanistic view; evaluation.
"""), ST(S + '08-st3', 'nature, bases and expression of emotions', """
T: emotion | a complex pattern of arousal, subjective feeling and cognitive interpretation
T: James-Lange theory | the theory that the perception of bodily changes following a stimulus produces the experience of emotion
T: Cannon-Bard theory | the theory that the thalamus sends messages at the same time to the cortex, producing emotional experience, and to the body, producing physiological changes
T: Schachter-Singer two-factor theory | the theory that emotion depends on physiological arousal and the cognitive label given to it
T: display rules | cultural norms about how and when emotions should be expressed
T: basic emotions | a small number of primary emotions, such as joy, fear and anger, from which other emotions are formed
T: paralanguage | the non-word features of speech, such as tone, pitch and loudness, that convey emotion
Q: The word 'emotion' comes from the Latin word 'emovere', meaning: | to stir up | to move away | to think | to feel
Q: The theory that we feel afraid because we tremble was proposed by: | James and Lange | Cannon and Bard | Schachter and Singer | Plutchik
Q: The theory that the thalamus produces emotional experience and bodily changes at the same time is the: | Cannon-Bard theory | James-Lange theory | two-factor theory | arousal theory
Q: According to Schachter and Singer, emotion depends on arousal and: | cognitive labelling | reflexes | the thalamus alone | display rules
Q: Plutchik proposed that the number of basic emotions is: | eight | two | twenty | five
Q: Cultural norms about expressing emotions are called: | display rules | paralanguage | prototypes | schemas
Q: In emergencies, emotional arousal is produced mainly by the: | sympathetic nervous system | parasympathetic nervous system | somatic nervous system | spinal reflexes alone
M:theory of emotion: James-Lange theory | bodily changes come first, then emotion
M:theory of emotion: Cannon-Bard theory | thalamus triggers feeling and bodily changes together
M:theory of emotion: Schachter-Singer theory | arousal plus cognitive label
S+: Emotions involve physiological arousal, subjective feelings and cognitive interpretation
S+: The hypothalamus and limbic system play an important role in emotions
S+: Facial expressions of some basic emotions are recognised across cultures
S+: Culture influences the expression of emotions through display rules
S+: Emotions are expressed verbally and non-verbally, through facial expressions, gestures and paralanguage
S+: Plutchik held that emotions vary in intensity and that basic emotions combine to form other emotions
S-: According to James-Lange theory, emotion comes before bodily changes | James-Lange theory holds that bodily changes come first and their perception is the emotion
S-: Cannon-Bard theory holds that emotion depends only on cognitive labelling | That is the Schachter-Singer view; Cannon-Bard says the thalamus triggers feeling and bodily changes together
S-: All cultures express emotions in exactly the same way | Display rules differ across cultures
C: The same arousal may be felt as fear or excitement | according to Schachter and Singer, emotion depends on the cognitive label given to arousal
C: People from different cultures can recognise a smile | facial expressions of basic emotions are largely universal
C: People in some cultures hide anger in public | display rules of a culture govern how emotions are expressed
X: C2 D2 2 | Distinguish between the James-Lange and Cannon-Bard theories of emotion. | James-Lange – bodily changes first, their perception is emotion; Cannon-Bard – thalamus sends messages simultaneously to cortex and body.
X: C2 D2 2 | What are display rules? Give an example. | Cultural norms about how and when to express emotions, e.g. not showing anger before elders in public.
X: C3 D3 3 | Explain the Schachter-Singer two-factor theory of emotion. | Emotion = physiological arousal + cognitive label; same arousal labelled differently depending on situation; experiment with injected arousal and different contexts.
X: C3 D4 4 | Explain the role of culture in the expression of emotions. | Basic facial expressions universal; display rules differ; non-verbal – gestures, gaze, paralanguage; cultural differences in emotion words and intensity; examples.
X: C4 D4 4 | Your heart races while waiting for exam results; your friend feels the same before a cricket match and calls it excitement. Explain using theories of emotion. | Same arousal; Schachter-Singer – label depends on cognitive appraisal of situation; James-Lange and Cannon-Bard compared; role of cognition.
L: D4 | Explain the nature of emotions. Describe the physiological and cognitive bases of emotions. | Arousal, feeling, cognition; basic emotions (Plutchik); physiology – ANS, hypothalamus, limbic system; theories – James-Lange, Cannon-Bard, Schachter-Singer.
L: D5 | Discuss the expression of emotions and the influence of culture on emotions. | Verbal and non-verbal expression; facial expressions; paralanguage; gestures; universality of basic expressions; display rules; cultural labelling; examples from India.
"""), ST(S + '08-st4', 'managing negative emotions and enhancing positive emotions', """
T: self-awareness | being aware of one's own emotions and feelings, the first step in managing emotions
T: self-monitoring | constantly assessing one's past and present emotional experiences and their effects
T: self-modification | changing one's behaviour or emotions through learnt techniques
T: positive emotions | pleasant emotions such as happiness, hope and contentment, which improve well-being
T: optimism | the tendency to expect positive outcomes
T: positive psychology | the study of positive emotions, character strengths and conditions that help people flourish
Q: The first step in managing emotions is: | self-awareness | self-modification | suppression | denial
Q: Constantly assessing one's emotional experiences is called: | self-monitoring | self-modelling | appraisal | displacement
Q: Which of these helps in enhancing positive emotions? | Positive interpersonal relationships | Social isolation | Holding grudges | Pessimism
Q: Seeing a problem in a different, less threatening light is called: | perceptual reinterpretation | denial | projection | regression
Q: The study of character strengths and conditions that help people flourish is: | positive psychology | psychoanalysis | behaviourism | psychophysics
M:technique: Self-awareness | knowing one's own feelings
M:technique: Self-monitoring | assessing one's emotional experiences
M:technique: Self-modification | changing one's behaviour through techniques
M:technique: Perceptual reinterpretation | seeing a problem from a different angle
S+: Managing emotions does not mean suppressing them but understanding and regulating them
S+: Appraising a situation objectively helps in managing negative emotions
S+: Seeking social support and having empathy help in managing emotions
S+: Personality traits such as optimism, hope and positive self-regard enhance positive emotions
S+: Meaningful work and positive relationships contribute to well-being
S+: Participating in community service helps people feel good about themselves
S-: Managing emotions means suppressing all feelings | Managing emotions means understanding and regulating them, not suppressing them
S-: Pessimism helps enhance positive emotions | Optimism and hope enhance positive emotions
C: Self-awareness helps in managing anger | one can regulate an emotion only after recognising it and its causes
C: Optimistic people cope better with stress | they expect positive outcomes and keep trying
C: Social support reduces negative emotions | sharing problems with others gives comfort and new ways of seeing them
X: C2 D2 2 | Give any two ways of managing negative emotions. | Self-awareness; appraise situation objectively; self-monitoring; self-modification; seek support; empathy; community service (any two).
X: C2 D2 2 | Name two factors that enhance positive emotions. | Optimism and hope; positive self-regard; meaningful work; positive relationships; social support (any two).
X: C3 D3 3 | Explain any three tips for managing negative emotions. | Enhance self-awareness; appraise objectively; self-monitoring; self-modelling; perceptual reinterpretation; think creatively; cultivate relationships; empathy; community service (any three).
X: C3 D4 4 | How can positive emotions be enhanced? Explain. | Personality traits – optimism, hope, happiness, positive self-regard; meaningful work; positive interpersonal relationships; social support; positive psychology.
X: C4 D4 4 | Suggest how a student who gets very angry at small provocations can learn to manage anger. | Self-awareness of triggers; appraise objectively; pause before reacting; self-monitoring; relaxation; express feelings assertively; seek support; empathy.
L: D4 | Explain the techniques of managing negative emotions and enhancing positive emotions. | Self-awareness; objective appraisal; self-monitoring; self-modelling; perceptual reinterpretation; creative thinking; relationships; empathy; community service; optimism, hope, meaningful work, social support.
"""), ]

CHAPTERS = [(CH05, {}), (CH06, {}), (CH07, {}), (CH08, {})]
