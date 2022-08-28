import regex
from core.pipeline_construction.base_extractor import BaseExtractor
from core.utils.text_utils import remove_hyphens_from_text


class MilitaryRankExtractor(BaseExtractor):
    extraction_key = 'militaryRank'

    def __init__(self, cursor_location_depends_on=None, options=None):
        super().__init__(cursor_location_depends_on, options)
        self._declare_expected_dependency_names(['person'])
        self._in_spouse_extractor = options['in_spouse_extractor']

        """
        This is a list of ranks in the Finnish ground and air forces as well as in
        the navy. The ranks are included together on this list, and the equivalent
        ranks are always with the ground/air force rank first, then the navy rank
        right under that.

        The format of the list is:
        (<rank>, <regular expression>, <forbidden prefixes>)

        The need for forbidden prefixes comes from not wanting, for example, the
        rank "kapteeniluutnantti" to be extracted as the rank "luutnantti".
        "luutnantti" is a lower rank but its regular expression would also find a
        match on "kapteeniluutnantti". On the other hand we also do not want to
        completely discard all prefixes, for example, we still want to find ranks
        like "lääkintäluutnantti".

        NOTE: These are in ascending order and must remain so in order for this to
        work correctly. This is because in most cases we want to pick the lowest
        rank found in the entry.
        """
        ranks_and_regex_patterns = (
            # miehistö
            ('sotamies', r'(?:sotamie(?:s|he(?:ksi|nä)){s<=1})', None),
            ('matruusi', r'(?:matruusi){s<=1}', ('yli',)),
            ('korpraali', r'(?:korpraali(?:na|ksi)?){s<=2}', None),
            ('ylimatruusi', r'(?:ylimatruusi){s<=1}', None),
            # aliupseerit
            ('alikersantti', r'a(?:likersantt?i){s<=1}', ('palo',)),
            ('kersantti', r'(?:kersant(?:ti(?:na)?|iksi)){s<=1}', ('yli', 'ali')),
            ('ylikersantti', r'y(?:likersantt?i){s<=2}', None),
            ('vääpeli', r'(?:vääpeli){s<=1}\w{0,4}', ('yli',)),
            ('pursimies', r'(?:pursimie[sh]){s<=1}', ('yli',)),
            ('ylivääpeli', r'(?:ylivääpeli){s<=1}', None),
            ('ylipursimies', r'(?:ylipursimie[sh]){s<=1}', None),
            ('sotilasmestari', r'(?:sotilasmestari){s<=1}', None),
            # upseerit
            ('vänrikki', r'(?:vänrik(ki|ik)){s<=1}', None),
            ('aliluutnantti', r'a(?:liluutnant){s<=1}', ('kenra',)),
            (
                'luutnantti',
                r'(?:luutnant){s<=1}',
                ('ali', 'yli', 'eversti', 'kenraali', 'kapteeni'),
            ),
            ('yliluutnantti', r'y(?:liluutnant){s<=1}', None),
            (
                'kapteeni',
                r'(?:(?:lääkintä){s<=1}|\b)(?:kapteeni(na|ksi)?){s<=1}\b',
                ('meri', 'komentaja', 'satama'),
            ),
            ('kapteeniluutnantti', r'(?:kapteeniluutnantti){s<=1}', None),
            ('majuri', r'majuri', 'kenraali'),
            ('komentajakapteeni', r'(?:komentajakapteeni){s<=2}', None),
            ('everstiluutnantti', r'(?:everstiluutnantti){s<=2}', None),
            ('komentaja', r'(?:komentaja){s<=1}(ksi|\b)', None),
            (
                'eversti',
                r'(?:lääkintä|insinööri|\b)(?:eversti){s<=1}(?:ksi|nä|\b)',
                None,
            ),
            ('kommodori', r'kommodori', None),
            ('kenraalimajuri', r'kenraalimajuri', None),
            ('kenraaliluutnantti', r'kenraaliluutnantti', None),
            ('kenraali', r'\b(kenraali){s<=1}(na|ksi|\b)', None),
        )
        flags = regex.UNICODE | regex.IGNORECASE
        self._RANKS_AND_REGEX = tuple(
            (rank, regex.compile(pattern, flags), unpermitted)
            for rank, pattern, unpermitted in ranks_and_regex_patterns
        )
        self._PROMOTION_REGEX = regex.compile('ylenn', flags)

    def _extract(self, entry, extraction_results, extraction_metadata):
        rank = None
        if self._is_person_male():
            rank = self._find_rank(entry)
        return self._add_to_extraction_results(
            rank, extraction_results, extraction_metadata
        )

    def _find_rank(self, entry):
        """
        Tries to find a person's military rank from a MiKARELIA text entry.
        :param entry: MiKARELIA text entry.
        :return: None or rank
        """
        text = remove_hyphens_from_text(entry['text'])

        # In case the person was promoted from a lower rank to a higher rank, we
        # do not want to stop at the lowest rank in the entry.
        find_highest_rank = self._PROMOTION_REGEX.search(text)
        found_rank = None
        for rank, rank_regex, forbidden_prefixes in self._RANKS_AND_REGEX:
            rank_matches = rank_regex.finditer(text)
            for match in rank_matches:
                if not self._contains_any_prefix(text, match, forbidden_prefixes):
                    found_rank = rank
            if found_rank is not None and not find_highest_rank:
                break

        return found_rank

    @staticmethod
    def _contains_any_prefix(text, match, prefixes):
        """
        Determines if the regex match is preceded by a string.
        :param text: Text where regex match was found
        :param match: Regex match
        :param prefixes: Prefixes whose presence to check for
        :return: True or False
        """
        if prefixes is None:
            return False
        for prefix in prefixes:
            rank_start = match.start()
            rank_word_start = rank_start - len(prefix)
            rank_prefix = text[rank_word_start:rank_start]
            if prefix == rank_prefix.casefold():
                return True

    def _is_person_male(self):
        """
        This function assumes only heterosexual marriages and checks
        that the person, whose data we are looking at, is male. If
        we are in the spouse extractor and primary person is female,
        then the spouse is male. If we are in the primary person and
        person is male, then the person is male.
        :return: Boolean, True or False.
        """
        is_male = False

        if (
            self._in_spouse_extractor
            and self._deps['person']['name']['gender'] == 'Female'
        ):
            is_male = True
        elif (
            not self._in_spouse_extractor
            and self._deps['person']['name']['gender'] == 'Male'
        ):
            is_male = True

        return is_male
