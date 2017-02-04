# -*- coding: utf-8 -*-
import re

from books.farmers.extraction.extractors.baseExtractor import BaseExtractor
from books.farmers.extraction.extractionExceptions import *
from books.farmers.extraction.extractors.dateExtractor import DateExtractor
from shared import textUtils
from books.farmers.extractionkeys import KEYS
from interface.valuewrapper import ValueWrapper
from shared import regexUtils

class BirthdayExtractor(BaseExtractor):


    def extract(self, text, entry):
        super(BirthdayExtractor, self).extract(text)
        self.PATTERN = r"(?:synt)\.?,?(?:(?:(?P<day>\d{1,2})(?:\.|,|:|s)(?P<month>\d{1,2})(?:\.|,|:|s)?-?(?P<year>\d{2,4}))|-(?P<yearOnly>\d{2,4})(?!\.|,|\d)(?=\D\D\D\D\D))" #r'(?:synt)\.?,? ?(?:(?:(?P<day>\d{1,2})(?:\.|,|:|s)? ?(?P<month>\d{1,2})(?:\.|,|:|s)? ?-?(?P<year>\d{2,4})))'
        self.OPTIONS = (re.UNICODE | re.IGNORECASE)    #TODO: TRY IGNORE CASE?
        self.REQUIRES_MATCH_POSITION = True
        self.SUBSTRING_WIDTH = 100
        self.dateExtractor = None
        self.foundDate = {}
        self.preparedText = ""
        self.error = False
        self.initVars(text)
        self._findDate(self.preparedText)
        return self._constructReturnDict()

    def initVars(self,text):
        self.dateExtractor = DateExtractor()
        self.preparedText = self._prepareTextForExtraction(text)

    def _prepareTextForExtraction(self, text):
        t = textUtils.takeSubStrBasedOnPos(text, self.matchStartPosition, self.SUBSTRING_WIDTH)
        t = textUtils.removeSpacesFromText(t)

        spouseFound = regexUtils.findFirstPositionWithRegexSearch("puol", t, re.IGNORECASE|re.UNICODE)
        if spouseFound != -1:
            t = t[0:spouseFound]

        return t

    def _findDate(self, text):
        try:
            self.foundDate = self.dateExtractor.extract(text, self.PATTERN, self.OPTIONS)
            self._setFinalMatchPosition()
        except DateException as e:
            #TODO: Better idea to have in DateExtractor class maybe?
            self.errorLogger.logError(BirthdayException.eType, self.currentChild)
            self.error = BirthdayException.eType
            self.foundDate = {"day": "","month": "",
                "year": "", "cursorLocation": ""}

    def _setFinalMatchPosition(self):
        #Dirty fix for inaccuracy in positions which would screw the Location extraction
        self.matchFinalPosition = self.dateExtractor.getFinalMatchPosition() + self.matchStartPosition - 4

    def _constructReturnDict(self):
        self.foundDate["day"] = ValueWrapper(self.foundDate["day"])
        self.foundDate["day"].error = self.error
        self.foundDate["month"] = ValueWrapper(self.foundDate["month"])
        self.foundDate["month"].error = self.error
        self.foundDate["year"] = ValueWrapper(self.foundDate["year"])
        self.foundDate["year"].error = self.error

        return {KEYS["birthDay"]:  self.foundDate["day"], KEYS["birthMonth"]: self.foundDate["month"],
                KEYS["birthYear"]:  self.foundDate["year"]}
