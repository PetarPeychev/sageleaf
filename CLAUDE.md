# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

Sageleaf is a statically-typed programming language that compiles to C99.

**IMPORTANT:** Full design is a WIP and available in `README.md`

- /runtime - Runtime code and standard library.
- /sageleaf - Sageleaf compiler.
  - main.py - Main entry point for the Sageleaf compiler.
  - /parse - Lexer, parser, AST, tokens.
  - /typecheck - Type checker which also annotates the AST.
  - /codegen - Code generator which emits C99 code.
- /sageleaf-syntax-highlighting - TextMate syntax highlighting for Sageleaf.
- /test - Tests for Sageleaf.

## Running the Compiler

The Sageleaf compiler CLI supports the following commands:

- `uv run sage build <file.sl>` - Build a Sageleaf program
- `uv run sage run <file.sl>` - Run a Sageleaf program
- `uv run sage emit c <file.sl>` - Emit C code for a Sageleaf program

## Development Workflow

After making changes, **ALWAYS** run the tests, linting and type checking tools with
`./check.sh`. These tools **MUST** pass with zero errors.
