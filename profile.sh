#!/bin/sh

gcc -O3 -fPIC -shared -o librender.so render.c && python profile.py
