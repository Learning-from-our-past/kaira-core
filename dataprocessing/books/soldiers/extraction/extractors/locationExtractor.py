# -*- coding: utf-8 -*-
import re

from books.soldiers.extraction.extractors.baseExtractor import BaseExtractor
from books.soldiers.extraction.extractionExceptions import *
from books.soldiers.extraction.extractors import textUtils, regexUtils
from books.soldiers.extractionkeys import KEYS
from interface.valuewrapper import ValueWrapper






#This class extracts a location string from provided substring/text.
#Used mostly by other books such as Death and Demobilization books.
#NOTE: DOESN'T INHERIT BASEEXTRACTOR!
#Also return match object to be used by caller

class LocationExtractor():
    PATTERN = r'(?:\d+| s)(?: |,|\.)(?P<location>[A-ZÄ-Ö]{1,1}[A-ZÄ-Öa-zä-ö-]{1,}(?: mlk)?)'
    OPTIONS = re.UNICODE
    matchFinalPosition = 0
    foundLocation = None

    def extract(self, text):
        self._findLocation(text)
        return self.foundLocation

    def setCustomPattern(self, pattern, options):
        self.PATTERN = pattern
        self.OPTIONS = options

    def _prepareTextForExtraction(self, text):
        t = textUtils.removeSpacesFromText(text)
        return t

    def _findLocation(self, text):
        try:
            self.foundLocation = regexUtils.safeSearch(self.PATTERN, text, self.OPTIONS)
            self.matchFinalPosition = self.foundLocation.end()
        except regexUtils.RegexNoneMatchException as e:
            raise LocationException(text)

    def getFinalMatchPosition(self):
        return self.matchFinalPosition








class BirthdayLocationExtractor(BaseExtractor):
    DEATHCHECK_PATTERN = r'(\bk\b|\bkaat\b)'
    REQUIRES_MATCH_POSITION = True
    SUBSTRING_WIDTH = 28
    locationExtractor = None
    preparedText = ""
    location = ""

    def extract(self, text):
        super(BirthdayLocationExtractor, self).extract(text)
        self.initVars(text)
        self._findLocation(self.preparedText)
        return self._constructReturnDict()

    def initVars(self,text):
        self.locationExtractor = LocationExtractor()
        self.preparedText = self._prepareTextForExtraction(text)

    def _prepareTextForExtraction(self, text):
        t = textUtils.takeSubStrBasedOnPos(text, self.matchStartPosition-4, self.SUBSTRING_WIDTH)   #TODO: Dirty -4 offset
        return t

    def _findLocation(self, text):
        try:
            self.foundLocation = self.locationExtractor.extract(text)
            self._checkIfLocationIsValid(text, self.foundLocation)
            self.location = self.foundLocation.group("location")
            self._setFinalMatchPosition()
        except LocationException as e:
            self.errorLogger.logError(ManLocationException.eType, self.currentChild )   #TODO: HOW ABOUT WOMEN?
            self._locationExtractionFailed()

    def _checkIfLocationIsValid(self, text, foundLocation):
        #check if the string has data on death. If it is before the location, be careful to not
        #put the death location to birth location.
        deathPosition = regexUtils.findFirstPositionWithRegexSearch(self.DEATHCHECK_PATTERN, text, re.UNICODE)
        if deathPosition != -1:
            if deathPosition < foundLocation.end(): #there is word kaat, or " k " before location match.
                raise LocationException(text)

    def _locationExtractionFailed(self):
        self.location = ""

    def _setFinalMatchPosition(self):
        #Dirty fix for inaccuracy in positions which would screw the Location extraction
        self.matchFinalPosition = self.locationExtractor.getFinalMatchPosition() + self.matchStartPosition - 4  #TODO: Dirty -4 offset

    def _constructReturnDict(self):
        return {KEYS["birthLocation"] :  ValueWrapper(self.location), "cursorLocation" : self.getFinalMatchPosition()}
