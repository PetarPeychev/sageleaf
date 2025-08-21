from __future__ import annotations

from pathlib import Path
from typing import Literal

from pydantic import BaseModel

from sageleaf.parse.tokens import SourceSpan, Token


class ASTNode(BaseModel):
    span: SourceSpan

    def print(self) -> str:
        try:
            with open(self.span.file_path) as f:
                lines = f.readlines()

            start_context_line = max(0, self.span.start_line - 2)
            end_context_line = min(len(lines), self.span.end_line + 1)
            context_lines = lines[start_context_line:end_context_line]

            class_name = self.__class__.__name__
            result = (
                f"{class_name} at {self.span.file_path.name} "
                f"{self.span.start_line}:{self.span.start_column}-"
                f"{self.span.end_line}:{self.span.end_column}\n"
            )

            for i, line in enumerate(context_lines):
                line_num = start_context_line + i + 1
                line_content = line.rstrip("\n")
                result += f"{line_num:4} | {line_content}\n"

                if self.span.start_line <= line_num <= self.span.end_line:

                    def create_underline(
                        start_col: int, end_col: int, content: str
                    ) -> str:
                        """Create underline that skips whitespace"""
                        underline = ""
                        for i in range(start_col - 1, min(end_col - 1, len(content))):
                            if i < len(content) and content[i] in " \t":
                                underline += " "
                            else:
                                underline += "^"
                        return underline if underline.strip() else "^"

                    if self.span.start_line == self.span.end_line:
                        spaces = " " * (6 + self.span.start_column)
                        underline = create_underline(
                            self.span.start_column, self.span.end_column, line_content
                        )
                        result += f"{spaces}{underline}\n"
                    elif line_num == self.span.start_line:
                        spaces = " " * (6 + self.span.start_column)
                        underline = create_underline(
                            self.span.start_column, len(line_content) + 1, line_content
                        )
                        result += f"{spaces}{underline}\n"
                    elif line_num == self.span.end_line:
                        spaces = " " * 7
                        underline = create_underline(
                            1, self.span.end_column, line_content
                        )
                        result += f"{spaces}{underline}\n"
                    else:
                        spaces = " " * 7
                        underline = create_underline(
                            1, len(line_content) + 1, line_content
                        )
                        result += f"{spaces}{underline}\n"

            return result.rstrip()

        except (OSError, IndexError):
            class_name = self.__class__.__name__
            return (
                f"{class_name} at {self.span.file_path}:"
                f"{self.span.start_line}:{self.span.start_column}-"
                f"{self.span.end_line}:{self.span.end_column}"
            )


class Program(ASTNode):
    statements: list[TopLevelStatement]
    functions: dict[str, FunctionDef] | None = None


type TopLevelStatement = (
    FunctionDef
    | NativeBlock
    | StructDef
    | UnionDef
    | ImportStatement
    | ConstDeclaration
    | VarDeclaration
)


class FunctionDef(ASTNode):
    kind: Literal["FunctionDef"] = "FunctionDef"
    name: str
    params: list[Parameter]
    return_type: Type | None
    body: list[Statement]

    name_token: Token


class Parameter(ASTNode):
    kind: Literal["Parameter"] = "Parameter"
    name: str
    type_annotation: Type


class StructDef(ASTNode):
    kind: Literal["StructDef"] = "StructDef"
    name: str
    type_params: list[str]
    fields: list[StructField]


class StructField(ASTNode):
    kind: Literal["StructField"] = "StructField"
    name: str
    type_annotation: Type


class UnionDef(ASTNode):
    kind: Literal["UnionDef"] = "UnionDef"
    name: str
    type_params: list[str]
    variants: list[UnionVariant]


class UnionVariant(ASTNode):
    kind: Literal["UnionVariant"] = "UnionVariant"
    name: str
    payload: Type | None


class ImportStatement(ASTNode):
    kind: Literal["ImportStatement"] = "ImportStatement"
    package: str
    items: list[str] | None
    alias: str | None


class NativeBlock(ASTNode):
    kind: Literal["NativeBlock"] = "NativeBlock"
    content: str


type Type = (
    I8
    | I16
    | I32
    | I64
    | U8
    | U16
    | U32
    | U64
    | Usize
    | F32
    | F64
    | Bool
    | Str
    | PointerType
    | GenericType
    | CustomType
    | AnonymousUnionType
    | AnonymousStructType
)


class NumberType(BaseModel):
    pass


class I8(ASTNode, NumberType):
    kind: Literal["I8"] = "I8"


