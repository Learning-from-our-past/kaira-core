# -*- coding: utf-8 -*-
import re
import regex
from baseExtractor import BaseExtractor
import regexUtils
import textUtils
from extraction.extractionExceptions import *

#This class extracts date from given string. Substringing has to be made in caller.
#The interface also differs a bit from other extractors since this is meant to be used by
#other extractors.
#NOTE: DOESN'T INHERIT BASEEXTRACTOR!
class DateExtractor():
    PATTERN = ur""
    OPTIONS = None
    preparedText = ""
    year = ""
    month = ""
    day = ""

    def extract(self, text, PATTERN, OPTIONS):
        self.PATTERN = PATTERN
        self.OPTIONS = OPTIONS
        self.preparedText = self._prepareTextForExtraction(text)
        self._findDate(self.preparedText)
        return self._constructReturnDict()

    def _prepareTextForExtraction(self, text):
        t = textUtils.removeSpacesFromText(text)
        return t

    def _findDate(self, text):
        try:
            foundDate = regexUtils.safeMatch(self.PATTERN, text, self.OPTIONS)
            self._getYearFromMatch(foundDate)
            self._getMonthAndDayFromMatch(foundDate)
            self._setFinalMatchPosition(foundDate)
        except regexUtils.RegexNoneMatchException as e:
            raise DateException(text)

    def _getMonthAndDayFromMatch(self, dateMatch):
        self.day = dateMatch.group("day")
        self.month = dateMatch.group("month")

    def _getYearFromMatch(self, dateMatch):
        #get the result from correct capturegroup.
        # If there is full date (12.7.18) it is in 1, if only year it is in 2.
        if dateMatch.group("year") is None:
            self.year = self._transformYear(dateMatch.group("yearOnly"))
        else:
            self.year = self._transformYear(dateMatch.group("year"))
        self._checkIsYearSensible()

    def _transformYear(self, year):
        #fix years to four digit format.
        if int(year) < 50:
            year = "19" + year
        elif int(year) < 1800:
            year = "18" + year
        return year

    def _checkIsYearSensible(self):
        if int(self.year) > 2000 or  int(self.year) < 1800:
            raise DateException(self.preparedText)

    def _setFinalMatchPosition(self, foundDate):
        self.matchFinalPosition = foundDate.end()

    def _constructReturnDict(self):
        return {"day": self.day,"month": self.month,
                "year": self.year, "cursorLocation": self.matchFinalPosition}

    def getFinalMatchPosition(self):
        return self.matchFinalPosition