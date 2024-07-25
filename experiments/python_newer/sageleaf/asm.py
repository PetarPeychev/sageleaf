from sageleaf.ast import Program


@dataclass
class Asm:
    body: list[Instr]


class Codegen:
    def __init__(self, ast: Program):
        self.ast = ast

    def codegen(self) -> str:
        return ""
