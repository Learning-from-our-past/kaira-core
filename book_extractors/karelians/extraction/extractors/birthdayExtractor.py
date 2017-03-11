# -*- coding: utf-8 -*-
import re
from book_extractors.extraction_pipeline import ExtractionPipeline, configure_extractor
from book_extractors.common.base_extractor import BaseExtractor
from book_extractors.extraction_exceptions import *
from book_extractors.common.dateExtractor import DateExtractor
from shared import textUtils
from book_extractors.common.extraction_keys import KEYS
from shared import regexUtils


class BirthdayExtractor(BaseExtractor):

    def __init__(self, options):
        super(BirthdayExtractor, self).__init__(options)
        self.PATTERN = r"(?:synt)\.?,?(?:\s+)?(?:(?:(?P<day>\d{1,2})(?:\.|,|:|\s+|s)\s?(?P<month>\d{1,2})(?:\.|,|:|\s+|s)?(?:\s+)?-?(?P<year>\d{2,4}))|\s?-(?P<yearOnly>\d{2,4})(?!\.|,|\s|\d)(?=\D\D\D\D\D))"  # r'(?:synt)\.?,? ?(?:(?:(?P<day>\d{1,2})(?:\.|,|:|s)? ?(?P<month>\d{1,2})(?:\.|,|:|s)? ?-?(?P<year>\d{2,4})))'
        self.OPTIONS = (re.UNICODE | re.IGNORECASE)
        self.REQUIRES_MATCH_POSITION = True
        self.SUBSTRING_WIDTH = 100

    def extract(self, entry, start_position=0):
        self.matchStartPosition = start_position # TODO: Remove once this class is stateless

        prepared_text = self._prepare_text_for_extraction(entry['text'], start_position)
        result = self._find_date(prepared_text, start_position)

        return self._constructReturnDict({
            KEYS["birthDay"]:  result[0]["day"],
            KEYS["birthMonth"]: result[0]["month"],
            KEYS["birthYear"]:  result[0]["year"]
        }, result[1])

    def _prepare_text_for_extraction(self, text, start_position):
        t = textUtils.takeSubStrBasedOnPos(text, start_position, self.SUBSTRING_WIDTH)

        spouse_found = regexUtils.findFirstPositionWithRegexSearch("puol", t, re.IGNORECASE|re.UNICODE)
        if spouse_found != -1:
            t = t[0:spouse_found]

        return t

    def _find_date(self, text, start_position):
        cursor_location = start_position
        found_date = {"day": "", "month": "", "year": "", "cursorLocation": ""}

        _sub_extraction_pipeline = ExtractionPipeline([
            configure_extractor(DateExtractor, extractor_options={'PATTERN': self.PATTERN, 'OPTIONS': self.OPTIONS})
        ])

        try:
            found_date = _sub_extraction_pipeline.process({'text': text})
            cursor_location = found_date['cursorLocation'] + start_position - 4
        except DateException as e:
            #TODO: Metadata logging here
            pass

        return found_date, cursor_location
