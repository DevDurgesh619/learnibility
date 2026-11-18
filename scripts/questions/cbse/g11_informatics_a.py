"""CBSE class 11 Informatics Practices (065): fact tables for the chapters not shared with Computer Science
(Understanding Data, Introduction to NumPy, Database Concepts, Introduction to SQL), written from NCERT
Informatics Practices class 11, plus the split of the shared Emerging Trends text into the IP subtopics.
Line format: g12_hum_engine.py. No textbook passage is reproduced.
"""
from __future__ import annotations

import g11_computer_science_a as CA

TXT = {}

# ---------------------------------------------------------------- ch02: AI text split into AI/ML/NLP and immersive
_IMM = ('reality', 'immersive', 'simulator', 'headset')


def split_ai():
    """Split the shared CS 'ai' block: lines about immersive experiences go to the IP AR/VR subtopic."""
    ai, imm = [], []
    for line in CA.TXT['ai'].strip().splitlines():
        tag, _, rest = line.partition(': ')
        parts = rest.split(' | ')
        if tag in ('T', 'M:technology'):
            probe = parts[0]
        elif tag == 'Q':
            probe = ' '.join(parts[:2])
        elif tag in ('X', 'L'):
            probe = parts[1] if len(parts) > 1 else rest
        else:
            probe = rest
        (imm if any(k in probe.lower() for k in _IMM) else ai).append(line)
    return '\n'.join(ai), '\n'.join(imm)


TXT['ai_more'] = """
T: chatbot | a computer program that uses natural language processing to hold a conversation with users through text or voice
T: computer vision | the field of AI that enables computers to identify and interpret images and videos
Q: Which field of AI lets a phone unlock by recognising the owner's face? | Computer vision | Natural language processing | Blockchain | Grid computing
Q: An AI system that learns to identify spam from examples of spam and non-spam emails uses: | machine learning | virtual reality | cloud storage | a spreadsheet
Q: Translating a sentence from Hindi to English automatically is an application of: | natural language processing | robotics | grid computing | data capturing
S+: Machine learning is a subset of artificial intelligence
S+: Spam filters and product recommendations use machine learning
S-: Artificial intelligence systems can work only with numbers | They can also work with text, speech and images
C: Voice assistants can answer spoken questions | natural language processing lets them understand and respond in human language
X: C2 D2 2 | Give two applications each of machine learning and natural language processing. | ML – spam filtering, recommendations, face recognition; NLP – voice assistants, translation, predictive typing, chatbots.
"""

TXT['imm_more'] = """
Q: Which technology is used when a furniture app shows how a sofa would look in your own room through the phone camera? | Augmented reality | Virtual reality | Grid computing | Blockchain
S+: Augmented reality adds digital information to the view of the real world, while virtual reality replaces it
S+: Immersive experiences are used in gaming, education, training and tourism
L: D4 | Explain immersive experiences, robotics and big data with examples. | AR – overlay on real view; VR – fully computer-generated world; uses in training, games; robots – automatic tasks, drones; big data – 5 Vs, analytics.
"""

# ---------------------------------------------------------------- ch05 Understanding Data
TXT['dtypes'] = """
T: structured data | data organised in a fixed format, such as rows and columns of a table, so that it is easy to search and process
T: unstructured data | data that has no fixed format or organisation, such as images, audio, video and text documents
T: data source | a place from which data is obtained, such as a survey, a sensor, a website or an existing record
Q: Which of the following is an example of structured data? | A table of students' roll numbers and marks | A video lecture | A voice message | A photograph of a classroom
Q: Which of the following is an example of unstructured data? | Posts and photos on social media | An attendance register in rows and columns | A railway timetable table | A bank statement table
Q: Data is collected and analysed mainly to: | take decisions | increase file sizes | replace all computers | avoid storage
M:data type: Spreadsheet of sales | structured data
M:data type: Recorded phone call | unstructured data
M:data type: Library catalogue table | structured data
M:data type: Collection of e-mails | unstructured data
S+: Data helps organisations to understand trends and take decisions
S+: Structured data can be stored in tables with rows and columns
S+: Unstructured data such as images and videos needs special methods to process
S-: Unstructured data is always stored in rows and columns | Structured data is stored in rows and columns; unstructured data has no fixed format
S-: Data is useful only after it is deleted | Data is useful when it is processed and analysed
C: A table of marks is called structured data | its values are organised in fixed rows and columns
C: A shop studies its past sales before ordering stock | analysing data helps to take better decisions
X: C2 D2 2 | Differentiate between structured and unstructured data with an example of each. | Structured – fixed format of rows and columns, e.g. marks table; unstructured – no fixed format, e.g. videos, images, e-mails.
X: C3 D3 3 | Why is data important? Give three examples of how organisations use data. | Basis of decisions; banks – detect fraud; shops – stock and offers; hospitals – patient care; government – planning (any three).
L: D4 | What is data? Explain its purpose and the types of data with examples. | Raw facts; purpose – decision making, planning, trends; structured – tables, records; unstructured – text, images, audio, video; metadata.
"""

