#!/bin/bash

g++ src/*.cpp -o sage

chmod +x sage

./sage "$@"

