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
    year = ""
    month = ""
    day = ""
    processedText = ""
    dates_always_20th_century = False
    MONTH_NAME_NUMBER_MAPPING = {"syks": 9, "marrask": 11, "eiok": 8, "elok": 8, "heinäk": 7, "helmik": 2, "huhtik" : 4,
    "jouluk": 12, "kesäk": 6, "lokak": 10, "maalisk": 3, "maallsk": 3, "syysk": 9, "tammik": 1, "toukok": 5}

    def extract(self, text, PATTERN, OPTIONS):
        self.PATTERN = PATTERN
        self.OPTIONS = OPTIONS
        preparedText = self._prepareTextForExtraction(text)
        self.processedText = preparedText
        self._findDate(preparedText)
        return self._constructReturnDict()

    def setDatesToAlwaysIn20thCentury(self, boolValue):
        self.dates_always_20th_century = boolValue

    def _prepareTextForExtraction(self, text):
        t = textUtils.removeSpacesFromText(text)
        return t

    def _findDate(self, text):
        try:
            foundDate = regexUtils.safeSearch(self.PATTERN, text, self.OPTIONS)
            if self._ifWrittenMonthNamesExtractThem(foundDate) is False:
                self._getYearFromMatch(foundDate)
                self._getMonthAndDayFromMatch(foundDate)
            self._setFinalMatchPosition(foundDate)
        except regexUtils.RegexNoneMatchException as e:
            raise DateException(text)

    def _getMonthAndDayFromMatch(self, dateMatch):
        self.day = dateMatch.group("day")
        self.month = dateMatch.group("month")

    def _ifWrittenMonthNamesExtractThem(self, dateMatch):
        try:
            #year and month available
            month = dateMatch.group("monthName")
            self.month = self._mapMonthNameToNumber(month)
            self.year = dateMatch.group("monthYear")    #special capture group.
            self.year = self._transformYear(self.year)
            return True
        except (IndexError, TypeError) as e:
            return False    #there is no monthYear or monthName, so use other extraction method

    def _mapMonthNameToNumber(self, name):
        if name in self.MONTH_NAME_NUMBER_MAPPING:
            return self.MONTH_NAME_NUMBER_MAPPING[name]
        else:
            return ""

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
        if not self.dates_always_20th_century:
            if int(year) < 50:
                year = "19" + year
            elif int(year) < 1800:
                year = "18" + year
        else:
            year = "19" + year
        return year

    def _checkIsYearSensible(self):
        if int(self.year) > 2000 or  int(self.year) < 1800:
            raise DateException(self.processedText)

    def _setFinalMatchPosition(self, foundDate):
        self.matchFinalPosition = foundDate.end()

    def _constructReturnDict(self):
        return {"day": self.day,"month": self.month,
                "year": self.year, "cursorLocation": self.matchFinalPosition}

    def getFinalMatchPosition(self):
        return self.matchFinalPosition