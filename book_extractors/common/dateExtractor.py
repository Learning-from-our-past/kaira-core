# -*- coding: utf-8 -*-
from shared import regexUtils
import shared.textUtils as textUtils
from book_extractors.extraction_exceptions import *
from book_extractors.common.base_extractor import BaseExtractor


class DateExtractor(BaseExtractor):

    def __init__(self, options):
        super(DateExtractor, self).__init__(options)
        self.PATTERN = options['PATTERN']
        self.OPTIONS = options['OPTIONS']
        self.MONTH_NAME_NUMBER_MAPPING = {"syks": 9, "marrask": 11, "eiok": 8, "elok": 8, "heinäk": 7, "helmik": 2, "huhtik": 4,
                                          "jouluk": 12, "kesäk": 6, "lokak": 10, "maalisk": 3, "maallsk": 3, "syysk": 9, "tammik": 1, "toukok": 5}

    def extract(self, entry, start_position=0):
        prepared_text = self._prepare_text_for_extraction(entry['text'])

        try:
            result = self._find_date(prepared_text, start_position)
        except DateException:
            # non-space pattern match didn't produce results, try with including spaces
            result = self._find_date(entry['text'], start_position)

        return self._constructReturnDict(result[0], result[1])

    @staticmethod
    def _prepare_text_for_extraction(text):
        return textUtils.removeSpacesFromText(text)

    def _find_date(self, text, start_position):
        try:
            found_date_matches = regexUtils.safeSearch(self.PATTERN, text, self.OPTIONS)
            months_and_years_from_words = self._if_written_month_names_extract_them(found_date_matches)
            cursor_location = start_position + found_date_matches.end()
            if months_and_years_from_words is None:
                year = self._get_year_from_match(found_date_matches)
                day_and_month = self._get_month_and_day_from_match(found_date_matches)

                return {'day': day_and_month['day'], 'month': day_and_month['month'], 'year': year}, cursor_location
            else:
                return {'day': '', 'month': months_and_years_from_words[0], 'year': months_and_years_from_words[1]}, cursor_location
        except regexUtils.RegexNoneMatchException:
            raise DateException(text)

    @staticmethod
    def _get_month_and_day_from_match(date_match):
        return {
            'day': date_match.group("day"),
            'month': date_match.group("month")
        }

    def _if_written_month_names_extract_them(self, date_match):
        try:
            # year and month available
            month_match = date_match.group("monthName")
            month = self._map_month_name_to_number(month_match)
            year = date_match.group("monthYear")    # special capture group.
            year = self._transform_year(year)
            return month, year
        except (IndexError, TypeError):
            return None    # there is no monthYear or monthName, so use other extraction method

    def _map_month_name_to_number(self, name):
        if name in self.MONTH_NAME_NUMBER_MAPPING:
            return self.MONTH_NAME_NUMBER_MAPPING[name]
        else:
            return ""

    def _get_year_from_match(self, date_match):
        # get the result from correct capturegroup.
        # If there is full date (12.7.18) it is in 1, if only year it is in 2.
        if date_match.group("year") is None:
            year = self._transform_year(date_match.group("yearOnly"))
        else:
            year = self._transform_year(date_match.group("year"))
        self._check_is_year_sensible(year)
        return year

    @staticmethod
    def _transform_year(year):
        # fix years to four digit format.
        if int(year) < 70:
            year = "19" + year
        elif int(year) < 1800:
            year = "18" + year

        return year

    @staticmethod
    def _check_is_year_sensible(year):
        if int(year) > 2000 or int(year) < 1800:
            raise DateException('Date is not sensible.')