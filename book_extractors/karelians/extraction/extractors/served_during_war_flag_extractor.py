from book_extractors.common.extractors.base_extractor import BaseExtractor


class ServedDuringWarFlagExtractor(BaseExtractor):
    extraction_key = 'servedDuringWarFlag'

    def __init__(self, key_of_cursor_location_dependent, options):
        super(ServedDuringWarFlagExtractor, self).__init__(key_of_cursor_location_dependent, options)

    def _extract(self, entry, extraction_results, extraction_metadata):
        served_during_war = self._check_served_during_war(entry['text'])

        return self._add_to_extraction_results(served_during_war, extraction_results, extraction_metadata)

    def _check_served_during_war(self, text):
        return None
