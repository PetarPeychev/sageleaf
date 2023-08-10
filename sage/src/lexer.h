#ifndef SAGE_LEXER_H
#define SAGE_LEXER_H
#include "types.h"

typedef enum
{
    // Keywords
    TOKEN_KEYWORD_LET,
    TOKEN_KEYWORD_INT,
    TOKEN_IDENTIFIER,

    // Single-Char Symbols
    TOKEN_COLON,
    TOKEN_EQUALS,

    // Literals
    TOKEN_INT_LITERAL,

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

#endif // SAGE_LEXER_H