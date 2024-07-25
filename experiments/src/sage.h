#ifndef SAGE_H
#define SAGE_H

// ###### Lexer ######
typedef enum TokenType
{
    TOKEN_EOF,
    TOKEN_LPAREN,
    TOKEN_RPAREN,
    TOKEN_LCURLY,
    TOKEN_RCURLY,
    TOKEN_FN,
    TOKEN_IDENTIFIER,
} TokenType;

char *token_type_to_str(TokenType type);

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
typedef enum NodeType
{
    NODE_EOF,
    NODE_FN,
} NodeType;

typedef struct Node
{
    NodeType type;
    void *data;
} Node;

typedef struct AST
{
    Node *definitions;
} AST;

typedef struct FNData
{
    char *name;
} FNData;

typedef struct Parser
{
    Token *tokens;
    int current_token;
} Parser;

AST parse(Token *tokens);
Node parse_definition(Parser *parser);
Node parse_fn(Parser *parser);
char *node_type_to_str(NodeType type);
void print_node(Node node);
void ast_to_graphviz(AST ast, char *filename);

// ###### Lowering ######
typedef enum IRInstructionType
{
    IR_INSTR_LABEL,
    IR_INSTR_EXIT,
} IRInstructionType;

typedef struct IRInstruction
{
    IRInstructionType type;
} IRInstruction;

typedef struct IR
{
    IRInstruction *instructions;
} IR;

#endif // SAGE_H
