# -*- coding: utf-8 -*-
from book_extractors.greatfarmers.extraction.extractors.baseExtractor import BaseExtractor
from book_extractors.greatfarmers.extractionkeys import KEYS
import shared.regexUtils as regexUtils
import re

class BoolExtractor(BaseExtractor):
    def __init__(self, entry, errorLogger):
        super(BoolExtractor, self).__init__(entry, errorLogger)
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
                self.results[key] = True
            except regexUtils.RegexNoneMatchException as e:
                self.results[key] = False
                pass

    def _constructReturnDict(self):
        return {KEYS["flags"] : self.results}
