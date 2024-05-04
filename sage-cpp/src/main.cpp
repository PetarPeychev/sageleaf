#include <fstream>
#include <iostream>

#include "../include/codegen.h"
#include "../include/lexer.h"
#include "../include/utils.h"

using namespace std;

int main(int argc, char *argv[])
{
    // if (argc == 1)
    // {
    //     cout << "Sageleaf: A programming language\n\n"
    //             "Usage: sage [file]"
    //          << endl;
    // }
    // else if (argc == 2)
    // {
    //     auto tokens = lex(read_file(argv[1]));
    //     for (auto token : tokens) { token.show(); }
    // }
    // else
    // {
    //     cout << "Error: Incorrect number of arguments.\n\n"
    //             "Usage: sage [file]"
    //          << endl;
    // }

    ofstream output("out.ssa");
    output << generate_qbe();
    output.close();
}
