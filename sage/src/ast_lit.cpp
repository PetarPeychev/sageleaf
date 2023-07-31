#include "../include/ast.h"

using namespace ast;
using namespace std;

Id::Id(string name) : name(name) {}
int Id::eval([[maybe_unused]] bool debug)
{
    throw std::runtime_error("Eval Error: Attempted to evaluate an identifier.");
}
void Id::show()
{
    std::cout << name;
}

Int::Int(int value) : value(value) {}
int Int::eval([[maybe_unused]] bool debug)
{
    return value;
}
void Int::show()
{
    std::cout << value;
}