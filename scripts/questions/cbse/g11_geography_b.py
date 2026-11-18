"""CBSE class 11 Geography, Fundamentals of Physical Geography (chapters 7-12): fact tables for g12_hum_engine."""
from g12_hum_engine import ST

S = 'cbse-g11-geography-ch'
WORLD = 'an outline map of the world'

CH07 = [ST(S + '07-st1', 'the composition of the atmosphere', """
T: atmosphere | the envelope of air (a mixture of gases, water vapour and dust particles) that surrounds the earth
T: ozone | a gas found mainly between 10 and 50 km above the earth's surface that absorbs ultraviolet rays of the sun
T: water vapour | the variable gaseous form of water in the atmosphere, up to 4 per cent by volume in warm and wet tropics
T: hygroscopic nuclei | dust and salt particles around which water vapour condenses to form clouds
T: greenhouse gas | a gas such as carbon dioxide that is transparent to incoming solar radiation but absorbs outgoing terrestrial radiation
Q: Which gas forms the largest share of the atmosphere by volume? | Nitrogen | Oxygen | Argon | Carbon dioxide
Q: Which of the following gases absorbs ultraviolet radiation from the sun? | Ozone | Nitrogen | Argon | Helium
Q: The proportion of water vapour in the atmosphere can be as high as 4 per cent by volume in: | warm and wet tropics | cold polar regions | dry deserts | high mountain tops
Q: Which gas is largely responsible for the greenhouse effect among the following? | Carbon dioxide | Nitrogen | Argon | Neon
Q: Dust particles in the atmosphere act as: | hygroscopic nuclei for condensation | a source of oxygen | absorbers of ultraviolet rays | a source of ozone
Q: About 99 per cent of the total mass of the atmosphere lies within a height of about: | 32 km | 8 km | 100 km | 500 km
M:gas-share: Nitrogen | about 78 per cent by volume
M:gas-share: Oxygen | about 21 per cent by volume
M:gas-share: Argon | about 0.93 per cent by volume
M:gas-share: Carbon dioxide | about 0.036 per cent by volume
S+: The atmosphere is a mixture of many gases along with water vapour and dust particles
S+: Water vapour decreases with altitude
S+: Water vapour absorbs part of the insolation and also preserves the earth's radiated heat
S+: Dust particles are generally concentrated in the lower layers of the atmosphere
S+: Subtropical and temperate regions have more dust particles than equatorial and polar regions because of dry winds
S+: Carbon dioxide in the atmosphere has been rising because of the burning of fossil fuels
S-: Oxygen is the most abundant gas in the atmosphere | Nitrogen is the most abundant gas, about 78 per cent by volume
S-: Water vapour increases with altitude | Water vapour decreases with altitude
S-: Ozone absorbs infrared radiation from the sun | Ozone absorbs ultraviolet radiation from the sun
S-: Dust particles are most concentrated in the upper atmosphere | They are concentrated in the lower layers of the atmosphere
C: Ozone is important for life on earth | it absorbs ultraviolet rays of the sun and prevents them from reaching the surface
C: Carbon dioxide is called a greenhouse gas | it is transparent to incoming solar radiation but absorbs outgoing terrestrial radiation
C: Water vapour helps keep the earth from becoming too hot or too cold | it absorbs part of the insolation and preserves the earth's radiated heat, acting like a blanket
C: Dust particles are important for weather | they act as hygroscopic nuclei around which water vapour condenses to form clouds
X: C2 D2 2 | State two roles of water vapour in the atmosphere. | It absorbs part of the insolation; it preserves the earth's radiated heat (acting as a blanket); it is the source of clouds and precipitation; it contributes to the stability or instability of air.
X: C3 D3 3 | Explain the importance of carbon dioxide, ozone and dust particles in the atmosphere. | Carbon dioxide – greenhouse gas absorbing terrestrial radiation; ozone – absorbs ultraviolet rays (10–50 km); dust – hygroscopic nuclei for condensation and cloud formation.
L: D4 | Describe the composition of the atmosphere. | Gases – nitrogen about 78%, oxygen about 21%, argon, carbon dioxide (greenhouse gas, rising due to fossil fuels), ozone (10–50 km, absorbs UV); water vapour – up to 4% in warm wet tropics, less in cold dry areas, decreases with height, absorbs and preserves heat; dust particles – lower layers, more in subtropical and temperate areas, hygroscopic nuclei.
"""), ST(S + '07-st2', 'the structure of the atmosphere', """
T: troposphere | the lowermost layer of the atmosphere, about 13 km thick on average, in which all weather changes take place
T: tropopause | the zone separating the troposphere from the stratosphere
T: stratosphere | the layer above the tropopause extending up to about 50 km, which contains the ozone layer
T: mesosphere | the layer between about 50 and 80 km in which temperature decreases with height to about minus 100°C
T: ionosphere | the layer between about 80 and 400 km containing electrically charged particles that reflect radio waves
T: exosphere | the uppermost layer of the atmosphere, about which very little is known
Q: All weather phenomena take place in the: | troposphere | stratosphere | mesosphere | ionosphere
Q: The ozone layer is found in the: | stratosphere | troposphere | mesosphere | exosphere
Q: Radio waves transmitted from the earth are reflected back by the: | ionosphere | troposphere | stratosphere | mesosphere
Q: The thickness of the troposphere is greatest at the: | equator | poles | tropic of Cancer | Arctic Circle
Q: In the mesosphere, temperature falls to about minus 100°C at a height of about: | 80 km | 13 km | 30 km | 400 km
Q: The height of the troposphere at the poles is about: | 8 km | 18 km | 50 km | 80 km
M:layer-height: Troposphere | from the surface up to about 13 km on average
M:layer-height: Stratosphere | from the tropopause up to about 50 km
M:layer-height: Mesosphere | from about 50 km to 80 km
M:layer-height: Ionosphere | from about 80 km to 400 km
S+: The atmosphere consists of layers with different density and temperature
S+: The troposphere is about 18 km thick at the equator and about 8 km at the poles
S+: Temperature in the troposphere decreases at the rate of about 1°C for every 165 m of height
S+: The air temperature at the tropopause is about minus 80°C over the equator and about minus 45°C over the poles
S+: The stratosphere contains the ozone layer
S+: Density of air is highest near the earth's surface and decreases rapidly with height
S-: The troposphere is thickest at the poles | It is thickest at the equator (about 18 km) because heat is carried up by strong convection
S-: The ozone layer is found in the mesosphere | The ozone layer is found in the stratosphere
S-: Temperature increases with height in the troposphere | It decreases at about 1°C for every 165 m of height
S-: The ionosphere lies below the stratosphere | The ionosphere lies above the mesosphere, between about 80 and 400 km
C: The troposphere is the most important layer for all biological activity | it contains dust particles and water vapour, and all changes in weather and climate take place in it
C: The troposphere is thicker at the equator than at the poles | strong convectional currents at the equator carry heat to greater heights
C: The stratosphere is important for life | it contains the ozone layer, which absorbs ultraviolet radiation and shields life from intense harmful energy
C: The ionosphere helps radio communication | its electrically charged particles reflect radio waves transmitted from the earth back to the earth
X: C2 D2 2 | Why is the troposphere the most important layer of the atmosphere? | It contains dust particles and water vapour; all weather changes take place in it; it supports biological activity.
X: C3 D3 3 | State three characteristics of the stratosphere. | Lies above the tropopause up to about 50 km; contains the ozone layer; ozone absorbs ultraviolet radiation and shields life; temperature rises with height in it.
L: D4 | Describe the structure of the atmosphere with the help of a suitable diagram. | Troposphere – up to about 13 km (8 km poles, 18 km equator), weather, temperature falls 1°C per 165 m; tropopause (−80°C equator, −45°C poles); stratosphere – up to 50 km, ozone layer; mesosphere – 50–80 km, temperature to −100°C; ionosphere – 80–400 km, electrically charged, reflects radio waves; exosphere – uppermost, little known.
"""), ST(S + '07-st3', 'the elements of weather and climate', """
T: weather | the momentary state of the atmosphere at a place
T: climate | the average of weather conditions over a long period of time
T: elements of weather | temperature, pressure, winds, humidity, clouds and precipitation, which together describe weather and climate
Q: The momentary state of the atmosphere at a place is called: | weather | climate | season | atmosphere
Q: The average of weather conditions over a long period is called: | climate | weather | humidity | pressure
Q: Which of the following is NOT an element of weather and climate? | Latitude | Temperature | Humidity | Precipitation
Q: Which of the following changes more quickly at a place? | Weather | Climate | Latitude | Altitude
S+: The main elements of weather and climate are temperature, pressure, winds, humidity, clouds and precipitation
S+: Weather changes quickly, even within a day or week
S+: Climate changes very slowly and may remain unchanged for 50 years or more
S+: The elements of weather and climate are interrelated
S-: Climate is the momentary state of the atmosphere | Weather is the momentary state; climate is the average over a long period
S-: Latitude is an element of weather | Latitude is a factor controlling climate, not an element of weather
S-: Weather does not change during a day | Weather changes quickly, even within a day
C: The climate of a place changes very slowly | it is the average of weather conditions over a long period of time
C: Temperature, pressure, winds and humidity are studied together | they are interrelated elements, and a change in one affects the others
X: C2 D2 2 | Distinguish between weather and climate. | Weather – momentary state of the atmosphere, changes quickly; climate – average of weather over a long period, changes slowly.
X: C3 D3 3 | Name the elements of weather and climate and explain how they are interrelated. | Temperature, pressure, winds, humidity, clouds, precipitation; e.g., heating lowers pressure, which causes winds; winds carry moisture that forms clouds and rain.
"""), ]

