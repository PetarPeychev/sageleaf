package main

// import (
// 	"fmt"
// 	"strconv"
// )

// type BindingStatement struct {
// 	Identifier string
// 	Type       string
// 	Value      int64
// }

// func (bs *BindingStatement) isNode() {}

// type Node interface {
// 	isNode()
// }

// type Parser struct {
// 	tokens []Token
// 	pos    int
// }

// func (p *Parser) peek() Token {
// 	if p.pos < len(p.tokens) {
// 		return p.tokens[p.pos]
// 	}
// 	return Token{}
// }

// func (p *Parser) consume() Token {
// 	token := p.peek()
// 	p.pos++
// 	return token
// }

// func (p *Parser) match(t TokenType) bool {
// 	if p.peek().Type == t {
// 		p.consume()
// 		return true
// 	}
// 	return false
// }

// func (p *Parser) parseStatement() (Node, error) {
// 	switch {
// 	case p.match(T_LET):
// 		return p.parseBindingStatement()
// 	default:
// 		return nil, fmt.Errorf("unknown statement")
// 	}
// }

// func (p *Parser) parseBindingStatement() (Node, error) {
// 	if p.peek().Type != T_IDENTIFIER {
// 		return nil, fmt.Errorf("expected identifier after 'let'")
// 	}
// 	identifier := p.consume().Value

// 	if !p.match(T_COLON) {
// 		return nil, fmt.Errorf("expected ':' after identifier")
// 	}

// 	if !p.match(T_INT_KEYWORD) {
// 		return nil, fmt.Errorf("expected 'int' keyword")
// 	}

// 	if !p.match(T_EQUALS) {
// 		return nil, fmt.Errorf("expected '=' after type keyword")
// 	}

// 	if p.peek().Type != T_INT_LITERAL {
// 		return nil, fmt.Errorf("expected int64 literal for value")
// 	}
// 	valueStr := p.consume().Value
// 	value, err := strconv.ParseInt(valueStr, 10, 64)
// 	if err != nil {
// 		return nil, fmt.Errorf("failed to parse int64 literal")
// 	}

// 	return &BindingStatement{
// 		Identifier: identifier,
// 		Type:       "int",
// 		Value:      value,
// 	}, nil
// }
