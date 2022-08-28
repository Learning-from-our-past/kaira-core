# -*- coding: utf-8 -*-
import re
from core.pipeline_construction.base_extractor import BaseExtractor
from extractors.common.extraction_keys import KEYS
from core.utils import regex_utils, text_utils


class CommonBirthdayExtractor(BaseExtractor):
    extraction_key = KEYS['birthData']

    def __init__(self, cursor_location_depends_on=None, options=None):
        super(CommonBirthdayExtractor, self).__init__(
            cursor_location_depends_on, options
        )
        self.PATTERN = options['PATTERN']
        self.OPTIONS = re.UNICODE | re.IGNORECASE
        self.REQUIRES_MATCH_POSITION = True
        self.SUBSTRING_WIDTH = 100

        if 'remove_spaces' in options:
            self._remove_spaces_from_text = options['remove_spaces']
        else:
            self._remove_spaces_from_text = True

        self._date_finder = DateFinder(self.PATTERN, self.OPTIONS)

    def _extract(self, entry, extraction_results, extraction_metadata):
        start_position = self.get_starting_position(extraction_metadata)
        prepared_text = self._prepare_text_for_extraction(entry['text'], start_position)
        found_birth_date, cursor_location = self._find_date(
            prepared_text, start_position
        )

        return self._add_to_extraction_results(
            found_birth_date, extraction_results, extraction_metadata, cursor_location
        )

    def _prepare_text_for_extraction(self, text, start_position):
        t = text_utils.take_sub_str_based_on_pos(
            text, start_position, self.SUBSTRING_WIDTH
        )

        if self._remove_spaces_from_text:
            t = text_utils.remove_spaces_from_text(t)

        spouse_found = regex_utils.find_first_position_with_regex_search(
            'puol', t, re.IGNORECASE | re.UNICODE
        )
        if spouse_found != -1:
            t = t[0:spouse_found]

        return t

    def _find_date(self, text, start_position):
        # By default we want assume the cursor location to be at start_position
        cursor_location = start_position

        try:
            found_date, date_cursor_location = self._date_finder.find_date(text)
            cursor_location = date_cursor_location + start_position - 4
        except DateException:
            # TODO: Better idea to have in DateExtractor class maybe?
            found_date = {'day': None, 'month': None, 'year': None}

        # Map date to birthDate
        birth_date = {
            KEYS['birthDay']: text_utils.int_or_none(found_date['day']),
            KEYS['birthMonth']: text_utils.int_or_none(found_date['month']),
            KEYS['birthYear']: text_utils.int_or_none(found_date['year']),
        }

        return birth_date, cursor_location


class DateFinder:
    """
    An utility class for date finding purposes. Not an extractor itself though.
    """

    def __init__(self, pattern, options):
        self.PATTERN = pattern
        self.OPTIONS = options
        self.MONTH_NAME_NUMBER_MAPPING = {
            'syks': 9,
            'marrask': 11,
            'eiok': 8,
            'elok': 8,
            'heinäk': 7,
            'helmik': 2,
            'huhtik': 4,
            'jouluk': 12,
            'kesäk': 6,
            'lokak': 10,
            'maalisk': 3,
            'maallsk': 3,
            'syysk': 9,
            'tammik': 1,
            'toukok': 5,
        }

    def find_date(self, text):
        prepared_text = self._prepare_text_for_extraction(text)

        try:
            result, cursor_location = self._find_date(prepared_text)
        except DateException:
            # non-space pattern match didn't produce results, try with including spaces
            result, cursor_location = self._find_date(text)

        return result, cursor_location

    @staticmethod
    def _prepare_text_for_extraction(text):
        # FIXME: This should probably be conditional based on the remove_spaces option set in CommonBirthDayExtractor.
        # Atm the resulting cursor_locations will be incorrect since the CBDE reports the end of match which will be incorrect
        # since its taken from a string with spaces removed! Note that fixing this will involve testing possible changes in outputs of
        # all existing book series which use this extractor.
        return text_utils.remove_spaces_from_text(text)

    def _find_date(self, text):
        try:
            found_date_matches = regex_utils.safe_search(
                self.PATTERN, text, self.OPTIONS
            )
            months_and_years_from_words = self._if_written_month_names_extract_them(
                found_date_matches
            )
            cursor_location = found_date_matches.end()
            if months_and_years_from_words is None:
                year = self._get_year_from_match(found_date_matches)
                day_and_month = self._get_month_and_day_from_match(found_date_matches)

                return {
                    'day': day_and_month['day'],
                    'month': day_and_month['month'],
                    'year': year,
                }, cursor_location
            else:
                return {
                    'day': '',
                    'month': months_and_years_from_words[0],
                    'year': months_and_years_from_words[1],
                }, cursor_location
        except regex_utils.RegexNoneMatchException:
            raise DateException(text)

    @staticmethod
    def _get_month_and_day_from_match(date_match):
        return {
            'day': text_utils.int_or_none(date_match.group('day')),
            'month': text_utils.int_or_none(date_match.group('month')),
        }

    def _if_written_month_names_extract_them(self, date_match):
        try:
            # year and month available
            month_match = date_match.group('monthName')
            month = self._map_month_name_to_number(month_match)
            year = date_match.group('monthYear')  # special capture group.
            year = self._transform_year(year)
            return month, year
        except (IndexError, TypeError):
            return None  # there is no monthYear or monthName, so use other extraction method

    def _map_month_name_to_number(self, name):
        if name in self.MONTH_NAME_NUMBER_MAPPING:
            return self.MONTH_NAME_NUMBER_MAPPING[name]
        else:
            return None

    def _get_year_from_match(self, date_match):
        # get the result from correct capturegroup.
        # If there is full date (12.7.18) it is in 1, if only year it is in 2.
        if date_match.group('year') is None:
            year = self._transform_year(date_match.group('yearOnly'))
        else:
            year = self._transform_year(date_match.group('year'))
        self._check_is_year_sensible(year)
        return year

    @staticmethod
    def _transform_year(year):
        # fix years to four digit format.
        if int(year) < 70:
            year = '19' + year
        elif int(year) < 1800:
            year = '18' + year

        return text_utils.int_or_none(year)

    @staticmethod
    def _check_is_year_sensible(year):
        if int(year) > 2000 or int(year) < 1800:
            raise DateException('Date is not sensible.')


class DateException(Exception):
    eType = "DATE"
    message = "ERROR in date extraction: "
    details = u""

    def __init__(self, text):
        self.details = text

    def __unicode__(self):
        return repr(self.message)
