"""CBSE class 11 Computer Science (083): Python chapters 5-10 (Getting Started with Python, Flow of Control,
Functions, Strings, Lists, Tuples and Dictionaries).

Short fact tables (TXT, shared with Informatics Practices class 11) plus code families. Every output, exception and
program check is computed by running the code: class 11 families in g11_computer_science_kit.py, and the validated
class 12 Python-revision families of g12_computer_science_a.py (imported, not edited).
"""
from __future__ import annotations

from qbank import F, ar
from g12_computer_science_kit import ST
import g11_computer_science_kit as K
import g12_computer_science_a as G

S = 'cbse-g11-computer-science-ch'

TXT = {}

TXT['pybasics'] = """
T: Python | a high-level, interpreted, free and open-source programming language created by Guido van Rossum
T: interactive mode | the mode in which Python statements are typed at the >>> prompt and executed one at a time
T: script mode | the mode in which a Python program is saved in a file with the .py extension and then executed
T: keyword | a reserved word that has a special meaning in Python and cannot be used as an identifier
T: identifier | a name used to identify a variable, function or other object in a program
T: comment | text in a program, starting with #, that is ignored by the interpreter and explains the code
T: variable | a name that refers to a value (object) stored in memory
Q: Python was created by: | Guido van Rossum | Dennis Ritchie | James Gosling | Bjarne Stroustrup
Q: The extension of a Python script file is: | .py | .pt | .pyt | .pn
Q: Which symbol starts a single-line comment in Python? | # | // | /* | --
Q: Which mode of Python does not let you save the statements for later use? | Interactive mode | Script mode | Program mode | File mode
Q: Python is case-sensitive. This means that: | Total and total are different identifiers | keywords may be written in any case | spaces are ignored | comments are executed
Q: Which prompt is shown by Python in interactive mode? | >>> | $ | C:\\> | ###
M:mode: Interactive mode | statements executed one at a time at >>>
M:mode: Script mode | program saved in a .py file and run
S+: Python is an interpreted language
S+: Python uses indentation to define blocks of code
S+: An identifier cannot begin with a digit
S+: Keywords cannot be used as variable names
S+: Python is a case-sensitive language
S+: Python is free and open-source software
S-: Python is a compiled, low-level language | Python is a high-level, interpreted language
S-: An identifier may contain spaces | Identifiers can contain only letters, digits and underscores, with no spaces
S-: Comments in Python are executed by the interpreter | Comments are ignored by the interpreter
C: The name 2total gives a syntax error | an identifier cannot begin with a digit
C: Programs are written in script mode for later use | statements typed in interactive mode are not saved
C: The word for cannot be used as a variable name | the word for is a keyword reserved by Python
X: C2 D2 2 | Differentiate between interactive mode and script mode in Python. | Interactive – one statement at a time at >>>, not saved; script – program saved in a .py file and run as a whole.
X: C2 D2 2 | State any four rules for naming identifiers in Python. | Letters, digits, underscore only; cannot start with a digit; cannot be a keyword; case-sensitive; no special symbols or spaces.
X: C3 D3 3 | Give any three features of Python. | High-level; interpreted; free and open source; easy syntax; case-sensitive; uses indentation; portable; rich library (any three).
"""

TXT['pytypes'] = """
T: data type | the kind of value a variable holds, which decides the operations that can be done on it
T: int | the data type for whole numbers, positive or negative, without a decimal point
T: float | the data type for real numbers with a decimal point
T: complex | the data type for numbers with a real and an imaginary part, written as a + bj
T: bool | the data type with only two values, True and False
T: sequence | an ordered collection of items indexed by integers, such as a string, list or tuple
T: mutable data type | a data type whose values can be changed in place, such as a list or dictionary
T: immutable data type | a data type whose values cannot be changed in place, such as int, float, str or tuple
T: None | a special data type with a single value None, which means no value
Q: Which of the following is a mutable data type? | list | tuple | str | int
Q: Which of the following is an immutable data type? | tuple | list | dict | set of list items
Q: The data type of the value 3 + 4j is: | complex | float | int | str
Q: Which function returns the data type of a value? | type() | id() | int() | data()
Q: The bool data type has the values: | True and False | 0 to 9 | yes and no | on only
Q: A dictionary in Python is a collection of: | key-value pairs | only numbers | ordered characters | fixed constants
M:type: int | whole numbers such as -7 and 25
M:type: float | real numbers such as 3.14
M:type: str | text such as "India"
M:type: list | ordered mutable sequence in square brackets
M:type: tuple | ordered immutable sequence in parentheses
M:type: dict | key-value pairs in curly brackets
S+: Strings, lists and tuples are sequence data types
S+: The keys of a dictionary must be unique
S+: Lists and dictionaries are mutable, while strings and tuples are immutable
S+: The bool type is a subtype of int, with True equal to 1 and False equal to 0
S+: The value None represents the absence of a value
S-: A tuple is a mutable data type | A tuple is immutable; a list is mutable
S-: Strings can be changed in place by assigning to an index | Strings are immutable; a new string must be created
S-: 3.0 is of type int | 3.0 is of type float
C: A tuple cannot be changed after it is created | tuples are immutable
C: A list can be changed using append() | lists are mutable
C: True + True gives 2 | bool is a subtype of int with True equal to 1
X: C2 D2 2 | Differentiate between mutable and immutable data types with examples. | Mutable – can be changed in place, e.g. list, dict; immutable – cannot be changed in place, e.g. int, float, str, tuple.
X: C2 D2 2 | Name the data types of: (i) 7.5 (ii) "7" (iii) [7] (iv) (7,). | (i) float (ii) str (iii) list (iv) tuple.
X: C3 D3 3 | Explain the sequence data types of Python with examples. | String – "abc", immutable; list – [1, 2], mutable; tuple – (1, 2), immutable; ordered and indexed.
L: D4 | Explain the different data types of Python with examples, and classify them as mutable or immutable. | Numbers – int, float, complex, bool; sequences – str, list, tuple; mapping – dict; None; mutable – list, dict; immutable – numbers, str, tuple.
"""

