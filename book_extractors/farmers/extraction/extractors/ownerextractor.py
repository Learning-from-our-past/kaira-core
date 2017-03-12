# -*- coding: utf-8 -*-
from book_extractors.common.base_extractor import BaseExtractor
from book_extractors.common.extraction_keys import KEYS
from book_extractors.extraction_pipeline import ExtractionPipeline, configure_extractor
from book_extractors.farmers.extraction.extractors.birthdayExtractor import BirthdayExtractor
import shared.textUtils as textUtils
import shared.regexUtils as regexUtils
from shared.genderExtract import Gender, GenderException
import re


class OwnerExtractor(BaseExtractor):

    def __init__(self, options):
        super(OwnerExtractor, self).__init__(options)
        self.SEARCH_SPACE = 200
        self.OWNER_YEAR_PATTERN = r"om(?:\.|,)\s?vuodesta\s(?P<year>\d\d\d\d)"
        self.OWNER_NAME_PATTERN = r"(?P<name>[A-ZÄ-Öa-zä-ö -]+(?:o\.s\.)?[A-ZÄ-Öa-zä-ö -]+)(?:\.|,)\ssynt"
        self.OWNER_OPTIONS = (re.UNICODE | re.IGNORECASE)

    def extract(self, entry, start_position=0):
        result = self._find_owner(entry['text'], start_position)
        return self._constructReturnDict({KEYS['owner']: result[0]}, result[1])

    def _find_owner(self, text, start_position):
        text = textUtils.takeSubStrBasedOnRange(text, start_position, self.SEARCH_SPACE)
        owner_year_result = self._find_owner_year(text, start_position)
        owner_name_details_result = self._find_owner_name_details(text, start_position)
        owner_birthday_result = self._find_owner_birthday(text)

        cursor_location = max(owner_year_result[1], owner_name_details_result[1], owner_birthday_result['cursorLocation'])
        result = {
            KEYS["ownerFrom"]: owner_year_result[0],
            KEYS["firstnames"]: owner_name_details_result[0][0],
            KEYS["surname"]: owner_name_details_result[0][1],
            KEYS["gender"]: owner_name_details_result[0][2],
            KEYS["ownerBirthData"]: owner_birthday_result
        }

        return result, cursor_location

    @staticmethod
    def _find_owner_birthday(text):
        _sub_extraction_pipeline = ExtractionPipeline([
            configure_extractor(BirthdayExtractor)
        ])

        results = _sub_extraction_pipeline.process({'text': text})
        return results

    def _find_owner_name_details(self, text, start_position):
        cursor_location = start_position
        owner_name_data = ('', '', '')
        try:
            owner_name_match = regexUtils.safeSearch(self.OWNER_NAME_PATTERN, text, self.OWNER_OPTIONS)
            cursor_location = start_position + owner_name_match.end()
            owner_name_data = self._split_names(owner_name_match.group("name"))
        except regexUtils.RegexNoneMatchException as e:
            # TODO: Metadata logging here self.errorLogger.logError(OwnerNameException.eType, self.currentChild)
            pass

        return owner_name_data, cursor_location

    @staticmethod
    def _find_owner_gender(name):
        try:
            owner_gender = Gender.find_gender(name)
        except GenderException:
            # TODO: Metadata logging here self.errorLogger.logError(e.eType, self.currentChild)
            owner_gender = ""

        return owner_gender

    def _split_names(self, name):
        first_names = ''
        owner_gender = ''
        name = re.sub(r"(?:<|>|&|')", r"", name)
        names = re.split(" ", name)

        surname = names[len(names)-1].strip(" ")
        if len(names) > 1:
            for i in range(0, len(names)-1):
                if names[i].strip(" ") != "o.s.":
                    first_names += names[i].strip(" ") + " "
            first_names = first_names.strip(" ")
            owner_gender = self._find_owner_gender(names[1])

        return first_names, surname, owner_gender

    def _find_owner_year(self, text, start_position):
        cursor_location = start_position
        owner_year = None
        try:
            owner_year = regexUtils.safeSearch(self.OWNER_YEAR_PATTERN, text, self.OWNER_OPTIONS)
            cursor_location = start_position + owner_year.end()
            owner_year = int(owner_year.group("year"))
        except regexUtils.RegexNoneMatchException:
            pass  # TODO: Metadata logging here self.errorLogger.logError(OwnerYearException.eType, self.currentChild)

        return owner_year, cursor_location
