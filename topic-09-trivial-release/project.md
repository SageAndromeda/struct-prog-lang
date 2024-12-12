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


### parser.py
Updated ENBF to note modulo as an arithmetic term: `arithmetic_term = arithmetic_factor { ("*" | "/" | "%") arithmetic_factor } ;`.

Add `%` to tokens in `parse_arithmetic_term(tokens)`: `while tokens[0]["tag"] in ["*", "/", "%"]:`.'

New tests for `test_parse_arithmetic_term`:
```python
ast, tokens = parse_arithmetic_term(tokenize("x%y"))
assert ast == {
    "tag": "%",
    "left": {"tag": "identifier", "value": "x"},
    "right": {"tag": "identifier", "value": "y"},
}

ast, tokens = parse_arithmetic_term(tokenize("x%y%z"))
assert ast == {
    "tag": "%",
    "left": {
        "tag": "%",
        "left": {"tag": "identifier", "value": "x"},
        "right": {"tag": "identifier", "value": "y"},
    },
    "right": {"tag": "identifier", "value": "z"},
}

ast, tokens = parse_arithmetic_term(tokenize("w*x/y%z"))
assert ast == {
    "tag": "%",
    "left": {
        "tag": "/",
        "left": {
            "tag": "*",
            "left": {"tag": "identifier", "value": "w"},
            "right": {"tag": "identifier", "value": "x"},
        },
        "right": {"tag": "identifier", "value": "y"},
    },
    "right": {"tag": "identifier", "value": "z"},
}

ast, tokens = parse_arithmetic_term(tokenize("w*x%y/z"))
assert ast == {
    "tag": "/",
    "left": {
        "tag": "%",
        "left": {
            "tag": "*",
            "left": {"tag": "identifier", "value": "w"},
            "right": {"tag": "identifier", "value": "x"},
        },
        "right": {"tag": "identifier", "value": "y"},
    },
    "right": {"tag": "identifier", "value": "z"},
}

ast, tokens = parse_arithmetic_term(tokenize("w%x/y*z"))
assert ast == {
    "tag": "*",
    "left": {
        "tag": "/",
        "left": {
            "tag": "%",
            "left": {"tag": "identifier", "value": "w"},
            "right": {"tag": "identifier", "value": "x"},
        },
        "right": {"tag": "identifier", "value": "y"},
    },
    "right": {"tag": "identifier", "value": "z"},
}
```

New tests for `test_parse_arithmetic_expression`:
```python
ast = parse_arithmetic_expression(tokenize("x%y"))[0]
assert ast == {
    "tag": "%",
    "left": {"tag": "identifier", "value": "x"},
    "right": {"tag": "identifier", "value": "y"},
}
ast = parse_arithmetic_expression(tokenize("w+x-y%z"))[0]
assert ast == {
    "tag": "-",
    "left": {
        "tag": "+",
        "left": {"tag": "identifier", "value": "w"},
        "right": {"tag": "identifier", "value": "x"},
    },
    "right": {
        "tag": "%",
        "left": {"tag": "identifier", "value": "y"},
        "right": {"tag": "identifier", "value": "z"},
    },
}
ast = parse_arithmetic_expression(tokenize("w+x%y-z"))[0]
assert ast == {
    "tag": "-",
    "left": {
        "tag": "+",
        "left": {"tag": "identifier", "value": "w"},
        "right": {
            "tag": "%",
            "left": {"tag": "identifier", "value": "x"},
            "right": {"tag": "identifier", "value": "y"},
        },
    },
    "right": {"tag": "identifier", "value": "z"},
}
ast = parse_arithmetic_expression(tokenize("(w%x)%(y%z)"))[0]
assert ast == {
    "tag": "%",
    "left": {
        "tag": "%",
        "left": {"tag": "identifier", "value": "w"},
        "right": {"tag": "identifier", "value": "x"},
    },
    "right": {
        "tag": "%",
        "left": {"tag": "identifier", "value": "y"},
        "right": {"tag": "identifier", "value": "z"},
    },
}
ast = parse_arithmetic_expression(tokenize("v/(w%x+y)*z"))[0]
assert ast == {
    "tag": "*",
    "left": {
        "tag": "/",
        "left": {"tag": "identifier", "value": "v"},
        "right": {
            "tag": "+",
            "left": {
                "tag": "%",
                "left": {"tag": "identifier", "value": "w"},
                "right": {"tag": "identifier", "value": "x"},
            },
            "right": {"tag": "identifier", "value": "y"},
        },
    },
    "right": {"tag": "identifier", "value": "z"},
}
```
