# -*- coding: utf-8 -*-
import re
from books.farmers.extraction.extractors.baseExtractor import BaseExtractor
from books.farmers.extraction.extractionExceptions import *
from books.farmers.extraction.extractors.dateExtractor import DateExtractor
from shared import textUtils
from books.farmers.extractionkeys import KEYS
from interface.valuewrapper import ValueWrapper
from shared import regexUtils
from books.farmers.extraction.extractors.professionextractor import ProfessionExtractor
from books.farmers.extraction.extractors.birthdayExtractor import BirthdayExtractor
from books.farmers.extraction.extractors.locationExtractor import BirthdayLocationExtractor
from books.farmers.extraction.extractors.origfamilyextractor import OrigFamilyExtractor
from books.farmers.extraction.extractors.deathextractor import DeathExtractor
from books.farmers.extraction.extractors.weddingextractor import WeddingExtractor

class SpouseExtractor(BaseExtractor):


    def extract(self, text, entry):
        super(SpouseExtractor, self).extract(text)
        self.entry = entry
        self.PATTERN = r"Puol\.?(?P<spousedata>[A-ZÄ-Öa-zä-ö\s\.,\d-]*)(?=(Lapset|poika|tytär|asuinp))"
        self.NAMEPATTERN = r"(?P<name>^[\w\s-]*)"
        self.OPTIONS = (re.UNICODE | re.IGNORECASE)    #TODO: TRY IGNORE CASE?
        self.REQUIRES_MATCH_POSITION = False
        self.SUBSTRING_WIDTH = 100

        self.hasSpouse = False
        self.spouseName = ""
        self.spouseDeath = ""
        self.weddingYear = ""
        self.profession = {KEYS["profession"] : ValueWrapper("")}
        self.birthday = {KEYS["birthDay"]:  ValueWrapper(""), KEYS["birthMonth"]:  ValueWrapper(""),
                KEYS["birthYear"]:  ValueWrapper(""), KEYS["birthLocation"]:  ValueWrapper("")}
        self.origFamily = {KEYS["origfamily"] : ValueWrapper("")}

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
            self.spouseName = re.sub(r"\so$","", self.spouseName)
            self._findSpouseDetails(text[name.end()-2:])
        except regexUtils.RegexNoneMatchException:
            self.errorLogger.logError(SpouseNameException.eType, self.currentChild)

    def _findSpouseDetails(self, text):
        origFamilyExt = OrigFamilyExtractor(self.entry, self.errorLogger, self.xmlDocument)
        origFamilyExt.setDependencyMatchPositionToZero()
        self.origFamily = origFamilyExt.extract(text, self.entry)


        professionExt = ProfessionExtractor(self.entry, self.errorLogger, self.xmlDocument)
        professionExt.dependsOnMatchPositionOf(origFamilyExt)
        self.profession = professionExt.extract(text, self.entry)


        birthdayExt = BirthdayExtractor(self.entry, self.errorLogger, self.xmlDocument)
        birthdayExt.setDependencyMatchPositionToZero()
        self.birthday = birthdayExt.extract(text, self.entry)

        birthLocExt = BirthdayLocationExtractor(self.entry, self.errorLogger, self.xmlDocument)
        birthLocExt.dependsOnMatchPositionOf(birthdayExt)
        birthdayLocation = birthLocExt.extract(text)

        spouseDeathExt = DeathExtractor(self.entry, self.errorLogger, self.xmlDocument)
        spouseDeathExt.dependsOnMatchPositionOf(birthLocExt)
        self.spouseDeath = spouseDeathExt.extract(text, self.entry)[KEYS["deathYear"]].value

        weddingExt = WeddingExtractor(self.entry, self.errorLogger, self.xmlDocument)
        weddingExt.dependsOnMatchPositionOf(birthLocExt)
        self.weddingYear = weddingExt.extract(text, self.entry)[KEYS["weddingYear"]].value

        self.birthday[KEYS["birthLocation"]] = birthdayLocation[KEYS["birthLocation"]]

    def _setFinalMatchPosition(self):
        #Dirty fix for inaccuracy in positions which would screw the Location extraction
        self.matchFinalPosition = self.foundSpouse.end() + self.matchStartPosition - 4

    def _constructReturnDict(self):
        print(self.profession)
        return {KEYS["spouse"]: ValueWrapper({ KEYS["hasSpouse"]:  ValueWrapper(self.hasSpouse),
                                               KEYS["weddingYear"]: ValueWrapper(self.weddingYear),
                                               KEYS["spouseName"]:  ValueWrapper(self.spouseName),
                                               KEYS["spouseOrigFamily"]: ValueWrapper(self.origFamily[KEYS["origfamily"]].value),
                                               KEYS["spouseProfession"]: ValueWrapper(self.profession[KEYS["profession"]].value),
                                               KEYS["spouseBirthData"]: ValueWrapper(self.birthday),
                                               KEYS["spouseDeathYear"]: ValueWrapper(self.spouseDeath)})}
