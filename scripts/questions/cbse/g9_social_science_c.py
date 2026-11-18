"""CBSE class 9 social science fact tables, chapters 11-15 (with computed personal-finance items)."""
from qbank import name, inr, num


def budget(r):
    who = name(r)
    inc = r.randrange(25, 90) * 1000
    items = {'rent': r.randrange(15, 30), 'food': r.randrange(20, 30), 'transport': r.randrange(5, 10),
             'school fees': r.randrange(8, 15), 'electricity and phone': r.randrange(3, 7)}
    spend = {k: round(inc * v / 100 / 100) * 100 for k, v in items.items()}
    tot = sum(spend.values())
    bal = inc - tot
    lines = ', '.join(f'{k} {inr(v)}' for k, v in spend.items())
    kind = 'surplus' if bal > 0 else ('deficit' if bal < 0 else 'balanced budget')
    return {'stem': f'{who}\'s family earns {inr(inc)} a month. Its monthly spending is: {lines}. Find the total expenditure and state whether the budget is in surplus or deficit, and by how much.',
            'answer': f'Total expenditure {inr(tot)}; {kind} of {inr(abs(bal))}' if bal else f'Total expenditure {inr(tot)}; balanced budget',
            'key': f'Total = {" + ".join(inr(v) for v in spend.values())} = {inr(tot)} (1 mark); income − expenditure = {inr(inc)} − {inr(tot)} = {inr(bal)} (1 mark); {kind} (1 mark).',
            'marks': 3, 'minutes': 4}


def saving_rate(r):
    who = name(r)
    inc = r.randrange(20, 80) * 1000
    pct = r.choice([10, 12, 15, 20, 25])
    s = inc * pct // 100
    return {'stem': f'{who} earns {inr(inc)} a month and saves {inr(s)}. What percentage of income is saved?',
            'answer': f'{pct} per cent',
            'key': f'{inr(s)} ÷ {inr(inc)} × 100 = {pct} per cent.',
            'distractors': [f'{pct + 5} per cent', f'{pct * 2} per cent', f'{100 - pct} per cent']}


def simple_interest(r):
    who = name(r)
    p = r.randrange(10, 100) * 1000
    rate = r.choice([4, 5, 6, 7, 8, 9])
    t = r.choice([2, 3, 4, 5])
    si = p * rate * t // 100
    return {'stem': f'{who} deposits {inr(p)} in a bank fixed deposit at {rate} per cent simple interest per year for {t} years. Find the interest and the amount at maturity.',
            'answer': f'Interest {inr(si)}; amount {inr(p + si)}',
            'key': f'SI = P × R × T ÷ 100 = {inr(p)} × {rate} × {t} ÷ 100 = {inr(si)}; amount = {inr(p)} + {inr(si)} = {inr(p + si)}.',
            'distractors': [f'Interest {inr(p * rate // 100)}; amount {inr(p + p * rate // 100)}', f'Interest {inr(si * 2)}; amount {inr(p + si * 2)}',
                            f'Interest {inr(si)}; amount {inr(si)}'], 'marks': 2, 'minutes': 3}


def compound_interest(r):
    who = name(r)
    p = r.randrange(10, 60) * 1000
    rate = r.choice([5, 8, 10])
    a = p * (1 + rate / 100) ** 2
    ci = a - p
    si = p * rate * 2 / 100
    return {'stem': (f'{who} invests {inr(p)} for 2 years at {rate} per cent per year compounded annually. Find the compound interest and compare it with the simple interest '
                     f'for the same period. Why is there a difference?'),
            'answer': f'CI = {inr(round(ci, 2))}; SI = {inr(si)}; CI is more by {inr(round(ci - si, 2))} because interest is earned on interest',
            'key': f'A = {inr(p)} × (1 + {rate}/100)² = {inr(round(a, 2))}; CI = {inr(round(ci, 2))} (1 mark); SI = {inr(si)} (1 mark); difference arises because second-year interest is also earned on first-year interest (1 mark).',
            'marks': 3, 'minutes': 5}


def loan_cost(r):
    who = name(r)
    p = r.randrange(20, 100) * 1000
    bank = r.choice([9, 10, 11, 12])
    lender = r.choice([24, 30, 36, 48])
    t = r.choice([1, 2])
    ib, il = p * bank * t // 100, p * lender * t // 100
    return {'stem': (f'{who} needs a loan of {inr(p)} for {t} year{"s" if t > 1 else ""}. A bank charges {bank} per cent simple interest per year and a local moneylender charges {lender} per cent. '
                     f'How much more interest would {who} pay to the moneylender, and why do many poor families still borrow from moneylenders?'),
            'answer': f'{inr(il - ib)} more; banks ask for collateral and documents that poor families often lack',
            'key': f'Bank interest {inr(ib)}, moneylender {inr(il)}, difference {inr(il - ib)} (2 marks); reason: lack of collateral/documents, easy and quick informal credit (1 mark).',
            'marks': 3, 'minutes': 5}


