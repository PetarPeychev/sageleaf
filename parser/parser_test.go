package parser

import (
	"reflect"
	"sage/ast"
	"sage/lexer"
	"testing"
)

func TestReturnStatement(t *testing.T) {
	input := `
		fn main(): i64 {
			return 42;
		}
	`

	program := New(lexer.New(input)).ParseProgram()

	expected := ast.Program{
		Declarations: []ast.Function{
			{
				Name:       "main",
				ReturnType: ast.I64{},
				Body: []ast.Return{
					{
						Value: ast.IntegerLiteral{Value: 42},
					},
				},
			},
		},
	}

	if !reflect.DeepEqual(program, expected) {
		t.Errorf("program not equal. got=%#v", program)
	}
}
