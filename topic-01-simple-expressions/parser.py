"""
parser.py -- implement parser for simple expressions

Accept a string of tokens, return an AST expressed as stack of dictionaries
"""

"""
    simple_expression = number | "(" expression ")" | "-" simple_expression
    factor = simple_expression
    term = factor { "*"|"/" factor }
    expression = term { "+"|"-" term }
"""

from pprint import pprint

from tokenizer import tokenize


def parse_simple_expression(tokens):
    """
    simple_expression = number | "(" expression ")" | "-" simple_expression
    """
    if tokens[0]["tag"] == "number":
        return tokens[0], tokens[1:]
    if tokens[0]["tag"] == "(":
        node, tokens = parse_expression(tokens[1:])
        assert tokens[0]["tag"] == ")", "Error: expected ')'"
        return node, tokens[1:]
    if tokens[0]["tag"] == "-":
        node, tokens = parse_simple_expression(tokens[1:])
        node = {"tag": "negate", "value": node}
        return node, tokens


def parse_expression(tokens):
    return parse_simple_expression(tokens)


def test_parse_simple_expression():
    """
    simple_expression = number | "(" expression ")" | "-" simple_expression
    """
    print("testing parse_simple_expression")
    tokens = tokenize("2")
    ast, tokens = parse_simple_expression(tokens)
    assert ast["tag"] == "number"
    assert ast["value"] == 2
    # pprint(ast)
    tokens = tokenize("(2)")
    ast, tokens = parse_simple_expression(tokens)
    assert ast["tag"] == "number"
    assert ast["value"] == 2
    # pprint(ast)
    tokens = tokenize("-2")
    ast, tokens = parse_simple_expression(tokens)
    assert ast == {
        "tag": "negate",
        "value": {"position": 1, "tag": "number", "value": 2},
    }
    # pprint(ast)
    tokens = tokenize("-(2)")
    ast, tokens = parse_simple_expression(tokens)
    assert ast == {
        "tag": "negate",
        "value": {"position": 2, "tag": "number", "value": 2},
    }
    tokens = tokenize("0")
    ast, tokens = parse_simple_expression(tokens)
    assert ast["tag"] == "number"
    assert ast["value"] == 0
    tokens = tokenize("-0")
    ast, tokens = parse_simple_expression(tokens)
    assert ast == {
        "tag": "negate",
        "value": {"position": 1, "tag": "number", "value": 0},
    }
    tokens = tokenize("-(0)")
    ast, tokens = parse_simple_expression(tokens)
    assert ast == {
        "tag": "negate",
        "value": {"position": 2, "tag": "number", "value": 0},
    }
    tokens = tokenize("12")
    ast, tokens = parse_simple_expression(tokens)
    assert ast["tag"] == "number"
    assert ast["value"] == 12
    tokens = tokenize("-(19-13)-5(4)")
    ast, tokens = parse_simple_expression(tokens)
    assert ast == {
        "tag": "negate",
        "value": {
            "tag": "-",
            "left": {"tag": "number", "value": 19, "position": 2},
            "right": {"tag": "number", "value": 13, "position": 5},
        },
    }
    # pprint(ast)


def parse_factor(tokens):
    """
    factor = simple_expression
    """
    return parse_simple_expression(tokens)


def test_parse_factor():
    """
    factor = simple_expression
    """
    print("testing parse_factor")
    for s in [
        "2",
        "(2)",
        "-2",
        "-(4)",
        "0",
        "1",
        "-0",
        "-(-0)",
        "79",
        "-(488-37)-6(3)",
        "-(74-13-56)-6(7)",
    ]:
        assert parse_factor(tokenize(s)) == parse_simple_expression(tokenize(s))


def parse_term(tokens):
    """
    term = factor { "*"|"/" factor }
    """
    node, tokens = parse_factor(tokens)
    while tokens[0]["tag"] in ["*", "/"]:
        tag = tokens[0]["tag"]
        right_node, tokens = parse_factor(tokens[1:])
        node = {"tag": tag, "left": node, "right": right_node}
    return node, tokens


