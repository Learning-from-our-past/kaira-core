import re

import core.utils.regex_utils as regexUtils
from core.pipeline_construction.base_extractor import BaseExtractor


class ForestExtractor(BaseExtractor):
    extraction_key = 'metsää'

    def __init__(self, cursor_location_depends_on=None, options=None):
        super(ForestExtractor, self).__init__(cursor_location_depends_on, options)
        self.FOREST_PATTERN = (
            r'(?:([0-9][0-9]) ha metsää){s<=1}|'
            r'(?<!H)(a metsää){s<=1}|'
            r'(metsää [0-9][0-9] ha){s<=1}'
        )
        self.FOREST_OPTIONS = re.UNICODE | re.IGNORECASE

    def _extract(self, entry, extraction_results, extraction_metadata):
        own_forest = self._find_forest(entry['text'])
        return self._add_to_extraction_results(
            own_forest, extraction_results, extraction_metadata
        )

    def _find_forest(self, text):
        try:
            regexUtils.safe_search(self.FOREST_PATTERN, text, self.FOREST_OPTIONS)
            return True
        except regexUtils.RegexNoneMatchException:
            pass
        return False
