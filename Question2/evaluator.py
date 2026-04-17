import os
import math

# -----------------------------
# Token representation
# -----------------------------
class Token:
    def __init__(self, ttype, value):
        self.type = ttype  # 'NUM', 'OP', 'LPAREN', 'RPAREN', 'END'
        self.value = value

    def __repr__(self):
        return f"[{self.type}:{self.value}]"


# -----------------------------
# Lexer / Tokenizer
# -----------------------------
def tokenize(expr):
    tokens = []
    i = 0
    n = len(expr)

    def is_digit(ch):
        return ch.isdigit() or ch == "."

    while i < n:
        ch = expr[i]

        if ch.isspace():
            i += 1
            continue

        if is_digit(ch):
            start = i
            dot_count = 0
            while i < n and is_digit(expr[i]):
                if expr[i] == ".":
                    dot_count += 1
                i += 1
            if dot_count > 1:
                raise ValueError("Invalid number")
            num_str = expr[start:i]
            tokens.append(Token("NUM", num_str))
            continue

        if ch in "+-*/":
            tokens.append(Token("OP", ch))
            i += 1
            continue

        if ch == "(":
            tokens.append(Token("LPAREN", ch))
            i += 1
            continue

        if ch == ")":
            tokens.append(Token("RPAREN", ch))
            i += 1
            continue

        # Unknown character
        raise ValueError("Invalid character")

    # Insert implicit multiplication: NUM or RPAREN followed by NUM or LPAREN
    implicit = []
    for idx, tok in enumerate(tokens):
        implicit.append(tok)
        if tok.type in ("NUM", "RPAREN"):
            if idx + 1 < len(tokens):
                nxt = tokens[idx + 1]
                if nxt.type in ("NUM", "LPAREN"):
                    implicit.append(Token("OP", "*"))

    implicit.append(Token("END", ""))

    # Check unary + (not allowed)
    # Unary position: at start, after LPAREN, after OP
    prev_type = "START"
    for t in implicit:
        if t.type == "OP" and t.value == "+":
            if prev_type in ("START", "LPAREN", "OP"):
                raise ValueError("Unary + not allowed")
        if t.type not in ("END",):
            prev_type = t.type

    return implicit


# -----------------------------
# Parser / AST nodes
# -----------------------------
class NumNode:
    def __init__(self, value):
        self.value = value  # float

class BinOpNode:
    def __init__(self, op, left, right):
        self.op = op  # '+', '-', '*', '/'
        self.left = left
        self.right = right

class NegNode:
    def __init__(self, expr):
        self.expr = expr


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.current = self.tokens[self.pos]

    def advance(self):
        self.pos += 1
        if self.pos < len(self.tokens):
            self.current = self.tokens[self.pos]

    def expect(self, ttype):
        if self.current.type == ttype:
            self.advance()
        else:
            raise ValueError("Unexpected token")

    def parse(self):
        node = self.parse_expression()
        if self.current.type != "END":
            raise ValueError("Extra input")
        return node

    # expression -> term (('+' | '-') term)*
    def parse_expression(self):
        node = self.parse_term()
        while self.current.type == "OP" and self.current.value in ("+", "-"):
            op = self.current.value
            self.advance()
            right = self.parse_term()
            node = BinOpNode(op, node, right)
        return node

    # term -> factor (('*' | '/') factor)*
    def parse_term(self):
        node = self.parse_factor()
        while self.current.type == "OP" and self.current.value in ("*", "/"):
            op = self.current.value
            self.advance()
            right = self.parse_factor()
            node = BinOpNode(op, node, right)
        return node

    # factor -> '-' factor | primary
    def parse_factor(self):
        if self.current.type == "OP" and self.current.value == "-":
            self.advance()
            expr = self.parse_factor()
            return NegNode(expr)
        return self.parse_primary()

    # primary -> NUM | '(' expression ')'
    def parse_primary(self):
        if self.current.type == "NUM":
            val = float(self.current.value)
            self.advance()
            return NumNode(val)

        if self.current.type == "LPAREN":
            self.advance()
            node = self.parse_expression()
            if self.current.type != "RPAREN":
                raise ValueError("Missing closing parenthesis")
            self.advance()
            return node

        raise ValueError("Unexpected token in primary")


