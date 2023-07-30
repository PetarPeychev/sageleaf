#pragma once

#include <iostream>

namespace ast
{
    struct Node
    {
        virtual ~Node() {}
        virtual void show() = 0;
    };

    struct Int : public Node
    {
        Int(int value);
        int value;
        void show();
    };

    struct Add : public Node
    {
        Add(Node *left, Node *right);
        ~Add();
        Node *left;
        Node *right;
        void show();
    };
}