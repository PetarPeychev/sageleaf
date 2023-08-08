package main

import (
	"unicode"
)

type TokenType int

const (
	T_INT_LITERAL TokenType = iota
	T_LET
	T_INT_KEYWORD
	T_COLON
	T_EQUALS
	T_IDENTIFIER
)

type Token struct {
	Type  TokenType
	Value string
}

func Lex(input string) []Token {
	var tokens []Token
	i := 0

	isIdentifierChar := func(ch rune) bool {
		return unicode.IsLetter(ch) || ch == '_'
	}

	for i < len(input) {
		char := rune(input[i])

		switch {
		case unicode.IsDigit(char):
			start := i
			for i < len(input) && unicode.IsDigit(rune(input[i])) {
				i++
			}
			tokens = append(tokens, Token{Type: T_INT_LITERAL, Value: input[start:i]})

		case char == ':':
			tokens = append(tokens, Token{Type: T_COLON, Value: ":"})
			i++

		case char == '=':
			tokens = append(tokens, Token{Type: T_EQUALS, Value: "="})
			i++

		case isIdentifierChar(char):
			start := i
			for i < len(input) && isIdentifierChar(rune(input[i])) {
				i++
			}
			identifier := input[start:i]
			if identifier == "let" {
				tokens = append(tokens, Token{Type: T_LET, Value: "let"})
			} else if identifier == "int" {
				tokens = append(tokens, Token{Type: T_INT_KEYWORD, Value: "int"})
			} else {
				tokens = append(tokens, Token{Type: T_IDENTIFIER, Value: identifier})
			}

		default:
			i++
		}
	}

	return tokens
}
