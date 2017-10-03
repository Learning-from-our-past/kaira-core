import re

import shared.regexUtils as regexUtils
import shared.textUtils as textUtils
from book_extractors.common.extraction_keys import KEYS
from book_extractors.common.extractors.base_extractor import BaseExtractor


class FormerSurnameExtractor(BaseExtractor):
    """
    Tries to find the possible o.s. (omaa sukua) part from entry.
    """
    REQUIRES_MATCH_POSITION = True
    SEARCH_SPACE = 40
    extraction_key = 'formerSurname'
    
    def __init__(self, key_of_cursor_location_dependent, options):
        super(FormerSurnameExtractor, self).__init__(key_of_cursor_location_dependent, options)
        self.FAMILY_PATTERN = r"(((?:o|0)\.? ?s\.?,? )(?P<family>([a-zä-ö-]*)(, ent\.?,? \w*)?)(?:,|\.))|(?P<family>ent\.?,? \w*)"
        self.FAMILY_OPTIONS = (re.UNICODE | re.IGNORECASE)

    def _extract(self, entry, extraction_results, extraction_metadata):
        start_position = self.get_starting_position(extraction_results, extraction_metadata)
        result = self._find_family(entry['text'], start_position)

        return self._add_to_extraction_results(result[0], extraction_results, extraction_metadata, cursor_location=result[1])

    def _find_family(self, text, start_position):
        text = textUtils.take_sub_str_based_on_pos(text, start_position, self.SEARCH_SPACE)
        cursor_location = 0
        own_family = None

        try:
            found_family_match = regexUtils.safe_search(self.FAMILY_PATTERN, text, self.FAMILY_OPTIONS)
            cursor_location = found_family_match.end()
            own_family = found_family_match.group("family")
        except regexUtils.RegexNoneMatchException as e:
            pass

        return own_family, cursor_location
