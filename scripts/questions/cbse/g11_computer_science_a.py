"""CBSE class 11 Computer Science (083): fact tables and families for the theory chapters
(1 Computer System, 2 Encoding Schemes and Number System, 3 Emerging Trends, 4 Introduction to Problem Solving,
11 Societal Impact), written from NCERT Computer Science class 11.

The fact text blocks (TXT) are shared with Informatics Practices class 11 (g11_informatics.py), which composes its own
subtopics from them. Computed families (conversions, Boolean logic, encodings, algorithm traces) are in
g11_computer_science_kit.py.
"""
from __future__ import annotations

from qbank import F, ar
from g12_computer_science_kit import ST
import g11_computer_science_kit as K

S = 'cbse-g11-computer-science-ch'

TXT = {}

TXT['org'] = """
T: computer | an electronic device that can be programmed to accept data (input), process it and generate results (output)
T: central processing unit | the electronic circuitry of a computer that carries out the actual processing, made up of the ALU, the control unit and registers
T: arithmetic logic unit | the part of the CPU that performs arithmetic operations and logical comparisons
T: control unit | the part of the CPU that controls the sequential execution of instructions and the flow of data inside the computer
T: registers | small, very fast storage locations inside the CPU that hold data and instructions being processed
T: system bus | the set of wires that carries data, addresses and control signals between the CPU, memory and other components
T: microprocessor | a CPU built on a single integrated circuit chip
T: input device | a device that converts data and instructions into a form the computer can process, such as a keyboard or scanner
T: output device | a device that converts processed data from the computer into a human-understandable form, such as a monitor or printer
Q: Which part of the CPU performs arithmetic and logical operations? | Arithmetic logic unit | Control unit | Registers | Cache memory
Q: Which bus carries the memory location to be read or written? | Address bus | Data bus | Control bus | USB
Q: Which of the following is an input device? | Scanner | Monitor | Printer | Speaker
Q: Which of the following is an output device? | Plotter | Microphone | Barcode reader | Keyboard
Q: The CPU fabricated on a single chip is called a: | microprocessor | microcontroller | motherboard | register
Q: Which component sends signals to coordinate the working of all other parts of the computer? | Control unit | ALU | Monitor | Hard disk
Q: Which bus can carry data in both directions between the CPU and memory? | Data bus | Address bus | Expansion slot | Serial port
M:device: Keyboard | input device
M:device: Monitor | output device
M:device: Scanner | input device
M:device: Printer | output device
M:CPU part: Arithmetic logic unit | performs calculations and comparisons
M:CPU part: Control unit | directs the sequence of operations
M:CPU part: Registers | hold data being processed inside the CPU
S+: A computer system has four main components: input devices, CPU, memory and output devices
S+: The CPU is also called the processor
S+: The system bus consists of the data bus, the address bus and the control bus
S+: The data bus is bidirectional, while the address bus carries addresses in one direction only, from the CPU
S+: Data and instructions from an input device are converted into binary form before processing
S+: Touch screens act as both input and output devices
S-: The control unit performs arithmetic calculations | The ALU performs calculations; the control unit controls the flow of operations
S-: A printer is an input device | A printer is an output device
S-: The address bus carries data in both directions | The data bus is bidirectional; the address bus is unidirectional
C: Registers are the fastest storage in a computer | they are located inside the CPU itself
C: Input devices must encode data before processing | the computer can process data only in binary form
X: C2 D2 2 | Name the three units of a CPU and state the function of any two. | ALU – arithmetic and logical operations; control unit – controls the execution of instructions and data flow; registers – hold data being processed.
X: C2 D2 2 | Differentiate between the data bus and the address bus. | Data bus carries data between components, bidirectional; address bus carries memory addresses from the CPU, unidirectional.
X: C3 D3 3 | Draw a block diagram of a computer system and explain the flow of data between its components. | Input → CPU (ALU, CU, registers) ↔ memory (primary, secondary) → output; data and instructions travel over the system bus; control signals from CU.
X: C3 D4 4 | Explain the role of the system bus. Describe its three types. | Connects CPU, memory and I/O; data bus – data, bidirectional; address bus – addresses, unidirectional; control bus – control signals such as read/write.
L: D4 | Describe the main components of a computer system and explain how data is transferred between them. | Input devices, CPU – ALU, CU, registers; primary and secondary memory; output devices; system bus – data, address, control buses; binary encoding of input.
"""

TXT['evolution'] = """
T: Pascaline | the mechanical calculator invented by Blaise Pascal that could add and subtract
T: Analytical Engine | the mechanical general-purpose computing machine designed by Charles Babbage
T: von Neumann architecture | the stored-program design in which a computer holds both data and instructions in memory
T: integrated circuit | a silicon chip on which many electronic components such as transistors are built together
Q: Who designed the Analytical Engine? | Charles Babbage | Blaise Pascal | Herman Hollerith | Alan Turing
Q: The Pascaline was invented by: | Blaise Pascal | Charles Babbage | John von Neumann | Herman Hollerith
Q: Herman Hollerith designed a machine that used punched cards for: | tabulating census data | weaving cloth | navigation | sending messages
Q: The stored-program concept, in which data and instructions are kept in memory, is linked with: | John von Neumann | Blaise Pascal | Herman Hollerith | Charles Babbage
Q: Which technology replaced vacuum tubes in computers? | Transistors | Punched cards | Relays | Valves
M:inventor: Blaise Pascal | Pascaline
M:inventor: Charles Babbage | Analytical Engine
M:inventor: Herman Hollerith | tabulating machine with punched cards
M:inventor: John von Neumann | stored-program architecture
S+: Early computing devices such as the abacus and Pascaline were mechanical
S+: Computers moved from vacuum tubes to transistors, integrated circuits and microprocessors
S+: Integrated circuits made computers smaller, cheaper and more reliable
S+: VLSI technology allows millions of transistors on a single chip
S-: The Analytical Engine was designed by Blaise Pascal | It was designed by Charles Babbage
S-: Transistors were replaced by vacuum tubes | Vacuum tubes were replaced by transistors
C: Modern computers are much smaller than early ones | integrated circuits pack millions of components on a tiny chip
C: The stored-program concept made computers general purpose | programs could be changed by loading new instructions into memory
X: C2 D2 2 | Name two early computing devices and their inventors. | Pascaline – Blaise Pascal; Analytical Engine – Charles Babbage; tabulating machine – Herman Hollerith (any two).
X: C3 D3 3 | Trace the evolution of computers from vacuum tubes to microprocessors. | Vacuum tubes – large, hot; transistors – smaller, reliable; ICs – many components on a chip; microprocessors/VLSI – CPU on a chip, personal computers.
"""

