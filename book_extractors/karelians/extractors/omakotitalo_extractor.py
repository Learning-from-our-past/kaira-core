import re

import utils.regexUtils as regexUtils
from book_extractors.common.extraction_keys import KEYS
from book_extractors.common.extractors.base_extractor import BaseExtractor


class OmakotitaloExtractor(BaseExtractor):
    extraction_key = 'ownHouse'

    def __init__(self, cursor_location_depends_on=None, options=None):
        super(OmakotitaloExtractor, self).__init__(cursor_location_depends_on, options)
        self.OMAKOTITALO_PATTERN = r"(?P<omakotitalo>omakotitalo)"
        self.OMAKOTITALO_OPTIONS = (re.UNICODE | re.IGNORECASE)

    def _extract(self, entry, extraction_results, extraction_metadata):
        own_house = self._find_omakotitalo(entry['text'])
        return self._add_to_extraction_results(own_house, extraction_results, extraction_metadata)

    def _find_omakotitalo(self, text):
        try:
            regexUtils.safe_search(self.OMAKOTITALO_PATTERN, text, self.OMAKOTITALO_OPTIONS)
            return True
        except regexUtils.RegexNoneMatchException:
            pass

        return False
