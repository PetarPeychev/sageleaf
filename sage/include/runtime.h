#pragma once

#include <iostream>
#include <unordered_map>
#include "ast.h"

namespace runtime
{
    struct Env
    {
        std::unordered_map<std::string, Value *> map;
        Env *parent;

        Env();
        Env(Env *parent);
        ~Env();
        void bind(std::string name, Value *value);
        Value *lookup(std::string name);
    };

    enum ValueType
    {
        V_None,
        V_Int,
        V_Closure
    };

    struct Value
    {
        ValueType type;
        virtual ~Value() {}
        virtual void show() = 0;
    };

    struct None : public Value
    {
        ValueType type = V_None;

        void show();
    };

    struct Int : public Value
    {
        ValueType type = V_Int;
        int value;

        Int(int value);
        void show();
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
}