TXT['memory'] = """
T: primary memory | the main memory that the CPU accesses directly, consisting of RAM and ROM
T: RAM | random access memory, the volatile read-write memory that holds the programs and data currently in use
T: ROM | read only memory, the non-volatile memory that holds start-up instructions such as the BIOS
T: cache memory | a small, very fast memory placed between the CPU and RAM to hold frequently used data and instructions
T: secondary memory | the non-volatile storage, such as hard disks, SSDs and pen drives, that stores data permanently
T: volatile memory | memory that loses its contents when the power is switched off
T: nibble | a group of 4 bits
T: byte | a group of 8 bits
T: solid state drive | a secondary storage device that stores data on flash memory chips with no moving parts
Q: Which memory loses its contents when power is switched off? | RAM | ROM | Hard disk | Pen drive
Q: Which memory lies between the CPU and RAM and stores frequently used instructions? | Cache memory | ROM | Hard disk | Virtual memory
Q: 1 KB is equal to: | 1024 bytes | 1000 bits | 1024 bits | 1000 bytes
Q: Which of these is a secondary storage device? | Solid state drive | Cache memory | RAM | Registers
Q: The start-up instructions of a computer are stored in: | ROM | RAM | cache memory | registers
Q: Which unit comes after the terabyte (TB)? | Petabyte (PB) | Gigabyte (GB) | Exabyte (EB) | Zettabyte (ZB)
Q: Which is the fastest memory? | Registers | Cache memory | RAM | Hard disk
M:memory: RAM | volatile read-write main memory
M:memory: ROM | non-volatile memory with start-up instructions
M:memory: Cache memory | fast memory between CPU and RAM
M:memory: Hard disk | non-volatile secondary storage
M:unit: Nibble | 4 bits
M:unit: Byte | 8 bits
M:unit: Kilobyte | 1024 bytes
M:unit: Megabyte | 1024 KB
S+: RAM is volatile, while ROM is non-volatile
S+: Cache memory is faster than RAM but smaller in size
S+: Secondary memory is slower than primary memory but cheaper and larger
S+: Data must be brought into primary memory before the CPU can process it
S+: 1 MB = 1024 KB and 1 GB = 1024 MB
S+: SSDs are faster than hard disk drives because they have no moving parts
S-: ROM loses its contents when the power is switched off | ROM is non-volatile; RAM is volatile
S-: Secondary memory is faster than cache memory | Cache memory is much faster than secondary memory
S-: 1 byte is equal to 4 bits | 1 byte is 8 bits; 4 bits make a nibble
C: Computers have cache memory | the CPU is much faster than RAM, so frequently used data is kept in faster memory close to it
C: Unsaved work is lost in a power cut | RAM is volatile and loses its contents when power fails
C: Files are saved on a hard disk or SSD | secondary memory is non-volatile and keeps data permanently
X: C2 D2 2 | Differentiate between RAM and ROM. | RAM – volatile, read-write, holds current programs and data; ROM – non-volatile, read-only, holds start-up instructions.
X: C2 D2 2 | What is cache memory? Why is it used? | Small, fast memory between CPU and RAM; holds frequently used data and instructions so the CPU need not wait for slower RAM.
X: C3 D3 3 | Differentiate between primary and secondary memory on any three points. | Primary – directly accessed by CPU, faster, costlier, smaller, mostly volatile (RAM); secondary – not directly accessed, slower, cheaper, larger, non-volatile.
X: C3 D4 4 | Arrange registers, RAM, cache memory and hard disk in increasing order of speed and explain why such a memory hierarchy is used. | Hard disk < RAM < cache < registers; faster memory is costlier and smaller; hierarchy balances speed, cost and capacity.
L: D4 | Explain the types of memory in a computer system with examples, and list the units of memory. | Registers; primary – RAM, ROM, cache; secondary – HDD, SSD, CD/DVD, pen drive; volatile and non-volatile; units – bit, nibble, byte, KB, MB, GB, TB, PB, EB, ZB, YB with 1024 rule.
"""

TXT['data'] = """
T: data | raw, unorganised facts such as numbers, text, images or sounds that can be processed to get information
T: information | processed and organised data that is meaningful and useful
T: data capturing | the process of gathering data from different sources in digital form
T: data storage | the process of storing captured data so that it can be retrieved later
T: data retrieval | the process of fetching stored data when it is needed
Q: Processed and meaningful data is called: | information | raw data | a bit | a signal
Q: Filling a feedback form on a website is an example of: | data capturing | data deletion | data retrieval only | data compression
Q: Fetching a customer's record from a database when needed is called: | data retrieval | data capturing | data storage | encoding
Q: Which of the following is an example of data rather than information? | A list of marks of students | The class average of the marks | A report showing the topper | A chart of results by section
M:data process: Data capturing | gathering data in digital form
M:data process: Data storage | keeping data for later use
M:data process: Data retrieval | fetching stored data when needed
S+: Data is processed to obtain information
S+: Data can be structured, such as a table, or unstructured, such as images and videos
S+: Data is stored on storage devices such as hard disks, SSDs and cloud storage
S+: Barcode readers and sensors capture data automatically
S-: Information is raw data that has not been processed | Information is processed, meaningful data
S-: Data can be retrieved without being stored | Data must be stored before it can be retrieved
C: The marks of a class become information when the average is calculated | information is obtained by processing data
C: Supermarkets use barcode readers at billing counters | barcodes allow fast and accurate capturing of product data
X: C2 D2 2 | Differentiate between data and information with an example. | Data – raw facts, e.g. marks of students; information – processed data, e.g. class average or topper.
X: C3 D3 3 | Explain data capturing, storage and retrieval with examples. | Capturing – forms, sensors, barcode; storage – hard disk, SSD, cloud; retrieval – searching and fetching records when needed.
"""

TXT['software'] = """
T: software | a set of instructions or programs that tells the computer what to do
T: system software | software that operates and manages the computer hardware, such as the operating system and utilities
T: operating system | the system software that manages hardware and software resources and provides an interface between the user and the computer
T: utility software | system software such as disk cleanup, antivirus and backup tools that helps maintain the computer
T: device driver | system software that lets the operating system communicate with a hardware device
T: language translator | a program that converts code written in a programming language into machine language
T: compiler | a translator that converts the whole high-level program into machine code at once and reports errors after scanning the whole program
T: interpreter | a translator that converts and executes a high-level program line by line, stopping at the first error
T: assembler | a translator that converts assembly language into machine code
T: application software | software that performs specific tasks for users, such as a word processor or a billing program
T: open source software | software whose source code is available for anyone to use, modify and share
Q: Which translator converts the entire program at once? | Compiler | Interpreter | Assembler | Loader
Q: Which translator converts assembly language into machine code? | Assembler | Compiler | Interpreter | Editor
Q: Which of the following is system software? | Operating system | Spreadsheet | Web browser | Photo editor
Q: Python is usually executed by a(n): | interpreter | assembler | loader | device driver
Q: Which software lets the operating system communicate with a printer? | Device driver | Compiler | Spreadsheet | Antivirus
Q: Which of the following is an example of open source software? | LibreOffice | Microsoft Word | Adobe Photoshop | Tally
Q: An interface in which the user types commands is a: | command-based interface | graphical user interface | touch-based interface | voice-based interface
M:software: Operating system | manages hardware and provides a user interface
M:software: Antivirus | utility software
M:software: Compiler | translates the whole program at once
M:software: Word processor | application software
M:OS function: Process management | allocating the CPU to programs
M:OS function: Memory management | allocating and freeing RAM
M:OS function: File management | creating, storing and organising files
M:OS function: Device management | controlling input and output devices
S+: Software can be classified as system software, programming tools and application software
S+: The operating system acts as an interface between the user and the hardware
S+: An operating system performs process, memory, file and device management
S+: Interfaces of operating systems may be command-based, graphical, touch-based, voice-based or gesture-based
S+: An interpreter stops at the first error, while a compiler lists errors after scanning the whole program
S+: Application software may be general purpose, such as a spreadsheet, or customised, such as a school's fee software
S-: A compiler translates and executes a program line by line | An interpreter works line by line; a compiler translates the whole program
S-: An operating system is application software | An operating system is system software
S-: Open source software never allows users to modify its code | Its source code is freely available to use and modify
C: Programs written in a high-level language need a translator | the computer understands only machine language
C: A device driver is needed for a new printer | the operating system communicates with hardware through its driver
C: A program translated by a compiler runs faster than one interpreted line by line | it is translated into machine code only once before execution
X: C2 D2 2 | Differentiate between a compiler and an interpreter. | Compiler – whole program at once, errors listed after full scan, faster execution; interpreter – line by line, stops at first error.
X: C2 D2 2 | Give two examples each of system software and application software. | System – Windows, Linux, antivirus, device drivers; application – word processor, spreadsheet, web browser, billing software.
X: C3 D3 3 | Explain any three functions of an operating system. | Process management; memory management; file management; device management; user interface (any three).
X: C3 D4 4 | Explain the different types of software with examples. | System software – OS, utilities, drivers; programming tools – translators, IDE; application software – general purpose and customised; open source and proprietary.
L: D4 | What is an operating system? Explain its functions and the different types of user interfaces. | Interface between user and hardware; process, memory, file and device management; CUI, GUI, touch, voice and gesture-based interfaces.
"""

