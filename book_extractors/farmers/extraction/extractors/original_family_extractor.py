import re

import shared.regexUtils as regexUtils
import shared.textUtils as textUtils
from book_extractors.common.extraction_keys import KEYS
from book_extractors.common.extractors.base_extractor import BaseExtractor


class OrigFamilyExtractor(BaseExtractor):
    extraction_key = KEYS['origfamily']
    """
    Tries to find the possible o.s. (omaa sukua) part from entry.
    """

    def __init__(self, key_of_cursor_location_dependent, options):
        super(OrigFamilyExtractor, self).__init__(key_of_cursor_location_dependent, options)
        self.REQUIRES_MATCH_POSITION = True
        self.SEARCH_SPACE = 40
        self.FAMILY_PATTERN = r"(((?:o|0)\.? ?s\.?,? )(?P<family>([a-zä-ö-]*)(, ent\.?,? \w*)?)(?:,|\.))|(?P<family>ent\.?,? \w*)"
        self.FAMILY_OPTIONS = (re.UNICODE | re.IGNORECASE)

    def _extract(self, entry, extraction_results):
        start_position = self.get_starting_position(extraction_results)
        result = self._find_family(entry['text'], start_position)
        return self._add_to_extraction_results(result[0], extraction_results, result[1])

    def _find_family(self, text, start_position):
        cursor_location = start_position
        text = textUtils.take_sub_str_based_on_pos(text, start_position, self.SEARCH_SPACE)
        family = None
        try:
            found_family_match = regexUtils.safe_search(self.FAMILY_PATTERN, text, self.FAMILY_OPTIONS)
            cursor_location = found_family_match.end()
            family = found_family_match.group("family")
        except regexUtils.RegexNoneMatchException as e:
            pass

        return family, cursor_location
