#include <stdlib.h>
#include <stdio.h>
#include <string.h>

#include "lexer.h"
#include "config.h"

#define stoken(token) tokens[token_count].type = token; token_count++; i++; continue

Token *lex(char *buffer)
{
    Token *tokens = malloc(sizeof(Token) * MAX_TOKENS);
    u32 token_count = 0;

    u32 i = 0;
    while (buffer[i] != '\0')
    {
        if (token_count >= MAX_TOKENS)
        {
            fprintf(stderr, "Error: Exceeded maximum number of tokens (%d)\n", MAX_TOKENS);
            exit(1);
        }

        /* -------------- Whitespace -------------- */
        if (buffer[i] == ' ' || buffer[i] == '\n' || buffer[i] == '\t')
        {
            i++;
            continue;
        }

        /* -------------- Single-Character Symbols -------------- */
        switch (buffer[i])
        {
            case ':':
            stoken(TOKEN_COLON);
            case ';':
            stoken(TOKEN_SEMICOLON);
            case ',':
            stoken(TOKEN_COMMA);
            case '=':
            stoken(TOKEN_EQUALS);
            case '+':
            stoken(TOKEN_ADD);
            case '*':
            stoken(TOKEN_MUL);
            case '/':
            stoken(TOKEN_DIV);
            case '%':
            stoken(TOKEN_MOD);
            case '(':
            stoken(TOKEN_LPAREN);
            case ')':
            stoken(TOKEN_RPAREN);
            case '[':
            stoken(TOKEN_LSQUARE);
            case ']':
            stoken(TOKEN_RSQUARE);
            case '{':
            stoken(TOKEN_LSQUIRLY);
            case '}':
            stoken(TOKEN_RSQUIRLY);
        }

        /* -------------- Multi-Character Symbols -------------- */
        if (buffer[i] == '-')
        {
            if (buffer[i + 1] == '>')
            {
                tokens[token_count].type = TOKEN_ARROW;
                token_count++;
                i += 2;
                continue;
            }
            else
            {
                stoken(TOKEN_SUB);
            }
        }

        if (buffer[i] == '<')
        {
            if (buffer[i + 1] == '=')
            {
                tokens[token_count].type = TOKEN_LTE;
                token_count++;
                i += 2;
                continue;
            }
            else
            {
                stoken(TOKEN_LT);
            }
        }

        if (buffer[i] == '>')
        {
            if (buffer[i + 1] == '=')
            {
                tokens[token_count].type = TOKEN_GTE;
                token_count++;
                i += 2;
                continue;
            }
            else
            {
                stoken(TOKEN_GT);
            }
        }

        /* -------------- Integers Literals -------------- */
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

        /* -------------- Keywords and Identifiers -------------- */
        if ((buffer[i] >= 'a' && buffer[i] <= 'z') || buffer[i] == '_')
        {
            u32 j = 0;
            while (buffer[i] != '\0' && ((buffer[i] >= 'a' && buffer[i] <= 'z') || buffer[i] == '_'))
            {
                tokens[token_count].value[j] = buffer[i];
                i++;
                j++;
            }
            tokens[token_count].value[j] = '\0';

            if (strcmp(tokens[token_count].value, "let") == 0)
                tokens[token_count].type = TOKEN_KEYWORD_LET;
            else if (strcmp(tokens[token_count].value, "var") == 0)
                tokens[token_count].type = TOKEN_KEYWORD_VAR;
            else if (strcmp(tokens[token_count].value, "type") == 0)
                tokens[token_count].type = TOKEN_KEYWORD_TYPE;
            else if (strcmp(tokens[token_count].value, "import") == 0)
                tokens[token_count].type = TOKEN_KEYWORD_IMPORT;
            else if (strcmp(tokens[token_count].value, "and") == 0)
                tokens[token_count].type = TOKEN_KEYWORD_AND;
            else if (strcmp(tokens[token_count].value, "or") == 0)
                tokens[token_count].type = TOKEN_KEYWORD_OR;
            else if (strcmp(tokens[token_count].value, "not") == 0)
                tokens[token_count].type = TOKEN_KEYWORD_NOT;
            else if (strcmp(tokens[token_count].value, "if") == 0)
                tokens[token_count].type = TOKEN_KEYWORD_IF;
            else if (strcmp(tokens[token_count].value, "is") == 0)
                tokens[token_count].type = TOKEN_KEYWORD_IS;
            else if (strcmp(tokens[token_count].value, "then") == 0)
                tokens[token_count].type = TOKEN_KEYWORD_THEN;
            else if (strcmp(tokens[token_count].value, "else") == 0)
                tokens[token_count].type = TOKEN_KEYWORD_ELSE;
            else if (strcmp(tokens[token_count].value, "int") == 0)
                tokens[token_count].type = TOKEN_KEYWORD_INT;
            else if (strcmp(tokens[token_count].value, "str") == 0)
                tokens[token_count].type = TOKEN_KEYWORD_STR;
            else if (strcmp(tokens[token_count].value, "float") == 0)
                tokens[token_count].type = TOKEN_KEYWORD_FLOAT;
            else if (strcmp(tokens[token_count].value, "bool") == 0)
                tokens[token_count].type = TOKEN_KEYWORD_BOOL;
            else if (strcmp(tokens[token_count].value, "none") == 0)
                tokens[token_count].type = TOKEN_KEYWORD_NONE;
            else if (strcmp(tokens[token_count].value, "any") == 0)
                tokens[token_count].type = TOKEN_KEYWORD_ANY;
            else if (strcmp(tokens[token_count].value, "true") == 0)
                tokens[token_count].type = TOKEN_KEYWORD_TRUE;
            else if (strcmp(tokens[token_count].value, "false") == 0)
                tokens[token_count].type = TOKEN_KEYWORD_FALSE;
            else
                tokens[token_count].type = TOKEN_IDENTIFIER;

            token_count++;
            continue;
        }

        /* -------------- String Literals -------------- */
        if (buffer[i] == '"')
        {
            u32 j = 0;
            i++;
            while (buffer[i] != '"' && buffer[i] != '\0')
            {
                tokens[token_count].value[j] = buffer[i];
                i++;
                j++;
            }

            if (buffer[i] == '\0')
            {
                tokens[token_count].type = TOKEN_ERROR;
                token_count++;
                i++;
                continue;
            }

            tokens[token_count].value[j] = '\0';
            tokens[token_count].type = TOKEN_STR_LITERAL;
            token_count++;
            i++;
            continue;
        }

        /* -------------- Comments -------------- */
        if (buffer[i] == '#')
        {
            while (buffer[i] != '\n' && buffer[i] != '\0')
                i++;
            continue;
        }

        /* -------------- If none of the above, Error -------------- */
        tokens[token_count].type = TOKEN_ERROR;
        token_count++;
        i++;
    }

    /* -------------- End of File -------------- */
    tokens[token_count].type = TOKEN_EOF;
    token_count++;

    return tokens;
}
