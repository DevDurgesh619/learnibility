"""CBSE class 11 Geography, Practical Work in Geography Part I (chapters 18-23): fact tables for g12_hum_engine.

Computed items (scale conversion, local time, projection construction, gradient, pixels) are in g11_geography_num.py.
"""
from g12_hum_engine import ST

S = 'cbse-g11-geography-ch'

CH18 = [ST(S + '18-st1', 'the essentials of maps and the difference between maps and sketches', """
T: map | a selective, symbolised and generalised representation of the whole or a part of the earth's surface on a plane surface at a reduced scale
T: sketch | a simple drawing made from memory or spot observation without a scale or projection
T: cartography | the art, science and technology of making maps
T: scale | the ratio between the distance on a map and the corresponding distance on the ground
T: map projection | the method of transforming the spherical surface of the earth onto a plane surface
T: generalisation | the selection and simplification of information to be shown on a map according to its purpose and scale
T: symbolisation | the use of conventional signs and symbols to show features on a map
T: orientation | the indication of the north direction on a map
Q: A drawing made without scale and projection is a: | sketch | map | plan | globe
Q: The art, science and technology of making maps is called: | cartography | photogrammetry | topography | geodesy
Q: The method of transforming the spherical surface of the earth onto a plane surface is called: | map projection | map scale | generalisation | orientation
Q: The selection and simplification of features to be shown on a map is called: | generalisation | symbolisation | projection | orientation
Q: Which of the following is NOT an essential of a map? | Aerial photograph of the area | Scale | Projection | Symbols
M:map-essential: Scale | ratio of map distance to ground distance
M:map-essential: Projection | transformation of the globe onto a plane
M:map-essential: Generalisation | selection and simplification of details
M:map-essential: Symbolisation | use of conventional signs
M:map-essential: Orientation | showing the north direction
S+: Every map is a reduced representation of the earth's surface
S+: A map must have a title, a scale, a north direction and a legend of symbols
S+: Maps are drawn according to a projection, while sketches are not
S+: The process of map making includes generalisation, map design, construction and production
S+: Conventional signs are understood by map users all over the world
S-: A sketch is drawn to scale | A sketch is drawn without scale; a map is drawn to scale
S-: A map shows every feature of the earth's surface | A map is selective and generalised according to its purpose and scale
S-: Map projection is the ratio between map and ground distance | That is the scale; projection transforms the globe onto a plane
C: Every map is a generalised representation | it is drawn at a reduced scale, and only features relevant to its purpose can be shown
C: Conventional signs are used on maps | they save space and make maps easy to read for users everywhere
C: A map needs a projection | the earth is spherical and its surface cannot be shown on a flat sheet without transformation
X: C2 D2 2 | Distinguish between a map and a sketch. | Map – drawn to scale and projection, accurate, symbolised; sketch – drawn from memory or observation without scale or projection.
X: C3 D3 3 | Name and explain any three essentials of a map. | Scale – ratio of map to ground distance; projection – globe onto plane; generalisation – selection by purpose; symbolisation – conventional signs; orientation – north direction.
L: D4 | What is a map? Explain the essentials of map making. | Selective, symbolised, generalised representation at reduced scale; scale; projection; generalisation; map design (symbols, lettering, layout); construction and production; title, legend, north arrow; map vs sketch.
"""), ST(S + '18-st2', 'the history of map making and types of maps', """
T: cadastral map | a very large-scale map showing the ownership of land and property boundaries, such as village and city plans
T: topographical map | a large-scale map prepared from precise surveys, showing relief, drainage, vegetation, settlements and transport
T: wall map | a map on large sheets, smaller in scale than topographical maps, used in classrooms
T: atlas map | a very small-scale map giving a generalised picture of physical, climatic and economic features of large areas
T: physical map | a map showing natural features such as relief, geology, soils, climate and vegetation
T: cultural map | a map showing man-made features such as political divisions, population, economy and transport
T: thematic map | a map that shows a particular theme or distribution
Q: Maps showing the ownership of land and property boundaries are: | cadastral maps | atlas maps | wall maps | physical maps
Q: Topographical maps in India are prepared by the: | Survey of India | Indian Meteorological Department | Geological Survey of India | Census of India
Q: The Survey of India was established in: | 1767 | 1857 | 1947 | 1905
Q: The oldest known map, drawn on a clay tablet, was found in: | Mesopotamia | China | India | Egypt
Q: Which of the following is a small-scale map? | Atlas map | Cadastral map | Topographical map | City plan
Q: Maps showing political divisions, population and economic activities are: | cultural maps | physical maps | relief maps | geological maps
Q: Large-scale maps include: | cadastral and topographical maps | atlas and wall maps | wall and globe maps | only atlas maps
Y: 1767 | Survey of India established
M:map-type: Cadastral map | land ownership and property boundaries
M:map-type: Topographical map | relief, drainage and settlements from precise surveys
M:map-type: Wall map | large sheets used in classrooms
M:map-type: Atlas map | very small-scale generalised maps of large areas
S+: Maps are classified on the basis of scale and function
S+: Large-scale maps include cadastral maps and topographical maps; small-scale maps include wall maps and atlas maps
S+: The Survey of India prepares topographical maps at scales such as 1:250,000, 1:50,000 and 1:25,000
S+: Ptolemy prepared a map of the world in ancient Greece
S+: Physical maps include relief, geological, climatic, soil and vegetation maps
S-: Atlas maps are large-scale maps | Atlas maps are small-scale maps; cadastral and topographical maps are large-scale
S-: Cadastral maps show the climate of a region | Cadastral maps show the ownership of land and property boundaries
S-: Topographical maps in India are prepared by the Census of India | They are prepared by the Survey of India
C: Cadastral maps are drawn on a very large scale | they must show the boundaries of individual fields and properties precisely
C: Atlas maps show only generalised information | they are drawn on a very small scale covering large areas
C: Topographical maps are useful for planning | they show relief, drainage, land use, settlements and transport accurately
X: C2 D2 2 | Distinguish between large-scale and small-scale maps. | Large-scale – small area in great detail (cadastral, topographical); small-scale – large area with less detail (wall, atlas maps).
X: C3 D3 3 | Classify maps on the basis of function, with examples. | Physical maps – relief, geological, climatic, soil, vegetation; cultural maps – political, population, economic, transportation.
L: D4 | Classify maps on the basis of scale and explain each type. | Large-scale – cadastral (land ownership, village and city plans), topographical (Survey of India, precise surveys); small-scale – wall maps (classrooms), atlas maps (very small scale, generalised); history – Mesopotamian clay tablet, Ptolemy, Survey of India 1767.
"""), ST(S + '18-st3', 'the uses of maps and drawing instruments', """
T: divider | an instrument with two pointed legs used to measure distances on maps
T: opisometer | a small instrument with a wheel used to measure curved distances such as roads and rivers on maps
T: protractor | an instrument used to measure and draw angles and directions
T: set square | a triangular instrument used to draw parallel and perpendicular lines
T: compass | an instrument used to draw circles and arcs
T: bearing | the direction of a point measured clockwise in degrees from north
Q: Curved distances such as roads and rivers on a map are best measured with a/an: | opisometer | protractor | set square | prismatic compass
Q: Directions on a map are measured as bearings: | clockwise from north | anticlockwise from south | clockwise from east | from the equator
Q: The bearing of a point due east is: | 90° | 180° | 270° | 0°
Q: Which instrument is used to measure angles on a map? | Protractor | Divider | Opisometer | Ruler only
Q: The bearing of a point due south is: | 180° | 90° | 270° | 360°
M:instrument-use: Divider | measuring straight distances on a map
M:instrument-use: Opisometer | measuring curved distances along roads and rivers
M:instrument-use: Protractor | measuring angles and bearings
M:instrument-use: Set square | drawing parallel and perpendicular lines
M:instrument-use: Compass | drawing circles and arcs
S+: Maps are used to measure distance, direction and area
S+: Straight distances can be measured with a ruler or divider and converted using the scale
S+: The area of a region on a map can be estimated by the square method
S+: The north line on a map is the basis for measuring directions
S+: Maps help in planning, navigation, defence, administration and study of distributions
S-: Bearings are measured anticlockwise from south | Bearings are measured clockwise from north
S-: A protractor is used to measure curved distances | An opisometer measures curved distances; a protractor measures angles
S-: Maps cannot be used to measure area | Area can be measured by methods such as the square method
C: An opisometer is used to measure the length of a river on a map | the river's course is curved and cannot be measured accurately with a ruler
C: Directions on maps are expressed as bearings | measuring clockwise from north gives a precise and universal way of stating direction
C: Map users must know the scale | distances measured on the map can be converted to ground distances only with the scale
X: C2 D2 2 | Name two instruments used to measure distances on a map and state their use. | Divider – straight distances; opisometer – curved distances such as rivers and roads; ruler – straight lines.
X: C3 D3 3 | Explain how distance, direction and area are measured on a map. | Distance – ruler, divider, opisometer with scale; direction – bearings clockwise from north with a protractor; area – square method or polar planimeter.
""")]

