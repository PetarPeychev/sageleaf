#include <stdlib.h>
#include <string.h>

#include "lexer.h"
#include "config.h"

Token *lex(char *buffer)
{
    Token *tokens = malloc(sizeof(Token) * MAX_TOKENS);
    u32 token_count = 0;

    u32 i = 0;
    while (buffer[i] != '\0')
    {
        if (buffer[i] == ' ')
        {
            i++;
            continue;
        }

        if (buffer[i] == ':')
        {
            tokens[token_count].type = TOKEN_COLON;
            token_count++;
            i++;
            continue;
        }

        if (buffer[i] == '=')
        {
            tokens[token_count].type = TOKEN_EQUALS;
            token_count++;
            i++;
            continue;
        }

        if (buffer[i] >= '0' && buffer[i] <= '9')
        {
            u32 j = 0;
            while (buffer[i] >= '0' && buffer[i] <= '9')
            {
                tokens[token_count].value[j] = buffer[i];
                i++;
                j++;
            }
            tokens[token_count].value[j] = '\0';
            tokens[token_count].type = TOKEN_INT_LITERAL;
            token_count++;
            continue;
        }

        if (buffer[i] >= 'a' && buffer[i] <= 'z')
        {
            u32 j = 0;
            while (buffer[i] >= 'a' && buffer[i] <= 'z')
            {
                tokens[token_count].value[j] = buffer[i];
                i++;
                j++;
            }
            tokens[token_count].value[j] = '\0';

            if (strcmp(tokens[token_count].value, "let") == 0)
                tokens[token_count].type = TOKEN_KEYWORD_LET;
            else if (strcmp(tokens[token_count].value, "int") == 0)
                tokens[token_count].type = TOKEN_KEYWORD_INT;
            else
                tokens[token_count].type = TOKEN_IDENTIFIER;

            token_count++;
            continue;
        }

        if (buffer[i] == '\n')
        {
            tokens[token_count].type = TOKEN_EOF;
            token_count++;
            i++;
            continue;
        }

        tokens[token_count].type = TOKEN_ERROR;
        token_count++;
        i++;
    }

    tokens[token_count].type = TOKEN_EOF;
    token_count++;

    return tokens;
}