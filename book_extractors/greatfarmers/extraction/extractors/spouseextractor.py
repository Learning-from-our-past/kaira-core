# -*- coding: utf-8 -*-
import re
from book_extractors.common.base_extractor import BaseExtractor
from book_extractors.extraction_pipeline import ExtractionPipeline, configure_extractor
from book_extractors.common.extraction_keys import KEYS
from shared import regexUtils
from book_extractors.greatfarmers.extraction.extractors.birthdayExtractor import BirthdayExtractor
from book_extractors.greatfarmers.extraction.extractors.origfamilyextractor import OrigFamilyExtractor


class SpouseExtractor(BaseExtractor):

    def __init__(self, options):
        super(SpouseExtractor, self).__init__(options)
        self.PATTERN = r"vmo\.?(?P<spousedata>[A-ZÄ-Öa-zä-ö\s\.,\d-]*)(?=(Lapset|poika|tytär|asuinp|suvulla|tila))"
        self.NAMEPATTERN = r"(?P<name>^[\w\s-]*)"
        self.OPTIONS = (re.UNICODE | re.IGNORECASE)
        self.REQUIRES_MATCH_POSITION = False
        self.SUBSTRING_WIDTH = 100

    def extract(self, entry, start_position=0):
        results = self._find_spouse(entry['text'], start_position)
        return self._constructReturnDict({KEYS['spouse']: results[0]}, cursor_location=results[1])

    def _find_spouse(self, text, start_position):
        cursor_location = start_position
        spouse_data = None

        try:
            found_spouse_match = regexUtils.safeSearch(self.PATTERN, text, self.OPTIONS)
            spouse_data = self._find_spouse_data(found_spouse_match.group("spousedata"))

            # Dirty fix for inaccuracy in positions which would screw the Location extraction
            cursor_location = found_spouse_match.end() + start_position - 4
        except regexUtils.RegexNoneMatchException:
            pass

        return spouse_data, cursor_location

    def _find_spouse_data(self, text):
        try:
            name = regexUtils.safeSearch(self.NAMEPATTERN, text, self.OPTIONS)
            spouse_name = name.group("name").strip()
            spouse_name = re.sub(r"\so$","", spouse_name)
            spouse_details = self._find_spouse_details(text[name.end() - 2:])

            # Map data to spouse object
            return {
                KEYS["spouseBirthData"]: {
                    KEYS["birthDay"]: spouse_details[KEYS['birthDay']],
                    KEYS["birthYear"]: spouse_details[KEYS['birthYear']],
                    KEYS["birthMonth"]: spouse_details[KEYS['birthMonth']],
                },
                KEYS["origfamily"]: spouse_details[KEYS['origfamily']],
                KEYS["spouseName"]: spouse_name,
            }

        except regexUtils.RegexNoneMatchException:
            # TODO: Metadata logging here self.errorLogger.logError(SpouseNameException.eType, self.currentChild)
            pass

    def _find_spouse_details(self, text):
        _sub_extraction_pipeline = ExtractionPipeline([
            configure_extractor(OrigFamilyExtractor),
            configure_extractor(BirthdayExtractor)
        ])

        return _sub_extraction_pipeline.process({'text': text})
