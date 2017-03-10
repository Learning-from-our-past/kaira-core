# -*- coding: utf-8 -*-
import re
from book_extractors.common.base_extractor import BaseExtractor
from book_extractors.extraction_exceptions import *
from book_extractors.common.extraction_keys import KEYS
from shared import regexUtils
from book_extractors.greatfarmers.extraction.extractors.birthdayExtractor import BirthdayExtractor
from book_extractors.greatfarmers.extraction.extractors.origfamilyextractor import OrigFamilyExtractor


class SpouseExtractor(BaseExtractor):

    def extract(self, text, entry):
        super(SpouseExtractor, self).extract(text, entry)
        self.entry = entry
        self.PATTERN = r"vmo\.?(?P<spousedata>[A-ZÄ-Öa-zä-ö\s\.,\d-]*)(?=(Lapset|poika|tytär|asuinp|suvulla|tila))"
        self.NAMEPATTERN = r"(?P<name>^[\w\s-]*)"
        self.OPTIONS = (re.UNICODE | re.IGNORECASE)    #TODO: TRY IGNORE CASE?
        self.REQUIRES_MATCH_POSITION = False
        self.SUBSTRING_WIDTH = 100

        self.hasSpouse = False
        self.spouseName = ""
        self.birthday = {KEYS["birthDay"]:  "", KEYS["birthMonth"]:  "",
                KEYS["birthYear"]:  "", KEYS["birthLocation"]:  ""}
        self.origFamily = {KEYS["origfamily"] : ""}

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
            self.spouseName = name.group("name").strip()
            self.spouseName = re.sub(r"\so$","", self.spouseName)
            self._findSpouseDetails(text[name.end()-2:])
        except regexUtils.RegexNoneMatchException:
            # TODO: Metadata logging here self.errorLogger.logError(SpouseNameException.eType, self.currentChild)
            pass

    def _findSpouseDetails(self, text):
        origFamilyExt = OrigFamilyExtractor(self.entry)
        origFamilyExt.setDependencyMatchPositionToZero()
        self.origFamily = origFamilyExt.extract(text, self.entry)

        birthdayExt = BirthdayExtractor(self.entry)
        birthdayExt.setDependencyMatchPositionToZero()
        self.birthday = birthdayExt.extract(text, self.entry)

    def _setFinalMatchPosition(self):
        #Dirty fix for inaccuracy in positions which would screw the Location extraction
        self.matchFinalPosition = self.foundSpouse.end() + self.matchStartPosition - 4

    def _constructReturnDict(self):
        return {KEYS["spouse"]: { KEYS["hasSpouse"]:  self.hasSpouse,
                                               KEYS["spouseName"]:  self.spouseName,
                                               KEYS["spouseOrigFamily"]: self.origFamily[KEYS["origfamily"]],
                                               KEYS["spouseBirthData"]: self.birthday}}
