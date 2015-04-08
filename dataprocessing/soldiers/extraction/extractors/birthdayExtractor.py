# -*- coding: utf-8 -*-
import re

from soldiers.extraction.extractors.baseExtractor import BaseExtractor
import soldiers.extraction.extractors.textUtils as textUtils
from soldiers.extraction.extractionExceptions import *
from soldiers.extraction.extractors.dateExtractor import DateExtractor
from soldiers.extractionkeys import KEYS, ValueWrapper


class BirthdayExtractor(BaseExtractor):
    PATTERN = r'.*?(?:s|S|5|synt|Synt)\.?(?:(?:(?P<day>\d{1,2})(?:\.|,|:|s)(?P<month>\d{1,2})(?:\.|,|:|s)(?P<year>\d{2,4}))|(?P<yearOnly>\d{2,4})(?!\.|,|\d)(?=\D\D\D\D\D))'
    OPTIONS = re.UNICODE    #TODO: TRY IGNORE CASE?
    REQUIRES_MATCH_POSITION = True
    SUBSTRING_WIDTH = 24
    dateExtractor = None
    foundDate = {}
    preparedText = ""

    def extract(self, text):
        super(BirthdayExtractor, self).extract(text)
        self.initVars(text)
        self._findDate(self.preparedText)
        return self._constructReturnDict()

    def initVars(self,text):
        self.dateExtractor = DateExtractor()
        self.preparedText = self._prepareTextForExtraction(text)

    def _prepareTextForExtraction(self, text):
        t = textUtils.takeSubStrBasedOnPos(text, self.matchStartPosition, self.SUBSTRING_WIDTH)
        t = textUtils.removeSpacesFromText(t)
        return t

    def _findDate(self, text):
        try:
            self.foundDate = self.dateExtractor.extract(text, self.PATTERN, self.OPTIONS)
            self._setFinalMatchPosition()
        except DateException as e:
            raise BirthdayException(text)

    def _setFinalMatchPosition(self):
        #Dirty fix for inaccuracy in positions which would screw the Location extraction
        self.matchFinalPosition = self.dateExtractor.getFinalMatchPosition() + self.matchStartPosition - 4

    def _constructReturnDict(self):
        return {KEYS["birthDay"]:  ValueWrapper(self.foundDate["day"]), KEYS["birthMonth"]:  ValueWrapper(self.foundDate["month"]),
                KEYS["birthYear"]:  ValueWrapper(self.foundDate["year"]), KEYS["cursorLocation"]:  ValueWrapper(self.matchFinalPosition)}