CH19 = [ST(S + '19-st1', 'methods of expressing scale', """
T: statement of scale | a scale expressed in words, such as 1 cm represents 10 km
T: representative fraction | a scale expressed as a fraction or ratio, such as 1:100,000, in which map and ground distances are in the same unit
T: graphical scale | a scale shown by a line divided into primary and secondary divisions, also called a linear or bar scale
T: metric system | the system of measurement using kilometres, metres and centimetres
T: English system | the system of measurement using miles, furlongs, yards, feet and inches
Q: A scale written as 1:50,000 is a: | representative fraction | statement of scale | graphical scale | bar scale only
Q: Which method of expressing scale has no units and can be used universally? | Representative fraction | Statement of scale | Graphical scale | Verbal scale
Q: Which scale remains correct when a map is enlarged or reduced? | Graphical scale | Representative fraction | Statement of scale | Verbal statement in miles
Q: A scale written as '1 cm represents 5 km' is a: | statement of scale | representative fraction | graphical scale | linear scale only
Q: In the English system, 1 mile equals: | 63,360 inches | 100,000 inches | 1,000 yards | 5,280 inches
Q: In the metric system, 1 km equals: | 100,000 cm | 10,000 cm | 1,000 cm | 1,000,000 cm
M:scale-method: Statement of scale | scale expressed in words
M:scale-method: Representative fraction | scale expressed as a ratio without units
M:scale-method: Graphical scale | scale shown by a divided line
S+: The representative fraction expresses map and ground distances in the same unit
S+: A statement of scale can be understood only by those who know the unit used
S+: The graphical scale is drawn as a line divided into primary and secondary divisions
S+: 1 km = 1,000 m = 100,000 cm
S+: 1 mile = 8 furlongs = 1,760 yards = 63,360 inches
S-: A representative fraction has units | It has no units; the same unit applies to both map and ground distances
S-: A statement of scale remains correct when the map is enlarged | A graphical scale remains correct; a statement of scale does not
S-: 1 km equals 10,000 cm | 1 km equals 100,000 cm
C: The representative fraction is a universal method of scale | it has no units and can be converted into any system of measurement
C: The graphical scale remains valid when a map is reduced or enlarged | the line scale changes size along with the map
C: A statement of scale may not be understood everywhere | it uses units such as miles or kilometres that may not be familiar to all users
X: C2 D2 2 | State one merit and one limitation of the statement of scale. | Merit – simple and easy to understand; limitation – depends on the unit, not universal, and becomes wrong if the map is enlarged or reduced.
X: C3 D3 3 | Explain the three methods of expressing scale. | Statement – in words (1 cm represents 10 km); representative fraction – ratio without units (1:100,000); graphical – divided line, valid on enlargement and reduction.
"""), ST(S + '19-st2', 'conversion of scales between statement and representative fraction', """
T: conversion of scale | changing a scale from one method of expression to another, such as statement to representative fraction
Q: To convert a statement of scale into a representative fraction, the ground distance must be: | converted into the same unit as the map distance | divided by 10 | written in miles | left unchanged
Q: The RF of the statement '1 cm represents 1 km' is: | 1:100,000 | 1:1,000 | 1:10,000 | 1:1,000,000
Q: The RF of the statement '1 inch represents 1 mile' is: | 1:63,360 | 1:100,000 | 1:1,760 | 1:5,280
Q: Which of the following is the largest scale? | 1:10,000 | 1:50,000 | 1:250,000 | 1:1,000,000
Q: Which of the following is the smallest scale? | 1:1,000,000 | 1:250,000 | 1:50,000 | 1:25,000
S+: A large-scale map has a smaller denominator in its representative fraction
S+: To find the RF, map distance and ground distance must be in the same unit
S+: An RF of 1:63,360 means 1 inch represents 1 mile
S+: An RF of 1:100,000 means 1 cm represents 1 km
S-: A scale of 1:1,000,000 is larger than 1:50,000 | 1:50,000 is the larger scale because its denominator is smaller
S-: An RF of 1:100,000 means 1 cm represents 100 km | It means 1 cm represents 1 km
S-: An RF of 1:63,360 means 1 cm represents 1 km | It means 1 inch represents 1 mile
C: A map with RF 1:10,000 shows more detail than one with 1:1,000,000 | a larger scale gives more space to show each feature
C: Units must be the same when finding an RF | a representative fraction is a pure ratio and has no units
X: C2 D2 2 | Why is 1:50,000 called a larger scale than 1:250,000? | The denominator is smaller, so a given ground distance appears longer on the map and more detail can be shown.
"""), ST(S + '19-st3', 'construction of a graphical (linear) scale', """
T: primary division | the main division of a graphical scale, marked with round values such as 1 km or 5 km
T: secondary division | the subdivision of the first primary division of a graphical scale for reading smaller distances
Q: The length of a graphical scale is usually chosen to be about: | 12 to 15 cm | 1 to 2 cm | 50 cm | 100 cm
Q: In a graphical scale, the first primary division is subdivided into: | secondary divisions | contours | grids | parallels
Q: In a graphical scale, zero is placed: | after the first primary division from the left | at the extreme right end | at the extreme left end always | in the middle of the line
S+: A graphical scale is constructed with round numbers of the ground distance
S+: In a graphical scale, the secondary divisions are marked to the left of zero
S+: A graphical scale is usually drawn about 12 to 15 cm long
S+: The length of the line is calculated from the RF for a convenient round ground distance
S-: Secondary divisions are marked to the right of zero | They are marked to the left of zero, in the first primary division
S-: A graphical scale is drawn using odd values such as 7.3 km per division | Round values such as 1, 2, 5 or 10 km are used for primary divisions
C: Round values are used in a graphical scale | they make it easy to read distances directly from the scale
C: The first primary division is subdivided | it allows smaller distances to be measured accurately
X: C2 D2 2 | Why is the first primary division of a graphical scale subdivided? | To measure distances smaller than one primary division accurately; secondary divisions are placed to the left of zero.
""")]

