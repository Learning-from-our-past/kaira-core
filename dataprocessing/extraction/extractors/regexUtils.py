# -*- coding: utf-8 -*-
import re
import regex


def findFirstPositionWithRegexSearch(pattern, text, options=re.UNICODE):
    pos = -1
    r = re.compile(pattern, options)
    m = r.search(text)
    if m is not None:
        pos = m.start()
    return pos

def regexIter(pattern, text, options = re.UNICODE):
    r = re.compile(pattern, options)
    m = r.finditer(text)
    return m

def safeSearch(pattern, text, options = re.UNICODE):
    r = regex.compile(pattern, options)
    m = r.search(text)
    if m is None:
        raise RegexNoneMatchException(text)
    return m

def search(pattern, text, options = re.UNICODE):
    r = regex.compile(pattern, options)
    m = r.search(text)
    return m

def safeMatch(pattern, text, options = re.UNICODE):
    r = regex.compile(pattern, options)
    m = r.match(text)
    if m is None:
        raise RegexNoneMatchException(text)
    return m

def matchExists(pattern, text, options = re.UNICODE):
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