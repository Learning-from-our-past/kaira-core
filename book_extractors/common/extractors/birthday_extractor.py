# -*- coding: utf-8 -*-
import re

from book_extractors.common.extractors.base_extractor import BaseExtractor

from book_extractors.common.extraction_keys import KEYS
from book_extractors.common.extractors.date_extractor import DateExtractor
from book_extractors.extraction_exceptions import *
from book_extractors.extraction_pipeline import ExtractionPipeline, configure_extractor
from shared import regexUtils
from shared import text_utils


class CommonBirthdayExtractor(BaseExtractor):
    extraction_key = KEYS['birthData']

    def __init__(self, key_of_cursor_location_dependent, options):
        super(CommonBirthdayExtractor, self).__init__(key_of_cursor_location_dependent, options)
        self.PATTERN = options['PATTERN']
        self.OPTIONS = (re.UNICODE | re.IGNORECASE)
        self.REQUIRES_MATCH_POSITION = True
        self.SUBSTRING_WIDTH = 100

        if 'remove_spaces' in options:
            self._remove_spaces_from_text = options['remove_spaces']
        else:
            self._remove_spaces_from_text = True

        self._sub_extraction_pipeline = ExtractionPipeline([
            configure_extractor(DateExtractor, extractor_options={'PATTERN': self.PATTERN, 'OPTIONS': self.OPTIONS})
        ])

    def _extract(self, entry, extraction_results, extraction_metadata):
        start_position = self.get_starting_position(extraction_results, extraction_metadata)
        prepared_text = self._prepare_text_for_extraction(entry['text'], start_position)
        result = self._find_date(prepared_text, start_position)

        return self._add_to_extraction_results(result[0], extraction_results, extraction_metadata, result[1])

    def _prepare_text_for_extraction(self, text, start_position):
        t = text_utils.take_sub_str_based_on_pos(text, start_position, self.SUBSTRING_WIDTH)

        if self._remove_spaces_from_text:
            t = text_utils.remove_spaces_from_text(t)

        spouse_found = regexUtils.find_first_position_with_regex_search("puol", t, re.IGNORECASE | re.UNICODE)
        if spouse_found != -1:
            t = t[0:spouse_found]

        return t

    def _find_date(self, text, start_position):
        cursor_location = start_position

        try:
            result, metadata = self._sub_extraction_pipeline.process({'text': text})
            found_date = result['date']
            cursor_location = self.get_last_cursor_location(result, metadata) + start_position - 4
        except DateException:
            # TODO: Better idea to have in DateExtractor class maybe?
            found_date = {"day": None, "month": None, "year": None, "cursorLocation": 0}
            self.metadata_collector.add_error_record('birthDateNotFound', 2)

        # Map date to birthDate
        birth_date = {KEYS["birthDay"]: text_utils.int_or_none(found_date["day"]),
                      KEYS["birthMonth"]: text_utils.int_or_none(found_date["month"]),
                      KEYS["birthYear"]: text_utils.int_or_none(found_date["year"])}

        return birth_date, cursor_location