class I16(ASTNode, NumberType):
    kind: Literal["I16"] = "I16"


class I32(ASTNode, NumberType):
    kind: Literal["I32"] = "I32"


class I64(ASTNode, NumberType):
    kind: Literal["I64"] = "I64"


class U8(ASTNode, NumberType):
    kind: Literal["U8"] = "U8"


class U16(ASTNode, NumberType):
    kind: Literal["U16"] = "U16"


class U32(ASTNode, NumberType):
    kind: Literal["U32"] = "U32"


class U64(ASTNode, NumberType):
    kind: Literal["U64"] = "U64"


class Usize(ASTNode, NumberType):
    kind: Literal["Usize"] = "Usize"


class F32(ASTNode, NumberType):
    kind: Literal["F32"] = "F32"


class F64(ASTNode, NumberType):
    kind: Literal["F64"] = "F64"


class Bool(ASTNode):
    kind: Literal["Bool"] = "Bool"


class Str(ASTNode):
    kind: Literal["Str"] = "Str"


class PointerType(ASTNode):
    kind: Literal["PointerType"] = "PointerType"
    target: Type


class GenericType(ASTNode):
    kind: Literal["GenericType"] = "GenericType"
    name: str


class CustomType(ASTNode):
    kind: Literal["CustomType"] = "CustomType"
    name: str
    type_args: list[Type]


class AnonymousUnionType(ASTNode):
    kind: Literal["AnonymousUnionType"] = "AnonymousUnionType"
    variants: list[UnionVariant]


class AnonymousStructType(ASTNode):
    kind: Literal["AnonymousStructType"] = "AnonymousStructType"
    fields: list[StructField]


type Statement = (
    ReturnStatement
    | VarDeclaration
    | ConstDeclaration
    | Assignment
    | ExpressionStatement
    | IfStatement
    | WhileStatement
    | ForStatement
    | BreakStatement
    | ContinueStatement
    | MatchStatement
    | NativeBlock
)


class ReturnStatement(ASTNode):
    kind: Literal["ReturnStatement"] = "ReturnStatement"
    value: Expression | None
    type: Type | None = None
    return_token: Token | None = None


class VarDeclaration(ASTNode):
    kind: Literal["VarDeclaration"] = "VarDeclaration"
    name: str
    type_annotation: Type | None
    value: Expression


class ConstDeclaration(ASTNode):
    kind: Literal["ConstDeclaration"] = "ConstDeclaration"
    name: str
    type_annotation: Type | None
    value: Expression


class Assignment(ASTNode):
    kind: Literal["Assignment"] = "Assignment"
    target: Expression
    value: Expression


class ExpressionStatement(ASTNode):
    kind: Literal["ExpressionStatement"] = "ExpressionStatement"
    expression: Expression


class IfStatement(ASTNode):
    kind: Literal["IfStatement"] = "IfStatement"
    condition: Expression
    then_body: list[Statement]
    elif_branches: list[ElifBranch]
    else_body: list[Statement] | None


class ElifBranch(ASTNode):
    kind: Literal["ElifBranch"] = "ElifBranch"
    condition: Expression
    body: list[Statement]


class WhileStatement(ASTNode):
    kind: Literal["WhileStatement"] = "WhileStatement"
    condition: Expression
    body: list[Statement]


class ForStatement(ASTNode):
    kind: Literal["ForStatement"] = "ForStatement"
    target: ForTarget
    iterable: Expression
    body: list[Statement]


type ForTarget = list[Identifier]


class BreakStatement(ASTNode):
    kind: Literal["BreakStatement"] = "BreakStatement"


class ContinueStatement(ASTNode):
    kind: Literal["ContinueStatement"] = "ContinueStatement"


class MatchStatement(ASTNode):
    kind: Literal["MatchStatement"] = "MatchStatement"
    value: Expression
    cases: list[MatchCase]


class MatchCase(ASTNode):
    kind: Literal["MatchCase"] = "MatchCase"
    pattern: Pattern
    guard: Expression | None
    body: list[Statement]


type Expression = (
    IntLiteral
    | FloatLiteral
    | StringLiteral
    | BoolLiteral
    | Identifier
    | BinaryOp
    | UnaryOp
    | FunctionCall
    | MethodCall
    | FieldAccess
    | IndexAccess
    | ListLiteral
    | MapLiteral
    | SetLiteral
    | StructLiteral
    | UnionLiteral
    | RangeExpression
)