TXT['dcollect'] = """
T: data collection | the process of gathering data from different sources for a purpose
T: data processing | the process of converting raw data into meaningful information by operations such as sorting, calculating and summarising
T: primary data | data collected first-hand for a specific purpose, for example through a survey or an experiment
T: secondary data | data that has already been collected by someone else and is reused, for example from published reports
T: data quality | the degree to which data is accurate, complete, consistent and up to date for its purpose
Q: Data collected by a student through her own survey of classmates is: | primary data | secondary data | metadata | unstructured data
Q: Using census figures published by the government in a project is an example of using: | secondary data | primary data | metadata | a sensor
Q: Arranging the records of a file in order of roll number is an example of: | data processing | data collection | data capturing only | data deletion
Q: A record in which the phone number field is left blank lacks: | completeness | volume | velocity | encryption
M:data quality: Accuracy | values are correct
M:data quality: Completeness | no required value is missing
M:data quality: Consistency | the same data matches everywhere it is stored
M:data quality: Timeliness | data is up to date
S+: Data can be collected through surveys, interviews, sensors, forms and online transactions
S+: Collected data must be stored before it can be processed
S+: Processing turns raw data into information that supports decisions
S+: Poor quality data leads to wrong conclusions
S+: Data can be stored on hard disks, SSDs, pen drives and cloud storage
S-: Secondary data is collected first-hand by the user | Primary data is first-hand; secondary data was collected earlier by others
S-: Data quality does not affect the result of processing | Wrong or incomplete data gives wrong results
C: Duplicate records are removed before analysing data | duplicates make totals and averages incorrect
C: A survey form uses fixed choices for answers | fixed choices make the collected data consistent and easy to process
X: C2 D2 2 | Differentiate between primary and secondary data with examples. | Primary – collected first-hand, e.g. own survey; secondary – collected earlier by others, e.g. census reports.
X: C3 D3 3 | Explain the steps of data collection, storage and processing with an example. | Collect – survey marks; store – spreadsheet or database on disk/cloud; process – sort, total, average to get results.
X: C3 D4 4 | A school collected feedback forms in which many entries were incomplete or duplicated. Explain how this affects data quality and suggest remedies. | Incomplete – missing values, wrong averages; duplicates – inflated counts; remedies – mandatory fields, validation, remove duplicates, check consistency.
L: D4 | Explain data collection, storage and processing, and describe the features of good quality data. | Sources – surveys, sensors, transactions; primary/secondary; storage devices and cloud; processing – sorting, calculation, summarising; quality – accurate, complete, consistent, timely.
"""

TXT['dstats'] = """
T: mean | the sum of all the values divided by the number of values
T: median | the middle value of the data when it is arranged in order
T: mode | the value that occurs the most number of times in the data
T: range | the difference between the largest and the smallest values of the data
T: standard deviation | a measure of how much the values are spread around the mean, equal to the square root of the mean of the squared deviations
T: variance | the mean of the squares of the deviations of the values from their mean, equal to the square of the standard deviation
T: measure of central tendency | a single value, such as the mean, median or mode, that represents the centre of the data
T: measure of variability | a value, such as the range or the standard deviation, that shows how spread out the data is
Q: For an even number of sorted values, the median is: | the average of the two middle values | the larger middle value | the first value | the mean of all values
Q: Which measure is most affected by one very large value? | Mean | Median | Mode | None of these
Q: Which measure can be found even for non-numeric data such as the most popular colour? | Mode | Mean | Standard deviation | Range
Q: A smaller standard deviation means the data is: | closer to the mean | more spread out | always zero | larger in value
Q: If every value of the data is the same, the standard deviation is: | 0 | 1 | equal to the mean | undefined
Q: The square of the standard deviation is the: | variance | range | mean | median
M:measure: Mean | sum of values ÷ number of values
M:measure: Median | middle value of sorted data
M:measure: Mode | most frequent value
M:measure: Range | largest − smallest
S+: Mean, median and mode are measures of central tendency
S+: Range and standard deviation are measures of variability
S+: Data must be sorted before finding the median
S+: Data can have more than one mode
S+: The median is not affected much by extreme values
S-: The range is the sum of the largest and smallest values | The range is the largest value minus the smallest value
S-: The standard deviation is the mean of the deviations | It is the square root of the mean of the squared deviations
S-: The mean is the value that occurs most often | That is the mode; the mean is the sum divided by the count
C: The median is preferred for the salaries of a company with a few very high salaries | extreme values pull the mean but not the median
C: The player with the smaller standard deviation of scores is called more consistent | the scores are closer to the mean
X: C2 D2 2 | Differentiate between measures of central tendency and measures of variability, giving two examples of each. | Central tendency – one representative value, e.g. mean, median, mode; variability – spread of data, e.g. range, standard deviation.
"""

