#include <iostream>

#include "../include/lexer.h"
#include "../include/utils.h"

using namespace std;

int main(int argc, char *argv[])
{
    if (argc == 1)
    {
        cout << "Sageleaf: A simple programming language\n\n"
                "Usage: sage [file]"
             << endl;
    }
    else if (argc == 2)
    {
        auto tokens = lex(read_file(argv[1]));
        for (auto token : tokens)
        {
            token.show();
        }
    }
    else
    {
        cout << "Error: Incorrect number of arguments.\n\n"
                "Usage: sage [file]"
             << endl;
    }
}
