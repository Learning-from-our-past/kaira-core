from book_extractors.common.extractors.base_extractor import BaseExtractor
from shared.text_utils import remove_hyphens_from_text
import regex
from book_extractors.karelians.extraction.extractors.name_extractor import NameExtractor


class InjuredInWarFlagExtractor(BaseExtractor):
    extraction_key = 'injuredInWarFlag'

    def __init__(self, cursor_location_depends_on=None, options=None):
        super(InjuredInWarFlagExtractor, self).__init__(cursor_location_depends_on, options)
        self._in_spouse_extractor = options['in_spouse_extractor']
        
        self.OPTIONS = regex.UNICODE
        self.INJURED_IN_WAR_PATTERN = r'(?:haavoi){s<=1}|(?<!S)(otainvalidi){s<=1}(?:\s|,|\.)'
        self.REGEX_INJURED_IN_WAR = regex.compile(self.INJURED_IN_WAR_PATTERN, self.OPTIONS)

        self._declare_expected_dependency_names(['person'])

    def _is_person_male(self):
        """
        This function assumes only heterosexual marriages and checks that the person, whose
        data we are looking at, is male. If we are in the spouse extractor and primary person
        is female, then the spouse is male. If we are in the primary person and person is
        male, then the person is male.
        :return: Boolean, True or False.
        """
        should_extract = False

        if self._in_spouse_extractor and self._deps['person']['name']['gender'] == 'Female':
            should_extract = True
        elif not self._in_spouse_extractor and self._deps['person']['name']['gender'] == 'Male':
            should_extract = True

        return should_extract

    def _extract(self, entry, extraction_results, extraction_metadata):
        injured_in_war = None
        if self._is_person_male():
            injured_in_war = self._check_injured_in_war(entry['full_text'])

        return self._add_to_extraction_results(injured_in_war, extraction_results, extraction_metadata)

    def _check_injured_in_war(self, text):
        text = remove_hyphens_from_text(text)
        injured = regex.search(self.REGEX_INJURED_IN_WAR, text)
        return injured is not None
