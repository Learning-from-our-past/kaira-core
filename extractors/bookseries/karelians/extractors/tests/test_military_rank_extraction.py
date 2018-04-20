import pytest
from extractors.bookseries.karelians.extractors.military_rank_extractor import MilitaryRankExtractor


class TestMilitaryRankExtraction:
    @staticmethod
    def _verify_rank(result_map, data, expected_rank, sex='Male', in_spouse=False):
        flag = MilitaryRankExtractor.extraction_key

        extractor = MilitaryRankExtractor(None, {'in_spouse_extractor': in_spouse})
        result_map.add_results('mockPrimaryPerson', {'name': {'gender': sex}})
        extractor.set_extraction_results_map(result_map)
        extractor.set_required_dependencies(['mockPrimaryPerson'])

        results = extractor.extract({'text': data}, {}, {})[0]
        assert results[flag] == expected_rank

    def should_extract_the_lowest_rank_in_the_entry(self, result_map):
        self._verify_rank(result_map,
                          'Testi Testikäs on sotamies ja hän palveli eversti Testaajan palvelijana.',
                          'sotamies')

    def should_extract_the_highest_rank_in_the_entry_if_a_promotion_is_mentioned(self, result_map):
        data = ('Testiläinen oli vääpeli talvisodassa ja palveliRaskaassa tykistössä. '
                'Hänet ylennettiin jatkosodassa everstiksi.')
        self._verify_rank(result_map, data, 'eversti')

    def should_extract_matruusi_ranks_with_prefixes_correctly(self, result_map):
        self._verify_rank(result_map, 'ylimatruusi', 'ylimatruusi')

    def should_extract_kersantti_ranks_with_prefixes_correctly(self, result_map):
        self._verify_rank(result_map, 'alikersantti', 'alikersantti')
        self._verify_rank(result_map, 'ylikersantti', 'ylikersantti')

    def should_extract_vaapeli_ranks_with_prefixes_correctly(self, result_map):
        self._verify_rank(result_map, 'ylivääpeli', 'ylivääpeli')

    def should_extract_pursimies_ranks_with_prefixes_correctly(self, result_map):
        self._verify_rank(result_map, 'ylipursimies', 'ylipursimies')

    def should_extract_luutnantti_ranks_with_prefixes_correctly(self, result_map):
        self._verify_rank(result_map, 'aliluutnantti', 'aliluutnantti')
        self._verify_rank(result_map, 'yliluutnantti', 'yliluutnantti')
        self._verify_rank(result_map, 'kapteeniluutnantti', 'kapteeniluutnantti')
        self._verify_rank(result_map, 'everstiluutnantti', 'everstiluutnantti')
        self._verify_rank(result_map, 'kenraaliluutnantti', 'kenraaliluutnantti')

    def should_not_extract_kenraalimajuri_as_kenraali_or_majuri(self, result_map):
        self._verify_rank(result_map, 'kenraalimajuri', 'kenraalimajuri')

    def should_not_extract_merikapteeni_as_kapteeni(self, result_map):
        data = ('Testikäs on käynyt Viipurin merenkulkukoulun, Raumalla '
                'yliperämieskurssin ja suorittanut merikapteenin tutkinnon')
        self._verify_rank(result_map, data, None)

    def should_extract_remaining_ranks_correctly(self, result_map):
        self._verify_rank(result_map, 'sotamies', 'sotamies')
        self._verify_rank(result_map, 'matruusi', 'matruusi')
        self._verify_rank(result_map, 'korpraali', 'korpraali')
        self._verify_rank(result_map, 'kersantti', 'kersantti')
        self._verify_rank(result_map, 'vääpeli', 'vääpeli')
        self._verify_rank(result_map, 'sotilasmestari', 'sotilasmestari')
        self._verify_rank(result_map, 'vänrikki', 'vänrikki')
        self._verify_rank(result_map, 'luutnantti', 'luutnantti')
        self._verify_rank(result_map, 'kapteeni', 'kapteeni')
        self._verify_rank(result_map, 'majuri', 'majuri')
        self._verify_rank(result_map, 'komentaja', 'komentaja')
        self._verify_rank(result_map, 'eversti', 'eversti')
        self._verify_rank(result_map, 'kommodori', 'kommodori')
        self._verify_rank(result_map, 'kenraali', 'kenraali')

    def should_extract_none_if_there_is_no_mention_of_a_military_rank(self, result_map):
        self._verify_rank(result_map, 'Testinen ei osallistunut sotaan.', None)

    def should_extract_none_if_primary_person_is_male_and_we_are_in_spouse_extractor(self, result_map):
        self._verify_rank(result_map, 'Testikäs palveli kommodorina talvisodassa.', None,
                          sex='Male', in_spouse=True)

    def should_extract_rank_if_primary_person_is_female_and_we_are_in_spouse_extractor(self, result_map):
        self._verify_rank(result_map, 'Testikäs palveli kommodorina talvisodassa.', 'kommodori',
                          sex='Female', in_spouse=True)

    def should_extract_none_if_primary_person_is_female_and_we_are_not_in_spouse_extractor(self, result_map):
        self._verify_rank(result_map, 'Testikäs palveli kommodorina talvisodassa.', None,
                          sex='Female', in_spouse=False)
