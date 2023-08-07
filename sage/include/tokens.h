#pragma once

#include <string>

#include "typedefs.h"

namespace tokens
{
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

    struct Token
    {
        TokenType type;
        std::string value;

        Token(TokenType type, std::string value);
        void show();
    };
}