def test_parse_term():
    """
    term = factor { "*"|"/" factor }
    """
    print("testing parse_term")
    tokens = tokenize("2*3")
    ast, tokens = parse_term(tokens)
    assert ast == {
        "left": {"position": 0, "tag": "number", "value": 2},
        "right": {"position": 2, "tag": "number", "value": 3},
        "tag": "*",
    }
    tokens = tokenize("2*3/4*5")
    ast, tokens = parse_term(tokens)
    assert ast == {
        "left": {
            "left": {
                "left": {"position": 0, "tag": "number", "value": 2},
                "right": {"position": 2, "tag": "number", "value": 3},
                "tag": "*",
            },
            "right": {"position": 4, "tag": "number", "value": 4},
            "tag": "/",
        },
        "right": {"position": 6, "tag": "number", "value": 5},
        "tag": "*",
    }
    tokens = tokenize("-3*4")
    ast, tokens = parse_term(tokens)
    assert ast == {
        "tag": "*",
        "left": {
            "tag": "negate",
            "value": {"tag": "number", "value": 3, "position": 1},
        },
        "right": {"tag": "number", "value": 4, "position": 3},
    }
    tokens = tokenize("0/9/8/7/6/5/4/3/2/1")
    ast, tokens = parse_term(tokens)
    assert ast == {
        "tag": "/",
        "left": {
            "tag": "/",
            "left": {
                "tag": "/",
                "left": {
                    "tag": "/",
                    "left": {
                        "tag": "/",
                        "left": {
                            "tag": "/",
                            "left": {
                                "tag": "/",
                                "left": {
                                    "tag": "/",
                                    "left": {
                                        "tag": "/",
                                        "left": {
                                            "tag": "number",
                                            "value": 0,
                                            "position": 0,
                                        },
                                        "right": {
                                            "tag": "number",
                                            "value": 9,
                                            "position": 2,
                                        },
                                    },
                                    "right": {
                                        "tag": "number",
                                        "value": 8,
                                        "position": 4,
                                    },
                                },
                                "right": {"tag": "number", "value": 7, "position": 6},
                            },
                            "right": {"tag": "number", "value": 6, "position": 8},
                        },
                        "right": {"tag": "number", "value": 5, "position": 10},
                    },
                    "right": {"tag": "number", "value": 4, "position": 12},
                },
                "right": {"tag": "number", "value": 3, "position": 14},
            },
            "right": {"tag": "number", "value": 2, "position": 16},
        },
        "right": {"tag": "number", "value": 1, "position": 18},
    }
    tokens = tokenize("2*3*4")
    ast, tokens = parse_term(tokens)
    assert ast == {
        "tag": "*",
        "left": {
            "tag": "*",
            "left": {"tag": "number", "value": 2, "position": 0},
            "right": {"tag": "number", "value": 3, "position": 2},
        },
        "right": {"tag": "number", "value": 4, "position": 4},
    }
    tokens = tokenize("-(713*5)-6(8/-4)")
    ast, tokens = parse_term(tokens)
    assert ast == {
        "tag": "negate",
        "value": {
            "tag": "*",
            "left": {"tag": "number", "value": 713, "position": 2},
            "right": {"tag": "number", "value": 5, "position": 6},
        },
    }
    tokens = tokenize("400/0")
    ast, tokens = parse_term(tokens)
    assert ast == {
        "tag": "/",
        "left": {"tag": "number", "value": 400, "position": 0},
        "right": {"tag": "number", "value": 0, "position": 4},
    }
    tokens = tokenize("0*144")
    ast, tokens = parse_term(tokens)
    assert ast == {
        "tag": "*",
        "left": {"tag": "number", "value": 0, "position": 0},
        "right": {"tag": "number", "value": 144, "position": 2},
    }


def parse_expression(tokens):
    """
    expression = term { "+"|"-" term }
    """
    node, tokens = parse_term(tokens)
    while tokens[0]["tag"] in ["+", "-"]:
        tag = tokens[0]["tag"]
        right_node, tokens = parse_term(tokens[1:])
        node = {"tag": tag, "left": node, "right": right_node}
    return node, tokens


