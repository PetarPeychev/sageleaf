from enum import StrEnum
from dataclasses import dataclass

class TokenType(StrEnum):
    FN = 'fn'
    I32 = 'i32'
    RETURN = 'return'
    COMMA = ','
    COLON = ':'
    SEMICOLON = ';'
    LPAREN = '('
    RPAREN = ')'
    LBRACE = '{'
    RBRACE = '}'
    IDENT = 'id'
    STR_LIT = 'str'
    INT_LIT = 'int'


class Token:
    type: TokenType
    value: int | str | None

    def __init__(self, type: TokenType, value: int | str | None = None):
        self.type = type
        self.value = value

    def __str__(self):
        value = ""
        if self.value is not None:
            value = f"({self.value})"
        return f"{self.type}{value}"

    def __repr__(self):
        return str(self)
