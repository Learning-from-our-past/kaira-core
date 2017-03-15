import re

import shared.regexUtils as regexUtils
from book_extractors.common.extraction_keys import KEYS
from book_extractors.common.extractors.base_extractor import BaseExtractor


class OmakotitaloExtractor(BaseExtractor):

    def __init__(self, key_of_cursor_location_dependent, options):
        super(OmakotitaloExtractor, self).__init__(key_of_cursor_location_dependent, options)
        self.OMAKOTITALO_PATTERN = r"(?P<omakotitalo>omakotitalo)"
        self.OMAKOTITALO_OPTIONS = (re.UNICODE | re.IGNORECASE)

    def extract(self, entry, extraction_results):
        own_house = self._find_omakotitalo(entry['text'])
        return self._constructReturnDict({KEYS["omakotitalo"]: own_house}, extraction_results)

    def _find_omakotitalo(self, text):
        try:
            regexUtils.safeSearch(self.OMAKOTITALO_PATTERN, text, self.OMAKOTITALO_OPTIONS)
            return True
        except regexUtils.RegexNoneMatchException:
            pass

        return False
