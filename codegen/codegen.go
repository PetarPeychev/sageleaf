package codegen

import (
	"fmt"
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

	for _, s := range f.Body {
		c.generateStatement(s)
	}
}

func (c *CodeGen) generateStatement(s ast.Statement) {
	switch s := s.(type) {
	case ast.Return:
		c.generateReturn(s)
	case ast.Assignment:
		// c.generateAssignment(s)
	default:
		panic("unknown statement type")
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
	case ast.Subtract:
		c.generateSubtract(e)
	case ast.Multiply:
		c.generateMultiply(e)
	case ast.Divide:
		c.generateDivide(e)
	default:
		fmt.Println(e)
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

func (c *CodeGen) generateSubtract(sub ast.Subtract) {
	c.generateExpression(sub.Left)
	c.generateExpression(sub.Right)
	c.code.WriteString("\tpop rdi\n")
	c.code.WriteString("\tpop rax\n")
	c.code.WriteString("\tsub rax, rdi\n")
	c.code.WriteString("\tpush rax\n")
}

func (c *CodeGen) generateMultiply(mul ast.Multiply) {
	c.generateExpression(mul.Left)
	c.generateExpression(mul.Right)
	c.code.WriteString("\tpop rdi\n")
	c.code.WriteString("\tpop rax\n")
	c.code.WriteString("\timul rax, rdi\n")
	c.code.WriteString("\tpush rax\n")
}

func (c *CodeGen) generateDivide(div ast.Divide) {
	c.generateExpression(div.Left)
	c.generateExpression(div.Right)
	c.code.WriteString("\tpop rdi\n")
	c.code.WriteString("\tpop rax\n")
	c.code.WriteString("\tidiv rdi\n")
	c.code.WriteString("\tpush rax\n")
}