TXT['boolean'] = """
T: Boolean logic | logic in which every variable or expression takes only one of two values, 1 (true) or 0 (false)
T: logic gate | an electronic circuit that performs a basic logical operation on one or more binary inputs to give one binary output
T: NOT gate | a gate with one input that gives the opposite (complement) of the input
T: AND gate | a gate whose output is 1 only when all of its inputs are 1
T: OR gate | a gate whose output is 1 when at least one of its inputs is 1
T: NAND gate | a gate whose output is 0 only when all of its inputs are 1, the complement of AND
T: NOR gate | a gate whose output is 1 only when all of its inputs are 0, the complement of OR
T: XOR gate | a gate whose output is 1 when its two inputs are different
T: truth table | a table that shows the output of a logical expression for every possible combination of inputs
T: De Morgan's laws | the laws stating that NOT (A AND B) = (NOT A) OR (NOT B) and NOT (A OR B) = (NOT A) AND (NOT B)
Q: Which gate has only one input? | NOT | AND | OR | XOR
Q: Which gates are called universal gates? | NAND and NOR | AND and OR | XOR and NOT | AND and NOT
Q: How many rows does the truth table of an expression with three variables have? | 8 | 6 | 3 | 9
Q: Which gate gives output 1 when its two inputs are different? | XOR | AND | NOR | NAND
Q: The output of a NOR gate is 1 when: | all inputs are 0 | all inputs are 1 | inputs are different | any input is 1
Q: According to De Morgan's law, NOT (A OR B) equals: | (NOT A) AND (NOT B) | (NOT A) OR (NOT B) | A AND B | NOT A OR B
M:gate: AND | output 1 only when all inputs are 1
M:gate: OR | output 1 when any input is 1
M:gate: NAND | output 0 only when all inputs are 1
M:gate: NOR | output 1 only when all inputs are 0
M:gate: XOR | output 1 when the two inputs differ
S+: A truth table for n inputs has 2 to the power n rows
S+: NAND and NOR gates are called universal gates because any other gate can be made from them
S+: The NOT operation is also called the complement or inversion
S+: The NAND gate is an AND gate followed by a NOT gate
S+: The output of an XOR gate is 0 when both inputs are the same
S-: The output of an AND gate is 1 when any one input is 1 | An AND gate gives 1 only when all inputs are 1; that describes OR
S-: A truth table for three inputs has 6 rows | It has 2^3 = 8 rows
S-: XOR gives output 1 when both inputs are 1 | XOR gives 1 only when the inputs are different
C: NAND is called a universal gate | NOT, AND and OR can all be built using only NAND gates
C: The output of NOR is the complement of OR | NOR is an OR gate followed by a NOT gate
C: A truth table with two inputs has four rows | each input can be 0 or 1, giving 2 × 2 combinations
X: C2 D2 2 | Draw the truth table of a two-input NAND gate. | A B Y: 0 0 1; 0 1 1; 1 0 1; 1 1 0.
X: C2 D2 2 | State De Morgan's laws. | NOT (A AND B) = (NOT A) OR (NOT B); NOT (A OR B) = (NOT A) AND (NOT B).
X: C3 D3 3 | Why are NAND and NOR called universal gates? Show how a NOT gate can be made with a NAND gate. | Any gate can be built from either alone; joining both inputs of a NAND gives NOT: NAND(A, A) = NOT A.
L: D4 | Explain the basic logic gates NOT, AND, OR, NAND, NOR and XOR with their truth tables. | Symbols/meaning; truth tables for each; NAND and NOR as complements and universal gates; XOR for different inputs; examples.
"""

TXT['encoding'] = """
T: encoding | the mechanism of converting data into an equivalent cipher using a specific code, such as converting characters to binary
T: ASCII | American Standard Code for Information Interchange, a 7-bit code that represents 128 characters
T: ISCII | Indian Script Code for Information Interchange, an 8-bit code for Indian scripts
T: Unicode | the universal standard that gives a unique code to every character of every language
T: UTF-8 | a Unicode encoding that uses 1 to 4 bytes per character, with 1 byte for ASCII characters
T: UTF-32 | a Unicode encoding that uses a fixed 4 bytes (32 bits) for every character
Q: How many characters can be represented in standard 7-bit ASCII? | 128 | 256 | 64 | 1024
Q: What is the decimal ASCII code of 'A'? | 65 | 97 | 48 | 64
Q: What is the decimal ASCII code of 'a'? | 97 | 65 | 98 | 32
Q: ISCII was developed to represent: | Indian scripts | Chinese characters | only English letters | emoji
Q: Which encoding uses a fixed 4 bytes for every character? | UTF-32 | UTF-8 | ASCII | ISCII
Q: Which coding scheme can represent characters of almost all the world's languages? | Unicode | ASCII | ISCII | BCD
Q: ISCII uses how many bits per character? | 8 | 7 | 16 | 32
M:code: ASCII | 7-bit code for 128 characters
M:code: ISCII | 8-bit code for Indian scripts
M:code: UTF-8 | variable 1 to 4 bytes per character
M:code: UTF-32 | fixed 4 bytes per character
S+: Computers store characters as numbers using an encoding scheme
S+: The ASCII code of a lower-case letter is 32 more than that of the corresponding upper-case letter
S+: The first 128 Unicode code points are the same as ASCII
S+: UTF-8 is the most widely used encoding on the web
S+: The ASCII codes of the digits '0' to '9' are 48 to 57
S-: ASCII can represent the characters of all Indian languages | ASCII covers only 128 characters; Unicode covers the world's scripts
S-: UTF-8 always uses 4 bytes per character | UTF-8 uses 1 to 4 bytes; UTF-32 always uses 4 bytes
S-: The ASCII code of 'a' is 65 | The ASCII code of 'A' is 65 and of 'a' is 97
C: Unicode was developed | ASCII and ISCII could not represent the scripts of all languages in one scheme
C: UTF-8 files of English text are the same size as ASCII files | UTF-8 uses one byte for each ASCII character
C: Text typed on one computer may show as boxes on another | the two computers may use different encoding schemes or lack the fonts
X: C2 D2 2 | What is encoding? Why is Unicode needed? | Converting characters to binary codes; Unicode gives a unique code to every character of all languages, removing incompatibility between schemes.
X: C2 D2 2 | Differentiate between UTF-8 and UTF-32. | UTF-8 – variable length, 1 to 4 bytes, compact for English; UTF-32 – fixed 4 bytes per character.
X: C3 D3 3 | Compare ASCII, ISCII and Unicode. | ASCII – 7-bit, 128 English characters; ISCII – 8-bit, Indian scripts; Unicode – all languages, UTF-8/16/32 encodings.
L: D4 | Explain the need for encoding schemes. Describe ASCII, ISCII and Unicode with examples. | Computers store binary; ASCII codes (A = 65, a = 97); ISCII for Indian scripts; Unicode – UTF-8, UTF-32; compatibility; examples.
"""

