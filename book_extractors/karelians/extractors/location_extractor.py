# -*- coding: utf-8 -*-
import re
from book_extractors.common.extraction_keys import KEYS
from book_extractors.common.extractors.base_extractor import BaseExtractor
from shared import regexUtils, text_utils
from book_extractors.common.postprocessors import place_name_cleaner
from shared.text_utils import remove_hyphens_from_text
from shared.geo.geocoding import GeoCoder, LocationNotFound


class FindLocation:
    PATTERN = r'(?:\d+| s)(?:\s|,|\.)(?P<location>[A-ZÄ-Ö]{1,1}[A-ZÄ-Öa-zä-ö-]{1,}(?: mlk)?)'
    OPTIONS = re.UNICODE
    matchFinalPosition = 0
    foundLocation = None

    def find_location(self, text):
        """
        Note: Returns match-object for caller instead of string.
        :param text:
        :return:
        """
        try:
            found_location_match = regexUtils.safe_search(self.PATTERN, text, self.OPTIONS)
            cursor_location = found_location_match.end()
            return found_location_match, cursor_location
        except regexUtils.RegexNoneMatchException:
            raise LocationException(text)


class BirthdayLocationExtractor(BaseExtractor):
    extraction_key = 'birthLocation'

    def __init__(self, cursor_location_depends_on=None, options=None):
        super(BirthdayLocationExtractor, self).__init__(cursor_location_depends_on, options)

        self.DEATHCHECK_PATTERN = r'(\bk\b|\bkaat\b)'
        self.REQUIRES_MATCH_POSITION = True
        # FIXME: This might need some adjusting still. 32 -> 42 improved results quite a bit though lowered
        # the DeathYear extraction results a bit.
        self.SUBSTRING_WIDTH = 42

    def _extract(self, entry, extraction_results, extraction_metadata):
        start_position = self.get_starting_position(extraction_metadata)
        prepared_text = self._prepare_text_for_extraction(entry['text'], start_position)

        location_result = self._find_location(prepared_text, start_position)
        return self._add_to_extraction_results(location_result[0], extraction_results, extraction_metadata, location_result[1])

    def _postprocess(self, entry, extraction_results, extraction_metadata):
        """
        After extraction, run a postprocess cleaning and name fixing for the location.
        :param entry: 
        :param extraction_results: 
        :return: 
        """
        self._get_output_path(extraction_results)[self.extraction_key] = self._augment_location_data(self._get_output_path(extraction_results)[self.extraction_key])
        return extraction_results, extraction_metadata

    def _augment_location_data(self, location_name):
        location_entry = {
            KEYS['locationName']: location_name,
            KEYS['region']: None,
            KEYS['latitude']: None,
            KEYS['longitude']: None
        }

        location_entry = place_name_cleaner.clean_place_name(location_entry)
        location_entry = place_name_cleaner.normalize_place(location_entry)

        # Try to find coordinates and region of the place from our geo database
        # If coordinates were found, merge them to the location entry dict.
        try:
            region_and_coordinates = GeoCoder.get_coordinates(location_entry[KEYS['locationName']])
            location_entry = {**location_entry, **region_and_coordinates}
        except LocationNotFound:
            pass

        return location_entry

    def _prepare_text_for_extraction(self, text, start_position):
        return text_utils.take_sub_str_based_on_pos(text, start_position - 4, self.SUBSTRING_WIDTH)   # Dirty -4 offset

    def _find_location(self, text, start_position):
        cursor_location = start_position

        try:
            location_match, match_end = self._find_location_match(text)
            self._check_if_location_is_valid(text, location_match)
            location = location_match.group('location')
            location = remove_hyphens_from_text(location)
            location = location.replace('\s', '')

            # FIXME: Why there is a magic number "4" here...? What is the point of it? See also text preparation function.
            cursor_location = match_end + start_position - 4
        except LocationException:
            self.metadata_collector.add_error_record('birthLocationNotFound', 2)
            location = ''

        return location, cursor_location

    def _find_location_match(self, text):
        """
        Note: Returns match-object for caller instead of string.
        :param text:
        :return:
        """
        pattern = r'(?:\d+| s)(?:\s|,|\.)(?P<location>[A-ZÄ-Ö]{1,1}[A-ZÄ-Öa-zä-ö-]{1,}(?: mlk)?)'
        try:
            found_location_match = regexUtils.safe_search(pattern, text, re.UNICODE)
            cursor_location = found_location_match.end()
            return found_location_match, cursor_location
        except regexUtils.RegexNoneMatchException:
            raise LocationException(text)

    def _check_if_location_is_valid(self, text, found_location):
        # check if the string has data on death. If it is before the location, be careful to not
        # put the death location to birth location.
        death_position = regexUtils.find_first_position_with_regex_search(self.DEATHCHECK_PATTERN, text, re.UNICODE)
        if death_position != -1:
            if death_position < found_location.end(): # there is word kaat, or " k " before location match.
                raise LocationException(text)


class LocationException(Exception):
    eType = "LOCATION"
    message = "ERROR in location extraction: "
    details = u""

    def __init__(self, text):
        self.details = text

    def __unicode__(self):
        return repr(self.message)
