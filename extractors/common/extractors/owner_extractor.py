# -*- coding: utf-8 -*-
import re

import core.utils.regex_utils as regexUtils
from core.utils import text_utils
from extractors.common.extraction_keys import KEYS
from core.pipeline_construction.base_extractor import BaseExtractor
from core.utils.sex_extract import Sex, SexException


class CommonOwnerExtractor(BaseExtractor):
    extraction_key = 'owner'

    def __init__(self, cursor_location_depends_on=None, options=None):
        super(CommonOwnerExtractor, self).__init__(cursor_location_depends_on, options)
        self.SEARCH_SPACE = 200
        self.OWNER_YEAR_PATTERN = options['OWNER_YEAR_PATTERN']
        self.OWNER_NAME_PATTERN = options['OWNER_NAME_PATTERN']
        self.OWNER_OPTIONS = (re.UNICODE | re.IGNORECASE)

    def _extract(self, entry, extraction_results, extraction_metadata):
        start_position = self.get_starting_position(extraction_metadata)
        result = self._find_owner(entry['text'], start_position)
        return self._add_to_extraction_results(result[0], extraction_results, extraction_metadata, result[1])

    def _find_owner(self, text, start_position):
        text = text_utils.take_sub_str_based_on_range(text, start_position, self.SEARCH_SPACE)
        owner_year_result = self._find_owner_year(text, start_position)
        owner_name_details_result = self._find_owner_name_details(text, start_position)
        owner_birthday_result, metadata = self._find_owner_birthday(text)

        cursor_location = max(owner_year_result[1], owner_name_details_result[1],
                              self.get_last_cursor_location(metadata))
        result = {
            KEYS["ownerFrom"]: owner_year_result[0],
            KEYS["firstnames"]: owner_name_details_result[0][0],
            KEYS["surname"]: owner_name_details_result[0][1],
            KEYS["gender"]: owner_name_details_result[0][2],
            KEYS["ownerBirthData"]: owner_birthday_result['birthday']
        }

        return result, cursor_location

    def _find_owner_year(self, text, start_position):
        cursor_location = start_position
        owner_year = None
        try:
            owner_year = regexUtils.safe_search(self.OWNER_YEAR_PATTERN, text, self.OWNER_OPTIONS)
            cursor_location = start_position + owner_year.end()
            owner_year = text_utils.int_or_none(owner_year.group("year"))
        except regexUtils.RegexNoneMatchException:
            self.metadata_collector.add_error_record('ownerYearNotFound', 2)

        return owner_year, cursor_location

    def _find_owner_name_details(self, text, start_position):
        cursor_location = start_position
        owner_name_data = ('', '', '')
        try:
            owner_name_match = regexUtils.safe_search(self.OWNER_NAME_PATTERN, text, self.OWNER_OPTIONS)
            cursor_location = start_position + owner_name_match.end()
            owner_name_data = self._split_names(owner_name_match.group("name"))
        except regexUtils.RegexNoneMatchException:
            self.metadata_collector.add_error_record('ownerNameNotFound', 7)

        return owner_name_data, cursor_location

    def _find_owner_birthday(self, text):
        return self._sub_extraction_pipeline.process({'text': text})

    @staticmethod
    def _find_owner_gender(names):
        owner_gender = ''
        for n in names:
            try:
                if len(n) > 2:
                    owner_gender = Sex.find_sex(n)
                    break
            except SexException:
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
