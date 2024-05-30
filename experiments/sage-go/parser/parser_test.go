package parser

import (
	"reflect"
	"sage/lexer"
	"testing"
)

func TestParseModule(t *testing.T) {
	tokens := []lexer.Token{
		{Type: lexer.FN, Value: []rune("fn")},
		{Type: lexer.IDENTIFIER, Value: []rune("main")},
		{Type: lexer.LPAREN, Value: []rune("(")},
		{Type: lexer.RPAREN, Value: []rune(")")},
		{Type: lexer.LBRACE, Value: []rune("{")},
		{Type: lexer.IDENTIFIER, Value: []rune("println")},
		{Type: lexer.LPAREN, Value: []rune("(")},
		{Type: lexer.STRING, Value: []rune("Hello, World!")},
		{Type: lexer.RPAREN, Value: []rune(")")},
		{Type: lexer.SEMICOLON, Value: []rune(";")},
		{Type: lexer.RBRACE, Value: []rune("}")},
		{Type: lexer.EOF, Value: []rune{-1}},
	}

	p := New(tokens)
	module, err := p.ParseModule()
	if err != nil {
		t.Errorf("Error: %s", err)
	}

	expected := Module{
		Body: []Statement{
			FunctionDeclaration{
				Name:   "main",
				Args:   []FunctionArgument{},
				Return: UnitType{},
				Body: []Statement{
					ExpressionStatement{
						Expression: FunctionCall{
							Name: "println",
							Args: []Expression{
								StringLiteral{Value: "Hello, World!"},
							},
						},
					},
				},
			},
		},
	}

	if !reflect.DeepEqual(module, expected) {
		t.Errorf("Module does not match. \nExpected: %+v\nGot:      %+v", expected, module)
	}
}
