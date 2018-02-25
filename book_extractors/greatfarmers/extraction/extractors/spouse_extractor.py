# -*- coding: utf-8 -*-
import re

from book_extractors.common.extraction_keys import KEYS
from book_extractors.common.extractors.base_extractor import BaseExtractor
from shared import regexUtils
from book_extractors.common.extractors.kaira_id_extractor import KairaIdProvider


class SpouseExtractor(BaseExtractor):
    extraction_key = KEYS["spouse"]

    def __init__(self, cursor_location_depends_on=None, options=None):
        super(SpouseExtractor, self).__init__(cursor_location_depends_on, options)
        self.PATTERN = r"vmo\.?(?P<spousedata>[A-ZÄ-Öa-zä-ö\s\.,\d-]*)(?=(Lapset|poika|tytär|asuinp|suvulla|tila))"
        self.NAMEPATTERN = r"(?P<name>^[\w\s-]*)"
        self.OPTIONS = (re.UNICODE | re.IGNORECASE)
        self.REQUIRES_MATCH_POSITION = False
        self.SUBSTRING_WIDTH = 100

        self.kaira_id_provider = KairaIdProvider()

    def _extract(self, entry, extraction_results, extraction_metadata):
        start_position = self.get_starting_position(extraction_metadata)
        results = self._find_spouse(entry['text'], start_position)
        return self._add_to_extraction_results(results[0], extraction_results, extraction_metadata, cursor_location=results[1])

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
            spouse_details, metadata = self._find_spouse_details(text[name.end() - 2:])

            # Map data to spouse object
            return {
                KEYS["spouseBirthData"]: {
                    **spouse_details['birthday']
                },
                KEYS["formerSurname"]: spouse_details[KEYS['formerSurname']],
                KEYS["spouseName"]: spouse_name,
                KEYS["kairaId"]: self.kaira_id_provider.get_new_id('S')
            }

        except regexUtils.RegexNoneMatchException:
            self.metadata_collector.add_error_record('spouseNotFound', 7)

    def _find_spouse_details(self, text):
        return self._sub_extraction_pipeline.process({'text': text})
