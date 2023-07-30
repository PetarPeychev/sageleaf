#include "../include/sage.h"

using namespace sage;

Int::Int(int value) : value(value) {}
int Int::eval(bool debug)
{
    // if (debug)
    // {
    //     std::cout << this->eval(false) << std::endl;
    // }
    return value;
}
void Int::show()
{
    std::cout << value;
}

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
