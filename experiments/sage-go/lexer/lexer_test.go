package lexer

import (
	"reflect"
	"testing"
)

func TestTokenize(t *testing.T) {
	input := "fn main() { println(\"Hello, World!\"); }"
	l := New(input)
	tokens := l.Tokenize()
	expected := []Token{
		{Type: FN, Value: []rune("fn")},
		{Type: IDENTIFIER, Value: []rune("main")},
		{Type: LPAREN, Value: []rune("(")},
		{Type: RPAREN, Value: []rune(")")},
		{Type: LBRACE, Value: []rune("{")},
		{Type: IDENTIFIER, Value: []rune("println")},
		{Type: LPAREN, Value: []rune("(")},
		{Type: STRING, Value: []rune("Hello, World!")},
		{Type: RPAREN, Value: []rune(")")},
		{Type: SEMICOLON, Value: []rune(";")},
		{Type: RBRACE, Value: []rune("}")},
		{Type: EOF, Value: []rune{-1}},
	}
	if !reflect.DeepEqual(tokens, expected) {
		t.Errorf("Tokens do not match. \nExpected: %v\nGot:      %v", expected, tokens)
	}
}