# ---------------------------------------------------------------- ch06 NumPy
TXT['np1'] = """
T: NumPy | Numerical Python, a Python library for working with multi-dimensional arrays and doing fast numerical computations
T: ndarray | the n-dimensional array object of NumPy, which holds elements of the same data type
T: ndim | the attribute that gives the number of dimensions (axes) of a NumPy array
T: shape | the attribute that gives a tuple of the number of elements along each dimension of an array
T: size | the attribute that gives the total number of elements in an array
T: arange() | the NumPy function that creates an array of evenly spaced values from start up to, but not including, stop
T: linspace() | the NumPy function that creates an array of a given number of evenly spaced values between start and stop, including stop
Q: Which statement is used to import NumPy with its usual alias? | import numpy as np | import np as numpy | include numpy | using numpy
Q: Which function creates an array filled with zeros? | np.zeros() | np.empty_list() | np.null() | np.clear()
Q: The elements of a NumPy array must be: | of the same data type | of different data types | only strings | only integers
Q: Which attribute gives the data type of the elements of an array? | dtype | ndim | size | shape
Q: np.zeros((2, 3)) creates an array with: | 2 rows and 3 columns | 3 rows and 2 columns | 6 rows | 5 elements
Q: What does np.linspace(0, 1, 5) give? | five equally spaced values from 0 to 1 including 1 | values from 0 to 1 in steps of 5 | five copies of 1 | the numbers 0 to 4
M:function: np.zeros() | array filled with 0
M:function: np.ones() | array filled with 1
M:function: np.arange() | values in steps, stop excluded
M:function: np.linspace() | given number of values, stop included
S+: A NumPy array stores elements of a single data type
S+: Arithmetic operations on NumPy arrays are done element by element
S+: NumPy arrays take less memory and are faster than lists for numerical work
S+: The default data type of np.zeros() and np.ones() is float
S+: A 2-D array can be created from a list of lists of equal length
S-: A NumPy array can hold elements of different data types like a list | All elements of an array have the same data type
S-: np.arange(1, 5) includes the number 5 | The stop value is excluded: 1, 2, 3, 4
S-: Multiplying a NumPy array by 2 repeats the array | It multiplies each element by 2; a list would be repeated
C: np.array([1, 2.5, 3]) gives an array of floats | all elements are converted to a common data type
C: NumPy is preferred for large numerical data | arrays are stored compactly and operations run element-wise without loops
X: C2 D2 2 | Give any two differences between a Python list and a NumPy array. | List – mixed data types, * repeats, no element-wise maths; array – one data type, element-wise operations, less memory, faster.
X: C3 D3 3 | Explain the array attributes ndim, shape and size with an example. | a = np.array([[1, 2, 3], [4, 5, 6]]); ndim 2; shape (2, 3); size 6.
L: D4 | Explain NumPy arrays and the ways of creating them with examples. | ndarray, same type; np.array() from list/list of lists; zeros(), ones(), arange(), linspace(); attributes ndim, shape, size, dtype; difference from lists.
"""

TXT['np2'] = """
T: indexing | accessing a single element of an array by its position, such as a[1, 2] for row 1, column 2 of a 2-D array
T: slicing | extracting a part of an array using start:stop:step for each dimension
T: transpose | the operation that turns the rows of a 2-D array into columns, done by a.transpose() or a.T
T: element-wise operation | an operation applied to each pair of corresponding elements of arrays of the same shape
Q: For a 2-D array a, a[2, 1] gives the element in: | row 2, column 1 (counting from 0) | row 1, column 2 | the third column only | the second row only
Q: For a 2-D array a, a[:, 0] gives: | the first column | the first row | the last column | the whole array
Q: Which of the following gives the transpose of a 2-D array a? | a.T | a.t() | a.trans | np.turn(a)
Q: What does np.sort(a) do for a 1-D array a? | returns a sorted copy of a | sorts a in descending order | returns the largest element | deletes duplicates
Q: The result of np.array([1, 2, 3]) + np.array([10, 20, 30]) is: | [11 22 33] | [1 2 3 10 20 30] | 66 | [10 40 90]
S+: Index numbering of NumPy arrays starts from 0
S+: A slice of an array leaves out the element at the stop index
S+: Operations such as +, -, * and / on two arrays of the same shape work element-wise
S+: The transpose of an array of shape (2, 3) has shape (3, 2)
S+: np.sort() on a 2-D array sorts each row unless axis=0 is given, which sorts each column
S-: The * operator on two NumPy arrays joins them | It multiplies corresponding elements
S-: a[1, 2] gives the element in row 2, column 1 | It gives row 1, column 2 (counting from 0)
C: a[0:2, 1:3] gives a 2 × 2 array from a 3 × 4 array | rows 0–1 and columns 1–2 are selected
C: a > 5 gives an array of True and False values | comparison is also done element-wise
X: C2 D2 2 | Write the statements to display (i) the second row and (ii) the last column of a 2-D array a. | (i) print(a[1]) (ii) print(a[:, -1]).
X: C3 D3 3 | Explain indexing and slicing of 2-D arrays with examples. | a[i, j] element; a[i] row; a[:, j] column; a[r1:r2, c1:c2] sub-array; stop excluded; negative indices from the end.
"""

