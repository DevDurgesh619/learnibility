"""CBSE Class 12 Biology, chapters 5-8: molecular basis of inheritance, evolution, human health and disease,
microbes in human welfare. Fact tables follow NCERT Biology XII; numbers are computed here.
"""
from __future__ import annotations

import math

from qbank import F, ar, mcq, name, num
from g11_chemistry_kit import build_all, sf, sci, cap
from g12_biology_a import table_mcq, table_rev, table_explain

P = 'cbse-g12-biology'

# ---------------------------------------------------------------- ch05 molecular basis of inheritance

COMP = {'A': 'T', 'T': 'A', 'G': 'C', 'C': 'G'}
TRANS = {'A': 'U', 'T': 'A', 'G': 'C', 'C': 'G'}


def dna_length(r):
    org, bp = r.choice([('bacteriophage φ×174', 5386), ('bacteriophage lambda', 48502), ('Escherichia coli', 4.6e6), ('a human diploid cell', 6.6e9)])
    L = bp * 0.34e-9
    if L >= 1:
        ans = f'{sf(L, 2)} m'
    elif L >= 1e-3:
        ans = f'{sf(L * 1000, 3)} mm'
    else:
        ans = f'{sf(L * 1e6, 3)} µm'
    bps = sci(bp, 2) if bp >= 1e6 else num(bp)
    return {'stem': f'The DNA of {org} has {bps} base pairs. If the distance between two consecutive base pairs is 0.34 nm, calculate the length of the DNA.',
            'answer': ans, 'key': f'Length = number of bp × 0.34 × 10⁻⁹ m = {bps} × 0.34 × 10⁻⁹ m (1) = {sci(L, 3) + " m = " if L < 1 else ""}{ans} (1).',
            'distractors': [f'{sci(L * 10, 2)} m', f'{sci(L / 2, 2)} m', f'{sci(bp * 3.4e-9 * 10, 2)} m']}


def h_bonds(r):
    n = r.choice([100, 200, 500, 1000, 2000])
    pa = r.choice([20, 25, 30, 35, 40])
    at = n * pa / 100 * 2
    gc = n - at
    hb = at * 2 + gc * 3
    return {'stem': f'A double-stranded DNA segment of {n} base pairs contains {pa}% adenine. How many hydrogen bonds hold the two strands together?',
            'answer': f'{num(hb)} hydrogen bonds',
            'key': f'A = T = {pa}% ⇒ A–T pairs = {2 * pa}% of {n} = {num(at)} (1); G≡C pairs = {num(gc)} (½); H-bonds = 2 × {num(at)} + 3 × {num(gc)} = {num(hb)} (1½).',
            'distractors': [f'{num(at * 3 + gc * 2)} hydrogen bonds', f'{num(n * 2.5)} hydrogen bonds', f'{num(hb * 2)} hydrogen bonds']}


def nucleosomes(r):
    bp = r.choice([2000, 4000, 10000, 20000, 200000, 2e6])
    n = bp / 200
    return {'stem': f'A typical nucleosome contains about 200 bp of DNA helix. How many nucleosomes would be formed by a DNA segment of {num(bp)} bp in a eukaryotic nucleus?',
            'answer': f'{num(n)} nucleosomes', 'key': f'Number = total bp / bp per nucleosome = {num(bp)}/200 = {num(n)} (1); each has a histone octamer around which DNA is wrapped (1).',
            'distractors': [f'{num(round(bp / 146))} nucleosomes', f'{num(n * 8)} nucleosomes', f'{num(bp / 2000)} nucleosomes']}


def comp_strand(r):
    s = ''.join(r.choice('ATGC') for _ in range(r.choice([9, 10, 12])))
    good = ''.join(COMP[c] for c in s)
    wrong = [''.join(TRANS[c] for c in s), good[::-1], ''.join({'A': 'G', 'G': 'A', 'T': 'C', 'C': 'T'}[c] for c in s)]
    return mcq(f'One strand of a DNA segment reads 5′-{s}-3′. What is the sequence of its complementary strand, written 3′ → 5′?', f'3′-{good}-5′',
               [f'3′-{w}-5′' for w in wrong], f'A pairs with T and G with C, and the strands are antiparallel: 3′-{good}-5′.', r)


def mrna(r):
    s = ''.join(r.choice('ATGC') for _ in range(r.choice([9, 12])))
    mode = r.choice(['coding', 'template'])
    if mode == 'coding':
        good = s.replace('T', 'U')
        stem = f'The coding strand of a structural gene reads 5′-{s}-3′. Write the sequence of the mRNA transcribed from this gene (5′ → 3′).'
        key = 'mRNA has the same sequence as the coding strand except that U replaces T'
        wrong = [''.join(TRANS[c] for c in s), s, ''.join(TRANS[c] for c in s)[::-1]]
    else:
        good = ''.join(TRANS[c] for c in s)[::-1]
        stem = f'The template strand of a structural gene reads 3′-{s[::-1]}-5′ when read from left to right. Write the sequence of the mRNA (5′ → 3′).'
        good = ''.join(TRANS[c] for c in s[::-1])
        key = 'mRNA is complementary to the template strand, with U in place of T'
        wrong = [s[::-1].replace('T', 'U'), ''.join(COMP[c] for c in s[::-1]), good[::-1]]
    wrong = [w for w in dict.fromkeys(wrong) if w != good]
    if len(wrong) < 3:
        raise ValueError('degenerate')
    return mcq(stem, f'5′-{good}-3′', [f'5′-{w}-3′' for w in wrong[:3]], f'{key}: 5′-{good}-3′.', r)


CODONS = {'UUU': 'Phe', 'UUC': 'Phe', 'UUA': 'Leu', 'UUG': 'Leu', 'CUU': 'Leu', 'AUU': 'Ile', 'AUG': 'Met', 'GUU': 'Val', 'GUC': 'Val',
          'UCU': 'Ser', 'CCU': 'Pro', 'ACU': 'Thr', 'GCU': 'Ala', 'UAU': 'Tyr', 'CAU': 'His', 'CAA': 'Gln', 'AAU': 'Asn', 'AAA': 'Lys',
          'GAU': 'Asp', 'GAA': 'Glu', 'UGU': 'Cys', 'UGG': 'Trp', 'CGU': 'Arg', 'GGU': 'Gly', 'GGC': 'Gly', 'AGA': 'Arg'}
STOPS = ['UAA', 'UAG', 'UGA']


def translate(r):
    k = r.choice([3, 4, 5, 6])
    body = [r.choice(list(CODONS)) for _ in range(k)]
    stop = r.choice(STOPS)
    seq = 'AUG' + ''.join(body) + stop
    aa = ['Met'] + [CODONS[c] for c in body]
    good = '–'.join(aa)
    wrong = ['–'.join(aa[1:]), '–'.join(aa + ['Stop']), '–'.join(aa[:-1])]
    wrong = [w for w in dict.fromkeys(wrong) if w != good]
    return {'stem': f'An mRNA has the sequence 5′-{seq}-3′. Using the genetic code, write the polypeptide formed and state how many amino acids it has. ({", ".join(sorted(set(f"{c} = {CODONS[c]}" for c in body)))}; AUG = Met; {stop} = stop)',
            'answer': f'{good} ({k + 1} amino acids)', 'key': f'Translation starts at AUG (Met) and reads triplets without gaps (1); {stop} is a stop codon with no tRNA, so translation ends: {good} = {k + 1} amino acids (1).',
            'distractors': [f'{w} ({w.count("–") + 1} amino acids)' for w in wrong]}


def codon_count(r):
    n = r.choice([150, 300, 600, 900, 1200])
    utr = r.choice([0, 30, 60])
    cod = (n - utr) // 3
    aa = cod - 1
    return {'stem': f'The coding region of an mRNA, from the start codon to the stop codon inclusive, has {n - utr} nucleotides. How many amino acids will the polypeptide have?',
            'answer': f'{aa} amino acids', 'key': f'{n - utr} nucleotides = {cod} codons (genetic code is triplet) (1); the stop codon does not code for any amino acid ⇒ {aa} (1).',
            'distractors': [f'{cod} amino acids', f'{n - utr} amino acids', f'{(n - utr) // 2} amino acids']}


GENEXP = [('the lac operon', 'lac z', 'β-galactosidase', 'hydrolyses lactose into galactose and glucose'),
          ('the lac operon', 'lac y', 'permease', 'increases permeability of the cell to β-galactosides'),
          ('the lac operon', 'lac a', 'transacetylase', 'transfers an acetyl group'),
          ('the lac operon', 'i gene', 'repressor', 'binds the operator and switches off transcription in the absence of lactose')]
lac_gene = table_mcq([(b, a, c, d) for a, b, c, d in GENEXP], 'In {b}, which product is coded by the {a}?', why_fmt='{a} codes for {ans}, which {why}.')

RNAS = [('mRNA', 'provides the template for translation'), ('tRNA', 'brings amino acids and reads the genetic code (adapter molecule)'),
        ('rRNA', 'plays structural and catalytic role during translation'), ('hnRNA', 'the primary transcript in eukaryotes that is processed into mRNA'),
        ('snRNA', 'involved in splicing of introns')]
rna_role = table_mcq([(a, '', b, '') for a, b in RNAS], 'What is the function of {a}?', why_fmt='{a}: {ans}.')

POL = [('RNA polymerase I', 'rRNAs (28S, 18S and 5.8S)'), ('RNA polymerase II', 'the precursor of mRNA (hnRNA)'), ('RNA polymerase III', 'tRNA, 5S rRNA and snRNAs')]
pol_role = table_mcq([(a, '', b, '') for a, b in POL], 'In eukaryotes, what does {a} transcribe?', why_fmt='{a} transcribes {ans}.',
                     pool=[b for _, b in POL] + ['DNA from an RNA template', 'the Okazaki fragments of DNA'])

