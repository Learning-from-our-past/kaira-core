# -*- coding: utf-8 -*-
import re
import regex
from baseExtractor import BaseExtractor
import extractUtils


class MedalsExtractor(BaseExtractor):

    RVA_PATTERN = ur'(?P<rva>\bRva|\brva)'
    VAPAUDEN_MITALI_PATTERN = ur'(?P<mitali>Vm ?1|Vm ?2)'
    VAPAUDEN_RISTI_PATTERN = ur'(?P<mitali>VR ?suur|VR ?[1-4](?: [a-zä-ö ]{1,})?|VR ?surur)'
    SUOMEN_VAPAUDEN_RISTI_PATTERN = ur'(?P<mitali>SVR ?suur|SVR ?[A-Za-zä-ö1-2 ]{1,})'

    medals = ""
    rvaPosition = -1    #Position of the possible rva key-word which might indicate that medal is for her.

    def extract(self, text):
        self.rvaPosition = extractUtils.findFirstPositionWithRegexSearch(self.RVA_PATTERN, text)
        self._extractMedal(self.VAPAUDEN_MITALI_PATTERN, text)
        self._extractMedal(self.VAPAUDEN_RISTI_PATTERN, text)
        self._extractMedal(self.SUOMEN_VAPAUDEN_RISTI_PATTERN, text)
        return self._constructReturnDict()

    def _extractMedal(self, pattern, text):
        foundMedals = extractUtils.regexIter(pattern, text)
        for medal in foundMedals:
            if self._checkIsTheMedalForMan(medal):
                self._addMedal(medal)

    def _checkIsTheMedalForMan(self, medalMatch):
        medalIsForMan = True
        if self.rvaPosition != -1:
            if medalMatch.start() > self.rvaPosition:
                medalIsForMan = False
        return medalIsForMan

    def _addMedal(self, medal):
        self.medals += medal.group("mitali") +","

    def _constructReturnDict(self):
        return {"medals" : self.medals}

