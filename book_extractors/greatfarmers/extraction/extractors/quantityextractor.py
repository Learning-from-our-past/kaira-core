# -*- coding: utf-8 -*-
from book_extractors.common.base_extractor import BaseExtractor
from book_extractors.common.extraction_keys import KEYS
import shared.regexUtils as regexUtils
import re

class QuantityExtractor(BaseExtractor):

    def __init__(self, entry, options):
        super(QuantityExtractor, self).__init__(entry)
        self.QUANTITY_PATTERN = r"(?:(?P<range>\d\d?\d?(?:-|—)\d\d?\d?)|(?P<number>\d\d?\d?)|(?P<word>yksi|yhtä|kahta|kaksi|kolme|neljä|viisi|kuusi|seitsemän|kahdeksan|yhdeksän|kymmenen))\s?"
        self.SPLIT_PATTERN1 = r"(?P<number>\d\d?)"
        self.patterns_to_find = options['patterns']
        self.results = {}
        self.OPTIONS = (re.UNICODE | re.IGNORECASE)
        self.NUMBER_MAP = {"yksi" : 1, "yhtä": 1, "kahta": 2, "kaksi" : 2, "kolme" : 3, "neljä" : 4, "viisi" : 5, "kuusi" : 6,
                           "seitsemän" : 7, "kahdeksan" : 8, "yhdeksän" : 9, "kymmenen" : 10}

    def extract(self, text, entry):
        self._find_patterns(text)
        return self._constructReturnDict()

    def _find_patterns(self, text):
        for key, pattern in self.patterns_to_find.items():
            try:
                usepattern = self.QUANTITY_PATTERN + pattern
                found = regexUtils.safeSearch(usepattern, text, self.OPTIONS)
                self.results[key] = self._process_value(found)
            except regexUtils.RegexNoneMatchException as e:
                try:
                    usepattern =  pattern + self.QUANTITY_PATTERN
                    found = regexUtils.safeSearch(usepattern, text, self.OPTIONS)
                    self.results[key] = self._process_value(found)
                except regexUtils.RegexNoneMatchException as e:
                    self.results[key] = ""

    def _process_value(self, match):
        if match.group("range") is not None:
             return self._take_average(match.group("range"))
        if match.group("number") is not None:
             return match.group("number")
        if match.group("word") is not None:
            try:
                return self.NUMBER_MAP[match.group("word").lower()]
            except KeyError:
                return ""

    def _take_average(self, range):
        numbers = regexUtils.regexIter(self.SPLIT_PATTERN1, range)
        numbers = list(numbers)
        sum = 0
        try:
            for m in numbers:
                sum += float(m.group("number"))

            if len(numbers) > 0:
                return float(sum/len(numbers))
            else:
                return ""
        except ValueError:
            return ""


    def _constructReturnDict(self):
        return {KEYS["quantities"] : self.results}
