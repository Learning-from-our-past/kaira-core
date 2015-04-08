# -*- coding: utf-8 -*-
import re

from soldiers.extraction.extractors.baseExtractor import BaseExtractor
import soldiers.extraction.extractors.regexUtils as regexUtils
from soldiers.extraction.extractionExceptions import *
from soldiers.extractionkeys import KEYS, ValueWrapper


class RankExtractor(BaseExtractor):
    RANK_PATTERN = r'(?:(?:Sotarvo){s<=1}|(?:SOIarvo){s<=1}|(?:Ylenn){s<=1})(?: |\n)(?P<rank>[A-ZÄ-Öa-zä-ö0-9, \n]{2,})(?:\.|:|,| )'
    RANK_OPTIONS = (re.UNICODE | re.IGNORECASE)
    ranks = ""

    def extract(self, text):
        self._findRanks(text)
        return self._constructReturnDict()

    def _findRanks(self, text):
        try:
            foundRanks = regexUtils.safeSearch(self.RANK_PATTERN, text, self.RANK_OPTIONS)
            self.ranks = foundRanks.group("rank")
            self.matchFinalPosition = foundRanks.end()
        except regexUtils.RegexNoneMatchException as e:
            self.errorLogger.logError(RankException.eType, self.currentChild )

    def _constructReturnDict(self):
        return {KEYS["rank"]:  ValueWrapper(self.ranks)}
