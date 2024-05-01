// #include "../include/runtime.h"

// using namespace runtime;

// Env::Env() {}

// Env::Env(Env *parent) : parent(parent) {}

// Env::~Env()
// {
//     for (auto &pair : this->map)
//     {
//         delete pair.second;
//     }
// }

// void Env::bind(std::string name, Value *value)
// {
//     this->map[name] = value;
// }

// Value *Env::lookup(std::string name)
// {
//     if (this->map.find(name) != this->map.end())
//     {
//         return this->map[name];
//     }
//     else if (this->parent != nullptr)
//     {
//         return this->parent->lookup(name);
//     }
//     else
//     {
//         return nullptr;
//     }
// }

// void None::show()
// {
//     std::cout << "none: none";
// }

// Int::Int(int value) : value(value) {}

// void Int::show()
// {
//     std::cout << "int: " << value;
// }