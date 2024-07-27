package main

import (
	"fmt"
	"os"
	"os/exec"
	"sage/codegen"
	"sage/formatter"
	"sage/lexer"
	"sage/parser"
	"strings"
)

func main() {
	args := os.Args[1:]

	if len(args) < 2 {
		fmt.Println("Usage: sage [command] [file]")
		os.Exit(1)
	}

	if len(args) > 2 {
		fmt.Println("Error: Too many arguments.")
		os.Exit(1)
	}

	command := args[0]
	file := args[1]

	switch command {
	case "build":
		build(file)
	case "run":
		run(file)
	case "test":
		test(file)
	case "format":
		format(file)
	default:
		fmt.Printf("Error: Unknown command %s.\n", command)
		os.Exit(1)
	}
}

func build(file string) {
	// read the source file
	content, err := os.ReadFile(file)
	if err != nil {
		panic(err)
	}

	// parse and generate the AST
	ast := parser.New(lexer.New(string(content))).ParseProgram()
	asm := codegen.New(ast).Generate()

	// write the assembly file
	f, err := os.Create(strings.TrimSuffix(file, ".sl") + ".asm")
	if err != nil {
		panic(err)
	}
	defer f.Close()
	f.WriteString(asm)

	// run the assembler
	cmd := exec.Command("nasm", "-f", "elf64", "-o", strings.TrimSuffix(file, ".sl")+".o", strings.TrimSuffix(file, ".sl")+".asm")
	cmd.Stdout = os.Stdout
	cmd.Stderr = os.Stderr
	err = cmd.Run()
	if err != nil {
		panic(err)
	}

	// run the linker
	cmd = exec.Command("ld", "-o", strings.TrimSuffix(file, ".sl"), strings.TrimSuffix(file, ".sl")+".o")
	cmd.Stdout = os.Stdout
	cmd.Stderr = os.Stderr
	err = cmd.Run()
	if err != nil {
		panic(err)
	}

	// clean up
	os.Remove(strings.TrimSuffix(file, ".sl") + ".o")
}

func run(file string) {
	build(file)
	os.Remove(strings.TrimSuffix(file, ".sl") + ".asm")

	// run the executable
	cmd := exec.Command(strings.TrimSuffix(file, ".sl"))
	cmd.Stdout = os.Stdout
	cmd.Stderr = os.Stderr
	err := cmd.Run()
	os.Remove(strings.TrimSuffix(file, ".sl"))
	if exitErr, ok := err.(*exec.ExitError); ok {
		exitCode := exitErr.ExitCode()
		os.Exit(exitCode)
	} else if err != nil {
		panic(err)
	}
}

func test(_ string) {
	fmt.Println("Error: Test not implemented.")
	os.Exit(1)
}

func format(file string) {
	content, err := os.ReadFile(file)
	if err != nil {
		panic(err)
	}
	ast := parser.New(lexer.New(string(content))).ParseProgram()
	f, err := os.Create(file)
	if err != nil {
		panic(err)
	}
	defer f.Close()
	f.WriteString(formatter.Format(ast))
}
