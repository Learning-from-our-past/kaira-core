# -*- coding: utf-8 -*-
import re

from book_extractors.common.extraction_keys import KEYS
from book_extractors.common.extractors.base_extractor import BaseExtractor
from book_extractors.extraction_pipeline import ExtractionPipeline, configure_extractor
from book_extractors.karelians.extraction.extractors.birthdayExtractor import BirthdayExtractor
from book_extractors.karelians.extraction.extractors.deathextractor import DeathExtractor
from book_extractors.karelians.extraction.extractors.locationExtractor import BirthdayLocationExtractor
from book_extractors.karelians.extraction.extractors.origfamilyextractor import OrigFamilyExtractor
from book_extractors.karelians.extraction.extractors.professionextractor import ProfessionExtractor
from book_extractors.karelians.extraction.extractors.weddingextractor import WeddingExtractor
from shared import regexUtils


class SpouseExtractor(BaseExtractor):
    extraction_key = 'spouse'

    def __init__(self, key_of_cursor_location_dependent, options):
        super(SpouseExtractor, self).__init__(key_of_cursor_location_dependent, options)

        self._sub_extraction_pipeline = ExtractionPipeline([
            configure_extractor(OrigFamilyExtractor),
            configure_extractor(ProfessionExtractor, depends_on_match_position_of_extractor=OrigFamilyExtractor),
            configure_extractor(BirthdayExtractor),
            configure_extractor(BirthdayLocationExtractor, depends_on_match_position_of_extractor=BirthdayExtractor),
            configure_extractor(DeathExtractor, depends_on_match_position_of_extractor=BirthdayLocationExtractor),
            configure_extractor(WeddingExtractor, depends_on_match_position_of_extractor=BirthdayLocationExtractor)
        ])

        self.PATTERN = r"Puol\.?,?(?P<spousedata>[A-ZÄ-Öa-zä-ö\s\.,\d-]*)(?=(Lapset|poika|tytär|asuinp))"
        self.NAMEPATTERN = r"(?P<name>^[\w\s-]*)"
        self.OPTIONS = (re.UNICODE | re.IGNORECASE)
        self.REQUIRES_MATCH_POSITION = False
        self.SUBSTRING_WIDTH = 100

        self.NO_SPOUSE_RESULT = {
            KEYS["spouseBirthData"]: {
                KEYS["birthDay"]: None,
                KEYS["birthYear"]: None,
                KEYS["birthMonth"]: None,
                KEYS["birthLocation"]: None
            },
            KEYS["deathYear"]: None,
            KEYS["origfamily"]: None,
            KEYS["profession"]: None,
            KEYS["weddingYear"]: None,
            KEYS["spouseName"]: None,
            KEYS["hasSpouse"]: False
        }

    def extract(self, entry, extraction_results):
        start_position = self.get_starting_position(extraction_results)
        result = self._find_spouse(entry['text'], start_position)
        return self._constructReturnDict(result[0], extraction_results, cursor_location=result[1])

    def _find_spouse(self, text, start_position):
        cursor_location = start_position
        spouse_data = self.NO_SPOUSE_RESULT

        try:
            found_spouse_match = regexUtils.safeSearch(self.PATTERN, text, self.OPTIONS)
            spouse_data = self._find_spouse_data(found_spouse_match.group("spousedata"))

            # Dirty fix for inaccuracy in positions which would screw the Location extraction
            cursor_location = found_spouse_match.end() + start_position - 4
        except regexUtils.RegexNoneMatchException:
            pass

        return spouse_data, cursor_location

    def _find_spouse_data(self, text):
        spouse_name = ''
        spouse_details = self.NO_SPOUSE_RESULT

        try:
            spouse_name_match = regexUtils.safeSearch(self.NAMEPATTERN, text, self.OPTIONS)
            spouse_name = spouse_name_match.group("name").strip()
            spouse_name = re.sub(r"\so$", "", spouse_name)
            spouse_details = self._find_spouse_details(text[spouse_name_match.end() - 2:])

            # Map data to spouse object
            return {
                KEYS["spouseBirthData"]: {
                    **spouse_details['birthday']
                },
                KEYS['spouseDeathYear']: spouse_details['death'],
                KEYS["origfamily"]: spouse_details['originalFamily'],
                KEYS["spouseProfession"]: spouse_details['profession'],
                KEYS["weddingYear"]: spouse_details['wedding'],
                KEYS["spouseName"]: spouse_name,
                KEYS["hasSpouse"]: True
            }

        except regexUtils.RegexNoneMatchException:
            self.metadata_collector.add_error_record('spouseNotFound', 6)

        return spouse_name, spouse_details

    def _find_spouse_details(self, text):
        return self._sub_extraction_pipeline.process({'text': text})
