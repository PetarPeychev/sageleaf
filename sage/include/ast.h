#pragma once

#include <iostream>

namespace ast
{
    typedef enum NodeType
    {
        IdType,
        IntType,
        AddType,
        SubType,
        ApplyType
    } NodeType;

    struct Node
    {
        NodeType type;

        virtual ~Node() {}
        virtual int eval(bool debug) = 0;
        virtual void show() = 0;
    };

    struct Id : public Node
    {
        NodeType type = IdType;
        std::string name;

        Id(std::string name);
        int eval(bool debug);
        void show();
    };

    struct Int : public Node
    {
        NodeType type = IntType;
        int value;

        Int(int value);
        int eval(bool debug);
        void show();
    };

    struct Add : public Node
    {
        NodeType type = AddType;
        Node *left;
        Node *right;

        Add(Node *left, Node *right);
        ~Add();
        int eval(bool debug);
        void show();
    };

    struct Sub : public Node
    {
        NodeType type = SubType;
        Node *left;
        Node *right;

        Sub(Node *left, Node *right);
        ~Sub();
        int eval(bool debug);
        void show();
    };

    struct Mul : public Node
    {
        NodeType type = SubType;
        Node *left;
        Node *right;

        Mul(Node *left, Node *right);
        ~Mul();
        int eval(bool debug);
        void show();
    };

    struct Div : public Node
    {
        NodeType type = SubType;
        Node *left;
        Node *right;

        Div(Node *left, Node *right);
        ~Div();
        int eval(bool debug);
        void show();
    };

    struct Apply : public Node
    {
        NodeType type = ApplyType;
        Node *func;
        Node *arg;

        Apply(Node *func, Node *arg);
        ~Apply();
        int eval(bool debug);
        void show();
    };
}