CH5S1 = {
    'topic': 'DNA structure, packaging and the search for genetic material',
    'terms': [('a nucleoside', 'a nitrogenous base linked to the OH of the 1′ carbon of a pentose sugar through an N-glycosidic linkage'),
              ('a nucleotide', 'a nucleoside with a phosphate group linked to the 5′-OH through a phosphoester linkage'),
              ('a nucleosome', 'the unit of chromatin formed by negatively charged DNA wrapped around a positively charged histone octamer'),
              ('euchromatin', 'loosely packed, lightly stained chromatin that is transcriptionally active'),
              ('heterochromatin', 'densely packed, darkly stained chromatin that is transcriptionally inactive'),
              ('transformation', 'the change of one strain of bacterium into another by uptake of DNA, as shown by Griffith'),
              ('Chargaff\'s rule', 'the rule that in double-stranded DNA the ratios A/T and G/C are constant and equal to one')],
    'groups': [('a purine', ['adenine', 'guanine']), ('a pyrimidine', ['cytosine', 'thymine', 'uracil']), ('a histone-related term', ['histone octamer', 'H1 histone', 'nucleosome core'])],
    'classify': False,
    'tf': (['DNA is a polymer of deoxyribonucleotides.', 'Histones are rich in the basic amino acids lysine and arginine.', 'The pitch of the DNA helix is 3.4 nm with about 10 bp per turn.',
            'Hershey and Chase used radioactive ³²P and ³⁵S to show that DNA is the genetic material.', 'RNA was the first genetic material.', 'In DNA the two strands are antiparallel.'],
           [('Histones are rich in acidic amino acids.', 'They are rich in basic amino acids lysine and arginine and are positively charged.'),
            ('The distance between two consecutive base pairs in DNA is 3.4 nm.', 'It is 0.34 nm; 3.4 nm is the pitch of one turn.'),
            ('Hershey and Chase found ³⁵S inside the infected bacteria.', 'Radioactive ³²P (DNA) entered the bacteria; ³⁵S (protein) stayed outside.'),
            ('DNA is more reactive than RNA.', 'RNA is more reactive because of the 2′-OH group; DNA is more stable.'),
            ('In prokaryotes DNA is packed with histones into nucleosomes.', 'Prokaryotes lack histones; their DNA is held by positively charged proteins in a region called the nucleoid.')]),
    'orders': [('levels of DNA packaging in a eukaryotic nucleus', ['DNA double helix', 'nucleosome', 'chromatin fibre (beads-on-string)', 'chromosome'], 'DNA wraps around histone octamers; nucleosomes coil into chromatin fibres that condense into chromosomes.', '→')],
    'ar': [('DNA is a better genetic material than RNA.', 'The 2′-OH group makes RNA labile and easily degradable.', 'a', 'DNA is chemically less reactive and more stable.'),
           ('Histones are positively charged.', 'Histones are rich in lysine and arginine.', 'a', 'These carry positive charges in their side chains.'),
           ('In the Hershey–Chase experiment the bacteria became radioactive with ³²P.', 'DNA, which contains phosphorus, entered the bacteria.', 'a', 'Protein (sulphur) stayed outside.'),
           ('Heat-killed S strain alone kills mice.', 'The capsule of S strain is required to cause disease.', 'd', 'Heat-killed S strain alone does not kill mice; the reason is true.')],
    'features': {'intro': 'A classic experiment showed this:', 'q': 'Which experiment is described', 'what': 'experiment', 'long': False,
                 'items': [("Griffith's experiment", ['used Streptococcus pneumoniae', 'S strain kills mice, R strain does not', 'heat-killed S + live R killed mice', 'showed a transforming principle']),
                           ('the Hershey–Chase experiment', ['used bacteriophages', 'proteins labelled with ³⁵S and DNA with ³²P', 'blending and centrifugation separated viral coats', 'showed DNA is the genetic material']),
                           ('the Meselson–Stahl experiment', ['used ¹⁵N and ¹⁴N', 'CsCl density gradient centrifugation', 'hybrid DNA after one generation', 'showed semiconservative replication']),
                           ("Avery, MacLeod and McCarty's work", ['purified biochemicals from heat-killed S cells', 'DNase stopped transformation', 'protease and RNase did not', 'identified DNA as the transforming principle'])]},
    'fams': [F('C3', 'D3', 'numerical', dna_length), F('C4', 'D4', 'multi_step', h_bonds), F('C3', 'D3', 'mcq', comp_strand), F('C3', 'D2', 'numerical', nucleosomes)],
    'qa': [('C4', 'D5', 'long', 'Describe the salient features of the double helix model of DNA proposed by Watson and Crick.',
            'Two polynucleotide chains with a sugar–phosphate backbone and bases projecting inwards; chains are antiparallel (5′→3′ and 3′→5′); bases pair by hydrogen bonds, A=T (two) and G≡C (three), so a purine always faces a pyrimidine giving uniform 2 nm width; chains are coiled right-handed; pitch 3.4 nm with about 10 bp per turn; 0.34 nm between base pairs; base-pair stacking adds stability.',
            '1 mark each for five features.'),
           ('C4', 'D3', 'case', 'In a laboratory in Bengaluru, students repeat a version of the Hershey–Chase experiment with bacteriophages grown on ³²P or ³⁵S.\n(i) Which component of the virus is labelled by each isotope? (1 mark)\n(ii) After infection, blending and centrifugation, where is the radioactivity found in each case? (2 marks)\n(iii) What does this prove? (1 mark)',
            '(i) ³²P labels DNA; ³⁵S labels protein. (ii) ³²P is found in the bacterial pellet (DNA entered the cells); ³⁵S is in the supernatant with the viral coats. (iii) DNA, not protein, is the genetic material passed from virus to bacteria.',
            '(i) 1 (ii) 2 (iii) 1.', ('case',))],
}

CH5S2 = {
    'topic': 'DNA replication',
    'terms': [('semiconservative replication', 'replication in which each daughter DNA molecule has one parental and one newly synthesised strand'),
              ('the replication fork', 'the small opening of the DNA helix where replication occurs'),
              ('Okazaki fragments', 'the short discontinuous pieces synthesised on the lagging strand template'),
              ('DNA ligase', 'the enzyme that joins the discontinuously synthesised fragments'),
              ('DNA-dependent DNA polymerase', 'the main enzyme that catalyses polymerisation of deoxynucleotides only in the 5′→3′ direction'),
              ('the origin of replication (ori)', 'the definite region of DNA where replication starts')],
    'tf': (['DNA polymerase can polymerise nucleotides only in the 5′→3′ direction.', 'In E. coli replication is completed in about 18 minutes.', 'Replication occurs in the S phase of the cell cycle.',
            'Deoxyribonucleoside triphosphates act as substrates and provide energy.', 'Meselson and Stahl used ¹⁵NH₄Cl to show semiconservative replication.'],
           [('DNA polymerase polymerises in the 3′→5′ direction.', 'It polymerises only in the 5′→3′ direction.'),
            ('Okazaki fragments are formed on the leading strand.', 'They are formed on the lagging strand (template 5′→3′).'),
            ('After two generations in ¹⁴N medium, all DNA was hybrid.', 'After two generations, equal amounts of hybrid and light DNA were found.'),
            ('Replication in eukaryotes occurs in the M phase.', 'It occurs in the S phase; failure of cell division after replication gives polyploidy.')]),
    'orders': [('sequence of events in DNA replication', ['unwinding at ori', 'formation of replication fork', 'polymerisation 5′→3′', 'joining of Okazaki fragments by ligase'], 'The helix opens at the origin, synthesis proceeds at the fork and ligase seals fragments.', '→')],
    'ar': [('Replication is continuous on one strand and discontinuous on the other.', 'DNA polymerase works only in the 5′→3′ direction.', 'a', 'The lagging strand is made in pieces.'),
           ('After one generation in ¹⁴N medium all DNA had hybrid density.', 'DNA replication is semiconservative.', 'a', 'Each molecule has one ¹⁵N and one ¹⁴N strand.'),
           ('DNA replication needs a large amount of energy.', 'Deoxyribonucleoside triphosphates serve both as substrate and energy source.', 'a', 'Two terminal phosphates are high-energy bonds.')],
    'features': {'intro': 'During replication a strand shows these features:', 'q': 'Which strand is it', 'what': 'strand', 'compare': True,
                 'items': [('the leading strand', ['synthesised continuously', 'template has 3′→5′ polarity', 'needs only one primer', 'synthesised towards the replication fork']),
                           ('the lagging strand', ['synthesised discontinuously', 'template has 5′→3′ polarity', 'forms Okazaki fragments', 'fragments are joined by DNA ligase'])]},
    'qa': [('C4', 'D5', 'long', 'Describe the Meselson and Stahl experiment and explain how it proved that DNA replicates semiconservatively.',
            'E. coli was grown for many generations in ¹⁵NH₄Cl so all DNA was heavy (¹⁵N). Cells were shifted to ¹⁴NH₄Cl and DNA was extracted at intervals and centrifuged in a CsCl density gradient. After one generation (20 min) all DNA had hybrid (intermediate) density; after two generations (40 min) equal amounts of hybrid and light DNA were found. This is expected only if each new molecule keeps one old strand.',
            '1 mark setup; 1 mark CsCl gradient; 2 marks results; 1 mark conclusion.'),
           ('C4', 'D4', 'explain', 'Why is replication discontinuous on one strand? Name the enzyme that joins the fragments.',
            'The two strands are antiparallel and DNA polymerase can add nucleotides only in the 5′→3′ direction; so on the template with 5′→3′ polarity the new strand is made in short Okazaki fragments, which are joined by DNA ligase.',
            '1 mark reason; 1 mark ligase.'),
           ('C4', 'D3', 'case', 'Tanya models DNA replication using two coloured ribbons for the parental strands.\n(i) Why does each daughter molecule have one ribbon of the old colour? (1 mark)\n(ii) Name the main enzyme and the energy source for polymerisation. (2 marks)\n(iii) In which phase of the eukaryotic cell cycle does replication occur? (1 mark)',
            '(i) Replication is semiconservative: each parental strand acts as a template. (ii) DNA-dependent DNA polymerase; deoxyribonucleoside triphosphates. (iii) S phase.',
            '(i) 1 (ii) 2 (iii) 1.', ('case',))],
}

CH5S3 = {
    'topic': 'transcription, genetic code and translation',
    'terms': [('transcription', 'the process of copying genetic information from one strand of DNA into RNA'),
              ('a cistron', 'a segment of DNA coding for a polypeptide'),
              ('splicing', 'the removal of introns and joining of exons in the primary transcript'),
              ('capping', 'the addition of methyl guanosine triphosphate to the 5′ end of hnRNA'),
              ('tailing', 'the addition of adenylate residues (200–300) at the 3′ end of hnRNA'),
              ('a codon', 'a triplet of bases on mRNA that codes for an amino acid'),
              ('aminoacylation', 'the charging of tRNA, in which an amino acid is activated in the presence of ATP and linked to its tRNA'),
              ('the untranslated regions (UTRs)', 'extra sequences on mRNA before the start codon and after the stop codon that are needed for efficient translation')],
    'tf': (['The genetic code is triplet, degenerate, unambiguous and nearly universal.', 'AUG codes for methionine and is the initiator codon.', 'UAA, UAG and UGA are stop codons.',
            'In bacteria, transcription and translation can be coupled.', 'The ribosome itself acts as a catalyst (ribozyme) for peptide bond formation.', 'There are 61 codons that code for amino acids.'],
           [('The genetic code is ambiguous.', 'It is unambiguous and specific: one codon codes for only one amino acid.'),
            ('Stop codons have specific tRNAs.', 'There are no tRNAs for stop codons.'),
            ('In eukaryotes splicing removes exons.', 'Splicing removes introns and joins exons.'),
            ('The genetic code is non-degenerate.', 'It is degenerate: some amino acids are coded by more than one codon.'),
            ('RNA polymerase III transcribes mRNA in eukaryotes.', 'RNA polymerase II transcribes the precursor of mRNA (hnRNA); RNA polymerase III makes tRNA, 5S rRNA and snRNAs.')]),
    'orders': [('sequence of post-transcriptional processing in eukaryotes', ['hnRNA (primary transcript)', 'splicing', 'capping and tailing', 'mRNA exported to cytoplasm'], 'Introns removed, 5′ cap and 3′ poly-A tail added.', '→'),
               ('sequence of steps in translation', ['charging of tRNA', 'initiation at AUG', 'elongation by peptide bonds', 'termination at stop codon', 'release of polypeptide'], 'Release factor binds the stop codon.', '→')],
    'ar': [('The genetic code is said to be degenerate.', 'Some amino acids are coded by more than one codon.', 'a', 'e.g. Phe: UUU and UUC.'),
           ('tRNA is called an adapter molecule.', 'tRNA has an anticodon that reads the codon and an amino acid acceptor end.', 'a', 'It links code to amino acid.'),
           ('Transcription and translation are coupled in bacteria.', 'In bacteria mRNA does not need processing and there is no nuclear membrane.', 'a', 'Both occur in the cytoplasm.'),
           ('A point mutation changing one base always changes the protein.', 'The genetic code is degenerate.', 'd', 'Because of degeneracy, some point mutations are silent; the reason is true.')],
    'features': {'intro': 'A structure or molecule involved in gene expression has these features:', 'q': 'Identify it', 'what': 'molecule', 'long': False,
                 'items': [('tRNA', ['clover-leaf secondary structure', 'anticodon loop', 'amino acid acceptor end', 'inverted L-shaped 3D structure']),
                           ('mRNA', ['carries the codons', 'has 5′ cap and 3′ poly-A tail in eukaryotes', 'has untranslated regions', 'template for translation']),
                           ('the ribosome', ['made of rRNA and proteins', 'two subunits', 'site of peptide bond formation', 'larger subunit has two sites for tRNA']),
                           ('the transcription unit', ['has a promoter, structural gene and terminator', 'promoter is towards the 5′ end of the coding strand', 'only the template strand is transcribed', 'coding strand has the same sequence as RNA except T for U'])]},
    'fams': [F('C3', 'D3', 'mcq', mrna), F('C4', 'D4', 'numerical', translate, marks=2), F('C3', 'D2', 'numerical', codon_count), F('C2', 'D2', 'mcq', rna_role), F('C2', 'D2', 'mcq', pol_role)],
    'qa': [('C4', 'D5', 'long', 'Describe the process of transcription in bacteria. How is it different in eukaryotes?',
            'In bacteria a single DNA-dependent RNA polymerase binds the promoter and initiates transcription (σ factor), elongates using ribonucleoside triphosphates, and terminates at the terminator (ρ factor). In eukaryotes there are three RNA polymerases (I: rRNAs; II: hnRNA; III: tRNA, 5S rRNA, snRNA); genes are split, so the primary transcript (hnRNA) is spliced to remove introns, capped at the 5′ end with methyl guanosine triphosphate and tailed with poly-A at the 3′ end before transport to the cytoplasm.',
            '2 marks bacteria; 3 marks eukaryotic differences.'),
           ('C4', 'D3', 'case', 'Sahil reads that a patient\'s haemoglobin has valine instead of glutamic acid at position 6 of the β chain.\n(i) Name the disorder. (1 mark)\n(ii) What change in the mRNA codon causes this? (1 mark)\n(iii) What kind of mutation is it, and why does a single base change alter the protein here? (2 marks)',
            '(i) Sickle-cell anaemia. (ii) GAG changed to GUG. (iii) A point mutation (base substitution); the new codon codes for a different amino acid, as the code is read in triplets.',
            '(i) 1 (ii) 1 (iii) 2.', ('case',))],
}