CH20 = [ST(S + '20-st1', 'parallels of latitude and meridians of longitude', """
T: latitude | the angular distance of a place north or south of the equator, measured in degrees
T: longitude | the angular distance of a place east or west of the Prime Meridian, measured in degrees
T: parallel of latitude | a circle joining places of the same latitude, parallel to the equator
T: meridian of longitude | a semi-circle joining the poles that connects places of the same longitude
T: Prime Meridian | the meridian of 0° longitude that passes through Greenwich near London
T: graticule | the network of parallels and meridians drawn on a globe or map
T: equator | the parallel of 0° latitude, the largest circle dividing the earth into the northern and southern hemispheres
Q: The parallel of 0° latitude is the: | equator | Prime Meridian | Tropic of Cancer | International Date Line
Q: The Prime Meridian passes through: | Greenwich | Paris | New Delhi | Washington
Q: The network of parallels and meridians is called: | graticule | grid reference | contour | projection
Q: The latitude of the Arctic Circle is: | 66½° N | 23½° N | 90° N | 45° N
Q: All meridians: | are of equal length and meet at the poles | are of different lengths | are parallel to the equator | are full circles of different sizes
Q: The length of a degree of longitude is greatest at the: | equator | poles | tropics | Arctic Circle
M:parallel-value: Equator | 0° latitude
M:parallel-value: Tropic of Cancer | 23½° N
M:parallel-value: Tropic of Capricorn | 23½° S
M:parallel-value: Arctic Circle | 66½° N
M:parallel-value: Antarctic Circle | 66½° S
S+: Parallels of latitude decrease in size from the equator towards the poles
S+: The poles are points, at 90° north and 90° south
S+: All meridians are semi-circles of equal length meeting at the poles
S+: There are 360 meridians at an interval of 1°, 180 to the east and 180 to the west of the Prime Meridian
S+: The distance between two meridians decreases from the equator towards the poles
S+: The latitude and longitude of a place together give its exact location
S-: All parallels are of equal length | Parallels decrease in size from the equator to the poles; meridians are equal
S-: The equator passes through Greenwich | The Prime Meridian passes through Greenwich; the equator is 0° latitude
S-: The distance between meridians is the same everywhere | It is greatest at the equator and decreases to zero at the poles
C: The distance covered by one degree of longitude decreases towards the poles | all meridians converge and meet at the poles
C: Latitude and longitude are both needed to locate a place | latitude alone gives only a parallel and longitude alone gives only a meridian
C: The equator is the largest parallel | it lies midway between the poles where the earth is widest
X: C2 D2 2 | Distinguish between parallels of latitude and meridians of longitude. | Parallels – circles parallel to equator, decrease in size polewards, measure N–S; meridians – equal semi-circles joining poles, measure E–W, converge at poles.
X: C3 D3 3 | State three characteristics of meridians of longitude. | Semi-circles from pole to pole; all equal in length; converge at poles; 360 meridians; spacing decreases polewards; used for time.
"""), ST(S + '20-st2', 'longitude and time: calculating local time', """
T: local time | the time of a place determined by the position of the sun, when the sun is overhead at noon on its meridian
T: Greenwich Mean Time | the local time of the Prime Meridian (0°) at Greenwich, used as the world reference time
Q: The earth rotates through 1° of longitude in: | 4 minutes | 1 minute | 15 minutes | 1 hour
Q: The earth rotates through 15° of longitude in: | 1 hour | 4 minutes | 30 minutes | 2 hours
Q: As we move east from the Prime Meridian, local time: | increases (is ahead) | decreases (is behind) | stays the same | becomes GMT
Q: Places to the west of Greenwich have local time: | behind GMT | ahead of GMT | the same as GMT | a day ahead of GMT
Q: The earth completes one rotation of 360° in about: | 24 hours | 12 hours | 365 days | 1 hour
S+: The earth rotates from west to east, through 360° in 24 hours
S+: A difference of 1° of longitude gives a difference of 4 minutes in local time
S+: Places east of a meridian are ahead in time, and places west are behind
S+: Local time is based on the time when the sun is highest in the sky at a place
S-: Places to the west of Greenwich are ahead of GMT | They are behind GMT; places to the east are ahead
S-: The earth rotates through 1° in 15 minutes | It rotates through 1° in 4 minutes and 15° in one hour
S-: The earth rotates from east to west | It rotates from west to east
C: Places to the east of Greenwich are ahead of GMT | the earth rotates from west to east, so the sun rises earlier there
C: There is a four-minute difference in local time for every degree of longitude | the earth turns through 360° in 24 hours, that is 1° every 4 minutes
X: C2 D2 2 | Why do places east of Greenwich have time ahead of GMT? | The earth rotates from west to east, so places to the east see the sun earlier; 1° = 4 minutes.
"""), ST(S + '20-st3', 'standard time, time zones and the International Date Line', """
T: standard time | the local time of a central meridian adopted for the whole of a country or time zone
T: time zone | a region of the earth that observes the same standard time, generally 15° of longitude wide
T: International Date Line | the line roughly along 180° longitude, where the date changes by one day on crossing it
Q: The world is divided into how many time zones of one hour each? | 24 | 12 | 36 | 15
Q: The International Date Line roughly follows the: | 180° meridian | 0° meridian | equator | 82°30' E meridian
Q: A traveller crossing the International Date Line from east to west: | gains a day | loses an hour | repeats the same day | loses a week
Q: The International Date Line is zigzag because it: | avoids land areas and island groups | follows the equator | follows ocean currents | follows the Prime Meridian
Q: The Indian Standard Time is based on the meridian of: | 82°30' E | 0° | 180° | 75° E
S+: Standard time avoids the confusion of different local times within a country
S+: Some large countries with a wide east-west extent have more than one time zone
S+: The time at 180° east and 180° west is the same, but the date differs by a day
S+: The International Date Line deviates from the 180° meridian to avoid dividing land areas
S+: Indian Standard Time is 5 hours 30 minutes ahead of Greenwich Mean Time
S-: Crossing the Date Line from east to west, a traveller repeats a day | He gains a day (the date advances); crossing west to east, he repeats a day
S-: The International Date Line follows the 0° meridian | It roughly follows the 180° meridian
S-: Every country uses its own local time for each city | Countries adopt standard time based on a central meridian
C: Countries adopt a standard time | local times differ from place to place, and a single time avoids confusion in railways, offices and communication
C: The International Date Line is not a straight line | it bends to avoid dividing countries and island groups into two dates
C: Some countries have several time zones | they have a large east-west extent, so one standard time would differ too much from local times
X: C2 D2 2 | What is the International Date Line? Why is it zigzag? | The line roughly along 180° where the date changes by a day; it bends to avoid land areas and island groups.
X: C3 D3 3 | Distinguish between local time and standard time and explain why India has adopted a standard meridian. | Local time – by sun at each meridian; standard time – of a central meridian for a country; India's extent of about 30° gives two hours difference, so 82°30' E (IST = GMT + 5:30) is used.
""")]

