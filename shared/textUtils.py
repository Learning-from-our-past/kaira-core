# -*- coding: utf-8 -*-
import re

from shared import regexUtils

# This is a selection of unicode codes for characters that all look more or less like hyphens
_unicode_hyphens = [0x002D, 0x007E, 0x058A, 0x05BE, 0x1400, 0x1806,
                    0x2010, 0x2011, 0x2012, 0x2013, 0x2014, 0x2015,
                    0x2053, 0x207B, 0x208B, 0x2212, 0x2E17, 0x2E3A,
                    0x2E3B, 0x30A0, 0xFE32, 0xFE58, 0xFE63, 0xFF0D]
_hyphen_regex_pattern = '|'.join(map(chr, _unicode_hyphens))


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
    text = text.replace('\n', '')
    text = text.replace(' ', '')
    return text.replace(' ', '')


def remove_hyphens_from_text(text):
    text = re.sub(_hyphen_regex_pattern, '', text)
    return text


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
