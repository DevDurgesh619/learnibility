"""CBSE class 12 Geography, India: People and Economy (chapters 9-17): fact tables for g12_hum_engine."""
from g12_hum_engine import ST

S = 'cbse-g12-geography-ch'
INDIA = 'an outline political map of India'

CH09 = [ST(S + '09-st1', 'distribution and density of population in India', """
T: density of population | the number of persons per unit area, usually per sq km
T: physiological density | total population divided by net cultivated area
T: agricultural density | total agricultural population divided by net cultivable area
Q: According to Census 2011, India's population accounts for about what share of the world's population? | About 17.5 per cent | About 5 per cent | About 30 per cent | About 2.4 per cent
Q: Which state had the largest population according to Census 2011? | Uttar Pradesh | Maharashtra | Bihar | West Bengal
Q: According to Census 2011, the density of population of India was: | 382 persons per sq km | 103 persons per sq km | 1,102 persons per sq km | 17 persons per sq km
Q: Which state had the highest density of population in Census 2011? | Bihar | Kerala | Uttar Pradesh | West Bengal
Q: Which state had the lowest density of population in Census 2011? | Arunachal Pradesh | Sikkim | Mizoram | Himachal Pradesh
M:dens: Bihar | highest density (1,102 per sq km)
M:dens: Arunachal Pradesh | lowest density (17 per sq km)
M:dens: India | average density 382 per sq km
M:dens: Uttar Pradesh | largest population
S+: The population of India is unevenly distributed
S+: Uttar Pradesh has the largest population, followed by Maharashtra and Bihar
S+: The northern plains and the coastal areas have high densities of population
S+: Hilly, dry and forested regions such as Rajasthan's desert and Arunachal Pradesh have low densities
S+: Physiological density relates population to net cultivated area
S+: Density of population helps to understand the spatial distribution of population in relation to land
S-: Population is evenly distributed in India | It is very unevenly distributed, with high densities in the plains and low densities in hilly and dry areas
S-: Arunachal Pradesh had the highest density of population in 2011 | Bihar had the highest density; Arunachal Pradesh had the lowest
S-: Physiological density is population divided by total area | It is total population divided by net cultivated area
C: The northern plains are densely populated | they have flat land, fertile alluvial soil, water for irrigation and a long history of agriculture and settlement
C: Arunachal Pradesh has a very low density of population | it has rugged terrain, dense forests and difficult accessibility
X: C2 D2 2 | Distinguish between physiological density and agricultural density. | Physiological density – total population ÷ net cultivated area; agricultural density – total agricultural population ÷ net cultivable area.
X: C3 D3 3 | Explain the factors responsible for the uneven distribution of population in India. | Physical – relief, climate, water, soils (plains vs mountains and deserts); socio-economic – agriculture, industry, urbanisation, transport; historical – long settlement history of river plains.
L: D4 | Describe the distribution and density of population in India. | Uneven distribution; UP, Maharashtra, Bihar most populous; density 382 (2011); Bihar highest, Arunachal lowest; plains and coasts dense, hills and deserts sparse; physiological and agricultural density.
"""), ST(S + '09-st2', 'growth of population in India', """
T: growth of population | the change in the number of people living in a particular area between two points of time, expressed in absolute numbers and as a percentage
T: population explosion | the phase of very rapid growth of population in India between 1951 and 1981
T: decadal growth rate | the percentage change in population over a ten-year period
Q: The phase from 1901 to 1921 in India's population growth is described as: | a period of stagnant or stationary growth | population explosion | steady growth | declining but high growth
Q: The period 1951 to 1981 in India is known as the period of: | population explosion | stagnant growth | steady growth | negative growth
Q: The period 1921 to 1951 in India is referred to as the period of: | steady population growth | population explosion | stagnant growth | negative growth
Q: After 1981, the growth rate of India's population: | started slowing down gradually though it remained high | became negative | rose sharply every decade | remained exactly stable
M:phase: 1901–1921 | stagnant or stationary growth
M:phase: 1921–1951 | steady population growth
M:phase: 1951–1981 | population explosion
M:phase: after 1981 | high growth but declining rate
S+: Growth of population in India is described in four distinct phases since 1901
S+: In the first phase (1901–1921) both the birth rate and the death rate were high, so growth was very low
S+: In the second phase (1921–1951) improvements in health and sanitation brought down the mortality rate
S+: The period 1951–1981 saw a rapid fall in mortality while fertility remained high, causing a population explosion
S+: After 1981 the growth rate started declining gradually because of a downward trend in the birth rate
S+: Southern states such as Kerala and Tamil Nadu have recorded lower growth rates than many northern states
S-: The period 1951–1981 was a period of stagnant population | It was the period of population explosion
S-: In the first phase (1901–1921) the death rate was very low | Both birth and death rates were high in the first phase
S-: India's population growth rate has been rising every decade since 1981 | The growth rate has been declining gradually since 1981
C: India experienced a population explosion between 1951 and 1981 | mortality fell rapidly because of developmental activities and better health facilities while fertility remained high
C: Population growth was very slow between 1901 and 1921 | both birth and death rates were high, and epidemics and famines took many lives
C: The growth rate of population has been declining since 1981 | the birth rate has been falling as age at marriage rose and the quality of life, especially education of women, improved
X: C2 D2 2 | What is meant by population explosion? Which period of India's population history is known by this name? | Very rapid growth of population when mortality falls but fertility remains high; 1951–1981 in India.
X: C3 D3 3 | Explain the four phases of growth of population in India. | 1901–1921 stagnant (high birth and death rates); 1921–1951 steady growth (better health and sanitation); 1951–1981 population explosion (fall in mortality, high fertility); after 1981 high but declining growth (falling birth rate).
L: D4 | Describe the trends in the growth of India's population since 1901 and the reasons for regional variations. | Four phases with reasons; slowing after 1981; regional variation – southern states lower growth, many northern states higher; role of literacy, health, women's status.
"""), ST(S + '09-st3', "composition of India's population", """
T: main workers | persons who work for at least 183 days (six months) in a year
T: marginal workers | persons who work for less than 183 days (six months) in a year
T: sex ratio | the number of females per thousand males, as used in India
T: rural-urban composition | the division of population into those living in villages and those living in towns
Q: In India, sex ratio is defined as the number of: | females per thousand males | males per thousand females | children per thousand adults | females per hundred people
Q: Which language family has the largest number of speakers in India? | Indo-European (Aryan) | Dravidian | Austric | Sino-Tibetan
Q: Persons who work for less than six months in a year are called: | marginal workers | main workers | non-workers | cultivators
Q: Which religious group forms the largest minority in India? | Muslims | Christians | Sikhs | Buddhists
Q: The Dravidian family of languages is also called: | Dravida | Kirata | Nishada | Aryan
M:lang: Austric | Nishada
M:lang: Dravidian | Dravida
M:lang: Sino-Tibetan | Kirata
M:lang: Indo-European | Aryan
S+: The majority of India's population lives in rural areas
S+: Indian languages belong to four language families: Austric, Dravidian, Sino-Tibetan and Indo-European
S+: The Census of India divides the population into main workers, marginal workers and non-workers
S+: Workers are grouped as cultivators, agricultural labourers, household industry workers and other workers
S+: Hindus form the majority in most states, and Muslims are the largest religious minority
S+: Sikhs are concentrated mostly in Punjab, Haryana and Delhi
S-: The majority of India's population lives in urban areas | The majority lives in rural areas
S-: Main workers work for less than 183 days in a year | Main workers work for at least 183 days; marginal workers for less
S-: The Sino-Tibetan family of languages is called Aryan | It is called Kirata; the Indo-European family is called Aryan
C: A large share of India's workers are engaged in the primary sector | agriculture is still the main source of livelihood in rural India
C: India's sex ratio has been unfavourable to females in many states | female foeticide, female infanticide and neglect of girls and women have reduced the number of females
X: C2 D2 2 | Distinguish between main workers and marginal workers. | Main workers – work at least 183 days (six months) a year; marginal workers – work less than 183 days a year.
X: C3 D3 3 | Name the four language families of India and their ancient names. | Austric – Nishada; Dravidian – Dravida; Sino-Tibetan – Kirata; Indo-European – Aryan.
L: D4 | Explain the rural-urban, linguistic, religious and occupational composition of India's population. | Majority rural; four language families; religious composition – Hindus majority, Muslims largest minority, Sikhs in Punjab-Haryana-Delhi, Christians on west coast and NE; workers – main, marginal, non-workers; four categories of workers.
"""), ST(S + '09-st4', 'adolescent population and the National Youth Policy', """
T: adolescent population | the population in the age group of 10 to 19 years
T: National Youth Policy | the policy of the Government of India for the overall development of the youth and adolescent population
Q: The adolescent population is generally the age group of: | 10–19 years | 0–9 years | 20–29 years | 60 years and above
Q: Which of the following is a challenge faced by adolescents in India? | Drug abuse and early marriage | Excess of employment | Very high literacy | Old-age dependency
Q: The National Youth Policy aims at: | the all-round development of the youth | reducing literacy | stopping migration completely | increasing child marriage
S+: Adolescents are generally grouped in the age group of 10 to 19 years
S+: Adolescents are the most dynamic and productive potential of a society if properly guided
S+: Challenges for adolescents include lack of education, drug abuse, early marriage, high maternal mortality and HIV/AIDS
S+: The National Youth Policy stresses the empowerment of youth and their participation in national development
S+: Adolescents need proper guidance and channelisation of their energies
S-: Adolescents are people in the age group of 20 to 35 years | Adolescents are generally in the age group of 10 to 19 years
S-: Adolescents face no social challenges in India | They face challenges such as illiteracy, drug abuse, early marriage and maternal mortality among adolescent mothers
S-: The National Youth Policy discourages youth participation in development | It encourages the empowerment and participation of youth
C: Adolescents are an important resource for the country | they are the most dynamic and productive section if properly guided
C: Early marriage of adolescent girls is a concern | it leads to high maternal mortality and poor health of mothers and children
X: C2 D2 2 | Mention any two challenges faced by the adolescent population in India. | Illiteracy, drug abuse and alcoholism, early marriage, high maternal mortality, HIV/AIDS, lack of guidance (any two).
L: D4 | Explain the importance of the adolescent population and the measures needed for their development. | Age group 10–19; dynamic and productive; challenges – illiteracy, drugs, early marriage, maternal mortality, HIV/AIDS; measures – education, health, skills, National Youth Policy, empowerment and participation.
""")]

