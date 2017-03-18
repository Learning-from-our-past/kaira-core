# -*- coding: utf-8 -*-
import re

from book_extractors.common.extraction_keys import KEYS
from book_extractors.common.extractors.base_extractor import BaseExtractor
from book_extractors.extraction_pipeline import ExtractionPipeline, configure_extractor
from book_extractors.greatfarmers.extraction.extractors.birthday_extractor import BirthdayExtractor
from book_extractors.greatfarmers.extraction.extractors.original_family_extractor import OrigFamilyExtractor
from shared import regexUtils


class SpouseExtractor(BaseExtractor):
    extraction_key = KEYS["spouse"]

    def __init__(self, key_of_cursor_location_dependent, options):
        super(SpouseExtractor, self).__init__(key_of_cursor_location_dependent, options)
        self.PATTERN = r"vmo\.?(?P<spousedata>[A-ZÄ-Öa-zä-ö\s\.,\d-]*)(?=(Lapset|poika|tytär|asuinp|suvulla|tila))"
        self.NAMEPATTERN = r"(?P<name>^[\w\s-]*)"
        self.OPTIONS = (re.UNICODE | re.IGNORECASE)
        self.REQUIRES_MATCH_POSITION = False
        self.SUBSTRING_WIDTH = 100

        self._sub_extraction_pipeline = ExtractionPipeline([
            configure_extractor(OrigFamilyExtractor),
            configure_extractor(BirthdayExtractor)
        ])

    def extract(self, entry, extraction_results):
        start_position = self.get_starting_position(extraction_results)
        results = self._find_spouse(entry['text'], start_position)
        return self._add_to_extraction_results(results[0], extraction_results, cursor_location=results[1])

    def _find_spouse(self, text, start_position):
        cursor_location = start_position
        spouse_data = None

        try:
            found_spouse_match = regexUtils.safe_search(self.PATTERN, text, self.OPTIONS)
            spouse_data = self._find_spouse_data(found_spouse_match.group("spousedata"))

            # Dirty fix for inaccuracy in positions which would screw the Location extraction
            cursor_location = found_spouse_match.end() + start_position - 4
        except regexUtils.RegexNoneMatchException:
            pass

        return spouse_data, cursor_location

    def _find_spouse_data(self, text):
        try:
            name = regexUtils.safe_search(self.NAMEPATTERN, text, self.OPTIONS)
            spouse_name = name.group("name").strip()
            spouse_name = re.sub(r"\so$","", spouse_name)
            spouse_details = self._find_spouse_details(text[name.end() - 2:])

            # Map data to spouse object
            return {
                KEYS["spouseBirthData"]: {
                    **spouse_details['birthday']
                },
                KEYS["origfamily"]: spouse_details[KEYS['origfamily']]['results'],
                KEYS["spouseName"]: spouse_name,
            }

        except regexUtils.RegexNoneMatchException:
            self.metadata_collector.add_error_record('spouseNotFound', 7)

    def _find_spouse_details(self, text):
        return self._sub_extraction_pipeline.process({'text': text})