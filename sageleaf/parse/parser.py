from __future__ import annotations

from pathlib import Path

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
    AnonymousStructType,
    AnonymousUnionType,
    Assignment,
    BinaryOp,
    Bool,
    BoolLiteral,
    BreakStatement,
    ConstDeclaration,
    ContinueStatement,
    CustomType,
    ElifBranch,
    Expression,
    ExpressionStatement,
    FieldAccess,
    FloatLiteral,
    ForStatement,
    FunctionCall,
    FunctionDef,
    GenericType,
    Identifier,
    IdentifierPattern,
    IfStatement,
    ImportStatement,
    IndexAccess,
    IntLiteral,
    ListLiteral,
    ListPattern,
    LiteralPattern,
    MapLiteral,
    MapPair,
    MatchCase,
    MatchStatement,
    MethodCall,
    NativeBlock,
    Parameter,
    Pattern,
    PointerType,
    Program,
    RangeExpression,
    ReturnStatement,
    SetLiteral,
    Statement,
    Str,
    StringLiteral,
    StructDef,
    StructField,
    StructPattern,
    StructPatternField,
    TopLevelStatement,
    Type,
    UnaryOp,
    UnionDef,
    UnionLiteral,
    UnionPattern,
    UnionVariant,
    Usize,
    VarDeclaration,
    WhileStatement,
    WildcardPattern,
)
from sageleaf.parse.lexer import Lexer
from sageleaf.parse.tokens import SourceSpan, Token, TokenType


class ParseError(Exception):
    def __init__(self, message: str, token: Token):
        token.span.print()
        super().__init__(f"Parse error: {message}")
        self.token = token


