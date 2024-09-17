from tokenizer import tokenize
from parser import parse


def evaluate(ast, environment):
    if ast["tag"] == "number":
        assert type(ast["value"]) in [float, int], f"unexpected numerical type {type(ast["value"])}"
        return ast["value"], False
    if ast["tag"] == "+":
        left_value, _ = evaluate(ast["left"], environment)
        right_value, _ = evaluate(ast["right"], environment)
        return left_value + right_value, False
    if ast["tag"] == "-":
        left_value, _ = evaluate(ast["left"], environment)
        right_value, _ = evaluate(ast["right"], environment)
        return left_value - right_value, False
    if ast["tag"] == "*":
        left_value, _ = evaluate(ast["left"], environment)
        right_value, _ = evaluate(ast["right"], environment)
        return left_value * right_value, False
    if ast["tag"] == "/":
        left_value, _ = evaluate(ast["left"], environment)
        right_value, _ = evaluate(ast["right"], environment)
        assert right_value !=0, "Division by zero"
        return left_value / right_value, False
    if ast["tag"] == "negate":
        value, _ = evaluate(ast["value"], environment)
        return -value, False
    assert False, "Unknown operator in AST"


def equals(code, environment, expected_result, expected_environment=None):
    # expected_environment is None by default because we don't want to modify env most of the time
    result, _ = evaluate(parse(tokenize(code)), environment)
    assert (
        result == expected_result
    ), f"""ERROR: When executing {[code]} 
    -- expected result -- {[expected_result]} 
    -- got -- {[result]} instead."""
    if expected_environment != None:
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
    equals("3", {}, 3, {})
    equals("4.2", {}, 4.2, {})
    equals("3.9", {}, 3.9, {})


def test_evaluate_addition():
    print("testing evaluate_addiiton")
    equals("1+1",{},2,{})
    equals("1+2+3",{},6,{})
    equals("1.2+2+3.9",{},7.1,{})

def test_evaluate_subtraction():
    print("testing evaluate_subtraction")
    equals("1-1",{},0,{})
    equals("3-2-1",{},0,{})
    equals("7.7-2-1.1",{},4.6,{})

def test_evaluate_multiplication():
    print("testing evaluate_multiplication")
    equals("1*1",{},1,{})
    equals("2.4*2",{},4.8,{})
    equals("3*4",{},12,{})
    equals("3+2*2",{},7,{})
    equals("(3+2)*2",{},10,{})

def test_evaluate_divison():
    print("testing evaluate_division")
    equals("1/1",{},1,{})
    equals("8/4/2",{},1,{})
    equals("4/2",{},2,{})
    equals("(3+3)/2",{},3,{})

def test_evaluate_negation():
    print("testing evaluate_negation")
    equals("-2",{},-2,{})
    equals("--3",{},3,{})
    

if __name__ == "__main__":
    test_evaluate_single_value()
    test_evaluate_addition()
    test_evaluate_subtraction()
    test_evaluate_multiplication()
    test_evaluate_divison()
    test_evaluate_negation()
    print("done")
