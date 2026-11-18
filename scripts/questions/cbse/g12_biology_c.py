"""CBSE Class 12 Biology, chapters 9-13: biotechnology principles and processes, biotechnology applications,
organisms and populations, ecosystem, biodiversity and conservation.

Fact tables follow NCERT (2023-24 rationalised text). Restriction fragment counts, PCR copies, population rates and
growth, productivity, 10% law transfers and species-area values are computed here.
"""
from __future__ import annotations

import math

from qbank import F, CITIES, GIRLS, mcq, name, num
from g11_chemistry_kit import build_all, sf, sci, cap
from g12_biology_a import table_mcq, table_rev, table_explain

P = 'cbse-g12-biology'

COMP = {'A': 'T', 'T': 'A', 'G': 'C', 'C': 'G'}


def revcomp(s: str) -> str:
    return ''.join(COMP[c] for c in reversed(s))


# ---------------------------------------------------------------- ch09 biotechnology: principles and processes

def fragments(r):
    n = r.randint(1, 6)
    shape = r.choice(['linear', 'circular'])
    enz = r.choice(['EcoRI', 'BamHI', 'HindIII', 'PstI', 'SalI'])
    what = {'linear': 'a linear DNA molecule', 'circular': 'a circular plasmid'}[shape]
    good = n + 1 if shape == 'linear' else n
    wrong = [n + 1 if shape == 'circular' else n, 2 * n, n - 1 if n > 1 else n + 2, n + 2]
    wrong = [w for w in dict.fromkeys(wrong) if w != good and w > 0][:3]
    why = (f'Cutting a linear molecule at {n} site(s) gives {n} + 1 = {good} fragments.' if shape == 'linear'
           else f'A circular molecule cut at {n} site(s) gives {n} fragment(s), as there are no free ends.')
    return mcq(f'{what[0].upper() + what[1:]} has {n} recognition site{"s" if n > 1 else ""} for {enz}. How many DNA fragments are obtained on complete digestion with {enz}?',
               f'{good}', [f'{w}' for w in wrong], why, r)


def pcr(r):
    n0 = r.choice([1, 2, 5, 10, 100])
    c = r.choice([5, 8, 10, 15, 20, 25, 30])
    tot = n0 * 2 ** c
    who = name(r)
    fmt = lambda x: num(x) if x < 1e7 else sci(x, 3)
    tot_s = fmt(tot)
    return {'stem': f'In a laboratory in {r.choice(CITIES)}, {who} starts a PCR with {n0} {"copy" if n0 == 1 else "copies"} of a double-stranded DNA template. Assuming 100% efficiency, how many copies of the DNA will be present after {c} cycles?',
            'answer': f'{tot_s} copies',
            'key': f'Each cycle (denaturation, annealing, extension) doubles the DNA (1): copies = {n0} × 2^{c} = {tot_s} (1).',
            'distractors': [f'{fmt(n0 * 2 * c)} copies', f'{fmt(n0 * c ** 2)} copies', f'{fmt(n0 * 2 ** (c - 1))} copies']}


def pcr_cycles(r):
    c = r.choice([3, 4, 5, 6, 7, 8, 10])
    tot = 2 ** c
    good = f'{c} cycles'
    return mcq(f'Starting with one DNA molecule, how many PCR cycles are needed to obtain {tot} copies (100% efficiency)?', good,
               [f'{c + 1} cycles', f'{c - 1} cycles', f'{tot} cycles'], f'Copies = 2ⁿ; 2^{c} = {tot}, so n = {c}.', r)


def site_freq(r):
    k = r.choice([4, 6, 8])
    L = r.choice([1e4, 5e4, 1e5, 1e6, 4.6e6])
    f = 4 ** k
    exp = L / f
    Ls = num(L) if L < 1e6 else f'{sf(L / 1e6, 2)} million'
    return {'stem': f'A restriction enzyme recognises a specific {k}-bp palindromic sequence. Assuming all four bases occur equally and randomly, how many times would this site be expected to occur in a DNA of {Ls} bp?',
            'answer': f'about {num(exp, 1) if exp < 10 else num(round(exp))} times',
            'key': f'Probability of a given {k}-bp sequence = (1/4)^{k} = 1/{f} (1); expected sites = {Ls} / {f} ≈ {num(exp, 1) if exp < 10 else num(round(exp))} (1).',
            'distractors': [f'about {num(L / 4 ** (k - 1), 0)} times', f'about {num(L / (4 * k), 0)} times', f'about {num(L / (2 * k), 0)} times']}


def palindrome(r):
    for _ in range(50):
        half = ''.join(r.choice('ATGC') for _ in range(3))
        good = half + revcomp(half)
        wrong = []
        while len(wrong) < 3:
            w = ''.join(r.choice('ATGC') for _ in range(6))
            if w != revcomp(w) and w not in wrong:
                wrong.append(w)
        # include the classic mistake: a mirror-image (same strand reversed) sequence
        mirror = half + half[::-1]
        if mirror != revcomp(mirror) and mirror not in wrong:
            wrong[0] = mirror
        return mcq('Which of the following sequences (5′ → 3′ on one strand) is a palindrome that could be a restriction enzyme recognition site?',
                   f'5′-{good}-3′', [f'5′-{w}-3′' for w in wrong],
                   f'5′-{good}-3′ is a palindrome: its complementary strand, read 5′ → 3′, is also {revcomp(good)}. The other sequences do not read the same on both strands.', r)
    raise ValueError('no palindrome')


ECO = [('E', 'the genus Escherichia'), ('co', 'the species coli'), ('R', 'the strain RY13'), ('I', 'the order in which the enzyme was isolated from that strain')]
eco_letter = table_mcq([(a, '', b, '') for a, b in ECO], 'In the name of the restriction enzyme EcoRI, what does "{a}" stand for?',
                       why_fmt='In EcoRI, E = Escherichia, co = coli, R = strain RY13, I = first enzyme isolated from it; here: {ans}.')

TOOLS = [('restriction endonuclease', 'cuts DNA at specific positions within it', 'molecular scissors; recognise palindromic sequences'),
         ('exonuclease', 'removes nucleotides from the ends of DNA', 'acts at the ends, not within the DNA'),
         ('DNA ligase', 'joins DNA fragments', 'molecular glue sealing sticky ends'),
         ('Taq polymerase', 'synthesises DNA at high temperature during PCR', 'thermostable, from Thermus aquaticus'),
         ('the ori site', 'starts replication and controls the copy number of the plasmid', 'any DNA linked to it can replicate'),
         ('the rop gene in pBR322', 'codes for proteins involved in plasmid replication', 'part of pBR322'),
         ('a selectable marker', 'helps identify and eliminate non-transformants', 'e.g. genes for resistance to ampicillin'),
         ('lysozyme', 'breaks the bacterial cell wall to release DNA', 'used to isolate DNA from bacteria')]
tool_role = table_mcq([(a, '', b, c) for a, b, c in TOOLS], 'What is the role of {a} in recombinant DNA technology?', why_fmt='{a}: {ans} ({why}).')
tool_rev = table_rev([(a, '', b, c) for a, b, c in TOOLS], 'Which tool or component of rDNA technology {ans}?', why_fmt='{a} {ans}.')

LYSE = [('bacterial cells', 'lysozyme'), ('plant cells', 'cellulase'), ('fungal cells', 'chitinase')]
lyse = table_mcq([(a, '', b, '') for a, b in LYSE], 'Which enzyme is used to break open {a} to isolate DNA?',
                 why_fmt='Lysozyme for bacteria, cellulase for plant cells, chitinase for fungi: {ans}.',
                 pool=['lysozyme', 'cellulase', 'chitinase', 'ribonuclease', 'protease'])


def ins_inact(r):
    site, gene, other = r.choice([('BamHI', 'tetracycline', 'ampicillin'), ('PstI', 'ampicillin', 'tetracycline'), ('PvuI', 'ampicillin', 'tetracycline'), ('SalI', 'tetracycline', 'ampicillin')])
    good = f'grow on {other} but not on {gene}'
    wrong = [f'grow on {gene} but not on {other}', 'grow on both antibiotics', 'grow on neither antibiotic']
    return mcq(f'A foreign gene is ligated into the {site} site of pBR322, which lies in the {gene} resistance gene. On which media will E. coli cells carrying the recombinant plasmid grow?',
               good, wrong, f'Insertion at {site} inactivates the {gene} resistance gene (insertional inactivation); the {other} resistance gene is still intact.', r)


def gel(r):
    sizes = r.sample([150, 300, 500, 800, 1200, 2000, 3500, 5000], 4)
    far = r.choice(['farthest', 'least'])
    good = min(sizes) if far == 'farthest' else max(sizes)
    return mcq(f'Four DNA fragments of {", ".join(str(s) for s in sizes)} bp are separated by agarose gel electrophoresis. Which fragment moves {"farthest from the well" if far == "farthest" else "the least distance from the well"}?',
               f'{good} bp', [f'{s} bp' for s in sizes if s != good],
               'DNA is negatively charged and moves to the anode; the agarose matrix sieves the fragments, so smaller fragments move farther.', r)


CH9S1 = {
    'topic': 'principles of biotechnology and recombinant DNA',
    'terms': [('biotechnology', 'the use of live organisms or enzymes from organisms to produce products and processes useful to humans (EFB definition integrates natural science and organisms, cells, parts thereof and molecular analogues)'),
              ('genetic engineering', 'the technique of altering the chemistry of genetic material (DNA and RNA), introducing it into host organisms and changing their phenotype'),
              ('a plasmid', 'an autonomously replicating circular extra-chromosomal DNA in bacteria'),
              ('recombinant DNA', 'DNA formed by joining a piece of foreign DNA to a vector DNA'),
              ('cloning', 'making multiple identical copies of any template DNA'),
              ('a vector', 'a DNA molecule, such as a plasmid, that carries foreign DNA into the host and replicates in it')],
    'tf': (['The first recombinant DNA was made by Stanley Cohen and Herbert Boyer in 1972.', 'Biotechnology deals with large-scale production and marketing of products using live organisms or their enzymes.',
            'The antibiotic resistance gene from Salmonella typhimurium was linked to a native plasmid of E. coli in the first rDNA experiment.', 'Restriction enzymes and DNA ligase are the basic tools of rDNA technology.'],
           [('The first recombinant DNA was made in 1953.', 'It was made in 1972 by Cohen and Boyer; 1953 is the year of the Watson–Crick model.'),
            ('A plasmid is chromosomal DNA of bacteria.', 'A plasmid is extra-chromosomal and replicates autonomously.'),
            ('DNA ligase cuts DNA at specific sites.', 'Restriction enzymes cut DNA; ligase joins the fragments.')]),
    'orders': [('basic steps in creating a genetically modified organism', ['identify DNA with desirable genes', 'introduce the identified DNA into the host', 'maintain the introduced DNA in the host and transfer to progeny'], 'These are the three basic steps.', '→')],
    'ar': [('A piece of foreign DNA introduced alone into a host usually cannot multiply.', 'It must be linked to an origin of replication to replicate in the host.', 'a', 'The vector provides the ori.'),
           ('Restriction enzymes are called molecular scissors.', 'They cut DNA at specific recognition sequences.', 'a', 'They cut at specific sites.'),
           ('Recombinant DNA technology was first achieved in 1972.', 'DNA ligase was discovered only after 1990.', 'c', 'Cohen and Boyer used DNA ligase in 1972; the reason is false.'),
           ('Plasmids are used as vectors.', 'Plasmids can replicate autonomously in bacteria.', 'a', 'They carry foreign DNA and multiply.')],
    'fams': [F('C2', 'D2', 'mcq', eco_letter), F('C3', 'D3', 'mcq', palindrome)],
    'qa': [('C3', 'D2', 'explain', 'Name the two core techniques that enabled the birth of modern biotechnology and state what each involves.',
            '(i) Genetic engineering – techniques to alter the chemistry of genetic material and introduce it into host organisms. (ii) Bioprocess engineering – maintenance of sterile (microbial contamination-free) conditions to enable growth of only the desired microbe or eukaryotic cell in large quantities.',
            '1 mark each.'),
           ('C4', 'D4', 'explain', 'Why is it necessary to link a foreign DNA to an origin of replication for it to be cloned?',
            'The ori is the sequence from where replication starts; a piece of DNA that is linked to the ori can replicate within the host cell. Without it, the foreign DNA cannot multiply in the host and is not cloned.',
            '1 mark role of ori; 1 mark consequence.'),
           ('C4', 'D3', 'case', 'In 1972 Cohen and Boyer cut a piece of DNA carrying an antibiotic resistance gene from a plasmid of Salmonella typhimurium and joined it to a plasmid of E. coli.\n(i) Which enzyme was used to cut the DNA? (1 mark)\n(ii) Which enzyme joined the cut DNA to the plasmid? (1 mark)\n(iii) Why was the plasmid needed, and what happened when it was transferred to E. coli? (2 marks)',
            '(i) A restriction enzyme (molecular scissors). (ii) DNA ligase. (iii) The plasmid acts as a vector with an origin of replication; in E. coli it replicated, making many copies of the antibiotic resistance gene (cloning).',
            '(i) 1 (ii) 1 (iii) 2.', ('case',))],
}

