# -*- coding: utf-8 -*-
import re

from book_extractors.common.base_extractor import BaseExtractor
from shared import textUtils
from book_extractors.common.extraction_keys import KEYS
from shared import regexUtils


class WeddingExtractor(BaseExtractor):

    def __init__(self, options):
        super(WeddingExtractor, self).__init__(options)
        self.PATTERN = r"(?:avioit)\.?\s?-(?P<year>\d{2,4})"
        self.OPTIONS = (re.UNICODE | re.IGNORECASE)
        self.REQUIRES_MATCH_POSITION = True
        self.SUBSTRING_WIDTH = 100

    def extract(self, entry, start_position=0):
        prepared_text = self._prepare_text_for_extraction(entry['text'], start_position)

        results = self._find_date(prepared_text, start_position)
        return self._constructReturnDict({
            KEYS["weddingYear"]:  results[0]
        }, results[1])

    def _prepare_text_for_extraction(self, text, start_position):
        t = textUtils.takeSubStrBasedOnPos(text, start_position, self.SUBSTRING_WIDTH)
        t = textUtils.removeSpacesFromText(t)
        return t

    def _find_date(self, text, start_position):
        cursor_location = start_position
        try:
            wedding = regexUtils.safeSearch(self.PATTERN, text, self.OPTIONS)

            # Dirty fix for inaccuracy in positions which would screw the Location extraction
            cursor_location = wedding.end() + start_position - 4
            wedding_year = "19" + wedding.group("year")
        except regexUtils.RegexNoneMatchException:
            wedding_year = ""

        return wedding_year, cursor_location