CH5S4 = {
    'topic': 'regulation of gene expression: the lac operon',
    'terms': [('an operon', 'a polycistronic structural gene regulated by a common promoter and regulatory genes, as in bacteria'),
              ('an inducer', 'a substance such as lactose that inactivates the repressor and switches on the operon'),
              ('the operator', 'the DNA sequence next to the promoter to which the repressor binds'),
              ('the repressor', 'the protein coded by the i gene that binds the operator and blocks transcription'),
              ('negative regulation', 'control of an operon by a repressor that prevents transcription')],
    'tf': (['The lac operon is switched on in the presence of lactose.', 'Lactose acts as the inducer of the lac operon.', 'The i gene is constitutively expressed.',
            'Regulation of the lac operon by the repressor is negative regulation.', 'The lac operon was explained by Jacob and Monod.'],
           [('In the absence of lactose the repressor cannot bind the operator.', 'Without lactose the repressor binds the operator and blocks RNA polymerase.'),
            ('The lac z gene codes for permease.', 'lac z codes for β-galactosidase; lac y codes for permease.'),
            ('Glucose is the inducer of the lac operon.', 'Lactose (or allolactose) is the inducer.'),
            ('The repressor is coded by lac a.', 'The repressor is coded by the i gene; lac a codes for transacetylase.')]),
    'ar': [('The lac operon is an inducible operon.', 'Lactose inactivates the repressor and allows transcription.', 'a', 'Substrate induces enzyme synthesis.'),
           ('In the absence of lactose, β-galactosidase is not made.', 'The repressor binds the operator and prevents RNA polymerase from transcribing.', 'a', 'Operon is switched off.'),
           ('The i gene is called a regulator gene.', 'The i gene codes for the repressor protein.', 'a', 'i stands for inhibitor.')],
    'features': {'intro': 'A part of the lac operon has this role:', 'q': 'Identify the part', 'what': 'part', 'case': False,
                 'items': [('lac z', ['structural gene', 'codes for β-galactosidase', 'enzyme hydrolyses lactose', 'products are galactose and glucose']),
                           ('lac y', ['structural gene', 'codes for permease', 'increases permeability to β-galactosides', 'helps lactose enter the cell']),
                           ('the i gene', ['regulatory gene', 'codes for the repressor', 'expressed constitutively', 'not part of the polycistronic mRNA']),
                           ('the operator', ['DNA sequence next to the promoter', 'repressor binds here', 'controls access of RNA polymerase', 'switch of the operon'])]},
    'fams': [F('C2', 'D2', 'mcq', lac_gene), F('C3', 'D3', 'mcq', lac_gene)],
    'qa': [('C4', 'D5', 'long', 'Explain the lac operon with a labelled diagram. What happens in the presence and in the absence of lactose?',
            'The lac operon has a regulatory i gene (repressor), promoter, operator and three structural genes z (β-galactosidase), y (permease), a (transacetylase). Absence of lactose: repressor binds the operator, RNA polymerase cannot transcribe – operon off. Presence of lactose: lactose (inducer) enters through permease and binds the repressor, which becomes inactive and cannot bind the operator; RNA polymerase transcribes the polycistronic mRNA – operon on. This is negative regulation.',
            '2 marks diagram; 1.5 marks absence; 1.5 marks presence.'),
           ('C4', 'D4', 'explain', 'Why is the lac operon said to be under negative regulation? What would happen if the repressor gene were mutated so that no repressor is formed?',
            'The repressor protein switches the operon off by binding to the operator; lactose switches it on by inactivating the repressor. Without a functional repressor the structural genes would be transcribed all the time (constitutive expression), even without lactose.',
            '1 mark negative regulation; 1 mark mutant effect.'),
           ('C4', 'D3', 'case', 'E. coli cells growing in a medium with glucose are moved to a medium with only lactose. After some time they produce β-galactosidase.\n(i) Why was β-galactosidase not produced earlier? (1 mark)\n(ii) What acts as the inducer? (1 mark)\n(iii) Explain how the inducer switches on the operon. (2 marks)',
            '(i) Without lactose, the repressor bound the operator and blocked transcription. (ii) Lactose (allolactose). (iii) Lactose binds the repressor and inactivates it; the repressor leaves the operator and RNA polymerase transcribes z, y and a genes.',
            '(i) 1 (ii) 1 (iii) 2.', ('case',))],
}

CH5S5 = {
    'topic': 'Human Genome Project and DNA fingerprinting',
    'terms': [('the Human Genome Project', 'the international project (1990–2003) to sequence the complete human genome'),
              ('ESTs', 'expressed sequence tags, used to identify the genes expressed as RNA'),
              ('sequence annotation', 'sequencing the whole set of the genome and later assigning functions to the different regions'),
              ('DNA fingerprinting', 'the technique of identifying differences in specific regions of DNA called repetitive DNA'),
              ('VNTR', 'variable number tandem repeats, minisatellites used as probes in DNA fingerprinting'),
              ('satellite DNA', 'repetitive DNA that separates as a minor peak during density gradient centrifugation'),
              ('polymorphism', 'variation at the genetic level in a population, arising through mutations')],
    'tf': (['The human genome has about 3 × 10⁹ bp.', 'Less than 2% of the genome codes for proteins.', 'Chromosome 1 has the most genes (2968) and the Y chromosome the fewest (231).',
            'DNA fingerprinting was developed by Alec Jeffreys.', 'BACs and YACs were used as vectors for sequencing.', 'About 1.4 million single base DNA differences (SNPs) were identified.'],
           [('The human genome contains about 80,000 genes.', 'It contains an estimated 20,500 genes.'),
            ('Most of the human genome codes for proteins.', 'Less than 2% codes for proteins.'),
            ('The Y chromosome has the largest number of genes.', 'Chromosome 1 has the most genes; Y has the fewest.'),
            ('DNA fingerprinting uses the DNA sequences that code for proteins.', 'It uses repetitive (satellite) DNA such as VNTRs, which do not code for proteins.')]),
    'orders': [('sequence of steps in DNA fingerprinting', ['isolation of DNA', 'digestion by restriction endonucleases', 'separation by gel electrophoresis', 'Southern blotting', 'hybridisation with labelled VNTR probe', 'autoradiography'], 'Steps of the Southern blot hybridisation method.', '→')],
    'ar': [('DNA fingerprinting is used in paternity disputes.', 'Each person inherits half of their VNTR alleles from each parent.', 'a', 'Bands can be matched to parents.'),
           ('Repetitive DNA is useful in DNA fingerprinting.', 'The number of repeats varies greatly between individuals.', 'a', 'High polymorphism.'),
           ('The human genome has many genes that code for proteins in every region.', 'Less than 2% of the genome codes for proteins.', 'd', 'Most of the genome is non-coding; the reason is true.')],
    'features': {'intro': 'A feature of the human genome is:', 'q': 'Which statement describes it', 'what': 'feature', 'long': False, 'case': False,
                 'items': [('genome size', ['about 3164.7 million bp', 'sequenced by 2003', 'BACs and YACs used as vectors', 'shotgun sequencing approach']),
                           ('gene content', ['about 20,500 genes', 'average gene 3000 bases', 'dystrophin is the largest known gene (2.4 million bases)', 'function unknown for over 50% of discovered genes']),
                           ('repetitive sequences', ['repeated hundreds to thousands of times', 'form a large part of the genome', 'thought to have no direct coding function', 'used in DNA fingerprinting'])]},
    'qa': [('C4', 'D5', 'long', 'What is DNA fingerprinting? Describe the steps involved, and give two applications.',
            'A technique to identify individuals by differences in repetitive DNA (VNTRs). Steps: isolate DNA; digest with restriction enzymes; separate fragments by gel electrophoresis; transfer (blot) to nylon or nitrocellulose membrane (Southern blotting); hybridise with labelled VNTR probe; detect by autoradiography. Applications: forensic identification of criminals, paternity testing, population and evolutionary studies.',
            '1 mark definition; 3 marks steps; 1 mark applications.'),
           ('C4', 'D3', 'case', 'In a court case in Delhi, DNA from a blood stain is compared with DNA of three suspects.\n(i) Which kind of DNA sequences are compared? (1 mark)\n(ii) Why do these sequences differ among people? (1 mark)\n(iii) Name the technique by which the DNA bands are transferred to a membrane and the method used to visualise them. (2 marks)',
            '(i) Repetitive DNA (satellite DNA such as VNTRs). (ii) The number of tandem repeats varies widely between individuals (polymorphism). (iii) Southern blotting; hybridisation with a labelled probe followed by autoradiography.',
            '(i) 1 (ii) 1 (iii) 2.', ('case',)),
           ('C4', 'D4', 'explain', 'List two goals of the Human Genome Project and two salient findings.',
            'Goals: identify all the approximately 20,500 human genes; determine the sequences of the 3 billion base pairs; store information in databases; improve tools for analysis; address ethical, legal and social issues. Findings: genome has 3164.7 million bp; less than 2% codes for proteins; chromosome 1 has most genes, Y the fewest; about 1.4 million SNPs.',
            '1 mark goals; 1 mark findings.')],
}

# ---------------------------------------------------------------- ch06 evolution


def hardy(r):
    q2 = r.choice([0.01, 0.04, 0.09, 0.16, 0.36, 0.0025, 0.0004])
    q = math.sqrt(q2)
    p = 1 - q
    who = r.choice(['albinism', 'cystic fibrosis'] if q2 <= 0.01 else ['a recessive trait', 'white flowers', 'dwarf height'])
    n = r.choice([1000, 5000, 10000, 2500])
    car = 2 * p * q
    return {'stem': f'In a population in Hardy–Weinberg equilibrium, {num(q2 * 100, 2)}% of individuals show {who} (homozygous recessive). Calculate the frequencies of the recessive and dominant alleles and the expected number of heterozygous carriers in a population of {n}.',
            'answer': f'q = {num(q, 2)}, p = {num(p, 2)}; carriers = {num(car * n, 0)}',
            'key': f'q² = {q2} ⇒ q = {num(q, 2)} (1); p = 1 − q = {num(p, 2)} (1); 2pq = {num(car, 4)} ⇒ {num(car, 4)} × {n} = {num(car * n, 0)} carriers (1).',
            'distractors': [f'q = {num(q2, 4)}, p = {num(1 - q2, 4)}; carriers = {num(2 * q2 * (1 - q2) * n, 0)}', f'q = {num(q, 2)}, p = {num(p, 2)}; carriers = {num(p * q * n, 0)}', f'q = {num(p, 2)}, p = {num(q, 2)}; carriers = {num(car * n, 0)}']}


