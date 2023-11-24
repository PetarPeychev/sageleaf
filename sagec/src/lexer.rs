use std::iter::Peekable;
use std::str::Chars;

#[derive(Debug, PartialEq)]
pub enum Token {
    Plus,
    Minus,
    Asterisk,
    Slash,
    LeftParen,
    RightParen,
    Integer(i64),
}

pub fn lex(input: String) -> Vec<Token> {
    let mut tokens = Vec::new();
    let mut chars = input.chars().peekable();

    while let Some(&c) = chars.peek() {
        if c.is_whitespace() {
            chars.next();
            continue;
        }

        let token = match c {
            '+' => {
                chars.next();
                Token::Plus
            }
            '-' => {
                chars.next();
                Token::Minus
            }
            '*' => {
                chars.next();
                Token::Asterisk
            }
            '/' => {
                chars.next();
                Token::Slash
            }
            '(' => {
                chars.next();
                Token::LeftParen
            }
            ')' => {
                chars.next();
                Token::RightParen
            }
            _ if c.is_digit(10) => read_integer(&mut chars),
            _ => {
                panic!("ERROR: Invalid character: {}", c);
            }
        };

        tokens.push(token);
    }

    tokens
}

fn read_integer(chars: &mut Peekable<Chars>) -> Token {
    let mut value_string = String::new();

    while let Some(&c) = chars.peek() {
        if !c.is_digit(10) {
            break;
        }
        value_string.push(c);
        chars.next();
    }

    let value = value_string
        .parse::<i64>()
        .expect("ERROR: Failed to parse integer.");
    Token::Integer(value)
}
