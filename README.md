# Optimus
![Build status](https://travis-ci.com/procurify/optimus.svg?branch=master "Optimus build status")

A schema transformation tool using JSON Schema and JSONPath


## Features
- Field renaming
- Function execution on field values

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

### Run UI

`npm run dev`