def hw_freq(r):
    p = r.choice([0.1, 0.2, 0.3, 0.4, 0.6, 0.7, 0.8, 0.9])
    q = round(1 - p, 2)
    which = r.choice(['AA', 'Aa', 'aa'])
    val = {'AA': p * p, 'Aa': 2 * p * q, 'aa': q * q}[which]
    wrong = {'AA': [2 * p * q, q * q, p], 'Aa': [p * q, p * p, q * q], 'aa': [2 * p * q, p * p, q]}[which]
    w = [num(x, 2) for x in wrong if abs(x - val) > 1e-9]
    w = list(dict.fromkeys(w))
    if len(w) < 3:
        w.append(num(val / 2, 2))
    return mcq(f'In a population in Hardy–Weinberg equilibrium the frequency of allele A is {p}. What is the expected frequency of genotype {which}?', num(val, 2), w[:3],
               f'p = {p}, q = {q}; p² + 2pq + q² = 1 ⇒ {which} = {num(val, 2)}.', r)


EVID = [('the forelimbs of whales, bats, cheetahs and humans', 'homologous organs', 'divergent evolution'),
        ('the wings of butterflies and birds', 'analogous organs', 'convergent evolution'),
        ('thorns of Bougainvillea and tendrils of Cucurbita', 'homologous organs', 'divergent evolution'),
        ('the eyes of octopus and of mammals', 'analogous organs', 'convergent evolution'),
        ('the flippers of penguins and of dolphins', 'analogous organs', 'convergent evolution'),
        ('sweet potato (root) and potato (stem)', 'analogous organs', 'convergent evolution'),
        ('the vertebrate hearts and brains', 'homologous organs', 'divergent evolution')]
evid = table_mcq([(a, '', b, c) for a, b, c in EVID], 'What do {a} represent?', why_fmt='{a} are {ans}, showing {why}.', pool=['homologous organs', 'analogous organs', 'vestigial organs', 'atavistic organs'])

HUMAN = [('Ramapithecus (and Dryopithecus)', 'about 15 million years ago', 'hairy, walked like gorillas and chimpanzees; Ramapithecus more man-like'),
         ('Australopithecines', 'about 2 million years ago', 'lived in East African grasslands; hunted with stone weapons and ate fruit'),
         ('Homo habilis', 'about 2 million years ago', 'first human-like being; brain capacity 650–800 cc; probably did not eat meat'),
         ('Homo erectus', 'about 1.5 million years ago', 'large brain around 900 cc; probably ate meat'),
         ('Neanderthal man', '1,00,000–40,000 years ago', 'brain size 1400 cc; lived in the Near East and Central Asia; buried their dead'),
         ('Homo sapiens', 'between 75,000–10,000 years ago (ice age)', 'arose in Africa, moved across continents; prehistoric cave art about 18,000 years ago')]


def human_pick(r):
    a, t, d = r.choice(HUMAN)
    wrong = [x[0] for x in HUMAN if x[0] != a]
    return mcq(f'Which ancestor in human evolution is described as: {d}?', a, r.sample(wrong, 3), f'{a} ({t}): {d}.', r)


GEO = [('Paleozoic', ['jawless fish', 'first amphibians', 'first reptiles']), ('Mesozoic', ['dinosaurs dominant', 'first mammals', 'first birds (Archaeopteryx)']),
       ('Cenozoic', ['rise of mammals', 'first primates', 'modern humans'])]

CH6S1 = {
    'topic': 'origin of life and theories of evolution',
    'terms': [('the Big Bang theory', 'the theory that the universe originated about 20 billion years ago from a huge explosion'),
              ('spontaneous generation', 'the old theory that life arose from decaying and rotting matter such as straw and mud'),
              ('panspermia', 'the idea that units of life called spores were transferred to different planets including Earth'),
              ('chemical evolution', 'the formation of diverse organic molecules from inorganic constituents, as proposed by Oparin and Haldane'),
              ('the Miller experiment', 'the 1953 experiment in which electric discharge in a flask of CH₄, H₂, NH₃ and water vapour at 800 °C produced amino acids')],
    'tf': (['Earth was formed about 4.5 billion years ago.', 'Life appeared about 500 million years after the formation of Earth, i.e. almost four billion years back.', 'Louis Pasteur showed that life comes only from pre-existing life.',
            'In Miller\'s experiment amino acids were formed.', 'The first non-cellular forms of life could have originated about 3 billion years ago.'],
           [('Miller used O₂, N₂ and CO₂ in his experiment.', 'He used CH₄, H₂, NH₃ and water vapour (reducing atmosphere).'),
            ('Pasteur proved spontaneous generation.', 'He disproved it: no life formed in pre-sterilised flasks kept sealed.'),
            ('Earth was formed about 20 billion years ago.', 'The universe is about 20 billion years old; Earth formed about 4.5 billion years ago.'),
            ('Early Earth had a free-oxygen atmosphere.', 'Early atmosphere had water vapour, CH₄, CO₂ and NH₃; there was no free oxygen.')]),
    'orders': [('sequence of events in the origin of life', ['formation of Earth', 'chemical evolution', 'formation of macromolecules', 'first cellular life'], 'Inorganic → organic molecules → macromolecules → cells.', '→')],
    'ar': [('Miller\'s experiment supported chemical evolution.', 'Amino acids were formed from simple gases under conditions like early Earth.', 'a', 'Organic molecules from inorganic ones.'),
           ('Pasteur disproved spontaneous generation.', 'In sealed, pre-sterilised flasks no life arose from killed yeast.', 'a', 'Life comes from pre-existing life.')],
    'features': {'intro': 'A theory of the origin of life states:', 'q': 'Which theory is it', 'what': 'theory', 'long': False,
                 'items': [('spontaneous generation', ['life arose from decaying matter', 'disproved by Louis Pasteur', 'believed for a long time', 'no pre-existing life needed']),
                           ('panspermia', ['spores came from outer space', 'favourite idea of some astronomers', 'life transferred between planets', 'still not proven']),
                           ('chemical evolution (Oparin–Haldane)', ['first form of life came from non-living organic molecules', 'formation preceded by chemical evolution', 'supported by Miller\'s experiment', 'early reducing atmosphere'])]},
    'qa': [('C4', 'D4', 'explain', 'Describe the experiment performed by S.L. Miller and state its significance.',
            'In 1953 Miller created electric discharge in a closed flask containing CH₄, H₂, NH₃ and water vapour at 800 °C and observed formation of amino acids. It supported the Oparin–Haldane idea of chemical evolution.',
            '1 mark set-up; 1 mark significance.'),
           ('C4', 'D3', 'case', 'Isha reads two old ideas: one says maggots arise from rotting meat, another says life came to Earth on spores from space.\n(i) Name these two ideas. (1 mark)\n(ii) Who disproved the first, and how? (2 marks)\n(iii) Which theory is now widely accepted? (1 mark)',
            '(i) Spontaneous generation; panspermia. (ii) Louis Pasteur: in pre-sterilised sealed flasks no life arose, while life arose in flasks open to air. (iii) The Oparin–Haldane theory of chemical evolution.',
            '(i) 1 (ii) 2 (iii) 1.', ('case',))],
}

CH6S2 = {
    'topic': 'evidences of evolution',
    'terms': [('homologous organs', 'organs with the same basic structure and origin but different functions'),
              ('analogous organs', 'organs that are not anatomically similar but perform similar functions'),
              ('divergent evolution', 'the evolution of different functions from the same structure in related organisms'),
              ('convergent evolution', 'the development of similar adaptive functions in unrelated groups'),
              ('industrial melanism', 'the increase of dark-winged moths in industrial areas of England after industrialisation'),
              ('palaeontology', 'the study of fossils, which are remains of hard parts of life forms found in rocks')],
    'groups': [('a pair of homologous organs', ['forelimbs of whale and bat', 'thorn of Bougainvillea and tendril of Cucurbita', 'hearts of different vertebrates']),
               ('a pair of analogous organs', ['wings of butterfly and bird', 'eyes of octopus and mammals', 'flippers of penguin and dolphin', 'sweet potato and potato'])],
    'tf': (['Homology indicates common ancestry.', 'Analogy is a result of convergent evolution.', 'Before industrialisation white-winged moths were more common in England.',
            'Excessive use of herbicides and pesticides has selected resistant varieties in a short time.', 'Fossils in different rock layers indicate the geological period in which organisms existed.'],
           [('Analogous organs indicate common ancestry.', 'Homologous organs indicate common ancestry; analogous organs arise by convergent evolution.'),
            ('Wings of butterfly and bird are homologous.', 'They are analogous; they perform the same function but differ in structure.'),
            ('After industrialisation light-coloured moths increased in England.', 'Dark (melanised) moths increased because tree trunks became dark with soot and lichens died.'),
            ('Embryological support for evolution by Ernst Haeckel was fully accepted.', 'Karl Ernst von Baer disapproved it, noting embryos never pass through adult stages of other animals.')]),
    'ar': [('Dark-winged moths increased in industrial England.', 'Dark moths were camouflaged on soot-covered tree trunks and escaped predators.', 'a', 'Natural selection.'),
           ('Forelimbs of whale and bat are homologous.', 'They have the same pattern of bones (humerus, radius, ulna, carpals, metacarpals, phalanges).', 'a', 'Common ancestry.'),
           ('Wings of birds and butterflies are homologous.', 'They perform the same function of flight.', 'd', 'They are analogous; the reason is true.')],
    'fams': [F('C3', 'D3', 'mcq', evid), F('C2', 'D2', 'mcq', evid)],
    'qa': [('C4', 'D4', 'explain', 'How does industrial melanism in England support evolution by natural selection?',
            'Before industrialisation, white-winged moths were more common as they were camouflaged on lichen-covered trees. After industrialisation soot darkened tree trunks and killed lichens, so dark-winged moths escaped predators and increased. The environment selected the better-adapted form.',
            '1 mark observation; 1 mark selection explanation.'),
           ('C4', 'D3', 'case', 'Rohit compares the forelimbs of a whale, a bat and a human, and the wings of a sparrow and a butterfly.\n(i) Which of these are homologous? (1 mark)\n(ii) Which are analogous? (1 mark)\n(iii) Name the type of evolution each pair shows and explain the difference. (2 marks)',
            '(i) Forelimbs of whale, bat and human. (ii) Wings of sparrow and butterfly. (iii) Homology – divergent evolution (same structure, different functions, common ancestry); analogy – convergent evolution (different structures evolving to perform the same function).',
            '(i) 1 (ii) 1 (iii) 2.', ('case',)),
           ('C4', 'D5', 'long', 'Discuss the evidences of evolution from palaeontology, comparative anatomy (homology and analogy), and biochemical/molecular similarity, with one example each.',
            'Palaeontology: fossils in rock layers of different ages show extinct forms and changes over time (e.g. dinosaurs). Homology: forelimbs of whales, bats, cheetahs and humans have similar bones – divergent evolution. Analogy: wings of butterflies and birds – convergent evolution. Biochemical: similarities in proteins and genes among diverse organisms indicate common ancestry. Also industrial melanism and resistance to pesticides as evidence of natural selection.',
            '1 mark each for five evidences with examples.')],
}