TXT['np3'] = """
T: concatenation | joining two or more arrays into one along an existing axis, done with np.concatenate()
T: reshaping | changing the shape of an array without changing its data, done with reshape()
T: splitting | dividing an array into several sub-arrays, done with np.split()
T: axis | a dimension of an array; for a 2-D array axis 0 runs down the rows and axis 1 runs across the columns
Q: Which function joins two arrays along an existing axis? | np.concatenate() | np.split() | np.reshape() | np.join_list()
Q: An array of 12 elements cannot be reshaped into: | 5 × 3 | 3 × 4 | 2 × 6 | 6 × 2
Q: np.concatenate((a, b), axis=1) for two 2 × 2 arrays gives an array of shape: | (2, 4) | (4, 2) | (2, 2) | (4, 4)
Q: np.split(a, 3) on an array of 9 elements gives: | three arrays of 3 elements each | nine arrays | three copies of a | an error
S+: reshape() needs the new shape to have the same total number of elements
S+: Concatenating along axis 0 adds rows, and along axis 1 adds columns
S+: np.split() with a number divides the array into that many equal parts
S+: np.split() with a list of indices splits the array at those positions
S-: reshape() can change the number of elements of an array | The total number of elements must stay the same
S-: Arrays of any shapes can always be concatenated along axis 0 | They must have the same number of columns
C: np.arange(6).reshape(5, 2) gives an error | 6 elements cannot fill a 5 × 2 array
C: Splitting an array of 10 elements into 3 equal parts gives an error | 10 cannot be divided into 3 equal parts
X: C2 D2 2 | Differentiate between concatenate() and split() with examples. | concatenate joins arrays, np.concatenate((a, b)); split divides one array into parts, np.split(a, 2).
X: C3 D3 3 | Explain reshape(), concatenate() and split() with one example each. | a.reshape(2, 3); np.concatenate((a, b), axis=0); np.split(a, 2) or at indices [2, 5].
"""

TXT['np4'] = """
T: loadtxt() | the NumPy function that reads data from a text or CSV file into an array, when no value is missing
T: genfromtxt() | the NumPy function that reads data from a text or CSV file into an array and can handle missing values
T: savetxt() | the NumPy function that writes an array to a text or CSV file
T: skiprows | the parameter of loadtxt() that gives the number of lines to skip at the start of the file, such as a header
T: delimiter | the parameter that gives the character, such as a comma, that separates values in a file
Q: Which function should be used to read a CSV file that has some missing values? | np.genfromtxt() | np.loadtxt() | np.savetxt() | np.array()
Q: For a 2-D array m, m.sum(axis=0) gives: | the sum of each column | the sum of each row | the total of all elements | the first row
Q: For a 2-D array m, m.max(axis=1) gives: | the largest value in each row | the largest value in each column | the largest value overall | the last row
Q: Which function writes an array to a text file? | np.savetxt() | np.loadtxt() | np.genfromtxt() | np.write()
Q: Which NumPy function gives the standard deviation of the elements of an array? | np.std() | np.sd() | np.dev() | np.var_sq()
M:function: np.mean() | average of the elements
M:function: np.std() | standard deviation
M:function: np.var() | variance
M:function: np.median() | middle value
S+: Without an axis, sum(), max(), min() and mean() work on all the elements of an array
S+: The parameter skiprows=1 is used to skip the header line of a CSV file
S+: genfromtxt() fills missing values with nan or with a value given by filling_values
S+: np.std() and np.var() divide by the number of elements n by default
S-: loadtxt() can read a file with missing values without any error | It raises an error; genfromtxt() handles missing values
S-: m.sum(axis=1) gives the sum of each column | axis=1 gives the sum of each row; axis=0 gives each column
C: A header line is skipped while loading numeric data | the header contains text that cannot be converted to numbers
C: Statistical functions on arrays need no loops | NumPy applies them to all elements at once
X: C2 D2 2 | Differentiate between loadtxt() and genfromtxt(). | Both read data from text/CSV files into arrays; loadtxt fails on missing values; genfromtxt handles missing values with nan or filling_values.
X: C3 D3 3 | Write statements to load marks.csv (with a header line and comma-separated values) into an array m and display the mean of each column. | m = np.loadtxt("marks.csv", skiprows=1, delimiter=","); print(m.mean(axis=0)).
L: D4 | Explain the statistical operations on NumPy arrays and the functions for loading and saving arrays with files. | max, min, sum, mean, median, std, var; axis 0 and 1; loadtxt with skiprows, delimiter, dtype; genfromtxt for missing values; savetxt.
"""

