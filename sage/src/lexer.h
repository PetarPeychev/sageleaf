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
    u8 value[256]; // Assuming identifiers and numbers won't exceed this length
} Token;