import re

import utils.regexUtils as regexUtils
import utils.text_utils as text_utils
from book_extractors.common.extraction_keys import KEYS
from core.base_extractor import BaseExtractor


class FormerSurnameExtractor(BaseExtractor):
    extraction_key = KEYS['formerSurname']
    """
    Tries to find the possible o.s. (omaa sukua) part from entry.
    """

    def __init__(self, cursor_location_depends_on=None, options=None):
        super(FormerSurnameExtractor, self).__init__(cursor_location_depends_on, options)
        self.REQUIRES_MATCH_POSITION = True
        self.SEARCH_SPACE = 40
        self.FAMILY_PATTERN = r"(?:(?:o|0)\.?\s?s\.?,?\s)(?P<family>[a-zä-ö-]*)"
        self.FAMILY_OPTIONS = (re.UNICODE | re.IGNORECASE)

    def _extract(self, entry, extraction_results, extraction_metadata):
        start_position = self.get_starting_position(extraction_metadata)
        results = self._find_family(entry['text'], start_position)
        return self._add_to_extraction_results(results[0], extraction_results, extraction_metadata, results[1])

    def _find_family(self, text, start_position):
        cursor_location = start_position
        own_family = None
        text = text_utils.take_sub_str_based_on_pos(text, start_position, self.SEARCH_SPACE)
        try:
            found_family_match = regexUtils.safe_search(self.FAMILY_PATTERN, text, self.FAMILY_OPTIONS)
            cursor_location = start_position + found_family_match.end()
            own_family = found_family_match.group("family")
        except regexUtils.RegexNoneMatchException:
            pass

        return own_family, cursor_location
