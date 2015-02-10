# -*- coding: utf-8 -*-
import re
import regex
from baseExtractor import BaseExtractor
import regexUtils
from extraction.extractionExceptions import *
from extraction.extractors.regimentExtractor import RegimentsExtractor


class WarExtractor(BaseExtractor):
    JATKOSOTA_PATTERN = ur'(?P<jsExists>(?:Js:|JS:|js:|jS:))'
    JATKOSOTA_OPTIONS = re.UNICODE
    TALVISOTA_PATTERN = ur'(?P<tsExists>(?:Ts:|TS:|ts:|tS:))'
    TALVISOTA_OPTIONS = re.UNICODE
    wereInJatkosota = False
    wereInTalvisota = False
    jatkosotaRegiments = ""
    talvisotaRegiments = ""
    regimentExtractor = None

    def extract(self, text):
        self.regimentExtractor = RegimentsExtractor(self.currentChild, self.errorLogger)
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
            self.jatkosotaRegiments = self.regimentExtractor.extract(text[foundJatkosotaMarkers[0].end():])["regiments"]

    def _extractTalvisota(self, text):
        foundTalvisotaMarkers = regexUtils.regexIter(self.TALVISOTA_PATTERN, text, self.TALVISOTA_OPTIONS)
        foundTalvisotaMarkers = tuple(foundTalvisotaMarkers)
        if len(foundTalvisotaMarkers) > 0:
            self.wereInTalvisota = True
            self.talvisotaRegiments = self.regimentExtractor.extract(text[foundTalvisotaMarkers[0].end():])["regiments"]

    def _constructReturnDict(self):
        return {"talvisota": self.wereInTalvisota, "talvisotaregiments": self.talvisotaRegiments,
                "jatkosotaregiments" : self.jatkosotaRegiments, "jatkosota" : self.wereInJatkosota}