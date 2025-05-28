package main

import (
	"fmt"
	"os"
	"os/exec"
	"sage/ast"
	"sage/codegen"
	"sage/lexer"
	"sage/parser"
	"strings"
)

func main() {
	args := os.Args[1:]

	if len(args) < 1 {
		fmt.Println("Usage: sage <command> [arguments]")
		fmt.Println("Sage is a tool for managing sageleaf source code.")
		fmt.Println()
		fmt.Println("Commands:")
		fmt.Println("  build   Compile a sage file to an executable.")
		fmt.Println("  run     Build and run a sage file.")
		os.Exit(1)
	}

	command := args[0]

	switch command {
	case "build":
		if len(args) != 2 {
			fmt.Println("Usage: sage build <file>")
			os.Exit(1)
		}

		file_path := args[1]
		trimmed_path := strings.TrimSuffix(file_path, ".sl")
		file := readFile(file_path)
		ast := parse(file)
		asm := generateAsm(ast)
		writeFile(trimmed_path+".asm", asm)
		assemble(trimmed_path+".asm", trimmed_path+".o")
		link(trimmed_path+".o", trimmed_path)

		os.Remove(trimmed_path + ".asm")
		os.Remove(trimmed_path + ".o")
	case "run":
		if len(args) != 2 {
			fmt.Println("Usage: sage run <file>")
			os.Exit(1)
		}

		file := args[1]
		trimmed_path := strings.TrimSuffix(file, ".sl")
		file = readFile(file)
		ast := parse(file)
		asm := generateAsm(ast)
		writeFile(trimmed_path+".asm", asm)
		assemble(trimmed_path+".asm", trimmed_path+".o")
		link(trimmed_path+".o", trimmed_path)

		cmd := exec.Command(trimmed_path)
		cmd.Stdout = os.Stdout
		cmd.Stderr = os.Stderr
		err := cmd.Run()

		os.Remove(trimmed_path + ".asm")
		os.Remove(trimmed_path + ".o")
		os.Remove(trimmed_path)

		if exitErr, ok := err.(*exec.ExitError); ok {
			exitCode := exitErr.ExitCode()
			os.Exit(exitCode)
		} else if err != nil {
			panic(err)
		}
	case "test":
		fmt.Println("Error: Not implemented yet.")
		os.Exit(1)
	case "format":
		fmt.Println("Error: Not implemented yet.")
		os.Exit(1)
	// Hidden options for development
	case "_build":
		if len(args) != 2 {
			fmt.Println("Usage: sage _build <file>")
			os.Exit(1)
		}

		file_path := args[1]
		trimmed_path := strings.TrimSuffix(file_path, ".sl")
		file := readFile(file_path)
		ast := parse(file)
		asm := generateAsm(ast)
		writeFile(trimmed_path+".asm", asm)
		assemble(trimmed_path+".asm", trimmed_path+".o")
		link(trimmed_path+".o", trimmed_path)
	default:
		fmt.Printf("Error: Unknown command %s.\n", command)
		os.Exit(1)
	}
}

func readFile(path string) string {
	content, err := os.ReadFile(path)
	if err != nil {
		panic(err)
	}
	return string(content)
}

func writeFile(path string, content string) {
	f, err := os.Create(path)
	if err != nil {
		panic(err)
	}
	defer f.Close()
	f.WriteString(content)
}

func parse(content string) ast.Program {
	lexer := lexer.New(content)
	parser := parser.New(lexer)
	return parser.ParseProgram()
}

func generateAsm(ast ast.Program) string {
	codegen := codegen.New(ast)
	return codegen.Generate()
}

func assemble(inputPath string, outputPath string) {
	cmd := exec.Command("nasm", "-f", "elf64", "-o", outputPath, inputPath)
	cmd.Stdout = os.Stdout
	cmd.Stderr = os.Stderr
	err := cmd.Run()
	if err != nil {
		panic(err)
	}
}

func link(inputPath string, outputPath string) {
	cmd := exec.Command("ld", "-o", outputPath, inputPath)
	cmd.Stdout = os.Stdout
	cmd.Stderr = os.Stderr
	err := cmd.Run()
	if err != nil {
		panic(err)
	}
}
