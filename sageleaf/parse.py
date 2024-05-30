def log(func):
    def new_func(*args, **kwargs):
        self_arg = args[0] # First argument is the self
        print(self_arg.tokens[self_arg.pos])
        return func(*args, **kwargs)
    return new_func

class Parser:
    def __init__(self, tokens: list[dict]):
        self.tokens = tokens
        self.pos = 0
        self.precedence: dict[str, int] = {}

    def consume(self, type: str) -> dict:
        if self.tokens[self.pos]["type"] == type:
            self.pos += 1
            return self.tokens[self.pos - 1]
        else:
            raise Exception(f"Expected {type}, got {self.tokens[self.pos]}")

    def parse(self) -> dict:
        program: dict = {
            "type": "program",
            "statements": [],
        }

        while self.pos < len(self.tokens):
            statement = self._parse_top_level()
            program["statements"].append(statement)

        return program

    def _parse_top_level(self) -> dict:
        if self.tokens[self.pos]["type"] == "fn":
            return self._parse_function_definition()
        else:
            raise Exception("Invalid statement")

    def _parse_function_definition(self) -> dict:
        self.consume("fn")
        name = self.consume("id")["value"]
        self.consume("(")
        self.consume(")")
        self.consume(":")
        return_type = self.consume("i32")
        body: list[dict] = []
        self.consume("{")
        while self.tokens[self.pos]["type"] != "}":
            body.append(self._parse_statement())
        self.consume("}")

        return {
            "type": "function_definition",
            "name": name,
            "parameters": [],
            "return_type": return_type,
            "body": body,
        }

    def _parse_statement(self) -> dict:
        if self.tokens[self.pos]["type"] == "return":
            return self._parse_return_statement()
        else:
            return self._parse_expression_statement()

    def _parse_return_statement(self) -> dict:
        self.consume("return")
        value = self._parse_expression()
        self.consume(";")

        return {
            "type": "return",
            "value": value,
        }

    def _parse_expression_statement(self) -> dict:
        expr = self._parse_expression()
        self.consume(";")

        return {
            "type": "expression_statement",
            "expression": expr,
        }

    def _parse_expression(self) -> dict:
        if self.tokens[self.pos]["type"] == "id":
            function_name = self.consume("id")["value"]
            self.consume("(")
            arguments = []
            if self.tokens[self.pos]["type"] != ")":
                argument = self._parse_expression()
                arguments.append(argument)
            while self.tokens[self.pos]["type"] != ")":
                self.consume(",")
                argument = self._parse_expression()
                arguments.append(argument)
            self.consume(")")
            return {
                "type": "function_call",
                "name": function_name,
                "arguments": arguments,
            }
        elif self.tokens[self.pos]["type"] == "string":
            return {
                "type": "string",
                "value": self.consume("string")["value"],
            }
        elif self.tokens[self.pos]["type"] == "integer":
            return {
                "type": "integer",
                "value": self.consume("integer")["value"],
            }
        else:
            raise Exception("Invalid expression")