DATA = {
    # ---------------- ch11 Life on Earth
    '11-st1': dict(
        T=[('biosphere', 'the narrow zone of the Earth where land, water and air meet and support life'),
           ('ecosystem', 'a community of living things interacting with each other and with their non-living environment'),
           ('food chain', 'a sequence showing who eats whom, starting with a green plant'),
           ('producers', 'green plants that make their own food using sunlight'),
           ('decomposers', 'organisms such as bacteria and fungi that break down dead plants and animals')],
        FB=[('In a food chain, green plants are ___.', 'producers', ['primary consumers', 'decomposers', 'carnivores']),
            ('Herbivores are called ___ consumers.', 'primary', ['secondary', 'tertiary', 'final']),
            ('Only about ___ per cent of energy is passed on from one level of a food chain to the next.', '10', ['50', '90', '1']),
            ('Bacteria and fungi that break down dead matter are ___.', 'decomposers', ['producers', 'herbivores', 'predators']),
            ('Many interlinked food chains together form a food ___.', 'web', ['pyramid only', 'cycle', 'line'])],
        EX=[('C2', 'D2', 'Why are decomposers important in an ecosystem?', ['they break down dead plants and animals', 'they return nutrients to the soil for plants to use']),
            ('C2', 'D3', 'Why do food chains rarely have more than four or five levels?', ['energy decreases at each level', 'too little energy is left to support more levels']),
            ('C3', 'D3', 'Build a food chain from a grassland with four links and name the role of each.', ['grass – producer', 'grasshopper – primary consumer', 'frog – secondary consumer', 'snake – tertiary consumer']),
            ('C4', 'D4', 'What would happen to a forest ecosystem if all tigers were removed? Analyse.', ['deer and other herbivores would multiply', 'overgrazing would damage vegetation', 'soil erosion and loss of other species may follow', 'the balance of the ecosystem would be disturbed'])],
        AR=[('Energy flow in an ecosystem is one-way.', 'Energy passes from the Sun to producers and then to consumers, and is lost as heat at each level.', 'a', 'R explains A.')],
    ),
    '11-st2': dict(
        T=[('biome', 'a large natural region with a distinct type of climate, vegetation and animal life'),
           ('tropical evergreen forests', 'dense forests of regions with over 200 cm of rainfall, which do not shed leaves at one time'),
           ('tropical deciduous forests', 'monsoon forests that shed leaves in the dry season, such as teak and sal forests'),
           ('thorn forests', 'forests of thorny trees and bushes in areas with less than 70 cm of rainfall'),
           ('mangrove forests', 'tidal forests of coastal deltas, such as the Sundarbans')],
        FB=[('The most widespread forests of India are the tropical ___ forests.', 'deciduous', ['evergreen', 'thorn', 'mangrove']),
            ('Sundari trees are found in the ___ forests.', 'mangrove', ['thorn', 'montane', 'deciduous']),
            ('Teak and sal are important trees of the ___ forests.', 'tropical deciduous', ['mangrove', 'thorn', 'alpine']),
            ('Acacia, babool and cactus are typical of ___ forests.', 'thorn', ['evergreen', 'mangrove', 'montane']),
            ('Tropical evergreen forests grow where rainfall is more than ___ cm.', '200', ['50', '70', '100']),
            ('The coniferous forest biome of the cold northern regions is called the ___.', 'taiga', ['tundra', 'savanna', 'steppe'])],
        EX=[('C2', 'D2', 'Why do tropical deciduous trees shed their leaves?', ['to reduce loss of water in the dry season', 'there is not enough water for leaves throughout the year']),
            ('C3', 'D3', 'Match each forest type of India with its rainfall and a region.', ['evergreen – over 200 cm – Western Ghats and north-east', 'deciduous – 70 to 200 cm – central India', 'thorn – below 70 cm – Rajasthan and Gujarat']),
            ('C4', 'D3', 'Explain how rainfall and temperature decide the natural vegetation of a region.', ['heavy rainfall and heat give dense evergreen forests', 'moderate seasonal rainfall gives deciduous forests', 'low rainfall gives thorny scrub', 'cold mountain climates give coniferous and alpine vegetation'])],
        AR=[('Mangrove forests grow in the deltas of the Ganga and Mahanadi.', 'Mangroves can survive in salty, tidal water.', 'a', 'R explains A.')],
        CAT=[('a tree of the tropical deciduous forests', 'trees of the tropical deciduous forests', ['teak', 'sal', 'sandalwood', 'shisham', 'khair'], ['sundari', 'deodar', 'cactus', 'pine'])],
        MAP=[('the Sundarbans', 'Sundarbans', 'West Bengal', 'India'), ('the Western Ghats evergreen forests', 'Western Ghats', 'along the west coast', 'India'),
             ('the thorn forests of Rajasthan', 'western Rajasthan', 'Rajasthan', 'India')],
    ),
    '11-st3': dict(
        T=[('biodiversity', 'the variety of plants, animals and micro-organisms in a region'),
           ('biodiversity hotspot', 'a region very rich in species, many found nowhere else, that is under threat'),
           ('endemic species', 'species found only in one particular area'),
           ('megadiverse country', 'one of the few countries that hold a very large share of the world\'s species')],
        FB=[('The Asiatic lion is found in the wild only in the ___ forest of Gujarat.', 'Gir', ['Kaziranga', 'Sundarbans', 'Corbett']),
            ('The one-horned rhinoceros is found in ___ National Park in Assam.', 'Kaziranga', ['Gir', 'Periyar', 'Bandipur']),
            ('India has ___ of the world\'s 36 biodiversity hotspots.', 'four', ['two', 'eight', 'ten']),
            ('The Royal Bengal tiger lives in the mangroves of the ___.', 'Sundarbans', ['Thar', 'Ladakh', 'Rann of Kachchh']),
            ('Cheetahs were brought back to India in 2022 at ___ National Park.', 'Kuno', ['Gir', 'Ranthambore', 'Kanha'])],
        EX=[('C2', 'D2', 'Why is India called a megadiverse country?', ['it has a large share of the world\'s plant and animal species', 'its varied climate and relief support many ecosystems']),
            ('C3', 'D3', 'Name the four biodiversity hotspots that include parts of India.', ['the Himalaya', 'Indo-Burma (north-east)', 'Western Ghats and Sri Lanka', 'Sundaland (Nicobar Islands)']),
            ('C4', 'D4', 'Why is the Western Ghats region rich in endemic species?', ['heavy rainfall and varied altitude create many habitats', 'long isolation allowed species to evolve separately', 'dense forests provide shelter for unique species'])],
        AR=[('The Asiatic lion is found only in Gujarat.', 'Gir forest is the last natural home of the Asiatic lion.', 'a', 'R explains A.')],
        MAP=[('Gir National Park', 'Gir', 'Gujarat', 'India'), ('Kaziranga National Park', 'Kaziranga', 'Assam', 'India'), ('Kuno National Park', 'Kuno', 'Madhya Pradesh', 'India'),
             ('Jim Corbett National Park', 'Corbett', 'Uttarakhand', 'India'), ('Periyar Tiger Reserve', 'Periyar', 'Kerala', 'India')],
    ),
    '11-st4': dict(
        T=[('Project Tiger', 'the conservation programme launched in 1973 to save tigers in reserves'),
           ('biosphere reserve', 'a large protected area that conserves ecosystems while allowing sustainable use by local people'),
           ('poaching', 'illegal hunting or capture of wild animals'),
           ('invasive species', 'species brought from elsewhere that spread and harm local plants and animals')],
        FB=[('Project Tiger was launched in ___.', '1973', ['1972', '1992', '1986']),
            ('The Wildlife (Protection) Act was passed in ___.', '1972', ['1973', '1986', '2002']),
            ('Project Elephant was launched in ___.', '1992', ['1973', '1986', '2005']),
            ('The first biosphere reserve of India was ___.', 'Nilgiri', ['Sundarbans', 'Nanda Devi', 'Gulf of Mannar']),
            ('The ___ is a critically endangered bird found mainly in Rajasthan.', 'Great Indian Bustard', ['peacock', 'house sparrow', 'pigeon'])],
        EX=[('C2', 'D2', 'Why is biodiversity declining?', ['forests are cleared for farms, mines and towns', 'poaching, pollution and invasive species']),
            ('C3', 'D3', 'Describe three steps taken by the Government of India to conserve wildlife.', ['Wildlife (Protection) Act, 1972', 'national parks, sanctuaries and biosphere reserves', 'Project Tiger and Project Elephant']),
            ('C4', 'D3', 'How can local communities help conserve biodiversity? Give examples.', ['sacred groves protected by communities', 'Bishnois protect blackbuck and trees', 'joint forest management with villagers', 'community reserves and eco-tourism'])],
        AR=[('Tiger numbers in India have increased in recent decades.', 'Project Tiger created protected reserves and checked poaching.', 'a', 'R explains A.')],
        CHRON=[('Wildlife (Protection) Act', 1972), ('Project Tiger', 1973), ('Nilgiri, the first biosphere reserve', 1986), ('Project Elephant', 1992), ('cheetahs reintroduced at Kuno', 2022)],
    ),
    # ---------------- ch12 Resistance and Resilience (1000–1700 CE)
    '12-st1': dict(
        T=[('raid', 'a sudden attack to seize wealth, without staying to rule'),
           ('Kitab-ul-Hind', 'the book on India written by the scholar Al-Biruni, who came with Mahmud of Ghazni'),
           ('Battles of Tarain', 'the battles of 1191 and 1192 between Prithviraj Chauhan and Muhammad Ghori')],
        FB=[('Mahmud of Ghazni attacked the Somnath temple in ___.', '1025', ['1191', '1206', '1000']),
            ('Prithviraj Chauhan defeated Muhammad Ghori in the First Battle of Tarain in ___.', '1191', ['1192', '1206', '1175']),
            ('Muhammad Ghori defeated Prithviraj Chauhan in the Second Battle of Tarain in ___.', '1192', ['1191', '1206', '1236']),
            ('The scholar ___ came with Mahmud of Ghazni and wrote about Indian society and science.', 'Al-Biruni', ['Ibn Battuta', 'Amir Khusrau', 'Abul Fazl']),
            ('Prithviraj Chauhan belonged to the ___ dynasty.', 'Chahamana (Chauhan)', ['Chola', 'Rashtrakuta', 'Pala'])],
        EX=[('C2', 'D2', 'Why did Mahmud of Ghazni raid India repeatedly?', ['to seize the wealth of temples and cities', 'to use it to build his kingdom in Ghazni']),
            ('C3', 'D3', 'Compare the First and Second Battles of Tarain.', ['1191: Prithviraj Chauhan defeated Muhammad Ghori', '1192: Ghori returned with a larger army and won', 'the second battle opened north India to Ghori\'s rule']),
            ('C4', 'D3', 'Why were the north Indian kingdoms unable to stop invasions from the north-west? Analyse.', ['rivalries among Rajput kingdoms', 'invaders used fast mounted archers', 'lack of a common defence of the north-west passes'])],
        AR=[('Al-Biruni\'s writings are a valuable source on eleventh-century India.', 'He learnt Sanskrit and studied Indian science, religion and society.', 'a', 'R explains A.')],
        CHRON=[('Mahmud of Ghazni\'s raid on Somnath', 1025), ('First Battle of Tarain', 1191), ('Second Battle of Tarain', 1192), ('founding of the Delhi Sultanate', 1206)],
        MAP=[('Somnath', 'Somnath', 'Gujarat', 'India'), ('Tarain', 'Tarain (Taraori)', 'Haryana', 'India'), ('Ajmer, Chauhan capital', 'Ajmer', 'Rajasthan', 'India')],
    ),
    '12-st2': dict(
        T=[('Ahoms', 'the people who came to the Brahmaputra valley in the thirteenth century and ruled Assam for about 600 years'),
           ('Vijay Stambh', 'the victory tower built at Chittor by Rana Kumbha of Mewar'),
           ('Kakatiyas', 'the dynasty of Warangal, whose ruler Rudramadevi was a famous queen')],
        FB=[('The Ahom kingdom was founded by ___ in 1228.', 'Sukaphaa', ['Lachit Borphukan', 'Sankaradeva', 'Rudra Singha']),
            ('The Ahoms defeated the Mughals at the Battle of Saraighat in ___.', '1671', ['1576', '1526', '1707']),
            ('Rudramadevi ruled the Kakatiya kingdom from ___.', 'Warangal', ['Hampi', 'Devagiri', 'Madurai']),
            ('The Vijay Stambh at Chittorgarh was built by ___.', 'Rana Kumbha', ['Rana Sanga', 'Maharana Pratap', 'Bappa Rawal']),
            ('Rani Abbakka of Ullal resisted the ___.', 'Portuguese', ['Mughals', 'Dutch', 'British']),
            ('Hemu was defeated by Akbar\'s forces at the Second Battle of Panipat in ___.', '1556', ['1526', '1576', '1761'])],
        EX=[('C2', 'D2', 'Why could the Ahoms rule Assam for about six centuries?', ['the paik system gave a large force of trained men', 'they adapted to the land, absorbed local people and fought skilfully on rivers']),
            ('C3', 'D3', 'Name three rulers or leaders who resisted the Sultanate or the Mughals and the region of each.', ['Maharana Pratap – Mewar', 'Rani Durgavati – Gondwana', 'Lachit Borphukan – Assam', 'Chand Bibi – Ahmadnagar']),
            ('C4', 'D3', 'Explain why resistance to the Sultanate and Mughals was strong in hilly, forest and river regions.', ['difficult terrain slowed large armies', 'local people knew the land and supported their rulers', 'guerrilla and river warfare suited these regions']),
            ('C4', 'D4', 'Evaluate the role of women rulers in resisting powerful empires, with examples.', ['Rani Durgavati fought Akbar\'s forces in 1564', 'Chand Bibi defended Ahmadnagar', 'Rani Abbakka resisted the Portuguese', 'Rudramadevi defended the Kakatiya kingdom'])],
        AR=[('The Mughals could not conquer Assam permanently.', 'The Ahoms used their knowledge of rivers and terrain to resist.', 'a', 'R explains A.')],
        CHRON=[('founding of the Ahom kingdom by Sukaphaa', 1228), ('Second Battle of Panipat', 1556), ('Rani Durgavati\'s last battle', 1564), ('Battle of Haldighati', 1576), ('Battle of Saraighat', 1671)],
        MAP=[('Saraighat', 'Saraighat', 'Assam (Guwahati)', 'India'), ('Warangal', 'Warangal', 'Telangana', 'India'), ('Chittorgarh', 'Chittorgarh', 'Rajasthan', 'India'),
             ('Ullal', 'Ullal', 'Karnataka (near Mangaluru)', 'India'), ('Haldighati', 'Haldighati', 'Rajasthan', 'India')],
    ),
    '12-st3': dict(
        T=[('miri-piri', 'Guru Hargobind\'s idea of combining spiritual and temporal authority'),
           ('Akal Takht', 'the seat of temporal authority built by Guru Hargobind at Amritsar'),
           ('war of Maratha independence', 'the long resistance of the Marathas to Aurangzeb from the 1680s to 1707 under Sambhaji, Rajaram and Tarabai')],
        FB=[('Guru Hargobind built the ___ at Amritsar.', 'Akal Takht', ['Golden Temple', 'Anandpur fort', 'Kartarpur gurdwara']),
            ('After Rajaram\'s death, the Maratha resistance to Aurangzeb was led by ___.', 'Tarabai', ['Jijabai', 'Ahilyabai', 'Yesubai']),
            ('Banda Singh Bahadur captured ___ in 1710.', 'Sirhind', ['Lahore', 'Delhi', 'Multan']),
            ('Sambhaji was executed on Aurangzeb\'s orders in ___.', '1689', ['1680', '1707', '1674']),
            ('Aurangzeb died in the Deccan in ___.', '1707', ['1689', '1720', '1761'])],
        EX=[('C2', 'D2', 'Why did Aurangzeb fail to crush the Marathas despite spending decades in the Deccan?', ['the Marathas used guerrilla warfare from hill forts', 'leaders like Rajaram and Tarabai kept the resistance alive']),
            ('C3', 'D3', 'Explain how the Sikh community became a force of resistance.', ['martyrdom of Guru Arjan and Guru Tegh Bahadur', 'Guru Hargobind\'s miri-piri and the Akal Takht', 'Guru Gobind Singh founded the Khalsa in 1699', 'Banda Singh Bahadur fought the Mughals in Punjab']),
            ('C4', 'D4', 'Compare the Maratha and Sikh resistance to the Mughals.', ['both drew on local support and faith', 'Marathas used hill forts and guerrilla tactics in the Deccan', 'Sikhs built the Khalsa and fought in Punjab', 'both weakened Mughal power in the eighteenth century'])],
        AR=[('The Deccan wars drained Mughal resources.', 'Aurangzeb fought the Marathas for over twenty-five years.', 'a', 'R explains A.')],
        CHRON=[('coronation of Shivaji', 1674), ('execution of Sambhaji', 1689), ('founding of the Khalsa', 1699), ('death of Aurangzeb', 1707), ('Banda Singh Bahadur captures Sirhind', 1710)],
    ),
    '12-st4': dict(
        T=[('resilience', 'the ability of a society to recover and continue its traditions after conflict'),
           ('Kerala school of mathematics', 'the tradition of mathematicians such as Madhava of Sangamagrama who worked on infinite series'),
           ('temple town', 'a town that grew around a major temple, such as Madurai or Puri')],
        FB=[('The Kerala mathematician ___ worked on infinite series for trigonometric functions.', 'Madhava of Sangamagrama', ['Aryabhata', 'Brahmagupta', 'Bhaskara I']),
            ('The Somnath temple was rebuilt after independence and inaugurated in ___.', '1951', ['1947', '1961', '1971']),
            ('Nilakantha Somayaji of the Kerala school wrote the ___.', 'Tantrasangraha', ['Aryabhatiya', 'Lilavati', 'Ashtadhyayi']),
            ('Despite wars, Indian cotton textiles continued to be exported across the ___ Ocean.', 'Indian', ['Arctic', 'Southern', 'Pacific'])],
        EX=[('C2', 'D2', 'How did Indian culture show resilience between 1000 and 1700 CE?', ['temples and learning centres were rebuilt', 'literature, music and crafts continued to flourish in many regions']),
            ('C3', 'D3', 'Give three examples of continuity in Indian economy and knowledge in this period.', ['textile and spice trade continued', 'the Kerala school developed mathematics', 'Ayurveda and Sanskrit learning continued', 'Bhakti literature grew in regional languages']),
            ('C4', 'D5', '"The history of 1000–1700 CE is not only of conquest but also of continuity." Evaluate.', ['many regional kingdoms resisted and survived', 'villages, crafts and trade continued', 'new forms of art, music and architecture emerged', 'languages and religious movements grew'])],
        AR=[('Indian textiles remained in demand abroad in the seventeenth century.', 'Indian weavers produced fine cotton and silk cloth.', 'a', 'R explains A.')],
    ),
    # ---------------- ch13 Governance and Public Policy
    '13-st1': dict(
        T=[('governance', 'the process by which decisions are made and implemented by institutions'),
           ('accountability', 'the duty of those in power to explain and answer for their actions'),
           ('transparency', 'openness in government so that citizens can see how decisions are made'),
           ('Citizen\'s Charter', 'a public statement by a department listing the services it provides and their time limits')],
        FB=[('Answering to the people for one\'s actions is called ___.', 'accountability', ['sovereignty', 'secrecy', 'federalism']),
            ('Making information about decisions open to the public is called ___.', 'transparency', ['censorship', 'delegation', 'devolution']),
            ('The civil servant who heads a district administration is the ___.', 'District Collector', ['Mayor', 'Sarpanch', 'Speaker'])],
        EX=[('C2', 'D2', 'Why is transparency important in governance?', ['it helps citizens check misuse of power', 'it reduces corruption and builds trust']),
            ('C3', 'D3', 'State three features of good governance.', ['accountability', 'transparency', 'rule of law', 'responsiveness and efficiency']),
            ('C4', 'D3', 'How can a Citizen\'s Charter improve public services?', ['citizens know what services to expect and in how much time', 'officials can be held responsible for delays', 'it encourages efficiency and better behaviour'])],
        AR=[('Good governance requires accountability.', 'Those in power should answer for their decisions to the people.', 'a', 'R explains A.')],
    ),
    '13-st2': dict(
        T=[('public policy', 'a course of action chosen by the government to deal with a public problem'),
           ('agenda setting', 'the first stage of policy-making, when a problem is recognised as needing action'),
           ('implementation', 'the stage in which a policy is put into practice by government departments'),
           ('policy evaluation', 'checking whether a policy achieved its goals'),
           ('NITI Aayog', 'the policy think tank of the Government of India set up in 2015')],
        FB=[('NITI Aayog was set up on 1 January ___.', '2015', ['2010', '1950', '2020']),
            ('The stage in which a problem is recognised as needing action is called ___.', 'agenda setting', ['evaluation', 'implementation', 'adoption']),
            ('Checking whether a policy has achieved its goals is called policy ___.', 'evaluation', ['formulation', 'agenda setting', 'adoption']),
            ('The National Education Policy was released in ___.', '2020', ['2010', '1986', '2015'])],
        EX=[('C2', 'D2', 'Why must policies be evaluated after implementation?', ['to find out whether they achieved their goals', 'to correct problems and improve them']),
            ('C3', 'D3', 'Arrange and explain the stages of the public policy cycle.', ['agenda setting', 'formulation of options and adoption of a policy', 'implementation by departments', 'evaluation and revision']),
            ('C4', 'D4', 'A state government wants to reduce school dropouts. Show how it would move through the policy cycle.', ['agenda: data show high dropout rates', 'formulation: options such as scholarships, meals or bicycles', 'adoption and implementation through schools', 'evaluation: compare dropout rates later'])],
        AR=[('Policies often change after evaluation.', 'Evaluation shows what worked and what did not.', 'a', 'R explains A.')],
        CAT=[('a stage of the public policy cycle', 'stages of the public policy cycle', ['agenda setting', 'formulation', 'implementation', 'evaluation'], ['impeachment', 'delimitation', 'judicial review', 'no-confidence motion'])],
    ),
    '13-st3': dict(
        T=[('welfare policy', 'a government policy to improve the well-being of people, especially the poor'),
           ('Public Distribution System', 'the system of supplying subsidised food grains through ration shops'),
           ('PM POSHAN', 'the scheme of hot cooked meals for children in government schools, earlier called the mid-day meal scheme'),
           ('Ayushman Bharat PM-JAY', 'the health scheme that gives poor families hospital cover of up to ₹5 lakh a year')],
        FB=[('The National Food Security Act was passed in ___.', '2013', ['2005', '2009', '2019']),
            ('The Right of Children to Free and Compulsory Education Act was passed in ___.', '2009', ['2002', '2013', '2020']),
            ('Under Ayushman Bharat PM-JAY, eligible families get health cover of up to ___ per year.', '₹5 lakh', ['₹50,000', '₹1 lakh', '₹10 lakh']),
            ('Under the National Food Security Act, eligible persons get ___ kg of food grains per month.', '5', ['2', '10', '35']),
            ('Ration shops are part of the ___.', 'Public Distribution System', ['Reserve Bank of India', 'Election Commission', 'stock market'])],
        EX=[('C2', 'D2', 'Why does the government run the Public Distribution System?', ['to provide food grains at low prices to the poor', 'to protect people from hunger and price rise']),
            ('C3', 'D3', 'Explain how the mid-day meal (PM POSHAN) scheme helps children.', ['improves nutrition', 'increases enrolment and attendance', 'reduces caste barriers as children eat together']),
            ('C4', 'D4', 'Evaluate the challenges in implementing welfare schemes in India.', ['leakages and corruption', 'exclusion of genuine beneficiaries', 'poor quality of services', 'lack of awareness among people'])],
        AR=[('The mid-day meal scheme has raised school attendance.', 'Children get a free hot meal at school.', 'a', 'R explains A.')],
    ),
    '13-st4': dict(
        T=[('Right to Information', 'the right of citizens to obtain information from public authorities under the RTI Act, 2005'),
           ('social audit', 'checking of a government programme by the people it is meant for, often in a public hearing'),
           ('e-governance', 'use of digital technology to deliver government services and information'),
           ('Direct Benefit Transfer', 'sending subsidies and benefits directly into beneficiaries\' bank accounts')],
        FB=[('The Right to Information Act was passed in ___.', '2005', ['2000', '2010', '1995']),
            ('Under the RTI Act, information must normally be given within ___ days.', '30', ['7', '60', '90']),
            ('Information concerning a person\'s life or liberty must be given within ___ hours under the RTI Act.', '48', ['24', '72', '12']),
            ('Social audits became mandatory under ___.', 'MGNREGA', ['the RTI Act', 'the Companies Act', 'the Wildlife Act']),
            ('The Digital India programme was launched in ___.', '2015', ['2005', '2010', '2020']),
            ('The Mazdoor Kisan Shakti Sangathan, which pioneered public hearings, began in ___.', 'Rajasthan', ['Kerala', 'Bihar', 'Punjab'])],
        EX=[('C2', 'D2', 'Why is the RTI Act called a powerful tool for citizens?', ['citizens can ask for information on how public money is spent', 'it exposes corruption and makes officials accountable']),
            ('C3', 'D3', 'Explain how e-governance makes services more efficient.', ['services such as certificates and bill payments can be had online', 'fewer visits to offices and less scope for bribes', 'records are digital and easy to track']),
            ('C4', 'D3', 'Evaluate the role of social audits in checking corruption in government schemes.', ['villagers check muster rolls and spending in public', 'false entries and ghost workers are exposed', 'it builds awareness and participation'])],
        AR=[('Direct Benefit Transfer reduces leakages.', 'Money goes directly into beneficiaries\' bank accounts without middlemen.', 'a', 'R explains A.')],
        SC=[('Mehak applied for a ration card six months ago but has heard nothing. Which tool can she use to find out the status of her application?', 'An application under the RTI Act',
             ['A no-confidence motion', 'A Public Interest Litigation in the Supreme Court first', 'A by-election'], 'RTI lets citizens seek information from public authorities.')],
    ),
    # ---------------- ch14 Managing Personal Finances
    '14-st1': dict(
        T=[('budget', 'a plan of expected income and expenditure for a period'),
           ('surplus budget', 'a budget in which income is more than expenditure'),
           ('deficit budget', 'a budget in which expenditure is more than income'),
           ('needs', 'things essential for living, such as food, shelter and health care'),
           ('wants', 'things that are desirable but not essential, such as a new phone or eating out')],
        FB=[('When expenditure is more than income, the budget is in ___.', 'deficit', ['surplus', 'balance', 'profit']),
            ('Food, shelter and medicines are examples of ___.', 'needs', ['wants', 'luxuries', 'investments']),
            ('A popular rule suggests spending 50 per cent on needs, 30 per cent on wants and ___ per cent on savings.', '20', ['10', '30', '5'])],
        EX=[('C2', 'D2', 'Why should a family make a budget?', ['to spend within its income', 'to plan savings for future needs and emergencies']),
            ('C3', 'D3', 'Classify into needs and wants: rent, a new video game, school fees, eating out, medicines, a branded jacket.', ['needs: rent, school fees, medicines', 'wants: video game, eating out, branded jacket', 'needs come first in a budget']),
            ('C4', 'D3', 'Suggest how a family with a deficit budget can balance it.', ['cut spending on wants', 'compare prices and avoid waste', 'find additional income', 'avoid new loans for consumption'])],
        AR=[('A budget helps a family save regularly.', 'It plans spending in advance within the family\'s income.', 'a', 'R explains A.')],
        GEN=[('C3', 'D3', 'numerical', budget, {'kinds': ('sa3',)}), ('C3', 'D1', 'short', saving_rate)],
    ),
    '14-st2': dict(
        T=[('savings account', 'a bank account for keeping savings that earns interest and allows withdrawals'),
           ('fixed deposit', 'money kept with a bank for a fixed period at a fixed rate of interest'),
           ('recurring deposit', 'a deposit in which a fixed sum is paid every month for a fixed period'),
           ('UPI', 'the Unified Payments Interface that lets people transfer money instantly using a mobile phone'),
           ('KYC', 'the "Know Your Customer" process by which a bank verifies identity and address')],
        FB=[('UPI was launched in 2016 by the ___.', 'National Payments Corporation of India', ['State Bank of India', 'SEBI', 'NITI Aayog']),
            ('The Pradhan Mantri Jan Dhan Yojana for bank accounts for all was launched in ___.', '2014', ['2004', '2016', '2020']),
            ('Bank deposits are insured by DICGC up to ___ per depositor per bank.', '₹5 lakh', ['₹1 lakh', '₹50,000', '₹25 lakh']),
            ('Banks in India are regulated by the ___.', 'Reserve Bank of India', ['SEBI', 'IRDAI', 'Election Commission']),
            ('Interest earned on interest is called ___ interest.', 'compound', ['simple', 'flat', 'nominal'])],
        EX=[('C2', 'D2', 'Why is it safer to keep savings in a bank than at home?', ['money is safe from theft and loss', 'it earns interest and deposits are insured']),
            ('C3', 'D3', 'Compare a savings account, a fixed deposit and a recurring deposit.', ['savings account: withdraw any time, lower interest', 'fixed deposit: lump sum locked for a period, higher interest', 'recurring deposit: fixed monthly payment, builds savings regularly']),
            ('C4', 'D3', 'Explain how digital payments have changed everyday transactions in India.', ['instant transfers through UPI using mobile phones', 'small shops and vendors accept QR payments', 'less need to carry cash', 'risk of fraud requires care with PINs and OTPs'])],
        AR=[('Compound interest grows faster than simple interest.', 'In compound interest, interest is also earned on past interest.', 'a', 'R explains A.')],
        GEN=[('C3', 'D2', 'numerical', simple_interest, {'kinds': ('sa2',)}), ('C4', 'D4', 'numerical', compound_interest, {'kinds': ('sa3',)})],
    ),
    '14-st3': dict(
        T=[('collateral', 'an asset such as land or gold that a borrower pledges to the lender as a guarantee'),
           ('EMI', 'the equated monthly instalment by which a loan is repaid'),
           ('debt trap', 'a situation in which a borrower takes new loans to repay old ones and cannot get out of debt'),
           ('credit score', 'a number that shows how reliably a person has repaid loans in the past')],
        FB=[('An asset pledged to the lender as a guarantee for a loan is called ___.', 'collateral', ['interest', 'principal', 'premium']),
            ('Informal lenders such as moneylenders usually charge ___ interest than banks.', 'higher', ['lower', 'the same', 'no']),
            ('A loan for buying a house is usually repaid through monthly ___.', 'EMIs', ['dividends', 'premiums', 'bonuses']),
            ('A good credit score helps a person get loans at ___ interest.', 'lower', ['higher', 'double', 'no'])],
        EX=[('C2', 'D2', 'Why do poor households often fall into a debt trap?', ['they borrow at high interest from moneylenders', 'crop failure or illness makes repayment impossible, so they borrow again']),
            ('C3', 'D3', 'Explain three precautions to take before taking a loan.', ['compare interest rates and charges', 'borrow only what can be repaid from income', 'read the terms carefully and borrow from a regulated lender']),
            ('C4', 'D3', 'Why are credit cards useful but risky?', ['they allow easy payments and short interest-free periods', 'unpaid dues attract very high interest', 'overspending can lead to debt'])],
        AR=[('Banks ask borrowers for collateral.', 'Collateral reduces the bank\'s risk if the borrower does not repay.', 'a', 'R explains A.')],
        GEN=[('C4', 'D4', 'numerical', loan_cost, {'kinds': ('sa3',)})],
    ),
    '14-st4': dict(
        T=[('insurance', 'a contract in which a person pays a premium and the insurer pays for a specified loss'),
           ('premium', 'the amount paid regularly to an insurance company'),
           ('mutual fund', 'a fund that pools money from many investors and invests it in shares, bonds and other assets'),
           ('diversification', 'spreading investments over different assets to reduce risk'),
           ('phishing', 'fraud in which criminals pose as a bank or company to steal passwords, PINs or OTPs')],
        FB=[('The stock market is regulated by ___.', 'SEBI', ['RBI', 'IRDAI', 'NABARD']),
            ('Insurance companies are regulated by ___.', 'IRDAI', ['SEBI', 'RBI', 'TRAI']),
            ('The national helpline number for reporting cyber financial fraud is ___.', '1930', ['100', '108', '1098']),
            ('Higher expected returns usually come with ___ risk.', 'higher', ['lower', 'no', 'fixed']),
            ('One should never share a bank ___ with anyone, even someone claiming to be from the bank.', 'OTP', ['branch address', 'IFSC code', 'name'])],
        EX=[('C2', 'D2', 'Why should young earners buy health insurance?', ['medical costs can be very high', 'insurance protects savings from being wiped out by illness']),
            ('C3', 'D3', 'State three ways to protect yourself from online financial fraud.', ['never share OTPs, PINs or passwords', 'do not click unknown links or download unknown apps', 'report fraud quickly to the bank and on 1930']),
            ('C4', 'D4', 'A scheme promises to double your money in three months. Evaluate whether you should invest.', ['such high, quick returns are unrealistic', 'it may be a Ponzi scheme using new investors\' money', 'check whether it is registered with SEBI or RBI', 'investments with higher returns carry higher risk'])],
        AR=[('Investors should diversify their savings.', 'Spreading money over different assets reduces the risk of a large loss.', 'a', 'R explains A.')],
        CAT=[('a regulator of the Indian financial system', 'regulators of the Indian financial system', ['RBI', 'SEBI', 'IRDAI', 'PFRDA'], ['NITI Aayog', 'Election Commission', 'UIDAI', 'ISRO'])],
    ),
    # ---------------- ch15 From Ideas to Startups
    '15-st1': dict(
        T=[('entrepreneur', 'a person who starts a business, bears its risks and organises resources'),
           ('entrepreneurship', 'the process of creating a new business or venture to meet a need'),
           ('innovation', 'a new idea, product or method that adds value'),
           ('risk-taking', 'willingness to act even when the outcome is uncertain')],
        FB=[('A person who starts a business and bears its risks is an ___.', 'entrepreneur', ['employee', 'investor only', 'consumer']),
            ('Bringing a new product or method into use is called ___.', 'innovation', ['inflation', 'imitation', 'taxation']),
            ('The reward of an entrepreneur for bearing risk is ___.', 'profit', ['wages', 'rent', 'interest'])],
        EX=[('C2', 'D2', 'Why is entrepreneurship important for India?', ['it creates jobs for many people', 'it brings new products and services and adds to growth']),
            ('C3', 'D3', 'List three qualities of a successful entrepreneur.', ['willingness to take risks', 'creativity and innovation', 'leadership and perseverance', 'ability to understand customers']),
            ('C4', 'D3', 'Why do many startups fail in their first few years? Analyse.', ['the product may not meet a real need', 'lack of funds', 'poor planning and management', 'strong competition'])],
        AR=[('Entrepreneurs earn profit.', 'They bear the risk of the business.', 'a', 'Profit is the reward for bearing risk.')],
    ),
    '15-st2': dict(
        T=[('prototype', 'an early model of a product made to test an idea'),
           ('minimum viable product', 'the simplest version of a product that can be tested with real users'),
           ('business plan', 'a document describing a business idea, its market, costs, funding and goals'),
           ('market research', 'collecting information about customers, their needs and competitors')],
        FB=[('An early working model of a product is called a ___.', 'prototype', ['patent', 'brand', 'licence']),
            ('Finding out what customers need and what competitors offer is ___.', 'market research', ['taxation', 'auditing', 'recycling']),
            ('Legal protection for a new invention is called a ___.', 'patent', ['dividend', 'debenture', 'subsidy'])],
        EX=[('C2', 'D2', 'Why should a startup begin by identifying a real problem?', ['customers pay only for solutions to their needs', 'it reduces the risk of making products no one wants']),
            ('C3', 'D3', 'Describe the steps from an idea to a product.', ['identify a problem and research the market', 'design and test a prototype', 'build a minimum viable product and get feedback', 'prepare a business plan and launch']),
            ('C4', 'D5', 'Students in Kavya\'s school find that many street vendors lose fruit because it spoils quickly. Propose a startup idea and outline a simple business plan.', ['problem: spoilage due to heat and no storage', 'idea: low-cost solar-powered cooling carts or boxes', 'customers: vendors and small shops; price affordable through rent or instalments', 'funding: savings, school incubator, small bank loan; test a prototype first'])],
        AR=[('Startups test a minimum viable product before a full launch.', 'Feedback from real users helps improve the product at low cost.', 'a', 'R explains A.')],
    ),
    '15-st3': dict(
        T=[('bootstrapping', 'starting a business with one\'s own savings and income from early sales'),
           ('angel investor', 'a wealthy individual who invests in an early-stage startup in return for a share'),
           ('venture capital', 'investment by firms in promising startups with high growth potential in return for ownership'),
           ('crowdfunding', 'raising small amounts of money from many people, usually online'),
           ('equity', 'a share of ownership in a company')],
        FB=[('Under the MUDRA scheme launched in 2015, the smallest category of loans is called ___.', 'Shishu', ['Kishor', 'Tarun', 'Bal']),
            ('Starting a business with one\'s own savings is called ___.', 'bootstrapping', ['crowdfunding', 'venture capital', 'leasing']),
            ('Raising small amounts from many people online is called ___.', 'crowdfunding', ['bootstrapping', 'mortgage', 'dividend']),
            ('A startup valued at over one billion US dollars is called a ___.', 'unicorn', ['tiger', 'pegasus', 'bull'])],
        EX=[('C2', 'D2', 'Why do venture capitalists ask for a share of ownership?', ['they take a big risk by investing in new firms', 'they hope to earn high returns when the company grows']),
            ('C3', 'D3', 'Compare three sources of funds for a startup.', ['own savings: no interest, but limited', 'bank loan: needs repayment with interest and often collateral', 'angel or venture capital: large funds in return for equity']),
            ('C4', 'D4', 'Why is risk an essential part of starting a business? Explain how founders can reduce it.', ['outcomes of new ideas are uncertain', 'test ideas with a prototype first', 'start small and grow step by step', 'diversify funding and keep costs low'])],
        AR=[('Angel investors take a share in the startup.', 'They provide early funds and bear the risk of failure.', 'a', 'R explains A.')],
        CAT=[('a source of startup funding', 'sources of startup funding', ['bootstrapping', 'angel investors', 'venture capital', 'bank loans', 'crowdfunding'], ['GST', 'income tax', 'dividend distribution', 'customs duty'])],
    ),
    '15-st4': dict(
        T=[('Startup India', 'the government initiative launched on 16 January 2016 to support startups'),
           ('incubator', 'an organisation that helps new startups with space, mentoring and networks'),
           ('Atal Innovation Mission', 'the government programme that sets up Atal Tinkering Labs in schools and incubators'),
           ('startup ecosystem', 'the network of founders, investors, incubators, universities and government that supports startups')],
        FB=[('Startup India was launched on 16 January ___.', '2016', ['2014', '2018', '2020']),
            ('Atal Tinkering Labs in schools are set up under the ___.', 'Atal Innovation Mission', ['Digital India', 'Skill India', 'Swachh Bharat']),
            ('National Startup Day in India is observed on ___.', '16 January', ['15 August', '2 October', '26 November']),
            ('Startups are recognised under Startup India by ___.', 'DPIIT', ['RBI', 'SEBI', 'UIDAI'])],
        EX=[('C2', 'D2', 'Why does the government support startups?', ['they create jobs and innovation', 'they help solve local problems and boost growth']),
            ('C3', 'D3', 'Explain three ways in which incubators help startups.', ['office space and equipment', 'mentoring by experts', 'links with investors and customers']),
            ('C4', 'D3', 'Analyse why Bengaluru has become a major startup hub.', ['many IT companies and skilled engineers', 'good institutions and incubators', 'availability of investors and mentors', 'a culture of innovation'])],
        AR=[('India has one of the largest startup ecosystems in the world.', 'A large market, skilled youth and government support encourage new ventures.', 'a', 'R explains A.')],
        CHRON=[('MUDRA scheme launched', 2015), ('Startup India launched', 2016), ('Flipkart founded in Bengaluru', 2007), ('National Startup Day declared', 2022)],
    ),
}
