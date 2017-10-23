from book_extractors.common.extractors.base_extractor import BaseExtractor
from book_extractors.karelians.extraction.extractors.name_extractor import NameExtractor
from shared.text_utils import remove_hyphens_from_text
import regex


class ServedDuringWarFlagExtractor(BaseExtractor):
    extraction_key = 'servedDuringWarFlag'

    def __init__(self, key_of_cursor_location_dependent, options, dependencies_contexts=None):
        super(ServedDuringWarFlagExtractor, self).__init__(key_of_cursor_location_dependent, options)
        self._set_dependencies([NameExtractor], dependencies_contexts)
        self._in_spouse_extractor = options['in_spouse_extractor']

        self.OPTIONS = regex.UNICODE
        self.SERVED_IN_WAR_PATTERN = r'(?:palvel(?!uksessa)(?:i|lut|len)){s<=1}'
        self.REGEX_SERVED_IN_WAR = regex.compile(self.SERVED_IN_WAR_PATTERN, self.OPTIONS)

    def _is_person_male(self):
        """
        This function assumes only heterosexual marriages and checks that the person, whose
        data we are looking at, is male. If we are in the spouse extractor and primary person
        is female, then the spouse is male. If we are in the primary person and person is
        male, then the person is male.
        :return: Boolean, True or False.
        """
        should_extract = False

        if self._in_spouse_extractor and self._deps['name']['gender'] == 'Female':
            should_extract = True
        elif not self._in_spouse_extractor and self._deps['name']['gender'] == 'Male':
            should_extract = True

        return should_extract

    def _extract(self, entry, extraction_results, extraction_metadata):
        served_during_war = None
        if self._is_person_male():
            served_during_war = self._check_served_during_war(entry['text'])

        return self._add_to_extraction_results(served_during_war, extraction_results, extraction_metadata)

    def _check_served_during_war(self, text):
        text = remove_hyphens_from_text(text)
        served = regex.search(self.REGEX_SERVED_IN_WAR, text)
        return served is not None
