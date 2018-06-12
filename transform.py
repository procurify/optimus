from jsonpath_rw import parse

expected_output = {
    'id': 'id',
    'date': 'date',
    'test': {
        'bar': 'test.foo'
    },
    'items': [{
        'id': 'items[*].id',
        'name': 'items[*].name'
    }],
    'vendor': 'vendor.name'
}


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
        else:
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
            if value.startswith('='):
                output[key] = value[1:]
            elif '.=' in value:
                output[key] = value.split('.=')[-1]
            else:
                expr = parse(value)
                output[key] = [m.value for m in expr.find(input_data)][0]

    return output
