# -*- coding: utf-8 -*-
import re

from books.soldiers.extraction.extractors.baseExtractor import BaseExtractor
from books.soldiers.extraction.extractionExceptions import *
from books.soldiers.extraction.extractors.dateExtractor import DateExtractor
from books.soldiers.extraction.extractors.locationExtractor import LocationExtractor
from books.soldiers.extraction.extractors import textUtils
from books.soldiers.extractionkeys import KEYS
from interface.valuewrapper import ValueWrapper


class DemobilizationExtractor(BaseExtractor):
    DATE_PATTERN = r'(?:Kot|kot|KOI)(?:(?:(?P<day>\d{1,2})(?:\.|,|:|s)(?P<month>\d{1,2})(?:\.|,|:|s)(?P<year>\d{2,4}))|(?P<yearOnly>\d{2,4}(?=\D\D\D\D\D))|(?:(?P<monthName>[a-zä-ö]*)(?P<monthYear>\d{2,4}(?=\D\D\D\D\D))))'
    DATE_OPTIONS = re.UNICODE | re.IGNORECASE
    LOCATION_PATTERN = r'\A(?P<location>[A-ZÄ-Öa-zä-ö-]+?)(?=[A-ZÄ-Ö.,:])'
    LOCATION_OPTIONS = re.UNICODE
    LOCATION_SUBSTRING_WIDTH = 100
    dateExtractor = None
    locationExtractor = None
    day = ""
    month = ""
    year = ""
    location = ""


    def extract(self, text):
        super(DemobilizationExtractor, self).extract(text)
        try:
            self.initExtractors()
            self._findDate(text)
            preparedTextForLocation = self._prepareTextForLocationExtraction(text)
            self._findLocation(preparedTextForLocation)
        except DemobilizationFailedException as e:
            #just return empty dict
            pass
        return self._constructReturnDict()

    def initExtractors(self):
        self.dateExtractor = DateExtractor()
        self.locationExtractor = LocationExtractor()
        self.locationExtractor.setCustomPattern(self.LOCATION_PATTERN, self.LOCATION_OPTIONS)

    def _prepareTextForLocationExtraction(self, text):
        #Demobilization location is directly after the date.
        t = textUtils.removeSpacesFromText(text)
        return textUtils.takeSubStrBasedOnPos(t, self.dateExtractor.getFinalMatchPosition(), self.LOCATION_SUBSTRING_WIDTH)

    def _findLocation(self, text):
        try:
            foundLocation = self.locationExtractor.extract(text)
            self.location = foundLocation.group("location")
            self._setFinalMatchPosition()
        except LocationException as e:
            self.errorLogger.logError(DemobilizationPlaceException.eType, self.currentChild)
            self._locationExtractionFailed()

    def _locationExtractionFailed(self):
        self.location = ""

    def _findDate(self, text):
        try:
            foundDate = self.dateExtractor.extract(text, self.DATE_PATTERN, self.DATE_OPTIONS)
            self._foundDateToVars(foundDate)
            self._setFinalMatchPosition()
        except DateException as e:
            self.errorLogger.logError(DemobilizationTimeException.eType, self.currentChild)
            raise DemobilizationFailedException()

    def _foundDateToVars(self, date):
        self.day = date["day"]
        self.month = date["month"]
        self.year = date["year"]

    def _setFinalMatchPosition(self):
        self.matchFinalPosition = self.dateExtractor.getFinalMatchPosition() + self.locationExtractor.getFinalMatchPosition()

    def _constructReturnDict(self):
        return {KEYS["kotiutusDay"]:  ValueWrapper(self.day),KEYS["kotiutusMonth"]:  ValueWrapper(self.month), KEYS["kotiutusYear"]:  ValueWrapper(self.year), KEYS["kotiutusPlace"] :  ValueWrapper(self.location)}


class DemobilizationFailedException(Exception):
    message = "ERROR in demobilization extraction"
    def __unicode__(self):
        return repr(self.message)
