# -*- coding: utf-8 -*-
import re
import regex
from baseExtractor import BaseExtractor
import regexUtils
from extraction.extractionExceptions import *


class RankExtractor(BaseExtractor):

    RANK_PATTERN = ur'(?:(?:Sotarvo){s<=1}|(?:SOIarvo){s<=1}|(?:Ylenn){s<=1})(?: |\n)(?P<rank>[A-ZÄ-Öa-zä-ö0-9, \n]{2,})(?:\.|:|,| )'
    RANK_OPTIONS = (re.UNICODE | re.IGNORECASE)
    ranks = ""

    def extract(self, text):
        self._findRanks(text)
        return self._constructReturnDict()

    def _findRanks(self, text):
        try:
            foundRanks = regexUtils.safeSearch(self.RANK_PATTERN, text, self.RANK_OPTIONS)
            self.ranks = foundRanks.group("rank")
        except regexUtils.RegexNoneMatchException as e:
            self.errorLogger.logError(RankException.eType, self.currentChild )

    def _constructReturnDict(self):
        return {"rank": self.ranks}
