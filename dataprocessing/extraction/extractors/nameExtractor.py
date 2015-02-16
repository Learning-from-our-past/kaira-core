# -*- coding: utf-8 -*-
import re
import regex
from extraction.extractors.baseExtractor import BaseExtractor
import extraction.extractors.regexUtils as regexUtils
from extraction.extractionExceptions import *


class NameExtractor(BaseExtractor):
    PATTERN = r'\A(?P<surname>[A-ZÄ-Öl() -]{3,})(:?,|.) {0,100}(?P<firstnames>[A-ZÄ-Öa-zä-ö() -]{0,})(:?,|.)'
    OPTIONS = re.UNICODE
    foundNames = None

    def extract(self, text):
        self._findNames(text)
        return self._constructReturnDict()

    def _findNames(self, text):
        try:
            self.foundNames = regexUtils.safeMatch(self.PATTERN, text, self.OPTIONS)
            self.matchFinalPosition = self.foundNames.end()

        except regexUtils.RegexNoneMatchException as e:
            raise NameException(text)

    def _constructReturnDict(self):
        return {"surname": self.foundNames.group("surname"), "firstnames": self.foundNames.group("firstnames"), "cursorLocation": self.foundNames.end()}


