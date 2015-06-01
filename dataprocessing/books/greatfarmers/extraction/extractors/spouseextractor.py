# -*- coding: utf-8 -*-
import re
from books.greatfarmers.extraction.extractors.baseExtractor import BaseExtractor
from books.greatfarmers.extraction.extractionExceptions import *
from books.greatfarmers.extraction.extractors.dateExtractor import DateExtractor
from shared import textUtils
from books.greatfarmers.extractionkeys import KEYS
from interface.valuewrapper import ValueWrapper
from shared import regexUtils
from books.greatfarmers.extraction.extractors.birthdayExtractor import BirthdayExtractor
from books.greatfarmers.extraction.extractors.origfamilyextractor import OrigFamilyExtractor

class SpouseExtractor(BaseExtractor):


    def extract(self, text, entry):
        super(SpouseExtractor, self).extract(text)
        self.entry = entry
        self.PATTERN = r"vmo\.?(?P<spousedata>[A-ZÄ-Öa-zä-ö\s\.,\d-]*)(?=(Lapset|poika|tytär|asuinp))"
        self.NAMEPATTERN = r"(?P<name>^[\w\s-]*)"
        self.OPTIONS = (re.UNICODE | re.IGNORECASE)    #TODO: TRY IGNORE CASE?
        self.REQUIRES_MATCH_POSITION = False
        self.SUBSTRING_WIDTH = 100

        self.hasSpouse = False
        self.spouseName = ValueWrapper("")
        self.birthday = {KEYS["birthDay"]:  ValueWrapper(""), KEYS["birthMonth"]:  ValueWrapper(""),
                KEYS["birthYear"]:  ValueWrapper(""), KEYS["birthLocation"]:  ValueWrapper("")}
        self.origFamily = {KEYS["origfamily"] : ValueWrapper("")}

        self._findSpouse(text)
        return self._constructReturnDict()

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
            self.spouseName.value = name.group("name").strip()
            self.spouseName.value = re.sub(r"\so$","", self.spouseName.value)
            self._findSpouseDetails(text[name.end()-2:])
        except regexUtils.RegexNoneMatchException:
            self.errorLogger.logError(SpouseNameException.eType, self.currentChild)
            self.spouseName.error = SpouseNameException.eType

    def _findSpouseDetails(self, text):
        origFamilyExt = OrigFamilyExtractor(self.entry, self.errorLogger, self.xmlDocument)
        origFamilyExt.setDependencyMatchPositionToZero()
        self.origFamily = origFamilyExt.extract(text, self.entry)

        birthdayExt = BirthdayExtractor(self.entry, self.errorLogger, self.xmlDocument)
        birthdayExt.setDependencyMatchPositionToZero()
        self.birthday = birthdayExt.extract(text, self.entry)

    def _setFinalMatchPosition(self):
        #Dirty fix for inaccuracy in positions which would screw the Location extraction
        self.matchFinalPosition = self.foundSpouse.end() + self.matchStartPosition - 4

    def _constructReturnDict(self):
        return {KEYS["spouse"]: ValueWrapper({ KEYS["hasSpouse"]:  ValueWrapper(self.hasSpouse),
                                               KEYS["spouseName"]:  self.spouseName,
                                               KEYS["spouseOrigFamily"]: ValueWrapper(self.origFamily[KEYS["origfamily"]].value),
                                               KEYS["spouseBirthData"]: ValueWrapper(self.birthday)})}
