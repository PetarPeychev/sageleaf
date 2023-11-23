use std::{iter::Peekable, str::Chars};

pub enum TokenKind {
    Plus,
    Minus,
    Asterisk,
    Slash,
    LeftParen,
    RightParen,
    Integer(i64),
}

pub struct Span {
    pub start: usize,
    pub end: usize,
    pub line: usize,
    pub literal: String,
}

impl Span {
    pub fn length(&self) -> usize {
        self.end - self.start
    }
}

pub struct Token {
    pub kind: TokenKind,
    pub span: Span,
}

pub struct Lexer<'a> {
    input: Peekable<Chars<'a>>,
    line: usize,
    position: usize,
}

// impl<'a> Iterator for Lexer<'a> {
//     type Item = Token;

//     fn next(&mut self) -> Option<Self::Item> {
//         match self.input.peek()? {
//             c if c.is_digit(10) => Some(self.lex_integer()),
//             c if c.is_whitespace() => {
//                 self.input.next();
//                 self.next()
//             }
//             c if c.is_ascii_punctuation() => Some(self.lex_punctuation()),
//             _ => None,
//         }
//     }
// }
