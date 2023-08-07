// #include "../include/ast.h"

// using namespace ast;

// Add::Add(Node *left, Node *right) : left(left), right(right) {}

// Add::~Add()
// {
//     delete left;
//     delete right;
// }

// runtime::Value *Add::eval(runtime::Env &env)
// {
//     auto l = this->left->eval(env);
//     auto r = this->right->eval(env);
//     runtime::Value *res;
//     if (l->type == runtime::V_Int && r->type == runtime::V_Int)
//     {
//         res = new runtime::Int(((runtime::Int *)l)->value + ((runtime::Int *)r)->value);
//     }
//     delete l;
//     delete r;
//     return res;
// }

// void Add::show()
// {
//     printf("(");
//     left->show();
//     printf(" + ");
//     right->show();
//     printf(")");
// }

// Sub::Sub(Node *left, Node *right) : left(left), right(right) {}

// Sub::~Sub()
// {
//     delete left;
//     delete right;
// }

// runtime::Value *Sub::eval(runtime::Env &env)
// {
//     auto l = this->left->eval(env);
//     auto r = this->right->eval(env);
//     runtime::Value *res;
//     if (l->type == runtime::V_Int && r->type == runtime::V_Int)
//     {
//         res = new runtime::Int(((runtime::Int *)l)->value - ((runtime::Int *)r)->value);
//     }
//     delete l;
//     delete r;
//     return res;
// }

// void Sub::show()
// {
//     printf("(");
//     left->show();
//     printf(" - ");
//     right->show();
//     printf(")");
// }

// Mul::Mul(Node *left, Node *right) : left(left), right(right) {}

// Mul::~Mul()
// {
//     delete left;
//     delete right;
// }

// runtime::Value *Mul::eval(runtime::Env &env)
// {
//     auto l = this->left->eval(env);
//     auto r = this->right->eval(env);
//     runtime::Value *res;
//     if (l->type == runtime::V_Int && r->type == runtime::V_Int)
//     {
//         res = new runtime::Int(((runtime::Int *)l)->value * ((runtime::Int *)r)->value);
//     }
//     delete l;
//     delete r;
//     return res;
// }

// void Mul::show()
// {
//     printf("(");
//     left->show();
//     printf(" * ");
//     right->show();
//     printf(")");
// }

// Div::Div(Node *left, Node *right) : left(left), right(right) {}

// Div::~Div()
// {
//     delete left;
//     delete right;
// }

// runtime::Value *Div::eval(runtime::Env &env)
// {
//     auto l = this->left->eval(env);
//     auto r = this->right->eval(env);
//     runtime::Value *res;
//     if (l->type == runtime::V_Int && r->type == runtime::V_Int)
//     {
//         res = new runtime::Int(((runtime::Int *)l)->value / ((runtime::Int *)r)->value);
//     }
//     delete l;
//     delete r;
//     return res;
// }

// void Div::show()
// {
//     printf("(");
//     left->show();
//     printf(" / ");
//     right->show();
//     printf(")");
// }
