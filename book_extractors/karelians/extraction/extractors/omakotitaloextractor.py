from book_extractors.common.base_extractor import BaseExtractor
from book_extractors.karelians.extractionkeys import KEYS
import shared.regexUtils as regexUtils
import re

class OmakotitaloExtractor(BaseExtractor):


    def extract(self, text, entry):
        self.OMAKOTITALO_PATTERN = r"(?P<omakotitalo>omakotitalo)"
        self.OMAKOTITALO_OPTIONS = (re.UNICODE | re.IGNORECASE)
        self.omakotitalo = False
        self._find_omakotitalo(text)
        return self._constructReturnDict()

    def _find_omakotitalo(self, text):
        try:
            found_house = regexUtils.safeSearch(self.OMAKOTITALO_PATTERN, text, self.OMAKOTITALO_OPTIONS)
            self.omakotitalo = True
        except regexUtils.RegexNoneMatchException as e:
            pass

    def _constructReturnDict(self):
        return {KEYS["omakotitalo"] : self.omakotitalo}
