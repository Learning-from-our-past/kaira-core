# -*- coding: utf-8 -*-
import re
import regex


def findFirstPositionWithRegexSearch(pattern, text):
    pos = -1
    r = re.compile(pattern, re.UNICODE)
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
    m = r.search(unicode(text))
    if m is None:
        raise RegexNoneMatchException(text)
    return m



class RegexNoneMatchException(Exception):
    message = u"No matches found: "

    def __init__(self, details):
        self.message += unicode(details)

    def __unicode__(self):
        return self.message