CH6S3 = {
    'topic': 'natural selection, mechanism of evolution and Hardy–Weinberg principle',
    'terms': [('natural selection', 'the process in which organisms better fit in an environment leave more progeny'),
              ('fitness', 'in Darwin\'s sense, ultimately reproductive fitness – those that are better fit leave more progeny'),
              ('saltation', 'single-step large mutation that de Vries believed caused speciation'),
              ('genetic drift', 'change in allele frequency in a small population by chance'),
              ('the founder effect', 'the drastic change in allele frequency when a small group of individuals forms a new population'),
              ('gene flow', 'the movement of alleles between populations by migration'),
              ('the Hardy–Weinberg principle', 'the principle that allele frequencies in a population are stable and constant from generation to generation in the absence of evolutionary forces')],
    'groups': [('a factor that disturbs Hardy–Weinberg equilibrium', ['gene migration (gene flow)', 'genetic drift', 'mutation', 'genetic recombination', 'natural selection']),
               ('an idea about the origin of life', ['spontaneous generation', 'panspermia (spores from outer space)', 'chemical evolution (Oparin and Haldane)'])],
    'classify': False,
    'tf': (['Darwin and Wallace worked independently on natural selection.', 'Hugo de Vries worked on evening primrose (Oenothera).', 'Mutations are random and directionless.',
            'In Hardy–Weinberg equilibrium p² + 2pq + q² = 1.', 'Branching descent and natural selection are the two key concepts of Darwinian theory.'],
           [('Darwin believed evolution occurs by large sudden mutations.', 'Darwin believed in small, directional variations; de Vries proposed saltation.'),
            ('Mutations are directional, like Darwinian variations.', 'Mutations are random and directionless.'),
            ('Genetic drift is important only in large populations.', 'Genetic drift has the greatest effect in small populations.'),
            ('Lamarck explained the long neck of giraffes by natural selection.', 'Lamarck proposed use and disuse of organs (inheritance of acquired characters).')]),
    'ar': [('Genetic drift can change allele frequencies.', 'Chance events have large effects in small populations.', 'a', 'Founder effect is an example.'),
           ('Mutations are a source of variation.', 'Mutations are random and directionless.', 'b', 'Both true; but randomness does not explain why they are a source of variation.'),
           ('The Hardy–Weinberg equation is p² + 2pq + q² = 1.', 'p and q are frequencies of two alleles of a gene with p + q = 1.', 'a', 'Binomial expansion of (p + q)².')],
    'features': {'intro': 'A pattern of natural selection is described:', 'q': 'Which type of selection is it', 'what': 'selection', 'long': False,
                 'items': [('stabilising selection', ['more individuals acquire the mean character value', 'peak gets higher and narrower', 'extremes are eliminated', 'favours the average']),
                           ('directional selection', ['more individuals acquire a value other than the mean', 'the peak shifts in one direction', 'one extreme is favoured', 'seen in pesticide resistance']),
                           ('disruptive selection', ['more individuals acquire both peripheral values', 'two peaks are formed', 'the mean is selected against', 'can lead to two forms'])]},
    'fams': [F('C4', 'D4', 'multi_step', hardy), F('C3', 'D3', 'mcq', hw_freq)],
    'qa': [('C4', 'D4', 'explain', 'State the Hardy–Weinberg principle. List the five factors that affect it.',
            'Allele frequencies in a population remain constant from generation to generation (p² + 2pq + q² = 1) if there is no disturbance. Factors: gene migration (gene flow), genetic drift, mutation, genetic recombination, natural selection.',
            '1 mark statement; 1 mark factors.'),
           ('C4', 'D5', 'long', 'Explain Darwin\'s theory of natural selection. How is the mutation theory of de Vries different from it?',
            'Darwin: organisms produce more offspring than can survive; there is variation, some of which is heritable; there is struggle for existence; individuals with useful variations survive and reproduce more (natural selection; fitness = reproductive fitness); over generations this leads to new species (branching descent). de Vries (evening primrose): evolution is caused by large, sudden mutations (saltation) that are random and directionless, not by small directional variations.',
            '3 marks Darwin; 2 marks de Vries.')],
}

CH6S4 = {
    'topic': 'adaptive radiation and human evolution',
    'terms': [('adaptive radiation', 'the process of evolution of different species in a geographical area starting from a point and radiating to other habitats'),
              ("Darwin's finches", 'the varieties of finches on the Galapagos islands that evolved different beak types from seed-eating ancestors'),
              ('Australian marsupials', 'pouched mammals that evolved from an ancestral stock within Australia into many forms'),
              ('Homo habilis', 'the first human-like being, with brain capacity of 650–800 cc'),
              ('Neanderthal man', 'the hominid with brain size of 1400 cc that lived in the Near East and Central Asia between 1,00,000 and 40,000 years ago')],
    'tf': (['Darwin\'s finches are an example of adaptive radiation.', 'Placental mammals in Australia show convergent evolution with marsupials.', 'Homo habilis had a brain capacity of 650–800 cc.',
            'Neanderthal man buried the dead.', 'Agriculture came around 10,000 years ago.'],
           [('Homo erectus had a brain capacity of 1400 cc.', 'Homo erectus had about 900 cc; Neanderthals had 1400 cc.'),
            ('Australopithecines lived about 15 million years ago.', 'They lived about 2 mya; Dryopithecus and Ramapithecus existed about 15 mya.'),
            ('Darwin\'s finches show convergent evolution.', 'They show adaptive radiation (divergent evolution) from a common ancestor.'),
            ('Homo sapiens arose in Asia.', 'Homo sapiens arose in Africa and moved across continents.')]),
    'orders': [('sequence of human evolution', ['Dryopithecus', 'Australopithecus', 'Homo habilis', 'Homo erectus', 'Homo neanderthalensis', 'Homo sapiens'], 'Order of appearance in the fossil record.', '→'),
               ('order of brain capacity', ['Homo habilis', 'Homo erectus', 'Neanderthal man'], '650–800 cc, about 900 cc, 1400 cc.', '<')],
    'ar': [('Darwin\'s finches are an example of adaptive radiation.', 'Finches with different beaks evolved from a seed-eating ancestor on the Galapagos.', 'a', 'Radiation into different niches.'),
           ('Placental wolf and Tasmanian wolf look similar.', 'They evolved in similar habitats from different ancestors.', 'a', 'Convergent evolution.'),
           ('Homo habilis ate meat regularly.', 'Homo habilis probably did not eat meat.', 'd', 'A is false; the reason is the NCERT statement.')],
    'features': {'intro': 'A form in human evolution is described:', 'q': 'Identify the form', 'what': 'form', 'compare': True,
                 'items': [(a, [t] + [x.strip() for x in d.split(';')]) for a, t, d in HUMAN]},
    'fams': [F('C3', 'D3', 'mcq', human_pick), F('C2', 'D2', 'mcq', human_pick)],
    'qa': [('C4', 'D4', 'explain', 'What is adaptive radiation? Give two examples.',
            'Evolution of different species in a geographical area from a common ancestor radiating into other habitats. Examples: Darwin\'s finches of the Galapagos; Australian marsupials; placental mammals in Australia.',
            '1 mark definition; 1 mark examples.'),
           ('C4', 'D5', 'long', 'Give a brief account of human evolution from Dryopithecus to Homo sapiens, mentioning brain capacity where known.',
            'About 15 mya Dryopithecus and Ramapithecus (hairy, walked like gorillas). About 2 mya Australopithecines in East Africa (stone weapons, fruit). Homo habilis (650–800 cc, did not eat meat). About 1.5 mya Homo erectus (about 900 cc, ate meat). Neanderthals (1400 cc, 1,00,000–40,000 years ago, buried dead). Homo sapiens arose in Africa during the ice age (75,000–10,000 years ago); cave art about 18,000 years ago; agriculture about 10,000 years ago.',
            '1 mark each for five correct stages.')],
}

# ---------------------------------------------------------------- ch07 human health and disease

DISEASES = [('typhoid', 'Salmonella typhi', 'contaminated food and water; confirmed by the Widal test', 'sustained high fever (39–40 °C), weakness, stomach pain, constipation, headache, loss of appetite', 'bacterium'),
            ('pneumonia', 'Streptococcus pneumoniae and Haemophilus influenzae', 'inhaling droplets or aerosols of an infected person; sharing utensils', 'alveoli fill with fluid; fever, chills, cough, headache; lips and fingernails may turn grey to bluish', 'bacterium'),
            ('common cold', 'rhinoviruses', 'droplets from cough or sneeze; contaminated objects', 'nasal congestion and discharge, sore throat, hoarseness, cough, headache; lasts 3–7 days', 'virus'),
            ('malaria', 'Plasmodium (P. vivax, P. malariae, P. falciparum)', 'bite of the infected female Anopheles mosquito', 'high recurring fever and chills every 3–4 days due to haemozoin', 'protozoan'),
            ('amoebiasis', 'Entamoeba histolytica', 'houseflies carry cysts to food and water', 'constipation, abdominal pain and cramps, stools with excess mucous and blood clots', 'protozoan'),
            ('ascariasis', 'Ascaris', 'eggs in soil, water and plants contaminated by faeces', 'internal bleeding, muscular pain, fever, anaemia and blockage of the intestinal passage', 'helminth'),
            ('filariasis (elephantiasis)', 'Wuchereria (W. bancrofti and W. malayi)', 'bite of the female Culex mosquito', 'chronic inflammation of the lymphatic vessels of the lower limbs and genital organs', 'helminth'),
            ('ringworm', 'Microsporum, Trichophyton and Epidermophyton', 'soil, or towels, clothes and combs of infected persons', 'dry, scaly lesions on skin, nails and scalp with intense itching', 'fungus')]
dis_path = table_mcq([(a, '', b, c) for a, b, c, d, e in DISEASES], 'Which pathogen causes {a}?', why_fmt='{a} is caused by {ans}; spread by {why}.')
dis_sym = table_rev([(a, '', d, b) for a, b, c, d, e in DISEASES], 'Which disease shows these symptoms: {ans}?', why_fmt='{a}: {ans} (pathogen {why}).')
dis_x = table_explain([(a, '', f'{b}; spread by {c}', d) for a, b, c, d, e in DISEASES], 'Name the pathogen and mode of transmission of {a}, and give its main symptoms.',
                      key_fmt='{ans} (1); symptoms: {why} (1).')

ANTIBODY = [('IgA', 'found in colostrum and secretions; gives passive immunity to the new-born'), ('IgE', 'involved in allergic reactions'),
            ('IgG', 'crosses the placenta to the foetus'), ('IgM', 'first antibody produced in a primary response'), ('IgD', 'found on the surface of B cells')]

IMMUN = [('vaccination against polio', 'active immunity', 'the body makes antibodies after exposure to weakened or killed pathogen'),
         ('antibodies passed to the foetus through the placenta', 'passive immunity', 'ready-made antibodies are received'),
         ('colostrum given to a new-born', 'passive immunity', 'IgA antibodies are received ready-made'),
         ('antitoxin injected after a snake bite', 'passive immunity', 'preformed antibodies neutralise the venom quickly'),
         ('recovering from chickenpox', 'active immunity', 'the body makes its own antibodies and memory cells'),
         ('anti-tetanus serum (ATS) given after a deep wound', 'passive immunity', 'preformed antibodies are injected'),
         ('hepatitis B vaccine made by recombinant DNA technology from yeast', 'active immunity', 'antigen stimulates antibody production')]


def immunity4(r):
    a, b, c = r.choice(IMMUN)
    opts = ['active immunity', 'passive immunity', 'innate immunity', 'autoimmunity']
    return mcq(f'What type of immunity is provided by {a}?', b, [o for o in opts if o != b], f'{cap(a)}: {b} – {c}.', r)


DRUGS = [('heroin (smack)', 'opioid', 'Papaver somniferum (poppy) latex, acetylated morphine', 'depressant; slows down body functions'),
         ('morphine', 'opioid', 'Papaver somniferum (poppy) latex', 'very effective sedative and painkiller; useful after surgery'),
         ('marijuana, hashish, charas, ganja', 'cannabinoid', 'inflorescences of Cannabis sativa', 'affect cardiovascular system'),
         ('cocaine (coke, crack)', 'coca alkaloid', 'Erythroxylum coca', 'interferes with transport of dopamine; stimulates the CNS and causes euphoria'),
         ('LSD and products of Atropa belladonna and Datura', 'hallucinogen', 'plants with hallucinogenic properties', 'cause hallucinations')]
drug_src = table_mcq([(a, '', c, d) for a, b, c, d in DRUGS], 'What is the source of {a}?', why_fmt='{a}: {ans}; {why}.')
drug_cls = table_mcq([(a, '', b, d) for a, b, c, d in DRUGS], 'To which group of drugs does {a} belong?', why_fmt='{a} belongs to the group {ans}s; {why}.',
                     pool=['opioid', 'cannabinoid', 'coca alkaloid', 'hallucinogen', 'barbiturate'])

