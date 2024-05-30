class Lexer:
    def __init__(self, code: str):
        self.input = code
        self.pos = 0

        self.keywords = {
            "fn": {"type": "fn"},
            "return": {"type": "return"},
            "i32": {"type": "i32"},
        }

    def tokenize(self) -> list[dict]:
        tokens: list[dict] = []
        while self.pos < len(self.input):
            if self.input[self.pos].isspace():
                self.pos += 1
            elif self.input[self.pos] == "(":
                tokens.append({"type": "("})
                self.pos += 1
            elif self.input[self.pos] == ")":
                tokens.append({"type": ")"})
                self.pos += 1
            elif self.input[self.pos] == "{":
                tokens.append({"type": "{"})
                self.pos += 1
            elif self.input[self.pos] == "}":
                tokens.append({"type": "}"})
                self.pos += 1
            elif self.input[self.pos] == ",":
                tokens.append({"type": ","})
                self.pos += 1
            elif self.input[self.pos] == ":":
                tokens.append({"type": ":"})
                self.pos += 1
            elif self.input[self.pos] == ";":
                tokens.append({"type": ";"})
                self.pos += 1
            elif self.input[self.pos] == '"':
                self.pos += 1
                value = ""
                while self.input[self.pos] != '"':
                    value += self.input[self.pos]
                    self.pos += 1
                tokens.append({"type": "string", "value": value})
                self.pos += 1
            elif self.input[self.pos].isdigit():
                value = ""
                while self.input[self.pos].isdigit():
                    value += self.input[self.pos]
                    self.pos += 1
                tokens.append({"type": "integer", "value": int(value)})
            elif self.input[self.pos].isalpha():
                value = ""
                while self.input[self.pos].isalnum():
                    value += self.input[self.pos]
                    self.pos += 1
                if value in self.keywords:
                    tokens.append(self.keywords[value])
                else:
                    tokens.append({"type": "id", "value": value})
            else:
                raise Exception("Invalid character")
        return tokens
