#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

#include "sage.h"

bool is_alpha(char c)
{
    return (c >= 'a' && c <= 'z') || (c >= 'A' && c <= 'Z') || c == '_';
}

bool is_num(char c)
{
    return c >= '0' && c <= '9';
}

bool is_alphanum(char c)
{
    return is_alpha(c) || is_num(c);
}

Token *tokenize(char *code)
{
    Token *tokens = malloc(sizeof(Token) * 1024);
    int num_tokens = 0;
    int i = 0;
    int line = 1;
    int column = 1;

    while (true)
    {
        char c = code[i];

        if (c == '\0')
        {
            break;
        }

        if (c == '\n')
        {
            line++;
            i++;
            column = 1;
        }
        else if (c == ' ' || c == '\t')
        {
            i++;
            column++;
        }
        else if (c == '(')
        {
            tokens[num_tokens] = (Token){
                .type = TOKEN_LPAREN,
                .index_start = i,
                .index_end = i,
                .line_start = line,
                .line_end = line,
                .column_start = column,
                .column_end = column,
            };
            num_tokens++;
            i++;
            column++;
        }
        else if (c == ')')
        {
            tokens[num_tokens] = (Token){
                .type = TOKEN_RPAREN,
                .index_start = i,
                .index_end = i,
                .line_start = line,
                .line_end = line,
                .column_start = column,
                .column_end = column,
            };
            num_tokens++;
            i++;
            column++;
        }
        else if (c == '{')
        {
            tokens[num_tokens] = (Token){
                .type = TOKEN_LCURLY,
                .index_start = i,
                .index_end = i,
                .line_start = line,
                .line_end = line,
                .column_start = column,
                .column_end = column,
            };
            num_tokens++;
            i++;
            column++;
        }
        else if (c == '}')
        {
            tokens[num_tokens] = (Token){
                .type = TOKEN_RCURLY,
                .index_start = i,
                .index_end = i,
                .line_start = line,
                .line_end = line,
                .column_start = column,
                .column_end = column,
            };
            num_tokens++;
            i++;
            column++;
        }
        else if (is_alpha(c))
        {
            int index_start = i;
            int index_end = i;
            int column_start = column;
            int column_end = column;

            while (true)
            {
                i++;
                column++;

                if (code[i] == '\0')
                {
                    break;
                }

                if (!is_alphanum(code[i]))
                {
                    break;
                }

                index_end = i;
                column_end = column;
            }

            char *identifier = malloc(sizeof(char) * (index_end - index_start + 2));
            strncpy(identifier, code + index_start, index_end - index_start + 1);
            identifier[index_end - index_start + 1] = '\0';

            if (strcmp(identifier, "fn") == 0)
            {
                tokens[num_tokens] = (Token){
                    .type = TOKEN_FN,
                    .index_start = index_start,
                    .index_end = index_end,
                    .line_start = line,
                    .line_end = line,
                    .column_start = column_start,
                    .column_end = column_end,
                };
                num_tokens++;
                free(identifier);
            }
            else
            {
                tokens[num_tokens] = (Token){
                    .type = TOKEN_IDENTIFIER,
                    .index_start = index_start,
                    .index_end = index_end,
                    .line_start = line,
                    .line_end = line,
                    .column_start = column_start,
                    .column_end = column_end,
                    .data = identifier,
                };
                num_tokens++;
            }
        }
    }

    tokens[num_tokens] = (Token){
        .type = TOKEN_EOF,
        .index_start = i,
        .index_end = i,
        .line_start = line,
        .line_end = line,
        .column_start = column,
        .column_end = column,
    };

    return tokens;
}

void print_token(Token token)
{
    if (token.type == TOKEN_LPAREN)
    {
        printf("LPAREN(%d, %d, %d, %d)\n", token.line_start, token.line_end, token.column_start, token.column_end);
    }
    else if (token.type == TOKEN_RPAREN)
    {
        printf("RPAREN(%d, %d, %d, %d)\n", token.line_start, token.line_end, token.column_start, token.column_end);
    }
    else if (token.type == TOKEN_LCURLY)
    {
        printf("LCURLY(%d, %d, %d, %d)\n", token.line_start, token.line_end, token.column_start, token.column_end);
    }
    else if (token.type == TOKEN_RCURLY)
    {
        printf("RCURLY(%d, %d, %d, %d)\n", token.line_start, token.line_end, token.column_start, token.column_end);
    }
    else if (token.type == TOKEN_FN)
    {
        printf("FN(%d, %d, %d, %d)\n", token.line_start, token.line_end, token.column_start, token.column_end);
    }
    else if (token.type == TOKEN_IDENTIFIER)
    {
        printf("IDENTIFIER(%s, %d, %d, %d, %d)\n", (char *)token.data, token.line_start, token.line_end, token.column_start, token.column_end);
    }
    else if (token.type == TOKEN_EOF)
    {
        printf("EOF(%d, %d, %d, %d)\n", token.line_start, token.line_end, token.column_start, token.column_end);
    }
}
