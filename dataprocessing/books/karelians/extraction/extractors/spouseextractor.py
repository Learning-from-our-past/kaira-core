# -*- coding: utf-8 -*-
import re

from books.karelians.extraction.extractors.baseExtractor import BaseExtractor
from books.karelians.extraction.extractionExceptions import *
from books.karelians.extraction.extractors.dateExtractor import DateExtractor
from shared import textUtils
from books.karelians.extractionkeys import KEYS
from interface.valuewrapper import ValueWrapper
from shared import regexUtils
from books.karelians.extraction.extractors.professionextractor import ProfessionExtractor

class SpouseExtractor(BaseExtractor):


    def extract(self, text, entry):
        super(SpouseExtractor, self).extract(text)
        self.entry = entry
        self.PATTERN = r"Puol\.?(?P<spousedata>[A-ZÄ-Öa-zä-ö\s\.,\d-]*)(?=(Lapset|poika|tytär|asuinp))"
        self.NAMEPATTERN = r"(?P<name>^[\w\s\.-]*)"
        self.OPTIONS = (re.UNICODE | re.IGNORECASE)    #TODO: TRY IGNORE CASE?
        self.REQUIRES_MATCH_POSITION = False
        self.SUBSTRING_WIDTH = 100

        self.hasSpouse = False
        self.spouseName = ""
        self.profession = {KEYS["profession"] : ValueWrapper("")}

        self.initVars(text)
        self._findSpouse(text)
        return self._constructReturnDict()

    def initVars(self,text):
        pass

    def _findSpouse(self, text):
        try:
            self.foundSpouse = regexUtils.safeSearch(self.PATTERN, text, self.OPTIONS)
            self.hasSpouse = True
            self._findSpouseName(self.foundSpouse.group("spousedata"))
            self._setFinalMatchPosition()
        except regexUtils.RegexNoneMatchException:
            pass

    def _findSpouseName(self, text):
        try:
            name = regexUtils.safeSearch(self.NAMEPATTERN, text, self.OPTIONS)
            self.spouseName = name.group("name").strip()
            self._findProfession(text[name.end():])
        except regexUtils.RegexNoneMatchException:
            self.errorLogger.logError(SpouseNameException.eType, self.currentChild)

    def _findProfession(self, text):
        professionExt = ProfessionExtractor(self.entry, self.errorLogger, self.xmlDocument)
        professionExt.setDependencyMatchPositionToZero()
        self.profession = professionExt.extract(text, self.entry)


    def _setFinalMatchPosition(self):
        #Dirty fix for inaccuracy in positions which would screw the Location extraction
        self.matchFinalPosition = self.foundSpouse.end() + self.matchStartPosition - 4

    def _constructReturnDict(self):
        print(self.profession)
        return {KEYS["spouse"]: ValueWrapper({ KEYS["hasSpouse"]:  ValueWrapper(self.hasSpouse),KEYS["spouseName"]:  ValueWrapper(self.spouseName), KEYS["spouseProfession"]: ValueWrapper(self.profession[KEYS["profession"]].value) })}
