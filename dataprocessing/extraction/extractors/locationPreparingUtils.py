# -*- coding: utf-8 -*-
import re
import regex
from  extraction.extractors.baseExtractor import BaseExtractor
import extraction.extractors.regexUtils as regexUtils
import extraction.extractors.textUtils as textUtils
from extraction.extractionExceptions import *

# This file provides simple functions to prepare location strings before passing them to
# the LocationExtractor class.
# TODO: Refactor into proper "proxy class" for locations.


def prepareBirthPlaceStringForExtraction(text, startPos, substringWidth):
    """Take substring for extracting man's location"""
    t = textUtils.takeSubStrBasedOnPos(text, startPos, substringWidth)
    #snip the string further if there is "Pso" to avoid extracting wife name instead of location name:
    t = textUtils.takeSubStrBasedOnFirstRegexOccurrence(t, r"Pso", re.IGNORECASE|re.UNICODE)
    return t