def test_parse_expression():
    """
    expression = term { "+"|"-" term }
    """
    print("testing parse_expression")
    tokens = tokenize("2+3")
    ast, tokens = parse_expression(tokens)
    assert ast == {
        "left": {"position": 0, "tag": "number", "value": 2},
        "right": {"position": 2, "tag": "number", "value": 3},
        "tag": "+",
    }
    tokens = tokenize("2+3-4+5")
    ast, tokens = parse_expression(tokens)
    assert ast == {
        "left": {
            "left": {
                "left": {"position": 0, "tag": "number", "value": 2},
                "right": {"position": 2, "tag": "number", "value": 3},
                "tag": "+",
            },
            "right": {"position": 4, "tag": "number", "value": 4},
            "tag": "-",
        },
        "right": {"position": 6, "tag": "number", "value": 5},
        "tag": "+",
    }
    tokens = tokenize("2+3*4+5")
    ast, tokens = parse_expression(tokens)
    assert ast == {
        "left": {
            "left": {"position": 0, "tag": "number", "value": 2},
            "right": {
                "left": {"position": 2, "tag": "number", "value": 3},
                "right": {"position": 4, "tag": "number", "value": 4},
                "tag": "*",
            },
            "tag": "+",
        },
        "right": {"position": 6, "tag": "number", "value": 5},
        "tag": "+",
    }
    tokens = tokenize("6/3+2")
    ast, tokens = parse_expression(tokens)
    assert ast == {
        "tag": "+",
        "left": {
            "tag": "/",
            "left": {"tag": "number", "value": 6, "position": 0},
            "right": {"tag": "number", "value": 3, "position": 2},
        },
        "right": {"tag": "number", "value": 2, "position": 4},
    }
    tokens = tokenize("(-(4*8-2)/4)")
    ast, tokens = parse_expression(tokens)
    assert ast == {
        "tag": "/",
        "left": {
            "tag": "negate",
            "value": {
                "tag": "-",
                "left": {
                    "tag": "*",
                    "left": {"tag": "number", "value": 4, "position": 3},
                    "right": {"tag": "number", "value": 8, "position": 5},
                },
                "right": {"tag": "number", "value": 2, "position": 7},
            },
        },
        "right": {"tag": "number", "value": 4, "position": 10},
    }
    tokens = tokenize("(2+3)*-4/5")
    ast, tokens = parse_expression(tokens)
    assert ast == {
        "tag": "/",
        "left": {
            "tag": "*",
            "left": {
                "tag": "+",
                "left": {"tag": "number", "value": 2, "position": 1},
                "right": {"tag": "number", "value": 3, "position": 3},
            },
            "right": {
                "tag": "negate",
                "value": {"tag": "number", "value": 4, "position": 7},
            },
        },
        "right": {"tag": "number", "value": 5, "position": 9},
    }
    tokens = tokenize("-(0*1)/1/0+0")
    ast, tokens = parse_expression(tokens)
    assert ast == {
        "tag": "+",
        "left": {
            "tag": "/",
            "left": {
                "tag": "/",
                "left": {
                    "tag": "negate",
                    "value": {
                        "tag": "*",
                        "left": {"tag": "number", "value": 0, "position": 2},
                        "right": {"tag": "number", "value": 1, "position": 4},
                    },
                },
                "right": {"tag": "number", "value": 1, "position": 7},
            },
            "right": {"tag": "number", "value": 0, "position": 9},
        },
        "right": {"tag": "number", "value": 0, "position": 11},
    }


def parse(tokens):
    return parse_expression(tokens)


def test_parse():
    print("testing parse")
    tokens = tokenize("2+3*4+5")
    assert parse(tokens) == parse_expression(tokens)


if __name__ == "__main__":
    test_parse_simple_expression()
    test_parse_factor()
    test_parse_term()
    test_parse_expression()
    test_parse()
    print("done")
