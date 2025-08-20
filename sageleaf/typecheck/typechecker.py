from sageleaf.parse.ast import (
    FunctionDef,
    Program,
)
from sageleaf.parse.tokens import SourceSpan


class TypeCheckError(Exception):
    def __init__(self, message: str, span: SourceSpan):
        span.print()
        super().__init__(f"Type check error: {message}")


class TypeChecker:
    def __init__(self, program: Program):
        self.program = program

    def check(self):
        self.collect_definitions()

    def collect_definitions(self):
        self.program.functions = {}
        for s in self.program.statements:
            match s:
                case FunctionDef():
                    if s.name in self.program.functions:
                        raise TypeCheckError(
                            f"Duplicate function definition: {s.name}",
                            s.name_token.span,
                        )
                    self.program.functions[s.name] = s
                case _:
                    pass
