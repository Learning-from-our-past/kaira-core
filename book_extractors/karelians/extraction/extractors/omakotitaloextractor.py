from book_extractors.common.base_extractor import BaseExtractor
from book_extractors.common.extraction_keys import KEYS
import shared.regexUtils as regexUtils
import re


class OmakotitaloExtractor(BaseExtractor):

    def __init__(self, options):
        super(OmakotitaloExtractor, self).__init__(options)
        self.OMAKOTITALO_PATTERN = r"(?P<omakotitalo>omakotitalo)"
        self.OMAKOTITALO_OPTIONS = (re.UNICODE | re.IGNORECASE)

    def extract(self, entry, start_position=0):
        own_house = self._find_omakotitalo(entry['text'])
        return self._constructReturnDict({KEYS["omakotitalo"]: own_house})

    def _find_omakotitalo(self, text):
        try:
            regexUtils.safeSearch(self.OMAKOTITALO_PATTERN, text, self.OMAKOTITALO_OPTIONS)
            return True
        except regexUtils.RegexNoneMatchException as e:
            pass

        return False
