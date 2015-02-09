# -*- coding: utf-8 -*-
import re
import regex
from baseExtractor import BaseExtractor
import regexUtils
from extraction.extractionExceptions import *


class ProfessionExtractor(BaseExtractor):
    PATTERN = ur'^ ?(?:,|\.| )(?P<profession>[A-ZÄ-Öa-zä-ö !-]+?)(?:\.|,|Pso)'
    OPTIONS = (re.UNICODE | re.IGNORECASE)
    profession = ""

    def extract(self, text):
        self._findProfession(text)
        return self._constructReturnDict()

    def _findProfession(self, text):
        try:
            foundProfession= regexUtils.safeSearch(self.PATTERN, text, self.OPTIONS)
            self.profession = foundProfession.group("profession")
        except regexUtils.RegexNoneMatchException as e:
            self.errorLogger.logError(ProfessionException.eType, self.currentChild )


    def _constructReturnDict(self):
        return {"profession": self.profession}