# -*- coding: utf-8 -*-
import re

from book_extractors.common.extractors.base_extractor import BaseExtractor
from shared import regexUtils
from shared import textUtils


class DeathExtractor(BaseExtractor):
    extraction_key = 'death'

    def __init__(self, key_of_cursor_location_dependent, options):
        super(DeathExtractor, self).__init__(key_of_cursor_location_dependent, options)
        self.PATTERN = r"(?:kuoli)\.?\s?-(?P<year>\d{2,4})(?!\.|,|\d)(?=\D\D\D\D\D)"
        self.OPTIONS = (re.UNICODE | re.IGNORECASE)
        self.REQUIRES_MATCH_POSITION = True
        self.SUBSTRING_WIDTH = 100

    def _extract(self, entry, extraction_results):
        start_position = self.get_starting_position(extraction_results)
        prepared_text = self._prepare_text_for_extraction(entry['text'], start_position)
        result = self._find_date(prepared_text, start_position)

        return self._add_to_extraction_results(result[0], extraction_results, result[1])

    def _prepare_text_for_extraction(self, text, start_position):
        t = textUtils.take_sub_str_based_on_pos(text, start_position, self.SUBSTRING_WIDTH)
        t = textUtils.remove_spaces_from_text(t)
        return t

    def _find_date(self, text, start_position):
        cursor_location = start_position
        try:
            death = regexUtils.safe_search(self.PATTERN, text, self.OPTIONS)

            # Dirty fix for inaccuracy in positions which would screw the Location extraction
            cursor_location = death.end() + start_position - 4
            death_year = textUtils.int_or_none("19" + death.group("year"))
        except regexUtils.RegexNoneMatchException as e:
            death_year = None

        return death_year, cursor_location
