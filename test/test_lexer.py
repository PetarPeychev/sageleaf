from pathlib import Path

from sageleaf.parse.lexer import Lexer
from sageleaf.parse.tokens import TokenType, load_tokens_from_json


def test_comprehensive_lexer_against_reference():
    test_file = Path(__file__).parent / "test_tokens.sl"
    reference_file = Path(__file__).parent / "test_tokens.json"

    with open(test_file, encoding="utf-8") as f:
        source_code = f.read()

    lexer = Lexer(source_code, test_file)
    actual_tokens = lexer.tokenize()

    expected_tokens = load_tokens_from_json(reference_file)

    assert len(actual_tokens) == len(expected_tokens)

    for i, (actual, expected) in enumerate(
        zip(actual_tokens, expected_tokens, strict=True)
    ):
        assert actual == expected, f"Token {i} mismatch: {actual} != {expected}"

    used_token_types = {token.type for token in actual_tokens}
    all_token_types = set(TokenType)
    missing_types = all_token_types - used_token_types

    assert not missing_types, f"Missing token types: {missing_types}"
