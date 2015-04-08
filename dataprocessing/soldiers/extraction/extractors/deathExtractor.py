# -*- coding: utf-8 -*-
import re

from soldiers.extraction.extractors.baseExtractor import BaseExtractor
import soldiers.extraction.extractors.regexUtils as regexUtils
import soldiers.extraction.extractors.textUtils as textUtils
from soldiers.extraction.extractionExceptions import *
from soldiers.extraction.extractors.dateExtractor import DateExtractor
from soldiers.extraction.extractors.locationExtractor import LocationExtractor
from soldiers.extractionkeys import KEYS, ValueWrapper


class DeathExtractor(BaseExtractor):
    #TODO: Split deatlocationExtract to own class like the birthday one?
    DATE_PATTERN_DEFAULT = r'k(?:(?:(?P<day>\d{1,2})(?:\.|,|:|s)(?P<month>\d{1,2})(?:\.|,|:|s)(?P<year>\d{2,4}))|(?P<yearOnly>\d{2,4})(?!\.|,|\d)(?=\D\D\D\D\D))'
    DATE_PATTERN_FALLEN = r'kaat(?:(?:(?P<day>\d{1,2})(?:\.|,|:|s)(?P<month>\d{1,2})(?:\.|,|:|s)(?P<year>\d{2,4}))|(?P<yearOnly>\d{2,4})(?!\.|,|\d)(?=\D\D\D\D\D))'
    date_pattern = ""
    DATE_OPTIONS = re.UNICODE | re.IGNORECASE
    LOCATION_SUBSTRING_WIDTH = 110
    DATE_SUBSTRING_WIDTH = 320

    REQUIRES_MATCH_POSITION = True
    dateExtractor = None
    locationExtractor = None
    day = ""
    month = ""
    year = ""
    location = ""
    fallenInWar = False
    doneForWife = False     #TODO: Refactor the code to make this needless later. Used in preparation

    def extract(self, text):
        super(DeathExtractor, self).extract(text)
        try:
            #TODO: Refactor to more easy to read format
            self.initExtractors()
            preparedText = self._takeSubstring(text)
            self._findIfFallenInWar(preparedText)

            preparedText = self._prepareTextForDateExtraction(preparedText)
            self._findDate(preparedText)

            preparedText = self._prepareTextForLocationExtraction(text)
            self._findLocation(preparedText)

        except DeathFailedException as e:
            #just return empty dict
            pass
        return self._constructReturnDict()

    def targetIsSpouse(self):
        self.doneForWife = True

    def initExtractors(self):
        self.dateExtractor = DateExtractor()
        self.dateExtractor.setDatesToAlwaysIn20thCentury(True)
        self.locationExtractor = LocationExtractor()

    def _takeSubstring(self, text):
        return textUtils.takeSubStrBasedOnFirstRegexOccurrence(text,r'(?P<match>pso|ts:|js:)', re.IGNORECASE | re.UNICODE)

    def _prepareTextForDateExtraction(self, text):
        return textUtils.takeSubStrBasedOnPos(text, self.matchStartPosition, self.DATE_SUBSTRING_WIDTH)

    def _prepareTextForLocationExtraction(self, text):
        #Death location is directly after the date.
        t = self._takeSubstring(text)

        if not self.doneForWife:
            #TODO: The dirty +10 is because the position returned from dateExtractor is slightly smaller because of
            #TODO: removing spaces from the string. There should be better solution for this. Save amount of removed spaces...?
            t = textUtils.takeSubStrBasedOnPos(t, self.dateExtractor.getFinalMatchPosition()+10, self.LOCATION_SUBSTRING_WIDTH)
        else:
            t = textUtils.takeSubStrBasedOnPos(t, self.dateExtractor.getFinalMatchPosition(), self.LOCATION_SUBSTRING_WIDTH)
        return t

    def _findIfFallenInWar(self, text):
        if regexUtils.matchExists(r" kaat ", text):
            self.fallenInWar = True
            self.date_pattern = self.DATE_PATTERN_FALLEN
        else:
            self.fallenInWar = False
            self.date_pattern = self.DATE_PATTERN_DEFAULT

    def _findLocation(self, text):
        try:
            foundLocation = self.locationExtractor.extract(text)
            self.location = foundLocation.group("location")
            self._setFinalMatchPosition()
        except LocationException as e:
            self._locationExtractionFailed()

    def _locationExtractionFailed(self):
        self.location = ""

    def _findDate(self, text):
        try:
            foundDate = self.dateExtractor.extract(text, self.date_pattern, self.DATE_OPTIONS)
            self._foundDateToVars(foundDate)
            self._setFinalMatchPosition()
        except DateException as e:
            raise DeathFailedException()

    def _foundDateToVars(self, date):
        self.day = date["day"]
        self.month = date["month"]
        self.year = date["year"]

    def _setFinalMatchPosition(self):
        self.matchFinalPosition = self.dateExtractor.getFinalMatchPosition() + self.locationExtractor.getFinalMatchPosition()

    def _constructReturnDict(self):
        return  {KEYS["deathDay"]:  ValueWrapper(self.day),KEYS["deathMonth"]:  ValueWrapper(self.month), KEYS["deathYear"]:  ValueWrapper(self.year), KEYS["kaatunut"]:  ValueWrapper(self.fallenInWar), KEYS["deathLocation"]:  ValueWrapper(self.location), "cursorLocation": self.matchFinalPosition}

class DeathFailedException(Exception):
    message = "Couldn't find death data."
    def __unicode__(self):
        return repr(self.message)