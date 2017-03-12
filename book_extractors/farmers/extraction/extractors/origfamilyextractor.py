from book_extractors.common.base_extractor import BaseExtractor
from book_extractors.common.extraction_keys import KEYS
import shared.textUtils as textUtils
import shared.regexUtils as regexUtils
import re


class OrigFamilyExtractor(BaseExtractor):
    """
    Tries to find the possible o.s. (omaa sukua) part from entry.
    """

    def __init__(self, options):
        super(OrigFamilyExtractor, self).__init__(options)
        self.REQUIRES_MATCH_POSITION = True
        self.SEARCH_SPACE = 40
        self.FAMILY_PATTERN = r"(((?:o|0)\.? ?s\.?,? )(?P<family>([a-zä-ö-]*)(, ent\.?,? \w*)?)(?:,|\.))|(?P<family>ent\.?,? \w*)"
        self.FAMILY_OPTIONS = (re.UNICODE | re.IGNORECASE)

    def extract(self, entry, start_position=0):
        result = self._find_family(entry['text'], start_position)
        return self._constructReturnDict({KEYS["origfamily"]: result[0]}, result[1])

    def _find_family(self, text, start_position):
        cursor_location = start_position
        text = textUtils.takeSubStrBasedOnPos(text, start_position, self.SEARCH_SPACE)
        family = ''
        try:
            found_family_match = regexUtils.safeSearch(self.FAMILY_PATTERN, text, self.FAMILY_OPTIONS)
            cursor_location = found_family_match.end()
            family = found_family_match.group("family")
        except regexUtils.RegexNoneMatchException as e:
            pass

        return family, cursor_location
