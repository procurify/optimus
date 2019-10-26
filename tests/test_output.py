from optimus.transformer import transform


def test_identical_transformation(purchase_order_data, purchase_order_schema):
    transformed_data = transform(purchase_order_data, purchase_order_schema)
    assert purchase_order_data == transformed_data


def test_field_removal(purchase_order_data, purchase_order_schema):
    pos = purchase_order_schema

    # Remove vendor field
    del pos["properties"]["vendor"]

    transformed_data = transform(purchase_order_data, purchase_order_schema)

    assert purchase_order_data != transformed_data
    assert "vendor" not in transformed_data


def test_root_field_rename(purchase_order_data, purchase_order_schema):
    pos = purchase_order_schema

    # Rename date to po_date
    pos["properties"]["po_date"] = pos["properties"]["date"]
    del pos["properties"]["date"]

    transformed_data = transform(purchase_order_data, purchase_order_schema)

    assert purchase_order_data != transformed_data
    assert "po_date" in transformed_data
    assert transformed_data["po_date"] == purchase_order_data["date"]


def test_root_field_to_root_field_mapping(purchase_order_data, purchase_order_schema):
    pos = purchase_order_schema

    # Map comment to currency
    pos["properties"]["comment"]["source"] = "currency"

    transformed_data = transform(purchase_order_data, purchase_order_schema)

    assert transformed_data["comment"] == purchase_order_data["currency"]


def test_root_field_to_nested_field_mapping(purchase_order_data, purchase_order_schema):
    pos = purchase_order_schema

    # Map comment to vendor name
    pos["properties"]["comment"]["source"] = "vendor.name"

    transformed_data = transform(purchase_order_data, purchase_order_schema)

    assert transformed_data["comment"] == purchase_order_data["vendor"]["name"]


def test_missing_field_in_source_data(purchase_order_data, purchase_order_schema):
    for item in purchase_order_data["items"]:
        del item["custom_fields"]["cost-center"]

    transformed_data = transform(purchase_order_data, purchase_order_schema)

    for item in transformed_data["items"]:
        assert item["custom_fields"]["cost-center"] == ""


def test_wrap_fields_in_an_object(purchase_order_data, purchase_order_schema):
    vendor_properties = purchase_order_schema["properties"]["vendor"]["properties"]
    vendor_properties["phones"] = {
        "type": "object",
        "source": "`this`",
        "properties": {
            "phoneOne": {"type": "string", "source": "phoneOne"},
            "phoneTwo": {"type": "string", "source": "phoneTwo"},
        },
    }

    transformed_data = transform(purchase_order_data, purchase_order_schema)
    vendor = transformed_data["vendor"]
    source_vendor = purchase_order_data["vendor"]
    assert vendor["phones"]["phoneOne"] == source_vendor["phoneOne"]
    assert vendor["phones"]["phoneTwo"] == source_vendor["phoneTwo"]
