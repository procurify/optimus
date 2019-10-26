from optimus.utils import rreplace


def test_rreplace_string():
    input_string = "foo-bar-baz"
    output_string = rreplace(input_string, "-", "|", 1)

    assert output_string == "foo-bar|baz"


def test_rreplace_dict():
    input_data = {"fname": "foo-bar-baz", "lname": "bar-baz-foo"}

    output_data = rreplace(input_data, "-", ">", 2)
    assert output_data["fname"] == "foo>bar>baz"


def test_rreplace_list():
    input_data = ["a-b-c", "d-e-f", "g-h-i"]
    output_data = rreplace(input_data, "-", ">", 1)
    assert output_data == ["a-b>c", "d-e>f", "g-h>i"]
