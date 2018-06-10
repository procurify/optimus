from jsonpath_rw import jsonpath, parse


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


def generate_schema(input_data):
	pass

def generate_transformation(schema, source_prefix=''):
	output = {}

	for key, value in schema['properties'].items():	
		if value['type'] == 'array':
			output[key] = [generate_transformation(
				schema=value['items'],
				source_prefix=value['source']
			)]
		elif value['type'] == 'object':
			output[key] = generate_transformation(
				schema=value,
				source_prefix=value['source']
			)
		else:
			source = value['source']
			if source_prefix:
				source = source_prefix + '.' + source
			output[key] = source

	return output


def transformer(input_data, transformation):
	output = {}

	for key, value in transformation.items():
		if isinstance(value, list):
			output[key] = [transformer(input_data, value[0])]
		elif isinstance(value, dict):
			output[key] = transformer(input_data, value)
		else:
			expr = parse(value)
			output[key] = [m.value for m in expr.find(input_data)][0]

	return output
