# -*- coding: utf-8 -*-
import re
import regex
from baseExtractor import BaseExtractor
import regexUtils
from extraction.extractionExceptions import *


class RegimentsExtractor(BaseExtractor):

    REGIMENT_PATTERN = ur'(?P<regiments>(:?[A-Za-zä-öÄ-Ö0-9 \n,])+)'
    REGIMENT_OPTIONS = re.UNICODE
    regiments = ""

    def extract(self, text):
        self._findRegiments(text)
        return self._constructReturnDict()

    def _findRegiments(self, text):
        try:
            foundRegiments = regexUtils.safeSearch(self.REGIMENT_PATTERN, text, self.REGIMENT_OPTIONS)
            self.regiments = foundRegiments.group("regiments")
        except regexUtils.RegexNoneMatchException as e:
            self.errorLogger.logError(RegimentException.eType, self.currentChild )

    def _constructReturnDict(self):
        return {"regiments": self.regiments}
