#pragma once

#include <iostream>

namespace sage
{
    typedef enum NodeType
    {
        IntType,
        AddType,
        SubType
    } NodeType;

    struct Node
    {
        NodeType type;

        virtual ~Node() {}
        virtual int eval(bool debug) = 0;
        virtual void show() = 0;
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
}