CH9S2 = {
    'topic': 'tools of rDNA technology',
    'terms': [('a restriction endonuclease', 'an enzyme that cuts DNA at a specific position within it after recognising a specific palindromic sequence'),
              ('sticky ends', 'single-stranded overhanging stretches left on DNA cut a little away from the centre of the palindrome'),
              ('a palindromic sequence', 'a sequence of base pairs that reads the same on the two strands when the orientation of reading is kept the same'),
              ('insertional inactivation', 'the inactivation of a gene in a vector when foreign DNA is inserted into it, used to identify recombinants'),
              ('a selectable marker', 'a gene that helps in identifying and eliminating non-transformants and selectively permitting the growth of transformants'),
              ('a competent host', 'a host cell made capable of taking up DNA, for example by treatment with divalent cations such as calcium')],
    'groups': [('a restriction endonuclease', ['EcoRI', 'BamHI', 'HindII', 'PstI', 'SalI']), ('a tool for introducing DNA into a host', ['micro-injection', 'biolistics (gene gun)', 'disarmed retrovirus', 'heat shock with Ca²⁺']),
               ('a feature of a cloning vector', ['origin of replication', 'selectable marker', 'cloning sites'])],
    'tf': (['The first restriction endonuclease to be isolated was HindII.', 'More than 900 restriction enzymes have been isolated from over 230 strains of bacteria.', 'Agrobacterium tumefaciens delivers DNA into dicot plants by its Ti plasmid.',
            'In blue-white selection, recombinant colonies are white.', 'Retroviruses are disarmed before being used as vectors in animal cells.'],
           [('In blue-white selection, recombinant colonies are blue.', 'Insertion inactivates β-galactosidase, so recombinant colonies do not produce colour (white).'),
            ('Restriction enzymes belong to the class ligases.', 'They belong to nucleases (endonucleases cut within DNA).'),
            ('DNA can pass through the cell membrane of bacteria without any treatment.', 'DNA is hydrophilic; cells must be made competent, e.g. with Ca²⁺ and heat shock.'),
            ('A vector should have many recognition sites for the enzyme used.', 'It should have a single (or very few) recognition site, otherwise the vector is cut into several fragments.')]),
    'ar': [('Sticky ends help DNA ligase join fragments.', 'Sticky ends form hydrogen bonds with their complementary cut counterparts.', 'a', 'Same enzyme gives complementary ends.'),
           ('Blue-white selection is preferred over antibiotic replica plating.', 'It needs only a single plating on a chromogenic substrate.', 'a', 'Replica plating on two antibiotics is cumbersome.'),
           ('Ti plasmid of Agrobacterium is used as a cloning vector in plants.', 'The Ti plasmid has been modified so that it is no longer pathogenic but still delivers genes.', 'a', 'Disarmed Ti plasmid.'),
           ('DNA is negatively charged.', 'DNA moves towards the cathode during electrophoresis.', 'c', 'DNA moves towards the anode.')],
    'features': {'intro': 'A part of the plasmid vector pBR322 has this role:', 'q': 'Identify the part', 'what': 'part', 'case': False,
                 'items': [('ori', ['sequence where replication starts', 'controls copy number', 'needed for any linked DNA to replicate', 'present once in the vector']),
                           ('ampR', ['codes for resistance to ampicillin', 'selectable marker', 'contains PstI and PvuI sites', 'inactivated if DNA is inserted at PstI']),
                           ('tetR', ['codes for resistance to tetracycline', 'selectable marker', 'contains the BamHI and SalI sites', 'inactivated if DNA is inserted at BamHI']),
                           ('rop', ['codes for proteins involved in replication of the plasmid', 'not a selectable marker', 'present in pBR322', 'has a PvuII site nearby'])]},
    'fams': [F('C2', 'D2', 'mcq', fragments), F('C3', 'D3', 'mcq', fragments), F('C3', 'D3', 'mcq', ins_inact), F('C4', 'D4', 'numerical', site_freq, marks=2),
             F('C2', 'D2', 'mcq', tool_role), F('C3', 'D2', 'mcq', tool_rev), F('C3', 'D3', 'mcq', palindrome)],
    'qa': [('C4', 'D5', 'long', 'What are the features required to facilitate cloning into a vector? Explain insertional inactivation with an example.',
            'Origin of replication (controls copy number), selectable marker (e.g. ampR, tetR) to identify transformants, and cloning sites (single recognition sites for restriction enzymes). In pBR322, inserting foreign DNA at the BamHI site of tetR makes recombinants tetracycline sensitive but still ampicillin resistant. In blue-white selection, inserting DNA in the lacZ gene (β-galactosidase) prevents blue colour on a chromogenic substrate, so recombinant colonies are white.',
            '1 mark each feature (3); 2 marks insertional inactivation.'),
           ('C4', 'D4', 'explain', 'How is a bacterial cell made competent to take up recombinant DNA?',
            'The cells are treated with a specific concentration of a divalent cation such as calcium, which increases the efficiency of DNA entry through pores in the cell wall; they are then incubated with the rDNA on ice, given a brief heat shock at 42 °C, and put back on ice.',
            '1 mark Ca²⁺; 1 mark heat shock.'),
           ('C4', 'D3', 'case', 'Kavya cuts a 10 kb linear DNA with EcoRI, which has three recognition sites in it, and also cuts a plasmid with one EcoRI site.\n(i) How many fragments does she get from the linear DNA and from the plasmid? (1 mark)\n(ii) What is the recognition sequence of EcoRI? (1 mark)\n(iii) Why are sticky ends formed, and why must the same enzyme cut both DNAs? (2 marks)',
            '(i) Four fragments from the linear DNA; the plasmid opens into one linear piece. (ii) 5′-GAATTC-3′ (cuts between G and A). (iii) EcoRI cuts a little away from the centre of the palindrome on both strands, leaving single-stranded overhangs; the same enzyme gives complementary sticky ends that can pair and be joined by DNA ligase.',
            '(i) 1 (ii) 1 (iii) 2.', ('case',))],
}

CH9S3 = {
    'topic': 'processes of rDNA technology',
    'terms': [('PCR', 'polymerase chain reaction, in which multiple copies of a gene are synthesised in vitro using primers and a thermostable DNA polymerase'),
              ('a primer', 'a small chemically synthesised oligonucleotide complementary to a region of DNA'),
              ('a bioreactor', 'a large vessel in which raw materials are biologically converted into specific products under optimal conditions'),
              ('downstream processing', 'the separation and purification of the product before it is ready for marketing'),
              ('gel electrophoresis', 'a technique in which negatively charged DNA fragments are separated by size by moving them towards the anode through an agarose matrix'),
              ('elution', 'the cutting out and extraction of separated DNA bands from the agarose gel'),
              ('transformation', 'a procedure by which a piece of DNA is introduced into a host bacterium')],
    'tf': (['In PCR, the DNA polymerase used is obtained from Thermus aquaticus.', 'Separated DNA fragments are stained with ethidium bromide and seen as orange bands under UV light.', 'Most commonly used bioreactors are of the stirring type.',
            'Purified DNA is precipitated by adding chilled ethanol.', 'Stirred-tank bioreactors provide better oxygen transfer.'],
           [('In PCR the DNA is denatured at a low temperature.', 'Denaturation is done at high temperature (about 94 °C); Taq polymerase withstands it.'),
            ('Smaller DNA fragments move slower in agarose gel.', 'Smaller fragments move farther; the matrix acts as a sieve.'),
            ('Ethanol precipitates proteins during DNA isolation.', 'Chilled ethanol precipitates the purified DNA as fine threads; proteases remove proteins.'),
            ('Downstream processing is done before fermentation.', 'It is done after the biosynthetic stage to purify the product.')]),
    'orders': [('sequence of steps in a PCR cycle', ['denaturation', 'annealing of primers', 'extension by Taq polymerase'], 'Each cycle doubles the DNA.', '→'),
               ('sequence of steps in rDNA technology', ['isolation of DNA', 'fragmentation by restriction endonuclease', 'isolation of the desired DNA fragment', 'ligation into a vector', 'transfer of rDNA into the host', 'culturing the host and extraction of the product'], 'As described in NCERT.', '→'),
               ('sequence for isolating DNA from a plant cell', ['treat with cellulase', 'remove RNA with ribonuclease', 'remove proteins with protease', 'add chilled ethanol', 'spool the DNA threads'], 'Purified DNA precipitates out.', '→')],
    'ar': [('Taq polymerase is used in PCR.', 'It remains active during the high temperature used to denature DNA.', 'a', 'Thermostable.'),
           ('A stirred-tank bioreactor is better than a shake flask for large-scale culture.', 'It provides better aeration and mixing throughout the culture.', 'a', 'Large volumes, optimal conditions.'),
           ('DNA fragments separate in agarose gel according to size.', 'The agarose gel acts as a molecular sieve.', 'a', 'Smaller fragments move farther.'),
           ('Downstream processing needs no quality control.', 'Products must be formulated with suitable preservatives.', 'd', 'Strict quality control testing is needed, especially for drugs and clinical trials.')],
    'features': {'intro': 'A part of a stirred-tank bioreactor has this function:', 'q': 'Identify the part', 'what': 'part', 'case': False,
                 'items': [('the agitator (stirrer)', ['mixes the contents', 'distributes oxygen evenly', 'motor driven', 'keeps cells in suspension']),
                           ('the sparger', ['bubbles sterile air into the medium', 'improves oxygen transfer', 'near the base', 'part of the aeration system']),
                           ('the foam control system', ['prevents foaming', 'adds antifoam when needed', 'at the top of the vessel', 'protects the vent']),
                           ('the sampling port', ['used to withdraw small volumes', 'checks product formation', 'allows monitoring', 'kept sterile'])]},
    'fams': [F('C3', 'D3', 'numerical', pcr, marks=2), F('C3', 'D2', 'mcq', pcr_cycles), F('C2', 'D2', 'mcq', gel), F('C2', 'D2', 'mcq', lyse)],
    'qa': [('C4', 'D5', 'long', 'Explain the steps of the polymerase chain reaction with a diagram. Why is Taq polymerase used?',
            'PCR amplifies a gene in vitro. (i) Denaturation: double-stranded DNA is heated (~94 °C) to separate strands. (ii) Annealing: two sets of primers bind to complementary regions at a lower temperature. (iii) Extension: Taq polymerase extends the primers using dNTPs, copying the region between them. Repeated cycles amplify the DNA about a billion times (2ⁿ copies). Taq polymerase from Thermus aquaticus is thermostable and remains active through the high temperature of denaturation.',
            '1 mark each step (3); 1 mark diagram; 1 mark Taq.'),
           ('C4', 'D4', 'explain', 'Describe how DNA fragments are separated and visualised by gel electrophoresis.',
            'DNA fragments are loaded into wells of an agarose gel and an electric field is applied; being negatively charged they move towards the anode, smaller fragments moving farther through the sieve-like matrix. The gel is stained with ethidium bromide and exposed to UV light: DNA appears as bright orange bands, which can be cut out and eluted.',
            '1 mark separation; 1 mark visualisation.'),
           ('C4', 'D3', 'case', 'A biotechnology firm in Hyderabad grows recombinant E. coli in a 1000-litre stirred-tank bioreactor to make a protein drug.\n(i) Why is a stirred-tank bioreactor used instead of shake flasks? (1 mark)\n(ii) Name any two conditions the bioreactor must keep optimal. (1 mark)\n(iii) What is downstream processing and why is quality control essential here? (2 marks)',
            '(i) For large volumes (100–1000 L) with even mixing and better oxygen availability. (ii) Temperature, pH, substrate, salts, vitamins, oxygen (any two). (iii) Separation and purification of the product, and formulation with preservatives; a drug must pass strict quality control and clinical trials for safety.',
            '(i) 1 (ii) 1 (iii) 2.', ('case',))],
}


# ---------------------------------------------------------------- ch10 biotechnology and its applications

CRY = [('cryIAc', 'cotton bollworms'), ('cryIIAb', 'cotton bollworms'), ('cryIAb', 'corn borer')]
cry_pest = table_mcq([(a, '', b, '') for a, b in CRY], 'The Bt toxin coded by the gene {a} controls which pest?', why_fmt='{a} controls {ans}.',
                     pool=['cotton bollworms', 'corn borer', 'Meloidogyne incognita (nematode)', 'aphids', 'locusts'])