# ---------------------------------------------------------------- ch07 Database Concepts
TXT['db1'] = """
T: file system | a way of storing data in separate files on a storage device, each file managed by its own application program
T: data redundancy | the same data being stored in more than one place, wasting storage
T: data inconsistency | different copies of the same data not matching, because only some copies were updated
T: data isolation | data being scattered in separate files of different formats, so that it is hard to combine
T: data dependence | the situation in which a change in the structure of a file needs changes in all the programs that use it
T: database | an organised collection of logically related data stored so that it can be easily accessed and managed
T: database management system | software that is used to create, manage and access databases, such as MySQL or Oracle
T: database schema | the design or structure of a database, describing its tables, columns and their types
T: metadata | the data about data, such as the schema and constraints, stored in the data dictionary of a database
T: database instance | the state of a database at a particular moment, that is, the data stored in it at that time
Q: Storing a customer's address in two different files leads to: | data redundancy | data independence | data security | data abstraction
Q: When the address of a student is changed in one file but not in another, it causes: | data inconsistency | data isolation | data dependence | metadata
Q: Which of the following is a database management system? | MySQL | Python | Windows | Chrome
Q: The data dictionary of a DBMS stores: | metadata | only images | only programs | user passwords only
Q: The structure of a database, including its tables and columns, is called its: | schema | instance | query | record
M:file system limitation: Data redundancy | duplicate copies of data
M:file system limitation: Data inconsistency | copies do not match
M:file system limitation: Data isolation | data scattered in separate files
M:file system limitation: Data dependence | programs tied to file structure
S+: A DBMS reduces data redundancy and inconsistency
S+: A DBMS allows controlled sharing of data among many users
S+: A query is a request to retrieve or change data in a database
S+: The database instance changes whenever data is added, changed or deleted
S+: MySQL, Oracle, PostgreSQL and Microsoft Access are examples of DBMS
S-: The file system removes data redundancy | A DBMS reduces redundancy; file systems often duplicate data
S-: The schema of a database changes every time a row is added | The instance changes; the schema stays the same
C: Data inconsistency is common in a file system | the same data is kept in several files that may not all be updated
C: A DBMS gives better data security | access to data can be controlled with user permissions
X: C2 D2 2 | Differentiate between a file system and a DBMS. | File system – separate files per application, redundancy, inconsistency, no controlled sharing; DBMS – one integrated database, less redundancy, consistency, controlled access.
X: C3 D3 3 | Explain any three limitations of a file system. | Redundancy – duplicate data; inconsistency – mismatched copies; isolation – scattered files; dependence – programs tied to file format; controlled sharing difficult.
X: C3 D4 4 | A school keeps fee records and library records in separate files, and both contain student addresses. Explain the problems this can cause and how a DBMS solves them. | Same address in two files – redundancy; update in one only – inconsistency; hard to combine – isolation; DBMS – one central database, data stored once, consistent, shared with access control.
L: D4 | What is a DBMS? Explain the limitations of the file system that a DBMS overcomes, and give examples of DBMS software. | Software to create and manage databases; overcomes redundancy, inconsistency, isolation, dependence, uncontrolled sharing; schema, metadata, instance, query; MySQL, Oracle, PostgreSQL, Access.
"""

TXT['db2'] = """
T: relational data model | a model in which data is organised as a collection of related tables called relations
T: relation | a table in a relational database, made up of rows and columns
T: attribute | a column of a relation, which stores one property of the entity
T: tuple | a row of a relation, which stores the data of one entity
T: domain | the set of all values that an attribute is allowed to take
T: degree | the number of attributes (columns) in a relation
T: cardinality | the number of tuples (rows) in a relation
Q: A row of a relation is also called a: | tuple | attribute | domain | degree
Q: A column of a relation is also called an: | attribute | tuple | instance | index
Q: A relation with 5 columns and 12 rows has degree: | 5 | 12 | 17 | 60
Q: A relation with 5 columns and 12 rows has cardinality: | 12 | 5 | 17 | 60
Q: The set of allowed values of an attribute is called its: | domain | degree | tuple | key
Q: An unknown or missing value in a relation is shown as: | NULL | 0 | a blank space | -1
M:term: Attribute | column
M:term: Tuple | row
M:term: Degree | number of columns
M:term: Cardinality | number of rows
S+: Each attribute of a relation has a unique name
S+: The order of tuples in a relation does not matter
S+: No two tuples of a relation can be identical
S+: Every value in a relation is atomic, that is, it cannot be divided further
S+: NULL is used for a value that is unknown or not applicable
S-: The degree of a relation is the number of rows | Degree is the number of columns; cardinality is the number of rows
S-: Two tuples of a relation can be exactly the same | Each tuple of a relation must be distinct
C: Adding a row increases the cardinality of a relation | cardinality is the number of tuples
C: Adding a column increases the degree of a relation | degree is the number of attributes
X: C2 D2 2 | Define degree and cardinality of a relation with an example. | Degree – number of attributes; cardinality – number of tuples; a table of 4 columns and 10 rows has degree 4 and cardinality 10.
X: C3 D3 3 | Explain the terms relation, attribute, tuple and domain with an example. | Relation – STUDENT table; attribute – column such as Name; tuple – one student's row; domain – allowed values, e.g. Class XI or XII.
L: D4 | Explain the relational data model and its terms with an example, and state the properties of a relation. | Relations as tables; attribute, tuple, domain, degree, cardinality, NULL; properties – unique attribute names, order of rows/columns immaterial, distinct tuples, atomic values.
"""

