from book_extractors.common.extraction_keys import KEYS
from book_extractors.common.extractors.base_extractor import BaseExtractor
import re;

class FarmAreaExtractor(BaseExtractor):
    """
    Extract the area of the farm in the data entry.
    """

    extraction_key = 'farmArea'

    def __init__(self, key_of_cursor_location_dependent, options):
        super(FarmAreaExtractor, self).__init__(key_of_cursor_location_dependent, options)
        self.OPTIONS = (re.UNICODE | re.IGNORECASE)
        self.PATTERN_MATCH = r'pinta-ala\son\s(?P<area>\d{1,3}(?:,|\.)\d{1,2}|\d{1,3})'
        self.AREA_REGEX = re.compile(self.PATTERN_MATCH, self.OPTIONS)

    def _extract(self, entry, extraction_results, extraction_metadata):
        matches = self.AREA_REGEX.search(entry['text'])
        area_float = None

        if matches:
            area_float = float(matches.group('area').replace(',', '.'))

        return self._add_to_extraction_results(area_float, extraction_results, extraction_metadata)
