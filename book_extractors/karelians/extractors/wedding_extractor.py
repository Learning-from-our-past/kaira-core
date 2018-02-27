# -*- coding: utf-8 -*-
import re

from core.pipeline_construction.base_extractor import BaseExtractor
from core.utils import regex_utils, text_utils


class WeddingExtractor(BaseExtractor):
    extraction_key = 'wedding'

    def __init__(self, cursor_location_depends_on=None, options=None):
        super(WeddingExtractor, self).__init__(cursor_location_depends_on, options)
        self.PATTERN = r'(?:avioit){s<=1}(?:[,.\s\-*:!;]?\s?-)?(?P<year>\d{2,4})'
        self.OPTIONS = (re.UNICODE | re.IGNORECASE)
        self.REQUIRES_MATCH_POSITION = True
        self.SUBSTRING_WIDTH = 100

    def _extract(self, entry, extraction_results, extraction_metadata):
        start_position = self.get_starting_position(extraction_metadata)
        prepared_text = self._prepare_text_for_extraction(entry['text'], start_position)

        results = self._find_date(prepared_text, start_position)
        return self._add_to_extraction_results(results[0], extraction_results, extraction_metadata, results[1])

    def _prepare_text_for_extraction(self, text, start_position):
        t = text_utils.take_sub_str_based_on_pos(text, start_position, self.SUBSTRING_WIDTH)
        t = text_utils.remove_spaces_from_text(t)
        return t

    def _find_date(self, text, start_position):
        cursor_location = start_position
        try:
            wedding = regex_utils.safe_search(self.PATTERN, text, self.OPTIONS)

            # Dirty fix for inaccuracy in positions which would screw the Location extraction
            cursor_location = wedding.end() + start_position - 4
            wedding_year = text_utils.int_or_none("19" + wedding.group("year"))
        except regex_utils.RegexNoneMatchException:
            wedding_year = None

        return wedding_year, cursor_location
