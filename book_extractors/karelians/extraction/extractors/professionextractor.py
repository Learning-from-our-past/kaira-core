from book_extractors.common.base_extractor import BaseExtractor
from book_extractors.common.extraction_keys import KEYS
import shared.textUtils as textUtils
import shared.regexUtils as regexUtils
import re

class ProfessionExtractor(BaseExtractor):

    SEARCH_SPACE = 60

    def extract(self, entry, start_position=0):
        self.PROFESSION_PATTERN = r"(?<profession>[a-zä-ö,\. ]*) synt"
        self.PROFESSION_OPTIONS = (re.UNICODE | re.IGNORECASE)
        self.professions = ""

        self.matchStartPosition = start_position  # TODO: Remove once this class is stateless

        self.profession_error = False
        self._find_profession(entry['text'])
        return self._constructReturnDict()


    def _find_profession(self, text):
        text = textUtils.takeSubStrBasedOnRange(text, self.matchStartPosition, self.SEARCH_SPACE)
        try:
            #limit the search range if there is spouse keyword:
            try:
                foundSpouseWord =  regexUtils.safeSearch(r"Puol", text, self.PROFESSION_OPTIONS)
                text = textUtils.takeSubStrBasedOnRange(text, 0, foundSpouseWord.start())
            except regexUtils.RegexNoneMatchException as e:
                pass

            foundProfession= regexUtils.safeSearch(self.PROFESSION_PATTERN, text, self.PROFESSION_OPTIONS)
            self.matchFinalPosition = foundProfession.end()
            self.professions = foundProfession.group("profession")
        except regexUtils.RegexNoneMatchException as e:
            pass

    def _clean_professions(self):
        self.professions = self.professions.strip(",")
        self.professions = self.professions.strip()
        self.professions = self.professions.lstrip()

        uppercase = re.match(r"[A-ZÄ-Ö]", self.professions)
        if uppercase is not None:
            comma = self.professions.find(",")
            if comma != -1:
                self.professions = self.professions[comma:]

        self.professions = self.professions.strip(",")
        self.professions = self.professions.strip(".")
        self.professions = self.professions.strip()
        self.professions = self.professions.lstrip()
        self.professions = re.sub(r"[a-zä-ö]{1,3}(?:,|\.)\s", "", self.professions, self.PROFESSION_OPTIONS)

        if len(self.professions) < 3:
            self.professions = ""

        if self.professions == "":
            # TODO: Metadata logging here  self.errorLogger.logError(ProfessionException.eType, self.currentChild)
            pass

    def _constructReturnDict(self):
        self._clean_professions()
        p = self.professions
        return {KEYS["profession"] : p}