TXT['pyops'] = """
T: operator | a symbol that performs an operation on one or more operands
T: floor division | the // operator, which divides and gives the integer part of the quotient (rounded down)
T: modulus | the % operator, which gives the remainder of a division
T: exponent operator | the ** operator, which raises a number to a power
T: relational operator | an operator such as ==, !=, >, <, >= or <= that compares two values and gives True or False
T: logical operator | the operators and, or and not, which combine or invert conditions
T: identity operator | the operators is and is not, which check whether two names refer to the same object
T: membership operator | the operators in and not in, which check whether a value is present in a sequence
T: operator precedence | the order in which operators are evaluated in an expression
Q: Which operator has the highest precedence in Python? | ** | * | + | and
Q: The value of 17 // 5 is: | 3 | 3.4 | 2 | 4
Q: The value of 17 % 5 is: | 2 | 3 | 3.4 | 5
Q: Which operator checks whether two variables refer to the same object? | is | == | in | =
Q: Which of these is a membership operator? | in | is | and | ==
Q: In the expression 2 + 3 * 4, which operation is done first? | multiplication | addition | both together | the one on the left
Q: The ** operator is evaluated: | from right to left | from left to right | in random order | only once
M:operator: // | floor division
M:operator: % | remainder
M:operator: ** | exponent
M:operator: in | membership test
M:operator: is | identity test
S+: The / operator always gives a float result in Python 3
S+: Among logical operators, not has the highest precedence, then and, then or
S+: Relational operators give a Boolean result
S+: The assignment x += 3 is the same as x = x + 3
S+: Parentheses can be used to change the order of evaluation
S-: The = operator is used to compare two values | = is assignment; == compares values
S-: The value of 7 / 2 is 3 in Python 3 | 7 / 2 gives 3.5; 7 // 2 gives 3
S-: The or operator has higher precedence than and | The and operator has higher precedence than or
C: 2 ** 3 ** 2 gives 512 | the exponent operator is evaluated from right to left
C: 10 / 5 gives 2.0 | the / operator always returns a float
C: "a" in "Python" gives False | membership is case-sensitive and checks the characters of the string
X: C2 D2 2 | Differentiate between / and // operators with an example. | / gives true division as float, 7 / 2 = 3.5; // gives floor division, 7 // 2 = 3.
X: C2 D2 2 | Differentiate between == and is operators. | == compares values; is checks whether two names refer to the same object in memory.
X: C3 D3 3 | Explain arithmetic, relational and logical operators with one example each. | Arithmetic +, -, *, /, //, %, **; relational ==, !=, <, >; logical and, or, not; examples.
L: D4 | Explain the types of operators in Python with examples and describe operator precedence. | Arithmetic, relational, assignment, logical, identity, membership; precedence – **, unary, * / // %, + -, relational, not, and, or.
"""

TXT['pyio'] = """
T: input() | the built-in function that reads a line typed by the user and returns it as a string
T: print() | the built-in function that displays values on the screen, separated by sep and followed by end
T: explicit type conversion | conversion done by the programmer using functions such as int(), float() and str(), also called type casting
T: implicit type conversion | conversion done automatically by Python, such as converting an int to float in 3 + 2.5
Q: The input() function always returns a value of type: | str | int | float | bool
Q: Which function converts the string "45" into a number? | int() | str() | chr() | input()
Q: What is the default value of the end parameter of print()? | a newline | a space | a comma | nothing
Q: What is the default value of the sep parameter of print()? | a space | a newline | a comma | a tab
Q: The result of 3 + 2.5 is of type float because of: | implicit type conversion | explicit type conversion | a syntax error | string concatenation
M:conversion: int("12") | explicit conversion to int
M:conversion: str(25) | explicit conversion to str
M:conversion: 3 + 2.0 | implicit conversion to float
S+: Values read with input() must be converted with int() or float() before arithmetic
S+: int() drops the fractional part of a float, as in int(7.9) which gives 7
S+: int("abc") raises a ValueError
S+: In implicit conversion, the smaller type is converted to the larger type to avoid loss of data
S-: input() returns an integer when the user types digits | input() always returns a string
S-: int(7.9) gives 8 | int() truncates the fractional part, giving 7
C: input("Age: ") + 1 gives an error | input() returns a string, which cannot be added to an integer
C: float(5) gives 5.0 | float() converts the integer to a real number
X: C2 D2 2 | Differentiate between implicit and explicit type conversion with examples. | Implicit – by Python automatically, e.g. 3 + 2.5 = 5.5; explicit – by programmer, e.g. int("12"), float(4).
X: C3 D3 3 | Write a program to input the length and breadth of a rectangle and display its area and perimeter. | l = float(input()); b = float(input()); print("Area", l * b); print("Perimeter", 2 * (l + b)).
"""

TXT['pyerrors'] = """
T: syntax error | an error caused by breaking the grammar rules of Python, reported before the program runs
T: logical error | an error in the logic of a program that gives a wrong output without any error message
T: runtime error | an error that occurs while the program is running and stops it abnormally, such as division by zero
T: debugging | the process of identifying and removing errors from a program
Q: A missing colon after an if condition causes a: | syntax error | logical error | runtime error | no error
Q: Dividing a number by zero while the program runs causes a: | runtime error | syntax error | logical error | compile warning
Q: A program to find the average prints (a + b / 2) instead of ((a + b) / 2). This is a: | logical error | syntax error | runtime error | type error message
Q: Which type of error is the hardest to detect? | Logical error | Syntax error | Runtime error with a message | Indentation error
S+: Syntax errors must be corrected before the program can run
S+: A logical error does not stop the program but gives incorrect results
S+: Runtime errors are also called exceptions
S+: Testing with known inputs and outputs helps detect logical errors
S-: A logical error stops the program with an error message | A logical error gives a wrong output without any message
S-: Syntax errors appear only after the program has produced some output | They are reported before the program begins to run
C: Logical errors are difficult to find | the program runs normally and shows no error message
C: print(10 / 0) stops the program | division by zero is a runtime error
X: C2 D2 2 | Differentiate between a syntax error and a logical error with examples. | Syntax – grammar rule broken, e.g. missing colon, program does not run; logical – wrong logic, e.g. a + b / 2 for average, wrong output.
X: C3 D3 3 | Explain the three types of errors in Python with an example of each. | Syntax – missing bracket; logical – wrong formula; runtime – division by zero or int("abc").
"""