TXT['numsys'] = """
T: number system | a method of representing numbers using a set of symbols (digits) and a base
T: base | the number of distinct digits used in a number system, also called the radix
T: binary number system | the base-2 number system that uses only the digits 0 and 1
T: octal number system | the base-8 number system that uses the digits 0 to 7
T: hexadecimal number system | the base-16 number system that uses the digits 0 to 9 and the letters A to F
T: positional value | the value of a digit that depends on its position, given by the base raised to the position
Q: What is the base of the hexadecimal number system? | 16 | 8 | 2 | 10
Q: Which digit is NOT used in the octal number system? | 8 | 7 | 0 | 1
Q: In hexadecimal, the letter D stands for the decimal value: | 13 | 12 | 14 | 11
Q: How many bits are needed to represent one hexadecimal digit? | 4 | 3 | 8 | 2
Q: How many bits are needed to represent one octal digit? | 3 | 4 | 2 | 8
Q: The largest digit in base 8 is: | 7 | 8 | 9 | F
M:number system: Binary | base 2, digits 0 and 1
M:number system: Octal | base 8, digits 0 to 7
M:number system: Decimal | base 10, digits 0 to 9
M:number system: Hexadecimal | base 16, digits 0 to 9 and A to F
S+: The decimal number system has base 10 and uses the digits 0 to 9
S+: Each octal digit can be written as a group of 3 bits
S+: Each hexadecimal digit can be written as a group of 4 bits
S+: Hexadecimal numbers are used for memory addresses and colour codes
S+: The positional values of the integer part of a binary number are powers of 2
S-: The hexadecimal system uses the digits 0 to 15 | It uses 0 to 9 and A to F for 10 to 15
S-: Each octal digit needs 4 bits | Each octal digit needs 3 bits; a hexadecimal digit needs 4
S-: 1010 is always a binary number | The digits 1 and 0 are valid in every base, so the base must be written
C: Computers use the binary number system | electronic circuits have two stable states, on and off
C: Hexadecimal is used for memory addresses | each hexadecimal digit stands for 4 bits, so long binary values become short
C: A number should be written with its base, such as (101)2 | the same digits stand for different values in different bases
X: C2 D2 2 | Why is the hexadecimal system used in computers? Give one use. | Each hex digit stands for 4 bits, so binary is written compactly; used in memory addresses, colour codes (#FF0000), MAC addresses.
X: C3 D3 3 | Write the positional values of the digits of (2A7)16 and find its decimal value. | 2×16² = 512; A(10)×16 = 160; 7×1 = 7; total 679.
"""

TXT['convert'] = """
T: repeated division method | the method of converting a decimal integer to another base by dividing by the base and reading the remainders from bottom to top
T: repeated multiplication method | the method of converting a decimal fraction to another base by multiplying by the base and taking the integer parts in order
Q: To convert a decimal integer to binary, we repeatedly: | divide by 2 and read the remainders from bottom to top | multiply by 2 and read the products | divide by 10 | subtract powers of 10
Q: To convert a decimal fraction to binary, we repeatedly: | multiply the fraction by 2 and take the integer parts from top to bottom | divide by 2 and read remainders | add 2 | multiply by 10
Q: To convert binary to octal, the bits are grouped in: | threes from the binary point | fours from the binary point | twos | eights
Q: To convert binary to hexadecimal, the bits are grouped in: | fours from the binary point | threes from the binary point | twos | eights
S+: Octal to hexadecimal conversion can be done through binary
S+: The decimal value of a number in any base is the sum of each digit times its positional value
S+: Some decimal fractions, such as 0.1, do not have an exact finite binary equivalent
S+: The positional values after the binary point are 2^-1, 2^-2, 2^-3 and so on
S-: In the repeated division method the remainders are read from top to bottom | They are read from the last remainder to the first (bottom to top)
S-: Every decimal fraction has an exact finite binary equivalent | Fractions such as 0.1 give a repeating binary fraction
C: The remainders are read from bottom to top in repeated division | the last remainder is the most significant digit
C: 0.5 in decimal is exactly 0.1 in binary | the first place after the binary point has the value 2^-1 = 0.5
X: C2 D2 2 | Explain the repeated division method of converting decimal to binary with an example. | Divide by 2, note remainders, read from bottom to top; e.g. 13 → 6 r1, 3 r0, 1 r1, 0 r1 → 1101.
X: C3 D3 3 | Explain how a decimal number with a fractional part is converted to binary. | Integer part by repeated division; fractional part by repeated multiplication by 2, taking integer parts in order; combine with a binary point.
"""

TXT['ai'] = """
T: artificial intelligence | the ability of a machine to imitate intelligent human behaviour such as learning, reasoning and decision making
T: machine learning | a subsystem of AI in which computers learn from data to make predictions without being explicitly programmed for each case
T: natural language processing | the area of AI that enables computers to understand and respond in human languages
T: virtual reality | a three-dimensional, computer-generated environment that a person can explore and interact with, cutting off the real world
T: augmented reality | the superimposition of computer-generated information on the user's view of the real world
T: immersive experience | an experience in which the user feels part of a computer-generated environment, as with VR and AR
Q: Which of these is an application of natural language processing? | Voice assistants answering spoken questions | Barcode scanning | Spreadsheet calculations | Disk defragmentation
Q: Superimposing digital information on the real world is called: | augmented reality | virtual reality | machine learning | big data
Q: A computer learning to recognise spam emails from examples is an example of: | machine learning | virtual reality | cloud computing | blockchain
Q: A headset that shows a fully computer-generated world is used for: | virtual reality | augmented reality | the Internet of Things | grid computing
Q: Predictive typing and spell check are applications of: | natural language processing | robotics | blockchain | IaaS
M:technology: Machine learning | learns patterns from data
M:technology: Natural language processing | understands human language
M:technology: Virtual reality | fully computer-generated 3D world
M:technology: Augmented reality | digital information over the real world
S+: Machine learning models are trained on data and then tested before use
S+: Virtual reality is used in training simulators, gaming and education
S+: Augmented reality is used in navigation apps and games that overlay information on the camera view
S+: Chatbots and voice assistants use natural language processing
S-: Augmented reality completely replaces the real world | Virtual reality replaces it; augmented reality adds information to it
S-: Machine learning needs a separate program for every new example | It learns patterns from data and generalises to new cases
C: Machine learning systems improve with more data | they learn patterns from the data they are trained on
C: Pilots train on flight simulators | virtual reality creates a safe, realistic environment for practice
X: C2 D2 2 | Differentiate between virtual reality and augmented reality with an example each. | VR – fully computer-generated environment, e.g. flight simulator; AR – digital information over the real view, e.g. navigation overlay, AR games.
X: C3 D3 3 | What is machine learning? Give two applications. | Subsystem of AI; learns from data to predict without explicit rules; e.g. spam filtering, recommendations, image recognition.
L: D4 | Explain artificial intelligence, machine learning and natural language processing with real-life applications. | Definitions; ML as part of AI, training on data; NLP – voice assistants, translation, predictive typing; immersive AR/VR.
"""

TXT['robotics'] = """
T: robot | a machine capable of carrying out one or more tasks automatically with accuracy and precision
T: drone | an unmanned aerial vehicle that can be controlled remotely or fly autonomously
T: big data | data sets that are so large and complex that traditional tools cannot process them
T: data analytics | the process of examining data sets to draw conclusions and support decisions
T: volume | the characteristic of big data that refers to its very large size
T: velocity | the characteristic of big data that refers to the high speed at which it is generated and processed
T: variety | the characteristic of big data that refers to its different forms, such as text, images and videos
T: veracity | the characteristic of big data that refers to its accuracy and trustworthiness
Q: Which characteristic of big data refers to the speed at which data is generated? | Velocity | Volume | Variety | Veracity
Q: Which characteristic of big data refers to the trustworthiness of data? | Veracity | Velocity | Volume | Value
Q: An unmanned aerial vehicle is called a: | drone | rover | humanoid | sensor
Q: The different forms of big data, such as text, audio and video, describe its: | variety | volume | velocity | veracity
Q: Robots are especially useful for tasks that are: | repetitive or dangerous for humans | always creative | purely emotional | done only once
M:big data V: Volume | huge size of data
M:big data V: Velocity | speed of data generation
M:big data V: Variety | different forms of data
M:big data V: Veracity | trustworthiness of data
M:big data V: Value | usefulness of the insight gained
S+: Robots are used in manufacturing, medicine, space exploration and defence
S+: Drones are used in agriculture, delivery, surveillance and disaster management
S+: Big data is characterised by volume, velocity, variety, veracity and value
S+: Data analytics helps businesses take decisions based on data
S+: Social media platforms generate big data every second
S-: Veracity refers to the speed of data generation | Velocity is speed; veracity is the trustworthiness of data
S-: Big data can be handled easily by ordinary spreadsheet software | Its size and complexity need special tools
C: Robots are used in car assembly lines | they do repetitive tasks quickly with accuracy and precision
C: Online shops suggest products to customers | data analytics finds patterns in big data on buying behaviour
X: C2 D2 2 | Name any four characteristics of big data. | Volume, velocity, variety, veracity, value (any four).
X: C3 D3 3 | What is a robot? Give three applications of robots. | Machine doing tasks automatically with accuracy; industry assembly, surgery, space rovers, defence, drones (any three).
L: D4 | Explain big data and its characteristics. How does data analytics help organisations? | Large complex data; 5 Vs with examples; analytics – patterns, decisions in business, health, governance.
"""

