#include "../include/codegen.h"

using namespace std;

string generate()
{
    string output = "export function w $main() { \n";
    output += "@start\n";
    output += "\tret 0\n";
    output += "}\n";

    return output;
}

string generate_main()
{
    string output = "export function w $main() { \n";
    output += "@start\n";
    output += "\tret 0\n";
    output += "}\n";

    return output;
}