TXT['db3'] = """
T: candidate key | an attribute or set of attributes that can uniquely identify each tuple of a relation
T: primary key | the candidate key chosen to uniquely identify the tuples of a relation, which cannot be NULL
T: alternate key | a candidate key that is not chosen as the primary key
T: foreign key | an attribute of one relation that refers to the primary key of another relation
T: composite primary key | a primary key made up of two or more attributes together
Q: A relation can have how many primary keys? | only one | any number | exactly two | none
Q: The candidate keys that are not chosen as the primary key are called: | alternate keys | foreign keys | composite keys | super values
Q: An attribute that refers to the primary key of another table is a: | foreign key | candidate key | alternate key | domain
Q: Which of these is the best primary key for a STUDENT table? | AdmissionNo | Name | City | Class
Q: A primary key made of more than one attribute is called a: | composite primary key | foreign key | alternate key | single key
M:key: Primary key | chosen to identify each row
M:key: Candidate key | can identify each row
M:key: Alternate key | candidate key not chosen
M:key: Foreign key | refers to another table's primary key
S+: A primary key cannot contain NULL or duplicate values
S+: Every primary key is a candidate key
S+: A foreign key links two relations
S+: The values of a foreign key must match values of the referenced primary key or be NULL
S-: A table can have more than one primary key | A table has only one primary key, which may be composite
S-: A foreign key must be unique in its own table | Foreign key values can repeat
C: Name is not chosen as the primary key of a STUDENT table | two students can have the same name
C: DeptNo in EMPLOYEE is a foreign key | it refers to the primary key DeptNo of the DEPARTMENT table
X: C2 D2 2 | Differentiate between a primary key and a foreign key. | Primary key – uniquely identifies rows of its own table, no NULL or duplicates; foreign key – refers to primary key of another table, may repeat or be NULL.
X: C3 D3 3 | Differentiate between candidate key, primary key and alternate key with an example. | Candidate – can identify rows, e.g. AdmNo, Email; primary – chosen one, AdmNo; alternate – the rest, Email.
L: D4 | Explain the different keys of a relational database with examples. | Candidate, primary (unique, not NULL, one per table), composite primary, alternate, foreign (links tables, referential integrity); examples from STUDENT and CLASS tables.
"""

