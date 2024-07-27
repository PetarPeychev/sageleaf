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
		"\tmov rax, 42\n" +
		"\tpush rax\n" +
		"\tmov rax, 60\n" +
		"\tpop rdi\n" +
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
		"\tmov rax, 0\n" +
		"\tpush rax\n" +
		"\tmov rax, 60\n" +
		"\tpop rdi\n" +
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
		"\tmov rax, 0\n" +
		"\tpush rax\n" +
		"\tmov rax, 60\n" +
		"\tpop rdi\n" +
		"\tsyscall\n"

	asm := New(ast).Generate()

	if asm != expected {
		t.Errorf("code not equal. expected:\n%q\n, got: \n%q", expected, asm)
	}
}

func TestAdd(t *testing.T) {
	input := `
		fn main(): i64 {
			return 28 + 9 + 5;
		}
	`

	ast := parser.New(lexer.New(input)).ParseProgram()

	expected := "global _start\n\n" +
		"section .data\n\n" +
		"section .text\n" +
		"_start:\n" +
		"\tmov rax, 28\n" +
		"\tpush rax\n" +
		"\tmov rax, 9\n" +
		"\tpush rax\n" +
		"\tpop rdi\n" +
		"\tpop rax\n" +
		"\tadd rax, rdi\n" +
		"\tpush rax\n" +
		"\tmov rax, 5\n" +
		"\tpush rax\n" +
		"\tpop rdi\n" +
		"\tpop rax\n" +
		"\tadd rax, rdi\n" +
		"\tpush rax\n" +
		"\tmov rax, 60\n" +
		"\tpop rdi\n" +
		"\tsyscall\n"

	asm := New(ast).Generate()

	if asm != expected {
		t.Errorf("code not equal. expected:\n%q\n, got: \n%q", expected, asm)
	}
}
