#!/bin/bash

qbe -o $1.asm $1.ssa
as -o $1.o $1.asm
gcc -o $1 $1.o

./$1

rm $1.asm $1.o