TXT['pyif'] = """
T: if statement | a statement that executes a block only when a condition is True
T: if-else statement | a statement that executes one block when a condition is True and another when it is False
T: if-elif-else statement | a statement that checks several conditions in order and executes the block of the first True condition
T: indentation | the leading spaces at the start of a line, which Python uses to group statements into a block
T: nested if | an if statement placed inside another if or else block
Q: Which keyword is used to check another condition when the first if condition is False? | elif | else if | elseif | then
Q: In Python, a block of statements is marked by: | indentation | curly braces | the keyword end | semicolons
Q: How many blocks of an if-elif-else ladder are executed at most? | one | all whose conditions are True | two | none
Q: What does the following print? x = 5; print("big" if x > 3 else "small") | big | small | True | 5
S+: In an if-elif-else ladder, only the first True condition's block is executed
S+: The else block is optional
S+: Each statement in a block must have the same indentation
S+: A condition is any expression that evaluates to True or False
S-: All blocks whose conditions are True are executed in an if-elif ladder | Only the first True block runs
S-: Python uses curly braces to mark blocks | Python uses indentation
C: The statement after an if must be indented | Python uses indentation to identify the block belonging to the if
C: In a grading program the highest grade condition is checked first | the ladder stops at the first True condition
X: C2 D2 2 | Differentiate between if-else and if-elif-else with an example. | if-else – two paths; if-elif-else – several conditions checked in order, e.g. grading.
X: C3 D3 3 | Write a program to input a number and print whether it is positive, negative or zero. | n = int(input()); if n > 0: print("Positive") elif n < 0: print("Negative") else: print("Zero").
"""

TXT['pyloops'] = """
T: loop | a statement that repeats a block of code
T: for loop | a loop that iterates over the items of a sequence or a range of numbers
T: while loop | a loop that repeats a block as long as its condition is True
T: range() | the built-in function that generates a sequence of integers from start up to (but not including) stop, in steps
T: infinite loop | a loop whose condition never becomes False, so it never ends
Q: What does range(5) generate? | 0, 1, 2, 3, 4 | 1, 2, 3, 4, 5 | 0, 1, 2, 3, 4, 5 | 5 only
Q: What does range(2, 11, 3) generate? | 2, 5, 8 | 2, 5, 8, 11 | 3, 6, 9 | 2, 4, 6, 8, 10
Q: Which loop is best when the number of iterations is not known in advance? | while loop | for loop with range() | nested for loop | none
Q: The default step value of range() is: | 1 | 0 | 2 | -1
Q: How many times does for i in range(1, 10, 2): run? | 5 | 4 | 9 | 10
S+: The stop value of range() is not included
S+: A while loop checks its condition before each iteration
S+: A for loop can iterate over strings, lists and tuples directly
S+: range() with a negative step counts downwards
S-: range(1, 5) includes the number 5 | The stop value is excluded: 1, 2, 3, 4
S-: A while loop always runs at least once | Its body is skipped if the condition is False at the start
C: A while loop must change its condition variable | otherwise the loop never ends
C: for i in range(10, 0, -2) prints 10 8 6 4 2 | a negative step counts down and stops before 0
X: C2 D2 2 | Differentiate between for and while loops. | for – iterates over a sequence/range, count known; while – repeats while a condition is True, count may be unknown.
X: C3 D3 3 | Explain range() with its three parameters, giving examples. | range(stop) from 0; range(start, stop); range(start, stop, step); stop excluded; negative step.
"""

TXT['pybreak'] = """
T: break | the statement that ends the loop immediately and passes control to the statement after the loop
T: continue | the statement that skips the remaining statements of the current iteration and moves to the next iteration
T: pass | a null statement that does nothing, used where a statement is required syntactically
Q: Which statement terminates a loop immediately? | break | continue | pass | exit
Q: Which statement skips the rest of the current iteration? | continue | break | pass | return
Q: Which statement does nothing and is used as a placeholder? | pass | continue | break | None
S+: The break statement can be used inside both for and while loops
S+: After continue, the loop condition is checked again in a while loop
S+: In nested loops, break ends only the innermost loop in which it appears
S-: The continue statement ends the loop completely | The continue statement skips only the current iteration; break ends the loop
S-: The break statement ends all the loops in a nested loop | It ends only the innermost loop containing it
C: A search loop uses break once the item is found | there is no need to check the remaining items
C: The continue statement is used to skip unwanted values in a loop | it moves control to the next iteration without running the rest of the body
X: C2 D2 2 | Differentiate between break and continue with an example. | break exits loop, e.g. stops at first multiple of 5; continue skips iteration, e.g. prints all except multiples of 5.
"""

TXT['pynested'] = """
T: nested loop | a loop placed inside the body of another loop
Q: In a nested loop, the inner loop runs completely for: | each iteration of the outer loop | only the first outer iteration | the last outer iteration | none of the iterations
Q: If the outer loop runs 4 times and the inner loop runs 3 times for each, the inner body runs: | 12 times | 7 times | 4 times | 3 times
Q: To print a triangle of stars with rows 1 to n, the inner loop usually depends on: | the outer loop variable | a random number | the input() function | nothing
S+: In nested loops the inner loop completes all its iterations for every iteration of the outer loop
S+: print() with end="" keeps the output on the same line
S+: Patterns are printed with the outer loop for rows and the inner loop for columns
S-: The outer loop runs completely for each iteration of the inner loop | The inner loop runs completely for each outer iteration
C: print() is called after the inner loop in pattern programs | it moves the output to the next line after each row
C: A 5 × 5 table needs 25 inner iterations | the inner loop runs 5 times for each of the 5 outer iterations
X: C2 D2 2 | What is a nested loop? How many times will the inner statement run in for i in range(3): for j in range(4)? | A loop inside another loop; 3 × 4 = 12 times.
"""

TXT['fndef'] = """
T: function | a named group of statements that performs a specific task and runs when it is called
T: user-defined function | a function created by the programmer using the def keyword
T: parameter | a variable in the function header that receives a value when the function is called
T: argument | a value passed to a function when it is called
T: default parameter | a parameter that is given a default value in the function header, used when no argument is passed
T: modular programming | dividing a program into separate functions (modules), each doing one task
Q: Which keyword is used to define a function in Python? | def | function | define | fun
Q: Values passed to a function when it is called are called: | arguments | parameters only | keywords | return values
Q: In def f(a, b=5):, b is a: | default parameter | keyword | global variable | return value
Q: Which of these is a valid function header? | def area(l, b=2): | def area(l=2, b): | def area[l, b]: | define area(l, b):
Q: Which of the following is an advantage of using functions? | The same code can be reused many times | Programs become longer | Variables cannot be used | Loops are not needed
S+: A function must be defined before it is called
S+: A default parameter must come after all the parameters without default values
S+: Functions increase reusability and make programs easier to read and test
S+: The function header ends with a colon and the body is indented
S-: A parameter with a default value can come before one without a default | Default parameters must come after non-default ones
S-: A function runs automatically when it is defined | It runs only when it is called
C: Functions reduce the length of programs | code written once in a function can be called many times
C: def f(a=1, b): gives a syntax error | a non-default parameter cannot follow a default parameter
X: C2 D2 2 | Differentiate between a parameter and an argument. | Parameter – variable in function header; argument – actual value passed in the call.
X: C2 D2 2 | Give any two advantages of using functions. | Reusability; modularity; easier testing and debugging; shorter programs; readability (any two).
X: C3 D3 3 | Write a function area(r) that returns the area of a circle, and call it for r = 7. | def area(r): return 3.14 * r * r; print(area(7)) gives 153.86.
"""

