import arrow

__all__ = ['string_literal', 'default_value', 'format_date']


def string_literal(value):
    return value


def default_value(value, alternate_value):
    return value if value else alternate_value


def format_date(value, format):
    date_value = arrow.get(value)
    return date_value.format(format)
