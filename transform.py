from collections import namedtuple
from jsonpath_rw import parse
import inspect
import functions

Function = namedtuple('Function', ['name', 'values', 'args', ])


def _handle_function_value(input_data, func):
    function = getattr(functions, func.name, None)
    assert function is not None, (
        "{} is not an available function"
    ).format(func.name)

    _values = func.values
    values = []
    for value in _values:
        expr = parse(value)
        parsed_value = [m.value for m in expr.find(input_data)][0]
        values.append(parsed_value)
    assert len(_values) == len(values), "Unable parse some values"

    args = values + func.args
    _required_no_args = inspect.getargspec(function).args
    assert len(_required_no_args) == len(args), (
        "Number of arguments mismatched. {} != {}".format(
            len(_required_no_args), len(args)
        )
    )
    return function(*args)


def _handle_string_value(value):
    result = value
    if value.startswith('='):
        result = value[1:]
    elif '.=' in value:
        result = value.split('.=')[-1]
    return result


def generate_transformation(schema, source_prefix=''):
    output = {}

    for key, value in schema['properties'].items():
        _source_prefix = source_prefix + '.' if source_prefix else ''

        if value['type'] == 'array':
            output[key] = [generate_transformation(
                schema=value['items'],
                source_prefix=_source_prefix + value['source']
            )]
        elif value['type'] == 'object':
            output[key] = generate_transformation(
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
        else:
            output[key] = value['source']
            if isinstance(value['source'], basestring):
                output[key] = _source_prefix + value['source']

    return output


def transformer(input_data, transformation):
    output = {}

    for key, value in transformation.items():
        if isinstance(value, list):
            output[key] = [transformer(input_data, value[0])]
        elif isinstance(value, dict):
            output[key] = transformer(input_data, value)
        else:
            if isinstance(value, Function):
                output[key] = _handle_function_value(input_data, func=value)
            elif value.startswith('=') or '.=' in value:
                output[key] = _handle_string_value(value)
            else:
                expr = parse(value)
                output[key] = [m.value for m in expr.find(input_data)][0]

    return output
