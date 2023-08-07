#pragma once

#include <string>
#include <vector>

#include "tokens.h"

namespace lexer
{
    std::vector<tokens::Token> lex(std::string);
}
