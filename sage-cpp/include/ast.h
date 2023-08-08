#pragma once

#include <iostream>
#include <vector>

#include "runtime.h"

typedef enum NodeType
{
    N_File,
    N_Let,
    N_Id,
    N_IntType,
    N_Int
} NodeType;

inline std::string node_to_str(NodeType type)
{
    switch (type)
    {
    case N_File:
        return "File";
    case N_Let:
        return "Let";
    case N_Id:
        return "Id";
    case N_IntType:
        return "IntType";
    case N_Int:
        return "Int";
    default:
        return "Unknown";
    }
}

struct Node
{
    NodeType type;
    Value value;
    std::vector<Node> children;

    void show()
    {
        std::cout << node_to_str(this->type)
                  << "("
                  << value_to_str(this->value.type)
                  << ")"
                  << std::endl;
    }
};
