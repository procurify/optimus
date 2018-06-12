import json
from flask import Flask, jsonify
from flask import render_template, request, abort
from transform import generate_transformation, transformer

app = Flask(__name__)


@app.route('/')
def index():
    with open('input.json', 'r') as fsock:
        input_data = json.loads(fsock.read())

    context = dict(input_json=json.dumps(input_data))
    return render_template('index.html', **context)


@app.route('/transform/', methods=['POST'])
def transform_json():
    request_json = request.get_json(silent=True)
    transformation = generate_transformation(request_json['schema'])

    transformed_data = transformer(
        request_json['input_json'],
        transformation
    )

    # validate(transformed_data, request_json['schema'])
    return jsonify(transformed_data)
