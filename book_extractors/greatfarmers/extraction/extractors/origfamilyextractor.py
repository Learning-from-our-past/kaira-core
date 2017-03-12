from book_extractors.common.base_extractor import BaseExtractor
from book_extractors.common.extraction_keys import KEYS
import shared.textUtils as textUtils
import shared.regexUtils as regexUtils
import re


class OrigFamilyExtractor(BaseExtractor):
    """
    Tries to find the possible o.s. (omaa sukua) part from entry.
    """

    def __init__(self, key_of_cursor_location_dependent, options):
        super(OrigFamilyExtractor, self).__init__(key_of_cursor_location_dependent, options)
        self.REQUIRES_MATCH_POSITION = True
        self.SEARCH_SPACE = 40
        self.FAMILY_PATTERN = r"(?:(?:o|0)\.?\s?s\.?,?\s)(?P<family>[a-zä-ö-]*)"
        self.FAMILY_OPTIONS = (re.UNICODE | re.IGNORECASE)

    def extract(self, entry, extraction_results):
        start_position = self.get_starting_position(extraction_results)
        results = self._find_family(entry['text'], start_position)
        return self._constructReturnDict({KEYS["origfamily"]: results[0]}, extraction_results, results[1])

    def _find_family(self, text, start_position):
        cursor_location = start_position
        own_family = ''
        text = textUtils.takeSubStrBasedOnPos(text, start_position, self.SEARCH_SPACE)
        try:
            found_family_match = regexUtils.safeSearch(self.FAMILY_PATTERN, text, self.FAMILY_OPTIONS)
            cursor_location = start_position + found_family_match.end()
            own_family = found_family_match.group("family")
        except regexUtils.RegexNoneMatchException as e:
            pass

        return own_family, cursor_location
