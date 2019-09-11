#!/bin/sh

mypy *.py && python -m unittest discover .