CH08 = [ST(S + '08-st1', 'insolation and the heating and cooling of the atmosphere', """
T: insolation | the incoming solar radiation received by the earth's surface in short waves
T: terrestrial radiation | the heat radiated by the earth in long-wave form, which heats the atmosphere from below
T: conduction | the transfer of heat from a warmer body to a cooler body in contact, as from the heated earth to the lowest layers of air
T: convection | the vertical transfer of heat by rising heated air, which is confined to the troposphere
T: advection | the transfer of heat through horizontal movement of air
T: aphelion | the position of the earth farthest from the sun (about 152 million km), around 4 July
T: perihelion | the position of the earth nearest to the sun (about 147 million km), around 3 January
Q: The earth is farthest from the sun (aphelion) around: | 4 July | 3 January | 21 March | 23 September
Q: The earth is nearest to the sun (perihelion) around: | 3 January | 4 July | 21 June | 22 December
Q: The transfer of heat through the horizontal movement of air is called: | advection | convection | conduction | radiation
Q: The 'loo' of northern India in summer is an outcome of: | advection | convection | conduction | condensation
Q: The axis of the earth makes an angle of 66½° with the plane of its orbit. This affects insolation through the: | angle of inclination of the sun's rays | distance between the earth and the moon | speed of ocean currents | density of rocks
Q: The maximum insolation on the earth's surface is received over the: | subtropical deserts | equatorial forests | polar ice caps | temperate grasslands
Q: The atmosphere is heated mainly by: | terrestrial radiation | direct absorption of insolation | heat from the earth's interior | heat from the moon
Q: The blue colour of the sky is due to: | scattering of sunlight by small particles | absorption of red light by ozone | reflection from the oceans | condensation of water vapour
M:heat-transfer: Conduction | transfer of heat between bodies in contact
M:heat-transfer: Convection | vertical transfer of heat by rising air
M:heat-transfer: Advection | horizontal transfer of heat by moving air
M:heat-transfer: Terrestrial radiation | heat given off by the earth in long waves
S+: The earth receives most of its energy from the sun in short wavelengths
S+: The amount of insolation varies with the angle of inclination of the sun's rays, length of day, transparency of the atmosphere and configuration of land
S+: Insolation is generally higher in the tropics than at the equator because the equator has more cloudiness
S+: The atmosphere is largely transparent to short-wave solar radiation
S+: Convection is confined to the troposphere
S+: In middle latitudes, most of the diurnal variation in weather is caused by advection
S-: The earth is nearest to the sun in July | It is nearest (perihelion) around 3 January and farthest (aphelion) around 4 July
S-: The atmosphere is heated mainly by direct insolation | It is heated mainly by terrestrial radiation from below
S-: Advection is the vertical transfer of heat | Advection is horizontal transfer of heat; convection is vertical
S-: Maximum insolation is received at the equator | Maximum insolation is received over subtropical deserts, where cloudiness is least
C: The atmosphere is heated from below | it is largely transparent to incoming short-wave radiation and absorbs the long-wave terrestrial radiation from the earth
C: Subtropical deserts receive the maximum insolation | cloudiness is least there
C: The sun appears red at sunrise and sunset | sunlight passes through a greater thickness of atmosphere and the shorter blue wavelengths are scattered away
C: The annual variation in the earth-sun distance does not have a great effect on daily weather | its effect is masked by other factors such as the distribution of land and sea and atmospheric circulation
X: C2 D2 2 | Name four factors that cause variation in insolation at the earth's surface. | Rotation of the earth on its axis; angle of inclination of the sun's rays; length of the day; transparency of the atmosphere; configuration of land (aspect).
X: C3 D3 3 | Explain how the atmosphere is heated by conduction, convection and advection. | Conduction – heated earth warms the lowest layer of air in contact; convection – heated air rises vertically, confined to the troposphere; advection – horizontal movement of air transfers heat, e.g., loo.
L: D4 | Discuss the factors that influence the amount of insolation received at the earth's surface. | Rotation and inclination of the axis (66½°); angle of the sun's rays – vertical rays heat a smaller area; length of day; transparency of atmosphere – clouds, dust, water vapour; configuration of land; earth-sun distance (perihelion 3 January, aphelion 4 July); subtropical deserts receive maximum.
"""), ST(S + '08-st2', 'the heat budget of the planet earth', """
T: heat budget | the balance between the incoming solar radiation and the outgoing terrestrial radiation that keeps the earth's temperature constant
T: albedo | the amount of radiation reflected back to space by the earth, about 35 units out of 100
T: heat surplus | the excess of incoming over outgoing radiation, found between about 40° north and 40° south
T: heat deficit | the excess of outgoing over incoming radiation, found towards the poles beyond about 40° latitude
Q: Of every 100 units of insolation reaching the top of the atmosphere, how many units are reflected back to space as albedo? | 35 | 14 | 51 | 65
Q: Of every 100 units of insolation, how many units are absorbed by the earth's surface? | 51 | 35 | 14 | 17
Q: Of every 100 units of insolation, how many units are absorbed by the atmosphere directly? | 14 | 35 | 51 | 48
Q: The surplus of heat energy is found between latitudes of about: | 40° north and 40° south | 60° north and 60° south | 10° north and 10° south | 23½° north and 66½° north
Q: The heat from the tropics is redistributed towards the poles mainly by: | atmospheric and oceanic circulation | volcanic eruptions | earthquakes | the rotation of the moon
S+: The earth as a whole does not accumulate or lose heat; it maintains its temperature
S+: Out of 100 units of insolation, 27 units are reflected from the top of the clouds and 2 units from snow and ice-covered areas
S+: The earth's surface absorbs 51 units of insolation and radiates the same amount back as terrestrial radiation
S+: Of the 51 units radiated by the earth, 17 units go directly to space and 34 units are absorbed by the atmosphere
S+: The atmosphere radiates 48 units back into space, made up of 14 units absorbed from insolation and 34 from terrestrial radiation
S+: There is a surplus of net radiation in the tropics and a deficit near the poles
S-: The earth's surface absorbs 35 units of insolation | It absorbs 51 units; 35 units are reflected as albedo
S-: The earth keeps getting warmer because it absorbs more heat than it loses | Over a long period, incoming and outgoing radiation balance and the earth's temperature remains constant
S-: Heat deficit is found in the tropics | Heat surplus is found in the tropics; heat deficit is found towards the poles
C: The earth's temperature remains constant over a long period | the amount of heat received as insolation equals the amount lost by terrestrial radiation
C: The tropics do not keep getting hotter and the poles colder | surplus heat is carried from the tropics to the poles by winds and ocean currents
C: Out of 100 units, only 65 units actually heat the earth system | 35 units are reflected back to space before reaching the surface or from snow and clouds
X: C2 D2 2 | What is meant by the heat budget of the earth? | The balance between incoming insolation and outgoing terrestrial radiation, which keeps the earth's temperature constant over time.
X: C3 D3 3 | Explain the latitudinal variation in the net radiation balance of the earth. | Surplus between about 40°N and 40°S; deficit towards the poles; surplus heat transferred poleward by winds and ocean currents, so the tropics do not keep heating.
L: D4 | Explain the heat budget of the planet earth with the help of a diagram. | 100 units – 35 reflected (27 clouds, 2 snow/ice, rest scattering) = albedo; 14 absorbed by atmosphere; 51 absorbed by surface; earth radiates 51 – 17 to space, 34 absorbed by atmosphere; atmosphere radiates 48 to space (14 + 34); total outgoing 65 = 17 + 48; balance keeps temperature constant; latitudinal surplus and deficit.
"""), ST(S + '08-st3', 'the factors controlling temperature and inversion of temperature', """
T: normal lapse rate | the decrease of temperature with height at the rate of about 6.5°C per 1,000 m
T: inversion of temperature | a situation in which temperature increases with height instead of decreasing
T: air drainage | the flow of cold, dense air down slopes into valleys at night, which can cause frost in valley bottoms
T: continentality | the effect of distance from the sea, which gives interior areas extreme temperatures
Q: The normal lapse rate is about: | 6.5°C per 1,000 m | 1°C per 1,000 m | 10°C per 100 m | 6.5°C per 100 m
Q: Inversion of temperature is common in: | polar areas | the equatorial region | hot deserts in summer afternoons | tropical oceans
Q: Which of the following conditions favours a surface inversion of temperature? | Long winter night with clear sky and still air | Cloudy sky with strong winds | Hot summer afternoon | Heavy rainfall
Q: Which of the following is NOT a factor controlling the distribution of temperature? | Rotation of the moon | Latitude | Altitude | Distance from the sea
Q: Places near the sea have a moderate climate because of the: | moderating influence of the sea | high altitude | low latitude only | absence of winds
S+: The temperature of a place depends on latitude, altitude, distance from the sea, air masses, ocean currents and local aspects
S+: Places at the same latitude but at different altitudes have different temperatures
S+: The sea gets heated and cools down slowly compared to land
S+: Warm ocean currents raise the temperature of coastal areas and cold currents lower it
S+: Frost and fog in valley bottoms at night are caused by air drainage
S-: Temperature increases with height in the troposphere under normal conditions | Normally temperature decreases at about 6.5°C per 1,000 m
S-: Places in the interior of continents have a moderate climate | The interior of continents has extreme temperatures because of continentality
S-: Inversion of temperature occurs on cloudy and windy nights | It occurs on long winter nights with clear skies and still air
C: Hill stations are cooler than the plains at the same latitude | temperature decreases with height at about 6.5°C per 1,000 m
C: Coastal places have a smaller range of temperature than inland places | the sea heats and cools slowly and moderates the temperature of nearby land
C: Plant life in valley bottoms may be damaged by frost on winter nights | cold dense air drains down the slopes at night and collects in the valleys
C: Inversion of temperature occurs on long, clear winter nights | the ground loses heat rapidly by radiation and cools the air in contact with it
X: C2 D2 2 | What is inversion of temperature? State two conditions favourable for it. | Temperature increases with height; long winter nights, clear skies, still air, dry air, snow-covered ground.
X: C3 D3 3 | Explain three factors that control the distribution of temperature. | Latitude – amount of insolation; altitude – lapse rate 6.5°C/1,000 m; distance from sea – moderating effect; air masses and ocean currents – warm or cold.
L: D4 | Discuss the factors that control the distribution of temperature on the earth's surface, and explain inversion of temperature. | Latitude; altitude (normal lapse rate 6.5°C/1,000 m); distance from sea (continentality); air masses and ocean currents; local aspects; inversion – long winter nights, clear skies, still air, common in polar areas; air drainage, frost and fog in valleys.
"""), ST(S + '08-st4', 'the distribution of temperature in January and July', """
T: isotherm | a line joining places having equal temperature
T: range of temperature | the difference between the mean temperatures of the warmest and the coldest months
Q: Lines joining places of equal temperature are called: | isotherms | isobars | isohyets | contours
Q: The highest annual range of temperature is found over the: | north-eastern part of Eurasia | equatorial oceans | Southern Ocean | western coast of Europe
Q: Isotherms are more regular in the southern hemisphere because it has: | a larger proportion of ocean | more mountains | more deserts | a larger landmass
Q: In January, isotherms bend northwards over the North Atlantic Ocean because of the: | warm North Atlantic Drift | cold Labrador Current | Himalayas | Siberian high
S+: Isotherms generally run parallel to the latitudes
S+: The effect of land and sea on temperature is more pronounced in the northern hemisphere
S+: In January, isotherms deviate northwards over the oceans and southwards over the continents in the northern hemisphere
S+: The least annual range of temperature is found over the equatorial oceans
S+: The highest range of temperature, more than 60°C, is found over the north-eastern part of the Eurasian continent because of continentality
S-: Isotherms in the northern hemisphere are more regular than in the southern hemisphere | They are more regular in the southern hemisphere, where oceans dominate
S-: The annual range of temperature is highest over equatorial oceans | It is least over equatorial oceans and highest over north-eastern Eurasia
S-: Isotherms join places of equal pressure | Isotherms join places of equal temperature; isobars join places of equal pressure
C: Isotherms are more regular in the southern hemisphere | the southern hemisphere has a much larger proportion of oceans, which heat and cool uniformly
C: North-eastern Eurasia has a very high range of temperature | it is far from the moderating influence of the sea (continentality)
C: Isotherms bend northwards over the North Atlantic in January | the warm North Atlantic Drift raises the temperature of the ocean and nearby coasts
X: C2 D2 2 | Why are isotherms more regular in the southern hemisphere? | The southern hemisphere has more ocean than land; water heats and cools uniformly, so temperatures change gradually with latitude.
X: C3 D3 3 | Explain the distribution of temperature in January in the northern hemisphere. | Isotherms bend north over oceans and south over continents; North Atlantic Drift bends them north; continents are very cold (Siberia); land-sea contrast marked.
L: D4 | Describe the distribution of temperature on the earth's surface in January and July. | Isotherms parallel to latitudes; January – northern hemisphere winter, bend north over oceans, south over land, North Atlantic Drift; July – isotherms bend north over continents; southern hemisphere more regular; highest range over north-eastern Eurasia (over 60°C), least over equatorial oceans.
""")]

