#!/bin/bash

g++ -Wall -Wextra src/*.cpp -o sage

chmod +x sage

./sage "$@"

