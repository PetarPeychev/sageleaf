use std::fmt;

pub enum TokenKind {
    Identifier(String),
    Integer(i64),
    Float(f64),
    String(String),
}

pub struct Span {
    pub start: usize,
    pub end: usize,
    pub line: usize,
    pub column: usize,
    pub literal: String,
}

pub struct Token {
    pub kind: TokenKind,
    pub span: Span,
}

impl fmt::Display for Token {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match &self.kind {
            TokenKind::Identifier(s) => write!(f, "Identifier({s})"),
            TokenKind::Integer(i) => write!(f, "Integer({i})"),
            TokenKind::Float(fl) => write!(f, "Float({fl})"),
            TokenKind::String(s) => write!(f, "String({s})"),
        }
    }
}

pub struct Lexer {
    pub input: String,
    pub pos: usize,
    pub next: usize,
    pub ch: char,
}
