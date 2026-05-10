#!/bin/bash

gcc -std=c99 -o build/sage src/*.c
./build/sage build test/"$1".sl
./test/"$1"
echo $?
rm ./test/"$1"
