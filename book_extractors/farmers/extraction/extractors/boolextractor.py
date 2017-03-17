# -*- coding: utf-8 -*-
import re

import shared.regexUtils as regexUtils
from book_extractors.common.extraction_keys import KEYS
from book_extractors.common.extractors.base_extractor import BaseExtractor


class BoolExtractor(BaseExtractor):
    extraction_key = KEYS['flags']

    def __init__(self, key_of_cursor_location_dependent, options):
        super(BoolExtractor, self).__init__(key_of_cursor_location_dependent, options)
        self.patterns_to_find = options['patterns']
        self.OPTIONS = (re.UNICODE | re.IGNORECASE)

    def extract(self, entry, extraction_results):
        result = self._find_patterns(entry['text'])
        return self._constructReturnDict(result, extraction_results, 0)

    def _find_patterns(self, text):
        results = {}
        for key, pattern in self.patterns_to_find.items():
            try:
                regexUtils.safeSearch(pattern, text, self.OPTIONS)
                results[key] = True
            except regexUtils.RegexNoneMatchException:
                results[key] = False
                pass
        return results