CH10 = [ST(S + '10-st1', 'types of rural settlements in India', """
T: clustered settlement | a compact, closely built-up rural settlement, also called agglomerated or nucleated
T: semi-clustered settlement | a fragmented settlement that results from the tendency of clustering in a restricted area of a dispersed settlement
T: hamleted settlement | a settlement fragmented into several units physically separated from each other but bearing a common name
T: dispersed settlement | an isolated settlement of huts or hamlets in remote jungles, small hills or on slopes
Q: Hamlets are locally called panna, para, palli, nagla and: | dhani | basti | kasba | mandi
Q: Clustered settlements are commonly found in the: | northern plains and north-eastern states | Kerala backwaters | Thar desert dunes alone | high Himalayas only
Q: Dispersed settlements are found in: | Meghalaya, Uttarakhand, Himachal Pradesh and Kerala | the Ganga plains | Punjab and Haryana | the Gujarat plain only
Q: In Rajasthan, compact settlements are mainly the result of: | scarcity of water | the need for defence only | fertile soils | dense forests
M:rural: clustered | northern plains and north-eastern states
M:rural: semi-clustered | Gujarat plain and parts of Rajasthan
M:rural: hamleted | middle and lower Ganga plain and Chhattisgarh
M:rural: dispersed | Meghalaya, Uttarakhand, Himachal Pradesh and Kerala
S+: Rural settlements in India can be broadly put into four types: clustered, semi-clustered, hamleted and dispersed
S+: In Bundelkhand and Nagaland people live in compact villages for security or defence
S+: In Rajasthan, scarcity of water has led to compact settlements
S+: Hamleted settlements are often caused by social and ethnic factors
S+: Dispersed settlements result from the extremely fragmented nature of the terrain and the land resource base
S-: Dispersed settlements are typical of the fertile northern plains | Clustered settlements are typical there; dispersed ones are found in hilly and forested areas
S-: Hamleted settlements have a single compact block of houses | They are fragmented into several separate units with a common name
S-: Physical features play no role in the type of rural settlement | Relief, altitude, drainage and water table strongly influence settlement types
C: Clustered settlements are found in the Bundelkhand region and Nagaland | people live in compact villages for security or defence
C: Dispersed settlements are found in the hills of Meghalaya and Uttarakhand | the terrain is extremely fragmented and land suitable for habitation is scattered
X: C2 D2 2 | Name the four types of rural settlements in India. | Clustered (agglomerated or nucleated), semi-clustered (fragmented), hamleted, and dispersed (isolated).
X: C3 D3 3 | Explain the factors responsible for different types of rural settlements in India. | Physical – relief, altitude, drainage, water table; cultural and ethnic – social structure, caste, religion; security – defence against thefts and robberies.
L: D4 | Describe the four types of rural settlements in India with examples and the factors responsible for them. | Clustered – plains, NE, Bundelkhand, Rajasthan; semi-clustered – Gujarat plain; hamleted – Ganga plain, Chhattisgarh (panna, para, palli, nagla, dhani); dispersed – Meghalaya, Uttarakhand, HP, Kerala; physical, cultural and security factors.
"""), ST(S + '10-st2', 'urban settlements and urbanisation in India', """
T: urbanisation | the increase in the share of urban population in the total population of a country
T: urban agglomeration | a continuous urban spread constituting a town and its adjoining urban outgrowths, or two or more physically contiguous towns
T: megacity | a city with a population of more than five million
T: metropolitan city | a city with a population between one and five million
Q: According to Census 2011, the level of urbanisation in India was: | 31.16 per cent | 17.5 per cent | 50 per cent | 10 per cent
Q: How many million-plus cities were there in India according to Census 2011? | 53 | 23 | 35 | 100
Q: A city with a population of more than five million is called a: | megacity | metropolitan city | class I town | census town
Q: Which of the following is an ancient town of India with a history of over 2,000 years? | Varanasi | Chandigarh | Jamshedpur | Gandhinagar
Q: Which of these towns was developed by Europeans as a trading port? | Surat | Varanasi | Madurai | Prayag
M:era: ancient towns | Varanasi, Prayag, Pataliputra and Madurai
M:era: medieval towns | Delhi, Hyderabad, Jaipur and Agra
M:era: modern towns | Mumbai, Chennai and Kolkata
M:era: post-independence planned towns | Chandigarh, Bhubaneswar and Gandhinagar
S+: Towns in India have flourished since prehistoric times, as seen in Harappa and Mohenjodaro
S+: Many medieval towns developed as headquarters of principalities and kingdoms
S+: The British developed Mumbai, Chennai and Kolkata in the British style
S+: According to the Census, an urban place has a minimum population of 5,000, a density of at least 400 persons per sq km and at least 75 per cent of the male workforce in non-agricultural work
S+: After independence, many towns were developed as administrative headquarters, such as Chandigarh, Bhubaneswar and Gandhinagar
S-: India's level of urbanisation was more than 50 per cent in 2011 | It was 31.16 per cent in 2011
S-: Varanasi is a modern town developed by the British | Varanasi is an ancient town
S-: A metropolitan city has more than five million people | Metropolitan cities have one to five million; megacities have more than five million
C: Many new towns developed after independence | administrative headquarters (Chandigarh, Bhubaneswar, Gandhinagar) and industrial centres (Durgapur, Bhilai) were planned
C: Medieval towns such as Agra and Jaipur flourished | they were headquarters of principalities and kingdoms
X: C2 D2 2 | Distinguish between a metropolitan city and a megacity. | Metropolitan city – population one to five million; megacity – more than five million.
X: C3 D3 3 | Explain the evolution of towns in India with examples. | Ancient (Varanasi, Prayag, Pataliputra, Madurai); medieval (Delhi, Hyderabad, Jaipur, Lucknow, Agra, Nagpur); modern (Surat, Daman, Goa, Puducherry by Europeans; Mumbai, Chennai, Kolkata by British; post-independence planned towns).
L: D4 | Describe the evolution of towns in India and the trends of urbanisation. | Prehistoric (Harappa, Mohenjodaro), ancient, medieval and modern towns with examples; Census definition of urban; urbanisation 31.16 per cent (2011); 53 million-plus cities; metropolitan and megacities.
"""), ST(S + '10-st3', 'functional classification of towns', """
T: administrative town | a town that supports administrative headquarters of higher order, such as Chandigarh, New Delhi and Bhopal
T: industrial town | a town where industries constitute the prime motive force, such as Jamshedpur and Bhilai
T: garrison town | a cantonment town, such as Ambala, Jalandhar, Mhow and Udhampur
T: religious and cultural town | a town that has emerged because of religious or cultural importance, such as Varanasi, Mathura, Amritsar and Puri
Q: Jamshedpur and Bhilai are examples of: | industrial towns | garrison towns | tourist towns | religious towns
Q: Ambala, Jalandhar and Mhow are examples of: | garrison (cantonment) towns | mining towns | educational towns | ports
Q: Raniganj, Jharia and Digboi are examples of: | mining towns | tourist towns | garrison towns | administrative towns
Q: Nainital, Mussoorie, Shimla and Pachmarhi are examples of: | tourist towns | industrial towns | mining towns | garrison towns
Q: Roorkee and Pilani are examples of: | educational towns | mining towns | port towns | cantonment towns
M:func: administrative | Chandigarh and Gandhinagar
M:func: industrial | Jamshedpur and Bhilai
M:func: transport | Kandla and Itarsi
M:func: mining | Jharia and Digboi
M:func: garrison | Ambala and Mhow
M:func: educational | Roorkee and Pilani
M:func: religious and cultural | Puri and Tirupati
M:func: tourist | Nainital and Mount Abu
S+: Towns can be classified on the basis of their dominant or specialised functions
S+: Transport towns include ports such as Kandla and Kochi and inland transport centres such as Agra, Itarsi and Katni
S+: Many big cities are multifunctional, performing several functions at the same time
S+: Commercial towns specialise in trade and commerce, such as Kolkata, Saharanpur and Satna
S+: Tourist towns such as Shimla, Mussoorie and Udagamandalam developed largely because of their pleasant climate and scenery
S-: Jharia and Digboi are tourist towns | They are mining towns
S-: Every town performs only one function | Many towns, especially big cities, are multifunctional
S-: Ambala and Mhow are religious towns | They are garrison (cantonment) towns
C: Towns such as Digboi and Jharia developed as mining towns | they grew around rich deposits of oil and coal
C: Hill towns such as Shimla and Mussoorie developed as tourist towns | their cool climate and scenery attract visitors
X: C2 D2 2 | Give two examples each of industrial towns and garrison towns in India. | Industrial – Jamshedpur, Bhilai, Salem, Coimbatore, Modinagar; garrison – Ambala, Jalandhar, Mhow, Babina, Udhampur (any two each).
X: C3 D3 3 | Explain the functional classification of towns with any three types and examples. | Administrative (Chandigarh, Bhopal), industrial (Jamshedpur, Bhilai), transport (Kandla, Itarsi), commercial (Kolkata, Satna), mining (Jharia, Digboi), garrison (Ambala, Mhow), educational (Roorkee, Pilani), religious (Varanasi, Puri), tourist (Shimla, Nainital) – any three.
L: D4 | Describe the functional classification of towns in India with examples. | Administrative, industrial, transport, commercial, mining, garrison, educational, religious and cultural, tourist towns with examples; multifunctional cities; changing functions over time.
""")]

