# -*- coding: utf-8 -*-
import re
import regex
from baseExtractor import BaseExtractor
import regexUtils
from extraction.extractionExceptions import *


class HobbiesExtractor(BaseExtractor):

    HOBBIES_PATTERN = ur'(?:Harr\b)(?P<hobbies>(?:.|\n)*?)(?=$|Rva|- os\b|\.)'
    HOBBIES_OPTIONS = (re.UNICODE | re.IGNORECASE)
    hobbies = ""

    def extract(self, text):
        self._findHobbies(text)
        return self._constructReturnDict()

    def _findHobbies(self, text):
        try:
            foundHobbies= regexUtils.safeSearch(self.HOBBIES_PATTERN, text, self.HOBBIES_OPTIONS)
            self.hobbies = foundHobbies.group("hobbies")
        except regexUtils.RegexNoneMatchException as e:
            pass

    def _constructReturnDict(self):
        return {"hobbies": self.hobbies}
