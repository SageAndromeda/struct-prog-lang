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

### evaluator.py
This is arguably the most important part! I have to make it return the result of `left % right` but also make sure it can properly return `-1%10` as `-1`.

Update `evaluate()` function to evaluate modulo operator:
``` python
if ast["tag"] == "%":
        left_value, _ = evaluate(ast["left"], environment)
        right_value, _ = evaluate(ast["right"], environment)
        assert right_value != 0, "Division by zero"
        if (left_value >= 0 and right_value >= 0) or (
            left_value < 0 and right_value < 0
        ):
            return left_value % right_value, False
        return (-1) * (((-1) * left_value) % right_value), False
```
If `left_value` and `right_value` have the same sign, it runs modulo as normal. If one is negative and the other positive, however, `left_value` will temporarily be converted to the other sign. Modulo will then be run like normal on that, and the remainder will be converted to the opposite sign. This essentially simulates JavaScript modulo.

Big test suit for modulo:
``` python
def test_evaluate_modulo():
    print("test evaluate modulo")
    equals("1%10", {}, 1, {})
    equals("8%4%2", {}, 0, {})
    equals("10%5.23", {}, 4.77, {})
    equals("-1%10", {}, -1, {})
    equals("1%-10", {}, 1, {})
    equals("1%-10", {}, 1, {})
    equals("772%(-43)", {}, 41, {})
    equals("(-772)%43", {}, -41, {})
    equals("(-772)%(-43)", {}, -41, {})
    equals("772%43", {}, 41, {})
    equals("-10%5.23", {}, -4.77, {})
    equals("3%2*5", {}, 5, {})
    equals("3+2%2", {}, 3, {})
    equals("(3+2)%2", {}, 1, {})
    equals("(3+2)%(-2)", {}, 1, {})
    equals("((9-22)+(3+2))%(-2)", {}, 0, {})
```

Finally, make sure it's in the test suite under `__main__`: `test_evaluate_modulo()`

## What did I learn?
First and foremost, I figured out a way to convert python's modulo operator into JavaScript's without using a built in function. The equation `(-1) * (((-1) * left_value) % right_value)` handles this. Because modulo works the same when `left_value` and `right_value` are both positive or both negative, I can essentially flip the sign of one (I chose `left_value`) run modulo, then convert it back to the other sign.

I did not realize at first that the right side being negative while the left was positive would also change how modulo worked. This led to the test `equals("(3+2)%(-2)", {}, 1, {})` failing. I looked for a pattern in when python and JavaScript modulos were the same or different (different when they had opposite preceeding signs), and used that to modify my if statement in the `evaluate` function to be false when the signs were different instead of just when `left_value` was negative. 

My code started crashing when I was running tests in `evaluator.py`, but not because they were failing. It seemd that if I didn't parenthesize my negative numbers, python thought I was trying to work with something that wasn't an integer. 

Finally, I found out that `%` is not a special character in a regex and thus doesn't need to be escaped.

### How do we know you have succeeded?
Firstly, all of the tests in `tokenizer.py`, `parser.py`, and `evaluator.py` run without failing including my new ones. Secondly, `runner.py` and `trivial` can be activated and given modulo operations and it will run them properly instead of crashing.

I've attached all of my files in a zip for you to look at.