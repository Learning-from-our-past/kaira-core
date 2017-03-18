# -*- coding: utf-8 -*-
import re

import shared.regexUtils as regexUtils
import shared.textUtils as textUtils
from book_extractors.common.extraction_keys import KEYS
from book_extractors.common.extractors.base_extractor import BaseExtractor
from book_extractors.extraction_pipeline import ExtractionPipeline, configure_extractor
from book_extractors.farmers.extraction.extractors.birthdayExtractor import BirthdayExtractor


class HostessExtractor(BaseExtractor):
    extraction_key = KEYS['hostess']

    def __init__(self, key_of_cursor_location_dependent, options):
        super(HostessExtractor, self).__init__(key_of_cursor_location_dependent, options)
        self.SEARCH_SPACE = 400
        self.HOSTESS_NAME_PATTERN = r"emäntä(?:nä)?(?:\svuodesta\s\d\d\d\d)?(?P<name>[A-ZÄ-Öa-zä-ö\.\s-]+),"
        self.HOSTESS_OPTIONS = (re.UNICODE | re.IGNORECASE)

        self._sub_extraction_pipeline = ExtractionPipeline([
            configure_extractor(BirthdayExtractor)
        ])

    def extract(self, entry, extraction_results):
        start_position = self.get_starting_position(extraction_results)
        results = self._find_hostess(entry['text'], start_position)
        return self._constructReturnDict(results[0], extraction_results, results[1])

    def _find_hostess(self, text, start_position):
        text = textUtils.takeSubStrBasedOnRange(text, start_position, self.SEARCH_SPACE)

        try:
            name = self._find_hostess_name(text)
            hostess_birthday = self._find_hostess_birthday(text[name[1]:])

            result = {
                KEYS["firstnames"]: name[0][0],
                KEYS["surname"]: name[0][1],
                KEYS["gender"]: 'Female',
                KEYS["hostessBirthData"]: hostess_birthday[0]
            }

            cursor_location = max(name[1], hostess_birthday[1])
            return result, cursor_location

        except regexUtils.RegexNoneMatchException:
            self.metadata_collector.add_error_record('hostessNotFound', 4)
            return None, 0

    def _find_hostess_birthday(self, text):
        results = self._sub_extraction_pipeline.process({'text': text})
        final_cursor_location = self.get_last_cursor_location(results)
        return results['birthday']['results'], final_cursor_location

    def _find_hostess_name(self, text):
        hostess_name_match = regexUtils.safeSearch(self.HOSTESS_NAME_PATTERN, text, self.HOSTESS_OPTIONS)
        cursor_location = hostess_name_match.end()
        hostess_name = self._split_names(hostess_name_match.group("name"))

        return hostess_name, cursor_location

    @staticmethod
    def _split_names(name):
        name = re.sub(r"(?:<|>|&|')", r"", name)
        names = re.split(" ", name)
        first_names = ''

        surname = names[len(names)-1].strip(" ")
        if len(names) > 1:
            for i in range(0, len(names)-1):
                if names[i].strip(" ") != "o.s.":
                    first_names += names[i].strip(" ") + " "
            first_names = first_names.strip(" ")

        return first_names, surname
