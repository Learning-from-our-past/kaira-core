# -*- coding: utf-8 -*-
import re

from books.soldiers.extraction.extractors.baseExtractor import BaseExtractor
from books.soldiers.extraction.extractors.regimentExtractor import RegimentsExtractor
from shared import regexUtils
from books.soldiers.extractionkeys import KEYS
from interface.valuewrapper import ValueWrapper


class WarExtractor(BaseExtractor):


    def extract(self, text):
        self.JATKOSOTA_PATTERN = r'(?P<jsExists>(?:Js:|JS:|js:|jS:))'
        self.JATKOSOTA_OPTIONS = re.UNICODE
        self.TALVISOTA_PATTERN = r'(?P<tsExists>(?:Ts:|TS:|ts:|tS:))'
        self.TALVISOTA_OPTIONS = re.UNICODE
        self.wereInJatkosota = False
        self.wereInTalvisota = False
        self.jatkosotaRegiments = ""
        self.talvisotaRegiments = ""
        self.regimentExtractor = None
        self.regimentExtractor = RegimentsExtractor(self.currentChild, self.errorLogger, self.xmlDocument)
        self._findWars(text)
        return self._constructReturnDict()

    def _findWars(self, text):
        self._extractJatkosota(text)
        self._extractTalvisota(text)

    def _extractJatkosota(self, text):
        foundJatkosotaMarkers = regexUtils.regexIter(self.JATKOSOTA_PATTERN, text, self.JATKOSOTA_OPTIONS)
        foundJatkosotaMarkers = tuple(foundJatkosotaMarkers)
        if len(foundJatkosotaMarkers) > 0:
            self.wereInJatkosota = True
            self.jatkosotaRegiments = self.regimentExtractor.extract(text[foundJatkosotaMarkers[0].end():])[KEYS["regiments"]]

    def _extractTalvisota(self, text):
        foundTalvisotaMarkers = regexUtils.regexIter(self.TALVISOTA_PATTERN, text, self.TALVISOTA_OPTIONS)
        foundTalvisotaMarkers = tuple(foundTalvisotaMarkers)
        if len(foundTalvisotaMarkers) > 0:
            self.wereInTalvisota = True
            self.talvisotaRegiments = self.regimentExtractor.extract(text[foundTalvisotaMarkers[0].end():])[KEYS["regiments"]]


    def _constructReturnDict(self):
        return {KEYS["talvisota"]:  ValueWrapper(self.wereInTalvisota), KEYS["talvisotaregiments"]:  ValueWrapper(self.talvisotaRegiments),
                KEYS["jatkosotaregiments"] :  ValueWrapper(self.jatkosotaRegiments), KEYS["jatkosota"] :  ValueWrapper(self.wereInJatkosota)}