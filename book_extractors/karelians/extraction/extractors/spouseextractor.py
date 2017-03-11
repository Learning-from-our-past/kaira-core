# -*- coding: utf-8 -*-
import re
from book_extractors.common.base_extractor import BaseExtractor
from book_extractors.common.extraction_keys import KEYS
from shared import regexUtils
from book_extractors.karelians.extraction.extractors.professionextractor import ProfessionExtractor
from book_extractors.karelians.extraction.extractors.birthdayExtractor import BirthdayExtractor
from book_extractors.karelians.extraction.extractors.locationExtractor import BirthdayLocationExtractor
from book_extractors.karelians.extraction.extractors.origfamilyextractor import OrigFamilyExtractor
from book_extractors.karelians.extraction.extractors.deathextractor import DeathExtractor
from book_extractors.karelians.extraction.extractors.weddingextractor import WeddingExtractor
from book_extractors.extraction_pipeline import ExtractionPipeline, configure_extractor


class SpouseExtractor(BaseExtractor):

    def __init__(self, options):
        super(SpouseExtractor, self).__init__(options)
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
                KEYS["birthLocation"]: ""
            },
            KEYS["deathYear"]: None,
            KEYS["origfamily"]: "",
            KEYS["profession"]: "",
            KEYS["weddingYear"]: None,
            KEYS["spouseName"]: "",
            KEYS["hasSpouse"]: False
        }

    def extract(self, entry, start_position=0):
        result = self._find_spouse(entry['text'], start_position)
        return self._constructReturnDict({KEYS['spouse']: result[0]}, cursor_location = result[1])

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
                    KEYS["birthDay"]: spouse_details[KEYS['birthDay']],
                    KEYS["birthYear"]: spouse_details[KEYS['birthYear']],
                    KEYS["birthMonth"]: spouse_details[KEYS['birthMonth']],
                    KEYS["birthLocation"]: spouse_details[KEYS['birthLocation']]
                },
                KEYS['spouseDeathYear']: spouse_details[KEYS['deathYear']],
                KEYS["origfamily"]: spouse_details[KEYS['origfamily']],
                KEYS["spouseProfession"]: spouse_details[KEYS['profession']],
                KEYS["weddingYear"]: spouse_details[KEYS['weddingYear']],
                KEYS["spouseName"]: spouse_name,
                KEYS["hasSpouse"]: True
            }

        except regexUtils.RegexNoneMatchException:
            # TODO: Metadata logging here self.errorLogger.logError(SpouseNameException.eType, self.currentChild)
            pass

        return spouse_name, spouse_details

    @staticmethod
    def _find_spouse_details(text):
        _sub_extraction_pipeline = ExtractionPipeline([
            configure_extractor(OrigFamilyExtractor),
            configure_extractor(ProfessionExtractor, depends_on_match_position_of_extractor=OrigFamilyExtractor),
            configure_extractor(BirthdayExtractor),
            configure_extractor(BirthdayLocationExtractor, depends_on_match_position_of_extractor=BirthdayExtractor),
            configure_extractor(DeathExtractor, depends_on_match_position_of_extractor=BirthdayLocationExtractor),
            configure_extractor(WeddingExtractor, depends_on_match_position_of_extractor=BirthdayLocationExtractor)
        ])

        return _sub_extraction_pipeline.process({'text': text})
