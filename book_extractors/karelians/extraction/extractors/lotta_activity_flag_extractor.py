from book_extractors.common.extractors.base_extractor import BaseExtractor
from book_extractors.karelians.extraction.extractors.name_extractor import NameExtractor
from shared.text_utils import remove_hyphens_from_text
import regex


class LottaActivityFlagExtractor(BaseExtractor):
    extraction_key = 'lottaActivityFlag'

    def __init__(self, key_of_cursor_location_dependent, options, dependencies_contexts=None):
        super(LottaActivityFlagExtractor, self).__init__(key_of_cursor_location_dependent, options)
        self._set_dependencies([NameExtractor], dependencies_contexts)
        self._in_spouse_extractor = options['in_spouse_extractor']

        self.OPTIONS = regex.UNICODE
        self.LOTTA_ACTIVITY_PATTERN = r'(?<=l|1|i|I|!)(?:otta){s<=1}|(?:Lotta\s(?:S|s)värd){s<=1}'
        self.REGEX_LOTTA_ACTIVITY = regex.compile(self.LOTTA_ACTIVITY_PATTERN, self.OPTIONS)

    def _is_person_female(self):
        """
        This function assumes only heterosexual marriages and checks that the person, whose
        data we are looking at, is female. If we are in the spouse extractor and primary person
        is male, then the spouse is female. If we are in the primary person and person is
        female, then the person is female.
        :return: Boolean
        """
        is_female = False

        if self._in_spouse_extractor and self._deps['name']['gender'] == 'Male':
            is_female = True
        elif not self._in_spouse_extractor and self._deps['name']['gender'] == 'Female':
            is_female = True

        return is_female

    def _extract(self, entry, extraction_results, extraction_metadata):
        lotta_activity = None

        if self._is_person_female():
            lotta_activity = self._check_lotta_activity(entry['text'])

        return self._add_to_extraction_results(lotta_activity, extraction_results, extraction_metadata)

    def _check_lotta_activity(self, text):
        text = remove_hyphens_from_text(text)
        lotta = regex.search(self.REGEX_LOTTA_ACTIVITY, text)
        return lotta is not None
