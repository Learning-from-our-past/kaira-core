# -*- coding: utf-8 -*-
import re
import regex
from extraction.extractors.baseExtractor import BaseExtractor
import extraction.extractors.regexUtils as regexUtils
from extraction.extractionExceptions import *
from extractionkeys import KEYS, ValueWrapper

class RegimentsExtractor(BaseExtractor):

    def extract(self, text):
        self.REGIMENT_PATTERN = r'(?P<regiments>(:?[A-Za-zä-öÄ-Ö0-9 \n,])+)'
        self.REGIMENT_OPTIONS = re.UNICODE
        self.regiments = ""
        self._findRegiments(text)
        return self._constructReturnDict()

    def _findRegiments(self, text):
        try:
            foundRegiments = regexUtils.safeSearch(self.REGIMENT_PATTERN, text, self.REGIMENT_OPTIONS)
            self.regiments = foundRegiments.group("regiments")
            self.matchFinalPosition = foundRegiments.end()
        except regexUtils.RegexNoneMatchException as e:
            self.errorLogger.logError(RegimentException.eType, self.currentChild )

    def _constructReturnDict(self):
        return {KEYS["regiments"]:  self.regiments}


