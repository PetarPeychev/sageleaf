// #pragma once

// #include <iostream>
// #include "runtime.h"

// namespace ast
// {
//     typedef enum NodeType
//     {
//         N_Id,
//         N_None,
//         N_Int,
//         N_Add,
//         N_Sub,
//         N_Apply
//     } NodeType;

//     struct Node
//     {
//         NodeType type;

//         virtual ~Node() {}
//         virtual runtime::Value *eval(runtime::Env &env) = 0;
//         virtual void show() = 0;
//     };

//     struct Id : public Node
//     {
//         NodeType type = N_Id;
//         std::string name;

//         Id(std::string name);
//         runtime::Value *eval(runtime::Env &env);
//         void show();
//     };

//     struct None : public Node
//     {
//         NodeType type = N_None;

//         runtime::Value *eval(runtime::Env &env);
//         void show();
//     };

//     struct Int : public Node
//     {
//         NodeType type = N_Int;
//         int value;

//         Int(int value);
//         runtime::Value *eval(runtime::Env &env);
//         void show();
//     };

//     struct Add : public Node
//     {
//         NodeType type = N_Add;
//         Node *left;
//         Node *right;

//         Add(Node *left, Node *right);
//         ~Add();
//         runtime::Value *eval(runtime::Env &env);
//         void show();
//     };

//     struct Sub : public Node
//     {
//         NodeType type = N_Sub;
//         Node *left;
//         Node *right;

//         Sub(Node *left, Node *right);
//         ~Sub();
//         runtime::Value *eval(runtime::Env &env);
//         void show();
//     };

//     struct Mul : public Node
//     {
//         NodeType type = N_Sub;
//         Node *left;
//         Node *right;

//         Mul(Node *left, Node *right);
//         ~Mul();
//         runtime::Value *eval(runtime::Env &env);
//         void show();
//     };

//     struct Div : public Node
//     {
//         NodeType type = N_Sub;
//         Node *left;
//         Node *right;

//         Div(Node *left, Node *right);
//         ~Div();
//         runtime::Value *eval(runtime::Env &env);
//         void show();
//     };

//     struct Apply : public Node
//     {
//         NodeType type = N_Apply;
//         Node *func;
//         Node *arg;

//         Apply(Node *func, Node *arg);
//         ~Apply();
//         runtime::Value *eval(runtime::Env &env);
//         void show();
//     };
// }