package parser

type Module struct {
	Name string
	Body []Statement
}

type Statement interface {
	isStatement()
}

type FunctionDeclaration struct {
	Name   string
	Args   []FunctionArgument
	Return Type
	Body   []Statement
}

func (f FunctionDeclaration) isStatement() {}

type FunctionArgument struct {
	Name string
	Type Type
}

type Type interface {
	isType()
}

type UnitType struct{}

func (UnitType) isType() {}

type ExpressionStatement struct {
	Expression Expression
}

func (e ExpressionStatement) isStatement() {}

type Expression interface {
	isExpression()
}

type FunctionCall struct {
	Name string
	Args []Expression
}

func (FunctionCall) isExpression() {}

type StringLiteral struct {
	Value string
}

func (StringLiteral) isExpression() {}
