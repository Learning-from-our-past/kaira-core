# -*- coding: utf-8 -*-
import re

from core.base_extractor import BaseExtractor
from utils import regexUtils
from utils import text_utils


class DeathExtractor(BaseExtractor):
    extraction_key = 'death'

    def __init__(self, cursor_location_depends_on=None, options=None):
        super(DeathExtractor, self).__init__(cursor_location_depends_on, options)
        self.PATTERN = r"(?:kuoli)\.?\s?-(?P<year>\d{2,4})(?!\.|,|\d)(?=\D\D\D\D\D)"
        self.OPTIONS = (re.UNICODE | re.IGNORECASE)
        self.REQUIRES_MATCH_POSITION = True
        self.SUBSTRING_WIDTH = 100

    def _extract(self, entry, extraction_results, extraction_metadata):
        start_position = self.get_starting_position(extraction_metadata)
        prepared_text = self._prepare_text_for_extraction(entry['text'], start_position)
        result = self._find_date(prepared_text, start_position)

        return self._add_to_extraction_results(result[0], extraction_results, extraction_metadata, result[1])

    def _prepare_text_for_extraction(self, text, start_position):
        t = text_utils.take_sub_str_based_on_pos(text, start_position, self.SUBSTRING_WIDTH)
        t = text_utils.remove_spaces_from_text(t)
        return t

    def _find_date(self, text, start_position):
        cursor_location = start_position
        try:
            death = regexUtils.safe_search(self.PATTERN, text, self.OPTIONS)

            # Dirty fix for inaccuracy in positions which would screw the Location extraction
            cursor_location = death.end() + start_position - 4
            death_year = text_utils.int_or_none("19" + death.group("year"))
        except regexUtils.RegexNoneMatchException as e:
            death_year = None

        return death_year, cursor_location
