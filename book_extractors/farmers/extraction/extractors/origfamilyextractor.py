from book_extractors.farmers.extraction.extractors.baseExtractor import BaseExtractor
from book_extractors.farmers.extractionkeys import KEYS
import shared.textUtils as textUtils
import shared.regexUtils as regexUtils
import re

class OrigFamilyExtractor(BaseExtractor):
    """
    Tries to find the possible o.s. (omaa sukua) part from entry.
    """
    REQUIRES_MATCH_POSITION = True
    SEARCH_SPACE = 40

    def extract(self, text, entry):
        self.FAMILY_PATTERN = r"(((?:o|0)\.? ?s\.?,? )(?P<family>([a-zä-ö-]*)(, ent\.?,? \w*)?)(?:,|\.))|(?P<family>ent\.?,? \w*)"
        self.FAMILY_OPTIONS = (re.UNICODE | re.IGNORECASE)
        self.own_family = ""

        self._find_family(text)
        return self._constructReturnDict()

    def _find_family(self, text):
        text = textUtils.takeSubStrBasedOnPos(text, self.matchStartPosition, self.SEARCH_SPACE)
        try:
            foundFamily= regexUtils.safeSearch(self.FAMILY_PATTERN, text, self.FAMILY_OPTIONS)
            self.matchFinalPosition = foundFamily.end()
            self.own_family = foundFamily.group("family")
        except regexUtils.RegexNoneMatchException as e:
            pass

    def _constructReturnDict(self):
        return {KEYS["origfamily"] : self.own_family}