CH21 = [ST(S + '21-st1', 'the meaning, need and elements of map projection', """
T: reduced earth | a model of the earth (globe) reduced to the required scale, from which a projection is drawn
T: global property | a property of the globe such as correct area, shape, direction or distance that a projection tries to preserve
T: developable surface | a surface such as a cylinder, cone or plane that can be flattened without stretching or tearing
T: non-developable surface | a surface such as a sphere that cannot be flattened without shrinking, breaking or creasing
Q: A surface that can be flattened without stretching or tearing is a: | developable surface | non-developable surface | sphere | spheroid
Q: Which of the following is a non-developable surface? | Sphere | Cylinder | Cone | Plane
Q: Which of the following is NOT an element of map projection? | Contour interval | Reduced earth | Parallels and meridians | Global property
Q: No map projection can preserve: | all global properties at once | the north direction | the scale along any line | the names of places
Q: A globe is not always convenient because it: | cannot show large-scale detail and is difficult to carry | shows wrong shapes | has no scale | cannot show oceans
S+: A globe is the best model of the earth, but it is not convenient for detailed study
S+: Map projection is needed because the spherical surface of the earth cannot be flattened without distortion
S+: The elements of map projection are the reduced earth, parallels of latitude, meridians of longitude and global property
S+: The cylinder, cone and plane are developable surfaces
S+: No projection can preserve correct area, shape, direction and distance all at the same time
S-: A sphere is a developable surface | A sphere is non-developable; cylinders, cones and planes are developable
S-: A single projection can preserve all global properties | No projection preserves all of them together
S-: A globe is convenient for showing large-scale detail | A globe cannot show detailed large-scale information and is difficult to carry
C: Map projections are needed | the globe cannot show detail conveniently and the spherical surface cannot be flattened without distortion
C: Every map projection has some distortion | a non-developable spherical surface cannot be transferred onto a plane without stretching or shrinking
X: C2 D2 2 | Distinguish between developable and non-developable surfaces. | Developable – can be flattened without stretching or tearing (cylinder, cone, plane); non-developable – cannot be flattened without distortion (sphere).
X: C3 D3 3 | Why are map projections needed? Name the elements of map projection. | Globe inconvenient for detail and to carry; sphere cannot be flattened; elements – reduced earth, parallels, meridians, global property.
"""), ST(S + '21-st2', 'the classification of map projections', """
T: cylindrical projection | a projection obtained by wrapping a cylinder round the globe
T: conical projection | a projection obtained by placing a cone over the globe touching it along a standard parallel
T: zenithal projection | a projection in which a plane touches the globe at a point, such as a pole
T: homolographic projection | an equal-area projection in which areas are correctly represented
T: orthomorphic projection | a projection in which shapes are correctly represented for small areas
T: azimuthal projection | a projection in which directions from the centre are correctly shown
T: gnomonic projection | a projection drawn by placing the source of light at the centre of the globe
T: stereographic projection | a projection drawn by placing the source of light at the periphery of the globe, opposite the point of contact
T: orthographic projection | a projection drawn by placing the source of light at an infinite distance from the globe
Q: A projection in which areas are correctly represented is called: | homolographic | orthomorphic | azimuthal | gnomonic
Q: A projection with the source of light at the centre of the globe is: | gnomonic | stereographic | orthographic | cylindrical
Q: A projection with the source of light at an infinite distance from the globe is: | orthographic | gnomonic | stereographic | conical
Q: A projection that shows correct shapes is: | orthomorphic | homolographic | equidistant | gnomonic
Q: On the basis of the developable surface, projections are classified as: | cylindrical, conical and zenithal | perspective and non-perspective | gnomonic and stereographic | equal area and orthomorphic
M:light-source: Gnomonic | light at the centre of the globe
M:light-source: Stereographic | light at the opposite end of the globe from the point of contact
M:light-source: Orthographic | light at an infinite distance
M:global-property-name: Homolographic | correct area
M:global-property-name: Orthomorphic | correct shape
M:global-property-name: Azimuthal | correct direction
M:global-property-name: Equidistant | correct distance
S+: Projections are classified by drawing technique, developable surface, global property and source of light
S+: By drawing technique, projections are perspective, non-perspective or conventional (mathematical)
S+: By global property, projections are equal area (homolographic), orthomorphic, azimuthal or equidistant
S+: Zenithal projections may be polar, equatorial or oblique depending on where the plane touches the globe
S-: A gnomonic projection has the light source at an infinite distance | It has the light at the centre of the globe; orthographic has it at infinity
S-: An orthomorphic projection preserves correct area | It preserves correct shape; homolographic preserves area
S-: Conical projections are drawn on a plane touching the globe at a point | That is a zenithal projection; conical projections use a cone
C: Projections are classified by source of light | the position of light (centre, opposite end or infinity) changes the way the graticule is projected
C: Different projections are chosen for different purposes | each projection preserves only some global properties
X: C2 D2 2 | Classify projections on the basis of the source of light. | Gnomonic – light at centre; stereographic – at the opposite end of the globe; orthographic – at infinite distance.
X: C3 D3 3 | Classify map projections on the basis of global properties. | Equal area (homolographic) – correct area; orthomorphic – correct shape; azimuthal – correct direction; equidistant – correct distance.
"""), ST(S + '21-st3', 'the construction of conical, cylindrical equal area and Mercator projections', """
T: standard parallel | the parallel along which the cone or cylinder touches the globe and the scale is correct
T: conical projection with one standard parallel | a projection in which a cone touches the globe along one parallel, suited to mid-latitude areas with small east-west extent
T: cylindrical equal area projection | Lambert's projection in which parallels and meridians are straight lines at right angles and areas are correct
T: Mercator's projection | an orthomorphic cylindrical projection devised by Gerardus Mercator in 1569, used for navigation
T: loxodrome | a line of constant bearing (rhumb line), shown as a straight line on Mercator's projection
Q: On Mercator's projection, lines of constant bearing (loxodromes) are shown as: | straight lines | curves | circles | points
Q: Mercator's projection is most useful for: | navigation | showing correct areas of countries | mapping only the poles | showing population density
Q: In a cylindrical equal area projection, the pole is shown as a: | straight line equal in length to the equator | point | small circle | curve
Q: The conical projection with one standard parallel is best suited for: | mid-latitude areas with a small east-west extent | the whole world | polar regions only | equatorial regions only
Q: In Mercator's projection, areas in high latitudes appear: | greatly exaggerated | correctly sized | smaller than real | absent at the equator
Q: Mercator's projection was devised in: | 1569 | 1769 | 1469 | 1869
Y: 1569 | Mercator's projection devised by Gerardus Mercator
M:projection-use: Mercator's projection | navigation charts and ocean routes
M:projection-use: Cylindrical equal area projection | world distribution of tropical crops and products
M:projection-use: Conical projection with one standard parallel | mid-latitude countries with small east-west extent
M:projection-use: Polar zenithal projection | maps of polar regions
S+: In a conical projection with one standard parallel, parallels are concentric arcs and meridians are straight lines meeting at the apex
S+: In the cylindrical equal area projection, the spacing of parallels decreases towards the poles
S+: The cylindrical equal area projection is suitable for showing the distribution of tropical crops such as rice, tea, coffee and rubber
S+: In Mercator's projection, scale is correct along the equator and increases towards the poles
S+: The poles cannot be shown on Mercator's projection
S+: Greenland appears much larger than it really is on Mercator's projection
S-: Mercator's projection shows correct areas | It is orthomorphic and greatly exaggerates areas in high latitudes
S-: In the cylindrical equal area projection, the pole is a point | The pole is a straight line equal to the equator
S-: The conical projection with one standard parallel is ideal for a world map | It is suited only to mid-latitude areas with small east-west extent
C: Mercator's projection is used for navigation | it shows lines of constant bearing (loxodromes) as straight lines
C: Areas in high latitudes are exaggerated on Mercator's projection | parallels and meridians are stretched more and more towards the poles to keep shapes correct
C: The cylindrical equal area projection distorts shape in high latitudes | parallels are crowded towards the poles while meridians stay parallel
X: C2 D2 2 | State two properties and two limitations of Mercator's projection. | Properties – orthomorphic, loxodromes straight, parallels and meridians straight at right angles; limitations – areas exaggerated in high latitudes, poles cannot be shown.
X: C3 D3 3 | State the properties and limitations of the conical projection with one standard parallel. | Parallels concentric arcs, meridians straight lines meeting at apex, scale correct along the standard parallel; limitations – not for world map, distortion away from standard parallel; suited to mid-latitudes.
L: D4 | Compare the cylindrical equal area projection with Mercator's projection. | Both cylindrical, parallels and meridians straight at right angles; equal area (Lambert) – correct area, parallels closer towards poles, pole a line equal to equator, shape distorted, tropical distributions; Mercator (1569) – orthomorphic, parallel spacing increases polewards, loxodromes straight, navigation, areas exaggerated, poles not shown.
""")]