APPL = [('Bt cotton', 'a cry gene from Bacillus thuringiensis', 'protects the plant against bollworms (lepidopterans)'),
        ('nematode-resistant tobacco', 'RNA interference against Meloidogyne incognita', 'dsRNA silences a specific mRNA of the nematode'),
        ('Humulin (human insulin)', 'chains A and B made separately in E. coli and joined by disulphide bonds', 'made by Eli Lilly in 1983'),
        ('Rosie the cow', 'the human alpha-lactalbumin gene', 'milk with 2.4 g of human protein per litre'),
        ('the first clinical gene therapy (1990)', 'the ADA gene introduced into lymphocytes', 'treated a 4-year-old girl with ADA deficiency'),
        ('Golden rice', 'genes for β-carotene synthesis', 'rice enriched with vitamin A precursor'),
        ('transgenic mice for vaccine safety', 'testing polio vaccine', 'replace monkeys in safety testing')]
appl = table_mcq([(a, '', b, c) for a, b, c in APPL], 'Which of the following was used or introduced to produce {a}?', why_fmt='{a}: {ans} – {why}.')
appl_rev = table_rev([(a, '', b, c) for a, b, c in APPL], 'Which product or achievement is based on {ans}?', why_fmt='{a} is based on {ans}.')


def rosie(r):
    v = r.choice([5, 10, 12, 20, 25, 40, 50])
    g = 2.4 * v
    who = name(r)
    return {'stem': f'Rosie, the first transgenic cow (1997), produced milk containing 2.4 g of human alpha-lactalbumin per litre. {who} calculates the amount of this protein in {v} L of such milk. What is it, and why is this milk better for human babies?',
            'answer': f'{num(g, 1)} g; it is nutritionally a more balanced product for human babies than natural cow milk',
            'key': f'Mass = 2.4 g L⁻¹ × {v} L = {num(g, 1)} g (1); human alpha-lactalbumin makes the milk nutritionally more balanced for human babies (1).',
            'distractors': [f'{num(2.4 / v, 2)} g; it has more lactose', f'{num(g * 10, 1)} g; it is nutritionally more balanced for babies', f'{num(g / 2, 1)} g; it is free of all proteins']}


def insulin_aa(r):
    a, b = 21, 30
    q = r.choice(['total', 'bonds', 'cpep', 'host'])
    if q == 'cpep':
        return mcq('Which part of proinsulin is removed during the maturation of insulin?', 'the C peptide', ['the A chain', 'the B chain', 'the disulphide bridges'],
                   'Proinsulin has an extra stretch, the C peptide, which is removed; the mature hormone has only chains A and B.', r)
    if q == 'host':
        return mcq('In 1983 Eli Lilly produced the A and B chains of human insulin separately by introducing the DNA sequences into plasmids of which organism?', 'Escherichia coli',
                   ['Bacillus thuringiensis', 'Agrobacterium tumefaciens', 'Saccharomyces cerevisiae'], 'The chains were produced in E. coli, extracted and combined by creating disulphide bonds.', r)
    if q == 'total':
        return mcq('Mature human insulin has an A chain of 21 amino acids and a B chain of 30 amino acids. How many amino acids does the mature insulin molecule have?',
                   '51', ['30', '21', '86'], 'Mature insulin = A + B chains = 21 + 30 = 51 amino acids; the C peptide of proinsulin is removed.', r)
    return mcq('In human insulin, how are the A and B polypeptide chains held together?', 'by disulphide bridges', ['by peptide bonds between the chains', 'by the C peptide', 'by hydrogen bonds only'],
               'The two chains are linked by disulphide bridges; the C peptide is removed during maturation of proinsulin.', r)


DIAG = [('ELISA', 'antigen–antibody interaction', 'detects antigens (proteins, glycoproteins) or antibodies made against the pathogen'),
        ('PCR', 'amplification of the nucleic acid of the pathogen', 'detects very low concentrations of a pathogen; used for suspected AIDS and cancer gene mutations'),
        ('a radioactive probe with autoradiography', 'hybridisation of a single-stranded labelled DNA or RNA with its complement', 'a clone with a mutated gene does not appear on the photographic film')]
diag = table_mcq([(a, '', b, c) for a, b, c in DIAG], 'The diagnostic technique {a} is based on which principle?', why_fmt='{a}: {ans} – {why}.',
                 pool=[x[1] for x in DIAG] + ['separation of DNA by size in an electric field', 'staining of bacteria in a smear'])

CH10S1 = {
    'topic': 'applications in agriculture',
    'terms': [('GMOs', 'plants, bacteria, fungi and animals whose genes have been altered by manipulation'),
              ('Bt toxin', 'an insecticidal protein produced by Bacillus thuringiensis that exists as an inactive protoxin and is activated by the alkaline pH of the insect gut'),
              ('RNA interference (RNAi)', 'a cellular defence in all eukaryotes that silences a specific mRNA by a complementary dsRNA'),
              ('a cry gene', 'a gene coding for the Bt toxin protein'),
              ('Agrobacterium vectors', 'vectors used to introduce nematode-specific genes into the host plant')],
    'tf': (['Bt toxin is coded by the cry genes.', 'Bt toxin is inactive inside the bacterium as a protoxin.', 'The alkaline pH of the insect gut solubilises the crystals and activates the toxin.',
            'GM crops have reduced reliance on chemical pesticides.', 'RNAi was used to make tobacco plants resistant to Meloidogyne incognita.'],
           [('Bt toxin kills the bacterium Bacillus thuringiensis itself.', 'The toxin exists as an inactive protoxin in the bacterium, so it does not kill it.'),
            ('Bt toxin is activated by the acidic pH of the insect gut.', 'It is activated by the alkaline pH of the insect gut.'),
            ('In RNAi, a single-stranded DNA silences the mRNA.', 'Complementary dsRNA binds and silences the mRNA.'),
            ('Bt cotton is resistant to all pests.', 'It protects against specific insects such as bollworms (lepidopterans).')]),
    'orders': [('sequence of events in the action of Bt toxin', ['insect eats Bt toxin crystals', 'alkaline gut pH solubilises crystals', 'toxin activated', 'toxin binds midgut epithelial cells and creates pores', 'cells swell and lyse', 'insect dies'], 'Toxin causes lysis of gut cells.', '→')],
    'ar': [('Bt toxin does not kill the Bacillus thuringiensis bacterium.', 'The toxin exists as an inactive protoxin in the bacterium.', 'a', 'Activated only in alkaline insect gut.'),
           ('RNAi-engineered tobacco is protected from the nematode Meloidogyne incognita.', 'The dsRNA silences a specific mRNA of the parasite, so it cannot survive in the host.', 'a', 'Gene silencing.'),
           ('GM plants help reduce post-harvest losses.', 'Genetic modification can make crops more tolerant to abiotic stresses.', 'b', 'Both true, but stress tolerance does not explain reduced post-harvest losses.')],
    'features': {'intro': 'A transgenic crop has these features:', 'q': 'Identify the crop', 'what': 'crop', 'compare': True, 'long': False,
                 'items': [('Bt cotton', ['contains a cry gene', 'produces an insecticidal protein', 'protects against bollworms', 'reduces use of chemical pesticides']),
                           ('RNAi tobacco', ['contains nematode-specific genes', 'produces dsRNA in host cells', 'silences parasite mRNA', 'resists Meloidogyne incognita'])]},
    'fams': [F('C2', 'D2', 'mcq', cry_pest), F('C3', 'D3', 'mcq', appl)],
    'qa': [('C4', 'D5', 'long', 'Explain how Bt toxin kills insects and how Bt cotton is produced.',
            'Bacillus thuringiensis forms protein crystals containing an inactive protoxin. In the alkaline pH of the insect gut the crystals are solubilised and the toxin is activated; it binds to the surface of midgut epithelial cells and creates pores, causing swelling and lysis, and the insect dies. Bt cotton: the specific cry genes (cryIAc, cryIIAb for bollworms; cryIAb for corn borer) are isolated from B. thuringiensis and incorporated into cotton plants, which then make the toxin.',
            '3 marks mechanism; 2 marks production.'),
           ('C4', 'D4', 'explain', 'Describe how RNA interference was used to protect tobacco plants from nematodes.',
            'Using Agrobacterium vectors, nematode-specific genes were introduced into tobacco so that they produced both sense and anti-sense RNA, forming dsRNA. This dsRNA bound to and silenced the specific mRNA of Meloidogyne incognita, so the parasite could not survive in the transgenic host.',
            '1 mark method; 1 mark silencing.'),
           ('C4', 'D3', 'case', 'A farmer in Vidarbha switches to Bt cotton after heavy bollworm damage.\n(i) From which organism is the Bt toxin gene obtained? (1 mark)\n(ii) Name the gene(s) that control cotton bollworms. (1 mark)\n(iii) Why is the toxin harmless to the bacterium but lethal to the insect? (2 marks)',
            '(i) Bacillus thuringiensis. (ii) cryIAc and cryIIAb. (iii) It exists as an inactive protoxin in the bacterium; in the alkaline gut of the insect it is activated, binds midgut cells, creates pores and causes lysis.',
            '(i) 1 (ii) 1 (iii) 2.', ('case',))],
}

CH10S2 = {
    'topic': 'applications in medicine',
    'terms': [('gene therapy', 'a collection of methods that allows correction of a gene defect diagnosed in a child or embryo by delivering a normal gene'),
              ('ADA deficiency', 'a disorder caused by deletion of the gene for adenosine deaminase, an enzyme crucial for the immune system'),
              ('proinsulin', 'the precursor of insulin that contains an extra stretch called the C peptide'),
              ('ELISA', 'enzyme-linked immunosorbent assay, a diagnostic test based on the principle of antigen–antibody interaction'),
              ('a probe', 'a single-stranded DNA or RNA tagged with a radioactive molecule used to detect complementary DNA')],
    'tf': (['Eli Lilly prepared two DNA sequences for chains A and B of human insulin in 1983.', 'The first clinical gene therapy was given in 1990 to a 4-year-old girl with ADA deficiency.', 'About 30 recombinant therapeutics have been approved for human use the world over; 12 are marketed in India.',
            'Insulin used earlier was extracted from the pancreas of slaughtered cattle and pigs.', 'PCR can detect HIV in suspected AIDS patients.'],
           [('Insulin from animal sources never caused allergies.', 'Animal insulin caused allergy or other reactions to the foreign protein in some patients.'),
            ('In proinsulin the C peptide remains in mature insulin.', 'The C peptide is removed during maturation.'),
            ('Gene therapy using lymphocytes is a permanent cure for ADA deficiency.', 'Lymphocytes are not immortal, so periodic infusion is needed; introducing the gene into early embryonic cells could be a permanent cure.'),
            ('ELISA is based on DNA hybridisation.', 'ELISA is based on antigen–antibody interaction.')]),
    'orders': [('sequence of steps in gene therapy for ADA deficiency', ['lymphocytes taken from patient\'s blood', 'grown in culture', 'functional ADA cDNA introduced using a retroviral vector', 'lymphocytes returned to patient'], 'Periodic infusion is needed.', '→')],
    'ar': [('Patients with ADA deficiency treated with genetically engineered lymphocytes need periodic infusions.', 'Lymphocytes are not immortal.', 'a', 'Cells die and must be replaced.'),
           ('Molecular diagnosis can detect a disease before symptoms appear.', 'PCR can detect very low concentrations of a pathogen.', 'a', 'Early detection.'),
           ('Insulin is given by injection and not orally.', 'Insulin is a polypeptide hormone digested in the gut.', 'a', 'Proteases would digest it.')],
    'fams': [F('C2', 'D2', 'mcq', insulin_aa), F('C3', 'D3', 'mcq', diag), F('C3', 'D3', 'mcq', appl_rev)],
    'qa': [('C4', 'D5', 'long', 'Describe how genetically engineered human insulin is produced. Why is it preferred over insulin from animal sources?',
            'Insulin is made of two short polypeptide chains A and B linked by disulphide bridges; in humans it is synthesised as proinsulin with an extra C peptide. Eli Lilly (1983) prepared two DNA sequences for chains A and B, introduced them into plasmids of E. coli, produced the chains separately, extracted them and combined them by creating disulphide bonds to form human insulin. It does not cause allergic reactions to foreign proteins and can be produced in large quantities to meet demand.',
            '3 marks production; 2 marks advantages.'),
           ('C4', 'D4', 'explain', 'Why is gene therapy using lymphocytes not a permanent cure for ADA deficiency? What could be a permanent cure?',
            'Genetically engineered lymphocytes are not immortal and die, so the patient needs periodic infusion. If the gene for ADA isolated from marrow cells is introduced into cells at early embryonic stages, it could be a permanent cure.',
            '1 mark each.'),
           ('C4', 'D3', 'case', 'A doctor in Chennai suspects HIV infection in a patient who shows no symptoms yet.\n(i) Which technique can detect very low concentrations of the virus\'s nucleic acid? (1 mark)\n(ii) Name a test based on antigen–antibody interaction used for HIV. (1 mark)\n(iii) Why are conventional methods (serum and urine analysis) not useful for early detection? (2 marks)',
            '(i) PCR. (ii) ELISA. (iii) Conventional methods detect the pathogen only when its concentration is high and symptoms have appeared; early detection needs methods that amplify or specifically detect low levels of the pathogen.',
            '(i) 1 (ii) 1 (iii) 2.', ('case',))],
}

