# -*- coding: utf-8 -*-
import re

from book_extractors.common.base_extractor import BaseExtractor
from book_extractors.common.dateExtractor import DateExtractor
from book_extractors.common.extraction_keys import KEYS
from book_extractors.extraction_exceptions import *
from book_extractors.extraction_pipeline import ExtractionPipeline, configure_extractor
from shared import regexUtils
from shared import textUtils


class BirthdayExtractor(BaseExtractor):

    def __init__(self, options):
        super(BirthdayExtractor, self).__init__(options)
        self.PATTERN = r"(?:synt)\.?,?(?:(?:(?P<day>\d{1,2})(?:\.|,|:|s)(?P<month>\d{1,2})(?:\.|,|:|s)?-?(?P<year>\d{2,4}))|-(?P<yearOnly>\d{2,4})(?!\.|,|\d)(?=\D\D\D\D\D))"  # r'(?:synt)\.?,? ?(?:(?:(?P<day>\d{1,2})(?:\.|,|:|s)? ?(?P<month>\d{1,2})(?:\.|,|:|s)? ?-?(?P<year>\d{2,4})))'
        self.OPTIONS = (re.UNICODE | re.IGNORECASE)
        self.REQUIRES_MATCH_POSITION = True
        self.SUBSTRING_WIDTH = 100

    def extract(self, entry, start_position=0):
        prepared_text = self._prepare_text_for_extraction(entry['text'], start_position)
        result = self._find_date(prepared_text, start_position)

        return self._constructReturnDict(result[0], result[1])

    def _prepare_text_for_extraction(self, text, start_position):
        t = textUtils.takeSubStrBasedOnPos(text, start_position, self.SUBSTRING_WIDTH)
        t = textUtils.removeSpacesFromText(t)

        spouse_found = regexUtils.findFirstPositionWithRegexSearch("puol", t, re.IGNORECASE|re.UNICODE)
        if spouse_found != -1:
            t = t[0:spouse_found]

        return t

    def _find_date(self, text, start_position):
        cursor_location = start_position
        _sub_extraction_pipeline = ExtractionPipeline([
            configure_extractor(DateExtractor, extractor_options={'PATTERN': self.PATTERN, 'OPTIONS': self.OPTIONS})
        ])

        try:
            found_date = _sub_extraction_pipeline.process({'text': text})
            cursor_location = found_date['cursorLocation'] + start_position - 4
        except DateException:
            # TODO: Better idea to have in DateExtractor class maybe?
            # TODO: Metadata logging here self.errorLogger.logError(BirthdayException.eType, self.currentChild)
            found_date = {"day": "","month": "", "year": "", "cursorLocation": ""}

        # Map date to birthDate
        birth_date = {KEYS["birthDay"]: found_date["day"],
                      KEYS["birthMonth"]: found_date["month"],
                      KEYS["birthYear"]: found_date["year"]}

        return birth_date, cursor_location