CH09 = [ST(S + '09-st1', 'atmospheric pressure and the world pressure belts', """
T: atmospheric pressure | the weight of a column of air from mean sea level to the top of the atmosphere, measured in millibars
T: isobar | a line joining places having equal pressure
T: equatorial low | the belt of low pressure near the equator, also called the doldrums
T: subtropical high | the belt of high pressure along about 30° north and south, also called the horse latitudes
T: sub-polar low | the belt of low pressure along about 60° north and south
T: polar high | the area of high pressure near the poles
Q: The average atmospheric pressure at sea level is about: | 1,013.2 mb | 1,000 mb | 913.2 mb | 1,213.2 mb
Q: In the lower atmosphere, pressure decreases by about 1 mb for every rise of: | 10 m | 100 m | 1 m | 1,000 m
Q: The subtropical high-pressure belts are found along about: | 30° north and south | 60° north and south | 10° north and south | 90° north and south
Q: The equatorial low-pressure belt is also known as the: | doldrums | horse latitudes | roaring forties | westerlies
Q: Atmospheric pressure is measured by a: | barometer | thermometer | hygrometer | rain gauge
Q: Lines joining places of equal pressure are called: | isobars | isotherms | isohyets | isohalines
M:pressure-belt: Equatorial low | near the equator
M:pressure-belt: Subtropical high | about 30° north and south
M:pressure-belt: Sub-polar low | about 60° north and south
M:pressure-belt: Polar high | near the poles
S+: Air pressure is measured with a mercury barometer or an aneroid barometer
S+: Pressure decreases rapidly with height in the lower atmosphere
S+: The pressure belts shift with the apparent movement of the sun, northwards in summer and southwards in winter of the northern hemisphere
S+: Horizontal differences in pressure cause winds
S+: Low pressure is found near the equator and high pressure along the subtropics
S+: For the study of horizontal pressure, pressure is reduced to sea level to remove the effect of altitude
S-: Pressure increases with height | Pressure decreases with height, by about 1 mb per 10 m in the lower atmosphere
S-: The subtropical highs are found along 60° north and south | They are found along about 30°; sub-polar lows lie along 60°
S-: The pressure belts are fixed throughout the year | They shift with the apparent movement of the sun
C: There is a low-pressure belt near the equator | intense heating makes the air expand and rise
C: Pressure is reduced to sea level on weather maps | this removes the effect of altitude so that horizontal differences can be compared
C: Pressure belts shift north and south during the year | the zone of maximum heating moves with the apparent movement of the sun
X: C2 D2 2 | What are isobars? What does closely spaced isobars indicate? | Lines joining places of equal pressure; closely spaced isobars show a steep pressure gradient and strong winds.
X: C3 D3 3 | Describe the world distribution of pressure belts. | Equatorial low (doldrums); subtropical highs at about 30°N and S (horse latitudes); sub-polar lows at about 60°N and S; polar highs; shift with the sun.
L: D4 | Explain the vertical and horizontal distribution of atmospheric pressure. | Vertical – pressure decreases with height, about 1 mb per 10 m; sea-level average 1,013.2 mb; horizontal – isobars, pressure reduced to sea level; belts – equatorial low, subtropical highs (30°), sub-polar lows (60°), polar highs; seasonal shifting with the sun.
"""), ST(S + '09-st2', 'the forces affecting the velocity and direction of wind', """
T: pressure gradient | the rate of change of pressure with respect to distance, which is strong where isobars are close together
T: Coriolis force | the deflecting force caused by the rotation of the earth, which deflects winds to the right in the northern hemisphere and to the left in the southern hemisphere
T: frictional force | the force that slows wind near the earth's surface, greatest at the surface and extending up to about 1 to 3 km
T: geostrophic wind | a wind in the upper atmosphere that blows parallel to the isobars when the pressure gradient and Coriolis force are balanced
Q: The Coriolis force is maximum at the: | poles | equator | tropics | 30° latitudes
Q: In the northern hemisphere, the Coriolis force deflects winds to the: | right | left | east only | west only
Q: Winds in the upper atmosphere that blow parallel to the isobars are called: | geostrophic winds | trade winds | local winds | land breezes
Q: The force that makes winds move from high to low pressure is the: | pressure gradient force | Coriolis force | frictional force | gravitational force of the moon
Q: Tropical cyclones do not form near the equator because there the: | Coriolis force is zero | pressure gradient is very steep | sea surface is cold | air is always dry
Q: Around a low-pressure area in the northern hemisphere, winds circulate: | anticlockwise | clockwise | in straight lines | only from west to east
M:wind-force: Pressure gradient force | causes air to move from high to low pressure
M:wind-force: Coriolis force | deflects winds because of the earth's rotation
M:wind-force: Frictional force | slows winds near the earth's surface
M:wind-force: Centripetal acceleration | keeps winds moving around pressure centres in curved paths
S+: The Coriolis force is directly proportional to the angle of latitude
S+: The Coriolis force is absent at the equator
S+: The Coriolis force acts perpendicular to the pressure gradient force
S+: Friction is greatest at the earth's surface and is least over the sea surface
S+: In a cyclone in the southern hemisphere, winds circulate clockwise
S+: Wind velocity is greater where the pressure gradient is steep
S-: The Coriolis force is maximum at the equator | It is maximum at the poles and absent at the equator
S-: In the northern hemisphere, winds are deflected to the left | They are deflected to the right in the northern hemisphere and to the left in the southern
S-: Friction affects winds mainly in the upper atmosphere | Friction is greatest at the surface and extends up to about 1–3 km
C: Tropical cyclones do not form at the equator | the Coriolis force is zero there, so air does not spiral around a low-pressure centre
C: Winds over the sea blow faster than over land | friction is least over the sea surface
C: Winds in the upper atmosphere blow parallel to the isobars | there is little friction, and the pressure gradient and Coriolis force balance each other
C: Winds are deflected from their path | the rotation of the earth produces the Coriolis force
X: C2 D2 2 | What is the Coriolis force? How does it change with latitude? | Deflecting force due to the earth's rotation; right in NH, left in SH; maximum at the poles, absent at the equator; proportional to latitude.
X: C3 D3 3 | Explain the three forces that affect the velocity and direction of winds. | Pressure gradient force – drives air from high to low pressure; frictional force – slows wind at the surface, least over sea; Coriolis force – deflects winds, right in NH, left in SH.
L: D4 | Discuss the forces affecting the velocity and direction of winds and explain geostrophic winds. | Pressure gradient force (closely spaced isobars, strong winds); friction (surface to 1–3 km, least over sea); Coriolis force (right in NH, left in SH, max at poles, absent at equator, perpendicular to pressure gradient); geostrophic winds in upper air parallel to isobars; cyclonic and anticyclonic circulation.
"""), ST(S + '09-st3', 'the general circulation of the atmosphere, seasonal and local winds', """
T: Hadley cell | the circulation cell in the tropics in which air rises at the ITCZ and sinks at the subtropical highs
T: Ferrel cell | the circulation cell in the middle latitudes in which air sinks at the subtropical high and rises at the sub-polar low
T: polar cell | the circulation cell in which cold dense air subsides near the poles and blows towards the middle latitudes as polar easterlies
T: Inter Tropical Convergence Zone | the low-pressure zone near the equator where the trade winds converge and air rises (ITCZ)
T: El Nino | the warming of the central and eastern Pacific off the coast of Peru, which affects weather over large areas including India
T: Walker circulation | the east-west circulation of air over the Pacific Ocean, linked with El Nino
T: land breeze | the wind that blows from land to sea at night because land cools faster than the sea
T: sea breeze | the wind that blows from sea to land during the day because land heats faster than the sea
Q: Winds blowing from the subtropical highs towards the equatorial low are called: | trade winds | westerlies | polar easterlies | jet streams
Q: Winds blowing from the subtropical highs towards the sub-polar lows are called: | westerlies | trade winds | polar easterlies | monsoons
Q: The circulation cell of the tropics is called the: | Hadley cell | Ferrel cell | polar cell | Walker cell
Q: The ITCZ is a zone of: | convergence and rising air | divergence and sinking air | high pressure | calm polar air
Q: During the day, the wind that blows from sea to land is called the: | sea breeze | land breeze | valley breeze | mountain wind
Q: At night, cool air from the mountain slopes flowing down into the valley is called the: | mountain wind | valley breeze | sea breeze | trade wind
Q: El Nino is associated with the warming of the ocean off the coast of: | Peru | Japan | Norway | South Africa
M:circulation-cell: Hadley cell | tropical cell between the ITCZ and the subtropical high
M:circulation-cell: Ferrel cell | middle-latitude cell between the subtropical high and the sub-polar low
M:circulation-cell: Polar cell | cell in which air subsides near the poles and blows to middle latitudes
M:circulation-cell: Walker cell | east-west cell over the Pacific Ocean
S+: The pattern of planetary winds depends on latitudinal variation of heating, emergence of pressure belts, migration of belts with the sun, distribution of land and sea, and rotation of the earth
S+: The general circulation of the atmosphere also sets in motion the ocean water circulation
S+: El Nino is the reason why the monsoon rainfall over India is sometimes weak
S+: In mountain areas, during the day the slopes get heated and air moves upslope as the valley breeze
S+: Land and sea breezes are caused by differential heating and cooling of land and sea
S+: The monsoon winds reverse their direction seasonally
S-: Trade winds blow from the sub-polar lows to the subtropical highs | Trade winds blow from the subtropical highs to the equatorial low
S-: The sea breeze blows at night | The sea breeze blows by day; the land breeze blows at night
S-: The Ferrel cell is the circulation cell of the tropics | The Hadley cell is the tropical cell; the Ferrel cell is in the middle latitudes
C: The sea breeze blows during the day | land heats faster than the sea, creating lower pressure over land
C: The land breeze blows at night | land cools faster than the sea, so higher pressure develops over land
C: Air rises at the ITCZ | the trade winds converge there and strong heating causes convection
C: Valley bottoms are cold on winter nights in mountains | cool dense air from the slopes flows down into the valleys as mountain wind
X: C2 D2 2 | Distinguish between land breeze and sea breeze. | Sea breeze – by day, from sea to land, land heats faster; land breeze – at night, from land to sea, land cools faster.
X: C3 D3 3 | Explain the three-cell model of the general circulation of the atmosphere. | Hadley cell – air rises at ITCZ, sinks at subtropical highs, trade winds; Ferrel cell – middle latitudes, westerlies; polar cell – air subsides at poles, polar easterlies.
L: D4 | Discuss the general circulation of the atmosphere and its effect on the oceans. | Factors – heating, pressure belts, migration with sun, land-sea, rotation; ITCZ, Hadley cell, trade winds; Ferrel cell, westerlies; polar cell, polar easterlies; circulation drives ocean currents; El Nino and Walker circulation, effect on Indian monsoon.
"""), ST(S + '09-st4', 'air masses, fronts, cyclones and thunderstorms', """
T: air mass | a large body of air with fairly uniform temperature and humidity, acquired from its source region
T: front | the boundary zone formed when two different air masses meet
T: extra-tropical cyclone | a cyclone that develops along the polar front in the middle and high latitudes
T: tropical cyclone | a violent storm that originates over warm tropical oceans and moves towards coastal areas
T: eye | the calm central region of a mature tropical cyclone with subsiding air
T: tornado | a small but violent whirling storm that forms from a severe thunderstorm, mostly in middle latitudes
T: occluded front | a front formed when a cold front overtakes a warm front and lifts the warm air completely off the surface
Q: Which of the following is a condition for the formation of a tropical cyclone? | Large sea surface with temperature above 27°C | Cold ocean surface | Absence of Coriolis force | Strong vertical wind shear
Q: Tropical cyclones in the Atlantic Ocean are called: | hurricanes | typhoons | willy-willies | tornadoes
Q: Tropical cyclones in the western Pacific and South China Sea are called: | typhoons | hurricanes | willy-willies | blizzards
Q: The calm centre of a tropical cyclone is called the: | eye | front | trough | crest
Q: When a cold front overtakes a warm front, the front formed is a/an: | occluded front | stationary front | warm front | cold front
Q: Extra-tropical cyclones generally move: | from west to east | from east to west | from pole to equator | in a fixed place
Q: The area where an air mass forms is called its: | source region | front | eye | cell
M:cyclone-name: Hurricanes | tropical cyclones of the Atlantic Ocean
M:cyclone-name: Typhoons | tropical cyclones of the western Pacific and South China Sea
M:cyclone-name: Willy-willies | tropical cyclones of Western Australia
M:cyclone-name: Cyclones | tropical cyclones of the Indian Ocean
M:air-mass: Maritime tropical (mT) | warm, moist air from tropical oceans
M:air-mass: Continental tropical (cT) | hot, dry air from subtropical deserts
M:air-mass: Maritime polar (mP) | cold, moist air from high-latitude oceans
M:air-mass: Continental polar (cP) | cold, dry air from high-latitude land areas
S+: Tropical cyclones need a continuous supply of moisture and lose strength after landfall
S+: The eye of a tropical cyclone is surrounded by the eye wall, where the strongest winds and heaviest rain occur
S+: Extra-tropical cyclones cover a larger area than tropical cyclones
S+: Extra-tropical cyclones can originate over land and sea, while tropical cyclones originate only over seas
S+: Thunderstorms are caused by intense convection on moist hot days
S+: A tornado over the sea is called a water spout
S-: Tropical cyclones originate over land | They originate over warm tropical seas and weaken on reaching land
S-: Hurricanes are tropical cyclones of the western Pacific | Hurricanes occur in the Atlantic; typhoons occur in the western Pacific
S-: The eye of a cyclone has the strongest winds | The eye is calm; the strongest winds are in the eye wall
S-: Extra-tropical cyclones move from east to west | They move from west to east with the westerlies
C: Tropical cyclones weaken after landfall | their supply of moisture from the warm sea is cut off
C: Tropical cyclones form over warm oceans with temperatures above 27°C | the warm water supplies the moisture and latent heat that drive the storm
C: Air masses take on the qualities of their source region | they stay over large uniform areas of land or sea for a long time
C: Fronts bring changes in weather | warm air is forced to rise over cold air along them, causing clouds and precipitation
X: C2 D2 2 | What is an air mass? Name any two types. | A large body of air with uniform temperature and humidity; maritime tropical (mT), continental tropical (cT), maritime polar (mP), continental polar (cP), continental arctic (cA).
X: C3 D3 3 | State three conditions favourable for the formation of tropical cyclones. | Large sea surface above 27°C; presence of Coriolis force; small variation in vertical wind speed; a pre-existing weak low; upper-level divergence.
X: C3 D3 3 | Distinguish between tropical and extra-tropical cyclones. | Tropical – form over warm seas, smaller, more violent, east to west, weaken over land; extra-tropical – form along polar front, larger area, move west to east, over land and sea.
L: D4 | Describe the formation and structure of tropical cyclones. | Conditions – warm sea above 27°C, Coriolis force, low vertical wind shear, pre-existing low, upper divergence; energy from latent heat of condensation; eye (calm) and eye wall (strongest winds, heaviest rain); names – cyclones, hurricanes, typhoons, willy-willies; weaken on landfall; storm surge damage.
""")]

