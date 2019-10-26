# Optimus
![Build status](https://travis-ci.com/procurify/optimus.svg?branch=master "Optimus build status")

A schema transformation tool using JSON Schema and JSONPath


## Features
- Field renaming
- Function execution on field values
- We're using the [jsonpath-rw](https://github.com/kennknowles/python-jsonpath-rw) library to parse JSON. So take a look at the [library's docs](https://github.com/kennknowles/python-jsonpath-rw#jsonpath-syntax) to get more information about the available options.

## Limitations
- Can't map nested field to a root field

## How To

### Setup environment

* `pipenv install`
* `pipenv shell`

### Run tests

`pytest`

### Run application

`FLASK_APP=app.py FLASK_ENV=development python -m flask run`