class IntLiteral(ASTNode):
    kind: Literal["IntLiteral"] = "IntLiteral"
    value: str
    type: NumberType | None = None


class FloatLiteral(ASTNode):
    kind: Literal["FloatLiteral"] = "FloatLiteral"
    value: str
    type: NumberType | None = None


class StringLiteral(ASTNode):
    kind: Literal["StringLiteral"] = "StringLiteral"
    value: str


class BoolLiteral(ASTNode):
    kind: Literal["BoolLiteral"] = "BoolLiteral"
    value: bool
    type: Bool | None = None


class Identifier(ASTNode):
    kind: Literal["Identifier"] = "Identifier"
    name: str


class BinaryOp(ASTNode):
    kind: Literal["BinaryOp"] = "BinaryOp"
    left: Expression
    operator: str
    right: Expression


class UnaryOp(ASTNode):
    kind: Literal["UnaryOp"] = "UnaryOp"
    operator: str
    operand: Expression


class FunctionCall(ASTNode):
    kind: Literal["FunctionCall"] = "FunctionCall"
    name: str
    args: list[Expression]


class MethodCall(ASTNode):
    kind: Literal["MethodCall"] = "MethodCall"
    object: Expression
    method: str
    args: list[Expression]


class FieldAccess(ASTNode):
    kind: Literal["FieldAccess"] = "FieldAccess"
    object: Expression
    field: str


class IndexAccess(ASTNode):
    kind: Literal["IndexAccess"] = "IndexAccess"
    object: Expression
    index: Expression


class ListLiteral(ASTNode):
    kind: Literal["ListLiteral"] = "ListLiteral"
    elements: list[Expression]


class MapLiteral(ASTNode):
    kind: Literal["MapLiteral"] = "MapLiteral"
    pairs: list[MapPair]


class MapPair(ASTNode):
    kind: Literal["MapPair"] = "MapPair"
    key: Expression
    value: Expression


class SetLiteral(ASTNode):
    kind: Literal["SetLiteral"] = "SetLiteral"
    elements: list[Expression]


class StructLiteral(ASTNode):
    kind: Literal["StructLiteral"] = "StructLiteral"
    name: str
    fields: list[StructLiteralField]


class StructLiteralField(ASTNode):
    kind: Literal["StructLiteralField"] = "StructLiteralField"
    name: str | None
    value: Expression


class UnionLiteral(ASTNode):
    kind: Literal["UnionLiteral"] = "UnionLiteral"
    variant: str
    value: Expression | None


class RangeExpression(ASTNode):
    kind: Literal["RangeExpression"] = "RangeExpression"
    start: Expression
    end: Expression
    inclusive: bool


type Pattern = (
    WildcardPattern
    | IdentifierPattern
    | LiteralPattern
    | StructPattern
    | UnionPattern
    | ListPattern
    | RangePattern
)


class WildcardPattern(ASTNode):
    kind: Literal["WildcardPattern"] = "WildcardPattern"


class IdentifierPattern(ASTNode):
    kind: Literal["IdentifierPattern"] = "IdentifierPattern"
    name: str


class LiteralPattern(ASTNode):
    kind: Literal["LiteralPattern"] = "LiteralPattern"
    value: Expression


class StructPattern(ASTNode):
    kind: Literal["StructPattern"] = "StructPattern"
    name: str
    fields: list[StructPatternField]


class StructPatternField(ASTNode):
    kind: Literal["StructPatternField"] = "StructPatternField"
    name: str | None
    pattern: Pattern


class UnionPattern(ASTNode):
    kind: Literal["UnionPattern"] = "UnionPattern"
    variant: str
    pattern: Pattern | None


class ListPattern(ASTNode):
    kind: Literal["ListPattern"] = "ListPattern"
    prefix_patterns: list[Pattern]
    rest_name: str | None
    suffix_patterns: list[Pattern]


class RangePattern(ASTNode):
    kind: Literal["RangePattern"] = "RangePattern"
    start: Expression
    end: Expression
    inclusive: bool


def dump_ast_to_json(ast: ASTNode, file_path: str | Path) -> None:
    """Dump an AST node to a JSON file."""
    import json

    with open(file_path, "w") as f:
        json.dump(ast.model_dump(), f, indent=2, default=str)


def load_ast_from_json(file_path: str | Path) -> Program:
    """Load an AST (Program) from a JSON file."""
    import json

    with open(file_path) as f:
        ast_data = json.load(f)

    return Program.model_validate(ast_data)
