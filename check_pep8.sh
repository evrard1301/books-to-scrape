#!/usr/bin/sh
python -m pycodestyle $(find . -name "*.py" | grep -v env | grep -v venv)
