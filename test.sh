#!/bin/bash

if [[ -z "$1" ]] ; then
    echo "Must supply the version to test, e.g. v1"
    exit 1
fi

python3 -m unittest discover -s $1/tests -p "*_test.py" -v
