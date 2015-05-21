# -*- coding: utf-8 -*-
from books.farmers.extraction.extractors.baseExtractor import BaseExtractor
from books.farmers.extractionkeys import KEYS
from interface.valuewrapper import ValueWrapper
#from books.farmers.extraction.extractionExceptions import ProfessionException
import shared.textUtils as textUtils
import shared.regexUtils as regexUtils
import re

class FarmExtractor(BaseExtractor):

    #kok\.pinta-ala.+?(\d\d,?\d\d)
    #(metsää\s?\d\d?\d?,?\d\d)|(\d\d?\d?,\d\d\s?ha\s?metsää)
    #(peltoa\s?\d\d?\d?,?\d\d)|(\d\d?\d?,\d\d\s?ha\s?peltoa)
    #(joutomaata\s?\d\d?\d?,?\d\d)|(\d\d?\d?,\d\d\s?ha\s?joutomaata)
    #(niittyä\s?\d\d?\d?,?\d\d)|(\d\d?\d?,\d\d\s?ha\s?niittyä)


    def extract(self, text, entry):
        self.ALL_AREA_PATTERN = r"(?:kok\.pinta-ala{s<=1}|kokonaispinta-ala{s<=1}).+?(?P<area1>\d\d?\d?,?\d\d)"
        self.FOREST_AREA_PATTERN = r"(?:metsää{s<=1}\s?(?P<area1>\d\d?\d?,?\d\d))|(?:(?P<area2>\d\d?\d?,\d\d)\s?ha\s?metsää{s<=1})"
        self.FIELD_AREA_PATTERN = r"(?:peltoa{s<=1}\s?(?P<area1>\d\d?\d?,?\d\d))|(?:(?P<area2>\d\d?\d?,\d\d)\s?ha\s?peltoa{s<=1})"
        self.WASTE_AREA_PATTERN = r"(?:joutomaata{s<=1}\s?(?P<area1>\d\d?\d?,?\d\d))|(?:(?P<area2>\d\d?\d?,\d\d)\s?ha\s?joutomaata{s<=1})"
        self.MEADOW_AREA_PATTERN = r"(?:niittyä{s<=1}\s?(?P<area1>\d\d?\d?,?\d\d))|(?:(?P<area1>\d\d?\d?,\d\d)\s?ha\s?niittyä{s<=1})"

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

        return {KEYS["farmDetails"] : ValueWrapper({
            KEYS["wholeArea"] : ValueWrapper(self.whole_area),
            KEYS["forestArea"] : ValueWrapper(self.forest_area),
            KEYS["fieldArea"] : ValueWrapper(self.field_area),
            KEYS["wasteArea"] : ValueWrapper(self.waste_area),
            KEYS["meadowArea"] : ValueWrapper(self.meadow_area)})
        }