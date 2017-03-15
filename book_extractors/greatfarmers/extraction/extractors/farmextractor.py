# -*- coding: utf-8 -*-
import re

import shared.regexUtils as regexUtils
from book_extractors.common.extraction_keys import KEYS
from book_extractors.common.extractors.base_extractor import BaseExtractor


class FarmExtractor(BaseExtractor):

    def __init__(self, key_of_cursor_location_dependent, options):
        super(FarmExtractor, self).__init__(key_of_cursor_location_dependent, options)
        self.ALL_AREA_PATTERN = r"(?:(?:kok\.pinta-ala){s<=1,i<=2}|(?:kokonaispinta-ala){s<=1,i<=2}).{0,20}?(?P<area1>\d\d?\d?,?\d?\d?)\sha"
        self.FOREST_AREA_PATTERN = r"(?:metsää{s<=1}\s?(?P<area1>\d\d?\d?,?\d?\d?))|(?:(?P<area2>\d\d?\d?,?\d?\d?)\s?ha\s?metsää{s<=1})"
        self.FIELD_AREA_PATTERN = r"(?:(?:(?:salaojitettua\s){s<=1,i<=1})?peltoa{s<=1}\s?(?P<area1>\d\d?\d?,?\d?\d?))|(?:(?P<area2>\d\d?\d?,?\d?\d?)\s?ha\s?(?:salaojitettua\s{s<=1,i<=1})?peltoa{s<=1})"
        self.WASTE_AREA_PATTERN = r"(?:(?:joutomaata|joutomaita)\s?(?P<area1>\d\d?\d?,?\d?\d?))|(?:(?P<area2>\d\d?\d?,?\d?\d?)\s?ha\s?joutomaata{s<=1})"
        self.MEADOW_AREA_PATTERN = r"(?:luonnonlaidunta{s<=1}\s?(?P<area1>\d\d?\d?,?\d?\d?))|(?:(?P<area1>\d\d?\d?,?\d?\d?)\s?ha\s?luonnonlaidunta{s<=1})"
        self.AREA_OPTIONS = (re.UNICODE | re.IGNORECASE)

    def extract(self, entry, extraction_results):
        start_position = self.get_starting_position(extraction_results)
        result = self._find_areas(entry['text'])
        return self._constructReturnDict({KEYS["farmDetails"]: result}, extraction_results, start_position)

    def _find_areas(self, text):
        whole_area = self._get_area(text, self.ALL_AREA_PATTERN)
        forest_area = self._get_area(text, self.FOREST_AREA_PATTERN)
        field_area = self._get_area(text, self.FIELD_AREA_PATTERN)
        waste_area = self._get_area(text, self.WASTE_AREA_PATTERN)
        meadow_area = self._get_area(text, self.MEADOW_AREA_PATTERN)

        return {
            KEYS["wholeArea"]: whole_area,
            KEYS["forestArea"]: forest_area,
            KEYS["fieldArea"]: field_area,
            KEYS["wasteArea"]: waste_area,
            KEYS["meadowArea"]: meadow_area
        }

    def _get_area(self, text, pattern):
        area = None
        try:
            found_area = regexUtils.safeSearch(pattern, text, self.AREA_OPTIONS)
            if found_area.group("area1") is not None:
                area = found_area.group("area1")
            elif found_area.group("area2") is not None:
                area = found_area.group("area2")
        except regexUtils.RegexNoneMatchException:
            pass

        return area
