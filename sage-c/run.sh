#!/bin/bash

./build.sh
chmod +x sage
./sage "$@"