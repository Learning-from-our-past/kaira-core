import re

import core.utils.regex_utils as regexUtils
from core.utils import text_utils
from core.pipeline_construction.base_extractor import BaseExtractor


class FormerSurnameExtractor(BaseExtractor):
    """
    Tries to find the possible o.s. (omaa sukua) part from entry.
    """

    SEARCH_SPACE = 40
    extraction_key = 'formerSurname'

    def __init__(self, cursor_location_depends_on=None, options=None):
        super(FormerSurnameExtractor, self).__init__(
            cursor_location_depends_on, options
        )
        self.FAMILY_PATTERN = (
            r'(((?:o|0)\.? ?s\.?,? )(?P<family>([a-zä-ö-]*)'
            r'(, ent\.?,? \w*)?)(?:,|\.))|'
            r'(?P<family>ent\.?,? \w*)'
        )
        self.FAMILY_OPTIONS = re.UNICODE | re.IGNORECASE

    def _extract(self, entry, extraction_results, extraction_metadata):
        start_position = self.get_starting_position(extraction_metadata)
        result = self._find_family(entry['text'], start_position)

        return self._add_to_extraction_results(
            result[0],
            extraction_results,
            extraction_metadata,
            cursor_location=result[1],
        )

    def _find_family(self, text, start_position):
        text = text_utils.take_sub_str_based_on_pos(
            text, start_position, self.SEARCH_SPACE
        )
        cursor_location = 0
        own_family = None

        try:
            found_family_match = regexUtils.safe_search(
                self.FAMILY_PATTERN, text, self.FAMILY_OPTIONS
            )
            cursor_location = found_family_match.end()
            own_family = found_family_match.group('family')
        except regexUtils.RegexNoneMatchException:
            pass

        return own_family, cursor_location
