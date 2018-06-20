import json

import pytest

fixtures_path = 'tests/fixture_files'


@pytest.fixture
def purchase_order_data():
    fixture_file = fixtures_path + '/purchase_order.json'
    with open(fixture_file, 'r') as f:
        return json.loads(f.read())


@pytest.fixture
def purchase_order_schema():
    fixture_file = fixtures_path + '/purchase_order.schema'
    with open(fixture_file, 'r') as f:
        return json.loads(f.read())


@pytest.fixture
def vendor_data():
    fixture_file = fixtures_path + '/vendor.json'
    with open(fixture_file, 'r') as f:
        return json.loads(f.read())


@pytest.fixture
def vendor_schema():
    fixture_file = fixtures_path + '/vendor.schema'
    with open(fixture_file, 'r') as f:
        return json.loads(f.read())
