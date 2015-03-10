# -*- coding: utf-8 -*-
import re
import regex
from extraction.extractors.baseExtractor import BaseExtractor
import extraction.extractors.regexUtils as regexUtils
import extraction.extractors.textUtils as textUtils
from extraction.extractionExceptions import *
from extraction.extractors.dateExtractor import DateExtractor
from extractionkeys import KEYS
class BirthdayExtractor(BaseExtractor):
    PATTERN = r'.*?(?:s|S|5)\.?(?:(?:(?P<day>\d{1,2})(?:\.|,|:|s)(?P<month>\d{1,2})(?:\.|,|:|s)(?P<year>\d{2,4}))|(?P<yearOnly>\d{2,4})(?!\.|,|\d)(?=\D\D\D\D\D))'
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
        return {KEYS["birthDay"]: self.foundDate["day"], KEYS["birthMonth"]: self.foundDate["month"],
                KEYS["birthYear"]: self.foundDate["year"], KEYS["cursorLocation"]: self.matchFinalPosition}
