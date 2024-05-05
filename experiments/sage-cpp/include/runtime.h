#pragma once

#include <iostream>
#include <unordered_map>

#include "ast.h"
#include "typedefs.h"

// struct Env
// {
//     std::unordered_map<std::string, Value *> map;
//     Env *parent;

//     Env();
//     Env(Env *parent);
//     ~Env();
//     void bind(std::string name, Value *value);
//     Value *lookup(std::string name);
// };

enum ValueType
{
    V_None,
    V_Int,
    V_Float,
    V_Str,
    V_Bool
};

union ValueData
{
    i64 int_value;
    f64 float_value;
    std::string str_value;
    bool bool_value;
};

inline std::string value_to_str(ValueType type)
{
    switch (type)
    {
    case V_None:
        return "None";
    case V_Int:
        return "Int";
    case V_Float:
        return "Float";
    case V_Str:
        return "Str";
    case V_Bool:
        return "Bool";
    default:
        return "Unknown";
    }
}

struct Value
{
    ValueType type;
    ValueData data;

    void show()
    {
        std::cout << value_to_str(type) << "(";
        switch (type)
        {
        case V_None:
            std::cout << "none";
            break;
        case V_Int:
            std::cout << data.int_value;
            break;
        case V_Float:
            std::cout << data.float_value;
            break;
        case V_Str:
            std::cout << data.str_value;
            break;
        case V_Bool:
            std::cout << data.bool_value;
            break;
        default:
            std::cout << "unknown";
            break;
        }
        std::cout << ")";
    }
};

// struct Closure : public Value
// {
//     ValueType type = V_Closure;
//     std::string name;
//     ast::Node *body;
//     Env *env;

//     Closure(std::string name, ast::Node *body, Env *env);
//     ~Closure();
//     void show();
// };
