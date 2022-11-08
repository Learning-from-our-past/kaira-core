import re

import core.utils.regex_utils as regexUtils
from core.pipeline_construction.base_extractor import BaseExtractor


class ReligionExtractor(BaseExtractor):
    extraction_key = 'religion'

    def __init__(self, cursor_location_depends_on=None, options=None):
        super(ReligionExtractor, self).__init__(cursor_location_depends_on, options)
        self.RELIGION_PATTERN = r'(?P<ortodoksi>ortodoksi)'
        self.RELIGION_OPTIONS = re.UNICODE | re.IGNORECASE

    def _extract(self, entry, extraction_results, extraction_metadata):
        own_religion = self._find_religion(entry['text'])
        return self._add_to_extraction_results(
            own_religion, extraction_results, extraction_metadata
        )

    def _find_religion(self, text):
        try:
            regexUtils.safe_search(self.RELIGION_PATTERN, text, self.RELIGION_OPTIONS)
            return True
        except regexUtils.RegexNoneMatchException:
            pass
        return False
