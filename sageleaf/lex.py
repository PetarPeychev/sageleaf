from sageleaf.tokens import TokenType as TT
from sageleaf.tokens import Token


class Lexer:
    def __init__(self, code: str):
        self.input = code
        self.pos = 0

        self.keywords = {
            "fn": TT.FN,
            "return": TT.RETURN,
            "i32": TT.I32,
        }

    def tokenize(self) -> list[Token]:
        tokens: list[Token] = []
        while self.pos < len(self.input):
            if self.input[self.pos].isspace():
                self.pos += 1
            elif self.input[self.pos] == "(":
                tokens.append(Token(TT.LPAREN))
                self.pos += 1
            elif self.input[self.pos] == ")":
                tokens.append(Token(TT.RPAREN))
                self.pos += 1
            elif self.input[self.pos] == "{":
                tokens.append(Token(TT.LBRACE))
                self.pos += 1
            elif self.input[self.pos] == "}":
                tokens.append(Token(TT.RBRACE))
                self.pos += 1
            elif self.input[self.pos] == ",":
                tokens.append(Token(TT.COMMA))
                self.pos += 1
            elif self.input[self.pos] == ":":
                tokens.append(Token(TT.COLON))
                self.pos += 1
            elif self.input[self.pos] == ";":
                tokens.append(Token(TT.SEMICOLON))
                self.pos += 1
            elif self.input[self.pos] == '"':
                self.pos += 1
                value = ""
                while self.input[self.pos] != '"':
                    value += self.input[self.pos]
                    self.pos += 1
                tokens.append(Token(TT.STR_LIT, value))
                self.pos += 1
            elif self.input[self.pos].isdigit():
                value = ""
                while self.input[self.pos].isdigit():
                    value += self.input[self.pos]
                    self.pos += 1
                tokens.append(Token(TT.INT_LIT, int(value)))
            elif self.input[self.pos].isalpha():
                value = ""
                while self.input[self.pos].isalnum():
                    value += self.input[self.pos]
                    self.pos += 1
                if value in self.keywords:
                    tokens.append(Token(self.keywords[value]))
                else:
                    tokens.append(Token(TT.IDENT, value))
            else:
                raise Exception(f"Invalid character {self.input[self.pos]}")
        return tokens
