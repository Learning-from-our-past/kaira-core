# -*- coding: utf-8 -*-
import re
from book_extractors.common.extraction_keys import KEYS
from book_extractors.common.extractors.base_extractor import BaseExtractor
from book_extractors.extraction_exceptions import *
from book_extractors.extraction_pipeline import ExtractionPipeline, configure_extractor
from shared import regexUtils, textUtils
from book_extractors.common.postprocessors import place_name_cleaner


class LocationExtractor(BaseExtractor):
    PATTERN = r'(?:\d+| s)(?:\s|,|\.)(?P<location>[A-ZÄ-Ö]{1,1}[A-ZÄ-Öa-zä-ö-]{1,}(?: mlk)?)'
    OPTIONS = re.UNICODE
    matchFinalPosition = 0
    foundLocation = None

    extraction_key = 'location'

    def _extract(self, entry, extraction_results):
        """
        Note: Returns match-object for caller instead of string.
        :param entry:
        :param start_location:
        :return:
        """
        result = self._find_location(entry['text'])
        return self._add_to_extraction_results({
            "locationMatch": result[0]
        }, extraction_results, result[1])

    def _find_location(self, text):
        try:
            found_location_match = regexUtils.safe_search(self.PATTERN, text, self.OPTIONS)
            cursor_location = found_location_match.end()
            return found_location_match, cursor_location
        except regexUtils.RegexNoneMatchException:
            raise LocationException(text)


class BirthdayLocationExtractor(BaseExtractor):
    extraction_key = 'birthLocation'

    def __init__(self, key_of_cursor_location_dependent, options):
        super(BirthdayLocationExtractor, self).__init__(key_of_cursor_location_dependent, options)
        self._sub_extraction_pipeline = ExtractionPipeline([
            configure_extractor(LocationExtractor)
        ])

        self.DEATHCHECK_PATTERN = r'(\bk\b|\bkaat\b)'
        self.REQUIRES_MATCH_POSITION = True
        self.SUBSTRING_WIDTH = 32

    def _extract(self, entry, extraction_results):
        start_position = self.get_starting_position(extraction_results)
        prepared_text = self._prepare_text_for_extraction(entry['text'], start_position)

        result = self._find_location(prepared_text, start_position)
        location_entry = self._augment_location_data(result[0])

        return self._add_to_extraction_results(location_entry, extraction_results, result[1])

    def _augment_location_data(self, location_name):
        location_entry = {
            KEYS['locationName']: location_name,
            KEYS['region']: None,
        }

        location_entry = place_name_cleaner.clean_place_name(location_entry)
        return place_name_cleaner.try_to_normalize_place_name(location_entry, self.metadata_collector)

    def _prepare_text_for_extraction(self, text, start_position):
        return textUtils.take_sub_str_based_on_pos(text, start_position - 4, self.SUBSTRING_WIDTH)   # Dirty -4 offset

    def _find_location(self, text, start_position):
        cursor_location = start_position

        try:
            results = self._sub_extraction_pipeline.process({'text': text})
            self._check_if_location_is_valid(text, results['location']['results']['locationMatch'])
            location = results['location']['results']['locationMatch'].group("location")
            location = location.replace('-', '')
            location = location.replace('\s', '')

            cursor_location = self.get_last_cursor_location(results) + start_position - 4
        except LocationException:
            self.metadata_collector.add_error_record('birthLocationNotFound', 2)
            location = ''

        return location, cursor_location

    def _check_if_location_is_valid(self, text, found_location):
        # check if the string has data on death. If it is before the location, be careful to not
        # put the death location to birth location.
        death_position = regexUtils.find_first_position_with_regex_search(self.DEATHCHECK_PATTERN, text, re.UNICODE)
        if death_position != -1:
            if death_position < found_location.end(): # there is word kaat, or " k " before location match.
                raise LocationException(text)