TXT['fnreturn'] = """
T: return statement | the statement that ends a function and sends a value back to the caller
T: flow of execution | the order in which statements are executed, which jumps into a function when it is called and returns after it ends
T: void function | a function that does not return a value; it returns None
Q: A function without a return statement returns: | None | 0 | an empty string | False
Q: Which statement sends a value back from a function? | return | print | yield back | send
Q: A function can return several values as a: | tuple | single integer only | keyword | comment
Q: When a function is called, control: | jumps to the function body and comes back after it ends | stays at the call | goes to the end of the program | restarts the program
S+: A return statement ends the function immediately
S+: Statements after a return statement inside the same block are not executed
S+: A function may have more than one return statement
S+: Multiple values returned by a function are packed into a tuple
S-: A function can return only one value | It can return several values packed as a tuple
S-: print() and return do the same thing | print() displays a value; return sends it back to the caller
C: x = f() gives None when f has no return statement | a function without return returns None
C: Statements after return are never executed | the return statement passes control back to the caller at once
X: C2 D2 2 | Differentiate between print() and return in a function. | print displays a value on screen; return sends value to caller for further use and ends the function.
"""

TXT['fnscope'] = """
T: scope | the part of a program in which a variable is accessible
T: local variable | a variable created inside a function, accessible only within that function
T: global variable | a variable created outside all functions, accessible throughout the program
T: global keyword | the keyword used inside a function to change a global variable
Q: A variable defined inside a function is a: | local variable | global variable | keyword | parameter of all functions
Q: Which keyword lets a function modify a global variable? | global | nonlocal only | static | extern
Q: A local variable exists: | only while the function runs | throughout the program | only before the function is called | in every module
S+: A global variable can be read inside a function without the global keyword
S+: Assigning to a variable inside a function makes it local unless it is declared global
S+: A local variable with the same name as a global variable hides the global one inside the function
S-: Local variables can be used anywhere in the program | They exist only inside their function
S-: The global keyword is needed to read a global variable | It is needed only to assign to it
C: A variable created inside a function cannot be printed outside it | its scope is local to the function
C: Changing x inside a function without global x does not change the global x | the assignment creates a new local variable
X: C2 D2 2 | Differentiate between local and global variables with an example. | Local – inside function, used only there; global – outside functions, usable throughout; example.
"""

TXT['fnbuiltin'] = """
T: built-in function | a function that is always available in Python, such as len(), print(), input() and abs()
T: module | a file containing Python definitions and functions that can be imported into a program
T: math module | the standard module with mathematical functions such as sqrt(), ceil(), floor() and pow()
T: random module | the standard module used to generate random numbers, with functions such as random(), randint() and randrange()
T: statistics module | the standard module with functions such as mean(), median() and mode()
Q: Which statement imports the math module? | import math | include math | using math | #include <math>
Q: Which function returns a random integer between a and b, both included? | random.randint(a, b) | random.random() | random.randrange(a, b) | math.rand(a, b)
Q: math.ceil(4.2) returns: | 5 | 4 | 4.0 | 4.2
Q: math.floor(-2.5) returns: | -3 | -2 | -2.5 | 3
Q: Which function returns the middle value of sorted data? | statistics.median() | statistics.mean() | statistics.mode() | math.middle()
Q: random.random() returns a value: | from 0.0 up to but not including 1.0 | from 1 to 10 | from 0 to 100 | exactly 0 or 1
M:function: math.sqrt() | square root
M:function: math.ceil() | smallest integer not less than x
M:function: math.floor() | largest integer not greater than x
M:function: random.randint() | random integer in a closed range
M:function: statistics.mode() | most frequent value
S+: Functions of a module are used with the module name, as in math.sqrt(16)
S+: from math import sqrt allows sqrt() to be used without the module name
S+: math.sqrt() returns a float
S+: random.randrange(1, 10) never returns 10
S-: random.randint(1, 6) can never return 6 | random.randint() includes both end points, so 6 is possible
S-: math.floor(4.7) returns 5 | math.floor(4.7) gives 4, while math.ceil(4.7) gives 5
C: math.sqrt(25) gives 5.0 | sqrt() always returns a float
C: A dice simulation uses random.randint(1, 6) | random.randint() returns an integer in the closed range 1 to 6
X: C2 D2 2 | Differentiate between random.randint() and random.randrange(). | randint(a, b) includes both a and b; randrange(a, b) excludes b and can take a step.
X: C3 D3 3 | Name the module and write the output: (i) sqrt(81) (ii) ceil(3.01) (iii) mean([2, 4, 6]). | math – 9.0; math – 4; statistics – 4.
"""

TXT['strops'] = """
T: string | an immutable sequence of characters enclosed in single, double or triple quotes
T: indexing | accessing a single item of a sequence by its position, starting from 0 (or -1 from the end)
T: slicing | extracting part of a sequence with the [start:stop:step] notation, where stop is excluded
T: concatenation | joining two strings (or lists or tuples) using the + operator
T: repetition | repeating a string (or list or tuple) a number of times using the * operator
Q: If s = "PYTHON", what is s[-1]? | N | P | O | Error
Q: If s = "PYTHON", what is s[1:4]? | YTH | YTHO | PYT | THO
Q: What is "ab" * 3? | ababab | ab3 | aaabbb | Error
Q: What is the index of the first character of a string? | 0 | 1 | -1 | None
Q: If s = "CBSE", what does s[::-1] give? | ESBC | CBSE | EBSC | Error
S+: Strings are immutable, so their characters cannot be changed in place
S+: Negative indexes count from the end of the string
S+: An index outside the range of a string gives IndexError, but slicing never does
S+: The in operator checks whether a substring is present in a string
S-: s[0] = "J" changes the first character of the string s | Strings are immutable; this raises TypeError
S-: Slicing with an index beyond the length raises IndexError | Slicing handles out-of-range indexes without error
C: s[10] gives an error for s = "Hello" while s[2:10] does not | indexing needs a valid position but slicing stops at the end of the string
C: "Py" + "thon" gives "Python" | + concatenates strings
X: C2 D2 2 | If s = "INFORMATICS", write the output of s[2:6] and s[-4:]. | ORMA and TICS.
"""

