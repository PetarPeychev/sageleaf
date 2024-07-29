package parser

import (
	"sage/ast"
	"sage/lexer"
	"sage/token"
	"strconv"
)

type Parser struct {
	lexer   *lexer.Lexer
	current token.Token
	next    token.Token
}

func New(l *lexer.Lexer) *Parser {
	p := &Parser{lexer: l}
	p.advance()
	return p
}

func (p *Parser) peek(t token.TokenType) bool {
	return p.next.Type == t
}

func (p *Parser) advance() token.Token {
	p.current = p.next
	p.next = p.lexer.Next()
	return p.current
}

func (p *Parser) consume(t token.TokenType) token.Token {
	if p.peek(t) {
		return p.advance()
	} else {
		panic("expected " + t + ", got " + p.current.Type)
	}
}

func (p *Parser) ParseProgram() ast.Program {
	program := ast.Program{}

	for !p.peek(token.EOF) {
		program.Declarations = append(program.Declarations, p.parseFunction())
	}

	return program
}

func (p *Parser) parseFunction() ast.Function {
	function := ast.Function{}

	p.consume(token.Function)

	function.Name = p.consume(token.Identifier).Literal

	p.consume(token.LeftParen)
	p.consume(token.RightParen)

	if !p.peek(token.Colon) {
		function.ReturnType = ast.None{}
	} else {
		p.consume(token.Colon)
		p.consume(token.I64)
		function.ReturnType = ast.I64{}
	}

	p.consume(token.LeftBrace)

	for !p.peek(token.RightBrace) {
		function.Body = append(function.Body, p.parseStatement())
		p.consume(token.Semicolon)
	}

	p.consume(token.RightBrace)

	return function
}

func (p *Parser) parseStatement() ast.Statement {
	if p.peek(token.Identifier) {
		return p.parseAssignment()
	} else if p.peek(token.Return) {
		return p.parseReturn()
	} else {
		panic("expected statement, got " + p.current.Type)
	}
}

func (p *Parser) parseAssignment() ast.Assignment {
	assignment := ast.Assignment{}

	assignment.Name = p.consume(token.Identifier).Literal

	p.consume(token.Colon)

	if p.peek(token.I64) {
		p.consume(token.I64)
		assignment.Type = ast.I64{}
	} else {
		assignment.Type = ast.I64{} // TODO: implement other types
	}

	p.consume(token.Equals)

	assignment.Value = p.parseExpression()

	return assignment
}

func (p *Parser) parseReturn() ast.Return {
	ret := ast.Return{}

	p.consume(token.Return)

	if p.peek(token.Semicolon) {
		ret.Value = ast.IntegerLiteral{Value: 0}
		return ret
	}

	ret.Value = p.parseExpression()

	return ret
}

func (p *Parser) parseExpression() ast.Expression {
	return p.parseAddSubtract()
}

func (p *Parser) parseAddSubtract() ast.Expression {
	var expr ast.Expression = p.parseMultiplyDivide()

	for p.peek(token.Plus) || p.peek(token.Minus) {
		if p.peek(token.Plus) {
			p.consume(token.Plus)
			right := p.parseMultiplyDivide()
			expr = ast.Add{Left: expr, Right: right}
		} else if p.peek(token.Minus) {
			p.consume(token.Minus)
			right := p.parseMultiplyDivide()
			expr = ast.Subtract{Left: expr, Right: right}
		}
	}

	return expr
}

func (p *Parser) parseMultiplyDivide() ast.Expression {
	var expr ast.Expression = p.parsePrimary()

	for p.peek(token.Asterisk) || p.peek(token.Slash) {
		if p.peek(token.Asterisk) {
			p.consume(token.Asterisk)
			right := p.parsePrimary()
			expr = ast.Multiply{Left: expr, Right: right}
		} else if p.peek(token.Slash) {
			p.consume(token.Slash)
			right := p.parsePrimary()
			expr = ast.Divide{Left: expr, Right: right}
		}
	}

	return expr
}

func (p *Parser) parsePrimary() ast.Expression {
	if p.peek(token.LeftParen) {
		p.consume(token.LeftParen)
		expr := p.parseExpression()
		p.consume(token.RightParen)
		return expr
	} else if p.peek(token.Integer) {
		return p.parseIntegerLiteral()
	} else {
		panic("expected expression, got " + p.current.Type)
	}
}

func (p *Parser) parseIntegerLiteral() ast.IntegerLiteral {
	il := ast.IntegerLiteral{}

	val, err := strconv.ParseInt(p.consume(token.Integer).Literal, 10, 64)
	if err != nil {
		panic(err)
	}

	il.Value = val

	return il
}