CH7S1 = {
    'topic': 'common diseases in humans',
    'terms': [('a pathogen', 'a disease-causing organism such as a bacterium, virus, fungus, protozoan or helminth'),
              ('the Widal test', 'the test used to confirm typhoid fever'),
              ('haemozoin', 'the toxic substance released when infected RBCs rupture in malaria, causing chills and high fever'),
              ('sporozoites', 'the infectious form of Plasmodium that enters the human body through the bite of an infected female Anopheles'),
              ('vector', 'an organism such as a mosquito or housefly that carries a pathogen from one host to another'),
              ('infectious disease', 'a disease that is easily transmitted from one person to another')],
    'groups': [('a disease caused by a bacterium', ['typhoid', 'pneumonia']), ('a disease caused by a virus', ['common cold', 'AIDS', 'dengue']),
               ('a disease caused by a protozoan', ['malaria', 'amoebiasis']), ('a disease caused by a helminth', ['ascariasis', 'filariasis']), ('a disease caused by a fungus', ['ringworm'])],
    'tf': (['Typhoid Mary was a cook who was a carrier of typhoid.', 'Malignant malaria is caused by Plasmodium falciparum.', 'The female Anopheles mosquito is the vector of malaria.',
            'Filariasis is transmitted by the female Culex mosquito.', 'Gambusia fish feed on mosquito larvae and help control vector-borne diseases.', 'Plasmodium multiplies asexually in the liver cells and then in RBCs.'],
           [('Malaria is caused by a bacterium.', 'It is caused by the protozoan Plasmodium.'),
            ('Pneumonia affects the intestine.', 'Pneumonia affects the alveoli of the lungs.'),
            ('Common cold is caused by bacteria and is cured by antibiotics.', 'It is caused by rhinoviruses; antibiotics do not act on viruses.'),
            ('Ringworm is caused by a worm.', 'Ringworm is a fungal disease caused by Microsporum, Trichophyton and Epidermophyton.'),
            ('Sexual reproduction of Plasmodium occurs in the human RBCs.', 'Gametocytes form in RBCs, but fertilisation and development occur in the mosquito\'s gut.')]),
    'orders': [('sequence of the life cycle of Plasmodium', ['sporozoites enter human blood', 'multiplication in liver cells', 'attack on RBCs', 'gametocytes formed in RBCs', 'mosquito takes up gametocytes', 'fertilisation in mosquito gut', 'sporozoites in salivary glands'], 'Asexual phase in humans and sexual phase in the mosquito.', '→')],
    'ar': [('Malaria patients get recurring chills and high fever.', 'Rupture of RBCs releases the toxin haemozoin.', 'a', 'Every 3–4 days.'),
           ('Mosquito-borne diseases can be controlled by introducing Gambusia in ponds.', 'Gambusia feeds on mosquito larvae.', 'a', 'Biological control of vectors.'),
           ('Antibiotics cure common cold.', 'Common cold is caused by rhinoviruses.', 'd', 'Antibiotics do not act on viruses; the reason is true.')],
    'fams': [F('C2', 'D2', 'mcq', dis_path), F('C3', 'D3', 'mcq', dis_sym), F('C3', 'D2', 'explain', dis_x), F('C2', 'D1', 'mcq', dis_path)],
    'qa': [('C4', 'D5', 'long', 'Describe the life cycle of Plasmodium with the help of a labelled diagram. Why does a malarial patient get high fever at regular intervals?',
            'Sporozoites enter human blood through the bite of an infected female Anopheles; they multiply asexually in liver cells, then attack RBCs, multiplying and rupturing them; gametocytes develop in RBCs. When a female Anopheles bites, gametocytes enter the mosquito, fertilisation and development occur in the gut wall, and sporozoites gather in salivary glands. Rupture of RBCs releases haemozoin, which causes chills and high fever every 3–4 days.',
            '2 marks human phase; 1.5 marks mosquito phase; 1.5 marks diagram and fever.'),
           ('C4', 'D4', 'explain', 'Suggest four measures to prevent infectious diseases.',
            'Personal hygiene (clean body, clean drinking water and food); public hygiene (proper disposal of waste, cleaning of water reservoirs); avoid contact with infected persons; control vectors (no stagnant water, Gambusia, insecticides, mosquito nets); vaccination.',
            '½ mark each, up to 2.'),
           ('C4', 'D3', 'case', 'After heavy rains in Mumbai, many residents report high fever with chills every third day. Another group in the same area has swelling of the legs.\n(i) Name the likely diseases in the two groups. (1 mark)\n(ii) Name the vector of each. (1 mark)\n(iii) Suggest two measures the municipal corporation should take. (2 marks)',
            '(i) Malaria and filariasis (elephantiasis). (ii) Female Anopheles mosquito; female Culex mosquito. (iii) Remove stagnant water, spray insecticides, introduce Gambusia fish in ponds, promote mosquito nets and screens.',
            '(i) 1 (ii) 1 (iii) 2.', ('case',))],
}

CH7S2 = {
    'topic': 'immunity, vaccination, allergies and autoimmunity',
    'terms': [('innate immunity', 'non-specific defence present at the time of birth, provided by barriers'),
              ('acquired immunity', 'pathogen-specific immunity characterised by memory'),
              ('an antibody', 'a protein of the H₂L₂ type (two heavy and two light chains) produced by B lymphocytes'),
              ('humoral immune response', 'the antibody-mediated immune response, as antibodies are found in the blood'),
              ('cell-mediated immunity', 'the immune response mediated by T lymphocytes, responsible for graft rejection'),
              ('an allergen', 'a substance such as pollen, dust mites or animal dander to which an exaggerated immune response is made'),
              ('autoimmunity', 'an immune attack on the body\'s own cells, as in rheumatoid arthritis'),
              ('primary lymphoid organs', 'the bone marrow and thymus, where immature lymphocytes differentiate into antigen-sensitive lymphocytes')],
    'groups': [('a physical barrier of innate immunity', ['skin', 'mucus coating of the respiratory tract']), ('a physiological barrier of innate immunity', ['acid in the stomach', 'saliva in the mouth', 'tears from eyes']),
               ('a cellular barrier of innate immunity', ['neutrophils (PMNL)', 'monocytes', 'natural killer cells', 'macrophages']), ('a cytokine barrier', ['interferons'])],
    'groups2': [('a primary lymphoid organ', ['bone marrow', 'thymus']), ('a secondary lymphoid organ', ['spleen', 'lymph nodes', 'tonsils', "Peyer's patches", 'appendix']),
                ('a cell of acquired immunity', ['B lymphocytes', 'helper T cells', 'memory B cells'])],
    'tf': (['Each antibody molecule has four peptide chains, two heavy and two light.', 'The secondary immune response is more intense than the primary response.', 'Antihistamines, adrenaline and steroids reduce symptoms of allergy.',
            'MALT constitutes about 50% of the lymphoid tissue in the human body.', 'Interferons are secreted by virus-infected cells and protect non-infected cells.'],
           [('The primary immune response is more intense than the secondary.', 'The secondary (anamnestic) response is much more intense due to memory cells.'),
            ('T lymphocytes produce antibodies.', 'B lymphocytes produce antibodies; T cells help B cells and mediate cell-mediated immunity.'),
            ('In passive immunity the body makes its own antibodies.', 'In passive immunity ready-made antibodies are given.'),
            ('Allergies are caused by IgG antibodies.', 'Allergy involves IgE antibodies and release of histamine and serotonin from mast cells.'),
            ('The thymus enlarges with age.', 'The thymus is large at birth and keeps reducing in size with age.')]),
    'ar': [('Colostrum gives passive immunity to the infant.', 'Colostrum contains abundant IgA antibodies.', 'a', 'Ready-made antibodies.'),
           ('Organ transplants need tissue and blood group matching.', 'The body can distinguish self from non-self and cell-mediated immunity rejects grafts.', 'a', 'Graft rejection.'),
           ('A booster dose of vaccine gives quicker protection.', 'Memory B and T cells produced in the primary response respond rapidly.', 'a', 'Anamnestic response.'),
           ('Allergy is caused by IgA antibodies.', 'In allergy, mast cells release histamine and serotonin.', 'd', 'IgE is involved; the reason is true.')],
    'features': {'intro': 'A type of immunity has these features:', 'q': 'Which type of immunity is it', 'what': 'immunity', 'compare': True,
                 'items': [('active immunity', ['body produces its own antibodies', 'slow to develop', 'long lasting', 'by infection or vaccination']),
                           ('passive immunity', ['ready-made antibodies are given', 'immediate protection', 'short lived', 'e.g. colostrum, antitoxins, IgG across placenta'])]},
    'fams': [F('C3', 'D3', 'mcq', immunity4), F('C2', 'D2', 'mcq', immunity4)],
    'qa': [('C4', 'D4', 'explain', 'Draw a labelled diagram of an antibody molecule.',
            'A Y-shaped molecule with two identical heavy chains and two identical light chains (H₂L₂) held by disulphide bonds; the tips of the arms carry antigen-binding sites.',
            '1 mark structure; 1 mark labels (heavy chain, light chain, antigen-binding site).'),
           ('C4', 'D5', 'long', 'What is innate immunity? Describe the four types of barriers involved. How is acquired immunity different?',
            'Non-specific defence present at birth. Physical barriers: skin, mucus of respiratory, gastrointestinal and urogenital tracts. Physiological: stomach acid, saliva, tears. Cellular: PMNL-neutrophils, monocytes, NK cells, macrophages that phagocytose microbes. Cytokine: interferons from virus-infected cells. Acquired immunity is pathogen-specific, has memory, and gives primary and secondary (anamnestic) responses via B and T lymphocytes.',
            '1 mark definition; 3 marks barriers; 1 mark acquired immunity.'),
           ('C4', 'D3', 'case', 'Meenal sneezes and gets watery eyes every spring when Parthenium pollen is in the air near her home in Pune.\n(i) What is this response called, and which antibody is involved? (1 mark)\n(ii) Which chemicals from mast cells cause the symptoms? (1 mark)\n(iii) Suggest two ways to manage the condition. (2 marks)',
            '(i) Allergy; IgE. (ii) Histamine and serotonin. (iii) Avoid exposure to the allergen (masks, stay indoors), use antihistamines, adrenaline or steroids as prescribed; identify allergen by skin tests.',
            '(i) 1 (ii) 1 (iii) 2.', ('case',))],
}

