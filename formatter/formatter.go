package formatter

// import (
// 	"sage/ast"
// 	"strconv"
// 	"strings"
// )

// func Format(program ast.Program) string {
// 	var buf strings.Builder
// 	for i, decl := range program.Declarations {
// 		if i > 0 {
// 			buf.WriteString("\n")
// 		}
// 		buf.WriteString(formatFunction(decl))
// 	}
// 	return buf.String()
// }

// func formatFunction(fn ast.Function) string {
// 	var buf strings.Builder
// 	buf.WriteString("fn ")
// 	buf.WriteString(fn.Name)
// 	buf.WriteString("(): ")
// 	buf.WriteString(formatType(fn.ReturnType))
// 	buf.WriteString(" {\n")
// 	for _, ret := range fn.Body {
// 		buf.WriteString("    ")
// 		buf.WriteString(formatReturn(ret))
// 		buf.WriteString(";\n")
// 	}
// 	buf.WriteString("}\n")
// 	return buf.String()
// }

// func formatReturn(ret ast.Return) string {
// 	var buf strings.Builder
// 	buf.WriteString("return ")
// 	buf.WriteString(formatExpression(ret.Value))
// 	return buf.String()
// }

// func formatExpression(expr ast.Expression) string {
// 	switch e := expr.(type) {
// 	case ast.IntegerLiteral:
// 		return formatIntegerLiteral(e)
// 	default:
// 		panic("unknown expression type")
// 	}
// }

// func formatIntegerLiteral(il ast.IntegerLiteral) string {
// 	return strconv.FormatInt(il.Value, 10)
// }

// func formatType(t ast.Type) string {
// 	switch t.(type) {
// 	case ast.I64:
// 		return "i64"
// 	case ast.None:
// 		return "none"
// 	default:
// 		panic("unknown type")
// 	}
// }
