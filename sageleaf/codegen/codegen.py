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
    NativeBlock,
    Program,
    Statement,
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
        self.indent_level = 0

    def indent(self, level: int = 1):
        self.indent_level += level

    def dedent(self, level: int = 1):
        self.indent_level -= level

    def add(self, s: str = "", indent: bool = True):
        if indent:
            self.code += "    " * self.indent_level + s + "\n"
        else:
            self.code += s + "\n"

    def generate(self) -> str:
        self.add("// --- Sageleaf Runtime ---")
        with open("runtime/core.c") as f:
            self.add(f.read().strip())
        self.add()

        self.add("// --- Sageleaf User Program ---")

        assert self.program.functions
        for f in self.program.functions.values():
            if f.name != "main":
                self.function_declaration(f)
                self.add()

        for f in self.program.functions.values():
            self.function_definition(f)
            self.add()

        return self.code

    def function_declaration(self, f: FunctionDef):
        params: list[str] = []
        for p in f.params:
            params.append(self.type_to_c_type(p.type_annotation) + " " + p.name)

        self.add(
            f"{self.type_to_c_type(f.return_type)} sl_{f.name}({', '.join(params)});"
        )

    def function_definition(self, f: FunctionDef):
        params: list[str] = []
        for p in f.params:
            params.append(self.type_to_c_type(p.type_annotation) + " " + p.name)

        self.add(
            f"{self.type_to_c_type(f.return_type)} sl_{f.name}({', '.join(params)})"
            + " {"
        )
        self.indent()
        for s in f.body:
            self.statement(s)
        self.dedent()
        self.add("}")

    def statement(self, s: Statement):
        match s:
            case NativeBlock():
                self.native(s)
            case _:
                raise CodeGenError(f"Unknown statement {s}", s.span)

    def native(self, n: NativeBlock):
        content = n.content
        if content.strip():
            lines = content.splitlines()

            while lines and not lines[0].strip():
                lines.pop(0)
            while lines and not lines[-1].strip():
                lines.pop()

            non_empty_lines = [line for line in lines if line.strip()]
            if non_empty_lines:
                min_indent = min(
                    len(line) - len(line.lstrip()) for line in non_empty_lines
                )
                for line in lines:
                    if line.strip():
                        if len(line) >= min_indent:
                            dedented = line[min_indent:]
                        else:
                            dedented = line.lstrip()
                        self.add(dedented)
                    else:
                        self.add("")

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
