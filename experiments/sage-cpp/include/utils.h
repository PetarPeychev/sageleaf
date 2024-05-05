#pragma once

#include <string>
#include <fstream>
#include <sstream>

std::string read_file(std::string filename)
{
    std::ifstream fstream(filename);
    std::stringstream buffer;
    buffer << fstream.rdbuf();
    std::string file_content = buffer.str();
    return file_content;
}