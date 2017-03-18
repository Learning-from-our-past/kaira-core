# -*- coding: utf-8 -*-
import re

from shared import regexUtils


def take_sub_str_based_on_pos(text, start, width=None):
    if width is not None:
        t = text[start:(start+width)]
    else:
        t = text[start:]
    return t


def take_sub_str_based_on_range(text, start, end):
    t = text[start:end]
    return t


def take_sub_str_based_on_first_regex_occurrence(text, pattern, options=re.UNICODE):
    pos = regexUtils.find_first_position_with_regex_search(pattern, text, options)
    if pos == -1:
        return text
    else:
        return text[0:pos]


def remove_spaces_from_text(text):
    text = text.replace("\n","")
    text = text.replace(" ","")
    return text.replace(" ","")


def int_or_none(value):
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def float_or_none(value):
    try:
        value = value.replace('\w', '')
        return float(value.replace(',', '.'))
    except (TypeError, ValueError, AttributeError):
        return None
