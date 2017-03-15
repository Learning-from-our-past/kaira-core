# -*- coding: utf-8 -*-
import re

from book_extractors.common.base_extractor import BaseExtractor
from book_extractors.extraction_exceptions import *
from shared import regexUtils, textUtils
from book_extractors.common.extraction_keys import KEYS
from book_extractors.extraction_pipeline import ExtractionPipeline, configure_extractor


class LocationExtractor(BaseExtractor):
    PATTERN = r'(?:\d+| s)(?:\s|,|\.)(?P<location>[A-ZÄ-Ö]{1,1}[A-ZÄ-Öa-zä-ö-]{1,}(?: mlk)?)'
    OPTIONS = re.UNICODE
    matchFinalPosition = 0
    foundLocation = None

    def extract(self, entry, extraction_results):
        """
        Note: Returns match-object for caller instead of string.
        :param entry:
        :param start_location:
        :return:
        """
        result = self._find_location(entry['text'])
        return self._constructReturnDict({
            "locationMatch": result[0]
        }, extraction_results, result[1])

    def _find_location(self, text):
        try:
            found_location_match = regexUtils.safeSearch(self.PATTERN, text, self.OPTIONS)
            cursor_location = found_location_match.end()
            return found_location_match, cursor_location
        except regexUtils.RegexNoneMatchException:
            raise LocationException(text)


class BirthdayLocationExtractor(BaseExtractor):


    def __init__(self, key_of_cursor_location_dependent, options):
        super(BirthdayLocationExtractor, self).__init__(key_of_cursor_location_dependent, options)
        self._sub_extraction_pipeline = ExtractionPipeline([
            configure_extractor(LocationExtractor)
        ])

        self.DEATHCHECK_PATTERN = r'(\bk\b|\bkaat\b)'
        self.REQUIRES_MATCH_POSITION = True
        self.SUBSTRING_WIDTH = 28

    def extract(self, entry, extraction_results):
        start_position = self.get_starting_position(extraction_results)
        prepared_text = self._prepare_text_for_extraction(entry['text'], start_position)

        result = self._find_location(prepared_text, start_position)
        return self._constructReturnDict({
            KEYS["birthLocation"]:  result[0]
        }, extraction_results, result[1])

    def _prepare_text_for_extraction(self, text, start_position):
        return textUtils.takeSubStrBasedOnPos(text, start_position-4, self.SUBSTRING_WIDTH)   # Dirty -4 offset

    def _find_location(self, text, start_position):
        cursor_location = start_position

        try:
            results = self._sub_extraction_pipeline.process({'text': text})
            self._check_if_location_is_valid(text, results['data']['locationMatch'])
            location = results['data']['locationMatch'].group("location")
            location = re.sub(r"([a-zä-ö])(\s|-)([a-zä-ö])", "\1\2", location)

            cursor_location = self.get_last_cursor_location(results) + start_position - 4
        except LocationException:
            # TODO: Metadata logging here self.errorLogger.logError(BirthLocationException.eType, self.currentChild )   #TODO: HOW ABOUT WOMEN?
            location = ''

        return location, cursor_location

    def _check_if_location_is_valid(self, text, found_location):
        # check if the string has data on death. If it is before the location, be careful to not
        # put the death location to birth location.
        death_position = regexUtils.findFirstPositionWithRegexSearch(self.DEATHCHECK_PATTERN, text, re.UNICODE)
        if death_position != -1:
            if death_position < found_location.end(): # there is word kaat, or " k " before location match.
                raise LocationException(text)
