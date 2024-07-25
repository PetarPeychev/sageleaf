import os
import sys


def main():
    # read file
    if len(sys.argv) != 2:
        print("Usage: python compiler.py <file>")
        sys.exit(1)

    file_name = sys.argv[1]
    pname = file_name[:-3]
    with open(file_name, "r") as f:
        code = f.read()
    print(f"{code}", "\n")

    # tokenize
    i = 0
    tokens = []
    while i < len(code):
        c = code[i]

        if c in [" ", "\n", "\t"]:
            i += 1
            continue
        elif c == "(":
            tokens.append({"type": "lparen"})
            i += 1
            continue
        elif c == ")":
            tokens.append({"type": "rparen"})
            i += 1
            continue
        elif c == "{":
            tokens.append({"type": "lbrace"})
            i += 1
            continue
        elif c == "}":
            tokens.append({"type": "rbrace"})
            i += 1
            continue
        elif c == ";":
            tokens.append({"type": "semi"})
            i += 1
            continue
        elif c == ":":
            tokens.append({"type": "colon"})
            i += 1
            continue
        elif c == ",":
            tokens.append({"type": "comma"})
            i += 1
            continue
        elif c == "+":
            tokens.append({"type": "+"})
            i += 1
            continue
        elif c == "-":
            tokens.append({"type": "-"})
            i += 1
            continue
        elif c == "*":
            tokens.append({"type": "*"})
            i += 1
            continue
        elif c == "/":
            tokens.append({"type": "/"})
            i += 1
            continue
        elif c.isalpha():
            name = ""
            while i < len(code):
                c = code[i]
                if c.isalnum():
                    name += c
                    i += 1
                else:
                    break
            if name in ["fn", "return"]:
                tokens.append({"type": name})
            else:
                tokens.append({"type": "name", "value": name})
            continue
        elif c.isdigit():
            number = ""
            while i < len(code):
                c = code[i]
                if c.isdigit():
                    number += c
                    i += 1
                else:
                    break
            tokens.append({"type": "int", "value": int(number)})
            continue

    print(tokens, "\n")

    # parse
    ast = []
    while len(tokens) > 0:
        token = tokens.pop(0)
        if token["type"] == "fn":
            fn = {"type": "fn", "name": tokens.pop(0)["value"], "args": [], "body": []}
            tokens.pop(0)  # (
            t = tokens.pop(0)
            if t["type"] == "name":
                fn["args"].append(t["value"])
                while True:
                    t = tokens.pop(0)  # , or )
                    if t["type"] == "comma":
                        t = tokens.pop(0)
                        if t["type"] == "name":
                            fn["args"].append(t["value"])
                    else:
                        break
            tokens.pop(0)  # {

            # function body
            while True:
                t = tokens.pop(0)
                if t["type"] == "rbrace":
                    break
                elif t["type"] == "return":
                    expr = parse_expr(tokens)
                    tokens.pop(0)  # ;
                    fn["body"].append({"type": "return", "value": expr})
            ast.append(fn)
    print(ast, "\n")

    ast_to_graphviz(ast, pname)

    # codegen
    asm = ""
    asm += "section .text\n"
    asm += "global _start\n"
    asm += "\n"

    for fn in ast:
        name = "_start" if fn["name"] == "main" else fn["name"]
        asm += f"{name}:\n"
        for stmt in fn["body"]:
            if stmt["type"] == "return":
                if name == "_start":
                    asm += f"\tmov rax, 60\n"
                    asm += f"\tmov rdi, {stmt['value']['value']}\n"
                    asm += f"\tsyscall\n"
                else:
                    asm += f"\tmov rax, {stmt['value']['value']}\n"
                    asm += f"\tret\n"
    print(asm)

    # write asm to file
    with open(f"{pname}.asm", "w") as f:
        f.write(asm)

    # compile to machine code
    os.system(f"nasm -f elf64 -o {pname}.o {pname}.asm")
    os.system(f"rm {pname}.asm")

    # link
    os.system(f"ld -o {pname} {pname}.o")
    os.system(f"rm {pname}.o")


def ast_to_graphviz(ast: list[dict], filename: str):
    labels, arrows = _ast_to_graphviz(ast)


def parse_expr(tokens: list[dict]) -> dict:
    return parse_add_sub(tokens)


def parse_add_sub(tokens: list[dict]) -> dict:
    left = parse_mul_div(tokens)

    while tokens[0]["type"] in ["+", "-"]:
        operator = tokens.pop(0)["type"]
        right = parse_mul_div(tokens)
        left = {
            "type": operator,
            "left": left,
            "right": right,
        }

    return left


def parse_mul_div(tokens: list[dict]) -> dict:
    left = parse_primary(tokens)

    while tokens[0]["type"] in ["*", "/"]:
        operator = tokens.pop(0)["type"]
        right = parse_primary(tokens)
        left = {
            "type": operator,
            "left": left,
            "right": right,
        }

    return left


def parse_primary(tokens: list[dict]) -> dict:
    if tokens[0]["type"] == "int":
        return {"type": "int", "value": tokens.pop(0)["value"]}
    elif tokens[0]["type"] == "(":
        expr = parse_expr(tokens)
        tokens.pop(0)  # )
        return expr
    else:
        raise Exception(f"Invalid expression: {tokens[0]['type']}")


if __name__ == "__main__":
    main()
