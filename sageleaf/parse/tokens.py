from enum import Enum
from pathlib import Path
from typing import Any

from pydantic import BaseModel


class SourceSpan(BaseModel):
    model_config = {"frozen": True}
    file_path: Path
    start_line: int
    start_column: int
    end_line: int
    end_column: int

    def model_dump(self, **kwargs: Any) -> dict[str, Any]:
        """Override model_dump to use relative paths."""
        data = super().model_dump(**kwargs)
        # Convert absolute path to relative path from current working directory
        try:
            data["file_path"] = str(Path(data["file_path"]).relative_to(Path.cwd()))
        except ValueError:
            # If relative_to fails, keep the absolute path as string
            data["file_path"] = str(data["file_path"])
        return data

    def print(self):
        print(f"{self.file_path.name} {self.start_line}:{self.start_column}")
        with open(self.file_path) as f:
            lines = f.readlines()

        start_line = max(0, self.start_line - 2)
        end_line = min(len(lines), self.start_line + 1)
        context_lines = lines[start_line:end_line]

        result = ""
        for i, line in enumerate(context_lines):
            line_num = start_line + i + 1
            line_content = line.rstrip("\n")
            result += f"{line_num:4} | {line_content}\n"

            if line_num == self.start_line:
                spaces = " " * (6 + self.start_column)

                underline = ""
                for i in range(
                    self.start_column - 1,
                    min(self.end_column - 1, len(line_content)),
                ):
                    if i < len(line_content) and line_content[i] in " \t":
                        underline += " "
                    else:
                        underline += "^"

                result += f"{spaces}{underline}\n"

        print(result.rstrip())


class TokenType(str, Enum):
    LPAREN = "LParen"
    RPAREN = "RParen"
    LBRACE = "LBrace"
    RBRACE = "RBrace"
    LBRACKET = "LBracket"
    RBRACKET = "RBracket"
    SEMICOLON = "Semicolon"
    COMMA = "Comma"
    DOT = "Dot"
    COLON = "Colon"
    UNDERSCORE = "Underscore"
    APOSTROPHE = "Apostrophe"

    PLUS = "Plus"
    MINUS = "Minus"
    SLASH = "Slash"
    STAR = "Star"
    PERCENT = "Percent"
    ASSIGN = "Assign"
    EQ = "Eq"
    NE = "Ne"
    GT = "Gt"
    LT = "Lt"
    GE = "Ge"
    LE = "Le"
    ARROW = "Arrow"
    AMPERSAND = "Ampersand"
    RANGE_INCLUSIVE = "RangeInclusive"
    RANGE_EXCLUSIVE = "RangeExclusive"

    FN = "Fn"
    TYPE = "Type"
    RETURN = "Return"
    FOR = "For"
    WHILE = "While"
    IF = "If"
    ELIF = "Elif"
    ELSE = "Else"
    AND = "And"
    OR = "Or"
    NOT = "Not"
    IN = "In"
    BREAK = "Break"
    CONTINUE = "Continue"
    MATCH = "Match"
    CASE = "Case"
    CONST = "Const"
    IMPORT = "Import"
    FROM = "From"
    AS = "As"
    STRUCT = "Struct"
    UNION = "Union"
    TRUE = "True"
    FALSE = "False"

    I8 = "I8"
    I16 = "I16"
    I32 = "I32"
    I64 = "I64"
    U8 = "U8"
    U16 = "U16"
    U32 = "U32"
    U64 = "U64"
    USIZE = "Usize"
    F32 = "F32"
    F64 = "F64"
    BOOL = "Bool"
    STR = "Str"

    INT_LITERAL = "IntLiteral"
    FLOAT_LITERAL = "FloatLiteral"
    STRING_LITERAL = "StringLiteral"
    C_LITERAL = "CLiteral"
    IDENTIFIER = "Identifier"

    EOF = "Eof"


class Token(BaseModel):
    model_config = {"frozen": True}
    type: TokenType
    value: Any
    span: SourceSpan


def dump_tokens_to_json(tokens: list[Token], file_path: str | Path) -> None:
    """Dump a list of tokens to a JSON file."""
    import json

    tokens_data = [token.model_dump() for token in tokens]
    with open(file_path, "w") as f:
        json.dump(tokens_data, f, indent=2, default=str)


def load_tokens_from_json(file_path: str | Path) -> list[Token]:
    """Load a list of tokens from a JSON file."""
    import json

    with open(file_path) as f:
        tokens_data = json.load(f)

    return [Token.model_validate(data) for data in tokens_data]


KEYWORDS = {
    "fn": TokenType.FN,
    "type": TokenType.TYPE,
    "return": TokenType.RETURN,
    "for": TokenType.FOR,
    "while": TokenType.WHILE,
    "if": TokenType.IF,
    "elif": TokenType.ELIF,
    "else": TokenType.ELSE,
    "and": TokenType.AND,
    "or": TokenType.OR,
    "not": TokenType.NOT,
    "in": TokenType.IN,
    "break": TokenType.BREAK,
    "continue": TokenType.CONTINUE,
    "match": TokenType.MATCH,
    "case": TokenType.CASE,
    "const": TokenType.CONST,
    "import": TokenType.IMPORT,
    "from": TokenType.FROM,
    "as": TokenType.AS,
    "struct": TokenType.STRUCT,
    "union": TokenType.UNION,
    "true": TokenType.TRUE,
    "false": TokenType.FALSE,
    "i8": TokenType.I8,
    "i16": TokenType.I16,
    "i32": TokenType.I32,
    "i64": TokenType.I64,
    "u8": TokenType.U8,
    "u16": TokenType.U16,
    "u32": TokenType.U32,
    "u64": TokenType.U64,
    "usize": TokenType.USIZE,
    "f32": TokenType.F32,
    "f64": TokenType.F64,
    "bool": TokenType.BOOL,
    "str": TokenType.STR,
}