CH10S3 = {
    'topic': 'transgenic animals, ethics and biopiracy',
    'terms': [('transgenic animals', 'animals that have had their DNA manipulated to possess and express an extra (foreign) gene'),
              ('GEAC', 'the Genetic Engineering Appraisal Committee set up by the Indian Government to decide on the validity of GM research and safety of introducing GM organisms'),
              ('biopiracy', 'the use of bio-resources by multinational companies and other organisations without proper authorisation from the countries and people concerned, without compensatory payment'),
              ('a patent', 'the right granted by a government to an inventor to prevent others from commercially using the invention')],
    'groups': [('a use of transgenic animals', ['study of normal physiology and development', 'study of disease', 'production of biological products', 'testing vaccine safety', 'testing chemical safety (toxicity)'])
               , ('an ethical concern about GMOs', ['unpredictable effects when introduced into ecosystems', 'use of animals causing suffering', 'biopiracy of indigenous resources']),
               ('an Indian regulatory or legal step', ['setting up GEAC', 'amendment of the Indian Patents Bill'])],
    'tf': (['Over 95% of all existing transgenic animals are mice.', 'Transgenic mice are being used to test the safety of the polio vaccine.', 'India has about 2,00,000 varieties of rice.', 'There are 27 documented varieties of Basmati grown in India.',
            'In 1997 an American company got patent rights on Basmati rice through the US Patent and Trademark Office.'],
           [('Most existing transgenic animals are cows.', 'Over 95% are mice.'),
            ('GEAC was set up by the United Nations.', 'GEAC is a committee set up by the Indian Government.'),
            ('Rosie produced milk containing human insulin.', 'Rosie\'s milk contained human alpha-lactalbumin.'),
            ('Biopiracy involves proper authorisation and payment to the country of origin.', 'Biopiracy is use of bio-resources without proper authorisation and compensation.')]),
    'ar': [('Transgenic animals are used to study diseases.', 'They can serve as models for human diseases such as cancer, cystic fibrosis and Alzheimer\'s.', 'a', 'Helps investigate new treatments.'),
           ('India has passed laws against biopiracy.', 'Industrialised nations are rich in biodiversity and traditional knowledge.', 'c', 'Developing and underdeveloped nations are rich in biodiversity; the reason is false.'),
           ('Transgenic mice are used to test the safety of vaccines.', 'They may replace the use of monkeys in safety testing of polio vaccine.', 'a', 'Safer, cheaper testing.')],
    'fams': [F('C3', 'D3', 'numerical', rosie, marks=2)],
    'qa': [('C4', 'D4', 'explain', 'What is biopiracy? Give an example from India.',
            'Use of bio-resources and traditional knowledge by multinational companies without proper authorisation and compensation to the countries and people concerned. Example: in 1997 an American company got patent rights on Basmati rice (a new variety derived from Indian farmers\' varieties); patents have also been sought on uses and products of turmeric and neem.',
            '1 mark definition; 1 mark example.'),
           ('C4', 'D5', 'long', 'List five reasons for which transgenic animals are produced, with an example for each where possible.',
            '(i) Normal physiology and development – e.g. insulin-like growth factor. (ii) Study of disease – models for cancer, cystic fibrosis, rheumatoid arthritis, Alzheimer\'s. (iii) Biological products – α-1-antitrypsin for emphysema; Rosie\'s milk with human alpha-lactalbumin (2.4 g/L). (iv) Vaccine safety – transgenic mice for polio vaccine. (v) Chemical safety testing (toxicity testing) – animals more sensitive to toxic substances give results in less time.',
            '1 mark each reason with example.'),
           ('C4', 'D3', 'case', 'A Haryana farmers\' group learns that a foreign company has patented a product based on a traditional rice variety from their region.\n(i) What is this practice called? (1 mark)\n(ii) Name the famous 1997 Indian example. (1 mark)\n(iii) What steps has India taken to prevent it, and why must GM research be regulated? (2 marks)',
            '(i) Biopiracy. (ii) The patent on Basmati rice granted in the USA. (iii) The Indian Patents Bill was amended to prevent unauthorised exploitation; GEAC decides on the validity of GM research and the safety of releasing GM organisms for public services, as they may have unpredictable effects.',
            '(i) 1 (ii) 1 (iii) 2.', ('case',))],
}


# ---------------------------------------------------------------- ch11 organisms and populations

