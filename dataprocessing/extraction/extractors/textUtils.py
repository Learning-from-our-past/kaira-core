# -*- coding: utf-8 -*-
import re
import regex

def takeSubStrBasedOnMatchPos(text, start, width=None):
    if width is not None:
        t = text[start:(start+width)]
    else:
        t = text[start:]
    return t

def removeSpacesFromText(text):
    return text.replace(" ","")