# ---------------------------------------------------------------- ch08 SQL
TXT['sql1'] = """
T: SQL | Structured Query Language, the standard language used to create, access and manipulate relational databases
T: MySQL | an open-source relational database management system that uses SQL
T: CHAR(n) | the fixed-length string data type that always uses n characters of storage, with n from 0 to 255
T: VARCHAR(n) | the variable-length string data type that stores up to n characters and uses only the space needed
T: DATE | the data type that stores a date in the format 'YYYY-MM-DD'
T: constraint | a rule applied to a column to restrict the values that can be stored in it
T: NOT NULL | the constraint that ensures a column cannot have a missing value
T: UNIQUE | the constraint that ensures all the values of a column are different
T: DEFAULT | the constraint that gives a column a value when no value is supplied for it
Q: SQL keywords are: | not case-sensitive | always lower case | always upper case | case-sensitive
Q: Each SQL statement in MySQL ends with a: | semicolon | colon | full stop | comma
Q: Which data type is best for a name whose length varies? | VARCHAR | CHAR | INT | DATE
Q: In which format does MySQL store a date? | 'YYYY-MM-DD' | 'DD-MM-YYYY' | 'MM/DD/YYYY' | 'YYYY/DD/MM'
Q: Which constraint uniquely identifies each row and does not allow NULL? | PRIMARY KEY | UNIQUE | DEFAULT | NOT NULL
Q: Which data type stores numbers with a decimal point? | FLOAT | INT | CHAR | DATE
M:data type: CHAR(n) | fixed-length text
M:data type: VARCHAR(n) | variable-length text
M:data type: INT | whole numbers
M:data type: DATE | 'YYYY-MM-DD'
M:constraint: NOT NULL | value must be given
M:constraint: UNIQUE | no repeated values
M:constraint: DEFAULT | value when none is given
M:constraint: PRIMARY KEY | unique and not NULL
S+: MySQL is a free and open-source RDBMS
S+: CHAR(10) uses 10 characters of storage even for a shorter value
S+: Text and date values are written within single quotes in SQL
S+: A UNIQUE column can contain NULL values
S+: A FOREIGN KEY constraint links a column to the primary key of another table
S-: VARCHAR(n) always uses n characters of storage | VARCHAR uses only the space needed; CHAR uses fixed space
S-: A PRIMARY KEY column can contain NULL | A primary key cannot be NULL and must be unique
C: VARCHAR is preferred for storing names | names have different lengths, so space is saved
C: A PIN code is stored as CHAR(6) | it always has six characters and no arithmetic is done on it
X: C2 D2 2 | Differentiate between CHAR and VARCHAR data types. | CHAR(n) – fixed length, always n characters; VARCHAR(n) – variable length up to n, uses only the space needed.
X: C2 D2 2 | Differentiate between the PRIMARY KEY and UNIQUE constraints. | Both prevent duplicates; PRIMARY KEY does not allow NULL and only one per table; UNIQUE allows NULL and many per table.
L: D4 | Explain the data types and constraints of MySQL with examples. | CHAR, VARCHAR, INT, FLOAT, DATE; NOT NULL, UNIQUE, DEFAULT, PRIMARY KEY, FOREIGN KEY with examples; choosing types for columns.
"""

TXT['sql2'] = """
T: DDL | Data Definition Language, the SQL commands such as CREATE, ALTER and DROP that define or change the structure of database objects
T: CREATE DATABASE | the SQL command that creates a new database
T: USE | the SQL command that selects a database to work in
T: CREATE TABLE | the SQL command that creates a new table with the given columns, data types and constraints
T: DESCRIBE | the SQL command that shows the structure of a table, also written as DESC
T: ALTER TABLE | the SQL command that changes the structure of an existing table, such as adding or removing a column
T: DROP TABLE | the SQL command that removes a table along with its structure and data
Q: Which command shows the list of tables in the current database? | SHOW TABLES; | DESCRIBE; | LIST TABLES; | SELECT TABLES;
Q: Which command is used to add a column to an existing table? | ALTER TABLE | UPDATE | INSERT INTO | CREATE TABLE
Q: Which command removes a table permanently with its structure? | DROP TABLE | DELETE FROM | ALTER TABLE | REMOVE TABLE
Q: Which command displays the structure of the table STUDENT? | DESCRIBE STUDENT; | SHOW STUDENT; | SELECT STUDENT; | STRUCTURE STUDENT;
Q: Which command selects the database SCHOOL for use? | USE SCHOOL; | OPEN SCHOOL; | SELECT SCHOOL; | START SCHOOL;
M:command: CREATE TABLE | make a new table
M:command: ALTER TABLE | change a table's structure
M:command: DROP TABLE | remove a table
M:command: DESCRIBE | show a table's structure
S+: CREATE, ALTER and DROP are DDL commands
S+: ALTER TABLE ... ADD adds a new column and ALTER TABLE ... DROP removes a column
S+: ALTER TABLE ... MODIFY changes the data type of a column
S+: A primary key can be added to an existing table using ALTER TABLE ... ADD PRIMARY KEY
S+: DROP DATABASE removes a database along with all its tables
S-: DROP TABLE removes only the rows of a table | It removes the table with its structure; DELETE removes rows
S-: DESCRIBE shows the rows of a table | DESCRIBE shows the structure; SELECT shows the rows
C: ALTER TABLE is a DDL command | it changes the structure of a table, not its data
C: A database must be selected with USE before creating tables in it | MySQL needs to know which database the table belongs to
X: C2 D2 2 | Differentiate between DROP TABLE and ALTER TABLE ... DROP. | DROP TABLE removes the whole table; ALTER TABLE ... DROP removes one column from the table.
X: C3 D3 3 | Write SQL commands to (i) create a database SHOP, (ii) open it and (iii) display the tables in it. | (i) CREATE DATABASE SHOP; (ii) USE SHOP; (iii) SHOW TABLES;
"""

