#ifndef SAGE_SYNTAX_H
#define SAGE_SYNTAX_H

typedef enum
{
    NODE_CONST,
    NODE_VAR,
    NODE_TYPEDEF,
    NODE_IMPORT,
} NodeType;

typedef struct
{
    NodeType type;
} Node;

#endif // SAGE_SYNTAX_H