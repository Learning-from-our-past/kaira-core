# -*- coding: utf-8 -*-
import re

import shared.regexUtils as regexUtils
from book_extractors.common.extraction_keys import KEYS
from book_extractors.common.extractors.base_extractor import BaseExtractor
from shared import textUtils

class QuantityExtractor(BaseExtractor):
    extraction_key = KEYS["quantities"]

    def __init__(self, key_of_cursor_location_dependent, options):
        super(QuantityExtractor, self).__init__(key_of_cursor_location_dependent, options)
        self.QUANTITY_PATTERN = r"(?:(?P<range>\d\d?\d?(?:-|—)\d\d?\d?)|(?P<number>\d\d?\d?)|(?P<word>yksi|yhtä|kahta|kaksi|kolme|neljä|viisi|kuusi|seitsemän|kahdeksan|yhdeksän|kymmenen))\s?"
        self.SPLIT_PATTERN1 = r"(?P<number>\d\d?)"
        self.patterns_to_find = options['patterns']
        self.OPTIONS = (re.UNICODE | re.IGNORECASE)
        self.NUMBER_MAP = {"yksi": 1, "yhtä": 1, "kahta": 2, "kaksi": 2, "kolme": 3, "neljä": 4, "viisi": 5, "kuusi": 6,
                           "seitsemän": 7, "kahdeksan": 8, "yhdeksän": 9, "kymmenen": 10}

    def extract(self, entry, extraction_results):
        start_position = self.get_starting_position(extraction_results)
        results = self._find_patterns(entry['text'])
        return self._constructReturnDict(results, extraction_results, start_position)

    def _find_patterns(self, text):
        results = {}
        for key, pattern in self.patterns_to_find.items():
            try:
                usepattern = self.QUANTITY_PATTERN + pattern
                found = regexUtils.safeSearch(usepattern, text, self.OPTIONS)
                results[key] = self._process_value(found)
            except regexUtils.RegexNoneMatchException:
                try:
                    usepattern = pattern + self.QUANTITY_PATTERN
                    found = regexUtils.safeSearch(usepattern, text, self.OPTIONS)
                    results[key] = self._process_value(found)
                except regexUtils.RegexNoneMatchException:
                    results[key] = None

        return results

    def _process_value(self, match):
        if match.group("range") is not None:
            return self._take_average(match.group("range"))
        if match.group("number") is not None:
            return textUtils.int_or_none(match.group("number"))
        if match.group("word") is not None:
            try:
                return self.NUMBER_MAP[match.group("word").lower()]
            except KeyError:
                return None

    def _take_average(self, txt_range):
        numbers = regexUtils.regexIter(self.SPLIT_PATTERN1, txt_range)
        numbers = list(numbers)
        num_sum = 0
        try:
            for m in numbers:
                num_sum += float(m.group("number"))

            if len(numbers) > 0:
                return float(num_sum/len(numbers))
            else:
                return None
        except ValueError:
            return None
