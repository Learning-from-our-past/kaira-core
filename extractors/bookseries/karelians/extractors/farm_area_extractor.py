from core.pipeline_construction.base_extractor import BaseExtractor
import regex


class FarmAreaExtractor(BaseExtractor):
    """
    Extract the area of the farm in the data entry.
    """

    extraction_key = 'farmTotalArea'

    def __init__(self, cursor_location_depends_on=None, options=None):
        super(FarmAreaExtractor, self).__init__(cursor_location_depends_on, options)
        self.OPTIONS = (regex.UNICODE | regex.IGNORECASE)
        self.PATTERN_MATCH_PINTAALA_ON = r'(pinta-ala){s<=1}\son\s(?P<area>\d{1,3}(?:,|\.)\d{1,2}|\d{1,3}(?!\s\d))\s?(?P<unit>ha|m|aar)'
        self.PATTERN_MATCH_AREA_HA_NA = r'(?P<area>(\d{1,3}(?:,|\.)\d{1,3})|(?<!\d\s)\d{1,3}(?!\s\d))(?=\sha(:n|\.n))'
        self.REGEX_PINTAALA_ON = regex.compile(self.PATTERN_MATCH_PINTAALA_ON, self.OPTIONS)
        self.REGEX_HA_NA = regex.compile(self.PATTERN_MATCH_AREA_HA_NA, self.OPTIONS)

    def _extract(self, entry, extraction_results, extraction_metadata):
        matches = self.REGEX_PINTAALA_ON.search(entry['text'])
        area_in_hectares = None

        if matches:
            unit_of_area = matches.group('unit')
            if unit_of_area != 'm':
                number = float(matches.group('area').replace(',', '.'))

                if unit_of_area == 'aar':
                    area_in_hectares = number / 100
                else:
                    area_in_hectares = number
        else:
            matches = self.REGEX_HA_NA.search(entry['text'])

            if matches:
                area_in_hectares = float(matches.group('area').replace(',', '.'))

        return self._add_to_extraction_results(area_in_hectares, extraction_results, extraction_metadata)