TXT['iot'] = """
T: Internet of Things | a network of devices with sensors and software that collect and exchange data over the Internet
T: Web of Things | the use of web technologies to connect IoT devices so that they can be accessed through the web
T: sensor | a device that detects changes in its surroundings, such as temperature or motion, and converts them into signals
T: smart city | a city that uses IoT, sensors and data to manage resources, traffic, energy and services efficiently
T: cloud computing | the delivery of computing services such as storage, servers and software over the Internet on demand
T: Infrastructure as a Service | the cloud service model that provides hardware such as servers, storage and networks on rent
T: Platform as a Service | the cloud service model that provides a platform with tools to develop and deploy applications
T: Software as a Service | the cloud service model in which ready-to-use software is accessed over the Internet
T: grid computing | a network of geographically spread computers that work together on a large task
Q: Using Google Docs in a browser without installing it is an example of: | Software as a Service | Infrastructure as a Service | Platform as a Service | grid computing
Q: Renting virtual servers and storage from a cloud provider is: | Infrastructure as a Service | Software as a Service | Platform as a Service | Web of Things
Q: A cloud service that gives programmers tools to build and deploy apps is: | Platform as a Service | Infrastructure as a Service | Software as a Service | a sensor
Q: A device that detects motion and turns on a light is a: | sensor | router | compiler | drone
Q: Which of the following is an example of an IoT device? | A smart watch that sends health data to a phone | A pen drive | A printed book | A calculator without connectivity
M:cloud model: IaaS | servers and storage on rent
M:cloud model: PaaS | platform to develop and deploy applications
M:cloud model: SaaS | ready software used over the Internet
S+: IoT devices collect data through sensors and share it over a network
S+: Smart cities use sensors for traffic control, waste management and street lighting
S+: Cloud computing lets users pay only for the resources they use
S+: Cloud services are commonly offered as IaaS, PaaS and SaaS
S+: Grid computing joins many computers to solve large problems together
S-: SaaS provides hardware such as servers on rent | IaaS provides hardware; SaaS provides ready software
S-: IoT devices work without collecting any data | IoT devices collect and exchange data through sensors
C: Users can open their cloud files from any device | the data is stored on remote servers accessible over the Internet
C: Smart traffic lights reduce waiting time | sensors measure traffic and adjust signals in real time
X: C2 D2 2 | Differentiate between IaaS and SaaS with an example. | IaaS – hardware (servers, storage) on rent, e.g. virtual machines; SaaS – software over the Internet, e.g. online office or email.
X: C3 D3 3 | What is a smart city? How do IoT and sensors help in it? | City using technology for services; sensors for traffic, parking, lights, waste, water, pollution; data used to manage resources.
X: C3 D4 4 | Explain cloud computing and its three service models with examples. | Services over Internet on demand; IaaS – servers; PaaS – development platform; SaaS – ready apps; pay-per-use, access anywhere.
L: D4 | Explain the Internet of Things, sensors and smart cities. | IoT definition; WoT; sensors – types and uses; smart homes, health, agriculture; smart city services; advantages and concerns.
"""

TXT['blockchain'] = """
T: blockchain | a decentralised and distributed digital ledger in which records are stored in blocks linked to each other in a chain
T: block | a unit of a blockchain that holds a set of records along with the hash of the previous block
T: distributed ledger | a shared record of transactions kept by many computers instead of a single central authority
T: hash | a unique fixed-length code generated from the data of a block, used to link blocks and detect changes
Q: In a blockchain, each block contains the hash of the: | previous block | next block | first user | central server
Q: A blockchain is maintained by: | many computers in a network | one central bank only | a single server | the operating system
Q: The best-known application of blockchain technology is: | digital currency | word processing | image editing | compiling programs
Q: Changing a record in one block of a blockchain is difficult because: | every later block's hash would change and other copies would not match | blocks are printed on paper | only one copy exists | records are encrypted with a password
S+: Blockchain removes the need for a central authority to verify transactions
S+: Each member of a blockchain network keeps a copy of the ledger
S+: Blockchain can be used for land records, healthcare data, voting and supply chains
S+: Records in a blockchain are difficult to alter once they are added
S-: A blockchain is stored on a single central computer | It is a distributed ledger kept by many computers
S-: Blocks in a blockchain are not connected to one another | Each block holds the hash of the previous block, forming a chain
C: Blockchain is considered secure | every block is linked by hashes and copies are held by many members, so tampering is detected
C: Blockchain can make land records more reliable | records cannot be altered without the agreement of the network
X: C2 D2 2 | What is blockchain? Name two applications. | Decentralised distributed ledger of linked blocks; digital currency, land records, healthcare, voting, supply chain (any two).
X: C3 D3 3 | Explain how blockchain makes records tamper-proof. | Each block has hash of previous; changing data changes hash and breaks the chain; many copies across nodes; consensus needed.
L: D4 | Explain blockchain technology and its applications. | Blocks, hashes, chain; decentralised distributed ledger; working of a transaction; uses – cryptocurrency, land records, health, voting, supply chain; advantages.
"""

TXT['steps'] = """
T: problem solving | the process of identifying a problem, developing an algorithm for it and implementing it as a program
T: algorithm | a finite sequence of clear, unambiguous steps to solve a problem
T: coding | writing the algorithm in a programming language
T: testing | checking a program with different inputs to see whether it gives the correct output
T: debugging | the process of finding and removing errors (bugs) in a program
Q: The first step in problem solving is: | analysing the problem | coding | testing | debugging
Q: Finding and removing errors from a program is called: | debugging | compiling | coding | analysing
Q: Writing an algorithm in a programming language is called: | coding | testing | decomposition | analysis
Q: Which of these is NOT a characteristic of a good algorithm? | It may run forever | It is precise | It ends after a finite number of steps | It gives output
M:step: Analysing the problem | understanding inputs and outputs
M:step: Developing an algorithm | writing the steps of the solution
M:step: Coding | converting the algorithm into a program
M:step: Testing and debugging | checking outputs and removing errors
S+: The steps of problem solving are analysing the problem, developing an algorithm, coding, and testing and debugging
S+: An algorithm must be precise, finite and must produce output
S+: A program should be tested with valid and invalid inputs
S+: The same problem can have more than one algorithm
S-: Coding is done before analysing the problem | The problem is analysed and an algorithm developed before coding
S-: An algorithm may have an unlimited number of steps | An algorithm must end after a finite number of steps
C: A problem must be analysed before writing an algorithm | the inputs, outputs and requirements must be clear to design a correct solution
C: Programs are tested with different inputs | a program may work for some inputs and fail for others
X: C2 D2 2 | List the steps of problem solving. | Analysing the problem; developing an algorithm; coding; testing and debugging.
X: C2 D2 2 | Give any four characteristics of a good algorithm. | Precision; uniqueness of steps; finiteness; input; output.
X: C3 D3 3 | Explain the importance of testing and debugging in problem solving. | Testing finds whether output is correct for varied inputs; debugging locates and fixes errors; ensures reliability.
L: D4 | Explain the steps involved in problem solving with a suitable example. | Analyse – inputs/outputs; algorithm; coding; testing and debugging; example such as finding the largest of three numbers.
"""