TXT['strtrav'] = """
T: traversing a string | accessing each character of a string one by one, usually with a loop
Q: Which loop header visits each character of a string s? | for ch in s: | for ch in range(s): | while ch in s: | for s in ch:
Q: Which expression gives the number of characters in a string s? | len(s) | s.len() | count(s) | size(s)
Q: To visit the characters of s with their positions, we can use: | for i in range(len(s)): | for i in s.range(): | for i in len(s): | while s:
S+: A string can be traversed using a for loop or a while loop with an index
S+: len() gives the number of characters, including spaces
S+: The last index of a string s is len(s) - 1
S-: The last index of a string s is len(s) | The last index is len(s) - 1
C: A loop header such as for i in range(len(s)) traverses a string by index | range(len(s)) gives the positions 0 to len(s) - 1
X: C2 D2 2 | Write two ways of traversing a string s. | for ch in s: print(ch); for i in range(len(s)): print(s[i]).
"""

TXT['strmeth'] = """
T: string method | a built-in function attached to string objects, called as s.method(), that returns a new value
T: split() | the method that breaks a string into a list of words, using a separator (space by default)
T: join() | the method that joins the items of a sequence of strings into one string using the given separator
T: find() | the method that returns the lowest index of a substring, or -1 if it is not found
T: strip() | the method that removes leading and trailing spaces (or given characters) from a string
Q: What does "hello world".split() return? | ['hello', 'world'] | ['hello world'] | ('hello', 'world') | hello, world
Q: What does "banana".count("a") return? | 3 | 2 | 1 | 6
Q: What does "banana".find("x") return? | -1 | 0 | None | Error
Q: What does "-".join(["a", "b", "c"]) return? | a-b-c | -a-b-c | abc- | ['a-b-c']
Q: Which method returns True if all characters of a string are digits? | isdigit() | isalpha() | isnumber() | digit()
Q: What does "  CS  ".strip() return? | CS | "  CS" | "CS  " | Error
M:method: upper() | converts to capital letters
M:method: lower() | converts to small letters
M:method: split() | breaks a string into a list
M:method: replace() | substitutes one substring by another
M:method: find() | gives the index of a substring or -1
S+: String methods return new strings and do not change the original string
S+: index() raises ValueError when the substring is not found, while find() returns -1
S+: split() without an argument splits on spaces
S+: isalpha() returns False if a string contains a space or digit
S-: s.upper() changes the string s itself | It returns a new string; s is unchanged
S-: find() raises an error when the substring is not found | find() returns -1; index() raises ValueError
C: s.upper() does not change s | strings are immutable, so methods return new strings
C: "a,b,c".split(",") gives ['a', 'b', 'c'] | split() breaks the string at each separator and returns a list
X: C2 D2 2 | Differentiate between find() and index() methods of strings. | Both give the first index of a substring; find() returns -1 if absent, index() raises ValueError.
X: C3 D3 3 | Write the output: s = "Save Water"; print(s.lower(), s.count("a"), s.split()). | save water 3 ['Save', 'Water'].
"""

TXT['strprog'] = """
T: palindrome | a string that reads the same forwards and backwards, such as "madam"
Q: Which expression checks whether a string s is a palindrome? | s == s[::-1] | s == s[-1] | s.reverse() | s == reversed
Q: Which loop correctly counts vowels in s? | for ch in s: if ch in "aeiouAEIOU": c += 1 | for ch in s: c = c + 1 | for i in s: if i == "a": break | while s: c += 1
S+: s[::-1] gives the reverse of a string s
S+: A palindrome check should usually ignore the case of letters, as in s.lower()
S+: Counting characters of a type uses a counter that is increased inside a loop
S-: "Madam" == "Madam"[::-1] gives True | It gives False because "madaM" differs in case; use lower()
C: "Level" is not found to be a palindrome by s == s[::-1] | the comparison is case-sensitive
X: C3 D3 3 | Write a program to count the number of words in a sentence that begin with a vowel. | s = input(); c = 0; for w in s.split(): if w[0] in "aeiouAEIOU": c += 1; print(c).
"""

TXT['listops'] = """
T: list | an ordered, mutable sequence of items of any type, enclosed in square brackets
T: mutability of lists | the property that list items can be changed, added or removed after the list is created
Q: Which of these creates an empty list? | [] | () | {} | ''
Q: If L = [10, 20, 30, 40], what is L[-2]? | 30 | 20 | 40 | Error
Q: What is [1, 2] + [3]? | [1, 2, 3] | [4, 2] | [1, 2, [3]] | Error
Q: What is [0] * 3? | [0, 0, 0] | [0] | 0 | [3]
Q: If L = [5, 6, 7], what does 6 in L give? | True | False | 1 | 6
S+: Lists can contain items of different data types
S+: Lists are mutable, so an item can be changed by assigning to its index
S+: Slicing a list gives a new list
S+: A list can contain another list as an item
S-: Lists are immutable | Lists are mutable; tuples are immutable
S-: Items of a list must all be of the same type | A list can mix data types
C: L[0] = 99 changes the list L | lists are mutable
C: L[1:3] gives a new list | slicing returns a new list containing the selected items
X: C2 D2 2 | Differentiate between a list and a string with respect to mutability. | List – mutable, items can be changed; string – immutable, characters cannot be changed in place.
"""

TXT['listmeth'] = """
T: append() | the list method that adds one item at the end of a list
T: extend() | the list method that adds all the items of another sequence at the end of a list
T: insert() | the list method that adds an item at a given index
T: pop() | the list method that removes and returns the item at a given index (the last item by default)
T: remove() | the list method that removes the first occurrence of a given value
T: sort() | the list method that arranges the items of a list in order, in place
Q: Which method adds a single element at the end of a list? | append() | extend() | insert() | add()
Q: Which method removes and returns the last element of a list? | pop() | remove() | del | clear()
Q: L.sort() returns: | None | the sorted list | a new list | True
Q: Which function returns a new sorted list without changing the original? | sorted() | sort() | order() | arrange()
Q: Which method removes an element by its value? | remove() | pop() | delete() | discard()
Q: Which method gives the number of times an element occurs in a list? | count() | len() | index() | find()
M:method: append() | adds one item at the end
M:method: extend() | adds items of another list
M:method: insert() | adds an item at a position
M:method: pop() | removes an item by index and returns it
M:method: remove() | removes the first matching value
S+: sort() changes the list in place, while sorted() returns a new list
S+: remove() raises ValueError if the value is not present
S+: L.append([1, 2]) adds a single item, which is a list
S+: index() returns the position of the first occurrence of a value
S-: append() can add several separate items at once | extend() adds several items; append() adds one item
S-: pop() removes an item by its value | pop() removes by index; remove() removes by value
C: L.extend([1, 2]) increases the length of L by 2 | extend() adds each item of the sequence separately
C: print(L.sort()) prints None | sort() sorts in place and returns None
X: C2 D2 2 | Differentiate between append() and extend() with examples. | append adds one item, L.append([4, 5]) → [..., [4, 5]]; extend adds each item, L.extend([4, 5]) → [..., 4, 5].
X: C2 D2 2 | Differentiate between pop() and remove(). | pop(i) removes by index and returns the item; remove(x) removes the first occurrence of value x.
"""

