#!/bin/bash
echo "Removing preexisting coverage (if it exists)"
rm -rf htmlcov
coverage run setup.py test
coverage html --include="ice/*"
open htmlcov/index.html
