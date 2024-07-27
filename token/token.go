package token

type TokenType string

type Token struct {
	Type    TokenType
	Literal string
}

const (
	EOF     = "EOF"
	Illegal = "Illegal"

	Identifier = "Identifier"
	Integer    = "Integer"

	Add      = "+"
	Minus    = "-"
	Multiply = "*"
	Divide   = "/"

	Semicolon = ";"
	Colon     = ":"

	LeftParen  = "("
	RightParen = ")"
	LeftBrace  = "{"
	RightBrace = "}"

	Function = "Function"
	I64      = "I64"
	Return   = "Return"
)

var keywords = map[string]TokenType{
	"fn":     Function,
	"i64":    I64,
	"return": Return,
}

func LookupIdentifierType(identifier string) TokenType {
	if tok, ok := keywords[identifier]; ok {
		return tok
	}
	return Identifier
}