TXT['listnest'] = """
T: nested list | a list that contains other lists as its items
T: shallow copy | a new list object with the same items, made with list(), copy() or slicing [:]
T: aliasing | giving a second name to the same list object, as in B = A, so changes through one name are seen through the other
Q: If L = [[1, 2], [3, 4]], what is L[1][0]? | 3 | 2 | 1 | 4
Q: After A = [1, 2]; B = A; B.append(3), what is A? | [1, 2, 3] | [1, 2] | [3] | Error
Q: Which of these makes a separate copy of list A? | B = A[:] | B = A | B == A | B is A
Q: If M = [[1, 2, 3], [4, 5, 6]], what is len(M)? | 2 | 6 | 3 | 1
S+: B = A does not create a new list; both names refer to the same list
S+: list(A), A.copy() and A[:] create a new list
S+: In a nested list, L[i][j] is the j-th item of the i-th inner list
S-: B = A creates a new independent copy of list A | B = A only creates another name (alias) for the same list
C: Changing B also changes A after B = A | both names refer to the same list object
C: Changing B does not change A after B = list(A) | list(A) creates a new list
X: C2 D2 2 | Differentiate between B = A and B = A.copy() for a list A. | B = A – alias, same object, changes reflect; B = A.copy() – new list, changes independent.
"""

TXT['listprog'] = """
T: linear search | searching for an item by comparing it with each element of a list from the beginning until it is found or the list ends
T: frequency | the number of times a value occurs in a collection
Q: In the worst case, linear search on a list of n elements makes: | n comparisons | 1 comparison | n/2 comparisons always | log n comparisons
Q: Which built-in functions give the largest and smallest elements of a list? | max() and min() | big() and small() | top() and bottom() | high() and low()
Q: The mean of the list L can be found as: | sum(L) / len(L) | len(L) / sum(L) | max(L) - min(L) | sum(L) * len(L)
S+: Linear search does not need the list to be sorted
S+: sum(L) / len(L) gives the mean of a list of numbers
S+: The count() method gives the frequency of an element in a list
S-: Linear search works only on sorted lists | Linear search works on any list
C: Linear search can stop early when the item is found | there is no need to compare the remaining elements
X: C2 D2 2 | Write a program to find the mean of the numbers in a list L. | total = 0; for x in L: total += x; print(total / len(L)).
"""

TXT['tuples'] = """
T: tuple | an ordered, immutable sequence of items enclosed in parentheses
T: tuple assignment | assigning the items of a tuple to several variables in one statement, as in a, b = 10, 20
T: nested tuple | a tuple that contains another tuple as an item
Q: Which of these creates a tuple with one element? | (5,) | (5) | [5] | {5}
Q: Which method is available for tuples? | count() | append() | remove() | sort()
Q: What does a, b = b, a do? | swaps the values of a and b | gives an error | makes both equal to a | deletes a
Q: If T = (1, 2, 3), what does T[1] = 5 give? | TypeError | (1, 5, 3) | (5, 2, 3) | IndexError
Q: What is (1, 2) + (3,)? | (1, 2, 3) | (4, 2) | Error | (1, 2, (3,))
S+: Tuples are immutable, so items cannot be added, removed or changed
S+: Tuples support indexing, slicing, concatenation and repetition
S+: Tuples have only two methods, count() and index()
S+: A tuple can contain a mutable item such as a list
S+: Tuple assignment can swap two variables without a third variable
S-: (5) is a tuple with one element | (5) is an int; a one-element tuple needs a comma: (5,)
S-: Tuples can be sorted in place with sort() | Tuples are immutable; sorted(T) returns a new list
C: Tuples are used for data that should not change | tuples are immutable
C: (5,) is a tuple but (5) is not | the comma, not the parentheses, makes a tuple
X: C2 D2 2 | Differentiate between a list and a tuple. | List – mutable, [ ], many methods; tuple – immutable, ( ), only count() and index().
X: C3 D3 3 | Write a program to input n numbers into a tuple and display the largest and the sum. | T = tuple(); for i in range(n): T = T + (int(input()),); print(max(T), sum(T)).
"""

TXT['dicts'] = """
T: dictionary | a mutable collection of key-value pairs enclosed in curly brackets, in which keys are unique and immutable
T: key | the unique, immutable part of a dictionary item that is used to access its value
Q: Which of these creates an empty dictionary? | {} | [] | () | dict[]
Q: If D = {"a": 1, "b": 2}, what is D["b"]? | 2 | "b" | 1 | Error
Q: Which of these can be a dictionary key? | a tuple | a list | another dictionary | a set
Q: Accessing a key that is not in a dictionary with D[key] gives: | KeyError | None | 0 | IndexError
Q: If D = {"x": 5}, what does D["y"] = 7 do? | adds a new key-value pair | gives an error | changes x | nothing
S+: Dictionary keys must be immutable and unique
S+: Values of a dictionary can be of any type and may repeat
S+: Assigning to a new key adds a new item to the dictionary
S+: The in operator checks keys, not values, of a dictionary
S+: A for loop over a dictionary visits its keys
S-: Dictionary keys can be repeated | Keys are unique; assigning to an existing key replaces its value
S-: A list can be used as a dictionary key | Keys must be immutable; a list is mutable
C: D[k] = v can change a dictionary | dictionaries are mutable
C: "Ravi" in D checks only the keys | the in operator on a dictionary tests membership among keys
X: C2 D2 2 | Differentiate between a list and a dictionary. | List – ordered by integer index, [ ]; dictionary – key-value pairs accessed by key, { }; both mutable.
"""

