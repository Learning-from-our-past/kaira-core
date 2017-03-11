# -*- coding: utf-8 -*-
import re

from book_extractors.common.base_extractor import BaseExtractor
from book_extractors.extraction_exceptions import *
from shared import regexUtils, textUtils
from book_extractors.common.extraction_keys import KEYS
from book_extractors.extraction_pipeline import ExtractionPipeline, configure_extractor


#This class extracts a location string from provided substring/text.
#Used mostly by other books such as Death and Demobilization books.
#NOTE: DOESN'T INHERIT BASEEXTRACTOR!
#Also return match object to be used by caller

class LocationExtractor(BaseExtractor):
    PATTERN = r'(?:\d+| s)(?:\s|,|\.)(?P<location>[A-ZÄ-Ö]{1,1}[A-ZÄ-Öa-zä-ö-]{1,}(?: mlk)?)'
    OPTIONS = re.UNICODE
    matchFinalPosition = 0
    foundLocation = None

    def extract(self, entry, start_location=0):
        self._findLocation(entry['text'])
        return self._constructReturnDict()

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

    def _constructReturnDict(self):
        return {"locationMatch": self.foundLocation, "cursorLocation": self.matchFinalPosition}


class BirthdayLocationExtractor(BaseExtractor):
    DEATHCHECK_PATTERN = r'(\bk\b|\bkaat\b)'
    REQUIRES_MATCH_POSITION = True
    SUBSTRING_WIDTH = 28

    def extract(self, entry, start_position=0):
        self._sub_extraction_pipeline = ExtractionPipeline([
            configure_extractor(LocationExtractor)
        ])

        self.matchStartPosition = start_position  # TODO: Remove once this class is stateless

        self.location = ""
        self.preparedText = self._prepareTextForExtraction(entry['text'])

        self._findLocation(self.preparedText)
        return self._constructReturnDict()

    def _prepareTextForExtraction(self, text):
        t = textUtils.takeSubStrBasedOnPos(text, self.matchStartPosition-4, self.SUBSTRING_WIDTH)   #TODO: Dirty -4 offset
        return t

    def _findLocation(self, text):
        try:
            results = self._sub_extraction_pipeline.process({'text': text})
            self._checkIfLocationIsValid(text, results['locationMatch'])
            self.location = results['locationMatch'].group("location")
            self.location = re.sub(r"([a-zä-ö])(\s|-)([a-zä-ö])", "\1\2", self.location)

            self.matchFinalPosition = results['cursorLocation'] + self.matchStartPosition - 4
        except LocationException as e:
            # TODO: Metadata logging here self.errorLogger.logError(BirthLocationException.eType, self.currentChild )   #TODO: HOW ABOUT WOMEN?
            self.location = ""

    def _checkIfLocationIsValid(self, text, foundLocation):
        #check if the string has data on death. If it is before the location, be careful to not
        #put the death location to birth location.
        deathPosition = regexUtils.findFirstPositionWithRegexSearch(self.DEATHCHECK_PATTERN, text, re.UNICODE)
        if deathPosition != -1:
            if deathPosition < foundLocation.end(): #there is word kaat, or " k " before location match.
                raise LocationException(text)

    def _constructReturnDict(self):
        return {KEYS["birthLocation"] :  self.location, "cursorLocation" : self.getFinalMatchPosition()}