CH22 = [ST(S + '22-st1', 'topographical maps and the Survey of India indexing', """
T: topographical map | a large-scale map prepared by precise survey showing natural and man-made features of an area
T: International Map Series | the series of 1:1,000,000 maps covering 4° latitude by 4° longitude, prepared under international agreement
T: India and Adjacent Countries Series | the Survey of India series in which 4° by 4° sheets are numbered and divided into smaller sheets
T: conventional signs | standard symbols and colours used on topographical maps to show features
Q: A topographical sheet on 1:1,000,000 scale covers: | 4° latitude by 4° longitude | 1° latitude by 1° longitude | 15' by 15' | 30' by 30'
Q: A topographical sheet on 1:250,000 scale covers: | 1° latitude by 1° longitude | 4° by 4° | 15' by 15' | 7'30" by 7'30"
Q: A topographical sheet on 1:50,000 scale covers: | 15' latitude by 15' longitude | 1° by 1° | 4° by 4° | 30' by 1°
Q: A 4° by 4° sheet is divided into how many 1:250,000 sheets? | 16 | 4 | 9 | 25
Q: The 1:250,000 sheets within a 4° sheet are designated by the letters: | A to P | A to D | 1 to 16 | NE, NW, SE, SW
Q: Water features such as rivers and lakes are shown on topographical maps in: | blue | brown | green | yellow
Q: Contours on topographical maps are shown in: | brown | blue | red | black
Q: Wooded areas are shown on topographical maps in: | green | yellow | blue | brown
Q: Cultivated areas are shown on topographical maps in: | yellow | green | blue | brown
M:sheet-extent: 1:1,000,000 | 4° latitude by 4° longitude
M:sheet-extent: 1:250,000 | 1° latitude by 1° longitude
M:sheet-extent: 1:50,000 | 15' latitude by 15' longitude
M:sheet-extent: 1:25,000 | 7'30" latitude by 7'30" longitude
M:map-colour: Blue | water features such as rivers and lakes
M:map-colour: Brown | contours and relief features
M:map-colour: Green | wooded areas
M:map-colour: Yellow | cultivated land
S+: Topographical maps are prepared by the Survey of India
S+: A 1:250,000 sheet is divided into 16 sheets on 1:50,000 scale, numbered 1 to 16, such as 53A/1
S+: A 1:50,000 sheet is divided into four 1:25,000 sheets designated NE, NW, SE and SW
S+: Topographical maps show relief, drainage, vegetation, settlements, transport and land use
S+: Conventional signs make topographical maps easy to read without lengthy descriptions
S-: A 1:250,000 sheet covers 15' by 15' | It covers 1° by 1°; a 1:50,000 sheet covers 15' by 15'
S-: Contours are shown in blue on topographical maps | Contours are shown in brown; water features in blue
S-: A 1:50,000 sheet is divided into sixteen 1:25,000 sheets | It is divided into four 1:25,000 sheets (NE, NW, SE, SW)
C: Topographical maps use conventional signs and colours | they show many features in little space and make the map readable to all users
C: Topographical maps are numbered by a reference system | a sheet can be located quickly from its number, such as 53A/1
X: C2 D2 2 | What do the sheet numbers 53 and 53A/1 indicate? | 53 – a 4° × 4° sheet on 1:1,000,000; 53A – a 1° × 1° sheet on 1:250,000; 53A/1 – a 15' × 15' sheet on 1:50,000.
X: C3 D3 3 | Explain the Survey of India indexing of topographical maps. | 4° × 4° sheets (1:1,000,000) numbered; each divided into 16 sheets of 1° × 1° (1:250,000), A to P; each into 16 sheets of 15' × 15' (1:50,000), 1 to 16; each into four 7'30" sheets (1:25,000), NE, NW, SE, SW.
"""), ST(S + '22-st2', 'contours, methods of depicting relief and drawing cross-sections', """
T: contour | an imaginary line joining places of the same elevation above mean sea level
T: contour interval | the difference in elevation between two successive contours, also called the vertical interval
T: horizontal equivalent | the horizontal distance between two points or contours on the ground
T: gradient | the ratio of the vertical interval to the horizontal equivalent
T: hachures | short lines drawn in the direction of slope to show relief
T: spot height | a point on a map with its exact height marked by a dot and number
T: bench mark | a mark of known height fixed on a permanent object, used as a reference in levelling
T: layer tints | colours used for different height zones to show relief
Q: Lines joining places of the same height above mean sea level are: | contours | isobars | isohyets | isotherms
Q: Closely spaced contours indicate a: | steep slope | gentle slope | flat plain | river
Q: Widely spaced contours indicate a: | gentle slope | steep slope | cliff | waterfall
Q: The difference in height between two successive contours is the: | contour interval | horizontal equivalent | gradient | spot height
Q: When contours are closely spaced at the top and widely spaced at the bottom, the slope is: | concave | convex | uniform | terraced
Q: Short lines drawn in the direction of slope to show relief are: | hachures | contours | layer tints | spot heights
M:relief-method: Hachures | short lines along the direction of slope
M:relief-method: Hill shading | shading of slopes assuming light from the north-west
M:relief-method: Layer tints | colours for different height zones
M:relief-method: Spot height | dot with exact height of a point
M:relief-method: Contours | lines joining points of equal height
S+: Contours are drawn at a regular interval called the contour interval
S+: Contours never cross each other except in the case of an overhanging cliff
S+: When contours are evenly spaced, the slope is uniform
S+: In a convex slope, contours are widely spaced at the top and closely spaced at the bottom
S+: In a concave slope, contours are closely spaced at the top and widely spaced at the bottom
S+: A cross-section (profile) is drawn from contours to show the shape of the land along a line
S-: Closely spaced contours indicate a gentle slope | Closely spaced contours indicate a steep slope
S-: Contours often cross each other | They do not cross except at an overhanging cliff
S-: In a convex slope, contours are close at the top and wide apart at the bottom | That is a concave slope; a convex slope has wide spacing at the top and close spacing at the bottom
C: Closely spaced contours show a steep slope | the land rises a large height over a short horizontal distance
C: Contours do not normally cross | a point cannot have two different heights, except under an overhanging cliff
C: Contours are the most widely used method of showing relief | they give exact heights and show the shape and slope of land
X: C2 D2 2 | Distinguish between a convex and a concave slope as shown by contours. | Convex – contours wide apart at the top, close at the bottom; concave – close at the top, wide apart at the bottom.
X: C3 D3 3 | Name and explain three methods of showing relief on maps. | Hachures – short lines along slope; hill shading; layer tints – colours by height; spot heights and bench marks; contours – lines of equal height.
"""), ST(S + '22-st3', 'identification of landforms and interpretation of topographical maps', """
T: conical hill | a hill shown by concentric contours rising evenly to a summit
T: plateau | an extensive elevated flat area, shown by contours closely spaced at the margins and widely spaced in the middle
T: V-shaped valley | a river valley shown by V-shaped contours pointing towards higher ground
T: spur | a tongue of land projecting from higher ground into lower ground, shown by V-shaped contours pointing towards lower ground
T: cliff | a very steep slope where contours run very close together or merge
T: gorge | a deep and narrow valley with very steep sides, shown by closely spaced contours along a river
T: settlement pattern | the arrangement of houses in a settlement, such as compact, scattered, linear or circular
Q: Concentric contours rising evenly to a summit show a: | conical hill | V-shaped valley | spur | gorge
Q: V-shaped contours pointing towards higher ground show a: | V-shaped valley | spur | cliff | plateau
Q: V-shaped contours pointing towards lower ground show a: | spur | V-shaped valley | gorge | waterfall
Q: Contours that merge into one another indicate a: | cliff | plateau | gentle slope | plain
Q: Settlements found along a road or river in a line show a: | linear pattern | circular pattern | dispersed pattern | radial pattern
Q: A settlement in which houses are clustered closely together shows a: | compact pattern | dispersed pattern | linear pattern | scattered pattern
M:landform-contour: Conical hill | concentric contours rising evenly to a summit
M:landform-contour: Plateau | close contours at the edges, wide in the middle
M:landform-contour: V-shaped valley | V-shaped contours pointing to higher ground
M:landform-contour: Spur | V-shaped contours pointing to lower ground
M:landform-contour: Cliff | contours merging into one another
S+: Interpretation of a topographical map involves the study of relief, drainage, vegetation, land use, settlements and transport
S+: Settlements are often found near water sources and along transport routes
S+: Settlements may be compact, scattered, linear or circular in pattern
S+: Transport routes generally follow gentle slopes and avoid steep relief
S+: Land use such as cultivation is usually found on plains and gentle slopes
S-: A spur is shown by V-shaped contours pointing towards higher ground | A spur's V points to lower ground; a valley's V points to higher ground
S-: Contours of a plateau are widely spaced at the margins | They are closely spaced at the margins and widely spaced on top
S-: Roads usually run across the steepest slopes | Roads usually follow gentle slopes and valleys
C: Settlements are often linear along roads and rivers | these provide water, transport and access to markets
C: Roads and railways follow valleys in hilly areas | valleys offer gentle gradients and easier construction
C: Cultivation is concentrated on plains and gentle slopes | level land with fertile soils and water is easier to farm
X: C2 D2 2 | How will you identify a V-shaped valley and a spur on a topographical map? | Valley – V-shaped contours with the V pointing to higher ground, often with a stream; spur – V pointing to lower ground.
X: C3 D3 3 | Describe the steps in interpreting a topographical map. | Read marginal information (scale, sheet number, legend); study relief and drainage from contours and streams; study land use and vegetation; settlement patterns; transport; relate human features to relief.
""")]