CH10 = [ST(S + '10-st1', 'humidity, evaporation and condensation', """
T: humidity | the water vapour present in the air
T: absolute humidity | the actual amount of water vapour present in the atmosphere, expressed as grams per cubic metre
T: relative humidity | the percentage of moisture present in the atmosphere compared with its full capacity at a given temperature
T: dew point | the temperature at which saturation occurs in a given sample of air
T: saturated air | air that contains the maximum amount of moisture it can hold at a given temperature
T: latent heat of vaporisation | the heat absorbed when water changes into water vapour
T: sublimation | the direct change of water vapour into ice when condensation takes place below freezing point
Q: The percentage of moisture in the air compared with its full capacity at a given temperature is: | relative humidity | absolute humidity | dew point | saturation
Q: The temperature at which a sample of air becomes saturated is called the: | dew point | freezing point | boiling point | lapse rate
Q: Absolute humidity is expressed in: | grams per cubic metre | per cent | millibars | degrees Celsius
Q: The change of water vapour directly into ice is called: | sublimation | evaporation | precipitation | infiltration
Q: Relative humidity is generally greater over: | oceans | deserts | continental interiors | high plateaus
Q: Condensation takes place when: | moist air is cooled to its dew point | air is heated | air sinks and is compressed | air becomes drier
S+: Water vapour present in the air varies from zero to about 4 per cent by volume
S+: The capacity of air to hold water vapour depends on its temperature
S+: Relative humidity changes with a rise or fall in temperature
S+: Evaporation is caused mainly by heat
S+: Condensation is the transformation of water vapour into water and takes place due to loss of heat
S+: Movement of air replaces saturated air with unsaturated air and so increases evaporation
S-: Relative humidity is expressed in grams per cubic metre | Absolute humidity is in grams per cubic metre; relative humidity is a percentage
S-: Warm air can hold less moisture than cold air | Warm air can hold more moisture than cold air
S-: Condensation is caused by a gain of heat | Condensation is caused by a loss of heat
C: Relative humidity falls when the air warms during the day | the capacity of air to hold moisture increases with temperature
C: Relative humidity is high over the oceans | there is a large supply of water for evaporation
C: Evaporation increases on a windy day | moving air replaces saturated air with unsaturated air
C: Clouds form when air rises | rising air cools, and when it reaches its dew point the water vapour condenses
X: C2 D2 2 | Distinguish between absolute humidity and relative humidity. | Absolute – actual water vapour in grams per cubic metre; relative – percentage of moisture compared with full capacity at that temperature.
X: C3 D3 3 | Explain the conditions under which condensation takes place. | Cooling of air to dew point – when volume is kept constant and temperature falls, when both volume and temperature fall, or when moisture is added by evaporation; needs hygroscopic nuclei; below freezing it is sublimation.
"""), ST(S + '10-st2', 'the forms of condensation: dew, frost, fog, mist and clouds', """
T: dew | moisture deposited as water droplets on cooler solid surfaces when the dew point is above freezing point
T: frost | ice crystals formed on cold surfaces when the dew point is at or below freezing point
T: fog | a cloud near the ground formed when a mass of air containing water vapour cools suddenly and visibility becomes poor
T: mist | a form of condensation similar to fog but containing more moisture, frequent over mountains
T: smog | fog mixed with smoke, found in urban and industrial centres
T: cirrus | high clouds formed at 8,000–12,000 m that are thin, detached and feathery
T: cumulus | clouds that look like cotton wool, generally formed at heights of 4,000–7,000 m
T: stratus | layered clouds covering large portions of the sky
T: nimbus | black or dark grey clouds formed at middle levels or very near the surface that bring rain
Q: Dew forms when the dew point is: | above freezing point | below freezing point | equal to the boiling point | above the air temperature
Q: Clouds that look like cotton wool are: | cumulus | cirrus | stratus | nimbus
Q: Thin, detached and feathery clouds at high altitudes are: | cirrus | cumulus | nimbus | stratus
Q: Black or dark grey rain-bearing clouds are: | nimbus | cirrus | cumulus | stratus
Q: Fog mixed with smoke is called: | smog | mist | frost | dew
Q: Frost forms when the dew point is: | at or below freezing point | above freezing point | above 30°C | equal to the air temperature at noon
M:cloud-type: Cirrus | thin, detached and feathery high clouds
M:cloud-type: Cumulus | clouds looking like cotton wool
M:cloud-type: Stratus | layered clouds covering large parts of the sky
M:cloud-type: Nimbus | black or dark grey rain-bearing clouds
S+: Clear sky, calm air, high relative humidity and cold long nights are ideal for the formation of dew
S+: Fogs are mini clouds in which condensation takes place around nuclei provided by dust, smoke and salt particles
S+: Mist contains more moisture than fog
S+: Clouds are masses of minute water droplets or tiny ice crystals formed by condensation of water vapour in free air at considerable height
S+: A combination of basic cloud types gives forms such as cumulonimbus and stratocumulus
S-: Dew forms when the dew point is below freezing point | Dew forms when the dew point is above freezing; frost forms when it is below
S-: Cirrus clouds are dark rain-bearing clouds near the ground | Cirrus are thin, feathery high clouds; nimbus are dark rain-bearing clouds
S-: Fog contains more moisture than mist | Mist contains more moisture than fog
C: Dew forms on calm, clear nights | the ground loses heat quickly and cools the air in contact to its dew point
C: Smog is common in industrial cities | smoke particles provide nuclei and mix with fog
C: Nimbus clouds bring rain | they are thick dark masses of water vapour formed at middle levels or near the surface
X: C2 D2 2 | Distinguish between dew and frost. | Dew – water droplets when the dew point is above freezing; frost – ice crystals when the dew point is at or below freezing.
X: C3 D3 3 | Describe the four basic types of clouds. | Cirrus – high (8,000–12,000 m), thin, feathery; cumulus – cotton wool, 4,000–7,000 m; stratus – layered, cover large areas; nimbus – dark grey, rain-bearing, middle levels or near surface.
"""), ST(S + '10-st3', 'precipitation, types of rainfall and the world distribution of rainfall', """
T: precipitation | the release of moisture from clouds in liquid or solid form, such as rain, snow, sleet or hail
T: sleet | frozen raindrops and refrozen melted snow-water
T: hailstones | pellets of ice formed when raindrops freeze while passing through layers of cold air
T: convectional rainfall | rainfall caused when heated air rises, cools and condenses, common in the equatorial region in the afternoon
T: orographic rainfall | rainfall caused when moist air is forced to rise over a mountain barrier, falling mainly on the windward side
T: rain-shadow area | the leeward side of a mountain that receives little rain
T: cyclonic rainfall | rainfall associated with cyclones and fronts
Q: Rainfall that occurs in the equatorial region in the afternoon with thunder and lightning is: | convectional | orographic | cyclonic | frontal only
Q: The leeward side of a mountain that receives less rainfall is called the: | rain-shadow area | windward side | doldrums | source region
Q: Frozen raindrops and refrozen melted snow-water are called: | sleet | hail | frost | dew
Q: Rainfall caused when moist air is forced to rise over mountains is: | orographic | convectional | cyclonic | sleet
Q: In the middle latitudes, coastal areas receive more rainfall on the: | western coasts | eastern coasts | interiors | leeward sides
M:rain-type: Convectional rainfall | heated air rises and cools; afternoon showers in equatorial areas
M:rain-type: Orographic rainfall | moist air forced up a mountain; windward side gets rain
M:rain-type: Cyclonic rainfall | rain associated with cyclones and fronts
M:rain-type: Rain-shadow | dry leeward side of a mountain
S+: Precipitation in the form of water is rainfall; when temperature is below 0°C it falls as snow
S+: The equatorial belt, the windward sides of mountains along western coasts and areas of monsoon receive heavy rainfall
S+: Rainfall decreases from the equator towards the poles
S+: Coastal areas receive more rainfall than interiors of continents
S+: Between 35° and 40° latitude, the eastern coasts receive more rain, and further polewards the western coasts receive more rain
S+: Interior continental areas receive moderate rainfall, and areas in rain-shadow and high latitudes receive less
S-: The windward side of a mountain receives less rainfall | The windward side receives more rain; the leeward side is in rain shadow
S-: Convectional rainfall is common in polar areas | It is common in the equatorial region and continental interiors in summer
S-: Rainfall increases from the equator towards the poles | Rainfall generally decreases from the equator towards the poles
C: The leeward side of a mountain receives little rainfall | descending air gets warmer and its capacity to hold moisture increases
C: Equatorial regions get rain almost every afternoon | intense heating causes air to rise by convection, cool and condense
C: Coastal areas receive more rainfall than interiors | moisture-laden winds from the sea shed most of their moisture near the coast
X: C2 D2 2 | What is orographic rainfall? Where does the rain-shadow area lie? | Rain caused when moist air rises over a mountain barrier; the rain-shadow lies on the leeward side, where descending air warms.
X: C3 D3 3 | Describe the three types of rainfall. | Convectional – heating, rising, afternoon rain in equatorial areas; orographic – moist air forced over mountains, windward rain, leeward rain shadow; cyclonic – associated with cyclones and fronts.
L: D4 | Describe the world distribution of rainfall. | Decreases from equator to poles; coasts wetter than interiors; equatorial belt and windward western coasts and monsoon areas heavy; 35°–40° east coasts wetter, further polewards west coasts; interiors moderate; rain-shadow and high latitudes low; more rain over oceans than land.
""")]

