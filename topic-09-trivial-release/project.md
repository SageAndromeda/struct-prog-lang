# Sage Hardiman

# CS 33101 Structure of Programming Languages Project.

## Add JavaScript Modulo Operator to trivial.


## The problem:
Trivial does not have a modulo operator `%`. 
Python and JavaScript have two different versions of the mod operator; doing a modulo with negavie numbers works differently depending on the language. In python, `-1%10` returns `9`, but in JavaScript and C++, the same code returns `-1` instead.
Trivial is python based, but since the language is similar to JavaScript, I will implement that version of modulo instead.

## Code

### tokenizer.py
Regex to find modulo symbol: `[r"%", "%"]`.
Updated test in `test_simple_tokens()` with `%` after `/`: `examples = ".,[,],+,-,*,/,%,(,),{,},;,:,!,&&,||,<,>,<=,>=,==,!=,=".split(","`. This test fails if the regex is removed.