TXT['flowchart'] = """
T: flowchart | a visual representation of an algorithm using standard symbols connected by arrows
T: pseudocode | an informal, non-formal description of the steps of an algorithm, written in plain language with keywords
T: terminal symbol | the oval flowchart symbol used to show the start or end of an algorithm
T: process symbol | the rectangular flowchart symbol used for a calculation or an action
T: decision symbol | the diamond-shaped flowchart symbol used for a condition with yes/no outcomes
T: input/output symbol | the parallelogram flowchart symbol used for reading input or displaying output
Q: Which flowchart symbol is used for a decision? | Diamond | Rectangle | Oval | Parallelogram
Q: Which flowchart symbol shows the start or end? | Oval | Diamond | Rectangle | Circle
Q: Which flowchart symbol is used for input or output? | Parallelogram | Diamond | Oval | Rectangle
Q: In a flowchart, a calculation such as SUM = A + B is written in a: | rectangle | diamond | oval | parallelogram
M:symbol: Oval | start or stop
M:symbol: Rectangle | process or calculation
M:symbol: Diamond | decision
M:symbol: Parallelogram | input or output
M:symbol: Arrow | flow of control
S+: A flowchart uses arrows to show the order in which steps are carried out
S+: Pseudocode is not tied to any programming language
S+: Pseudocode uses keywords such as INPUT, COMPUTE, PRINT, INCREMENT, DECREMENT, IF/ELSE and WHILE
S+: A decision box has one entry and two exits
S-: A rectangle is used for decisions in a flowchart | A diamond is used for decisions; a rectangle for processes
S-: Pseudocode must follow the exact syntax of Python | Pseudocode is informal and language-independent
C: Flowcharts help to understand an algorithm easily | they show the steps visually with standard symbols
C: Pseudocode is easy to convert into a program | it is written step by step close to programming logic, without strict syntax
X: C2 D2 2 | Differentiate between a flowchart and pseudocode. | Flowchart – graphical, standard symbols and arrows; pseudocode – textual, plain language with keywords.
X: C3 D3 3 | Draw a flowchart to find whether a number is even or odd. | Start → input N → decision N MOD 2 = 0? → yes: print Even; no: print Odd → Stop.
X: C3 D4 4 | Write pseudocode and draw a flowchart to find the largest of three numbers. | INPUT A, B, C; IF A > B AND A > C PRINT A ELSE IF B > C PRINT B ELSE PRINT C; flowchart with two decision boxes.
L: D4 | Explain the representation of algorithms using flowcharts and pseudocode with an example. | Symbols – oval, rectangle, diamond, parallelogram, arrow; pseudocode keywords; example of computing average or grade.
"""

TXT['control'] = """
T: sequence | the flow of control in which statements are executed one after another in order
T: selection | the flow of control in which a condition decides which of two or more paths is followed
T: repetition | the flow of control in which a set of steps is executed again and again while a condition holds, also called iteration
T: dry run | the manual tracing of an algorithm with sample inputs to check that it is correct
Q: Executing steps one after another in order is called: | sequence | selection | repetition | decomposition
Q: Choosing between paths based on a condition is called: | selection | sequence | repetition | debugging
Q: Executing a set of steps again and again is called: | repetition | selection | sequence | testing
Q: Tracing an algorithm by hand with sample values to check it is called a: | dry run | compilation | debugging only | flowchart
M:flow: Sequence | steps one after another
M:flow: Selection | path chosen by a condition
M:flow: Repetition | steps repeated while a condition holds
S+: Every algorithm is made of sequence, selection and repetition
S+: A dry run helps find logical errors before coding
S+: Verifying an algorithm checks that it gives the correct output for all valid inputs
S+: A repetition must have a condition that eventually becomes false so that the algorithm ends
S-: Selection means repeating steps | Selection chooses a path; repetition repeats steps
S-: An algorithm verified for one input is correct for all inputs | It must be checked with different kinds of inputs, including boundary cases
C: A dry run is done before coding | it is easier to correct the logic on paper than in a program
C: A loop in an algorithm must change its condition variable | otherwise the condition never becomes false and the loop never ends
X: C2 D2 2 | Name and explain the three types of flow of control in algorithms. | Sequence – one after another; selection – path chosen by condition; repetition – steps repeated while condition holds.
X: C3 D3 3 | What is meant by verifying an algorithm? How is a dry run done? | Checking correctness for all inputs; trace each step with sample inputs in a table of variables; compare with expected output.
"""

TXT['decomp'] = """
T: decomposition | breaking a complex problem into smaller sub-problems that are easier to solve
T: time complexity | the amount of time (number of steps) an algorithm takes as the input grows
T: space complexity | the amount of memory an algorithm needs while running
Q: Breaking a large problem into smaller parts is called: | decomposition | debugging | compilation | iteration
Q: Two algorithms for the same problem are usually compared on: | time and space they need | colour of the flowchart | number of programmers | font size
Q: To check if a number n is prime, testing divisors only up to the square root of n is better because it: | needs fewer steps | needs more memory | gives wrong answers | uses more loops
Q: Designing a railway reservation system by separately planning booking, payment and cancellation is an example of: | decomposition | sequence | debugging | encoding
S+: Decomposition makes it possible for different people to work on different parts of a problem
S+: A good algorithm uses less time and less memory
S+: Algorithms are compared by counting the steps they perform for the same input
S+: Sub-problems are solved separately and then combined to solve the original problem
S-: Decomposition makes a problem harder to solve | It breaks a problem into smaller parts that are easier to solve
S-: All algorithms for a problem take the same number of steps | Different algorithms may need very different numbers of steps
C: Large software is developed by teams using decomposition | the problem is divided into modules that can be built and tested separately
C: Algorithms are compared for efficiency | different algorithms for the same task may need very different time and memory
X: C2 D2 2 | What is decomposition? Give an example. | Breaking a complex problem into smaller sub-problems; e.g. a school result system divided into data entry, calculation and report printing.
X: C3 D3 3 | Why do we compare algorithms? On what basis are they compared? | Choose the efficient one; time (number of steps) and space (memory); example of prime checking up to √n vs n − 1.
L: D4 | Explain decomposition and the comparison of algorithms with suitable examples. | Breaking into sub-problems, teamwork, reuse; comparison by time and space; prime-checking and linear search examples.
"""

TXT['footprint'] = """
T: digital footprint | the trail of data a person leaves on the Internet while using digital devices
T: active digital footprint | data that a user leaves intentionally, such as posts, emails and filled forms
T: passive digital footprint | data that is collected about a user without their direct knowledge, such as browsing history or location
T: netiquette | the code of good manners to be followed while using the Internet
T: digital society | the society in which people use digital technology for communication, learning, shopping and services
Q: Posts and comments you put on social media form your: | active digital footprint | passive digital footprint | IP address | cookie only
Q: Browsing history collected by websites without your direct action forms your: | passive digital footprint | active digital footprint | copyright | trademark
Q: Writing a whole message in capital letters online is considered: | shouting and bad netiquette | good netiquette | a copyright violation | phishing
Q: Which of the following is good netiquette? | Respecting others' privacy and opinions | Sharing others' photos without consent | Posting rude comments | Spreading unverified news
M:footprint: Active digital footprint | posts, emails and forms filled
M:footprint: Passive digital footprint | browsing history and location data
S+: Digital footprints are difficult to delete completely
S+: Netiquette includes being ethical, respectful and responsible online
S+: One should not feed the troll, that is, not respond to people who post provocative comments
S+: Email etiquette includes being precise, polite and credible
S+: Social media etiquette includes using strong passwords and thinking before uploading
S-: Digital footprints disappear once a post is deleted | Copies and records may remain on servers and other devices
S-: Using all capital letters in emails is polite | Capital letters are read as shouting
C: One should think before posting online | digital footprints are permanent and can be seen by future employers and others
C: Respecting privacy is part of netiquette | sharing others' personal information without consent can harm them
X: C2 D2 2 | Differentiate between active and passive digital footprints. | Active – data left intentionally, e.g. posts, emails; passive – collected without direct action, e.g. browsing history, cookies, location.
X: C3 D3 3 | State any three netiquettes to be followed on social media. | Be respectful; think before posting; don't share others' personal data; use strong passwords; avoid feeding trolls; verify before sharing (any three).
L: D4 | What is a digital footprint? Explain netiquette with reference to net, communication and social media etiquettes. | Active and passive footprints; permanence; be ethical, respectful, responsible; email – precise, polite, credible; social media – secure, reliable, think before uploading.
"""

