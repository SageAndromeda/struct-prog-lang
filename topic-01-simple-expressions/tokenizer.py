# Tokenizer

"""
Break character stream into tokens, provide a token stream
"""

import re

patterns = [
    # ["\\+\\+", "++"], # ++ must be before + or it will tokenize + first
    ["\\+", "+"],  # Regex that looks for plus sign and produces one
    ["\\-", "-"],
    ["\\(", "("],
    ["\\)", ")"],
    ["\\*", "*"],
    ["\\/", "/"],
    ["(\\d*\\.\\d+)|(\\d+\\.\\d*)|(\\d+)", "number"],
]

for pattern in patterns:
    pattern[0] = re.compile(pattern[0])


def tokenize(characters):
    tokens = []
    position = 0
    while position < len(characters):
        for pattern, tag in patterns:
            match = pattern.match(characters, position)
            if match:
                break  # breaks for but not while
        assert match
        print("Match found: ", match)
        token = {
            "tag": tag,
            "value": match.group(0),
            "position": position,
        }
        tokens.append(token)
        position = match.end()
    for token in tokens:
        if token["tag"] == "number":
            if "." in token["value"]:
                token["value"] = float(token["value"])
            else:
                token["value"] = int(token["value"])
    return tokens


def test_simple_tokens():
    print("testing simple tokens")
    print(tokenize("+"))
    assert tokenize("+") == [{"tag": "+", "value": "+", "position": 0}]
    assert tokenize("-") == [{"tag": "-", "value": "-", "position": 0}]
    i = 0
    for char in ["+", "-"]:
        tokens = tokenize(char)
        assert tokens[0]["tag"] == char
        assert tokens[0]["value"] == char
    for char in "+-*/":
        tokens = tokenize(char)
        assert tokens[0]["tag"] == char
        assert tokens[0]["value"] == char
        assert tokens[0]["position"] == i
    for number in ["123.45", "1.", ".1", "123"]:
        tokens = tokenize(number)
        assert tokens[0]["tag"] == "number"
        assert tokens[0]["value"] == float(number)


if __name__ == "__main__":  # Idiom in Python saying this is the main program
    test_simple_tokens()
    # tokens = tokenize("123.45")
    # print(tokens)
    print("Done.")
