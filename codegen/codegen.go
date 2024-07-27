package codegen

import (
	"sage/ast"
	"strconv"
	"strings"
)

const (
	SYSCALL_EXIT = "60"
)

type CodeGen struct {
	ast     ast.Program
	code    strings.Builder
	in_main bool
}

func New(ast ast.Program) *CodeGen {
	return &CodeGen{ast: ast}
}

func (c *CodeGen) Generate() string {
	c.code.WriteString("global _start\n\n")
	c.code.WriteString("section .data\n")
	c.code.WriteString("\n")

	c.code.WriteString("section .text\n")
	for _, f := range c.ast.Declarations {
		c.generateFunction(f)
	}
	return c.code.String()
}

func (c *CodeGen) generateFunction(f ast.Function) {
	if f.Name == "main" {
		c.code.WriteString("_start:\n")
		c.in_main = true

		if len(f.Body) == 0 {
			c.generateReturn(ast.Return{Value: ast.IntegerLiteral{Value: 0}})
			return
		}
	} else {
		panic("Not implemented yet.")
	}

	for _, r := range f.Body {
		c.generateReturn(r)
	}
}

func (c *CodeGen) generateReturn(r ast.Return) {
	c.generateExpression(r.Value)

	if !c.in_main {
		panic("Not implemented yet.")
	} else {
		c.code.WriteString("\tmov rax, " + SYSCALL_EXIT + "\n")
		c.code.WriteString("\tpop rdi\n")
		c.code.WriteString("\tsyscall\n")
	}
}

func (c *CodeGen) generateExpression(expr ast.Expression) {
	switch e := expr.(type) {
	case ast.IntegerLiteral:
		c.generateIntegerLiteral(e)
	case ast.Add:
		c.generateAdd(e)
	default:
		panic("unknown expression type")
	}
}

func (c *CodeGen) generateIntegerLiteral(il ast.IntegerLiteral) {
	c.code.WriteString("\tmov rax, " + strconv.FormatInt(il.Value, 10) + "\n")
	c.code.WriteString("\tpush rax\n")
}

func (c *CodeGen) generateAdd(add ast.Add) {
	c.generateExpression(add.Left)
	c.generateExpression(add.Right)
	c.code.WriteString("\tpop rdi\n")
	c.code.WriteString("\tpop rax\n")
	c.code.WriteString("\tadd rax, rdi\n")
	c.code.WriteString("\tpush rax\n")
}
