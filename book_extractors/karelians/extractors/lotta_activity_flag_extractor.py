from core.base_extractor import BaseExtractor
from core.utils.text_utils import remove_hyphens_from_text
from core.utils.text_utils import check_string_for_substrings
from core.utils.text_utils import take_sub_str_based_on_start_and_end_and_radius
from core.utils.text_utils import is_first_character_lower_case
import regex


class LottaActivityFlagExtractor(BaseExtractor):
    extraction_key = 'lottaActivityFlags'

    def __init__(self, cursor_location_depends_on=None, options=None):
        super(LottaActivityFlagExtractor, self).__init__(cursor_location_depends_on, options)
        self._in_spouse_extractor = options['in_spouse_extractor']

        lotta_org_pattern = r'(?P<lottaOrg>(?:[Ll]otta\s?(?:S|s)värd|[Ll]ottayhdis|[Ll]ottajärjes)){s<=1}'

        """
        The pattern below finds words with the base pattern "lotta", "lottiin"
        and "lottana". It also allows for the pattern "lottiinna" but that does
        not interest us. It also allows for up to 12 characters before the word
        "lotta", so we could find people like "muonituslotta" or any other word
        in front of "lotta" that forms a compound word with "lotta". "lotta/na"
        has to be followed immediately by punctuation or whitespace, so we only
        get words that actually stop with "lotta".
        """
        lotta_activity_pattern_one = r'(?P<lotta>(?<=[\s.,])\w{0,12}lot(?:ta|tiin)(?:na)?){s<=1}(?=[\s.,!])'

        """
        The pattern below works similarly to the one above, but instead of
        allowing for words in front of "lotta", it allows for them after the
        word "lotta". This means we can find people whose lotta participation
        is expressed as, for example, "lottatyössä", "lottatoimintaan". "lotta"
        has to be preceded by punctuation or whitespace, so we get only words
        that actually start with "lotta".
        """
        lotta_activity_pattern_two = r'(?<=[\s.,])(?P<lotta>lotta){s<=1}\w{0,12}'
        
        """
        Trying to combine these two patterns into one pattern resulted in a
        headache as it caused the regex to match too many false positives and
        the "postprocessing" logic after finding the regex matches got too
        complicated.
        """

        lotta_word_pattern = r'(?<=[\s.,])\w{0,12}(lotta){s<=1}\w{0,12}(?=[\s.,])'

        food_lotta_pattern = r'(?:(?:uonituslott)|(?:anttiinilott)){s<=2}|(?:(?:uonitustehtä)|(?:anttiinitehtä)){s<=2}'
        office_lotta_pattern = r'(?:(?:anslialott)|(?:oimistolott)|(?:eskuslott)|(?:uhelinlott)|(?:iesti(?:tys|ntä)?lott)){s<=1}'
        nurse_lotta_pattern = r'(?:lääkintälott[ai]){s<=2}'
        antiair_lotta_pattern = r'[\s.,](?:[ij!1][vts](?:lotta){s<=1})|(?:lmavalvontalott){s<=2}|(?:ilmavalvontatehtäv){s<=2}'
        pikkulotta_pattern = r'(?:pikkulott){s<=1}'

        regex_options = regex.UNICODE
        self._REGEX_LOTTA_ORGANIZATION = regex.compile(lotta_org_pattern, regex_options)
        self._REGEX_GENERAL_LOTTA_PATTERN_ONE = regex.compile(lotta_activity_pattern_one, regex_options)
        self._REGEX_GENERAL_LOTTA_PATTERN_TWO = regex.compile(lotta_activity_pattern_two, regex_options)
        self._REGEX_LOTTA_WORD = regex.compile(lotta_word_pattern, regex_options)
        self._REGEX_FOOD_LOTTA = regex.compile(food_lotta_pattern, regex_options)
        self._REGEX_OFFICE_LOTTA = regex.compile(office_lotta_pattern, regex_options)
        self._REGEX_NURSE_LOTTA = regex.compile(nurse_lotta_pattern, regex_options)
        self._REGEX_ANTIAIR_LOTTA = regex.compile(antiair_lotta_pattern, (regex_options | regex.IGNORECASE))
        self._REGEX_PIKKULOTTA = regex.compile(pikkulotta_pattern, (regex_options | regex.IGNORECASE))

        self._NO_RESULT = {'lotta': None,
                           'foodLotta': None,
                           'officeLotta': None,
                           'nurseLotta': None,
                           'antiairLotta': None,
                           'pikkulotta': None,
                           'organizationLotta': None}

        self._word_suffix_length = 4
        self._surroundings_radius = 15

        self._declare_expected_dependency_names(['person'])

    def _is_person_female(self):
        """
        This function assumes only heterosexual marriages and checks that the person, whose
        data we are looking at, is female. If we are in the spouse extractor and primary person
        is male, then the spouse is female. If we are in the primary person and person is
        female, then the person is female.
        :return: Boolean
        """
        is_female = False

        if self._in_spouse_extractor and self._deps['person']['name']['gender'] == 'Male':
            is_female = True
        elif not self._in_spouse_extractor and self._deps['person']['name']['gender'] == 'Female':
            is_female = True

        return is_female

    @staticmethod
    def is_any_value_in_dict_true(dict_to_check):
        for key, value in dict_to_check.items():
            if value:
                return True
        return False

    def _extract(self, entry, extraction_results, extraction_metadata):
        if self._is_person_female():
            text = remove_hyphens_from_text(entry['full_text'])
            lotta_activity = self._extract_lotta_flags(text)
        else:
            lotta_activity = self._NO_RESULT

        return self._add_to_extraction_results(lotta_activity, extraction_results, extraction_metadata)

    def _extract_lotta_flags(self, text):
        lotta_flags = {'foodLotta': self._REGEX_FOOD_LOTTA.search(text) is not None,
                       'officeLotta': self._REGEX_OFFICE_LOTTA.search(text) is not None,
                       'nurseLotta': self._REGEX_NURSE_LOTTA.search(text) is not None,
                       'antiairLotta': self._REGEX_ANTIAIR_LOTTA.search(text) is not None,
                       'pikkulotta': self._REGEX_PIKKULOTTA.search(text) is not None}

        lotta = True
        org_lotta = False
        if not self.is_any_value_in_dict_true(lotta_flags):
            lotta = self._check_for_lotta_activity(text)
            org_lotta = self._REGEX_LOTTA_ORGANIZATION.search(text) is not None

        lotta_flags['lotta'] = lotta
        lotta_flags['organizationLotta'] = org_lotta
        return lotta_flags

    def _check_for_lotta_activity(self, text):
        lotta = self._check_for_lotta_organization(text)
        if not lotta:
            lotta = self._check_for_first_lotta_pattern_variant(text)
        if not lotta:
            lotta = self._check_for_second_lotta_pattern_variant(text)
        return lotta

    def _check_for_lotta_organization(self, text):
        lotta = self._REGEX_LOTTA_ORGANIZATION.search(text)

        return lotta is not None

    def _check_for_first_lotta_pattern_variant(self, text):
        """
        Check the comment attached to the regex pattern in the constructor for
        more explanation on how this works, as well as the docstring of the
        is_lotta_match_desirable function.
        """
        lotta_found = False
        lotta_matches = self._REGEX_GENERAL_LOTTA_PATTERN_ONE.finditer(text)

        for match in lotta_matches:
            if self._is_lotta_match_desirable(text, match):
                lotta_found = True
                break

        return lotta_found

    def _check_for_second_lotta_pattern_variant(self, text):
        """
        This route has some documentation in the constructor where the regex
        pattern is defined and some of the same stuff from the function
        is_lotta_match_desirable applies here (i.e. disregarding upper case
        first character matches because they are likely to be names).
        """
        lotta_found = False
        lotta_matches = self._REGEX_GENERAL_LOTTA_PATTERN_TWO.finditer(text)

        for match in lotta_matches:
            lotta_surroundings = take_sub_str_based_on_start_and_end_and_radius(text,
                                                                                match.start(),
                                                                                match.end(),
                                                                                self._surroundings_radius)
            lotta_word = self._find_full_lotta_word_from_string(lotta_surroundings)
            if lotta_word:
                if is_first_character_lower_case(lotta_word):
                    lotta_found = True
                    break

        return lotta_found

    def _find_full_lotta_word_from_string(self, match_string):
        """
        Try to find the entire "lotta" word from the given string, including
        other words attached to it (i.e. in the case of a compound word).
        :param match_string: A string that is suspected to contain a word with
        the string "lotta" in it.
        :return: A string that contains the lotta word in full. e.g. "Lottanen"
        or "muonituslottana"
        """
        lotta_word_match = self._REGEX_LOTTA_WORD.search(match_string)
        lotta_word = None

        if lotta_word_match:
            lotta_word = lotta_word_match[0]

        return lotta_word

    def _is_lotta_match_desirable(self, text, lotta_match):
        """
        Test whether this is likely to be a false positive or a true positive.
        :param text: The current person entry's text.
        :param lotta_match_string: The string from the regex lotta match found
        in the current person entry's text.
        :return: True or False
        """
        match_string = lotta_match.group('lotta')
        lotta_ending = match_string[-self._word_suffix_length:]
        forbidden_suffices = ('sta', 'ja')
        forbidden_patterns_in_match = ('uotta', 'dotta', 'lohta')

        """
        Words ending with the suffices -sta (e.g. "omakotitalosta") and -ja 
        (e.g. "kiillottaja") are false positives. Thus, any matches showing
        these patterns have to be discarded.
        
        If, in the overall match, the substrings "uotta", "dotta" or "lohta" 
        are present, they are likely to be false positives. (e.g. "vuotta", 
        "kalastaa lohta")
        """
        if (not check_string_for_substrings(forbidden_suffices, lotta_ending)
                and not check_string_for_substrings(forbidden_patterns_in_match, match_string)):
            lotta_surroundings = take_sub_str_based_on_start_and_end_and_radius(text,
                                                                                lotta_match.start(),
                                                                                lotta_match.end(),
                                                                                self._surroundings_radius)
            lotta_word = self._find_full_lotta_word_from_string(lotta_surroundings)
            if lotta_word:
                permitted_patterns = ('Pikku', 'IV')
                """
                Only accept matches with lower case first character to omit people
                whose name is "Lotta". But to capture some pikkulottas and air 
                surveillance lottas, we have to allow upper case first characters in 
                some cases. (e.g. "Pikkulotta", "Iv-lotta")
                """
                if (is_first_character_lower_case(lotta_word) or
                        check_string_for_substrings(permitted_patterns, lotta_word, ignore_case=True)):
                        return True
        return False
