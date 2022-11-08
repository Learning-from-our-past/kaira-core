import re

import core.utils.regex_utils as regexUtils
from core.pipeline_construction.base_extractor import BaseExtractor


class FishingExtractor(BaseExtractor):
    extraction_key = 'fishing'

    def __init__(self, cursor_location_depends_on=None, options=None):
        super(FishingExtractor, self).__init__(cursor_location_depends_on, options)
        self.FISHING_PATTERN = (
            r'(?P<kalastus>kalastus)|(kalastamista)|(kalastaa)|(kalastaminen)'
        )
        self.FISHING_OPTIONS = re.UNICODE | re.IGNORECASE

    def _extract(self, entry, extraction_results, extraction_metadata):
        own_fishing = self._find_fishing(entry['text'])
        return self._add_to_extraction_results(
            own_fishing, extraction_results, extraction_metadata
        )

    def _find_fishing(self, text):
        try:
            regexUtils.safe_search(self.FISHING_PATTERN, text, self.FISHING_OPTIONS)
            return True
        except regexUtils.RegexNoneMatchException:
            pass
        return False
