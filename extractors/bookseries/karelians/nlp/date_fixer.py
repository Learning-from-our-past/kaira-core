import regex
from core.utils.text_utils import remove_spaces_from_text

"""
A utility designed to try and fix dates in the person entry strings found in the
"Siirtokarjalaisten tie" books.

The regex patterns below are different ways to try and find dates in the text that are in formats
that the Finnish dependency parser will not be able to properly understand. For it to be able
to understand dates properly, they should be in the following format: <day>.<month>.<year>.
The dates in the person entries are often in the format <day>.<month>.<shortened year>, where
<shortened year> is a dash and two digits. But very often the dates may be missing dots, or have
dots replaced with commas, or there may be liberal amounts of whitespace between the numbers.
These regex patterns can be added to freely.
"""


_REGEX_PATTERNS = [
    # numbers allowing one insertion, separated by dots that may be followed by any number of
    # whitespace
    r'\s?(?P<day>\d{1,2}){i<=1}\.\s*(?P<month>\d{1,2}){i<=1}\.\s*\-?(?P<year>\d{2,4}){i<=1}',
    # "syntyi" followed by a date where the numbers are separated by between one to six whitespace
    r'(?<=syntyi)\s(?P<day>\d{1,2})\s{1,6}(?P<month>\d{1,2})\s{1,6}-?(?P<year>\d{2,4})',
    # dates where the day is followed by a dot or a comma and one to six whitespace, but the
    # month and year are only separated by one to six whitespace
    r'\s(?P<day>\d{1,2})[.,]\s{1,6}(?P<month>\d{1,2})\s{1,6}-?(?P<year>\d{2,4})',
    # same as above but the dot or comma is between month and year instead
    r'\s(?P<day>\d{1,2})\s{1,6}(?P<month>\d{1,2})[.,]\s{1,6}-?(?P<year>\d{2,4})',
    # same as above two but there is a dot or comma separating both day and month and month and
    # year
    r'\s(?P<day>\d{1,2})[,.]\s{1,6}(?P<month>\d{1,2})[.,]\s{1,6}-?(?P<year>\d{2,4})'
]
_REGEX_FLAGS = (regex.UNICODE | regex.IGNORECASE)


def fix_dates(string):
    """
    Run date fixing.
    :param string: Text interleaved with dates (day-month-year)
    :return: Input string with dates fixed
    """
    text = string
    for pattern in _REGEX_PATTERNS:
        text = regex.sub(pattern, _create_date_string_from_regex_match,
                         text, flags=_REGEX_FLAGS)
    return text


def _create_date_string_from_regex_match(match_object):
    """
    Tries to create a string with date out of a regex match
    :param match_object: A regex match that should have the named groups 'day',
    'month' and 'year'
    :return: a string with the format ' <day>.<month>.<year>'
    """
    day = remove_spaces_from_text(match_object.group('day'))
    month = remove_spaces_from_text(match_object.group('month'))
    year = remove_spaces_from_text(match_object.group('year'))
    year = regex.sub(r'\D+', '', year)

    if int(year) < 70:
        year = '19{}'.format(year)
    elif int(year) < 1800:
        year = '18{}'.format(year)

    return ' {}.{}.{}'.format(day, month, year)
