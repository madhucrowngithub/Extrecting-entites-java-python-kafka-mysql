#!/bin/bash

if [ ! -z "$PYTHON_ENV" ]; then
    OS=$(uname | perl -ne 'if (m/cygwin/i) { print "WINDOWS" } else { print "LINUX"; }')

    if [ "$OS" == "WINDOWS" ]; then
      source $PYTHON_ENV/Scripts/activate
    else
      source $PYTHON_ENV/bin/activate
    fi
fi

rm -rf dist/*.whl build &&
python setup.py bdist_wheel &&
rm -rf build &&
deactivate
