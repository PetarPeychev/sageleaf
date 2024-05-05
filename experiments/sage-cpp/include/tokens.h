#pragma once

#include <string>
#include <iostream>

#include "typedefs.h"

typedef enum TokenType
{
    // Single Character Tokens
    T_Add,
    T_Sub,
    T_Mul,
    T_Div,
    T_Exp,
    T_Mod,
    T_Eq,
    T_Lt,
    T_Gt,
    T_Colon,
    T_Semi,
    T_Comma,
    T_Dot,
    T_LParen,
    T_RParen,
    T_LSquirly,
    T_RSquirly,
    T_LSquare,
    T_RSquare,

    // Multi Character Tokens
    T_Arrow,
    T_Pipe,
    T_Lte,
    T_Gte,

    // Keywords
    T_If,
    T_Is,
    T_Then,
    T_Else,
    T_Let,
    T_Type,
    T_Import,
    T_And,
    T_Or,
    T_Not,
    T_IntType,
    T_FloatType,
    T_BoolType,
    T_StrType,
    T_None,
    T_True,
    T_False,

    // Variable Length Tokens
    T_Id,
    T_Int,
    T_Float,
    T_Bool,
    T_Str,
} TokenType;

inline std::string tok_to_str(TokenType t)
{
    switch (t)
    {
    case T_Add:
        return "Add";
    case T_Sub:
        return "Sub";
    case T_Mul:
        return "Mul";
    case T_Div:
        return "Div";
    case T_Exp:
        return "Exp";
    case T_Mod:
        return "Mod";
    case T_Eq:
        return "Eq";
    case T_Lt:
        return "Lt";
    case T_Gt:
        return "Gt";
    case T_Colon:
        return "Colon";
    case T_Semi:
        return "Semi";
    case T_Comma:
        return "Comma";
    case T_Dot:
        return "Dot";
    case T_LParen:
        return "LParen";
    case T_RParen:
        return "RParen";
    case T_LSquirly:
        return "LSquirly";
    case T_RSquirly:
        return "RSquirly";
    case T_LSquare:
        return "LSquare";
    case T_RSquare:
        return "RSquare";
    case T_Arrow:
        return "Arrow";
    case T_Pipe:
        return "Pipe";
    case T_Lte:
        return "Lte";
    case T_Gte:
        return "Gte";
    case T_If:
        return "If";
    case T_Is:
        return "Is";
    case T_Then:
        return "Then";
    case T_Else:
        return "Else";
    case T_Let:
        return "Let";
    case T_Type:
        return "Type";
    case T_Import:
        return "Import";
    case T_And:
        return "And";
    case T_Or:
        return "Or";
    case T_Not:
        return "Not";
    case T_IntType:
        return "IntType";
    case T_FloatType:
        return "FloatType";
    case T_BoolType:
        return "BoolType";
    case T_StrType:
        return "StrType";
    case T_None:
        return "None";
    case T_True:
        return "True";
    case T_False:
        return "False";
    case T_Id:
        return "Id";
    case T_Int:
        return "Int";
    case T_Float:
        return "Float";
    case T_Bool:
        return "Bool";
    case T_Str:
        return "Str";
    default:
        return "Unknown";
    }
}

struct Token
{
    TokenType type;
    std::string value;

    Token(TokenType type, std::string value) : type(type), value(value) {}

    void show()
    {
        std::cout << tok_to_str(this->type) << "(" << value << ")" << std::endl;
    }
};
