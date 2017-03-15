# -*- coding: utf-8 -*-
from book_extractors.common.base_extractor import BaseExtractor
from book_extractors.common.extraction_keys import KEYS
import shared.regexUtils as regexUtils
import re


class BoolExtractor(BaseExtractor):
    def __init__(self, key_of_cursor_location_dependent, options):
        super(BoolExtractor, self).__init__(key_of_cursor_location_dependent, options)
        self.patterns_to_find = options['patterns']
        self.OPTIONS = (re.UNICODE | re.IGNORECASE)

    def extract(self, entry, extraction_results):
        start_position = self.get_starting_position(extraction_results)
        results = self._find_patterns(entry['text'])
        return self._constructReturnDict({KEYS["flags"]: results}, extraction_results, start_position)

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
