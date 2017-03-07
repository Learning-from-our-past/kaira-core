# -*- coding: utf-8 -*-
import re
from book_extractors.common.base_extractor import BaseExtractor
from book_extractors.karelians.extraction.extractionExceptions import *
from book_extractors.karelians.extractionkeys import KEYS
from shared import regexUtils
from book_extractors.karelians.extraction.extractors.professionextractor import ProfessionExtractor
from book_extractors.karelians.extraction.extractors.birthdayExtractor import BirthdayExtractor
from book_extractors.karelians.extraction.extractors.locationExtractor import BirthdayLocationExtractor
from book_extractors.karelians.extraction.extractors.origfamilyextractor import OrigFamilyExtractor
from book_extractors.karelians.extraction.extractors.deathextractor import DeathExtractor
from book_extractors.karelians.extraction.extractors.weddingextractor import WeddingExtractor

class SpouseExtractor(BaseExtractor):

    def extract(self, text, entry):
        super(SpouseExtractor, self).extract(text, entry)
        self.entry = entry
        self.PATTERN = r"Puol\.?,?(?P<spousedata>[A-ZÄ-Öa-zä-ö\s\.,\d-]*)(?=(Lapset|poika|tytär|asuinp))"
        self.NAMEPATTERN = r"(?P<name>^[\w\s-]*)"
        self.OPTIONS = (re.UNICODE | re.IGNORECASE)    #TODO: TRY IGNORE CASE?
        self.REQUIRES_MATCH_POSITION = False
        self.SUBSTRING_WIDTH = 100

        self.hasSpouse = False
        self.spouseName = ""
        self.spouseDeath = ""
        self.weddingYear = ""
        self.profession = {KEYS["profession"] : ""}
        self.birthday = {KEYS["birthDay"]:  "", KEYS["birthMonth"]:  "",
                KEYS["birthYear"]:  "", KEYS["birthLocation"]:  ""}
        self.origFamily = {KEYS["origfamily"] : ""}

        self.initVars(text)
        self._findSpouse(text)
        return self._constructReturnDict()

    def initVars(self, text):
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
        origFamilyExt = OrigFamilyExtractor(self.entry, self.errorLogger)
        origFamilyExt.setDependencyMatchPositionToZero()
        self.origFamily = origFamilyExt.extract(text, self.entry)

        professionExt = ProfessionExtractor(self.entry, self.errorLogger)
        professionExt.dependsOnMatchPositionOf(origFamilyExt)
        self.profession = professionExt.extract(text, self.entry)

        birthdayExt = BirthdayExtractor(self.entry, self.errorLogger)
        birthdayExt.setDependencyMatchPositionToZero()
        self.birthday = birthdayExt.extract(text, self.entry)

        birthLocExt = BirthdayLocationExtractor(self.entry, self.errorLogger)
        birthLocExt.dependsOnMatchPositionOf(birthdayExt)
        birthdayLocation = birthLocExt.extract(text, self.entry)

        spouseDeathExt = DeathExtractor(self.entry, self.errorLogger)
        spouseDeathExt.dependsOnMatchPositionOf(birthLocExt)
        self.spouseDeath = spouseDeathExt.extract(text, self.entry)[KEYS["deathYear"]]

        weddingExt = WeddingExtractor(self.entry, self.errorLogger)
        weddingExt.dependsOnMatchPositionOf(birthLocExt)
        self.weddingYear = weddingExt.extract(text, self.entry)[KEYS["weddingYear"]]

        self.birthday[KEYS["birthLocation"]] = birthdayLocation[KEYS["birthLocation"]]

    def _setFinalMatchPosition(self):
        #Dirty fix for inaccuracy in positions which would screw the Location extraction
        self.matchFinalPosition = self.foundSpouse.end() + self.matchStartPosition - 4

    def _constructReturnDict(self):
        p = self.profession[KEYS["profession"]]
        return {KEYS["spouse"]: { KEYS["hasSpouse"]:  self.hasSpouse,
                                               KEYS["weddingYear"]: self.weddingYear,
                                               KEYS["spouseName"]:  self.spouseName,
                                               KEYS["spouseOrigFamily"]: self.origFamily[KEYS["origfamily"]],
                                               KEYS["spouseProfession"]: p,
                                               KEYS["spouseBirthData"]: self.birthday,
                                               KEYS["spouseDeathYear"]: self.spouseDeath}}
