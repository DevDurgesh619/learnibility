"""CBSE class 12 Geography, Practical Work in Geography Part II (chapters 18-21): fact tables for g12_hum_engine.

Numeric items for these chapters come from g12_geography_num.EXTRA.
"""
from g12_hum_engine import ST

S = 'cbse-g12-geography-ch'

CH18 = [ST(S + '18-st1', 'the need for data and forms of data', """
T: data | numbers that represent measurements from the real world
T: datum | a single measurement
T: statistics | the collection, analysis and interpretation of numerical data
T: qualitative data | data that describe attributes or qualities that cannot be measured directly, such as types of soil or land use
T: quantitative data | data expressed in numbers that can be measured, such as rainfall, population or temperature
Q: A single measurement is called a: | datum | data set | table | frequency
Q: Data that are expressed in numbers and can be measured are called: | quantitative data | qualitative data | secondary data | unpublished data
Q: Which of the following is an example of qualitative data? | Type of soil in a village | Rainfall in mm | Population of a town | Temperature in °C
Q: Data are needed in geography mainly to: | describe, analyse and explain spatial patterns and relationships | replace all maps | avoid field work | decorate reports
S+: Data are defined as numbers that represent measurements from the real world
S+: Geographical analysis depends on data to understand spatial patterns and relationships
S+: Information is a meaningful answer to a query or a fact that can be obtained from data
S+: Data help in planning and decision-making at local, regional and national levels
S+: Raw data must be processed and presented to become meaningful
S-: A datum is a large collection of measurements | A datum is a single measurement; data are many measurements
S-: Rainfall in mm is qualitative data | It is quantitative data because it is measured in numbers
S-: Raw data can be interpreted easily without processing | Raw data need to be organised and processed to be meaningful
C: Data are essential for geographical studies | they allow geographers to describe and analyse spatial patterns and relationships accurately
C: Raw data need to be processed | large masses of unorganised numbers are difficult to understand and interpret
X: C2 D2 2 | Distinguish between data and information. | Data – numbers representing measurements of the real world; information – meaningful answer or fact obtained from data after processing.
X: C3 D3 3 | Why are data needed in geography? Give three reasons. | Describe phenomena precisely; analyse spatial patterns and relationships; compare places and times; support planning and decision-making; test theories.
L: D4 | Explain the need for data in geography and the difference between qualitative and quantitative data with examples. | Data as measurements; need – description, analysis, comparison, planning; qualitative (soil type, land use) vs quantitative (rainfall, population, temperature); processing raw data.
"""), ST(S + '18-st2', 'primary and secondary sources of data', """
T: primary data | data collected for the first time by an individual or a group, directly from the field
T: secondary data | data collected from published or unpublished sources that have already been gathered by others
T: questionnaire | a list of simple questions with possible answers given to respondents to fill in themselves
T: schedule | a list of questions filled in by the enumerator after asking the respondents
T: Census of India | the decennial count of India's population conducted by the Office of the Registrar General and Census Commissioner
Q: Data collected through personal observation and interviews are: | primary data | secondary data | unpublished data | international data
Q: Which of the following is a source of secondary data? | Census of India | Personal observation | Interview | Questionnaire filled by the researcher's respondents
Q: The Census of India is conducted by the: | Office of the Registrar General and Census Commissioner | National Sample Survey Office | India Meteorological Department | Planning Commission
Q: The Human Development Report is published by the: | UNDP | WHO | WTO | UNESCO
Q: A list of questions filled in by the enumerator after asking the respondent is called a: | schedule | questionnaire | census | frequency table
M:src: Census of India | Office of the Registrar General and Census Commissioner
M:src: Human Development Report | UNDP
M:src: weather reports | India Meteorological Department
M:src: sample surveys | National Sample Survey Office
S+: Primary data are collected through personal observation, interviews, questionnaires and schedules
S+: Secondary data come from published sources such as government publications, international publications, newspapers and periodicals
S+: The Census of India, the reports of the National Sample Survey and weather reports of the India Meteorological Department are government publications
S+: Unpublished records of government, municipal corporations and other bodies are also sources of secondary data
S+: Instruments such as soil kits and water quality kits are used to collect primary data in the field
S-: The Census of India is a source of primary data for a student project | For a student, Census data are secondary data collected by others
S-: A questionnaire is filled in by the enumerator | A questionnaire is filled in by respondents; a schedule is filled in by the enumerator
S-: Newspapers are a source of primary data | They are a source of secondary data
C: Secondary data are widely used in geography | they save time and money and cover large areas and long periods
C: Primary data are more reliable for a specific study | they are collected directly by the researcher for the purpose of the study
X: C2 D2 2 | Distinguish between a questionnaire and a schedule. | Questionnaire – questions answered and filled in by respondents; schedule – questions asked and filled in by the enumerator.
X: C3 D3 3 | Name three published sources of secondary data with one example each. | Government publications (Census of India, NSSO reports, IMD weather reports); semi-government publications (municipal and zila parishad reports); international publications (UN Demographic Yearbook, UNDP Human Development Report); private publications; newspapers and magazines.
L: D4 | Explain the sources of primary and secondary data with examples. | Primary – personal observation, interview, questionnaire, schedule, kits; secondary – published (government, semi-government, international, private, newspapers) and unpublished records; examples: Census, NSSO, IMD, UNDP.
"""), ST(S + '18-st3', 'tabulation and classification of data', """
T: frequency | the number of times a value or values in a class interval occur in a data set
T: class interval | the range of values in a group of a frequency distribution, with a lower and an upper limit
T: exclusive method | the method of grouping in which the upper limit of one class is the lower limit of the next and is not counted in the class
T: inclusive method | the method of grouping in which both the lower and the upper limits are included in the class
T: ogive | a cumulative frequency curve
T: frequency polygon | a graph drawn by joining the mid-points of the tops of the bars of a histogram
T: index number | a statistical measure that shows change in a variable compared with a base year taken as 100
Q: A cumulative frequency curve is called an: | ogive | histogram | isopleth | polygraph
Q: In the exclusive method of classification, the upper limit of a class is: | not included in that class | included in that class | always zero | double the lower limit
Q: The class mark of a class interval is its: | mid-point | upper limit | lower limit | frequency
Q: In an index number, the value for the base year is taken as: | 100 | 0 | 1 | 1,000
Q: Tally marks are usually drawn in groups of: | five | two | ten | three
S+: Data are tabulated and classified to make them easy to understand and compare
S+: Data can be presented as absolute data, as ratios or percentages, or as index numbers
S+: In the inclusive method both the lower and the upper limits are part of the class interval
S+: Frequency distribution shows how values are distributed in different class intervals
S+: A frequency polygon is drawn by joining the mid-points of the tops of the bars of a histogram
S-: An ogive is a type of bar diagram | An ogive is a cumulative frequency curve
S-: In the exclusive method both class limits are included in the class | In the exclusive method the upper limit is excluded from the class
S-: In index numbers the base year value is taken as 0 | The base year value is taken as 100
C: Tally marks are used in grouping data | they make it quick and easy to count the frequency of values falling in each class
C: Data are classified into class intervals | grouping makes large masses of raw data easy to understand and compare
X: C2 D2 2 | Distinguish between the inclusive and exclusive methods of classification. | Inclusive – both lower and upper limits included (10–19, 20–29); exclusive – upper limit of a class excluded and becomes lower limit of the next (10–20, 20–30).
L: D4 | Explain the methods of tabulation and classification of data with the help of a frequency distribution. | Absolute data, ratios and percentages, index numbers; grouping raw data into classes; inclusive and exclusive methods; tally marks; frequency, cumulative frequency, ogive, histogram and frequency polygon.
""")]

