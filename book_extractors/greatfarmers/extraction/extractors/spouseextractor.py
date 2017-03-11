# -*- coding: utf-8 -*-
import re
from book_extractors.common.base_extractor import BaseExtractor
from book_extractors.extraction_pipeline import ExtractionPipeline, configure_extractor
from book_extractors.common.extraction_keys import KEYS
from shared import regexUtils
from book_extractors.greatfarmers.extraction.extractors.birthdayExtractor import BirthdayExtractor
from book_extractors.greatfarmers.extraction.extractors.origfamilyextractor import OrigFamilyExtractor


class SpouseExtractor(BaseExtractor):

    def extract(self, entry, start_position=0):
        self.matchStartPosition = start_position  # TODO: Remove once this class is stateless

        self._sub_extraction_pipeline = ExtractionPipeline([
            configure_extractor(OrigFamilyExtractor),
            configure_extractor(BirthdayExtractor)
        ])

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
        self.origFamily = ""

        self._findSpouse(entry['text'])
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
        results = self._sub_extraction_pipeline.process({'text': text})

        self.origFamily = results[KEYS['origfamily']]
        self.birthday = {KEYS["birthDay"]: results[KEYS['birthDay']],
                         KEYS["birthMonth"]:  results[KEYS['birthMonth']],
                         KEYS["birthYear"]:  results[KEYS["birthYear"]]}

    def _setFinalMatchPosition(self):
        #Dirty fix for inaccuracy in positions which would screw the Location extraction
        self.matchFinalPosition = self.foundSpouse.end() + self.matchStartPosition - 4

    def _constructReturnDict(self):
        return {KEYS["spouse"]: { KEYS["hasSpouse"]:  self.hasSpouse,
                                               KEYS["spouseName"]:  self.spouseName,
                                               KEYS["spouseOrigFamily"]: self.origFamily,
                                               KEYS["spouseBirthData"]: self.birthday}}