CH7S3 = {
    'topic': 'AIDS and cancer',
    'terms': [('AIDS', 'acquired immuno deficiency syndrome, a deficiency of the immune system caused by HIV'),
              ('a retrovirus', 'a virus with an RNA genome that makes DNA using reverse transcriptase, such as HIV'),
              ('ELISA', 'enzyme-linked immunosorbent assay, a widely used diagnostic test for AIDS'),
              ('contact inhibition', 'the property by which contact with other cells inhibits uncontrolled growth of normal cells'),
              ('metastasis', 'the spread of cancer cells to distant sites through blood, forming new tumours'),
              ('proto-oncogenes', 'genes in normal cells that, when activated under certain conditions, lead to oncogenic transformation'),
              ('a benign tumour', 'a tumour that remains confined to its original location and does not spread')],
    'groups': [('a method of cancer detection', ['biopsy and histopathology', 'MRI', 'CT scan', 'radiography (X-rays)']), ('a method of cancer treatment', ['surgery', 'radiation therapy', 'chemotherapy', 'immunotherapy with α-interferon']),
               ('a carcinogen', ['X-rays and gamma rays', 'UV rays', 'tobacco smoke', 'oncogenic viruses'])],
    'tf': (['HIV is a retrovirus with an RNA genome.', 'Macrophages act as an HIV factory.', 'HIV attacks helper T lymphocytes (TH cells).',
            'Malignant tumours show metastasis.', 'Biological response modifiers such as α-interferon activate the immune system against tumours.', 'There is always a time lag between HIV infection and appearance of AIDS symptoms.'],
           [('AIDS can spread by shaking hands with an infected person.', 'HIV spreads by sexual contact, transfusion of contaminated blood, sharing needles and from mother to child through the placenta.'),
            ('HIV attacks B lymphocytes.', 'HIV attacks helper T lymphocytes, whose number decreases progressively.'),
            ('Benign tumours spread to other parts by metastasis.', 'Benign tumours stay confined; malignant tumours metastasise.'),
            ('Cancer cells show contact inhibition.', 'Cancer cells lose contact inhibition and divide uncontrollably.'),
            ('AIDS is curable with antiretroviral drugs.', 'Antiretroviral drugs only prolong life; AIDS is not curable.')]),
    'orders': [('sequence of events after HIV infection', ['virus enters macrophages', 'viral RNA copied into DNA by reverse transcriptase', 'viral DNA incorporated into host DNA', 'new viruses produced', 'helper T cells attacked', 'immune deficiency'], 'Macrophages act as the HIV factory.', '→')],
    'ar': [('AIDS patients suffer from many infections.', 'HIV progressively reduces the number of helper T lymphocytes.', 'a', 'Immune deficiency.'),
           ('Cancer cells form tumours.', 'Cancer cells have lost the property of contact inhibition.', 'a', 'Uncontrolled division.'),
           ('Smoking increases the risk of lung cancer.', 'Tobacco smoke contains chemical carcinogens.', 'a', 'Carcinogens cause oncogenic transformation.'),
           ('Malignant tumours remain confined to their site.', 'Malignant tumours invade and damage surrounding tissues.', 'd', 'Malignant tumours spread by metastasis; the reason is true.')],
    'features': {'intro': 'A tumour shows these features:', 'q': 'Which type of tumour is it', 'what': 'tumour', 'compare': True, 'long': False,
                 'items': [('a benign tumour', ['confined to original location', 'does not spread', 'causes little damage', 'cells may be enclosed in a capsule']),
                           ('a malignant tumour', ['mass of proliferating neoplastic cells', 'invades and damages surrounding tissue', 'spreads by metastasis', 'cells starve normal cells of nutrients'])]},
    'qa': [('C4', 'D5', 'long', 'Describe how HIV infects the human body and causes AIDS. How is AIDS diagnosed, and how can its spread be prevented?',
            'HIV enters macrophages, where its RNA genome is copied into viral DNA by reverse transcriptase; viral DNA joins the host DNA and directs production of virus particles (macrophages act as HIV factory). HIV enters helper T cells, replicates and destroys them, so TH cell count falls and the person suffers infections (Mycobacterium, viruses, fungi, Toxoplasma). Diagnosis: ELISA. Prevention: screening blood, disposable needles, condoms, awareness, NACO and NGOs.',
            '2 marks infection; 1 mark consequences; 1 mark diagnosis; 1 mark prevention.'),
           ('C4', 'D4', 'explain', 'How do normal cells differ from cancer cells? Name two causes of cancer.',
            'Normal cells show contact inhibition and controlled division; cancer cells lose contact inhibition, divide uncontrollably and may metastasise. Causes: physical carcinogens (X-rays, UV), chemical carcinogens (tobacco smoke), biological (oncogenic viruses, activated proto-oncogenes).',
            '1 mark difference; 1 mark causes.'),
           ('C4', 'D3', 'case', 'At a blood bank in Lucknow, every unit of donated blood is tested before use.\n(i) Name one virus the blood is tested for and the test used. (1 mark)\n(ii) Which cells does this virus mainly destroy? (1 mark)\n(iii) Why does a person infected with this virus often die of other infections? Give two other ways the virus spreads. (2 marks)',
            '(i) HIV; ELISA. (ii) Helper T lymphocytes. (iii) Falling TH cells weaken immunity so opportunistic infections take hold; spreads through sharing needles, unprotected sex and from mother to child.',
            '(i) 1 (ii) 1 (iii) 2.', ('case',))],
}

CH7S4 = {
    'topic': 'drugs and alcohol abuse',
    'terms': [('opioids', 'drugs that bind to specific opioid receptors in the CNS and gastrointestinal tract'),
              ('cannabinoids', 'chemicals that interact with cannabinoid receptors present mainly in the brain'),
              ('addiction', 'a psychological attachment to certain effects such as euphoria and a temporary feeling of well-being from drugs and alcohol'),
              ('withdrawal syndrome', 'the characteristic and unpleasant symptoms when regular dose of drugs or alcohol is abruptly stopped'),
              ('dependence', 'the tendency of the body to manifest withdrawal syndrome if the regular dose is discontinued')],
    'tf': (['Heroin is obtained by acetylation of morphine.', 'Cocaine interferes with the transport of dopamine.', 'Chronic use of alcohol damages the liver (cirrhosis).',
            'Morphine is used as a sedative and painkiller after surgery.', 'Peer pressure and curiosity are common reasons for adolescents to try drugs.'],
           [('Heroin is a stimulant.', 'Heroin is a depressant that slows down body functions.'),
            ('Cannabinoids are obtained from Papaver somniferum.', 'They are obtained from the inflorescences of Cannabis sativa; opioids come from the poppy.'),
            ('Cocaine is obtained from the poppy plant.', 'Cocaine is obtained from the coca plant Erythroxylum coca.'),
            ('Drug abuse does not affect the unborn baby.', 'Use during pregnancy adversely affects the foetus.')]),
    'ar': [('Sharing needles among drug users is very dangerous.', 'It can spread HIV and hepatitis B.', 'a', 'Infections spread through blood.'),
           ('Morphine is used medically after surgery.', 'Morphine is a very effective sedative and painkiller.', 'a', 'Controlled medical use.'),
           ('Heroin is a stimulant drug.', 'Heroin is obtained by acetylation of morphine.', 'd', 'Heroin is a depressant; the reason is true.')],
    'fams': [F('C2', 'D2', 'mcq', drug_src), F('C2', 'D1', 'mcq', drug_cls), F('C3', 'D3', 'mcq', drug_cls)],
    'qa': [('C4', 'D4', 'explain', 'List four warning signs of drug and alcohol abuse among adolescents.',
            'Drop in academic performance, unexplained absence from school, lack of interest in personal hygiene, withdrawal and isolation, depression, fatigue, aggressive behaviour, deteriorating relationships, change in sleeping and eating habits.',
            '½ mark each, up to 2.'),
           ('C4', 'D5', 'long', 'Name the source and effect of opioids, cannabinoids and coca alkaloids. Suggest measures for prevention and control of drug abuse among adolescents.',
            'Opioids (heroin, morphine) from poppy latex; depressants. Cannabinoids from Cannabis sativa inflorescences; affect cardiovascular system. Cocaine from Erythroxylum coca; interferes with dopamine transport, stimulates CNS, euphoria. Prevention: avoid undue peer pressure, education and counselling, seek help from parents and peers, look for danger signs, seek professional and medical help.',
            '3 marks drugs; 2 marks measures.'),
           ('C4', 'D3', 'case', 'Ravi, a Class 11 student, starts skipping classes, stops caring about hygiene and becomes aggressive at home after joining a new group of friends.\n(i) What could these signs indicate? (1 mark)\n(ii) Name one drug that is a depressant and its source. (1 mark)\n(iii) Suggest two steps his parents and teachers can take. (2 marks)',
            '(i) Possible drug or alcohol abuse. (ii) Heroin (from morphine of Papaver somniferum) or morphine. (iii) Avoid undue pressure, talk and counsel him, seek help from peers, parents and professionals (psychologists, de-addiction centres).',
            '(i) 1 (ii) 1 (iii) 2.', ('case',))],
}

# ---------------------------------------------------------------- ch08 microbes in human welfare

PRODUCTS = [('Lactobacillus (lactic acid bacteria)', 'curd', 'converts milk to curd and improves its vitamin B₁₂ content'),
            ('Saccharomyces cerevisiae (baker\'s yeast)', 'bread and ethanol', 'ferments dough and is used to produce alcoholic beverages'),
            ('Propionibacterium sharmanii', 'Swiss cheese', 'produces large amounts of CO₂ that form big holes'),
            ('Aspergillus niger', 'citric acid', 'organic acid producer'),
            ('Acetobacter aceti', 'acetic acid', 'organic acid producer'),
            ('Clostridium butylicum', 'butyric acid', 'organic acid producer'),
            ('Penicillium notatum', 'penicillin', 'the first antibiotic, discovered by Alexander Fleming'),
            ('Streptococcus', 'streptokinase', 'clot buster that removes clots from blood vessels of patients with myocardial infarction'),
            ('Trichoderma polysporum', 'cyclosporin A', 'immunosuppressive agent in organ-transplant patients'),
            ('Monascus purpureus', 'statins', 'blood-cholesterol lowering agents that competitively inhibit cholesterol synthesis')]
microbe_prod = table_mcq([(a, '', b, c) for a, b, c in PRODUCTS], 'Which product is obtained from {a}?', why_fmt='{a} gives {ans}: {why}.')
prod_microbe = table_rev([(a, '', b, c) for a, b, c in PRODUCTS], 'Which microbe is used to produce {ans}?', why_fmt='{a} gives {ans}.')

BIOCON = [('ladybird', 'aphids', 'predatory insect'), ('dragonflies', 'mosquitoes', 'predatory insect'), ('Bacillus thuringiensis', 'butterfly caterpillars', 'bacterial toxin kills larvae'),
          ('Trichoderma', 'several plant fungal pathogens', 'free-living fungus in root ecosystems'), ('Nucleopolyhedrovirus (baculovirus)', 'insects and other arthropods', 'species-specific, narrow-spectrum insecticide')]
biocon = table_mcq([(a, '', b, c) for a, b, c in BIOCON], 'Which pest is controlled by {a} as a biocontrol agent?', why_fmt='{a} controls {ans} ({why}).')

BIOFERT = [('Rhizobium', 'symbiotic nitrogen fixation in root nodules of leguminous plants'), ('Azospirillum', 'free-living nitrogen fixation in soil'),
           ('Azotobacter', 'free-living nitrogen fixation in soil'), ('Glomus (mycorrhiza)', 'absorption of phosphorus from soil'),
           ('Anabaena, Nostoc, Oscillatoria (cyanobacteria)', 'nitrogen fixation in paddy fields and adding organic matter')]
biofert = table_mcq([(a, '', b, '') for a, b in BIOFERT], 'What is the role of {a} as a biofertiliser?', why_fmt='{a}: {ans}.')


def bod(r):
    b1 = r.choice([200, 250, 300, 400, 500, 600])
    b2 = r.choice([10, 20, 25, 30, 40, 50])
    pct = (b1 - b2) / b1 * 100
    who = name(r)
    return {'stem': f'At a sewage treatment plant near Nagpur, {who} finds that the BOD of the primary effluent is {b1} mg L⁻¹ and that of the water leaving the aeration tank is {b2} mg L⁻¹. Calculate the percentage reduction in BOD. What does this reduction indicate?',
            'answer': f'{num(pct, 1)}% reduction; most organic matter has been consumed by microbes',
            'key': f'Reduction = ({b1} − {b2})/{b1} × 100 = {num(pct, 1)}% (1); BOD measures the oxygen needed by microbes to oxidise organic matter, so a lower BOD means less organic matter / pollution potential (1).',
            'distractors': [f'{num(b2 / b1 * 100, 1)}% reduction; most organic matter has been consumed by microbes', f'{num(pct, 1)}% reduction; more organic matter has been added', f'{num(pct, 1)}% reduction; dissolved oxygen in the water has decreased']}


