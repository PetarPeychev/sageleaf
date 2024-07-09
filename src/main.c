#include <stdio.h>
#include <stdbool.h>

#include "sage.h"

int main(int argc, char *argv[])
{
    char *code = "fn main() {}";
    Token *tokens = tokenize(code);

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

    return 0;
}
