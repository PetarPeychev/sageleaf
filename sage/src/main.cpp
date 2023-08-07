// #include "../include/ast.h"
#include "../include/lexer.h"
#include <string.h>
#include <iostream>

using namespace std;
using namespace lexer;

// void test()
// {
//     auto tree = new Sub(
//         new Int(489),
//         new Add(
//             new Mul(
//                 new Int(17),
//                 new Div(
//                     new Int(88),
//                     new Int(44))),
//             new Int(35)));

//     auto env = runtime::Env();
//     tree->eval(env);
//     cout << endl;

//     auto functree = new Apply(
//         new Id("print"),
//         new Int(69));

//     functree->show();
//     cout << endl;

//     delete functree;
//     delete tree;
// }

void lex_test()
{
    // auto tokens = lexer::lex("let int_to_str: int -> str = s -> if s is 1 then \"one\" is 2 then \"two\" is 3 then \"three\" else \"i can't count that high\"");
    // for (auto token : tokens)
    // {
    //     token.show();
    // }
    // cout << endl;
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
        // test();
        auto tokens = lex("let int_to_str: int -> str = s -> if s is 1 then \"one\" is 2 then \"two\" is 3 then \"three\" else \"i can't count that high\"");
        for (auto token : tokens)
        {
            token.show();
        }
        cout << endl;
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