TXT['dictmeth'] = """
T: get() | the dictionary method that returns the value of a key, or None (or a given default) if the key is absent
T: items() | the dictionary method that returns the key-value pairs of a dictionary
T: update() | the dictionary method that adds or changes items using another dictionary
Q: Which method returns all keys of a dictionary? | keys() | values() | items() | get()
Q: D.get("z", 0) returns 0 when: | "z" is not a key in D | D is empty only | "z" is a value | always
Q: Which statement deletes the item with key k from D? | del D[k] | D.remove(k) | D.delete(k) | D.drop(k)
Q: Which method removes all items from a dictionary? | clear() | pop() | del() | empty()
Q: len(D) gives: | the number of key-value pairs | the number of values only | the total of the values | the last key
M:method: keys() | all the keys
M:method: values() | all the values
M:method: items() | key-value pairs
M:method: get() | value of a key without KeyError
M:method: update() | merge another dictionary
S+: get() does not raise an error for a missing key
S+: pop(key) removes the item and returns its value
S+: update() replaces the values of existing keys and adds new keys
S+: D.get(k, 0) + 1 is commonly used to count frequencies
S-: get() raises KeyError for a missing key | get() returns None or the given default
S-: clear() deletes the dictionary variable itself | clear() empties the dictionary; del D deletes the variable
C: D.get(k, 0) is used in frequency programs | it gives 0 for a key seen for the first time instead of raising KeyError
C: update() can change existing values | items with keys already present are replaced
X: C2 D2 2 | Differentiate between D[k] and D.get(k). | Both return the value for key k; D[k] raises KeyError if k is absent, D.get(k) returns None (or a default).
X: C3 D3 3 | Write a program to count the frequency of each word in a sentence using a dictionary. | D = {}; for w in s.split(): D[w] = D.get(w, 0) + 1; print(D).
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
    return [ST(prefix + suf, topic, _fix_a('\n'.join(TXT[k] for k in keys))) for suf, topic, keys in mapping]


CS_MAP = {
    5: [('05-st1', 'Python features, modes, keywords and identifiers', ['pybasics']), ('05-st2', 'data types and mutability', ['pytypes']),
        ('05-st3', 'operators and expressions', ['pyops']), ('05-st4', 'input, output and type conversion', ['pyio']), ('05-st5', 'errors and debugging', ['pyerrors'])],
    6: [('06-st1', 'selection statements', ['pyif']), ('06-st2', 'for and while loops', ['pyloops']), ('06-st3', 'break and continue statements', ['pybreak']),
        ('06-st4', 'nested loops and patterns', ['pynested'])],
    7: [('07-st1', 'user-defined functions, arguments and parameters', ['fndef']), ('07-st2', 'return values and flow of execution', ['fnreturn']),
        ('07-st3', 'scope of variables', ['fnscope']), ('07-st4', 'built-in functions and the math, random and statistics modules', ['fnbuiltin'])],
    8: [('08-st1', 'string operations', ['strops']), ('08-st2', 'traversing a string', ['strtrav']), ('08-st3', 'built-in string methods', ['strmeth']),
        ('08-st4', 'string handling programs', ['strprog'])],
    9: [('09-st1', 'list operations and mutability', ['listops']), ('09-st2', 'traversing lists and list methods', ['listmeth']),
        ('09-st3', 'nested lists and copying lists', ['listnest']), ('09-st4', 'list manipulation programs', ['listprog'])],
    10: [('10-st1', 'tuples', ['tuples']), ('10-st2', 'dictionaries', ['dicts']), ('10-st3', 'dictionary methods and programs', ['dictmeth'])],
}

AR_PY = {
    'types': [('A tuple cannot be changed after it is created.', 'Tuples are immutable sequences in Python.', 'a', 'Immutability is why a tuple cannot be changed.'),
              ('Strings in Python are immutable.', 'Each character of a string can be changed using indexing, as in s[0] = "A".', 'c', 'A is true; R is false: item assignment on a string gives TypeError.'),
              ('A list can contain elements of different data types.', 'Lists in Python are heterogeneous sequences.', 'a', 'Lists can mix data types.')],
    'ops': [('The expression 2 ** 3 ** 2 evaluates to 512.', 'The exponent operator ** is evaluated from right to left.', 'a', '3 ** 2 = 9 first, then 2 ** 9 = 512.'),
            ('15 // 4 gives 3 and 15 % 4 gives 3.', 'The // operator gives the quotient and % gives the remainder.', 'a', 'Floor division and modulus explain both results.'),
            ('The expression not True or True evaluates to True.', 'The or operator has higher precedence than not.', 'c', 'A is true; R is false: not has higher precedence than or.')],
    'loops': [('The loop for i in range(5): runs five times.', 'range(5) generates the numbers 0 to 4.', 'a', 'Five values 0–4, so five iterations.'),
              ('The break statement skips only the current iteration of a loop.', 'The continue statement moves control to the next iteration of the loop.', 'd', 'A is false: break exits the loop; R is true.')],
    'dict': [('Dictionary keys must be immutable.', 'A list can be used as a key in a dictionary.', 'c', 'A is true; R is false: a list is mutable and cannot be a key.')],
    'list': [('The statement L = [1, 2] * 2 gives [2, 4].', 'The * operator replicates a list.', 'd', 'A is false: [1, 2] * 2 = [1, 2, 1, 2]; R is true.')],
}


def arf(key, C='C3', D='D3'):
    return F(C, D, 'mcq', lambda r: ar(*r.choice(AR_PY[key])), kinds=('ar',))


def fams_python(S=S, chapters=(5, 6, 7, 8, 9, 10)):
    chs = [subs(S, CS_MAP[c]) for c in chapters]
    st = lambda x: S + x
    E = {
        st('05-st1'): [F('C4', 'D4', 'case', K.py_case, marks=4, gap='G7'), F('C1', 'D1', 'mcq', K.keyword_pick), F('C2', 'D2', 'mcq', K.ident_valid), F('C3', 'D3', 'explain', K.ident_classify, marks=2)],
        st('05-st2'): [F('C1', 'D2', 'mcq', K.type_out), F('C3', 'D3', 'mcq', K.mutability), F('C4', 'D4', 'mcq', G.alias_out, gap='G5'), arf('types')],
        st('05-st3'): [F('C4', 'D4', 'case', K.py_case, marks=4, gap='G7'), F('C2', 'D2', 'mcq', G.expr_eval), F('C3', 'D3', 'mcq', K.ops_out), F('C3', 'D4', 'mcq', G.expr_eval, gap='G5'), arf('ops')],
        st('05-st4'): [F('C2', 'D2', 'mcq', K.conv_out), F('C2', 'D3', 'mcq', K.input_out), F('C3', 'D3', 'mcq', K.print_out),
                       F('C4', 'D3', 'multi_step', lambda r: K.prog_write(r, 3, K.PROGS[:1] + K.PROGS[6:8]), marks=3)],
        st('05-st5'): [F('C4', 'D4', 'explain', K.error_find11, marks=2, gap='G5'), F('C2', 'D2', 'mcq', K.error_kind), F('C3', 'D4', 'explain', K.error_find11, marks=2, gap='G5'), F('C3', 'D4', 'explain', G.error_find, marks=2, gap='G5')],
        st('06-st1'): [F('C2', 'D2', 'short', K.if_out, marks=1), F('C3', 'D3', 'short', K.if_out, marks=1),
                       F('C4', 'D3', 'multi_step', lambda r: K.prog_write(r, 3, [K.PROGS[i] for i in (1, 7, 9)]), marks=3)],
        st('06-st2'): [F('C2', 'D2', 'mcq', K.range_out), F('C3', 'D3', 'short', G.loop_out, marks=2), F('C3', 'D3', 'mcq', K.pseudo_trace_mcq),
                       F('C4', 'D3', 'multi_step', lambda r: K.prog_write(r, 3, [K.PROGS[i] for i in (0, 2, 3, 4, 5, 10, 11)]), marks=3),
                       F('C4', 'D5', 'long', lambda r: K.prog_pair(r), marks=5), arf('loops')],
        st('06-st3'): [F('C4', 'D4', 'case', K.loop_case, marks=4, gap='G7'), F('C3', 'D3', 'short', K.break_continue, marks=2), F('C3', 'D3', 'mcq', K.bc_mcq), F('C3', 'D4', 'mcq', K.bc_mcq, gap='G5')],
        st('06-st4'): [F('C3', 'D3', 'short', K.nested_out, marks=2), F('C4', 'D4', 'multi_step', K.pattern_write, marks=3, gap='G5'),
                       F('C4', 'D5', 'long', lambda r: K.prog_pair(r, K.PROGS + [(f'Write a program to display the pattern below.\n{K.run(t.format(n=5, s="*"))}',
                                                                                  t.format(n=5, s='*'), '', None) for t, _ in K.PATTERNS[:4]]), marks=5)],
        st('07-st1'): [F('C2', 'D2', 'mcq', G.header_valid), F('C3', 'D3', 'mcq', G.call_valid), F('C2', 'D3', 'short', G.default_out, marks=2),
                       F('C4', 'D3', 'multi_step', lambda r: G.fn_task(r, marks=3), marks=3), F('C4', 'D4', 'case', G.args_case, marks=4, gap='G7')],
        st('07-st2'): [F('C2', 'D3', 'short', G.func_call_out, marks=2), F('C3', 'D3', 'mcq', G.returns_none), F('C3', 'D3', 'short', G.multi_return, marks=2),
                       F('C4', 'D5', 'long', G.fn_task2, marks=5)],
        st('07-st3'): [F('C3', 'D3', 'short', G.scope_out, marks=2), F('C3', 'D4', 'mcq', G.unbound, gap='G5'), F('C4', 'D4', 'mcq', G.mutable_pass, gap='G5'),
                       F('C4', 'D4', 'case', G.scope_case, marks=4, gap='G7')],
        st('07-st4'): [F('C4', 'D4', 'case', K.module_case, marks=4, gap='G7'), F('C2', 'D2', 'mcq', G.math_out), F('C2', 'D2', 'mcq', G.stats_out), F('C3', 'D4', 'mcq', G.rand_possible, gap='G5'),
                       F('C3', 'D3', 'short', G.rand_range, marks=2)],
        st('08-st1'): [F('C4', 'D4', 'case', K.str_case, marks=4, gap='G7'), F('C2', 'D2', 'short', G.slicing, marks=1), F('C2', 'D2', 'mcq', K.str_ops), F('C3', 'D3', 'mcq', K.str_ops)],
        st('08-st2'): [F('C4', 'D4', 'short', K.str_traverse, marks=2, gap='G5'), F('C3', 'D3', 'short', K.str_traverse, marks=2), F('C3', 'D4', 'short', K.str_traverse, marks=2, gap='G5')],
        st('08-st3'): [F('C4', 'D4', 'case', K.str_case, marks=4, gap='G7'), F('C2', 'D2', 'mcq', K.str_method), F('C2', 'D3', 'mcq', G.str_methods), F('C3', 'D3', 'mcq', K.str_method)],
        st('08-st4'): [F('C4', 'D3', 'multi_step', lambda r: K.prog_write(r, 3, K.STR_PROGS), marks=3), F('C4', 'D5', 'long', lambda r: K.prog_pair(r, K.STR_PROGS), marks=5),
                       F('C3', 'D3', 'short', K.str_traverse, marks=2)],
        st('09-st1'): [F('C4', 'D4', 'case', K.list_case, marks=4, gap='G7'), F('C2', 'D2', 'mcq', K.list_index), F('C3', 'D3', 'mcq', K.list_index), arf('list')],
        st('09-st2'): [F('C4', 'D4', 'case', K.list_case, marks=4, gap='G7'), F('C2', 'D3', 'mcq', K.list_method), F('C3', 'D3', 'short', G.list_ops, marks=2), F('C3', 'D4', 'mcq', K.list_method, gap='G5')],
        st('09-st3'): [F('C3', 'D3', 'mcq', K.nested_list), F('C3', 'D4', 'mcq', K.copy_out, gap='G5'), F('C4', 'D4', 'mcq', G.alias_out, gap='G5')],
        st('09-st4'): [F('C3', 'D3', 'short', K.list_prog_out, marks=2), F('C4', 'D3', 'multi_step', lambda r: K.prog_write(r, 3, K.LIST_PROGS), marks=3),
                       F('C4', 'D5', 'long', lambda r: K.prog_pair(r, K.LIST_PROGS), marks=5)],
        st('10-st1'): [F('C4', 'D4', 'case', K.dict_case, marks=4, gap='G7'), F('C2', 'D2', 'mcq', K.tuple_out), F('C3', 'D3', 'mcq', K.tuple_out), F('C3', 'D3', 'mcq', K.tuple_exc)],
        st('10-st2'): [F('C4', 'D4', 'case', K.dict_case, marks=4, gap='G7'), F('C2', 'D2', 'mcq', G.dict_ops), F('C3', 'D3', 'mcq', K.dict_method), arf('dict')],
        st('10-st3'): [F('C3', 'D3', 'short', K.freq_out, marks=2), F('C3', 'D4', 'mcq', K.dict_method, gap='G5'),
                       F('C4', 'D3', 'multi_step', lambda r: K.prog_write(r, 3, K.DICT_PROGS), marks=3), F('C4', 'D5', 'long', lambda r: K.prog_pair(r, K.DICT_PROGS), marks=5)],
    }
    E = {k: v for k, v in E.items() if any(k.startswith(S + f'{c:02d}') for c in chapters)}
    return chs, E
