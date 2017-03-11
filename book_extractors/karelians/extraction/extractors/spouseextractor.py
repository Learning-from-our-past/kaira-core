# -*- coding: utf-8 -*-
import re
from book_extractors.common.base_extractor import BaseExtractor
from book_extractors.extraction_exceptions import *
from book_extractors.common.extraction_keys import KEYS
from shared import regexUtils
from book_extractors.karelians.extraction.extractors.professionextractor import ProfessionExtractor
from book_extractors.karelians.extraction.extractors.birthdayExtractor import BirthdayExtractor
from book_extractors.karelians.extraction.extractors.locationExtractor import BirthdayLocationExtractor
from book_extractors.karelians.extraction.extractors.origfamilyextractor import OrigFamilyExtractor
from book_extractors.karelians.extraction.extractors.deathextractor import DeathExtractor
from book_extractors.karelians.extraction.extractors.weddingextractor import WeddingExtractor
from book_extractors.extraction_pipeline import ExtractionPipeline, configure_extractor


class SpouseExtractor(BaseExtractor):

    def extract(self, entry, start_position=0):

        self.matchStartPosition = start_position  # TODO: Remove once this class is stateless

        self._sub_extraction_pipeline = ExtractionPipeline([
            configure_extractor(OrigFamilyExtractor),
            configure_extractor(ProfessionExtractor, depends_on_match_position_of_extractor=OrigFamilyExtractor),
            configure_extractor(BirthdayExtractor),
            configure_extractor(BirthdayLocationExtractor, depends_on_match_position_of_extractor=BirthdayExtractor),
            configure_extractor(DeathExtractor, depends_on_match_position_of_extractor=BirthdayLocationExtractor),
            configure_extractor(WeddingExtractor, depends_on_match_position_of_extractor=BirthdayLocationExtractor)
        ])

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
        self.profession = ""
        self.birthday = {KEYS["birthDay"]:  "", KEYS["birthMonth"]:  "",
                KEYS["birthYear"]:  "", KEYS["birthLocation"]:  ""}
        self.origFamily = ""

        self.initVars(entry['text'])
        self._findSpouse(entry['text'])
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
            # TODO: Metadata logging here self.errorLogger.logError(SpouseNameException.eType, self.currentChild)
            pass

    def _findSpouseDetails(self, text):
        results = self._sub_extraction_pipeline.process({'text': text})

        self.origFamily = results[KEYS["origfamily"]]
        self.profession = results[KEYS["profession"]]
        self.spouseDeath = results[KEYS["deathYear"]]
        self.weddingYear = results[KEYS["weddingYear"]]
        self.birthday[KEYS["birthLocation"]] = results[KEYS["birthLocation"]]
        self.birthday[KEYS["birthDay"]] = results[KEYS["birthDay"]]
        self.birthday[KEYS["birthMonth"]] = results[KEYS["birthMonth"]]
        self.birthday[KEYS["birthYear"]] = results[KEYS["birthYear"]]

    def _setFinalMatchPosition(self):
        #Dirty fix for inaccuracy in positions which would screw the Location extraction
        self.matchFinalPosition = self.foundSpouse.end() + self.matchStartPosition - 4

    def _constructReturnDict(self):
        return {KEYS["spouse"]: { KEYS["hasSpouse"]:  self.hasSpouse,
                                               KEYS["weddingYear"]: self.weddingYear,
                                               KEYS["spouseName"]:  self.spouseName,
                                               KEYS["spouseOrigFamily"]: self.origFamily,
                                               KEYS["spouseProfession"]: self.profession,
                                               KEYS["spouseBirthData"]: self.birthday,
                                               KEYS["spouseDeathYear"]: self.spouseDeath}}
