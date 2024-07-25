#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>

#include "sage.h"

char *node_type_to_str(NodeType type)
{
    switch (type)
    {
    case NODE_EOF:
        return "EOF";
    case NODE_FN:
        return "FN";
    default:
        return "Unknown";
    }
}

void print_node(Node node)
{
    if (node.type == NODE_FN)
    {
        printf("FN(%s)\n", ((FNData *)node.data)->name);
    }
}

void ast_to_graphviz(AST ast, char *filename)
{
    FILE *file = fopen(filename, "w");

    fprintf(file, "digraph {\n");
    fprintf(file, "\troot [shape=box];\n");
    for (int i = 0; ast.definitions[i].type != NODE_EOF; i++)
    {
        char *label;
        if (ast.definitions[i].type == NODE_FN)
        {
            label = ((FNData *)ast.definitions[i].data)->name;
        }
        else
        {
            label = node_type_to_str(ast.definitions[i].type);
        }

        fprintf(file, "\tn%d [label=\"%s\"];\n", i, label);
    }
    fprintf(file, "\n");
    for (int i = 0; ast.definitions[i].type != NODE_EOF; i++)
    {
        fprintf(file, "\troot -> n%d;\n", i);
    }
    fprintf(file, "}\n");

    fclose(file);

    system("dot -Tpng ast.dot -o ast.png");
}

Token peek(Parser *parser)
{
    return parser->tokens[parser->current_token];
}

Token previous(Parser *parser)
{
    return parser->tokens[parser->current_token - 1];
}

bool isAtEnd(Parser *parser)
{
    return peek(parser).type == TOKEN_EOF;
}

bool check(Parser *parser, TokenType type)
{
    return peek(parser).type == type;
}

Token advance(Parser *parser)
{
    Token token = peek(parser);
    parser->current_token++;
    return token;
}

bool match(Parser *parser, TokenType type)
{
    if (check(parser, type))
    {
        advance(parser);
        return true;
    }
    else
    {
        return false;
    }
}

AST parse(Token *tokens)
{
    AST ast = {.definitions = malloc(sizeof(Node) * 1024)};
    int num_definitions = 0;
    Parser parser = {.tokens = tokens, .current_token = 0};

    while (!isAtEnd(&parser))
    {
        Node definition = parse_definition(&parser);
        ast.definitions[num_definitions] = definition;
        num_definitions++;
    }

    ast.definitions[num_definitions] = (Node){.type = NODE_EOF};

    return ast;
}

Node parse_definition(Parser *parser)
{
    if (check(parser, TOKEN_FN))
    {
        return parse_fn(parser);
    }
    else
    {
        printf(
            "Error: Expected start of definition, but got %s\n",
            node_type_to_str(peek(parser).type));
        exit(1);
    }
}

Node parse_fn(Parser *parser)
{
    match(parser, TOKEN_FN);

    if (!match(parser, TOKEN_IDENTIFIER))
    {
        printf(
            "Error: Expected identifier after 'fn', but got %s\n",
            node_type_to_str(peek(parser).type));
        exit(1);
    }

    char *name = previous(parser).data;

    if (!match(parser, TOKEN_LPAREN))
    {
        printf(
            "Error: Expected '(' after function name, but got %s\n",
            node_type_to_str(peek(parser).type));
        exit(1);
    }

    if (!match(parser, TOKEN_RPAREN))
    {
        printf(
            "Error: Expected ')' after function name, but got %s\n",
            node_type_to_str(peek(parser).type));
        exit(1);
    }

    if (!match(parser, TOKEN_LCURLY))
    {
        printf(
            "Error: Expected '{' after function signature, but got %s\n",
            node_type_to_str(peek(parser).type));
        exit(1);
    }

    if (!match(parser, TOKEN_RCURLY))
    {
        printf(
            "Error: Expected '}' after function signature, but got %s\n",
            node_type_to_str(peek(parser).type));
        exit(1);
    }

    FNData *data = malloc(sizeof(FNData));
    data->name = name;

    return (Node){.type = NODE_FN, .data = data};
}