TXT['sql3'] = """
T: DML | Data Manipulation Language, the SQL commands such as INSERT, UPDATE and DELETE that add, change or remove data
T: INSERT INTO | the SQL command that adds new rows to a table
T: UPDATE | the SQL command that changes the values of existing rows of a table
T: DELETE | the SQL command that removes rows from a table
Q: Which command adds a new row to a table? | INSERT INTO | UPDATE | ALTER TABLE | ADD ROW
Q: Which clause of UPDATE gives the new value of a column? | SET | VALUES | WHERE | INTO
Q: DELETE FROM STUDENT; without a WHERE clause: | removes all rows but keeps the table | removes the table | gives an error | removes one row
Q: Which of these is a DML command? | UPDATE | CREATE TABLE | DROP TABLE | ALTER TABLE
Q: In INSERT INTO, text and date values are written: | within single quotes | without quotes | within brackets only | in capital letters only
M:command: INSERT INTO | adds rows
M:command: UPDATE | changes existing values
M:command: DELETE | removes rows
S+: INSERT INTO, UPDATE and DELETE are DML commands
S+: Without a WHERE clause, UPDATE changes every row of the table
S+: The values in INSERT INTO must be in the same order as the columns, unless the column names are listed
S+: DELETE removes rows but keeps the structure of the table
S-: DELETE removes the structure of the table | DELETE removes rows; DROP TABLE removes the structure
S-: UPDATE adds new rows to a table | UPDATE changes existing rows; INSERT INTO adds rows
C: A WHERE clause is used with UPDATE | otherwise every row of the table would be changed
C: The cardinality of a table falls after DELETE | DELETE removes tuples from the table
X: C2 D2 2 | Differentiate between DELETE and DROP TABLE. | DELETE – DML, removes rows, structure stays; DROP TABLE – DDL, removes the table with structure and data.
X: C3 D3 3 | Differentiate between the DDL and DML commands of SQL with two examples of each. | DDL – define or change structure, CREATE, ALTER, DROP; DML – add, change, remove data, INSERT, UPDATE, DELETE.
"""

TXT['sql4'] = """
T: SELECT | the SQL command that retrieves data from one or more tables
T: WHERE clause | the clause that gives the condition that rows must satisfy to be selected, updated or deleted
T: DISTINCT | the keyword that removes duplicate rows from the result of a SELECT query
T: ORDER BY | the clause that sorts the result of a query in ascending (ASC, the default) or descending (DESC) order
T: LIKE | the operator used with % and _ to match patterns in text
T: BETWEEN | the operator that checks whether a value lies within a range, including both end values
T: IN | the operator that checks whether a value matches any value in a list
T: alias | a temporary name given to a column in the result of a query using AS
Q: In a LIKE pattern, % stands for: | zero or more characters | exactly one character | a digit only | a space
Q: In a LIKE pattern, _ stands for: | exactly one character | zero or more characters | the end of the text | a number
Q: Which condition checks for a missing value in the column Bonus? | Bonus IS NULL | Bonus = NULL | Bonus == NULL | Bonus EMPTY
Q: The default order of ORDER BY is: | ascending | descending | random | the order of insertion
Q: Marks BETWEEN 40 AND 60 is the same as: | Marks >= 40 AND Marks <= 60 | Marks > 40 AND Marks < 60 | Marks >= 40 OR Marks <= 60 | Marks IN (40, 60)
Q: Which keyword removes duplicate values from the result? | DISTINCT | UNIQUE | ONLY | DIFFERENT
M:operator: LIKE | pattern matching
M:operator: BETWEEN | range including both ends
M:operator: IN | matches any value in a list
M:operator: IS NULL | missing value
S+: SELECT * displays all the columns of a table
S+: Arithmetic operators can be used on columns in a SELECT query, such as Salary * 12
S+: NOT IN selects rows whose value is not in the given list
S+: ORDER BY with two columns sorts by the second column when the first column values are equal
S+: Any arithmetic with NULL gives NULL
S-: BETWEEN 10 AND 20 excludes 10 and 20 | BETWEEN includes both end values
S-: A NULL value can be checked using = NULL | IS NULL must be used
C: LIKE 'A%' selects names starting with A | % matches any number of characters after A
C: Salary + Bonus gives NULL for an employee whose Bonus is NULL | any arithmetic with NULL gives NULL
X: C2 D2 2 | Differentiate between the WHERE clause and the ORDER BY clause. | WHERE selects rows that meet a condition; ORDER BY sorts the result rows in ascending or descending order.
X: C2 D2 2 | Differentiate between the IN and BETWEEN operators with examples. | IN matches values in a list, City IN ('Delhi', 'Pune'); BETWEEN matches a range including ends, Marks BETWEEN 40 AND 60.
L: D4 | Explain the SELECT command with WHERE, DISTINCT, ORDER BY and the operators IN, BETWEEN, LIKE and IS NULL, giving an example of each. | SELECT columns/*, FROM; WHERE condition; DISTINCT removes duplicates; ORDER BY ASC/DESC; IN list; BETWEEN inclusive; LIKE % _; IS NULL; aliases and arithmetic.
"""