CH19 = [ST(S + '19-st1', 'measures of central tendency', """
T: mean | the value obtained by summing all observations and dividing by the number of observations
T: median | the value of the rank-ordered middle observation, which divides the data into two equal parts
T: mode | the value that occurs most frequently in a data set
T: measures of central tendency | statistical measures such as mean, median and mode that give a single value representing a data set
Q: The value that occurs most frequently in a data set is the: | mode | mean | median | range
Q: The middle value of a set of observations arranged in order is the: | median | mode | mean | standard deviation
Q: The mean is affected most by: | extreme values | the number of modes | the order of the data | the median
Q: Which measure of central tendency can be found for qualitative data such as the most common soil type? | Mode | Mean | Median | Standard deviation
M:ct: mean | sum of observations divided by their number
M:ct: median | middle value of ordered data
M:ct: mode | most frequent value
M:ct: range | difference between highest and lowest values
S+: The mean, median and mode are measures of central tendency
S+: The mean is the most commonly used measure of central tendency
S+: The median is not affected by extreme values in the data
S+: A data set may have more than one mode
S+: For grouped data the mean is calculated by multiplying class marks by frequencies, adding them and dividing by the total frequency
S-: The median is always the most frequent value | The mode is the most frequent value; the median is the middle value
S-: The mean is not affected by extreme values | The mean is strongly affected by extreme values
S-: A data set can have only one mode | It may have more than one mode
C: The median is preferred when data contain extreme values | it depends only on the middle position and is not affected by very large or very small values
C: The mean is widely used as a measure of central tendency | it takes all observations into account
X: C2 D2 2 | Distinguish between the mean and the median. | Mean – sum of observations ÷ number, affected by extreme values; median – middle value of ordered data, not affected by extreme values.
L: D4 | Explain the three measures of central tendency and their merits and limitations. | Mean – all values, affected by extremes; median – positional, unaffected by extremes, needs ordering; mode – most frequent, can be for qualitative data, may be more than one; methods for grouped and ungrouped data.
"""), ST(S + '19-st2', 'measures of dispersion', """
T: dispersion | the spread or scatter of values around a central value in a data set
T: range | the difference between the highest and the lowest values in a data set
T: mean deviation | the arithmetic average of the absolute deviations of observations from the mean or median
T: standard deviation | the square root of the mean of the squared deviations from the mean
T: coefficient of variation | the standard deviation expressed as a percentage of the mean, used to compare variability of data sets
Q: The difference between the highest and lowest values is the: | range | mean | mode | median
Q: Which measure of dispersion is the square root of the mean of squared deviations from the mean? | Standard deviation | Mean deviation | Range | Quartile deviation
Q: Which measure is used to compare the variability of two data sets with different means? | Coefficient of variation | Range | Mode | Median
Q: Measures of dispersion show: | how values are spread around the central value | only the middle value | only the most frequent value | the total of all values
S+: Measures of dispersion describe the spread of values around the central value
S+: Range is the simplest measure of dispersion but depends only on the two extreme values
S+: Standard deviation is the most widely used measure of dispersion
S+: The coefficient of variation is the standard deviation divided by the mean, multiplied by 100
S+: Two data sets with the same mean may have very different dispersion
S-: Range depends on all the values in a data set | Range depends only on the highest and lowest values
S-: Standard deviation is the difference between the highest and lowest values | That is the range; standard deviation is the root of the mean squared deviation
S-: Two data sets with the same mean always have the same spread | Their dispersion can be very different
C: Standard deviation is a better measure of dispersion than range | it takes into account every observation and not just the two extremes
C: Measures of dispersion are needed along with averages | two data sets with the same mean can differ greatly in spread
X: C2 D2 2 | Why is standard deviation considered a better measure of dispersion than range? | SD uses all observations; range depends only on extremes and is affected by unusual values.
L: D4 | Explain the measures of dispersion and their uses in geography. | Range, mean deviation, standard deviation, coefficient of variation; definitions and formulae; uses – comparing variability of rainfall, temperature, crop yields; same mean, different spread.
"""), ST(S + '19-st3', 'correlation and rank correlation', """
T: correlation | the degree and direction of relationship between two variables
T: positive correlation | a relationship in which both variables increase or decrease together
T: negative correlation | a relationship in which one variable increases as the other decreases
T: Spearman's rank correlation | a method of measuring correlation using the ranks of the values of two variables
T: scatter diagram | a graph in which the values of two variables are plotted as points to show their relationship
Q: If one variable increases as the other decreases, the correlation is: | negative | positive | zero | perfect positive
Q: The value of a correlation coefficient always lies between: | −1 and +1 | 0 and 10 | 0 and 100 | −10 and +10
Q: A correlation coefficient of +1 indicates: | perfect positive correlation | no correlation | perfect negative correlation | weak negative correlation
Q: In Spearman's formula ρ = 1 − 6Σd² ÷ (N³ − N), d stands for: | the difference between the ranks of paired values | the deviation from the mean | the class interval | the density
M:corr: +1 | perfect positive correlation
M:corr: −1 | perfect negative correlation
M:corr: 0 | no correlation
M:corr: −0.9 | high negative correlation
S+: Correlation measures the degree and direction of the relationship between two variables
S+: The correlation coefficient lies between −1 and +1
S+: A scatter diagram gives a visual idea of the relationship between two variables
S+: Spearman's rank correlation uses ranks instead of the actual values
S+: Correlation does not by itself prove that one variable causes the other
S-: A correlation coefficient can be greater than +1 | It always lies between −1 and +1
S-: Negative correlation means both variables increase together | In negative correlation one variable increases as the other decreases
S-: A high correlation always proves cause and effect | Correlation shows association, not necessarily causation
C: Rank correlation is useful for geographical data | many data, such as levels of development, can be ranked even when exact values are not comparable
C: A correlation coefficient close to zero shows little relationship | the values of one variable do not change in a consistent way with the other
X: C2 D2 2 | Distinguish between positive and negative correlation with one example each. | Positive – both variables change in the same direction (literacy and per capita income); negative – opposite directions (altitude and temperature).
L: D4 | Explain the meaning and types of correlation and the method of Spearman's rank correlation. | Correlation – degree and direction; positive, negative, zero; scatter diagram; range −1 to +1; Spearman – rank both variables, d, d², ρ = 1 − 6Σd² ÷ (N³ − N); interpretation; correlation is not causation.
""")]

