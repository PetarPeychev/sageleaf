#include <iostream>

#include "../include/lexer.h"

using namespace std;

bool is_digit(char c)
{
    return c >= '0' && c <= '9';
}

bool is_alpha(char c)
{
    return (c >= 'a' && c <= 'z') || (c >= 'A' && c <= 'Z') || c == '_';
}

bool is_alphanum(char c)
{
    return is_digit(c) || is_alpha(c);
}

bool match(string input, int i, string pattern)
{
    for (size_t j = 0; j < pattern.length(); j++)
    {
        if (input[i + j] != pattern[j])
        {
            return false;
        }
    }
    return true;
}

vector<Token> lex(string input)
{
    vector<Token> tokens;
    for (size_t i = 0; i < input.length(); i++)
    {
        char c = input[i];
        if (c == ' ' || c == '\t' || c == '\n')
        {
        }
        else if (match(input, i, "->"))
        {
            tokens.push_back(Token(T_Arrow, "->"));
            i += 2;
        }
        else if (match(input, i, "|>"))
        {
            tokens.push_back(Token(T_Pipe, "|>"));
            i += 2;
        }
        else if (match(input, i, "<="))
        {
            tokens.push_back(Token(T_Lte, "<="));
            i += 2;
        }
        else if (match(input, i, ">="))
        {
            tokens.push_back(Token(T_Gte, ">="));
            i += 2;
        }
        else if (c == '+')
        {
            tokens.push_back(Token(T_Add, "+"));
        }
        else if (c == '-')
        {
            tokens.push_back(Token(T_Sub, "-"));
        }
        else if (c == '*')
        {
            tokens.push_back(Token(T_Mul, "*"));
        }
        else if (c == '/')
        {
            tokens.push_back(Token(T_Div, "/"));
        }
        else if (c == '^')
        {
            tokens.push_back(Token(T_Exp, "^"));
        }
        else if (c == '%')
        {
            tokens.push_back(Token(T_Mod, "%"));
        }
        else if (c == '=')
        {
            tokens.push_back(Token(T_Eq, "="));
        }
        else if (c == '<')
        {
            tokens.push_back(Token(T_Lt, "<"));
        }
        else if (c == '>')
        {
            tokens.push_back(Token(T_Gt, ">"));
        }
        else if (c == ':')
        {
            tokens.push_back(Token(T_Colon, ":"));
        }
        else if (c == ';')
        {
            tokens.push_back(Token(T_Semi, ";"));
        }
        else if (c == ',')
        {
            tokens.push_back(Token(T_Comma, ","));
        }
        else if (c == '.')
        {
            tokens.push_back(Token(T_Dot, ","));
        }
        else if (c == '(')
        {
            tokens.push_back(Token(T_LParen, "("));
        }
        else if (c == ')')
        {
            tokens.push_back(Token(T_RParen, ")"));
        }
        else if (c == '{')
        {
            tokens.push_back(Token(T_LSquirly, "{"));
        }
        else if (c == '}')
        {
            tokens.push_back(Token(T_RSquirly, "}"));
        }
        else if (c == '[')
        {
            tokens.push_back(Token(T_LSquare, "["));
        }
        else if (c == ']')
        {
            tokens.push_back(Token(T_RSquare, "]"));
        }
        else if (is_alpha(c))
        {
            string value = {c};
            while (true)
            {
                if (i + 1 >= input.length())
                    break;
                char next = input[i + 1];
                if (is_alphanum(next))
                {
                    value += next;
                    i++;
                }
                else
                {
                    break;
                }
            }
            if (value == "if")
                tokens.push_back(Token(T_If, value));
            else if (value == "is")
                tokens.push_back(Token(T_Is, value));
            else if (value == "then")
                tokens.push_back(Token(T_Then, value));
            else if (value == "else")
                tokens.push_back(Token(T_Else, value));
            else if (value == "let")
                tokens.push_back(Token(T_Let, value));
            else if (value == "type")
                tokens.push_back(Token(T_Type, value));
            else if (value == "import")
                tokens.push_back(Token(T_Import, value));
            else if (value == "and")
                tokens.push_back(Token(T_And, value));
            else if (value == "or")
                tokens.push_back(Token(T_Or, value));
            else if (value == "not")
                tokens.push_back(Token(T_Not, value));
            else if (value == "int")
                tokens.push_back(Token(T_IntType, value));
            else if (value == "float")
                tokens.push_back(Token(T_FloatType, value));
            else if (value == "bool")
                tokens.push_back(Token(T_BoolType, value));
            else if (value == "str")
                tokens.push_back(Token(T_StrType, value));
            else if (value == "none")
                tokens.push_back(Token(T_None, value));
            else if (value == "true")
                tokens.push_back(Token(T_True, value));
            else if (value == "false")
                tokens.push_back(Token(T_False, value));
            else
                tokens.push_back(Token(T_Id, value));
        }
        else if (is_digit(c))
        {
            string value = {c};
            bool decimal = false;
            while (true)
            {
                if (i + 1 >= input.length())
                    break;
                char next = input[i + 1];
                if (is_digit(next))
                {
                    value += next;
                    i++;
                }
                else if (next == '.')
                {
                    if (decimal)
                    {
                        cout << "Unexpected character: " << next << endl;
                        exit(1);
                    }
                    else
                    {
                        decimal = true;
                        value += next;
                        i++;
                    }
                }
                else
                {
                    break;
                }
            }
            if (decimal)
                tokens.push_back(Token(T_Float, value));
            else
                tokens.push_back(Token(T_Int, value));
        }
        else if (c == '"')
        {
            string value = "";
            i++;
            while (true)
            {
                if (i >= input.length())
                    break;
                char next = input[i];
                if (next == '"')
                {
                    break;
                }
                else
                {
                    value += next;
                    i++;
                }
            }
            tokens.push_back(Token(T_Str, value));
        }
        else if (c == '#')
        {
            while (true)
            {
                if (i >= input.length())
                    break;
                char next = input[i];
                if (next == '\n')
                {
                    break;
                }
                else
                {
                    i++;
                }
            }
        }
        else
        {
            cout << "Unexpected character: " << c << endl;
            exit(1);
        }
    }
    return tokens;
}