CH11 = [ST(S + '11-st1', 'land-use categories and changes in India', """
T: culturable waste-land | land left fallow (uncultivated) for more than five years, which can be brought under cultivation after improvement
T: current fallow | land left without cultivation for one or less than one agricultural year
T: fallow other than current fallow | cultivable land left uncultivated for more than a year but less than five years
T: net area sown | the physical extent of land on which crops are sown and harvested
T: common property resources | land owned by the state or community that provides fodder, fuel and minor forest products for common use
Q: Land left uncultivated for more than five years is classified as: | culturable waste-land | current fallow | net area sown | barren land
Q: Land left without cultivation for one or less than one agricultural year is called: | current fallow | culturable waste-land | fallow other than current fallow | barren land
Q: Land under settlements, roads, railways and industries is classified as: | land put to non-agricultural uses | barren and wasteland | net area sown | permanent pastures
Q: Who benefits most from common property resources in rural India? | The landless, marginal farmers and women | Large landlords only | Urban industrialists | Foreign companies
M:land: culturable waste-land | uncultivated for more than five years
M:land: current fallow | uncultivated for one year or less
M:land: fallow other than current fallow | uncultivated for one to five years
M:land: barren and wastelands | ravines, desert land and barren hills
S+: Land-use records in India classify land into nine categories
S+: Area under non-agricultural uses has been increasing because of the growth of settlements, industries and infrastructure
S+: Barren and wastelands include barren hilly terrain, desert lands and ravines
S+: Common property resources provide fodder for livestock and fuel for households
S+: Common property resources are especially important for the landless, marginal farmers and women
S-: Current fallow is land left uncultivated for more than five years | Current fallow is uncultivated for one year or less; more than five years is culturable waste-land
S-: Area under non-agricultural uses has been decreasing in India | It has been increasing with urbanisation, industries and infrastructure
S-: Common property resources are privately owned by large farmers | They are owned by the state or community and used in common
C: Area under non-agricultural uses has increased | urban settlements, industries, roads and railways have expanded
C: Common property resources matter to the rural poor | the landless and marginal farmers depend on them for fodder, fuel and minor forest products
X: C2 D2 2 | Distinguish between current fallow and culturable waste-land. | Current fallow – uncultivated for one year or less; culturable waste-land – uncultivated for more than five years but can be reclaimed.
X: C3 D3 3 | What are common property resources? Why are they important for rural people? | Land owned by the state or community; provide fodder, fuel, minor forest products, fruits, fish; support the landless, marginal farmers and women; need community management.
L: D4 | Explain the land-use categories in India and the changes in land use. | Nine categories (forest, non-agricultural uses, barren and wasteland, pastures, tree crops, culturable waste, current fallow, other fallow, net area sown); changes with economic growth – rise in non-agricultural use; common property resources.
"""), ST(S + '11-st2', 'cropping seasons, types of farming and major crops', """
T: kharif | the cropping season that coincides with the south-west monsoon, with crops such as rice, cotton, bajra, maize, jowar and tur
T: rabi | the cropping season that begins with the onset of winter in October-November, with crops such as wheat, gram, rapeseed and mustard and barley
T: zaid | a short summer cropping season after the harvest of rabi crops, with crops such as watermelons, cucumbers, vegetables and fodder
T: dryland farming | rainfed farming in regions with annual rainfall less than 75 cm, with hardy crops such as ragi, bajra, moong, gram and guar
T: wetland farming | rainfed farming in regions where rainfall exceeds the soil moisture requirement of plants, with crops such as rice, jute and sugarcane
T: protective irrigation | irrigation that aims to protect crops from adverse effects of soil moisture deficiency
Q: Which crop is grown in the kharif season in northern India? | Rice | Wheat | Gram | Barley
Q: Wheat is mainly a: | rabi crop | kharif crop | zaid crop | plantation crop
Q: Which state is the leading producer of tea in India? | Assam | Kerala | Punjab | Rajasthan
Q: Which state is the leading producer of coffee in India? | Karnataka | Assam | Uttar Pradesh | Punjab
Q: In West Bengal, farmers grow three crops of rice called aus, aman and: | boro | kuruvai | thaladi | samba
Q: Dryland farming is practised in regions with annual rainfall of less than: | 75 cm | 200 cm | 150 cm | 300 cm
M:season: kharif | rice, cotton, bajra and maize
M:season: rabi | wheat, gram and mustard
M:season: zaid | watermelons, cucumbers and fodder
M:crop: tea | Assam
M:crop: coffee | Karnataka
M:crop: sugarcane | Uttar Pradesh
M:crop: jute | West Bengal
S+: India has three distinct cropping seasons in the northern and interior parts: kharif, rabi and zaid
S+: In southern states, the absence of a cold winter allows tropical crops such as rice to be grown in more than one season
S+: Dryland farming emphasises soil moisture conservation and rainwater harvesting
S+: In wetland farming areas there may be floods and soil erosion, and crops such as rice, jute and sugarcane are grown
S+: Rice is grown in a variety of agro-climatic regions in India, and in West Bengal three crops of rice are grown in a year
S+: Tea is grown in the Brahmaputra valley of Assam, the Darjeeling and Jalpaiguri districts of West Bengal and the Nilgiris
S-: Wheat is a kharif crop | Wheat is a rabi crop sown in winter
S-: Dryland farming is practised where rainfall exceeds 200 cm | It is practised where annual rainfall is less than 75 cm
S-: Jute is mainly grown in Rajasthan | Jute is mainly grown in West Bengal and the eastern part of India
C: Rice can be grown in more than one season in southern India | there is no severe winter and temperatures remain high throughout the year
C: Dryland farming areas grow ragi, bajra and gram | these hardy crops can withstand low rainfall and dry conditions
C: Tea is grown on hill slopes in Assam and the Nilgiris | tea needs a warm, moist climate and well-drained slopes where water does not stand at the roots
X: C2 D2 2 | Distinguish between dryland farming and wetland farming. | Dryland – rainfall below 75 cm, hardy crops (ragi, bajra, gram), moisture conservation; wetland – rainfall exceeds soil moisture needs, rice, jute, sugarcane, flood and erosion risk.
X: C3 D3 3 | Name the three cropping seasons of India with two crops of each. | Kharif – rice, cotton, bajra, maize, jowar, tur; rabi – wheat, gram, rapeseed and mustard, barley; zaid – watermelon, cucumber, vegetables, fodder.
L: D4 | Describe the cropping seasons and types of farming in India with examples of major crops. | Kharif, rabi, zaid with crops; southern differences; irrigated (protective and productive) and rainfed (dryland and wetland) farming; rice, wheat, tea, coffee, sugarcane, jute and their leading areas.
"""), ST(S + '11-st3', 'agricultural development and the Green Revolution', """
T: Green Revolution | the use of high yielding variety seeds with chemical fertilisers, pesticides and assured irrigation from the mid-1960s to raise farm production
T: HYV seeds | high yielding varieties of seeds, especially of wheat and rice, introduced as part of the Green Revolution
T: agro-climatic planning | planning launched by the Planning Commission in 1988 to induce regionally balanced agricultural development
Q: The Green Revolution was initially introduced in: | irrigated areas such as Punjab, Haryana and western Uttar Pradesh | rainfed areas of Rajasthan | the north-eastern hills | coastal Kerala only
Q: The Green Revolution was based mainly on: | HYV seeds, chemical fertilisers and irrigation | shifting cultivation | collective farming | organic manure only
Q: The Green Revolution brought the biggest increase in production of: | wheat and rice | tea and coffee | jute and cotton | pulses and oilseeds
Q: Agro-climatic planning was initiated by the Planning Commission in: | 1988 | 1951 | 1965 | 2000
S+: The Green Revolution began in India in the mid-1960s
S+: The Green Revolution made India self-sufficient in foodgrains
S+: Benefits of the Green Revolution were initially limited to irrigated areas
S+: The Green Revolution increased regional inequalities between developed and backward agricultural areas
S+: Overuse of chemical fertilisers and irrigation has caused problems such as waterlogging and soil salinity in some areas
S-: The Green Revolution spread equally to all parts of India | It was initially confined to irrigated areas such as Punjab, Haryana and western Uttar Pradesh
S-: The Green Revolution mainly increased production of tea and coffee | It mainly increased production of wheat and rice
S-: The Green Revolution had no environmental side effects | It led to waterlogging, salinity and over-use of groundwater in some areas
C: The Green Revolution led to regional disparities | its benefits were limited to irrigated areas that could use HYV seeds, fertilisers and machines
C: Agro-climatic planning was introduced in 1988 | there was a need for regionally balanced agricultural development, especially in dryland and rainfed areas
X: C2 D2 2 | Mention two positive and two negative effects of the Green Revolution. | Positive – higher foodgrain production, self-sufficiency, higher farm incomes; negative – regional inequality, waterlogging and salinity, groundwater depletion, overuse of chemicals.
X: C4 D4 3 | 'The Green Revolution was a mixed blessing for Indian agriculture.' Evaluate. | Gains – food self-sufficiency, higher yields of wheat and rice; costs – limited to irrigated areas, regional and inter-personal disparities, ecological damage (salinity, waterlogging, groundwater decline).
L: D4 | Explain the growth of Indian agriculture after independence with reference to the Green Revolution. | Food shortages after independence; mid-1960s Green Revolution – HYV seeds, fertilisers, irrigation, Punjab-Haryana-western UP; self-sufficiency; disparities and ecological problems; agro-climatic planning 1988.
"""), ST(S + '11-st4', 'problems of Indian agriculture', """
T: fragmentation of land holdings | the division of land into small and scattered plots, which makes farming uneconomic
T: land degradation | the decline in the productivity of land because of salinisation, waterlogging, soil erosion and loss of fertility
T: disguised unemployment | a situation in which more people are engaged in farming than needed, so their removal does not reduce output
Q: Which of these is a major problem of Indian agriculture? | Dependence on erratic monsoon | Excess of irrigation everywhere | Very large farm size | Over-commercialisation in all areas
Q: Waterlogging and salinity in irrigated areas are examples of: | land degradation | land reforms | crop rotation | dryland farming
Q: Small and fragmented holdings make farming: | uneconomic | highly mechanised | more commercial | free of risk
S+: A large part of Indian agriculture depends on the monsoon, which is erratic
S+: Agricultural productivity in India is low compared to many other countries
S+: Small farmers face constraints of financial resources and indebtedness
S+: Lack of land reforms has kept land concentrated in a few hands in many areas
S+: Vast under-employment exists in agriculture, especially in unirrigated areas
S-: Indian farms are mostly very large | Most holdings are small and fragmented
S-: Indian agriculture is independent of the monsoon | A large part of agriculture depends on the erratic monsoon
S-: Land degradation is not a problem in irrigated areas | Waterlogging and salinisation have degraded land in many irrigated areas
C: Many Indian farmers are in debt | crop failures, low yields and the need to buy inputs force them to borrow
C: Indian agriculture is risky | it depends on the erratic monsoon and faces droughts and floods
X: C2 D2 2 | Mention any four problems of Indian agriculture. | Dependence on erratic monsoon; low productivity; financial constraints and indebtedness; lack of land reforms; small and fragmented holdings; lack of commercialisation; under-employment; land degradation (any four).
L: D4 | Explain the major problems of Indian agriculture and suggest measures to solve them. | Monsoon dependence, low productivity, indebtedness, lack of land reforms, small holdings, lack of commercialisation, under-employment, land degradation; measures – irrigation, credit, land reforms, consolidation, diversification, soil conservation.
""")]

