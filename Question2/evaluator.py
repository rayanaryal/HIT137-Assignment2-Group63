'''
HIT137 SOFTWARE NOW
Assignment 2

Group: Group 63
Group Members and Student ID:
        Rupesh Timalsina: S400656
        Swastik Bista: S400506
        Rajan Aryal: S333047
'''


import os

# -------------------- MAIN FUNCTION --------------------
def evaluate_file(input_path: str) -> list[dict]:
    results = []

    # read expressions (one per line)
    with open(input_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # output file to be created in same directory
    output_path = os.path.join(os.path.dirname(input_path), "output.txt")

    with open(output_path, "w", encoding="utf-8") as out:
        for line in lines:
            original = line.rstrip("\n")

            try:
                # tokenize input
                tokens = tokenize(original)

                # parse into a tree
                state = {"tokens": tokens, "pos": 0}
                tree = parse_expression(state)

                # after parsing, we must be at the END
                if current_token(state)["type"] != "END":
                    raise ValueError("Extra tokens after valid expression")

                # print tree and token string after parsing succeeds
                tree_string = tree_to_string(tree)
                token_string = format_tokens(tokens)

                # evaluate tree
                value = evaluate_tree(tree)

                # if evaluation returns ERROR (division by zero), keep tree/tokens
                if value == "ERROR":
                    result_value = "ERROR"
                else:
                    result_value = float(value)

                result_dict = {
                    "input": original,
                    "tree": tree_string,
                    "tokens": token_string,
                    "result": result_value
                }

            except Exception:

                # invalid token or parse error
                result_dict = {
                    "input": original,
                    "tree": "ERROR",
                    "tokens": "ERROR",
                    "result": "ERROR"
                }

            results.append(result_dict)

            # output
            out.write(f"Input: {result_dict['input']}\n")
            out.write(f"Tree: {result_dict['tree']}\n")
            out.write(f"Tokens: {result_dict['tokens']}\n")

            if result_dict["result"] == "ERROR":
                out.write("Result: ERROR\n")
            else:
                out.write(f"Result: {format_result(result_dict['result'])}\n")

            out.write("\n")

    return results


# -------------------- TOKENIZER --------------------
def tokenize(text: str) -> list[dict]:
    tokens = []
    i = 0
    prev_type = None

    while i < len(text):
        ch = text[i]

        # ignore whitespace
        if ch.isspace():
            i += 1
            continue

        # numbers (integer or decimal)
        if ch.isdigit() or ch == ".":
            start = i
            dot_count = 0

            while i < len(text) and (text[i].isdigit() or text[i] == "."):
                if text[i] == ".":
                    dot_count += 1
                i += 1

            number_text = text[start:i]

            if dot_count > 1 or number_text == ".":
                raise ValueError("Invalid number")

            # implicit multiplication: 2(3) or )3 or 2 3
            if prev_type in ["NUM", "RPAREN"]:
                tokens.append({"type": "OP", "value": "*"})

            tokens.append({"type": "NUM", "value": number_text})
            prev_type = "NUM"
            continue

        # left parenthesis
        if ch == "(":
            # implicit multiplication: 2(3) or )(...)
            if prev_type in ["NUM", "RPAREN"]:
                tokens.append({"type": "OP", "value": "*"})

            tokens.append({"type": "LPAREN", "value": "("})
            prev_type = "LPAREN"
            i += 1
            continue

        # right parenthesis
        if ch == ")":
            tokens.append({"type": "RPAREN", "value": ")"})
            prev_type = "RPAREN"
            i += 1
            continue

        # operators
        if ch in "+-*/":
            tokens.append({"type": "OP", "value": ch})
            prev_type = "OP"
            i += 1
            continue

        # invalid character
        raise ValueError("Invalid character")

    tokens.append({"type": "END", "value": ""})
    return tokens


# -------------------- TOKEN FORMATTING --------------------
def format_tokens(tokens: list[dict]) -> str:
    parts = []

    for token in tokens:
        if token["type"] == "END":
            parts.append("[END]")
        else:
            parts.append(f"[{token['type']}:{token['value']}]")

    return " ".join(parts)


# -------------------- PARSER HELPERS --------------------
def current_token(state: dict) -> dict:
    return state["tokens"][state["pos"]]


def consume_token(state: dict, expected_type=None, expected_value=None) -> dict:
    token = current_token(state)

    if expected_type is not None and token["type"] != expected_type:
        raise ValueError("Unexpected token type")

    if expected_value is not None and token["value"] != expected_value:
        raise ValueError("Unexpected token value")

    state["pos"] += 1
    return token


# -------------------- RECURSIVE DESCENT PARSER --------------------
# expression -> term ((+|-) term)*
def parse_expression(state: dict):
    left = parse_term(state)

    while current_token(state)["type"] == "OP" and current_token(state)["value"] in ["+", "-"]:
        op = consume_token(state, "OP")["value"]
        right = parse_term(state)
        left = ("bin", op, left, right)

    return left


# term -> factor ((*|/) factor)*
def parse_term(state: dict):
    left = parse_factor(state)

    while current_token(state)["type"] == "OP" and current_token(state)["value"] in ["*", "/"]:
        op = consume_token(state, "OP")["value"]
        right = parse_factor(state)
        left = ("bin", op, left, right)

    return left


# factor -> -factor | primary
# unary plus is NOT allowed
def parse_factor(state: dict):
    token = current_token(state)

    # unary plus error and unary negation
    if token["type"] == "OP" and token["value"] == "+":
        raise ValueError("Unary plus not supported")

    if token["type"] == "OP" and token["value"] == "-":
        consume_token(state, "OP", "-")
        operand = parse_factor(state)
        return ("neg", operand)

    return parse_primary(state)


# primary -> NUM | (expression)
def parse_primary(state: dict):
    token = current_token(state)

    if token["type"] == "NUM":
        consume_token(state, "NUM")
        return ("num", float(token["value"]))

    if token["type"] == "LPAREN":
        consume_token(state, "LPAREN")
        expr = parse_expression(state)
        consume_token(state, "RPAREN")
        return expr

    raise ValueError("Expected number or (")


# -------------------- TREE EVALUATION --------------------
def evaluate_tree(tree):
    kind = tree[0]

    # number node
    if kind == "num":
        return tree[1]

    # unary negation node
    if kind == "neg":
        val = evaluate_tree(tree[1])
        if val == "ERROR":
            return "ERROR"
        return -val

    # binary node
    if kind == "bin":
        op = tree[1]
        left_val = evaluate_tree(tree[2])
        right_val = evaluate_tree(tree[3])

        if left_val == "ERROR" or right_val == "ERROR":
            return "ERROR"

        if op == "+":
            return left_val + right_val
        if op == "-":
            return left_val - right_val
        if op == "*":
            return left_val * right_val
        if op == "/":
            if right_val == 0:
                return "ERROR"
            return left_val / right_val

    return "ERROR"


# -------------------- TREE FORMATTING --------------------
def tree_to_string(tree) -> str:
    kind = tree[0]

    if kind == "num":
        return format_number(tree[1])

    if kind == "neg":
        return f"(neg {tree_to_string(tree[1])})"

    if kind == "bin":
        op = tree[1]
        left = tree_to_string(tree[2])
        right = tree_to_string(tree[3])
        return f"({op} {left} {right})"

    raise ValueError("Invalid tree")


# -------------------- OUTPUT NUMBER FORMATTING --------------------
def format_number(value: float) -> str:

    # for tree formatting: print integer without .0
    if float(value).is_integer():
        return str(int(value))
    return str(value)


def format_result(value: float) -> str:

    # result formatting rules
    if float(value).is_integer():
        return str(int(value))
    return f"{value:.4f}"




# --------------------- TEST CODE (INPUT FILE) ---------------------
if __name__ == "__main__":
    test_file = "input.txt"
    result = evaluate_file(test_file)
    for r in result:
        print(r)
