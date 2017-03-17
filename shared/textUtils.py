# -*- coding: utf-8 -*-
import re

from shared import regexUtils


def takeSubStrBasedOnPos(text, start, width=None):
    if width is not None:
        t = text[start:(start+width)]
    else:
        t = text[start:]
    return t

def takeSubStrBasedOnRange(text, start, end):
    t = text[start:end]
    return t

def takeSubStrBasedOnFirstRegexOccurrence(text, pattern, options=re.UNICODE):
    pos = regexUtils.findFirstPositionWithRegexSearch(pattern, text, options)
    if pos == -1:
        return text
    else:
        return text[0:pos]


def removeSpacesFromText(text):
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
