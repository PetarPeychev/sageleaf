package main

import (
	"fmt"
	"os"
	"sage/lexer"
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

	l := lexer.New(string(input))
	tokens := l.Tokenize()
	fmt.Printf("Tokens: %v\n\n", tokens)
}
