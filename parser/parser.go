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
		function.Body = append(function.Body, p.parseReturn())
		p.consume(token.Semicolon)
	}

	p.consume(token.RightBrace)

	return function
}

func (p *Parser) parseReturn() ast.Return {
	ret := ast.Return{}

	p.consume(token.Return)

	ret.Value = p.parseExpression()

	return ret
}

func (p *Parser) parseExpression() ast.Expression {
	return p.parseIntegerLiteral()
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
