"""IB MYP 5 Sciences (integrated) – ib-g10-science. The eAssessment year.

Criteria language: A knowing & understanding, B inquiring & designing, C processing & evaluating, D reflecting on the
impacts of science. Mocks follow the MYP 5 on-screen eAssessment: 3 tasks, 100 marks – Knowing & understanding (A) 25,
Investigation skills (B+C) 50, Applying science (D) 25. Shared builders: ib_myp_science_common.py.
"""
from __future__ import annotations

import math

from _common import F, Registry, T, mcq, name, two_names  # noqa: F401
from ib_myp_science_common import MARKBAND_D, SUB, dataset as _dataset, evx, exx, g, sci, inquiry as _inquiry  # noqa: F401

CONFIG = {'minutesPerMark': 1.2, 'mcqMinutes': 1.5}

# 20 items, 100 marks: A 25 (5×1 + 4×5), B+C 50 (5×6 + 4×5), D 25 (10 + 15).
MOCK = [
    dict(section='Task 1 – Knowing and understanding: quick-check items (criterion A)', count=5, c=['C1'], d=[1, 2, 2], type='mcq', marks=1),
    dict(section='Task 1 – Knowing and understanding: explain and apply scientific knowledge (criterion A)', count=4, c=['C2'], d=[2, 3, 3], type='explain', marks=5),
    dict(section='Task 2 – Investigation skills: planning an investigation (criterion B)', count=5, c=['C3', 'C3', 'C4'], d=[3, 4], type='multi_step', marks=6, style='inquiry'),
    dict(section='Task 2 – Investigation skills: processing and evaluating data (criterion C)', count=4, c=['C3'], d=[3, 4], type='multi_step', marks=5, style='data'),
    dict(section='Task 3 – Applying science: discuss and evaluate an application (criterion D)', count=1, c=['C4'], d=[4], type='long', marks=10, style='essay'),
    dict(section='Task 3 – Applying science: extended response on a global issue (criterion D)', count=1, c=['C4'], d=[5], type='long', marks=15, style='essay'),
]

R = Registry()
STYLE = {'eval_marks': 8, 'essay_marks': 15, 'markband': MARKBAND_D}


def init(subject_id):
    pass


def templates(st):
    out = R.build(st, STYLE)
    for t in out:  # Task 3 (criterion D) mock slots draw only on evaluate / extended-response templates
        if t.name in ('evaluate', 'extended'):
            t.style = 'essay'
    return out


def inquiry(key, *a):
    _inquiry(R, key, *a)


def dataset(key, *a):
    _dataset(R, key, *a)


# =============================================================================================
# ch01 Evolution and Natural Selection
# =============================================================================================
R.facts('ch01-st1', F(
    terms=[('evolution', 'the gradual change in the inherited characteristics of a population over many generations'),
           ('fossil', 'the preserved remains or traces of an organism that lived long ago, usually found in rock'),
           ('homologous structure', 'a structure with the same basic bone arrangement in different species, showing a common ancestor, e.g. the pentadactyl limb'),
           ('vestigial structure', 'a reduced structure that no longer has its original function, e.g. the human appendix or whale pelvic bones'),
           ('common ancestor', 'an ancestral species from which two or more later species evolved'),
           ('molecular evidence', 'comparisons of DNA or protein sequences between species; more similar sequences show closer relationships')],
    facts=[('Why is the fossil record incomplete?', 'Most organisms decay before they can fossilise, and many fossils are destroyed or not yet found', ['Fossils only form from animals with shells', 'Evolution did not happen in some periods', 'Fossils are always destroyed by heat'], 'Soft-bodied organisms rarely fossilise.'),
           ('A human arm, a bat wing and a whale flipper share the same bone pattern. What does this suggest?', 'They evolved from a common ancestor', ['They have the same function', 'They evolved separately with no link', 'They are the same species'], 'Homologous structures.'),
           ('Two species differ in 2% of their DNA bases; two others differ in 15%. What does this show?', 'The first pair share a more recent common ancestor', ['The second pair are more closely related', 'Both pairs are equally related', 'DNA cannot show relationships'], 'Mutations accumulate over time.'),
           ('In undisturbed rock layers, where are the oldest fossils usually found?', 'In the lowest layers', ['In the top layers', 'Evenly spread', 'Only in volcanic rock'], 'Sediments are laid down on top of older ones.'),
           ('Which evidence for evolution comes from comparing cytochrome c protein sequences?', 'Molecular (biochemical) evidence', ['Fossil evidence', 'Anatomical evidence', 'Behavioural evidence'], 'More differences → more distant relationship.')],
    why=[('Explain how the fossil record of the horse provides evidence for evolution.', 'Fossils in successively younger rock show gradual changes – larger body size, fewer toes, longer legs and teeth for grazing – matching adaptation to open grasslands over about 55 million years.'),
         ('Explain why DNA evidence is often considered stronger than anatomical evidence for working out relationships.', 'DNA differences can be counted objectively and accumulate at a roughly steady rate, while similar structures can arise independently (convergent evolution) and mislead.'),
         ('Explain why vestigial structures support the theory of evolution.', 'They are reduced remnants of structures that were useful in ancestors; they would not be expected if species were created separately with no shared history.')],
    contrast=[('homologous structures', 'analogous structures', 'Homologous structures share the same underlying anatomy because of a common ancestor but may have different functions; analogous structures have the same function (e.g. wings of birds and insects) but evolved separately with different structures.'),
              ('relative dating of fossils', 'radiometric dating', 'Relative dating orders fossils by their rock layer (lower = older); radiometric dating uses the decay of radioactive isotopes to give an age in years.')],
    misc=[('Evolution means humans evolved from modern chimpanzees.', 'Humans and chimpanzees share a common ancestor that lived about 6–7 million years ago; neither evolved from the other.'),
          ('There are no transitional fossils.', 'Many transitional fossils exist, such as Archaeopteryx (dinosaurs to birds) and Tiktaalik (fish to tetrapods).')],
    cases=[('Tiktaalik roseae (2004)', 'Palaeontologists predicted that fish-to-land transitional fossils would be found in 375-million-year-old river rocks and searched Arctic Canada; they found Tiktaalik, a fish with a neck, sturdy fins and lungs.', 'testable predictions in evolution', 'A successful prediction about where and in which age of rock a fossil would be found is strong evidence for evolution.'),
           ('The human genome and chimpanzee genome projects', 'Sequencing showed that humans and chimpanzees share about 98–99% of their DNA sequence, and human chromosome 2 is a fusion of two ape chromosomes.', 'molecular evidence', 'Molecular data independently confirmed relationships first proposed from anatomy and fossils.')],
    evaluate=[('DNA evidence has made fossil evidence unnecessary for understanding evolution.', ['DNA gives precise, quantitative relationships between living species', 'can detect relationships invisible in anatomy'], ['DNA rarely survives beyond about a million years, so extinct groups need fossils', 'fossils show what ancestors looked like and when changes happened'], 'Fossils and DNA are complementary; together they give a far more complete picture than either alone.'),
              ('Museums should return fossils to the countries where they were found.', ['fossils are part of a country’s natural heritage', 'supports local science and tourism'], ['some countries lack facilities to conserve and study them', 'international museums make fossils accessible to more researchers'], 'Fossils should generally be returned or co-curated, with partnerships to build local scientific capacity.')],
    extended=[('Describe three different types of evidence for evolution and explain how each supports the idea that species share common ancestors.', 'Fossils: rock layers show a sequence of changing forms and transitional fossils (Archaeopteryx); anatomical: homologous structures (pentadactyl limb) with the same bone plan modified for different uses, vestigial structures; molecular: DNA/protein sequences – the more similar, the more recent the common ancestor; patterns from each type of evidence agree with each other.', 6)],
))


@R.add('ch01-st1', 'C3', (1, 5), 'numerical')
def dna_diff(rng, slot):
    sp = [('human', 0), ('chimpanzee', 1.2), ('gorilla', 1.6), ('orang-utan', 3.1), ('macaque', 6.5)]
    a, b = rng.sample(sp[1:], 2)
    rate = rng.choice([0.25, 0.4])
    k = rng.choice(['closer', 'time'] if slot.d >= 3 else ['closer'])
    if k == 'closer':
        c = a if a[1] < b[1] else b
        return dict(stem=f'The DNA of a {a[0]} differs from human DNA at {a[1]}% of bases; the DNA of a {b[0]} differs at {b[1]}%. Which species is more closely related to humans, and why?', answer=f'The {c[0]}; fewer differences means a more recent common ancestor',
                    markingKey=f'1 {c[0]}; 1 fewer DNA differences ({c[1]}%) → less time for mutations to accumulate since the common ancestor.', marks=2)
    t = a[1] / rate
    return dict(stem=f'Assume DNA differences build up at about {rate}% per million years since two species split. Human and {a[0]} DNA differ by {a[1]}%. Estimate how long ago they shared a common ancestor and state one assumption.', answer=f'about {g(t)} million years ago; assumes mutations accumulate at a constant rate',
                markingKey=f'M1 {a[1]} ÷ {rate}; A1 ≈ {g(t)} million years; B1 constant mutation rate (molecular clock) / rate calibrated by fossils.', marks=3)


inquiry('ch01-st1',
        dict(ctx='how the depth of a rock layer in a cliff relates to the complexity of the fossils found in it',
             iv='depth of the rock layer below the cliff top (m)', dv='number of different fossil species (and the most complex body plan) found per 1 m² of rock face',
             cvs=[('area of rock face searched (1 m²)', 'larger areas find more species'), ('search time per sample (20 min)', 'longer searches find more'), ('same identification key', 'identification must be consistent'), ('undisturbed layers only', 'folded or faulted rocks change the order')],
             hyp='If the rock layer is deeper (older), then the fossils will be simpler and fewer types, because life has become more diverse and complex over time through evolution.',
             method='Choose an undisturbed sedimentary cliff with permission; mark sample squares of 1 m² at 2 m depth intervals; search each square for 20 min; photograph and identify fossils with a key; record the number of species and the most complex group; repeat at three locations along the cliff; compare with published dates for the layers.',
             weak=('only one location of the cliff was sampled', 'sample several locations at each depth to make the results representative'),
             safety='beware of falling rocks – wear a hard hat, stay away from overhangs, check tide times and never hammer cliff faces'))
dataset('ch01-st1',
        dict(intro='{who} compared the amino acid sequence of the protein cytochrome c in different species with the human sequence; three databases were used for each species and gave slightly different counts.', iv=('Time since common ancestor with humans', 'million years'), xs=[90, 170, 310, 450, 600],
             dv=('Amino acid differences', ''), f=lambda x: 0.035 * x + 0.5, dp=0, trend='The number of amino acid differences increases with the time since the species shared a common ancestor with humans.',
             why='Mutations in the gene for cytochrome c accumulate over time; the longer two lineages have been separate, the more differences have built up.'))

R.facts('ch01-st2', F(
    terms=[('natural selection', 'the process by which individuals with advantageous inherited variations survive and reproduce more, so those alleles become more common'),
           ('variation', 'differences in characteristics between individuals of the same species'),
           ('mutation', 'a random change in the DNA base sequence, the original source of new alleles'),
           ('selection pressure', 'an environmental factor, such as a predator or disease, that affects survival and reproduction'),
           ('fitness', 'the ability of an organism to survive and pass on its alleles to offspring'),
           ('adaptation', 'an inherited feature that increases an organism’s chance of survival and reproduction in its environment')],
    facts=[('What is the original source of new genetic variation?', 'Mutation', ['Natural selection', 'Competition', 'Adaptation during the lifetime'], 'Sexual reproduction then mixes alleles.'),
           ('Which scientist co-published the theory of natural selection with Charles Darwin in 1858?', 'Alfred Russel Wallace', ['Gregor Mendel', 'Jean-Baptiste Lamarck', 'Louis Pasteur'], 'Both worked independently.'),
           ('Why do populations produce more offspring than the environment can support?', 'It leads to competition, so only some survive to reproduce', ['To make sure all survive', 'Because resources are unlimited', 'To prevent mutation'], 'A key observation of Darwin.'),
           ('In natural selection, what is passed on to offspring?', 'Alleles for the advantageous characteristic', ['Characteristics acquired during life', 'Learned behaviour only', 'Muscles developed by exercise'], 'Only inherited variation is selected.'),
           ('Which is an example of natural selection observed in the wild?', 'Peppered moths becoming darker in sooty industrial areas', ['Giraffes stretching their necks', 'Dog breeders selecting for small size', 'A person getting fitter by training'], 'Dark moths were better camouflaged.')],
    why=[('Explain how the dark form of the peppered moth became more common in industrial England.', 'Soot darkened tree bark; pale moths were seen and eaten by birds more often; dark moths survived and reproduced more, passing on the allele for dark colour, so its frequency increased.'),
         ('Explain why natural selection does not produce a “perfect” organism.', 'It can only act on existing variation; environments change; and features are trade-offs, so organisms are only better suited to current conditions than others.'),
         ('Explain why Lamarck’s idea of inheritance of acquired characteristics was rejected.', 'Changes during a lifetime (e.g. bigger muscles) do not alter the DNA in sex cells, so they are not passed on; experiments failed to show such inheritance.')],
    contrast=[('natural selection', 'selective breeding', 'In natural selection the environment determines which individuals reproduce; in selective (artificial) breeding humans choose which individuals reproduce for desired traits.'),
              ('Darwin’s theory', 'Lamarck’s theory', 'Darwin: random inherited variation exists and the best-suited individuals survive and reproduce; Lamarck: organisms change in response to need and pass on acquired characteristics.')],
    misc=[('Organisms evolve because they need to adapt.', 'Variation arises randomly by mutation; the environment then selects individuals that already have useful variations – there is no intention.'),
          ('Individual organisms evolve during their lifetime.', 'Populations evolve over generations; individuals do not change their alleles.')],
    cases=[('Darwin’s finches on the Galápagos', 'Peter and Rosemary Grant showed that after the 1977 drought, finches with larger, deeper beaks survived better because only large, hard seeds were left; the next generation had larger average beaks.', 'natural selection measured in the wild', 'It showed natural selection can change a population measurably in a single generation.'),
           ('Peppered moth (Biston betularia)', 'Dark moths rose to about 98% of the Manchester population by 1895; after clean-air laws, pale moths became common again.', 'directional selection', 'The change reversing as soot disappeared strengthened the link between camouflage and survival.')],
    evaluate=[('Darwin’s theory of natural selection is “just a theory” and should be taught alongside alternatives in science lessons.', ['students should understand how ideas compete'], ['in science “theory” means a well-tested explanation supported by huge evidence', 'alternatives such as creationism are not testable scientific explanations'], 'Natural selection is a robust scientific theory; non-scientific alternatives belong in other subjects, not science.'),
              ('Darwin deserves more credit than Wallace for the theory of natural selection.', ['Darwin collected decades of evidence and wrote On the Origin of Species'], ['Wallace reached the same idea independently and prompted publication', 'they presented jointly in 1858'], 'Both deserve credit; Darwin’s weight of evidence made the theory widely accepted.')],
    extended=[('A population of rabbits lives on a snowy island. A mutation causes white fur in some individuals. Use the steps of natural selection to explain how the population could become mostly white over many generations.', 'Variation: some rabbits have the white-fur allele from mutation. Overproduction and competition: more offspring than resources. Selection: white rabbits are better camouflaged from predators such as foxes, so more survive. Reproduction: survivors pass on the allele. Over many generations the allele frequency increases until most rabbits are white.', 6)],
))


@R.add('ch01-st2', 'C3', (1, 5), 'numerical')
def allele_freq(rng, slot):
    n0 = rng.choice([200, 400, 500, 800])
    p0 = rng.choice([10, 20, 25, 40])
    k = rng.choice(['pct', 'change'])
    p1 = p0 + rng.choice([15, 20, 30, 35])
    d0, d1 = n0 * p0 // 100, n0 * p1 // 100
    trait = rng.choice(['dark moths', 'beetles with green shells', 'mice with sandy-coloured fur', 'snails with banded shells', 'lizards with long legs'])
    if k == 'pct':
        return dict(stem=f'A sample of {n0} individuals contained {d1} {trait}. Calculate the percentage of {trait} in the population.', answer=f'{p1}%',
                    markingKey=f'M1 {d1} ÷ {n0} × 100; A1 {p1}%.', marks=2)
    return dict(stem=f'In a sample of {n0}, {d0} were {trait}. Twenty generations later a sample of {n0} contained {d1} {trait}. Calculate the change in percentage and explain it using natural selection.', answer=f'from {p0}% to {p1}% – an increase of {p1 - p0} percentage points; the trait gave a survival advantage so more of these individuals reproduced and passed on the allele',
                markingKey=f'M1 {d0}/{n0} = {p0}% and {d1}/{n0} = {p1}%; A1 +{p1 - p0} percentage points; B1 selection pressure gives advantage; B1 survivors reproduce and pass on alleles.', marks=4)


inquiry('ch01-st2',
        dict(ctx='how the colour of a background affects the survival of coloured “prey” (pasta or paper shapes) picked by student “predators”, as a model of natural selection',
             iv='colour of the background (green grass, brown soil, white sheet)', dv='percentage of each colour of prey remaining after 30 s of collecting',
             cvs=[('number of each colour of prey (50)', 'percentages must be comparable'), ('size and shape of prey', 'larger prey are easier to find'), ('collecting time (30 s)', 'longer times collect more'), ('the same predators, picking one at a time', 'technique affects collection')],
             hyp='If the prey colour matches the background, then more of that colour will survive, because predators find camouflaged prey less easily – a model of natural selection.',
             method='Scatter 50 green, 50 brown and 50 white pasta pieces in a 2 m × 2 m area of each background; “predators” pick up one piece at a time for 30 s; count survivors of each colour; “survivors reproduce” – double the survivors and repeat for three generations; calculate percentage of each colour each generation.',
             weak=('predators could see where prey were scattered', 'predators wait outside the area while prey are scattered randomly by another person'),
             safety='check for allergies if using food; watch for trip hazards outdoors'))
dataset('ch01-st2',
        dict(intro='{who} analysed data on the percentage of dark peppered moths caught in traps near an industrial city in different years (three trap sites).', iv=('Year', ''), xs=[1970, 1980, 1990, 2000, 2010],
             dv=('Dark moths', '%'), f=lambda x: 90 * math.exp(-(x - 1970) / 18) + 2, dp=0, trend='The percentage of dark moths fell steadily from about 90% in 1970 to a low value by 2010.',
             why='After clean-air laws, soot no longer darkened tree bark; pale moths were better camouflaged, so birds ate more dark moths and the dark allele became less common.'))

R.facts('ch01-st3', F(
    terms=[('species', 'a group of organisms that can interbreed to produce fertile offspring'),
           ('speciation', 'the formation of new species when populations become reproductively isolated and evolve differently'),
           ('geographical isolation', 'separation of populations by a physical barrier such as a mountain range, river or sea'),
           ('reproductive isolation', 'when two populations can no longer interbreed to produce fertile offspring'),
           ('hybrid', 'the offspring of two different species, often infertile (e.g. a mule)'),
           ('adaptive radiation', 'the rapid evolution of many species from one ancestor, each adapted to a different niche')],
    facts=[('A horse and a donkey produce a mule, which is infertile. What does this show?', 'Horses and donkeys are different species', ['They are the same species', 'Mules are a new species', 'Mules are clones'], 'Offspring must be fertile.'),
           ('What is the first step in allopatric speciation?', 'Populations are separated by a geographical barrier', ['Mutation creates a new species instantly', 'Populations interbreed more', 'All individuals die except one'], 'Then different selection pressures act.'),
           ('Which is an example of behavioural isolation?', 'Two bird populations with different courtship songs no longer mate', ['A river separates two populations', 'Hybrid offspring are infertile', 'Flowers open at different seasons'], 'Mating signals differ.'),
           ('Why did many finch species evolve on the Galápagos Islands?', 'Populations on different islands faced different food sources and were isolated', ['All islands had identical conditions', 'Finches chose to change their beaks', 'Humans introduced them'], 'Adaptive radiation.')],
    why=[('Explain how a river changing course could lead to two new species of snail.', 'The river splits the population (geographical isolation); no gene flow; different mutations and selection pressures on each side change allele frequencies; eventually the populations cannot interbreed – reproductive isolation – two species.'),
         ('Explain why speciation usually takes a very long time.', 'Many genetic changes must accumulate through mutation and selection over many generations before populations are reproductively isolated.'),
         ('Explain why the species concept is difficult to apply to bacteria and fossils.', 'Bacteria reproduce asexually so interbreeding cannot be tested, and fossils cannot be tested for fertile offspring.')],
    contrast=[('geographical isolation', 'reproductive isolation', 'Geographical isolation is a physical barrier separating populations; reproductive isolation is when populations can no longer produce fertile offspring together, which may follow long geographical isolation.'),
              ('a species', 'a population', 'A species is all organisms that can interbreed to produce fertile offspring; a population is the members of one species living in a particular area.')],
    misc=[('A new species forms when one individual has a big mutation.', 'Speciation usually involves many small changes accumulating in an isolated population over many generations.'),
          ('If two animals can mate, they must be the same species.', 'Different species sometimes mate, but the hybrids are usually infertile, as with mules and ligers.')],
    cases=[('Cichlid fish of Lake Victoria', 'Hundreds of cichlid species evolved in the lake in about 15 000 years, with different jaws and colours; female choice of male colour keeps species apart.', 'rapid speciation', 'Shows how sexual selection and different niches drive speciation; introduced Nile perch and pollution have since caused many extinctions.')],
    evaluate=[('Building motorways through wild areas could eventually cause new species to form.', ['roads are barriers that isolate populations of small animals', 'different selection pressures on each side'], ['speciation needs thousands of generations – far longer than road lifetimes', 'small isolated populations are more likely to go extinct than to speciate'], 'Roads can isolate populations, but the main risk is local extinction, not new species; wildlife crossings help maintain gene flow.')],
    extended=[('Using the example of squirrels separated by the Grand Canyon (Abert’s and Kaibab squirrels), explain how geographical isolation can lead to speciation.', 'One original population split by the canyon; no interbreeding (no gene flow); random mutations differ in each population; different environments (vegetation, predators, climate) give different selection pressures; natural selection changes allele frequencies (e.g. Kaibab has white tail and dark belly); over many generations differences accumulate until they could no longer interbreed to produce fertile offspring – separate species (currently considered subspecies, showing the process in progress).', 6)],
))
inquiry('ch01-st3',
        dict(ctx='how isolation affects the variation in shell banding between snail populations on islands of different distances from the mainland',
             iv='distance of the island from the mainland (km)', dv='difference in percentage of banded snails compared with the mainland population',
             cvs=[('sample size (100 snails per site)', 'small samples give unreliable percentages'), ('habitat type sampled (hedgerow)', 'background affects selection'), ('time of year', 'snail activity changes'), ('same classification rule for “banded”', 'judgement must be consistent')],
             hyp='If an island is further from the mainland, then its snail population will differ more in banding, because fewer snails migrate between them (less gene flow), so the populations evolve independently.',
             method='Use published data or field surveys of five islands; collect 100 snails at random from similar hedgerow habitats; classify each as banded or unbanded and release them; calculate percentage banded; compare with the mainland; plot difference against distance.',
             weak=('different habitats were sampled on each island', 'sample the same habitat type everywhere so background colour is controlled'),
             safety='follow conservation rules – return snails unharmed; take care on coastal paths'))
dataset('ch01-st3',
        dict(intro='{who} studied fruit flies kept on two different foods (maltose or starch) for many generations and measured the percentage of matings between flies from the same food group (three trials per generation count).', iv=('Generations apart', ''), xs=[5, 10, 20, 30, 40],
             dv=('Same-group matings', '%'), f=lambda x: 50 + 30 * (1 - math.exp(-x / 15)), dp=0, trend='The percentage of matings within the same food group increases with the number of generations apart, from about 50% towards about 80%.',
             why='Different foods gave different selection pressures; the groups evolved differences (e.g. in scent or behaviour) and began to prefer their own group – early reproductive isolation, the first stage of speciation.'))

R.facts('ch01-st4', F(
    terms=[('classification', 'the arrangement of organisms into groups based on shared features and evolutionary relationships'),
           ('binomial name', 'the two-part scientific name of a species: genus then species, e.g. Homo sapiens'),
           ('taxonomic hierarchy', 'the ranks domain, kingdom, phylum, class, order, family, genus, species'),
           ('dichotomous key', 'a key that identifies organisms using a series of questions, each with two choices'),
           ('domain', 'the highest rank: Archaea, Bacteria and Eukarya'),
           ('phylogenetic tree', 'a branching diagram showing evolutionary relationships between species')],
    facts=[('What is the correct order of taxonomic ranks from largest to smallest?', 'Kingdom, phylum, class, order, family, genus, species', ['Species, genus, family, order, class, phylum, kingdom', 'Kingdom, class, phylum, family, order, species, genus', 'Phylum, kingdom, order, class, genus, family, species'], '“King Philip Came Over For Good Soup.”'),
           ('In the name Panthera leo, what does Panthera represent?', 'The genus', ['The species', 'The family', 'The kingdom'], 'The genus is written first with a capital.'),
           ('Why do scientists use binomial names rather than common names?', 'They are unique and understood internationally', ['They are easier to pronounce', 'They describe the colour', 'They change every year'], 'Common names vary by language and region.'),
           ('Which three domains are used in modern classification?', 'Archaea, Bacteria and Eukarya', ['Plants, animals and fungi', 'Prokaryotes, viruses and eukaryotes', 'Vertebrates, invertebrates and plants'], 'Proposed by Carl Woese in 1990.'),
           ('Two species in the same family must also be in the same…', 'order', ['genus', 'species', 'nothing else'], 'Each rank is inside the one above.')],
    why=[('Explain why classification systems have changed over time.', 'New evidence, especially DNA sequences and electron microscopy, revealed relationships that differed from those based on appearance, so groups were revised.'),
         ('Explain why a dichotomous key must use features that do not vary within a species.', 'If a feature varies (e.g. size or colour in individuals), the same species could be sent down different branches and misidentified.'),
         ('Explain why classification based on evolutionary relationships is useful.', 'It predicts shared features (e.g. biochemistry for drug discovery) and shows how species are related through common ancestors.')],
    contrast=[('artificial classification', 'natural (phylogenetic) classification', 'Artificial classification uses convenient features such as habitat or colour; natural classification groups organisms by evolutionary relationships using many shared features and DNA.'),
              ('a genus', 'a species', 'A genus is a group of closely related species; a species is a single group of organisms that can interbreed to produce fertile offspring.')],
    misc=[('Organisms that look similar must be closely related.', 'Unrelated organisms can look similar due to convergent evolution, e.g. sharks and dolphins; DNA reveals true relationships.'),
          ('Bacteria and archaea are basically the same.', 'Archaea differ from bacteria in membrane lipids, cell walls and genes, and are as different from bacteria as we are; they are a separate domain.')],
    cases=[('Carl Linnaeus and Systema Naturae (1735)', 'Linnaeus introduced binomial names and a hierarchy of groups; his system is still used, although groups are now based on evolution and DNA.', 'naming and classifying', 'A shared naming system allowed scientists worldwide to communicate precisely about species.'),
           ('Carl Woese and the three domains (1977–1990)', 'By comparing ribosomal RNA sequences, Woese found that some “bacteria” were very different and proposed the domain Archaea.', 'molecular classification', 'Molecular data overturned the two-group prokaryote/eukaryote view of life.')],
    evaluate=[('DNA barcoding should replace dichotomous keys for identifying species.', ['accurate even for similar-looking species, larvae or fragments', 'objective'], ['needs laboratory equipment and databases', 'keys are cheap, quick and usable in the field'], 'DNA barcoding is powerful for research and difficult cases, but keys remain useful for fieldwork.')],
    extended=[('Write a dichotomous key to separate five animals: spider, butterfly, earthworm, snail, crab. Explain why each question uses a fixed, observable feature.', 'e.g. 1 Legs present? yes → 2; no → 4. 2 Eight legs? yes → spider; no → 3. 3 Wings? yes → butterfly; no (10 legs, hard shell) → crab. 4 Shell present? yes → snail; no → earthworm. Fixed features (number of legs, presence of wings/shell) do not vary between individuals of a species or with age, so identification is reliable; avoid size or colour.', 6)],
))


@R.add('ch01-st4', 'C2', (1, 3), 'mcq')
def taxon(rng, slot):
    sp = [('Homo sapiens', 'human'), ('Panthera leo', 'lion'), ('Panthera tigris', 'tiger'), ('Canis lupus', 'wolf'), ('Felis catus', 'cat'), ('Canis familiaris', 'domestic dog')]
    a, b = rng.sample(sp, 2)
    same = a[0].split()[0] == b[0].split()[0]
    corr = 'the same genus' if same else 'different genera'
    return mcq(rng, f'The {a[1]} is {a[0]} and the {b[1]} is {b[0]}. What do the names tell you?', f'They are in {corr}', [f'They are in {x}' for x in ['the same species', 'different kingdoms', 'the same genus', 'different genera'] if x != corr][:3],
               f'B1 the first word is the genus – they are in {corr}.')


inquiry('ch01-st4',
        dict(ctx='how the number of features in a dichotomous key affects how accurately students identify leaf species',
             iv='number of questions (features) in the key (3, 5, 7)', dv='percentage of 20 leaf samples correctly identified',
             cvs=[('the same 20 leaf samples', 'some leaves are harder to identify'), ('time allowed (10 min)', 'more time may improve accuracy'), ('students of similar experience', 'practice affects accuracy'), ('clear, fixed features in each key', 'vague features confuse users')],
             hyp='If the key has more questions, then accuracy will increase, because each step uses a specific feature and fewer species are separated at each step.',
             method='Write three keys for the same 8 tree species using 3, 5 and 7 features; give groups of 10 students one key each and the same 20 leaves; allow 10 min; mark identifications against the correct answers; calculate mean percentage correct for each key.',
             weak=('the same students used all three keys and learned the leaves', 'use different but similar groups for each key, or change the leaf samples'),
             safety='some leaves (e.g. yew) are toxic – wash hands; avoid plants with thorns or irritant sap'))
dataset('ch01-st4',
        dict(intro='{who} compared the percentage of shared DNA between humans and other species in the same and different taxonomic groups (kingdom only = 1 … same genus = 7; three published estimates each).', iv=('Number of shared taxonomic ranks', ''), xs=[1, 3, 4, 5, 6],
             dv=('DNA similarity', '%'), f=lambda x: 55 + 7.0 * x, dp=0, trend='DNA similarity increases the more taxonomic ranks two species share.',
             why='Species that share lower ranks (family, genus) share a more recent common ancestor, so there has been less time for DNA differences to accumulate.'))

R.facts('ch01-st5', F(
    terms=[('antibiotic', 'a medicine that kills bacteria or stops them growing, but does not affect viruses'),
           ('antibiotic resistance', 'the ability of bacteria to survive an antibiotic that would normally kill them'),
           ('MRSA', 'methicillin-resistant Staphylococcus aureus, a bacterium resistant to many antibiotics'),
           ('selective advantage', 'a feature that makes an organism more likely to survive and reproduce in particular conditions'),
           ('superbug', 'a bacterium resistant to several antibiotics')],
    facts=[('Why should antibiotics not be prescribed for a cold?', 'Colds are caused by viruses, which antibiotics do not affect', ['Colds are too mild', 'Antibiotics make colds worse', 'Colds are caused by fungi'], 'Unnecessary use increases resistance.'),
           ('Why should patients complete the full course of antibiotics?', 'To kill all the bacteria so resistant survivors do not multiply', ['To use up the medicine', 'To make the bacteria stronger', 'To prevent viruses'], 'Stopping early leaves the most resistant bacteria.'),
           ('How do new antibiotic-resistant strains first appear?', 'By random mutation in bacterial DNA', ['Bacteria choose to become resistant', 'Antibiotics cause the mutation directly', 'Viruses make bacteria resistant'], 'Selection then increases them.'),
           ('Why does antibiotic resistance spread quickly?', 'Bacteria reproduce very rapidly, so resistant bacteria soon form large populations', ['Bacteria live for many years', 'Antibiotics spread it', 'Resistance is caused by temperature'], 'Some divide every 20 minutes.'),
           ('Which practice in farming contributes to antibiotic resistance?', 'Routinely giving antibiotics to healthy livestock', ['Rotating crops', 'Using organic fertiliser', 'Planting hedgerows'], 'Banned in the EU since 2006 for growth promotion.')],
    why=[('Explain how a population of bacteria becomes resistant to an antibiotic.', 'Random mutation gives some bacteria resistance; the antibiotic kills non-resistant bacteria; resistant ones survive and reproduce rapidly with no competition, passing on the resistance gene; the population becomes mostly resistant.'),
         ('Explain why antibiotic resistance is described as evolution in action.', 'It shows natural selection changing the allele frequency of a population over a short time that we can observe.'),
         ('Explain why it is hard to develop new antibiotics.', 'It is expensive and slow; few new chemical classes have been found; bacteria quickly evolve resistance, and drug companies earn little from short courses.')],
    contrast=[('antibiotic resistance', 'immunity', 'Antibiotic resistance is a property of bacteria that survive a drug; immunity is a property of the host’s immune system that protects against a pathogen.'),
              ('antibiotics', 'antivirals', 'Antibiotics target bacterial structures such as cell walls and ribosomes; antivirals stop viruses replicating inside host cells.')],
    misc=[('People become resistant to antibiotics.', 'It is the bacteria that become resistant, not the person.'),
          ('Antibiotics cause bacteria to mutate into resistant forms.', 'Mutations happen randomly; antibiotics select those that are already resistant.')],
    cases=[('Alexander Fleming’s warning (1945)', 'In his Nobel lecture, Fleming warned that underdosing with penicillin could make bacteria resistant; resistant Staphylococcus was common in hospitals within a decade.', 'predicting resistance', 'His warning remains relevant: misuse of antibiotics drives resistance.'),
           ('Global antimicrobial resistance (2019)', 'A major study estimated about 1.27 million deaths in 2019 were directly caused by antibiotic-resistant infections.', 'scale of the problem', 'The WHO lists resistance among the top global public-health threats.')],
    evaluate=[('Doctors should prescribe antibiotics only after a laboratory test confirms a bacterial infection.', ['avoids unnecessary use, slowing resistance', 'chooses the correct antibiotic'], ['tests take time – delays could be dangerous in severe infections', 'not all clinics have laboratories'], 'Testing should be standard where possible, with rapid tests and exceptions for serious illness.'),
              ('Farmers should be banned from using antibiotics in animals.', ['farm use contributes to resistant bacteria reaching humans', 'better hygiene and vaccines can replace routine use'], ['sick animals need treatment for welfare', 'could increase costs and food prices'], 'Routine preventive use should be banned, but treatment of sick animals under veterinary control should continue.')],
    extended=[('Antibiotic resistance has been called a “slow pandemic”. Explain how resistance develops by natural selection and evaluate three strategies to reduce it.', 'Mutation → some resistant; antibiotic kills others; survivors multiply; resistance spreads, including by plasmid transfer between bacteria. Strategies: reducing prescriptions for viral infections (effective, needs public education); finishing courses and correct doses (reduces survivors); hospital hygiene/handwashing (reduces spread of MRSA); banning routine farm use; funding new antibiotics and phage therapy (slow, expensive). Combined global approach needed.', 8)],
))


@R.add('ch01-st5', 'C3', (1, 5), 'numerical')
def bact_growth(rng, slot):
    k = rng.choice(['double', 'zone'] if slot.d >= 2 else ['double'])
    if k == 'double':
        t = rng.choice([20, 30])
        h = rng.choice([2, 3, 4, 5])
        n0 = rng.choice([1, 10, 100])
        n = n0 * 2 ** (h * 60 // t)
        return dict(stem=f'A bacterium divides every {t} minutes. Starting with {n0} resistant bacteria, how many would there be after {h} hours if conditions stay ideal?', answer=f'{n:,}',
                    markingKey=f'M1 number of divisions = {h} × 60 ÷ {t} = {h * 60 // t}; M1 {n0} × 2^{h * 60 // t}; A1 {n:,}.', marks=3)
    d = rng.choice([8, 10, 12, 14, 18, 22])
    r = d / 2
    a = math.pi * r * r
    return dict(stem=f'An antibiotic disc on an agar plate of bacteria produced a clear zone of diameter {d} mm. Calculate the area of the clear zone (A = πr²) and explain what a smaller zone would show.', answer=f'{g(a)} mm²; a smaller zone shows the bacteria are less sensitive (more resistant) to the antibiotic',
                markingKey=f'M1 r = {g(r)} mm; M1 π × {g(r)}²; A1 {g(a)} mm²; B1 smaller clear zone → antibiotic less effective / bacteria more resistant.', marks=4)


inquiry('ch01-st5',
        dict(ctx='how the type of antibiotic affects the growth of a harmless bacterium (E. coli K-12) on agar plates',
             iv='antibiotic on the paper disc (four types, same concentration)', dv='diameter of the clear zone around each disc after 48 h at 25 °C',
             cvs=[('concentration and volume of antibiotic on each disc', 'more antibiotic diffuses further'), ('incubation temperature (25 °C)', 'safe temperature that limits pathogen growth'), ('same agar depth and bacterial lawn', 'affects diffusion and growth'), ('incubation time (48 h)', 'zones change over time')],
             hyp='If antibiotic A is used, then the clear zone will be largest, because the bacterium is most sensitive to it, so the antibiotic kills it at lower concentrations as it diffuses outwards.',
             method='Using aseptic technique, spread E. coli K-12 evenly on nutrient agar; place four antibiotic discs and a control disc soaked in sterile water with sterile forceps; tape the lid with two strips (do not seal fully); incubate upside down at 25 °C for 48 h; measure zone diameters with a ruler; repeat with three plates.',
             weak=('the lid was sealed all round, allowing anaerobic pathogens to grow', 'use only two strips of tape, incubate at 25 °C and never open plates after incubation'),
             safety='aseptic technique: disinfect benches, flame loops, never open incubated plates, autoclave all cultures before disposal'))
dataset('ch01-st5',
        dict(intro='{who} analysed hospital data on the percentage of Staphylococcus aureus samples resistant to an antibiotic in years after the drug was introduced (three hospitals).', iv=('Years after introduction', ''), xs=[2, 4, 6, 8, 10],
             dv=('Resistant samples', '%'), f=lambda x: 80 / (1 + math.exp(-(x - 6) / 1.2)), dp=0, trend='The percentage of resistant samples was low at first, then rose rapidly between years 4 and 8 and began to level off.',
             why='Each use of the antibiotic killed sensitive bacteria and selected resistant ones; resistant bacteria multiplied and spread between patients, so resistance became common.'))


# =============================================================================================
# ch02 Ecology: Populations and Nutrient Cycles
# =============================================================================================
R.facts('ch02-st1', F(
    terms=[('carrying capacity', 'the maximum population size that an environment can support indefinitely'),
           ('limiting factor', 'a factor in short supply that restricts population growth, such as food, space, light or nesting sites'),
           ('exponential growth', 'growth in which the population increases by the same proportion in each time interval, giving a J-shaped curve'),
           ('sigmoid growth curve', 'an S-shaped curve with lag, exponential and plateau (stationary) phases'),
           ('density-dependent factor', 'a factor whose effect increases as population density increases, e.g. competition, disease'),
           ('predator–prey cycle', 'linked rises and falls in predator and prey populations, with predator peaks lagging behind prey peaks')],
    facts=[('In a sigmoid growth curve, why does the population level off?', 'Limiting factors such as food and space reduce the birth rate or increase the death rate', ['All individuals stop reproducing', 'Mutations stop', 'The population has no limiting factors'], 'Births ≈ deaths at carrying capacity.'),
           ('Which is a density-independent factor?', 'A sudden flood', ['Competition for food', 'Spread of disease', 'Predation'], 'Affects populations regardless of size.'),
           ('In a predator–prey graph, why does the predator peak come after the prey peak?', 'Predator numbers rise only after there is plenty of prey to feed their young', ['Predators eat plants first', 'Prey eat predators', 'The graph is drawn wrongly'], 'There is a time lag.'),
           ('What is happening in the lag phase of a bacterial growth curve?', 'Cells are adjusting and making enzymes before dividing rapidly', ['The population is dying', 'Resources have run out', 'The population is at carrying capacity'], 'Growth is slow.')],
    why=[('Explain why human population growth has been almost exponential for the last 200 years.', 'Medicine, sanitation and increased food production reduced death rates (especially infant mortality) while birth rates stayed high for a long time.'),
         ('Explain why introducing rabbits to Australia led to a population explosion.', 'There were few predators, little competition, plenty of food and suitable habitat, so the limiting factors on growth were removed.'),
         ('Explain why a population can briefly overshoot the carrying capacity.', 'Resources take time to run out; individuals born when food was plentiful continue to consume until shortage increases deaths, then the population falls back.')],
    contrast=[('exponential growth', 'logistic (sigmoid) growth', 'Exponential growth has no limits and accelerates (J-curve); logistic growth slows as limiting factors act and levels off at the carrying capacity (S-curve).'),
              ('density-dependent factors', 'density-independent factors', 'Density-dependent factors (competition, disease, predation) have a bigger effect in crowded populations; density-independent factors (floods, frost) affect the population whatever its size.')],
    misc=[('Populations always grow until every individual has died of starvation.', 'Most populations stabilise around carrying capacity because birth and death rates balance.'),
          ('Predators control prey numbers but prey have no effect on predators.', 'Prey availability strongly controls predator numbers; the populations affect each other.')],
    cases=[('Snowshoe hare and lynx records (Hudson’s Bay Company)', 'Fur-trapping records from 1845–1935 show hare and lynx numbers rising and falling in about 10-year cycles, with lynx peaks after hare peaks.', 'predator–prey cycles', 'Long-term data revealed the cycle; later studies showed hare food supply also plays a part.'),
           ('Reindeer on St Matthew Island (1944–1966)', '29 reindeer introduced to a predator-free island grew to about 6000 by 1963, ate the lichen, and crashed to 42 after a hard winter.', 'overshoot and crash', 'It shows what can happen when a population exceeds carrying capacity with no predators.')],
    evaluate=[('Culling deer is the best way to protect woodland from overgrazing.', ['quickly reduces numbers below carrying capacity', 'protects young trees and biodiversity'], ['ethical objections to killing animals', 'reintroducing predators (e.g. wolves, lynx) or fencing could be more natural'], 'Culling is often necessary where natural predators are absent, but long-term solutions may include predator reintroduction.')],
    extended=[('Sketch and describe a sigmoid population growth curve for yeast in a flask, explaining each phase in terms of limiting factors.', 'Lag phase: few cells, adjusting, little division. Exponential (log) phase: plenty of glucose, cells divide rapidly, numbers double regularly. Stationary phase: glucose runs low, ethanol and waste build up, births = deaths – carrying capacity. Death phase (in a closed flask): food exhausted, toxins high, deaths exceed births.', 6)],
))


@R.add('ch02-st1', 'C3', (1, 5), 'numerical')
def pop_growth(rng, slot):
    k = rng.choice(['rate', 'double', 'pct'] if slot.d >= 2 else ['rate', 'pct'])
    if k == 'rate':
        a = rng.choice([200, 450, 800, 1200])
        b = a + rng.choice([300, 600, 900, 1500])
        t = rng.choice([3, 5, 6, 10])
        return dict(stem=f'A population of {rng.choice(["aphids", "rabbits", "duckweed plants", "voles"])} increased from {a} to {b} in {t} weeks. Calculate the mean rate of population growth.', answer=f'{g((b - a) / t)} per week',
                    markingKey=f'M1 ({b} − {a}) ÷ {t}; A1 {g((b - a) / t)} individuals per week.', marks=2)
    if k == 'double':
        n0 = rng.choice([50, 100, 500])
        d = rng.choice([2, 3, 4])
        t = rng.choice([8, 12, 16])
        n = n0 * 2 ** (t // d)
        return dict(stem=f'A population of {n0} yeast cells doubles every {d} hours during the exponential phase. Calculate the population after {t} hours, and state why this cannot continue indefinitely.', answer=f'{n:,}; glucose runs out and ethanol builds up (limiting factors)',
                    markingKey=f'M1 doublings = {t} ÷ {d} = {t // d}; M1 {n0} × 2^{t // d}; A1 {n:,}; B1 limiting factor named.', marks=4)
    a = rng.choice([1200, 2500, 4000])
    p = rng.choice([-35, -20, 15, 40])
    b = round(a * (1 + p / 100))
    return dict(stem=f'A bird population changed from {a} to {b} after a harsh winter or a good breeding season. Calculate the percentage change.', answer=f'{p:+d}%',
                markingKey=f'M1 ({b} − {a}) ÷ {a} × 100; A1 {p:+d}%.', marks=2)


inquiry('ch02-st1',
        dict(ctx='how the initial concentration of glucose affects the maximum population of yeast in a culture',
             iv='glucose concentration of the culture medium (1, 2, 4, 6, 8 %)', dv='maximum yeast cell count per mm³ (haemocytometer) over 5 days',
             cvs=[('starting number of yeast cells', 'more cells reach the plateau sooner'), ('temperature (25 °C)', 'affects growth rate'), ('volume of culture (50 cm³)', 'affects total resources'), ('sampling method (shake before sampling)', 'cells settle at the bottom')],
             hyp='If the glucose concentration is higher, then the maximum population will be higher, because more food raises the carrying capacity until another factor such as ethanol becomes limiting.',
             method='Prepare 50 cm³ of each glucose solution with the same nutrients; add 1 cm³ of yeast suspension; incubate at 25 °C; each day shake and take a 0.1 cm³ sample; count cells with a haemocytometer under a microscope; repeat with three flasks per concentration; plot growth curves and find the maximum.',
             weak=('the flasks were not shaken before sampling', 'swirl each flask the same number of times before taking every sample'),
             safety='use aseptic technique; dispose of cultures after disinfection; handle glass slides carefully'))
dataset('ch02-st1',
        dict(intro='{who} counted duckweed fronds in a beaker of pond water every 4 days (three beakers).', iv=('Time', 'days'), xs=[4, 8, 12, 16, 20],
             dv=('Number of fronds', ''), f=lambda x: 400 / (1 + 39 * math.exp(-0.35 * x)), dp=0, trend='The number of fronds increases slowly, then rapidly, and then levels off – a sigmoid (S-shaped) growth curve.',
             why='At first there are plenty of resources and few plants; growth becomes exponential; then space, light and mineral ions become limiting, and the population approaches the carrying capacity.'))

R.facts('ch02-st2', F(
    terms=[('trophic level', 'the position of an organism in a food chain (producer, primary consumer, secondary consumer …)'),
           ('biomass', 'the dry mass of living material in organisms'),
           ('pyramid of biomass', 'a diagram showing the biomass at each trophic level'),
           ('pyramid of energy', 'a diagram showing the energy flowing through each trophic level per unit area per year; always pyramid-shaped'),
           ('net primary productivity', 'the rate at which producers store energy as biomass after their own respiration'),
           ('ecological efficiency', 'the percentage of energy at one trophic level that is transferred to the next')],
    facts=[('Why is a pyramid of energy never inverted?', 'Energy is lost at each trophic level, so less is available to each level above', ['Energy increases at each level', 'Energy is recycled', 'Producers have the least energy'], 'Second law of thermodynamics.'),
           ('How can a pyramid of biomass be inverted in the ocean?', 'Phytoplankton reproduce so fast that a small standing biomass supports a larger mass of zooplankton', ['Fish make their own food', 'Energy increases up the chain', 'Phytoplankton are heavier than whales'], 'Biomass is measured at one moment.'),
           ('Which process releases most of the energy “lost” between trophic levels?', 'Respiration, as heat', ['Photosynthesis', 'Decomposition only', 'Excretion of oxygen'], 'Also undigested material and uneaten parts.'),
           ('Why is dry mass used to measure biomass?', 'Water content varies a lot and is not useful energy', ['Dry mass is easier to see', 'Wet mass is always zero', 'Water is biomass'], 'Samples are dried at about 80 °C to constant mass.')],
    why=[('Explain why there are rarely more than five trophic levels in a food chain.', 'Only about 10% of energy is passed on each step, so after four or five transfers too little energy remains to support a population.'),
         ('Explain why mammals and birds have lower ecological efficiency than reptiles.', 'They use much energy in respiration to maintain a constant body temperature, so less is converted to biomass for the next level.'),
         ('Explain why measuring biomass destroys the organisms and how ecologists reduce this problem.', 'Organisms must be dried to constant mass; ecologists take small samples and use estimates from known wet-to-dry ratios.')],
    contrast=[('a pyramid of numbers', 'a pyramid of biomass', 'A pyramid of numbers counts individuals at each level and can be any shape (one tree supports many insects); a pyramid of biomass shows the dry mass at each level and is usually pyramid-shaped.'),
              ('gross primary productivity', 'net primary productivity', 'GPP is the total energy captured by producers in photosynthesis; NPP is what is left after producers’ own respiration and is available to consumers.')],
    misc=[('Energy is lost from the ecosystem when it is lost from a trophic level.', 'Energy lost from a level is transferred to the surroundings as heat or to decomposers; it is not destroyed.'),
          ('Herbivores convert all the plant material they eat into their own biomass.', 'Much is egested undigested and much energy is used in respiration; only a small fraction becomes herbivore biomass.')],
    cases=[('Silver Springs, Florida (Odum, 1957)', 'Howard Odum measured energy flow through every trophic level of a spring ecosystem, finding that each level received only about 10–20% of the previous one’s energy.', 'quantifying energy flow', 'It was one of the first complete energy budgets of an ecosystem and established the energy pyramid idea.')],
    evaluate=[('Insect farming should replace beef as a major protein source.', ['insects convert feed to biomass much more efficiently (cold-blooded)', 'much less land, water and greenhouse gas'], ['cultural reluctance to eat insects', 'allergy risks; welfare and scale-up questions'], 'Insects are a much more efficient protein source and could reduce environmental impact, though acceptance will take time.')],
    extended=[('Use energy-flow ideas to explain why a field of wheat can feed more people if they eat the bread than if the wheat is fed to cattle and they eat the beef. Include a calculation with 10% efficiency per step.', 'If wheat stores 100 000 kJ: eating wheat directly gives ~10 000 kJ to humans (10% of it assimilated, simplified); feeding cattle first gives ~10 000 kJ to cattle and only ~1000 kJ to humans. The extra trophic level loses ~90% through respiration (heat), movement, undigested material; so about 10× more people can be fed from crops.', 6)],
))


@R.add('ch02-st2', 'C3', (1, 5), 'numerical')
def eco_eff(rng, slot):
    k = rng.choice(['eff', 'loss', 'npp'] if slot.d >= 2 else ['eff'])
    a = rng.choice([87000, 24000, 15000, 50000])
    p = rng.choice([8, 10, 12, 16])
    b = a * p / 100
    if k == 'eff':
        return dict(stem=f'Producers in a grassland store {a} kJ/m² per year, and primary consumers store {g(b)} kJ/m² per year. Calculate the ecological efficiency of the transfer.', answer=f'{p}%',
                    markingKey=f'M1 {g(b)} ÷ {a} × 100; A1 {p}%.', marks=2)
    if k == 'loss':
        eat = rng.choice([3000, 4000, 5000])
        fae = rng.choice([1200, 1600, 2000])
        resp = rng.choice([900, 1200, 1500])
        grow = eat - fae - resp
        return dict(stem=f'A cow eats grass containing {eat} kJ. It loses {fae} kJ in faeces and {resp} kJ in respiration. Calculate the energy available for growth and the percentage efficiency of conversion to biomass.', answer=f'{grow} kJ; {g(grow / eat * 100)}%',
                    markingKey=f'M1 {eat} − {fae} − {resp} = {grow} kJ; M1 {grow} ÷ {eat} × 100; A1 {g(grow / eat * 100)}%.', marks=3)
    gpp = rng.choice([20000, 30000, 36000])
    r = rng.choice([40, 50, 60])
    return dict(stem=f'Plants in a forest have a gross primary productivity of {gpp} kJ/m² per year and use {r}% of it in respiration. Calculate the net primary productivity.', answer=f'{g(gpp * (100 - r) / 100)} kJ/m² per year',
                markingKey=f'M1 respiration = {g(gpp * r / 100)}; M1 NPP = GPP − R; A1 {g(gpp * (100 - r) / 100)} kJ/m² per year.', marks=3)


inquiry('ch02-st2',
        dict(ctx='how the mass of food eaten by mealworms affects the increase in their biomass',
             iv='mass of bran provided per container (2, 4, 6, 8, 10 g)', dv='increase in total mass of 20 mealworms over 2 weeks',
             cvs=[('number and starting mass of mealworms (20)', 'larger mealworms grow differently'), ('temperature (25 °C)', 'affects respiration and growth'), ('moisture (same slice of carrot each week)', 'water affects survival'), ('container size', 'crowding affects growth')],
             hyp='If more bran is available, then biomass will increase more, but only about 10–20% of the bran eaten will become mealworm biomass, because much energy is used in respiration or egested.',
             method='Weigh 20 mealworms and place in a container with a known mass of bran; keep at 25 °C in the dark; after 2 weeks reweigh mealworms and remaining bran (sieve out frass); calculate mass eaten and gain in mass; calculate % conversion; repeat with three containers per mass.',
             weak=('the frass (faeces) was weighed with the leftover bran', 'sieve the bran to separate frass before weighing'),
             safety='wash hands after handling animals and bran; treat animals humanely and return them to the culture'))
dataset('ch02-st2',
        dict(intro='{who} measured the energy stored per square metre at each trophic level of a lake ecosystem in three different years.', iv=('Trophic level', ''), xs=[1, 2, 3, 4, 5],
             dv=('Energy stored', 'kJ/m² per year'), f=lambda x: 30000 * 0.1 ** (x - 1), dp=1, trend='The energy stored decreases by roughly a factor of ten at each higher trophic level.',
             why='About 90% of energy is used in respiration, lost as heat, or passes to decomposers in waste and dead material, so only about 10% becomes biomass at the next level.'))

R.facts('ch02-st3', F(
    terms=[('carbon cycle', 'the movement of carbon between the atmosphere, living organisms, oceans and rocks'),
           ('carbon sink', 'a reservoir that absorbs more carbon than it releases, e.g. oceans, forests, peat'),
           ('decomposition', 'the breakdown of dead organic matter by bacteria and fungi, releasing CO₂ by respiration'),
           ('fossilisation', 'the slow conversion of dead organisms into fossil fuels under heat and pressure over millions of years'),
           ('carbon sequestration', 'the long-term capture and storage of carbon dioxide'),
           ('ocean acidification', 'the decrease in ocean pH caused by absorption of extra atmospheric CO₂')],
    facts=[('Which process removes carbon dioxide from the atmosphere?', 'Photosynthesis', ['Respiration', 'Combustion', 'Decomposition'], 'Carbon is fixed into glucose.'),
           ('Which process returns carbon from dead leaves to the atmosphere?', 'Respiration by decomposers', ['Photosynthesis', 'Fossilisation', 'Transpiration'], 'Bacteria and fungi.'),
           ('Why do waterlogged peat bogs store carbon?', 'Lack of oxygen slows decomposition', ['Peat photosynthesises', 'Water absorbs carbon dioxide', 'Peat burns slowly'], 'Dead plants accumulate.'),
           ('What is the main way carbon in fossil fuels enters the atmosphere?', 'Combustion', ['Photosynthesis', 'Decomposition', 'Feeding'], 'It releases CO₂ stored for millions of years.'),
           ('Approximately what is the current atmospheric CO₂ concentration?', 'About 420 ppm', ['About 280 ppm', 'About 4%', 'About 21%'], 'Pre-industrial level was about 280 ppm.')],
    why=[('Explain why atmospheric CO₂ concentration rises in winter and falls in summer in the Northern Hemisphere.', 'In summer, photosynthesis by plants exceeds respiration, removing CO₂; in winter many plants lose leaves and photosynthesis falls while respiration and decomposition continue.'),
         ('Explain how marine organisms with shells take part in the long-term carbon cycle.', 'They use carbon to make calcium carbonate shells; after death shells form sediments that become limestone, locking carbon away for millions of years.'),
         ('Explain why burning fossil fuels upsets the balance of the carbon cycle.', 'It releases carbon that was locked away for millions of years far faster than photosynthesis and oceans can absorb it, so CO₂ accumulates in the atmosphere.')],
    contrast=[('respiration', 'photosynthesis in the carbon cycle', 'Respiration releases CO₂ to the atmosphere from all organisms; photosynthesis removes CO₂ and fixes it into organic compounds in producers.'),
              ('a carbon source', 'a carbon sink', 'A carbon source releases more carbon than it absorbs (e.g. burning forests, power stations); a sink absorbs more than it releases (e.g. growing forests, oceans).')],
    misc=[('Planting trees permanently removes carbon dioxide.', 'Trees store carbon while alive, but release it when they die and decompose or burn unless the wood is preserved.'),
          ('Carbon atoms are created by plants.', 'Carbon atoms are not created or destroyed; they are recycled between compounds and reservoirs.')],
    cases=[('The Keeling Curve (Mauna Loa, 1958–present)', 'Charles Keeling began measuring atmospheric CO₂ on Mauna Loa in Hawaii; the record shows a yearly zig-zag and a rise from about 315 ppm to over 420 ppm.', 'long-term monitoring', 'It is the clearest direct evidence of rising atmospheric CO₂ from human activities.')],
    evaluate=[('Carbon capture and storage at power stations is the best way to tackle rising CO₂.', ['captures up to 90% of CO₂ from large sources', 'allows use of existing infrastructure'], ['expensive and energy-intensive', 'risk of leaks; storage sites limited', 'may delay switching to renewables'], 'CCS can help for hard-to-decarbonise industries, but cutting emissions with renewables is cheaper and more certain.')],
    extended=[('Draw (describe) the carbon cycle, naming four processes that move carbon, and explain how human activities have changed it.', 'Photosynthesis (atmosphere → plants), feeding (plants → animals), respiration (organisms → atmosphere), decomposition (dead matter → decomposers → atmosphere), combustion (fossil fuels/biomass → atmosphere), fossilisation and ocean dissolution. Humans: burning fossil fuels and deforestation add CO₂ faster than sinks absorb; less photosynthesis; CO₂ rose from 280 to over 420 ppm, enhancing the greenhouse effect and acidifying oceans.', 8)],
))


@R.add('ch02-st3', 'C3', (1, 5), 'numerical')
def co2_rise(rng, slot):
    k = rng.choice(['rate', 'pct'])
    y1, y2 = rng.choice([(1960, 2020), (1980, 2020), (1990, 2023), (2000, 2024)])
    c = {1960: 317, 1980: 339, 1990: 354, 2000: 370, 2020: 414, 2023: 421, 2024: 424}
    if k == 'rate':
        r = (c[y2] - c[y1]) / (y2 - y1)
        return dict(stem=f'Atmospheric CO₂ at Mauna Loa was {c[y1]} ppm in {y1} and {c[y2]} ppm in {y2}. Calculate the mean rate of increase in ppm per year.', answer=f'{g(r)} ppm per year',
                    markingKey=f'M1 ({c[y2]} − {c[y1]}) ÷ ({y2} − {y1}); A1 {g(r)} ppm/year.', marks=2)
    p = (c[y2] - 280) / 280 * 100
    return dict(stem=f'Pre-industrial CO₂ concentration was about 280 ppm. In {y2} it was {c[y2]} ppm. Calculate the percentage increase and name two human activities responsible.', answer=f'{g(p)}%; burning fossil fuels and deforestation',
                markingKey=f'M1 ({c[y2]} − 280) ÷ 280 × 100; A1 {g(p)}%; B1 two of: burning fossil fuels, deforestation, cement production, agriculture.', marks=3)


inquiry('ch02-st3',
        dict(ctx='how light intensity affects the uptake of carbon dioxide by pondweed, measured with hydrogencarbonate indicator',
             iv='distance of the lamp from the tube (10, 20, 30, 40 cm)', dv='colour change of hydrogencarbonate indicator after 1 hour, measured as absorbance in a colorimeter',
             cvs=[('length of pondweed (5 cm)', 'more leaf area takes up more CO₂'), ('volume of indicator (10 cm³)', 'affects colour change'), ('temperature (water heat shield)', 'lamps heat the tubes'), ('control tube with no pondweed', 'shows colour change is due to the plant')],
             hyp='If light intensity is higher, then more CO₂ will be removed and the indicator will turn more purple, because photosynthesis is faster and exceeds respiration.',
             method='Put 10 cm³ of red hydrogencarbonate indicator (equilibrated with air) into tubes; add 5 cm³ of pondweed and seal; place tubes at each distance from an LED lamp behind a water heat shield; include control tubes; after 1 hour measure absorbance at 550 nm; repeat three times; plot absorbance against light intensity (1/d²).',
             weak=('one tube was wrapped in foil but not counted as a dark control', 'include both a dark tube (respiration only) and a no-plant tube as controls'),
             safety='keep water away from the lamp and mains sockets'))
dataset('ch02-st3',
        dict(intro='{who} measured the CO₂ concentration in the air inside a closed greenhouse at different times of day (three days).', iv=('Time of day', 'h'), xs=[4, 8, 12, 16, 20],
             dv=('CO₂ concentration', 'ppm'), f=lambda x: 420 + 80 * math.cos((x - 4) / 24 * 2 * math.pi), dp=0, trend='CO₂ concentration is highest before dawn, falls through the morning to a minimum in the afternoon and rises again in the evening.',
             why='At night only respiration occurs, adding CO₂; in daylight photosynthesis is faster than respiration, so plants take CO₂ from the air.'))

R.facts('ch02-st4', F(
    terms=[('nitrogen fixation', 'the conversion of nitrogen gas into ammonia or nitrates by bacteria (or lightning)'),
           ('nitrifying bacteria', 'bacteria that convert ammonium compounds into nitrites and then nitrates'),
           ('denitrifying bacteria', 'bacteria in waterlogged soil that convert nitrates back into nitrogen gas'),
           ('root nodules', 'swellings on the roots of legumes containing nitrogen-fixing bacteria'),
           ('transpiration', 'the loss of water vapour from leaves, part of the water cycle'),
           ('precipitation', 'water falling from clouds as rain, snow or hail')],
    facts=[('Why do plants need nitrates?', 'To make amino acids and proteins', ['To make glucose', 'To absorb light', 'To make cellulose only'], 'Deficiency causes yellow leaves.'),
           ('Which plants have nitrogen-fixing bacteria in root nodules?', 'Legumes such as peas, beans and clover', ['Grasses', 'Conifers', 'Mosses'], 'Farmers use them in crop rotation.'),
           ('What do denitrifying bacteria do?', 'Convert nitrates into nitrogen gas', ['Convert nitrogen gas into nitrates', 'Make ammonia from protein', 'Fix carbon dioxide'], 'Common in waterlogged, anaerobic soils.'),
           ('Which process moves water from the ocean into the atmosphere?', 'Evaporation', ['Condensation', 'Precipitation', 'Infiltration'], 'Powered by the Sun.'),
           ('Why does ploughing and draining fields help soil fertility?', 'It aerates the soil, helping nitrifying bacteria and reducing denitrification', ['It adds nitrogen gas', 'It kills all bacteria', 'It stops nitrification'], 'Nitrifiers need oxygen.')],
    why=[('Explain how nitrogen in a dead leaf becomes available to another plant.', 'Decomposers break down proteins into ammonium compounds; nitrifying bacteria convert ammonium to nitrites and then nitrates; plant roots absorb nitrates by active transport.'),
         ('Explain why farmers grow clover or beans in crop rotation.', 'Bacteria in root nodules fix atmospheric nitrogen into ammonium compounds; when the crop is ploughed in, the soil gains nitrates for the next crop, so less fertiliser is needed.'),
         ('Explain why deforestation can reduce local rainfall.', 'Trees transpire large volumes of water vapour that forms clouds; fewer trees means less water vapour and less precipitation downwind.')],
    contrast=[('nitrogen fixation', 'nitrification', 'Nitrogen fixation turns N₂ gas into ammonia/ammonium; nitrification turns ammonium into nitrites then nitrates.'),
              ('nitrifying bacteria', 'denitrifying bacteria', 'Nitrifying bacteria (aerobic) make nitrates available to plants; denitrifying bacteria (anaerobic) turn nitrates back into N₂ gas, reducing soil fertility.')],
    misc=[('Plants take nitrogen gas straight from the air.', 'Plants cannot use N₂ gas; they absorb nitrates or ammonium from the soil, made by bacteria or added as fertiliser.'),
          ('The water cycle only involves evaporation and rain.', 'It also includes transpiration, condensation, infiltration, run-off, groundwater flow and storage in ice and organisms.')],
    cases=[('The Haber process and the nitrogen cycle', 'Industrial fixation of nitrogen into ammonia now roughly doubles the natural rate of nitrogen fixation; about half the world’s food depends on it.', 'human impact on nutrient cycles', 'Fertiliser run-off causes eutrophication and nitrous oxide emissions, showing a trade-off between food and environment.')],
    evaluate=[('Organic farming without artificial fertilisers can feed the world.', ['healthier soils, less pollution and eutrophication', 'legumes and manure recycle nitrogen'], ['yields are typically 20–25% lower', 'would need more land, possibly causing deforestation'], 'Organic methods can reduce pollution, but feeding everyone would probably also need efficient use of some artificial fertiliser and less food waste.')],
    extended=[('Explain the roles of four different types of bacteria in the nitrogen cycle and suggest how waterlogged soil affects plant growth.', 'Nitrogen-fixing (free-living and in legume nodules): N₂ → ammonium. Decomposers (putrefying): proteins/urea → ammonium. Nitrifying: ammonium → nitrites → nitrates (aerobic). Denitrifying: nitrates → N₂ (anaerobic). Waterlogged soil: little oxygen – nitrifiers inhibited, denitrifiers thrive – nitrates fall – plants become nitrogen deficient (yellow leaves, poor growth); roots also lack oxygen for respiration.', 6)],
))
inquiry('ch02-st4',
        dict(ctx='how the mass of nitrate fertiliser added affects the growth of duckweed',
             iv='mass of nitrate fertiliser per dm³ of water (0, 0.1, 0.2, 0.4, 0.8 g)', dv='number of duckweed fronds after 14 days',
             cvs=[('starting number of fronds (10)', 'more plants give more growth'), ('light intensity and duration', 'needed for photosynthesis'), ('temperature', 'affects growth rate'), ('volume of water (200 cm³)', 'affects nutrient concentration')],
             hyp='If more nitrate is added, then the duckweed will grow more fronds, because nitrates are needed to make amino acids and proteins for new cells, up to a point where another factor limits growth.',
             method='Set up beakers with 200 cm³ distilled water plus other nutrients and each mass of nitrate; add 10 fronds; keep under the same lamp at 20 °C for 14 days; count fronds every 2 days; repeat with three beakers per concentration; plot final count against nitrate mass.',
             weak=('tap water was used, which already contains nitrate', 'use distilled water with a nitrate-free nutrient solution'),
             safety='fertiliser is an irritant – wear gloves; wash hands after handling pond plants'))
dataset('ch02-st4',
        dict(intro='{who} measured the nitrate concentration of a stream at different distances downstream from a field fertilised in spring (three samples each).', iv=('Distance downstream', 'm'), xs=[0, 100, 200, 400, 800],
             dv=('Nitrate concentration', 'mg/dm³'), f=lambda x: 4 + 30 * math.exp(-x / 250), dp=1, trend='The nitrate concentration is highest next to the field and decreases with distance downstream.',
             why='Nitrates from fertiliser leach and run off into the stream; downstream they are diluted and taken up by algae and plants, and some are denitrified.'))


# =============================================================================================
# ch03 Human Impact on Ecosystems
# =============================================================================================
R.facts('ch03-st1', F(
    terms=[('biodiversity', 'the variety of life in an area: genetic, species and ecosystem diversity'),
           ('species richness', 'the number of different species in an area'),
           ('species evenness', 'how evenly the individuals are distributed among the species present'),
           ('Simpson’s diversity index', 'a measure of biodiversity that combines richness and evenness: D = 1 − Σ(n/N)²'),
           ('indicator species', 'a species whose presence or absence shows the level of pollution or environmental quality'),
           ('endemic species', 'a species found naturally in only one geographic area')],
    facts=[('Which two features of a community are combined in a diversity index?', 'Species richness and species evenness', ['Population size and biomass', 'Temperature and light', 'Predators and prey'], 'Both matter.'),
           ('A stream contains many mayfly and stonefly larvae. What does this suggest?', 'The water is clean and well-oxygenated', ['The water is heavily polluted', 'The water has no oxygen', 'There are no plants'], 'They are indicator species.'),
           ('Which indicator suggests heavily polluted water with low oxygen?', 'Many sludge worms and rat-tailed maggots', ['Many mayfly nymphs', 'Many stonefly larvae', 'Brown trout'], 'They tolerate low oxygen.'),
           ('Which ecosystem type has the highest species richness on land?', 'Tropical rainforest', ['Desert', 'Tundra', 'Boreal forest'], 'Warm, wet, stable, many niches.'),
           ('What does a Simpson’s index (1 − Σ(n/N)²) close to 1 show?', 'High diversity', ['Low diversity', 'Only one species', 'A polluted habitat'], 'Close to 0 = low diversity.')],
    why=[('Explain why a habitat with high biodiversity is usually more stable.', 'Many species and complex food webs mean that if one species declines, others can fill its role; populations are less likely to crash.'),
         ('Explain why species richness alone can give a misleading picture of biodiversity.', 'Two habitats can have the same number of species but one may be dominated by a single species; evenness must also be considered.'),
         ('Explain why lichens are used to monitor air pollution.', 'Many lichen species are sensitive to sulfur dioxide; the number and type of lichens present indicate the air quality.')],
    contrast=[('species richness', 'species evenness', 'Richness is how many species are present; evenness is how equal the numbers of each species are.'),
              ('genetic diversity', 'species diversity', 'Genetic diversity is the variety of alleles within a species; species diversity is the variety of species in a community.')],
    misc=[('A field of one crop with millions of plants has high biodiversity.', 'A monoculture has very low biodiversity: one species dominates and few others are present.'),
          ('Biodiversity is just the number of animals in an area.', 'Biodiversity includes plants, fungi and microorganisms, genetic variety and ecosystem variety.')],
    cases=[('Kick sampling for the Biological Monitoring Working Party (BMWP) score', 'Freshwater invertebrates are sampled by kicking the stream bed into a net; each family scores points for its pollution sensitivity and the total indicates water quality.', 'measuring biodiversity in practice', 'It is a cheap, standardised method used by environmental agencies to monitor rivers.')],
    evaluate=[('Biodiversity should be protected mainly because of its value to humans (e.g. medicines, food).', ['provides medicines (e.g. aspirin from willow), food crops, pollination worth billions', 'easier to persuade governments'], ['species have intrinsic value regardless of usefulness', 'we cannot predict which species will be useful'], 'Economic arguments help, but biodiversity is also worth protecting for its own sake and for unknown future value.')],
    extended=[('Describe how you would compare the biodiversity of a mown school lawn and an unmown meadow, and explain how you would process the data.', 'Lay out grids; use random coordinates; place 10 × 0.25 m² quadrats in each habitat; identify and count each species (or % cover) using a key; calculate species richness and Simpson’s index D = 1 − Σ(n/N)² for each habitat; compare; repeat on different days; expect the meadow to have higher diversity because mowing removes tall species and allows a few grasses to dominate.', 6)],
))


@R.add('ch03-st1', 'C3', (2, 5), 'numerical')
def simpson(rng, slot):
    k = rng.randrange(3)
    counts = rng.choice([[10, 10, 10, 10], [25, 10, 3, 2], [12, 8, 6, 4], [30, 5, 5], [6, 6, 6, 6, 6], [18, 9, 3]])
    N = sum(counts)
    D = 1 - sum((n / N) ** 2 for n in counts)
    sp = ['daisy', 'clover', 'dandelion', 'buttercup', 'plantain'][:len(counts)]
    lst = ', '.join(f'{s} {n}' for s, n in zip(sp, counts))
    return dict(stem=f'A quadrat survey found: {lst}. Calculate Simpson’s diversity index using D = 1 − Σ(n/N)².', answer=f'D = {D:.2f}',
                markingKey=f'M1 N = {N}; M1 Σ(n/N)² = {" + ".join(f"({n}/{N})²" for n in counts)} = {1 - D:.3f}; A1 D = {D:.2f}.', marks=3)


inquiry('ch03-st1',
        dict(ctx='how the distance downstream from a sewage outlet affects the biodiversity of freshwater invertebrates',
             iv='distance downstream from the outlet (0, 50, 100, 200, 400 m)', dv='Simpson’s diversity index of invertebrates from a 1-minute kick sample',
             cvs=[('sampling time (1 min) and net size', 'longer sampling catches more'), ('depth and flow rate of sampling site (riffles)', 'different microhabitats have different species'), ('same identification key and observer', 'identification must be consistent'), ('same day and weather', 'rain changes flow and pollution levels')],
             hyp='If the distance from the sewage outlet increases, then the diversity index will increase, because organic pollution is diluted and broken down, so oxygen levels recover and more sensitive species can survive.',
             method='At each distance, choose a riffle of similar depth; kick the stream bed upstream of a net for 1 min; empty into a white tray; identify and count invertebrates with a key; return them; calculate Simpson’s index; repeat three samples at each site; measure dissolved oxygen.',
             weak=('samples were taken in pools at some sites and riffles at others', 'sample the same type of microhabitat (riffles) at every site'),
             safety='wear waders and gloves; check depth and flow; cover cuts (risk of Weil’s disease); work in groups'))
dataset('ch03-st1',
        dict(intro='{who} counted the number of lichen species on tree trunks at different distances from a city centre (three trees at each distance).', iv=('Distance from city centre', 'km'), xs=[1, 3, 5, 8, 12],
             dv=('Lichen species per tree', ''), f=lambda x: 2 + 1.2 * x, dp=0, trend='The number of lichen species increases with distance from the city centre.',
             why='Many lichens are sensitive to air pollutants such as sulfur dioxide and nitrogen oxides, which are most concentrated near the city centre.'))

R.facts('ch03-st2', F(
    terms=[('greenhouse effect', 'the trapping of infrared radiation emitted by Earth’s surface by gases in the atmosphere, keeping Earth warm'),
           ('enhanced greenhouse effect', 'the increased warming caused by extra greenhouse gases from human activities'),
           ('deforestation', 'the large-scale clearing of forests, often for farming, logging or building'),
           ('methane', 'a powerful greenhouse gas released by cattle, rice paddies, landfill and leaking gas wells'),
           ('bioaccumulation', 'the build-up of a persistent substance in an organism faster than it is removed'),
           ('climate change', 'long-term changes in temperature and weather patterns, now largely caused by human activities')],
    facts=[('Which wavelengths of radiation do greenhouse gases absorb and re-emit?', 'Infrared', ['Ultraviolet', 'Visible light only', 'X-rays'], 'Earth emits infrared.'),
           ('Which two effects of deforestation increase atmospheric CO₂?', 'Burning trees releases CO₂ and fewer trees remain to absorb it', ['It increases photosynthesis', 'It adds oxygen', 'It causes acid rain only'], 'Also decomposition of remains.'),
           ('Which gas has a greater warming effect per molecule: CO₂ or methane?', 'Methane', ['Carbon dioxide', 'They are the same', 'Neither absorbs infrared'], 'About 28× over 100 years.'),
           ('Which is an expected consequence of global warming?', 'Rising sea levels from melting ice and thermal expansion', ['Thicker Arctic sea ice', 'Fewer heatwaves', 'Lower sea levels'], 'Low-lying areas flood.'),
           ('Why are mercury levels highest in large predatory fish such as tuna?', 'Mercury bioaccumulates and is magnified up the food chain', ['Large fish absorb it from air', 'Mercury is made by fish', 'Small fish have none'], 'Biomagnification.')],
    why=[('Explain why the greenhouse effect is essential for life but the enhanced greenhouse effect is a problem.', 'Without natural greenhouse gases Earth would average about −18 °C; extra gases from human activity trap more infrared, raising temperatures and disrupting climate.'),
         ('Explain how deforestation can reduce biodiversity beyond the area cut down.', 'Remaining forest is fragmented into small patches that cannot support large animals; edges dry out; soil erodes into rivers; local rainfall decreases.'),
         ('Explain why plastic pollution harms marine food chains.', 'Animals eat or are tangled in plastic; microplastics are eaten by plankton and pass up food chains, carrying toxic chemicals that accumulate.')],
    contrast=[('the greenhouse effect', 'ozone depletion', 'The greenhouse effect involves gases trapping infrared and warming Earth; ozone depletion is the thinning of the stratospheric ozone layer by CFCs, letting more UV reach the surface.'),
              ('weather', 'climate', 'Weather is the day-to-day state of the atmosphere; climate is the average weather over 30 years or more.')],
    misc=[('Global warming is caused by the hole in the ozone layer.', 'They are separate problems; global warming is caused by greenhouse gases trapping infrared, not by extra UV through the ozone hole.'),
          ('A cold winter proves global warming is not happening.', 'Climate is a long-term average; individual cold events do not change the global upward trend.')],
    cases=[('Amazon deforestation and the tipping point', 'Since 1970 about 17% of the Amazon rainforest has been lost; scientists warn that at 20–25% loss parts could turn into savanna as rainfall decreases.', 'deforestation and climate', 'Losing the Amazon would release huge amounts of carbon and destroy a major biodiversity hotspot.'),
           ('Minamata disease (Japan, 1950s)', 'A factory released mercury into Minamata Bay; it bioaccumulated in fish and shellfish and poisoned thousands of people who ate them.', 'bioaccumulation', 'It led to the 2013 Minamata Convention to control mercury pollution worldwide.')],
    evaluate=[('Richer countries should pay poorer countries to protect their rainforests.', ['rainforests benefit the whole world (carbon, biodiversity)', 'richer countries caused most historic emissions'], ['payments may not reach local people or prevent illegal logging', 'sovereignty concerns'], 'Payment schemes are fair and useful if transparent and supporting local communities.'),
              ('Individual actions, such as eating less meat, can make a real difference to climate change.', ['food is about a quarter of emissions; diets matter', 'collective action shifts markets'], ['energy, industry and policy changes have far larger effects'], 'Individual actions help and influence others, but large-scale policy change is essential.')],
    extended=[('Explain how the enhanced greenhouse effect leads to global warming and evaluate the evidence that humans are responsible.', 'Sun’s short-wave radiation passes through atmosphere; Earth emits infrared; CO₂, methane and water vapour absorb and re-emit infrared, warming lower atmosphere; burning fossil fuels and deforestation raised CO₂ from 280 to over 420 ppm. Evidence: Keeling curve, ice-core CO₂–temperature correlation, isotopic signature of fossil carbon, warming pattern (stratosphere cooling), models only match with human emissions. Correlation alone is not causation, but multiple independent lines agree – strong scientific consensus.', 8)],
))


@R.add('ch03-st2', 'C3', (1, 5), 'numerical')
def biomag(rng, slot):
    k = rng.choice(['factor', 'area'])
    if k == 'factor':
        w = rng.choice([0.00005, 0.0001, 0.0002])
        f1, f2, f3 = rng.choice([10, 20]), rng.choice([5, 10]), rng.choice([10, 15])
        top = w * f1 * f2 * f3
        return dict(stem=f'A pesticide is present in water at {w} ppm. Its concentration increases {f1}× in plankton, {f2}× from plankton to small fish, and {f3}× from small fish to birds. Calculate the concentration in the birds and name this process.', answer=f'{g(top)} ppm; biomagnification',
                    markingKey=f'M1 {w} × {f1} × {f2} × {f3}; A1 {g(top)} ppm; B1 biomagnification (bioaccumulation along the food chain).', marks=3)
    a = rng.choice([1200, 3000, 5000, 8000])
    y = rng.choice([5, 8, 10])
    tot = rng.choice([40000, 60000, 100000])
    return dict(stem=f'A forest of {tot} km² loses {a} km² per year. Calculate the percentage lost after {y} years at this rate.', answer=f'{g(a * y / tot * 100)}%',
                markingKey=f'M1 {a} × {y} = {a * y} km²; M1 ÷ {tot} × 100; A1 {g(a * y / tot * 100)}%.', marks=3)


inquiry('ch03-st2',
        dict(ctx='how the concentration of carbon dioxide in a sealed bottle affects the temperature rise when it is illuminated by a lamp',
             iv='percentage of CO₂ in the bottle (air ≈ 0.04%, 10%, 25%, 50%, 100%)', dv='temperature rise in 15 minutes measured with a digital thermometer',
             cvs=[('distance from lamp and lamp power', 'affects energy received'), ('size and colour of bottle', 'affects absorption'), ('starting temperature', 'affects heat loss'), ('position of thermometer (shaded)', 'direct light on the probe gives false readings')],
             hyp='If the CO₂ concentration is higher, then the temperature will rise more, because CO₂ absorbs and re-emits infrared radiation, modelling the greenhouse effect.',
             method='Fill identical clear bottles with air or CO₂ mixtures (from a cylinder or reaction of acid and carbonate measured with a gas syringe); seal with a thermometer probe through the lid, shaded from direct light; place 30 cm from a 100 W infrared lamp; record temperature every minute for 15 min; repeat three times; plot rise against % CO₂.',
             weak=('the probe was in direct light so measured the probe heating, not the gas', 'shade the probe tip with a small foil cover'),
             safety='infrared lamps get very hot; CO₂ in high concentration can cause drowsiness – ventilate the room'))
dataset('ch03-st2',
        dict(intro='{who} used global data to compare atmospheric CO₂ concentration with average global temperature anomaly in different years (three data sets).', iv=('CO₂ concentration', 'ppm'), xs=[320, 340, 360, 390, 420],
             dv=('Temperature anomaly', '°C'), f=lambda x: 0.01 * (x - 300), dp=2, trend='The global temperature anomaly increases as CO₂ concentration increases – a positive correlation.',
             why='CO₂ is a greenhouse gas that absorbs and re-emits infrared radiation from Earth’s surface; more CO₂ enhances the greenhouse effect. Correlation alone does not prove causation, but physics and other evidence support a causal link.'))

R.facts('ch03-st3', F(
    terms=[('conservation', 'the protection and careful management of species, habitats and natural resources'),
           ('in situ conservation', 'protecting species in their natural habitat, e.g. national parks'),
           ('ex situ conservation', 'protecting species outside their habitat, e.g. zoos, seed banks'),
           ('sustainable resource use', 'using resources in a way that meets present needs without preventing future generations meeting theirs'),
           ('fishing quota', 'a limit on the mass of fish that can be caught, to keep fish stocks sustainable'),
           ('rewilding', 'restoring ecosystems by reintroducing species and allowing natural processes to return')],
    facts=[('Which is an example of ex situ conservation?', 'Storing seeds in the Svalbard Global Seed Vault', ['Creating a national park', 'Protecting a coral reef', 'Banning hunting in a forest'], 'Outside the natural habitat.'),
           ('Why do fishing nets have a minimum mesh size?', 'So young fish escape and can reproduce', ['To catch more fish', 'To make nets lighter', 'To catch only large sharks'], 'Maintains breeding stocks.'),
           ('What is the purpose of captive breeding programmes?', 'To increase numbers of endangered species for possible release', ['To make animals tame', 'To create new species', 'To sell animals'], 'e.g. California condor.'),
           ('Why are wildlife corridors created between habitats?', 'They allow animals to move between fragments, maintaining gene flow', ['To stop animals moving', 'To build roads', 'To grow crops'], 'Reduces inbreeding.'),
           ('Which is a sustainable forestry practice?', 'Replanting trees as they are harvested', ['Clear-felling without replanting', 'Burning forests for farmland', 'Harvesting only the youngest trees'], 'Forest Stewardship Council certification.')],
    why=[('Explain why small, isolated populations are at greater risk of extinction.', 'Low genetic diversity means fewer alleles to adapt to disease or change; inbreeding increases harmful recessive conditions; random events can wipe them out.'),
         ('Explain why seed banks are important for food security.', 'They store genetic diversity of crops and wild relatives, which can be used to breed varieties resistant to new diseases or climate.'),
         ('Explain why fishing quotas are difficult to enforce.', 'Oceans are vast and shared; illegal fishing and discarding of unwanted catch are hard to monitor; quotas may be set too high for political reasons.')],
    contrast=[('in situ conservation', 'ex situ conservation', 'In situ protects species in their natural habitats with all their ecological interactions; ex situ protects them outside, in zoos or seed banks, useful when habitats are destroyed.'),
              ('conservation', 'preservation', 'Conservation allows sustainable use of resources with management; preservation aims to keep areas untouched by humans.')],
    misc=[('Saving one charismatic species, like the panda, saves the ecosystem.', 'Protecting panda habitat also protects many species (umbrella species), but whole ecosystems need wider management.'),
          ('Zoos are the best way to save endangered species.', 'Zoos help, but protecting wild habitats is usually more effective and keeps species’ natural behaviours and interactions.')],
    cases=[('Grey wolves reintroduced to Yellowstone (1995)', 'Wolves reduced elk overgrazing, allowing willows and aspen to recover, which helped beavers, songbirds and river banks.', 'trophic cascades and rewilding', 'Top predators can restore whole ecosystems.'),
           ('Collapse of the Grand Banks cod fishery (1992)', 'Overfishing off Newfoundland caused cod stocks to collapse by over 95%; a moratorium put 30 000 people out of work and stocks have recovered only slowly.', 'unsustainable resource use', 'It showed the need for science-based quotas set before collapse.')],
    evaluate=[('Marine protected areas where all fishing is banned are the best way to restore fish stocks.', ['fish populations and size increase rapidly inside reserves', 'spillover benefits nearby fisheries'], ['loss of income for local fishing communities', 'hard to enforce over large areas'], 'No-take zones are highly effective when well enforced and combined with support for fishing communities.'),
              ('Rewilding large areas of farmland in Europe would be beneficial.', ['increases biodiversity and carbon storage', 'reduces flooding, tourism income'], ['reduces food production', 'conflicts with farmers over predators such as wolves'], 'Rewilding less productive land can be very beneficial if planned with local communities.')],
    extended=[('A rare orchid survives only in one small nature reserve. Evaluate three conservation strategies that could be used to protect it.', 'In situ protection (fencing, managing grazing, controlling invasive species) – keeps natural pollinators but vulnerable to one disaster. Seed banking/tissue culture (ex situ) – insurance against extinction, preserves genetic diversity, but plants may lose adaptation. Creating new populations in suitable habitats/corridors – spreads risk, increases gene flow but needs suitable sites and pollinators. Best: combination, with monitoring and public education.', 6)],
))


@R.add('ch03-st3', 'C3', (1, 5), 'numerical')
def mark_recapture(rng, slot):
    m = rng.choice([30, 40, 50, 60])
    n2 = rng.choice([40, 50, 60])
    r = rng.choice([4, 5, 6, 8, 10])
    N = m * n2 / r
    return dict(stem=f'Ecologists caught and marked {m} fish in a pond and released them. A week later they caught {n2} fish, of which {r} were marked. Estimate the population size (N = number marked × number in second sample ÷ number recaptured).', answer=f'{g(N)} fish',
                markingKey=f'M1 {m} × {n2} ÷ {r}; A1 {g(N)}; (assumes marks not lost, no births/deaths/migration, random mixing).', marks=2)


inquiry('ch03-st3',
        dict(ctx='how the mesh size of a fishing net affects the proportion of juvenile fish caught, using a model with different-sized beads',
             iv='mesh size of the model net (5, 10, 15, 20 mm)', dv='percentage of small “juvenile” beads (8 mm) among the beads retained',
             cvs=[('number of each bead size (100 small, 100 large)', 'proportion depends on what is available'), ('sweeping method and number of sweeps', 'affects how many are caught'), ('container size', 'density affects capture'), ('same person sweeping', 'technique varies')],
             hyp='If the mesh size is larger, then a smaller percentage of juvenile beads will be caught, because small beads pass through the holes – modelling how mesh regulations let young fish escape and breed.',
             method='Mix 100 small and 100 large beads in a tray of water; sweep a frame net of each mesh size through the tray five times; count small and large beads retained; return beads and repeat three times per mesh; calculate the percentage of small beads in the catch.',
             weak=('beads stuck in the mesh were counted inconsistently', 'agree a rule: only beads lifted out of the water in the net count as caught'),
             safety='mop up water spills; small beads are a choking hazard'))
dataset('ch03-st3',
        dict(intro='{who} used survey data to record the population of a rare butterfly in a nature reserve in years after grazing management began (three transects).', iv=('Years after management began', ''), xs=[1, 2, 4, 6, 8],
             dv=('Butterflies counted per transect', ''), f=lambda x: 120 / (1 + 7 * math.exp(-0.6 * x)), dp=0, trend='The butterfly count increased slowly at first, then rapidly, and began to level off after about 6 years.',
             why='Grazing kept grass short, allowing the caterpillars’ food plants to grow; as the population recovered it approached the carrying capacity of the reserve.'))


# =============================================================================================
# ch04 Biotechnology
# =============================================================================================
R.facts('ch04-st1', F(
    terms=[('genetic engineering', 'changing the genome of an organism by inserting a gene from another organism'),
           ('restriction enzyme', 'an enzyme that cuts DNA at a specific base sequence, often leaving sticky ends'),
           ('DNA ligase', 'an enzyme that joins pieces of DNA together'),
           ('plasmid', 'a small circular loop of DNA in bacteria, used as a vector'),
           ('vector', 'something used to carry a gene into a cell, such as a plasmid or virus'),
           ('recombinant DNA', 'DNA that combines genetic material from two different sources'),
           ('sticky ends', 'short single-stranded overhangs left by some restriction enzymes that pair with complementary sticky ends')],
    facts=[('Which enzyme is used to cut the human insulin gene out of DNA?', 'A restriction enzyme', ['DNA ligase', 'Amylase', 'Protease'], 'It cuts at a specific sequence.'),
           ('Why is the same restriction enzyme used to cut both the plasmid and the gene?', 'To produce matching sticky ends that can pair up', ['To make the DNA longer', 'To kill the bacteria', 'To join the DNA'], 'Complementary base pairing.'),
           ('Which enzyme joins the gene into the plasmid?', 'DNA ligase', ['Restriction enzyme', 'Lipase', 'DNA polymerase only'], 'Seals the sugar-phosphate backbone.'),
           ('Why are antibiotic-resistance marker genes often included in plasmids?', 'So bacteria that have taken up the plasmid can be identified', ['To make bacteria grow faster', 'To make insulin', 'To cut DNA'], 'Only transformed bacteria survive on antibiotic agar.'),
           ('What is produced by genetically engineered bacteria for people with type 1 diabetes?', 'Human insulin', ['Glucagon', 'Antibiotics', 'Haemoglobin'], 'Since 1982.')],
    why=[('Explain why bacteria are useful for producing human proteins.', 'They reproduce rapidly, use the same genetic code, are easy to grow in fermenters and have plasmids that can carry new genes.'),
         ('Explain why genetically engineered insulin is better than insulin from pigs.', 'It is identical to human insulin, so fewer allergic reactions; supply is unlimited and not affected by animal supply or religious objections.'),
         ('Explain why sticky ends make recombinant DNA possible.', 'The single-stranded overhangs from the same restriction enzyme have complementary base sequences, so they hydrogen-bond together before ligase seals them.')],
    contrast=[('a restriction enzyme', 'DNA ligase', 'A restriction enzyme cuts DNA at specific sequences; DNA ligase joins DNA fragments together.'),
              ('a plasmid', 'a chromosome', 'A plasmid is a small circular extra piece of DNA in bacteria that can transfer between cells; a chromosome is the main DNA carrying most of the organism’s genes.')],
    misc=[('Genetic engineering creates new genes from nothing.', 'It moves existing genes between organisms (or edits them); it does not create genes from nothing.'),
          ('Bacteria that make human insulin are part human.', 'They carry one human gene; the rest of their DNA is bacterial.')],
    cases=[('Recombinant insulin (Genentech, 1978–1982)', 'Scientists inserted synthetic human insulin genes into E. coli; in 1982 Humulin became the first genetically engineered medicine approved for humans.', 'genetic engineering in medicine', 'It replaced animal insulin and showed that GM bacteria could make human proteins safely at scale.'),
           ('CRISPR-Cas9 (Doudna and Charpentier, 2012)', 'A bacterial defence system was adapted to cut DNA at almost any chosen sequence, allowing precise gene editing.', 'new tools for genetic engineering', 'Nobel Prize 2020; used to develop treatments for sickle-cell disease, but raises ethical questions about editing human embryos.')],
    evaluate=[('Gene editing with CRISPR should be allowed to correct genetic diseases in human embryos.', ['could eliminate severe inherited diseases (e.g. Huntington’s)', 'prevents suffering in future generations'], ['changes are inherited by all descendants – unknown long-term effects', 'off-target edits', 'could lead to “designer babies” and inequality'], 'Research should continue, but heritable embryo editing should wait for proven safety and broad social agreement.')],
    extended=[('Describe the steps used to produce human insulin using genetically modified bacteria.', 'Identify insulin gene; cut it out with a restriction enzyme (sticky ends); cut plasmid with the same enzyme; mix and join with DNA ligase → recombinant plasmid; insert into bacteria (transformation, e.g. heat shock); grow on antibiotic agar to select transformed bacteria (marker gene); culture in large fermenters with controlled pH, temperature, nutrients, oxygen; extract and purify insulin.', 6)],
))


@R.add('ch04-st1', 'C3', (1, 4), 'numerical')
def transform_eff(rng, slot):
    col = rng.choice([40, 80, 120, 250])
    ug = rng.choice([0.1, 0.2, 0.5])
    return dict(stem=f'In a bacterial transformation, {col} colonies grew on antibiotic agar after using {ug} µg of plasmid DNA. Calculate the transformation efficiency in colonies per µg and explain why only transformed bacteria grow.', answer=f'{g(col / ug)} colonies per µg; only bacteria with the plasmid carry the antibiotic-resistance marker gene',
                markingKey=f'M1 {col} ÷ {ug}; A1 {g(col / ug)} per µg; B1 marker gene gives resistance – untransformed bacteria are killed.', marks=3)


inquiry('ch04-st1',
        dict(ctx='how the temperature of the heat-shock step affects the number of E. coli K-12 cells that take up a plasmid carrying a fluorescence gene',
             iv='heat-shock temperature (37, 42, 47, 52 °C for 50 s)', dv='number of glowing colonies on antibiotic agar after 24 h',
             cvs=[('mass of plasmid DNA added', 'more plasmid gives more transformants'), ('volume and density of bacterial suspension', 'more cells give more colonies'), ('heat-shock time (50 s)', 'length of shock affects uptake'), ('incubation temperature and time', 'affects colony growth')],
             hyp='If the heat-shock temperature is about 42 °C, then the most colonies will form, because the heat changes membrane permeability enough to let plasmids in without killing too many cells.',
             method='Mix ice-cold competent cells with the same mass of plasmid in calcium chloride; hold on ice 10 min; heat shock at the set temperature for 50 s; return to ice; add broth and recover for 30 min; spread equal volumes on antibiotic agar; incubate at 30 °C for 24 h; count fluorescent colonies under UV; repeat three times.',
             weak=('the timing of the heat shock varied by several seconds', 'use a timer and a water bath at the exact temperature; transfer all tubes together in a rack'),
             safety='use a non-pathogenic strain; aseptic technique; UV light can damage eyes – use UV-protective glasses; autoclave all waste'))
dataset('ch04-st1',
        dict(intro='{who} counted transformed colonies when different masses of plasmid DNA were used (three plates each).', iv=('Mass of plasmid', 'ng'), xs=[10, 20, 40, 80, 160],
             dv=('Colonies', ''), f=lambda x: 300 * x / (x + 60), dp=0, trend='The number of colonies increases with mass of plasmid, but by less at higher masses, levelling off.',
             why='More plasmid means more bacteria can take one up; at high masses the number of competent cells able to take up DNA becomes limiting.'))

R.facts('ch04-st2', F(
    terms=[('genetically modified organism (GMO)', 'an organism whose genome has been changed by genetic engineering'),
           ('Bt crop', 'a crop modified with a gene from Bacillus thuringiensis to produce a toxin that kills insect pests'),
           ('herbicide-resistant crop', 'a crop modified to survive spraying with a specific weedkiller'),
           ('Golden Rice', 'rice genetically modified to produce beta-carotene (provitamin A) in the grain'),
           ('gene flow', 'the transfer of genes between populations, e.g. by pollen from GM crops to wild relatives'),
           ('monoculture', 'growing one crop variety over a large area')],
    facts=[('What is the purpose of Golden Rice?', 'To reduce vitamin A deficiency', ['To increase protein', 'To kill insect pests', 'To resist drought only'], 'Vitamin A deficiency causes blindness.'),
           ('How does Bt cotton reduce pesticide use?', 'The plant makes its own insecticidal toxin', ['It repels all animals', 'It grows faster than pests', 'It is poisonous to humans'], 'The toxin targets certain caterpillars.'),
           ('What is a concern about herbicide-resistant crops?', 'Weeds may evolve resistance and more herbicide may be used', ['They cannot be harvested', 'They are always toxic', 'They cannot reproduce'], '“Superweeds”.'),
           ('Which is a potential ecological risk of GM crops?', 'Pollen transferring modified genes to wild relatives', ['Crops turning into animals', 'Plants losing chlorophyll', 'Soil becoming radioactive'], 'Gene flow.')],
    why=[('Explain why GM crops resistant to pests can increase yields.', 'Less of the crop is eaten or damaged, so more is harvested; farmers also save the cost of spraying.'),
         ('Explain why insects may evolve resistance to Bt crops.', 'Random mutations give some insects resistance; they survive on Bt crops and reproduce, so resistance spreads – which is why refuges of non-Bt crops are planted.'),
         ('Explain why some people oppose GM foods even though no harm to health has been shown.', 'Concerns about long-term ecological effects, corporate control of seeds and patents, labelling and choice, and ethical objections to “unnatural” changes.')],
    contrast=[('genetic modification', 'selective breeding', 'Genetic modification transfers specific genes, even between species, in one generation; selective breeding chooses parents with desired traits over many generations within a species.'),
              ('a Bt crop', 'a herbicide-resistant crop', 'A Bt crop produces its own insecticide; a herbicide-resistant crop survives being sprayed with weedkiller, so weeds can be killed.')],
    misc=[('Eating GM food will change your DNA.', 'Digestion breaks down DNA from all foods into nucleotides; it is not incorporated into your genome.'),
          ('GM crops are always bad for the environment.', 'Some reduce pesticide use and allow less tillage, but others may encourage more herbicide use; effects depend on the crop and management.')],
    cases=[('Bt cotton in India (from 2002)', 'Bt cotton spread to over 90% of India’s cotton area; yields rose and insecticide use fell at first, but pink bollworm later evolved resistance.', 'benefits and limits of GM crops', 'It shows both the benefits of GM traits and how evolution can reduce them without careful management.')],
    evaluate=[('Golden Rice should be grown widely in countries with vitamin A deficiency.', ['could prevent hundreds of thousands of cases of childhood blindness and death', 'cheap, fits existing diets'], ['opposition to GM; possible cross-pollination', 'supplements and diverse diets are alternatives'], 'Golden Rice is a valuable tool alongside supplements and dietary diversity, given strong evidence of safety and benefit.')],
    extended=[('Evaluate the use of herbicide-resistant GM soybeans by farmers.', 'Benefits: easy, effective weed control; higher yields; less soil disturbance (no-till farming reduces erosion and CO₂ release). Drawbacks: overuse of one herbicide leading to resistant superweeds; reduced biodiversity of field weeds and insects; seed costs and patents controlling farmers; concerns over herbicide residues. Conclusion: useful with rotation of herbicides and crops and integrated weed management.', 6)],
))
inquiry('ch04-st2',
        dict(ctx='whether pollen from a GM maize field transfers the modified gene to non-GM maize at different distances',
             iv='distance of the non-GM maize plot from the GM field (5, 25, 50, 100, 200 m)', dv='percentage of kernels that test positive for the GM gene',
             cvs=[('maize variety and flowering time', 'only plants flowering together can cross'), ('number of cobs sampled per plot (20)', 'sample size affects reliability'), ('wind direction (downwind plots)', 'pollen is carried by wind'), ('the same test kit', 'test sensitivity varies')],
             hyp='If the distance increases, then the percentage of GM-positive kernels will decrease, because less pollen reaches plants further away.',
             method='Plant non-GM maize plots downwind at each distance; after flowering and ripening, collect 20 cobs per plot; test 50 kernels per cob for the GM marker using a strip test; calculate the percentage positive; repeat for two seasons; plot against distance.',
             weak=('upwind and downwind plots were mixed together in the results', 'record wind direction and compare only plots in the same direction'),
             safety='follow regulations for GM field trials; wear gloves and dispose of test strips properly'))
dataset('ch04-st2',
        dict(intro='{who} used farm data on the mass of insecticide sprayed per hectare on cotton in years after Bt cotton was introduced (three regions).', iv=('Years after introduction', ''), xs=[0, 2, 4, 6, 8],
             dv=('Insecticide used', 'kg/ha'), f=lambda x: 2.5 * math.exp(-x / 4) + 0.6, dp=2, trend='Insecticide use decreased after Bt cotton was introduced, rapidly at first and then levelling off.',
             why='Bt cotton produces its own toxin against bollworms, so farmers needed to spray less; some spraying continues for other pests (and later for resistant pests).'))

R.facts('ch04-st3', F(
    terms=[('clone', 'a genetically identical copy of an organism, cell or gene'),
           ('somatic cell nuclear transfer', 'cloning by transferring the nucleus of a body cell into an egg cell whose nucleus has been removed'),
           ('stem cell', 'an undifferentiated cell that can divide and develop into different cell types'),
           ('embryonic stem cell', 'a stem cell from an early embryo that can become any type of cell'),
           ('adult stem cell', 'a stem cell found in tissues such as bone marrow that can form a limited range of cells'),
           ('therapeutic cloning', 'producing an embryo with the patient’s genes to obtain stem cells that will not be rejected'),
           ('tissue culture', 'growing new plants from small groups of cells in sterile growth medium')],
    facts=[('What was Dolly the sheep (1996)?', 'The first mammal cloned from an adult body cell', ['The first GM animal', 'The first test-tube baby', 'A sheep made from two parents'], 'Somatic cell nuclear transfer.'),
           ('Why are plants cloned by taking cuttings?', 'Offspring are identical to a parent with desired features, cheaply and quickly', ['To increase variation', 'To make new species', 'To create seeds'], 'Asexual reproduction.'),
           ('Where are adult stem cells found?', 'Bone marrow', ['Red blood cells', 'Nerve endings only', 'Hair'], 'They make blood cells.'),
           ('What is the main advantage of embryonic stem cells over adult stem cells?', 'They can differentiate into any cell type', ['They are easier to obtain ethically', 'They never form tumours', 'They are found in all adults'], 'Pluripotent.'),
           ('Why is therapeutic cloning thought to avoid rejection?', 'The stem cells have the same genes as the patient', ['The cells have no genes', 'The immune system is removed', 'The cells are from an animal'], 'Same antigens.')],
    why=[('Explain why cloned crops may be vulnerable to disease.', 'All plants are genetically identical, so if a pathogen can infect one it can infect them all – there is no variation for resistance.'),
         ('Explain how stem cells might treat type 1 diabetes.', 'Stem cells could be differentiated into insulin-producing beta cells and transplanted, replacing the cells destroyed by the immune system.'),
         ('Explain why embryonic stem cell research is controversial.', 'Obtaining the cells destroys early embryos, which some people believe have the moral status of a person.')],
    contrast=[('reproductive cloning', 'therapeutic cloning', 'Reproductive cloning aims to produce a whole cloned organism; therapeutic cloning produces an early embryo only to harvest stem cells for treatment.'),
              ('embryonic stem cells', 'adult stem cells', 'Embryonic stem cells can become any cell type but raise ethical issues; adult stem cells are less ethically controversial but can only form a limited range of cells.')],
    misc=[('A clone is an identical copy that will have the same personality and memories.', 'A clone has the same genes, but environment and experience shape development, so it is a different individual.'),
          ('Stem cell treatments are already available for most diseases.', 'Only a few (e.g. bone marrow transplants) are established; many are experimental or unproven.')],
    cases=[('Dolly the sheep (Roslin Institute, 1996)', 'The nucleus of an udder cell was fused with an enucleated egg; after 277 attempts, Dolly was born.', 'cloning from adult cells', 'It proved specialised adult cells contain all the genes needed to make a whole animal.'),
           ('Induced pluripotent stem cells (Yamanaka, 2006)', 'Adding four genes to adult skin cells reprogrammed them into stem cells similar to embryonic ones.', 'avoiding embryo use', 'Nobel Prize 2012; reduces ethical concerns, though there are cancer risks.')],
    evaluate=[('Cloning endangered animals is a good way to save species from extinction.', ['can increase numbers when very few remain', 'can restore lost genetic diversity from frozen cells'], ['clones have very low genetic diversity', 'low success rate and welfare concerns', 'does not fix habitat loss'], 'Cloning may help in rare cases, but habitat protection and breeding programmes are far more important.')],
    extended=[('Describe how Dolly the sheep was cloned and evaluate the use of animal cloning in agriculture.', 'Udder cell taken from sheep A; egg from sheep B with nucleus removed; nucleus of udder cell inserted (electric shock fuses and stimulates division); embryo grown then implanted in surrogate C; Dolly genetically identical to A. Evaluation: copies high-yield animals quickly; but low success rate, health problems (early ageing debated), reduced genetic diversity → disease risk, ethical and welfare concerns, expensive.', 6)],
))
inquiry('ch04-st3',
        dict(ctx='how the concentration of plant hormone (auxin) in the growth medium affects root formation in cauliflower tissue culture',
             iv='auxin concentration in the agar (0, 0.5, 1.0, 2.0, 4.0 mg/dm³)', dv='number of explants forming roots after 3 weeks (out of 10)',
             cvs=[('size of explant (2 mm cube)', 'larger pieces may grow more'), ('sterile technique', 'contamination kills explants'), ('temperature and light', 'affect growth'), ('same part of the cauliflower (florets)', 'tissues respond differently')],
             hyp='If the auxin concentration increases up to an optimum, then more explants will form roots, because auxin stimulates root cell division and differentiation; very high concentrations will inhibit growth.',
             method='Sterilise cauliflower florets in dilute bleach; rinse with sterile water; cut 2 mm explants with a sterile scalpel; place 10 in each sterile tube of agar with a set auxin concentration; seal and keep at 25 °C under a 16 h light period; after 3 weeks count explants with roots; repeat three times.',
             weak=('several tubes became contaminated with mould', 'work near a Bunsen flame or in a sterile cabinet and sterilise tools with ethanol between cuts'),
             safety='bleach and ethanol are irritants and flammable; handle scalpels carefully, cutting away from the body'))
dataset('ch04-st3',
        dict(intro='{who} recorded the percentage of successful cloned embryos (live births per embryos transferred) in a cattle cloning programme in successive years (three farms).', iv=('Year of programme', ''), xs=[1, 2, 3, 4, 5],
             dv=('Success rate', '%'), f=lambda x: 2 + 2.2 * x, dp=1, trend='The success rate increased each year but remained low (under about 15%).',
             why='Technique improvements (handling eggs, timing of fusion and implantation) raise success, but reprogramming an adult nucleus remains unreliable, so many embryos fail.'))

R.facts('ch04-st4', F(
    terms=[('bioethics', 'the study of moral issues arising from biology and medicine'),
           ('informed consent', 'agreement to take part in research or treatment after understanding the risks and benefits'),
           ('patent', 'a legal right to be the only one to make or sell an invention for a period of time'),
           ('biopiracy', 'commercial use of biological resources or traditional knowledge from a community without permission or fair payment'),
           ('precautionary principle', 'taking action to avoid possible harm even if there is no complete scientific proof of harm'),
           ('genetic testing', 'analysing DNA to find alleles linked to disease or other characteristics')],
    facts=[('Which international agreement aims to share fairly the benefits of genetic resources with the countries they come from?', 'The Nagoya Protocol', ['The Paris Agreement', 'The Kyoto Protocol', 'The Montreal Protocol'], 'Under the Convention on Biological Diversity.'),
           ('Which is an ethical concern about genetic testing for disease risk?', 'Insurance companies or employers could discriminate', ['It always gives wrong results', 'It changes your DNA', 'It is impossible'], 'Privacy of genetic data.'),
           ('What does the precautionary principle suggest for a new biotechnology?', 'Avoid releasing it until it is shown to be safe if serious harm is possible', ['Release it immediately', 'Ignore any risks', 'Ban all research'], 'Used in EU GMO rules.'),
           ('Why do many countries require labelling of GM foods?', 'To allow consumers to make informed choices', ['GM foods are proven toxic', 'To increase prices', 'To hide ingredients'], 'Rules vary between countries.')],
    why=[('Explain why patents on genetically modified seeds are controversial.', 'They reward innovation, but farmers may be unable to save seed, increasing costs, and companies gain control over food supply.'),
         ('Explain why access to biotechnology can increase global inequality.', 'Expensive treatments and technologies are first available in richer countries, while poorer countries may lack infrastructure and funding.'),
         ('Explain why public engagement is important in decisions about biotechnology.', 'Decisions involve values as well as science; trust and acceptance are greater when people understand the issues and have a say.')],
    contrast=[('ethical issues', 'scientific issues', 'Scientific issues ask what is possible or what the evidence shows (e.g. is a GM crop safe?); ethical issues ask what is right or wrong (e.g. should we modify embryos?).'),
              ('biotechnology in richer countries', 'biotechnology in poorer countries', 'Richer countries can afford advanced treatments and regulation; poorer countries may benefit most from cheap solutions (e.g. GM drought-tolerant crops) but have less access and influence.')],
    misc=[('If something is scientifically possible, it is ethically acceptable.', 'Science tells us what can be done; whether it should be done depends on ethical, social and economic judgements.'),
          ('Ethical issues have one correct answer that science can provide.', 'Ethical questions depend on values; science informs but cannot settle them.')],
    cases=[('Henrietta Lacks and HeLa cells (1951)', 'Cancer cells taken from Henrietta Lacks without her knowledge became the first immortal cell line, used in polio vaccine and countless studies; her family received no compensation for decades.', 'informed consent', 'Her case changed rules on consent and recognition in medical research.'),
           ('The neem tree patent (1990s)', 'A US company patented a neem-based fungicide although Indian farmers had used neem for centuries; the European patent was revoked in 2000 after a legal challenge.', 'biopiracy', 'It highlighted the need to protect traditional knowledge and share benefits.')],
    evaluate=[('Companies should be allowed to patent genes they discover.', ['encourages investment in expensive research', 'protects inventions'], ['genes are natural, not inventions', 'patents can block research and make tests expensive (e.g. BRCA tests before 2013)'], 'Natural genes should not be patentable (as the US Supreme Court ruled in 2013), but specific new technologies using them can be.'),
              ('Gene drives should be released to wipe out malaria-carrying mosquitoes.', ['could save hundreds of thousands of lives a year', 'targets one species only'], ['irreversible effects on ecosystems', 'consent of affected communities and neighbouring countries needed'], 'Gene drives are promising but should be tested carefully with local consent and staged trials before wide release.')],
    extended=[('Discuss the ethical, social and economic implications of offering genetic testing for adult-onset disease (e.g. Huntington’s) to everyone.', 'Benefits: informed life and family planning; early monitoring; research. Concerns: no cure for Huntington’s – psychological distress; privacy and discrimination by insurers/employers; implications for relatives who did not consent; cost to health systems and unequal access; need for counselling and informed consent. Judgement: offer testing with counselling, strong data protection and anti-discrimination laws, not compulsory.', 8)],
))
inquiry('ch04-st4',
        dict(ctx='how giving people scientific information affects their acceptance of GM foods, using a survey',
             iv='type of information given before the survey (none, a one-page factual summary, a summary plus Q&A session)', dv='mean acceptance score on a 1–10 scale',
             cvs=[('same survey questions and wording', 'wording influences answers'), ('similar age groups and sample size (50 each)', 'opinions vary with age and samples must be comparable'), ('anonymous responses', 'people answer more honestly'), ('same time of year', 'news stories can affect opinions')],
             hyp='If people receive factual information and can ask questions, then their acceptance score will increase, because uncertainty and misconceptions are reduced.',
             method='Recruit three similar groups of 50 adults with informed consent; give each group one type of information; ask the same 10 questions anonymously; calculate mean acceptance score for each group; compare using means and ranges.',
             weak=('the factual summary was written to promote GM foods', 'use balanced, peer-reviewed information approved by independent reviewers'),
             safety='ethics: informed consent, right to withdraw, anonymous data stored securely'))
dataset('ch04-st4',
        dict(intro='{who} analysed global survey data on the percentage of people who support GM crops in countries with different average years of schooling (three survey years).', iv=('Mean years of schooling', ''), xs=[4, 6, 8, 10, 12],
             dv=('Support for GM crops', '%'), f=lambda x: 30 + 2.5 * x, dp=0, trend='Support for GM crops tends to increase with the average years of schooling – a weak positive correlation.',
             why='Education may increase understanding of the science, but other factors such as culture, media coverage and how much food is grown locally also affect opinion, so correlation does not show cause.'))


# =============================================================================================
# ch05 The Mole and Quantitative Chemistry
# =============================================================================================
MR = {'H₂O': 18, 'CO₂': 44, 'NaCl': 58.5, 'CaCO₃': 100, 'NaOH': 40, 'H₂SO₄': 98, 'HCl': 36.5, 'MgO': 40, 'CuSO₄': 159.5, 'NH₃': 17,
      'C₆H₁₂O₆': 180, 'O₂': 32, 'Mg': 24, 'Fe₂O₃': 160, 'CH₄': 16, 'KCl': 74.5, 'Na₂CO₃': 106, 'C₂H₅OH': 46}

R.facts('ch05-st1', F(
    terms=[('mole', 'the amount of substance containing 6.02 × 10²³ particles (atoms, molecules or ions)'),
           ('Avogadro constant', '6.02 × 10²³ per mole – the number of particles in one mole of a substance'),
           ('molar mass', 'the mass of one mole of a substance in g/mol, numerically equal to its relative formula mass'),
           ('relative formula mass (Mr)', 'the sum of the relative atomic masses of all the atoms in a formula'),
           ('relative atomic mass (Ar)', 'the weighted mean mass of an atom of an element compared with 1/12 of the mass of a carbon-12 atom')],
    facts=[('How many particles are in one mole of any substance?', '6.02 × 10²³', ['6.02 × 10²²', '12', '1000'], 'Avogadro constant.'),
           ('What is the molar mass of water, H₂O (Ar: H = 1, O = 16)?', '18 g/mol', ['17 g/mol', '10 g/mol', '34 g/mol'], '2 × 1 + 16.'),
           ('Which equation links moles, mass and molar mass?', 'moles = mass ÷ molar mass', ['moles = mass × molar mass', 'moles = molar mass ÷ mass', 'moles = mass + molar mass'], 'n = m/M.'),
           ('Which contains the most atoms?', '1 mol of CH₄', ['1 mol of He', '1 mol of O₂', '1 mol of CO₂'], 'CH₄ has 5 atoms per molecule.'),
           ('Why is the mole useful to chemists?', 'It links a measurable mass to a number of particles', ['It measures volume directly', 'It is the mass of one atom', 'It is used only for gases'], 'Allows counting by weighing.')],
    why=[('Explain why 12 g of carbon and 24 g of magnesium contain the same number of atoms.', 'Each is one mole (Ar C = 12, Mg = 24), and one mole of any element contains 6.02 × 10²³ atoms.'),
         ('Explain why chemists need the mole concept to react substances in the right proportions.', 'Equations show ratios of particles, not masses; converting masses to moles lets chemists measure out the correct numbers of particles.'),
         ('Explain why relative atomic masses are often not whole numbers.', 'They are weighted averages of the masses of an element’s isotopes, e.g. chlorine is 75% ³⁵Cl and 25% ³⁷Cl, giving 35.5.')],
    contrast=[('relative formula mass', 'molar mass', 'Relative formula mass is a ratio with no units; molar mass has the same number but units of g/mol – the mass of one mole.'),
              ('one mole of oxygen atoms', 'one mole of oxygen molecules', 'One mole of O atoms has a mass of 16 g; one mole of O₂ molecules contains twice as many atoms and has a mass of 32 g.')],
    misc=[('One mole of every substance has the same mass.', 'One mole contains the same number of particles, but the mass depends on the molar mass, e.g. 1 mol H₂ = 2 g, 1 mol CO₂ = 44 g.'),
          ('A mole is a unit of mass.', 'The mole is the unit of amount of substance (number of particles); mass is in grams.')],
    cases=[('Redefining the kilogram and mole (2019)', 'The SI redefined the mole as exactly 6.022 140 76 × 10²³ particles, no longer tied to 12 g of carbon-12; silicon spheres with precisely counted atoms helped.', 'precision in measurement', 'Defining units by fixed constants makes them universal and stable.')],
    evaluate=[('The mole is too abstract to be taught before university.', ['the numbers are hard to imagine', 'students often confuse mass and moles'], ['essential for quantitative chemistry, medicine doses, industry', 'analogies (a dozen, a ream) make it accessible'], 'The mole is challenging but essential; with analogies and practice it is appropriate for MYP 5.')],
    extended=[('Explain what is meant by a mole and calculate (a) the number of moles in 22 g of CO₂, (b) the number of molecules, and (c) the number of oxygen atoms. (Ar: C = 12, O = 16; NA = 6.02 × 10²³)', 'A mole is 6.02 × 10²³ particles. Mr CO₂ = 44; (a) 22 ÷ 44 = 0.5 mol; (b) 0.5 × 6.02 × 10²³ = 3.01 × 10²³ molecules; (c) 2 O per molecule → 6.02 × 10²³ O atoms.', 5)],
))


@R.add('ch05-st1', 'C3', (1, 5), 'numerical')
def moles(rng, slot):
    f_ = rng.choice(list(MR))
    M = MR[f_]
    k = rng.choice(['n', 'm', 'N', 'M'] if slot.d >= 2 else ['n', 'M'])
    if k == 'M':
        parts = {'H₂O': '2(1) + 16', 'CO₂': '12 + 2(16)', 'NaCl': '23 + 35.5', 'CaCO₃': '40 + 12 + 3(16)', 'NaOH': '23 + 16 + 1', 'H₂SO₄': '2(1) + 32 + 4(16)', 'HCl': '1 + 35.5',
                 'MgO': '24 + 16', 'CuSO₄': '63.5 + 32 + 4(16)', 'NH₃': '14 + 3(1)', 'C₆H₁₂O₆': '6(12) + 12(1) + 6(16)', 'O₂': '2(16)', 'Mg': '24', 'Fe₂O₃': '2(56) + 3(16)',
                 'CH₄': '12 + 4(1)', 'KCl': '39 + 35.5', 'Na₂CO₃': '2(23) + 12 + 3(16)', 'C₂H₅OH': '2(12) + 6(1) + 16'}
        return dict(stem=f'Calculate the molar mass of {f_}. (Ar: H 1, C 12, N 14, O 16, Na 23, Mg 24, S 32, Cl 35.5, K 39, Ca 40, Fe 56, Cu 63.5)', answer=f'{g(M)} g/mol',
                    markingKey=f'M1 {parts[f_]}; A1 {g(M)} g/mol.', marks=2)
    n = rng.choice([0.1, 0.2, 0.25, 0.5, 1.5, 2, 0.05])
    m = n * M
    if k == 'n':
        return dict(stem=f'How many moles are in {g(m)} g of {f_} (M = {g(M)} g/mol)?', answer=f'{g(n)} mol', markingKey=f'M1 n = m ÷ M = {g(m)} ÷ {g(M)}; A1 {g(n)} mol.', marks=2)
    if k == 'm':
        return dict(stem=f'Calculate the mass of {g(n)} mol of {f_} (M = {g(M)} g/mol).', answer=f'{g(m)} g', markingKey=f'M1 m = n × M = {g(n)} × {g(M)}; A1 {g(m)} g.', marks=2)
    N = n * 6.02e23
    return dict(stem=f'How many particles (formula units or molecules) are there in {g(m)} g of {f_} (M = {g(M)} g/mol)? (NA = 6.02 × 10²³ mol⁻¹)', answer=sci(N),
                markingKey=f'M1 n = {g(m)} ÷ {g(M)} = {g(n)} mol; M1 × 6.02 × 10²³; A1 {sci(N)}.', marks=3)


inquiry('ch05-st1',
        dict(ctx='how the number of moles of magnesium reacted affects the mass of magnesium oxide formed, to find the formula of magnesium oxide',
             iv='mass of magnesium ribbon (0.10–0.50 g, converted to moles)', dv='mass of oxygen combined, found from the increase in mass of a crucible and lid',
             cvs=[('heating until constant mass', 'all magnesium must react'), ('lid lifted only briefly', 'prevents loss of MgO smoke'), ('crucible cooled in a desiccator before weighing', 'hot crucibles give wrong mass readings'), ('clean ribbon (sandpapered)', 'oxide coating adds mass')],
             hyp='If the moles of magnesium increase, then the moles of oxygen combined will increase in a 1 : 1 ratio, because the formula of magnesium oxide is MgO.',
             method='Weigh a crucible and lid; add coiled magnesium and reweigh; heat strongly, lifting the lid occasionally; heat to constant mass; cool and reweigh; calculate mass of oxygen; convert both masses to moles (÷ 24 and ÷ 16); plot moles O against moles Mg; repeat for five masses.',
             weak=('the crucible was weighed while still hot', 'cool it in a desiccator to room temperature before weighing'),
             safety='very bright flame – do not look directly; hot crucibles – use tongs and a heatproof mat; eye protection'))
dataset('ch05-st1',
        dict(intro='{who} heated different masses of hydrated copper sulfate to constant mass and recorded the mass of water lost (three trials).', iv=('Mass of hydrated salt', 'g'), xs=[1.0, 2.0, 3.0, 4.0, 5.0],
             dv=('Mass of water lost', 'g'), f=lambda x: 0.36 * x, dp=2, trend='The mass of water lost is directly proportional to the mass of hydrated copper sulfate heated.',
             why='Hydrated copper sulfate (CuSO₄·5H₂O) contains a fixed ratio of 5 mol of water per mole of CuSO₄, so a fixed fraction (36%) of its mass is water.'))

R.facts('ch05-st2', F(
    terms=[('balanced equation', 'a symbol equation showing the mole ratio of reactants and products'),
           ('mole ratio', 'the ratio of the numbers of moles of substances in a balanced equation'),
           ('limiting reactant', 'the reactant that is completely used up and limits the amount of product'),
           ('excess reactant', 'the reactant that is left over when the reaction stops'),
           ('stoichiometry', 'the quantitative relationship between reactants and products in a reaction')],
    facts=[('In 2Mg + O₂ → 2MgO, what is the mole ratio of Mg to MgO?', '1 : 1', ['2 : 1', '1 : 2', '2 : 3'], '2 : 2 simplifies to 1 : 1.'),
           ('In N₂ + 3H₂ → 2NH₃, how many moles of NH₃ form from 3 mol of H₂?', '2 mol', ['3 mol', '6 mol', '1 mol'], 'Ratio H₂ : NH₃ = 3 : 2.'),
           ('What decides the maximum amount of product?', 'The limiting reactant', ['The excess reactant', 'The catalyst', 'The temperature only'], 'It runs out first.'),
           ('In CaCO₃ → CaO + CO₂, what mass of CaO forms from 100 g of CaCO₃ (Mr 100; CaO 56)?', '56 g', ['100 g', '44 g', '28 g'], '1 mol → 1 mol.')],
    why=[('Explain why reacting masses must be converted to moles rather than compared directly.', 'Equations give ratios of particles; different substances have different molar masses, so equal masses contain different numbers of particles.'),
         ('Explain why industrial chemists often use one reactant in excess.', 'To make sure the more expensive reactant is completely used up, increasing the yield based on it.'),
         ('Explain how conservation of mass can be used to check a reacting-mass calculation.', 'The total mass of products must equal the total mass of reactants; if the masses do not add up, there is an error.')],
    contrast=[('the limiting reactant', 'the excess reactant', 'The limiting reactant is completely used and determines how much product forms; the excess reactant is left over.'),
              ('a mass ratio', 'a mole ratio', 'A mass ratio compares grams; a mole ratio compares numbers of particles and comes directly from the balanced equation.')],
    misc=[('In 2H₂ + O₂ → 2H₂O, 2 g of hydrogen reacts with 1 g of oxygen.', 'The ratio is in moles: 2 mol H₂ (4 g) reacts with 1 mol O₂ (32 g).'),
          ('Adding more of the excess reactant increases the product.', 'Only adding more of the limiting reactant increases the product.')],
    evaluate=[('Atom economy is more important than yield when choosing an industrial process.', ['high atom economy means less waste and fewer by-products', 'more sustainable'], ['yield, rate, energy costs and safety also matter', 'by-products may be useful and sold'], 'Both matter; a sustainable process balances atom economy with yield, energy use and cost.')],
    extended=[('Iron is extracted by Fe₂O₃ + 3CO → 2Fe + 3CO₂. Calculate the mass of iron produced from 800 tonnes of iron(III) oxide, showing each step, and explain why the actual mass may be less. (Ar: Fe 56, O 16)', 'Mr Fe₂O₃ = 160; 800 t = 800 × 10⁶ g ÷ 160 = 5 × 10⁶ mol; ratio 1 : 2 → 1 × 10⁷ mol Fe; × 56 = 5.6 × 10⁸ g = 560 t. Less in practice: impure ore, incomplete reaction, losses in handling, side reactions.', 6)],
))


@R.add('ch05-st2', 'C3', (2, 5), 'numerical')
def reacting_mass(rng, slot):
    rx = rng.choice([
        ('2Mg + O₂ → 2MgO', 'magnesium', 24, 'magnesium oxide', 40, 1, 1),
        ('CaCO₃ → CaO + CO₂', 'calcium carbonate', 100, 'calcium oxide', 56, 1, 1),
        ('CaCO₃ → CaO + CO₂', 'calcium carbonate', 100, 'carbon dioxide', 44, 1, 1),
        ('2Na + Cl₂ → 2NaCl', 'sodium', 23, 'sodium chloride', 58.5, 1, 1),
        ('Fe₂O₃ + 3CO → 2Fe + 3CO₂', 'iron(III) oxide', 160, 'iron', 56, 1, 2),
        ('N₂ + 3H₂ → 2NH₃', 'hydrogen', 2, 'ammonia', 17, 3, 2),
        ('CH₄ + 2O₂ → CO₂ + 2H₂O', 'methane', 16, 'water', 18, 1, 2),
        ('2H₂O₂ → 2H₂O + O₂', 'hydrogen peroxide', 34, 'oxygen', 32, 2, 1)])
    eq, a, Ma, b, Mb, ra, rb = rx
    n = rng.choice([0.1, 0.2, 0.5, 1, 2, 4])
    ma = n * ra * Ma
    nb = n * rb
    mb = nb * Mb
    return dict(stem=f'{eq}. Calculate the mass of {b} formed from {g(ma)} g of {a}. (M: {a} {g(Ma)} g/mol, {b} {g(Mb)} g/mol)', answer=f'{g(mb)} g',
                markingKey=f'M1 moles of {a} = {g(ma)} ÷ {g(Ma)} = {g(n * ra)} mol; M1 mole ratio {ra} : {rb} → {g(nb)} mol {b}; A1 {g(nb)} × {g(Mb)} = {g(mb)} g.', marks=3)


inquiry('ch05-st2',
        dict(ctx='how the mass of sodium hydrogencarbonate heated affects the mass of sodium carbonate produced, to test the equation 2NaHCO₃ → Na₂CO₃ + H₂O + CO₂',
             iv='mass of sodium hydrogencarbonate (1.0, 2.0, 3.0, 4.0 g)', dv='mass of solid residue (sodium carbonate) after heating to constant mass',
             cvs=[('heating to constant mass', 'decomposition must be complete'), ('the same balance (±0.01 g)', 'precision of results'), ('cooling before weighing', 'hot objects give wrong readings'), ('same crucible or boiling tube type', 'mass of container must be known')],
             hyp='If the mass of sodium hydrogencarbonate increases, then the residue will be 63% of the starting mass, because 168 g of NaHCO₃ produces 106 g of Na₂CO₃ according to the 2 : 1 mole ratio.',
             method='Weigh an empty crucible; add the sodium hydrogencarbonate and reweigh; heat gently then strongly for 5 min; cool and weigh; reheat until mass is constant; calculate residue mass; compare with the mass predicted from the equation; repeat three times for each mass.',
             weak=('heating stopped before constant mass was reached', 'reheat and reweigh until two readings agree within 0.01 g'),
             safety='hot crucibles – use tongs and heatproof mats; eye protection'))
dataset('ch05-st2',
        dict(intro='{who} added increasing masses of magnesium to 50 cm³ of 1.0 mol/dm³ hydrochloric acid and measured the volume of hydrogen collected (three trials).', iv=('Mass of magnesium', 'g'), xs=[0.1, 0.2, 0.4, 0.6, 0.8],
             dv=('Volume of hydrogen', 'cm³'), f=lambda x: min(1000 * x, 600), dp=0, trend='The volume of hydrogen increases in proportion to the mass of magnesium up to 0.6 g, and then stays constant.',
             why='Mg + 2HCl → MgCl₂ + H₂: at first magnesium is limiting; 50 cm³ of 1.0 mol/dm³ acid contains 0.05 mol HCl, which reacts with 0.025 mol (0.6 g) Mg, so above this the acid is limiting and no more hydrogen forms.'))

R.facts('ch05-st3', F(
    terms=[('concentration', 'the amount of solute per unit volume of solution, in mol/dm³ or g/dm³'),
           ('mol/dm³', 'the unit of concentration: moles of solute in 1 dm³ of solution'),
           ('titration', 'a technique to find the exact volume of one solution that reacts with a known volume of another'),
           ('burette', 'a graduated tube with a tap used to add accurate, variable volumes in a titration'),
           ('pipette', 'glassware used to measure an exact fixed volume, e.g. 25.0 cm³'),
           ('end point', 'the point in a titration when the indicator changes colour'),
           ('concordant results', 'titres that agree within 0.10 cm³')],
    facts=[('How many cm³ are in 1 dm³?', '1000', ['100', '10', '10 000'], '1 dm³ = 1 litre.'),
           ('Which equation links moles, concentration and volume?', 'moles = concentration × volume (in dm³)', ['moles = concentration ÷ volume', 'moles = volume ÷ concentration', 'moles = concentration + volume'], 'n = c × V.'),
           ('Which piece of apparatus measures 25.0 cm³ of alkali accurately?', 'A volumetric pipette', ['A beaker', 'A measuring cylinder', 'A conical flask'], 'Use a pipette filler.'),
           ('Why is a white tile placed under the conical flask in a titration?', 'To see the colour change of the indicator clearly', ['To keep the flask warm', 'To stop the flask breaking', 'To catch drips'], ''),
           ('Which titres should be used to calculate the mean?', 'Concordant titres within 0.10 cm³ of each other', ['All titres including the rough one', 'Only the first titre', 'The largest titre'], 'Exclude the rough titre.')],
    why=[('Explain why a rough titration is carried out first.', 'It shows the approximate end point so later titrations can add acid dropwise near the end point for accuracy.'),
         ('Explain why the burette is rinsed with the acid before filling.', 'Any water left inside would dilute the acid and change its concentration.'),
         ('Explain why the conical flask is swirled during a titration.', 'To mix the solutions thoroughly so the indicator shows the true end point.')],
    contrast=[('concentration in mol/dm³', 'concentration in g/dm³', 'mol/dm³ gives the number of moles per dm³; g/dm³ gives the mass per dm³; multiply mol/dm³ by molar mass to get g/dm³.'),
              ('a pipette', 'a burette', 'A pipette delivers one fixed volume accurately; a burette delivers variable volumes that are read from its scale.')],
    misc=[('The titre is the burette reading at the end.', 'The titre is the volume added: final reading − initial reading.'),
          ('A more concentrated solution always contains more solute.', 'It contains more solute per dm³; a small volume of concentrated solution may contain less solute than a large volume of dilute solution.')],
    evaluate=[('Titrations with a pH probe and data logger are better than using an indicator.', ['no judgement of colour; works for coloured solutions', 'gives a full pH curve'], ['probes must be calibrated and are more expensive', 'indicators are quick and reliable for simple acid–alkali titrations'], 'Data loggers give more information and objectivity, but indicators remain adequate for routine titrations.')],
    extended=[('Describe how to carry out a titration to find the concentration of a sodium hydroxide solution using 0.100 mol/dm³ hydrochloric acid, and show how the result would be calculated if the mean titre were 22.50 cm³ for 25.0 cm³ of alkali.', 'Rinse and fill burette with acid; pipette 25.0 cm³ NaOH into conical flask; add 2–3 drops of phenolphthalein; titrate with swirling until pink just disappears; rough then accurate titres dropwise; repeat until concordant (±0.10 cm³). n(HCl) = 0.100 × 22.50/1000 = 2.25 × 10⁻³ mol; 1 : 1 ratio → n(NaOH) = 2.25 × 10⁻³; c = 2.25 × 10⁻³ ÷ 0.0250 = 0.0900 mol/dm³.', 8)],
))


@R.add('ch05-st3', 'C3', (1, 5), 'numerical')
def conc_titr(rng, slot):
    k = rng.choice(['c', 'n', 'gdm', 'titr'] if slot.d >= 3 else ['c', 'n', 'gdm'])
    if k == 'c':
        n = rng.choice([0.05, 0.1, 0.2, 0.25, 0.5])
        V = rng.choice([100, 200, 250, 500])
        return dict(stem=f'{g(n)} mol of sodium hydroxide is dissolved to make {V} cm³ of solution. Calculate the concentration in mol/dm³.', answer=f'{g(n / (V / 1000))} mol/dm³',
                    markingKey=f'M1 V = {V} ÷ 1000 = {g(V / 1000)} dm³; M1 c = n ÷ V; A1 {g(n / (V / 1000))} mol/dm³.', marks=3)
    if k == 'n':
        c = rng.choice([0.1, 0.2, 0.5, 1.0, 2.0])
        V = rng.choice([10, 20, 25, 50])
        return dict(stem=f'How many moles of acid are in {V} cm³ of {g(c)} mol/dm³ hydrochloric acid?', answer=f'{g(c * V / 1000)} mol',
                    markingKey=f'M1 n = c × V = {g(c)} × {V}/1000; A1 {g(c * V / 1000)} mol.', marks=2)
    if k == 'gdm':
        c = rng.choice([0.1, 0.2, 0.5])
        f_ = rng.choice(['NaOH', 'NaCl', 'H₂SO₄', 'Na₂CO₃'])
        return dict(stem=f'Convert a {g(c)} mol/dm³ solution of {f_} (M = {g(MR[f_])} g/mol) into g/dm³.', answer=f'{g(c * MR[f_])} g/dm³',
                    markingKey=f'M1 {g(c)} × {g(MR[f_])}; A1 {g(c * MR[f_])} g/dm³.', marks=2)
    ca = rng.choice([0.100, 0.150, 0.200])
    t = rng.choice([18.40, 20.00, 22.50, 24.80])
    acid, ratio = rng.choice([('hydrochloric acid', 1), ('sulfuric acid', 2)])
    na = ca * t / 1000
    nb = na * ratio
    cb = nb / 0.025
    eq = 'HCl + NaOH → NaCl + H₂O' if ratio == 1 else 'H₂SO₄ + 2NaOH → Na₂SO₄ + 2H₂O'
    return dict(stem=f'25.0 cm³ of sodium hydroxide solution was neutralised by {t:.2f} cm³ of {ca:.3f} mol/dm³ {acid}. {eq}. Calculate the concentration of the sodium hydroxide.', answer=f'{cb:.3g} mol/dm³',
                markingKey=f'M1 n(acid) = {ca:.3f} × {t:.2f}/1000 = {na:.3g} mol; M1 ratio 1 : {ratio} → n(NaOH) = {nb:.3g} mol; M1 ÷ 0.0250 dm³; A1 {cb:.3g} mol/dm³.', marks=4)


inquiry('ch05-st3',
        dict(ctx='how the brand of vinegar affects its ethanoic acid concentration, found by titration with sodium hydroxide',
             iv='brand of vinegar (four brands, each diluted 1 : 10)', dv='mean concordant titre of 0.100 mol/dm³ NaOH needed to neutralise 25.0 cm³ of diluted vinegar',
             cvs=[('volume of diluted vinegar (25.0 cm³ pipette)', 'more acid needs more alkali'), ('concentration of NaOH (0.100 mol/dm³)', 'affects titre'), ('indicator and number of drops (phenolphthalein, 3)', 'end point judgement'), ('dilution factor (1 : 10) using volumetric flask', 'concentration calculation depends on it')],
             hyp='If brand A is labelled 6% acidity, then it will need the largest titre, because a higher concentration of ethanoic acid needs more moles of NaOH to neutralise it.',
             method='Dilute 25.0 cm³ of each vinegar to 250 cm³ in a volumetric flask; pipette 25.0 cm³ into a conical flask; add phenolphthalein; titrate with NaOH from a burette until a permanent pale pink; repeat until concordant; calculate concentration (×10 for dilution) and compare with labels.',
             weak=('the end point was overshot to dark pink', 'add NaOH dropwise near the end point and stop at the first permanent pale pink'),
             safety='sodium hydroxide is corrosive – wear eye protection; use a pipette filler, never mouth-pipette'))
dataset('ch05-st3',
        dict(intro='{who} titrated 25.0 cm³ portions of a hydrochloric acid solution diluted to different extents with 0.100 mol/dm³ sodium hydroxide (three titres each).', iv=('Acid concentration', 'mol/dm³'), xs=[0.04, 0.08, 0.12, 0.16, 0.20],
             dv=('Titre', 'cm³'), f=lambda x: 250 * x, dp=2, trend='The titre is directly proportional to the acid concentration.',
             why='Moles of acid = c × V; with a fixed 25.0 cm³ of acid and fixed NaOH concentration, the volume of NaOH needed (1 : 1 ratio) is proportional to the acid concentration.'))

R.facts('ch05-st4', F(
    terms=[('molar gas volume', 'the volume occupied by one mole of any gas: 24 dm³ at room temperature and pressure (r.t.p.)'),
           ('r.t.p.', 'room temperature and pressure: about 20 °C and 1 atmosphere'),
           ('theoretical yield', 'the maximum mass of product calculated from the balanced equation'),
           ('actual yield', 'the mass of product actually obtained'),
           ('percentage yield', 'actual yield ÷ theoretical yield × 100'),
           ('atom economy', 'Mr of desired product ÷ total Mr of all reactants × 100')],
    facts=[('What volume does 1 mol of oxygen occupy at r.t.p.?', '24 dm³', ['22.4 cm³', '1 dm³', '32 dm³'], 'The same for any gas.'),
           ('What volume does 0.5 mol of CO₂ occupy at r.t.p.?', '12 dm³', ['24 dm³', '22 dm³', '48 dm³'], '0.5 × 24.'),
           ('Why is percentage yield usually less than 100%?', 'Some product is lost, reactions may be incomplete or side reactions occur', ['Mass is destroyed', 'Products always evaporate', 'The equation is wrong'], 'Also reversible reactions.'),
           ('A reaction has a theoretical yield of 20 g but 15 g is obtained. What is the percentage yield?', '75%', ['133%', '25%', '5%'], '15 ÷ 20 × 100.')],
    why=[('Explain why equal volumes of different gases at the same temperature and pressure contain the same number of molecules.', 'Gas molecules are far apart, so the volume depends on the number of molecules, not their size (Avogadro’s law).'),
         ('Explain why a high percentage yield is important in industry.', 'Less raw material is wasted, costs are lower and less waste must be treated, making the process more sustainable.'),
         ('Explain why a reaction with 100% yield may still have a low atom economy.', 'All reactants could be converted to products, but much of the mass may go into unwanted by-products.')],
    contrast=[('percentage yield', 'atom economy', 'Percentage yield compares the product actually obtained with the maximum possible; atom economy shows what fraction of the reactants’ mass ends up in the desired product, assuming complete reaction.'),
              ('theoretical yield', 'actual yield', 'Theoretical yield is calculated from the equation; actual yield is measured after the experiment and is usually less.')],
    misc=[('One mole of a heavy gas takes up more space than one mole of a light gas.', 'At the same temperature and pressure one mole of any gas occupies the same volume (24 dm³ at r.t.p.).'),
          ('A percentage yield above 100% means a very good experiment.', 'A yield over 100% indicates an error, e.g. the product was still wet or impure.')],
    cases=[('Ibuprofen synthesis (Boots vs BHC process)', 'The original 1960s six-step route had about 40% atom economy; the 1990s BHC three-step route reached about 77% (nearly 100% with by-product recovery).', 'green chemistry', 'Higher atom economy cut waste and costs and won a US Green Chemistry award.')],
    evaluate=[('Chemical companies should be required to choose the process with the highest atom economy.', ['less waste, more sustainable use of resources'], ['other factors – yield, rate, energy use, safety and cost – may make a lower atom economy route better', 'by-products may be useful'], 'Atom economy should be a major factor, but decisions need to balance it with yield, energy and safety.')],
    extended=[('Calcium carbonate decomposes: CaCO₃ → CaO + CO₂. 25 g of CaCO₃ is heated and 11.2 g of CaO is collected. Calculate the theoretical yield, the percentage yield, the volume of CO₂ at r.t.p. and the atom economy for CaO. (Mr CaCO₃ 100, CaO 56, CO₂ 44)', 'n(CaCO₃) = 0.25 mol → theoretical CaO = 0.25 × 56 = 14 g; % yield = 11.2/14 × 100 = 80%; CO₂ (theoretical) = 0.25 × 24 = 6.0 dm³; atom economy = 56/100 × 100 = 56%.', 6)],
))


@R.add('ch05-st4', 'C3', (1, 5), 'numerical')
def gas_yield(rng, slot):
    k = rng.choice(['vol', 'nfromv', 'yield', 'ae'] if slot.d >= 2 else ['vol', 'yield'])
    if k == 'vol':
        n = rng.choice([0.1, 0.25, 0.5, 2, 0.05])
        gas = rng.choice(['hydrogen', 'oxygen', 'carbon dioxide', 'nitrogen'])
        return dict(stem=f'Calculate the volume of {g(n)} mol of {gas} at r.t.p. (molar volume = 24 dm³).', answer=f'{g(n * 24)} dm³', markingKey=f'M1 V = n × 24 = {g(n)} × 24; A1 {g(n * 24)} dm³.', marks=2)
    if k == 'nfromv':
        V = rng.choice([60, 120, 240, 480, 600])
        return dict(stem=f'A reaction produced {V} cm³ of hydrogen at r.t.p. How many moles is this?', answer=f'{g(V / 24000)} mol', markingKey=f'M1 n = {V} ÷ 24 000; A1 {g(V / 24000)} mol.', marks=2)
    if k == 'yield':
        th = rng.choice([8.0, 12.5, 20.0, 40.0])
        p = rng.choice([60, 72, 85, 90])
        a = th * p / 100
        return dict(stem=f'The theoretical yield of a salt was {g(th)} g. A student obtained {g(a)} g of dry crystals. Calculate the percentage yield and give one reason it is below 100%.', answer=f'{p}%; e.g. some solution was lost when filtering or not all crystals formed',
                    markingKey=f'M1 {g(a)} ÷ {g(th)} × 100; A1 {p}%; B1 loss during transfer/filtration, incomplete reaction, product left in solution.', marks=3)
    rx = rng.choice([('making ammonia: N₂ + 3H₂ → 2NH₃', 34, 34, 'NH₃'), ('making quicklime: CaCO₃ → CaO + CO₂', 56, 100, 'CaO'),
                     ('making ethanol by fermentation: C₆H₁₂O₆ → 2C₂H₅OH + 2CO₂', 92, 180, 'C₂H₅OH'), ('making hydrogen: CH₄ + H₂O → CO + 3H₂', 6, 34, 'H₂')])
    nm, top, bot, p = rx
    return dict(stem=f'Calculate the atom economy for {nm}, where {p} is the useful product. (Total Mr of desired product = {top}; total Mr of reactants = {bot})', answer=f'{g(top / bot * 100)}%',
                markingKey=f'M1 {top} ÷ {bot} × 100; A1 {g(top / bot * 100)}%.', marks=2)


inquiry('ch05-st4',
        dict(ctx='how the mass of magnesium reacting with excess acid affects the volume of hydrogen produced, to find the molar gas volume',
             iv='mass of magnesium ribbon (0.02, 0.04, 0.06, 0.08, 0.10 g)', dv='volume of hydrogen collected in a gas syringe at room temperature',
             cvs=[('excess acid (50 cm³ of 1.0 mol/dm³ HCl)', 'magnesium must be the limiting reactant'), ('room temperature and pressure recorded', 'gas volume depends on both'), ('airtight apparatus', 'leaks reduce the volume'), ('clean magnesium ribbon', 'oxide layer reduces the hydrogen produced')],
             hyp='If the mass of magnesium doubles, then the hydrogen volume will double, and the volume per mole of hydrogen will be about 24 dm³, because Mg + 2HCl → MgCl₂ + H₂ gives 1 mol H₂ per mol Mg.',
             method='Clean and weigh magnesium ribbon; put 50 cm³ of acid in a conical flask connected to a gas syringe; drop in the magnesium and quickly replace the bung; record the final volume when reaction stops; repeat for each mass three times; calculate moles of Mg and molar volume = volume ÷ moles H₂.',
             weak=('gas escaped while the bung was being replaced', 'hang the magnesium in a small tube inside the flask and tip it after sealing'),
             safety='hydrogen is flammable – no flames; acid is an irritant – eye protection'))
dataset('ch05-st4',
        dict(intro='{who} made copper sulfate crystals using different heating times for the evaporation step and calculated the percentage yield (three batches each).', iv=('Evaporation time', 'min'), xs=[5, 10, 15, 20, 25],
             dv=('Percentage yield', '%'), f=lambda x: 88 - 0.06 * (x - 15) ** 2 - (12 if x > 20 else 0), dp=0, trend='The percentage yield rises to a maximum at about 15 minutes of evaporation and then falls, especially for the longest time.',
             why='Too little evaporation leaves salt dissolved in the solution; too much heating spits solution out and can decompose the crystals (removing water of crystallisation), reducing the yield.'))


# =============================================================================================
# ch06 Organic Chemistry
# =============================================================================================
ALK = ['meth', 'eth', 'prop', 'but', 'pent', 'hex', 'hept', 'oct']


def cf(c, h, extra=''):
    return (f'C{c}' if c > 1 else 'C').translate(SUB) + (f'H{h}' if h > 1 else 'H').translate(SUB) + extra


R.facts('ch06-st1', F(
    terms=[('crude oil', 'a mixture of many hydrocarbons formed over millions of years from the remains of plankton'),
           ('hydrocarbon', 'a compound containing hydrogen and carbon only'),
           ('fractional distillation', 'separating crude oil into fractions with similar boiling points using a fractionating column'),
           ('fraction', 'a group of hydrocarbons with similar chain lengths and boiling points'),
           ('viscosity', 'how thick (resistant to flow) a liquid is'),
           ('cracking', 'breaking long-chain hydrocarbons into shorter, more useful alkanes and alkenes using heat and a catalyst')],
    facts=[('Where in the fractionating column do the fractions with the lowest boiling points collect?', 'At the top', ['At the bottom', 'In the middle', 'They stay in the furnace'], 'The column is coolest at the top.'),
           ('How does viscosity change as hydrocarbon chain length increases?', 'It increases', ['It decreases', 'It stays the same', 'It becomes zero'], 'Stronger intermolecular forces.'),
           ('Which fraction is used as fuel for aircraft?', 'Kerosene', ['Bitumen', 'Refinery gases', 'Fuel oil'], 'Medium chain length (C10–C16).'),
           ('Why are long-chain hydrocarbons cracked?', 'There is more demand for shorter chains like petrol, and cracking also produces alkenes', ['Long chains are not hydrocarbons', 'To make crude oil', 'To increase viscosity'], 'Supply and demand.'),
           ('Which fraction is used to surface roads?', 'Bitumen', ['Petrol', 'Diesel', 'Naphtha'], 'Very long chains, very viscous.')],
    why=[('Explain how fractional distillation separates crude oil.', 'Crude oil is vaporised and enters a column that is hot at the bottom and cool at the top; hydrocarbons rise and condense at the level where the temperature is below their boiling point, so fractions with similar boiling points are collected together.'),
         ('Explain why longer hydrocarbon chains have higher boiling points.', 'Longer molecules have stronger intermolecular forces between them, so more energy is needed to separate them.'),
         ('Explain why short-chain hydrocarbons make better fuels than long-chain ones.', 'They ignite more easily (more flammable), are less viscous, flow easily and burn more cleanly with a less smoky flame.')],
    contrast=[('fractional distillation', 'cracking', 'Fractional distillation is a physical process that separates existing hydrocarbons by boiling point; cracking is a chemical reaction that breaks long molecules into smaller ones.'),
              ('a short-chain fraction', 'a long-chain fraction', 'Short-chain fractions (gases, petrol) have low boiling points, low viscosity and are very flammable; long-chain fractions (fuel oil, bitumen) have high boiling points, are viscous and hard to ignite.')],
    misc=[('Fractional distillation breaks hydrocarbon molecules into smaller ones.', 'It only separates molecules by boiling point; breaking molecules is cracking, a chemical reaction.'),
          ('Each fraction is a single pure compound.', 'Each fraction is a mixture of hydrocarbons with similar chain lengths and boiling points.')],
    cases=[('Deepwater Horizon oil spill (2010)', 'An explosion on an oil rig in the Gulf of Mexico killed 11 workers and released about 4.9 million barrels of crude oil, harming marine life and coasts.', 'environmental cost of oil extraction', 'It led to tighter drilling regulations and highlighted the risks of deep-sea oil extraction.')],
    evaluate=[('Crude oil is too valuable to burn and should be kept for making plastics and medicines.', ['finite resource; feedstock for plastics, medicines, lubricants', 'burning releases CO₂'], ['transport and energy still depend heavily on oil fuels', 'alternative feedstocks (biomass) are developing'], 'Reducing fuel use and keeping oil for chemicals makes sense as renewable energy and electric transport expand.')],
    extended=[('Describe how crude oil is separated into fractions and explain how the properties and uses of the fractions change with chain length.', 'Heat crude oil to ~350 °C to vaporise; vapour enters column (temperature gradient hot at bottom, cool at top); vapours rise, condense at levels below their boiling point; collected on trays. Short chains (C1–C4 refinery gas, petrol C5–C10): low bp, low viscosity, very flammable – fuels for cars, cooking. Medium (kerosene, diesel): jet and lorry fuel. Long (fuel oil, bitumen): high bp, viscous, hard to ignite – ships, roads. Cracking converts surplus long chains into useful short chains.', 6)],
))


@R.add('ch06-st1', 'C3', (1, 4), 'numerical')
def crack_eq(rng, slot):
    c = rng.choice([10, 12, 14, 16])
    a = rng.choice([2, 3])
    rest = c - a
    return dict(stem=f'An alkane {cf(c, 2 * c + 2)} is cracked to form one molecule of an alkene with {a} carbon atoms and one alkane. Write the formulae of the two products.', answer=f'{cf(a, 2 * a)} and {cf(rest, 2 * rest + 2)}',
                markingKey=f'1 alkene {cf(a, 2 * a)} (CₙH₂ₙ); 1 alkane {cf(rest, 2 * rest + 2)} (CₙH₂ₙ₊₂); carbons and hydrogens balance: {c} C and {2 * c + 2} H.', marks=2)


inquiry('ch06-st1',
        dict(ctx='how the chain length of an alkane affects its viscosity',
             iv='number of carbon atoms (hexane C6, octane C8, decane C10, dodecane C12, liquid paraffin ~C20)', dv='time for a steel ball to fall 20 cm through each liquid in a measuring cylinder',
             cvs=[('temperature of the liquids', 'viscosity falls as temperature rises'), ('the same steel ball', 'size and mass affect fall time'), ('same distance and cylinder', 'fall time depends on distance'), ('releasing from rest at the surface', 'pushing changes the speed')],
             hyp='If the chain length increases, then the ball will take longer to fall, because longer molecules have stronger intermolecular forces and tangle more, making the liquid more viscous.',
             method='Fill identical measuring cylinders to the same height with each hydrocarbon in a fume cupboard; mark two lines 20 cm apart; release the ball at the surface; time it between the lines; repeat five times; calculate means; plot fall time against carbon number.',
             weak=('timing by eye was inaccurate for the fast fall in hexane', 'use a longer cylinder or film with a slow-motion camera'),
             safety='hydrocarbons are flammable and harmful – use a fume cupboard, no flames, eye protection'))
dataset('ch06-st1',
        dict(intro='{who} collected the boiling points of straight-chain alkanes, in kelvin, from three different data sources.', iv=('Number of carbon atoms', ''), xs=[2, 4, 6, 8, 10],
             dv=('Boiling point', 'K'), f=lambda x: {2: -89, 4: -1, 6: 69, 8: 126, 10: 174}[x] + 273, dp=0, trend='Boiling point (in kelvin) increases with the number of carbon atoms, but by smaller amounts for each extra two carbons.',
             why='Longer chains have stronger intermolecular forces, so more energy is needed to separate the molecules; each extra CH₂ adds a smaller fraction to the total.'))

R.facts('ch06-st2', F(
    terms=[('homologous series', 'a family of organic compounds with the same general formula and functional group, similar chemical properties and a trend in physical properties'),
           ('alkane', 'a saturated hydrocarbon with only C–C single bonds; general formula CₙH₂ₙ₊₂'),
           ('alkene', 'an unsaturated hydrocarbon with a C=C double bond; general formula CₙH₂ₙ'),
           ('saturated', 'containing only single carbon–carbon bonds'),
           ('unsaturated', 'containing at least one carbon–carbon double (or triple) bond'),
           ('functional group', 'the atom or group of atoms that gives a homologous series its characteristic reactions'),
           ('isomers', 'compounds with the same molecular formula but different structural formulae')],
    facts=[('What is the general formula of the alkanes?', 'CₙH₂ₙ₊₂', ['CₙH₂ₙ', 'CₙH₂ₙ₋₂', 'CₙHₙ'], 'e.g. C₃H₈.'),
           ('What is the functional group of the alkenes?', 'C=C double bond', ['–OH', '–COOH', 'C–C single bond'], 'Makes them reactive.'),
           ('What is the name of C₃H₆?', 'Propene', ['Propane', 'Ethene', 'Butene'], 'Three carbons, one double bond.'),
           ('Why is there no alkene called “methene”?', 'An alkene needs at least two carbon atoms to have a C=C bond', ['Methane is too reactive', 'It is a gas', 'Methene exists but is rare'], 'Ethene is the first.'),
           ('Successive members of a homologous series differ by…', 'CH₂', ['CH₄', 'C₂H₄', 'H₂'], 'Each adds one CH₂.')],
    why=[('Explain why members of a homologous series have similar chemical reactions.', 'They have the same functional group, which is where reactions happen.'),
         ('Explain why alkenes are more reactive than alkanes.', 'The C=C double bond can open up and allow other atoms to add on (addition reactions); alkanes have only strong single bonds.'),
         ('Explain why butane has two isomers but propane has none.', 'With four carbons, the chain can be straight or branched (methylpropane); three carbons can only be arranged in one way.')],
    contrast=[('an alkane', 'an alkene', 'An alkane is saturated with only single bonds (CₙH₂ₙ₊₂) and fairly unreactive; an alkene is unsaturated with a C=C bond (CₙH₂ₙ) and undergoes addition reactions.'),
              ('a molecular formula', 'a structural formula', 'A molecular formula shows the number of each atom (C₂H₆); a structural formula shows how the atoms are bonded (CH₃–CH₃).')],
    misc=[('Isomers are the same compound written differently.', 'Isomers are different compounds with different properties that share the same molecular formula.'),
          ('All hydrocarbons are alkanes.', 'Hydrocarbons include alkanes, alkenes, alkynes and aromatic compounds.')],
    evaluate=[('IUPAC systematic names should replace all common names in chemistry.', ['unambiguous worldwide; name gives structure'], ['common names (acetone, acetic acid) are widely used in industry and everyday life', 'long systematic names can be cumbersome'], 'Systematic names are essential for precision; common names remain useful in context.')],
    extended=[('Name the first four alkanes and alkenes, give their molecular formulae, and explain how the general formulae and functional groups define the two homologous series.', 'Alkanes: methane CH₄, ethane C₂H₆, propane C₃H₈, butane C₄H₁₀ (CₙH₂ₙ₊₂, single bonds, saturated). Alkenes: ethene C₂H₄, propene C₃H₆, butene C₄H₈, pentene C₅H₁₀ (CₙH₂ₙ, C=C, unsaturated). Each series differs by CH₂, same functional group → similar reactions; physical properties (bp) increase with chain length.', 6)],
))


@R.add('ch06-st2', 'C1', (1, 3), 'mcq')
def name_formula(rng, slot):
    kind = rng.choice(['alkane', 'alkene'])
    c = rng.randint(1 if kind == 'alkane' else 2, 8)
    h = 2 * c + 2 if kind == 'alkane' else 2 * c
    nm = ALK[c - 1] + ('ane' if kind == 'alkane' else 'ene')
    fm = cf(c, h)
    if rng.random() < 0.5:
        wr = [cf(c, 2 * c if kind == 'alkane' else 2 * c + 2), cf(c + 1, h), cf(max(c - 1, 1), h)]
        wr = [w for w in dict.fromkeys(wr) if w != fm]
        while len(wr) < 3:
            wr.append(cf(c + len(wr) + 1, 2 * (c + len(wr) + 1)))
        return mcq(rng, f'What is the molecular formula of {nm}?', fm, wr[:3], f'B1 {fm}: {c} carbon atoms, {"CₙH₂ₙ₊₂" if kind == "alkane" else "CₙH₂ₙ"}.')
    other = ALK[c - 1] + ('ene' if kind == 'alkane' else 'ane')
    wr = [w for w in [other, ALK[c % 8] + nm[-3:], ALK[(c - 2) % 8] + nm[-3:]] if w != nm and w not in ('methene',)]
    return mcq(rng, f'What is the name of the hydrocarbon {fm}?', nm, wr[:3] if len(wr) >= 3 else wr + ['ethyne'], f'B1 {nm}')


inquiry('ch06-st2',
        dict(ctx='how the number of carbon atoms in an alkane affects the energy released per gram when it burns',
             iv='alkane fuel (in spirit burners: hexane, heptane, octane, decane)', dv='temperature rise of 100 g water in a copper can, used to calculate energy per gram of fuel burned',
             cvs=[('mass of water (100 g)', 'temperature rise depends on mass heated'), ('distance from flame to can', 'more heat lost if further'), ('temperature rise (stop at 20 °C rise)', 'heat loss increases with temperature'), ('draught shield', 'reduces heat loss')],
             hyp='If the alkane has more carbon atoms, then the energy released per gram will be similar (about 45 kJ/g), but the energy per mole will increase, because each extra CH₂ adds similar bonds to be broken and formed.',
             method='Weigh a spirit burner of fuel; put 100 g water in a copper can clamped 2 cm above the wick; record temperature; light and heat until the temperature rises 20 °C; extinguish, reweigh; calculate energy = 100 × 4.18 × 20 and divide by mass burned; repeat three times for each fuel; convert to kJ/mol.',
             weak=('the flame was yellow and sooty, depositing soot on the can', 'adjust the wick to give a cleaner flame and clean the can between trials'),
             safety='alkanes are highly flammable – keep lids on burners, no refilling near flames, eye protection, fume extraction'))
dataset('ch06-st2',
        dict(intro='{who} calculated the energy released per mole when different alkanes were burned in a calorimetry experiment (three trials each).', iv=('Number of carbon atoms', ''), xs=[1, 2, 3, 4, 5],
             dv=('Energy released', 'kJ/mol'), f=lambda x: 620 * x + 250, dp=0, trend='The energy released per mole increases by roughly the same amount for each extra carbon atom.',
             why='Each additional CH₂ group adds the same bonds (one C–C and two C–H) to break and more C=O and O–H bonds to form, so the energy released per mole rises steadily; values are below data-book values because of heat loss.'))

R.facts('ch06-st3', F(
    terms=[('complete combustion', 'burning in plenty of oxygen to form carbon dioxide and water only'),
           ('incomplete combustion', 'burning in limited oxygen, forming carbon monoxide and/or carbon (soot) as well as water'),
           ('addition reaction', 'a reaction in which atoms add across a C=C double bond, forming a single product'),
           ('bromine water test', 'orange bromine water turns colourless when shaken with an alkene, but not with an alkane'),
           ('hydrogenation', 'addition of hydrogen to an alkene using a nickel catalyst, forming an alkane'),
           ('hydration', 'addition of steam to an alkene using a phosphoric acid catalyst, forming an alcohol')],
    facts=[('What happens when bromine water is shaken with ethene?', 'It turns from orange to colourless', ['It turns from colourless to orange', 'It turns blue', 'No change'], 'Bromine adds across the C=C.'),
           ('What is the product of ethene + hydrogen?', 'Ethane', ['Ethanol', 'Ethanoic acid', 'Polyethene'], 'Nickel catalyst, 150 °C.'),
           ('What is the product of ethene + steam?', 'Ethanol', ['Ethane', 'Ethanoic acid', 'Ethyl ethanoate'], 'Hydration, phosphoric acid catalyst, 300 °C.'),
           ('What is the product when bromine adds to ethene?', '1,2-dibromoethane', ['Bromoethane', 'Ethyl bromide and hydrogen', 'Dibromomethane'], 'C₂H₄Br₂.'),
           ('Which pollutant from incomplete combustion is toxic and colourless?', 'Carbon monoxide', ['Carbon dioxide', 'Water vapour', 'Soot'], 'Binds to haemoglobin.')],
    why=[('Explain why alkanes do not decolourise bromine water.', 'They are saturated with no C=C bond, so bromine cannot add on.'),
         ('Explain why alkenes burn with a smokier flame than alkanes.', 'They have a higher proportion of carbon, so more carbon is left unburned as soot (incomplete combustion).'),
         ('Explain why hydrogenation is used to make margarine.', 'Adding hydrogen to C=C bonds in vegetable oils raises their melting point, making them solid at room temperature and spreadable.')],
    contrast=[('a substitution reaction', 'an addition reaction', 'In substitution an atom is replaced by another (alkanes with halogens in UV light); in addition atoms add across a double bond and no atoms are lost (alkenes).'),
              ('complete combustion', 'incomplete combustion', 'Complete combustion has plenty of oxygen and forms CO₂ and H₂O; incomplete combustion in limited oxygen forms CO and soot and releases less energy.')],
    misc=[('Bromine water turns colourless because the alkene dissolves it.', 'It decolourises because bromine reacts with the alkene by addition, forming a colourless dibromo compound.'),
          ('Carbon monoxide is just a weak form of carbon dioxide.', 'CO is a different, highly toxic gas that binds to haemoglobin much more strongly than oxygen.')],
    cases=[('Leaded petrol phase-out (completed 2021)', 'Tetraethyl lead was added to petrol to stop engine knocking; it caused lead poisoning and lowered children’s IQ; Algeria was the last country to stop selling it in 2021.', 'chemistry of fuels and health', 'A UN campaign estimated the phase-out prevents over a million premature deaths a year.')],
    evaluate=[('Petrol and diesel cars should be banned in cities.', ['reduces CO, NOx and particulates – improves health', 'reduces CO₂ if replaced by electric vehicles on clean electricity'], ['cost for people who cannot afford new cars', 'electricity may still come from fossil fuels', 'battery production has environmental costs'], 'Gradual bans with support and clean electricity improve health and climate.')],
    extended=[('Write balanced equations for the complete combustion of propane and its incomplete combustion forming carbon monoxide, and evaluate the dangers of using a gas heater in a poorly ventilated room.', 'Complete: C₃H₈ + 5O₂ → 3CO₂ + 4H₂O. Incomplete (CO): 2C₃H₈ + 7O₂ → 6CO + 8H₂O. In poor ventilation oxygen runs low → incomplete combustion → toxic CO (colourless, odourless, binds haemoglobin, can kill) and soot; also less energy released. Need ventilation, servicing and CO alarms.', 6)],
))


@R.add('ch06-st3', 'C3', (2, 5), 'short')
def combust_eq(rng, slot):
    c = rng.randint(1, 6)
    kind = rng.choice(['alkane', 'alkane', 'alkene'] if c > 1 else ['alkane'])
    h = 2 * c + 2 if kind == 'alkane' else 2 * c
    o2 = c + h / 4
    nm = ALK[c - 1] + ('ane' if kind == 'alkane' else 'ene')
    if o2 == int(o2):
        eq = f'{cf(c, h)} + {int(o2) if o2 != 1 else ""}O₂ → {c if c > 1 else ""}CO₂ + {h // 2 if h // 2 > 1 else ""}H₂O'
    else:
        eq = f'2{cf(c, h)} + {int(2 * o2)}O₂ → {2 * c}CO₂ + {h}H₂O'
    return dict(stem=f'Write the balanced symbol equation for the complete combustion of {nm}, {cf(c, h)}.', answer=eq.replace('+ O₂', '+ O₂'),
                markingKey=f'1 correct products CO₂ and H₂O; 1 balanced: {eq}.', marks=2)


inquiry('ch06-st3',
        dict(ctx='how the concentration of bromine water affects the volume of an alkene (cyclohexene) needed to decolourise it',
             iv='concentration of bromine water (0.01, 0.02, 0.03, 0.04 mol/dm³)', dv='volume of cyclohexene solution added from a burette until the orange colour just disappears',
             cvs=[('volume of bromine water (10 cm³)', 'more bromine needs more alkene'), ('concentration of cyclohexene solution', 'affects volume needed'), ('swirling after each addition', 'ensures complete reaction'), ('white background and lighting', 'end point judgement')],
             hyp='If the bromine water is more concentrated, then a proportionally larger volume of cyclohexene will be needed, because one C=C double bond reacts with one Br₂ molecule.',
             method='In a fume cupboard, put 10 cm³ of bromine water in a conical flask on a white tile; add cyclohexene solution from a burette with swirling until colourless; record volume; repeat three times for each concentration; plot volume against concentration.',
             weak=('the end point was judged in poor light', 'use a white tile and a colourless comparison flask'),
             safety='bromine water is toxic and corrosive – use a fume cupboard, gloves and eye protection; cyclohexene is flammable'))
dataset('ch06-st3',
        dict(intro='{who} measured the carbon monoxide concentration in exhaust gas from a petrol engine at different air-to-fuel ratios (three test runs).', iv=('Air-to-fuel mass ratio', ''), xs=[11, 12, 13, 14, 15],
             dv=('CO in exhaust', '%'), f=lambda x: 8 * math.exp(-(x - 11) / 1.2) + 0.3, dp=1, trend='The carbon monoxide percentage decreases sharply as the air-to-fuel ratio increases.',
             why='With more air, there is enough oxygen for complete combustion of the hydrocarbons to CO₂; in fuel-rich mixtures incomplete combustion produces CO.'))

R.facts('ch06-st4', F(
    terms=[('alcohol', 'an organic compound containing the –OH functional group; general formula CₙH₂ₙ₊₁OH'),
           ('carboxylic acid', 'an organic compound containing the –COOH functional group'),
           ('ester', 'a compound formed when an alcohol reacts with a carboxylic acid; functional group –COO–'),
           ('fermentation', 'the anaerobic conversion of sugar into ethanol and carbon dioxide by yeast'),
           ('esterification', 'the reaction of an alcohol with a carboxylic acid, using an acid catalyst, to form an ester and water'),
           ('oxidation of ethanol', 'conversion of ethanol to ethanoic acid by oxygen (microbes) or oxidising agents')],
    facts=[('What is the functional group of the alcohols?', '–OH', ['–COOH', 'C=C', '–COO–'], 'Hydroxyl group.'),
           ('What is the name of CH₃COOH?', 'Ethanoic acid', ['Methanoic acid', 'Ethanol', 'Ethyl ethanoate'], 'Two carbons including the COOH carbon.'),
           ('Which ester forms from ethanol and ethanoic acid?', 'Ethyl ethanoate', ['Ethanoic ethylate', 'Methyl ethanoate', 'Ethyl methanoate'], 'Alcohol part named first as “ethyl”.'),
           ('What are the optimum conditions for fermentation?', 'Yeast, sugar, about 30–35 °C, no oxygen', ['Nickel catalyst at 150 °C', 'Phosphoric acid at 300 °C', 'UV light'], 'Enzymes are denatured above ~40 °C.'),
           ('Why does wine left open to the air turn sour?', 'Ethanol is oxidised to ethanoic acid', ['Ethanol turns into sugar', 'Water evaporates', 'Yeast produces more ethanol'], 'Vinegar is ethanoic acid.')],
    why=[('Explain why fermentation stops when the ethanol concentration reaches about 15%.', 'High ethanol concentrations kill the yeast (denature enzymes and damage membranes), so fermentation stops.'),
         ('Explain why esters are used in perfumes and food flavourings.', 'Many esters are volatile and have pleasant fruity smells.'),
         ('Explain why ethanoic acid is a weak acid.', 'It only partially ionises in water, so it produces fewer H⁺ ions than a strong acid of the same concentration.')],
    contrast=[('producing ethanol by fermentation', 'producing ethanol by hydration of ethene', 'Fermentation uses renewable sugar, low temperature and is slow, giving impure dilute ethanol; hydration uses non-renewable ethene from crude oil, 300 °C and high pressure, and is fast and continuous with pure ethanol.'),
              ('an alcohol', 'a carboxylic acid', 'An alcohol has the –OH group and is neutral; a carboxylic acid has the –COOH group and is a weak acid that reacts with carbonates to give CO₂.')],
    misc=[('All alcohols are safe to drink in small amounts.', 'Methanol is highly toxic and can cause blindness and death; only ethanol is in drinks and it is also harmful in excess.'),
          ('Carboxylic acids are strong acids because they are acids.', 'Carboxylic acids are weak acids that only partially ionise.')],
    cases=[('Brazil’s bioethanol programme (Proálcool, from 1975)', 'Brazil ferments sugar cane to ethanol; most cars run on flex-fuel blends, cutting oil imports and CO₂ emissions.', 'renewable fuels from fermentation', 'It shows large-scale biofuel use, though it raises land-use and deforestation concerns.')],
    evaluate=[('Bioethanol is a sustainable replacement for petrol.', ['renewable; CO₂ absorbed by crops partly balances CO₂ from burning', 'reduces dependence on oil imports'], ['uses farmland that could grow food', 'fertiliser, processing and transport emissions; possible deforestation'], 'Bioethanol from waste or non-food crops can be sustainable; from food crops on cleared land it may not be.')],
    extended=[('Compare the production of ethanol by fermentation and by hydration of ethene, and evaluate which method a country without oil reserves but with a warm climate should use.', 'Fermentation: C₆H₁₂O₆ → 2C₂H₅OH + 2CO₂; yeast, 30–35 °C, anaerobic; renewable sugar; batch process, slow, needs distillation; low energy. Hydration: C₂H₄ + H₂O → C₂H₅OH; 300 °C, 60–70 atm, H₃PO₄ catalyst; continuous, fast, pure, high atom economy; needs crude oil. Country: fermentation using sugar cane – renewable, local, no oil imports – but must manage land use.', 8)],
))


@R.add('ch06-st4', 'C2', (1, 3), 'short')
def ester_name(rng, slot):
    al = rng.choice([('methanol', 'methyl'), ('ethanol', 'ethyl'), ('propanol', 'propyl'), ('butanol', 'butyl')])
    ac = rng.choice([('methanoic acid', 'methanoate'), ('ethanoic acid', 'ethanoate'), ('propanoic acid', 'propanoate'), ('butanoic acid', 'butanoate')])
    es = f'{al[1]} {ac[1]}'
    return dict(stem=f'Name the ester formed when {al[0]} reacts with {ac[0]}, and state the other product and the catalyst.', answer=f'{es}; water; concentrated sulfuric acid',
                markingKey=f'1 {es} (alcohol part “{al[1]}” first, acid part “{ac[1]}” second); 1 water and an acid catalyst (concentrated H₂SO₄).', marks=2)


inquiry('ch06-st4',
        dict(ctx='how the temperature affects the rate of fermentation of glucose by yeast',
             iv='temperature of the water bath (15, 25, 35, 45, 55 °C)', dv='volume of CO₂ collected in a gas syringe in 20 minutes',
             cvs=[('mass of yeast (2 g)', 'more yeast ferments faster'), ('concentration and volume of glucose (50 cm³ of 10%)', 'substrate availability'), ('anaerobic conditions (layer of oil)', 'oxygen allows aerobic respiration instead'), ('pre-warming time (10 min)', 'mixture must reach the bath temperature')],
             hyp='If temperature increases up to about 35 °C, then more CO₂ will be produced, because yeast enzymes work faster; above about 45 °C the rate will fall as enzymes are denatured.',
             method='Mix 2 g yeast with 50 cm³ of 10% glucose in a flask; cover with oil; connect to a gas syringe; place in a water bath for 10 min; record the gas volume over 20 min; repeat at each temperature three times; plot volume against temperature.',
             weak=('the yeast mixture was not pre-warmed', 'leave the flask in the water bath for 10 min before starting the timing'),
             safety='hot water baths – take care; wash hands; flasks under pressure could pop bungs – use a gas syringe'))
dataset('ch06-st4',
        dict(intro='{who} measured the percentage of ethanol in a fermenting sugar solution over several days (three fermenters).', iv=('Time', 'days'), xs=[1, 3, 5, 8, 12],
             dv=('Ethanol concentration', '%'), f=lambda x: 14 * (1 - math.exp(-x / 4)), dp=1, trend='The ethanol concentration increases quickly at first and then levels off at about 13–14%.',
             why='Yeast ferments glucose to ethanol; as ethanol builds up and sugar is used up, the yeast is inhibited and then killed, so fermentation slows and stops.'))

R.facts('ch06-st5', F(
    terms=[('polymer', 'a very large molecule made by joining many small molecules (monomers) together'),
           ('monomer', 'a small molecule that can join with others to form a polymer'),
           ('addition polymerisation', 'the joining of many alkene monomers by opening their C=C bonds, with no other product'),
           ('repeat unit', 'the section of a polymer chain that repeats, shown in brackets with an n'),
           ('biodegradable', 'able to be broken down by microorganisms'),
           ('thermoplastic', 'a polymer that softens when heated and can be remoulded')],
    facts=[('Which monomer is used to make poly(ethene)?', 'Ethene', ['Ethane', 'Ethanol', 'Chloroethane'], 'C₂H₄.'),
           ('Why are most plastics non-biodegradable?', 'Microorganisms cannot break their strong C–C bonds', ['They contain water', 'They are too light', 'They are made of metal'], 'They persist for hundreds of years.'),
           ('What polymer is made from chloroethene?', 'PVC (poly(chloroethene))', ['Polystyrene', 'Polypropene', 'Nylon'], 'Used for window frames, pipes.'),
           ('What is the only product of addition polymerisation?', 'The polymer', ['The polymer and water', 'The polymer and CO₂', 'The monomer and hydrogen'], 'Atom economy = 100%.'),
           ('Which is a problem with burning plastic waste?', 'It can release toxic gases and CO₂', ['It creates more plastic', 'It produces no energy', 'It makes the plastic biodegradable'], 'e.g. HCl from PVC.')],
    why=[('Explain why poly(ethene) is unreactive even though it is made from ethene.', 'Polymerisation uses up the C=C double bonds; the polymer is saturated with only single bonds, like an alkane.'),
         ('Explain why recycling plastics is more difficult than recycling metals.', 'There are many types of plastic that must be sorted; mixed or contaminated plastics are hard to reuse; each recycling cycle shortens chains and lowers quality.'),
         ('Explain why microplastics are a concern in oceans.', 'Small pieces are eaten by plankton and fish, enter food chains, can carry toxins, and last for centuries.')],
    contrast=[('a monomer', 'a polymer', 'A monomer is a small unsaturated molecule (e.g. ethene); a polymer is a long chain formed by joining thousands of monomers (e.g. poly(ethene)).'),
              ('landfill', 'incineration of plastic waste', 'Landfill buries plastic, using land and leaving it for centuries; incineration burns it, releasing energy but producing CO₂ and possibly toxic gases.')],
    misc=[('Biodegradable plastics disappear quickly anywhere.', 'Many “biodegradable” plastics only break down in industrial composting conditions, not in the sea or soil.'),
          ('All plastics can be recycled together.', 'Different polymers must be sorted by type (resin codes), as mixed plastics produce weak, low-quality material.')],
    cases=[('Bacteria that digest PET (Ideonella sakaiensis, 2016)', 'Scientists in Japan found bacteria at a recycling plant that produce enzymes to break down PET plastic; engineered enzymes now work faster.', 'biotechnology for plastic waste', 'It could enable recycling PET back into monomers, but large-scale use is still developing.')],
    evaluate=[('Single-use plastics should be banned worldwide.', ['reduces ocean pollution and litter', 'encourages reusable alternatives'], ['some single-use plastics are essential (medical equipment, food hygiene)', 'alternatives (paper, glass) may have higher carbon footprints'], 'Bans on avoidable single-use items are justified, with exemptions for essential uses and investment in alternatives.')],
    extended=[('Describe how poly(propene) is formed from propene, drawing (describing) the repeat unit, and evaluate three methods of dealing with waste plastics.', 'n CH₂=CHCH₃ → –[CH₂–CH(CH₃)]ₙ–; C=C opens, monomers join into a long chain, high pressure/catalyst, no other product. Disposal: landfill (cheap, uses land, persists centuries, may leach); incineration with energy recovery (reduces volume, generates electricity but CO₂ and toxic gases need scrubbing); recycling (saves crude oil and energy, but needs sorting, quality decreases); also reduce/reuse.', 6)],
))


@R.add('ch06-st5', 'C2', (1, 3), 'mcq')
def monomer_poly(rng, slot):
    pr = [('ethene', 'poly(ethene)'), ('propene', 'poly(propene)'), ('chloroethene', 'poly(chloroethene) (PVC)'), ('tetrafluoroethene', 'poly(tetrafluoroethene) (PTFE)'), ('phenylethene (styrene)', 'poly(phenylethene) (polystyrene)')]
    m, p = rng.choice(pr)
    if rng.random() < 0.5:
        return mcq(rng, f'Which polymer is formed by the addition polymerisation of {m}?', p, rng.sample([b for a, b in pr if b != p], 3), f'B1 {p}')
    return mcq(rng, f'Which monomer is used to make {p}?', m, rng.sample([a for a, b in pr if a != m], 3), f'B1 {m}')


inquiry('ch06-st5',
        dict(ctx='how the type of plastic bag (conventional, “biodegradable”, compostable) affects the loss of mass when buried in compost',
             iv='type of plastic bag material', dv='percentage loss in dry mass of a 5 cm × 5 cm sample after 12 weeks in compost',
             cvs=[('sample size and thickness', 'larger samples take longer'), ('temperature and moisture of compost', 'affect microbial activity'), ('same compost source', 'microbe populations differ'), ('drying samples before weighing', 'water adds mass')],
             hyp='If the bag is compostable, then it will lose the most mass, because microorganisms in compost can break down its polymer chains, while conventional poly(ethene) is not biodegradable.',
             method='Cut, dry and weigh five 5 cm × 5 cm samples of each material; bury them in mesh bags in the same compost bin kept moist at about 25 °C; after 12 weeks retrieve, rinse, dry to constant mass and reweigh; calculate percentage mass loss; compare means.',
             weak=('samples were weighed while still damp', 'dry all samples in an oven at low temperature to constant mass before weighing'),
             safety='wear gloves when handling compost; wash hands; take care with scissors'))
dataset('ch06-st5',
        dict(intro='{who} measured the mass of a starch-based plastic sample remaining in compost over time (three samples).', iv=('Time', 'weeks'), xs=[2, 4, 6, 8, 10],
             dv=('Mass remaining', '%'), f=lambda x: 100 * math.exp(-x / 6), dp=0, trend='The percentage of mass remaining decreases with time, quickly at first and then more slowly.',
             why='Microorganisms in compost secrete enzymes that break down the starch-based polymer; as the material is used up, there is less left to digest each week.'))


# =============================================================================================
# ch07 Energetics
# =============================================================================================
R.facts('ch07-st1', F(
    terms=[('enthalpy change (ΔH)', 'the heat energy transferred in a reaction at constant pressure, in kJ/mol'),
           ('exothermic', 'a reaction that releases energy to the surroundings; ΔH is negative'),
           ('endothermic', 'a reaction that absorbs energy from the surroundings; ΔH is positive'),
           ('activation energy', 'the minimum energy colliding particles need to react'),
           ('energy profile', 'a diagram showing the energy of reactants and products and the activation energy as a reaction proceeds'),
           ('catalyst', 'a substance that speeds up a reaction by providing a pathway with lower activation energy, without being used up')],
    facts=[('What is the sign of ΔH for an exothermic reaction?', 'Negative', ['Positive', 'Zero', 'It has no sign'], 'Energy is lost by the system.'),
           ('On an energy profile for an endothermic reaction, where are the products?', 'Higher than the reactants', ['Lower than the reactants', 'At the same level', 'Below the activation energy'], 'Energy has been absorbed.'),
           ('How does a catalyst change an energy profile?', 'It lowers the activation energy peak', ['It raises the products', 'It changes ΔH', 'It removes the reactants'], 'ΔH is unchanged.'),
           ('Which reaction is endothermic?', 'Thermal decomposition of calcium carbonate', ['Combustion of methane', 'Neutralisation', 'Respiration'], 'Needs continuous heating.'),
           ('ΔH for a reaction is −890 kJ/mol. What does this tell you?', '890 kJ is released per mole reacting', ['890 kJ is absorbed per mole', 'The reaction is endothermic', 'The reaction is slow'], 'This is methane combustion.')],
    why=[('Explain why an exothermic reaction can still need heating to start.', 'The reactants need enough energy to overcome the activation energy; once started, the energy released provides activation energy for further reactions.'),
         ('Explain why a catalyst does not change the enthalpy change of a reaction.', 'It only provides an alternative pathway with lower activation energy; the energies of reactants and products are unchanged.'),
         ('Explain, in terms of energy, why photosynthesis is endothermic.', 'More energy is taken in (from light) to break bonds in CO₂ and H₂O than is released forming bonds in glucose and O₂, so energy is stored in the products.')],
    contrast=[('activation energy', 'enthalpy change', 'Activation energy is the energy barrier from reactants to the peak; enthalpy change is the overall energy difference between reactants and products.'),
              ('an exothermic energy profile', 'an endothermic energy profile', 'In an exothermic profile the products are lower than the reactants (ΔH negative); in an endothermic profile the products are higher (ΔH positive).')],
    misc=[('Catalysts increase the energy of the particles.', 'Catalysts lower the activation energy so more collisions are successful at the same temperature; they do not add energy.'),
          ('A negative ΔH means the reaction absorbs energy.', 'Negative ΔH means energy is released to the surroundings (exothermic).')],
    cases=[('Catalytic converters in cars', 'Platinum and rhodium catalysts lower the activation energy for converting CO, NOx and unburnt hydrocarbons into CO₂, N₂ and H₂O at exhaust temperatures.', 'catalysts and activation energy', 'They have greatly reduced urban air pollution since the 1990s, though they rely on rare, expensive metals.')],
    evaluate=[('Using catalysts is the most important way to make industrial processes more sustainable.', ['lower temperatures save energy and reduce CO₂', 'more selective, less waste'], ['many catalysts use scarce or toxic metals', 'renewable energy and recycling also matter'], 'Catalysts are a major tool for green chemistry, alongside renewable energy and better process design.')],
    extended=[('Draw (describe) labelled energy profiles for the combustion of methane with and without a catalyst, and explain how the catalyst affects the rate and the energy change.', 'Reactants CH₄ + 2O₂ higher; products CO₂ + 2H₂O lower; ΔH = −890 kJ/mol arrow downward; activation energy hump. Catalysed: lower hump, same reactant and product levels. Lower Ea → more particles have energy ≥ Ea → more successful collisions per second → faster rate; ΔH unchanged.', 6)],
))


@R.add('ch07-st1', 'C3', (1, 4), 'numerical')
def profile_read(rng, slot):
    r = rng.choice([100, 150, 200, 250])
    p = r + rng.choice([-180, -120, -90, 60, 80])
    peak = max(r, p) + rng.choice([60, 90, 120])
    dh = p - r
    ea = peak - r
    return dict(stem=f'On an energy profile, the reactants are at {r} kJ/mol, the products at {p} kJ/mol and the peak at {peak} kJ/mol. Calculate ΔH and the activation energy, and state whether the reaction is exothermic or endothermic.', answer=f'ΔH = {dh:+d} kJ/mol; Ea = {ea} kJ/mol; {"exothermic" if dh < 0 else "endothermic"}',
                markingKey=f'M1 ΔH = products − reactants = {p} − {r}; A1 {dh:+d} kJ/mol; A1 Ea = {peak} − {r} = {ea} kJ/mol; B1 {"exothermic (ΔH negative)" if dh < 0 else "endothermic (ΔH positive)"}.', marks=4)


inquiry('ch07-st1',
        dict(ctx='how the mass of a catalyst (manganese(IV) oxide) affects the rate of decomposition of hydrogen peroxide',
             iv='mass of manganese(IV) oxide powder (0.1, 0.2, 0.3, 0.4, 0.5 g)', dv='volume of oxygen collected in a gas syringe in the first 30 s',
             cvs=[('volume and concentration of H₂O₂ (25 cm³, 5 vol)', 'more peroxide gives more oxygen'), ('temperature', 'affects rate'), ('particle size of catalyst', 'surface area affects rate'), ('airtight connections', 'leaks reduce the volume')],
             hyp='If more catalyst is used, then the rate will increase, because there is more catalyst surface where H₂O₂ molecules can react via a lower-activation-energy pathway.',
             method='Put 25 cm³ H₂O₂ in a conical flask connected to a gas syringe; add the weighed MnO₂ and quickly insert the bung; record volume at 30 s; repeat three times for each mass; at the end filter, dry and reweigh the catalyst to show it is unchanged.',
             weak=('oxygen escaped before the bung was inserted', 'place the catalyst in a small tube inside the flask and tip it after sealing'),
             safety='hydrogen peroxide is an irritant and oxidiser – eye protection; MnO₂ is harmful – avoid inhaling powder'))
dataset('ch07-st1',
        dict(intro='{who} measured the temperature change when 50 cm³ of hydrochloric acid of different concentrations was mixed with 50 cm³ of 3.0 mol/dm³ sodium hydroxide (in excess; three trials).', iv=('Acid concentration', 'mol/dm³'), xs=[0.5, 1.0, 1.5, 2.0, 2.5],
             dv=('Temperature rise', '°C'), f=lambda x: 6.8 * x, dp=1, trend='The temperature rise is directly proportional to the acid concentration.',
             why='Neutralisation is exothermic; more concentrated acid means more moles react in the same volume, releasing proportionally more energy into the same mass of solution.'))

R.facts('ch07-st2', F(
    terms=[('bond energy', 'the energy needed to break one mole of a particular covalent bond in the gas state, in kJ/mol'),
           ('bond breaking', 'an endothermic process – energy is taken in'),
           ('bond making', 'an exothermic process – energy is released'),
           ('ΔH from bond energies', 'ΔH = total energy to break bonds in reactants − total energy released forming bonds in products'),
           ('mean bond enthalpy', 'the average energy to break a bond, averaged over many different compounds')],
    facts=[('Is breaking bonds exothermic or endothermic?', 'Endothermic', ['Exothermic', 'Neither', 'Depends on the bond'], 'Energy is needed to separate atoms.'),
           ('If more energy is released making bonds than is used breaking bonds, the reaction is…', 'exothermic', ['endothermic', 'neutral', 'slow'], 'ΔH negative.'),
           ('How many C–H bonds are broken when one molecule of methane burns?', '4', ['2', '1', '8'], 'CH₄ has four C–H bonds.'),
           ('Why are values calculated from mean bond energies only approximate?', 'Bond energies vary slightly between molecules and are for gases', ['They are always wrong', 'Bonds have no energy', 'Products have no bonds'], 'Averages are used.')],
    why=[('Explain why the combustion of hydrogen is exothermic, using bond energies.', 'Energy is needed to break H–H and O=O bonds, but more energy is released forming the strong O–H bonds in water, so overall energy is released.'),
         ('Explain why a calculated ΔH from bond energies differs from a value measured by calorimetry.', 'Mean bond energies are averages for gaseous molecules; calorimetry involves heat losses and substances in other states (e.g. liquid water).'),
         ('Explain why bonds with higher bond energy are harder to break.', 'The atoms are held more strongly by the shared electrons, so more energy is needed to separate them.')],
    contrast=[('bond breaking', 'bond making', 'Bond breaking absorbs energy (endothermic); bond making releases energy (exothermic); the balance between them gives ΔH.')],
    misc=[('Breaking bonds releases energy, which is why fuels give out heat.', 'Breaking bonds always takes in energy; fuels release energy because forming the new bonds in CO₂ and H₂O releases more.'),
          ('Strong bonds store a lot of energy that is released when they break.', 'Energy is released when strong bonds form, not when they break.')],
    evaluate=[('Hydrogen is the ideal fuel because its combustion releases energy and forms only water.', ['no CO₂ at the point of use', 'high energy per kg'], ['most hydrogen is made from methane, releasing CO₂', 'hard to store and transport (low density, explosive)'], 'Hydrogen is promising if produced by electrolysis with renewable electricity, but storage and production challenges remain.')],
    extended=[('Use bond energies to calculate ΔH for H₂ + Cl₂ → 2HCl (H–H 436, Cl–Cl 242, H–Cl 431 kJ/mol), draw (describe) the energy profile, and explain the sign.', 'Breaking: 436 + 242 = 678 kJ; making: 2 × 431 = 862 kJ; ΔH = 678 − 862 = −184 kJ/mol. Exothermic: more energy released forming bonds than absorbed breaking them; profile – products below reactants by 184 kJ/mol with activation energy hump.', 6)],
))

BE = {'C–H': 413, 'O=O': 498, 'C=O': 805, 'O–H': 464, 'H–H': 436, 'Cl–Cl': 242, 'H–Cl': 431, 'C–C': 347, 'C=C': 614, 'N≡N': 945, 'N–H': 391, 'Br–Br': 193, 'C–Br': 285}


@R.add('ch07-st2', 'C3', (2, 5), 'numerical')
def bond_dh(rng, slot):
    rx = rng.choice([
        ('CH₄ + 2O₂ → CO₂ + 2H₂O', {'C–H': 4, 'O=O': 2}, {'C=O': 2, 'O–H': 4}),
        ('H₂ + Cl₂ → 2HCl', {'H–H': 1, 'Cl–Cl': 1}, {'H–Cl': 2}),
        ('2H₂ + O₂ → 2H₂O', {'H–H': 2, 'O=O': 1}, {'O–H': 4}),
        ('N₂ + 3H₂ → 2NH₃', {'N≡N': 1, 'H–H': 3}, {'N–H': 6}),
        ('C₂H₄ + H₂ → C₂H₆', {'C=C': 1, 'C–H': 4, 'H–H': 1}, {'C–C': 1, 'C–H': 6}),
        ('C₂H₄ + Br₂ → C₂H₄Br₂', {'C=C': 1, 'C–H': 4, 'Br–Br': 1}, {'C–C': 1, 'C–H': 4, 'C–Br': 2})])
    eq, brk, mk = rx
    eb = sum(BE[b] * n for b, n in brk.items())
    em = sum(BE[b] * n for b, n in mk.items())
    dh = eb - em
    used = sorted(set(brk) | set(mk))
    data = ', '.join(f'{b} {BE[b]}' for b in used)
    return dict(stem=f'Use the bond energies (kJ/mol: {data}) to calculate ΔH for {eq}, and state whether it is exothermic or endothermic.', answer=f'ΔH = {dh:+d} kJ/mol; {"exothermic" if dh < 0 else "endothermic"}',
                markingKey=f'M1 bonds broken = {" + ".join(f"{n}({BE[b]})" for b, n in brk.items())} = {eb} kJ; M1 bonds made = {" + ".join(f"{n}({BE[b]})" for b, n in mk.items())} = {em} kJ; A1 ΔH = {eb} − {em} = {dh:+d} kJ/mol; B1 {"exothermic" if dh < 0 else "endothermic"}.', marks=4)


inquiry('ch07-st2',
        dict(ctx='how the number of carbon atoms in an alcohol affects the energy released per mole on combustion, compared with values predicted from bond energies',
             iv='alcohol (methanol, ethanol, propanol, butanol)', dv='energy released per mole calculated from the temperature rise of 100 g water',
             cvs=[('mass of water (100 g)', 'temperature rise depends on mass'), ('distance of flame to calorimeter', 'heat loss'), ('temperature rise (20 °C)', 'heat loss increases with temperature'), ('copper calorimeter with lid and draught shield', 'reduces heat loss')],
             hyp='If the alcohol has more carbon atoms, then more energy will be released per mole, by about 600–650 kJ per extra CH₂, because each extra CH₂ adds one C–C and two C–H bonds broken and more C=O and O–H bonds formed.',
             method='Weigh spirit burners; heat 100 g water in a copper can by 20 °C; reweigh burner; calculate moles burned; energy = 100 × 4.18 × 20; kJ/mol = energy ÷ moles ÷ 1000; repeat three times; compare with bond-energy predictions.',
             weak=('results were about 50% of predicted values due to heat loss', 'use a draught shield, insulated lid and a flame calorimeter, and keep the flame close to the can'),
             safety='alcohols are highly flammable – keep lids on, never refill burners near flames, eye protection'))
dataset('ch07-st2',
        dict(intro='{who} compared experimental enthalpies of combustion of alcohols with predicted values (three experimental runs each).', iv=('Number of carbon atoms', ''), xs=[1, 2, 3, 4, 5],
             dv=('Energy released', 'kJ/mol'), f=lambda x: 0.55 * (650 * x + 76), dp=0, trend='The energy released increases steadily with the number of carbon atoms, but every value is roughly half the predicted value.',
             why='Each extra CH₂ adds a similar amount of bond-making energy; experimental values are low because much heat is lost to the surroundings and combustion may be incomplete.'))

R.facts('ch07-st3', F(
    terms=[('calorimetry', 'measuring the energy transferred in a reaction from the temperature change of a known mass of water or solution'),
           ('specific heat capacity', 'the energy needed to raise the temperature of 1 g of a substance by 1 °C (water: 4.18 J/g °C)'),
           ('Q = mcΔT', 'the equation for heat transferred: mass × specific heat capacity × temperature change'),
           ('coffee-cup calorimeter', 'an insulated polystyrene cup with a lid used for reactions in solution'),
           ('heat loss', 'energy transferred to the surroundings rather than measured, the main source of error in calorimetry')],
    facts=[('Why is a polystyrene cup used for neutralisation experiments?', 'It is a good insulator, reducing heat loss', ['It conducts heat well', 'It reacts with the acid', 'It is cheaper than glass'], 'Add a lid as well.'),
           ('What value is used for the specific heat capacity of dilute aqueous solutions?', '4.18 J/g °C', ['1.00 J/g °C', '41.8 J/g °C', '0.418 J/g °C'], 'Same as water.'),
           ('What mass is used in Q = mcΔT for a reaction in 50 cm³ of solution?', 'About 50 g (mass of the solution)', ['The mass of the solid reactant', '1 g', 'The mass of the cup'], 'Density ≈ 1 g/cm³.'),
           ('How can heat loss in a calorimetry experiment be corrected?', 'Plot temperature against time and extrapolate back to the time of mixing', ['Take the first reading only', 'Use a hotter starting temperature', 'Stir less'], 'Cooling correction.')],
    why=[('Explain why measured enthalpy changes are usually smaller than data-book values.', 'Heat is lost to the surroundings and the calorimeter, so the measured temperature change is smaller than it should be.'),
         ('Explain why the solution is stirred during calorimetry.', 'To spread the heat evenly so the thermometer reading represents the whole solution.'),
         ('Explain why the temperature change, not the final temperature, is used in calculations.', 'Energy transferred depends on how much the temperature changes, not on its absolute value.')],
    contrast=[('Q (heat energy)', 'ΔH (enthalpy change)', 'Q is the energy transferred in a particular experiment (J); ΔH is the energy change per mole of reaction (kJ/mol) with a sign showing direction.'),
              ('a flame calorimeter', 'a polystyrene-cup calorimeter', 'A flame calorimeter measures energy from burning fuels; a polystyrene cup measures energy changes of reactions in solution.')],
    misc=[('In Q = mcΔT, m is the mass of the fuel or solid that reacts.', 'm is the mass of the water or solution being heated.'),
          ('If the temperature falls, Q is negative so no energy was transferred.', 'A fall in temperature shows energy was absorbed (endothermic), ΔH positive.')],
    evaluate=[('Bomb calorimeters should be used for all school calorimetry experiments.', ['very accurate, little heat loss', 'used for food energy labels'], ['very expensive and need training', 'simple calorimeters show the principles and errors well'], 'Simple calorimeters are adequate for learning; bomb calorimeters are for professional measurement.')],
    extended=[('In a neutralisation, 50 cm³ of 1.0 mol/dm³ HCl and 50 cm³ of 1.0 mol/dm³ NaOH gave a temperature rise of 6.5 °C. Calculate ΔH in kJ/mol, and describe two improvements to reduce error.', 'Q = 100 × 4.18 × 6.5 = 2717 J = 2.717 kJ; moles = 0.05; ΔH = −2.717/0.05 = −54.3 kJ/mol. Improvements: lid and second cup for insulation; record temperature over time and extrapolate to time of mixing; use a more precise thermometer/probe; pre-equilibrate both solutions to the same starting temperature.', 6)],
))


@R.add('ch07-st3', 'C3', (1, 5), 'numerical')
def calorim(rng, slot):
    k = rng.choice(['Q', 'dH', 'fuel'] if slot.d >= 3 else ['Q'])
    if k == 'Q':
        m = rng.choice([50, 100, 150, 200])
        dt = rng.choice([4.5, 6.0, 8.5, 12.0, 15.5])
        return dict(stem=f'A reaction changes the temperature of {m} g of water by {dt} °C. Calculate the heat energy transferred (c = 4.18 J/g °C).', answer=f'{g(m * 4.18 * dt)} J',
                    markingKey=f'M1 Q = mcΔT = {m} × 4.18 × {dt}; A1 {g(m * 4.18 * dt)} J.', marks=2)
    if k == 'dH':
        V = rng.choice([25, 50])
        c = rng.choice([1.0, 2.0])
        dt = rng.choice([6.2, 6.8, 13.1, 13.6]) if c == 2.0 else rng.choice([6.2, 6.8])
        Q = 2 * V * 4.18 * dt
        n = c * V / 1000
        dh = -Q / n / 1000
        return dict(stem=f'{V} cm³ of {g(c)} mol/dm³ HCl was mixed with {V} cm³ of {g(c)} mol/dm³ NaOH. The temperature rose by {dt} °C. Calculate ΔH of neutralisation in kJ/mol.', answer=f'{g(dh)} kJ/mol',
                    markingKey=f'M1 Q = {2 * V} × 4.18 × {dt} = {g(Q)} J; M1 n = {g(c)} × {V}/1000 = {g(n)} mol; M1 ΔH = −Q ÷ n ÷ 1000; A1 {g(dh)} kJ/mol (negative).', marks=4)
    fuel, M = rng.choice([('ethanol', 46), ('methanol', 32), ('propanol', 60), ('butanol', 74)])
    mb = rng.choice([0.50, 0.65, 0.80, 1.20])
    dt = rng.choice([20, 25, 30])
    Q = 100 * 4.18 * dt
    dh = -Q / (mb / M) / 1000
    return dict(stem=f'Burning {mb:.2f} g of {fuel} (M = {M} g/mol) raised the temperature of 100 g of water by {dt} °C. Calculate the enthalpy of combustion in kJ/mol.', answer=f'{g(dh)} kJ/mol',
                markingKey=f'M1 Q = 100 × 4.18 × {dt} = {g(Q)} J; M1 n = {mb:.2f} ÷ {M} = {g(mb / M)} mol; M1 ΔH = −{g(Q)} ÷ {g(mb / M)} ÷ 1000; A1 {g(dh)} kJ/mol.', marks=4)


inquiry('ch07-st3',
        dict(ctx='how the metal used affects the temperature rise in a displacement reaction with copper(II) sulfate solution',
             iv='metal powder (magnesium, zinc, iron, tin)', dv='maximum temperature rise of 25 cm³ of 0.5 mol/dm³ copper(II) sulfate',
             cvs=[('moles of metal (in excess, e.g. 0.02 mol)', 'excess ensures all copper ions react'), ('volume and concentration of CuSO₄', 'determines energy released'), ('insulated cup with lid', 'reduces heat loss'), ('stirring rate', 'spreads heat evenly')],
             hyp='If the metal is more reactive (further above copper), then the temperature rise will be larger, because the displacement reaction releases more energy per mole.',
             method='Measure 25 cm³ CuSO₄ into a polystyrene cup with lid; record temperature every 30 s for 2 min; add excess metal powder at 2.5 min, stir; record every 30 s for 6 min; plot and extrapolate to find the maximum rise; repeat three times; calculate ΔH per mole of Cu²⁺.',
             weak=('the highest reading was used without correcting for cooling', 'extrapolate the cooling curve back to the time of mixing'),
             safety='copper sulfate is harmful and an irritant – eye protection; magnesium powder is flammable'))
dataset('ch07-st3',
        dict(intro='{who} used a polystyrene cup to measure the temperature of copper sulfate solution after adding zinc powder, every minute (three trials).', iv=('Time after mixing', 'min'), xs=[1, 2, 3, 5, 7],
             dv=('Temperature', '°C'), f=lambda x: 20 + 28 * math.exp(-0.06 * x) if x >= 1 else 20, dp=1, trend='The temperature is highest just after mixing and then falls steadily as the solution cools.',
             why='The displacement reaction is exothermic and is fast, so it releases energy immediately; afterwards the solution loses heat to the surroundings, so the maximum must be found by extrapolating back to the time of mixing.'))

R.facts('ch07-st4', F(
    terms=[('electrochemical cell', 'a device that converts chemical energy into electrical energy using a redox reaction'),
           ('fuel cell', 'a cell that produces electricity continuously from a fuel (such as hydrogen) and oxygen supplied from outside'),
           ('rechargeable battery', 'a battery in which the chemical reaction can be reversed by supplying electrical energy'),
           ('energy density', 'the energy stored per kilogram (or per litre) of a fuel or battery'),
           ('lithium-ion battery', 'a rechargeable battery in which lithium ions move between electrodes; used in phones and electric vehicles'),
           ('electrolysis of water', 'splitting water into hydrogen and oxygen using electricity')],
    facts=[('What is the only product of a hydrogen–oxygen fuel cell?', 'Water', ['Carbon dioxide', 'Hydrogen peroxide', 'Methane'], '2H₂ + O₂ → 2H₂O.'),
           ('Why do non-rechargeable batteries eventually stop working?', 'The reactants are used up', ['They become hot', 'They are oxidised by air', 'Electrons are destroyed'], 'The reaction stops.'),
           ('What does a higher voltage cell usually need?', 'Electrodes made of metals with a bigger difference in reactivity', ['Larger electrodes of the same metal', 'Pure water', 'No electrolyte'], 'e.g. zinc and copper.'),
           ('Which fuel has the highest energy per kilogram?', 'Hydrogen', ['Coal', 'Wood', 'Ethanol'], 'About 142 MJ/kg.'),
           ('Why do lithium-ion batteries suit electric vehicles?', 'They are rechargeable with high energy density and low mass', ['They never wear out', 'They contain no metals', 'They release CO₂'], 'Lithium is very light.')],
    why=[('Explain why hydrogen fuel cells are not completely “zero emission”.', 'No CO₂ is produced in the vehicle, but most hydrogen is made from natural gas (releasing CO₂) and energy is used to compress and transport it.'),
         ('Explain why fuel cells can be more efficient than petrol engines.', 'They convert chemical energy directly to electrical energy without combustion, avoiding large heat losses.'),
         ('Explain why the voltage of a simple cell depends on the metals used.', 'The voltage depends on the difference in tendency of the two metals to lose electrons – their reactivity.')],
    contrast=[('a fuel cell', 'a battery', 'A fuel cell produces electricity as long as fuel and oxygen are supplied from outside; a battery stores a fixed amount of reactants and stops (or must be recharged) when they are used up.'),
              ('burning hydrogen', 'using hydrogen in a fuel cell', 'Burning releases energy as heat for engines; a fuel cell releases it directly as electricity, more efficiently.')],
    misc=[('Rechargeable batteries create energy when charged.', 'Charging stores electrical energy as chemical energy by reversing the reaction; energy is not created.'),
          ('Electric cars produce no pollution at all.', 'Batteries need mining and manufacturing, and the electricity may come from fossil fuels; tyre and brake particles also pollute.')],
    cases=[('Apollo fuel cells (1960s)', 'Apollo spacecraft used hydrogen–oxygen fuel cells for electricity, and astronauts drank the water produced.', 'fuel cells in technology', 'Showed fuel cells work reliably in demanding conditions and inspired modern hydrogen vehicles.'),
           ('Lithium mining in South America’s “lithium triangle”', 'Brine is pumped from under salt flats in Chile, Argentina and Bolivia and evaporated to extract lithium, using large amounts of water in a very dry region.', 'environmental cost of batteries', 'Battery growth brings economic benefits but water use affects local communities and ecosystems.')],
    evaluate=[('Hydrogen fuel-cell cars are a better choice than battery electric cars.', ['quick refuelling, long range', 'only water emitted from the vehicle'], ['few hydrogen stations', 'producing, compressing and transporting hydrogen wastes much energy; overall efficiency lower than batteries'], 'For cars, batteries are currently more efficient; hydrogen may suit heavy transport and long ranges.'),
              ('Governments should stop selling new petrol cars by 2030.', ['reduces CO₂ and urban air pollution', 'drives battery development'], ['charging infrastructure and electricity supply may not be ready', 'cost for consumers; battery raw material supply'], 'A 2030–2035 deadline is ambitious but achievable with investment in charging, grids and recycling.')],
    extended=[('Compare petrol, lithium-ion batteries and hydrogen fuel cells as energy sources for vehicles, considering energy density, emissions, efficiency and sustainability.', 'Petrol: very high energy density (≈46 MJ/kg), cheap infrastructure, but CO₂, NOx and particulates; engines ~25–30% efficient; finite. Li-ion: lower energy density (≈0.5–0.9 MJ/kg) – heavy, slower charging; ~85–90% efficient; no tailpipe emissions; mining and recycling issues. Fuel cells: hydrogen very high energy per kg but low per litre (storage tanks); only water at tailpipe; overall efficiency lower due to production/compression; mostly made from methane now. Judgement depends on clean electricity and use.', 8)],
))


@R.add('ch07-st4', 'C3', (1, 5), 'numerical')
def fuel_energy(rng, slot):
    k = rng.choice(['mass', 'range', 'eff'])
    if k == 'mass':
        E = rng.choice([50, 75, 100])
        a, ea = rng.choice([('hydrogen', 142), ('petrol', 46), ('ethanol', 30)])
        return dict(stem=f'A journey needs {E} MJ of energy from fuel. The energy density of {a} is {ea} MJ/kg. Calculate the mass of {a} needed.', answer=f'{g(E / ea)} kg',
                    markingKey=f'M1 mass = energy ÷ energy density = {E} ÷ {ea}; A1 {g(E / ea)} kg.', marks=2)
    if k == 'range':
        cap = rng.choice([40, 60, 75, 100])
        use = rng.choice([0.15, 0.18, 0.2])
        return dict(stem=f'An electric car has a {cap} kWh battery and uses {use} kWh per km. Estimate its range.', answer=f'{g(cap / use)} km',
                    markingKey=f'M1 {cap} ÷ {use}; A1 {g(cap / use)} km.', marks=2)
    i = rng.choice([100, 200, 500])
    e = rng.choice([25, 40, 60, 85])
    return dict(stem=f'A fuel cell releases {i} kJ of chemical energy and supplies {i * e // 100} kJ of electrical energy. Calculate its efficiency.', answer=f'{e}%',
                markingKey=f'M1 {i * e // 100} ÷ {i} × 100; A1 {e}%.', marks=2)


inquiry('ch07-st4',
        dict(ctx='how the pair of metals used as electrodes affects the voltage of a simple electrochemical cell',
             iv='metal paired with copper (magnesium, zinc, iron, lead)', dv='voltage across the electrodes measured with a high-resistance voltmeter',
             cvs=[('electrolyte and concentration (1 mol/dm³ salt solution)', 'affects voltage'), ('distance between electrodes', 'affects internal resistance and reading'), ('area of electrode in solution', 'affects current'), ('cleaned electrodes (sandpaper)', 'oxide layers reduce voltage')],
             hyp='If the metal is more reactive (further from copper in the reactivity series), then the voltage will be higher, because it has a greater tendency to lose electrons.',
             method='Clean metal strips with sandpaper; place copper and the test metal 3 cm apart in 50 cm³ of salt solution; connect to a voltmeter; record the voltage after 30 s; repeat three times with fresh solution; rank the metals.',
             weak=('the strips were placed at different depths', 'mark a line on each strip and dip to the same depth'),
             safety='magnesium is flammable; wash hands after handling lead; eye protection'))
dataset('ch07-st4',
        dict(intro='{who} measured the voltage of a phone battery as it was discharged at a constant current (three batteries).', iv=('Time', 'h'), xs=[1, 3, 5, 7, 9],
             dv=('Voltage', 'V'), f=lambda x: 4.1 - 0.06 * x - (0.5 if x > 8 else 0), dp=2, trend='The voltage falls slowly and steadily for most of the time and then drops more quickly near the end.',
             why='As the reactants in the cell are used up, the voltage falls; when they are almost exhausted the voltage drops sharply and the battery needs recharging.'))


# =============================================================================================
# ch08 Reversible Reactions and Equilibrium
# =============================================================================================
R.facts('ch08-st1', F(
    terms=[('reversible reaction', 'a reaction in which products can react to re-form the reactants, shown by ⇌'),
           ('dynamic equilibrium', 'the state of a reversible reaction in a closed system where the forward and backward rates are equal and concentrations stay constant'),
           ('closed system', 'a system in which no substances can enter or leave'),
           ('position of equilibrium', 'the relative amounts of reactants and products at equilibrium'),
           ('hydrated salt', 'a salt containing water of crystallisation, e.g. blue CuSO₄·5H₂O')],
    facts=[('What does the symbol ⇌ show?', 'The reaction is reversible', ['The reaction is fast', 'The reaction is exothermic', 'The reaction has finished'], 'Can go both ways.'),
           ('At dynamic equilibrium, what is true about the rates?', 'The forward and backward rates are equal', ['Both reactions have stopped', 'The forward rate is zero', 'The backward rate is faster'], 'Reactions continue.'),
           ('What happens when water is added to white anhydrous copper sulfate?', 'It turns blue and gets hot', ['It turns white and cold', 'It turns green', 'No change'], 'The reverse of dehydration – exothermic.'),
           ('Why can equilibrium only be reached in a closed system?', 'Otherwise products or reactants escape and the reverse reaction cannot keep pace', ['Open systems are too hot', 'Catalysts need closed systems', 'Light is needed'], 'e.g. gases escaping.')],
    why=[('Explain why concentrations stay constant at equilibrium even though reactions are still happening.', 'The forward and backward reactions happen at the same rate, so reactants are made as fast as they are used.'),
         ('Explain why heating blue copper sulfate is endothermic but adding water to anhydrous copper sulfate is exothermic.', 'In a reversible reaction the energy change in one direction is equal and opposite to the other.'),
         ('Explain why a reversible reaction in an open beaker may go to completion.', 'If a gaseous product escapes, the backward reaction cannot occur, so the forward reaction continues until the reactant is used up.')],
    contrast=[('a reversible reaction', 'an irreversible reaction', 'A reversible reaction can go both ways and may reach equilibrium; an irreversible reaction goes essentially to completion, e.g. combustion.'),
              ('static equilibrium', 'dynamic equilibrium', 'In static equilibrium nothing is moving (a balanced seesaw); in dynamic equilibrium forward and backward reactions continue at equal rates.')],
    misc=[('At equilibrium there are equal amounts of reactants and products.', 'Equal rates, not equal amounts; the position may lie towards reactants or products.'),
          ('At equilibrium the reaction has stopped.', 'Both reactions continue at equal rates – the equilibrium is dynamic.')],
    cases=[('Haemoglobin and oxygen', 'Haemoglobin binds oxygen reversibly: in the lungs (high O₂) oxyhaemoglobin forms; in respiring tissues (low O₂) oxygen is released.', 'reversible reactions in the body', 'A reversible equilibrium allows the same molecule to load and unload oxygen.')],
    evaluate=[('The “two beakers of water” model is a good way to explain dynamic equilibrium.', ['shows rates becoming equal and levels constant while transfer continues'], ['beakers do not show particles or energy changes', 'can wrongly suggest equal amounts'], 'It is a helpful model for dynamic equilibrium, but its limitations should be discussed.')],
    extended=[('Describe what happens to the rates and concentrations from the start of a reversible reaction until dynamic equilibrium is reached, and explain why this only happens in a closed system.', 'At start only reactants: forward rate high, backward zero. As reactants are used, forward rate falls; products build up, backward rate rises. Eventually rates are equal – concentrations constant – dynamic equilibrium; both reactions continue. A closed system is needed so that no reactants or products escape; otherwise the backward reaction cannot balance the forward.', 6)],
))
inquiry('ch08-st1',
        dict(ctx='how the temperature affects the colour of an equilibrium mixture of cobalt chloride complexes',
             iv='temperature of the water bath (0, 20, 40, 60, 80 °C)', dv='absorbance of the solution at 650 nm (blue complex) measured with a colorimeter',
             cvs=[('concentration of cobalt chloride and HCl', 'changes equilibrium position'), ('volume in each cuvette', 'path length affects absorbance'), ('time at each temperature (5 min)', 'equilibrium must be re-established'), ('calibration with a blank', 'colorimeter drift')],
             hyp='If the temperature increases, then the solution will become more blue (higher absorbance), because the forward reaction forming the blue complex is endothermic.',
             method='Prepare a pink cobalt chloride solution in hydrochloric acid; pour equal volumes into tubes; place in water baths at each temperature for 5 min; transfer quickly to cuvettes; measure absorbance at 650 nm; repeat three times; plot absorbance against temperature.',
             weak=('the samples cooled while being transferred', 'use a temperature-controlled cuvette holder or read immediately'),
             safety='cobalt chloride is toxic and a possible carcinogen – gloves, eye protection, avoid skin contact; concentrated HCl in a fume cupboard'))
dataset('ch08-st1',
        dict(intro='{who} monitored the concentration of product in a reversible reaction in a sealed flask over time (three runs).', iv=('Time', 'min'), xs=[2, 4, 8, 12, 20],
             dv=('Product concentration', 'mol/dm³'), f=lambda x: 0.60 * (1 - math.exp(-x / 4)), dp=3, trend='The product concentration increases quickly at first, then more slowly, and becomes constant at about 0.6 mol/dm³.',
             why='As products build up the backward reaction speeds up and the forward reaction slows; when their rates are equal, dynamic equilibrium is reached and concentrations stay constant.'))

R.facts('ch08-st2', F(
    terms=[('Le Chatelier’s principle', 'if a system at equilibrium is disturbed, the position of equilibrium shifts to oppose the change'),
           ('shift to the right', 'the equilibrium position moves towards the products'),
           ('effect of pressure', 'increasing pressure shifts equilibrium towards the side with fewer moles of gas'),
           ('effect of temperature', 'increasing temperature shifts equilibrium in the endothermic direction'),
           ('effect of concentration', 'adding a reactant shifts equilibrium towards the products, using it up')],
    facts=[('For N₂ + 3H₂ ⇌ 2NH₃, what happens to the yield of ammonia if pressure is increased?', 'It increases', ['It decreases', 'No change', 'The reaction stops'], '4 moles of gas → 2 moles.'),
           ('The forward reaction is exothermic. What happens to the yield if temperature is increased?', 'It decreases', ['It increases', 'No change', 'It doubles'], 'Equilibrium shifts in the endothermic direction.'),
           ('How does a catalyst affect the position of equilibrium?', 'It has no effect; equilibrium is reached faster', ['It shifts it to the right', 'It shifts it to the left', 'It increases yield'], 'Both rates increase equally.'),
           ('For H₂ + I₂ ⇌ 2HI (all gases), what is the effect of increasing pressure on the yield?', 'No effect', ['Increases yield', 'Decreases yield', 'Stops the reaction'], 'Equal moles of gas on both sides.')],
    why=[('Explain why removing ammonia from the reaction mixture increases the yield.', 'Removing a product lowers its concentration; the equilibrium shifts to the right to replace it, converting more reactants.'),
         ('Explain, using Le Chatelier’s principle, why the colour of brown NO₂ ⇌ colourless N₂O₄ fades when pressure is increased.', 'The equilibrium shifts towards N₂O₄ (fewer moles of gas) to reduce the pressure, so less brown NO₂ is present (after the initial darkening from compression).'),
         ('Explain why a catalyst is still useful in reversible reactions even though it does not change the yield.', 'It allows equilibrium to be reached much faster, so more product is made per hour, or lower temperatures can be used.')],
    contrast=[('the position of equilibrium', 'the rate of reaching equilibrium', 'The position (yield) depends on concentration, pressure and temperature; the rate depends on temperature, pressure, concentration and catalysts.')],
    misc=[('Increasing temperature always increases yield.', 'It increases yield only if the forward reaction is endothermic; for exothermic forward reactions the yield falls.'),
          ('A catalyst increases the amount of product at equilibrium.', 'A catalyst speeds up both directions equally so the yield is unchanged; equilibrium is reached sooner.')],
    evaluate=[('Le Chatelier’s principle can be used to predict exactly how much product will form.', ['correctly predicts the direction of shift', 'useful for choosing conditions'], ['it is qualitative – it does not give amounts', 'equilibrium constants are needed for quantitative predictions'], 'It is a powerful qualitative tool, but quantitative yields require equilibrium constant calculations.')],
    extended=[('For 2SO₂(g) + O₂(g) ⇌ 2SO₃(g), ΔH = −196 kJ/mol, predict and explain the effect on the yield of SO₃ of (a) increasing temperature, (b) increasing pressure, (c) adding a catalyst, (d) adding more O₂.', '(a) yield decreases – equilibrium shifts in endothermic (backward) direction to absorb heat; (b) yield increases – 3 moles of gas → 2, shift to fewer moles; (c) no change in yield, faster attainment; (d) yield increases – shifts right to use up added O₂.', 6)],
))


@R.add('ch08-st2', 'C2', (2, 4), 'mcq')
def le_chat(rng, slot):
    rx = rng.choice([('N₂(g) + 3H₂(g) ⇌ 2NH₃(g)', 'exothermic', 4, 2), ('2SO₂(g) + O₂(g) ⇌ 2SO₃(g)', 'exothermic', 3, 2), ('N₂O₄(g) ⇌ 2NO₂(g)', 'endothermic', 1, 2),
                     ('CH₄(g) + H₂O(g) ⇌ CO(g) + 3H₂(g)', 'endothermic', 2, 4), ('H₂(g) + I₂(g) ⇌ 2HI(g)', 'exothermic', 2, 2)])
    eq, fw, l, r = rx
    ch = rng.choice(['raise T', 'raise P'])
    if ch == 'raise T':
        corr = 'Shifts to the right; more product' if fw == 'endothermic' else 'Shifts to the left; less product'
        q = 'temperature is increased'
    else:
        corr = 'No change in position' if l == r else ('Shifts to the right; more product' if r < l else 'Shifts to the left; less product')
        q = 'pressure is increased'
    opts = ['Shifts to the right; more product', 'Shifts to the left; less product', 'No change in position', 'The reaction stops']
    return mcq(rng, f'For {eq} (forward reaction {fw}), what happens to the position of equilibrium if the {q}?', corr, [o for o in opts if o != corr], f'B1 {corr}')


inquiry('ch08-st2',
        dict(ctx='how the concentration of added iron(III) ions affects the colour of the iron(III) thiocyanate equilibrium',
             iv='volume of 0.1 mol/dm³ iron(III) chloride added (0, 1, 2, 3, 4 drops to 10 cm³ mixture)', dv='absorbance of the red complex at 470 nm',
             cvs=[('starting concentration of the equilibrium mixture', 'affects absorbance'), ('temperature', 'changes equilibrium position'), ('total volume (top up with water)', 'dilution changes absorbance'), ('time before reading (2 min)', 'equilibrium must be re-established')],
             hyp='If more Fe³⁺ is added, then the mixture will become darker red, because the equilibrium Fe³⁺ + SCN⁻ ⇌ FeSCN²⁺ shifts to the right to use up the added Fe³⁺.',
             method='Prepare an equilibrium mixture of dilute iron(III) chloride and potassium thiocyanate; put 10 cm³ into five tubes; add 0–4 drops of iron(III) chloride, then water to keep the volume equal; mix and wait 2 min; measure absorbance; repeat three times.',
             weak=('different volumes were compared without topping up', 'add water so every tube has the same total volume'),
             safety='iron(III) chloride is corrosive and potassium thiocyanate harmful – gloves and eye protection'))
dataset('ch08-st2',
        dict(intro='{who} analysed data for the percentage of ammonia at equilibrium at 400 °C at different pressures (three data sources).', iv=('Pressure', 'atm'), xs=[50, 100, 200, 300, 400],
             dv=('Ammonia at equilibrium', '%'), f=lambda x: 60 * x / (x + 180), dp=0, trend='The percentage of ammonia at equilibrium increases with pressure, but the increase gets smaller at higher pressures.',
             why='The forward reaction N₂ + 3H₂ ⇌ 2NH₃ reduces the number of gas moles from 4 to 2, so higher pressure shifts equilibrium to the right (Le Chatelier).'))

R.facts('ch08-st3', F(
    terms=[('Haber process', 'the industrial process that makes ammonia from nitrogen and hydrogen: N₂ + 3H₂ ⇌ 2NH₃'),
           ('compromise conditions', 'conditions chosen to balance yield, rate, cost and safety, e.g. 450 °C and 200 atm for ammonia'),
           ('iron catalyst', 'the catalyst used in the Haber process to increase the rate'),
           ('recycling unreacted gases', 'returning unreacted nitrogen and hydrogen to the reactor to increase overall conversion'),
           ('Contact process', 'the industrial process for sulfuric acid, including 2SO₂ + O₂ ⇌ 2SO₃ with a vanadium(V) oxide catalyst')],
    facts=[('Where does the nitrogen for the Haber process come from?', 'The air', ['Natural gas', 'Water', 'Crude oil'], 'Air is 78% nitrogen.'),
           ('Where does most of the hydrogen for the Haber process come from?', 'Natural gas (methane) reacted with steam', ['The air', 'Ammonia', 'Seawater evaporation'], 'Steam reforming – releases CO₂.'),
           ('Why is 450 °C used instead of a lower temperature?', 'A lower temperature would give a higher yield but a much slower rate', ['Higher temperature gives higher yield', 'The catalyst melts below 450 °C', 'Ammonia only forms above 450 °C'], 'Compromise.'),
           ('Why is a pressure of about 200 atm used rather than 1000 atm?', 'Higher pressures are very expensive and dangerous', ['Higher pressure lowers the yield', 'The catalyst does not work at high pressure', 'Ammonia is a liquid at high pressure'], 'Equipment cost and safety.'),
           ('How is ammonia removed from the reaction mixture?', 'It is cooled and condensed into a liquid', ['It is filtered', 'It is dissolved in oil', 'It is burned'], 'Unreacted gases are recycled.')],
    why=[('Explain why only about 15% of the gases are converted to ammonia in each pass, yet the overall conversion is about 97%.', 'Unreacted nitrogen and hydrogen are recycled through the reactor many times, so eventually almost all are converted.'),
         ('Explain why the Haber process is important for world food supply.', 'Ammonia is used to make nitrogen fertilisers (e.g. ammonium nitrate); fertilisers greatly increase crop yields – about half the world’s food depends on them.'),
         ('Explain the environmental impacts of the Haber process.', 'It uses about 1–2% of world energy and produces CO₂ from making hydrogen from methane; fertiliser run-off causes eutrophication and N₂O emissions.')],
    contrast=[('rate', 'yield in the Haber process', 'Higher temperature increases the rate but decreases the yield (exothermic forward reaction); higher pressure increases both but costs more.'),
              ('the Haber process', 'the Contact process', 'The Haber process makes ammonia (N₂ + 3H₂, iron catalyst, ~450 °C, ~200 atm); the Contact process makes sulfuric acid via SO₃ (V₂O₅ catalyst, ~450 °C, ~1–2 atm).')],
    misc=[('Industry always uses conditions that give the highest yield.', 'Industry chooses compromise conditions that give an acceptable yield quickly and economically and safely.'),
          ('The iron catalyst increases the yield of ammonia.', 'The catalyst increases the rate only; it does not change the equilibrium yield.')],
    cases=[('Fritz Haber and Carl Bosch (1909–1913)', 'Haber developed the ammonia synthesis in the laboratory; Bosch scaled it up industrially at BASF. Haber also led Germany’s chemical weapons programme in World War I.', 'science, benefits and ethics', 'The process feeds billions but was also used to make explosives – showing that science can be used for good and harm.'),
           ('Green ammonia projects', 'New plants make hydrogen by electrolysis using wind or solar power, so ammonia can be produced with low CO₂ emissions; ammonia is also being tested as a shipping fuel.', 'making industrial chemistry sustainable', 'Shows how the Haber process could be decarbonised.')],
    evaluate=[('Fritz Haber should be remembered more as a hero than a villain.', ['his process prevents mass starvation by enabling fertiliser production', 'Nobel Prize in Chemistry 1918'], ['he developed and personally supervised poison gas attacks', 'his process also supplied explosives for war'], 'Haber’s legacy is mixed: the process is enormously beneficial, but his role in chemical warfare must not be forgotten.'),
              ('The Haber process should switch entirely to “green” hydrogen as soon as possible.', ['removes about 1% of world CO₂ emissions', 'uses renewable electricity'], ['green hydrogen is currently more expensive', 'needs huge renewable capacity'], 'Switching is essential for net zero, but needs investment and a phased transition to keep fertiliser affordable.')],
    extended=[('Explain the choice of conditions (temperature, pressure, catalyst, removal of ammonia) in the Haber process, using ideas about rate, equilibrium position and cost.', 'Exothermic forward reaction: low T favours yield but slow → compromise 450 °C. Fewer moles of gas on right: high P favours yield and rate, but expensive and dangerous → ~200 atm. Iron catalyst: faster rate at lower temperature, no effect on yield. Ammonia condensed and removed; unreacted gases recycled → ~97% overall conversion. Conditions balance acceptable yield, fast rate, and cost/safety.', 8)],
))


@R.add('ch08-st3', 'C3', (1, 5), 'numerical')
def haber_calc(rng, slot):
    k = rng.choice(['conv', 'mass', 'recycle'] if slot.d >= 3 else ['conv', 'mass'])
    if k == 'conv':
        p = rng.choice([12, 15, 18, 20])
        n = rng.choice([100, 500, 1000])
        return dict(stem=f'In one pass through the reactor, {p}% of the nitrogen is converted to ammonia. If {n} tonnes of nitrogen enter, how much nitrogen is unconverted and recycled?', answer=f'{g(n * (100 - p) / 100)} tonnes',
                    markingKey=f'M1 {100 - p}% unconverted; M1 {n} × {100 - p}/100; A1 {g(n * (100 - p) / 100)} tonnes.', marks=2)
    if k == 'mass':
        t = rng.choice([14, 28, 56, 140])
        nh3 = t / 28 * 2 * 17
        return dict(stem=f'N₂ + 3H₂ ⇌ 2NH₃. Calculate the maximum mass of ammonia that could be made from {t} tonnes of nitrogen (Mr N₂ = 28, NH₃ = 17).', answer=f'{g(nh3)} tonnes',
                    markingKey=f'M1 moles ratio: 28 t N₂ → 2 × 17 = 34 t NH₃; M1 {t} × 34 ÷ 28; A1 {g(nh3)} tonnes.', marks=3)
    p = rng.choice([15, 20, 25])
    passes = rng.choice([3, 5, 10])
    left = (1 - p / 100) ** passes
    return dict(stem=f'Each pass converts {p}% of the remaining reactants to ammonia, and unreacted gases are recycled. What percentage of the original reactants has been converted after {passes} passes?', answer=f'{g((1 - left) * 100)}%',
                markingKey=f'M1 fraction left = (1 − {p / 100:g})^{passes} = {g(left)}; M1 converted = 1 − {g(left)}; A1 {g((1 - left) * 100)}%.', marks=3)


inquiry('ch08-st3',
        dict(ctx='how temperature affects the equilibrium yield of a model gas-phase reaction, using published data and a simulation',
             iv='temperature set in the simulation (300, 350, 400, 450, 500 °C) at 200 atm', dv='equilibrium percentage of ammonia and time to reach 95% of equilibrium',
             cvs=[('pressure (200 atm)', 'pressure also affects yield'), ('initial N₂ : H₂ ratio (1 : 3)', 'ratio affects yield'), ('catalyst setting (on)', 'affects rate'), ('same simulation version and settings', 'models differ')],
             hyp='If the temperature increases, then the equilibrium yield will decrease but equilibrium will be reached faster, because the forward reaction is exothermic but all reactions speed up at higher temperatures.',
             method='Use a validated Haber process simulation; set pressure 200 atm and catalyst on; run at each temperature; record equilibrium % NH₃ and time to approach equilibrium; repeat runs; plot both against temperature to show the compromise; compare with published industrial data.',
             weak=('only one variable (yield) was recorded, so the compromise could not be shown', 'record both the yield and the rate (time to equilibrium) at each temperature'),
             safety='no physical hazards in a simulation; consider screen breaks; real ammonia is toxic – never attempt high-pressure reactions in school'))
dataset('ch08-st3',
        dict(intro='{who} analysed published data for the equilibrium yield of ammonia at 200 atm at different temperatures (three sources).', iv=('Temperature', '°C'), xs=[300, 350, 400, 450, 500],
             dv=('Ammonia at equilibrium', '%'), f=lambda x: 63 * math.exp(-(x - 300) / 180), dp=0, trend='The equilibrium yield of ammonia decreases as temperature increases.',
             why='The forward reaction is exothermic; raising the temperature shifts the equilibrium in the endothermic (backward) direction, so less ammonia is present at equilibrium.'))
evx(R, 'ch08-st2', ('Chemical engineers should always choose conditions that give the highest equilibrium yield.', ['less unreacted material to separate and recycle'], ['high-yield conditions may be very slow (low temperature) or dangerous and costly (very high pressure)', 'rate and energy cost decide profitability'], 'Engineers choose compromise conditions that balance yield, rate, cost and safety, not just maximum yield.'),
    ('Le Chatelier’s principle is just common sense and does not need to be taught as a scientific principle.', ['the idea of a system opposing change is intuitive'], ['predictions about pressure, temperature and moles of gas are not obvious', 'it is essential for designing industrial processes and understanding biological equilibria'], 'It is a powerful, testable principle with many applications and should be taught explicitly.'))
exx(R, 'ch08-st2', ('The equilibrium CO(g) + 2H₂(g) ⇌ CH₃OH(g) has ΔH = −91 kJ/mol. Recommend the conditions of temperature and pressure for making methanol industrially, explaining the effect of each on yield and rate, and the role of a catalyst.', 'Pressure: 3 moles of gas → 1, so high pressure increases yield and rate; but costly and hazardous – choose moderately high (50–100 atm). Temperature: exothermic forward reaction, so low temperature gives high yield but slow rate – compromise about 250 °C. Catalyst (copper/zinc oxide) increases rate so a lower temperature can be used; no effect on yield. Remove methanol by condensing and recycle unreacted gases.', 6))
R.f['ch07-st2'].why = list(R.f['ch07-st2'].why) + [('Explain why the C≡O bond in carbon monoxide is harder to break than the C–O bond in methanol.', 'A triple bond has three shared pairs of electrons holding the atoms together, so much more energy is needed to break it than a single bond.')]
R.f['ch07-st2'].contrast = list(R.f['ch07-st2'].contrast) + [('a measured enthalpy change', 'a value calculated from mean bond energies', 'A measured value comes from an experiment on the real substances (with heat losses); a bond-energy value is calculated from average bond strengths in gaseous molecules, so both are approximations in different ways.')]


# =============================================================================================
# ch09 Energy Resources and Electricity Generation
# =============================================================================================
R.facts('ch09-st1', F(
    terms=[('renewable resource', 'an energy resource that is replenished naturally on a human timescale, e.g. solar, wind, hydro, tidal, geothermal, biomass'),
           ('non-renewable resource', 'an energy resource that will run out, e.g. coal, oil, natural gas, uranium'),
           ('base-load supply', 'the minimum continuous electricity demand, met by reliable stations running all the time'),
           ('intermittency', 'the variation in output of resources such as wind and solar that depend on weather and time of day'),
           ('energy storage', 'storing surplus electricity, e.g. pumped hydro or batteries, to use when demand is high'),
           ('capacity factor', 'actual energy produced in a year ÷ the energy that would be produced at full power all year, as a percentage')],
    facts=[('Which resource is renewable but can be predicted months in advance?', 'Tidal power', ['Wind power', 'Solar power', 'Coal'], 'Tides follow the Moon’s orbit.'),
           ('Which resource provides reliable base-load power with very low CO₂ emissions?', 'Nuclear power', ['Wind power', 'Solar power', 'Diesel generators'], 'But produces radioactive waste.'),
           ('Which resource can respond fastest to a sudden increase in demand?', 'Pumped-storage hydroelectricity', ['Nuclear', 'Coal', 'Tidal'], 'Within seconds to minutes.'),
           ('What is a disadvantage of tidal barrages?', 'They flood estuary habitats used by birds and fish', ['They emit CO₂', 'They only work at night', 'They are non-renewable'], 'High building cost too.'),
           ('Why is biomass considered renewable?', 'Plants can be regrown within years', ['It produces no CO₂', 'It never runs out without replanting', 'It is made from fossils'], 'Only if replanted.')],
    why=[('Explain why a country cannot rely only on solar and wind power without storage.', 'Their output varies with weather and time of day and may not match demand, so energy must be stored or supplied by other sources when output is low.'),
         ('Explain why nuclear power is non-renewable but low-carbon.', 'Uranium is a finite resource, but fission produces no CO₂, so emissions come only from construction, mining and processing.'),
         ('Explain why gas-fired power stations are often used to balance supply and demand.', 'They can start up and change output quickly, unlike nuclear or coal stations.')],
    contrast=[('wind power', 'solar power', 'Wind power uses moving air to turn turbines, works day and night but varies with wind speed; solar power uses photovoltaic cells (or heat), only works in daylight and varies with cloud cover and season.'),
              ('a renewable resource', 'a sustainable resource', 'A renewable resource is naturally replenished; a sustainable resource is used in a way that does not harm future generations – renewables can be unsustainable if they damage ecosystems.')],
    misc=[('Renewable energy is always cheaper than fossil fuels.', 'New wind and solar are now often the cheapest electricity, but costs depend on location, storage and grid needs.'),
          ('Renewable resources have no environmental impact.', 'They affect landscapes, wildlife, land use and need materials such as metals for turbines and panels.')],
    cases=[('Germany’s Energiewende', 'Germany expanded wind and solar to over 40% of electricity and phased out nuclear in 2023, but relied on coal and gas for backup during the transition.', 'balancing an energy transition', 'Shows the challenges of intermittency, costs and policy trade-offs.')],
    evaluate=[('Nuclear power should be a major part of every country’s plan to reach net zero.', ['reliable low-carbon base load', 'small land area per MWh'], ['high construction cost and long build times', 'radioactive waste and accident risk', 'renewables plus storage are getting cheaper'], 'Nuclear can help some countries decarbonise, but cost and waste issues mean it is not right for every country.'),
              ('Wind farms should be built in national parks if they are the windiest locations.', ['more electricity per turbine', 'helps tackle climate change, which also threatens parks'], ['spoils protected landscapes and tourism', 'may harm wildlife', 'offshore sites are alternatives'], 'National parks should generally be protected; offshore and less sensitive windy sites should be prioritised.')],
    extended=[('Evaluate the suitability of wind, solar, nuclear and gas for supplying a large city’s electricity, considering reliability, cost, emissions and environmental impact.', 'Wind: cheap, renewable, no CO₂, intermittent, needs land/sea and storage. Solar: cheap, modular, only daytime, seasonal. Nuclear: reliable base load, very low CO₂, expensive and slow to build, waste and risk. Gas: flexible, reliable, cheaper to build, but CO₂ and finite. Best: mix – renewables for bulk energy, storage and some flexible low-carbon or gas backup, possibly nuclear base load.', 8)],
))


@R.add('ch09-st1', 'C3', (1, 5), 'numerical')
def cap_factor(rng, slot):
    k = rng.choice(['cf', 'energy'])
    P = rng.choice([2, 3, 5, 8])
    cfv = rng.choice([25, 30, 35, 45])
    E = P * 8760 * cfv / 100
    if k == 'energy':
        return dict(stem=f'A {P} MW wind turbine has a capacity factor of {cfv}%. Calculate the energy it produces in a year in MWh (1 year = 8760 h).', answer=f'{g(E, 4)} MWh',
                    markingKey=f'M1 maximum = {P} × 8760 = {P * 8760} MWh; M1 × {cfv}/100; A1 {g(E, 4)} MWh.', marks=3)
    return dict(stem=f'A {P} MW solar farm produced {g(E, 4)} MWh in a year. Calculate its capacity factor (1 year = 8760 h) and suggest why it is well below 100%.', answer=f'{cfv}%; it produces nothing at night and less on cloudy days and in winter',
                markingKey=f'M1 maximum = {P} × 8760 = {P * 8760} MWh; M1 {g(E, 4)} ÷ {P * 8760} × 100; A1 {cfv}%; B1 night/cloud/season.', marks=4)


inquiry('ch09-st1',
        dict(ctx='how the number of blades on a model wind turbine affects its power output',
             iv='number of blades (2, 3, 4, 6)', dv='power output = V²/R across a fixed 10 Ω resistor',
             cvs=[('wind speed from the fan (same setting and distance)', 'power depends strongly on wind speed'), ('blade size, shape and angle', 'affect the force on blades'), ('the same generator and resistor', 'affect the output'), ('time for speed to stabilise (30 s)', 'output must be steady')],
             hyp='If the number of blades increases from 2 to 3, then the power output will increase, but further blades will add little or reduce power, because extra blades add mass and air turbulence.',
             method='Fix the turbine 1 m from a fan; fit each blade set (equal blades, same pitch); switch on the fan and wait 30 s; record the voltage across a 10 Ω resistor; calculate power; repeat three times; plot power against number of blades.',
             weak=('the fan airflow was uneven, so moving the turbine slightly changed the reading', 'mark the turbine position and use a honeycomb straightener in front of the fan'),
             safety='keep fingers away from spinning blades; secure the turbine; do not overload the fan socket'))
dataset('ch09-st1',
        dict(intro='{who} measured the output of a small solar panel at different times of day (three sunny days).', iv=('Hours after sunrise', 'h'), xs=[1, 3, 6, 9, 11],
             dv=('Power output', 'W'), f=lambda x: 2 + 48 * math.sin(math.pi * x / 12), dp=1, trend='The power output rises from low values after sunrise to a maximum around midday (about 6 h after sunrise) and then falls again.',
             why='Around midday the Sun is highest, so light strikes the panel more directly and passes through less atmosphere; light intensity per square metre is greatest.'))

R.facts('ch09-st2', F(
    terms=[('turbine', 'a set of blades turned by steam, water or wind that drives a generator'),
           ('generator', 'a device that uses electromagnetic induction to convert kinetic energy into electrical energy'),
           ('boiler', 'where fuel burns (or nuclear fission occurs) to heat water into high-pressure steam'),
           ('cooling tower', 'a structure that condenses steam back into water by transferring thermal energy to the air'),
           ('efficiency', 'useful energy output ÷ total energy input × 100'),
           ('combined heat and power (CHP)', 'a power station that uses its waste heat to warm nearby buildings, increasing overall efficiency')],
    facts=[('What is the correct order of energy transfers in a coal power station?', 'chemical → thermal → kinetic → electrical', ['thermal → chemical → electrical → kinetic', 'electrical → kinetic → thermal → chemical', 'kinetic → chemical → thermal → electrical'], 'Boiler → turbine → generator.'),
           ('What is the typical efficiency of a coal-fired power station?', 'About 35–40%', ['About 90%', 'About 10%', '100%'], 'Most energy is lost as heat.'),
           ('Where is most energy wasted in a thermal power station?', 'As heat in the cooling water and flue gases', ['In the transmission cables only', 'In the generator magnets', 'In the turbine blades as sound'], 'Condenser losses.'),
           ('Which power station type does not use a turbine?', 'Solar photovoltaic', ['Nuclear', 'Gas', 'Hydroelectric'], 'PV cells convert light directly.'),
           ('Why do combined-cycle gas turbine stations reach about 60% efficiency?', 'Hot exhaust from the gas turbine is used to make steam for a second turbine', ['They burn coal as well', 'They have no generator', 'They run at low temperature'], 'Two stages of energy use.')],
    why=[('Explain why thermal power stations are usually built next to rivers or the sea.', 'They need large amounts of water to cool and condense the steam after it passes through the turbines.'),
         ('Explain why CHP schemes increase the overall efficiency of a power station.', 'Waste heat that would be released to the air or river is used to heat buildings, so a greater share of the fuel’s energy is useful.'),
         ('Explain why a nuclear power station and a coal power station have similar turbines and generators.', 'Both heat water to make high-pressure steam that turns a turbine linked to a generator; only the heat source differs.')],
    contrast=[('a turbine', 'a generator', 'A turbine converts the kinetic energy of steam, water or wind into rotation; the generator uses that rotation to induce an electrical current.'),
              ('a coal power station', 'a hydroelectric power station', 'A coal station burns fuel to make steam to drive turbines (about 35% efficient, CO₂ emissions); a hydroelectric station uses falling water to turn turbines directly (about 90% efficient, no fuel).')],
    misc=[('Power stations produce energy.', 'Power stations transfer energy from one store (chemical, nuclear, kinetic) into electrical energy; they do not create energy.'),
          ('The steam from cooling towers is pollution.', 'The visible plume is mostly condensed water vapour; the main pollution is CO₂ and other gases from the chimney.')],
    cases=[('Three Gorges Dam, China', 'The world’s largest power station (22.5 GW) uses the Yangtze river; it reduces coal use but displaced about 1.3 million people and changed river ecosystems.', 'large-scale hydroelectricity', 'Shows the trade-off between clean electricity and social and environmental costs.')],
    evaluate=[('Building more hydroelectric dams is the best way to provide clean electricity.', ['reliable, flexible, very efficient, long life', 'can store energy (pumped storage)'], ['floods valleys, displaces people, blocks fish migration', 'methane from rotting vegetation in reservoirs', 'suitable sites are limited'], 'Hydroelectricity is valuable where sites are suitable and impacts are managed, but cannot meet all needs.')],
    extended=[('Describe how a gas-fired power station generates electricity, draw (describe) a Sankey diagram for a 40% efficient station with 1000 MJ input, and suggest two ways to improve its efficiency.', 'Gas burns in a boiler → heats water → high-pressure steam → turbine spins → generator (coil in magnetic field) → electricity; steam condensed in cooling towers. Sankey: 1000 MJ in; 400 MJ electrical; 600 MJ wasted (≈ 500 in cooling water, rest flue gases, friction). Improvements: combined-cycle gas turbine; CHP to use waste heat; better insulation/maintenance.', 6)],
))


@R.add('ch09-st2', 'C3', (1, 5), 'numerical')
def station_eff(rng, slot):
    k = rng.choice(['eff', 'fuel', 'waste'])
    inp = rng.choice([1000, 2500, 3000, 5000])
    e = rng.choice([33, 38, 40, 55, 60])
    out = inp * e / 100
    if k == 'eff':
        return dict(stem=f'A power station uses {inp} MW of fuel energy and supplies {g(out)} MW of electrical power. Calculate its efficiency.', answer=f'{e}%',
                    markingKey=f'M1 {g(out)} ÷ {inp} × 100; A1 {e}%.', marks=2)
    if k == 'waste':
        return dict(stem=f'A {e}% efficient power station takes in {inp} MW. Calculate the power wasted and state where most of it goes.', answer=f'{g(inp - out)} MW; mostly as heat in cooling water and flue gases',
                    markingKey=f'M1 useful = {g(out)} MW; M1 wasted = {inp} − {g(out)}; A1 {g(inp - out)} MW; B1 thermal energy in cooling water/surroundings.', marks=4)
    P = rng.choice([500, 1000, 2000])
    fuel, ed = rng.choice([('natural gas', 55), ('coal', 30)])
    hours = 24
    fuel_e = P / (e / 100) * 3600 * hours  # MJ per day
    mass = fuel_e / ed / 1000
    return dict(stem=f'A {P} MW power station burning {fuel} (energy density {ed} MJ/kg) is {e}% efficient. Calculate the mass of fuel burned per day in tonnes.', answer=f'{g(mass)} tonnes',
                markingKey=f'M1 input power = {P} ÷ {e / 100:g} = {g(P / (e / 100))} MW; M1 energy per day = {g(P / (e / 100))} × 3600 × 24 = {g(fuel_e)} MJ; M1 mass = ÷ {ed} MJ/kg = {g(fuel_e / ed)} kg; A1 {g(mass)} tonnes.', marks=4)


inquiry('ch09-st2',
        dict(ctx='how the speed of rotation of a model generator affects the output voltage',
             iv='rotation rate of the generator shaft (1, 2, 3, 4, 5 revolutions per second)', dv='peak output voltage measured with a data logger',
             cvs=[('the same generator (coil turns and magnet)', 'both affect induced voltage'), ('load resistor connected (10 Ω)', 'load changes the terminal voltage'), ('method of measuring speed (optical sensor)', 'accuracy of the IV'), ('steady rotation before recording', 'changing speed gives varying voltage')],
             hyp='If the rotation rate increases, then the peak voltage will increase in proportion, because the magnetic field through the coil changes faster, inducing a larger voltage.',
             method='Drive the generator with a variable-speed motor; measure rotation rate with an optical sensor; connect the output across a 10 Ω resistor to a data logger; record peak voltage at each speed once steady; repeat three times; plot peak voltage against rotation rate.',
             weak=('the speed drifted while readings were taken', 'use a motor speed controller and record only when the speed sensor shows a steady value'),
             safety='keep fingers and hair away from rotating parts; secure the apparatus with clamps'))
dataset('ch09-st2',
        dict(intro='{who} compared the efficiency of power stations commissioned in different decades using published data (three stations per decade).', iv=('Year commissioned', ''), xs=[1960, 1975, 1990, 2005, 2020],
             dv=('Efficiency', '%'), f=lambda x: 28 + 0.5 * (x - 1960), dp=0, trend='Power station efficiency has increased steadily over time.',
             why='Newer stations use higher steam temperatures and pressures, better turbine design and combined-cycle gas turbines, so a larger fraction of the fuel energy becomes electrical energy.'))

R.facts('ch09-st3', F(
    terms=[('energy mix', 'the combination of energy resources used to meet a country’s or the world’s energy needs'),
           ('sustainability', 'meeting the needs of the present without compromising the ability of future generations to meet theirs'),
           ('net zero', 'a balance between greenhouse gases emitted and removed from the atmosphere'),
           ('energy security', 'reliable access to affordable energy, without depending on unstable supplies'),
           ('carbon footprint', 'the total greenhouse gas emissions caused by an activity, product or person, in CO₂ equivalent'),
           ('energy poverty', 'lack of access to modern energy services such as electricity and clean cooking fuels')],
    facts=[('Approximately what share of global primary energy still came from fossil fuels in the early 2020s?', 'About 80%', ['About 20%', 'About 50%', 'About 99%'], 'Coal, oil and gas.'),
           ('Which international agreement aims to limit warming to well below 2 °C?', 'The Paris Agreement (2015)', ['The Montreal Protocol', 'The Kyoto Protocol (1987)', 'The Geneva Convention'], '“Pursue 1.5 °C.”'),
           ('How many people lacked access to electricity worldwide in the early 2020s?', 'About 700–750 million', ['About 7 million', 'About 3 billion', 'Nobody'], 'Mostly in sub-Saharan Africa.'),
           ('Which is a way to increase energy security?', 'Diversifying energy sources and producing more domestically', ['Relying on one imported fuel', 'Removing storage', 'Closing interconnectors'], 'Less risk from supply shocks.')],
    why=[('Explain why developing countries may find it hard to stop using fossil fuels quickly.', 'They need affordable energy to grow and reduce poverty; existing infrastructure, finance for renewables and grid investment may be lacking.'),
         ('Explain why reducing energy demand is as important as changing energy sources.', 'Energy not used needs no generation, avoids emissions and costs, and makes the switch to renewables easier.'),
         ('Explain why energy storage is key to a sustainable energy mix.', 'It stores surplus renewable energy for times of low output, smoothing supply and replacing fossil-fuel backup.')],
    contrast=[('primary energy', 'electricity', 'Primary energy is energy in its natural form (coal, oil, sunlight, wind); electricity is a secondary energy carrier generated from primary sources.'),
              ('energy efficiency', 'energy conservation', 'Energy efficiency is doing the same task with less energy (LED bulbs); energy conservation is choosing to use less energy (switching lights off).')],
    misc=[('Electricity is the same as total energy use.', 'Electricity is only about 20% of final energy use; transport, heating and industry use large amounts of fuel directly.'),
          ('Switching to renewables only matters in rich countries.', 'Emissions from all countries affect the climate, and many developing countries have excellent renewable resources and fast-growing demand.')],
    cases=[('Solar mini-grids in sub-Saharan Africa', 'Solar panels with batteries power village mini-grids and home systems where the national grid does not reach, often paid for by mobile phone.', 'energy access and sustainability', 'Brings electricity to millions without building fossil-fuel plants, improving health and education.')],
    evaluate=[('Rich countries should pay for poorer countries’ transition to renewable energy.', ['rich countries caused most historic emissions', 'climate change is global – everyone benefits'], ['domestic taxpayers may object', 'money must be well governed to be effective'], 'Climate finance is fair and necessary; transparent, well-targeted funding benefits both rich and poor countries.'),
              ('Carbon taxes are the most effective way to change a country’s energy mix.', ['makes polluting energy more expensive, rewarding low-carbon options', 'revenue can fund renewables or be returned to households'], ['can hit poorer households hardest', 'industries may move abroad'], 'Carbon pricing works well when combined with support for low-income households and border adjustments.')],
    extended=[('Discuss how a country could move towards a sustainable energy mix by 2050, considering scientific, economic, social and environmental factors.', 'Science: expand wind, solar, hydro, possibly nuclear; storage (batteries, pumped hydro, hydrogen); electrify transport and heating; grid upgrades; efficiency (insulation, LEDs). Economic: investment costs vs falling renewable prices, jobs in new industries, stranded fossil assets. Social: fair transition for fossil-fuel workers; affordability; public acceptance of wind farms. Environmental: lower CO₂ and air pollution; land use and mining impacts. Judgement: phased plan with targets, carbon pricing and support.', 8)],
))


@R.add('ch09-st3', 'C3', (1, 5), 'numerical')
def energy_mix(rng, slot):
    k = rng.choice(['share', 'co2'])
    if k == 'share':
        tot = rng.choice([300, 400, 600])
        r = rng.choice([90, 120, 150, 210])
        return dict(stem=f'A country generates {tot} TWh of electricity per year, of which {r} TWh is from renewables. Calculate the percentage from renewables.', answer=f'{g(r / tot * 100)}%',
                    markingKey=f'M1 {r} ÷ {tot} × 100; A1 {g(r / tot * 100)}%.', marks=2)
    E = rng.choice([100, 250, 500])
    a, b = 0.9, rng.choice([0.4, 0.45])
    return dict(stem=f'Coal electricity emits about {a} kg CO₂ per kWh and gas about {b} kg CO₂ per kWh. Calculate the CO₂ saved per year if {E} GWh of coal generation is replaced by gas. (1 GWh = 10⁶ kWh)', answer=f'{g(E * (a - b))} × 10⁶ kg = {g(E * (a - b) * 1000)} tonnes',
                markingKey=f'M1 saving per kWh = {a} − {b} = {g(a - b)} kg; M1 × {E} × 10⁶ kWh; A1 {g(E * (a - b))} × 10⁶ kg = {g(E * (a - b) * 1000)} tonnes.', marks=3)


inquiry('ch09-st3',
        dict(ctx='how the energy-saving measures in a school affect its daily electricity use',
             iv='measure in place (none; LED lighting; LED lighting plus automatic switch-off timers)', dv='mean daily electricity use in kWh from the school meter over 4 weeks',
             cvs=[('school days only (exclude weekends and holidays)', 'occupancy changes use'), ('season (similar weeks)', 'heating and lighting demand changes with season'), ('same buildings and equipment', 'new equipment changes demand'), ('meter readings at the same time each day', 'reading time affects daily totals')],
             hyp='If LED lighting and timers are both installed, then daily electricity use will fall the most, because LEDs need less power for the same light and timers prevent lights and computers being left on.',
             method='Record the meter reading at 8 am every school day for 4 weeks before changes; install LEDs and record for 4 similar weeks; add timers and record for 4 more weeks; calculate mean daily kWh and its range for each period; adjust for weather using degree-day data if needed.',
             weak=('the periods compared were in different seasons', 'compare similar weeks (or use the same weeks of the previous year) and correct for daylight hours'),
             safety='only qualified electricians install equipment; do not open meter cabinets'))
dataset('ch09-st3',
        dict(intro='{who} analysed data on the share of electricity generated from wind and solar worldwide in different years (three data sources).', iv=('Year', ''), xs=[2010, 2013, 2016, 2019, 2022],
             dv=('Share from wind and solar', '%'), f=lambda x: 1.7 * math.exp((x - 2010) / 7.2), dp=1, trend='The share of electricity from wind and solar increased rapidly, more than doubling roughly every five years.',
             why='Falling costs of solar panels and turbines, government targets and carbon pricing made new wind and solar cheaper than fossil fuels in many places.'))
evx(R, 'ch09-st3', ('Every household should install solar panels.', ['cuts bills and emissions; uses roof space', 'reduces grid demand at midday'], ['high upfront cost; not suitable for shaded or rented homes', 'output peaks when demand is low unless batteries are added'], 'Household solar is valuable where suitable and affordable, supported by grants and storage, but large-scale renewables are also needed.'))
evx(R, 'ch09-st2', ('Old coal power stations should be converted to burn biomass (wood pellets).', ['reuses existing turbines and grid connections', 'claimed to be low-carbon if forests are replanted'], ['pellets are often shipped long distances', 'regrowing forests takes decades, so CO₂ is not balanced quickly', 'can drive deforestation'], 'Conversion can be a short-term step, but only with sustainably sourced local biomass; it is not a long-term solution.'))


# =============================================================================================
# ch10 Electromagnetic Induction and Transformers
# =============================================================================================
R.facts('ch10-st1', F(
    terms=[('electromagnetic induction', 'the production of a potential difference across a conductor when it moves relative to a magnetic field, or when the field through it changes'),
           ('generator effect', 'the induction of a potential difference (and a current if the circuit is complete) by relative motion of a conductor and a magnetic field'),
           ('induced current', 'a current produced by electromagnetic induction in a complete circuit'),
           ('Lenz’s law', 'an induced current always flows in a direction that opposes the change that caused it'),
           ('magnetic flux', 'a measure of the amount of magnetic field passing through an area'),
           ('Faraday’s law', 'the induced voltage is proportional to the rate of change of magnetic flux linkage')],
    facts=[('What happens when a magnet is held still inside a coil?', 'No potential difference is induced', ['A large current flows', 'The magnet loses its magnetism', 'The coil becomes hot'], 'There must be relative motion.'),
           ('Which change increases the induced voltage when a magnet is pushed into a coil?', 'Moving the magnet faster', ['Moving it slower', 'Using fewer turns', 'Using a weaker magnet'], 'Faster rate of change.'),
           ('What happens to the direction of the induced current when the magnet is pulled out instead of pushed in?', 'It reverses', ['It stays the same', 'It stops', 'It doubles'], 'Opposite motion → opposite current.'),
           ('Who discovered electromagnetic induction in 1831?', 'Michael Faraday', ['Isaac Newton', 'Albert Einstein', 'Marie Curie'], 'Also Joseph Henry independently.'),
           ('Which device uses electromagnetic induction?', 'A microphone (moving-coil)', ['A filament lamp', 'A thermistor', 'An LDR'], 'Sound moves a coil in a magnetic field.')],
    why=[('Explain why pushing a magnet into a coil connected to a circuit feels harder than pushing it into a coil that is not connected.', 'In a complete circuit an induced current flows and creates a magnetic field that opposes the magnet’s motion (Lenz’s law), so work must be done against it.'),
         ('Explain why more turns on a coil give a larger induced voltage.', 'Each turn has a voltage induced in it; the turns are in series so the voltages add.'),
         ('Explain how a dynamo on a bicycle produces electricity.', 'The wheel turns a magnet near a coil; the changing magnetic field through the coil induces an alternating voltage that lights the lamp.')],
    contrast=[('the motor effect', 'the generator effect', 'In the motor effect a current in a magnetic field produces a force and motion; in the generator effect motion in a magnetic field produces a voltage and current.'),
              ('an induced voltage', 'an induced current', 'An induced voltage is produced whenever the flux through a conductor changes; an induced current flows only if the conductor is part of a complete circuit.')],
    misc=[('A magnet near a coil always produces a current.', 'A current is only induced while the magnetic field through the coil is changing (movement or changing field) and the circuit is complete.'),
          ('Generators create electrical energy from nothing.', 'Generators transfer kinetic energy into electrical energy; work must be done to turn them.')],
    cases=[('Faraday’s iron ring experiment (1831)', 'Faraday wound two coils on an iron ring; switching the current in one coil on or off briefly produced a current in the other – the first transformer.', 'discovery of induction', 'It led to generators, transformers and the electricity supply system.'),
           ('Regenerative braking', 'Electric and hybrid cars use their motors as generators when braking; the car’s kinetic energy induces a current that recharges the battery.', 'induction in transport', 'Recovers energy that would be wasted as heat in brakes, increasing range by 10–20%.')],
    evaluate=[('Faraday’s discovery of induction was the most important scientific discovery of the 19th century.', ['made electricity generation and distribution possible', 'basis of generators, transformers, motors'], ['other discoveries (evolution, germ theory, periodic table) were equally transformative'], 'It was among the most important, especially for technology, but “most important” depends on criteria.')],
    extended=[('Describe an experiment to show the factors affecting the size of the voltage induced when a magnet moves through a coil, and explain the results using the idea of rate of change of magnetic field.', 'Connect coil to a sensitive voltmeter/data logger; drop or push a magnet through; vary speed (drop height), number of turns, magnet strength; record peak voltage; repeat. Larger speed, more turns, stronger magnet → larger voltage, because the magnetic flux through the coil changes faster/by more, and each turn adds voltage. Direction reverses as magnet leaves or when poles reversed (Lenz).', 6)],
))


@R.add('ch10-st1', 'C3', (1, 4), 'numerical')
def induced_v(rng, slot):
    v1 = rng.choice([0.2, 0.3, 0.5, 0.8])
    f1 = rng.choice([2, 3, 4])
    n1 = rng.choice([100, 200])
    n2 = n1 * rng.choice([2, 3])
    k = rng.choice(['speed', 'turns'])
    if k == 'speed':
        return dict(stem=f'A magnet pushed into a coil at a certain speed induces a peak voltage of {v1} V. Predict the voltage if the magnet moves {f1} times as fast, and explain.', answer=f'{g(v1 * f1)} V; the magnetic field through the coil changes {f1} times as fast',
                    markingKey=f'M1 voltage ∝ rate of change of flux; A1 {g(v1 * f1)} V; B1 explanation.', marks=3)
    return dict(stem=f'A coil of {n1} turns gives a peak induced voltage of {v1} V. Predict the voltage with {n2} turns under the same conditions.', answer=f'{g(v1 * n2 / n1)} V',
                markingKey=f'M1 voltage ∝ number of turns: {v1} × {n2}/{n1}; A1 {g(v1 * n2 / n1)} V.', marks=2)


inquiry('ch10-st1',
        dict(ctx='how the speed at which a magnet falls through a coil affects the peak induced voltage',
             iv='drop height of the magnet above the coil (5, 10, 20, 40, 80 cm), giving different speeds', dv='peak induced voltage recorded by a data logger',
             cvs=[('the same magnet', 'strength affects voltage'), ('the same coil (number of turns)', 'more turns give more voltage'), ('magnet dropped through a guide tube, same orientation', 'orientation and path affect flux change'), ('data-logger sampling rate (high)', 'low sampling may miss the peak')],
             hyp='If the drop height increases, then the peak voltage will increase, because the magnet moves faster through the coil, so the magnetic field changes more rapidly.',
             method='Clamp a coil around a vertical plastic tube; connect to a data logger at 1000 samples/s; drop the magnet from rest from each height through the tube onto a cushion; record the peak voltage; repeat five times; calculate speed √(2gh) and plot peak voltage against speed.',
             weak=('the magnet sometimes hit the side of the tube', 'use a narrow guide tube and discard runs where it hits the side'),
             safety='strong magnets can trap fingers; keep away from electronic devices and pacemakers'))
dataset('ch10-st1',
        dict(intro='{who} measured the peak voltage induced when a magnet was dropped through coils with different numbers of turns (three drops each).', iv=('Number of turns', ''), xs=[50, 100, 150, 200, 250],
             dv=('Peak voltage', 'mV'), f=lambda x: 1.2 * x, dp=0, trend='The peak induced voltage increases in direct proportion to the number of turns.',
             why='The same change in magnetic field induces the same voltage in each turn; the turns are in series so the voltages add.'))

R.facts('ch10-st2', F(
    terms=[('alternating current (ac)', 'current that repeatedly reverses direction'),
           ('direct current (dc)', 'current that flows in one direction only, e.g. from a cell'),
           ('frequency', 'the number of complete cycles per second, measured in hertz (Hz)'),
           ('peak voltage', 'the maximum voltage reached in an ac cycle'),
           ('slip rings', 'rings in an ac generator that keep a continuous connection with the rotating coil without reversing'),
           ('commutator', 'a split ring in a dc generator or motor that reverses connections every half turn'),
           ('oscilloscope', 'an instrument that displays how a voltage changes with time')],
    facts=[('What is the frequency of the mains supply in the UK, Europe and India?', '50 Hz', ['60 Hz', '230 Hz', '1 Hz'], 'It is 60 Hz in the USA.'),
           ('What does a dc trace look like on an oscilloscope?', 'A horizontal straight line', ['A sine wave', 'A square wave crossing zero', 'Random spikes'], 'Constant voltage.'),
           ('What component makes an ac generator different from a dc generator?', 'Slip rings instead of a split-ring commutator', ['A stronger magnet', 'More turns of wire', 'An iron core'], ''),
           ('If an ac generator coil spins faster, what happens to the output?', 'Both the frequency and peak voltage increase', ['Only the frequency increases', 'Only the voltage increases', 'Neither changes'], 'Faster rate of change of flux.'),
           ('What is the period of a 50 Hz supply?', '0.02 s', ['50 s', '0.5 s', '2 s'], 'T = 1/f.')],
    why=[('Explain why the output of an ac generator is a sine wave.', 'As the coil rotates, the rate at which it cuts magnetic field lines changes smoothly – maximum when the coil is parallel to the field and zero when perpendicular – and reverses each half turn.'),
         ('Explain why mains electricity is ac rather than dc.', 'ac can be stepped up and down easily with transformers, allowing efficient high-voltage transmission.'),
         ('Explain why a dc generator needs a commutator.', 'The commutator reverses the connections to the external circuit every half turn, so the current always flows the same way.')],
    contrast=[('ac', 'dc', 'ac repeatedly reverses direction (sine wave on an oscilloscope); dc flows in one direction only (a horizontal line).'),
              ('slip rings', 'a split-ring commutator', 'Slip rings keep the same coil end connected to the same brush, giving ac; a split ring swaps the connections every half turn, giving dc.')],
    misc=[('In ac the electrons travel all the way from the power station to the house.', 'In ac the electrons vibrate back and forth a tiny distance; energy is transferred along the wires.'),
          ('An ac voltage of 230 V means the voltage is always 230 V.', '230 V is the effective (rms) value; the voltage varies between about +325 V and −325 V.')],
    cases=[('The “War of the Currents” (1880s–1890s)', 'Edison promoted dc power; Tesla and Westinghouse promoted ac; ac won because transformers allowed efficient long-distance transmission.', 'ac vs dc', 'Today high-voltage dc (HVDC) is used again for very long cables, showing technology choices change.')],
    evaluate=[('High-voltage dc links should replace ac for long-distance and undersea transmission.', ['lower losses over very long distances and in undersea cables', 'can link grids with different frequencies'], ['converter stations are expensive', 'ac is simpler for local distribution'], 'HVDC is best for very long or undersea links; ac remains best for most local grids.')],
    extended=[('Describe the structure of a simple ac generator and explain how it produces an alternating voltage. Describe how the output trace on an oscilloscope changes if the coil rotates twice as fast.', 'Rectangular coil rotating between poles of a magnet; ends connected to slip rings with brushes. Rotation changes the flux through the coil → induced voltage; direction reverses every half turn → ac sine wave. Twice as fast: twice the frequency (half the period, cycles closer together) and twice the peak voltage (taller wave).', 6)],
))


@R.add('ch10-st2', 'C3', (1, 5), 'numerical')
def ac_freq(rng, slot):
    k = rng.choice(['f', 'T', 'osc'] if slot.d >= 2 else ['f', 'T'])
    if k == 'f':
        T = rng.choice([0.02, 0.01, 0.05, 0.004, 0.1])
        return dict(stem=f'An ac supply has a period of {T} s. Calculate its frequency.', answer=f'{g(1 / T)} Hz', markingKey=f'M1 f = 1 ÷ T = 1 ÷ {T}; A1 {g(1 / T)} Hz.', marks=2)
    if k == 'T':
        f = rng.choice([50, 60, 25, 100, 200])
        return dict(stem=f'Calculate the period of a {f} Hz alternating current, in milliseconds.', answer=f'{g(1000 / f)} ms', markingKey=f'M1 T = 1 ÷ {f} = {g(1 / f)} s; A1 {g(1000 / f)} ms.', marks=2)
    tb = rng.choice([2, 5, 10])
    dv = rng.choice([2, 5])
    sq = rng.choice([4, 5, 8])
    hv = rng.choice([2, 3, 4])
    T = sq * tb / 1000
    return dict(stem=f'On an oscilloscope, one complete wave is {sq} squares wide and the peak is {hv} squares above the centre line. The time base is {tb} ms/square and the y-gain is {dv} V/square. Calculate the frequency and the peak voltage.', answer=f'{g(1 / T)} Hz; {hv * dv} V',
                markingKey=f'M1 T = {sq} × {tb} ms = {g(T)} s; A1 f = {g(1 / T)} Hz; M1 peak = {hv} × {dv}; A1 {hv * dv} V.', marks=4)


inquiry('ch10-st2',
        dict(ctx='how the rotation frequency of a hand-cranked ac generator affects the frequency and peak voltage of its output',
             iv='cranking rate (1, 2, 3, 4 turns per second, set with a metronome)', dv='output frequency and peak voltage measured from a data-logger trace',
             cvs=[('the same generator and gearing', 'gearing changes coil speed'), ('the same load resistor', 'affects terminal voltage'), ('steady cranking', 'changes in speed make the trace irregular'), ('data-logger settings', 'time base must show several cycles')],
             hyp='If the cranking rate doubles, then both the output frequency and the peak voltage will double, because the coil rotates twice as fast and the flux changes twice as quickly.',
             method='Connect the generator across a 10 Ω resistor to a data logger; crank at each rate with a metronome for 10 s; from the trace measure the period of several cycles and the peak voltage; calculate frequency; repeat three times; plot both against cranking rate.',
             weak=('the cranking rate varied during a trial', 'use a motor with speed control or average the period over 10 cycles'),
             safety='secure the generator; low voltages only; keep loose clothing away from moving parts'))
dataset('ch10-st2',
        dict(intro='{who} measured the peak voltage from an ac generator at different rotation frequencies (three trials).', iv=('Rotation frequency', 'Hz'), xs=[5, 10, 15, 20, 25],
             dv=('Peak voltage', 'V'), f=lambda x: 0.36 * x, dp=2, trend='The peak voltage is directly proportional to the rotation frequency.',
             why='Faster rotation makes the magnetic flux through the coil change more quickly, so the induced voltage is larger (Faraday’s law); the output frequency also equals the rotation frequency.'))

R.facts('ch10-st3', F(
    terms=[('transformer', 'a device with two coils on an iron core that changes the size of an alternating voltage'),
           ('step-up transformer', 'a transformer with more turns on the secondary coil, increasing the voltage'),
           ('step-down transformer', 'a transformer with fewer turns on the secondary coil, decreasing the voltage'),
           ('national grid', 'the network of cables and transformers that distributes electricity across a country'),
           ('transformer equation', 'Vp/Vs = Np/Ns'),
           ('power loss in cables', 'P = I²R – the heating power lost in transmission cables')],
    facts=[('Why does a transformer only work with ac?', 'A changing magnetic field is needed to induce a voltage in the secondary coil', ['dc is too dangerous', 'ac has more energy', 'dc would melt the iron core'], 'Steady dc gives a constant field.'),
           ('A transformer has 100 primary turns and 2000 secondary turns. What type is it?', 'Step-up', ['Step-down', 'Isolating', 'It is not a transformer'], 'Ns > Np.'),
           ('Why is electricity transmitted at very high voltages?', 'For the same power the current is lower, so less energy is lost as heat', ['High voltage travels faster', 'It is safer', 'It needs thinner pylons'], 'P loss = I²R.'),
           ('What is the purpose of the iron core?', 'To link the magnetic field from the primary to the secondary coil', ['To carry the current', 'To insulate the coils', 'To store charge'], 'Iron is easily magnetised.'),
           ('If a 100% efficient transformer steps up the voltage by 10×, what happens to the current?', 'It decreases by 10×', ['It increases by 10×', 'It stays the same', 'It becomes zero'], 'VpIp = VsIs.')],
    why=[('Explain why doubling the transmission current increases the power loss in cables by four times.', 'Power loss = I²R; doubling I makes I² four times bigger.'),
         ('Explain why step-down transformers are needed near homes.', 'The grid voltage (e.g. 400 kV) is far too dangerous for homes, so it is reduced in stages to 230 V.'),
         ('Explain why transformer cores are laminated (made of thin insulated sheets).', 'Laminations reduce eddy currents induced in the core, which would waste energy as heat.')],
    contrast=[('a step-up transformer', 'a step-down transformer', 'A step-up transformer has more secondary than primary turns and increases voltage (decreasing current); a step-down has fewer secondary turns and decreases voltage (increasing current).'),
              ('transmission voltage', 'domestic voltage', 'Transmission voltage is very high (e.g. 132–400 kV) to reduce losses; domestic voltage is about 230 V for safety.')],
    misc=[('A step-up transformer increases the power.', 'Power out cannot exceed power in; if voltage goes up, current goes down (VpIp ≈ VsIs).'),
          ('Transformers work with batteries.', 'Batteries supply dc, which does not produce a changing magnetic field, so no voltage is induced in the secondary.')],
    cases=[('Smart grids and interconnectors', 'Undersea interconnectors link national grids (e.g. Norway–UK North Sea Link, 2021) so countries can share surplus renewable electricity.', 'modern grid design', 'Helps balance intermittent renewables over larger areas.')],
    evaluate=[('Overhead power lines should be replaced by underground cables.', ['improves landscapes; less storm damage', 'concerns about pylons near homes reduced'], ['underground cables cost 5–10× more', 'harder to repair; heat and cooling issues'], 'Underground cables suit sensitive landscapes and cities, but cost limits their use elsewhere.')],
    extended=[('Explain how a transformer works, and use calculations to show why transmitting 100 MW at 400 kV rather than at 25 kV reduces power losses in a cable of resistance 5 Ω.', 'Alternating current in primary → changing magnetic field in iron core → changing flux through secondary → induced alternating voltage; Vs/Vp = Ns/Np. At 25 kV: I = 100 × 10⁶ / 25 000 = 4000 A, loss = 4000² × 5 = 80 MW (impractical). At 400 kV: I = 250 A, loss = 250² × 5 = 312 500 W ≈ 0.31 MW. Higher voltage → lower current → much lower I²R loss.', 8)],
))


@R.add('ch10-st3', 'C3', (1, 5), 'numerical')
def transformer(rng, slot):
    k = rng.choice(['Vs', 'Ns', 'Is', 'loss'] if slot.d >= 2 else ['Vs', 'Ns'])
    Vp = rng.choice([230, 12, 25000, 400000])
    Np = rng.choice([100, 200, 500, 1000, 2000])
    r = rng.choice([0.05, 0.1, 0.5, 2, 5, 20])
    Ns = int(Np * r)
    Vs = Vp * r
    if k == 'Vs':
        return dict(stem=f'A transformer has {Np} turns on the primary and {Ns} turns on the secondary. The primary voltage is {g(Vp)} V. Calculate the secondary voltage and state whether it is step-up or step-down.', answer=f'{g(Vs)} V; {"step-up" if r > 1 else "step-down"}',
                    markingKey=f'M1 Vs = Vp × Ns/Np = {g(Vp)} × {Ns}/{Np}; A1 {g(Vs)} V; B1 {"step-up" if r > 1 else "step-down"}.', marks=3)
    if k == 'Ns':
        return dict(stem=f'A transformer must change {g(Vp)} V to {g(Vs)} V. The primary coil has {Np} turns. How many turns are needed on the secondary?', answer=f'{Ns} turns',
                    markingKey=f'M1 Ns = Np × Vs/Vp = {Np} × {g(Vs)}/{g(Vp)}; A1 {Ns}.', marks=2)
    if k == 'Is':
        Ip = rng.choice([0.5, 1, 2, 4])
        return dict(stem=f'A 100% efficient transformer has Vp = {g(Vp)} V, Ip = {Ip} A and Vs = {g(Vs)} V. Calculate the secondary current.', answer=f'{g(Vp * Ip / Vs)} A',
                    markingKey=f'M1 VpIp = VsIs; M1 Is = {g(Vp)} × {Ip} ÷ {g(Vs)}; A1 {g(Vp * Ip / Vs)} A.', marks=3)
    P = rng.choice([10e6, 50e6, 100e6])
    V = rng.choice([25000, 132000, 400000])
    R_ = rng.choice([2, 5, 10])
    I = P / V
    loss = I * I * R_
    return dict(stem=f'{g(P / 1e6)} MW is transmitted at {g(V)} V through cables of total resistance {R_} Ω. Calculate the current and the power lost in the cables, and the percentage of power lost.', answer=f'{g(I)} A; {g(loss)} W; {g(loss / P * 100)}%',
                markingKey=f'M1 I = P ÷ V = {g(P)} ÷ {g(V)} = {g(I)} A; M1 loss = I²R = {g(I)}² × {R_}; A1 {g(loss)} W; A1 {g(loss / P * 100)}% of the power.', marks=4)


inquiry('ch10-st3',
        dict(ctx='how the number of turns on the secondary coil of a demonstration transformer affects the output voltage',
             iv='number of secondary turns (100, 200, 300, 400, 500) with 200 primary turns', dv='secondary voltage measured with an ac voltmeter',
             cvs=[('primary voltage (2 V ac)', 'output depends on input'), ('the same laminated iron core, fully closed', 'gaps reduce flux linkage'), ('primary turns (200)', 'turns ratio determines output'), ('no load or the same load', 'load affects the output voltage')],
             hyp='If the number of secondary turns increases, then the output voltage will increase in proportion, because Vs/Vp = Ns/Np.',
             method='Wind 200 turns of insulated wire as the primary on a C-core; connect to a 2 V ac low-voltage supply; wind the secondary with 100 turns, close the core with the clip; read Vs; add turns in steps of 100; repeat three times; plot Vs against Ns and compare with the theoretical line.',
             weak=('the core was not clamped tightly, so readings were low and variable', 'clamp the two halves of the core firmly together each time'),
             safety='use only low-voltage ac supplies; never connect to the mains; the secondary voltage can be higher than the input – keep it below 12 V'))
dataset('ch10-st3',
        dict(intro='{who} measured the efficiency of a demonstration transformer at different output currents (three trials).', iv=('Output current', 'A'), xs=[0.2, 0.4, 0.6, 0.8, 1.0],
             dv=('Efficiency', '%'), f=lambda x: 92 - 15 * (x - 0.5) ** 2 - 4 / (x * 10), dp=0, trend='The efficiency rises to a maximum at a moderate current and falls slightly at higher currents.',
             why='At low current, fixed losses in the core (magnetising and eddy currents) are a large fraction of the small output; at high current, heating in the coils (I²R) increases.'))
evx(R, 'ch10-st3', ('Every country should build a “supergrid” connecting it to its neighbours.', ['shares renewable surpluses, reducing the need for backup', 'improves energy security'], ['very expensive', 'depends on international cooperation and political stability'], 'Interconnection brings strong benefits for renewables and security, if agreements and investment are in place.'))
evx(R, 'ch10-st2', ('Mains frequency should be standardised at the same value worldwide.', ['appliances could be used everywhere', 'easier to connect grids'], ['changing existing grids and equipment would be hugely expensive', 'HVDC links already connect grids of different frequencies'], 'Standardisation would be convenient but the cost of change is too high; converters solve most problems.'))
evx(R, 'ch10-st1', ('Wireless (induction) charging should replace charging cables for phones and electric cars.', ['convenient, no worn sockets', 'can be built into roads or parking spaces'], ['less efficient – more energy wasted as heat', 'more expensive; slower charging'], 'Wireless charging is convenient but less efficient, so cables remain better where efficiency matters.'))


# =============================================================================================
# ch11 Nuclear Physics
# =============================================================================================
NUC = [('hydrogen', 'H', 1, 1), ('hydrogen', 'H', 1, 2), ('helium', 'He', 2, 4), ('lithium', 'Li', 3, 7), ('carbon', 'C', 6, 12), ('carbon', 'C', 6, 14),
       ('nitrogen', 'N', 7, 14), ('oxygen', 'O', 8, 16), ('sodium', 'Na', 11, 23), ('potassium', 'K', 19, 40), ('cobalt', 'Co', 27, 60), ('strontium', 'Sr', 38, 90),
       ('iodine', 'I', 53, 131), ('caesium', 'Cs', 55, 137), ('radon', 'Rn', 86, 222), ('radium', 'Ra', 88, 226), ('uranium', 'U', 92, 235), ('uranium', 'U', 92, 238),
       ('plutonium', 'Pu', 94, 239), ('americium', 'Am', 95, 241)]
SYM = {1: 'H', 2: 'He', 6: 'C', 7: 'N', 8: 'O', 18: 'Ar', 19: 'K', 20: 'Ca', 26: 'Fe', 27: 'Co', 28: 'Ni', 38: 'Sr', 39: 'Y', 53: 'I', 54: 'Xe', 55: 'Cs', 56: 'Ba',
       82: 'Pb', 83: 'Bi', 84: 'Po', 86: 'Rn', 88: 'Ra', 90: 'Th', 91: 'Pa', 92: 'U', 93: 'Np', 94: 'Pu', 95: 'Am'}

R.facts('ch11-st1', F(
    terms=[('nucleus', 'the small, dense, positively charged centre of an atom containing protons and neutrons'),
           ('atomic number (Z)', 'the number of protons in the nucleus; it identifies the element'),
           ('mass number (A)', 'the total number of protons and neutrons in the nucleus'),
           ('isotopes', 'atoms of the same element with the same number of protons but different numbers of neutrons'),
           ('nucleon', 'a particle in the nucleus – a proton or a neutron'),
           ('nuclide notation', 'writing a nucleus as its symbol with the mass number A at the top left and the atomic number Z at the bottom left'),
           ('alpha-scattering experiment', 'Geiger and Marsden’s experiment (1909) in which alpha particles fired at gold foil showed that atoms have a tiny dense nucleus')],
    facts=[('In the alpha-scattering experiment, most alpha particles passed straight through the gold foil. What did this show?', 'Most of the atom is empty space', ['The nucleus is very large', 'Gold atoms are positively charged throughout', 'Alpha particles have no mass'], 'Only a few were deflected strongly.'),
           ('A very small number of alpha particles bounced back from the gold foil. What did this show?', 'The positive charge and most of the mass are concentrated in a tiny nucleus', ['Electrons are very heavy', 'The atom is a solid sphere', 'Gold foil is magnetic'], 'Rutherford’s nuclear model.'),
           ('Carbon-12 and carbon-14 are isotopes. How do their nuclei differ?', 'Carbon-14 has two more neutrons', ['Carbon-14 has two more protons', 'Carbon-14 has two more electrons in the nucleus', 'They have different atomic numbers'], 'Same Z = 6; A differs by 2.'),
           ('Which model of the atom did the nuclear model replace?', 'The plum-pudding model', ['The Bohr model', 'The quark model', 'The wave model'], 'Thomson’s model of positive charge with embedded electrons.'),
           ('Why do isotopes of an element have the same chemical properties?', 'They have the same number of electrons, arranged in the same way', ['They have the same mass', 'They have the same number of neutrons', 'Their nuclei are identical'], 'Chemistry depends on electrons.'),
           ('Roughly how does the diameter of a nucleus compare with the diameter of the atom?', 'About 100 000 times smaller', ['About 10 times smaller', 'About the same', 'About 100 times larger'], '~10⁻¹⁵ m vs ~10⁻¹⁰ m.')],
    why=[('Explain why an atom is electrically neutral overall.', 'It has equal numbers of protons (positive) and electrons (negative), so the charges cancel.'),
         ('Explain why the alpha-scattering results could not be explained by the plum-pudding model.', 'In the plum-pudding model the positive charge is spread out, so it could not deflect fast alpha particles strongly; large deflections need a small, concentrated positive charge.'),
         ('Explain why a few alpha particles were deflected through large angles.', 'They passed very close to a nucleus, and the strong repulsion between the positive alpha particle and the positive nucleus pushed them sharply away.')],
    contrast=[('atomic number', 'mass number', 'Atomic number (Z) is the number of protons; mass number (A) is protons plus neutrons.'),
              ('the plum-pudding model', 'the nuclear model', 'The plum-pudding model spreads positive charge throughout the atom with electrons embedded; the nuclear model puts the positive charge and mass in a tiny central nucleus with electrons around it.')],
    misc=[('Isotopes of an element have different numbers of protons.', 'Isotopes have the same number of protons; only the number of neutrons differs.'),
          ('The mass number is the mass of the atom in grams.', 'The mass number is a count of nucleons; it has no unit.')],
    cases=[('Rutherford, Geiger and Marsden (1909–1911)', 'Alpha particles fired at thin gold foil: most passed through, a few were deflected, about 1 in 8000 bounced back.', 'the nuclear model of the atom', 'An unexpected result led to a new model, showing how evidence changes scientific theories.'),
           ('Chadwick discovers the neutron (1932)', 'Chadwick showed that radiation from beryllium bombarded with alpha particles contained neutral particles of about the same mass as the proton.', 'neutrons and isotopes', 'Explained why mass numbers are larger than atomic numbers and made nuclear fission possible.')],
    evaluate=[('The alpha-scattering experiment proved that the plum-pudding model was completely wrong.', ['large-angle deflections could not happen with spread-out charge', 'the results fitted a nuclear model quantitatively'], ['the model correctly included electrons and overall neutrality', 'one experiment led to a better model, which was itself later refined (Bohr, neutrons)'], 'The experiment disproved the distribution of charge in the plum-pudding model, but science builds on earlier models rather than discarding them completely.')],
    extended=[('Describe the alpha-scattering experiment and explain how its results led to the nuclear model of the atom.', 'Alpha particles from a source fired at thin gold foil in a vacuum; detector moved around. Most went straight through → atom mostly empty space. Some deflected at small angles → positive charge concentrated. A very few bounced back → tiny, dense, positive nucleus containing most of the mass. Electrons orbit at a distance. Replaced plum-pudding model.', 6)],
))


@R.add('ch11-st1', 'C3', (1, 5), 'numerical')
def nuc_count(rng, slot):
    el, s, Z, A = rng.choice(NUC)
    k = rng.choice(['pne', 'iso', 'ion'] if slot.d >= 3 else ['pne', 'iso'])
    if k == 'pne':
        return dict(stem=f'A nucleus is written as ^{A}_{Z}{s} ({el}-{A}). State the number of protons, neutrons and electrons in a neutral atom of this nuclide.', answer=f'{Z} {"proton" if Z == 1 else "protons"}, {A - Z} {"neutron" if A - Z == 1 else "neutrons"}, {Z} {"electron" if Z == 1 else "electrons"}',
                    markingKey=f'B1 protons = Z = {Z}; M1 neutrons = A − Z = {A} − {Z}; A1 {A - Z}; B1 electrons = {Z} (neutral atom).', marks=3)
    if k == 'iso':
        el, s, Z, A = rng.choice([('carbon', 'C', 6, 13), ('oxygen', 'O', 8, 17), ('oxygen', 'O', 8, 18), ('hydrogen', 'H', 1, 3), ('uranium', 'U', 92, 235), ('chlorine', 'Cl', 17, 35),
                                  ('chlorine', 'Cl', 17, 37), ('iodine', 'I', 53, 127), ('cobalt', 'Co', 27, 59), ('caesium', 'Cs', 55, 133), ('nitrogen', 'N', 7, 15), ('lithium', 'Li', 3, 6),
                                  ('helium', 'He', 2, 3), ('potassium', 'K', 19, 39), ('strontium', 'Sr', 38, 88), ('plutonium', 'Pu', 94, 240)])
        return dict(stem=f'An isotope of {el} has {A - Z} neutron{"s" * (A - Z != 1)}. Its atomic number is {Z}. Write its mass number and its nuclide notation.', answer=f'A = {A}; ^{A}_{Z}{s}',
                    markingKey=f'M1 A = Z + N = {Z} + {A - Z}; A1 {A}; B1 notation ^{A}_{Z}{s}.', marks=3)
    el, s, Z, A, q = rng.choice([('lithium', 'Li', 3, 7, 1), ('sodium', 'Na', 11, 23, 1), ('potassium', 'K', 19, 39, 1), ('magnesium', 'Mg', 12, 24, 2), ('calcium', 'Ca', 20, 40, 2),
                                 ('aluminium', 'Al', 13, 27, 3), ('iron', 'Fe', 26, 56, 3), ('oxygen', 'O', 8, 16, -2), ('chlorine', 'Cl', 17, 37, -1), ('sulfur', 'S', 16, 32, -2)])
    ch = f'+{q}' if q > 0 else f'−{-q}'
    how = f'lost {q} electron' + ('s' * (q > 1)) if q > 0 else f'gained {-q} electron' + ('s' * (q < -1))
    return dict(stem=f'An ion of {el}-{A} (^{A}_{Z}{s}) has a charge of {ch}. How many protons, neutrons and electrons does it have?', answer=f'{Z} protons, {A - Z} neutrons, {Z - q} electrons',
                markingKey=f'B1 {Z} protons; B1 {A - Z} neutrons; M1 a {ch} ion has {how}; A1 {Z - q} electrons.', marks=4)


inquiry('ch11-st1',
        dict(ctx='how the angle of deflection affects the number of alpha particles detected, using a computer simulation of the gold-foil experiment',
             iv='detector angle (10°, 30°, 60°, 90°, 150°)', dv='number of alpha particles counted per minute',
             cvs=[('the same simulated foil thickness', 'thicker foil gives more scattering'), ('the same alpha-particle energy', 'faster particles are deflected less'), ('the same counting time', 'longer times give larger counts'), ('the same target element (gold)', 'nuclear charge affects deflection')],
             hyp='If the detector angle increases, then the count rate will fall sharply, because only particles passing very close to a small nucleus are deflected through large angles.',
             method='Use the simulation with gold foil and a fixed alpha energy; set the detector at each angle; run for 60 simulated seconds; record the count; repeat five runs at each angle; plot count against angle (use a log scale if needed).',
             weak=('counts at large angles were so small that random variation dominated', 'run the simulation for longer at large angles and compare count rates'),
             safety='a simulation removes the hazard; the real experiment needs an alpha source handled with tongs in a vacuum chamber'))
dataset('ch11-st1',
        dict(intro='{who} used a simulation of the gold-foil experiment and recorded alpha-particle counts per minute at different scattering angles (three runs).', iv=('Scattering angle', '°'), xs=[15, 30, 45, 60, 90],
             dv=('Count rate', 'counts/min'), f=lambda x: 3200 / (math.sin(math.radians(x / 2)) ** 4) / 3000, dp=0, trend='The count rate falls very steeply as the scattering angle increases.',
             why='Most alpha particles pass far from any nucleus and are hardly deflected; only the rare particles passing very close to the tiny, dense nucleus are scattered through large angles.'))

R.facts('ch11-st2', F(
    terms=[('radioactive decay', 'the random, spontaneous change of an unstable nucleus, emitting radiation'),
           ('alpha particle (α)', 'a helium nucleus – 2 protons and 2 neutrons, ⁴₂He'),
           ('beta-minus particle (β⁻)', 'a fast electron emitted when a neutron in the nucleus changes into a proton'),
           ('gamma ray (γ)', 'high-energy electromagnetic radiation emitted from an unstable nucleus'),
           ('ionising radiation', 'radiation that can knock electrons out of atoms, forming ions'),
           ('background radiation', 'low-level radiation always present, from rocks, radon gas, cosmic rays, food and medical sources'),
           ('count rate', 'the number of decays detected per second (or minute) by a Geiger–Müller tube')],
    facts=[('Which radiation is stopped by a sheet of paper?', 'Alpha', ['Beta', 'Gamma', 'All three'], 'Alpha is the most strongly ionising and least penetrating.'),
           ('Which radiation needs several centimetres of lead to reduce it significantly?', 'Gamma', ['Alpha', 'Beta', 'None of them'], 'Gamma is weakly ionising and very penetrating.'),
           ('In beta-minus decay, what happens inside the nucleus?', 'A neutron changes into a proton and an electron', ['A proton changes into a neutron', 'Two protons are lost', 'An electron is absorbed'], 'Z increases by 1, A stays the same.'),
           ('In alpha decay, how do the mass number and atomic number change?', 'A decreases by 4 and Z decreases by 2', ['A decreases by 2 and Z by 4', 'A stays the same and Z increases by 1', 'Both stay the same'], 'An alpha particle is ⁴₂He.'),
           ('Which type of radiation is not deflected by an electric or magnetic field?', 'Gamma', ['Alpha', 'Beta', 'All are deflected equally'], 'Gamma rays are uncharged.'),
           ('Which is the largest source of background radiation for most people?', 'Radon gas from rocks and soil', ['Nuclear power stations', 'Mobile phones', 'Microwave ovens'], 'Radon is about half of the average dose.')],
    why=[('Explain why alpha particles are the most ionising type of radiation.', 'They are large, heavy and carry a +2 charge, so they interact strongly with atoms they pass and lose their energy quickly.'),
         ('Explain why gamma emission does not change the mass number or atomic number of a nucleus.', 'A gamma ray is electromagnetic radiation with no mass or charge; it only carries away excess energy.'),
         ('Explain why a background count must be subtracted from count-rate readings.', 'The detector also counts background radiation; subtracting it leaves only the count caused by the source.')],
    contrast=[('alpha radiation', 'gamma radiation', 'Alpha is a helium nucleus, strongly ionising, stopped by paper; gamma is an electromagnetic wave, weakly ionising, reduced only by thick lead or concrete.'),
              ('beta-minus decay', 'alpha decay', 'In beta-minus decay a neutron becomes a proton, so Z rises by 1 and A is unchanged; in alpha decay A falls by 4 and Z falls by 2.')],
    misc=[('Radioactive decay can be sped up by heating the source.', 'Decay is random and spontaneous; it is not affected by temperature, pressure or chemical reactions.'),
          ('An object exposed to gamma rays becomes radioactive.', 'Irradiation by gamma does not make an object radioactive; contamination (radioactive atoms on or in it) does.')],
    cases=[('Marie and Pierre Curie (1898)', 'The Curies isolated polonium and radium from pitchblende and showed radioactivity was a property of atoms.', 'discovery of radioactive elements', 'Marie Curie’s death from aplastic anaemia showed the dangers of radiation before they were understood.')],
    evaluate=[('Homes in high-radon areas should be required by law to install radon protection.', ['radon is a leading cause of lung cancer after smoking', 'sumps and ventilation are cheap compared with health costs'], ['cost falls on homeowners', 'risk varies greatly; testing first might be better'], 'Mandatory testing with required protection where levels are high balances health and cost.')],
    extended=[('Compare the nature, ionising power and penetration of alpha, beta and gamma radiation, and describe an experiment to identify which type(s) a source emits.', 'α: ⁴₂He, +2, highly ionising, stopped by paper / few cm air. β⁻: electron, −1, moderately ionising, stopped by ~3 mm aluminium. γ: EM wave, no charge, weakly ionising, reduced by thick lead. Experiment: measure background; record count rate with source near GM tube; insert paper, then aluminium, then lead; a large drop with paper → α; with aluminium → β; remaining count through Al → γ. Subtract background; handle source with tongs.', 6)],
))


@R.add('ch11-st2', 'C3', (1, 5), 'numerical')
def decay_eq(rng, slot):
    k = rng.choice(['alpha', 'beta', 'chain'] if slot.d >= 3 else ['alpha', 'beta'])
    alphas = [(92, 238), (88, 226), (86, 222), (94, 239), (95, 241), (84, 210), (90, 232)]
    betas = [(6, 14), (38, 90), (53, 131), (55, 137), (27, 60), (19, 40), (90, 234), (83, 210)]
    if k == 'alpha':
        Z, A = rng.choice(alphas)
        return dict(stem=f'^{A}_{Z}{SYM[Z]} decays by alpha emission. Write the balanced nuclear equation and name the daughter nuclide.', answer=f'^{A}_{Z}{SYM[Z]} → ^{A - 4}_{Z - 2}{SYM[Z - 2]} + ⁴₂He',
                    markingKey=f'B1 alpha = ⁴₂He; M1 A: {A} − 4 = {A - 4}; M1 Z: {Z} − 2 = {Z - 2}; A1 daughter {SYM[Z - 2]}-{A - 4}.', marks=4)
    if k == 'beta':
        Z, A = rng.choice(betas)
        return dict(stem=f'^{A}_{Z}{SYM[Z]} is a beta-minus emitter. Write the balanced nuclear equation for its decay.', answer=f'^{A}_{Z}{SYM[Z]} → ^{A}_{Z + 1}{SYM[Z + 1]} + ⁰₋₁e',
                    markingKey=f'B1 beta = ⁰₋₁e; M1 A unchanged ({A}); M1 Z rises to {Z + 1}; A1 daughter {SYM[Z + 1]}-{A}.', marks=4)
    Z, A = 92, 238
    na = rng.choice([1, 2, 3])
    nb = rng.choice([1, 2])
    Z2, A2 = Z - 2 * na + nb, A - 4 * na
    return dict(stem=f'Uranium-238 (Z = 92) undergoes {na} alpha {'decay' if na == 1 else 'decays'} and {nb} beta-minus {'decay' if nb == 1 else 'decays'}. Calculate the mass number and atomic number of the final nucleus.', answer=f'A = {A2}, Z = {Z2} ({SYM.get(Z2, "?")})',
                markingKey=f'M1 A = 238 − 4 × {na} = {A2}; M1 Z = 92 − 2 × {na} + {nb}; A1 Z = {Z2}; B1 element {SYM.get(Z2, "?")}.', marks=4)


inquiry('ch11-st2',
        dict(ctx='how the thickness of aluminium absorbers affects the count rate from a beta source',
             iv='thickness of aluminium (0, 0.5, 1.0, 1.5, 2.0, 2.5 mm)', dv='corrected count rate (counts per minute minus background)',
             cvs=[('distance between source and GM tube (fixed with a clamp)', 'count rate falls with distance'), ('the same source and GM tube', 'activity and detector efficiency differ'), ('counting time (1 minute, repeated three times)', 'decay is random so counts vary'), ('background count measured and subtracted', 'background adds to every reading')],
             hyp='If the aluminium thickness increases, then the count rate will decrease, because more beta particles are absorbed by the aluminium.',
             method='Measure the background count for 5 minutes; clamp the GM tube 5 cm from a strontium-90 source; record the count for 1 minute with no absorber; insert aluminium sheets of increasing thickness; record three 1-minute counts each; subtract background; plot corrected count rate against thickness.',
             weak=('counts varied a lot between repeats because decay is random', 'count for longer (e.g. 5 minutes) to reduce the percentage uncertainty'),
             safety='handle the source with tongs at arm’s length; never point it at anyone; keep exposure time short; return it to its lead box immediately'))
dataset('ch11-st2',
        dict(intro='{who} measured the corrected count rate from a beta source with different thicknesses of aluminium (three 1-minute counts each).', iv=('Aluminium thickness', 'mm'), xs=[0.0, 0.5, 1.0, 1.5, 2.0],
             dv=('Corrected count rate', 'counts/min'), f=lambda x: 840 * math.exp(-1.1 * x), dp=0, trend='The count rate falls as the aluminium gets thicker, quickly at first and then more slowly.',
             why='Thicker aluminium absorbs more of the beta particles; each extra layer removes a similar fraction of those remaining, so the decrease is roughly exponential.'))

R.facts('ch11-st3', F(
    terms=[('half-life', 'the time taken for the number of unstable nuclei (or the activity) of a sample to fall to half'),
           ('activity', 'the number of nuclei decaying per second, measured in becquerels (Bq)'),
           ('becquerel (Bq)', 'one decay per second'),
           ('random decay', 'it is impossible to predict when a particular nucleus will decay, only the probability'),
           ('radiometric dating', 'using the known half-life of an isotope to find the age of a rock or once-living material'),
           ('decay curve', 'a graph of activity (or number of nuclei) against time, falling by half every half-life')],
    facts=[('A sample has an activity of 800 Bq. Its half-life is 3 days. What is its activity after 9 days?', '100 Bq', ['200 Bq', '267 Bq', '0 Bq'], '9 days = 3 half-lives: 800 → 400 → 200 → 100.'),
           ('What fraction of the original nuclei remains after 4 half-lives?', '1/16', ['1/4', '1/8', '1/32'], '(1/2)⁴.'),
           ('Why is carbon-14 dating not used for rocks millions of years old?', 'Too little carbon-14 would remain to measure accurately', ['Rocks contain no atoms', 'Carbon-14 decays faster in rock', 'Its half-life is too long'], 'Half-life of C-14 ≈ 5700 years.'),
           ('Why is a short half-life gamma emitter used as a medical tracer?', 'It can be detected outside the body and its activity falls quickly so the dose is low', ['It is not ionising', 'It stays in the body for years', 'It makes the patient immune'], 'e.g. technetium-99m, 6 h.'),
           ('Why can we predict the half-life of a large sample but not when one nucleus will decay?', 'Decay is random, but with huge numbers of nuclei the overall rate is predictable', ['Large samples decay more slowly', 'Single nuclei never decay', 'Half-life depends on the sample size'], 'Statistics of large numbers.')],
    why=[('Explain why a long half-life makes nuclear waste difficult to deal with.', 'The waste stays radioactive for thousands of years, so it must be stored safely, isolated from people and groundwater, for a very long time.'),
         ('Explain why the activity of a sample never quite reaches zero in a decay curve model.', 'Each half-life only halves the number of undecayed nuclei, so in principle some remain; in practice, with very few nuclei left, the activity falls below background.'),
         ('Explain why a source with a half-life of a few hours would not be suitable for measuring paper thickness in a factory.', 'Its activity would fall quickly, so readings would change through the day and the source would need replacing very often.')],
    contrast=[('half-life', 'the lifetime of a single nucleus', 'Half-life is the time for half of a large sample to decay and is constant; the time at which one nucleus decays is random and unpredictable.'),
              ('a long half-life source', 'a short half-life source', 'A long half-life source has a low, slowly falling activity for a given number of nuclei and stays hazardous for a long time; a short half-life source is very active but its activity falls quickly.')],
    misc=[('After two half-lives a sample has completely decayed.', 'After two half-lives one quarter of the original nuclei remain.'),
          ('Half-life halves each time, so the second half-life is shorter.', 'Half-life is constant for an isotope; each half-life is the same length of time.')],
    cases=[('Ötzi the Iceman', 'Carbon-14 dating of the body found in the Alps in 1991 showed he lived about 5300 years ago.', 'radiocarbon dating', 'Dating needs a known half-life and an assumed starting ratio of C-14 to C-12.'),
           ('Technetium-99m in hospitals', 'About 40 million scans a year use Tc-99m, a gamma emitter with a 6-hour half-life produced from molybdenum-99.', 'choosing half-life for tracers', 'Supply relies on a few ageing reactors, so shortages affect patients worldwide.')],
    evaluate=[('Radiocarbon dating gives exact ages for archaeological remains.', ['based on a constant, well-measured half-life', 'calibrated against tree rings'], ['decay is random so results have uncertainty (e.g. ±50 years)', 'atmospheric C-14 levels have varied; contamination affects samples'], 'Radiocarbon dating gives reliable ages with stated uncertainty, not exact dates.')],
    extended=[('Explain what is meant by half-life, describe how you would determine it from a set of count-rate readings, and explain how half-life affects the choice of isotope for a medical tracer and for dating rocks.', 'Half-life: time for activity / number of undecayed nuclei to halve. Measure background; record count rate at regular intervals; subtract background; plot corrected count rate against time; read the time for the count to halve from several starting points and average. Tracer: short half-life (hours), gamma emitter → low dose, detectable outside. Dating rocks: half-life comparable with age (e.g. uranium-238, 4.5 billion years) so a measurable fraction remains.', 6)],
))


@R.add('ch11-st3', 'C3', (1, 5), 'numerical')
def half_life(rng, slot):
    k = rng.choice(['after', 'find', 'frac', 'age'] if slot.d >= 3 else ['after', 'frac'])
    if k == 'after':
        A0 = rng.choice([640, 800, 1200, 1600, 3200, 4800])
        h = rng.choice([2, 5, 6, 8, 12])
        n = rng.choice([2, 3, 4])
        unit = rng.choice(['hours', 'days', 'minutes'])
        return dict(stem=f'A radioactive source has an activity of {A0} Bq. Its half-life is {h} {unit}. Calculate its activity after {h * n} {unit}.', answer=f'{g(A0 / 2 ** n)} Bq',
                    markingKey=f'M1 {h * n} ÷ {h} = {n} half-lives; M1 {A0} × (1/2)^{n}; A1 {g(A0 / 2 ** n)} Bq.', marks=3)
    if k == 'find':
        A0 = rng.choice([960, 1280, 2000, 2400])
        n = rng.choice([2, 3, 4])
        h = rng.choice([3, 4, 10, 15, 20])
        return dict(stem=f'The corrected count rate of a sample falls from {A0} counts/min to {g(A0 / 2 ** n)} counts/min in {h * n} minutes. Calculate the half-life.', answer=f'{h} minutes',
                    markingKey=f'M1 {A0} → {g(A0 / 2 ** n)} is {n} halvings; M1 {h * n} ÷ {n}; A1 {h} minutes.', marks=3)
    if k == 'frac':
        n = rng.choice([2, 3, 4, 5])
        N0 = rng.choice([8000, 16000, 64000])
        return dict(stem=f'A sample contains {N0} undecayed nuclei. How many remain undecayed after {n} half-lives, and what fraction is this?', answer=f'{g(N0 / 2 ** n)} nuclei; 1/{2 ** n}',
                    markingKey=f'M1 {N0} × (1/2)^{n}; A1 {g(N0 / 2 ** n)}; B1 fraction 1/{2 ** n}.', marks=3)
    n = rng.choice([1, 2, 3])
    return dict(stem=f'A wooden tool contains 1/{2 ** n} of the carbon-14 found in living wood. The half-life of carbon-14 is 5700 years. Estimate the age of the tool, and give one reason the estimate is uncertain.', answer=f'{g(5700 * n)} years',
                markingKey=f'M1 1/{2 ** n} = {n} half-lives; A1 {n} × 5700 = {g(5700 * n)} years; B1 decay is random / C-14 levels in the atmosphere have varied / contamination.', marks=3)


inquiry('ch11-st3',
        dict(ctx='modelling radioactive decay by throwing dice, to find how the number of dice remaining changes with the number of throws',
             iv='throw number (0, 1, 2, … 10)', dv='number of dice remaining (a six counts as “decayed” and is removed)',
             cvs=[('the same starting number of dice (100)', 'the model needs a large sample'), ('fair six-sided dice', 'the decay probability must be 1/6 for each die'), ('the same rule for removing dice', 'changing the rule changes the “half-life”'), ('dice thrown in the same tray', 'dice falling out would be miscounted')],
             hyp='If the number of throws increases, then the number of dice remaining will fall exponentially, halving every 3–4 throws, because each die has the same random 1/6 chance of “decaying” on each throw.',
             method='Throw 100 dice into a tray; remove those showing six and count the rest; repeat for 10 throws; repeat the whole experiment three times (or pool class results); plot dice remaining against throw number; read the “half-life” from the graph at several points.',
             weak=('with only 100 dice the curve was irregular', 'pool the class’s results so the sample is larger and the randomness averages out'),
             safety='a low-risk model; pick up dropped dice so no one slips'))
dataset('ch11-st3',
        dict(intro='{who} recorded the corrected count rate of a protactinium generator over time (three runs).', iv=('Time', 's'), xs=[0, 60, 120, 180, 240],
             dv=('Corrected count rate', 'counts/10 s'), f=lambda x: 400 * 0.5 ** (x / 70), dp=0, trend='The count rate falls rapidly and then more slowly, halving in roughly equal time intervals.',
             why='Each nucleus has a fixed probability of decaying per second, so the activity falls by the same fraction in equal times – an exponential decay with a constant half-life.'))

R.facts('ch11-st4', F(
    terms=[('nuclear fission', 'the splitting of a large unstable nucleus (e.g. uranium-235) into two smaller nuclei, releasing energy and neutrons'),
           ('chain reaction', 'a reaction in which neutrons released by fission cause further fissions'),
           ('nuclear fusion', 'the joining of two light nuclei (e.g. hydrogen isotopes) to form a heavier nucleus, releasing energy'),
           ('control rods', 'rods (e.g. boron) that absorb neutrons to control the rate of fission in a reactor'),
           ('moderator', 'a material (e.g. water or graphite) that slows neutrons down so they are more likely to cause fission'),
           ('critical mass', 'the minimum mass of fissile material needed for a self-sustaining chain reaction'),
           ('mass defect', 'the small decrease in total mass in a nuclear reaction, released as energy (E = mc²)')],
    facts=[('What must a uranium-235 nucleus absorb before it undergoes induced fission?', 'A slow neutron', ['A proton', 'An alpha particle', 'A gamma ray'], 'U-236 forms and splits.'),
           ('What is the job of the control rods in a reactor?', 'To absorb neutrons and so control the rate of fission', ['To slow neutrons down', 'To cool the reactor', 'To start the fission'], 'Lowering them reduces power.'),
           ('Why is fusion very difficult to achieve on Earth?', 'Nuclei must be extremely hot and close together to overcome their electrostatic repulsion', ['Hydrogen is very rare', 'Fusion produces no energy', 'Fusion needs uranium'], 'Temperatures over 100 million °C.'),
           ('Which process releases energy in the Sun?', 'Fusion of hydrogen into helium', ['Fission of uranium', 'Burning of hydrogen with oxygen', 'Radioactive decay of iron'], ''),
           ('What happens to the mass of the products in fission compared with the reactants?', 'It is slightly less; the difference is released as energy', ['It is greater', 'It is exactly the same', 'It becomes zero'], 'E = mc².')],
    why=[('Explain why a chain reaction can occur in uranium-235.', 'Each fission releases 2 or 3 neutrons; if at least one of them causes another fission, the reaction continues.'),
         ('Explain why fission products are a problem for nuclear power.', 'The daughter nuclei are radioactive, often with long half-lives, so spent fuel must be stored securely for thousands of years.'),
         ('Explain why fusion is described as a possible “clean” energy source.', 'It produces no CO₂ and no long-lived radioactive fission products; the fuel (deuterium, tritium bred from lithium) is abundant.')],
    contrast=[('nuclear fission', 'nuclear fusion', 'Fission splits a heavy nucleus into smaller ones; fusion joins light nuclei into a heavier one. Both convert a little mass into energy.'),
              ('control rods', 'the moderator', 'Control rods absorb neutrons to slow the rate of reaction; the moderator slows neutrons down so they can cause fission.')],
    misc=[('A nuclear reactor can explode like a nuclear bomb.', 'Reactor fuel is not enriched enough and is not assembled to form a supercritical mass; accidents involve steam or hydrogen explosions and fires, not nuclear explosions.'),
          ('Fusion reactors are already producing electricity for the grid.', 'Experiments such as JET and NIF have released fusion energy, but no fusion power station yet supplies the grid.')],
    cases=[('ITER, France', 'An international fusion reactor under construction, aiming to produce 500 MW of fusion power from 50 MW of heating.', 'fusion research', 'Huge cost and delays show the engineering challenge; success could transform energy supply.'),
           ('National Ignition Facility (2022)', 'Lasers focused on a deuterium–tritium pellet produced more fusion energy (3.15 MJ) than the laser energy delivered (2.05 MJ).', 'fusion ignition', 'A scientific milestone, though the lasers used far more electrical energy than was produced.')],
    evaluate=[('Governments should fund fusion research instead of building new fission power stations.', ['fusion has no long-lived waste and abundant fuel', 'no risk of meltdown'], ['fusion power may be decades away; climate action is needed now', 'fission is proven, low-carbon technology'], 'Fund both: fission for near-term low-carbon power, fusion as a long-term option.')],
    extended=[('Describe how a nuclear reactor uses fission to generate electricity, including the roles of the fuel, moderator, control rods and coolant, and evaluate nuclear power as a low-carbon energy source.', 'U-235 absorbs a slow neutron → splits into two daughters + 2–3 neutrons + energy; moderator slows neutrons; control rods absorb neutrons to keep one neutron per fission causing another; coolant carries heat to boiler → steam → turbine → generator. Evaluation: very low CO₂, reliable baseload, small fuel mass; but radioactive waste, high cost and long build time, accident risk (Chernobyl, Fukushima), proliferation concerns. Judgement with reasons.', 8)],
))


@R.add('ch11-st4', 'C3', (1, 5), 'numerical')
def emc2(rng, slot):
    k = rng.choice(['E', 'fiss', 'fuel'] if slot.d >= 3 else ['E', 'fiss'])
    c = 3e8
    if k == 'E':
        m = rng.choice([1e-3, 2e-3, 5e-6, 1e-6, 0.01])
        E = m * c * c
        return dict(stem=f'In a nuclear reaction, {sci(m)} kg of mass is converted into energy. Use E = mc² (c = 3.0 × 10⁸ m/s) to calculate the energy released.', answer=f'{sci(E)} J',
                    markingKey=f'M1 E = {sci(m)} × (3.0 × 10⁸)²; A1 {sci(E)} J.', marks=2)
    if k == 'fiss':
        Zb, Ab, Zc, Ac = rng.choice([(56, 141, 36, 92), (54, 140, 38, 94), (55, 137, 37, 96), (56, 144, 36, 89)])
        n_out = 236 - Ab - Ac
        return dict(stem=f'Uranium-235 (Z = 92) absorbs a neutron and splits into ^{Ab}_{Zb}{SYM.get(Zb, "X")} and a nucleus with Z = {Zc}, releasing {n_out} neutrons. Calculate the mass number of the second nucleus.', answer=f'{236 - Ab - n_out}',
                    markingKey=f'M1 total A before = 235 + 1 = 236; M1 236 − {Ab} − {n_out}; A1 {236 - Ab - n_out}; (Z check: 92 = {Zb} + {Zc}).', marks=3)
    Ef = 3.2e-11
    m = rng.choice([1, 2, 5])
    N = m * 1000 / 235 * 6.0e23
    E = N * Ef
    return dict(stem=f'Each fission of uranium-235 releases about 3.2 × 10⁻¹¹ J. Calculate the energy released by complete fission of {m} kg of U-235 (molar mass 235 g/mol, Avogadro constant 6.0 × 10²³), and compare with burning coal (30 MJ/kg).', answer=f'{sci(E)} J; equivalent to about {sci(E / 3e7)} kg of coal',
                markingKey=f'M1 moles = {m * 1000} ÷ 235; M1 nuclei = moles × 6.0 × 10²³ = {sci(N)}; A1 E = {sci(E)} J; B1 ÷ 3.0 × 10⁷ J/kg → {sci(E / 3e7)} kg of coal.', marks=4)


inquiry('ch11-st4',
        dict(ctx='how the number of neutrons released per fission affects the growth of a chain reaction, using a mousetrap-and-ball (or online) model',
             iv='number of “neutrons” (balls) released per triggered trap (1, 2, 3)', dv='number of traps triggered in the first 5 seconds',
             cvs=[('the same number of traps (50)', 'more traps give more possible events'), ('the same spacing of traps in the box', 'spacing affects the chance of a hit'), ('one starting ball dropped from the same height', 'starting energy affects the first event'), ('the same time window (video timed)', 'longer times give more triggers')],
             hyp='If more balls are released per trap, then the number of traps triggered will rise faster, because each event causes more further events – like extra neutrons in fission.',
             method='Set 50 mousetraps in a clear box, each loaded with 1, 2 or 3 table-tennis balls; drop a single ball in; video the box and count triggered traps in 5 s; repeat three times for each number of balls; compare with a branching-model simulation.',
             weak=('some balls escaped from the open top', 'use a lid to keep balls inside – a model of reflectors and critical mass'),
             safety='mousetraps can snap fingers; load them with tongs and wear eye protection'))
dataset('ch11-st4',
        dict(intro='{who} used a simulation to record the number of fissions in each generation of a chain reaction when 1.5 neutrons per fission went on to cause another fission on average.', iv=('Generation', ''), xs=[1, 2, 3, 4, 5],
             dv=('Number of fissions', ''), f=lambda x: 100 * 1.5 ** (x - 1), dp=0, trend='The number of fissions increases faster and faster with each generation.',
             why='Each fission produces more than one effective neutron, so the number of fissions multiplies each generation (exponential growth); control rods keep this factor at exactly 1 in a reactor.'))

R.facts('ch11-st5', F(
    terms=[('irradiation', 'exposing an object to radiation; it does not make the object radioactive'),
           ('contamination', 'unwanted radioactive atoms on or inside an object or person'),
           ('radiation dose', 'a measure of the harm radiation may cause to the body, measured in sieverts (Sv)'),
           ('radiotherapy', 'using ionising radiation to destroy cancer cells'),
           ('radioactive tracer', 'a radioactive isotope introduced into a system so its movement can be followed with a detector'),
           ('ALARA', '“as low as reasonably achievable” – the principle for limiting radiation exposure')],
    facts=[('Why is gamma radiation used to sterilise medical equipment?', 'It penetrates the packaging and kills microorganisms without making the equipment radioactive', ['It makes the equipment radioactive so bacteria die later', 'It heats the equipment', 'It removes dirt'], 'Irradiation, not contamination.'),
           ('Why is an alpha source inside the body more dangerous than outside?', 'Inside, alpha is absorbed by nearby cells and is highly ionising; outside, it is stopped by the dead skin layer', ['Alpha is more penetrating inside the body', 'Alpha turns into gamma inside the body', 'It is not – alpha is always harmless'], 'e.g. inhaled radon.'),
           ('Which radiation is used in smoke detectors?', 'Alpha (from americium-241)', ['Gamma', 'Beta', 'X-rays'], 'Smoke absorbs alpha, reducing the current.'),
           ('A worker’s badge records radiation dose. What unit is used?', 'Sievert (or millisievert)', ['Becquerel', 'Joule', 'Hertz'], 'Dose measures biological effect.'),
           ('Which precaution reduces exposure when handling a source?', 'Using long tongs to increase distance', ['Holding it close to see the label', 'Wearing a cotton glove only', 'Using it for as long as possible'], 'Time, distance, shielding.')],
    why=[('Explain why ionising radiation can cause cancer.', 'It can damage DNA in cells; mutations may cause cells to divide uncontrollably.'),
         ('Explain why radiotherapy beams are directed from several different angles.', 'The beams overlap at the tumour, giving it a high dose, while healthy tissue along each path receives a smaller dose.'),
         ('Explain why beta sources are used to monitor the thickness of paper in a factory.', 'Beta partly passes through paper; if the paper gets thicker, fewer beta particles reach the detector, so the rollers can be adjusted. Alpha would be fully stopped and gamma would hardly change.')],
    contrast=[('irradiation', 'contamination', 'Irradiation is exposure to radiation from a source outside, which stops when the source is removed; contamination is radioactive material on or in an object, which continues to emit radiation.'),
              ('radiotherapy', 'a medical tracer', 'Radiotherapy uses a large, targeted dose to kill cancer cells; a tracer uses a small dose of a short-lived gamma emitter to image an organ.')],
    misc=[('Any amount of radiation will definitely cause cancer.', 'Risk increases with dose; low doses (like background) carry a very small risk.'),
          ('Food that has been irradiated is radioactive.', 'Irradiated food is exposed to gamma rays but does not become radioactive.')],
    cases=[('Chernobyl, Ukraine (1986)', 'A reactor explosion and fire released radioactive iodine-131 and caesium-137 across Europe; about 350 000 people were relocated.', 'contamination and its effects', 'Thyroid cancers increased in children who consumed contaminated milk; the exclusion zone remains today.'),
           ('Fukushima Daiichi, Japan (2011)', 'A tsunami disabled cooling systems, causing meltdowns in three reactors and releases of radioactive material.', 'nuclear safety and risk', 'Few deaths from radiation, but evacuation caused great harm and changed energy policy in Japan and Germany.'),
           ('PET scans', 'Fluorine-18 (half-life 110 minutes) attached to glucose shows active cancer cells in the body.', 'tracers in medicine', 'Benefits of diagnosis outweigh the small dose; isotopes must be produced close to hospitals.')],
    evaluate=[('The benefits of using ionising radiation in medicine outweigh the risks.', ['diagnoses and treats cancers, saving many lives', 'doses are carefully controlled and kept ALARA'], ['small increase in cancer risk, especially from repeated scans', 'staff exposure and radioactive waste'], 'Benefits usually greatly outweigh the risks when each use is justified and doses are minimised.'),
              ('Food irradiation should be used more widely to reduce food waste.', ['kills bacteria and pests; extends shelf life', 'food does not become radioactive'], ['public mistrust and labelling concerns', 'may reduce some vitamins; cost of facilities'], 'Irradiation is safe and useful; clear labelling and public education are needed for wider use.')],
    extended=[('Discuss the uses of radioactive isotopes in medicine and industry, explaining how the type of radiation and half-life are chosen for each, and evaluate the risks and how they are managed.', 'Uses: tracers (Tc-99m gamma, 6 h – detectable outside, short dose); radiotherapy (Co-60 gamma, or targeted isotopes); sterilisation (gamma penetrates packaging); thickness gauges (beta, long half-life for steady readings); smoke detectors (alpha, Am-241, 432 years). Risks: DNA damage, cancer; contamination vs irradiation; managed by time–distance–shielding, dosimeters, ALARA, secure storage and disposal. Evaluation of benefits vs risks, judgement.', 8)],
))


@R.add('ch11-st5', 'C3', (1, 5), 'numerical')
def dose(rng, slot):
    k = rng.choice(['annual', 'compare', 'inv'] if slot.d >= 3 else ['annual', 'compare'])
    if k == 'annual':
        h = rng.choice([0.5, 1, 2, 3])
        r = rng.choice([0.2, 0.3, 0.4])
        days = rng.choice([200, 220, 250])
        D = h * r * days / 1000
        return dict(stem=f'A worker receives a dose rate of {r} μSv per hour above background for {h} {'hour' if h == 1 else 'hours'} a day on {days} working days a year. Calculate the extra annual dose in mSv and compare it with the 20 mSv annual limit for radiation workers.', answer=f'{g(D)} mSv; well below the 20 mSv limit',
                    markingKey=f'M1 {r} × {h} × {days} = {g(D * 1000)} μSv; A1 {g(D)} mSv; B1 comparison with 20 mSv.', marks=3)
    if k == 'compare':
        scan, sv = rng.choice([('chest X-ray', 0.02), ('CT scan of the head', 2), ('CT scan of the chest', 7), ('dental X-ray', 0.005)])
        bg = 2.7
        return dict(stem=f'A {scan} gives an effective dose of about {sv} mSv. The average annual background dose is {bg} mSv. Express the scan dose as a number of days of background radiation.', answer=f'about {g(sv / bg * 365)} days',
                    markingKey=f'M1 {bg} ÷ 365 = {g(bg / 365)} mSv per day; M1 {sv} ÷ {g(bg / 365)}; A1 ≈ {g(sv / bg * 365)} days.', marks=3)
    d1 = rng.choice([0.5, 1, 2])
    d2 = d1 * rng.choice([2, 3, 4])
    r1 = rng.choice([40, 80, 120])
    return dict(stem=f'The dose rate {d1} m from a gamma source is {r1} μSv/h. Gamma intensity follows an inverse-square law. Calculate the dose rate at {g(d2)} m.', answer=f'{g(r1 * (d1 / d2) ** 2)} μSv/h',
                markingKey=f'M1 rate ∝ 1/d²; M1 {r1} × ({d1}/{g(d2)})²; A1 {g(r1 * (d1 / d2) ** 2)} μSv/h.', marks=3)


inquiry('ch11-st5',
        dict(ctx='how the distance from a gamma source affects the corrected count rate, to justify using tongs',
             iv='distance between source and GM tube (10, 15, 20, 30, 40 cm)', dv='corrected count rate (counts per minute minus background)',
             cvs=[('the same source', 'activity differs between sources'), ('the same GM tube and counter', 'detectors differ in efficiency'), ('counting time (1 minute ×3)', 'decay is random'), ('source and tube aligned on a metre rule', 'misalignment reduces the count')],
             hyp='If the distance doubles, then the count rate will fall to about a quarter, because gamma radiation spreads out over a larger area (inverse-square law).',
             method='Measure background for 5 minutes; place a sealed cobalt-60 source on a metre rule facing the GM tube; record three 1-minute counts at each distance; subtract background; plot corrected count rate against 1/d² and test for a straight line.',
             weak=('the exact position of the source inside its holder was unknown, so distances were slightly wrong', 'plot count rate against 1/(d + x) and find the offset x, or use larger distances'),
             safety='use tongs; keep the source pointing away from people; limit time; store in a lead-lined box; staff supervision'))
dataset('ch11-st5',
        dict(intro='{who} measured the corrected count rate from a sealed gamma source at different distances (three 1-minute counts each).', iv=('Distance from source', 'cm'), xs=[10, 15, 20, 30, 40],
             dv=('Corrected count rate', 'counts/min'), f=lambda x: 360000 / x ** 2, dp=0, trend='The count rate falls rapidly as distance increases – roughly to a quarter when the distance doubles.',
             why='Gamma rays spread out from the source over the surface of a sphere, so intensity follows an inverse-square law; keeping a distance (tongs) greatly reduces exposure.'))


# =============================================================================================
# ch12 Space
# =============================================================================================
PLANETS = [('Mercury', 0.39, 0.24), ('Venus', 0.72, 0.62), ('Earth', 1.0, 1.0), ('Mars', 1.52, 1.88), ('Jupiter', 5.2, 11.9), ('Saturn', 9.58, 29.4)]

R.facts('ch12-st1', F(
    terms=[('orbit', 'the curved path of one body around another, held by gravity'),
           ('natural satellite', 'a body that orbits a planet naturally, e.g. the Moon'),
           ('artificial satellite', 'a human-made object placed in orbit, e.g. for communications or weather'),
           ('geostationary orbit', 'an orbit above the equator with a period of 24 hours, so the satellite stays above the same point on Earth'),
           ('dwarf planet', 'a body orbiting the Sun that is massive enough to be round but has not cleared its orbit, e.g. Pluto'),
           ('orbital speed', 'the speed of an orbiting body; for a circular orbit v = 2πr/T'),
           ('astronomical unit (AU)', 'the mean distance from the Earth to the Sun, about 1.5 × 10¹¹ m')],
    facts=[('What provides the centripetal force that keeps the Moon in orbit around the Earth?', 'The gravitational attraction of the Earth', ['The Moon’s magnetic field', 'Air resistance', 'The Sun’s light pressure'], 'Gravity acts towards the centre.'),
           ('How does the orbital period of a planet change with distance from the Sun?', 'Planets further away take longer to orbit', ['Further planets orbit faster', 'All planets take one year', 'There is no pattern'], 'Weaker gravity and longer path.'),
           ('A satellite in a circular orbit moves at constant speed. Why is it accelerating?', 'Its direction, and so its velocity, is constantly changing', ['Its speed is increasing', 'It is not accelerating', 'Its mass is changing'], 'Acceleration towards the centre.'),
           ('Why are polar-orbit satellites useful for mapping and weather monitoring?', 'The Earth rotates beneath them, so they pass over every part of the surface', ['They stay over one point', 'They are further away and see more', 'They do not need fuel'], 'Low orbit, period ~100 min.'),
           ('If a satellite moves to a lower orbit, what happens to its speed?', 'It increases', ['It decreases', 'It stays the same', 'It falls to zero'], 'Stronger gravity requires higher speed.')],
    why=[('Explain why a satellite in a stable orbit does not fall to Earth.', 'It is falling towards Earth all the time, but its sideways speed is so high that the Earth’s surface curves away as fast as it falls, so it keeps going round.'),
         ('Explain why a communications satellite is placed in a geostationary orbit.', 'It stays above the same point on the equator, so dishes on Earth can point at it without moving.'),
         ('Explain why the speed of a comet changes during its elliptical orbit.', 'Near the Sun gravity is stronger and the comet speeds up as it falls inward; far from the Sun it slows down as it moves outward against gravity.')],
    contrast=[('a geostationary orbit', 'a low polar orbit', 'A geostationary orbit is high (about 36 000 km), above the equator, with a 24-hour period; a low polar orbit is a few hundred kilometres up, passes over the poles and has a period of about 100 minutes.'),
              ('a planet', 'a dwarf planet', 'A planet orbits the Sun, is round and has cleared its orbit of other objects; a dwarf planet is round but has not cleared its orbit.')],
    misc=[('Astronauts float on the International Space Station because there is no gravity there.', 'Gravity at the ISS is about 90% of that on the surface; astronauts float because they and the station are in free fall together.'),
          ('Planets orbit the Sun in perfect circles.', 'Planetary orbits are ellipses, though most are close to circular.')],
    cases=[('Kepler’s laws (1609–1619)', 'Using Tycho Brahe’s data, Kepler showed planets move in ellipses and that T² is proportional to r³.', 'orbital patterns', 'Newton later explained the laws with his law of gravitation.'),
           ('Space debris', 'Over 30 000 tracked pieces of debris orbit Earth; collisions (e.g. Iridium–Cosmos 2009) create more fragments.', 'artificial satellites and their impacts', 'Debris threatens satellites and astronauts and raises questions about responsibility for clean-up.')],
    evaluate=[('Companies should be allowed to launch unlimited numbers of satellites for internet coverage.', ['brings internet to remote regions', 'commercial investment drives innovation'], ['increases space debris and collision risk', 'bright satellites interfere with astronomy'], 'Large constellations need international regulation of numbers, brightness and end-of-life disposal.')],
    extended=[('Describe how gravity keeps planets and satellites in orbit, explain how orbital speed and period change with orbital radius, and compare geostationary and polar orbits for different uses.', 'Gravity provides a centripetal force towards the central body; the body’s velocity is tangential, so it continuously changes direction. Larger radius → weaker gravity → lower speed and longer period (T² ∝ r³). Geostationary: 24 h, equatorial, ~36 000 km – communications, TV. Polar: low, ~100 min – mapping, weather, spying; scans whole Earth.', 6)],
))


@R.add('ch12-st1', 'C3', (1, 5), 'numerical')
def orbit_speed(rng, slot):
    k = rng.choice(['v', 'T', 'kepler'] if slot.d >= 3 else ['v', 'T'])
    if k == 'v':
        name_, r, T, Tu = rng.choice([('the Moon', 3.84e8, 27.3 * 86400, '27.3 days'), ('the Earth around the Sun', 1.5e11, 3.156e7, '365.25 days'),
                                      ('a GPS satellite', 2.66e7, 43080, '11.97 hours'), ('a geostationary satellite', 4.22e7, 86164, '23.93 hours')])
        v = 2 * math.pi * r / T
        return dict(stem=f'The orbital radius of {name_} is {sci(r)} m and its period is {Tu}. Calculate its orbital speed in m/s.', answer=f'{sci(v)} m/s',
                    markingKey=f'M1 T in seconds = {sci(T)} s; M1 v = 2πr ÷ T = 2π × {sci(r)} ÷ {sci(T)}; A1 {sci(v)} m/s.', marks=3)
    if k == 'T':
        h, v = rng.choice([(400, 7670), (500, 7610), (800, 7450), (1000, 7350)])
        r = (6370 + h) * 1000
        T = 2 * math.pi * r / v
        return dict(stem=f'A satellite orbits {h} km above the Earth’s surface (Earth’s radius 6370 km) at {v} m/s. Calculate its orbital period in minutes.', answer=f'{g(T / 60)} minutes',
                    markingKey=f'M1 r = 6370 + {h} = {6370 + h} km = {sci(r)} m; M1 T = 2πr ÷ v; A1 {g(T)} s; A1 {g(T / 60)} minutes.', marks=4)
    p1 = rng.choice(PLANETS[3:])
    T = p1[1] ** 1.5
    return dict(stem=f'Kepler’s third law states that T² ∝ r³. Using T = 1 year for Earth at r = 1 AU, calculate the orbital period of {p1[0]} at {p1[1]} AU.', answer=f'{g(T)} years',
                markingKey=f'M1 T² = r³ = {p1[1]}³; M1 T = √({g(p1[1] ** 3)}); A1 {g(T)} years.', marks=3)


inquiry('ch12-st1',
        dict(ctx='how the radius of a circular path affects the time period of a bung whirled on a string, as a model of orbits',
             iv='radius of the circle (0.3, 0.4, 0.5, 0.6, 0.7 m)', dv='time for 10 revolutions, used to find the period',
             cvs=[('the same hanging mass on the string (gives the same central force)', 'central force affects the period'), ('the same rubber bung', 'mass of the orbiting body matters in this model'), ('a horizontal circle, marker kept just below the tube', 'radius changes if the marker moves'), ('the same person timing', 'reaction time differs between people')],
             hyp='If the radius increases, then the period will increase, because with the same central force the bung must move more slowly around a longer path.',
             method='Thread a string through a glass tube; tie a rubber bung to one end and a 100 g mass to the other; mark the radius with a paper clip; whirl the bung so the clip stays just below the tube; time 10 revolutions; repeat three times for each radius; calculate T and plot T² against r.',
             weak=('the paper clip drifted up and down, so the radius changed', 'have a partner watch the marker and only start timing once it is steady'),
             safety='wear eye protection; check the bung is tied securely; clear space around the student'))
dataset('ch12-st1',
        dict(intro='{who} used published data to compare orbital radius (in astronomical units) with orbital period for planets.', iv=('Orbital radius', 'AU'), xs=[0.4, 0.7, 1.0, 1.5, 5.2],
             dv=('Orbital period', 'years'), f=lambda x: x ** 1.5, dp=2, trend='The orbital period increases with orbital radius, and increases more than in proportion.',
             why='Further planets travel a longer path and, because gravity is weaker further from the Sun, they move more slowly; Kepler’s third law gives T² ∝ r³.'))

R.facts('ch12-st2', F(
    terms=[('nebula', 'a cloud of gas (mainly hydrogen) and dust in space where stars form'),
           ('protostar', 'a hot, dense ball of gas forming as a nebula collapses under gravity, before fusion starts'),
           ('main-sequence star', 'a stable star fusing hydrogen into helium in its core, where outward pressure balances gravity'),
           ('red giant', 'a star that has swollen and cooled after hydrogen in its core runs low, fusing helium and heavier elements'),
           ('white dwarf', 'the small, hot, dense core left after a Sun-like star sheds its outer layers'),
           ('supernova', 'the explosion of a massive star at the end of its life, scattering heavy elements'),
           ('neutron star', 'the extremely dense remnant of a supernova, made mostly of neutrons'),
           ('black hole', 'a region where gravity is so strong that not even light can escape')],
    facts=[('What balances the inward pull of gravity in a main-sequence star?', 'Outward pressure from energy released by fusion', ['Magnetic forces', 'The star’s rotation', 'Nothing – it is collapsing'], 'Equilibrium.'),
           ('What will the Sun eventually become?', 'A red giant, then a white dwarf', ['A supernova, then a black hole', 'A neutron star', 'A blue supergiant'], 'The Sun is not massive enough for a supernova.'),
           ('Where were elements heavier than iron formed?', 'In supernova explosions', ['In the Big Bang', 'In main-sequence stars like the Sun', 'In planets'], 'Fusion beyond iron absorbs energy.'),
           ('Which stars have the shortest lifetimes?', 'The most massive stars', ['The least massive stars', 'All stars have the same lifetime', 'White dwarfs'], 'They use fuel very rapidly.'),
           ('What determines whether a star ends as a white dwarf or a neutron star / black hole?', 'Its mass', ['Its colour at birth', 'Its distance from Earth', 'The number of planets around it'], 'Above about 8 solar masses → supernova.')],
    why=[('Explain why a protostar heats up as it forms.', 'Gravity pulls the gas inwards; gravitational potential energy is converted into thermal energy, so the particles move faster and the temperature rises until fusion can start.'),
         ('Explain why the iron in your blood was made inside stars.', 'Elements up to iron are made by fusion in the cores of massive stars; these were scattered by supernovae and became part of the cloud that formed the Sun and Earth.'),
         ('Explain why a star leaves the main sequence.', 'The hydrogen in its core runs low, so fusion slows, the core contracts and heats, and the outer layers expand – it becomes a red giant (or supergiant).')],
    contrast=[('a white dwarf', 'a neutron star', 'A white dwarf is the remnant of a Sun-like star, about Earth-sized and held up by electron pressure; a neutron star forms in a supernova of a massive star, is only about 20 km across and is made of neutrons.'),
              ('the life cycle of a Sun-like star', 'the life cycle of a massive star', 'A Sun-like star becomes a red giant, then a white dwarf; a massive star becomes a red supergiant, explodes as a supernova and leaves a neutron star or black hole.')],
    misc=[('Stars burn hydrogen like a fire.', 'Stars release energy by nuclear fusion of hydrogen nuclei, not by chemical burning with oxygen.'),
          ('Black holes suck in everything in the universe.', 'Far from a black hole its gravity is like that of any object of the same mass; only matter that comes close is captured.')],
    cases=[('Betelgeuse dimming (2019–2020)', 'The red supergiant Betelgeuse dimmed noticeably; observations showed a dust cloud ejected by the star rather than an imminent supernova.', 'late stages of massive stars', 'Shows how new observations test predictions.'),
           ('Supernova 1987A', 'A supernova in the Large Magellanic Cloud was seen with the naked eye; neutrino detectors recorded the burst hours before the light arrived.', 'supernovae', 'Confirmed models of core collapse in massive stars.')],
    evaluate=[('“We are made of star stuff” (Carl Sagan) is scientifically accurate.', ['carbon, oxygen, nitrogen and iron were made by fusion in stars', 'supernovae scattered these elements into the gas that formed the solar system'], ['hydrogen in our bodies was made in the Big Bang, not in stars', 'some light elements come from other processes'], 'Mostly accurate: almost all elements heavier than helium in our bodies were made in stars.')],
    extended=[('Describe the life cycle of a star with a mass much greater than the Sun, explaining the role of gravity and fusion at each stage, and compare it with the life cycle of the Sun.', 'Nebula collapses under gravity → protostar heats → fusion of H begins → main sequence (fusion pressure balances gravity). Massive star: H runs out → red supergiant, fuses heavier elements up to iron → core collapses → supernova → neutron star or black hole. Sun: main sequence ~10 billion years → red giant → sheds planetary nebula → white dwarf. Massive stars live shorter lives and make heavy elements.', 6)],
))


@R.add('ch12-st2', 'C3', (1, 5), 'numerical')
def star_calc(rng, slot):
    k = rng.choice(['life', 'mass', 'wien'] if slot.d >= 3 else ['life', 'mass'])
    if k == 'life':
        M = rng.choice([2, 4, 10, 0.5])
        t = 10 * M ** -2.5
        return dict(stem=f'A star’s main-sequence lifetime is roughly t = 10 × M^(−2.5) billion years, where M is its mass in solar masses. Estimate the lifetime of a star of {M} solar masses, and explain why massive stars live shorter lives.', answer=f'about {g(t)} billion years',
                    markingKey=f'M1 t = 10 × {M}^(−2.5); A1 ≈ {g(t)} billion years; B1 massive stars have stronger gravity, hotter cores and fuse hydrogen much faster.', marks=3)
    if k == 'mass':
        rate = 6.0e11
        yrs = rng.choice([1, 100, 1000])
        m = rate * 3.16e7 * yrs
        return dict(stem=f'The Sun fuses about 6.0 × 10¹¹ kg of hydrogen every second. Calculate the mass of hydrogen fused in {yrs} {'year' if yrs == 1 else 'years'} (1 year = 3.16 × 10⁷ s).', answer=f'{sci(m)} kg',
                    markingKey=f'M1 seconds = {yrs} × 3.16 × 10⁷; M1 6.0 × 10¹¹ × seconds; A1 {sci(m)} kg.', marks=3)
    Tk = rng.choice([3000, 5800, 10000, 20000])
    lam = 2.9e-3 / Tk
    return dict(stem=f'Wien’s law gives the peak wavelength emitted by a star: λ = 2.9 × 10⁻³ ÷ T (T in kelvin). Calculate λ for a star with surface temperature {Tk} K and state the star’s likely colour.', answer=f'{g(lam * 1e9)} nm; {"red" if Tk < 4000 else "yellow-white" if Tk < 7000 else "blue-white"}',
                markingKey=f'M1 λ = 2.9 × 10⁻³ ÷ {Tk}; A1 {sci(lam)} m = {g(lam * 1e9)} nm; B1 colour {"red (peak in infrared/red)" if Tk < 4000 else "yellow-white" if Tk < 7000 else "blue-white (peak in UV)"}.', marks=3)


inquiry('ch12-st2',
        dict(ctx='how the temperature of a glowing filament affects its colour, as a model for star colour and temperature',
             iv='voltage across a 12 V filament lamp (2, 4, 6, 8, 10, 12 V), giving different filament temperatures', dv='ratio of red to blue light intensity measured with a light sensor and coloured filters',
             cvs=[('the same lamp', 'filaments differ'), ('the same distance from lamp to sensor', 'intensity depends on distance'), ('a darkened room', 'room light adds to readings'), ('the same filters and sensor', 'filters transmit different amounts')],
             hyp='If the voltage increases, then the red-to-blue ratio will decrease, because a hotter filament emits relatively more short-wavelength (blue) light, just as hotter stars appear bluer.',
             method='Connect the lamp to a variable supply and measure the voltage; fix a light sensor 20 cm away in a dark box; for each voltage take readings through a red then a blue filter; repeat three times; calculate the red:blue ratio and plot it against voltage.',
             weak=('the lamp heated the box, affecting the sensor', 'switch off between readings and take readings quickly'),
             safety='the lamp gets very hot; do not touch it; keep below the rated voltage'))
dataset('ch12-st2',
        dict(intro='{who} used published data for main-sequence stars to compare mass with estimated lifetime.', iv=('Mass of star', 'solar masses'), xs=[0.8, 1.0, 1.5, 2.0, 3.0],
             dv=('Main-sequence lifetime', 'billion years'), f=lambda x: 10 * x ** -2.5, dp=2, trend='The lifetime falls steeply as the mass of the star increases.',
             why='A more massive star has stronger gravity, so its core is hotter and denser and fuses hydrogen much faster; it uses up its fuel sooner even though it has more of it.'))

R.facts('ch12-st3', F(
    terms=[('red-shift', 'the increase in wavelength of light from a source moving away from the observer; spectral lines shift towards the red end'),
           ('absorption spectrum', 'a continuous spectrum crossed by dark lines where elements in a star’s atmosphere absorb particular wavelengths'),
           ('Big Bang theory', 'the theory that the universe began about 13.8 billion years ago from an extremely hot, dense state and has been expanding ever since'),
           ('cosmic microwave background (CMB)', 'microwave radiation coming from all directions – the cooled remnant of radiation from the early universe'),
           ('Hubble’s law', 'the recession speed of a galaxy is proportional to its distance: v = H₀d'),
           ('light-year', 'the distance light travels in one year, about 9.46 × 10¹⁵ m'),
           ('galaxy', 'a huge system of billions of stars held together by gravity, e.g. the Milky Way')],
    facts=[('What do astronomers observe in the spectra of almost all distant galaxies?', 'The absorption lines are shifted towards longer (redder) wavelengths', ['The lines are shifted towards blue', 'There are no absorption lines', 'The lines are always in the same place as on Earth'], 'Red-shift.'),
           ('What does it mean that more distant galaxies show greater red-shift?', 'More distant galaxies are moving away faster, so the universe is expanding', ['Distant galaxies are hotter', 'Distant galaxies are made of different elements', 'Light slows down over long distances'], 'Hubble 1929.'),
           ('Which observation is strong evidence for the Big Bang and not for a steady-state universe?', 'The cosmic microwave background radiation', ['The existence of stars', 'The colour of the Sun', 'The orbits of planets'], 'Predicted remnant of the hot early universe.'),
           ('Why is the CMB now detected as microwaves rather than visible light or gamma rays?', 'The expansion of the universe has stretched its wavelength', ['It was always microwaves', 'Dust absorbed the visible light', 'Microwaves travel faster'], 'Extreme red-shift.'),
           ('A galaxy shows a blue-shift. What does this tell you?', 'It is moving towards us', ['It is moving away fast', 'It is very old', 'It is very hot'], 'e.g. the Andromeda galaxy.')],
    why=[('Explain how red-shift shows that the universe is expanding.', 'Light from distant galaxies is red-shifted, showing they are moving away; the further away a galaxy is, the greater its red-shift, so space itself is expanding in all directions.'),
         ('Explain why the age of the universe can be estimated from Hubble’s constant.', 'If galaxies have been moving apart at speed v from a single point, the time taken to reach distance d is d/v = 1/H₀, which gives an estimate of the time since the Big Bang.'),
         ('Explain why scientists accept the Big Bang theory rather than the steady-state theory.', 'Both explain red-shift, but only the Big Bang predicts the cosmic microwave background and the observed abundance of hydrogen and helium.')],
    contrast=[('red-shift', 'blue-shift', 'Red-shift is an increase in wavelength from a source moving away; blue-shift is a decrease in wavelength from a source moving towards the observer.'),
              ('the Big Bang theory', 'the steady-state theory', 'The Big Bang theory says the universe began in a hot, dense state and is expanding and cooling; the steady-state theory said the universe has always existed, with new matter created as it expands, keeping density constant.')],
    misc=[('The Big Bang was an explosion at a particular point in space.', 'The Big Bang was the expansion of space itself everywhere, not an explosion into existing space from a centre.'),
          ('Red-shift means a galaxy looks red to the eye.', 'Red-shift means spectral lines are shifted to longer wavelengths; the galaxy need not appear red.')],
    cases=[('Hubble and Humason (1929)', 'Using Cepheid variable stars for distances and spectra for speeds, Hubble showed recession speed is proportional to distance.', 'evidence for expansion', 'Changed our view from a static to an expanding universe.'),
           ('Discovery of the CMB (1964)', 'Penzias and Wilson found unexplained microwave “noise” from all directions in their radio antenna.', 'evidence for the Big Bang', 'An accidental discovery that matched predictions and led to the Nobel Prize in 1978.'),
           ('The Hubble tension', 'Measurements of H₀ from the CMB (about 67 km/s/Mpc) and from nearby supernovae (about 73 km/s/Mpc) disagree.', 'uncertainty in science', 'Either there are unknown errors or new physics is needed – an open question.')],
    evaluate=[('The Big Bang theory is proven beyond doubt.', ['red-shift, CMB and the abundance of light elements all support it', 'it makes successful predictions'], ['dark matter and dark energy are not yet understood', 'the Hubble tension shows measurements disagree'], 'The Big Bang is the best-supported model, but science never proves theories absolutely and details are still being refined.')],
    extended=[('Explain what red-shift is and how observations of red-shift and the cosmic microwave background support the Big Bang theory. Discuss why scientific ideas about the origin of the universe have changed over time.', 'Red-shift: absorption lines from distant galaxies shifted to longer wavelengths → galaxies receding. Greater distance → greater red-shift (Hubble’s law) → expanding universe → traced back to a single hot, dense origin. CMB: uniform microwave radiation from all directions, predicted as cooled radiation from early universe; steady-state could not explain it. Change: static universe → expanding (Hubble) → Big Bang vs steady state → Big Bang accepted after CMB; ongoing work on dark energy. Theories change with new evidence and technology.', 8)],
))


@R.add('ch12-st3', 'C3', (1, 5), 'numerical')
def hubble(rng, slot):
    k = rng.choice(['v', 'd', 'z', 'age', 'ly'] if slot.d >= 3 else ['v', 'd', 'ly'])
    H = 70
    if k == 'v':
        d = rng.choice([50, 120, 200, 450, 800])
        return dict(stem=f'Hubble’s constant is about {H} km/s per megaparsec (Mpc). Calculate the recession speed of a galaxy {d} Mpc away.', answer=f'{g(H * d)} km/s',
                    markingKey=f'M1 v = H₀d = {H} × {d}; A1 {g(H * d)} km/s.', marks=2)
    if k == 'd':
        v = rng.choice([3500, 7000, 14000, 21000])
        return dict(stem=f'A galaxy is receding at {v} km/s. Using H₀ = {H} km/s/Mpc, calculate its distance.', answer=f'{g(v / H)} Mpc',
                    markingKey=f'M1 d = v ÷ H₀ = {v} ÷ {H}; A1 {g(v / H)} Mpc.', marks=2)
    if k == 'z':
        l0 = rng.choice([393.4, 486.1, 656.3])
        z = rng.choice([0.01, 0.02, 0.05, 0.1])
        l = round(l0 * (1 + z), 1)
        z = (l - l0) / l0
        v = float(f'{z * 3e5:.3g}')
        return dict(stem=f'A spectral line with a laboratory wavelength of {l0} nm is observed at {l:.1f} nm in a galaxy’s spectrum. Calculate the red-shift z = Δλ/λ and the galaxy’s speed using v = zc (c = 3.0 × 10⁵ km/s).', answer=f'z = {g(z)}; v ≈ {g(v)} km/s',
                    markingKey=f'M1 Δλ = {l:.1f} − {l0} = {l - l0:.1f} nm; A1 z = {g(z)}; M1 v = {g(z)} × 3.0 × 10⁵; A1 ≈ {g(v)} km/s.', marks=4)
    if k == 'age':
        H2 = rng.choice([67, 70, 73])
        t = 977.8 / H2
        return dict(stem=f'The age of the universe can be estimated as 1/H₀. If H₀ = {H2} km/s/Mpc, then 1/H₀ = 977.8 ÷ {H2} billion years. Calculate the estimated age and explain why different values of H₀ give different ages.', answer=f'about {g(t)} billion years',
                    markingKey=f'M1 977.8 ÷ {H2}; A1 ≈ {g(t)} billion years; B1 larger H₀ → faster expansion → less time needed to reach present size, so a younger universe.', marks=3)
    ly = rng.choice([4.2, 8.6, 25, 2.5e6])
    m = ly * 9.46e15
    return dict(stem=f'A {"galaxy" if ly > 1e5 else "star"} is {g(ly)} light-years away. Convert this distance to metres (1 light-year = 9.46 × 10¹⁵ m) and state how long ago the light we see left it.', answer=f'{sci(m)} m; {g(ly)} years ago',
                markingKey=f'M1 {g(ly)} × 9.46 × 10¹⁵; A1 {sci(m)} m; B1 light left {g(ly)} years ago.', marks=3)


inquiry('ch12-st3',
        dict(ctx='how the distance between dots on an inflating balloon affects how fast they move apart, as a model of Hubble’s law',
             iv='initial distance of dots from a reference dot (2, 4, 6, 8, 10 cm)', dv='increase in distance from the reference dot after a set number of pumps',
             cvs=[('the same balloon', 'balloons stretch differently'), ('the same number of pump strokes', 'more air gives more stretching'), ('distances measured with a flexible tape along the surface', 'a straight ruler would cut across the curve'), ('dots drawn with the balloon partly inflated to the same size', 'starting size affects stretch')],
             hyp='If a dot starts further from the reference dot, then it will move away further in the same time, because the whole surface stretches uniformly – like galaxies receding faster with distance.',
             method='Partly inflate a balloon; draw a reference dot and five others at measured distances; add five pump strokes; remeasure each distance with a tape; calculate the increase; repeat with three balloons; plot increase (speed) against initial distance.',
             weak=('the balloon did not stretch evenly near the knot', 'draw dots around the middle of the balloon away from the knot'),
             safety='balloons can burst; wear eye protection and check for latex allergies'))
dataset('ch12-st3',
        dict(intro='{who} used published data to compare the distance of galaxies with their recession speed.', iv=('Distance', 'Mpc'), xs=[20, 50, 100, 150, 200],
             dv=('Recession speed', 'km/s'), f=lambda x: 70 * x, dp=0, trend='Recession speed increases in direct proportion to distance.',
             why='The universe is expanding uniformly, so galaxies twice as far away recede twice as fast (Hubble’s law); the gradient gives Hubble’s constant.'))

R.facts('ch12-st4', F(
    terms=[('refracting telescope', 'a telescope that uses lenses to collect and focus light'),
           ('reflecting telescope', 'a telescope that uses a large curved mirror to collect and focus light'),
           ('radio telescope', 'a large dish that collects radio waves from space'),
           ('space telescope', 'a telescope in orbit above the atmosphere, e.g. Hubble or James Webb'),
           ('resolution', 'the ability of a telescope to show fine detail and separate close objects'),
           ('exoplanet', 'a planet orbiting a star other than the Sun'),
           ('space probe', 'an uncrewed spacecraft sent to study other bodies in the solar system')],
    facts=[('Why are X-ray telescopes placed in space?', 'The atmosphere absorbs X-rays, so they cannot reach the ground', ['X-rays are too bright on Earth', 'X-ray telescopes are too heavy', 'X-rays only exist in space'], 'Gamma, X-ray and most UV/IR are absorbed.'),
           ('Why do professional optical telescopes on Earth have very large mirrors?', 'A larger aperture collects more light and gives better resolution', ['Large mirrors are cheaper', 'Large mirrors filter out radio waves', 'They magnify less'], 'Faint distant objects.'),
           ('Why are ground-based optical telescopes built on high mountains?', 'There is less atmosphere above them, so less absorption and turbulence', ['They are closer to the stars', 'It is warmer there', 'There is more light pollution'], 'Also drier and darker.'),
           ('Why does the James Webb Space Telescope observe mainly in the infrared?', 'Light from very distant galaxies is red-shifted into the infrared, and infrared passes through dust', ['Infrared is the brightest radiation', 'Visible light cannot travel in space', 'Infrared telescopes need no cooling'], 'It must be kept very cold.'),
           ('How are most exoplanets detected?', 'By the small dip in a star’s brightness as the planet passes in front of it (transit)', ['By seeing them directly with the eye', 'By their own light', 'By sound waves'], 'Kepler and TESS missions.')],
    why=[('Explain why radio telescopes are much larger than optical telescopes.', 'Radio waves have much longer wavelengths, and resolution depends on wavelength ÷ aperture, so a much larger dish is needed for similar detail.'),
         ('Explain why space telescopes give sharper images than similar telescopes on the ground.', 'Above the atmosphere there is no turbulence to blur images and no absorption of many wavelengths.'),
         ('Explain why astronomers use telescopes for several parts of the electromagnetic spectrum.', 'Different objects and processes emit different wavelengths, e.g. cool dust in infrared, hot gas in X-rays, so each part reveals different information.')],
    contrast=[('a reflecting telescope', 'a refracting telescope', 'A reflecting telescope uses a curved mirror and can be built very large; a refracting telescope uses lenses, which sag and cause colour fringes when very large.'),
              ('a space telescope', 'a ground-based telescope', 'A space telescope avoids atmospheric absorption and blurring but is expensive and hard to repair; a ground-based telescope can be larger, cheaper and upgraded but is limited by the atmosphere and weather.')],
    misc=[('Telescopes work mainly by making things look bigger.', 'Their main job is to collect more radiation (light-gathering power) and to resolve fine detail.'),
          ('Space telescopes are used because they are closer to the stars.', 'The extra distance of a few hundred kilometres is negligible; they are used to get above the atmosphere.')],
    cases=[('James Webb Space Telescope (2021)', 'A 6.5 m segmented mirror at the L2 point, 1.5 million km from Earth, observing in infrared at about −233 °C.', 'space telescopes', 'Has observed some of the earliest galaxies and the atmospheres of exoplanets; cost about $10 billion.'),
           ('Event Horizon Telescope (2019)', 'A network of radio telescopes across the world combined to act like an Earth-sized dish and imaged the shadow of the black hole in M87.', 'resolution and interferometry', 'International collaboration made a previously impossible observation.'),
           ('Mars rovers (Curiosity, Perseverance)', 'Robotic rovers analyse rocks for evidence of past water and life; Perseverance is collecting samples for return to Earth.', 'space exploration', 'Robots explore where humans cannot yet go, at lower cost and risk.')],
    evaluate=[('Money spent on space exploration would be better spent solving problems on Earth.', ['billions could fund health, education or climate action', 'benefits of exploration can seem distant'], ['satellites monitor climate, weather and crops', 'technology spin-offs (e.g. imaging, materials) and inspiration for science'], 'Space spending is a small share of budgets and brings real benefits on Earth, so a balance is justified.'),
              ('Humans, not robots, should be sent to explore Mars.', ['humans can adapt and make decisions quickly', 'inspires the public'], ['far more expensive and risky; radiation and long journeys', 'robots can work for years without life support'], 'Robots are better value for most science now; human missions may follow once the risks are reduced.')],
    extended=[('Compare ground-based and space telescopes, explaining how the choice depends on the wavelength being observed, and evaluate the benefits and drawbacks of a major space mission such as the James Webb Space Telescope.', 'Atmosphere absorbs gamma, X-ray, most UV and IR → those need space telescopes; visible and radio reach the ground. Ground: large, cheap, maintainable; but turbulence, weather, light pollution. Space: sharp images, all wavelengths; but very expensive, no repair (JWST at L2), limited lifetime. JWST: infrared shows the earliest galaxies (red-shifted), star formation behind dust, exoplanet atmospheres; cost ~$10 billion, delays, risk of failure. Judgement weighing scientific return against cost.', 8)],
))


@R.add('ch12-st4', 'C3', (1, 5), 'numerical')
def telescope(rng, slot):
    k = rng.choice(['area', 'res', 'delay', 'transit'] if slot.d >= 3 else ['area', 'delay'])
    if k == 'area':
        d1 = rng.choice([0.1, 0.2, 0.25])
        d2 = rng.choice([2.4, 6.5, 8.2, 10])
        return dict(stem=f'Light-gathering power depends on mirror area. How many times more light does a {d2} m mirror collect than a {d1} m amateur telescope?', answer=f'{g((d2 / d1) ** 2)} times',
                    markingKey=f'M1 area ∝ diameter²; M1 ({d2} ÷ {d1})²; A1 {g((d2 / d1) ** 2)} times.', marks=3)
    if k == 'res':
        lam, nm = rng.choice([(550e-9, 'visible light of 550 nm'), (2e-6, 'infrared of 2 μm'), (0.21, 'radio waves of 21 cm')])
        D = rng.choice([2.4, 6.5, 100])
        th = 1.22 * lam / D
        return dict(stem=f'The smallest angle a telescope can resolve is θ = 1.22λ/D. Calculate θ (in radians) for a {D} m telescope observing {nm}, and explain what this shows about radio telescopes.', answer=f'{sci(th)} rad',
                    markingKey=f'M1 θ = 1.22 × {sci(lam)} ÷ {D}; A1 {sci(th)} rad; B1 long wavelengths need much larger apertures for the same resolution.', marks=3)
    if k == 'delay':
        body, d = rng.choice([('the Moon', 3.84e8), ('Mars (at closest approach)', 5.5e10), ('Mars (at its furthest)', 4.0e11), ('Jupiter', 6.3e11)])
        t = d / 3e8
        return dict(stem=f'A radio signal is sent to a probe at {body}, {sci(d)} m away. Calculate the time for the signal to arrive (c = 3.0 × 10⁸ m/s) and explain why rovers must drive themselves.', answer=f'{g(t)} s' + (f' (about {g(t / 60)} minutes)' if t > 120 else ''),
                    markingKey=f'M1 t = d ÷ c = {sci(d)} ÷ 3.0 × 10⁸; A1 {g(t)} s; B1 delay too long for real-time remote control.', marks=3)
    Rs = rng.choice([1.0, 0.8, 1.2])
    rp = rng.choice([0.01, 0.05, 0.1])
    dip = (rp / Rs) ** 2 * 100
    return dict(stem=f'A planet with radius {rp} times the Sun’s radius transits a star of radius {Rs} solar radii. The fractional dip in brightness is (r_planet ÷ r_star)². Calculate the percentage dip in brightness.', answer=f'{g(dip)}%',
                markingKey=f'M1 ({rp} ÷ {Rs})²; A1 {g(dip / 100)}; A1 {g(dip)}%.', marks=3)


inquiry('ch12-st4',
        dict(ctx='how the diameter of a lens aperture affects the ability to resolve two close light sources, as a model of telescope resolution',
             iv='aperture diameter (2, 4, 6, 8, 10 mm, set with card masks over a lens)', dv='greatest distance at which two LEDs 2 mm apart can still be seen as separate',
             cvs=[('the same LEDs and colour', 'wavelength affects resolution'), ('the same lens and observer', 'eyesight and lens quality differ'), ('a dark corridor', 'stray light reduces contrast'), ('LEDs at the same brightness', 'brighter sources are easier to separate')],
             hyp='If the aperture diameter increases, then the two LEDs can be resolved from further away, because a wider aperture produces less spreading (diffraction) of the light.',
             method='Fix two red LEDs 2 mm apart at the end of a corridor; view them through a lens covered by a card mask with a hole; walk back until they merge into one; measure the distance; repeat with each aperture and three observers; plot maximum distance against aperture.',
             weak=('different observers judged “merged” differently', 'use a camera and analyse the images, or average many observers'),
             safety='do not look at bright lights or the Sun through any lens; keep the corridor clear of trip hazards'))
dataset('ch12-st4',
        dict(intro='{who} measured the maximum distance at which two LEDs could be resolved through masks of different aperture (three observers).', iv=('Aperture diameter', 'mm'), xs=[2, 4, 6, 8, 10],
             dv=('Maximum resolving distance', 'm'), f=lambda x: 2.9 * x, dp=1, trend='The maximum resolving distance increases roughly in proportion to the aperture diameter.',
             why='A wider aperture reduces diffraction, so the smallest resolvable angle (≈1.22λ/D) is smaller and close sources can be separated from further away – why telescopes are built with large apertures.'))
evx(R, 'ch05-st4',
    ('Chemical companies should be judged on atom economy rather than percentage yield.', ['atom economy shows how much of the reactants ends up as useful product, so it measures waste at the design stage', 'a high-yield process can still produce large amounts of unwanted by-products'], ['percentage yield shows how efficiently a real process runs and affects cost', 'by-products may be sold or recycled, so a low atom economy is not always wasteful'], 'Both matter: atom economy for choosing a greener route, percentage yield for running it efficiently.'))
exx(R, 'ch05-st4', ('A pharmaceutical company makes a drug in a five-step synthesis, each step with an 80% yield. Calculate the overall yield, explain why real yields are less than 100%, and discuss how chemists could improve the sustainability of the process.', 'Overall yield = 0.8⁵ = 0.328 → 32.8%. Reasons: reversible reactions, side reactions, product lost in filtering/transfer, impure reactants. Improvements: fewer steps, catalysts / enzymes, higher atom-economy routes, recycle solvents and unreacted reactants, use renewable feedstocks; balance against cost and purity requirements.', 8))
