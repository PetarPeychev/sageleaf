use std::{iter::Peekable, slice::Iter};

use crate::lexer::Token;

#[derive(Debug)]
pub struct AST {
    pub statements: Vec<Statement>,
}

#[derive(Debug)]
pub enum Statement {
    Expression(Expression),
}

#[derive(Debug)]
pub enum Expression {
    Integer(i64),
    UnaryOperation {
        operator: UnaryOperator,
        rhs: Box<Expression>,
    },
    BinaryOperation {
        operator: BinaryOperator,
        lhs: Box<Expression>,
        rhs: Box<Expression>,
    },
}

#[derive(Debug)]
pub enum UnaryOperator {
    Negate,
}

#[derive(Debug)]
pub enum BinaryOperator {
    Add,
    Subtract,
    Multiply,
    Divide,
}

pub fn parse(tokens: Vec<Token>) -> AST {
    let mut ast = AST {
        statements: Vec::new(),
    };

    let mut tokens = tokens.iter().peekable();

    while let Some(&token) = tokens.peek() {
        let statement = match token {
            _ => Statement::Expression(parse_expression(&mut tokens)),
        };

        ast.statements.push(statement);
    }

    ast
}

fn parse_expression<'a>(tokens: &mut Peekable<Iter<'a, Token>>) -> Expression {
    let mut expr = parse_term(tokens);

    while let Some(token) = tokens.peek() {
        match token {
            Token::Plus | Token::Minus => {
                let operator = match tokens.next() {
                    Some(Token::Plus) => BinaryOperator::Add,
                    Some(Token::Minus) => BinaryOperator::Subtract,
                    _ => unreachable!(),
                };
                let rhs = parse_term(tokens);
                expr = Expression::BinaryOperation {
                    operator,
                    lhs: Box::new(expr),
                    rhs: Box::new(rhs),
                };
            }
            _ => break,
        }
    }

    expr
}

fn parse_term<'a>(tokens: &mut Peekable<Iter<'a, Token>>) -> Expression {
    let mut expr = parse_factor(tokens);

    while let Some(token) = tokens.peek() {
        match token {
            Token::Asterisk | Token::Slash => {
                let operator = match tokens.next() {
                    Some(Token::Asterisk) => BinaryOperator::Multiply,
                    Some(Token::Slash) => BinaryOperator::Divide,
                    _ => unreachable!(),
                };
                let rhs = parse_factor(tokens);
                expr = Expression::BinaryOperation {
                    operator,
                    lhs: Box::new(expr),
                    rhs: Box::new(rhs),
                };
            }
            _ => break,
        }
    }

    expr
}

fn parse_factor<'a>(tokens: &mut Peekable<Iter<'a, Token>>) -> Expression {
    match tokens.next() {
        Some(Token::Integer(value)) => Expression::Integer(*value),
        Some(Token::LeftParen) => {
            let expr = parse_expression(tokens);
            match tokens.next() {
                Some(Token::RightParen) => expr,
                Some(token) => panic!("Error: Expected RightParen, found {:?}", token),
                None => panic!("Error: Unexpected end of input, expected RightParen"),
            }
        }
        Some(Token::Minus) => {
            let rhs = parse_factor(tokens);
            Expression::UnaryOperation {
                operator: UnaryOperator::Negate,
                rhs: Box::new(rhs),
            }
        }
        Some(token) => panic!("Error: Unexpected token in factor {:?}", token),
        None => panic!("Error: Unexpected end of input in factor"),
    }
}
