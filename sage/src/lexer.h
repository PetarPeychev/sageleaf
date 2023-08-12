#ifndef SAGE_LEXER_H
#define SAGE_LEXER_H
#include "types.h"

typedef enum
{
    // Keywords
    TOKEN_KEYWORD_LET,
    TOKEN_KEYWORD_VAR,
    TOKEN_KEYWORD_TYPE,
    TOKEN_KEYWORD_IMPORT,

    TOKEN_KEYWORD_AND,
    TOKEN_KEYWORD_OR,
    TOKEN_KEYWORD_NOT,

    TOKEN_KEYWORD_IF,
    TOKEN_KEYWORD_IS,
    TOKEN_KEYWORD_THEN,
    TOKEN_KEYWORD_ELSE,

    TOKEN_KEYWORD_INT,
    TOKEN_KEYWORD_STR,
    TOKEN_KEYWORD_FLOAT,
    TOKEN_KEYWORD_BOOL,
    TOKEN_KEYWORD_NONE,
    TOKEN_KEYWORD_ANY,
    TOKEN_KEYWORD_TRUE,
    TOKEN_KEYWORD_FALSE,

    TOKEN_IDENTIFIER,

    // Single-Char Symbols
    TOKEN_COLON,
    TOKEN_SEMICOLON,
    TOKEN_COMMA,
    TOKEN_EQUALS,
    TOKEN_ADD,
    TOKEN_SUB,
    TOKEN_MUL,
    TOKEN_DIV,
    TOKEN_MOD,
    TOKEN_POW,
    TOKEN_LT,
    TOKEN_GT,
    TOKEN_LPAREN,
    TOKEN_RPAREN,
    TOKEN_LSQUARE,
    TOKEN_RSQUARE,
    TOKEN_LSQUIRLY,
    TOKEN_RSQUIRLY,

    // Multi-Char Symbols
    TOKEN_ARROW,
    TOKEN_PIPE,
    TOKEN_GTE,
    TOKEN_LTE,

    // Literals
    TOKEN_INT_LITERAL,
    TOKEN_STR_LITERAL,

    // Misc
    TOKEN_ERROR,
    TOKEN_EOF
} TokenType;

typedef struct
{
    TokenType type;
    char value[1024]; // Assuming identifiers and numbers won't exceed this length
} Token;

Token *lex(char *buffer);

char *token_type_to_string(TokenType type);

char *token_to_string(Token *token);

#endif // SAGE_LEXER_H
