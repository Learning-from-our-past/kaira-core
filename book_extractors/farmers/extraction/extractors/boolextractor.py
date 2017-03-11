# -*- coding: utf-8 -*-
from book_extractors.common.base_extractor import BaseExtractor
from book_extractors.common.extraction_keys import KEYS
import shared.regexUtils as regexUtils
import re


class BoolExtractor(BaseExtractor):

    def __init__(self, options):
        super(BoolExtractor, self).__init__(options)
        self.patterns_to_find = options['patterns']
        self.results = {}

    def extract(self, entry, start_positions=0):
        self.OPTIONS = (re.UNICODE | re.IGNORECASE)

        self._find_patterns(entry['text'])
        return self._constructReturnDict()

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
