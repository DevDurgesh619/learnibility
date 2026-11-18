"""CBSE Class 12 Biology, chapters 1-4: reproduction in flowering plants, human reproduction, reproductive health,
principles of inheritance and variation.

Families are built from NCERT fact tables with the shared kit in g11_chemistry_kit.py; numbers (ploidy, gamete counts,
Mendelian ratios, probabilities, map distances) are computed here. Also defines small helpers reused by _b and _c.
"""
from __future__ import annotations

import itertools
from fractions import Fraction

from qbank import F, GIRLS, ar, mcq, name, num
from g11_chemistry_kit import build_all, sf, cap

P = 'cbse-g12-biology'


# ---------------------------------------------------------------- shared helpers

def table_mcq(rows, stem_fmt, why_fmt='{Ans}: {why}.', pool=None, k=3):
    """rows: (a, b, answer, why). MCQ over a fact table; wrong options are other rows' answers (or `pool`)."""
    def g(r):
        a, b, ans, why = r.choice(rows)
        src = pool if pool else [x[2] for x in rows]
        wrong = [x for x in dict.fromkeys(src) if x != ans]
        if len(wrong) < k:
            raise ValueError('pool too small')
        return mcq(stem_fmt.format(a=a, b=b), ans, r.sample(wrong, k), why_fmt.format(a=cap(a), b=b, ans=ans, Ans=cap(ans), why=why), r)
    return g


def table_rev(rows, stem_fmt, why_fmt='{a}: {ans}.'):
    """Reverse lookup: given the answer column, pick the row label (column a)."""
    def g(r):
        a, b, ans, why = r.choice(rows)
        wrong = [x[0] for x in rows if x[2] != ans and x[0] != a]
        wrong = list(dict.fromkeys(wrong))
        if len(wrong) < 3:
            raise ValueError('pool too small')
        return mcq(stem_fmt.format(ans=ans, b=b), a, r.sample(wrong, 3), why_fmt.format(a=cap(a), ans=ans, why=why), r)
    return g


def table_explain(rows, stem_fmt, key_fmt='{ans} (1); {why} (1).'):
    def g(r):
        a, b, ans, why = r.choice(rows)
        others = [f'{cap(x[2])}; {x[3]}' for x in rows if x[2] != ans]
        return {'stem': stem_fmt.format(a=a, b=b), 'answer': f'{cap(ans)}; {why}', 'key': key_fmt.format(ans=cap(ans), why=why),
                'distractors': r.sample(others, min(3, len(others)))}
    return g


def frac(x: Fraction) -> str:
    return str(x.numerator) if x.denominator == 1 else f'{x.numerator}/{x.denominator}'


# ---------------------------------------------------------------- ch01 sexual reproduction in flowering plants

PLANTS = [('rice', 24), ('maize', 20), ('wheat', 42), ('onion', 16), ('pea', 14), ('tomato', 24), ('potato', 48), ('sugarcane', 80)]
PLOIDY = [('the egg cell', 1), ('a synergid', 1), ('an antipodal cell', 1), ('the primary endosperm nucleus', 3), ('an endosperm cell', 3),
          ('a nucellus cell', 2), ('an integument cell', 2), ('the zygote', 2), ('a microspore (pollen grain)', 1), ('a cell of the anther wall', 2),
          ('a male gamete', 1), ('the megaspore mother cell', 2), ('a functional megaspore', 1), ('an aleurone cell of the endosperm', 3),
          ('a cell of the embryo', 2), ('a tapetum cell', 2)]


