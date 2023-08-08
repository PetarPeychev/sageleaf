package main

import "fmt"

// func main() {
// 	input := `let variableName: int = 1234567890`
// 	tokens := Lex(input)

// 	for _, token := range tokens {
// 		fmt.Printf("TOKEN Type: %d, Value: %s\n", token.Type, token.Value)
// 	}
// }

func main() {
	input := `let variableName: int = 42`
	fmt.Printf("Input: %s\n\n", input)

	tokens := Lex(input)

	for _, token := range tokens {
		fmt.Printf("TOKEN Type: %d, Value: %s\n", token.Type, token.Value)
	}
	fmt.Println()

	parser := &Parser{tokens: tokens}
	node, err := parser.parseStatement()
	if err != nil {
		fmt.Printf("Parsing error: %s\n", err)
		return
	}

	stmt := node.(*BindingStatement)
	fmt.Printf("BindingStatement: Identifier = %s, Type = %s, Value = %d\n\n", stmt.Identifier, stmt.Type, stmt.Value)
}