TXT['ipr'] = """
T: intellectual property rights | the legal rights given to creators over the use of their creations of the mind
T: copyright | the legal right of creators of literary, artistic, musical works and software over the use and copying of their work
T: patent | the exclusive right granted to an inventor over an invention, usually for 20 years
T: trademark | a word, symbol, design or logo that identifies a brand and distinguishes it from others
T: plagiarism | presenting someone else's work or ideas as one's own without giving credit
T: licence | a legal document that states the terms under which a work or software may be used, copied or shared
T: GNU General Public License | a free software licence that lets users use, modify and share software, requiring modified versions to be shared under the same licence
T: Creative Commons | a set of licences that let creators share their works with others under chosen conditions
T: free and open source software | software that is free to use and whose source code is available to study, modify and share
Q: The right over an invention is protected by a: | patent | copyright | trademark | licence plate
Q: The logo of a company is protected as a: | trademark | patent | copyright only | GPL
Q: Copying text from a website and submitting it as your own project is: | plagiarism | patenting | licensing | trademarking
Q: Which licence is commonly used for free software? | GNU General Public License | Trademark licence | Patent licence | Proprietary EULA
Q: Which of these is an example of FOSS? | Ubuntu | Microsoft Windows | Adobe Photoshop | macOS
Q: A patent is usually granted for: | 20 years | 5 years | the creator's lifetime only | 1 year
M:IPR: Copyright | books, music and software
M:IPR: Patent | inventions
M:IPR: Trademark | brand names and logos
M:licence: GPL | free software, modified versions shared on the same terms
M:licence: Creative Commons | sharing creative works on chosen conditions
S+: Copyright protects the expression of an idea, not the idea itself
S+: Plagiarism can be avoided by giving credit to the original source
S+: Creative Commons licences let creators decide how others may use their work
S+: FOSS can be freely used, modified and distributed
S+: Using pirated software is a violation of copyright
S-: A patent protects brand names and logos | A trademark protects brand names and logos; a patent protects inventions
S-: Free software means software that can never be modified | FOSS allows users to study, modify and share it
S-: Plagiarism is allowed if the source is on the Internet | Using others' work without credit is plagiarism wherever it comes from
C: Software companies use licences | a licence states how the software may be used, copied and shared
C: Students should cite sources in projects | presenting others' work without credit is plagiarism
X: C2 D2 2 | Differentiate between copyright and patent. | Copyright – creative works like books, music, software; patent – inventions, exclusive right usually for 20 years.
X: C2 D2 2 | What is plagiarism? How can it be avoided? | Using others' work or ideas as one's own; avoid by citing sources, quoting, paraphrasing with credit.
X: C3 D3 3 | Explain GPL, Creative Commons and FOSS. | GPL – free software licence, share modifications on same terms; CC – licences for creative works with chosen conditions; FOSS – free to use with open code, e.g. Ubuntu, LibreOffice.
L: D4 | Explain intellectual property rights and the ways in which they can be violated. Describe open source licensing. | Copyright, patent, trademark; violations – plagiarism, copyright infringement, trademark infringement, piracy; licences – GPL, CC, Apache; FOSS examples.
"""

TXT['cyber'] = """
T: cyber crime | a criminal activity in which a computer or network is used as a tool or a target
T: hacking | gaining unauthorised access to a computer or network
T: ethical hacking | hacking done with permission to find and fix security weaknesses, by white hat hackers
T: phishing | a fraud in which fake emails or websites trick users into revealing passwords or bank details
T: ransomware | malware that locks or encrypts a user's data and demands payment to release it
T: cyber bullying | using digital technology to harass, threaten or humiliate a person
T: identity theft | stealing someone's personal information to impersonate them, often for financial gain
T: IT Act | the Information Technology Act, 2000 of India, amended in 2008, which deals with cyber crime and electronic commerce
T: malware | malicious software such as viruses, worms and Trojans designed to harm a computer
Q: An email that pretends to be from a bank and asks for your password is an example of: | phishing | ethical hacking | netiquette | a patent
Q: Malware that encrypts your files and demands money is: | ransomware | adware | a firewall | a cookie
Q: Hacking done with the owner's permission to find security flaws is: | ethical hacking | black hat hacking | phishing | cyber bullying
Q: The law that deals with cyber crime in India is the: | Information Technology Act, 2000 | Indian Copyright Act, 1957 | Right to Information Act, 2005 | Consumer Protection Act, 2019
Q: Posting insulting messages repeatedly about a classmate online is: | cyber bullying | phishing | plagiarism | hacking
Q: Which of these helps in safe browsing? | Checking that a site uses https before entering details | Clicking every pop-up | Using the same password everywhere | Sharing OTPs
M:cyber crime: Phishing | fake emails to steal passwords
M:cyber crime: Ransomware | data locked for a ransom
M:cyber crime: Cyber bullying | harassing a person online
M:cyber crime: Identity theft | using another person's personal details
S+: Strong passwords and two-factor authentication protect accounts
S+: Antivirus software and regular updates protect against malware
S+: Personal details and OTPs should never be shared over email or phone with strangers
S+: The IT Act, 2000 was amended in 2008
S+: Cyber crimes in India can be reported to the cyber crime cell or online portal
S-: Ethical hacking is a crime | Ethical hacking is done with permission to improve security
S-: Phishing emails always come from unknown, strange-looking addresses | They often imitate trusted banks or companies
S-: Ransomware improves the speed of a computer | Ransomware locks data and demands payment
C: Banks never ask for passwords by email | such emails are phishing attempts to steal account details
C: Regular backups protect against ransomware | data can be restored without paying the attacker
C: One should log out from shared computers | others may otherwise access the accounts and personal data
X: C2 D2 2 | What is phishing? How can one stay safe from it? | Fake emails/sites to steal details; do not click unknown links, check URL and https, never share passwords or OTPs.
X: C2 D2 2 | Differentiate between ethical and unethical hacking. | Ethical – with permission, to find and fix weaknesses (white hat); unethical – unauthorised, for harm or gain (black hat).
X: C3 D3 3 | State three measures for cyber safety. | Strong passwords; antivirus and updates; avoid unknown links and attachments; safe browsing (https); privacy settings; backups (any three).
X: C3 D4 4 | Explain any four types of cyber crime with examples. | Hacking; phishing; ransomware; cyber bullying; identity theft; meaning and example of each.
L: D4 | What is cyber crime? Describe its common forms and the measures for cyber safety, with reference to the IT Act. | Hacking, phishing, ransomware, cyber bullying, identity theft; safety – passwords, updates, antivirus, safe browsing, privacy; IT Act 2000 (amended 2008), reporting.
"""

