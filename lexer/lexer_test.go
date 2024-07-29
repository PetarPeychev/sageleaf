package lexer

import (
	"testing"

	"sage/token"
)

func TestNextToken(t *testing.T) {
	input := `
		fn main(): i64 {
			x := 1;
			return 42;
		} @@

		fn $add():i64{return 3 + 4 * 5 - 6;}
	`

	tests := []struct {
		expectedType    token.TokenType
		expectedLiteral string
	}{
		{token.Function, "fn"},
		{token.Identifier, "main"},
		{token.LeftParen, "("},
		{token.RightParen, ")"},
		{token.Colon, ":"},
		{token.I64, "i64"},
		{token.LeftBrace, "{"},
		{token.Identifier, "x"},
		{token.Colon, ":"},
		{token.Equals, "="},
		{token.Integer, "1"},
		{token.Semicolon, ";"},
		{token.Return, "return"},
		{token.Integer, "42"},
		{token.Semicolon, ";"},
		{token.RightBrace, "}"},
		{token.Illegal, "@"},
		{token.Illegal, "@"},
		{token.Function, "fn"},
		{token.Illegal, "$"},
		{token.Identifier, "add"},
		{token.LeftParen, "("},
		{token.RightParen, ")"},
		{token.Colon, ":"},
		{token.I64, "i64"},
		{token.LeftBrace, "{"},
		{token.Return, "return"},
		{token.Integer, "3"},
		{token.Plus, "+"},
		{token.Integer, "4"},
		{token.Asterisk, "*"},
		{token.Integer, "5"},
		{token.Minus, "-"},
		{token.Integer, "6"},
		{token.Semicolon, ";"},
		{token.RightBrace, "}"},
		{token.EOF, ""},
	}

	l := New(input)

	for i, tt := range tests {
		tok := l.Next()
		if tok.Type != tt.expectedType {
			t.Fatalf("tests[%d] - tokenType wrong. expected=%q, got=%q", i, tt.expectedType, tok.Type)
		}

		if tok.Literal != tt.expectedLiteral {
			t.Fatalf("tests[%d] - literal wrong. expected=%q, got=%q", i, tt.expectedLiteral, tok.Literal)
		}
	}
}
