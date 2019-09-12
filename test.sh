#!/bin/sh

gcc -O3 -fPIC -shared -o librender.so render.c && mypy *.py && python -m unittest discover .
