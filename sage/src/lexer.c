#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <stdarg.h>

#include "lexer.h"
#include "config.h"

#define stoken(token)                 \
    tokens[token_count].type = token; \
    token_count++;                    \
    i++;                              \
    continue

#define mtoken(token, size)           \
    tokens[token_count].type = token; \
    token_count++;                    \
    i += size;                        \
    continue

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
                mtoken(TOKEN_ARROW, 2);
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
                mtoken(TOKEN_LTE, 2);
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
                mtoken(TOKEN_GTE, 2);
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
                stoken(TOKEN_ERROR);
            }

            tokens[token_count].value[j] = '\0';
            stoken(TOKEN_STR_LITERAL);
        }

        /* -------------- Comments -------------- */
        if (buffer[i] == '#')
        {
            while (buffer[i] != '\n' && buffer[i] != '\0')
                i++;
            continue;
        }

        /* -------------- If none of the above, Error -------------- */
        stoken(TOKEN_ERROR);
    }

    /* -------------- End of File -------------- */
    tokens[token_count].type = TOKEN_EOF;
    token_count++;

    return tokens;
}

char *token_type_to_string(TokenType type)
{
    switch (type)
    {
    case TOKEN_KEYWORD_LET:
        return "let";
    case TOKEN_KEYWORD_VAR:
        return "var";
    case TOKEN_KEYWORD_TYPE:
        return "type";
    case TOKEN_KEYWORD_IMPORT:
        return "import";
    case TOKEN_KEYWORD_AND:
        return "and";
    case TOKEN_KEYWORD_OR:
        return "or";
    case TOKEN_KEYWORD_NOT:
        return "not";
    case TOKEN_KEYWORD_IF:
        return "if";
    case TOKEN_KEYWORD_IS:
        return "is";
    case TOKEN_KEYWORD_THEN:
        return "then";
    case TOKEN_KEYWORD_ELSE:
        return "else";
    case TOKEN_KEYWORD_INT:
        return "int";
    case TOKEN_KEYWORD_STR:
        return "str";
    case TOKEN_KEYWORD_FLOAT:
        return "float";
    case TOKEN_KEYWORD_BOOL:
        return "bool";
    case TOKEN_KEYWORD_NONE:
        return "none";
    case TOKEN_KEYWORD_ANY:
        return "any";
    case TOKEN_KEYWORD_TRUE:
        return "true";
    case TOKEN_KEYWORD_FALSE:
        return "false";
    case TOKEN_IDENTIFIER:
        return "id";
    case TOKEN_COLON:
        return ":";
    case TOKEN_SEMICOLON:
        return ";";
    case TOKEN_COMMA:
        return ",";
    case TOKEN_EQUALS:
        return "=";
    case TOKEN_ADD:
        return "+";
    case TOKEN_SUB:
        return "-";
    case TOKEN_MUL:
        return "*";
    case TOKEN_DIV:
        return "/";
    case TOKEN_MOD:
        return "%";
    case TOKEN_LT:
        return "<";
    case TOKEN_GT:
        return ">";
    case TOKEN_LPAREN:
        return "(";
    case TOKEN_RPAREN:
        return ")";
    case TOKEN_LSQUARE:
        return "[";
    case TOKEN_RSQUARE:
        return "]";
    case TOKEN_LSQUIRLY:
        return "{";
    case TOKEN_RSQUIRLY:
        return "}";
    case TOKEN_ARROW:
        return "->";
    case TOKEN_PIPE:
        return "|>";
    case TOKEN_GTE:
        return ">=";
    case TOKEN_LTE:
        return "<=";
    case TOKEN_INT_LITERAL:
        return "int";
    case TOKEN_STR_LITERAL:
        return "str";
    case TOKEN_ERROR:
        return "error";
    case TOKEN_EOF:
        return "eof";
    default:
        return "error";
    }
}

int vasprintf(char **str, const char *fmt, va_list args)
{
    int size = 0;
    va_list tmpa;

    // copy
    va_copy(tmpa, args);

    // apply variadic arguments to
    // sprintf with format to get size
    size = vsnprintf(NULL, 0, fmt, tmpa);

    // toss args
    va_end(tmpa);

    // return -1 to be compliant if
    // size is less than 0
    if (size < 0)
    {
        return -1;
    }

    // alloc with size plus 1 for `\0'
    *str = (char *)malloc(size + 1);

    // return -1 to be compliant
    // if pointer is `NULL'
    if (NULL == *str)
    {
        return -1;
    }

    // format string with original
    // variadic arguments and set new size
    size = vsprintf(*str, fmt, args);
    return size;
}

int asprintf(char **str, const char *fmt, ...)
{
    int size = 0;
    va_list args;

    // init variadic argumens
    va_start(args, fmt);

    // format and get size
    size = vasprintf(str, fmt, args);

    // toss args
    va_end(args);

    return size;
}

char *token_to_string(Token *token)
{
#pragma GCC diagnostic push
#pragma GCC diagnostic ignored "-Wswitch-enum"
    char *string;
    switch (token->type)
    {
    case TOKEN_INT_LITERAL:
    case TOKEN_IDENTIFIER:
        return token->value;
    case TOKEN_STR_LITERAL:
        if (0 > asprintf(&string, "\"%s\"", token->value))
            return "error";
        return string;
    default:
        return token_type_to_string(token->type);
    }

#pragma GCC diagnostic pop
}