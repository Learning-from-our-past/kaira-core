# -*- coding: utf-8 -*-
import re
import regex
from baseExtractor import BaseExtractor
import regexUtils, textUtils
from extraction.extractionExceptions import *


class ProfessionExtractor(BaseExtractor):
    PATTERN = ur'^ ?(?:,|\.| )(?P<profession>[A-ZÄ-Öa-zä-ö !-]+?)(?:\.|,|Pso)'
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
        return {"profession": self.profession}