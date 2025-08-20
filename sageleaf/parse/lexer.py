from collections.abc import Callable
from pathlib import Path

from sageleaf.parse.tokens import KEYWORDS, SourceSpan, Token, TokenType


class LexerError(Exception):
    def __init__(self, message: str, line: int, column: int):
        super().__init__(f"Lexer error at {line}:{column}: {message}")
        self.line = line
        self.column = column


class Lexer:
    def __init__(self, source: str, file_path: Path):
        self.source = source
        # Convert to relative path from current working directory
        try:
            self.file_path = file_path.relative_to(Path.cwd())
        except ValueError:
            # If relative_to fails, keep the original path
            self.file_path = file_path
        self.pos = 0
        self.line = 1
        self.column = 1

    def make_token(
        self,
        token_type: TokenType,
        value: str | None,
        start_line: int,
        start_column: int,
        end_line: int | None = None,
        end_column: int | None = None,
    ) -> Token:
        """Create a token with proper source span information."""
        if end_line is None:
            end_line = start_line
        if end_column is None:
            if value is None:
                end_column = start_column
            else:
                end_column = start_column + len(str(value))

        span = SourceSpan(
            file_path=self.file_path,
            start_line=start_line,
            start_column=start_column,
            end_line=end_line,
            end_column=end_column,
        )
        return Token(type=token_type, value=value, span=span)

    def tokenize(self) -> list[Token]:
        tokens: list[Token] = []
        while True:
            token = self.next_token()
            tokens.append(token)
            if token.type == TokenType.EOF:
                break
        return tokens

    def current_char(self) -> str | None:
        if self.pos >= len(self.source):
            return None
        return self.source[self.pos]

    def peek_char(self, offset: int = 1) -> str | None:
        peek_pos = self.pos + offset
        if peek_pos >= len(self.source):
            return None
        return self.source[peek_pos]

    def advance(self, skip: int = 1) -> None:
        for _ in range(skip):
            if self.pos < len(self.source):
                if self.source[self.pos] == "\n":
                    self.line += 1
                    self.column = 1
                else:
                    self.column += 1
                self.pos += 1

    def skip_whitespace(self) -> None:
        char = self.current_char()
        while char and char in " \t\r":
            self.advance()
            char = self.current_char()

    def skip_single_line_comment(self):
        self.advance(2)

        char = self.current_char()
        while char and char != "\n":
            self.advance()
            char = self.current_char()

    def read_while(self, predicate: Callable[[str], bool]) -> str:
        start = self.pos
        char = self.current_char()
        while char and predicate(char):
            self.advance()
            char = self.current_char()
        return self.source[start : self.pos]

    def read_string_literal(self) -> str:
        start_line, start_column = self.line, self.column
        self.advance()

        value = ""
        while self.current_char() and self.current_char() != '"':
            if self.current_char() == "\\":
                self.advance()
                escape_char = self.current_char()
                if escape_char is None:
                    raise LexerError(
                        "unterminated string literal", start_line, start_column
                    )

                if escape_char == "n":
                    value += "\n"
                elif escape_char == "t":
                    value += "\t"
                elif escape_char == "r":
                    value += "\r"
                elif escape_char == "\\":
                    value += "\\"
                elif escape_char == '"':
                    value += '"'
                elif escape_char == "0":
                    value += "\0"
                else:
                    value += escape_char
                self.advance()
            else:
                char = self.current_char()
                if char:
                    value += char
                self.advance()

        if self.current_char() != '"':
            raise LexerError("unterminated string literal", start_line, start_column)

        self.advance()  # Skip closing quote
        return value

    def read_number_literal(self) -> tuple[TokenType, str]:
        # Check for hexadecimal (0x), binary (0b), or octal (0o) literals
        if self.current_char() == "0":
            next_char = self.peek_char()
            if next_char and next_char.lower() == "x":
                # Check if there are valid hex digits after 0x
                saved_pos = self.pos
                saved_line = self.line
                saved_column = self.column
                self.advance(2)  # Skip '0x'
                hex_digits = self.read_while(
                    lambda c: c.isdigit() or c.lower() in "abcdef"
                )
                if hex_digits:
                    # Valid hexadecimal literal
                    return TokenType.INT_LITERAL, "0x" + hex_digits
                else:
                    # No hex digits, revert and parse as regular number
                    self.pos = saved_pos
                    self.line = saved_line
                    self.column = saved_column
            elif next_char and next_char.lower() == "b":
                # Check if there are valid binary digits after 0b
                saved_pos = self.pos
                saved_line = self.line
                saved_column = self.column
                self.advance(2)  # Skip '0b'
                bin_digits = self.read_while(lambda c: c in "01")
                if bin_digits:
                    # Valid binary literal
                    return TokenType.INT_LITERAL, "0b" + bin_digits
                else:
                    # No binary digits, revert and parse as regular number
                    self.pos = saved_pos
                    self.line = saved_line
                    self.column = saved_column
            elif next_char and next_char.lower() == "o":
                # Check if there are valid octal digits after 0o
                saved_pos = self.pos
                saved_line = self.line
                saved_column = self.column
                self.advance(2)  # Skip '0o'
                oct_digits = self.read_while(lambda c: c.isdigit() and c < "8")
                if oct_digits:
                    # Valid octal literal
                    return TokenType.INT_LITERAL, "0o" + oct_digits
                else:
                    # No octal digits, revert and parse as regular number
                    self.pos = saved_pos
                    self.line = saved_line
                    self.column = saved_column

        # Regular decimal number
        value = self.read_while(lambda c: c.isdigit())
        is_float = False

        # Check for float
        next_char = self.peek_char()
        if self.current_char() == "." and next_char and next_char.isdigit():
            value += "."
            self.advance()
            value += self.read_while(lambda c: c.isdigit())
            is_float = True

        # Check for scientific notation
        char = self.current_char()
        if char and char.lower() == "e":
            value += char
            self.advance()
            is_float = True

            # Optional sign
            sign_char = self.current_char()
            if sign_char and sign_char in "+-":
                value += sign_char
                self.advance()

            # Exponent digits
            value += self.read_while(lambda c: c.isdigit())

        return TokenType.FLOAT_LITERAL if is_float else TokenType.INT_LITERAL, value

    def read_identifier(self) -> str:
        return self.read_while(lambda c: c.isalnum() or c == "_")

    def read_native_block(self) -> str:
        start_line, start_column = self.line, self.column

        self.skip_whitespace()
        if self.current_char() == "\n":
            self.advance()
            self.skip_whitespace()

        if self.current_char() != "{":
            raise LexerError(
                "expected '{' after 'native' keyword", start_line, start_column
            )

        self.advance()  # Skip opening brace
        brace_count = 1
        content = ""

        char = self.current_char()
        while char and brace_count > 0:
            if char == "{":
                brace_count += 1
            elif char == "}":
                brace_count -= 1

            if brace_count > 0:
                content += char

            self.advance()
            char = self.current_char()

        if brace_count > 0:
            raise LexerError("unterminated native block", start_line, start_column)

        return content

    def next_token(self) -> Token:
        while self.current_char():
            start_line, start_column = self.line, self.column

            char = self.current_char()
            if char and char in " \t\r":
                self.skip_whitespace()
                continue

            if self.current_char() == "\n":
                self.advance()
                continue

            if self.current_char() == "/" and self.peek_char() == "/":
                self.skip_single_line_comment()
                continue

            if self.current_char() == '"':
                value = self.read_string_literal()
                return self.make_token(
                    TokenType.STRING_LITERAL, value, start_line, start_column
                )

            char = self.current_char()
            if char and char.isdigit():
                token_type, value = self.read_number_literal()
                return self.make_token(token_type, value, start_line, start_column)

            char = self.current_char()
            if char and (char.isalpha() or char == "_"):
                value = self.read_identifier()

                if value == "native":
                    self.skip_whitespace()
                    if self.current_char() == "\n":
                        self.advance()
                        self.skip_whitespace()

                    if self.current_char() == "{":
                        c_content = self.read_native_block()
                        return self.make_token(
                            TokenType.C_LITERAL, c_content, start_line, start_column
                        )
                    else:
                        raise LexerError(
                            "native keyword must be followed by a block {...}",
                            start_line,
                            start_column,
                        )

                if value == "_":
                    return self.make_token(
                        TokenType.UNDERSCORE, value, start_line, start_column
                    )

                token_type = KEYWORDS.get(value, TokenType.IDENTIFIER)
                return self.make_token(token_type, value, start_line, start_column)

            if self.current_char() == "=" and self.peek_char() == "=":
                self.advance(2)
                return self.make_token(TokenType.EQ, "==", start_line, start_column)

            if self.current_char() == "!" and self.peek_char() == "=":
                self.advance(2)
                return self.make_token(TokenType.NE, "!=", start_line, start_column)

            if self.current_char() == ">" and self.peek_char() == "=":
                self.advance(2)
                return self.make_token(TokenType.GE, ">=", start_line, start_column)

            if self.current_char() == "<" and self.peek_char() == "=":
                self.advance(2)
                return self.make_token(TokenType.LE, "<=", start_line, start_column)

            if self.current_char() == "-" and self.peek_char() == ">":
                self.advance(2)
                return self.make_token(TokenType.ARROW, "->", start_line, start_column)

            if self.current_char() == "." and self.peek_char() == ".":
                if self.peek_char(2) == "=":
                    self.advance(3)
                    return self.make_token(
                        TokenType.RANGE_INCLUSIVE, "..=", start_line, start_column
                    )
                elif self.peek_char(2) == "<":
                    self.advance(3)
                    return self.make_token(
                        TokenType.RANGE_EXCLUSIVE, "..<", start_line, start_column
                    )

            char = self.current_char()
            self.advance()

            if char == "(":
                return self.make_token(TokenType.LPAREN, char, start_line, start_column)
            elif char == ")":
                return self.make_token(TokenType.RPAREN, char, start_line, start_column)
            elif char == "{":
                return self.make_token(TokenType.LBRACE, char, start_line, start_column)
            elif char == "}":
                return self.make_token(TokenType.RBRACE, char, start_line, start_column)
            elif char == "[":
                return self.make_token(
                    TokenType.LBRACKET, char, start_line, start_column
                )
            elif char == "]":
                return self.make_token(
                    TokenType.RBRACKET, char, start_line, start_column
                )
            elif char == ";":
                return self.make_token(
                    TokenType.SEMICOLON, char, start_line, start_column
                )
            elif char == ",":
                return self.make_token(TokenType.COMMA, char, start_line, start_column)
            elif char == ".":
                return self.make_token(TokenType.DOT, char, start_line, start_column)
            elif char == ":":
                return self.make_token(TokenType.COLON, char, start_line, start_column)
            elif char == "+":
                return self.make_token(TokenType.PLUS, char, start_line, start_column)
            elif char == "-":
                return self.make_token(TokenType.MINUS, char, start_line, start_column)
            elif char == "/":
                return self.make_token(TokenType.SLASH, char, start_line, start_column)
            elif char == "*":
                return self.make_token(TokenType.STAR, char, start_line, start_column)
            elif char == "%":
                return self.make_token(
                    TokenType.PERCENT, char, start_line, start_column
                )
            elif char == "=":
                return self.make_token(TokenType.ASSIGN, char, start_line, start_column)
            elif char == ">":
                return self.make_token(TokenType.GT, char, start_line, start_column)
            elif char == "<":
                return self.make_token(TokenType.LT, char, start_line, start_column)
            elif char == "&":
                return self.make_token(
                    TokenType.AMPERSAND, char, start_line, start_column
                )
            elif char == "'":
                return self.make_token(
                    TokenType.APOSTROPHE, char, start_line, start_column
                )
            else:
                raise LexerError(
                    f"unexpected character: {char!r}", start_line, start_column
                )

        return self.make_token(TokenType.EOF, None, self.line, self.column)
