package ast

type Program struct {
	Declarations []Function
}

type Function struct {
	Name       string
	ReturnType Type
	Body       []Return
}

type Type interface {
	type_()
}

type I64 struct {
	Type
}

type None struct {
	Type
}

type Return struct {
	Value Expression
}

type Expression interface {
	expression()
}

type IntegerLiteral struct {
	Value int64
}

func (il IntegerLiteral) expression() {}
