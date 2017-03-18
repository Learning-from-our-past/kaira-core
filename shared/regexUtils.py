# -*- coding: utf-8 -*-
import re
import regex


def find_first_position_with_regex_search(pattern, text, options=re.UNICODE):
    pos = -1
    r = re.compile(pattern, options)
    m = r.search(text)
    if m is not None:
        pos = m.start()
    return pos


def regex_iter(pattern, text, options = re.UNICODE):
    r = re.compile(pattern, options)
    m = r.finditer(text)
    return m


def regex_all(pattern, text, options = re.UNICODE):
    r = re.compile(pattern, options)
    m = r.findall(text)
    return m


def safe_search(pattern, text, options = re.UNICODE):
    r = regex.compile(pattern, options)
    m = r.search(text)
    if m is None:
        raise RegexNoneMatchException(text)
    return m


def search(pattern, text, options = re.UNICODE):
    r = regex.compile(pattern, options)
    m = r.search(text)
    return m


def safe_match(pattern, text, options = re.UNICODE):
    r = regex.compile(pattern, options)
    m = r.match(text)
    if m is None:
        raise RegexNoneMatchException(text)
    return m


def match_exists(pattern, text, options = re.UNICODE):
    r = regex.compile(pattern, options)
    m = r.search(text)
    if m is None:
        return False
    else:
        return True


class RegexNoneMatchException(Exception):
    message = u"No matches found: "

    def __init__(self, details):
        self.message += details

    def __unicode__(self):
        return self.message
