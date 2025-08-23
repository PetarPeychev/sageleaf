from sageleaf.parse import ast
from sageleaf.parse.tokens import SourceSpan


class TypeCheckError(Exception):
    def __init__(self, message: str, span: SourceSpan):
        error = f"[Error] {message} at "
        print(error, end="")
        span.print()
        super().__init__(error)


class TypeChecker:
    def __init__(self, program: ast.Program):
        self.program = program

    def check(self):
        self.collect_definitions()

        for s in self.program.statements:
            match s:
                case ast.FunctionDef():
                    self.check_function_def(s)
                case _:
                    pass

    def collect_definitions(self):
        self.program.functions = {}
        for s in self.program.statements:
            match s:
                case ast.FunctionDef():
                    if s.name in self.program.functions:
                        raise TypeCheckError(
                            f"Duplicate function definition '{s.name}'",
                            s.name_token.span,
                        )
                    self.program.functions[s.name] = s
                case _:
                    pass

    def check_function_def(self, function_def: ast.FunctionDef):
        for s in function_def.body:
            match s:
                case ast.ReturnStatement():
                    self.check_return_statement(s, function_def.return_type)
                case ast.ExpressionStatement():
                    self.check_expression(s.expression, None)
                case _:
                    pass

    def check_return_statement(self, r: ast.ReturnStatement, t: ast.Type | None):
        assert r.return_token
        if t:
            r.type = t
            if not r.value:
                raise TypeCheckError(
                    "Return statement must have a value", r.return_token.span
                )
            self.check_expression(r.value, r.type)
        elif r.value:
            raise TypeCheckError(
                "Return statement must not have a value", r.return_token.span
            )

    def check_expression(self, e: ast.Expression, t: ast.Type | None):
        match e:
            case ast.IntLiteral():
                if not t or isinstance(t, ast.NumberType):
                    e.type = t
                else:
                    raise TypeCheckError(
                        f"Expected {self.type_to_name(t)}, got integer literal", e.span
                    )
            case ast.FloatLiteral():
                if not t or isinstance(t, ast.NumberType):
                    e.type = t
                else:
                    raise TypeCheckError(
                        f"Expected {self.type_to_name(t)}, got float literal", e.span
                    )
            case ast.BoolLiteral():
                if not t or isinstance(t, ast.Bool):
                    e.type = t
                else:
                    raise TypeCheckError(
                        f"Expected {self.type_to_name(t)}, got bool literal", e.span
                    )
            case ast.FunctionCall():
                assert self.program.functions
                if not t or self.program.functions[e.name].return_type == t:
                    e.type = t
                    if len(e.args) != len(self.program.functions[e.name].params):
                        raise TypeCheckError(
                            f"Expected {len(self.program.functions[e.name].params)} "
                            f"arguments, got {len(e.args)}",
                            e.name_token.span,
                        )
                    for arg, param in zip(
                        e.args, self.program.functions[e.name].params, strict=True
                    ):
                        self.check_expression(arg, param.type_annotation)
                else:
                    raise TypeCheckError(
                        f"Expected {self.type_to_name(t)}, got function call",
                        e.name_token.span,
                    )
            case _:
                raise TypeCheckError(f"Unsupported expression {e.kind}", e.span)

    def type_to_name(self, t: ast.Type) -> str:
        match t:
            case ast.I8():
                return "i8"
            case ast.I16():
                return "i16"
            case ast.I32():
                return "i32"
            case ast.I64():
                return "i64"
            case ast.U8():
                return "u8"
            case ast.U16():
                return "u16"
            case ast.U32():
                return "u32"
            case ast.U64():
                return "u64"
            case ast.Usize():
                return "usize"
            case ast.F32():
                return "f32"
            case ast.F64():
                return "f64"
            case ast.Bool():
                return "bool"
            case ast.Str():
                return "str"
            case _:
                raise TypeCheckError(f"Unknown type {t}", t.span)
