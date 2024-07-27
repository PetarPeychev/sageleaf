package codegen

import (
	"sage/lexer"
	"sage/parser"
	"testing"
)

func TestReturn(t *testing.T) {
	input := `
		fn main(): i64 {
			return 42;
		}
	`

	ast := parser.New(lexer.New(input)).ParseProgram()

	expected := "global _start\n\n" +
		"section .data\n\n" +
		"section .text\n" +
		"_start:\n" +
		"\tmov rax, 60\n" +
		"\tmov rdi, 42\n" +
		"\tsyscall\n"

	asm := New(ast).Generate()

	if asm != expected {
		t.Errorf("code not equal. expected:\n%q\n, got: \n%q", expected, asm)
	}
}

func TestReturnNone(t *testing.T) {
	input := `
		fn main() {
			return;
		}
	`

	ast := parser.New(lexer.New(input)).ParseProgram()

	expected := "global _start\n\n" +
		"section .data\n\n" +
		"section .text\n" +
		"_start:\n" +
		"\tmov rax, 60\n" +
		"\tmov rdi, 0\n" +
		"\tsyscall\n"

	asm := New(ast).Generate()

	if asm != expected {
		t.Errorf("code not equal. expected:\n%q\n, got: \n%q", expected, asm)
	}
}

func TestNoReturn(t *testing.T) {
	input := `
		fn main() {}
	`

	ast := parser.New(lexer.New(input)).ParseProgram()

	expected := "global _start\n\n" +
		"section .data\n\n" +
		"section .text\n" +
		"_start:\n" +
		"\tmov rax, 60\n" +
		"\tmov rdi, 0\n" +
		"\tsyscall\n"

	asm := New(ast).Generate()

	if asm != expected {
		t.Errorf("code not equal. expected:\n%q\n, got: \n%q", expected, asm)
	}
}
