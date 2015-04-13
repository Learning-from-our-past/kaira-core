# -*- coding: utf-8 -*-
import re

from books.soldiers.extraction.extractors.baseExtractor import BaseExtractor
from books.soldiers.extraction.extractionExceptions import *
from shared import regexUtils, textUtils
from books.soldiers.extractionkeys import KEYS
from interface.valuewrapper import ValueWrapper


class ProfessionExtractor(BaseExtractor):
    PATTERN = r'^ ?(?:,|\.| )(?P<profession>[A-ZÄ-Öa-zä-ö !-]+?)(?:\.|,|Pso)'
    OPTIONS = (re.UNICODE | re.IGNORECASE)
    REQUIRES_MATCH_POSITION = True
    profession = ""

    def extract(self, text):
        super(ProfessionExtractor, self).extract(text)
        text = self._prepareTextForExtraction(text)
        self._findProfession(text)
        return self._constructReturnDict()

    def _prepareTextForExtraction(self, text):
        t = textUtils.takeSubStrBasedOnPos(text, self.matchStartPosition)
        return t

    def _findProfession(self, text):
        try:
            foundProfession= regexUtils.safeSearch(self.PATTERN, text, self.OPTIONS)
            self.profession = foundProfession.group("profession")
            self.matchFinalPosition = foundProfession.end()
        except regexUtils.RegexNoneMatchException as e:
            self.errorLogger.logError(ProfessionException.eType, self.currentChild )


    def _constructReturnDict(self):
        return {KEYS["profession"]:  ValueWrapper(self.profession)}