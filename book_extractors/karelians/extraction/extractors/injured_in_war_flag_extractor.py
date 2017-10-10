from book_extractors.common.extractors.base_extractor import BaseExtractor
from shared.text_utils import remove_hyphens_from_text
import regex


class InjuredInWarFlagExtractor(BaseExtractor):
    extraction_key = 'injuredInWarFlag'

    def __init__(self, key_of_cursor_location_dependent, options):
        super(InjuredInWarFlagExtractor, self).__init__(key_of_cursor_location_dependent, options)

        self.run_extractor = True
        if options is not None and 'run_extractor' in options:
            self.run_extractor = options['run_extractor']

        self.OPTIONS = regex.UNICODE
        self.INJURED_IN_WAR_PATTERN = r'(?:haavoi){s<=1}|(?<!S)(otainvalidi){s<=1}(?:\s|,|\.)'
        self.REGEX_INJURED_IN_WAR = regex.compile(self.INJURED_IN_WAR_PATTERN, self.OPTIONS)

    def _extract(self, entry, extraction_results, extraction_metadata):
        if self.run_extractor:
            injured_in_war = self._check_injured_in_war(entry['text'])
            return self._add_to_extraction_results(injured_in_war, extraction_results, extraction_metadata)
        else:
            return extraction_results, extraction_metadata

    def _check_injured_in_war(self, text):
        text = remove_hyphens_from_text(text)
        injured = regex.search(self.REGEX_INJURED_IN_WAR, text)
        return injured is not None