CH20 = [ST(S + '20-st1', 'general rules for drawing graphs, diagrams and maps', """
T: scale | the measure used to represent data on a graph or diagram, which must be chosen to fit the data and the space
T: legend | the key on a graph, diagram or map that explains the colours, symbols and patterns used
T: title | the heading of a graph or map that states the area, the period and the subject shown
Q: The key that explains colours and symbols on a map or diagram is called the: | legend | scale | title | grid
Q: The title of a diagram should indicate: | the area, the time period and the subject | only the colour scheme | only the scale | only the source of data
Q: Which of these is a general rule for drawing graphs and diagrams? | Selecting a suitable method and scale | Using as many colours as possible | Leaving out the title | Using different scales on the same axis
S+: Selection of a suitable method of representation is the first rule of drawing graphs and diagrams
S+: The scale should be neither too large nor too small for the data and the space available
S+: The title, legend and direction are important parts of the design of a map or diagram
S+: The source of data should be mentioned below the diagram
S+: Graphs and diagrams make data easier to understand and compare than tables
S-: The title of a diagram is not necessary | The title is essential and should indicate the area, period and subject
S-: Any scale can be used without considering the data | The scale must suit the range of data and the space available
S-: A legend is used to show the north direction | A legend explains colours and symbols; a north arrow shows direction
C: Graphs and diagrams are used to present data | they make complex data easy to understand and compare at a glance
C: A suitable scale must be chosen | too large a scale cannot fit the space and too small a scale hides differences in the data
X: C2 D2 2 | State any two general rules for drawing graphs and diagrams. | Select a suitable method; select a suitable scale; design with title, legend and direction; mention the source of data (any two).
L: D4 | Explain the general rules for drawing graphs, diagrams and maps. | Selection of a suitable method; selection of a suitable scale; design – title (area, period, subject), legend, direction; neatness; source of data; advantages of graphical representation.
"""), ST(S + '20-st2', 'line graphs, bar diagrams and pie diagrams', """
T: line graph | a graph used to represent time-series data such as temperature, rainfall or population growth
T: polygraph | a line graph in which two or more variables are shown by different lines for comparison
T: bar diagram | a diagram of columns of equal width drawn on a common base, whose lengths represent values
T: compound bar diagram | a bar diagram in which a bar is divided into components to show parts of the total
T: line and bar graph | a combined diagram such as a climograph showing temperature as a line and rainfall as bars
T: pie diagram | a circle divided into sectors, each proportional to the share of a component of the total
Q: A climograph showing temperature and rainfall of a station is an example of a: | line and bar graph | pie diagram | dot map | choropleth map
Q: In a pie diagram, the angle of a sector is calculated as: | value ÷ total × 360 | value × 100 | total ÷ value × 100 | value ÷ 360
Q: A line graph is most suitable for showing: | time-series data | spatial distribution of population | percentage shares | land use by dots
Q: A line graph showing the growth rates of several cities with different lines is a: | polygraph | pie diagram | ogive | isopleth
Q: In a pie diagram, a share of 25 per cent is shown by a sector of: | 90 degrees | 25 degrees | 45 degrees | 180 degrees
M:graph: line graph | time-series data
M:graph: polygraph | several variables on one graph
M:graph: compound bar diagram | components of a total
M:graph: pie diagram | sectors of a circle
M:graph: line and bar graph | climograph of temperature and rainfall
S+: Line graphs are usually drawn to represent time-series data
S+: Bars in a bar diagram should be of equal width and equally spaced
S+: In a line and bar graph, rainfall is often shown by bars and temperature by a line
S+: In a pie diagram the total is represented by a circle of 360 degrees
S+: Sectors of a pie diagram are usually arranged in order of size
S-: In a pie diagram the total is represented by 100 degrees | The whole circle of 360 degrees represents the total
S-: A line graph is best for showing percentage shares of a total | A pie diagram or compound bar diagram is better for shares; line graphs suit time series
S-: Bars of a bar diagram can be of different widths | Bars should be of equal width
C: A pie diagram is suitable for showing composition | each sector is proportional to the share of a component in the total
C: Line graphs suit time-series data | they show changes over time clearly with a continuous line
X: C2 D2 2 | Distinguish between a simple bar diagram and a compound bar diagram. | Simple – one bar for each value; compound – each bar divided into components to show parts of a total.
L: D4 | Describe the construction and uses of line graphs, bar diagrams and pie diagrams. | Line graphs and polygraphs for time series; simple, multiple and compound bar diagrams; line and bar graph (climograph); pie diagram – angle = value ÷ total × 360; uses of each.
"""), ST(S + '20-st3', 'thematic maps: dot, choropleth and isopleth maps', """
T: thematic map | a map that shows the distribution of a particular phenomenon such as population, rainfall or crops
T: dot map | a map in which dots of uniform size, each representing a fixed value, show the distribution of a phenomenon
T: choropleth map | a map in which areas such as districts or states are shaded according to the value of a variable
T: isopleth map | a map in which lines join places having equal values of a variable
T: isohyet | a line joining places receiving equal rainfall
T: isotherm | a line joining places having equal temperature
T: isobar | a line joining places having equal atmospheric pressure
Q: A map in which areas are shaded according to the density of population is a: | choropleth map | dot map | isopleth map | flow map
Q: Lines joining places of equal rainfall are called: | isohyets | isotherms | isobars | contours
Q: Lines joining places of equal temperature are called: | isotherms | isohyets | isobars | isobaths
Q: A dot map is most suitable for showing the: | distribution of population | administrative boundaries | ocean currents | wind direction
Q: Lines joining places of equal atmospheric pressure are called: | isobars | isotherms | isohyets | contours
M:iso: isotherm | equal temperature
M:iso: isohyet | equal rainfall
M:iso: isobar | equal pressure
M:iso: contour | equal height
S+: In a dot map, all dots are of the same size and each dot represents a fixed number
S+: Choropleth maps show data relating to administrative units such as districts and states
S+: In a choropleth map, darker shades are used for higher values and lighter shades for lower values
S+: Isopleth maps are drawn for phenomena that change continuously, such as temperature and rainfall
S+: Interpolation is used to draw isopleths between points of known values
S-: In a dot map, dots of different sizes are used | All dots are of uniform size, each representing a fixed value
S-: Isohyets join places of equal temperature | Isohyets join places of equal rainfall; isotherms join places of equal temperature
S-: Choropleth maps are best for continuous phenomena like temperature | Isopleth maps suit continuous phenomena; choropleth maps suit data by administrative units
C: Choropleth maps are used for population density by districts | the data relate to administrative units and can be shaded by classes
C: Isopleths are drawn using interpolation | values are known only at certain points, and lines of equal value must be estimated between them
X: C2 D2 2 | Distinguish between a choropleth map and an isopleth map. | Choropleth – shading of administrative units by value classes (density); isopleth – lines joining places of equal value (isotherms, isohyets).
L: D4 | Describe the methods of preparing dot maps, choropleth maps and isopleth maps. | Dot maps – uniform dots, fixed value, distribution; choropleth – classes, graded shading of administrative units; isopleth – interpolation, lines of equal value (isotherm, isohyet, isobar, contour); suitability of each.
""")]

