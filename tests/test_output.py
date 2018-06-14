from optimus.transformer import transform


def test_identical_transformation(purchase_order_data, purchase_order_schema):
    transformed_data = transform(
        purchase_order_data,
        purchase_order_schema
    )
    assert purchase_order_data == transformed_data


def test_field_removal(purchase_order_data, purchase_order_schema):
    pos = purchase_order_schema

    # Remove vendor field
    del (pos['properties']['vendor'])

    transformed_data = transform(
        purchase_order_data,
        purchase_order_schema
    )

    assert purchase_order_data != transformed_data
    assert 'vendor' not in transformed_data


def test_root_field_rename(purchase_order_data, purchase_order_schema):
    pos = purchase_order_schema

    # Rename date to po_date
    pos['properties']['po_date'] = pos['properties']['date']
    del (pos['properties']['date'])

    transformed_data = transform(
        purchase_order_data,
        purchase_order_schema
    )

    assert purchase_order_data != transformed_data
    assert 'po_date' in transformed_data
    assert transformed_data['po_date'] == purchase_order_data['date']


def test_root_field_to_root_field_mapping(
        purchase_order_data, purchase_order_schema):
    pos = purchase_order_schema

    # Map comment to currency
    pos['properties']['comment']['source'] = 'currency'

    transformed_data = transform(
        purchase_order_data,
        purchase_order_schema
    )

    assert transformed_data['comment'] == purchase_order_data['currency']


def test_root_field_to_nested_field_mapping(
        purchase_order_data, purchase_order_schema):
    pos = purchase_order_schema

    # Map comment to vendor name
    pos['properties']['comment']['source'] = 'vendor.name'

    transformed_data = transform(
        purchase_order_data,
        purchase_order_schema
    )

    assert transformed_data['comment'] == purchase_order_data['vendor']['name']
