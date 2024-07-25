#include <stdio.h>
#include <stdbool.h>

#include "sage.h"

int main(int argc, char *argv[])
{
    char *code = "fn main() {}";
    printf("Code:\n");
    printf("%s\n\n", code);
    Token *tokens = tokenize(code);

    printf("Tokens:\n");
    int i = 0;
    while (true)
    {
        print_token(tokens[i]);
        if (tokens[i].type == TOKEN_EOF)
        {
            break;
        }
        i++;
    }
    printf("\n");

    printf("AST:\n");
    AST ast = parse(tokens);
    for (int i = 0; ast.definitions[i].type != NODE_EOF; i++)
    {
        print_node(ast.definitions[i]);
    }

    ast_to_graphviz(ast, "ast.dot");

    return 0;
}
