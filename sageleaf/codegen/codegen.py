from pathlib import Path

from sageleaf.parse import ast
from sageleaf.parse.lexer import Lexer
from sageleaf.parse.parser import Parser
from sageleaf.parse.tokens import SourceSpan
from sageleaf.typecheck.typechecker import TypeChecker


class CodeGenError(Exception):
    def __init__(self, message: str, span: SourceSpan):
        error = f"[Error] {message} at "
        print(error, end="")
        span.print()
        super().__init__(error)


class CodeGenerator:
    def __init__(self, program: ast.Program, lib: bool = False):
        self.program = program
        self.code = ""
        self.indent_level = 0
        self.lib = lib

    def indent(self, level: int = 1):
        self.indent_level += level

    def dedent(self, level: int = 1):
        self.indent_level -= level

    def add(self, s: str = "", indent: bool = True, newline: bool = True):
        if indent:
            self.code += "    " * self.indent_level
        self.code += s
        if newline:
            self.code += "\n"

    def type_to_c_type(self, t: ast.Type | None) -> str:
        match t:
            case ast.I8():
                return "int8_t"
            case ast.I16():
                return "int16_t"
            case ast.I32():
                return "int32_t"
            case ast.I64():
                return "int64_t"
            case ast.U8():
                return "uint8_t"
            case ast.U16():
                return "uint16_t"
            case ast.U32():
                return "uint32_t"
            case ast.U64():
                return "uint64_t"
            case ast.Usize():
                return "size_t"
            case ast.F32():
                return "float"
            case ast.F64():
                return "double"
            case ast.Bool():
                return "bool"
            case None:
                return "void"
            case _:
                raise CodeGenError(f"Unknown type {t}", t.span)

    def generate(self) -> str:
        if not self.lib:
            self.add("// --- Sageleaf Runtime ---")
            with open("runtime/core.c") as f:
                self.add(f.read().strip())
            self.add()

            self.add("// --- Sageleaf Library ---")
            with open("runtime/lib.sl") as f:
                lib_source = f.read().strip()
            lexer = Lexer(lib_source, Path("runtime/lib.sl"))
            tokens = lexer.tokenize()
            parser = Parser(tokens)
            ast = parser.parse()
            typechecker = TypeChecker(ast)
            typechecker.check()
            codegen = CodeGenerator(ast, lib=True)
            self.add(codegen.generate(), newline=False)

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

    def function_declaration(self, f: ast.FunctionDef):
        params: list[str] = []
        for p in f.params:
            params.append(self.type_to_c_type(p.type_annotation) + " sl_" + p.name)

        self.add(
            f"{self.type_to_c_type(f.return_type)} sl_{f.name}({', '.join(params)});"
        )

    def function_definition(self, f: ast.FunctionDef):
        params: list[str] = []
        for p in f.params:
            params.append(self.type_to_c_type(p.type_annotation) + " sl_" + p.name)

        self.add(
            f"{self.type_to_c_type(f.return_type)} sl_{f.name}({', '.join(params)})"
            + " {"
        )
        self.indent()
        for s in f.body:
            self.statement(s)
        self.dedent()
        self.add("}")

    def statement(self, s: ast.Statement):
        match s:
            case ast.NativeBlock():
                self.native(s)
            case ast.ReturnStatement():
                self.return_statement(s)
            case _:
                raise CodeGenError(f"Unknown statement {s}", s.span)

    def native(self, n: ast.NativeBlock):
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

    def return_statement(self, r: ast.ReturnStatement):
        match r.value:
            case None:
                self.add("return;")
            case expr:
                self.add(f"return {self.expression(expr)};")

    def expression(self, e: ast.Expression) -> str:
        match e:
            case ast.IntLiteral():
                return f"{e.value}"
            case ast.FloatLiteral():
                return f"{e.value}"
            case ast.BoolLiteral():
                return "true" if e.value else "false"
            case _:
                raise CodeGenError(f"Unsupported expression {e}", e.span)
