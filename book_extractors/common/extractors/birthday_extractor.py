# -*- coding: utf-8 -*-
import re

from book_extractors.common.extractors.base_extractor import BaseExtractor

from book_extractors.common.extraction_keys import KEYS
from book_extractors.common.extractors.dateExtractor import DateExtractor
from book_extractors.extraction_exceptions import *
from book_extractors.extraction_pipeline import ExtractionPipeline, configure_extractor
from shared import regexUtils
from shared import textUtils


class CommonBirthdayExtractor(BaseExtractor):

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

    def extract(self, entry, extraction_results):
        start_position = self.get_starting_position(extraction_results)
        prepared_text = self._prepare_text_for_extraction(entry['text'], start_position)
        result = self._find_date(prepared_text, start_position)

        return self._constructReturnDict(result[0], extraction_results, result[1])

    def _prepare_text_for_extraction(self, text, start_position):
        t = textUtils.takeSubStrBasedOnPos(text, start_position, self.SUBSTRING_WIDTH)

        if self._remove_spaces_from_text:
            t = textUtils.removeSpacesFromText(t)

        spouse_found = regexUtils.findFirstPositionWithRegexSearch("puol", t, re.IGNORECASE|re.UNICODE)
        if spouse_found != -1:
            t = t[0:spouse_found]

        return t

    def _find_date(self, text, start_position):
        cursor_location = start_position

        try:
            result = self._sub_extraction_pipeline.process({'text': text})
            found_date = result['data']
            cursor_location = self.get_last_cursor_location(result) + start_position - 4
        except DateException:
            # TODO: Better idea to have in DateExtractor class maybe?
            # TODO: Metadata logging here self.errorLogger.logError(BirthdayException.eType, self.currentChild)
            found_date = {"day": "","month": "", "year": "", "cursorLocation": ""}

        # Map date to birthDate
        birth_date = {KEYS["birthDay"]: found_date["day"],
                      KEYS["birthMonth"]: found_date["month"],
                      KEYS["birthYear"]: found_date["year"]}

        return birth_date, cursor_location
