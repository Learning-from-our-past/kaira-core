# -*- coding: utf-8 -*-
from books.greatfarmers.extraction.extractors.baseExtractor import BaseExtractor
from books.greatfarmers.extractionkeys import KEYS
from interface.valuewrapper import ValueWrapper
import shared.textUtils as textUtils
import shared.regexUtils as regexUtils
import re

class BoolExtractor(BaseExtractor):

    def __init__(self, currentChild, errorLogger, xmlDocument):
        super(BoolExtractor, self).__init__(currentChild, errorLogger, xmlDocument)
        self.patterns_to_find = {}
        self.results = {}


    def extract(self, text, entry):
        self.OPTIONS = (re.UNICODE | re.IGNORECASE)

        self._find_patterns(text)
        return self._constructReturnDict()

    def set_patterns_to_find(self, patterns):
        """
        :param patterns: Take a dict of key : pattern values to extract.
        """
        self.patterns_to_find = patterns

    def _find_patterns(self, text):

        for key, pattern in self.patterns_to_find.items():
            try:
                found = regexUtils.safeSearch(pattern, text, self.OPTIONS)
                self.results[key] = ValueWrapper(True)
            except regexUtils.RegexNoneMatchException as e:
                self.results[key] = ValueWrapper(False)
                pass

    def _constructReturnDict(self):
        return {KEYS["flags"] : ValueWrapper(self.results)}
