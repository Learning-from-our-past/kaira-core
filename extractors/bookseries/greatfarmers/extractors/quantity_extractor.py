# -*- coding: utf-8 -*-
import re

import core.utils.regex_utils as regexUtils
from extractors.common.extraction_keys import KEYS
from core.pipeline_construction.base_extractor import BaseExtractor
from core.utils import text_utils


class QuantityExtractor(BaseExtractor):
    extraction_key = KEYS["quantities"]

    def __init__(self, cursor_location_depends_on=None, options=None):
        super(QuantityExtractor, self).__init__(cursor_location_depends_on, options)
        self.QUANTITY_PATTERN = r"(?:(?P<range>\d\d?\d?(?:-|—)\d\d?\d?)|(?P<number>\d\d?\d?)|(?P<word>yksi|yhtä|kahta|kaksi|kolme|neljä|viisi|kuusi|seitsemän|kahdeksan|yhdeksän|kymmenen))\s?"
        self.SPLIT_PATTERN1 = r"(?P<number>\d\d?)"
        self.patterns_to_find = options['patterns']
        self.OPTIONS = re.UNICODE | re.IGNORECASE
        self.NUMBER_MAP = {
            "yksi": 1,
            "yhtä": 1,
            "kahta": 2,
            "kaksi": 2,
            "kolme": 3,
            "neljä": 4,
            "viisi": 5,
            "kuusi": 6,
            "seitsemän": 7,
            "kahdeksan": 8,
            "yhdeksän": 9,
            "kymmenen": 10,
        }

    def _extract(self, entry, extraction_results, extraction_metadata):
        start_position = self.get_starting_position(extraction_metadata)
        results = self._find_patterns(entry['text'])
        return self._add_to_extraction_results(
            results, extraction_results, extraction_metadata, start_position
        )

    def _find_patterns(self, text):
        results = {}
        for key, pattern in self.patterns_to_find.items():
            try:
                usepattern = self.QUANTITY_PATTERN + pattern
                found = regexUtils.safe_search(usepattern, text, self.OPTIONS)
                results[key] = self._process_value(found)
            except regexUtils.RegexNoneMatchException:
                try:
                    usepattern = pattern + self.QUANTITY_PATTERN
                    found = regexUtils.safe_search(usepattern, text, self.OPTIONS)
                    results[key] = self._process_value(found)
                except regexUtils.RegexNoneMatchException:
                    results[key] = None

        return results

    def _process_value(self, match):
        if match.group("range") is not None:
            return self._take_average(match.group("range"))
        if match.group("number") is not None:
            return text_utils.int_or_none(match.group("number"))
        if match.group("word") is not None:
            try:
                return self.NUMBER_MAP[match.group("word").lower()]
            except KeyError:
                return None

    def _take_average(self, txt_range):
        numbers = regexUtils.regex_iter(self.SPLIT_PATTERN1, txt_range)
        numbers = list(numbers)
        num_sum = 0
        try:
            for m in numbers:
                num_sum += float(m.group("number"))

            if len(numbers) > 0:
                return float(num_sum / len(numbers))
            else:
                return None
        except ValueError:
            return None
