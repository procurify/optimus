#!/bin/bash

# fail on first non-zero error code
set -e

if ! [ -x "$(command -v pipenv)" ]; then
  pip install pipenv
fi

pipenv install --dev
$(pipenv --venv)/bin/pytest tests -vv