CH12 = [ST(S + '12-st1', 'surface and groundwater resources of India', """
T: surface water | water that flows in rivers, lakes, ponds and tanks
T: groundwater | water stored below the surface in the pores of soils and rocks, which is replenished by rainfall
T: lagoons | water bodies along the coast, as in Kerala, Odisha and West Bengal, used for fishing and irrigating some crops
Q: India accounts for about what share of the world's water resources? | About 4 per cent | About 16 per cent | About 25 per cent | About 1 per cent
Q: India accounts for about what share of the world's surface area? | About 2.45 per cent | About 4 per cent | About 16 per cent | About 10 per cent
Q: The total annual precipitation in India is about: | 4,000 cubic km | 1,122 cubic km | 400 cubic km | 40,000 cubic km
Q: The total utilisable water resource of India is estimated at about: | 1,122 cubic km | 4,000 cubic km | 1,869 cubic km | 690 cubic km
Q: The level of groundwater utilisation is relatively high in: | Punjab, Haryana, Rajasthan and Tamil Nadu | Chhattisgarh and Odisha | Kerala and Assam | Meghalaya and Mizoram
S+: India has about 2.45 per cent of the world's surface area, 4 per cent of its water resources and about 16 per cent of its population
S+: Surface water and replenishable groundwater together amount to about 1,869 cubic km a year
S+: Only about 60 per cent of available water can be put to beneficial use because of topographical, hydrological and other constraints
S+: The Ganga, the Brahmaputra and the Barak rivers carry a large share of India's surface water
S+: Groundwater utilisation is very high in north-western India and in parts of south India
S-: India has about 16 per cent of the world's water resources | India has about 4 per cent of the world's water resources but about 16 per cent of its population
S-: All the water received through precipitation can be used | Only about 60 per cent of the available water can be put to beneficial use
S-: Groundwater utilisation is highest in the north-eastern states | It is high in Punjab, Haryana, Rajasthan and Tamil Nadu
C: Water is a scarce resource in India | India has about 16 per cent of the world's population but only about 4 per cent of its water resources
C: Groundwater is over-used in Punjab and Haryana | intensive irrigated agriculture of water-demanding crops depends heavily on tubewells
X: C2 D2 2 | Distinguish between surface water and groundwater resources. | Surface – rivers, lakes, ponds, tanks; groundwater – stored in soils and rocks below the surface, replenished by rainfall, extracted by wells and tubewells.
X: C3 D3 3 | Explain the availability of water resources in India. | Precipitation about 4,000 cubic km; surface and replenishable groundwater 1,869 cubic km; utilisable 1,122 cubic km (about 60 per cent); Ganga, Brahmaputra, Barak basins; high groundwater use in Punjab, Haryana, Rajasthan, TN.
L: D4 | Describe the surface and groundwater resources of India and their distribution. | Share of world water and population; precipitation, available and utilisable water; river basins; groundwater utilisation by region; lagoons and lakes; uneven distribution.
"""), ST(S + '12-st2', 'water demand, utilisation and deterioration of water quality', """
T: water pollution | the deterioration of water quality when foreign matter such as micro-organisms, chemicals and industrial wastes enters water bodies
T: Water (Prevention and Control of Pollution) Act | the act of 1974 for the prevention and control of water pollution in India
Q: Which sector accounts for the largest share of water use in India? | Agriculture | Industry | Domestic | Hydroelectricity
Q: The Water (Prevention and Control of Pollution) Act was passed in: | 1974 | 1986 | 2002 | 1952
Q: The Environment Protection Act was passed in: | 1986 | 1974 | 1992 | 2010
Q: Which two rivers are described by NCERT as highly polluted? | The Ganga and the Yamuna | The Narmada and the Tapi | The Godavari and the Krishna | The Brahmaputra and the Barak
S+: Agriculture accounts for most of the surface water and groundwater use in India
S+: Water demand for domestic and industrial purposes is increasing with urbanisation and industrialisation
S+: Industrial effluents, untreated sewage and agricultural chemicals pollute water bodies
S+: The Water (Prevention and Control of Pollution) Act of 1974 and the Environment Protection Act of 1986 have not been implemented effectively
S+: Polluted water causes water-borne diseases such as diarrhoea and intestinal worms
S-: Industry uses the largest share of water in India | Agriculture uses the largest share
S-: The Water (Prevention and Control of Pollution) Act was passed in 1986 | It was passed in 1974; the Environment Protection Act was passed in 1986
S-: Water quality is improving in all Indian rivers | Many rivers such as the Ganga and Yamuna are highly polluted
C: Demand for water is increasing in India | population, urbanisation, industrialisation and irrigated agriculture are all growing
C: Water quality is deteriorating | industrial effluents, untreated sewage and agricultural chemicals are discharged into water bodies
X: C2 D2 2 | Mention two causes of water pollution in India. | Industrial effluents; untreated urban sewage; fertilisers and pesticides from agriculture; cultural activities such as immersion of idols and bathing at fairs (any two).
L: D4 | Explain the demand for water in India and the causes and consequences of deterioration of water quality. | Agriculture main user; rising domestic and industrial demand; pollution by industry, sewage, agriculture; Ganga and Yamuna; diseases; laws of 1974 and 1986 and their weak implementation.
"""), ST(S + '12-st3', 'water conservation, watershed management and rainwater harvesting', """
T: watershed management | the efficient management and conservation of surface and groundwater resources, including prevention of runoff and storage and recharge of groundwater
T: rainwater harvesting | the method of capturing rainwater and storing it for later use or for recharging groundwater
T: Haryali | a watershed development project sponsored by the central government to enable rural people to conserve water for drinking, irrigation, fisheries and afforestation
T: Neeru-Meeru | the 'Water and You' programme of Andhra Pradesh for water conservation
T: Arvary Pani Sansad | a people's parliament for the Arvary river in Alwar, Rajasthan, which manages water through community effort
Q: Neeru-Meeru (Water and You) is a water conservation programme of: | Andhra Pradesh | Rajasthan | Tamil Nadu | Gujarat
Q: Arvary Pani Sansad is associated with: | Alwar, Rajasthan | Ahmedabad, Gujarat | Chennai, Tamil Nadu | Pune, Maharashtra
Q: Which state made rainwater harvesting structures compulsory for all houses? | Tamil Nadu | Punjab | Bihar | Assam
Q: Haryali is a watershed development project sponsored by: | the central government | the World Bank alone | a private company | the UN
M:ws: Haryali | central government watershed project
M:ws: Neeru-Meeru | Andhra Pradesh
M:ws: Arvary Pani Sansad | Alwar, Rajasthan
M:ws: compulsory rooftop harvesting | Tamil Nadu
S+: Watershed management includes prevention of runoff, storage and recharge of groundwater
S+: Rainwater harvesting raises the groundwater level and reduces the need for drawing water from far away
S+: Tamil Nadu has made water harvesting structures compulsory in all houses
S+: Watershed programmes succeed best with people's participation
S+: Water conservation includes reducing wastage, recycling and reuse of water
S-: Haryali is a watershed programme of Rajasthan only | Haryali is sponsored by the central government
S-: Rainwater harvesting lowers the groundwater level | It recharges and raises the groundwater level
S-: Arvary Pani Sansad is a programme of Andhra Pradesh | It is in Alwar, Rajasthan; Neeru-Meeru is in Andhra Pradesh
C: Rainwater harvesting is useful in water-scarce areas | it stores rainwater and recharges groundwater for use in the dry season
C: Watershed management needs people's participation | conservation structures can be maintained only if local communities share the effort and benefits
X: C2 D2 2 | What is rainwater harvesting? Mention two of its benefits. | Capturing and storing rainwater; benefits – raises groundwater, reduces water scarcity, reduces runoff and floods, improves water quality (any two).
X: C3 D3 3 | Explain any three watershed management programmes in India. | Haryali (central government, rural water for drinking, irrigation, afforestation); Neeru-Meeru (Andhra Pradesh); Arvary Pani Sansad (Alwar, Rajasthan); compulsory rooftop harvesting in Tamil Nadu.
L: D4 | Explain the need for water conservation in India and the methods of watershed management and rainwater harvesting. | Scarcity and rising demand; pollution; watershed management (runoff control, recharge); Haryali, Neeru-Meeru, Arvary Pani Sansad; rainwater harvesting, Tamil Nadu; recycling and reuse; people's participation.
""")]

