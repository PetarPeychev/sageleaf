#include "../include/sage.h"
#include <string.h>

using namespace ast;
using namespace std;

void test()
{
    Int *a = new Int(34);
    Int *b = new Int(35);
    Add *c = new Add(a, b);

    c->show();
    cout << endl;

    delete c;
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
