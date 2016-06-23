#!/bin/bash

# ${1} = name
# ${2} = workDir

cd "third-party/${1}/${2}"
rm -rf third-party
ln -snf ../../ third-party
cd -
