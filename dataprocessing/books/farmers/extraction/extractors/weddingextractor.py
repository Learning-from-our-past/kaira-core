# -*- coding: utf-8 -*-
import re

from books.farmers.extraction.extractors.baseExtractor import BaseExtractor
from books.farmers.extraction.extractionExceptions import *
from books.farmers.extraction.extractors.dateExtractor import DateExtractor
from shared import textUtils
from books.farmers.extractionkeys import KEYS
from interface.valuewrapper import ValueWrapper
from shared import regexUtils

class WeddingExtractor(BaseExtractor):


    def extract(self, text, entry):
        super(WeddingExtractor, self).extract(text)
        self.PATTERN = r"(?:avioit)\.?\s?-(?P<year>\d{2,4})"
        self.OPTIONS = (re.UNICODE | re.IGNORECASE)
        self.REQUIRES_MATCH_POSITION = True
        self.SUBSTRING_WIDTH = 100

        self.weddingYear = ""
        self.preparedText = ""
        self.initVars(text)
        self._findDate(self.preparedText)
        return self._constructReturnDict()

    def initVars(self,text):
        self.preparedText = self._prepareTextForExtraction(text)

    def _prepareTextForExtraction(self, text):
        t = textUtils.takeSubStrBasedOnPos(text, self.matchStartPosition, self.SUBSTRING_WIDTH)
        t = textUtils.removeSpacesFromText(t)
        return t

    def _findDate(self, text):
        try:
            wedding = regexUtils.safeSearch(self.PATTERN, text, self.OPTIONS)
            self._setFinalMatchPosition(wedding.end())
            self.weddingYear = "19" + wedding.group("year")
        except regexUtils.RegexNoneMatchException as e:
            self.weddingYear = ""

    def _setFinalMatchPosition(self, end):
        #Dirty fix for inaccuracy in positions which would screw the Location extraction
        self.matchFinalPosition = end + self.matchStartPosition - 4

    def _constructReturnDict(self):
        return {KEYS["weddingYear"]:  ValueWrapper(self.weddingYear)}
