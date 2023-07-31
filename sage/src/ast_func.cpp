#include "../include/ast.h"

using namespace ast;

Apply::Apply(Node *func, Node *arg) : func(func), arg(arg) {}
Apply::~Apply()
{
    delete func;
    delete arg;
}
int Apply::eval([[maybe_unused]] bool debug)
{
    throw std::runtime_error("Eval Error: Evaluation of function application is not yet implemented.");
}
void Apply::show()
{
    printf("(");
    func->show();
    printf(" ");
    arg->show();
    printf(")");
}
