from sageleaf.tokens import Token
from sageleaf.tokens import TokenType as TT
from sageleaf.ast import (
    Module,
    Declaration,
    DeclarationKind,
    FunctionDeclaration,
    Argument,
    Type,
    TypeKind,
    BasicType,
    ExpressionStatement,
    ReturnStatement,
    Statement,
    StatementKind,
    Expression,
    ExpressionKind,
    Identifier,
    FunctionCall,
    StringLiteral,
    IntegerLiteral,
    Literal,
    LiteralKind,
)

from typing import Any


def log(func):
    def new_func(*args, **kwargs):
        self_arg = args[0]  # First argument is the self
        print(self_arg.tokens[self_arg.pos])
        return func(*args, **kwargs)

    return new_func


class Parser:
    def __init__(self, tokens: list[Token]):
        self.tokens = tokens
        self.pos = 0
        self.precedence: dict[str, int] = {}

    def consume(self, type: Any) -> Token:
        if self.tokens[self.pos].type == type:
            self.pos += 1
            return self.tokens[self.pos - 1]
        else:
            raise Exception(f"Expected {type}, got {self.tokens[self.pos]}")

    def match(self, type: Any) -> bool:
        if self.tokens[self.pos].type == type:
            return True
        else:
            return False

    def parse(self) -> Module:
        declarations: list[Declaration] = []

        while self.pos < len(self.tokens):
            declaration = self._parse_declaration()
            declarations.append(declaration)

        return Module(declarations)

    def _parse_declaration(self) -> Declaration:
        if self.match(TT.FN):
            return Declaration(
                DeclarationKind.FUNCTION, self._parse_function_declaration()
            )
        else:
            raise Exception("Invalid statement")

    def _parse_function_declaration(self) -> FunctionDeclaration:
        self.consume(TT.FN)
        name = self.consume(TT.IDENT).value
        assert isinstance(name, str)
        self.consume(TT.LPAREN)
        self.consume(TT.RPAREN)
        self.consume(TT.COLON)
        return_type = self._parse_type()
        body: list[Statement] = []
        self.consume(TT.LBRACE)
        while not self.match(TT.RBRACE):
            body.append(self._parse_statement())
        self.consume(TT.RBRACE)

        return FunctionDeclaration(Identifier(name), [], return_type, body)

    def _parse_type(self) -> Type:
        if self.consume(TT.I32):
            return Type(TypeKind.BASIC, BasicType.I32)
        else:
            raise Exception("Invalid type")

    def _parse_statement(self) -> Statement:
        if self.match(TT.RETURN):
            return Statement(StatementKind.RETURN, self._parse_return_statement())
        else:
            return Statement(
                StatementKind.EXPRESSION, self._parse_expression_statement()
            )

    def _parse_return_statement(self) -> ReturnStatement:
        self.consume(TT.RETURN)
        value = self._parse_expression()
        self.consume(TT.SEMICOLON)

        return ReturnStatement(value)

    def _parse_expression_statement(self) -> ExpressionStatement:
        expr = self._parse_expression()
        self.consume(TT.SEMICOLON)

        return ExpressionStatement(expr)

    def _parse_expression(self) -> Expression:
        if self.match(TT.IDENT):
            function_name = self.consume(TT.IDENT).value
            assert isinstance(function_name, str)
            self.consume(TT.LPAREN)
            arguments = []
            if not self.match(TT.RPAREN):
                argument = self._parse_expression()
                arguments.append(argument)
            while not self.match(TT.RPAREN):
                self.consume(TT.COMMA)
                argument = self._parse_expression()
                arguments.append(argument)
            self.consume(TT.RPAREN)
            return Expression(
                ExpressionKind.FUNCTION_CALL,
                FunctionCall(Identifier(function_name), arguments),
            )
        elif self.match(TT.STR_LIT):
            value = self.consume(TT.STR_LIT).value
            assert isinstance(value, str)
            return Expression(
                ExpressionKind.LITERAL,
                Literal(LiteralKind.STRING, StringLiteral(value)),
            )
        elif self.match(TT.INT_LIT):
            value = self.consume(TT.INT_LIT).value
            assert isinstance(value, int)
            return Expression(
                ExpressionKind.LITERAL,
                Literal(LiteralKind.INTEGER, IntegerLiteral(value)),
            )
        else:
            raise Exception("Invalid expression")
