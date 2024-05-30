package parser

import (
	"errors"
	"sage/lexer"
)

type Parser struct {
	tokens []lexer.Token
	pos    int
}

func New(tokens []lexer.Token) *Parser {
	return &Parser{
		tokens: tokens,
		pos:    0,
	}
}

func (p *Parser) peek() lexer.Token {
	if p.pos < len(p.tokens) {
		return p.tokens[p.pos]
	}
	return lexer.Token{Type: lexer.EOF}
}

// func (p *Parser) peekN(n int) lexer.Token {
// 	if p.pos+n-1 < len(p.tokens) {
// 		return p.tokens[p.pos+n-1]
// 	}
// 	return lexer.Token{Type: lexer.EOF}
// }

func (p *Parser) consume() lexer.Token {
	token := p.peek()
	p.pos++
	return token
}

func (p *Parser) match(t lexer.TokenType) bool {
	if p.peek().Type == t {
		p.consume()
		return true
	}
	return false
}

func (p *Parser) ParseModule() (Module, error) {
	if p.pos >= len(p.tokens) {
		return Module{}, nil
	}

	var statements []Statement
	for {
		token := p.peek()
		if token.Type == lexer.EOF {
			break
		}

		statement, err := p.parseTopLevelStatement()
		if err != nil {
			return Module{Body: statements}, err
		}
		statements = append(statements, statement)
	}

	return Module{Body: statements}, nil
}

func (p *Parser) parseTopLevelStatement() (Statement, error) {
	switch p.peek().Type {
	case lexer.FN:
		return p.parseFunctionDeclaration()
	default:
		return nil, nil
	}
}

func (p *Parser) parseFunctionDeclaration() (Statement, error) {
	if !p.match(lexer.FN) {
		return nil, errors.New("expected function declaration")
	}

	name := p.consume().Value

	if !p.match(lexer.LPAREN) {
		return nil, errors.New("expected '(' after function name")
	}

	args := []FunctionArgument{}
	for {
		if p.match(lexer.RPAREN) {
			break
		}

		// name := p.consume().Value
		// if !p.match(lexer.COLON) {
		// 	return nil, errors.New("expected ':' after function argument name")
		// }
		// typ := p.parseType()
		// arg := FunctionArgument{
		// 	Name: name,
		// 	Type: typ,
		// }
		// args = append(args, arg)

		// if p.match(lexer.RPAREN) {
		// 	break
		// }

		// if !p.match(lexer.COMMA) {
		// 	return nil, errors.New("expected ',' after function argument")
		// }
	}

	// returnType := UnitType{}
	// if p.match(lexer.COLON) {
	// 	returnType = p.parseType()
	// }

	if !p.match(lexer.LBRACE) {
		return nil, errors.New("expected '{' after function signature")
	}

	body := []Statement{}
	for {
		if p.match(lexer.RBRACE) {
			break
		}

		statement, err := p.parseStatement()
		if err != nil {
			return nil, err
		}
		body = append(body, statement)
	}

	return FunctionDeclaration{
		Name:   string(name),
		Args:   args,
		Return: UnitType{},
		Body:   body,
	}, nil

}

func (p *Parser) parseStatement() (Statement, error) {
	switch p.peek().Type {
	case lexer.IDENTIFIER:
		id := p.consume().Value
		if p.match(lexer.LPAREN) {
			args := []Expression{}
			for {
				if p.peek().Type == lexer.RPAREN {
					break
				}

				expr, err := p.parseExpression()
				if err != nil {
					return nil, err
				}
				args = append(args, expr)

				if p.match(lexer.RPAREN) {
					break
				}

				// if !p.match(lexer.COMMA) {
				// 	return nil, errors.New("expected ',' after function argument")
				// }
			}
			if !p.match(lexer.SEMICOLON) {
				return nil, errors.New("expected ';' after function call")
			}
			return ExpressionStatement{
				Expression: FunctionCall{
					Name: string(id),
					Args: args,
				},
			}, nil
		} else {
			return nil, errors.New("expected '(' after function name")
		}
	default:
		return nil, errors.New("expected function call")
	}
}

func (p *Parser) parseExpression() (Expression, error) {
	switch p.peek().Type {
	case lexer.STRING:
		value := p.consume().Value
		return StringLiteral{Value: string(value)}, nil
	}
	return nil, errors.New("expected expression")
}
