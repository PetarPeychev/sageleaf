#!/bin/bash

dotnet publish --output "." -r linux-x64 -c Release -p:PublishSingleFile=true -p:PublishTrimmed=true --self-contained true

rm sage.pdb