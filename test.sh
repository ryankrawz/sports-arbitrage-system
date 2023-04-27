#!/bin/bash

if [[ -z "$1" ]] ; then
    echo "Must supply the version to be ran, e.g. v1"
    exit 1
fi

if [[ -z "$2" ]] ; then
    echo "Must supply the test module, e.g. login"
    exit 1
fi

python3 -m unittest $1/tests/$2.py
