from tokenizer import tokenize
from parser import parse


def evaluate(ast, environment):
    environment["x"] = 3
    return 4, False


def equals(code, environment, expected_result, expected_environment=None):
    # expected_environment is None by default because we don't want to modify env most of the time
    result, _ = evaluate(parse(tokenize(code)), environment)
    print([environment, expected_environment])
    assert (
        result == expected_result
    ), f"""ERROR: When executing {[code]} 
    -- expected result -- {[expected_result]} 
    -- got -- {[result]} instead."""
    if expected_environment != None:
        print("checking environment")
        assert (
            environment == expected_environment
        ), f"""ERROR: When executing
        {[code]}
        -- expected environment -- {[expected_environment]}
        -- got --
        {[environment]} instead."""


def test_evaluate_single_value():
    print("test evaluate_single_value")
    equals("4", {}, 4, {})


if __name__ == "__main__":
    test_evaluate_single_value()
    print("done")
