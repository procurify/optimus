import inspect
from collections import namedtuple
from six import string_types
from jsonpath_rw import parse

from optimus import functions
from optimus.utils import rreplace

Tuple = namedtuple('Tuple', ['path'])
Function = namedtuple('Function', ['name', 'values', 'args'])


def _handle_function(input_data, func):
    function = getattr(functions, func.name, None)
    assert function is not None, (
        "{} is not an available function"
    ).format(func.name)

    values = []
    for value in func.values:
        expr = parse(value)
        parsed_value = [m.value for m in expr.find(input_data)][0]
        values.append(parsed_value)
    assert len(func.values) == len(values), "Unable parse some values"

    args = values + func.args
    _required_no_of_args = inspect.getargspec(function).args
    assert len(_required_no_of_args) == len(args), (
        "Number of arguments mismatch. {} != {}".format(
            len(_required_no_of_args), len(args)
        )
    )

    return function(*args)


def generate_transformation(input_data, schema, source_prefix=''):
    output = {}

    for key, value in schema['properties'].items():
        _source_prefix = source_prefix + '.' if source_prefix else ''

        _input_data = ''
        if value['type'] in ('array', 'object'):
            expr = parse(value['source'])
            _input_data = [i.value for i in expr.find(input_data)]

        if value['type'] == 'array':
            if not value['source'].endswith('[*]'):
                continue

            _results = []
            for index, item in enumerate(_input_data):
                _source_suffix = rreplace(
                    value['source'],
                    '[*]',
                    '[{}]'.format(index),
                    1
                )

                _results.append(generate_transformation(
                    input_data=item,
                    schema=value['items'],
                    source_prefix=_source_prefix + _source_suffix
                ))

            output[key] = _results

        elif value['type'] == 'object':
            output[key] = generate_transformation(
                input_data=_input_data[0],
                schema=value,
                source_prefix=_source_prefix + value['source']
            )

        elif value['type'] == 'function':
            assert len(value['source']) == 3
            function_name, values, args = value['source']
            output[key] = Function(
                name=function_name,
                values=[_source_prefix + v for v in values],
                args=args
            )

        elif value['type'] == 'tuple':
            output[key] = Tuple(path=value['source'])

        else:
            output[key] = value['source']
            if isinstance(value['source'], string_types):
                output[key] = _source_prefix + value['source']

    return output


def apply_transformation(input_data, transformation):
    output = {}

    for key, value in transformation.items():
        if isinstance(value, list):
            output[key] = [apply_transformation(input_data, v) for v in value]

        elif isinstance(value, dict):
            output[key] = apply_transformation(input_data, value)
        else:
            if isinstance(value, Function):
                output[key] = _handle_function(input_data, func=value)
            elif isinstance(value, Tuple):
                expr = parse(value.path)
                output[key] = [m.value for m in expr.find(input_data)]
            else:
                expr = parse(value)
                output_value = [m.value for m in expr.find(input_data)]
                output[key] = output_value[0] if output_value else ''

    return output


def transform(input_data, schema):
    transformation = generate_transformation(input_data, schema)
    return apply_transformation(input_data, transformation)