def ploidy(r):
    pl, n2 = r.choice(PLANTS)
    part, k = r.choice(PLOIDY)
    n = n2 // 2
    good = n * k
    wrong = [str(x) for x in dict.fromkeys([n, n2, 3 * n, 4 * n, n // 2 if n % 2 == 0 else 5 * n]) if x != good][:3]
    lab = {1: 'haploid (n)', 2: 'diploid (2n)', 3: 'triploid (3n)'}[k]
    return mcq(f'The leaf cells of {pl} have {n2} chromosomes. How many chromosomes are present in {part}?', str(good), wrong,
               f'{cap(part)} is {lab}; n = {n}, so it has {good} chromosomes.', r)


def ploidy_x(r):
    pl, n2 = r.choice(PLANTS)
    a = r.choice(PLOIDY)
    b = r.choice([x for x in PLOIDY if x[1] != a[1]])
    n = n2 // 2
    lab = {1: 'n', 2: '2n', 3: '3n'}
    return {'stem': f'In {pl} (2n = {n2}), give the ploidy and the chromosome number of (i) {a[0]} and (ii) {b[0]}.',
            'answer': f'(i) {lab[a[1]]} = {n * a[1]}; (ii) {lab[b[1]]} = {n * b[1]}',
            'key': f'n = {n} (½); (i) {a[0]}: {lab[a[1]]} = {n * a[1]} (½ + ½); (ii) {b[0]}: {lab[b[1]]} = {n * b[1]} (½).',
            'distractors': [f'(i) {lab[a[1]]} = {n2 * a[1]}; (ii) {lab[b[1]]} = {n2 * b[1]}', f'(i) {lab[b[1]]} = {n * b[1]}; (ii) {lab[a[1]]} = {n * a[1]}',
                            f'(i) {lab[a[1]]} = {n * a[1]}; (ii) {lab[a[1]]} = {n * a[1]}']}


def meioses(r):
    s = r.choice([20, 40, 50, 60, 80, 100, 120, 200, 400])
    pmc = s // 4 if s % 4 == 0 else None
    if pmc is None:
        raise ValueError('not divisible')
    tot = s + pmc
    return {'stem': f'How many meiotic divisions are needed to produce {s} viable seeds in a flowering plant? Explain.',
            'answer': f'{tot} meiotic divisions',
            'key': f'Each seed needs one ovule, i.e. one megaspore mother cell ⇒ {s} meioses (1); each meiosis of a pollen mother cell gives 4 pollen grains, and one pollen grain fertilises one ovule ⇒ {s}/4 = {pmc} meioses (1); total = {tot}.',
            'distractors': [f'{s} meiotic divisions', f'{s // 4} meiotic divisions', f'{2 * s} meiotic divisions']}


CH1S1 = {
    'topic': 'flower structure and development of gametophytes',
    'terms': [('the androecium', 'the whorl of stamens, the male reproductive organ of the flower'),
              ('the gynoecium', 'the female reproductive part of the flower, made of one or more pistils'),
              ('the tapetum', 'the innermost wall layer of the microsporangium that nourishes the developing pollen grains'),
              ('microsporogenesis', 'the formation of microspores from a pollen mother cell by meiosis'),
              ('megasporogenesis', 'the formation of megaspores from the megaspore mother cell'),
              ('sporopollenin', 'the highly resistant organic material of the exine of a pollen grain'),
              ('the germ pore', 'the aperture in the exine where sporopollenin is absent'),
              ('the filiform apparatus', 'the special cellular thickenings at the micropylar tip of the synergids that guide the pollen tube')],
    'groups': [('a part of the stamen', ['anther', 'filament', 'connective']), ('a part of the pistil', ['stigma', 'style', 'ovary']),
               ('a part of the ovule', ['nucellus', 'integuments', 'funicle', 'hilum', 'micropyle', 'chalaza']),
               ('a wall layer of the microsporangium', ['epidermis', 'endothecium', 'middle layers', 'tapetum'])],
    'tf': (['A typical angiosperm anther is bilobed and dithecous.', 'A typical angiosperm embryo sac is 8-nucleate and 7-celled.', 'Pollen grains of many species can be stored in liquid nitrogen at −196 °C.',
            'The exine of the pollen grain is made of sporopollenin.', 'In most angiosperms only one megaspore is functional; the other three degenerate.', 'The vegetative cell of a pollen grain is larger and has abundant food reserve.'],
           [('The embryo sac is 7-nucleate and 8-celled.', 'It is 8-nucleate and 7-celled.'),
            ('The generative cell is larger than the vegetative cell.', 'The vegetative cell is bigger; the generative cell is small and spindle shaped.'),
            ('The tapetum is the outermost layer of the anther wall.', 'The epidermis is outermost; the tapetum is innermost and nourishes pollen.'),
            ('Monosporic development means the embryo sac forms from all four megaspores.', 'It forms from a single functional megaspore.'),
            ('Sporopollenin is easily degraded by enzymes.', 'Sporopollenin resists high temperature, strong acids and alkali, and no enzyme is known to degrade it.')]),
    'orders': [('sequence of microsporogenesis', ['sporogenous tissue', 'pollen mother cell', 'microspore tetrad', 'pollen grain'], 'Each pollen mother cell divides by meiosis to form a tetrad of microspores that mature into pollen.', '→'),
               ('sequence of wall layers of the microsporangium from outside to inside', ['epidermis', 'endothecium', 'middle layers', 'tapetum'], 'The tapetum is innermost and nourishes the developing pollen.', '→'),
               ('sequence in the development of the embryo sac', ['megaspore mother cell', 'four megaspores', 'functional megaspore', '2-nucleate stage', '4-nucleate stage', '8-nucleate embryo sac'], 'One meiosis then three free-nuclear mitoses.', '→')],
    'ar': [('Pollen grains are well preserved as fossils.', 'The exine contains sporopollenin, which is one of the most resistant organic materials.', 'a', 'It resists acids, alkali and high temperature.'),
           ('The embryo sac is 8-nucleate but 7-celled.', 'The two polar nuclei are present in a single large central cell.', 'a', 'Hence 8 nuclei in 7 cells.'),
           ('The functional megaspore undergoes meiosis to form the embryo sac.', 'The embryo sac develops by three successive mitotic divisions.', 'd', 'The functional megaspore divides by mitosis (free-nuclear), not meiosis; the reason is true.')],
    'features': {'intro': 'A cell or structure of the flower has these features:', 'q': 'Identify the cell or structure', 'what': 'structure', 'long': False,
                 'items': [('the tapetum', ['innermost wall layer of the anther', 'cells have dense cytoplasm', 'cells generally have more than one nucleus', 'nourishes the developing pollen grains']),
                           ('the synergids', ['two cells at the micropylar end', 'part of the egg apparatus with the egg cell', 'bear the filiform apparatus', 'guide the entry of the pollen tube']),
                           ('the antipodal cells', ['three cells at the chalazal end', 'haploid', 'part of the embryo sac', 'usually degenerate']),
                           ('the vegetative cell of a pollen grain', ['larger of the two cells', 'abundant food reserve', 'large irregularly shaped nucleus', 'forms the pollen tube'])]},
    'fams': [F('C3', 'D3', 'mcq', ploidy), F('C4', 'D4', 'explain', ploidy_x, marks=2), F('C4', 'D4', 'numerical', meioses, marks=2)],
    'qa': [('C4', 'D5', 'long', 'Describe the structure of a typical microsporangium with a labelled diagram. Explain the process of microsporogenesis.',
            'A transverse section shows four wall layers: epidermis, endothecium, 2–3 middle layers and the innermost tapetum, which nourishes pollen. The centre has sporogenous tissue whose cells act as pollen mother cells (2n); each undergoes meiosis to form a tetrad of four haploid microspores, which separate on dehydration and develop into pollen grains.',
            '2 marks labelled diagram; 1 mark wall layers and functions; 2 marks microsporogenesis.'),
           ('C4', 'D5', 'long', 'Describe the development of the female gametophyte in angiosperms. Draw a labelled diagram of a mature embryo sac.',
            'The megaspore mother cell (2n) in the nucellus at the micropylar region divides by meiosis to give four megaspores; one becomes functional (monosporic). Its nucleus divides mitotically three times (free-nuclear) to form 8 nuclei; cell walls form giving 3 cells of the egg apparatus (2 synergids, 1 egg) at the micropylar end, 3 antipodals at the chalazal end, and a large central cell with 2 polar nuclei. Thus 8-nucleate, 7-celled.',
            '2 marks development; 1 mark free-nuclear divisions; 2 marks labelled diagram.'),
           ('C4', 'D3', 'case', 'Nisha, a botany student, observes a pollen grain under the microscope. She sees a hard outer layer with some apertures and two cells inside.\n(i) Name the two layers of the pollen wall. (1 mark)\n(ii) What are the apertures called and why is sporopollenin absent there? (1 mark)\n(iii) Name the two cells and give one role of each. (2 marks)',
            '(i) Exine (outer, sporopollenin) and intine (inner, cellulose and pectin). (ii) Germ pores; the pollen tube emerges through them. (iii) Vegetative cell – forms the pollen tube; generative cell – divides to form two male gametes.',
            '(i) 1 (ii) 1 (iii) 1 + 1.', ('case',))],
}

CH1S2 = {
    'topic': 'pollination and pollen–pistil interaction',
    'terms': [('autogamy', 'the transfer of pollen grains from the anther to the stigma of the same flower'),
              ('geitonogamy', 'the transfer of pollen grains from the anther to the stigma of another flower of the same plant'),
              ('xenogamy', 'the transfer of pollen grains from the anther to the stigma of a flower of a different plant'),
              ('cleistogamous flowers', 'flowers that do not open at all, so that only autogamy is possible'),
              ('self-incompatibility', 'a genetic mechanism that prevents pollen from fertilising ovules of the same flower or plant by inhibiting pollen germination or tube growth'),
              ('emasculation', 'the removal of anthers from a bisexual flower bud before the anther dehisces'),
              ('bagging', 'covering the emasculated flower with a bag of butter paper to prevent contamination with unwanted pollen'),
              ('pollen–pistil interaction', 'the dynamic process from pollen deposition on the stigma to the entry of the pollen tube into the ovule')],
    'groups': [('a wind-pollinated plant', ['maize', 'wheat', 'rice', 'grasses']), ('a water-pollinated plant', ['Vallisneria', 'Hydrilla', 'Zostera']),
               ('an insect-pollinated plant', ['Salvia', 'Ophrys', 'Yucca', 'sunflower']), ('a plant with cleistogamous flowers', ['Viola (common pansy)', 'Oxalis', 'Commelina'])],
    'tf': (['Geitonogamy is functionally cross-pollination but genetically similar to autogamy.', 'Xenogamy brings genetically different pollen to the stigma.', 'Wind-pollinated flowers often have a single ovule in each ovary and numerous flowers packed in an inflorescence.',
            'In Vallisneria the female flower reaches the water surface by a long stalk.', 'Cleistogamous flowers produce assured seed set even without pollinators.', 'Pollen of wind-pollinated plants is light and non-sticky.'],
           [('Geitonogamy is genetically different from autogamy.', 'The pollen comes from the same plant, so it is genetically similar to autogamy.'),
            ('Cleistogamous flowers are always cross-pollinated.', 'They never open, so only autogamy occurs.'),
            ('Most water-pollinated plants are monocots like grasses.', 'Water pollination is limited to about 30 genera, mostly monocots such as Vallisneria, Hydrilla and Zostera; grasses are wind pollinated.'),
            ('In Yucca the moth gets nothing in return for pollinating the flower.', 'The moth lays eggs in the ovary and its larvae feed on some developing seeds.'),
            ('Wind-pollinated flowers have large, colourful petals and nectar.', 'They have small, inconspicuous flowers; insect-pollinated flowers are colourful and scented.')]),
    'ar': [('Self-incompatibility promotes cross-pollination.', 'It prevents pollen of the same flower from fertilising its ovules.', 'a', 'Pollen germination or tube growth is inhibited.'),
           ('Emasculation is needed only if the female parent bears bisexual flowers.', 'In unisexual female flowers there are no anthers to remove.', 'a', 'Only bagging is needed for unisexual flowers.'),
           ('Cleistogamous flowers are invariably autogamous.', 'Cleistogamous flowers do not open at all.', 'a', 'No chance of cross-pollen landing.'),
           ('Geitonogamy introduces genetic variation like xenogamy.', 'In geitonogamy the pollen comes from a different flower of the same plant.', 'd', 'Same plant ⇒ genetically like autogamy; the reason is true.')],
    'features': {'intro': 'A flower shows these adaptations:', 'q': 'Which mode of pollination is it adapted for', 'what': 'mode',
                 'items': [('wind pollination', ['light, non-sticky pollen', 'well-exposed stamens', 'large feathery stigma', 'single ovule in each ovary']),
                           ('insect pollination', ['large, colourful, fragrant flowers', 'rich in nectar', 'sticky pollen', 'flowers may be clustered into inflorescences to be conspicuous']),
                           ('water pollination', ['pollen protected by a mucilaginous covering', 'flowers at or below water surface', 'long ribbon-like pollen in seagrasses', 'seen in Vallisneria and Zostera'])]},
    'orders': [('sequence of steps in an artificial hybridisation programme', ['selection of parents', 'emasculation', 'bagging', 'dusting pollen on stigma', 'rebagging'], 'Emasculate before dehiscence, bag, then pollinate with desired pollen and rebag.', '→'),
               ('sequence of pollen–pistil interaction', ['pollen lands on stigma', 'pistil recognises compatible pollen', 'pollen germinates', 'pollen tube grows through style', 'tube enters ovule through micropyle', 'tube enters a synergid'], 'Guided by the filiform apparatus.', '→')],
    'qa': [('C4', 'D4', 'explain', 'Why is xenogamy considered better than autogamy? Give two outbreeding devices.',
            'Xenogamy brings genetically different pollen and produces variation and vigour. Outbreeding devices: pollen release and stigma receptivity not synchronised, anther and stigma at different positions, self-incompatibility, unisexual flowers (monoecy in castor/maize, dioecy in papaya).',
            '1 mark advantage; 1 mark two devices.'),
           ('C4', 'D3', 'case', 'A plant breeder in Ludhiana wants to cross a wheat variety with high yield (female parent) with one that is rust resistant.\n(i) Why must she emasculate the flowers of the female parent? (1 mark)\n(ii) Why are the flowers bagged? (1 mark)\n(iii) What would be different if the female parent had unisexual flowers? Explain. (2 marks)',
            '(i) Wheat flowers are bisexual; anthers must be removed before dehiscence to prevent self-pollination. (ii) Bagging with butter paper prevents contamination by unwanted pollen. (iii) Emasculation is not needed; female flower buds are only bagged, dusted with the desired pollen when the stigma is receptive, and rebagged.',
            '(i) 1 (ii) 1 (iii) 2.', ('case',)),
           ('C4', 'D5', 'long', 'What are outbreeding devices? Describe any three. Why is self-incompatibility considered a genetic mechanism?',
            'Devices that discourage self-pollination and encourage cross-pollination: (i) non-synchrony of pollen release and stigma receptivity; (ii) different positions of anther and stigma; (iii) self-incompatibility; (iv) production of unisexual flowers. Self-incompatibility is genetically controlled: the pistil recognises its own pollen through chemical interaction and inhibits germination or tube growth.',
            '1 mark definition; 3 marks three devices; 1 mark genetic basis.')],
}

CH1S3 = {
    'topic': 'double fertilisation and post-fertilisation events',
    'terms': [('syngamy', 'the fusion of one male gamete with the egg cell to form the zygote'),
              ('triple fusion', 'the fusion of the second male gamete with the two polar nuclei to form the primary endosperm nucleus'),
              ('double fertilisation', 'the occurrence of syngamy and triple fusion in the same embryo sac'),
              ('the scutellum', 'the single shield-shaped cotyledon of the grass embryo'),
              ('the coleoptile', 'the hollow foliar structure that encloses the plumule in a monocot embryo'),
              ('perisperm', 'the residual persistent nucellus in some seeds, such as black pepper and beet'),
              ('a false fruit', 'a fruit in which the thalamus also contributes to fruit formation, as in apple and strawberry'),
              ('seed dormancy', 'a state of inactivity in which the seed\'s metabolic activity slows down as it matures')],
    'groups': [('an albuminous seed', ['wheat', 'maize', 'barley', 'castor', 'sunflower']), ('a non-albuminous (exalbuminous) seed', ['pea', 'groundnut', 'bean']),
               ('a seed with perisperm', ['black pepper', 'beet']), ('a false fruit', ['apple', 'strawberry', 'cashew'])],
    'tf': (['Endosperm development precedes embryo development.', 'The coconut water is free-nuclear endosperm and the white kernel is cellular endosperm.', 'The primary endosperm nucleus is triploid.',
            'The zygote develops at the micropylar end of the embryo sac.', 'Seeds of some species can remain viable for hundreds of years; a lupine seed germinated after about 10,000 years.'],
           [('Embryo develops before the endosperm.', 'The endosperm develops first, to nourish the embryo.'),
            ('In pea and groundnut the endosperm persists in the mature seed.', 'They are non-albuminous; the endosperm is used up by the developing embryo.'),
            ('The primary endosperm nucleus is diploid.', 'It is triploid (two polar nuclei + one male gamete).'),
            ('After fertilisation the integuments form the fruit wall.', 'Integuments form the seed coat; the ovary wall forms the pericarp.'),
            ('The ovule develops into the fruit.', 'The ovule develops into the seed; the ovary develops into the fruit.')]),
    'ar': [('Endosperm formation precedes embryo formation.', 'The developing embryo needs nutrition from the endosperm.', 'a', 'Endosperm stores food for the embryo.'),
           ('The primary endosperm nucleus is triploid.', 'It is formed by fusion of two polar nuclei with one male gamete.', 'a', 'n + n + n = 3n.'),
           ('Apple is called a false fruit.', 'In apple the thalamus also contributes to fruit formation.', 'a', 'Not only the ovary forms the fruit.'),
           ('Pea seeds are albuminous.', 'In pea the endosperm is completely consumed during embryo development.', 'd', 'Pea seeds are non-albuminous; the reason is true.')],
    'features': {'intro': 'After fertilisation, a part of the flower develops as follows:', 'q': 'Which part of the ovule or flower forms it', 'what': 'part', 'long': False, 'case': False,
                 'items': [('the zygote', ['forms the embryo', 'develops at the micropylar end', 'divides after some endosperm has formed', 'passes through proembryo, globular and heart-shaped stages']),
                           ('the primary endosperm cell', ['forms the endosperm', 'triploid', 'repeated free-nuclear divisions in coconut', 'stores reserve food']),
                           ('the integuments', ['form the seed coat', 'harden as protective layers', 'micropyle remains as a small pore', 'outer becomes testa, inner becomes tegmen']),
                           ('the ovary wall', ['forms the pericarp (fruit wall)', 'may be fleshy as in guava, orange and mango', 'may be dry as in groundnut and mustard', 'protects the seeds'])]},
    'qa': [('C4', 'D4', 'explain', 'Why is fertilisation in angiosperms called double fertilisation? Name the products formed.',
            'Two fusions occur in each embryo sac: syngamy (male gamete + egg → diploid zygote) and triple fusion (male gamete + two polar nuclei → triploid primary endosperm nucleus).',
            '1 mark two fusions; 1 mark products with ploidy.'),
           ('C4', 'D5', 'long', 'Describe the post-fertilisation events in a flowering plant: development of endosperm and embryo, and maturation of the ovule into a seed and the ovary into a fruit. Distinguish between albuminous and non-albuminous seeds with examples.',
            'PEN divides to form endosperm (free-nuclear, then cellular; e.g. coconut). Zygote at the micropylar end forms proembryo, globular, heart-shaped and mature embryo. The ovule becomes the seed: integuments → seed coat, micropyle persists, water content falls, dormancy may set in. The ovary becomes the fruit; the ovary wall forms the pericarp. Albuminous seeds retain endosperm (wheat, maize, castor, sunflower); non-albuminous seeds have none left (pea, groundnut).',
            '1 mark endosperm; 1 mark embryo; 1 mark seed; 1 mark fruit; 1 mark seed types.'),
           ('C4', 'D3', 'case', 'Rahul splits open a tender coconut and finds sweet water inside; a mature coconut has a thick white kernel.\n(i) What does the coconut water represent? (1 mark)\n(ii) What is the white kernel? (1 mark)\n(iii) What is the ploidy of these tissues and how are they formed? (2 marks)',
            '(i) Free-nuclear endosperm (thousands of nuclei). (ii) Cellular endosperm. (iii) Triploid (3n); formed from the primary endosperm nucleus produced by triple fusion of a male gamete with two polar nuclei.',
            '(i) 1 (ii) 1 (iii) 2.', ('case',))],
}

CH1S4 = {
    'topic': 'apomixis, parthenocarpy and polyembryony',
    'terms': [('apomixis', 'the production of seeds without fertilisation, a form of asexual reproduction that mimics sexual reproduction'),
              ('parthenocarpy', 'the development of fruit without fertilisation, giving seedless fruits'),
              ('polyembryony', 'the occurrence of more than one embryo in a seed'),
              ('a hybrid variety', 'a variety produced by crossing two genetically different parents, whose seed must be produced every year'),
              ('nucellar embryony', 'the development of embryos from nucellar cells that protrude into the embryo sac')],
    'groups': [('a plant showing apomixis', ['some species of Asteraceae', 'grasses (some species)']), ('a plant showing polyembryony', ['mango', 'jamun (Syzygium)']),
               ('a parthenocarpic fruit', ['banana', 'seedless grapes (induced)', 'seedless watermelon (induced)'])],
    'classify': False,
    'tf': (['Apomictic embryos are genetically identical to the parent.', 'Parthenocarpy can be induced by growth hormones.', 'Polyembryony is common in citrus and mango.',
            'If hybrids are made apomictic, farmers can keep using hybrid seed year after year.', 'Banana is a parthenocarpic fruit.'],
           [('Apomixis requires fertilisation of the egg.', 'Apomixis produces seeds without fertilisation.'),
            ('Seeds of hybrids maintain hybrid characters in the next generation.', 'Hybrid characters segregate in the progeny, so hybrid seed must be bought every year.'),
            ('Parthenocarpic fruits contain many seeds.', 'They are seedless as no fertilisation occurs.'),
            ('Polyembryony means more than one seed in a fruit.', 'It means more than one embryo in a seed.')]),
    'ar': [('Farmers have to buy hybrid seeds every year.', 'Hybrid characters segregate in the progeny of hybrids.', 'a', 'Progeny of hybrids do not retain hybrid vigour uniformly.'),
           ('Apomixis is important for the hybrid seed industry.', 'Apomictic hybrids do not show segregation of characters.', 'a', 'Seed can be reused.'),
           ('Banana fruits have no seeds.', 'Banana is a parthenocarpic fruit.', 'a', 'Fruit develops without fertilisation.'),
           ('Nucellar embryos are genetically different from the parent.', 'Nucellar cells are diploid cells of the mother plant.', 'd', 'Nucellar embryos are clones of the parent; the reason is true.')],
    'features': {'intro': 'A special mode of reproduction in plants shows:', 'q': 'Which phenomenon is it', 'what': 'phenomenon', 'case': False,
                 'items': [('apomixis', ['seeds without fertilisation', 'embryo genetically identical to the parent', 'seen in some Asteraceae and grasses', 'useful to fix hybrid vigour']),
                           ('parthenocarpy', ['fruit without fertilisation', 'fruits are seedless', 'can be induced by growth hormones', 'seen in banana']),
                           ('polyembryony', ['more than one embryo in a seed', 'often from nucellar cells', 'seen in citrus and mango', 'extra embryos are genetically identical to the parent'])]},
    'qa': [('C4', 'D4', 'explain', 'If one can induce parthenocarpy through the application of growth substances, which fruits would you select to induce parthenocarpy and why?',
            'Fruits that are eaten fresh and whose seeds are a nuisance, such as orange, lemon, watermelon, grapes and guava; seedless fruits are preferred by consumers and are easier to process for juice.',
            '1 mark examples; 1 mark reason.'),
           ('C4', 'D3', 'case', 'Seema notices that when she sows seeds from the orange tree in her garden at Nagpur, several seedlings come out of a single seed.\n(i) Name the phenomenon. (1 mark)\n(ii) From which cells do the extra embryos arise? (1 mark)\n(iii) Are the seedlings genetically like the parent? Explain, and state one advantage to horticulture. (2 marks)',
            '(i) Polyembryony. (ii) Nucellar cells that protrude into the embryo sac (nucellar embryony). (iii) Yes, nucellar embryos are clones of the mother plant as they form without fertilisation; uniform, true-to-type seedlings can be raised.',
            '(i) 1 (ii) 1 (iii) 2.', ('case',))],
}

# ---------------------------------------------------------------- ch02 human reproduction

HCELLS = [('a spermatogonium', 46), ('a primary spermatocyte', 46), ('a secondary spermatocyte', 23), ('a spermatid', 23), ('a sperm', 23),
          ('an oogonium', 46), ('a primary oocyte', 46), ('a secondary oocyte', 23), ('the first polar body', 23), ('the zygote', 46),
          ('a Sertoli cell', 46), ('a Leydig cell', 46), ('an ovum', 23)]


def hchrom(r):
    c, n = r.choice(HCELLS)
    wrong = [str(x) for x in (23, 46, 92, 69) if x != n][:3]
    return mcq(f'How many chromosomes are present in {c} of a human?', str(n), wrong,
               f'{cap(c)} is {"haploid (n = 23)" if n == 23 else "diploid (2n = 46)"}.', r)


GAM = [('primary spermatocytes', 4, 'sperms'), ('secondary spermatocytes', 2, 'sperms'), ('spermatids', 1, 'sperms'),
       ('primary oocytes', 1, 'ova'), ('secondary oocytes', 1, 'ova')]


def gamete_count(r):
    c, f, g = r.choice(GAM)
    n = r.choice([10, 25, 50, 100, 200, 500])
    why = {'primary spermatocytes': 'each primary spermatocyte completes meiosis I and II to give 4 spermatids, each forming a sperm',
           'secondary spermatocytes': 'each secondary spermatocyte completes meiosis II to give 2 spermatids',
           'spermatids': 'each spermatid changes into one sperm by spermiogenesis',
           'primary oocytes': 'meiosis is unequal; each primary oocyte gives one ovum and polar bodies',
           'secondary oocytes': 'meiosis II is unequal; each secondary oocyte gives one ovum and a second polar body'}[c]
    return {'stem': f'How many {g} are formed from {n} {c}? Explain.', 'answer': f'{n * f} {g}',
            'key': f'{cap(why)} (1) ⇒ {n} × {f} = {n * f} {g} (1).',
            'distractors': [f'{n * 4 if f != 4 else n} {g}', f'{n * 2 if f != 2 else n * 4} {g}', f'{n // 2 if n % 2 == 0 else n * 3} {g}']}


CYCLE = [(r_, 'menstrual phase', 'the endometrium breaks down and menstrual flow occurs because no fertilisation took place') for r_ in (1, 2, 3, 4, 5)] + \
        [(d, 'follicular (proliferative) phase', 'primary follicles grow into a Graafian follicle and the endometrium regenerates under rising LH, FSH and oestrogen') for d in (7, 8, 9, 10, 11, 12)] + \
        [(14, 'ovulatory phase', 'the LH surge (with FSH) causes rupture of the Graafian follicle and release of the ovum')] + \
        [(d, 'luteal (secretory) phase', 'the corpus luteum secretes large amounts of progesterone that maintains the endometrium') for d in (16, 18, 20, 22, 24, 26)]


def cycle_phase(r):
    d, ph, why = r.choice(CYCLE)
    phases = ['menstrual phase', 'follicular (proliferative) phase', 'ovulatory phase', 'luteal (secretory) phase']
    who = r.choice(GIRLS)
    return mcq(f'In a regular 28-day menstrual cycle, which phase is {who}\'s body in on day {d}?', ph, [p for p in phases if p != ph],
               f'Day {d}: {ph} – {why}.', r)


CH2S1 = {
    'topic': 'male and female reproductive systems',
    'terms': [('the seminiferous tubules', 'the highly coiled tubules in each testicular lobule where sperms are produced'),
              ('Sertoli cells', 'the cells in the seminiferous tubules that provide nutrition to the germ cells'),
              ('Leydig cells', 'the interstitial cells outside the seminiferous tubules that synthesise and secrete androgens'),
              ('the scrotum', 'the pouch outside the abdominal cavity that keeps the testes 2–2.5 °C below body temperature'),
              ('the fimbriae', 'the finger-like projections of the infundibulum that help collect the ovum after ovulation'),
              ('the endometrium', 'the inner glandular layer lining the uterine cavity that undergoes cyclical changes'),
              ('the myometrium', 'the thick middle layer of smooth muscle of the uterus that contracts strongly during delivery'),
              ('the mammary lobes', 'the 15–20 masses of glandular tissue in each breast containing alveoli that secrete milk')],
    'groups': [('a male accessory duct', ['rete testis', 'vasa efferentia', 'epididymis', 'vas deferens']), ('a male accessory gland', ['seminal vesicles', 'prostate', 'bulbourethral glands']),
               ('a part of the oviduct', ['infundibulum', 'ampulla', 'isthmus']), ('a layer of the uterine wall', ['perimetrium', 'myometrium', 'endometrium'])],
    'tf': (['Each testis has about 250 compartments called testicular lobules.', 'Leydig cells secrete androgens.', 'The ampulla is the wider part of the oviduct where fertilisation usually occurs.',
            'The secretions of the accessory glands constitute seminal plasma rich in fructose, calcium and certain enzymes.', 'The scrotum keeps the testicular temperature 2–2.5 °C lower than body temperature.'],
           [('Sertoli cells secrete testosterone.', 'Leydig (interstitial) cells secrete androgens; Sertoli cells nourish germ cells.'),
            ('Fertilisation normally occurs in the uterus.', 'It occurs in the ampullary region of the oviduct.'),
            ('The endometrium is the outer layer of the uterus.', 'The perimetrium is outer; the endometrium is the inner glandular layer.'),
            ('The bulbourethral glands are female accessory glands.', 'They are male accessory glands whose secretion lubricates the penis.'),
            ('The testes are located inside the abdominal cavity.', 'They lie outside in the scrotum, which keeps them cooler for spermatogenesis.')]),
    'orders': [('path of sperms from the testis', ['seminiferous tubules', 'rete testis', 'vasa efferentia', 'epididymis', 'vas deferens', 'ejaculatory duct', 'urethra'], 'Sperms are stored in the epididymis and leave via vas deferens and urethra.', '→'),
               ('parts of the oviduct from ovary to uterus', ['infundibulum', 'ampulla', 'isthmus'], 'The funnel-shaped infundibulum is closest to the ovary; the narrow isthmus joins the uterus.', '→')],
    'ar': [('Testes are situated outside the abdominal cavity.', 'Spermatogenesis needs a temperature about 2–2.5 °C lower than body temperature.', 'a', 'The scrotum maintains this.'),
           ('The myometrium shows strong contractions during delivery.', 'It is a thick layer of smooth muscle.', 'a', 'Contractions expel the baby.'),
           ('Sertoli cells are called nurse cells.', 'Sertoli cells provide nutrition to the germ cells.', 'a', 'They nourish developing sperms.'),
           ('Leydig cells are found inside the seminiferous tubules.', 'Leydig cells secrete androgens.', 'd', 'They lie in the interstitial spaces outside the tubules; the reason is true.')],
    'features': {'intro': 'A structure of the human reproductive system has these features:', 'q': 'Identify the structure', 'what': 'structure',
                 'items': [('the epididymis', ['located along the posterior surface of each testis', 'stores sperms', 'receives sperms from vasa efferentia', 'leads to vas deferens']),
                           ('the seminal vesicles', ['paired male accessory glands', 'secretion rich in fructose', 'contribute to seminal plasma', 'open into the ejaculatory duct with vas deferens']),
                           ('the oviduct', ['about 10–12 cm long', 'has infundibulum, ampulla and isthmus', 'site of fertilisation', 'fimbriae collect the ovum']),
                           ('the uterus', ['inverted pear shape', 'wall has perimetrium, myometrium and endometrium', 'site of implantation', 'opens into the vagina through the cervix'])]},
    'qa': [('C4', 'D5', 'long', 'Draw a labelled diagram of the male reproductive system. Describe the role of the accessory ducts and glands.',
            'Diagram: testes in scrotum, epididymis, vas deferens, seminal vesicle, ejaculatory duct, prostate, bulbourethral gland, urethra, penis. Ducts (rete testis, vasa efferentia, epididymis, vas deferens) store and transport sperms; seminal vesicles, prostate and bulbourethral glands secrete seminal plasma rich in fructose, calcium and enzymes; bulbourethral secretion lubricates the penis.',
            '2 marks diagram; 1.5 marks ducts; 1.5 marks glands.'),
           ('C4', 'D4', 'explain', 'Describe the structure of a seminiferous tubule.',
            'Each tubule is lined by male germ cells (spermatogonia) that divide to form sperms, and by Sertoli cells that nourish the germ cells. Interstitial spaces outside contain blood vessels and Leydig cells that secrete androgens.',
            '1 mark germ cells and Sertoli cells; 1 mark interstitial cells.'),
           ('C4', 'D3', 'case', 'A doctor in Pune explains to a group of Class 12 students why the testes hang outside the body.\n(i) Name the structure that holds the testes. (1 mark)\n(ii) Why is this position necessary? (1 mark)\n(iii) Name the cells that make sperms and the cells that secrete testosterone in the testis. (2 marks)',
            '(i) Scrotum. (ii) It keeps the testes 2–2.5 °C below body temperature, needed for spermatogenesis. (iii) Spermatogonia (male germ cells) in the seminiferous tubules produce sperms; Leydig cells secrete testosterone.',
            '(i) 1 (ii) 1 (iii) 2.', ('case',))],
}

CH2S2 = {
    'topic': 'gametogenesis',
    'terms': [('spermatogenesis', 'the process by which spermatogonia in the testis produce sperms'),
              ('spermiogenesis', 'the transformation of spermatids into sperms'),
              ('spermiation', 'the release of sperms from the seminiferous tubules'),
              ('oogenesis', 'the process of formation of a mature female gamete'),
              ('the acrosome', 'the cap-like structure on the anterior part of the sperm head that contains enzymes for fertilisation'),
              ('the Graafian follicle', 'the mature tertiary follicle containing the secondary oocyte and a fluid-filled antrum'),
              ('the zona pellucida', 'the new membrane formed around the secondary oocyte in the Graafian follicle')],
    'tf': (['Oogenesis begins in the foetal ovary.', 'The middle piece of the sperm has numerous mitochondria.', 'Spermatogenesis starts at puberty due to increased GnRH.',
            'A human male ejaculates about 200–300 million sperms during a coitus.', 'The first polar body is formed at the end of meiosis I in oogenesis.'],
           [('Oogenesis starts at puberty.', 'It begins during foetal development; oogonia form and enter prophase I before birth.'),
            ('Each primary oocyte gives four functional ova.', 'Meiosis is unequal; one ovum and polar bodies form.'),
            ('Spermatids are diploid.', 'Spermatids are haploid; they form after meiosis II.'),
            ('FSH acts on the Leydig cells.', 'LH acts on Leydig cells to stimulate androgen secretion; FSH acts on Sertoli cells.'),
            ('Meiosis II in human oocytes is completed before ovulation.', 'The secondary oocyte completes meiosis II only after a sperm enters it.')]),
    'orders': [('sequence of spermatogenesis', ['spermatogonium', 'primary spermatocyte', 'secondary spermatocyte', 'spermatid', 'sperm'], 'Mitosis, meiosis I, meiosis II, then spermiogenesis.', '→'),
               ('sequence of follicle development', ['primary follicle', 'secondary follicle', 'tertiary follicle', 'Graafian follicle'], 'Layers of granulosa cells and an antrum develop progressively.', '→'),
               ('parts of a human sperm from front to back', ['acrosome', 'head (nucleus)', 'neck', 'middle piece', 'tail'], 'The acrosome caps the head; mitochondria in the middle piece power the tail.', '→')],
    'ar': [('The middle piece of a sperm has many mitochondria.', 'Mitochondria provide energy for the movement of the tail.', 'a', 'Sperm motility needs ATP.'),
           ('Polar bodies are formed during oogenesis.', 'Cytoplasmic division in oogenesis is unequal.', 'a', 'Most cytoplasm goes to the oocyte.'),
           ('A primary spermatocyte gives four sperms.', 'Meiosis in spermatogenesis is followed by equal cytoplasmic divisions.', 'a', 'Four spermatids, each forming a sperm.'),
           ('Spermatogenesis starts before birth.', 'Spermatogenesis starts at puberty under GnRH.', 'd', 'A is false; spermatogenesis begins at puberty.')],
    'features': {'intro': 'A process of gametogenesis has these features:', 'q': 'Which process is it', 'what': 'process', 'compare': True,
                 'items': [('spermatogenesis', ['starts at puberty', 'occurs in seminiferous tubules', 'one primary cell gives four gametes', 'continues throughout life']),
                           ('oogenesis', ['starts during foetal development', 'occurs in the ovary', 'one primary cell gives one gamete and polar bodies', 'stops at menopause'])]},
    'fams': [F('C3', 'D3', 'mcq', hchrom), F('C3', 'D3', 'numerical', gamete_count), F('C4', 'D4', 'numerical', gamete_count, marks=2)],
    'qa': [('C4', 'D5', 'long', 'Describe the process of oogenesis with a schematic diagram. How is it different from spermatogenesis in the number of gametes formed?',
            'Oogonia form in the foetal ovary and enter meiosis I as primary oocytes, which remain arrested in prophase I inside primary follicles. Follicles grow into secondary, tertiary and Graafian follicles. The primary oocyte completes meiosis I forming a large secondary oocyte and a small first polar body. The secondary oocyte is released at ovulation and completes meiosis II only on sperm entry, forming the ovum and a second polar body. One primary oocyte gives one ovum, whereas one primary spermatocyte gives four sperms.',
            '3 marks process; 1 mark diagram; 1 mark difference.'),
           ('C4', 'D4', 'explain', 'What is the role of LH and FSH in spermatogenesis?',
            'Under GnRH from the hypothalamus, the pituitary releases LH and FSH. LH acts on Leydig cells to secrete androgens, which stimulate spermatogenesis. FSH acts on Sertoli cells and stimulates secretion of factors that help spermiogenesis.',
            '1 mark LH; 1 mark FSH.')],
}

CH2S3 = {
    'topic': 'menstrual cycle, fertilisation and implantation',
    'terms': [('menarche', 'the first menstruation that begins at puberty'),
              ('menopause', 'the stopping of menstrual cycles around 50 years of age'),
              ('ovulation', 'the release of the secondary oocyte from the Graafian follicle'),
              ('the corpus luteum', 'the structure formed from the ruptured Graafian follicle that secretes progesterone'),
              ('the blastocyst', 'the stage of embryo with an outer trophoblast and an inner cell mass that implants in the uterus'),
              ('implantation', 'the embedding of the blastocyst in the endometrium of the uterus'),
              ('cleavage', 'the mitotic divisions of the zygote as it moves through the isthmus towards the uterus'),
              ('the morula', 'the embryo with 8–16 blastomeres')],
    'tf': (['The LH surge induces ovulation around the 14th day of a 28-day cycle.', 'The corpus luteum secretes progesterone.', 'Absence of menstruation may indicate pregnancy.',
            'The sex of the baby is decided by the father\'s sperm.', 'The trophoblast layer attaches to the endometrium during implantation.'],
           [('Ovulation occurs on the 1st day of the menstrual cycle.', 'It occurs around the 14th day of a 28-day cycle.'),
            ('The corpus luteum secretes FSH.', 'It secretes large amounts of progesterone.'),
            ('Fertilisation can occur only if the ovum and sperm meet in the uterus.', 'They must reach the ampullary region of the oviduct simultaneously.'),
            ('The inner cell mass forms the placenta.', 'The trophoblast attaches to the endometrium; the inner cell mass differentiates into the embryo.'),
            ('The sex of the child is determined by the mother.', 'The sperm carries either X or Y; the ovum always carries X.')]),
    'orders': [('sequence of events after fertilisation', ['zygote', 'cleavage', 'morula', 'blastocyst', 'implantation'], 'Cleavage in the isthmus forms the morula, which becomes a blastocyst and implants in the uterus.', '→'),
               ('sequence of phases of the menstrual cycle', ['menstrual phase', 'follicular phase', 'ovulation', 'luteal phase'], 'Menstruation lasts 3–5 days, ovulation is near day 14 and the luteal phase follows.', '→')],
    'ar': [('The corpus luteum degenerates in the absence of fertilisation.', 'Fall in progesterone causes disintegration of the endometrium.', 'b', 'Both are true; but R describes the result of degeneration, not its cause.'),
           ('The sex of the human baby is decided by the father.', 'Sperms carry either an X or a Y chromosome.', 'a', 'Ova always carry X.'),
           ('The endometrium thickens in the luteal phase.', 'Progesterone from the corpus luteum maintains the endometrium.', 'a', 'It is prepared for implantation.')],
    'fams': [F('C3', 'D3', 'mcq', cycle_phase), F('C2', 'D2', 'mcq', cycle_phase)],
    'qa': [('C4', 'D4', 'explain', 'What is the role of the LH surge in the menstrual cycle? What happens to the Graafian follicle after ovulation?',
            'A rapid rise in LH (with FSH) at mid-cycle causes rupture of the Graafian follicle and release of the ovum (ovulation). The ruptured follicle changes into the corpus luteum, which secretes progesterone.',
            '1 mark LH surge; 1 mark corpus luteum.'),
           ('C4', 'D5', 'long', 'Describe the events of the menstrual cycle with the changes in the ovary, uterus and hormone levels. What happens if fertilisation does not occur?',
            'Menstrual phase (days 1–5): breakdown of endometrium. Follicular phase: primary follicles grow into a Graafian follicle; endometrium regenerates; LH and FSH rise gradually, oestrogen secreted. Ovulation (~day 14): LH surge ruptures the Graafian follicle. Luteal phase: corpus luteum secretes progesterone that maintains the endometrium. Without fertilisation, the corpus luteum degenerates, progesterone falls and menstruation starts again.',
            '1 mark each phase; 1 mark no-fertilisation outcome.'),
           ('C4', 'D3', 'case', 'Divya\'s menstrual cycle is regular at 28 days. Her last period started on 1st March.\n(i) On approximately which date is she likely to ovulate? (1 mark)\n(ii) Which hormone surge causes ovulation? (1 mark)\n(iii) Which structure forms after ovulation, and what does it secrete? What happens to it if fertilisation does not occur? (2 marks)',
            '(i) About 14th March. (ii) LH surge (with FSH). (iii) Corpus luteum; secretes progesterone; it degenerates, causing disintegration of the endometrium and menstruation.',
            '(i) 1 (ii) 1 (iii) 2.', ('case',))],
}

CH2S4 = {
    'topic': 'pregnancy, embryonic development, parturition and lactation',
    'terms': [('the placenta', 'the structural and functional unit between the developing embryo and the maternal body'),
              ('the chorionic villi', 'the finger-like projections of the trophoblast that interdigitate with the uterine tissue'),
              ('the umbilical cord', 'the cord connecting the foetus to the placenta that transports substances to and from the embryo'),
              ('parturition', 'the process of delivery of the foetus at the end of pregnancy'),
              ('the foetal ejection reflex', 'the mild uterine contractions signalled by the fully developed foetus and placenta that trigger the release of oxytocin'),
              ('colostrum', 'the milk produced during the initial few days of lactation, containing antibodies (IgA)'),
              ('stem cells', 'the cells of the inner cell mass that can give rise to all tissues and organs')],
    'groups': [('a hormone made only during pregnancy', ['hCG', 'hPL', 'relaxin']), ('a hormone whose level rises during pregnancy', ['oestrogens', 'progestogens', 'cortisol', 'prolactin', 'thyroxine'])],
    'classify': False,
    'tf': (['The placenta acts as an endocrine tissue.', 'Human pregnancy lasts about 9 months.', 'Colostrum contains antibodies that give resistance to the new-born.',
            'The heart of the embryo forms after one month of pregnancy.', 'Oxytocin causes strong contractions of the uterine muscles during parturition.'],
           [('The placenta does not secrete any hormones.', 'It secretes hCG, hPL, oestrogens and progestogens.'),
            ('Relaxin is produced by the pituitary.', 'Relaxin is secreted by the ovary in the later phase of pregnancy.'),
            ('Parturition is induced by prolactin.', 'It is induced by a neuroendocrine mechanism involving oxytocin.'),
            ('By the end of the first trimester the foetus opens its eyelids.', 'Eyelids separate and eyelashes form by the end of about 24 weeks (second trimester).')]),
    'orders': [('sequence of development in the human foetus', ['heart forms (1 month)', 'limbs and digits (2 months)', 'major organs formed (12 weeks)', 'first movements and hair on head (5 months)', 'eyelids separate (24 weeks)', 'ready for delivery (9 months)'], 'Milestones as described in NCERT.', '→')],
    'ar': [('Colostrum is essential for the new-born.', 'It contains IgA antibodies.', 'a', 'Gives passive immunity.'),
           ('The placenta acts as an endocrine gland.', 'It secretes hCG, hPL, oestrogens and progestogens.', 'a', 'These maintain pregnancy.'),
           ('Stem cells of the inner cell mass can form all tissues.', 'The inner cell mass differentiates into ectoderm, mesoderm and endoderm.', 'a', 'They are pluripotent.')],
    'features': {'intro': 'A hormone involved in pregnancy or birth has this role:', 'q': 'Identify the hormone', 'what': 'hormone', 'long': False,
                 'items': [('oxytocin', ['released from the maternal pituitary', 'causes strong uterine contractions', 'stimulated by the foetal ejection reflex', 'helps in milk ejection']),
                           ('hCG', ['secreted by the placenta', 'maintains the corpus luteum', 'detected in pregnancy tests', 'produced only during pregnancy']),
                           ('relaxin', ['secreted by the ovary late in pregnancy', 'produced only during pregnancy', 'relaxes the pelvic ligaments', 'helps in parturition']),
                           ('prolactin', ['level rises during pregnancy', 'secreted by the anterior pituitary', 'stimulates milk production', 'acts on the mammary alveoli'])]},
    'qa': [('C4', 'D4', 'explain', 'Explain the role of the placenta as an endocrine organ and in exchange of materials.',
            'The placenta allows supply of oxygen and nutrients to the embryo and removal of CO₂ and wastes through the umbilical cord. It secretes hCG, hPL, oestrogens and progestogens, which maintain pregnancy.',
            '1 mark exchange; 1 mark hormones.'),
           ('C4', 'D5', 'long', 'Describe the process of parturition. What is the role of hormones in it? Why is breastfeeding recommended during the initial period of an infant\'s growth?',
            'At term, signals from the fully developed foetus and placenta cause mild uterine contractions (foetal ejection reflex), which trigger oxytocin release from the maternal pituitary. Oxytocin causes stronger contractions, which stimulate more oxytocin; the baby is expelled through the birth canal, followed by the placenta. Relaxin relaxes pelvic ligaments. Breast milk, especially colostrum, contains antibodies (IgA) that protect the new-born and is complete nutrition.',
            '2 marks process; 2 marks hormones; 1 mark breastfeeding.')],
}

# ---------------------------------------------------------------- ch03 reproductive health

CONTRA = [('periodic abstinence', 'natural method', 'avoiding coitus from day 10 to day 17 of the cycle, when ovulation is expected'),
          ('withdrawal (coitus interruptus)', 'natural method', 'the male withdraws the penis before ejaculation'),
          ('lactational amenorrhoea', 'natural method', 'no ovulation during intense lactation, effective up to about six months after parturition'),
          ('condoms', 'barrier method', 'a thin rubber/latex sheath that prevents sperm from entering the female tract; also protects against STIs'),
          ('diaphragms, cervical caps and vaults', 'barrier method', 'rubber barriers inserted to cover the cervix; reusable'),
          ('Cu-T and Multiload 375', 'copper releasing IUD', 'Cu ions suppress sperm motility and fertilising capacity'),
          ('LNG-20 and Progestasert', 'hormone releasing IUD', 'make the uterus unsuitable for implantation and the cervix hostile to sperm'),
          ('Lippes loop', 'non-medicated IUD', 'increases phagocytosis of sperms within the uterus'),
          ('Saheli', 'oral contraceptive', 'a once-a-week non-steroidal pill developed at CDRI, Lucknow'),
          ('vasectomy', 'surgical method (sterilisation)', 'a small part of the vas deferens is removed or tied up'),
          ('tubectomy', 'surgical method (sterilisation)', 'a small part of the fallopian tube is removed or tied up'),
          ('emergency contraceptive pills', 'oral contraceptive', 'progestogens or progestogen–oestrogen combination taken within 72 hours of coitus')]
contra_type = table_mcq([(a, '', b, c) for a, b, c in CONTRA], 'To which category of contraceptive methods does {a} belong?', why_fmt='{a} – category: {ans}; {why}.',
                        pool=['natural method', 'barrier method', 'copper releasing IUD', 'hormone releasing IUD', 'non-medicated IUD', 'oral contraceptive', 'surgical method (sterilisation)'])

STI = [('gonorrhoea', 'bacterium (Neisseria gonorrhoeae)'), ('syphilis', 'bacterium (Treponema pallidum)'), ('genital herpes', 'virus (herpes simplex virus)'),
       ('chlamydiasis', 'bacterium (Chlamydia trachomatis)'), ('genital warts', 'virus (human papilloma virus)'), ('trichomoniasis', 'protozoan (Trichomonas vaginalis)'),
       ('hepatitis B', 'virus (hepatitis B virus)'), ('HIV infection/AIDS', 'virus (human immunodeficiency virus)')]
sti_cause = table_mcq([(a, '', b, '') for a, b in STI], 'Which type of pathogen causes {a}?', why_fmt='{a} is caused by a {ans}.')

ART = [('IVF–ET (test tube baby)', 'fertilisation outside the body in conditions similar to the body, followed by embryo transfer'),
       ('ZIFT', 'transfer of the zygote or early embryo (up to 8 blastomeres) into the fallopian tube'),
       ('IUT', 'transfer of an embryo with more than 8 blastomeres into the uterus'),
       ('GIFT', 'transfer of an ovum collected from a donor into the fallopian tube of a female who cannot produce ova but can provide conditions for fertilisation'),
       ('ICSI', 'injection of a sperm directly into the ovum in the laboratory'),
       ('artificial insemination (AI)', 'semen from the husband or a donor is introduced into the vagina or uterus (IUI)'),
       ('IUI', 'semen is artificially introduced into the uterus of the female')]
art_pick = table_mcq([(b, '', a, '') for a, b in ART], 'Which assisted reproductive technology involves {a}?', why_fmt='{Ans}: {a}.')

CH3S1 = {
    'topic': 'reproductive health, population and birth control',
    'terms': [('reproductive health', 'total well-being in all aspects of reproduction – physical, emotional, behavioural and social'),
              ('RCH programmes', 'Reproductive and Child Health Care programmes that create awareness and provide facilities for reproduction-related areas'),
              ('an IUD', 'an intra-uterine device inserted by doctors or nurses in the uterus through the vagina to prevent conception'),
              ('sterilisation', 'a terminal surgical method of contraception in the male (vasectomy) or female (tubectomy)'),
              ('lactational amenorrhoea', 'the absence of menstruation during the period of intense lactation following parturition'),
              ('amniocentesis', 'a foetal sex determination test based on the chromosomal pattern in the amniotic fluid, now banned for sex determination')],
    'tf': (['India was among the first countries to initiate action plans for reproductive health at the national level (family planning, 1951).', 'An ideal contraceptive should be user-friendly, easily available, effective and reversible with no side effects.',
            'Saheli was developed at CDRI, Lucknow.', 'Condoms also protect against STIs and AIDS.', 'Statutory ban on amniocentesis for sex determination helps check female foeticide.'],
           [('Copper releasing IUDs make the uterus unsuitable for implantation by releasing hormones.', 'Copper ions suppress sperm motility and fertilising capacity; hormone-releasing IUDs act on the uterus.'),
            ('Lactational amenorrhoea is effective up to two years after parturition.', 'It is effective only up to a maximum of six months after parturition.'),
            ('Vasectomy is easily reversible.', 'Reversibility of surgical methods is very poor.'),
            ('Saheli is a daily steroidal pill.', 'Saheli is a once-a-week non-steroidal pill.')]),
    'ar': [('Lactational amenorrhoea is a natural contraceptive method.', 'Ovulation does not occur during the period of intense lactation.', 'a', 'Effective up to six months.'),
           ('Condoms are a popular contraceptive.', 'They also give protection against STIs and AIDS.', 'b', 'Both true; protection from STIs is an added advantage rather than the explanation of contraception.'),
           ('Surgical methods of contraception are called terminal methods.', 'They block gamete transport and are poorly reversible.', 'a', 'Usually permanent.')],
    'features': {'intro': 'A contraceptive method works like this:', 'q': 'Identify the method', 'what': 'method',
                 'items': [('copper releasing IUD (Cu-T)', ['inserted into the uterus', 'releases Cu ions', 'suppresses sperm motility', 'can be used for spacing children']),
                           ('oral pills', ['contain progestogens or progestogen–oestrogen combinations', 'inhibit ovulation and implantation', 'taken daily for 21 days', 'alter the quality of cervical mucus']),
                           ('vasectomy', ['surgical method in males', 'small part of vas deferens removed or tied', 'blocks sperm transport', 'very poorly reversible']),
                           ('condoms', ['barrier made of thin rubber or latex', 'prevent semen entering the female tract', 'disposable', 'protect against STIs'])]},
    'fams': [F('C2', 'D2', 'mcq', contra_type), F('C3', 'D3', 'mcq', contra_type)],
    'qa': [('C4', 'D4', 'explain', 'Suggest the aspects of reproductive health that need to be given special attention in the present scenario.',
            'Awareness about reproduction-related aspects and STIs; sex education in schools; access to contraception and family planning; safe and hygienic pregnancy and delivery, post-natal care of mother and child; check on female foeticide and early marriage.',
            '½ mark each for four aspects.'),
           ('C4', 'D3', 'case', 'At a health camp in Jaipur, a nurse explains contraceptive options to a newly married couple who want to delay their first child by two years.\n(i) Suggest one suitable reversible method for the woman and one for the man. (2 marks)\n(ii) How does a Cu-T prevent pregnancy? (1 mark)\n(iii) Why are surgical methods not advised for them? (1 mark)',
            '(i) Woman: IUD (Cu-T) or oral pills; man: condoms. (ii) Released Cu ions suppress sperm motility and fertilising capacity. (iii) Surgical methods are terminal and very poorly reversible; they want children later.',
            '(i) 2 (ii) 1 (iii) 1.', ('case',)),
           ('C4', 'D5', 'long', 'What is an ideal contraceptive? Describe natural, barrier, IUD, oral and surgical methods of contraception with one example each.',
            'Ideal: user-friendly, available, effective, reversible, no or least side effects, no interference with sexual drive. Natural: periodic abstinence (days 10–17). Barrier: condoms/diaphragms. IUDs: Cu-T (copper), LNG-20 (hormone), Lippes loop (non-medicated). Oral: pills with progestogens/oestrogen, Saheli (weekly, non-steroidal). Surgical: vasectomy, tubectomy.',
            '1 mark ideal; 4 marks methods with examples.')],
}

CH3S2 = {
    'topic': 'MTP and sexually transmitted infections',
    'terms': [('MTP', 'medical termination of pregnancy, the intentional or voluntary termination of pregnancy before full term'),
              ('STIs', 'infections or diseases transmitted through sexual intercourse, also called venereal diseases or RTIs'),
              ('PID', 'pelvic inflammatory disease, a complication of untreated STIs'),
              ('ectopic pregnancy', 'implantation and development of the embryo at a site other than the uterus, a possible complication of STIs')],
    'groups': [('an STI caused by a bacterium', ['gonorrhoea', 'syphilis', 'chlamydiasis']), ('an STI caused by a virus', ['genital herpes', 'genital warts', 'hepatitis B', 'HIV infection']),
               ('an STI caused by a protozoan', ['trichomoniasis'])],
    'tf': (['MTPs are considered relatively safe during the first trimester (up to 12 weeks).', 'Hepatitis B, genital herpes and HIV infections are not completely curable.', 'Early detection and treatment of STIs prevents complications such as PID and infertility.',
            'The MTP (Amendment) Act, 2017 was enacted by the Government of India to reduce illegal abortions.', 'STIs can be transmitted by sharing injection needles and from mother to foetus.'],
           [('MTP is safe at any stage of pregnancy.', 'It is relatively safe only in the first trimester.'),
            ('All STIs are completely curable.', 'Hepatitis B, genital herpes and HIV infections are not completely curable.'),
            ('STIs are transmitted only by sexual contact.', 'Some (HIV, hepatitis B) also spread by sharing needles, transfusion and from mother to foetus.'),
            ('Syphilis is caused by a virus.', 'It is caused by the bacterium Treponema pallidum.')]),
    'ar': [('Early detection of STIs is important.', 'STIs can lead to PID, abortions, still births, ectopic pregnancies and infertility if untreated.', 'a', 'Timely treatment prevents complications.'),
           ('Hepatitis B is not completely curable.', 'Hepatitis B can also be transmitted by sharing injection needles.', 'b', 'Both are true, but the mode of transmission does not explain why it is not curable.'),
           ('MTP should be done only by qualified medical professionals.', 'Illegal MTPs by unqualified quacks are unsafe and can be fatal.', 'a', 'Safety of the mother.')],
    'fams': [F('C2', 'D2', 'mcq', sti_cause)],
    'qa': [('C3', 'D2', 'explain', 'Give two reasons why MTP is permitted under certain conditions.',
            'To get rid of unwanted pregnancies (failure of contraception, rape) and when continuation of pregnancy could be harmful or fatal to the mother or foetus (e.g. foetal abnormality).',
            '1 mark each.'),
           ('C4', 'D4', 'explain', 'Suggest simple principles to prevent STIs.',
            'Avoid sex with unknown partners or multiple partners; always use condoms during coitus; in case of doubt consult a qualified doctor for early detection and complete treatment.',
            '½ mark each, up to 2.'),
           ('C4', 'D3', 'case', 'At a youth awareness drive in Kolkata, a doctor says that adolescents in the 15–24 age group are most at risk of STIs.\n(i) Name two STIs that are not completely curable. (1 mark)\n(ii) Name two complications of untreated STIs in women. (1 mark)\n(iii) Give two ways STIs can spread other than sexual contact, and two preventive steps. (2 marks)',
            '(i) Genital herpes, hepatitis B, HIV (any two). (ii) PID, abortions, still births, ectopic pregnancy, infertility (any two). (iii) Sharing injection needles, transfusion of infected blood, mother to foetus; avoid unknown/multiple partners, always use condoms.',
            '(i) 1 (ii) 1 (iii) 2.', ('case',))],
}

CH3S3 = {
    'topic': 'infertility and assisted reproductive technologies',
    'terms': [('infertility', 'the inability to produce children inspite of unprotected sexual cohabitation'),
              ('IVF', 'in vitro fertilisation, fertilisation outside the body in almost similar conditions as that in the body'),
              ('ZIFT', 'zygote intra-fallopian transfer of a zygote or early embryo up to 8 blastomeres'),
              ('ICSI', 'intra-cytoplasmic sperm injection, in which a sperm is directly injected into the ovum'),
              ('GIFT', 'gamete intra-fallopian transfer of an ovum from a donor into the fallopian tube'),
              ('artificial insemination', 'the artificial introduction of semen from the husband or a donor into the vagina or uterus')],
    'tf': (['ZIFT transfers embryos with up to 8 blastomeres into the fallopian tube.', 'IUT transfers embryos with more than 8 blastomeres into the uterus.', 'Artificial insemination is used when the male cannot inseminate or has a low sperm count.',
            'ICSI is a specialised procedure to form an embryo in the laboratory.', 'Infertility may be due to problems in the male or the female partner.'],
           [('ZIFT transfers embryos with more than 8 blastomeres into the uterus.', 'That is IUT; ZIFT transfers up to 8 blastomeres into the fallopian tube.'),
            ('In GIFT, a zygote is transferred into the fallopian tube.', 'In GIFT, an ovum from a donor is transferred into the fallopian tube.'),
            ('Infertility is always due to the female partner.', 'It may be due to defects in either partner.'),
            ('In IUI the semen is introduced into the fallopian tube.', 'In IUI the semen is introduced into the uterus.')]),
    'ar': [('IVF followed by embryo transfer is popularly called the test tube baby programme.', 'The ova and sperms are made to fuse in the laboratory.', 'a', 'Fertilisation outside the body.'),
           ('GIFT is suitable for women who cannot produce ova.', 'The ovum from a donor is transferred into her fallopian tube.', 'a', 'She can provide conditions for fertilisation.'),
           ('ART procedures are cheap and widely available in India.', 'ART requires specialised professionals and expensive instrumentation.', 'd', 'They are expensive and available in few centres; the reason is true.')],
    'fams': [F('C3', 'D3', 'mcq', art_pick), F('C2', 'D2', 'mcq', art_pick)],
    'qa': [('C4', 'D4', 'explain', 'Distinguish between ZIFT and IUT.',
            'ZIFT: zygote or early embryo with up to 8 blastomeres transferred into the fallopian tube. IUT: embryo with more than 8 blastomeres transferred into the uterus.',
            '1 mark each.'),
           ('C4', 'D3', 'case', 'A couple in Chennai has been unable to have a child for four years. Tests show the husband has a very low sperm count, while the wife is healthy.\n(i) Suggest two techniques that could help them. (2 marks)\n(ii) Explain how one of them is carried out. (1 mark)\n(iii) Suggest one alternative the couple could consider apart from ART. (1 mark)',
            '(i) Artificial insemination (IUI) and ICSI. (ii) In IUI, semen collected from the husband is introduced into the uterus; in ICSI a sperm is injected into the ovum in the laboratory and the embryo is transferred. (iii) Legal adoption of an orphaned or destitute child.',
            '(i) 2 (ii) 1 (iii) 1.', ('case',)),
           ('C4', 'D5', 'long', 'What is infertility? Describe four assisted reproductive technologies and the situations in which each is used.',
            'Inability to conceive inspite of unprotected cohabitation. IVF–ET: fertilisation in the laboratory and embryo transfer by ZIFT (≤ 8 blastomeres into fallopian tube) or IUT (> 8 into uterus). GIFT: donor ovum into fallopian tube for women who cannot produce ova but can sustain fertilisation. ICSI: sperm injected into ovum. AI/IUI: semen into vagina or uterus when male cannot inseminate or has low sperm count.',
            '1 mark definition; 4 marks techniques.')],
}

# ---------------------------------------------------------------- ch04 principles of inheritance and variation

TRAITS = [('pea plants', 'tall', 'dwarf', 'T', 't', 'height'), ('pea plants', 'round seeds', 'wrinkled seeds', 'R', 'r', 'seed shape'),
          ('pea plants', 'yellow seeds', 'green seeds', 'Y', 'y', 'seed colour'), ('pea plants', 'violet flowers', 'white flowers', 'V', 'v', 'flower colour'),
          ('pea plants', 'green pods', 'yellow pods', 'G', 'g', 'pod colour'), ('pea plants', 'inflated pods', 'constricted pods', 'I', 'i', 'pod shape'),
          ('pea plants', 'axial flowers', 'terminal flowers', 'A', 'a', 'flower position')]

CROSSES = {('AA', 'AA'): 'all dominant', ('AA', 'Aa'): 'all dominant', ('AA', 'aa'): 'all dominant', ('Aa', 'Aa'): '3 dominant : 1 recessive',
           ('Aa', 'aa'): '1 dominant : 1 recessive', ('aa', 'aa'): 'all recessive'}


def _g(gt, T, t):
    return gt.replace('A', T).replace('a', t)


def mono(r):
    org, dom, rec, T, t, _ = r.choice(TRAITS)
    p1, p2 = r.choice(list(CROSSES))
    res = CROSSES[(p1, p2)]
    ph = res.replace('dominant', dom).replace('recessive', rec)
    g1, g2 = _g(p1, T, t), _g(p2, T, t)
    opts = [x.replace('dominant', dom).replace('recessive', rec) for x in ('all dominant', '3 dominant : 1 recessive', '1 dominant : 1 recessive', 'all recessive', '1 dominant : 2 intermediate : 1 recessive')]
    geno = {('AA', 'AA'): f'all {T}{T}', ('AA', 'Aa'): f'1 {T}{T} : 1 {T}{t}', ('AA', 'aa'): f'all {T}{t}', ('Aa', 'Aa'): f'1 {T}{T} : 2 {T}{t} : 1 {t}{t}',
            ('Aa', 'aa'): f'1 {T}{t} : 1 {t}{t}', ('aa', 'aa'): f'all {t}{t}'}[(p1, p2)]
    return mcq(f'In {org}, {dom} ({T}) is dominant over {rec} ({t}). What is the phenotypic ratio of the progeny of the cross {g1} × {g2}?', ph, [o for o in opts if o != ph][:3] if ph in opts else r.sample(opts, 3),
               f'Gametes combine to give {geno}, i.e. {ph}.', r)


def dihybrid_prob(r):
    (o1, d1, r1, T1, t1, _), (o2, d2, r2, T2, t2, _) = r.sample(TRAITS, 2)
    target = r.choice(['dd', 'dr', 'rd', 'rr', 'homo_dom', 'het_both'])
    p = {'dd': Fraction(9, 16), 'dr': Fraction(3, 16), 'rd': Fraction(3, 16), 'rr': Fraction(1, 16), 'homo_dom': Fraction(1, 16), 'het_both': Fraction(4, 16)}[target]
    desc = {'dd': f'{d1} and {d2}', 'dr': f'{d1} and {r2}', 'rd': f'{r1} and {d2}', 'rr': f'{r1} and {r2}',
            'homo_dom': f'genotype {T1}{T1}{T2}{T2}', 'het_both': f'genotype {T1}{t1}{T2}{t2}'}[target]
    n = r.choice([160, 320, 480, 640, 800, 1600])
    k = p * n
    return {'stem': f'In pea, {d1} ({T1}) is dominant over {r1} ({t1}) and {d2} ({T2}) is dominant over {r2} ({t2}); the genes assort independently. A plant {T1}{t1}{T2}{t2} is selfed and {n} seeds are raised. What fraction of the progeny, and how many plants, are expected to show {desc}?',
            'answer': f'{frac(p)}; {num(float(k))} plants',
            'key': f'Each gene segregates 3 : 1 (or 1 : 2 : 1 for genotype) independently (1); probability = {frac(p)} (1); {frac(p)} × {n} = {num(float(k))} plants (1).',
            'distractors': [f'{frac(Fraction(3, 16) if p != Fraction(3, 16) else Fraction(9, 16))}; {num(float((Fraction(3, 16) if p != Fraction(3, 16) else Fraction(9, 16)) * n))} plants',
                            f'{frac(Fraction(1, 4))}; {n // 4} plants' if p != Fraction(1, 4) else f'{frac(Fraction(1, 16))}; {n // 16} plants', f'{frac(Fraction(1, 2))}; {n // 2} plants']}


def test_cross(r):
    org, dom, rec, T, t, _ = r.choice(TRAITS)
    het = r.random() < 0.5
    n = r.choice([40, 60, 80, 100, 120, 200])
    who = name(r)
    if het:
        obs = f'{n // 2} {dom} and {n // 2} {rec}'
        ans = f'{T}{t} (heterozygous)'
        why = f'a 1 : 1 ratio is obtained only when the {dom} parent is {T}{t}'
    else:
        obs = f'all {n} {dom}'
        ans = f'{T}{T} (homozygous)'
        why = f'no {rec} progeny appear, so the {dom} parent gives only {T} gametes'
    return {'stem': f'{who} crosses a {dom} {org[:-1]} of unknown genotype with a {rec} plant ({t}{t}) and gets {obs} plants. What is this cross called, and what is the genotype of the {dom} parent?',
            'answer': f'Test cross; {ans}', 'key': f'Crossing with the recessive parent is a test cross (1); {why} ⇒ {ans} (1).',
            'distractors': [f'Test cross; {T}{t} (heterozygous)' if not het else f'Test cross; {T}{T} (homozygous)', f'Back cross with dominant parent; {ans}', f'Dihybrid cross; {t}{t} (homozygous recessive)']}


BLOOD = {'A': ['IᴬIᴬ', 'IᴬI°'], 'B': ['IᴮIᴮ', 'IᴮI°'], 'AB': ['IᴬIᴮ'], 'O': ['I°I°']}


def _bg(gt):
    s = set([gt[:2], gt[2:]])
    if s == {'Iᴬ', 'Iᴮ'}:
        return 'AB'
    if 'Iᴬ' in s:
        return 'A'
    if 'Iᴮ' in s:
        return 'B'
    return 'O'


def _kids(g1, g2):
    kids = {}
    for a in (g1[:2], g1[2:]):
        for b in (g2[:2], g2[2:]):
            ph = _bg(a + b)
            kids[ph] = kids.get(ph, 0) + 1
    return kids


def _bg_desc(kids):
    tot = sum(kids.values())
    return ', '.join(f'{k} ({frac(Fraction(kids[k], tot))})' if kids[k] != tot else f'{k} only' for k in ['A', 'B', 'AB', 'O'] if k in kids)


def blood_cross(r):
    g1 = r.choice(['IᴬIᴬ', 'IᴬI°', 'IᴮIᴮ', 'IᴮI°', 'IᴬIᴮ', 'I°I°'])
    g2 = r.choice(['IᴬI°', 'IᴮI°', 'IᴬIᴮ', 'I°I°', 'IᴬIᴬ'])
    kids = _kids(g1, g2)
    good = _bg_desc(kids)
    alt = []
    for x1 in ['IᴬIᴬ', 'IᴬI°', 'IᴮIᴮ', 'IᴮI°', 'IᴬIᴮ', 'I°I°']:
        for x2 in ['IᴬI°', 'IᴮI°', 'IᴬIᴮ', 'I°I°', 'IᴬIᴬ']:
            k2 = _kids(x1, x2)
            d = _bg_desc(k2)
            if d != good:
                alt.append(d)
    alt = list(dict.fromkeys(alt))
    alt.sort(key=lambda d: (len(set(d.split(', ')) ^ set(good.split(', '))), d))
    alt = r.sample(alt[:6], 3)
    return mcq(f'ABO blood groups are controlled by gene I with alleles Iᴬ, Iᴮ (co-dominant) and I° (recessive). What blood groups, and in what proportions, are expected among children of parents {g1} × {g2}?', good, alt[:3],
               f'Gametes {g1[:2]}, {g1[2:]} × {g2[:2]}, {g2[2:]} give {good}.', r)


def recomb(r):
    a, b = r.sample(['white eye (w)', 'yellow body (y)', 'miniature wing (m)', 'vermilion eye (v)', 'cut wing (ct)'], 2)
    n = r.choice([200, 400, 500, 800, 1000])
    rf = r.choice([1.3, 5, 10, 12, 20, 25, 37.2])
    rec = round(n * rf / 100)
    rf2 = rec / n * 100
    return {'stem': f'In a test cross of Drosophila involving the linked genes {a} and {b}, {rec} of {n} progeny were recombinants. Calculate the recombination frequency and the map distance between the genes.',
            'answer': f'{num(rf2, 2)}%; {num(rf2, 2)} map units (cM)',
            'key': f'Recombination frequency = recombinants/total × 100 = {rec}/{n} × 100 = {num(rf2, 2)}% (1); 1% recombination = 1 map unit, so distance = {num(rf2, 2)} cM (1).',
            'distractors': [f'{num(100 - rf2, 2)}%; {num(100 - rf2, 2)} map units', f'{num(rf2 / 2, 2)}%; {num(rf2 / 2, 2)} map units', f'{num(rf2, 2)}%; {num(rf2 * 2, 2)} map units']}


def sexlinked(r):
    dis = r.choice(['colour blindness', 'haemophilia'])
    case = r.choice(['carrier_normal', 'normal_affected', 'carrier_affected', 'affected_normal'])
    who = name(r)
    if case == 'carrier_normal':
        mom, dad = 'carrier (XᴴXʰ)', 'normal (XᴴY)'
        ans = 'sons: ½ affected; daughters: none affected, ½ carriers'
    elif case == 'normal_affected':
        mom, dad = 'normal (XᴴXᴴ)', f'affected (XʰY)'
        ans = 'sons: none affected; daughters: all carriers'
    elif case == 'carrier_affected':
        mom, dad = 'carrier (XᴴXʰ)', 'affected (XʰY)'
        ans = 'sons: ½ affected; daughters: ½ affected, ½ carriers'
    else:
        mom, dad = 'affected (XʰXʰ)', 'normal (XᴴY)'
        ans = 'sons: all affected; daughters: all carriers'
    opts = ['sons: ½ affected; daughters: none affected, ½ carriers', 'sons: none affected; daughters: all carriers',
            'sons: ½ affected; daughters: ½ affected, ½ carriers', 'sons: all affected; daughters: all carriers', 'sons: all normal; daughters: all affected']
    return mcq(f'{dis.capitalize()} is an X-linked recessive disorder. {who}\'s mother is {mom} and father is {dad} for this trait. What is expected among their children?', ans,
               r.sample([o for o in opts if o != ans], 3), f'Sons get their X from the mother and Y from the father; daughters get one X from each parent ⇒ {ans}.', r)


DISORDERS = [('Down\'s syndrome', 'trisomy of chromosome 21', 'chromosomal'), ('Klinefelter\'s syndrome', '44 + XXY (47 chromosomes)', 'chromosomal'),
             ('Turner\'s syndrome', '44 + XO (45 chromosomes)', 'chromosomal'), ('haemophilia', 'X-linked recessive gene; blood does not clot', 'Mendelian'),
             ('sickle-cell anaemia', 'autosomal recessive; Glu → Val at the 6th position of the β-globin chain', 'Mendelian'),
             ('phenylketonuria', 'autosomal recessive; lack of the enzyme that converts phenylalanine to tyrosine', 'Mendelian'),
             ('colour blindness', 'X-linked recessive; defect in red or green cone cells', 'Mendelian'),
             ('thalassaemia', 'autosomal recessive; reduced synthesis of α or β globin chains', 'Mendelian')]
disorder_cause = table_mcq([(a, '', b, c) for a, b, c in DISORDERS], 'What is the cause of {a}?', why_fmt='{a}: {ans}.')

SEXDET = [('humans', 'XX–XY (male heterogamety)', 'males produce X and Y sperms'), ('Drosophila', 'XX–XY (male heterogamety)', 'males are XY'),
          ('grasshopper', 'XX–XO (male heterogamety)', 'males have only one X'), ('birds', 'ZW–ZZ (female heterogamety)', 'females are ZW'),
          ('honey bee', 'haplodiploidy', 'males develop from unfertilised eggs (haploid) and females from fertilised eggs (diploid)')]
sexdet = table_mcq([(a, '', b, c) for a, b, c in SEXDET], 'What type of sex determination is found in {a}?', why_fmt='{a}: {ans}; {why}.',
                   pool=['XX–XY (male heterogamety)', 'XX–XO (male heterogamety)', 'ZW–ZZ (female heterogamety)', 'haplodiploidy'])

CH4S1 = {
    'topic': "Mendel's laws and crosses",
    'terms': [('an allele', 'one of the alternative forms of a gene that code for a pair of contrasting traits'),
              ('a homozygous individual', 'an individual with identical alleles for a trait, e.g. TT or tt'),
              ('a heterozygous individual', 'an individual with two different alleles for a trait, e.g. Tt'),
              ('a test cross', 'the cross of an organism showing the dominant phenotype with the recessive parent to find its genotype'),
              ('the law of dominance', 'the law that in a dissimilar pair of factors one member dominates the other'),
              ('the law of segregation', 'the law that alleles do not blend and separate during gamete formation so that each gamete gets one'),
              ('the law of independent assortment', 'the law that in inheritance of two pairs of traits the segregation of one pair is independent of the other'),
              ('a Punnett square', 'a graphical representation used to calculate the probability of all possible genotypes of offspring')],
    'tf': (['Mendel worked on garden pea for seven years (1856–1863).', 'The monohybrid F₂ phenotypic ratio is 3 : 1 and genotypic ratio is 1 : 2 : 1.', 'The dihybrid F₂ phenotypic ratio is 9 : 3 : 3 : 1.',
            'A test cross with a heterozygote gives a 1 : 1 ratio.', 'Mendel selected 7 pairs of contrasting traits in pea.'],
           [('The monohybrid F₂ genotypic ratio is 3 : 1.', 'It is 1 : 2 : 1; the phenotypic ratio is 3 : 1.'),
            ('In a test cross the unknown plant is crossed with the dominant parent.', 'It is crossed with the recessive parent.'),
            ('The law of independent assortment is based on the monohybrid cross.', 'It is based on the dihybrid cross.'),
            ('Mendel studied 14 pairs of contrasting traits in pea.', 'He studied 7 pairs (14 true-breeding varieties).')]),
    'ar': [('Mendel chose the garden pea for his experiments.', 'Pea has many clear contrasting traits and is easily self- and cross-pollinated.', 'a', 'Ideal material.'),
           ('A cross between Tt and tt gives tall and dwarf in a 1 : 1 ratio.', 'The heterozygote produces T and t gametes in equal numbers.', 'a', 'Test cross ratio.'),
           ('The recessive trait reappears in the F₂ generation.', 'Alleles do not blend in the F₁ hybrid.', 'a', 'Law of segregation.')],
    'fams': [F('C3', 'D3', 'mcq', mono), F('C4', 'D4', 'multi_step', dihybrid_prob), F('C3', 'D3', 'explain', test_cross), F('C2', 'D2', 'mcq', mono)],
    'qa': [('C4', 'D5', 'long', 'Explain the law of independent assortment with the help of a dihybrid cross between a pea plant with round yellow seeds (RRYY) and one with wrinkled green seeds (rryy). Give the F₂ phenotypic ratio.',
            'P: RRYY × rryy → F₁ RrYy (round yellow). F₁ forms four types of gametes RY, Ry, rY, ry in equal proportion because the two gene pairs segregate independently. Selfing gives a 16-box Punnett square: 9 round yellow : 3 round green : 3 wrinkled yellow : 1 wrinkled green.',
            '1 mark cross; 1 mark gametes; 2 marks Punnett square; 1 mark ratio and statement.'),
           ('C4', 'D3', 'case', 'Arnav, a student in Bhopal, crosses a pure tall pea plant with a pure dwarf one. All F₁ plants are tall. He selfs the F₁ and raises 800 F₂ plants.\n(i) How many F₂ plants are expected to be dwarf? (1 mark)\n(ii) Which law explains the reappearance of dwarf plants? (1 mark)\n(iii) How would he find out whether a tall F₂ plant is TT or Tt? (2 marks)',
            '(i) 200 (¼ of 800). (ii) Law of segregation. (iii) Test cross with a dwarf (tt) plant: all tall progeny ⇒ TT; tall and dwarf in 1 : 1 ⇒ Tt.',
            '(i) 1 (ii) 1 (iii) 2.', ('case',))],
}

CH4S2 = {
    'topic': 'deviations from Mendelism',
    'terms': [('incomplete dominance', 'inheritance in which the F₁ has a phenotype intermediate between the two parents'),
              ('co-dominance', 'inheritance in which both alleles express themselves fully in the F₁, as in AB blood group'),
              ('multiple alleles', 'more than two alleles of a gene in a population, as in the ABO blood group gene'),
              ('pleiotropy', 'the phenomenon in which a single gene affects multiple phenotypic traits'),
              ('polygenic inheritance', 'inheritance in which a trait is controlled by three or more genes, each with an additive effect, as in human skin colour')],
    'groups': [('an example of incomplete dominance', ['flower colour in snapdragon (dog flower)', 'starch grain size in pea']), ('an example of co-dominance', ['AB blood group in humans']),
               ('an example of pleiotropy', ['phenylketonuria in humans', 'starch synthesis and seed shape in pea']), ('an example of polygenic inheritance', ['human skin colour', 'human height'])],
    'classify': False,
    'tf': (['In snapdragon, a cross between red (RR) and white (rr) gives pink (Rr) F₁.', 'In incomplete dominance the F₂ phenotypic ratio is 1 : 2 : 1.', 'ABO blood group alleles Iᴬ and Iᴮ are co-dominant.',
            'Six genotypes and four phenotypes are possible for the ABO blood group.', 'Human skin colour is an example of polygenic inheritance.'],
           [('In incomplete dominance the F₂ phenotypic ratio is 3 : 1.', 'Phenotypic and genotypic ratios are both 1 : 2 : 1.'),
            ('A person with blood group AB has the genotype IᴬI°.', 'AB blood group has the genotype IᴬIᴮ.'),
            ('There are four genotypes for the ABO blood group.', 'There are six genotypes and four phenotypes.'),
            ('Pleiotropy means a single trait is controlled by many genes.', 'That is polygenic inheritance; pleiotropy is one gene affecting many traits.')]),
    'ar': [('A person with genotype IᴬIᴮ has blood group AB.', 'Iᴬ and Iᴮ are co-dominant.', 'a', 'Both sugars are expressed.'),
           ('In snapdragon the F₁ of a red × white cross is pink.', 'The R allele is incompletely dominant over r.', 'a', 'Intermediate phenotype.'),
           ('Phenylketonuria is an example of pleiotropy.', 'A single gene mutation causes mental retardation and reduced hair and skin pigmentation.', 'a', 'One gene, many effects.')],
    'fams': [F('C3', 'D3', 'mcq', blood_cross), F('C4', 'D4', 'mcq', blood_cross)],
    'qa': [('C4', 'D4', 'explain', 'A child has blood group O. If the father has blood group A and the mother blood group B, work out the genotypes of the parents and the possible genotypes of the other offspring.',
            'Father IᴬI°, mother IᴮI°. Offspring: IᴬIᴮ (AB), IᴬI° (A), IᴮI° (B), I°I° (O), each ¼.',
            '1 mark parents; 1 mark offspring.'),
           ('C4', 'D3', 'case', 'Kiran crosses a red-flowered snapdragon with a white-flowered one. All F₁ plants have pink flowers. She selfs the F₁.\n(i) Name the type of inheritance. (1 mark)\n(ii) Give the F₂ phenotypic and genotypic ratios. (2 marks)\n(iii) Why does this not disprove Mendel\'s law of segregation? (1 mark)',
            '(i) Incomplete dominance. (ii) Phenotype 1 red : 2 pink : 1 white; genotype 1 RR : 2 Rr : 1 rr. (iii) The parental red and white phenotypes reappear in F₂, showing that alleles did not blend but segregated.',
            '(i) 1 (ii) 2 (iii) 1.', ('case',)),
           ('C4', 'D5', 'long', 'Explain co-dominance and multiple allelism with the example of the human ABO blood group. List the possible genotypes and phenotypes.',
            'Gene I has three alleles: Iᴬ, Iᴮ (produce sugar polymers A and B on RBCs) and I° (no sugar). Iᴬ and Iᴮ are dominant over I° but co-dominant with each other. Genotypes: IᴬIᴬ, IᴬI° (A); IᴮIᴮ, IᴮI° (B); IᴬIᴮ (AB); I°I° (O). Six genotypes, four phenotypes. More than two alleles for one gene in a population = multiple alleles.',
            '2 marks explanation; 2 marks genotypes/phenotypes; 1 mark multiple alleles.')],
}

CH4S3 = {
    'topic': 'chromosomal theory, linkage and sex determination',
    'terms': [('linkage', 'the physical association of genes on a chromosome'),
              ('recombination', 'the generation of non-parental gene combinations'),
              ('the chromosomal theory of inheritance', 'the theory of Sutton and Boveri that chromosomes are the carriers of genes and their behaviour explains Mendel\'s laws'),
              ('the X body', 'the structure seen by Henking in some insect sperms, later named the X chromosome'),
              ('male heterogamety', 'the condition in which males produce two kinds of gametes, as in XX–XY and XX–XO systems'),
              ('female heterogamety', 'the condition in which females produce two kinds of gametes, as in the ZW–ZZ system of birds')],
    'tf': (['Morgan worked with Drosophila melanogaster.', 'Tightly linked genes show very low recombination.', 'Alfred Sturtevant used recombination frequency to map genes on chromosomes.',
            'In birds the female is heterogametic (ZW).', 'In grasshoppers the male has only one X chromosome.'],
           [('Tightly linked genes show high recombination.', 'Tightly linked genes show very low recombination; loosely linked genes show higher recombination.'),
            ('Mendel discovered linkage in pea.', 'Linkage was described by T.H. Morgan in Drosophila.'),
            ('In birds the male is heterogametic.', 'In birds females are ZW (heterogametic) and males ZZ.'),
            ('In humans the mother decides the sex of the child.', 'The father\'s sperm carries X or Y and decides the sex.')]),
    'ar': [('Drosophila is a good material for genetic studies.', 'It completes its life cycle in about two weeks and a single mating gives a large number of progeny.', 'a', 'Also easy to grow and has clear hereditary variations.'),
           ('The sex of a child is determined by the father.', 'The father produces two types of sperm, X and Y.', 'a', 'Male heterogamety.'),
           ('Genes that are close together on a chromosome show low recombination.', 'Crossing over is less likely between genes that are close together.', 'a', 'Recombination frequency reflects distance.')],
    'fams': [F('C4', 'D4', 'numerical', recomb, marks=2), F('C2', 'D2', 'mcq', sexdet), F('C3', 'D3', 'mcq', sexdet)],
    'qa': [('C4', 'D4', 'explain', 'In Morgan\'s dihybrid crosses in Drosophila, why were the F₂ ratios very different from 9 : 3 : 3 : 1?',
            'The two genes were on the X chromosome (linked), so parental combinations were much more frequent than recombinants; the proportion of recombinants depended on the distance between the genes.',
            '1 mark linkage; 1 mark recombination/distance.'),
           ('C4', 'D5', 'long', 'Describe the different mechanisms of sex determination with examples: XX–XY, XX–XO, ZW–ZZ and haplodiploidy.',
            'XX–XY: humans, Drosophila; male XY produces X and Y sperms (male heterogamety). XX–XO: grasshopper; male has one X, produces sperm with and without X. ZW–ZZ: birds; female ZW is heterogametic. Haplodiploidy: honey bee; fertilised eggs (2n = 32) become females, unfertilised (n = 16) become males by parthenogenesis.',
            '1 mark each system; 1 mark heterogamety concept.'),
           ('C4', 'D3', 'case', 'A poultry farmer near Namakkal wants to know which parent decides the sex of chicks.\n(i) What are the sex chromosomes of a hen and a cock? (1 mark)\n(ii) Which parent decides the sex of the chick? (1 mark)\n(iii) How is this different from humans? Explain with gametes. (2 marks)',
            '(i) Hen ZW, cock ZZ. (ii) The hen, as she produces Z and W eggs. (iii) In humans the male is heterogametic (XY) and produces X and Y sperms; the female (XX) produces only X eggs, so the father decides.',
            '(i) 1 (ii) 1 (iii) 2.', ('case',))],
}

CH4S4 = {
    'topic': 'mutation, pedigree analysis and genetic disorders',
    'terms': [('mutation', 'a phenomenon that results in alteration of DNA sequences and consequently changes the genotype and phenotype'),
              ('a point mutation', 'a mutation due to change in a single base pair of DNA, as in sickle-cell anaemia'),
              ('a frameshift mutation', 'a mutation caused by insertion or deletion of base pairs that shifts the reading frame'),
              ('aneuploidy', 'gain or loss of a chromosome due to failure of segregation of chromatids during cell division'),
              ('polyploidy', 'an increase in a whole set of chromosomes due to failure of cytokinesis after telophase, common in plants'),
              ('pedigree analysis', 'the analysis of traits in several generations of a family to study inheritance'),
              ('mutagens', 'chemical and physical factors, such as UV radiation, that induce mutations')],
    'groups': [('a Mendelian disorder', ['haemophilia', 'colour blindness', 'sickle-cell anaemia', 'phenylketonuria', 'thalassaemia', 'cystic fibrosis']),
               ('a chromosomal disorder', ["Down's syndrome", "Klinefelter's syndrome", "Turner's syndrome"])],
    'groups2': [('an X-linked recessive disorder', ['haemophilia', 'colour blindness']), ('an autosomal recessive disorder', ['sickle-cell anaemia', 'phenylketonuria', 'thalassaemia', 'cystic fibrosis']),
                ('a disorder due to sex-chromosome aneuploidy', ["Klinefelter's syndrome", "Turner's syndrome"])],
    'tf': (['Sickle-cell anaemia is caused by substitution of glutamic acid by valine at the sixth position of the β-globin chain.', 'Down\'s syndrome is due to trisomy of chromosome 21.', 'Klinefelter\'s syndrome individuals have the karyotype 47, XXY.',
            'Turner\'s syndrome is due to absence of one X chromosome (45, XO).', 'Colour blindness occurs in about 8% of males and 0.4% of females.'],
           [('Haemophilia is more common in females than males.', 'It is X-linked recessive; males (hemizygous) are affected far more often.'),
            ('Down\'s syndrome is caused by a point mutation.', 'It is a chromosomal disorder due to an extra copy of chromosome 21.'),
            ('Turner\'s syndrome individuals have 47 chromosomes.', 'They have 45 chromosomes (44 + XO).'),
            ('Sickle-cell anaemia is X-linked.', 'It is an autosome-linked recessive trait.'),
            ('Thalassaemia is a qualitative problem of globin synthesis.', 'Thalassaemia is a quantitative problem (too few globin molecules); sickle-cell anaemia is qualitative.')]),
    'ar': [('A haemophilic son can be born to normal parents.', 'The mother may be a carrier of the X-linked recessive allele.', 'a', 'Son receives his X from the mother.'),
           ('Sickle-cell anaemia is caused by a point mutation.', 'GAG is changed to GUG in the β-globin gene codon, so glutamic acid is replaced by valine.', 'a', 'Single base substitution.'),
           ('Down\'s syndrome is a Mendelian disorder.', 'It is caused by non-disjunction leading to trisomy of chromosome 21.', 'd', 'It is a chromosomal disorder; the reason is true.')],
    'features': {'intro': 'A genetic disorder shows these features:', 'q': 'Identify the disorder', 'what': 'disorder',
                 'items': [("Down's syndrome", ['trisomy of chromosome 21', 'short stature with small round head', 'furrowed tongue and partially open mouth', 'palm is broad with a characteristic palm crease']),
                           ("Klinefelter's syndrome", ['karyotype 47, XXY', 'overall masculine development', 'gynaecomastia (breast development)', 'individuals are sterile']),
                           ("Turner's syndrome", ['karyotype 45, XO', 'females are sterile as ovaries are rudimentary', 'lack of secondary sexual characters', 'short stature']),
                           ('sickle-cell anaemia', ['autosomal recessive', 'Glu replaced by Val in β-globin', 'RBCs become sickle shaped under low oxygen', 'heterozygotes are carriers']),
                           ('haemophilia', ['X-linked recessive', 'a protein in the blood clotting cascade is affected', 'a simple cut may cause non-stop bleeding', 'Queen Victoria\'s family pedigree shows many affected descendants'])]},
    'fams': [F('C3', 'D3', 'mcq', sexlinked), F('C2', 'D2', 'mcq', disorder_cause), F('C4', 'D4', 'mcq', sexlinked)],
    'qa': [('C4', 'D4', 'explain', 'Explain why haemophilia is seen more often in men than in women.',
            'The gene is on the X chromosome and is recessive. Males have only one X (hemizygous), so a single defective allele causes the disease; females need two copies, which is rare as it needs a carrier mother and an affected father.',
            '1 mark X-linked recessive; 1 mark hemizygous males.'),
           ('C4', 'D3', 'case', 'In a family in Hyderabad, both parents are normal, but their son suffers from a disorder in which his blood does not clot properly. His sister is normal.\n(i) Name the disorder and how it is inherited. (1 mark)\n(ii) Write the genotypes of the parents. (2 marks)\n(iii) What is the chance that the sister is a carrier? (1 mark)',
            '(i) Haemophilia; X-linked recessive. (ii) Mother XᴴXʰ (carrier), father XᴴY (normal). (iii) ½ (50%).',
            '(i) 1 (ii) 2 (iii) 1.', ('case',))],
}

SPECS = {'ch01-st1': CH1S1, 'ch01-st2': CH1S2, 'ch01-st3': CH1S3, 'ch01-st4': CH1S4,
         'ch02-st1': CH2S1, 'ch02-st2': CH2S2, 'ch02-st3': CH2S3, 'ch02-st4': CH2S4,
         'ch03-st1': CH3S1, 'ch03-st2': CH3S2, 'ch03-st3': CH3S3,
         'ch04-st1': CH4S1, 'ch04-st2': CH4S2, 'ch04-st3': CH4S3, 'ch04-st4': CH4S4}
FAMILIES = build_all(P, SPECS)