CH23 = [ST(S + '23-st1', 'remote sensing: stages and the electromagnetic spectrum', """
T: remote sensing | the process of acquiring and measuring information about objects and phenomena without being in physical contact with them
T: electromagnetic spectrum | the continuum of electromagnetic radiation arranged by wavelength or frequency, from gamma rays to radio waves
T: spectral signature | the characteristic pattern of reflection of energy by an object at different wavelengths
T: sensor | a device that collects reflected or emitted electromagnetic radiation and converts it into a signal
T: platform | a carrier such as an aircraft or a satellite on which sensors are mounted
Q: The main source of energy in remote sensing is the: | sun | moon | earth's interior | sensor
Q: The visible part of the electromagnetic spectrum lies roughly between: | 0.4 and 0.7 micrometres | 7 and 10 micrometres | 1 and 2 metres | 10 and 100 nanometres
Q: The characteristic pattern of reflectance of an object at different wavelengths is its: | spectral signature | resolution | tone | swath
Q: The device that records reflected or emitted energy in remote sensing is a: | sensor | platform | pixel | data product
Q: A carrier on which sensors are mounted is called a: | platform | pixel | band | scanner
S+: The stages of remote sensing are source of energy, propagation through the atmosphere, interaction with the earth's surface, propagation of reflected or emitted energy, detection by sensors, conversion into data products, extraction of information and conversion into maps or tables
S+: Different objects reflect energy differently at different wavelengths
S+: Healthy vegetation reflects strongly in the near-infrared part of the spectrum
S+: Clear water absorbs most of the near-infrared radiation and appears dark in infrared images
S+: Remote sensing provides repetitive coverage of large areas
S-: In remote sensing the sensor touches the object | Information is acquired without physical contact with the object
S-: Clear water appears bright in near-infrared images | Clear water absorbs near-infrared radiation and appears dark
S-: All objects reflect energy in the same way at all wavelengths | Each object has its own spectral signature
C: Different objects can be identified in satellite images | each object reflects and absorbs energy differently, giving it a distinct spectral signature
C: Water bodies appear dark in near-infrared images | water absorbs most near-infrared radiation
C: Remote sensing is useful for monitoring large areas | satellites provide repetitive coverage of large and inaccessible areas
X: C2 D2 2 | What is remote sensing? Name its main source of energy. | Acquiring information about objects without physical contact, using reflected or emitted energy recorded by sensors; the sun.
X: C3 D3 3 | Describe the stages of remote sensing. | Energy source (sun); propagation through atmosphere; interaction with earth's surface; propagation of reflected/emitted energy; detection by sensor; conversion into data products; extraction of information; conversion into maps and tables.
L: D4 | Explain the stages of remote sensing and the role of the electromagnetic spectrum. | Stages – source, propagation, interaction, return propagation, detection, data products, information extraction, maps; spectrum – gamma to radio, visible 0.4–0.7 µm, infrared, microwave; spectral signatures – vegetation bright in near-infrared, water dark; applications.
"""), ST(S + '23-st2', 'sensors, resolution and satellite images', """
T: multispectral scanner | a sensor that records reflected energy in several bands of the spectrum at once
T: whiskbroom scanner | a scanner with a rotating mirror that scans the ground across the flight path one line at a time
T: pushbroom scanner | a scanner with an array of detectors that records a whole line across the path at once
T: spatial resolution | the size of the smallest object on the ground that a sensor can distinguish, given by the size of a pixel
T: spectral resolution | the ability of a sensor to record energy in narrow wavelength bands
T: radiometric resolution | the ability of a sensor to distinguish small differences in the strength of energy
T: temporal resolution | how often a sensor revisits and records the same area
T: pixel | the smallest unit (picture element) of a digital image
T: sun-synchronous satellite | a satellite in a near-polar orbit that passes over a place at the same local time
T: geostationary satellite | a satellite at about 36,000 km above the equator that moves with the earth's rotation and observes the same area continuously
Q: Satellites that observe the same area continuously from about 36,000 km above the equator are: | geostationary satellites | sun-synchronous satellites | polar satellites only | aircraft platforms
Q: The size of the smallest object that a sensor can distinguish is its: | spatial resolution | spectral resolution | radiometric resolution | temporal resolution
Q: How often a satellite revisits the same area is its: | temporal resolution | spatial resolution | spectral resolution | radiometric resolution
Q: The smallest unit of a digital image is a: | pixel | band | swath | tone
Q: The INSAT satellites of India are: | geostationary satellites | sun-synchronous satellites | aircraft platforms | ground stations
Q: The IRS series of Indian satellites are: | sun-synchronous satellites | geostationary satellites | communication satellites only | weather balloons
Q: A scanner that uses an array of detectors to record a whole line at once is a: | pushbroom scanner | whiskbroom scanner | photographic camera | radar altimeter
M:resolution-type: Spatial resolution | size of the smallest object distinguished
M:resolution-type: Spectral resolution | width of the wavelength bands recorded
M:resolution-type: Radiometric resolution | ability to detect small differences in energy
M:resolution-type: Temporal resolution | frequency of revisiting the same area
S+: Sensors are of two types: photographic (cameras) and non-photographic (scanners)
S+: Multispectral scanners are of two types: whiskbroom and pushbroom
S+: Sun-synchronous satellites are used for earth resources observation, such as the IRS and Landsat series
S+: Geostationary satellites are used for communication and weather monitoring, such as INSAT
S+: The finer the spatial resolution, the smaller the objects that can be identified
S-: INSAT satellites are sun-synchronous | INSAT satellites are geostationary; IRS satellites are sun-synchronous
S-: A coarser spatial resolution shows smaller objects | A finer spatial resolution shows smaller objects
S-: Temporal resolution refers to the size of a pixel | It refers to how often the same area is revisited; pixel size is spatial resolution
C: Geostationary satellites are used for weather monitoring | they observe the same area continuously from a fixed position over the equator
C: Sun-synchronous satellites are suitable for earth resources study | they pass over each place at the same local time, giving comparable images under similar light
C: Multispectral images are useful in identifying objects | they record energy in several bands, so differences in spectral signatures can be compared
X: C2 D2 2 | Distinguish between sun-synchronous and geostationary satellites. | Sun-synchronous – near-polar orbit, same local time, earth resources (IRS, Landsat); geostationary – about 36,000 km over equator, fixed view, communication and weather (INSAT).
X: C3 D3 3 | Explain the four types of resolution of a sensor. | Spatial – smallest object (pixel size); spectral – band width; radiometric – sensitivity to energy differences; temporal – revisit frequency.
"""), ST(S + '23-st3', 'interpretation of satellite imageries', """
T: tone | the relative brightness or colour of objects in an image
T: texture | the variation of tone that gives an image a smooth or rough appearance
T: association | the relationship between an object and the features around it, used to identify the object
T: false colour composite | an image in which bands are displayed in colours different from their natural colours, such as near-infrared shown in red
T: shadow | the dark outline cast by tall objects that helps to identify their shape and height
Q: In a standard false colour composite, healthy vegetation appears: | red | blue | white | black
Q: The relative brightness or colour of objects in an image is called: | tone | texture | pattern | association
Q: Identifying a school by the presence of a playground nearby uses the element of: | association | tone | shadow | size
Q: Clear, deep water in a standard false colour composite generally appears: | dark blue to black | bright red | white | yellow
Q: The smooth or rough appearance of an area in an image is its: | texture | tone | size | shape
M:image-element: Tone | brightness or colour of objects
M:image-element: Texture | smooth or rough appearance
M:image-element: Shape | outline or form of objects
M:image-element: Association | relationship with surrounding features
M:image-element: Shadow | dark outline cast by tall objects
S+: The elements of image interpretation are tone or colour, texture, size, shape, shadow, pattern and association
S+: In a standard false colour composite, healthy vegetation appears red because it reflects strongly in the near-infrared
S+: Size and shape help to distinguish features such as buildings, roads and fields
S+: Shadows help in identifying the height and shape of tall objects
S+: Pattern refers to the spatial arrangement of objects, such as orchards in rows
S-: In a standard false colour composite, healthy vegetation appears green | It appears red because near-infrared is shown in red
S-: Tone refers to the outline of an object | Tone is relative brightness or colour; shape is the outline
S-: Association is the size of an object | Association is the relationship of an object with surrounding features
C: Healthy vegetation appears red in a standard false colour composite | it reflects strongly in the near-infrared band, which is displayed in red
C: Association helps in image interpretation | some features occur together, such as a school with a playground or a factory with a railway siding
C: Shadows help interpret tall objects | the shape of a shadow reveals the height and outline of features such as towers and buildings
X: C2 D2 2 | Why does healthy vegetation appear red in a standard false colour composite? | It reflects strongly in near-infrared, and the near-infrared band is displayed in red.
X: C3 D3 3 | Name and explain any three elements of image interpretation. | Tone/colour – brightness; texture – smooth or rough; size; shape; shadow; pattern – arrangement; association – related features.
L: D4 | Describe the elements used in the interpretation of satellite imageries. | Tone/colour (FCC – vegetation red, water dark); texture; size; shape; shadow; pattern; association; with examples of settlements, fields, water bodies, forests.
""")]

CHAPTERS = [
    (CH18, {'chapter_topic': 'maps'}),
    (CH19, {'chapter_topic': 'map scale'}),
    (CH20, {'chapter_topic': 'latitude, longitude and time'}),
    (CH21, {'chapter_topic': 'map projections'}),
    (CH22, {'chapter_topic': 'topographical maps'}),
    (CH23, {'chapter_topic': 'remote sensing'}),
]
