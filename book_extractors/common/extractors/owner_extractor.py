# -*- coding: utf-8 -*-
import re

import shared.regexUtils as regexUtils
import shared.textUtils as textUtils
from book_extractors.common.extraction_keys import KEYS
from book_extractors.common.extractors.base_extractor import BaseExtractor
from book_extractors.extraction_pipeline import ExtractionPipeline, configure_extractor
from shared.genderExtract import Gender, GenderException


class CommonOwnerExtractor(BaseExtractor):
    extraction_key = 'owner'

    def __init__(self, key_of_cursor_location_dependent, options):
        super(CommonOwnerExtractor, self).__init__(key_of_cursor_location_dependent, options)
        self.SEARCH_SPACE = 200
        self.OWNER_YEAR_PATTERN = options['OWNER_YEAR_PATTERN']
        self.OWNER_NAME_PATTERN = options['OWNER_NAME_PATTERN']
        self.OWNER_OPTIONS = (re.UNICODE | re.IGNORECASE)

        self._sub_extraction_pipeline = ExtractionPipeline([
            configure_extractor(options['BIRTHDAY_EXTRACTOR'])
        ])

    def extract(self, entry, extraction_results):
        start_position = self.get_starting_position(extraction_results)
        result = self._find_owner(entry['text'], start_position)
        return self._constructReturnDict(result[0], extraction_results, result[1])

    def _find_owner(self, text, start_position):
        text = textUtils.takeSubStrBasedOnRange(text, start_position, self.SEARCH_SPACE)
        owner_year_result = self._find_owner_year(text, start_position)
        owner_name_details_result = self._find_owner_name_details(text, start_position)
        owner_birthday_result = self._find_owner_birthday(text)

        cursor_location = max(owner_year_result[1], owner_name_details_result[1], self.get_last_cursor_location(owner_birthday_result))
        result = {
            KEYS["ownerFrom"]: owner_year_result[0],
            KEYS["firstnames"]: owner_name_details_result[0][0],
            KEYS["surname"]: owner_name_details_result[0][1],
            KEYS["gender"]: owner_name_details_result[0][2],
            KEYS["ownerBirthData"]: owner_birthday_result['birthday']['results']
        }

        return result, cursor_location

    def _find_owner_year(self, text, start_position):
        cursor_location = start_position
        owner_year = None
        try:
            owner_year = regexUtils.safeSearch(self.OWNER_YEAR_PATTERN, text, self.OWNER_OPTIONS)
            cursor_location = start_position + owner_year.end()
            owner_year = textUtils.int_or_none(owner_year.group("year"))
        except regexUtils.RegexNoneMatchException:
            self.metadata_collector.add_error_record('ownerYearNotFound', 2)

        return owner_year, cursor_location

    def _find_owner_name_details(self, text, start_position):
        cursor_location = start_position
        owner_name_data = ('', '', '')
        try:
            owner_name_match = regexUtils.safeSearch(self.OWNER_NAME_PATTERN, text, self.OWNER_OPTIONS)
            cursor_location = start_position + owner_name_match.end()
            owner_name_data = self._split_names(owner_name_match.group("name"))
        except regexUtils.RegexNoneMatchException:
            self.metadata_collector.add_error_record('ownerNameNotFound', 7)

        return owner_name_data, cursor_location

    def _find_owner_birthday(self, text):
        results = self._sub_extraction_pipeline.process({'text': text})
        return results

    @staticmethod
    def _find_owner_gender(names):
        owner_gender = ''
        for n in names:
            try:
                if len(n) > 2:
                    owner_gender = Gender.find_gender(n)
                    break
            except GenderException:
                pass

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
            owner_gender = self._find_owner_gender(names)

        return first_names, surname, owner_gender
