from sageleaf.parse.ast import (
    F32,
    F64,
    I8,
    I16,
    I32,
    I64,
    U8,
    U16,
    U32,
    U64,
    Bool,
    FunctionDef,
    Program,
    Type,
    Usize,
)
from sageleaf.parse.tokens import SourceSpan


class CodeGenError(Exception):
    def __init__(self, message: str, span: SourceSpan):
        error = f"[Error] {message} at "
        print(error, end="")
        span.print()
        super().__init__(error)


class CodeGenerator:
    def __init__(self, program: Program):
        self.program = program
        self.code = ""

    def generate(self) -> str:
        self.code += "// --- Sageleaf Runtime ---\n\n"
        with open("runtime/core.c") as f:
            self.code += f.read().strip()

        self.code += "\n\n// --- Sageleaf User Program ---\n\n"

        assert self.program.functions
        for f in self.program.functions.values():
            self.function_declaration(f)

        self.code += "\n"

        for f in self.program.functions.values():
            self.function_definition(f)

        return self.code

    def function_declaration(self, f: FunctionDef):
        self.code += self.type_to_c_type(f.return_type)
        self.code += " "
        self.code += f.name
        self.code += "("

        for i, p in enumerate(f.params):
            self.code += self.type_to_c_type(p.type_annotation)
            self.code += " "
            self.code += p.name
            if i < len(f.params) - 1:
                self.code += ", "

        self.code += ");\n"

    def function_definition(self, f: FunctionDef):
        self.code += self.type_to_c_type(f.return_type)
        self.code += " "
        self.code += f.name
        self.code += "("

        for i, p in enumerate(f.params):
            self.code += self.type_to_c_type(p.type_annotation)
            self.code += " "
            self.code += p.name
            if i < len(f.params) - 1:
                self.code += ", "

        self.code += ") {\n"
        # TODO: Implement function body
        self.code += "}\n"

    def type_to_c_type(self, t: Type | None) -> str:
        match t:
            case I8():
                return "int8_t"
            case I16():
                return "int16_t"
            case I32():
                return "int32_t"
            case I64():
                return "int64_t"
            case U8():
                return "uint8_t"
            case U16():
                return "uint16_t"
            case U32():
                return "uint32_t"
            case U64():
                return "uint64_t"
            case Usize():
                return "size_t"
            case F32():
                return "float"
            case F64():
                return "double"
            case Bool():
                return "bool"
            case None:
                return "void"
            case _:
                raise CodeGenError(f"Unknown type {t}", t.span)
