from __future__ import annotations
from abc import ABC
from dataclasses import dataclass

from sageleaf.tokens import T, TT


class Expr(ABC):
    pass


@dataclass
class Int(Expr):
    value: int


@dataclass
class I64:
    pass


@dataclass
class Arg:
    name: str
    type: I64


class Stmt(ABC):
    pass


@dataclass
class Ret(Stmt):
    value: Expr


@dataclass
class Func:
    name: str
    args: list[Arg]
    return_type: I64
    body: list[Stmt]


@dataclass
class Program:
    body: list[Func]


class Parser:
    def __init__(self, tokens: list[T]):
        self.tokens = tokens
        self.pos = 0

    def consume(self, tt: TT) -> T:
        if self.tokens[self.pos].tt == tt:
            self.pos += 1
            return self.tokens[self.pos - 1]
        else:
            raise ValueError(f"Expected {type}, got {self.tokens[self.pos]}")

    def match(self, tt: TT) -> bool:
        return self.tokens[self.pos].tt == tt

    def parse(self) -> Program:
        funcs: list[Func] = []

        while self.pos < len(self.tokens):
            func = self._parse_func()
            funcs.append(func)

        return Program(funcs)

    def _parse_func(self) -> Func:
        self.consume(TT.FN)
        name = self.consume(TT.NAME).val
        assert isinstance(name, str)
        self.consume(TT.LPAREN)
        self.consume(TT.RPAREN)
        self.consume(TT.COLON)
        return_type = self._parse_i64()
        body: list[Stmt] = []
        self.consume(TT.LBRACE)
        while not self.match(TT.RBRACE):
            body.append(self._parse_stmnt())
        self.consume(TT.RBRACE)

        return Func(name, [], return_type, body)

    def _parse_i64(self) -> I64:
        self.consume(TT.I64)
        return I64()

    def _parse_stmnt(self) -> Stmt:
        return self._parse_ret()

    def _parse_ret(self) -> Ret:
        self.consume(TT.RETURN)
        value = self._parse_int()
        self.consume(TT.SEMICOLON)

        return Ret(value)

    def _parse_int(self) -> Int:
        value = self.consume(TT.INT_LIT).val
        assert isinstance(value, int)
        return Int(value)
