import re

import core.utils.regex_utils as regexUtils
from core.pipeline_construction.base_extractor import BaseExtractor


class HuntingExtractor(BaseExtractor):
    extraction_key = 'hunting'

    def __init__(self, cursor_location_depends_on=None, options=None):
        super(HuntingExtractor, self).__init__(cursor_location_depends_on, options)
        self.HUNTING_PATTERN = r'(?P<metsästys>metsästys|(metsästämi))'
        self.HUNTING_OPTIONS = re.UNICODE | re.IGNORECASE

    def _extract(self, entry, extraction_results, extraction_metadata):
        own_hunting = self._find_hunting(entry['text'])
        return self._add_to_extraction_results(
            own_hunting, extraction_results, extraction_metadata
        )

    def _find_hunting(self, text):
        try:
            regexUtils.safe_search(self.HUNTING_PATTERN, text, self.HUNTING_OPTIONS)
            return True
        except regexUtils.RegexNoneMatchException:
            pass
        return False
