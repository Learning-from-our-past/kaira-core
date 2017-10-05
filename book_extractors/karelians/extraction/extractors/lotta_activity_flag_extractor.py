from book_extractors.common.extractors.base_extractor import BaseExtractor
from shared.textUtils import remove_hyphens_from_text
import regex


class LottaActivityFlagExtractor(BaseExtractor):
    extraction_key = 'lottaActivityFlag'

    def __init__(self, key_of_cursor_location_dependent, options):
        super(LottaActivityFlagExtractor, self).__init__(key_of_cursor_location_dependent, options)
        self.OPTIONS = regex.UNICODE
        self.LOTTA_ACTIVITY_PATTERN = r'(?:(?<=l)otta|(L|l)otta(?=\s(S|s)värd)){s<=1}'
        self.REGEX_LOTTA_ACTIVITY = regex.compile(self.LOTTA_ACTIVITY_PATTERN, self.OPTIONS)

    def _extract(self, entry, extraction_results, extraction_metadata):
        lotta_activity = self._check_lotta_activity(entry['text'])

        return self._add_to_extraction_results(lotta_activity, extraction_results, extraction_metadata)

    def _check_lotta_activity(self, text):
        text = remove_hyphens_from_text(text)
        lotta = regex.search(self.REGEX_LOTTA_ACTIVITY, text)
        return lotta is not None
