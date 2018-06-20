import arrow
import pycountry

__all__ = ['string_literal', 'default_value', 'format_date',
           'boolean', 'alpha_2_country']


def string_literal(value):
    return value


def default_value(value, alternate_value):
    return value if value else alternate_value


def format_date(value, format):
    date_value = arrow.get(value)
    return date_value.format(format)


def boolean(value, true_repr, false_repr):
    return true_repr if value else false_repr


def alpha_2_country(value):
    try:
        return pycountry.countries.lookup(value).alpha_2
    except LookupError:
        # country_name is empty string, None, or no match found
        return ''
