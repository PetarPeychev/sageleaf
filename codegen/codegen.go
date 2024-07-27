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
	ast  ast.Program
	code strings.Builder
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
		c.code.WriteString(c.generateFunction(f))
	}

	return c.code.String()
}

func (c *CodeGen) generateFunction(f ast.Function) string {
	code := strings.Builder{}
	if f.Name == "main" {
		code.WriteString("_start:\n")

		for _, r := range f.Body {
			code.WriteString("\tmov rax, " + SYSCALL_EXIT + "\n")
			switch r.Value.(type) {
			case ast.IntegerLiteral:
				exit_code := strconv.FormatInt(r.Value.(ast.IntegerLiteral).Value, 10)
				code.WriteString("\tmov rdi, " + exit_code + "\n")
				code.WriteString("\tsyscall\t\n")
			default:
				panic("Not implemented yet.")
			}
		}
	} else {
		panic("Not implemented yet.")
	}
	return code.String()
}
