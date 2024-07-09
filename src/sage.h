#ifndef SAGE_H
#define SAGE_H

// ###### Lexer ######
typedef enum TokenType
{
    TOKEN_LPAREN,
    TOKEN_RPAREN,
    TOKEN_LCURLY,
    TOKEN_RCURLY,
    TOKEN_FN,
    TOKEN_IDENTIFIER,
    TOKEN_EOF,
} TokenType;

typedef struct Token
{
    TokenType type;
    int index_start;
    int index_end;
    int line_start;
    int line_end;
    int column_start;
    int column_end;
    void *data;
} Token;

Token *tokenize(char *code);
void print_token(Token token);

// ###### Parser ######
typedef struct AST
{
    Node *definitions;
} AST;

typedef struct Node
{
    NodeType type;
    void *data;
} Node;

typedef enum NodeType
{
    NODE_FN,
} NodeType;

typedef struct FNData
{
    char *name;
} FNData;

AST parse(Token *tokens);

#endif // SAGE_H