CH13 = [ST(S + '13-st1', 'types and distribution of minerals in India', """
T: mineral | a natural substance of organic or inorganic origin with definite chemical and physical properties
T: metallic minerals | minerals from which metals are obtained, divided into ferrous and non-ferrous minerals
T: non-metallic minerals | minerals of organic or inorganic origin that do not yield metals, such as mica, limestone and coal
Q: Most of India's metallic minerals occur in: | the peninsular plateau region in old crystalline rocks | the alluvial plains | the Thar desert sand dunes | the Himalayan glaciers
Q: Which mineral belt includes the Chota Nagpur plateau and the Odisha plateau? | The north-eastern plateau region | The south-western plateau region | The north-western region | The Himalayan belt
Q: Copper and zinc are mainly found in which mineral belt? | The north-western region (Aravalli) | The north-eastern plateau region | The Himalayan belt only | The Kerala coast
Q: Mineral oil is found mainly in Assam and in: | the offshore and coastal areas of Gujarat and Maharashtra | the Chota Nagpur plateau | the Aravalli hills | the Himalayan glaciers
M:belt: north-eastern plateau region | iron ore, coal, manganese and mica
M:belt: south-western plateau region | high-grade iron ore, manganese and limestone
M:belt: north-western region | copper, zinc, sandstone and marble
M:belt: Kerala coast | monazite sands with thorium
S+: Over 97 per cent of India's coal reserves occur in the valleys of the Damodar, Sone, Mahanadi and Godavari
S+: The north-eastern plateau region covers Chota Nagpur in Jharkhand, the Odisha plateau, West Bengal and parts of Chhattisgarh
S+: The south-western plateau region extends over Karnataka, Goa and the contiguous Tamil Nadu uplands and Kerala
S+: The north-western belt extends along the Aravalli in Rajasthan and part of Gujarat
S+: The Himalayan belt has copper, lead, zinc, cobalt and tungsten
S-: Most metallic minerals of India occur in the northern plains | They occur mostly in the peninsular plateau region in old crystalline rocks
S-: Copper and zinc are mainly found in the Kerala coast | They are found mainly in the Aravalli region of Rajasthan and Gujarat
S-: Coal is a metallic mineral | Coal is a non-metallic mineral and a fuel
C: Most of India's metallic minerals are found in the peninsular plateau | the old crystalline rocks of the plateau contain rich deposits of metallic minerals
C: The north-eastern plateau region is rich in minerals | it contains Chota Nagpur and the Odisha plateau with iron ore, coal, manganese, bauxite and mica
X: C2 D2 2 | Distinguish between metallic and non-metallic minerals with examples. | Metallic – yield metals; ferrous (iron ore, manganese) and non-ferrous (copper, bauxite); non-metallic – do not yield metals (mica, limestone, coal).
X: C3 D3 3 | Name the major mineral belts of India and one important mineral of each. | North-eastern plateau (iron ore, coal); south-western plateau (iron ore, manganese); north-western (copper, zinc); Himalayan belt (copper, lead, zinc, cobalt, tungsten).
L: D4 | Describe the distribution of minerals in India with reference to the major mineral belts. | North-eastern plateau, south-western plateau, north-western region, Himalayan belt, Assam (oil), offshore areas; minerals in each; peninsular old crystalline rocks; coal in Damodar, Sone, Mahanadi, Godavari valleys.
"""), ST(S + '13-st2', 'ferrous, non-ferrous and non-metallic minerals', """
T: haematite | the best quality iron ore, with a high iron content
T: bauxite | the ore from which aluminium is obtained, found mainly in tertiary deposits and laterite rocks
T: mica | a non-metallic mineral used in the electrical and electronics industries because of its insulating properties
Q: Which state is the largest producer of manganese in India? | Odisha | Rajasthan | Kerala | Punjab
Q: Bauxite is the ore of: | aluminium | iron | copper | manganese
Q: Khetri in Rajasthan is famous for: | copper | mica | bauxite | coal
Q: The Hazaribagh plateau of Jharkhand is known for: | mica | bauxite | oil | lignite
Q: Kudremukh in Karnataka is known for: | iron ore | copper | mica | natural gas
Q: Which state is the largest producer of bauxite in India? | Odisha | Gujarat | Rajasthan | Punjab
M:min: iron ore | Bailadila
M:min: manganese | Balaghat
M:min: copper | Khetri
M:min: bauxite | Koraput
M:min: mica | Hazaribagh
M:min: lignite | Neyveli
P: Bailadila | iron ore mines in the Bastar region of Chhattisgarh
P: Kudremukh | iron ore mines in the Western Ghats of Karnataka
P: Balaghat | manganese mines in Madhya Pradesh
P: Khetri | copper mines in Rajasthan
P: Koraput | bauxite mines in Odisha
P: Mayurbhanj | iron ore mines in Odisha
P: Singhbhum | copper mines in Jharkhand
S+: Iron ore in India is mainly haematite and magnetite
S+: Odisha and Jharkhand have large deposits of iron ore, and Chhattisgarh has the Bailadila mines
S+: Odisha is the largest producer of manganese and of bauxite
S+: Copper is mined in Singhbhum in Jharkhand, Balaghat in Madhya Pradesh and Khetri in Rajasthan
S+: Mica is found in the Hazaribagh plateau of Jharkhand, Nellore in Andhra Pradesh and parts of Rajasthan
S-: Bauxite is the ore of iron | Bauxite is the ore of aluminium
S-: Khetri is famous for mica | Khetri is famous for copper
S-: Haematite is the poorest quality iron ore | Haematite is a high quality iron ore
C: Mica is important for the electrical and electronics industries | it has excellent insulating properties and can be split into thin sheets
C: Manganese is important for the iron and steel industry | it is used in making steel and ferro-manganese alloys
X: C2 D2 2 | Name two important mining areas each of iron ore and copper in India. | Iron ore – Bailadila, Kudremukh, Mayurbhanj, Noamundi, Sandur-Hospet; copper – Singhbhum, Balaghat, Khetri (any two each).
X: C3 D3 3 | Describe the distribution of bauxite and manganese in India. | Bauxite – Odisha largest (Kalahandi, Koraput), Jharkhand, Gujarat, Chhattisgarh, MP, Maharashtra; manganese – Odisha largest, Karnataka, Maharashtra, MP (Balaghat), Telangana.
L: D4 | Describe the distribution of iron ore, manganese, bauxite, copper and mica in India. | Iron ore – Odisha, Jharkhand, Chhattisgarh (Bailadila), Karnataka (Kudremukh), Goa; manganese – Odisha, Balaghat; bauxite – Odisha (Koraput); copper – Singhbhum, Balaghat, Khetri; mica – Hazaribagh, Nellore.
"""), ST(S + '13-st3', 'conventional and non-conventional energy resources', """
T: conventional energy | energy from sources such as coal, petroleum, natural gas and nuclear minerals, which are exhaustible
T: non-conventional energy | energy from renewable sources such as solar, wind, tidal, geothermal and bio-energy
T: geothermal energy | energy obtained from the heat of the earth's interior, as at Manikaran in Himachal Pradesh
T: bio-energy | energy derived from biological products such as agricultural residues and municipal and industrial waste
Q: Jharia and Raniganj are important fields of: | coal | petroleum | copper | uranium
Q: Digboi, the oldest oil field of India, is in: | Assam | Gujarat | Maharashtra | Rajasthan
Q: Neyveli in Tamil Nadu is known for: | lignite | natural gas | bauxite | iron ore
Q: Uranium is mined at Jaduguda in: | Jharkhand | Kerala | Karnataka | Assam
Q: Manikaran in Himachal Pradesh is an example of a site for: | geothermal energy | tidal energy | wind energy | nuclear energy
Q: Which refinery is an example of a field-based refinery? | Digboi | Barauni | Mathura | Panipat
M:energy: Jharia | coal
M:energy: Digboi | petroleum
M:energy: Neyveli | lignite
M:energy: Jaduguda | uranium
M:energy: Manikaran | geothermal energy
M:energy: Gulf of Khambhat | tidal energy
P: Jharia | the largest coalfield of India in the Damodar valley in Jharkhand
P: Raniganj | a major coalfield of West Bengal
P: Neyveli | lignite deposits in Tamil Nadu
P: Digboi | the oldest oil field and refinery in Assam
P: Mumbai High | an offshore oil field off the coast of Maharashtra
P: Ankaleshwar | an oil field in Gujarat
P: Jamnagar | an oil refinery town in Gujarat
P: Mathura | an oil refinery in Uttar Pradesh
P: Tarapur | a nuclear power station in Maharashtra
P: Kalpakkam | a nuclear power station in Tamil Nadu
S+: About 80 per cent of India's coal deposits are of bituminous type and are of non-coking grade
S+: Gondwana coal is found mainly in the Damodar valley, with Jharia the largest and Raniganj the second largest coalfield
S+: Tertiary coal occurs in Assam, Arunachal Pradesh, Meghalaya and Nagaland
S+: Oil refineries are of two types: field-based, such as Digboi, and market-based, such as Barauni
S+: The Gas Authority of India Limited was set up in 1984 to transport and market natural gas
S+: Thorium is obtained from the monazite sands of the Kerala coast
S+: Wind energy is being developed in Rajasthan, Gujarat, Maharashtra and Karnataka
S-: Jharia is an oil field in Assam | Jharia is the largest coalfield, in Jharkhand; Digboi is an oil field in Assam
S-: Non-conventional sources of energy are exhaustible | They are renewable and inexhaustible
S-: Thorium is mined from the coal of the Damodar valley | It is obtained from the monazite sands of Kerala
C: Non-conventional energy sources are being promoted in India | they are renewable, cleaner and reduce dependence on exhaustible fossil fuels
C: Barauni is called a market-based refinery | it was set up near the market for petroleum products rather than near an oil field
C: The Gulf of Khambhat is suitable for tidal energy | it has a high tidal range
X: C2 D2 2 | Distinguish between conventional and non-conventional sources of energy with two examples each. | Conventional – exhaustible, often polluting (coal, petroleum, natural gas, nuclear); non-conventional – renewable, clean (solar, wind, tidal, geothermal, bio-energy).
X: C3 D3 3 | Describe the distribution of coal in India. | Gondwana coal – Damodar valley (Jharia largest, Raniganj, Bokaro), Sone, Mahanadi, Godavari valleys; tertiary coal – Assam, Arunachal, Meghalaya, Nagaland; lignite – Neyveli (TN).
L: D4 | Describe the conventional and non-conventional energy resources of India. | Coal (Gondwana and tertiary, Jharia, Raniganj, Neyveli), petroleum (Digboi, Ankaleshwar, Mumbai High; field and market refineries), natural gas (GAIL 1984), nuclear (Jaduguda uranium, Kerala thorium, Tarapur, Kalpakkam); solar, wind, tidal, geothermal (Manikaran), bio-energy.
"""), ST(S + '13-st4', 'conservation of mineral resources', """
T: conservation of minerals | the judicious and planned use of mineral resources so that they last longer and serve future generations
T: recycling | the reuse of scrap metals and other materials to save mineral resources
T: substitution | the use of alternative materials in place of scarce minerals
Q: Which of these helps conserve mineral resources? | Recycling scrap metals | Increasing wasteful mining | Exporting all strategic minerals | Ignoring substitutes
Q: Using solar and wind energy instead of coal is an example of: | using alternative energy sources | mining expansion | waste disposal | recycling of copper
Q: The challenge of sustainable development requires: | conservation of mineral resources | unlimited extraction of minerals | stopping all industries | exporting raw ores only
S+: Minerals are non-renewable and take millions of years to form
S+: Alternative energy sources such as solar, wind, tidal and geothermal can replace exhaustible minerals
S+: The use of scrap metals allows recycling of metals such as copper, lead and zinc
S+: Substitutes for scarce metals can reduce their consumption
S+: Exports of strategic and scarce minerals should be reduced to keep reserves for future use
S-: Minerals are renewable resources that form quickly | Minerals are non-renewable and take millions of years to form
S-: Recycling scrap metals increases the demand for new ores | Recycling reduces the demand for fresh ores
S-: Conservation means stopping the use of all minerals | Conservation means judicious and planned use of minerals
C: Conservation of minerals is essential | minerals are non-renewable and their reserves are limited
C: Recycling of metals helps conservation | scrap metals can be reused instead of mining fresh ore
X: C2 D2 2 | Suggest two measures for the conservation of mineral resources. | Use alternative energy sources; recycle scrap metals; use substitutes for scarce minerals; reduce exports of strategic minerals; improved technology to reduce wastage (any two).
L: D4 | Why is conservation of mineral resources necessary? Explain the measures for conservation. | Non-renewable, limited reserves, long formation time; sustainable development; measures – alternative energy, recycling, substitutes, reduced exports of strategic minerals, better technology.
""")]

