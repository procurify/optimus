import json
from jsonschema import validate
from jsonpath_rw import jsonpath, parse
from flask import Flask, jsonify
from flask import render_template, request, abort
from transform import generate_transformation, transformer


app = Flask(__name__)


@app.route('/')
def index():
    with open('input.json', 'r') as fsock:
        input_data =  json.loads(fsock.read())

    with open('schema.json', 'r') as fsock:
        schema = json.loads(fsock.read())

    transformation = generate_transformation(schema)

    print(transformer(input_data, transformation))
    # validate(transformation, schema)

    context = dict(input_json=json.dumps(input_data))
    return render_template('index.html', **context)

