#include "../include/ast.h"
#include <string.h>

using namespace ast;
using namespace std;

void test()
{
    auto tree = new Sub(
        new Int(489),
        new Add(
            new Mul(
                new Int(17),
                new Div(
                    new Int(88),
                    new Int(44))),
            new Int(35)));

    tree->eval(true);
    cout << endl;

    auto functree = new Apply(
        new Id("print"),
        new Apply(
            new Id("str"),
            new Int(69)));

    functree->show();
    cout << endl;

    delete functree;
    delete tree;
}

int main(int argc, char *argv[])
{
    if (argc == 1)
    {
        cout << "Sageleaf: A simple programming language\n\n"
                "Usage: sage [file]"
             << endl;
    }
    else if ((argc == 2) && (strcmp(argv[1], "test") == 0))
    {
        test();
    }
    else if (argc == 2)
    {
        cout << "File: " << argv[1] << endl;
    }
    else
    {
        cout << "Error: Incorrect number of arguments.\n\n"
                "Usage: sage [file]"
             << endl;
    }
}