CH14 = [ST(S + '14-st1', 'planning in India and target area programmes', """
T: sectoral planning | planning that formulates and implements programmes for sectors of the economy such as agriculture, irrigation, industry and power
T: regional planning | planning that aims to reduce regional imbalances in development
T: target area planning | planning that targets specific areas lagging behind in development, such as command areas, drought-prone areas and hill areas
T: Hill Area Development Programme | a programme initiated in the Fifth Five Year Plan for the development of hill areas
T: Drought Prone Area Programme | a programme initiated during the Fourth Five Year Plan to provide employment and create productive assets in drought-prone areas
Q: The Hill Area Development Programme was initiated during the: | Fifth Five Year Plan | First Five Year Plan | Third Five Year Plan | Tenth Five Year Plan
Q: The Drought Prone Area Programme was initiated during the: | Fourth Five Year Plan | First Five Year Plan | Eighth Five Year Plan | Second Five Year Plan
Q: The Small Farmers Development Agency is an example of: | target group programme | target area programme | sectoral planning for industry | hill area programme
Q: According to the National Committee on the Development of Backward Areas (1981), hill areas for the programme are those with a height above: | 600 m | 2,000 m | 100 m | 1,500 m
M:prog: Hill Area Development Programme | Fifth Five Year Plan
M:prog: Drought Prone Area Programme | Fourth Five Year Plan
M:prog: Small Farmers Development Agency | target group programme
M:prog: Command Area Development Programme | target area programme
S+: Planning involves thinking, formulating a scheme and implementing a set of activities to achieve a goal
S+: Regional planning aims to reduce disparities in economic development between regions
S+: Target area programmes include the Command Area Development Programme, Drought Prone Area Programme, Desert Development Programme and Hill Area Development Programme
S+: The Hill Area Development Programme aimed to harness indigenous resources of hill areas through horticulture, plantation agriculture, animal husbandry and small-scale industry
S+: The Drought Prone Area Programme aimed at providing employment and creating productive assets in drought-prone areas
S-: Regional planning aims to increase regional disparities | It aims to reduce regional imbalances in development
S-: The Hill Area Development Programme was started in the First Five Year Plan | It was started in the Fifth Five Year Plan
S-: Target group programmes are aimed at specific areas | Target group programmes focus on groups such as small and marginal farmers; target area programmes focus on areas
C: Target area planning was introduced | some areas such as drought-prone and hill areas lagged behind in development even after sectoral planning
C: The Drought Prone Area Programme emphasised irrigation and afforestation | these measures help to reduce the effects of drought and create productive assets
X: C2 D2 2 | Distinguish between sectoral planning and regional planning. | Sectoral – programmes for sectors such as agriculture, irrigation, industry, power; regional – reducing regional imbalances in development.
X: C3 D3 3 | Explain the objectives of the Hill Area Development Programme. | Initiated in the Fifth Plan; harness indigenous resources of hill areas; horticulture, plantation agriculture, animal husbandry, poultry, forestry, small-scale and village industry; consider topography, ecology and social conditions.
L: D4 | Explain the target area and target group approaches of planning in India with examples. | Sectoral and regional planning; target area – Command Area, Drought Prone Area, Desert Development, Hill Area Development Programmes; target group – Small Farmers Development Agency, Marginal Farmers Development Agency; objectives.
"""), ST(S + '14-st2', 'the Integrated Tribal Development Project in Bharmaur', """
T: Bharmaur tribal region | a notified tribal area in Chamba district of Himachal Pradesh, comprising the Bharmaur and Holi tehsils
T: Gaddis | a tribal community of the Bharmaur region who practise transhumance
T: Integrated Tribal Development Project | a development project for the tribal region of Bharmaur that focused on transport, communication, agriculture, education and health
Q: Bharmaur tribal region is located in which district of Himachal Pradesh? | Chamba | Kangra | Shimla | Kullu
Q: The tribal community of the Bharmaur region is: | the Gaddis | the Bhils | the Santhals | the Todas
Q: The Bharmaur region is drained by the river: | Ravi and its tributaries | Sutlej | Beas | Chenab only
Q: Which of these is an important outcome of the ITDP in Bharmaur? | Increase in literacy, especially female literacy | Decline in school enrolment | Decline in the sex ratio | Increase in child marriage
S+: The Bharmaur region has harsh climatic conditions, a low resource base and a fragile environment
S+: The Gaddis have traditionally practised transhumance and maintained a distinct identity in the Himalayan region
S+: The ITDP gave priority to transport and communications, agriculture and allied activities, and social and community services
S+: The ITDP led to an increase in literacy rate, improvement in sex ratio and decline in child marriage
S+: The importance of pastoralism in the traditional economy of Bharmaur has declined
S-: Bharmaur is located in Kangra district | It is in Chamba district of Himachal Pradesh
S-: The ITDP led to a decline in female literacy | Female literacy increased considerably
S-: The Gaddis are a community of plains farmers | The Gaddis are a tribal community of the Himalayas who practise transhumance
C: The Bharmaur region was declared a tribal area for development | it was economically and socially backward with harsh climate and a fragile environment
C: Pastoralism has declined in Bharmaur | the ITDP encouraged agriculture, horticulture and other occupations, and many Gaddis took up new livelihoods
X: C2 D2 2 | Who are the Gaddis? Where do they live? | A tribal community that practises transhumance; they live in the Bharmaur region of Chamba district, Himachal Pradesh.
X: C3 D4 3 | Explain the social benefits of the Integrated Tribal Development Project in Bharmaur. | Rise in literacy, especially female literacy; improvement in sex ratio; decline in child marriage; schools, health care, potable water, roads, electricity; change from pastoralism to agriculture.
L: D4 | Describe the Bharmaur region and the achievements of the Integrated Tribal Development Project. | Chamba district, Bharmaur and Holi tehsils, Ravi and tributaries; harsh climate, fragile environment; Gaddis and transhumance; ITDP priorities; outcomes – literacy, sex ratio, child marriage, infrastructure; decline in pastoralism.
"""), ST(S + '14-st3', 'sustainable development and the Indira Gandhi Canal command area', """
T: sustainable development | development that meets the needs of the present without compromising the ability of future generations to meet their own needs
T: Brundtland Report | the report 'Our Common Future' of the World Commission on Environment and Development, published in 1987
T: Indira Gandhi Canal | one of the largest canal systems of India, previously known as the Rajasthan Canal, which originates at the Harike barrage in Punjab
T: lift canal | a canal that lifts water to higher ground, used in stage II of the Indira Gandhi Canal command area
Q: The Indira Gandhi Canal originates at the: | Harike barrage in Punjab | Bhakra dam | Hirakud dam | Farakka barrage
Q: The Indira Gandhi Canal was conceived in 1948 by: | Kanwar Sain | M. Visvesvaraya | K.L. Rao | Mahalanobis
Q: The report 'Our Common Future' (1987) is also known as the: | Brundtland Report | Mahalanobis Report | Rio Declaration | Kyoto Protocol
Q: Which problem has increased in the Indira Gandhi Canal command area because of intensive irrigation? | Waterlogging and soil salinity | Glacial erosion | Volcanic activity | Coastal erosion
Q: Which crop is NOT advisable in the Indira Gandhi Canal command area because it needs too much water? | Rice | Citrus fruits | Gram | Fodder crops
S+: The Indira Gandhi Canal runs parallel to the Pakistan border at an average distance of 40 km in the Thar desert
S+: Stage I of the command area lies in Ganganagar, Hanumangarh and the northern part of Bikaner districts
S+: Stage II of the command area covers Bikaner, Jaisalmer, Barmer, Jodhpur, Nagaur and Churu districts and uses lift canals
S+: Canal irrigation has increased cultivated area and the intensity of cropping in the region
S+: Measures for sustainable development include strict water management, avoiding water-intensive crops, and afforestation and pasture development
S+: The Brundtland Report defined sustainable development as development that meets the needs of the present without compromising the ability of future generations
S-: The Indira Gandhi Canal originates at the Bhakra dam | It originates at the Harike barrage in Punjab
S-: Water-intensive crops such as rice should be encouraged in the canal command area | They should be avoided; plantation of citrus fruits and less water-intensive crops is advised
S-: Canal irrigation has had no environmental side effects in western Rajasthan | It has caused waterlogging and soil salinity
C: Waterlogging and soil salinity have increased in the canal command area | intensive irrigation and excessive use of water have raised the water table
C: Afforestation and shelterbelts are promoted in the command area | they protect the land from wind erosion and help to restore the fragile ecosystem
C: Sustainable development became a central idea in the 1980s | concern grew about environmental damage caused by economic development
X: C2 D2 2 | What is sustainable development? Which report popularised the concept? | Development meeting present needs without compromising future generations; Brundtland Report 'Our Common Future' (1987).
X: C3 D4 3 | Suggest three measures to promote sustainable development in the Indira Gandhi Canal command area. | Strict water management; protective irrigation in stage I, extensive irrigation in stage II; avoid water-intensive crops (citrus instead); lining of watercourses and on-farm development; reclamation of waterlogged land; afforestation and shelterbelts; land to poor farmers.
L: D4 | Describe the Indira Gandhi Canal command area and the measures for its sustainable development. | Harike barrage origin; Kanwar Sain 1948; parallel to Pakistan border; stage I and II districts; lift canals; benefits – irrigation, crops, cropping intensity; problems – waterlogging, salinity; measures for sustainability.
""")]

