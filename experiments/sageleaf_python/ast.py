from __future__ import annotations
from enum import StrEnum
from dataclasses import dataclass


@dataclass
class StringLiteral:
    value: str


@dataclass
class IntegerLiteral:
    value: int


class LiteralKind(StrEnum):
    STRING = "string"
    INTEGER = "integer"


@dataclass
class Literal:
    kind: LiteralKind
    value: StringLiteral | IntegerLiteral


@dataclass
class Identifier:
    name: str


@dataclass
class FunctionCall:
    name: Identifier
    args: list[Expression]


class ExpressionKind(StrEnum):
    IDENTIFIER = "identifier"
    FUNCTION_CALL = "function_call"
    LITERAL = "literal"


@dataclass
class Expression:
    kind: ExpressionKind
    value: Identifier | FunctionCall | Literal


class BasicType(StrEnum):
    I32 = "i32"


class TypeKind(StrEnum):
    BASIC = "basic"


@dataclass
class Type:
    kind: TypeKind
    value: BasicType


@dataclass
class Argument:
    name: Identifier
    type: Type


@dataclass
class ExpressionStatement:
    expression: Expression


@dataclass
class ReturnStatement:
    value: Expression


class StatementKind(StrEnum):
    EXPRESSION = "expression"
    RETURN = "return"


@dataclass
class Statement:
    kind: StatementKind
    value: ExpressionStatement | ReturnStatement


@dataclass
class FunctionDeclaration:
    name: Identifier
    args: list[Argument]
    return_type: Type
    body: list[Statement]


class DeclarationKind(StrEnum):
    FUNCTION = "function"


@dataclass
class Declaration:
    kind: DeclarationKind
    value: FunctionDeclaration


@dataclass
class Module:
    body: list[Declaration]