class Parser:
    def __init__(self, tokens: list[Token]):
        self.tokens = tokens
        self.pos = 0

    @property
    def current_token(self) -> Token | None:
        if self.pos >= len(self.tokens):
            return None
        return self.tokens[self.pos]

    def peek(self, offset: int = 1) -> Token | None:
        peek_pos = self.pos + offset
        if peek_pos >= len(self.tokens):
            return None
        return self.tokens[peek_pos]

    def advance(self) -> Token:
        token = self.current_token
        assert token is not None, "advance() called when current_token is None"
        self.pos += 1
        return token

    def expect(self, token_type: TokenType) -> Token:
        token = self.current_token
        if not token or token.type != token_type:
            expected = token_type.value
            actual = token.type.value if token else "EOF"
            raise ParseError(
                f"Expected {expected}, got {actual}", token or self.tokens[-1]
            )
        self.advance()
        return token

    def match(self, *token_types: TokenType) -> bool:
        if not self.current_token:
            return False
        return self.current_token.type in token_types

    def merge_spans(self, first: SourceSpan, second: SourceSpan) -> SourceSpan:
        return SourceSpan(
            file_path=first.file_path,
            start_line=first.start_line,
            start_column=first.start_column,
            end_line=second.end_line,
            end_column=second.end_column,
        )

    def parse(self) -> Program:
        statements: list[TopLevelStatement] = []
        start_span = (
            self.current_token.span
            if self.current_token
            else SourceSpan(
                file_path=Path(""),
                start_line=1,
                start_column=1,
                end_line=1,
                end_column=1,
            )
        )

        while self.current_token and self.current_token.type != TokenType.EOF:
            stmt = self.parse_top_level_statement()
            if stmt:
                statements.append(stmt)

        end_span = self.tokens[-1].span if self.tokens else start_span
        program_span = self.merge_spans(start_span, end_span)

        return Program(span=program_span, statements=statements)

    def parse_top_level_statement(self) -> TopLevelStatement | None:
        if self.match(TokenType.FN):
            return self.parse_function_def()
        elif self.match(TokenType.STRUCT):
            return self.parse_struct_def()
        elif self.match(TokenType.UNION):
            return self.parse_union_def()
        elif self.match(TokenType.IMPORT):
            return self.parse_import_statement()
        elif self.match(TokenType.C_LITERAL):
            return self.parse_native_block()
        elif self.match(TokenType.CONST):
            return self.parse_const_declaration()
        elif self.match(TokenType.IDENTIFIER):
            return self.parse_var_declaration()
        elif self.current_token:
            raise ParseError(
                "Unexpected token in top-level statement", self.current_token
            )
        return None

    def parse_function_def(self) -> FunctionDef:
        start_token = self.expect(TokenType.FN)
        name_token = self.expect(TokenType.IDENTIFIER)
        name = name_token.value

        while self.match(TokenType.APOSTROPHE):
            self.advance()
            self.expect(TokenType.IDENTIFIER)

        self.expect(TokenType.LPAREN)
        params: list[Parameter] = []

        if not self.match(TokenType.RPAREN):
            params.append(self.parse_parameter())
            while self.match(TokenType.COMMA):
                self.advance()
                params.append(self.parse_parameter())

        self.expect(TokenType.RPAREN)

        return_type = None
        if self.match(TokenType.ARROW):
            self.advance()
            return_type = self.parse_type()

        self.expect(TokenType.LBRACE)
        body: list[Statement] = []

        while not self.match(TokenType.RBRACE) and self.current_token:
            stmt = self.parse_statement()
            if stmt:
                body.append(stmt)

        end_token = self.expect(TokenType.RBRACE)
        span = self.merge_spans(start_token.span, end_token.span)

        return FunctionDef(
            span=span,
            name=name,
            params=params,
            return_type=return_type,
            body=body,
            name_token=name_token,
        )

    def parse_parameter(self) -> Parameter:
        name_token = self.expect(TokenType.IDENTIFIER)
        self.expect(TokenType.COLON)
        param_type = self.parse_type()

        span = self.merge_spans(name_token.span, param_type.span)
        return Parameter(span=span, name=name_token.value, type_annotation=param_type)

    def parse_struct_def(self) -> StructDef:
        start_token = self.expect(TokenType.STRUCT)
        name_token = self.expect(TokenType.IDENTIFIER)
        name = name_token.value

        type_params: list[str] = []
        if self.match(TokenType.APOSTROPHE):
            while self.match(TokenType.APOSTROPHE):
                self.advance()
                param_token = self.expect(TokenType.IDENTIFIER)
                type_params.append(param_token.value)

        self.expect(TokenType.LBRACE)
        fields: list[StructField] = []

        while not self.match(TokenType.RBRACE) and self.current_token:
            field = self.parse_struct_field()
            if field:
                fields.append(field)

            if self.match(TokenType.COMMA):
                self.advance()

        end_token = self.expect(TokenType.RBRACE)
        span = self.merge_spans(start_token.span, end_token.span)

        return StructDef(span=span, name=name, type_params=type_params, fields=fields)

    def parse_struct_field(self) -> StructField:
        name_token = self.expect(TokenType.IDENTIFIER)
        self.expect(TokenType.COLON)
        field_type = self.parse_type()

        span = self.merge_spans(name_token.span, field_type.span)
        return StructField(span=span, name=name_token.value, type_annotation=field_type)

    def parse_union_def(self) -> UnionDef:
        start_token = self.expect(TokenType.UNION)
        name_token = self.expect(TokenType.IDENTIFIER)
        name = name_token.value

        type_params: list[str] = []
        if self.match(TokenType.APOSTROPHE):
            while self.match(TokenType.APOSTROPHE):
                self.advance()
                param_token = self.expect(TokenType.IDENTIFIER)
                type_params.append(param_token.value)

        self.expect(TokenType.LBRACE)
        variants: list[UnionVariant] = []

        while not self.match(TokenType.RBRACE) and self.current_token:
            variant = self.parse_union_variant()
            if variant:
                variants.append(variant)

            if self.match(TokenType.COMMA):
                self.advance()

        end_token = self.expect(TokenType.RBRACE)
        span = self.merge_spans(start_token.span, end_token.span)

        return UnionDef(
            span=span, name=name, type_params=type_params, variants=variants
        )

    def parse_union_variant(self) -> UnionVariant:
        name_token = self.expect(TokenType.IDENTIFIER)
        payload = None

        if self.match(TokenType.COLON):
            self.advance()
            payload = self.parse_type()
            span = self.merge_spans(name_token.span, payload.span)
        else:
            span = name_token.span

        return UnionVariant(span=span, name=name_token.value, payload=payload)

    def parse_import_statement(self) -> ImportStatement:
        start_token = self.expect(TokenType.IMPORT)

        first_token = self.expect(TokenType.IDENTIFIER)

        if self.match(TokenType.COMMA):
            items: list[str] = [first_token.value]

            while self.match(TokenType.COMMA):
                self.advance()
                items.append(self.expect(TokenType.IDENTIFIER).value)

            self.expect(TokenType.FROM)
            package_token = self.expect(TokenType.IDENTIFIER)
            package = package_token.value

            span = self.merge_spans(start_token.span, package_token.span)

            return ImportStatement(span=span, package=package, items=items, alias=None)
        elif self.match(TokenType.FROM):
            items: list[str] = [first_token.value]
            self.advance()
            package_token = self.expect(TokenType.IDENTIFIER)
            package = package_token.value

            span = self.merge_spans(start_token.span, package_token.span)

            return ImportStatement(span=span, package=package, items=items, alias=None)
        else:
            package = first_token.value
            alias = None
            end_span = first_token.span

            if self.match(TokenType.AS):
                self.advance()
                alias_token = self.expect(TokenType.IDENTIFIER)
                alias = alias_token.value
                end_span = alias_token.span

            span = self.merge_spans(start_token.span, end_span)

            return ImportStatement(span=span, package=package, items=None, alias=alias)

    def parse_native_block(self) -> NativeBlock:
        token = self.expect(TokenType.C_LITERAL)
        return NativeBlock(span=token.span, content=token.value)

    def parse_statement(self) -> Statement | None:
        if self.match(TokenType.RETURN):
            return self.parse_return_statement()
        elif self.match(TokenType.CONST):
            return self.parse_const_declaration()
        elif self.match(TokenType.IF):
            return self.parse_if_statement()
        elif self.match(TokenType.WHILE):
            return self.parse_while_statement()
        elif self.match(TokenType.FOR):
            return self.parse_for_statement()
        elif self.match(TokenType.BREAK):
            return self.parse_break_statement()
        elif self.match(TokenType.CONTINUE):
            return self.parse_continue_statement()
        elif self.match(TokenType.MATCH):
            return self.parse_match_statement()
        elif self.match(TokenType.C_LITERAL):
            return self.parse_native_block()
        else:
            return self.parse_var_declaration_or_assignment()

    def parse_return_statement(self) -> ReturnStatement:
        start_token = self.expect(TokenType.RETURN)
        value = None
        end_span = start_token.span

        if not self.match(TokenType.SEMICOLON):
            value = self.parse_expression()
            end_span = value.span

        self.expect(TokenType.SEMICOLON)
        span = self.merge_spans(start_token.span, end_span)

        return ReturnStatement(span=span, value=value)

    def parse_const_declaration(self) -> ConstDeclaration:
        start_token = self.expect(TokenType.CONST)
        name_token = self.expect(TokenType.IDENTIFIER)

        type_annotation = None
        if self.match(TokenType.COLON):
            self.advance()
            type_annotation = self.parse_type()

        self.expect(TokenType.ASSIGN)
        value = self.parse_expression()
        self.expect(TokenType.SEMICOLON)

        span = self.merge_spans(start_token.span, value.span)

        return ConstDeclaration(
            span=span,
            name=name_token.value,
            type_annotation=type_annotation,
            value=value,
        )

    def parse_var_declaration_or_assignment(self) -> Statement:
        peek_token = self.peek()
        if peek_token and peek_token.type == TokenType.COLON:
            return self.parse_var_declaration()
        else:
            expr = self.parse_expression()

            if self.match(TokenType.ASSIGN):
                self.advance()
                value = self.parse_expression()
                self.expect(TokenType.SEMICOLON)

                span = self.merge_spans(expr.span, value.span)
                return Assignment(span=span, target=expr, value=value)
            else:
                self.expect(TokenType.SEMICOLON)
                return ExpressionStatement(span=expr.span, expression=expr)

    def parse_var_declaration(self) -> VarDeclaration:
        name_token = self.expect(TokenType.IDENTIFIER)

        type_annotation = None
        if self.match(TokenType.COLON):
            self.advance()
            type_annotation = self.parse_type()

        self.expect(TokenType.ASSIGN)
        value = self.parse_expression()
        self.expect(TokenType.SEMICOLON)

        span = self.merge_spans(name_token.span, value.span)

        return VarDeclaration(
            span=span,
            name=name_token.value,
            type_annotation=type_annotation,
            value=value,
        )

    def parse_if_statement(self) -> IfStatement:
        start_token = self.expect(TokenType.IF)
        condition = self.parse_expression()
        self.expect(TokenType.LBRACE)

        then_body: list[Statement] = []
        while not self.match(TokenType.RBRACE) and self.current_token:
            stmt = self.parse_statement()
            if stmt:
                then_body.append(stmt)

        self.expect(TokenType.RBRACE)

        elif_branches: list[ElifBranch] = []
        while self.match(TokenType.ELIF):
            elif_token = self.advance()
            elif_condition = self.parse_expression()
            self.expect(TokenType.LBRACE)

            elif_body: list[Statement] = []
            while not self.match(TokenType.RBRACE) and self.current_token:
                stmt = self.parse_statement()
                if stmt:
                    elif_body.append(stmt)

            elif_end = self.expect(TokenType.RBRACE)
            elif_span = self.merge_spans(elif_token.span, elif_end.span)

            elif_branches.append(
                ElifBranch(span=elif_span, condition=elif_condition, body=elif_body)
            )

        else_body: list[Statement] | None = None
        end_span = then_body[-1].span if then_body else condition.span

        if self.match(TokenType.ELSE):
            self.advance()
            self.expect(TokenType.LBRACE)

            else_body = []
            while not self.match(TokenType.RBRACE) and self.current_token:
                stmt = self.parse_statement()
                if stmt:
                    else_body.append(stmt)

            else_end = self.expect(TokenType.RBRACE)
            end_span = else_end.span
        elif elif_branches:
            end_span = elif_branches[-1].span

        span = self.merge_spans(start_token.span, end_span)

        return IfStatement(
            span=span,
            condition=condition,
            then_body=then_body,
            elif_branches=elif_branches,
            else_body=else_body,
        )

    def parse_while_statement(self) -> WhileStatement:
        start_token = self.expect(TokenType.WHILE)
        condition = self.parse_expression()
        self.expect(TokenType.LBRACE)

        body: list[Statement] = []
        while not self.match(TokenType.RBRACE) and self.current_token:
            stmt = self.parse_statement()
            if stmt:
                body.append(stmt)

        end_token = self.expect(TokenType.RBRACE)
        span = self.merge_spans(start_token.span, end_token.span)

        return WhileStatement(span=span, condition=condition, body=body)

    def parse_for_statement(self) -> ForStatement:
        start_token = self.expect(TokenType.FOR)

        target: list[Identifier] = []
        target.append(self.parse_identifier())

        if self.match(TokenType.COLON):
            self.advance()
            self.parse_type()

        while self.match(TokenType.COMMA):
            self.advance()
            target.append(self.parse_identifier())
            if self.match(TokenType.COLON):
                self.advance()
                self.parse_type()

        self.expect(TokenType.IN)
        iterable = self.parse_expression()
        self.expect(TokenType.LBRACE)

        body: list[Statement] = []
        while not self.match(TokenType.RBRACE) and self.current_token:
            stmt = self.parse_statement()
            if stmt:
                body.append(stmt)

        end_token = self.expect(TokenType.RBRACE)
        span = self.merge_spans(start_token.span, end_token.span)

        return ForStatement(span=span, target=target, iterable=iterable, body=body)

    def parse_break_statement(self) -> BreakStatement:
        token = self.expect(TokenType.BREAK)
        self.expect(TokenType.SEMICOLON)
        return BreakStatement(span=token.span)

    def parse_continue_statement(self) -> ContinueStatement:
        token = self.expect(TokenType.CONTINUE)
        self.expect(TokenType.SEMICOLON)
        return ContinueStatement(span=token.span)

    def parse_match_statement(self) -> MatchStatement:
        start_token = self.expect(TokenType.MATCH)
        value = self.parse_expression()
        self.expect(TokenType.LBRACE)

        cases: list[MatchCase] = []
        while not self.match(TokenType.RBRACE) and self.current_token:
            case = self.parse_match_case()
            if case:
                cases.append(case)

        end_token = self.expect(TokenType.RBRACE)
        span = self.merge_spans(start_token.span, end_token.span)

        return MatchStatement(span=span, value=value, cases=cases)

    def parse_match_case(self) -> MatchCase:
        start_token = self.expect(TokenType.CASE)
        pattern = self.parse_pattern()

        guard = None
        if self.match(TokenType.IF):
            self.advance()
            guard = self.parse_expression()

        self.expect(TokenType.COLON)

        body: list[Statement] = []
        if self.match(TokenType.LBRACE):
            self.advance()
            while not self.match(TokenType.RBRACE) and self.current_token:
                stmt = self.parse_statement()
                if stmt:
                    body.append(stmt)
            self.expect(TokenType.RBRACE)
        else:
            stmt = self.parse_statement()
            if stmt:
                body.append(stmt)

        end_span = body[-1].span if body else pattern.span
        span = self.merge_spans(start_token.span, end_span)

        return MatchCase(span=span, pattern=pattern, guard=guard, body=body)

    def parse_pattern(self) -> Pattern:
        if self.match(TokenType.UNDERSCORE):
            token = self.advance()
            return WildcardPattern(span=token.span)
        elif self.match(TokenType.IDENTIFIER):
            name_token = self.advance()
            return IdentifierPattern(span=name_token.span, name=name_token.value)
        elif self.match(
            TokenType.INT_LITERAL,
            TokenType.FLOAT_LITERAL,
            TokenType.STRING_LITERAL,
            TokenType.TRUE,
            TokenType.FALSE,
        ):
            expr = self.parse_primary_expression()
            return LiteralPattern(span=expr.span, value=expr)
        elif self.match(TokenType.LBRACKET):
            return self.parse_list_pattern()
        elif self.match(TokenType.DOT):
            return self.parse_union_pattern()
        else:
            if self.current_token:
                raise ParseError("Expected pattern", self.current_token)
            else:
                raise ParseError(
                    "Expected pattern but reached end of input",
                    Token(
                        type=TokenType.EOF,
                        value="",
                        span=SourceSpan(
                            file_path=Path(""),
                            start_line=1,
                            start_column=1,
                            end_line=1,
                            end_column=1,
                        ),
                    ),
                )

    def parse_list_pattern(self) -> ListPattern:
        start_token = self.expect(TokenType.LBRACKET)

        prefix_patterns: list[Pattern] = []
        rest_name = None
        suffix_patterns: list[Pattern] = []

        if not self.match(TokenType.RBRACKET):
            pattern = self.parse_pattern()

            if self.match(TokenType.COMMA):
                prefix_patterns.append(pattern)
                self.advance()

                peek_token = self.peek()
                if (
                    self.match(TokenType.DOT)
                    and peek_token
                    and peek_token.type == TokenType.DOT
                ):
                    self.advance()
                    self.advance()
                    if self.match(TokenType.IDENTIFIER):
                        rest_name = self.advance().value

                    if self.match(TokenType.COMMA):
                        self.advance()
                        while not self.match(TokenType.RBRACKET):
                            suffix_patterns.append(self.parse_pattern())
                            if self.match(TokenType.COMMA):
                                self.advance()
                            else:
                                break
                else:
                    while not self.match(TokenType.RBRACKET):
                        prefix_patterns.append(self.parse_pattern())
                        if self.match(TokenType.COMMA):
                            self.advance()
                        else:
                            break
            else:
                prefix_patterns.append(pattern)

        end_token = self.expect(TokenType.RBRACKET)
        span = self.merge_spans(start_token.span, end_token.span)

        return ListPattern(
            span=span,
            prefix_patterns=prefix_patterns,
            rest_name=rest_name,
            suffix_patterns=suffix_patterns,
        )

    def parse_union_pattern(self) -> UnionPattern:
        start_token = self.expect(TokenType.DOT)
        variant_token = self.expect(TokenType.IDENTIFIER)

        pattern = None
        end_span = variant_token.span

        if self.match(TokenType.LBRACE):
            self.advance()

            if self.match(TokenType.RBRACE):
                end_token = self.advance()
                end_span = end_token.span
            else:
                patterns: list[Pattern] = []
                patterns.append(self.parse_pattern())

                while self.match(TokenType.COMMA):
                    self.advance()
                    if self.match(TokenType.RBRACE):
                        break
                    patterns.append(self.parse_pattern())

                end_token = self.expect(TokenType.RBRACE)
                end_span = end_token.span

                if len(patterns) == 1:
                    pattern = patterns[0]
                else:
                    struct_fields: list[StructPatternField] = []
                    for _i, p in enumerate(patterns):
                        struct_fields.append(
                            StructPatternField(span=p.span, name=None, pattern=p)
                        )
                    pattern = StructPattern(
                        span=self.merge_spans(patterns[0].span, patterns[-1].span),
                        name="",
                        fields=struct_fields,
                    )

        span = self.merge_spans(start_token.span, end_span)

        return UnionPattern(span=span, variant=variant_token.value, pattern=pattern)

    def parse_expression(self) -> Expression:
        return self.parse_logical_or()

    def parse_logical_or(self) -> Expression:
        left = self.parse_logical_and()

        while self.match(TokenType.OR):
            op_token = self.advance()
            right = self.parse_logical_and()
            span = self.merge_spans(left.span, right.span)
            left = BinaryOp(span=span, left=left, operator=op_token.value, right=right)

        return left

    def parse_logical_and(self) -> Expression:
        left = self.parse_equality()

        while self.match(TokenType.AND):
            op_token = self.advance()
            right = self.parse_equality()
            span = self.merge_spans(left.span, right.span)
            left = BinaryOp(span=span, left=left, operator=op_token.value, right=right)

        return left

    def parse_equality(self) -> Expression:
        left = self.parse_comparison()

        while self.match(TokenType.EQ, TokenType.NE):
            op_token = self.advance()
            right = self.parse_comparison()
            span = self.merge_spans(left.span, right.span)
            left = BinaryOp(span=span, left=left, operator=op_token.value, right=right)

        return left

    def parse_comparison(self) -> Expression:
        left = self.parse_range()

        while self.match(TokenType.LT, TokenType.LE, TokenType.GT, TokenType.GE):
            op_token = self.advance()
            right = self.parse_range()
            span = self.merge_spans(left.span, right.span)
            left = BinaryOp(span=span, left=left, operator=op_token.value, right=right)

        return left

    def parse_range(self) -> Expression:
        left = self.parse_addition()

        if self.match(TokenType.RANGE_INCLUSIVE, TokenType.RANGE_EXCLUSIVE):
            op_token = self.advance()
            right = self.parse_addition()
            span = self.merge_spans(left.span, right.span)
            inclusive = op_token.type == TokenType.RANGE_INCLUSIVE
            return RangeExpression(
                span=span, start=left, end=right, inclusive=inclusive
            )

        return left

    def parse_addition(self) -> Expression:
        left = self.parse_multiplication()

        while self.match(TokenType.PLUS, TokenType.MINUS):
            op_token = self.advance()
            right = self.parse_multiplication()
            span = self.merge_spans(left.span, right.span)
            left = BinaryOp(span=span, left=left, operator=op_token.value, right=right)

        return left

    def parse_multiplication(self) -> Expression:
        left = self.parse_unary()

        while self.match(TokenType.STAR, TokenType.SLASH, TokenType.PERCENT):
            op_token = self.advance()
            right = self.parse_unary()
            span = self.merge_spans(left.span, right.span)
            left = BinaryOp(span=span, left=left, operator=op_token.value, right=right)

        return left

    def parse_unary(self) -> Expression:
        if self.match(
            TokenType.NOT, TokenType.MINUS, TokenType.STAR, TokenType.AMPERSAND
        ):
            op_token = self.advance()
            operand = self.parse_unary()
            span = self.merge_spans(op_token.span, operand.span)
            return UnaryOp(span=span, operator=op_token.value, operand=operand)

        return self.parse_postfix()

    def parse_postfix(self) -> Expression:
        expr = self.parse_primary_expression()

        while True:
            if self.match(TokenType.DOT):
                self.advance()
                if self.match(TokenType.IDENTIFIER):
                    field_token = self.advance()
                    if self.match(TokenType.LPAREN):
                        args = self.parse_argument_list()
                        span = self.merge_spans(
                            expr.span, args[-1].span if args else field_token.span
                        )
                        expr = MethodCall(
                            span=span, object=expr, method=field_token.value, args=args
                        )
                    else:
                        span = self.merge_spans(expr.span, field_token.span)
                        expr = FieldAccess(
                            span=span, object=expr, field=field_token.value
                        )
                else:
                    raise ParseError(
                        "Expected field name after '.'",
                        self.current_token or self.tokens[-1],
                    )
            elif self.match(TokenType.LBRACKET):
                self.advance()
                index = self.parse_expression()
                end_token = self.expect(TokenType.RBRACKET)
                span = self.merge_spans(expr.span, end_token.span)
                expr = IndexAccess(span=span, object=expr, index=index)
            elif self.match(TokenType.LPAREN) and isinstance(expr, Identifier):
                args = self.parse_argument_list()
                end_span = args[-1].span if args else expr.span
                span = self.merge_spans(expr.span, end_span)
                expr = FunctionCall(span=span, name=expr.name, args=args)
            else:
                break

        return expr

    def parse_argument_list(self) -> list[Expression]:
        self.expect(TokenType.LPAREN)
        args: list[Expression] = []

        if not self.match(TokenType.RPAREN):
            args.append(self.parse_expression())
            while self.match(TokenType.COMMA):
                self.advance()
                args.append(self.parse_expression())

        self.expect(TokenType.RPAREN)
        return args

    def parse_primary_expression(self) -> Expression:
        if self.match(TokenType.INT_LITERAL):
            token = self.advance()
            return IntLiteral(span=token.span, value=token.value)
        elif self.match(TokenType.FLOAT_LITERAL):
            token = self.advance()
            return FloatLiteral(span=token.span, value=token.value)
        elif self.match(TokenType.STRING_LITERAL):
            token = self.advance()
            return StringLiteral(span=token.span, value=token.value)
        elif self.match(TokenType.TRUE):
            token = self.advance()
            return BoolLiteral(span=token.span, value=True)
        elif self.match(TokenType.FALSE):
            token = self.advance()
            return BoolLiteral(span=token.span, value=False)
        elif self.match(TokenType.IDENTIFIER):
            token = self.advance()
            return Identifier(span=token.span, name=token.value)
        elif self.match(TokenType.LBRACKET):
            return self.parse_list_literal()
        elif self.match(TokenType.LBRACE):
            return self.parse_map_or_set_literal()
        elif self.match(TokenType.LPAREN):
            self.advance()
            expr = self.parse_expression()
            self.expect(TokenType.RPAREN)
            return expr
        elif self.match(TokenType.DOT):
            return self.parse_union_literal()
        else:
            if self.current_token:
                raise ParseError(
                    f"Unexpected token: {self.current_token.value}", self.current_token
                )
            else:
                raise ParseError("Unexpected end of input", self.tokens[-1])

    def parse_list_literal(self) -> ListLiteral:
        start_token = self.expect(TokenType.LBRACKET)
        elements: list[Expression] = []

        if not self.match(TokenType.RBRACKET):
            elements.append(self.parse_expression())
            while self.match(TokenType.COMMA):
                self.advance()
                if self.match(TokenType.RBRACKET):
                    break
                elements.append(self.parse_expression())

        end_token = self.expect(TokenType.RBRACKET)
        span = self.merge_spans(start_token.span, end_token.span)

        return ListLiteral(span=span, elements=elements)

    def parse_map_or_set_literal(self) -> Expression:
        start_token = self.expect(TokenType.LBRACE)

        if self.match(TokenType.RBRACE):
            end_token = self.advance()
            span = self.merge_spans(start_token.span, end_token.span)
            return MapLiteral(span=span, pairs=[])

        first_expr = self.parse_expression()

        if self.match(TokenType.COLON):
            self.advance()
            value_expr = self.parse_expression()
            pairs: list[MapPair] = [
                MapPair(
                    span=self.merge_spans(first_expr.span, value_expr.span),
                    key=first_expr,
                    value=value_expr,
                )
            ]

            while self.match(TokenType.COMMA):
                self.advance()
                if self.match(TokenType.RBRACE):
                    break
                key = self.parse_expression()
                self.expect(TokenType.COLON)
                value = self.parse_expression()
                pairs.append(
                    MapPair(
                        span=self.merge_spans(key.span, value.span),
                        key=key,
                        value=value,
                    )
                )

            end_token = self.expect(TokenType.RBRACE)
            span = self.merge_spans(start_token.span, end_token.span)
            return MapLiteral(span=span, pairs=pairs)
        else:
            elements: list[Expression] = [first_expr]

            while self.match(TokenType.COMMA):
                self.advance()
                if self.match(TokenType.RBRACE):
                    break
                elements.append(self.parse_expression())

            end_token = self.expect(TokenType.RBRACE)
            span = self.merge_spans(start_token.span, end_token.span)
            return SetLiteral(span=span, elements=elements)

    def parse_union_literal(self) -> UnionLiteral:
        start_token = self.expect(TokenType.DOT)
        variant_token = self.expect(TokenType.IDENTIFIER)

        value = None
        end_span = variant_token.span

        if self.match(TokenType.LBRACE):
            self.advance()

            if self.match(TokenType.RBRACE):
                end_token = self.advance()
                end_span = end_token.span
            else:
                elements: list[Expression] = []
                elements.append(self.parse_expression())

                while self.match(TokenType.COMMA):
                    self.advance()
                    if self.match(TokenType.RBRACE):
                        break
                    elements.append(self.parse_expression())

                end_token = self.expect(TokenType.RBRACE)
                end_span = end_token.span

                if len(elements) == 1:
                    value = elements[0]
                else:
                    value = ListLiteral(
                        span=self.merge_spans(elements[0].span, elements[-1].span),
                        elements=elements,
                    )

        span = self.merge_spans(start_token.span, end_span)

        return UnionLiteral(span=span, variant=variant_token.value, value=value)

    def parse_type(self) -> Type:
        return self.parse_pointer_type()

    def parse_pointer_type(self) -> Type:
        if self.match(TokenType.STAR):
            star_token = self.advance()
            target = self.parse_primary_type()
            span = self.merge_spans(star_token.span, target.span)
            return PointerType(span=span, target=target)

        return self.parse_primary_type()

    def parse_primary_type(self) -> Type:
        if self.match(TokenType.I8):
            token = self.advance()
            return I8(span=token.span)
        elif self.match(TokenType.I16):
            token = self.advance()
            return I16(span=token.span)
        elif self.match(TokenType.I32):
            token = self.advance()
            return I32(span=token.span)
        elif self.match(TokenType.I64):
            token = self.advance()
            return I64(span=token.span)
        elif self.match(TokenType.U8):
            token = self.advance()
            return U8(span=token.span)
        elif self.match(TokenType.U16):
            token = self.advance()
            return U16(span=token.span)
        elif self.match(TokenType.U32):
            token = self.advance()
            return U32(span=token.span)
        elif self.match(TokenType.U64):
            token = self.advance()
            return U64(span=token.span)
        elif self.match(TokenType.USIZE):
            token = self.advance()
            return Usize(span=token.span)
        elif self.match(TokenType.F32):
            token = self.advance()
            return F32(span=token.span)
        elif self.match(TokenType.F64):
            token = self.advance()
            return F64(span=token.span)
        elif self.match(TokenType.BOOL):
            token = self.advance()
            return Bool(span=token.span)
        elif self.match(TokenType.STR):
            token = self.advance()
            return Str(span=token.span)
        elif self.match(TokenType.APOSTROPHE):
            token = self.advance()
            name_token = self.expect(TokenType.IDENTIFIER)
            span = self.merge_spans(token.span, name_token.span)
            return GenericType(span=span, name=name_token.value)
        elif self.match(TokenType.IDENTIFIER):
            name_token = self.advance()
            type_args: list[Type] = []

            while self.match(TokenType.APOSTROPHE) or self.match(
                TokenType.IDENTIFIER,
                TokenType.I8,
                TokenType.I16,
                TokenType.I32,
                TokenType.I64,
                TokenType.U8,
                TokenType.U16,
                TokenType.U32,
                TokenType.U64,
                TokenType.USIZE,
                TokenType.F32,
                TokenType.F64,
                TokenType.BOOL,
                TokenType.STR,
                TokenType.LPAREN,
            ):
                if self.match(
                    TokenType.COMMA,
                    TokenType.RBRACE,
                    TokenType.RPAREN,
                    TokenType.SEMICOLON,
                    TokenType.LBRACE,
                ):
                    break

                if self.match(TokenType.APOSTROPHE):
                    self.advance()

                type_args.append(self.parse_primary_type())

            end_span = type_args[-1].span if type_args else name_token.span
            span = self.merge_spans(name_token.span, end_span)

            return CustomType(span=span, name=name_token.value, type_args=type_args)
        elif self.match(TokenType.UNION):
            return self.parse_anonymous_union_type()
        elif self.match(TokenType.STRUCT):
            return self.parse_anonymous_struct_type()
        elif self.match(TokenType.LPAREN):
            self.advance()  # consume '('
            inner_type = self.parse_type()
            self.expect(TokenType.RPAREN)
            return inner_type
        else:
            if self.current_token:
                raise ParseError(
                    f"Expected type, got {self.current_token.value}", self.current_token
                )
            else:
                raise ParseError("Expected type", self.tokens[-1])

    def parse_anonymous_union_type(self) -> AnonymousUnionType:
        start_token = self.expect(TokenType.UNION)
        self.expect(TokenType.LBRACE)

        variants: list[UnionVariant] = []
        while not self.match(TokenType.RBRACE) and self.current_token:
            variant = self.parse_union_variant()
            if variant:
                variants.append(variant)

            if self.match(TokenType.COMMA):
                self.advance()

        end_token = self.expect(TokenType.RBRACE)
        span = self.merge_spans(start_token.span, end_token.span)

        return AnonymousUnionType(span=span, variants=variants)

    def parse_anonymous_struct_type(self) -> AnonymousStructType:
        start_token = self.expect(TokenType.STRUCT)
        self.expect(TokenType.LBRACE)

        fields: list[StructField] = []
        while not self.match(TokenType.RBRACE) and self.current_token:
            field = self.parse_struct_field()
            if field:
                fields.append(field)

            if self.match(TokenType.COMMA):
                self.advance()

        end_token = self.expect(TokenType.RBRACE)
        span = self.merge_spans(start_token.span, end_token.span)

        return AnonymousStructType(span=span, fields=fields)

    def parse_identifier(self) -> Identifier:
        token = self.expect(TokenType.IDENTIFIER)
        return Identifier(span=token.span, name=token.value)


def parse_source(source: str, file_path: Path) -> Program:
    lexer = Lexer(source, file_path)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    return parser.parse()