CH15 = [ST(S + '15-st1', 'road and rail transport in India', """
T: Golden Quadrilateral | the six-lane highway project linking Delhi, Mumbai, Chennai and Kolkata
T: North-South Corridor | the highway corridor linking Srinagar in the north with Kanyakumari in the south
T: East-West Corridor | the highway corridor linking Silchar in Assam with Porbandar in Gujarat
T: Konkan Railway | the 760 km railway from Roha in Maharashtra to Mangaluru in Karnataka, completed in 1998
T: broad gauge | the railway gauge in which the distance between rails is 1.676 m
Q: The first train in India ran in 1853 from Mumbai to: | Thane | Pune | Surat | Nashik
Q: The Konkan Railway connects Roha in Maharashtra with: | Mangaluru | Kochi | Goa only | Chennai
Q: The East-West Corridor links Silchar with: | Porbandar | Kanyakumari | Srinagar | Mumbai
Q: Which organisation is responsible for the development and maintenance of National Highways? | National Highways Authority of India | Border Roads Organisation | Indian Railways | Airports Authority of India
Q: The distance between the rails in broad gauge is: | 1.676 m | 1 m | 0.762 m | 0.610 m
Q: The Grand Trunk Road was originally built as the Shahi (Royal) Road by: | Sher Shah Suri | Akbar | Ashoka | Lord Dalhousie
M:road: Golden Quadrilateral | Delhi, Mumbai, Chennai and Kolkata
M:road: North-South Corridor | Srinagar to Kanyakumari
M:road: East-West Corridor | Silchar to Porbandar
M:road: Konkan Railway | Roha to Mangaluru
P: Srinagar | the northern end of the North-South Corridor
P: Kanyakumari | the southern end of the North-South Corridor
P: Silchar | the eastern end of the East-West Corridor in Assam
P: Porbandar | the western end of the East-West Corridor in Gujarat
P: Roha | the northern end of the Konkan Railway in Maharashtra
P: Mangaluru | the southern end of the Konkan Railway in Karnataka
S+: National Highways form only about 2 per cent of the total road length but carry about 40 per cent of road traffic
S+: The National Highways Authority of India was operationalised in 1995
S+: The Border Roads Organisation constructs and maintains roads in strategic border areas
S+: Indian Railways has three gauges: broad gauge, metre gauge and narrow gauge
S+: The Konkan Railway crosses Maharashtra, Goa and Karnataka
S-: The first train in India ran from Delhi to Agra | It ran from Mumbai to Thane in 1853
S-: National Highways form about 40 per cent of India's road length | They form about 2 per cent of road length but carry about 40 per cent of traffic
S-: The Konkan Railway links Mumbai with Chennai | It links Roha in Maharashtra with Mangaluru in Karnataka
C: The Konkan Railway is considered an engineering marvel | it was built across a difficult terrain of the Western Ghats coast with many rivers, bridges and tunnels
C: National Highways carry a large share of road traffic | they connect state capitals, major cities and ports across the country
X: C2 D2 2 | Name the four metropolitan cities linked by the Golden Quadrilateral. | Delhi, Mumbai, Chennai and Kolkata.
X: C3 D3 3 | Explain the importance of the Konkan Railway. | 760 km from Roha to Mangaluru, completed in 1998; links Maharashtra, Goa and Karnataka; difficult Western Ghats terrain; faster movement of goods and people along the west coast; boosts trade and tourism.
L: D4 | Describe the road and rail transport network of India. | Roads – Sher Shah Suri, Nagpur Plan, NH (2 per cent length, 40 per cent traffic), NHAI 1995, Golden Quadrilateral, NS and EW corridors, BRO, rural roads; railways – 1853 Mumbai-Thane, gauges, Konkan Railway.
"""), ST(S + '15-st2', 'water, air and pipeline transport in India', """
T: National Waterway 1 | the Ganga–Bhagirathi–Hugli river system between Haldia and Allahabad (Prayagraj)
T: National Waterway 2 | the Brahmaputra river between Sadiya and Dhubri
T: National Waterway 3 | the West Coast Canal in Kerala between Kottapuram and Kollam
T: HVJ pipeline | the gas pipeline from Hazira in Gujarat through Vijaipur in Madhya Pradesh to Jagdishpur in Uttar Pradesh
Q: National Waterway 1 is on the river: | Ganga | Brahmaputra | Godavari | Narmada
Q: National Waterway 2 lies between Sadiya and: | Dhubri | Haldia | Kollam | Allahabad
Q: Air transport in India began in 1911 with an airmail service between Allahabad and: | Naini | Delhi | Kanpur | Lucknow
Q: The HVJ pipeline carries: | natural gas | crude oil | water | iron ore slurry
Q: Which company provides helicopter services to ONGC and in hilly areas? | Pawan Hans | Air India | Indian Airlines | Vayudoot only
Q: The Inland Waterways Authority of India was set up in: | 1986 | 1953 | 1911 | 1995
M:nw: National Waterway 1 | Haldia–Allahabad
M:nw: National Waterway 2 | Sadiya–Dhubri
M:nw: National Waterway 3 | Kottapuram–Kollam
M:nw: HVJ pipeline | Hazira–Vijaipur–Jagdishpur
P: Haldia | the eastern end of National Waterway 1
P: Sadiya | the eastern end of National Waterway 2 on the Brahmaputra
P: Dhubri | the western end of National Waterway 2
P: Kollam | the southern end of National Waterway 3
S+: Waterways are a fuel-efficient and environment-friendly mode of transport
S+: The Inland Waterways Authority of India was set up in 1986 for the development of national waterways
S+: Air transport began in India in 1911 with an airmail service over a distance of about 10 km between Allahabad and Naini
S+: Oil India Limited constructed a long pipeline from the Naharkatiya oil field in Assam to the Barauni refinery in Bihar
S+: The HVJ pipeline links Hazira in Gujarat with Jagdishpur in Uttar Pradesh via Vijaipur in Madhya Pradesh
S-: National Waterway 2 is on the Ganga | National Waterway 2 is on the Brahmaputra; National Waterway 1 is on the Ganga
S-: The HVJ pipeline carries crude oil from Assam | It is a natural gas pipeline from Hazira to Jagdishpur
S-: Air transport began in India after independence | It began in 1911 with an airmail service between Allahabad and Naini
C: Pipelines are useful for transporting oil and gas | they provide uninterrupted flow, cause little wastage and reduce traffic on roads and railways
C: Inland water transport is environment-friendly | it is fuel-efficient and suitable for bulky cargo
X: C2 D2 2 | Name the three National Waterways of India with their stretches. | NW1 – Ganga, Haldia to Allahabad; NW2 – Brahmaputra, Sadiya to Dhubri; NW3 – West Coast Canal, Kottapuram to Kollam.
X: C3 D3 3 | Explain the importance of pipeline transport in India with examples. | Transport of oil and gas; uninterrupted flow; low running cost; Naharkatiya–Barauni oil pipeline; HVJ gas pipeline to fertiliser and power plants; reduces load on rail and road.
L: D4 | Describe water, air and pipeline transport in India. | Inland waterways – NW1, NW2, NW3, IWAI 1986; ocean transport; air – 1911 airmail, Air India, Pawan Hans, AAI; pipelines – Naharkatiya–Barauni, HVJ gas pipeline; advantages and limitations.
"""), ST(S + '15-st3', 'communication networks in India', """
T: personal communication | communication between individuals through letters, telephone, e-mail and the internet
T: mass communication | communication with large numbers of people through radio, television, newspapers and films
T: INSAT | the Indian National Satellite system, a multi-purpose satellite system for telecommunication, meteorological observation and broadcasting
T: IRS | the Indian Remote Sensing satellite system, used for resource monitoring and management
Q: Radio broadcasting in India started in 1923 by: | the Radio Club of Bombay | All India Radio | Doordarshan | ISRO
Q: Which satellite system is used for telecommunication, meteorological observation and broadcasting? | INSAT | IRS | GPS | Landsat
Q: The Indian Remote Sensing satellite IRS-1A was launched in: | 1988 | 1975 | 1995 | 2005
Q: Which of these is a means of mass communication? | Television | Letter | Telephone call | Personal e-mail
M:comm: INSAT | telecommunication, meteorology and broadcasting
M:comm: IRS | resource monitoring and management
M:comm: radio | started by the Radio Club of Bombay in 1923
M:comm: letter | personal communication
S+: Communication networks in India can be divided into personal communication and mass communication
S+: The postal network of India is one of the largest in the world
S+: Satellite communication helps in weather forecasting, disaster warning, broadcasting and resource mapping
S+: Satellite communication in India is managed through two systems, INSAT and IRS
S+: The National Remote Sensing Agency at Hyderabad provides facilities for acquiring and processing satellite data
S-: INSAT is used only for remote sensing of resources | INSAT is a multi-purpose system for telecommunication, meteorology and broadcasting; IRS is for remote sensing
S-: Radio broadcasting in India started in 1957 | It started in 1923 through the Radio Club of Bombay
S-: Newspapers are a means of personal communication | They are a means of mass communication
C: Satellites have revolutionised communication in India | they provide nationwide telecommunication, broadcasting and weather forecasting even in remote areas
C: Mass media are important in a democracy | they spread information, education and awareness among a large population
X: C2 D2 2 | Distinguish between personal and mass communication with examples. | Personal – between individuals (letters, telephone, e-mail); mass – to large numbers (radio, television, newspapers, films).
L: D4 | Describe the communication networks of India, including satellite communication. | Personal communication (postal, telephone, internet); mass communication (radio from 1923, television, newspapers, films); satellites – INSAT (telecom, meteorology, broadcasting), IRS (IRS-1A 1988, resource mapping); importance.
""")]

CH16 = [ST(S + '16-st1', "changing pattern of India's exports and imports", """
T: composition of trade | the types of goods and services that a country exports and imports
T: balance of payments | the record of all economic transactions of a country with the rest of the world
Q: Which item dominates India's imports? | Petroleum and crude products | Tea | Jute | Cotton textiles
Q: The share of agriculture and allied products in India's exports has: | declined | increased steadily | remained unchanged | become the only export
Q: In the 1950s and 1960s India imported large quantities of: | foodgrains | software services | iron ore | petroleum products for export
Q: Which of these is an important item of both export and import for India? | Gems and jewellery | Tea | Coal | Jute
S+: The share of agriculture and allied products in India's exports has declined
S+: The share of petroleum products and manufactured goods in India's exports has increased
S+: Petroleum and crude products form the largest item in India's imports
S+: India imported foodgrains in the 1950s and 1960s, but the Green Revolution reduced this dependence
S+: Gems and jewellery are an important part of both India's exports and imports
S-: The share of agriculture in India's exports has increased steadily | It has declined over time
S-: Foodgrains are the largest item of India's imports today | Petroleum and crude products are the largest import
S-: India does not import any gems or precious stones | Pearls, precious stones and gold are important imports
C: India's imports of foodgrains declined after the 1960s | the Green Revolution increased domestic production of wheat and rice
C: Petroleum dominates India's imports | domestic production of crude oil is not enough to meet growing demand
X: C2 D2 2 | Mention two changes in the composition of India's exports. | Decline in share of agriculture and allied products; increase in petroleum products, manufactured goods, engineering goods, gems and jewellery.
L: D4 | Describe the changing composition of India's exports and imports since independence. | Exports – decline of agriculture, rise of manufactures, petroleum products, gems and jewellery; imports – foodgrains earlier, now petroleum, gold and precious stones, machinery, electronics, fertilisers; role of Green Revolution.
"""), ST(S + '16-st2', "direction of India's trade", """
T: direction of trade | the countries and regions with which a country trades
T: trading partner | a country with which another country carries out a large volume of trade
Q: The direction of trade refers to: | the countries with which a country trades | the types of goods traded | the total value of trade | the difference between exports and imports
Q: In recent decades, India's trade with Asian countries has: | increased | stopped | declined to zero | remained unchanged since 1950
Q: India's trade with ASEAN countries has grown mainly because of: | closer economic ties and the 'Look East' approach | the closure of sea routes | a ban on Asian imports | the end of all trade blocs
S+: India has trade relations with most countries and major trading blocs of the world
S+: The share of Asian countries in India's trade has increased
S+: The USA, China and the UAE are among India's important trading partners
S+: India aims to increase its share in world trade
S-: India trades only with European countries | India trades with countries in all continents and trading blocs
S-: Asia's share in India's trade has declined | It has increased
S-: The direction of trade means the total value of trade | It refers to the countries a country trades with
C: India's trade with Asia has grown | Asian economies have grown fast and India has built closer economic ties with them
C: India trades with many countries | it needs a variety of goods and markets that no single region can provide
X: C2 D2 2 | What is meant by direction of trade? Name two important trading partners of India. | Countries a country trades with; USA, China, UAE (any two).
L: D4 | Explain the direction of India's international trade and the reasons for its changes. | Trade with all continents and blocs; rising share of Asia and ASEAN; USA, China, UAE among main partners; reasons – liberalisation, growth of Asian economies, closer ties; aim to increase share in world trade.
"""), ST(S + '16-st3', "sea ports and airports as gateways of India's trade", """
T: tidal port | a port that is affected by tides, such as Kandla in the Gulf of Kachchh
T: riverine port | a port located on a river, such as Kolkata on the Hugli
T: landlocked harbour | a harbour protected by land on most sides, such as Visakhapatnam
Q: Which port was developed after independence to ease the volume of trade on Mumbai port? | Kandla | Kochi | Chennai | Paradip
Q: Kolkata port is located on the river: | Hugli | Mahanadi | Godavari | Krishna
Q: Which port is described as the deepest landlocked and well-protected port of India? | Visakhapatnam | Kolkata | Kandla | Tuticorin
Q: Paradip port is situated in the delta of the: | Mahanadi | Godavari | Ganga | Krishna
Q: Marmagao port is situated in: | Goa | Karnataka | Kerala | Gujarat
Q: Which port handles iron ore concentrates exported from Kudremukh? | New Mangalore | Kandla | Haldia | Paradip
M:port: Kandla | Gulf of Kachchh, Gujarat
M:port: Marmagao | Goa
M:port: Kochi | Kerala
M:port: Paradip | Mahanadi delta, Odisha
M:port: Visakhapatnam | Andhra Pradesh
M:port: Haldia | downstream of Kolkata on the Hugli
P: Kandla | a tidal port in the Gulf of Kachchh, Gujarat
P: Mumbai | the biggest port of India with a spacious natural harbour
P: Marmagao | a port of Goa at the entrance of the Zuari estuary
P: New Mangalore | a port of Karnataka that exports iron ore from Kudremukh
P: Kochi | a natural harbour of Kerala at the head of the Vembanad Kayal
P: Tuticorin | a port of Tamil Nadu trading with Sri Lanka and the Maldives
P: Chennai | one of the oldest artificial ports on the east coast
P: Visakhapatnam | the deepest landlocked and well-protected port of India
P: Paradip | a port in the Mahanadi delta in Odisha
P: Kolkata | a riverine port on the Hugli about 128 km inland from the Bay of Bengal
S+: Kandla was the first port developed after independence to ease the volume of trade on Mumbai port
S+: Mumbai is the biggest port with a spacious natural and well-sheltered harbour
S+: Jawaharlal Nehru Port at Nhava Sheva was developed as a satellite port to relieve pressure on Mumbai port
S+: Kolkata is a riverine port on the Hugli about 128 km inland from the Bay of Bengal, and it faces the problem of silting
S+: Haldia, about 105 km downstream from Kolkata, was developed to reduce congestion at Kolkata port
S+: Visakhapatnam is connected to the sea by a channel cut through solid rock and sand
S-: Kolkata is a deep-water sea port on the open coast | It is a riverine port on the Hugli, 128 km inland, and faces silting
S-: Kandla is located on the east coast | Kandla is on the west coast in the Gulf of Kachchh, Gujarat
S-: Paradip is situated in the Godavari delta | It is situated in the Mahanadi delta in Odisha
C: Haldia port was developed | Kolkata port faced congestion and silting, so a port downstream was needed
C: Kandla port was developed after independence | Karachi went to Pakistan at Partition and the volume of trade on Mumbai port had to be eased
C: Marmagao is important for India's exports | it handles large exports of iron ore from Goa
X: C2 D2 2 | Why was Kandla port developed after independence? | To ease the volume of trade on Mumbai port after Karachi went to Pakistan at Partition; it serves the vast hinterland of north-western India.
X: C3 D3 3 | Describe any three major ports on the east coast of India. | Kolkata (riverine, Hugli, silting) and Haldia; Paradip (Mahanadi delta, iron ore); Visakhapatnam (deepest landlocked, protected); Chennai (old artificial port); Tuticorin (trade with Sri Lanka and Maldives).
L: D4 | Describe the major sea ports of India on the west and east coasts. | West – Kandla, Mumbai, JNPT, Marmagao, New Mangalore, Kochi; east – Tuticorin, Chennai, Visakhapatnam, Paradip, Kolkata, Haldia; features and functions; airports as gateways for light and valuable cargo.
""")]

