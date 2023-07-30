#include "../include/sage.h"

using namespace ast;

Int::Int(int value) : value(value) {}
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
void Add::show()
{
    printf("(");
    left->show();
    printf(" + ");
    right->show();
    printf(")");
}
