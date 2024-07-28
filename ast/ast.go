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

type Add struct {
	Expression
	Left  Expression
	Right Expression
}

type Subtract struct {
	Expression
	Left  Expression
	Right Expression
}

type Multiply struct {
	Expression
	Left  Expression
	Right Expression
}

type Divide struct {
	Expression
	Left  Expression
	Right Expression
}

type IntegerLiteral struct {
	Expression
	Value int64
}