CH17 = [ST(S + '17-st1', 'environmental pollution', """
T: environmental pollution | the release of substances and energy as waste products of human activities, resulting in harmful changes in the natural environment
T: water pollution | the degradation of water quality by the release of industrial, agricultural and domestic wastes into water bodies
T: air pollution | the addition of contaminants such as dust, fumes, gas, mist and smoke to air in amounts and durations harmful to life and property
T: noise pollution | the state of unbearable and uncomfortable sound caused by various sources, measured in decibels
T: smog | a mixture of smoke and fog that forms over cities and harms health
Q: The unit used to measure noise is: | decibel | hertz | pascal | joule
Q: Which two rivers are described as highly polluted in India? | The Ganga and the Yamuna | The Narmada and the Tapi | The Mahanadi and the Godavari | The Kaveri and the Krishna
Q: Which of these is a major source of air pollution? | Combustion of fossil fuels | Afforestation | Rainwater harvesting | Organic farming
Q: Pilgrimages, religious fairs and tourism cause water pollution through: | cultural activities | mining | shifting cultivation | rainfall
M:poll: water pollution | industrial effluents and sewage
M:poll: air pollution | combustion of fossil fuels
M:poll: noise pollution | measured in decibels
M:poll: land pollution | improper disposal of solid waste
S+: Pollution can be classified as water, air, land and noise pollution
S+: Industries such as leather, pulp and paper, textiles and chemicals discharge effluents into rivers
S+: Air pollution causes respiratory, nervous and circulatory diseases
S+: Noise from factories, construction, vehicles and aircraft is a major source of noise pollution
S+: Smog forms over many cities and harms human health
S-: Noise is measured in hertz | Noise level is measured in decibels
S-: Air pollution has no effect on human health | It causes respiratory, nervous and circulatory diseases
S-: Cultural activities such as religious fairs do not pollute water | They add organic and other wastes to rivers and lakes
C: Rivers such as the Ganga and Yamuna are highly polluted | cities and industries along them discharge untreated sewage and industrial effluents
C: Noise pollution is high in big cities | heavy traffic, construction, factories and loudspeakers produce loud sounds continuously
X: C2 D2 2 | Name two sources each of air pollution and noise pollution. | Air – combustion of fossil fuels, mining, industries, vehicles; noise – factories, construction, vehicles, aircraft, loudspeakers (any two each).
X: C3 D3 3 | Explain the main sources of water pollution in India. | Industrial effluents (leather, paper, textiles, chemicals); untreated urban sewage; agricultural chemicals; cultural activities (pilgrimages, religious fairs, immersion); Ganga and Yamuna examples.
L: D4 | Describe the types of environmental pollution in India, their sources and effects. | Water (industry, sewage, agriculture, cultural activities; diseases); air (fossil fuels, mining, industry; smog, respiratory diseases); noise (decibels; traffic, factories); land pollution; need for control.
"""), ST(S + '17-st2', 'urban waste disposal and slums', """
T: solid waste | a variety of old and used articles such as rusted metal, broken glass, plastic, paper and food waste discarded by households and industries
T: slums | residential areas of the least choice, with dilapidated houses, poor hygienic conditions, poor ventilation and lack of basic amenities
T: Dharavi | a slum in Mumbai described as one of the largest slums of Asia
Q: Dharavi, described as one of Asia's largest slums, is in: | Mumbai | Kolkata | Delhi | Chennai
Q: Slums are characterised by: | poor housing, sanitation and lack of basic amenities | wide roads and parks | planned drainage | high-rise apartments
Q: A major cause of the growth of slums in Indian cities is: | rural-urban migration of the poor | decline in city population | lack of jobs in villages being solved | planned housing for all
S+: Solid waste causes health hazards by creating foul smells and breeding flies and rodents
S+: Solid waste should be treated as a resource for energy and compost
S+: Slum dwellers often work in low-paid, risky occupations in the informal sector
S+: Rural-urban migration of poor people seeking jobs leads to the growth of slums
S+: Slums lack safe drinking water, sanitation and proper drainage
S-: Slums have well-ventilated houses and good sanitation | They have dilapidated houses, poor ventilation and poor sanitation
S-: Solid waste is harmless if left in the open | It breeds flies and rodents and spreads diseases
S-: Dharavi is in Kolkata | Dharavi is in Mumbai
C: Slums grow in big cities | poor migrants from rural areas cannot afford proper housing in the city
C: Uncollected solid waste is a health hazard | it gives off foul smells and breeds flies, rodents and diseases
X: C2 D2 2 | Mention two problems faced by slum dwellers. | Poor housing and ventilation; lack of safe drinking water, sanitation and drainage; diseases; low-paid insecure jobs; crime and social problems (any two).
L: D4 | Explain the problems of urban waste disposal and slums in Indian cities with reference to Dharavi. | Solid waste sources and health hazards; waste as resource (energy, compost); slums – causes (migration, poverty), conditions (housing, water, sanitation, health), Dharavi; need for planning.
"""), ST(S + '17-st3', 'land degradation and the case study approach', """
T: land degradation | the temporary or permanent decline in the productive capacity of land
T: wasteland | degraded land that is unproductive, such as gullied land, desert sands and barren rocky areas
T: watershed management | a programme to conserve land and water through community participation, as in Jhabua district
Q: Gullied and ravinous land, desert sands and barren rocky areas are examples of: | land degraded by natural processes | land degraded by human activities | net sown area | current fallow
Q: Waterlogged and saline lands are examples of land degraded by: | human activities | glaciers | volcanic activity | coastal sands
Q: Jhabua district, a case study of watershed management, is in: | Madhya Pradesh | Rajasthan | Gujarat | Maharashtra
Q: The tribal community of Jhabua district associated with watershed management is the: | Bhils | Gaddis | Todas | Nagas
S+: Land degradation can be caused by natural processes and by human activities
S+: Waterlogged, saline and alkaline lands are mostly degraded by human activities
S+: The watershed management programme in Jhabua district has helped prevent land degradation and improve soil quality
S+: The Bhils of Jhabua revitalised common property resources through their own efforts
S+: The case study approach examines a problem in a specific area in detail
S-: Waterlogging is caused only by natural processes | It is mostly caused by human activities such as over-irrigation
S-: Jhabua district is in Rajasthan | It is in Madhya Pradesh
S-: Land degradation always increases the productivity of land | It reduces the productive capacity of land
C: Over-irrigation has degraded land in many areas | excess water raises the water table, causing waterlogging and salinity
C: Watershed management succeeded in Jhabua | the local Bhil community participated in conserving land, water and common property resources
X: C2 D2 2 | Distinguish between land degraded by natural processes and by human activities with examples. | Natural – gullied and ravinous land, desert or coastal sands, barren rocky areas, steep slopes, glacial areas; human – waterlogged, saline and alkaline land, degraded forests, mining areas.
L: D4 | Explain the causes of land degradation in India and the lessons from the Jhabua watershed management programme. | Natural and human causes; waterlogging, salinity, deforestation, mining; Jhabua – western Madhya Pradesh, Bhils, watershed programme, soil and water conservation, revival of common property resources, community participation.
""")]

CHAPTERS = [
    (CH09, {'chapter_topic': "India's population"}),
    (CH10, {'chapter_topic': 'human settlements'}),
    (CH11, {'chapter_topic': 'land resources and agriculture'}),
    (CH12, {'chapter_topic': 'water resources'}),
    (CH13, {'chapter_topic': 'mineral and energy resources', 'map_name': INDIA}),
    (CH14, {'chapter_topic': 'planning and sustainable development'}),
    (CH15, {'chapter_topic': 'transport and communication in India', 'map_name': INDIA}),
    (CH16, {'chapter_topic': "India's international trade", 'map_name': INDIA}),
    (CH17, {'chapter_topic': 'geographical perspective on selected issues'}),
]
