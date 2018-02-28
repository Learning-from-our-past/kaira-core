# -*- coding: utf-8 -*-
import re

import core.utils.regex_utils as regexUtils
from extractors.common.extraction_keys import KEYS
from core.pipeline_construction.base_extractor import BaseExtractor
from core.utils import text_utils

class FarmExtractor(BaseExtractor):
    extraction_key = KEYS['farmDetails']

    def __init__(self, cursor_location_depends_on=None, options=None):
        super(FarmExtractor, self).__init__(cursor_location_depends_on, options)
        self.ALL_AREA_PATTERN = r"(?:(?:kok\.pinta-ala){s<=1,i<=2}|(?:kokonaispinta-ala){s<=1,i<=2}).{0,20}?(?P<area1>\d\d?\d?,?\d\d)\sha"
        self.FOREST_AREA_PATTERN = r"(?:metsää{s<=1}\s?(?P<area1>\d\d?\d?,?\d\d))|(?:(?P<area2>\d\d?\d?,\d\d)\s?ha\s?metsää{s<=1})"
        self.FIELD_AREA_PATTERN = r"(?:(?:(?:salaojitettua\s){s<=1,i<=1})?peltoa{s<=1}\s?(?P<area1>\d\d?\d?,?\d\d))|(?:(?P<area2>\d\d?\d?,\d\d)\s?ha\s?(?:salaojitettua\s{s<=1,i<=1})?peltoa{s<=1})"
        self.WASTE_AREA_PATTERN = r"(?:joutomaata{s<=1}\s?(?P<area1>\d\d?\d?,?\d\d))|(?:(?P<area2>\d\d?\d?,\d\d)\s?ha\s?joutomaata{s<=1})"
        self.MEADOW_AREA_PATTERN = r"(?:niittyä{s<=1}\s?(?P<area1>\d\d?\d?,?\d\d))|(?:(?P<area1>\d\d?\d?,\d\d)\s?ha\s?niittyä{s<=1})"
        self.AREA_OPTIONS = (re.UNICODE | re.IGNORECASE)

    def _extract(self, entry, extraction_results, extraction_metadata):
        start_position = self.get_starting_position(extraction_metadata)
        result = self._find_areas(entry['text'])
        return self._add_to_extraction_results(result, extraction_results, extraction_metadata, start_position)

    def _find_areas(self, text):
        whole_area = self._get_area(text, self.ALL_AREA_PATTERN)
        forest_area = self._get_area(text, self.FOREST_AREA_PATTERN)
        field_area = self._get_area(text, self.FIELD_AREA_PATTERN)
        waste_area = self._get_area(text, self.WASTE_AREA_PATTERN)
        meadow_area = self._get_area(text, self.MEADOW_AREA_PATTERN)

        return {
            KEYS["wholeArea"]: text_utils.float_or_none(whole_area[0]),
            KEYS["forestArea"]: text_utils.float_or_none(forest_area[0]),
            KEYS["fieldArea"]: text_utils.float_or_none(field_area[0]),
            KEYS["wasteArea"]: text_utils.float_or_none(waste_area[0]),
            KEYS["meadowArea"]: text_utils.float_or_none(meadow_area[0])
        }

    def _get_area(self, text, pattern):
        area = None
        cursor_location = 0
        try:
            found_area_match = regexUtils.safe_search(pattern, text, self.AREA_OPTIONS)
            cursor_location = found_area_match.end()
            if found_area_match.group("area1") is not None:
                area = found_area_match.group("area1")
            elif found_area_match.group("area2") is not None:
                area = found_area_match.group("area2")
        except regexUtils.RegexNoneMatchException:
            pass

        return area, cursor_location
