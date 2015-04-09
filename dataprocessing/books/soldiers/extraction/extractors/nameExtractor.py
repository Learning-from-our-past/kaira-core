# -*- coding: utf-8 -*-
import re

from books.soldiers.extraction.extractors.baseExtractor import BaseExtractor
from books.soldiers.extraction.extractionExceptions import *
from books.soldiers.extraction.extractors import regexUtils
from books.soldiers.extractionkeys import KEYS
from interface.valuewrapper import ValueWrapper


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
        return {KEYS["surname"]:  ValueWrapper(self.foundNames.group("surname")),
                KEYS["firstnames"]:  ValueWrapper(self.foundNames.group("firstnames")), "cursorLocation": self.foundNames.end()}