# -----------------------------
# Tree formatting
# -----------------------------
def format_tree(node):
    if isinstance(node, NumNode):
        # Display number literal as formatted value
        if node.value.is_integer():
            return str(int(node.value))
        else:
            return str(node.value)

    if isinstance(node, NegNode):
        return f"(neg {format_tree(node.expr)})"

    if isinstance(node, BinOpNode):
        return f"({node.op} {format_tree(node.left)} {format_tree(node.right)})"

    return "ERROR"


# -----------------------------
# Evaluation
# -----------------------------
def eval_node(node):
    if isinstance(node, NumNode):
        return node.value

    if isinstance(node, NegNode):
        return -eval_node(node.expr)

    if isinstance(node, BinOpNode):
        left = eval_node(node.left)
        right = eval_node(node.right)

        if node.op == "+":
            return left + right
        if node.op == "-":
            return left - right
        if node.op == "*":
            return left * right
        if node.op == "/":
            if right == 0:
                raise ZeroDivisionError("Division by zero")
            return left / right

    raise ValueError("Invalid node")


# -----------------------------
# Token string formatting
# -----------------------------
def format_tokens(tokens):
    parts = []
    for t in tokens:
        if t.type == "END":
            parts.append("[END]")
        else:
            parts.append(f"[{t.type}:{t.value}]")
    return " ".join(parts)


# -----------------------------
# Main interface
# -----------------------------
def evaluate_expression(expr):
    expr_stripped = expr.strip()
    if expr_stripped == "":
        raise ValueError("Empty expression")

    tokens = tokenize(expr_stripped)
    parser = Parser(tokens)
    tree = parser.parse()
    value = eval_node(tree)
    return tree, tokens, value


def format_result_value(val):
    if isinstance(val, float):
        if val.is_integer():
            return str(int(val))
        else:
            return f"{val:.4f}".rstrip("0").rstrip(".")
    return str(val)


def evaluate_file(input_path: str) -> list[dict]:
    results = []

    base_dir = os.path.dirname(os.path.abspath(input_path))
    output_path = os.path.join(base_dir, "output.txt")

    with open(input_path, "r") as f:
        lines = f.readlines()

    out_lines = []

    for line in lines:
        original = line.rstrip("\n")
        entry = {"input": original, "tree": "", "tokens": "", "result": ""}

        try:
            tree, tokens, value = evaluate_expression(original)
            tree_str = format_tree(tree)
            tokens_str = format_tokens(tokens)
            result_str = format_result_value(value)

            entry["tree"] = tree_str
            entry["tokens"] = tokens_str
            entry["result"] = float(result_str) if "." in result_str else float(result_str)

            out_lines.append(f"Input: {original}")
            out_lines.append(f"Tree: {tree_str}")
            out_lines.append(f"Tokens: {tokens_str}")
            out_lines.append(f"Result: {result_str}")
            out_lines.append("")

        except Exception:
            entry["tree"] = "ERROR"
            entry["tokens"] = "ERROR"
            entry["result"] = "ERROR"

            out_lines.append(f"Input: {original}")
            out_lines.append("Tree: ERROR")
            out_lines.append("Tokens: ERROR")
            out_lines.append("Result: ERROR")
            out_lines.append("")

        results.append(entry)

    with open(output_path, "w") as f:
        f.write("\n".join(out_lines).rstrip() + "\n")

    return results


if __name__ == "__main__":
    # Simple manual test runner (optional)
    path = input("Enter input file path: ").strip()
    evaluate_file(path)
    print("output.txt written.")