CH11 = [ST(S + '11-st1', 'the hydrological cycle and the relief of the ocean floor', """
T: hydrological cycle | the continuous circulation of water in its various forms between the land, the oceans and the atmosphere
T: continental shelf | the extended margin of each continent occupied by relatively shallow seas and gulfs, the shallowest part of the ocean
T: continental slope | the steep slope connecting the continental shelf and the ocean basin, beginning where the shelf ends
T: deep sea plain | the gently sloping area of the ocean basin, the flattest and smoothest region of the world, at depths of 3,000 to 6,000 m
T: oceanic deep | the deepest part of the ocean, a relatively steep-sided narrow basin also called a trench
T: mid-oceanic ridge | a chain of mountains in the ocean with a rift valley along its axis, formed where plates move apart
T: seamount | a mountain with pointed summits rising from the sea floor that does not reach the surface of the ocean
T: guyot | a flat-topped seamount
T: submarine canyon | a deep valley cut across the continental shelf and slope, some comparable to the Grand Canyon
T: atoll | a low island in tropical oceans consisting of coral reefs surrounding a central lagoon
Q: About what proportion of the earth's surface is covered by water? | 71 per cent | 51 per cent | 29 per cent | 91 per cent
Q: The largest share of the earth's water is found in the: | oceans | ice caps and glaciers | groundwater | rivers and lakes
Q: The shallowest part of the ocean is the: | continental shelf | continental slope | deep sea plain | oceanic deep
Q: Flat-topped seamounts are called: | guyots | atolls | trenches | canyons
Q: The deepest parts of the oceans are the: | oceanic deeps or trenches | continental shelves | mid-oceanic ridges | guyots
Q: The largest continental shelf of the world is the: | Siberian shelf in the Arctic Ocean | shelf along the Chilean coast | shelf off Sumatra | shelf around Antarctica
Q: Oceanic trenches are most numerous in the: | Pacific Ocean | Atlantic Ocean | Indian Ocean | Arctic Ocean
M:ocean-relief: Continental shelf | shallow extended margin of a continent
M:ocean-relief: Continental slope | steep slope from the shelf break to the ocean basin
M:ocean-relief: Deep sea plain | flattest and smoothest part of the ocean floor
M:ocean-relief: Oceanic deep | deepest, narrow steep-sided basin
M:ocean-relief: Guyot | flat-topped seamount
M:ocean-relief: Atoll | coral reef ring around a central lagoon
P: Mariana Trench | the deepest known part of the oceans, in the western Pacific Ocean
P: Mid-Atlantic Ridge | a mid-oceanic ridge running north–south along the middle of the Atlantic Ocean
P: Emperor Seamount | a chain of seamounts in the Pacific Ocean
P: Siberian Shelf | the largest continental shelf of the world, in the Arctic Ocean
P: Red Sea | a sea with very high salinity because of high evaporation and little inflow of fresh water
P: Baltic Sea | a sea with low salinity because of a large inflow of river water
P: Dead Sea | a salt lake in West Asia with very high salinity because of high evaporation
P: Mediterranean Sea | a partly enclosed sea with higher salinity than the open Atlantic because of high evaporation
S+: About 71 per cent of the planet's surface is covered with water and about 29 per cent is land
S+: About 97 per cent of the earth's water is in the oceans and is too saline for human use
S+: The continental shelf is almost absent along some margins, such as the coast of Chile and the west coast of Sumatra
S+: The average width of continental shelves is about 80 km
S+: Continental shelves are covered with sediments brought by rivers, glaciers and wind, and are rich in fossil fuels
S+: Mid-oceanic ridges have a rift valley along their crest and are areas of intense volcanic activity
S-: The continental slope is the shallowest part of the ocean | The continental shelf is the shallowest part
S-: Most of the earth's water is in rivers and lakes | About 97 per cent is in the oceans
S-: Seamounts rise above the ocean surface | Seamounts do not reach the surface of the ocean
S-: Oceanic trenches are most numerous in the Atlantic Ocean | Most trenches are in the Pacific Ocean
C: Continental shelves are important for fishing and minerals | they are shallow, receive sunlight and are covered by sediments that form fossil fuels
C: Oceanic deeps are associated with earthquakes and volcanoes | they lie along plate boundaries where one plate sinks below another
C: Fresh water is scarce though the earth has plenty of water | about 97 per cent of the earth's water is in the saline oceans
C: Atolls are found in tropical oceans | corals grow only in warm, clear, shallow tropical waters
X: C2 D2 2 | What is a continental shelf? Why is it economically important? | Shallow extended margin of a continent; source of fish, oil, gas and minerals; sunlight supports marine life.
X: C3 D3 3 | Name and describe any three minor relief features of the ocean floor. | Mid-oceanic ridge – mountains with central rift; seamount – pointed summit not reaching surface; submarine canyon – deep valley across shelf and slope; guyot – flat-topped seamount; atoll – coral ring with lagoon.
L: D4 | Describe the major relief features of the ocean floor. | Continental shelf – shallow, average 80 km wide, absent off Chile, Siberian shelf largest; continental slope – steep; deep sea plain – flattest, 3,000–6,000 m; oceanic deeps – trenches, most in Pacific, Mariana; minor features – ridges, seamounts, guyots, canyons, atolls.
"""), ST(S + '11-st2', 'the temperature of ocean waters', """
T: thermocline | the layer below the warm surface layer of the ocean, about 500 to 1,000 m thick, in which temperature decreases rapidly with depth
T: surface layer of the ocean | the top layer of warm water, about 500 m thick, with temperatures of 20°C to 25°C in the tropics
T: deep layer of the ocean | the cold layer below the thermocline that extends to the ocean floor, with temperatures near 0°C
Q: The layer of ocean water in which temperature decreases rapidly with depth is the: | thermocline | halocline | surface layer | deep layer
Q: The average temperature of the surface water of the oceans is about: | 27°C | 7°C | 17°C | 37°C
Q: The highest temperature of the ocean surface is generally recorded: | slightly north of the equator | exactly at the poles | at 60° south | at 40° north
Q: Oceans in the northern hemisphere record relatively higher temperatures than in the southern hemisphere because they: | are in contact with larger land areas | have more icebergs | are deeper | receive less insolation
Q: Which of the following is NOT a factor affecting the temperature of ocean water? | Tides | Latitude | Ocean currents | Unequal distribution of land and water
S+: The temperature of surface water decreases from the equator towards the poles
S+: Prevailing winds blowing from land towards the oceans drive warm surface water away from the coast, and cold water rises from below
S+: Warm ocean currents raise the temperature in cold areas, and cold currents lower it in warm areas
S+: The temperature of ocean water decreases with depth
S+: Enclosed seas in the low latitudes record higher temperatures than the open oceans
S-: The temperature of ocean water increases with depth | It decreases with depth; below the thermocline it is near 0°C
S-: The highest ocean temperatures are found exactly at the equator | They are recorded slightly north of the equator
S-: The thermocline lies at the ocean floor | It lies just below the warm surface layer and is followed by the cold deep layer
C: Northern hemisphere oceans are warmer than southern hemisphere oceans | they are in contact with larger land areas
C: Upwelling of cold water occurs along some coasts | offshore winds drive warm surface water away and cold water rises from below
C: Enclosed seas in low latitudes are warmer than open oceans | they mix little with the colder open ocean water
X: C2 D2 2 | What is a thermocline? | The layer below the warm surface layer, about 500–1,000 m thick, in which ocean temperature falls rapidly with depth.
X: C3 D3 3 | Explain three factors that affect the temperature of ocean water. | Latitude – insolation decreases polewards; unequal land and water – northern oceans warmer; prevailing winds – offshore winds cause upwelling; ocean currents – warm and cold.
L: D4 | Describe the horizontal and vertical distribution of temperature in the oceans. | Factors – latitude, land and water, winds, currents; average surface 27°C, decreasing polewards; highest slightly north of equator; northern hemisphere warmer; vertical – surface layer (about 500 m, 20–25°C in tropics), thermocline (500–1,000 m thick, rapid fall in temperature), deep cold layer near 0°C.
"""), ST(S + '11-st3', 'the salinity of ocean waters', """
T: salinity | the total content of dissolved salts in sea water, expressed as parts per thousand (grams of salt per 1,000 g of sea water)
T: halocline | the zone in the ocean where salinity changes sharply with depth
T: brackish water | water with salinity less than that of sea water, found where fresh river water mixes with sea water
Q: The average salinity of ocean water is about: | 35 parts per thousand | 24.7 parts per thousand | 50 parts per thousand | 3.5 parts per thousand
Q: Salinity is expressed as: | parts per thousand | grams per cubic centimetre | parts per hundred only | millibars
Q: The zone where salinity increases sharply with depth is called the: | halocline | thermocline | pycnocline of temperature | tropopause
Q: Which of the following increases the salinity of the ocean? | High evaporation | Heavy rainfall | Inflow of rivers | Melting of ice
Q: Which of the following seas has higher salinity than the open ocean? | Mediterranean Sea | Baltic Sea | Black Sea | Sea of Okhotsk
Q: The Baltic Sea has low salinity because of: | large inflow of river water | high evaporation | its location in the tropics | volcanic activity
M:salinity-factor: High evaporation | increases salinity
M:salinity-factor: Inflow of river water | lowers salinity near coasts and estuaries
M:salinity-factor: Freezing of sea water | increases salinity of the remaining water
M:salinity-factor: Melting of ice | lowers salinity in polar regions
S+: Salinity is affected by evaporation, precipitation, fresh water from rivers, freezing and thawing of ice, winds and ocean currents
S+: Salinity is higher in the subtropics than at the equator because the equator receives heavy rainfall
S+: Salinity generally decreases towards the poles
S+: The Mediterranean Sea has higher salinity than the open Atlantic because of high evaporation
S+: Salinity changes with depth, and the change depends on the location of the sea
S+: Salinity is low in seas that receive large volumes of river water, such as the Baltic Sea
S-: The average salinity of ocean water is 3.5 parts per thousand | It is about 35 parts per thousand
S-: Salinity is highest at the equator | It is higher in the subtropics; heavy rain lowers it at the equator
S-: Inflow of river water increases salinity | River water dilutes sea water and lowers salinity
S-: Melting of ice increases salinity | Melting of ice lowers salinity; freezing increases it
C: Salinity is lower at the equator than in the subtropics | the equator receives heavy rainfall that dilutes the sea water
C: The Mediterranean Sea has high salinity | evaporation is high and it is partly enclosed
C: Salinity is low near river mouths | large amounts of fresh river water dilute the sea water
C: The Baltic Sea has low salinity | many rivers bring fresh water into it and evaporation is low
X: C2 D2 2 | Define salinity. What is the average salinity of the oceans? | Total content of dissolved salts in sea water in parts per thousand (‰); average about 35‰.
X: C3 D3 3 | Explain three factors that affect the salinity of ocean water. | Evaporation and precipitation; fresh water inflow from rivers; freezing and thawing of ice; winds and ocean currents.
L: D4 | Discuss the factors affecting salinity and its horizontal distribution. | Factors – evaporation and precipitation, river inflow, freezing and thawing, winds, currents; average 35‰; subtropics higher than equator; decreases polewards; enclosed seas – Mediterranean and Red Sea high, Baltic low; inland salt lakes such as the Dead Sea very high; halocline.
""")]

