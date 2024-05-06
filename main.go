package main

import (
	"encoding/json"
	"fmt"
	"os"
	"sage/lexer"
	"sage/parser"
)

func main() {
	args := os.Args[1:]

	if len(args) == 0 {
		fmt.Println("Usage: sage [file]")
		os.Exit(1)
	}

	if len(args) > 1 {
		fmt.Println("Error: Too many arguments.")
		os.Exit(1)
	}

	file := args[0]

	input, err := os.ReadFile(file)
	if err != nil {
		fmt.Printf("Error: Could not read file %s.\n", file)
		os.Exit(1)
	}
	fmt.Printf("Input:\n%s\n\n", input)

	l := lexer.New(string(input))
	tokens := l.Tokenize()
	fmt.Printf("Tokens: %v\n\n", tokens)

	p := parser.New(tokens)
	module, err := p.ParseModule()
	if err != nil {
		fmt.Printf("Error: %s\n", err)
		os.Exit(1)
	}
	m, err := json.MarshalIndent(module, "", "  ")
	if err != nil {
		fmt.Printf("Error: %s\n", err)
		os.Exit(1)
	}
	fmt.Printf("%s\n\n", string(m))
	fmt.Printf("Module: %+v\n\n", module)
}
