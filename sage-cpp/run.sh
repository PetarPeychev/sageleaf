#!/bin/bash

g++ -Wall -Wextra src/*.cpp -o sage

chmod +x sage

./sage "$@"

qbe -o out.asm out.ssa
as -o out.o out.asm
gcc -o out out.o

./out

rm out.asm out.o out.ssa out

