#include <iostream>

#include "../include/tokens.h"

using namespace tokens;

Token::Token(TokenType type, std::string value) : type(type), value(value) {}

void Token::show()
{
    std::cout << "Token(" << type << ", " << value << ")" << std::endl;
}
