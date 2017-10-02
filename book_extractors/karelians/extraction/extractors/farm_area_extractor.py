from book_extractors.common.extractors.base_extractor import BaseExtractor
import regex


class FarmAreaExtractor(BaseExtractor):
    """
    Extract the area of the farm in the data entry.
    """

    extraction_key = 'farmArea'

    def __init__(self, key_of_cursor_location_dependent, options):
        super(FarmAreaExtractor, self).__init__(key_of_cursor_location_dependent, options)
        self.OPTIONS = (regex.UNICODE | regex.IGNORECASE)
        self.PATTERN_MATCH = r'(pinta-ala){s<=1}\son\s(?P<area>\d{1,3}(?:,|\.)\d{1,2}|\d{1,3}(?!\s\d))\s?(?P<unit>ha|m|aar)'
        self.AREA_REGEX = regex.compile(self.PATTERN_MATCH, self.OPTIONS)

    def _extract(self, entry, extraction_results, extraction_metadata):
        matches = self.AREA_REGEX.search(entry['text'])
        area_in_hectares = None

        if matches:
            unit_of_area = matches.group('unit')
            if unit_of_area != 'm':
                number = float(matches.group('area').replace(',', '.'))

                if unit_of_area == 'aar':
                    area_in_hectares = number / 100
                else:
                    area_in_hectares = number

        return self._add_to_extraction_results(area_in_hectares, extraction_results, extraction_metadata)
