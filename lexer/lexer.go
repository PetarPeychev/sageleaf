package lexer

import (
	"unicode"
	"unicode/utf8"
)

type TokenType int

const (
	FN TokenType = iota
	IDENTIFIER
	SEMICOLON
	LPAREN
	RPAREN
	LBRACE
	RBRACE
	STRING
	ERROR
	EOF
)

type Token struct {
	Type  TokenType
	Value []rune
}

func (t Token) String() string {
	switch t.Type {
	case FN:
		return "FN"
	case IDENTIFIER:
		return "IDENTIFIER(" + string(t.Value) + ")"
	case SEMICOLON:
		return "SEMICOLON"
	case LPAREN:
		return "LPAREN"
	case RPAREN:
		return "RPAREN"
	case LBRACE:
		return "LBRACE"
	case RBRACE:
		return "RBRACE"
	case STRING:
		return "STRING(" + string(t.Value) + ")"
	case ERROR:
		return "ERROR"
	case EOF:
		return "EOF"
	default:
		return "UNKNOWN"
	}
}

type Lexer struct {
	input []rune
	pos   int
	size  int
}

func New(input string) *Lexer {
	return &Lexer{
		input: []rune(input),
		pos:   0,
		size:  utf8.RuneCountInString(input),
	}
}

func isIdentifierChar(ch rune) bool {
	return unicode.IsLetter(ch) || ch == '_'
}

func (l *Lexer) peek() rune {
	if l.pos >= l.size {
		return -1
	}
	return l.input[l.pos]
}

func (l *Lexer) consume() rune {
	if l.pos >= l.size {
		return -1
	}
	r := l.input[l.pos]
	l.pos++
	return r
}

func (l *Lexer) readString() Token {
	l.consume() // consume the starting "
	start := l.pos
	for l.pos < l.size && l.input[l.pos] != '"' {
		l.pos++
	}
	end := l.pos
	if l.input[l.pos] != '"' {
		return Token{Type: ERROR, Value: []rune{l.consume()}}
	}
	l.consume() // consume the ending "
	return Token{Type: STRING, Value: l.input[start:end]}
}

func (l *Lexer) readIdentifier() Token {
	start := l.pos
	for l.pos < l.size && isIdentifierChar(l.input[l.pos]) {
		l.pos++
	}
	identifier := l.input[start:l.pos]

	switch string(identifier) {
	case "fn":
		return Token{Type: FN, Value: identifier}
	default:
		return Token{Type: IDENTIFIER, Value: identifier}
	}
}

func (l *Lexer) nextToken() Token {
	next := l.peek()
	switch {
	case next == -1:
		return Token{Type: EOF, Value: []rune{l.consume()}}
	case unicode.IsSpace(next):
		l.consume()
		return l.nextToken()
	case next == ';':
		return Token{Type: SEMICOLON, Value: []rune{l.consume()}}
	case next == '(':
		return Token{Type: LPAREN, Value: []rune{l.consume()}}
	case next == ')':
		return Token{Type: RPAREN, Value: []rune{l.consume()}}
	case next == '{':
		return Token{Type: LBRACE, Value: []rune{l.consume()}}
	case next == '}':
		return Token{Type: RBRACE, Value: []rune{l.consume()}}
	case next == '"':
		return l.readString()
	case isIdentifierChar(next):
		return l.readIdentifier()
	default:
		return Token{Type: ERROR, Value: []rune{l.consume()}}
	}
}

func (l *Lexer) Tokenize() []Token {
	var tokens []Token
	for {
		token := l.nextToken()
		if token.Type == EOF {
			break
		}
		tokens = append(tokens, token)
	}
	return tokens
}
