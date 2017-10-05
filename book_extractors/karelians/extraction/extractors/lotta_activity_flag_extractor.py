from book_extractors.common.extractors.base_extractor import BaseExtractor


class LottaActivityFlagExtractor(BaseExtractor):
    extraction_key = 'lottaActivityFlag'

    def __init__(self, key_of_cursor_location_dependent, options):
        super(LottaActivityFlagExtractor, self).__init__(key_of_cursor_location_dependent, options)

    def _extract(self, entry, extraction_results, extraction_metadata):
        lotta_activity = self._check_lotta_activity(entry['text'])

        return self._add_to_extraction_results(lotta_activity, extraction_results, extraction_metadata)

    def _check_lotta_activity(self, text):
        return None
