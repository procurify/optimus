#!/bin/bash

# fail on first non-zero error code
set -e

if ! [ -x "$(command -v pipenv)" ]; then
  pip install pipenv
fi

pipenv install
pipenv shell
pytest tests
