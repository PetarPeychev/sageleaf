package ast

type Program struct {
	Declarations []Function
}

type Function struct {
	Name       string
	ReturnType Type
	Body       []Statement
}

type Type interface {
	typeNode()
}

type I64 struct {
	Type
}

type None struct {
	Type
}

type Statement interface {
	statementNode()
}

type Return struct {
	Statement
	Value Expression
}

type Assignment struct {
	Statement
	Name  string
	Type  Type
	Value Expression
}

type Expression interface {
	expressionNode()
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
