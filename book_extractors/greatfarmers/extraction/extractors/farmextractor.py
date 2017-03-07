# -*- coding: utf-8 -*-
from book_extractors.greatfarmers.extraction.extractors.baseExtractor import BaseExtractor
from book_extractors.greatfarmers.extractionkeys import KEYS
import shared.regexUtils as regexUtils
import re

class FarmExtractor(BaseExtractor):

    def extract(self, text, entry):
        self.ALL_AREA_PATTERN = r"(?:(?:kok\.pinta-ala){s<=1,i<=2}|(?:kokonaispinta-ala){s<=1,i<=2}).{0,20}?(?P<area1>\d\d?\d?,?\d?\d?)\sha"
        self.FOREST_AREA_PATTERN = r"(?:metsää{s<=1}\s?(?P<area1>\d\d?\d?,?\d?\d?))|(?:(?P<area2>\d\d?\d?,?\d?\d?)\s?ha\s?metsää{s<=1})"
        self.FIELD_AREA_PATTERN = r"(?:(?:(?:salaojitettua\s){s<=1,i<=1})?peltoa{s<=1}\s?(?P<area1>\d\d?\d?,?\d?\d?))|(?:(?P<area2>\d\d?\d?,?\d?\d?)\s?ha\s?(?:salaojitettua\s{s<=1,i<=1})?peltoa{s<=1})"
        self.WASTE_AREA_PATTERN = r"(?:(?:joutomaata|joutomaita)\s?(?P<area1>\d\d?\d?,?\d?\d?))|(?:(?P<area2>\d\d?\d?,?\d?\d?)\s?ha\s?joutomaata{s<=1})"
        self.MEADOW_AREA_PATTERN = r"(?:luonnonlaidunta{s<=1}\s?(?P<area1>\d\d?\d?,?\d?\d?))|(?:(?P<area1>\d\d?\d?,?\d?\d?)\s?ha\s?luonnonlaidunta{s<=1})"

        self.AREA_OPTIONS = (re.UNICODE | re.IGNORECASE)
        self.whole_area = ""
        self.forest_area = ""
        self.field_area = ""
        self.waste_area = ""
        self.meadow_area = ""

        self._find_areas(text)
        return self._constructReturnDict()

    def _find_areas(self, text):
        self.whole_area = self._get_area(text, self.ALL_AREA_PATTERN)
        self.forest_area = self._get_area(text, self.FOREST_AREA_PATTERN)
        self.field_area = self._get_area(text, self.FIELD_AREA_PATTERN)
        self.waste_area = self._get_area(text, self.WASTE_AREA_PATTERN)
        self.meadow_area = self._get_area(text, self.MEADOW_AREA_PATTERN)

    def _get_area(self, text, pattern):
        area = ""
        try:
            foundArea= regexUtils.safeSearch(pattern, text, self.AREA_OPTIONS)
            self.matchFinalPosition = foundArea.end()
            if foundArea.group("area1") is not None:
                area = foundArea.group("area1")
            elif foundArea.group("area2") is not None:
                area = foundArea.group("area2")
        except regexUtils.RegexNoneMatchException as e:
            pass

        return area

    def _constructReturnDict(self):

        return {KEYS["farmDetails"] : {
            KEYS["wholeArea"] : self.whole_area,
            KEYS["forestArea"] : self.forest_area,
            KEYS["fieldArea"] : self.field_area,
            KEYS["wasteArea"] : self.waste_area,
            KEYS["meadowArea"] : self.meadow_area}
        }
