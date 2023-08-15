#ifndef SAGE_SYNTAX_H
#define SAGE_SYNTAX_H

typedef enum
{
    NODE_PROG,
} NodeType;

typedef struct
{
    NodeType type;

} Node;

#endif // SAGE_SYNTAX_H