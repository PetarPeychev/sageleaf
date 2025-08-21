# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

Sageleaf is a statically-typed programming language that compiles to C99.

**IMPORTANT:** Full design is a WIP and available in `README.md`

## Running the Compiler

The Sageleaf compiler CLI supports the following commands:

- `uv run sage build <package/dir>` - Build a Sageleaf program
- `uv run sage run <package/dir>` - Run a Sageleaf program
- `uv run sage emit c <package/dir>` - Emit C code for a Sageleaf program

## Development Workflow

After making changes, **ALWAYS** run the tests, linting and type checking tools with
`./check.sh`. These tools **MUST** pass with zero errors.
