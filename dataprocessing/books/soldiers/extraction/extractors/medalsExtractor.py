# -*- coding: utf-8 -*-
from books.soldiers.extraction.extractors.baseExtractor import BaseExtractor
import books.soldiers.extraction.extractors.regexUtils as regexUtils
from books.soldiers.extractionkeys import KEYS
from interface.valuewrapper import ValueWrapper


class MedalsExtractor(BaseExtractor):

    RVA_PATTERN = r'(?P<rva>\bRva|\brva)'
    VAPAUDEN_MITALI_PATTERN = r'(?P<mitali>Vm ?1|Vm ?2)'
    VAPAUDEN_RISTI_PATTERN = r'(?P<mitali>VR ?suur|VR ?[1-4](?: [a-zä-ö ]{1,})?|VR ?surur)'
    SUOMEN_VAPAUDEN_RISTI_PATTERN = r'(?P<mitali>SVR ?suur|SVR ?[A-Za-zä-ö1-2 ]{1,})'

    medals = ""
    rvaPosition = -1    #Position of the possible rva key-word which might indicate that medal is for her.

    def extract(self, text):
        self.rvaPosition = regexUtils.findFirstPositionWithRegexSearch(self.RVA_PATTERN, text)
        self._extractMedal(self.VAPAUDEN_MITALI_PATTERN, text)
        self._extractMedal(self.VAPAUDEN_RISTI_PATTERN, text)
        self._extractMedal(self.SUOMEN_VAPAUDEN_RISTI_PATTERN, text)
        return self._constructReturnDict()

    def _extractMedal(self, pattern, text):
        foundMedals = regexUtils.regexIter(pattern, text)
        for medal in foundMedals:
            if self._checkIsTheMedalForMan(medal):
                self._addMedal(medal)


    def _checkIsTheMedalForMan(self, medalMatch):
        medalIsForMan = True
        if self.rvaPosition != -1:
            if medalMatch.start() > self.rvaPosition:
                medalIsForMan = False
                self._saveFinalMatchPosition(medalMatch)
        return medalIsForMan

    def _saveFinalMatchPosition(self, medalMatch):
        if medalMatch.end() > self.matchFinalPosition:
         self.matchFinalPosition = medalMatch.end()

    def _addMedal(self, medal):
        self.medals += medal.group("mitali") +","

    def _constructReturnDict(self):
        return {KEYS["medals"] :  ValueWrapper(self.medals)}