CH21 = [ST(S + '21-st1', 'GIS: components and spatial data formats', """
T: Geographic Information System | a system for capturing, storing, checking, integrating, manipulating, analysing and displaying data that are spatially referenced to the earth
T: raster data | spatial data represented as a grid of cells, each with a value
T: vector data | spatial data represented as points, lines and polygons defined by coordinates
T: spatial data | data about the location and shape of geographical features
T: attribute data | non-spatial data that describe the characteristics of spatial features
Q: In a GIS, data represented as a grid of cells are called: | raster data | vector data | attribute data | tabular data only
Q: Points, lines and polygons are used to represent: | vector data | raster data | images only | attribute tables only
Q: Which of these is a component of a GIS? | Hardware, software, data and people | Only paper maps | Only satellites | Only printers
Q: Information about the population of a village stored in a table linked to its location is: | attribute data | raster data | a scanned map | a buffer
M:gis: raster | grid of cells
M:gis: vector | points, lines and polygons
M:gis: attribute data | characteristics of features
M:gis: spatial data | location and shape of features
S+: A GIS integrates spatial data and attribute data
S+: The components of a GIS are hardware, software, data, people and procedures
S+: Raster data have a simple data structure and overlay operations are easy to perform
S+: Vector data are compact and represent boundaries and networks precisely
S+: Spatial data in a GIS are referenced to locations on the earth
S-: Vector data are made of grid cells | Raster data are grid cells; vector data are points, lines and polygons
S-: A GIS can handle only attribute data | A GIS handles both spatial and attribute data
S-: Raster data always need less storage than vector data | Raster data usually need large storage volumes
C: Raster data are convenient for overlay analysis | every layer has the same grid of cells, so cells can be combined directly
C: Vector data represent roads and boundaries well | points, lines and polygons are defined precisely by coordinates
X: C2 D2 2 | Distinguish between raster and vector data formats. | Raster – grid of cells, simple structure, easy overlay, large storage; vector – points, lines, polygons, compact, precise boundaries, complex overlay.
X: C3 D3 3 | Explain the components of a GIS. | Hardware (computers, input and output devices); software (to store, analyse and display data); data (spatial and attribute); people (users and experts); procedures or methods.
L: D4 | Explain the meaning, components and data formats of a GIS. | Definition; components – hardware, software, data, people, procedures; spatial and attribute data; raster and vector formats with merits and limitations.
"""), ST(S + '21-st2', 'advantages of GIS and sequence of GIS activities', """
T: data verification and editing | the GIS activity in which captured data are checked and errors corrected
T: spatial analysis | the GIS activity of examining locations, attributes and relationships of features to answer queries
T: digitisation | the conversion of map information into digital form
Q: Which is usually the first activity in the sequence of GIS activities? | Spatial data input | Spatial analysis | Output and display | Data editing
Q: The conversion of a paper map into digital form is called: | digitisation | interpolation | tabulation | buffering
Q: Which of these is an advantage of a GIS? | Easy updating and querying of spatial data | It cannot integrate data | It needs no data | It works only with paper maps
S+: The sequence of GIS activities includes spatial data input, entering attribute data, data verification and editing, linking spatial and attribute data, and spatial analysis
S+: A GIS allows users to ask queries about locations and attributes
S+: A GIS can integrate data from many sources, such as maps, satellite images and field surveys
S+: Data in a GIS can be updated easily
S+: A GIS allows different scenarios to be tested for planning
S-: Spatial analysis is the first step of GIS activities | Spatial data input comes first; analysis comes after data are entered, verified and linked
S-: Data in a GIS cannot be updated once entered | Data can be updated easily
S-: A GIS can use only one source of data | It integrates data from many sources
C: GIS is widely used in planning | it integrates many types of data and allows queries and analysis of spatial relationships
C: Data verification and editing is an essential step | errors in captured data would lead to wrong analysis and decisions
X: C2 D2 2 | Mention any two advantages of a GIS. | Integrates data from many sources; easy updating; queries about location and attributes; overlay and analysis; testing planning scenarios (any two).
L: D4 | Explain the sequence of activities in a GIS and its advantages. | Spatial data input (digitisation, scanning, images); attribute data entry; verification and editing; linking spatial and attribute data; spatial analysis (overlay, buffer, network); advantages.
"""), ST(S + '21-st3', 'overlay and buffer analysis in GIS', """
T: overlay analysis | the GIS operation that combines two or more data layers to produce a new layer showing their combined characteristics
T: buffer analysis | the GIS operation that creates a zone of a specified distance around a point, line or area feature
T: network analysis | the GIS operation that analyses routes and connectivity along a network such as roads
Q: Creating a zone of 500 m around a school to find nearby houses is an example of: | buffer analysis | overlay analysis | digitisation | tabulation
Q: Combining a land use layer with a soil layer to find suitable areas is an example of: | overlay analysis | buffer analysis | network analysis | interpolation
Q: Finding the shortest route between two places on a road map in a GIS uses: | network analysis | buffer analysis | overlay analysis | classification
S+: Overlay analysis combines two or more layers to answer questions about places where conditions coincide
S+: Buffers can be created around points, lines and areas
S+: Buffer analysis can be used to find areas within a specified distance of a road, river or facility
S+: Overlay analysis can be used to identify suitable sites, for example for a new industry or school
S+: Network analysis helps in finding the shortest or quickest routes
S-: Buffers can be created only around points | Buffers can be created around points, lines and areas
S-: Overlay analysis uses only a single layer | Overlay combines two or more layers
S-: Buffer analysis finds the shortest route between places | That is network analysis; buffer analysis creates zones at a given distance
C: Overlay analysis is useful for site selection | it combines several conditions such as land use, slope and soil to find areas that meet all of them
C: Buffer analysis is used in planning services | it shows which areas lie within a given distance of facilities such as schools, hospitals or roads
X: C2 D2 2 | Distinguish between overlay analysis and buffer analysis. | Overlay – combines two or more layers into a new layer; buffer – creates zones of specified distance around points, lines or areas.
L: D4 | Explain overlay, buffer and network analysis in a GIS with examples. | Overlay – combining layers (land use and soil) for site selection; buffer – zones around point, line, area features (school, road, river); network – shortest route; uses in planning.
""")]

CHAPTERS = [
    (CH18, {'chapter_topic': 'data: its source and compilation'}),
    (CH19, {'chapter_topic': 'data processing'}),
    (CH20, {'chapter_topic': 'graphical representation of data'}),
    (CH21, {'chapter_topic': 'spatial information technology'}),
]
