import arrow

__all__ = ['format_date']


def default_value(value, default_value):
    return value if value else default_value


def format_date(value, format):
    date_value = arrow.get(value)
    return date_value.format(format)


def string_literal(value):
    return value
