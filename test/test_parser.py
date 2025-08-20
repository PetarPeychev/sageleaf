#!/usr/bin/env python3

import json
from pathlib import Path

from sageleaf.parse.lexer import Lexer
from sageleaf.parse.parser import Parser


def test_parser():
    test_file = Path(__file__).parent / "test_parser_comprehensive.sl"
    with open(test_file) as f:
        source = f.read()

    lexer = Lexer(source, test_file)
    tokens = lexer.tokenize()

    parser = Parser(tokens)
    ast = parser.parse()

    # Load expected JSON output
    expected_output_file = Path(__file__).parent / "test_parser_output.json"
    with open(expected_output_file) as f:
        expected_ast_json = json.load(f)

    # Convert parsed AST to JSON format for comparison
    actual_ast_json = json.loads(ast.model_dump_json())

    # Compare the parsed AST with expected output
    assert actual_ast_json == expected_ast_json, (
        f"Parsed AST does not match expected output in {expected_output_file}"
    )


if __name__ == "__main__":
    test_parser()
