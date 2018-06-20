import json
from flask import Flask, jsonify
from flask import render_template, request
from optimus.transformer import transform

app = Flask(__name__)


@app.route('/')
def index():
    with open('tests/fixture_files/vendor.json', 'r') as fsock:
        input_data = json.loads(fsock.read())

    context = dict(input_json=json.dumps(input_data))
    return render_template('index.html', **context)


@app.route('/transform/', methods=['POST'])
def transform_json():
    request_json = request.get_json(silent=True)
    transformed_data = transform(
        request_json['input_json'],
        request_json['schema']
    )

    # validate(transformed_data, request_json['schema'])
    return jsonify(transformed_data)
