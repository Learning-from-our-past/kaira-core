from core.pipeline_construction.base_extractor import BaseExtractor
from core.utils.text_utils import remove_hyphens_from_text
import regex


class MarttaActivityFlagExtractor(BaseExtractor):
    extraction_key = 'marttaActivityFlag'

    def __init__(self, cursor_location_depends_on=None, options=None):
        super(MarttaActivityFlagExtractor, self).__init__(
            cursor_location_depends_on, options
        )
        self._declare_expected_dependency_names(['person'])
        self._in_spouse_extractor = options['in_spouse_extractor']

        regex_options = regex.UNICODE | regex.IGNORECASE
        martta_base_pattern = r'martt'
        martta_org_ending_patterns = (
            r'(?:a-?(?:\s?yhdist|järjes|seura|toimin|liit|kerho))'
        )
        martta_without_org_ending_patterns = r'(?:oihin|ojen)'
        regex_allow_one_substitution = r'{s<=1}'
        martta_pattern = r'(?:{}(?:{}|{})){}'.format(
            martta_base_pattern,
            martta_org_ending_patterns,
            martta_without_org_ending_patterns,
            regex_allow_one_substitution,
        )

        self._REGEX_MARTTA_FLAG = regex.compile(martta_pattern, regex_options)

    def _is_person_female(self):
        """
        This function assumes only heterosexual marriages and checks
        that the person, whose data we are looking at, is female. If
        we are in the spouse extractor and primary person is male,
        then the spouse is female. If we are in the primary person
        and person is female, then the person is female.
        :return: Boolean
        """
        is_female = False

        if (
            self._in_spouse_extractor
            and self._deps['person']['name']['gender'] == 'Male'
        ):
            is_female = True
        elif (
            not self._in_spouse_extractor
            and self._deps['person']['name']['gender'] == 'Female'
        ):
            is_female = True

        return is_female

    def _extract(self, entry, extraction_results, extraction_metadata):
        martta_activity = None
        if self._is_person_female():
            martta_activity = self._check_martta_activity(entry['text'])

        return self._add_to_extraction_results(
            martta_activity, extraction_results, extraction_metadata
        )

    def _check_martta_activity(self, text):
        text = remove_hyphens_from_text(text)
        martta = regex.search(self._REGEX_MARTTA_FLAG, text)
        return martta is not None
