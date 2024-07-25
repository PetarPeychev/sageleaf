from enum import StrEnum


class TT(StrEnum):
    # Keywords
    FN = "fn"
    # IF = "if"
    # ELIF = "elif"
    # ELSE = "else"
    RETURN = "return"

    # Types
    I64 = "i64"

    # Punctuation
    COMMA = ","
    COLON = ":"
    SEMICOLON = ";"
    # ASSIGN = "="
    LPAREN = "("
    RPAREN = ")"
    LBRACE = "{"
    RBRACE = "}"

    # Arithmetic Operators
    PLUS = "+"
    MINUS = "-"
    MUL = "*"
    DIV = "/"

    # Comparison Operators
    # IS = "is"
    # LT = "<"
    # GT = ">"
    # LE = "<="
    # GE = ">="

    # Logical Operators
    # AND = "and"
    # OR = "or"
    # NOT = "not"

    # Literals
    NAME = "name"
    # STR_LIT = "str"
    INT_LIT = "int"
    # TRUE = "true"
    # FALSE = "false"


class T:
    tt: TT
    val: int | str | None

    def __init__(self, tt: TT, val: int | str | None = None):
        self.tt = tt
        self.val = val

    def __str__(self):
        value = ""
        if self.val is not None:
            value = f"({self.val})"
        return f"{self.tt}{value}"

    def __repr__(self):
        return str(self)


class Lexer:
    def __init__(self, code: str):
        self.input = code
        self.pos = 0

        self.keywords = {
            "fn": TT.FN,
            "i64": TT.I64,
            "return": TT.RETURN,
        }

    def tokenize(self) -> list[T]:
        toks: list[T] = []
        while self.pos < len(self.input):
            if self.input[self.pos].isspace():
                self.pos += 1
            elif self.input[self.pos] == "(":
                toks.append(T(TT.LPAREN))
                self.pos += 1
            elif self.input[self.pos] == ")":
                toks.append(T(TT.RPAREN))
                self.pos += 1
            elif self.input[self.pos] == "{":
                toks.append(T(TT.LBRACE))
                self.pos += 1
            elif self.input[self.pos] == "}":
                toks.append(T(TT.RBRACE))
                self.pos += 1
            elif self.input[self.pos] == ",":
                toks.append(T(TT.COMMA))
                self.pos += 1
            elif self.input[self.pos] == ":":
                toks.append(T(TT.COLON))
                self.pos += 1
            elif self.input[self.pos] == ";":
                toks.append(T(TT.SEMICOLON))
                self.pos += 1
            # elif self.input[self.pos] == "=":
            #     toks.append(T(TT.ASSIGN))
            #     self.pos += 1
            elif self.input[self.pos] == "+":
                toks.append(T(TT.PLUS))
                self.pos += 1
            elif self.input[self.pos] == "-":
                toks.append(T(TT.MINUS))
                self.pos += 1
            elif self.input[self.pos] == "*":
                toks.append(T(TT.MUL))
                self.pos += 1
            elif self.input[self.pos] == "/":
                toks.append(T(TT.DIV))
                self.pos += 1
            # elif self.input[self.pos] == ">":
            #     toks.append(T(TT.GT))
            #     self.pos += 1
            # elif self.input[self.pos] == '"':
            #     self.pos += 1
            #     value = ""
            #     while self.input[self.pos] != '"':
            #         value += self.input[self.pos]
            #         self.pos += 1
            #     toks.append(T(TT.STR_LIT, value))
            #     self.pos += 1
            elif self.input[self.pos].isdigit():
                value = ""
                while self.input[self.pos].isdigit():
                    value += self.input[self.pos]
                    self.pos += 1
                toks.append(T(TT.INT_LIT, int(value)))
            elif self.input[self.pos].isalpha():
                value = ""
                while self.input[self.pos].isalnum():
                    value += self.input[self.pos]
                    self.pos += 1
                if value in self.keywords:
                    toks.append(T(self.keywords[value]))
                else:
                    toks.append(T(TT.NAME, value))
            else:
                raise ValueError(f"Invalid character {self.input[self.pos]}")
        return toks
