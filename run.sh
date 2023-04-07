#!/bin/bash

if [[ -z "$1" ]] ; then
    echo "Must supply the version to be ran, e.g. v1"
    exit 1
fi

python3 $1/main.py
