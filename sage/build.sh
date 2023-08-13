#!/bin/bash

gcc -std=c17 -g -Og -Wall -Wextra -Wpedantic -Wfloat-equal -Wpointer-arith -Wcast-align -Wswitch-enum src/*.c -o sage