CH8S1 = {
    'topic': 'microbes in household and industrial products',
    'terms': [('fermentation', 'the anaerobic breakdown of sugars by microbes such as yeast to produce alcohol and CO₂'),
              ('antibiotics', 'chemical substances produced by some microbes that can kill or retard the growth of other disease-causing microbes'),
              ('a clot buster', 'an enzyme such as streptokinase used to remove clots from blood vessels'),
              ('a starter (inoculum)', 'a small amount of curd added to fresh milk, which contains millions of LAB'),
              ('distillation', 'the process used to produce hard liquors such as whisky, brandy and rum from fermented broth'),
              ('pectinases and proteases', 'enzymes used to clarify bottled fruit juices')],
    'groups': [('a beverage made without distillation', ['wine', 'beer']), ('a beverage made with distillation', ['whisky', 'brandy', 'rum']),
               ('an enzyme produced using microbes', ['lipases', 'pectinases', 'proteases', 'streptokinase'])],
    'tf': (['LAB increase the vitamin B₁₂ content of curd.', 'The large holes in Swiss cheese are due to CO₂ produced by Propionibacterium sharmanii.', 'Penicillin was discovered by Alexander Fleming.',
            'Lipases are used in detergent formulations to remove oily stains.', 'Statins competitively inhibit the enzyme responsible for cholesterol synthesis.', 'Toddy is made by fermenting sap from palms.'],
           [('Roquefort cheese is ripened by bacteria.', 'Roquefort cheese is ripened by growing specific fungi.'),
            ('Cyclosporin A is used as a clot buster.', 'Cyclosporin A is an immunosuppressive agent; streptokinase is the clot buster.'),
            ('Wine and beer are produced with distillation.', 'Wine and beer are made without distillation; whisky, brandy and rum need distillation.'),
            ('Citric acid is produced by Acetobacter aceti.', 'Citric acid comes from Aspergillus niger; Acetobacter aceti makes acetic acid.')]),
    'ar': [('Dough used for idli and dosa becomes puffed up.', 'CO₂ is produced during fermentation by bacteria.', 'a', 'Gas makes the batter rise.'),
           ('Curd is more nutritious than milk.', 'LAB increase vitamin B₁₂ content of curd.', 'a', 'Also check pathogens in the stomach.'),
           ('Penicillin was used extensively to treat soldiers in World War II.', 'Penicillin is an antibiotic that kills bacteria.', 'a', 'Treated infected wounds.')],
    'fams': [F('C2', 'D2', 'mcq', microbe_prod), F('C3', 'D3', 'mcq', prod_microbe), F('C2', 'D1', 'mcq', prod_microbe)],
    'qa': [('C4', 'D4', 'explain', 'How did Alexander Fleming discover penicillin? Who established its full potential as an antibiotic?',
            'While working on Staphylococci, Fleming observed a mould growing on an unwashed culture plate around which Staphylococci could not grow; the chemical was named penicillin after the mould Penicillium notatum. Its full potential was established later by Ernest Chain and Howard Florey.',
            '1 mark discovery; 1 mark Chain and Florey.'),
           ('C4', 'D3', 'case', 'Gauri\'s grandmother in Indore adds a spoonful of curd to warm milk and leaves it overnight.\n(i) Which microbes convert milk into curd? (1 mark)\n(ii) What does the added curd act as? (1 mark)\n(iii) Give two ways in which these microbes are beneficial to humans. (2 marks)',
            '(i) Lactic acid bacteria (Lactobacillus). (ii) Starter or inoculum containing millions of LAB. (iii) They improve nutritional quality by increasing vitamin B₁₂, and in the stomach they check disease-causing microbes.',
            '(i) 1 (ii) 1 (iii) 2.', ('case',)),
           ('C4', 'D5', 'long', 'Name the microbes used to produce the following and give one use of each product: (i) citric acid, (ii) streptokinase, (iii) cyclosporin A, (iv) statins, (v) ethanol.',
            '(i) Aspergillus niger – food and drinks acidulant. (ii) Streptococcus – clot buster for heart-attack patients. (iii) Trichoderma polysporum – immunosuppressant in organ transplants. (iv) Monascus purpureus – lowers blood cholesterol. (v) Saccharomyces cerevisiae – beverages and industrial alcohol.',
            '1 mark each.')],
}

CH8S2 = {
    'topic': 'microbes in sewage treatment and biogas production',
    'terms': [('sewage', 'the municipal waste-water generated every day in cities and towns, containing large amounts of organic matter and microbes'),
              ('BOD', 'biochemical oxygen demand, the amount of oxygen consumed if all the organic matter in one litre of water were oxidised by bacteria'),
              ('flocs', 'masses of bacteria associated with fungal filaments forming mesh-like structures in the aeration tank'),
              ('activated sludge', 'the sediment of bacterial flocs in the settling tank, part of which is pumped back into the aeration tank as inoculum'),
              ('biogas', 'a mixture of gases, predominantly methane, produced by microbial activity and used as fuel'),
              ('methanogens', 'anaerobic bacteria such as Methanobacterium that produce large amounts of methane from cellulosic material')],
    'tf': (['Primary treatment involves physical removal of particles by filtration and sedimentation.', 'The greater the BOD of waste water, the greater is its polluting potential.', 'Methanobacterium is commonly found in the rumen of cattle.',
            'Cattle dung (gobar) is rich in methanogens.', 'Biogas plant technology in India was developed mainly by IARI and KVIC.', 'The Ganga Action Plan and Yamuna Action Plan were initiated by the Ministry of Environment and Forests.'],
           [('Secondary treatment is a purely physical process.', 'Secondary treatment is biological: aerobic microbes in flocs consume organic matter.'),
            ('Low BOD indicates highly polluted water.', 'High BOD indicates high organic matter and polluting potential.'),
            ('Biogas is mainly carbon dioxide.', 'Biogas is predominantly methane, with CO₂ and H₂.'),
            ('Anaerobic sludge digesters use aerobic bacteria.', 'They use anaerobic bacteria that digest bacteria and fungi in the sludge, producing biogas.')]),
    'orders': [('sequence of sewage treatment', ['filtration and sedimentation (primary)', 'aeration with flocs (secondary)', 'settling tank (activated sludge)', 'anaerobic sludge digester', 'effluent released into water bodies'], 'Primary physical treatment, then biological treatment and sludge digestion.', '→')],
    'ar': [('The effluent from secondary treatment is released into rivers.', 'BOD of the effluent is significantly reduced.', 'a', 'Most organic matter is consumed.'),
           ('Cattle dung is used for biogas production.', 'Cattle dung is rich in methanogenic bacteria.', 'a', 'Methanobacterium in the rumen.'),
           ('Biogas spent slurry can be used as fertiliser.', 'Biogas is predominantly methane.', 'b', 'Both are true, but the composition of biogas does not explain the use of the slurry.')],
    'features': {'intro': 'A stage of sewage treatment has these features:', 'q': 'Which stage is it', 'what': 'stage', 'compare': True,
                 'items': [('primary treatment', ['physical removal of particles', 'filtration and sedimentation', 'grit (soil and pebbles) removed', 'primary sludge settles']),
                           ('secondary treatment', ['biological treatment', 'large aeration tanks', 'flocs of bacteria and fungi', 'BOD reduced significantly']),
                           ('anaerobic sludge digestion', ['part of activated sludge pumped into digesters', 'anaerobic bacteria act', 'bacteria and fungi in sludge are digested', 'methane, H₂S and CO₂ formed'])]},
    'fams': [F('C4', 'D4', 'numerical', bod, marks=2), F('C3', 'D3', 'numerical', bod)],
    'qa': [('C4', 'D5', 'long', 'Describe the role of microbes in the secondary treatment of sewage. How is biogas produced in a biogas plant?',
            'Primary effluent is passed into aeration tanks; vigorous mechanical agitation pumps in air, allowing aerobic microbes to form flocs which consume organic matter and reduce BOD. Effluent then goes to a settling tank where flocs sediment (activated sludge); part is used as inoculum and the rest is pumped to anaerobic sludge digesters, where anaerobic bacteria digest it and produce methane, H₂S and CO₂ (biogas). In a biogas plant, slurry of cattle dung is fed into a concrete tank 10–15 feet deep; methanogens produce biogas collected in a floating cover; the gas is supplied for cooking and lighting; spent slurry is used as fertiliser.',
            '3 marks sewage; 2 marks biogas plant.'),
           ('C4', 'D3', 'case', 'A village near Anand installs a biogas plant using cattle dung.\n(i) Which group of bacteria produces the gas? (1 mark)\n(ii) Name the main gas produced. (1 mark)\n(iii) Give two advantages of the plant to the village. (2 marks)',
            '(i) Methanogens (e.g. Methanobacterium). (ii) Methane. (iii) Cheap fuel for cooking and lighting; spent slurry is a good fertiliser; less use of firewood, cleaner surroundings.',
            '(i) 1 (ii) 1 (iii) 2.', ('case',))],
}

CH8S3 = {
    'topic': 'microbes as biocontrol agents and biofertilisers',
    'terms': [('biocontrol', 'the use of biological methods for controlling plant diseases and pests'),
              ('biofertilisers', 'organisms that enrich the nutrient quality of the soil'),
              ('mycorrhiza', 'a symbiotic association of fungi with plant roots'),
              ('Bt', 'Bacillus thuringiensis, a bacterium whose spores are sprayed to kill butterfly caterpillars'),
              ('integrated pest management (IPM)', 'an approach that uses biocontrol and other methods to reduce dependence on toxic chemical pesticides')],
    'tf': (['Mycorrhizal fungi such as Glomus absorb phosphorus from soil.', 'Cyanobacteria are important biofertilisers in paddy fields.', 'Baculoviruses are species-specific, narrow-spectrum insecticides.',
            'Bt toxin is released in the gut of the larvae and kills them.', 'Trichoderma species are effective biocontrol agents of several plant pathogens.'],
           [('Rhizobium fixes nitrogen as a free-living bacterium in soil.', 'Rhizobium fixes nitrogen symbiotically in root nodules of legumes; Azotobacter and Azospirillum are free-living.'),
            ('Baculoviruses are broad-spectrum insecticides that also kill beneficial insects.', 'They are species-specific and narrow-spectrum with no negative impact on non-target organisms.'),
            ('Chemical pesticides kill only harmful insects.', 'They kill both useful and harmful organisms indiscriminately.'),
            ('Ladybirds are used to control mosquitoes.', 'Ladybirds control aphids; dragonflies control mosquitoes.')]),
    'ar': [('Baculoviruses are desirable in IPM programmes.', 'They are species-specific and do not harm non-target insects.', 'a', 'Protects beneficial insects.'),
           ('Mycorrhizal plants show resistance to root-borne pathogens.', 'The fungus also absorbs phosphorus from soil for the plant.', 'b', 'Both are true, but phosphorus uptake is not the explanation of disease resistance.'),
           ('Organic farmers prefer biocontrol.', 'Chemical pesticides are toxic and harm useful organisms.', 'a', 'Biocontrol is eco-friendly.')],
    'fams': [F('C2', 'D2', 'mcq', biocon), F('C2', 'D1', 'mcq', biofert), F('C3', 'D3', 'mcq', biofert), F('C3', 'D3', 'mcq', biocon)],
    'qa': [('C4', 'D4', 'explain', 'Name two free-living and one symbiotic nitrogen-fixing bacteria, and one fungus that acts as a biofertiliser.',
            'Free-living: Azotobacter, Azospirillum (also cyanobacteria like Anabaena, Nostoc). Symbiotic: Rhizobium in legume root nodules. Fungus: Glomus (mycorrhiza), which absorbs phosphorus.',
            '1 mark bacteria; 1 mark fungus.'),
           ('C4', 'D3', 'case', 'An organic farmer near Nashik does not use chemical pesticides on his vegetables. He releases ladybirds and sprays a bacterial powder on his cabbage.\n(i) Which pest do ladybirds control? (1 mark)\n(ii) Name the bacterium likely used and how it kills caterpillars. (2 marks)\n(iii) Give one advantage of biocontrol over chemical pesticides. (1 mark)',
            '(i) Aphids. (ii) Bacillus thuringiensis; its spores are sprayed, eaten by larvae, and the toxin released in the gut kills them. (iii) It does not harm useful organisms or pollute the environment; reduces chemical residues in food.',
            '(i) 1 (ii) 2 (iii) 1.', ('case',)),
           ('C4', 'D5', 'long', 'What are biocontrol agents and biofertilisers? Describe two examples of each and explain why they are preferred over chemicals.',
            'Biocontrol agents control pests biologically: Bacillus thuringiensis kills butterfly caterpillars; Trichoderma controls plant fungal pathogens; baculoviruses (NPV) are narrow-spectrum; ladybirds eat aphids. Biofertilisers enrich soil: Rhizobium (legumes), Azotobacter, Azospirillum, Glomus (phosphorus), cyanobacteria in paddy. They avoid toxic residues, harm to non-target organisms and soil degradation.',
            '2 marks biocontrol; 2 marks biofertilisers; 1 mark advantages.')],
}

SPECS = {'ch05-st1': CH5S1, 'ch05-st2': CH5S2, 'ch05-st3': CH5S3, 'ch05-st4': CH5S4, 'ch05-st5': CH5S5,
         'ch06-st1': CH6S1, 'ch06-st2': CH6S2, 'ch06-st3': CH6S3, 'ch06-st4': CH6S4,
         'ch07-st1': CH7S1, 'ch07-st2': CH7S2, 'ch07-st3': CH7S3, 'ch07-st4': CH7S4,
         'ch08-st1': CH8S1, 'ch08-st2': CH8S2, 'ch08-st3': CH8S3}
FAMILIES = build_all(P, SPECS)
