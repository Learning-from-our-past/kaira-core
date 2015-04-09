# -*- coding: utf-8 -*-
import re

from books.soldiers.extraction.extractors.baseExtractor import BaseExtractor
from books.soldiers.extraction.extractors import regexUtils
from books.soldiers.extractionkeys import KEYS
from interface.valuewrapper import ValueWrapper


class HobbiesExtractor(BaseExtractor):

    HOBBIES_PATTERN = r'(?:Harr\b)(?P<hobbies>(?:.|\n)*?)(?=$|Rva|- os\b|\.)'
    HOBBIES_OPTIONS = (re.UNICODE | re.IGNORECASE)
    hobbies = ""

    def extract(self, text):
        super(HobbiesExtractor, self).extract(text)
        self._findHobbies(text)
        return self._constructReturnDict()

    def _findHobbies(self, text):
        try:
            foundHobbies= regexUtils.safeSearch(self.HOBBIES_PATTERN, text, self.HOBBIES_OPTIONS)
            self.matchFinalPosition = foundHobbies.end()
            self.hobbies = foundHobbies.group("hobbies")
        except regexUtils.RegexNoneMatchException as e:
            pass

    def _constructReturnDict(self):
        return {KEYS["hobbies"]:  ValueWrapper(self.hobbies)}