CH12 = [ST(S + '12-st1', 'waves and their characteristics', """
T: wave | the oscillating movement of the ocean surface in which energy, not water, moves forward
T: wave crest | the highest point of a wave
T: wave trough | the lowest point of a wave
T: wave height | the vertical distance from the bottom of a trough to the top of a crest
T: wave amplitude | one-half of the wave height
T: wave period | the time interval between two successive wave crests or troughs passing a fixed point
T: wavelength | the horizontal distance between two successive crests
T: wave frequency | the number of waves passing a given point during a one-second interval
Q: In a wave, what moves forward across the ocean? | Energy | Water | Salt | Sediment from the sea floor
Q: Most waves in the ocean are caused by: | wind | the moon | earthquakes only | ocean currents
Q: The vertical distance from the trough to the crest of a wave is the: | wave height | wavelength | wave period | wave amplitude
Q: One-half of the wave height is the: | wave amplitude | wave period | wavelength | wave frequency
Q: The horizontal distance between two successive crests is the: | wavelength | wave height | wave amplitude | wave speed
Q: The number of waves passing a point in one second is the: | wave frequency | wave period | wavelength | wave speed
M:wave-part: Wave crest | highest point of a wave
M:wave-part: Wave trough | lowest point of a wave
M:wave-part: Wave height | vertical distance from trough to crest
M:wave-part: Wavelength | horizontal distance between successive crests
M:wave-part: Wave period | time between two successive crests passing a point
S+: Waves are energy that moves across the ocean surface while water particles move in small circles
S+: Wind provides energy to the waves
S+: The largest waves are found in the open oceans
S+: A wave breaks when the depth of water becomes less than about half the wavelength of the wave
S+: Waves continue to grow larger as they move and absorb energy from the wind
S-: In a wave, water moves forward across the ocean | Energy moves forward; water particles only move in small circles
S-: The wave period is the distance between two crests | The wave period is the time between two crests; wavelength is the distance
S-: The largest waves are found in shallow coastal waters | The largest waves are found in the open oceans
C: Waves break near the shore | the depth of water becomes less than half the wavelength, so the wave front slows down and topples over
C: The largest waves are found in the open ocean | waves grow as they travel long distances absorbing energy from the wind
C: A floating object rises and falls but does not move far with a wave | water particles move in small circles while the energy moves forward
X: C2 D2 2 | Distinguish between wave height and wave amplitude. | Wave height – vertical distance from trough to crest; amplitude – one-half of the wave height.
X: C3 D3 3 | Explain how waves are formed and why they break near the coast. | Wind transfers energy to the water surface; energy moves while water particles move in circles; near the coast, depth less than half the wavelength slows the base and the wave breaks.
"""), ST(S + '12-st2', 'tides: spring and neap tides and their importance', """
T: tide | the periodic rise and fall of the sea level, once or twice a day, caused mainly by the attraction of the sun and the moon
T: spring tide | a tide higher than normal that occurs when the sun, the moon and the earth are in a straight line, at full moon and new moon
T: neap tide | a tide lower than normal that occurs when the sun and the moon are at right angles to each other
T: semi-diurnal tide | the most common tidal pattern, with two high tides and two low tides each day
T: diurnal tide | a tidal pattern with only one high tide and one low tide each day
T: mixed tide | a tidal pattern with variations in heights of successive high and low tides
T: perigee | the position of the moon closest to the earth in its orbit, when tides are unusually high
Q: The highest tides in the world occur in the: | Bay of Fundy | Gulf of Mexico | Bay of Bengal | Red Sea
Q: Spring tides occur when: | the sun, the moon and the earth are in a straight line | the sun and the moon are at right angles | the moon is at apogee | the earth is at aphelion
Q: Neap tides normally occur about seven days after: | spring tides | perigee | a tsunami | an equinox
Q: Tides with two high and two low waters each day are: | semi-diurnal tides | diurnal tides | mixed tides | neap tides only
Q: The movement of water caused by meteorological effects such as winds and atmospheric pressure is called: | a surge | a tide | a current | a spring tide
Q: Tides are caused mainly by the gravitational pull of the: | moon and the sun | moon and Mars | earth's core | winds
M:tide-type: Spring tide | sun, moon and earth in a straight line
M:tide-type: Neap tide | sun and moon at right angles to each other
M:tide-type: Semi-diurnal tide | two high and two low tides each day
M:tide-type: Diurnal tide | one high and one low tide each day
M:tide-type: Mixed tide | successive high and low tides of different heights
S+: The moon's gravitational pull and, to a lesser extent, the sun's pull are the major causes of tides
S+: Tidal bulges on the side facing the moon and the opposite side cause high tides
S+: The tidal range of the Bay of Fundy in Canada is about 15–16 m
S+: Tides help in navigation by raising the water level, allowing ships to enter harbours
S+: Tides help in desilting sediments and removing polluted water from river estuaries
S+: Tides are used to generate electricity in some places
S-: Neap tides occur at full moon and new moon | Spring tides occur at full moon and new moon; neap tides occur when the sun and moon are at right angles
S-: Tides are caused mainly by winds | Tides are caused mainly by the gravitational pull of the moon and sun; wind effects cause surges
S-: The moon's pull on tides is weaker than the sun's | The moon's pull is stronger because it is much closer to the earth
C: Spring tides are higher than normal | the gravitational pulls of the sun and the moon act together when they are in line with the earth
C: Neap tides are lower than normal | the pulls of the sun and the moon act at right angles and partly counteract each other
C: The moon has a greater effect on tides than the sun | the moon is much closer to the earth even though the sun is much larger
C: Tides are important for navigation | high tides raise the water level so that ships can enter harbours and estuaries
X: C2 D2 2 | Distinguish between spring tides and neap tides. | Spring – sun, moon and earth in line (full and new moon), higher than normal; neap – sun and moon at right angles, lower than normal, about seven days later.
X: C3 D3 3 | State three uses of tides. | Navigation – ships enter harbours at high tide; fishing; desilting of estuaries and removal of polluted water; generation of tidal power.
L: D4 | What are tides? Explain their causes, types and importance. | Periodic rise and fall of sea level; gravitational pull of moon and sun, centrifugal force; tidal bulges; types by frequency – semi-diurnal, diurnal, mixed; by sun-moon-earth positions – spring and neap; perigee and perihelion; Bay of Fundy; importance – navigation, fishing, desilting, tidal energy.
"""), ST(S + '12-st3', 'ocean currents: forces, types and effects', """
T: ocean current | a river-like flow of water in a definite path and direction in the oceans
T: warm current | an ocean current that flows from low latitudes towards higher latitudes and raises the temperature of the areas it reaches
T: cold current | an ocean current that carries cold water from higher latitudes into lower latitudes
T: gyre | a large circular loop of ocean currents in the major ocean basins
T: upwelling | the rising of cold, nutrient-rich water from depth to the surface
Q: Which of the following is a cold current? | Labrador Current | Gulf Stream | Kuroshio Current | Brazil Current
Q: Which of the following is a warm current? | Gulf Stream | Canaries Current | Benguela Current | Peru Current
Q: Cold currents are usually found on the: | west coasts of continents in low and middle latitudes | east coasts of continents in low latitudes | equatorial regions only | inland seas
Q: The Grand Banks near Newfoundland are rich fishing grounds because: | warm and cold currents meet there | the water is very deep | there are no currents | the sea is frozen all year
Q: The Atacama Desert lies near the cold: | Peru (Humboldt) Current | Benguela Current | Canaries Current | California Current
Q: The primary force that drives ocean currents at the surface is: | wind | the moon | earthquakes | the tides
P: Gulf Stream | a warm current flowing along the east coast of North America into the North Atlantic
P: Labrador Current | a cold current flowing south along the north-east coast of North America
P: Canaries Current | a cold current flowing south along the north-west coast of Africa
P: Peru Current | a cold current flowing north along the west coast of South America, also called the Humboldt Current
P: Benguela Current | a cold current along the south-west coast of Africa
P: Kuroshio Current | a warm current flowing north-east off the east coast of Japan
P: Grand Banks | rich fishing grounds off Newfoundland where the Gulf Stream and the Labrador Current meet
P: Bay of Fundy | a bay in Canada that has the highest tides in the world
M:current-ocean: Gulf Stream | North Atlantic, off the east coast of the USA
M:current-ocean: Kuroshio Current | North Pacific, off the east coast of Japan
M:current-ocean: Benguela Current | South Atlantic, off south-west Africa
M:current-ocean: Peru Current | South Pacific, off western South America
M:current-ocean: West Australian Current | Indian Ocean, off western Australia
S+: Ocean currents are influenced by heating by solar energy, wind, gravity and the Coriolis force
S+: Cold currents generally flow on the west coasts of continents in the low and middle latitudes
S+: Warm currents generally flow on the east coasts of continents in the low and middle latitudes
S+: In the northern hemisphere, warm currents are found on the west coasts of continents in higher latitudes
S+: Mixing of warm and cold currents produces some of the richest fishing grounds of the world
S+: Cold currents along west coasts contribute to the formation of deserts such as the Atacama and the Namib
S-: The Labrador Current is a warm current | The Labrador Current is a cold current; the Gulf Stream is warm
S-: Cold currents are usually found on the east coasts of continents in low latitudes | They are found on the west coasts in low and middle latitudes
S-: The Kuroshio is a cold current of the Atlantic Ocean | The Kuroshio is a warm current of the North Pacific off Japan
S-: Ocean currents have no effect on climate | They affect temperature, rainfall, fog and fishing of coastal areas
C: The Grand Banks are rich fishing grounds | the warm Gulf Stream and the cold Labrador Current meet there, supporting plankton growth
C: The west coasts of continents in the subtropics have deserts | cold currents cool the air above, reducing evaporation and rainfall
C: Fog is common where warm and cold currents meet | warm moist air is cooled to its dew point over cold water
C: North-western Europe has mild winters | the warm North Atlantic Drift raises the temperature of its coasts
X: C2 D2 2 | Name two warm and two cold ocean currents. | Warm – Gulf Stream, Kuroshio, Brazil, North Atlantic Drift, Agulhas; cold – Labrador, Canaries, Peru (Humboldt), Benguela, California, Oyashio.
X: C3 D3 3 | Explain three effects of ocean currents on the climate of coastal areas. | Warm currents raise temperature (mild winters in NW Europe); cold currents lower temperature and cause aridity (Atacama, Namib); meeting of warm and cold currents gives fog and rich fishing (Grand Banks).
L: D4 | Explain the forces that cause ocean currents and describe their types and effects. | Forces – solar heating, wind, gravity, Coriolis force; types – surface and deep, warm and cold; west coasts cold in low and middle latitudes, east coasts warm; gyres; effects – temperature, desert formation, fog, fishing grounds, navigation; examples – Gulf Stream, Labrador, Kuroshio, Peru, Benguela.
""")]

CHAPTERS = [
    (CH07, {'chapter_topic': 'the composition and structure of the atmosphere'}),
    (CH08, {'chapter_topic': 'solar radiation, heat balance and temperature'}),
    (CH09, {'chapter_topic': 'atmospheric circulation and weather systems'}),
    (CH10, {'chapter_topic': 'water in the atmosphere'}),
    (CH11, {'chapter_topic': 'the oceans', 'map_name': WORLD}),
    (CH12, {'chapter_topic': 'movements of ocean water', 'map_name': WORLD}),
]
