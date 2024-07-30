package ast

import (
	"sage/symbols"
	"sage/types"
)

type Program struct {
	Declarations []Function
	Symbols      *symbols.Table
}

type Function struct {
	Name       string
	ReturnType types.Type
	Body       Block
}

type Block struct {
	Statements []Statement
	Symbols    *symbols.Table
}

type Statement interface {
	statementNode()
}

type Return struct {
	Statement
	Value Expression
}

type Declaration struct {
	Statement
	Name  string
	Type  types.Type
	Value Expression
}

type Assignment struct {
	Statement
	Name  string
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