def birth_rate(r):
    kind = r.choice(['birth', 'death'])
    org, place = r.choice([('lotus plants', 'a pond'), ('fruit flies', 'a laboratory culture'), ('deer', 'a sanctuary'), ('frogs', 'a pond near Kolkata'), ('rabbits', 'a grassland')])
    N = r.choice([20, 40, 50, 80, 100, 200, 250])
    k = r.randint(2, N // 2)
    rate = k / N
    word = 'new ones are added through reproduction' if kind == 'birth' else 'individuals die'
    return {'stem': f'In {place} there were {N} {org} last year. In one year {k} {word}. Calculate the {kind} rate.',
            'answer': f'{num(rate, 3)} per individual per year',
            'key': f'{cap(kind)} rate = number of {"births" if kind == "birth" else "deaths"} / population = {k}/{N} (1) = {num(rate, 3)} per individual per year (1).',
            'distractors': [f'{num(N / k, 3)} per individual per year', f'{num(k / (N + k), 3)} per individual per year', f'{k} per individual per year']}


def pop_change(r):
    N = r.choice([500, 800, 1000, 1200, 2000, 5000])
    B, D, I, E = (r.randint(20, 300) for _ in range(4))
    N1 = N + (B + I) - (D + E)
    if N1 <= 0:
        raise ValueError
    who = name(r)
    place = r.choice(['a forest patch', 'a wetland', 'a lake', 'an island'])
    sp = r.choice(['spotted deer', 'herons', 'langurs', 'frogs'])
    return {'stem': f'{who} studies a population of {sp} in {place} that had {N} individuals at time t. During the year there were {B} births, {D} deaths, {I} immigrants and {E} emigrants. Find the population density at time t + 1.',
            'answer': f'{N1} individuals',
            'key': f'Nₜ₊₁ = Nₜ + [(B + I) − (D + E)] (1) = {N} + [({B} + {I}) − ({D} + {E})] = {N1} (1).',
            'distractors': [f'{N + B - D} individuals', f'{N + (B + E) - (D + I)} individuals', f'{N + B + I + D + E} individuals']}


def expo(r):
    N0 = r.choice([50, 100, 200, 500, 1000])
    rr = r.choice([0.01, 0.02, 0.05, 0.1, 0.2, 0.3])
    t = r.choice([2, 5, 10, 20])
    if rr * t > 4:
        raise ValueError
    Nt = N0 * math.exp(rr * t)
    return {'stem': f'A population of {N0} individuals grows exponentially with an intrinsic rate of natural increase r = {rr} per year. Using Nₜ = N₀eʳᵗ, calculate the population after {t} years. (Take e = 2.718)',
            'answer': f'≈ {num(round(Nt))} individuals',
            'key': f'rt = {rr} × {t} = {num(rr * t, 2)} (1); Nₜ = {N0} × e^{num(rr * t, 2)} = {N0} × {num(math.exp(rr * t), 3)} ≈ {num(round(Nt))} (1).',
            'distractors': [f'≈ {num(round(N0 * (1 + rr * t)))} individuals', f'≈ {num(round(N0 * rr * t))} individuals', f'≈ {num(round(N0 * math.exp(rr * t) * 2))} individuals']}


def logistic(r):
    K = r.choice([500, 1000, 2000, 5000])
    frac = r.choice([0.1, 0.25, 0.5, 0.75, 0.9])
    N = int(K * frac)
    rr = r.choice([0.1, 0.2, 0.4, 0.5])
    g = rr * N * (K - N) / K
    return {'stem': f'A population follows logistic growth with r = {rr} per year and carrying capacity K = {K}. Using dN/dt = rN(K − N)/K, find the growth rate when N = {N}.',
            'answer': f'{num(g, 1)} individuals per year',
            'key': f'(K − N)/K = ({K} − {N})/{K} = {num((K - N) / K, 2)} (1); dN/dt = {rr} × {N} × {num((K - N) / K, 2)} = {num(g, 1)} per year (1).',
            'distractors': [f'{num(rr * N, 1)} individuals per year', f'{num(rr * N * N / K, 1)} individuals per year', f'{num(rr * (K - N), 1)} individuals per year']}


def doubling(r):
    rr = r.choice([0.01, 0.02, 0.0205, 0.03, 0.05, 0.07, 0.1])
    t = math.log(2) / rr
    return {'stem': f'A human population has an r value of {rr} per year. Assuming exponential growth, how long will it take to double? (ln 2 = 0.693)',
            'answer': f'about {num(t, 1)} years',
            'key': f'2N₀ = N₀eʳᵗ ⇒ t = ln 2 / r (1) = 0.693/{rr} ≈ {num(t, 1)} years (1).',
            'distractors': [f'about {num(1 / rr, 1)} years', f'about {num(2 / rr, 1)} years', f'about {num(math.log10(2) / rr, 1)} years']}


def pyramid(r):
    shape = r.choice(['expanding', 'stable', 'declining'])
    if shape == 'expanding':
        pre = r.randint(40, 50); post = r.randint(5, 12)
    elif shape == 'stable':
        pre = r.randint(30, 36); post = r.randint(28, 33)
    else:
        pre = r.randint(12, 20); post = r.randint(35, 45)
    rep = 100 - pre - post
    if rep < 20:
        raise ValueError
    desc = {'expanding': 'triangular (broad base)', 'stable': 'bell-shaped', 'declining': 'urn-shaped (narrow base)'}
    good = f'{desc[shape]}; the population is {"growing" if shape == "expanding" else "stable" if shape == "stable" else "declining"}'
    wrong = [f'{desc[s]}; the population is {"growing" if s == "expanding" else "stable" if s == "stable" else "declining"}' for s in desc if s != shape]
    wrong.append(f'{desc[shape]}; the population is {"declining" if shape != "declining" else "growing"}')
    return mcq(f'In a town survey, {pre}% of people are pre-reproductive, {rep}% reproductive and {post}% post-reproductive. What would be the shape of its age pyramid and what does it show?',
               good, wrong, f'A large pre-reproductive base ⇒ triangular (growing); nearly equal pre- and reproductive groups ⇒ bell-shaped (stable); a small base ⇒ urn-shaped (declining). Here: {good}.', r)


INTER = [('mutualism', '+', '+'), ('competition', '−', '−'), ('predation', '+', '−'), ('parasitism', '+', '−'), ('commensalism', '+', '0'), ('amensalism', '−', '0')]
EXAMPLES = [('an orchid growing as an epiphyte on a mango branch', 'commensalism', 'orchid benefits, mango is unaffected'),
            ('barnacles growing on the back of a whale', 'commensalism', 'barnacles benefit, whale is unaffected'),
            ('cattle egret foraging near grazing cattle', 'commensalism', 'egrets catch insects stirred up by cattle'),
            ('sea anemone with stinging tentacles and the clown fish living among them', 'commensalism', 'clown fish gets protection; anemone is unaffected'),
            ('lichens (fungus and photosynthesising alga)', 'mutualism', 'both partners benefit'),
            ('mycorrhizae between fungi and roots of higher plants', 'mutualism', 'fungus helps absorb nutrients; plant gives carbohydrates'),
            ('fig tree and its pollinating wasp', 'mutualism', 'wasp pollinates; fig gives oviposition site and food'),
            ('Ophrys orchid and the bee it deceives by sexual mimicry', 'mutualism', 'pseudocopulation transfers pollen (plant–pollinator mutualism)'),
            ('Cuscuta growing on hedge plants', 'parasitism', 'Cuscuta derives nutrients, host is harmed'),
            ('the cuckoo laying eggs in the nest of the crow', 'brood parasitism', 'crow incubates cuckoo eggs'),
            ('a tiger eating a deer', 'predation', 'tiger benefits, deer is killed'),
            ('a sparrow eating seeds', 'predation', 'seed eaters are predators in a broad sense'),
            ('Abingdon tortoise and goats introduced on Galapagos islands', 'competition', 'goats outcompeted the tortoise for food'),
            ('flamingoes and resident fishes in South American lakes feeding on zooplankton', 'competition', 'both compete for the same food')]
inter_ex = table_mcq([(a, '', b, c) for a, b, c in EXAMPLES], 'Name the population interaction shown by {a}.', why_fmt='{Ans}: {why}.',
                     pool=['commensalism', 'mutualism', 'parasitism', 'predation', 'competition', 'amensalism', 'brood parasitism'])


def inter_sign(r):
    nm, a, b = r.choice(INTER)
    good = f'{a}/{b}' if b != '0' else f'{a}/0'
    pool = list(dict.fromkeys(f'{x}/{y}' for _, x, y in INTER if f'{x}/{y}' != good))
    return mcq(f'Which sign combination (species A/species B) describes {nm}? (+ beneficial, − detrimental, 0 neutral)', good, r.sample(pool, 3),
               f'{cap(nm)}: {good}.', r)


CH11S1 = {
    'topic': 'population attributes',
    'terms': [('a population', 'a group of individuals of a species living in a well-defined geographical area that share or compete for similar resources and potentially interbreed'),
              ('birth rate (natality)', 'the number of births per capita in a population in a given period'),
              ('death rate (mortality)', 'the number of deaths per capita in a population in a given period'),
              ('an age pyramid', 'a plot of the age distribution (per cent of pre-reproductive, reproductive and post-reproductive individuals) of a population'),
              ('population density', 'the number of individuals of a population per unit area, denoted by N'),
              ('immigration', 'the number of individuals of the same species that have come into the habitat from elsewhere during a given period')],
    'tf': (['A population has attributes that an individual organism does not.', 'An urn-shaped age pyramid indicates a declining population.', 'Pug marks and faecal pellets can be used to estimate tiger populations.',
            'Biomass or per cent cover is a better measure of population size when individuals differ greatly in size.', 'Sex ratio is an attribute of a population.'],
           [('An individual organism has a birth rate.', 'Birth rate is an attribute of a population, not of an individual.'),
            ('A triangular age pyramid indicates a declining population.', 'A triangular pyramid with a broad base indicates an expanding population.'),
            ('Population density always has to be measured in numbers.', 'Per cent cover or biomass can be more meaningful, e.g. a few large banyan trees vs many Parthenium plants.')]),
    'groups': [('an attribute of a population', ['birth rate', 'death rate', 'sex ratio', 'age distribution']), ('an attribute of an individual', ['birth', 'death', 'sex (male or female)']),
               ('an indirect way to estimate population size', ['pug marks', 'faecal pellets', 'number of fish caught per trap'])],
    'classify': False,
    'ar': [('Per cent cover is a better measure of density than numbers for a large tree among many small herbs.', 'One huge banyan tree and 200 Parthenium plants would otherwise suggest the herb dominates.', 'a', 'Size differences matter.'),
           ('Tiger census in India uses pug marks and faecal pellets.', 'Counting tigers directly is difficult.', 'a', 'Indirect estimation.'),
           ('A bell-shaped age pyramid shows a growing population.', 'In a bell-shaped pyramid pre-reproductive and reproductive groups are about equal.', 'd', 'Bell-shaped = stable; the reason is true.')],
    'fams': [F('C3', 'D3', 'numerical', birth_rate, marks=2), F('C3', 'D3', 'mcq', pyramid), F('C4', 'D4', 'mcq', pyramid)],
    'qa': [('C4', 'D4', 'explain', 'Draw and explain the three types of age pyramids of human populations.',
            'Expanding: triangular with a broad base of pre-reproductive individuals (growing). Stable: bell-shaped, pre-reproductive and reproductive groups about equal. Declining: urn-shaped with a narrow base (fewer young). The shape reflects the growth status of the population.',
            '½ mark each diagram; ½ mark each interpretation.'),
           ('C4', 'D3', 'case', 'A forest department team in Madhya Pradesh wants to know the number of tigers in a reserve.\n(i) Why is a direct count not practical? (1 mark)\n(ii) Name two indirect methods used. (1 mark)\n(iii) Why is relative density often enough for ecological studies? Give an example. (2 marks)',
            '(i) Tigers are elusive and range over large areas. (ii) Pug marks and faecal pellets (also camera traps). (iii) Absolute numbers are not always needed; relative density serves the purpose, e.g. the number of fish caught per trap is a good measure of the fish population in a lake.',
            '(i) 1 (ii) 1 (iii) 2.', ('case',))],
}

CH11S2 = {
    'topic': 'population growth',
    'terms': [('the carrying capacity (K)', 'the maximum population a habitat can support with its limited resources'),
              ('exponential growth', 'J-shaped growth in which the population grows in geometric fashion when resources are unlimited'),
              ('logistic growth', 'sigmoid (S-shaped) growth of a population in a habitat with limited resources, described by the Verhulst–Pearl equation'),
              ('the intrinsic rate of natural increase (r)', 'the difference between per capita birth rate and per capita death rate, b − d'),
              ('biotic potential', 'the maximum rate at which a population can grow under ideal conditions')],
    'tf': (['Exponential growth gives a J-shaped curve.', 'Logistic growth gives a sigmoid curve with lag, log, deceleration and asymptote phases.', 'The r value for the human population in India in 1981 was 0.0205.',
            'For the Norway rat r is 0.015 and for the flour beetle 0.12.', 'In nature resources are finite, so logistic growth is more realistic.'],
           [('Exponential growth occurs when resources are limited.', 'It occurs only when resources are unlimited.'),
            ('The carrying capacity is the minimum population a habitat supports.', 'It is the maximum population the habitat can support.'),
            ('r is the sum of per capita birth and death rates.', 'r = b − d.')]),
    'orders': [('phases of logistic (sigmoid) growth', ['lag phase', 'acceleration', 'deceleration', 'asymptote at carrying capacity K'], 'Growth slows as N approaches K.', '→')],
    'ar': [('Logistic growth is more realistic than exponential growth.', 'Resources in nature are limited, so growth slows near the carrying capacity.', 'a', 'Verhulst–Pearl model.'),
           ('A population growing exponentially gives a J-shaped curve.', 'Under unlimited resources the per capita growth rate stays constant.', 'a', 'dN/dt = rN.'),
           ('At carrying capacity the population stops growing.', 'At N = K, the term (K − N)/K becomes zero.', 'a', 'dN/dt = 0.')],
    'fams': [F('C3', 'D3', 'numerical', pop_change, marks=2), F('C4', 'D4', 'numerical', expo, marks=3), F('C4', 'D4', 'numerical', logistic, marks=3), F('C3', 'D3', 'numerical', doubling, marks=2)],
    'qa': [('C4', 'D5', 'long', 'Compare exponential and logistic growth with equations and graphs. Which is more realistic and why?',
            'Exponential: dN/dt = rN, Nₜ = N₀eʳᵗ; unlimited resources; J-shaped curve. Logistic (Verhulst–Pearl): dN/dt = rN(K − N)/K; limited resources; sigmoid curve with lag, acceleration, deceleration and asymptote at carrying capacity K. Logistic growth is more realistic because resources in nature are finite and competition increases as N approaches K.',
            '2 marks exponential; 2 marks logistic; 1 mark realism.'),
           ('C4', 'D4', 'explain', 'If r for a population is 0.1 per year and K = 1000, when is the absolute growth rate the highest? Explain.',
            'dN/dt = rN(K − N)/K is a maximum when N = K/2 = 500 individuals, i.e. at the inflection point of the sigmoid curve, where dN/dt = 0.1 × 500 × 0.5 = 25 per year.',
            '1 mark N = K/2; 1 mark calculation.'),
           ('C4', 'D3', 'case', 'Students in Bengaluru grow yeast in a flask with a fixed amount of glucose and count cells daily.\n(i) What shape of growth curve do they expect? (1 mark)\n(ii) Name the growth model. (1 mark)\n(iii) Why does growth eventually stop, and what is that population size called? (2 marks)',
            '(i) Sigmoid (S-shaped). (ii) Logistic (Verhulst–Pearl) growth. (iii) Glucose and space are limited; as resources are used up and wastes build up, birth rate falls to equal death rate; the maximum population supported is the carrying capacity (K).',
            '(i) 1 (ii) 1 (iii) 2.', ('case',))],
}

CH11S3 = {
    'topic': 'population interactions',
    'terms': [('mutualism', 'an interaction in which both interacting species benefit'),
              ('commensalism', 'an interaction in which one species benefits and the other is neither benefited nor harmed'),
              ('amensalism', 'an interaction in which one species is harmed and the other is unaffected'),
              ('brood parasitism', 'a type of parasitism in which the parasitic bird lays its eggs in the nest of its host and lets the host incubate them'),
              ('competitive exclusion principle', 'Gause\'s principle that two closely related species competing for the same resources cannot co-exist indefinitely and the competitively inferior one is eliminated'),
              ('resource partitioning', 'a mechanism of co-existence in which competing species choose different times or patterns for feeding, as in MacArthur\'s warblers'),
              ('an ectoparasite', 'a parasite that feeds on the external surface of the host, such as lice on humans and ticks on dogs')],
    'tf': (['Predators help in maintaining species diversity in a community.', 'The monarch butterfly is distasteful to predators because of a chemical acquired from a poisonous weed.', 'Calotropis produces highly poisonous cardiac glycosides.',
            'In lichens the fungus and alga live in mutualism.', 'The prickly pear cactus in Australia was controlled by introducing a cactus-feeding predator moth.'],
           [('In commensalism both species benefit.', 'One benefits and the other is unaffected.'),
            ('Competition occurs only between closely related species.', 'Totally unrelated species can compete, e.g. flamingoes and fishes for zooplankton.'),
            ('Parasites always kill their hosts quickly.', 'Parasites usually harm but do not quickly kill hosts; they reduce survival, growth and reproduction.'),
            ('Cuscuta is an ectoparasite with chlorophyll.', 'Cuscuta has lost its chlorophyll and leaves and derives nutrition from the host.')]),
    'ar': [('The prickly pear cactus spread rapidly in Australia.', 'There were no natural predators of the cactus in Australia.', 'a', 'Exotic species without predators spread.'),
           ('Many parasites have evolved complex life cycles.', 'They need intermediate hosts to complete their life cycle, e.g. the liver fluke uses a snail and a fish.', 'a', 'Host specificity.'),
           ('Monarch butterflies are avoided by predators.', 'The caterpillar feeds on a poisonous weed and stores the chemical in the body.', 'a', 'Chemical defence.'),
           ('Barnacles growing on the back of a whale is an example of mutualism.', 'In commensalism one species benefits and the other is unaffected.', 'd', 'It is commensalism; the reason is true.')],
    'features': {'intro': 'A plant defends itself against herbivores by:', 'q': 'Identify the plant', 'what': 'plant',
                 'items': [('Acacia', ['thorns', 'morphological defence', 'common in dry areas', 'leaves protected by spines']),
                           ('cactus', ['spines (modified leaves)', 'morphological defence', 'succulent stem', 'desert plant']),
                           ('Calotropis', ['cardiac glycosides', 'chemical defence', 'cattle and goats do not browse it', 'common weed in abandoned fields']),
                           ('tobacco and coffee plants', ['nicotine and caffeine', 'chemical defence against grazers', 'alkaloids', 'commercially important products'])]},
    'fams': [F('C2', 'D2', 'mcq', inter_ex), F('C3', 'D3', 'mcq', inter_ex), F('C3', 'D2', 'mcq', inter_sign)],
    'qa': [('C4', 'D5', 'long', 'Explain with examples the various ways in which predators are important in nature. How do prey species defend themselves?',
            'Predators transfer energy to higher trophic levels, keep prey populations under control (prickly pear cactus controlled by a moth in Australia; biological control of pests), and maintain species diversity by reducing competition among prey (removal of the starfish Pisaster led to extinction of more than 10 invertebrate species). Prey defences: camouflage (cryptic colouring in frogs and insects), distastefulness (monarch butterfly), and in plants thorns (Acacia, cactus) and chemicals (cardiac glycosides of Calotropis; nicotine, caffeine, quinine).',
            '3 marks role of predators; 2 marks defences.'),
           ('C4', 'D4', 'explain', 'Explain Gause\'s competitive exclusion principle. How did MacArthur show that competing species can co-exist?',
            'Two closely related species competing for the same resources cannot co-exist indefinitely; the competitively inferior one will be eliminated eventually. MacArthur showed that five closely related species of warblers on the same tree avoided competition and co-existed because of behavioural differences in their foraging activities (resource partitioning).',
            '1 mark each.'),
           ('C4', 'D3', 'case', 'On a nature walk near Shillong, Riya notices an orchid on a mango tree, Cuscuta on a hedge, and lichens on a rock.\n(i) Name the interaction between the orchid and the mango tree. (1 mark)\n(ii) Why is Cuscuta called a parasite? (1 mark)\n(iii) What interaction is shown by lichens, and how does each partner gain? (2 marks)',
            '(i) Commensalism. (ii) It has lost its chlorophyll and leaves and derives nutrition from the host plant, harming it. (iii) Mutualism: the alga makes food by photosynthesis; the fungus provides shelter and absorbs water and minerals.',
            '(i) 1 (ii) 1 (iii) 2.', ('case',))],
}


# ---------------------------------------------------------------- ch12 ecosystem

def npp(r):
    gpp = r.choice([1000, 1500, 2000, 2400, 3000, 5000, 8000])
    rp = r.choice([0.2, 0.25, 0.3, 0.4, 0.5])
    R = int(gpp * rp)
    n = gpp - R
    unit = r.choice(['kcal m⁻² yr⁻¹', 'g m⁻² yr⁻¹'])
    eco = r.choice(['a grassland', 'a tropical rainforest', 'a crop field near Ludhiana', 'a pond'])
    return {'stem': f'The gross primary productivity of {eco} is {gpp} {unit}, and plants use {R} {unit} in respiration. Calculate the net primary productivity and state what it represents.',
            'answer': f'{n} {unit}; the biomass available for consumption by heterotrophs (herbivores and decomposers)',
            'key': f'NPP = GPP − R = {gpp} − {R} = {n} {unit} (1); NPP is the available biomass for consumption by heterotrophs (1).',
            'distractors': [f'{gpp + R} {unit}; the biomass available for consumption by heterotrophs', f'{n} {unit}; the total rate of photosynthesis', f'{R} {unit}; the biomass available to herbivores']}


def ten_pc(r):
    E = r.choice([1000, 5000, 10000, 20000, 50000, 100000])
    lv = r.choice([2, 3, 4])
    names = ['producers', 'primary consumers', 'secondary consumers', 'tertiary consumers']
    out = E * 0.1 ** (lv - 1)
    who = name(r)
    return {'stem': f'{who} reads that producers in a food chain fix {num(E)} J of energy. Using the 10 per cent law, how much energy reaches the {names[lv - 1]}?',
            'answer': f'{num(out, 3)} J',
            'key': f'Only about 10% of energy is transferred to each next trophic level (1): {num(E)} × (0.1)^{lv - 1} = {num(out, 3)} J (1).',
            'distractors': [f'{num(E * 0.1 ** lv, 3)} J', f'{num(E * 0.1 ** (lv - 2) if lv > 2 else E * 0.5, 3)} J', f'{num(E * 0.9 ** (lv - 1), 3)} J']}


def ten_back(r):
    top = r.choice([1, 2, 5, 10, 20])
    lv = r.choice([3, 4])
    need = top * 10 ** (lv - 1)
    names = {3: 'secondary consumer', 4: 'tertiary consumer'}
    return mcq(f'A {names[lv]} receives {top} kJ of energy. Applying the 10 per cent law, how much energy must have been fixed by the producers?',
               f'{num(need)} kJ', [f'{num(need // 10)} kJ', f'{num(need * 10)} kJ', f'{num(top * 10 * (lv - 1))} kJ'],
               f'The {names[lv]} is trophic level {lv}; energy at producers = {top} × 10^{lv - 1} = {num(need)} kJ.', r)


def par(r):
    inc = r.choice([1e6, 2e6, 5e6, 1e7])
    pc = r.choice([2, 5, 10])
    p = inc * 0.5
    cap_ = p * pc / 100
    return {'stem': f'A field receives {sf(inc / 1e6, 2)} × 10⁶ J of incident solar radiation. If photosynthetically active radiation (PAR) is 50% of this and plants capture {pc}% of PAR, how much energy is captured by the plants?',
            'answer': f'{num(cap_)} J',
            'key': f'PAR = 50% of {num(inc)} = {num(p)} J (1); captured = {pc}% of {num(p)} = {num(cap_)} J (1).',
            'distractors': [f'{num(inc * pc / 100)} J', f'{num(p)} J', f'{num(cap_ / 10)} J']}


PYR = [('pyramid of numbers in a grassland', 'upright', 'producers are most numerous'),
       ('pyramid of numbers in a tree ecosystem', 'inverted', 'a single large tree supports many insects'),
       ('pyramid of biomass in the sea', 'inverted', 'the biomass of fishes far exceeds that of phytoplankton at a given time'),
       ('pyramid of biomass in a forest', 'upright', 'producers have the largest biomass'),
       ('pyramid of energy in any ecosystem', 'always upright', 'energy decreases at each successive trophic level')]
pyr = table_mcq([(a, '', b, c) for a, b, c in PYR], 'What is the shape of the {a}?', why_fmt='{Ans} – {why}.',
                pool=['upright', 'inverted', 'always upright', 'spindle-shaped'])

TL = [('grass', 'first trophic level (producer)'), ('a grasshopper eating grass', 'second trophic level (primary consumer)'), ('a frog eating grasshoppers', 'third trophic level (secondary consumer)'),
      ('a snake eating frogs', 'fourth trophic level (tertiary consumer)'), ('phytoplankton', 'first trophic level (producer)'), ('zooplankton', 'second trophic level (primary consumer)'),
      ('a small fish eating zooplankton', 'third trophic level (secondary consumer)'), ('a goat', 'second trophic level (primary consumer)')]
tl = table_mcq([(a, '', b, '') for a, b in TL], 'In a food chain, what is the trophic level of {a}?', why_fmt='{a}: {ans}.')

DECOMP = [('fragmentation', 'detritivores such as earthworms break detritus into smaller particles'), ('leaching', 'water-soluble inorganic nutrients go down into the soil horizon and precipitate as unavailable salts'),
          ('catabolism', 'bacterial and fungal enzymes degrade detritus into simpler inorganic substances'), ('humification', 'a dark amorphous substance called humus, highly resistant to microbial action, accumulates'),
          ('mineralisation', 'humus is further degraded by microbes, releasing inorganic nutrients')]
decomp = table_rev([(a, '', b, '') for a, b in DECOMP], 'Name the step of decomposition in which {ans}.', why_fmt='{a}: {ans}.')

CH12S1 = {
    'topic': 'ecosystem structure, function and productivity',
    'terms': [('an ecosystem', 'a functional unit of nature where living organisms interact among themselves and with their surrounding physical environment'),
              ('stratification', 'the vertical distribution of different species occupying different levels, as in a forest'),
              ('primary production', 'the amount of biomass or organic matter produced per unit area over a time period by plants during photosynthesis'),
              ('gross primary productivity (GPP)', 'the rate of production of organic matter during photosynthesis'),
              ('net primary productivity (NPP)', 'GPP minus respiration losses; the biomass available for consumption by heterotrophs'),
              ('secondary productivity', 'the rate of formation of new organic matter by consumers')],
    'tf': (['The annual net primary productivity of the whole biosphere is approximately 170 billion tons (dry weight) of organic matter.', 'Oceans, despite covering about 70% of the surface, have a productivity of only 55 billion tons.',
            'Primary productivity depends on the plant species, environmental factors, availability of nutrients and photosynthetic capacity.', 'Trees occupy the top vertical strata of a forest, shrubs the second and herbs and grasses the bottom layers.'],
           [('NPP = GPP + R.', 'NPP = GPP − R.'),
            ('Oceans have the highest productivity of the biosphere because they are the largest.', 'Oceans cover about 70% of the surface but produce only 55 of the 170 billion tons.'),
            ('Secondary productivity is the rate of photosynthesis.', 'Secondary productivity is the rate of formation of new organic matter by consumers.')]),
    'groups': [('a producer in a pond ecosystem', ['phytoplankton', 'some algae', 'floating and submerged plants']), ('a consumer in a pond ecosystem', ['zooplankton', 'free-swimming fishes', 'bottom-dwelling fishes']),
               ('a decomposer in a pond ecosystem', ['bacteria at the bottom', 'fungi', 'flagellates'])],
    'ar': [('Oceans have low productivity despite their size.', 'Productivity in oceans is limited by nutrients such as nitrogen and light at depth.', 'a', 'Nutrient-poor open oceans.'),
           ('NPP is less than GPP.', 'Plants use part of the GPP in respiration.', 'a', 'NPP = GPP − R.'),
           ('A pond is a self-sustainable ecosystem.', 'A pond has producers, consumers and decomposers, with solar energy as input.', 'a', 'Complete functional unit.')],
    'fams': [F('C3', 'D3', 'numerical', npp, marks=2), F('C4', 'D4', 'numerical', par, marks=2)],
    'qa': [('C4', 'D5', 'long', 'Describe the components of a pond ecosystem and explain the four basic functional aspects of an ecosystem.',
            'Abiotic: water, dissolved inorganic and organic substances, soil at the bottom; solar input, temperature, day length. Biotic: producers (phytoplankton, algae, floating, submerged and marginal plants), consumers (zooplankton, free-swimming and bottom-dwelling animals), decomposers (fungi, bacteria, flagellates). Functions: productivity, decomposition, energy flow and nutrient cycling. Energy is converted by autotrophs, consumed by heterotrophs and the dead matter decomposed to release minerals for reuse.',
            '2 marks components; 3 marks functions.'),
           ('C4', 'D4', 'explain', 'Distinguish between gross and net primary productivity. Why is NPP important?',
            'GPP is the rate of production of organic matter during photosynthesis; a considerable part of it is used by plants in respiration. NPP = GPP − R. NPP is the biomass available for consumption by heterotrophs (herbivores and decomposers), so it determines how much energy flows to higher trophic levels.',
            '1 mark difference; 1 mark importance.'),
           ('C4', 'D3', 'case', 'A school group in Bhopal compares a grassland plot with a deep lake of the same area.\n(i) What is primary productivity? (1 mark)\n(ii) Give two factors on which it depends. (1 mark)\n(iii) Oceans cover 70% of the earth, yet their productivity is about 55 of 170 billion tons. Explain. (2 marks)',
            '(i) The rate of biomass production per unit area over a time period by plants. (ii) Plant species, environmental factors, availability of nutrients, photosynthetic capacity (any two). (iii) In the open ocean, nutrients (especially nitrogen) are scarce and light penetrates only the upper layers, so productivity per unit area is low.',
            '(i) 1 (ii) 1 (iii) 2.', ('case',))],
}

CH12S2 = {
    'topic': 'decomposition',
    'terms': [('detritus', 'dead plant remains such as leaves, bark and flowers, and dead remains of animals including faecal matter'),
              ('detritivores', 'organisms such as earthworms that break down detritus into smaller particles'),
              ('humus', 'a dark-coloured amorphous substance highly resistant to microbial action that serves as a reservoir of nutrients'),
              ('mineralisation', 'the release of inorganic nutrients by the microbial degradation of humus'),
              ('leaching', 'the process by which water-soluble inorganic nutrients go down into the soil horizon')],
    'tf': (['Decomposition is largely an oxygen-requiring process.', 'Warm and moist environments favour decomposition.', 'Decomposition is slower if detritus is rich in lignin and chitin.',
            'Decomposition is quicker if detritus is rich in nitrogen and water-soluble substances like sugars.', 'Low temperature and anaerobiosis inhibit decomposition, leading to build-up of organic material.'],
           [('Decomposition is faster when detritus is rich in lignin and chitin.', 'Lignin and chitin slow decomposition.'),
            ('Humus decomposes very quickly.', 'Humus is highly resistant to microbial action and decomposes extremely slowly.'),
            ('Decomposition is faster in cold, dry conditions.', 'Warm and moist conditions favour it.'),
            ('Leaching makes nutrients available near the soil surface.', 'Leaching carries soluble nutrients down where they precipitate as unavailable salts.')]),
    'orders': [('steps of decomposition', ['fragmentation', 'leaching', 'catabolism', 'humification', 'mineralisation'], 'Fragmentation, leaching and catabolism operate simultaneously; humification and mineralisation occur in the soil.', '→')],
    'ar': [('Decomposition is slow in cold regions.', 'Low temperature reduces the activity of decomposers.', 'a', 'Temperature controls microbial activity.'),
           ('Humus is a reservoir of nutrients.', 'Humus is colloidal and highly resistant to microbial action.', 'b', 'Both true; its colloidal nature and slow mineralisation make it a nutrient reservoir, but resistance alone does not explain it.'),
           ('Decomposition is faster in warm and moist conditions.', 'Decomposition is an anaerobic process.', 'c', 'Decomposition is largely an oxygen-requiring process; the reason is false.')],
    'fams': [F('C2', 'D2', 'mcq', decomp), F('C3', 'D3', 'mcq', decomp)],
    'qa': [('C4', 'D5', 'long', 'Describe the steps of decomposition and the factors that affect its rate.',
            'Fragmentation: detritivores such as earthworms break detritus into smaller particles. Leaching: water-soluble nutrients go down into the soil and precipitate as unavailable salts. Catabolism: bacterial and fungal enzymes degrade detritus into simple inorganic substances. Humification: accumulation of humus, dark and resistant to microbes. Mineralisation: degradation of humus releases inorganic nutrients. Rate is controlled by chemical composition (slower with lignin and chitin, faster with nitrogen and sugars) and climatic factors (warm and moist favour it; low temperature and anaerobiosis inhibit it).',
            '3 marks steps; 2 marks factors.'),
           ('C4', 'D4', 'explain', 'Why does organic matter accumulate in the soil of cold, waterlogged regions?',
            'Low temperature reduces the activity of decomposers and waterlogging creates anaerobic conditions; since decomposition is largely an oxygen-requiring process, it is inhibited and organic material builds up.',
            '1 mark each factor.'),
           ('C4', 'D3', 'case', 'Aditi keeps two compost pits on her farm near Nashik: one of kitchen peels kept moist and warm, the other of dry sawdust.\n(i) Which pit decomposes faster? (1 mark)\n(ii) Name the step in which earthworms act. (1 mark)\n(iii) Give two reasons for the difference in rates. (2 marks)',
            '(i) The moist pit with kitchen peels. (ii) Fragmentation. (iii) Kitchen peels are rich in nitrogen and water-soluble sugars while sawdust is rich in lignin; warm, moist and aerated conditions favour decomposer activity.',
            '(i) 1 (ii) 1 (iii) 2.', ('case',))],
}

CH12S3 = {
    'topic': 'energy flow and ecological pyramids',
    'terms': [('a food chain', 'a sequence of organisms through which energy flows by one eating another'),
              ('the grazing food chain (GFC)', 'a food chain that starts with producers, such as grass → goat → man'),
              ('the detritus food chain (DFC)', 'a food chain that begins with dead organic matter and includes decomposers'),
              ('a trophic level', 'the specific place an organism occupies in a food chain based on its source of nutrition'),
              ('the standing crop', 'the mass of living material at each trophic level at a particular time'),
              ('the 10 per cent law', 'the observation that only about 10% of the energy is transferred to each trophic level from the lower trophic level')],
    'tf': (['Energy flow in an ecosystem is unidirectional.', 'In an aquatic ecosystem the GFC is the major conduit for energy flow.', 'In a terrestrial ecosystem a much larger fraction of energy flows through the detritus food chain than through the GFC.',
            'The pyramid of energy is always upright.', 'Ecological pyramids do not take into account the same species belonging to two or more trophic levels.'],
           [('Energy flows in a cycle in an ecosystem.', 'Energy flow is unidirectional, from the sun to producers to consumers.'),
            ('The pyramid of biomass in the sea is upright.', 'It is generally inverted because the biomass of fishes exceeds that of phytoplankton.'),
            ('About 50% of energy is passed to the next trophic level.', 'Only about 10% is passed on.'),
            ('Ecological pyramids accommodate food webs well.', 'They assume a simple food chain and do not accommodate a food web.')]),
    'ar': [('The pyramid of energy is always upright.', 'Energy decreases at each successive trophic level as some is lost as heat.', 'a', 'Second law of thermodynamics.'),
           ('The number of trophic levels in a food chain is limited.', 'Only about 10% of energy is transferred to the next level.', 'a', 'Too little energy remains after 4–5 levels.'),
           ('The pyramid of numbers in a tree ecosystem is inverted.', 'A single tree supports a large number of insects.', 'a', 'One producer, many consumers.'),
           ('The pyramid of biomass in the sea is upright.', 'Phytoplankton have a short life span and are rapidly consumed.', 'd', 'It is inverted; the reason is true.')],
    'fams': [F('C3', 'D3', 'numerical', ten_pc, marks=2), F('C3', 'D3', 'mcq', ten_back), F('C2', 'D2', 'mcq', pyr), F('C3', 'D3', 'mcq', pyr), F('C2', 'D1', 'mcq', tl)],
    'qa': [('C4', 'D5', 'long', 'What are ecological pyramids? Describe the pyramids of number, biomass and energy with one example each where it is inverted or always upright. Give two limitations of pyramids.',
            'Graphic representations of the relationship between organisms at different trophic levels, with producers at the base. Number: upright in a grassland, inverted in a tree ecosystem. Biomass: upright in most terrestrial ecosystems, inverted in the sea (fish biomass > phytoplankton). Energy: always upright, as energy decreases at each level. Limitations: they do not consider the same species at two or more trophic levels; they assume a simple food chain and do not accommodate food webs; saprophytes are not given a place.',
            '1 mark definition; 3 marks pyramids; 1 mark limitations.'),
           ('C4', 'D4', 'explain', 'Distinguish between the grazing food chain and the detritus food chain.',
            'GFC starts from producers (grass → goat → man) and is the main conduit of energy in aquatic ecosystems. DFC begins with dead organic matter, made of decomposers (fungi, bacteria) that get energy from detritus; in terrestrial ecosystems a larger fraction of energy flows through the DFC.',
            '1 mark each.'),
           ('C4', 'D3', 'case', 'In a grassland near Jaipur, grass fixes 20,000 J, which passes to grasshoppers, then frogs, then snakes.\n(i) State the 10 per cent law. (1 mark)\n(ii) How much energy reaches the snakes? (1 mark)\n(iii) Why are food chains rarely longer than four or five links? (2 marks)',
            '(i) Only about 10% of energy is transferred from one trophic level to the next. (ii) 20,000 → 2000 → 200 → 20 J. (iii) Energy available decreases by about 90% at each level, being lost as heat in respiration, so after four or five levels too little energy is left to support another level.',
            '(i) 1 (ii) 1 (iii) 2.', ('case',))],
}


# ---------------------------------------------------------------- ch13 biodiversity and its conservation

def species_area(r):
    C = r.choice([12, 20, 25, 40, 60])
    Z = r.choice([0.1, 0.15, 0.2, 0.25])
    A = r.choice([10, 100, 1000, 10000])
    S = C * A ** Z
    return {'stem': f'For a region, the species–area relationship is S = CA^Z with C = {C} and Z = {Z}. Estimate the species richness for an area of {num(A)} km².',
            'answer': f'≈ {num(S, 1)} species',
            'key': f'log S = log C + Z log A = log {C} + {Z} × log {num(A)} = {num(math.log10(C), 3)} + {num(Z * math.log10(A), 3)} (1); S = 10^{num(math.log10(S), 3)} ≈ {num(S, 1)} species (1).',
            'distractors': [f'≈ {num(C * A * Z, 1)} species', f'≈ {num(C + Z * A, 1)} species', f'≈ {num(C * A ** (2 * Z), 1)} species']}


def z_value(r):
    Z = r.choice([0.1, 0.15, 0.2, 0.6, 0.8, 1.0, 1.2])
    A1 = r.choice([10, 100])
    A2 = A1 * 100
    C = r.choice([10, 20, 30])
    S1, S2 = round(C * A1 ** Z), round(C * A2 ** Z)
    z = math.log10(S2 / S1) / math.log10(A2 / A1)
    kind = 'very large areas such as entire continents (or frugivorous birds and mammals in tropical forests)' if z >= 0.6 else 'small regions within a continent, whatever the taxonomic group'
    return {'stem': f'In one region the number of species rises from {num(S1, 1)} in {A1} km² to {num(S2, 1)} in {num(A2)} km². Calculate Z, the slope of the log S–log A line, and say what kind of area this value is typical of.',
            'answer': f'Z ≈ {num(z, 2)}; typical of {kind}',
            'key': f'Z = (log S₂ − log S₁)/(log A₂ − log A₁) = log({num(S2 / S1, 2)})/log(100) = {num(z, 2)} (1); NCERT: Z ≈ 0.1–0.2 for small regions, 0.6–1.2 for very large areas (1).',
            'distractors': [f'Z ≈ {num(S2 / S1 / 100, 2)}; typical of {kind}', f'Z ≈ {num(z, 2)}; typical of {"small regions within a continent, whatever the taxonomic group" if z >= 0.6 else "very large areas such as entire continents"}',
                            f'Z ≈ {num(1 / z, 2)}; typical of oceanic islands only']}


def ext_pct(r):
    tot = 784
    part, k = r.choice([('vertebrates', 338), ('invertebrates', 359), ('plants', 87)])
    pct = k / tot * 100
    return {'stem': f'IUCN Red List (2004) documents the extinction of 784 species in the last 500 years, of which {k} are {part}. What percentage of the recorded extinctions are {part}?',
            'answer': f'{num(pct, 1)}%',
            'key': f'Percentage = {k}/784 × 100 (1) = {num(pct, 1)}% (1).',
            'distractors': [f'{num(100 - pct, 1)}%', f'{num(k / 1000 * 100, 1)}%', f'{num(784 / k, 1)}%']}


def india_share(r):
    tot = r.choice([1.5, 1.6, 1.75, 2.0])
    pct = 8.1
    n = tot * 1e6 * pct / 100
    return {'stem': f'India has about 8.1% of the global species diversity. If about {tot} million species have been recorded globally, estimate the number of species recorded from India.',
            'answer': f'about {num(n / 1e3, 0)} thousand species',
            'key': f'{tot} × 10⁶ × 8.1/100 (1) = {num(n, 0)} ≈ {num(n / 1e3, 0)} thousand (1).',
            'distractors': [f'about {num(tot * 1e6 * 2.4 / 100 / 1e3, 0)} thousand species', f'about {num(n / 1e2, 0)} thousand species', f'about {num(n / 1e4, 0)} thousand species']}


QUARTET = [('the Nile perch introduced into Lake Victoria', 'alien species invasion', 'led to extinction of more than 200 species of cichlid fish'),
           ('Parthenium (carrot grass), Lantana and water hyacinth spreading in India', 'alien species invasion', 'they threaten native species'),
           ('illegal introduction of the African catfish Clarias gariepinus for aquaculture', 'alien species invasion', 'it threatens indigenous catfishes in Indian rivers'),
           ('the Amazon rainforest being cut and cleared for soybean and cattle pastures', 'habitat loss and fragmentation', 'the "lungs of the planet" are being destroyed'),
           ('tropical rain forests reduced from 14% to 6% of the earth\'s land surface', 'habitat loss and fragmentation', 'the most important cause of extinction'),
           ('Steller\'s sea cow and passenger pigeon becoming extinct in the last 500 years', 'over-exploitation', 'excessive hunting by humans'),
           ('many marine fish populations declining from overharvesting', 'over-exploitation', 'commercial species are endangered'),
           ('a parasite fish becoming extinct along with its host fish', 'co-extinction', 'obligatory association with the host'),
           ('a plant becoming extinct when its pollinator wasp species dies out', 'co-extinction', 'obligatory plant–pollinator mutualism')]
quartet = table_mcq([(a, '', b, c) for a, b, c in QUARTET], 'Which cause of biodiversity loss is illustrated by {a}?', why_fmt='{Ans}: {why}.',
                    pool=['alien species invasion', 'habitat loss and fragmentation', 'over-exploitation', 'co-extinction'])

CONS = [('a biosphere reserve', 'in situ'), ('a national park', 'in situ'), ('a wildlife sanctuary', 'in situ'), ('a sacred grove', 'in situ'),
        ('a zoological park', 'ex situ'), ('a botanical garden', 'ex situ'), ('a seed bank', 'ex situ'), ('cryopreservation of gametes', 'ex situ'), ('a wildlife safari park', 'ex situ')]


def cons_pick(r):
    want = r.choice(['in situ', 'ex situ'])
    good = r.choice([a for a, b in CONS if b == want])
    wrong = r.sample([a for a, b in CONS if b != want], 3)
    return mcq(f'Which of the following is an example of {want} conservation?', good, wrong,
               f'{cap(good)} is {want} conservation ({"protecting species in their natural habitat" if want == "in situ" else "taking threatened species out of their natural habitat to a special setting"}).', r)


NUMS = [('the number of species described globally (IUCN 2004)', 'slightly more than 1.5 million'), ('Robert May\'s global estimate of species diversity', 'about 7 million'),
        ('India\'s share of the world\'s land area', '2.4%'), ('India\'s share of global species diversity', '8.1%'),
        ('the number of biodiversity hotspots in the world', '34'), ('the area of the earth\'s land covered by all hotspots together', 'less than 2%'),
        ('the number of species extinctions recorded by IUCN (2004) in the last 500 years', '784'),
        ('the proportion of all recorded species that are animals', 'more than 70%'), ('the number of strains of rice in India', 'more than 50,000'),
        ('the number of varieties of mango in India', '1,000')]
nums = table_mcq([(a, '', b, '') for a, b in NUMS], 'According to NCERT, what is {a}?', why_fmt='{a}: {ans}.')

CH13S1 = {
    'topic': 'biodiversity: levels, patterns and importance',
    'terms': [('biodiversity', 'the term popularised by Edward Wilson for the combined diversity at all levels of biological organisation'),
              ('genetic diversity', 'diversity shown by a single species at the genetic level over its distributional range, as in Rauwolfia vomitoria'),
              ('species diversity', 'diversity at the species level, as in the higher number of amphibian species in the Western Ghats than the Eastern Ghats'),
              ('ecological diversity', 'diversity at the ecosystem level, such as deserts, rain forests, mangroves, coral reefs, wetlands and estuaries in India'),
              ('the rivet popper hypothesis', 'Paul Ehrlich\'s analogy in which each species is a rivet in an airplane (ecosystem); losing rivets can endanger the flight'),
              ('the latitudinal gradient', 'the pattern in which species diversity decreases as we move away from the equator towards the poles')],
    'tf': (['India is one of the 12 mega diversity countries of the world.', 'Tropical forests have more species than temperate forests.', 'Colombia, near the equator, has nearly 1,400 species of birds.',
            'Tilman found that plots with more species showed less year-to-year variation in total biomass.', 'Insects make up more than 70% of all recorded animal species.'],
           [('Species diversity increases from the equator to the poles.', 'It decreases from the equator towards the poles.'),
            ('Species richness decreases with increasing explored area.', 'It increases with explored area, but only up to a limit.'),
            ('India has 20% of the world\'s land area.', 'India has only 2.4% of the world\'s land area.'),
            ('Biodiversity was a term coined by Paul Ehrlich.', 'It was popularised by the sociobiologist Edward Wilson.')]),
    'ar': [('Tropics have greater biodiversity than temperate regions.', 'Tropical latitudes have remained relatively undisturbed for millions of years and receive more solar energy.', 'a', 'More evolutionary time, more stable environment and more productivity.'),
           ('Communities with more species tend to be more stable.', 'Tilman\'s experiments found less year-to-year variation in total biomass in plots with more species.', 'a', 'Long-term ecosystem experiments.'),
           ('The Western Ghats have a greater amphibian species diversity than the Eastern Ghats.', 'This is an example of species diversity.', 'b', 'Both true; the reason names the level of diversity but does not explain the greater number.')],
    'fams': [F('C4', 'D4', 'numerical', species_area, marks=2), F('C4', 'D5', 'numerical', z_value, marks=3), F('C3', 'D3', 'numerical', india_share, marks=2), F('C2', 'D2', 'mcq', nums)],
    'qa': [('C4', 'D5', 'long', 'Explain the latitudinal gradient in species diversity. Give three hypotheses that explain greater biological diversity in the tropics.',
            'Species diversity decreases from the equator towards the poles: e.g. Colombia has nearly 1,400 bird species, New York 105 and Greenland 56; India has more than 1,200. Hypotheses: (i) speciation is a function of time; temperate regions were subjected to frequent glaciations while the tropics remained relatively undisturbed for millions of years, allowing long evolutionary time; (ii) tropical environments are less seasonal and more constant and predictable, promoting niche specialisation; (iii) more solar energy is available in the tropics, giving higher productivity.',
            '2 marks pattern; 3 marks hypotheses.'),
           ('C4', 'D4', 'explain', 'Explain the rivet popper hypothesis.',
            'Paul Ehrlich compared an ecosystem to an airplane and species to rivets. Removing a few rivets (species) may not affect flight safety initially, but as more are removed the plane becomes dangerously weak; loss of rivets on key parts (key species that drive major ecosystem functions) is more serious than on less important parts.',
            '1 mark analogy; 1 mark key species.'),
           ('C4', 'D3', 'case', 'Tanvi compares bird lists: Colombia ~1,400 species, India >1,200, New York 105 and Greenland 56.\n(i) What pattern does this show? (1 mark)\n(ii) Give one reason for it. (1 mark)\n(iii) For areas within a region, Z ≈ 0.1–0.2. What does Z represent, and when is it much steeper? (2 marks)',
            '(i) Latitudinal gradient: diversity decreases from the equator to the poles. (ii) Tropics were undisturbed for long periods, less seasonal, or receive more solar energy (any one). (iii) Z is the slope of the line (regression coefficient) of log S against log A; it is steeper (0.6–1.2) for very large areas such as whole continents.',
            '(i) 1 (ii) 1 (iii) 2.', ('case',))],
}

CH13S2 = {
    'topic': 'loss of biodiversity',
    'terms': [('the evil quartet', 'the four major causes of biodiversity loss: habitat loss and fragmentation, over-exploitation, alien species invasions and co-extinctions'),
              ('co-extinction', 'the extinction of a species that has an obligatory association with another species when that species becomes extinct'),
              ('habitat fragmentation', 'the breaking up of large habitats into small fragments, harming animals needing large territories'),
              ('the IUCN Red List', 'the list maintained by IUCN documenting threatened and extinct species')],
    'tf': (['The Amazon rain forest is called the "lungs of the planet".', 'The Nile perch introduced into Lake Victoria led to the extinction of more than 200 cichlid species.', 'Habitat loss and fragmentation is the most important cause of extinction.',
            'Some 32% of all amphibian species in the world face the threat of extinction.', 'Steller\'s sea cow and the passenger pigeon became extinct due to over-exploitation by humans.'],
           [('Alien species always increase native biodiversity.', 'Invasive alien species often cause decline or extinction of indigenous species.'),
            ('Tropical rain forests once covered 30% of the earth\'s land surface.', 'They once covered 14% and now cover no more than 6%.'),
            ('The current species extinction rate is similar to the pre-human rate.', 'It is estimated to be 100 to 1,000 times faster.'),
            ('Dodo became extinct due to co-extinction.', 'Dodo (Mauritius) became extinct due to human activities; co-extinction refers to associated species dying out together.')]),
    'ar': [('Habitat fragmentation affects animals requiring large territories.', 'Large habitats broken into small fragments cannot support such animals.', 'a', 'Also affects migratory animals.'),
           ('Alien species can cause extinction of native species.', 'Invasive species have no natural enemies in the new habitat and outcompete natives.', 'a', 'Nile perch, Parthenium, water hyacinth.'),
           ('A host fish going extinct also leads to extinction of its specific parasites.', 'This is an example of co-extinction.', 'b', 'Both true; the reason names the phenomenon but does not explain the mechanism (obligatory association).')],
    'fams': [F('C2', 'D2', 'mcq', quartet), F('C3', 'D3', 'mcq', quartet), F('C3', 'D3', 'numerical', ext_pct, marks=2)],
    'qa': [('C4', 'D5', 'long', 'What is the "evil quartet"? Describe each cause of biodiversity loss with an example.',
            '(i) Habitat loss and fragmentation – tropical rain forests reduced from 14% to 6% of land; Amazon cleared for soybean and cattle pastures. (ii) Over-exploitation – Steller\'s sea cow and passenger pigeon became extinct; marine fish overharvested. (iii) Alien species invasions – Nile perch in Lake Victoria caused extinction of over 200 cichlid species; Parthenium, Lantana, water hyacinth; African catfish Clarias gariepinus. (iv) Co-extinctions – parasites of a host fish, plant–pollinator mutualism.',
            '1 mark term; 1 mark each cause with example.'),
           ('C4', 'D4', 'explain', 'Explain co-extinction with two examples.',
            'When a species becomes extinct, the plant and animal species associated with it in an obligatory way also become extinct. Examples: when a host fish species becomes extinct its unique assemblage of parasites meets the same fate; co-evolved plant–pollinator mutualism, where extinction of one invariably leads to extinction of the other.',
            '1 mark definition; 1 mark examples.'),
           ('C4', 'D3', 'case', 'Fish farmers in Kerala illegally introduce the African catfish Clarias gariepinus into local ponds, from where it reaches rivers.\n(i) Which cause of biodiversity loss does this illustrate? (1 mark)\n(ii) What threat does it pose? (1 mark)\n(iii) Give one more example from India and one from Africa. (2 marks)',
            '(i) Alien species invasion. (ii) It threatens the indigenous catfishes of Indian rivers. (iii) India: Parthenium (carrot grass), Lantana or water hyacinth (Eichhornia); Africa: Nile perch in Lake Victoria, which caused extinction of more than 200 cichlid species.',
            '(i) 1 (ii) 1 (iii) 2.', ('case',))],
}

CH13S3 = {
    'topic': 'biodiversity conservation',
    'terms': [('in situ conservation', 'on-site conservation that protects the whole ecosystem and its biodiversity'),
              ('ex situ conservation', 'off-site conservation in which threatened plants and animals are taken out of their natural habitat and protected in special settings'),
              ('biodiversity hotspots', 'regions with very high levels of species richness and high degree of endemism'),
              ('cryopreservation', 'the preservation of gametes of threatened species in viable and fertile condition for long periods using very low temperatures'),
              ('sacred groves', 'tracts of forest set aside around places of worship and protected by tribal communities'),
              ('endemism', 'the occurrence of species confined to a particular region and not found anywhere else')],
    'groups': [('a method of in situ conservation', ['biosphere reserves', 'national parks', 'wildlife sanctuaries', 'sacred groves']), ('a method of ex situ conservation', ['zoological parks', 'botanical gardens', 'seed banks', 'cryopreservation']),
               ('a cause of biodiversity loss', ['over-exploitation', 'alien species invasions', 'co-extinctions'])],
    'tf': (['Three of the 34 biodiversity hotspots – Western Ghats and Sri Lanka, Indo-Burma and Himalaya – cover India\'s rich biodiversity regions.', 'Strict protection of hotspots could reduce ongoing mass extinctions by almost 30%.',
            'Sacred groves are found in the Khasi and Jaintia Hills of Meghalaya, the Aravalli Hills of Rajasthan and the Western Ghats.', 'The Earth Summit was held in Rio de Janeiro in 1992.',
            'The World Summit on Sustainable Development was held in Johannesburg in 2002.'],
           [('Zoological parks are in situ conservation.', 'They are ex situ: animals are kept out of their natural habitat.'),
            ('Biodiversity hotspots have low endemism.', 'They have high species richness and high endemism.'),
            ('The Earth Summit was held in Johannesburg in 1992.', 'It was held in Rio de Janeiro in 1992; Johannesburg hosted the 2002 summit.'),
            ('Hotspots together cover about 20% of the earth\'s land area.', 'All hotspots together cover less than 2% of the land area.')]),
    'ar': [('Sacred groves help conserve biodiversity.', 'They are protected by tribal communities because of religious beliefs.', 'a', 'Refuges for rare and threatened plants.'),
           ('In situ conservation is preferred for the conservation of whole ecosystems.', 'It protects species in their natural habitat along with their interactions.', 'a', 'Whole ecosystem protected.'),
           ('Seed banks are a method of in situ conservation.', 'Seeds of different genetic strains of commercially important plants can be kept for long periods.', 'd', 'Seed banks are ex situ; the reason is true.')],
    'features': {'intro': 'A reason to conserve biodiversity is described as:', 'q': 'Which kind of reason is it', 'what': 'reason', 'long': False,
                 'items': [('narrowly utilitarian', ['direct economic benefits', 'food, firewood, fibre, construction material', 'medicines (25% of drugs from plants)', 'bioprospecting for products']),
                           ('broadly utilitarian', ['ecosystem services', 'Amazon forest produces about 20% of the oxygen', 'pollination by bees and birds', 'aesthetic pleasure']),
                           ('ethical', ['every species has intrinsic value', 'moral duty to pass on the biological legacy', 'we share the planet with millions of species', 'not based on economic value'])]
                 , 'compare': False, 'case': False},
    'fams': [F('C2', 'D2', 'mcq', cons_pick), F('C3', 'D2', 'mcq', cons_pick)],
    'qa': [('C4', 'D5', 'long', 'Why should we conserve biodiversity? Describe in situ and ex situ methods of conservation with examples.',
            'Reasons: narrowly utilitarian (food, fibre, medicines, bioprospecting), broadly utilitarian (ecosystem services – the Amazon produces about 20% of total oxygen; pollination; aesthetics) and ethical (intrinsic value of every species). In situ: protecting the whole ecosystem – biodiversity hotspots, biosphere reserves, national parks, wildlife sanctuaries and sacred groves (Khasi and Jaintia Hills, Aravalli Hills, Western Ghats). Ex situ: zoological parks, botanical gardens, wildlife safari parks, cryopreservation of gametes, in vitro fertilisation, tissue culture and seed banks.',
            '2 marks reasons; 1.5 marks in situ; 1.5 marks ex situ.'),
           ('C4', 'D4', 'explain', 'What are biodiversity hotspots? Name the hotspots that cover India.',
            'Regions with very high species richness and a high degree of endemism; there are 34 hotspots covering less than 2% of earth\'s land area. India: Western Ghats and Sri Lanka, Indo-Burma, and Himalaya.',
            '1 mark definition; 1 mark names.'),
           ('C4', 'D3', 'case', 'Students from Shillong visit the Mawphlang sacred forest in the Khasi Hills and later a seed bank.\n(i) Is the sacred forest an in situ or ex situ method? (1 mark)\n(ii) Why have sacred groves remained rich in species? (1 mark)\n(iii) How does a seed bank differ, and why are both needed? (2 marks)',
            '(i) In situ. (ii) Tribal communities protect them because of religious beliefs, so trees and wildlife are not cut or hunted. (iii) A seed bank is ex situ – seeds of different genetic strains are stored for long periods outside the habitat; in situ protects whole ecosystems and interactions while ex situ is a backup for threatened species and crop genetic resources.',
            '(i) 1 (ii) 1 (iii) 2.', ('case',))],
}

SPECS = {'ch09-st1': CH9S1, 'ch09-st2': CH9S2, 'ch09-st3': CH9S3,
         'ch10-st1': CH10S1, 'ch10-st2': CH10S2, 'ch10-st3': CH10S3,
         'ch11-st1': CH11S1, 'ch11-st2': CH11S2, 'ch11-st3': CH11S3,
         'ch12-st1': CH12S1, 'ch12-st2': CH12S2, 'ch12-st3': CH12S3,
         'ch13-st1': CH13S1, 'ch13-st2': CH13S2, 'ch13-st3': CH13S3}
FAMILIES = build_all(P, SPECS)
