#!/usr/bin/env python3

from pathlib import Path

from sageleaf.parse.lexer import Lexer
from sageleaf.parse.tokens import Token, dump_tokens_to_json


def main():
    test_file = Path(__file__).parent / "test_tokens.sl"
    json_file = Path(__file__).parent / "test_tokens.json"

    # Read the test file
    with open(test_file, encoding="utf-8") as f:
        source_code = f.read()

    # Create lexer and tokenize
    lexer = Lexer(source_code, test_file)
    tokens: list[Token] = []
    try:
        while True:
            token = lexer.next_token()
            tokens.append(token)
            if token.type.value == "Eof":
                break
    except Exception:
        print(f"Successfully parsed {len(tokens)} tokens")
        print("Last few tokens:")
        for token in tokens[-5:]:
            print(
                f"  {token.type}: {repr(token.value)} at line {token.span.start_line}"
            )
        print(f"\nError at line {lexer.line}, column {lexer.column}")
        print(f"Current character: {repr(lexer.current_char())}")
        print(f"Position in source: {lexer.pos}")
        if lexer.pos > 0:
            context_start = max(0, lexer.pos - 30)
            context_end = min(len(source_code), lexer.pos + 30)
            context = source_code[context_start:context_end]
            print(f"Context: {repr(context)}")
        raise

    # Dump tokens to JSON
    dump_tokens_to_json(tokens, json_file)

    print(f"Generated {len(tokens)} tokens")
    print(f"Reference saved to: {json_file}")


if __name__ == "__main__":
    main()
