import os
from flask import Flask, jsonify, render_template, request
from optimus.transformer import transform

app = Flask(__name__)

PROD_ENV = 'production'
DEV_ENV = 'development'
FLASK_ENV = os.environ['FLASK_ENV']

if FLASK_ENV == DEV_ENV:
    from flask_cors import CORS

    CORS(app)


@app.route('/')
def index():
    context = {}
    return render_template('old_index.html', **context)


@app.route('/transform/', methods=['POST'])
def transform_json():
    request_json = request.get_json(silent=True)
    transformed_data = transform(
        request_json['input_json'],
        request_json['schema']
    )

    # validate(transformed_data, request_json['schema'])
    return jsonify(transformed_data)
