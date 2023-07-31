#include "../include/ast.h"

using namespace ast;

Add::Add(Node *left, Node *right) : left(left), right(right) {}
Add::~Add()
{
    delete left;
    delete right;
}
int Add::eval(bool debug)
{
    if (debug)
    {
        this->show();
        std::cout << " => ";
        std::cout << this->eval(false) << std::endl;
        left->eval(debug);
        right->eval(debug);
        return left->eval(false) + right->eval(false);
    }
    else
        return left->eval(debug) + right->eval(debug);
}
void Add::show()
{
    printf("(");
    left->show();
    printf(" + ");
    right->show();
    printf(")");
}

Sub::Sub(Node *left, Node *right) : left(left), right(right) {}
Sub::~Sub()
{
    delete left;
    delete right;
}
int Sub::eval(bool debug)
{
    if (debug)
    {
        this->show();
        std::cout << " => ";
        std::cout << this->eval(false) << std::endl;
        left->eval(debug);
        right->eval(debug);
        return left->eval(false) - right->eval(false);
    }
    else
        return left->eval(debug) - right->eval(debug);
}
void Sub::show()
{
    printf("(");
    left->show();
    printf(" - ");
    right->show();
    printf(")");
}

Mul::Mul(Node *left, Node *right) : left(left), right(right) {}
Mul::~Mul()
{
    delete left;
    delete right;
}
int Mul::eval(bool debug)
{
    if (debug)
    {
        this->show();
        std::cout << " => ";
        std::cout << this->eval(false) << std::endl;
        left->eval(debug);
        right->eval(debug);
        return left->eval(false) * right->eval(false);
    }
    else
        return left->eval(debug) * right->eval(debug);
}
void Mul::show()
{
    printf("(");
    left->show();
    printf(" * ");
    right->show();
    printf(")");
}

Div::Div(Node *left, Node *right) : left(left), right(right) {}
Div::~Div()
{
    delete left;
    delete right;
}
int Div::eval(bool debug)
{
    if (debug)
    {
        this->show();
        std::cout << " => ";
        std::cout << this->eval(false) << std::endl;
        left->eval(debug);
        right->eval(debug);
        return left->eval(false) / right->eval(false);
    }
    else
        return left->eval(debug) / right->eval(debug);
}
void Div::show()
{
    printf("(");
    left->show();
    printf(" / ");
    right->show();
    printf(")");
}
