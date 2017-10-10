from book_extractors.common.extractors.base_extractor import BaseExtractor
from shared.text_utils import remove_hyphens_from_text
import regex


class ServedDuringWarFlagExtractor(BaseExtractor):
    extraction_key = 'servedDuringWarFlag'

    def __init__(self, key_of_cursor_location_dependent, options):
        super(ServedDuringWarFlagExtractor, self).__init__(key_of_cursor_location_dependent, options)

        self.run_extractor = True
        if options is not None and 'run_extractor' in options:
            self.run_extractor = options['run_extractor']

        self.OPTIONS = regex.UNICODE
        self.SERVED_IN_WAR_PATTERN = r'(?:palvel(?!uksessa)(?:i|lut|len)){s<=1}'
        self.REGEX_SERVED_IN_WAR = regex.compile(self.SERVED_IN_WAR_PATTERN, self.OPTIONS)

    def _extract(self, entry, extraction_results, extraction_metadata):
        if self.run_extractor:
            served_during_war = self._check_served_during_war(entry['text'])
            return self._add_to_extraction_results(served_during_war, extraction_results, extraction_metadata)
        else:
            return extraction_results, extraction_metadata

    def _check_served_during_war(self, text):
        text = remove_hyphens_from_text(text)
        served = regex.search(self.REGEX_SERVED_IN_WAR, text)
        return served is not None