TXT['ewaste'] = """
T: e-waste | discarded electronic devices such as computers, mobile phones and televisions
T: ergonomics | the science of designing the workplace and devices to suit users and reduce strain and injury
T: Internet addiction | a condition in which a person cannot control the use of the Internet, harming daily life and health
Q: Which harmful substance is found in e-waste? | Lead | Oxygen | Glucose | Calcium carbonate
Q: The science of designing comfortable workstations is called: | ergonomics | ecology | economics | encryption
Q: The best way to manage old but working electronic devices is to: | reuse them by donating or selling | burn them | throw them in a river | bury them in fields
Q: Looking at a screen for long hours without breaks can cause: | eye strain | better eyesight | stronger bones | fewer headaches
M:practice: Reduce | buy only what is needed and use devices longer
M:practice: Reuse | donate or sell working devices
M:practice: Recycle | recover materials through authorised recyclers
S+: E-waste contains toxic materials such as lead, mercury and cadmium
S+: E-waste should be given to authorised recyclers
S+: Reduce, reuse and recycle are the main ways of managing e-waste
S+: Sitting with a straight back and the monitor at eye level reduces strain
S+: Taking regular breaks from screens reduces eye strain
S-: Burning e-waste is a safe way to dispose of it | Burning releases toxic gases; it should go to authorised recyclers
S-: Using devices for long hours has no effect on health | It can cause eye strain, back pain and sleep problems
C: E-waste should not be thrown with household garbage | it contains toxic substances that pollute soil and water
C: Ergonomically designed chairs are recommended | they support correct posture and reduce back and neck strain
X: C2 D2 2 | What is e-waste? Why is it harmful? | Discarded electronic devices; contain lead, mercury, cadmium that pollute soil, water, air and harm health.
X: C3 D3 3 | Suggest three ways of managing e-waste. | Reduce purchases; reuse/donate working devices; recycle through authorised recyclers; take-back programmes.
X: C3 D4 4 | Explain the health concerns of using technology and how they can be reduced. | Eye strain, back and neck pain, repetitive strain, sleep problems, Internet addiction; ergonomics, breaks, posture, limits on screen time.
L: D4 | Discuss e-waste management and the health concerns related to the use of technology. | Hazards of e-waste; reduce, reuse, recycle; authorised recyclers; health – eyes, posture, RSI, addiction; ergonomics and remedies.
"""


def _fix_a(text):
    """g12_computer_science_kit.ST prefixes 'In Python, ' to statements that look like code; a statement or reason that
    starts with the article 'a' would be caught by its single-letter rule, so capitalise it first."""
    out = []
    for line in text.split('\n'):
        tag, sep, rest = line.partition(': ')
        if tag in ('S+', 'S-', 'C') and sep:
            parts = rest.split(' | ')
            parts = [('A ' + x[2:]) if x.startswith('a ') else x for x in parts]
            line = f'{tag}: ' + ' | '.join(parts)
        out.append(line)
    return '\n'.join(out)


def subs(prefix, mapping):
    """mapping: list of (subtopic suffix, topic name, [TXT keys]) -> list of Sub."""
    return [ST(prefix + suf, topic, _fix_a('\n'.join(TXT[k] for k in keys))) for suf, topic, keys in mapping]


CS_MAP = {
    1: [('01-st1', 'basic computer organisation', ['org', 'evolution']), ('01-st2', 'types of memory and units of memory', ['memory']),
        ('01-st3', 'software and operating systems', ['software']), ('01-st4', 'Boolean logic and logic gates', ['boolean'])],
    2: [('02-st1', 'encoding schemes', ['encoding']), ('02-st2', 'number systems', ['numsys']), ('02-st3', 'conversion between number systems', ['convert'])],
    3: [('03-st1', 'artificial intelligence and immersive experiences', ['ai']), ('03-st2', 'robotics, big data and data analytics', ['robotics']),
        ('03-st3', 'Internet of Things and cloud computing', ['iot']), ('03-st4', 'blockchain technology', ['blockchain'])],
    4: [('04-st1', 'steps for problem solving', ['steps']), ('04-st2', 'algorithms, flowcharts and pseudocode', ['flowchart']),
        ('04-st3', 'flow of control in algorithms and verifying algorithms', ['control']), ('04-st4', 'decomposition and comparison of algorithms', ['decomp'])],
    11: [('11-st1', 'digital footprints and netiquette', ['footprint']), ('11-st2', 'data protection and intellectual property rights', ['ipr']),
         ('11-st3', 'cyber crime and cyber safety', ['cyber']), ('11-st4', 'e-waste management and health concerns', ['ewaste'])],
}


AR_THEORY = {
    '01-st4': [('A NAND gate with both inputs joined acts as a NOT gate.', 'NAND gives 0 only when all its inputs are 1.', 'a', 'With A = B, NAND(A, A) = NOT A.'),
               ('NOT (A AND B) is equal to (NOT A) AND (NOT B).', "De Morgan's law changes AND into OR when the complement is taken.", 'd',
                'A is false: NOT (A AND B) = (NOT A) OR (NOT B); R is true.')],
    '02-st2': [('(17)8 is a valid octal number.', 'The octal number system uses the digits 0 to 7.', 'a', 'Both digits 1 and 7 are allowed in base 8.'),
               ('(129)8 is a valid octal number.', 'The octal number system uses the digits 0 to 7.', 'd', 'A is false: 9 is not an octal digit; R is true.')],
    '02-st3': [('(1111)2 is equal to (F)16.', 'Every group of four bits can be replaced by one hexadecimal digit.', 'a', '1111 = 15 = F; grouping by four explains it.'),
               ('(0.1)10 can be written exactly as a finite binary fraction.', 'Multiplying a fraction by 2 repeatedly gives its binary digits.', 'd',
                'A is false: 0.1 gives a repeating binary fraction; R is true.')],
}


def fams_theory():
    """Chapters 1-4 and 11 for Computer Science; returns (chapters, extra families)."""
    chs = [subs(S, CS_MAP[c]) for c in (1, 2, 3, 4, 11)]
    E = {}
    st = lambda x: S + x
    E[st('01-st1')] = []
    E[st('01-st2')] = [F('C2', 'D2', 'mcq', K.unit_convert), F('C3', 'D3', 'explain', K.unit_written, marks=2)]
    E[st('01-st4')] = [F('C2', 'D2', 'mcq', K.bool_eval), F('C2', 'D3', 'mcq', K.gate_identify), F('C3', 'D3', 'explain', K.gate_out, marks=2),
                       F('C3', 'D3', 'explain', K.truth_table, marks=3), F('C3', 'D4', 'mcq', K.equivalent, gap='G5'),
                       F('C4', 'D4', 'multi_step', K.demorgan_verify, marks=3), F('C4', 'D4', 'case', K.logic_case, marks=4, gap='G7'),
                       F('C3', 'D3', 'mcq', lambda r: ar(*r.choice(AR_THEORY['01-st4'])), kinds=('ar',))]
    E[st('02-st1')] = [F('C2', 'D2', 'mcq', K.ascii_code), F('C2', 'D3', 'short', K.ascii_decode, marks=1), F('C3', 'D4', 'mcq', K.utf_bytes, gap='G5')]
    E[st('02-st2')] = [F('C1', 'D1', 'mcq', K.valid_number), F('C3', 'D3', 'mcq', K.compare_bases), F('C2', 'D2', 'mcq', K.base_to_dec),
                       F('C3', 'D3', 'mcq', lambda r: ar(*r.choice(AR_THEORY['02-st2'])), kinds=('ar',)), F('C4', 'D4', 'case', K.colour_case, marks=4, gap='G7')]
    E[st('02-st3')] = [F('C2', 'D2', 'mcq', K.dec_to_base), F('C2', 'D2', 'short', K.conv_written, marks=1), F('C2', 'D3', 'mcq', K.group_conv),
                       F('C3', 'D3', 'explain', K.oct_hex, marks=2), F('C3', 'D3', 'explain', K.frac_to_bin, marks=2), F('C3', 'D4', 'mcq', K.bin_frac_to_dec),
                       F('C4', 'D4', 'multi_step', K.conv_multi, marks=3), F('C3', 'D3', 'mcq', lambda r: ar(*r.choice(AR_THEORY['02-st3'])), kinds=('ar',))]
    E[st('04-st2')] = [F('C3', 'D3', 'explain', K.pseudo_trace, marks=2), F('C3', 'D3', 'mcq', K.pseudo_trace_mcq)]
    E[st('04-st3')] = [F('C3', 'D4', 'explain', lambda r: K.pseudo_trace(r, marks=3), marks=3, gap='G5'), F('C2', 'D3', 'mcq', K.pseudo_trace_mcq)]
    E[st('04-st4')] = [F('C4', 'D4', 'explain', K.compare_algos, marks=2, gap='G5')]
    return chs, {k: v for k, v in E.items() if v}
