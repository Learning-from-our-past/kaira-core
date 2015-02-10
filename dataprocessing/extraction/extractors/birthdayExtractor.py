# -*- coding: utf-8 -*-
import re
import regex
from baseExtractor import BaseExtractor
import regexUtils
import textUtils
from extraction.extractionExceptions import *


class BirthdayExtractor(BaseExtractor):
    PATTERN = ur'.*?(?:s|S|5)\.?(?:(?:(?P<day>\d{1,2})(?:\.|,|:|s)(?P<month>\d{1,2})(?:\.|,|:|s)(?P<year>\d{2,4}))|(?P<yearOnly>\d{2,4})(?!\.|,|\d)(?=\D\D\D\D\D))'
    OPTIONS = re.UNICODE    #TODO: TRY IGNORE CASE?
    REQUIRES_MATCH_POSITION = True
    SUBSTRING_WIDTH = 18
    preparedText = ""
    year = ""
    month = ""
    day = ""

    def extract(self, text):
        super(BirthdayExtractor, self).extract(text)
        self.preparedText = self._prepareTextForExtraction(text)
        self._findDate(self.preparedText)
        return self._constructReturnDict()

    def _prepareTextForExtraction(self, text):
        t = textUtils.takeSubStrBasedOnMatchPos(text, self.matchStartPosition, self.SUBSTRING_WIDTH)
        t = textUtils.removeSpacesFromText(t)
        return t

    def _findDate(self, text):
        try:
            foundDate = regexUtils.safeMatch(self.PATTERN, text, self.OPTIONS)
            self._getYearFromMatch(foundDate)
            self._getMonthAndDayFromMatch(foundDate)
            self._setFinalMatchPosition(foundDate)
        except regexUtils.RegexNoneMatchException as e:
            raise BirthdayException(text)

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
            raise BirthdayException(self.preparedText)

    def _setFinalMatchPosition(self, foundDate):
        #Dirty fix for inaccuracy in positions which would screw the Location extraction
        self.matchFinalPosition = self.matchStartPosition + foundDate.end()-4

    def _constructReturnDict(self):
        return {"birthDay": self.day,"birthMonth": self.month,
                "birthYear": self.year, "cursorLocation": self.matchFinalPosition}
