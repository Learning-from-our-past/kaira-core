import pytest
from extractors.bookseries.karelians.extractors.martta_activity_flag_extractor import MarttaActivityFlagExtractor


class TestMarttaActivityFlagExtraction:
    @pytest.yield_fixture(autouse=True)
    def extractor(self):
        return MarttaActivityFlagExtractor(None, {'in_spouse_extractor': False})

    def _verify_flags(self, expected_flags_and_texts, result_map, in_spouse=False, sex='Female'):
        flag = MarttaActivityFlagExtractor.extraction_key
        parent_data = {'extraction_results': {'name': {'gender': sex}},
                       'parent_data': None}

        result_map.add_results('mockPrimaryPerson', {'name': {'gender': sex}})

        # Wire the dependencies and mock result map directly to the extractor
        extractor = MarttaActivityFlagExtractor(None, {'in_spouse_extractor': in_spouse})
        extractor.set_extraction_results_map(result_map)
        extractor.set_required_dependencies(['mockPrimaryPerson'])

        for e in expected_flags_and_texts:
            results, metadata = extractor.extract({'text': e[0]}, {}, {})
            assert results[flag] is e[1]

    def should_return_true_if_text_contains_mentions_of_participating_in_martta_org_and_primaryperson_is_female_and_extractor_not_in_spouse_extractor(self, result_map):
        self._verify_flags([
            ('Rouva Nimetön on kuulunut Vahvialan Marttayhdistykseen.', True),
            ('ja ottanut osaa Lotta- ja Marttajärjestön toimintaan.', True),
            ('hänelle on myönnetty Marttaliiton kultainen ansiomerkki.', True),
            ('Rouva Tanskanen on Kurkijoen Marttaseuran jäsen.', True),
            ('on osal listunut nuorisoseura ja marttatoimintaan.', True),
            ('Emäntä Hoikka on Ostamon Marttakerhon perustajajäsen', True),
            ('Hän on kuulunut Vanajan Marttoihin,', True),
            (' on toiminut Ojaisten marttojen puheenjohtajana', True)
        ], result_map, in_spouse=False, sex='Female')

    def should_return_true_if_text_contains_mentions_of_participating_in_martta_org_with_typos_and_spaces_and_hyphens_and_primaryperson_is_female_and_extractor_not_in_spouse_extractor(self, result_map):
        self._verify_flags([
            ('Rouva Nimetön on kuulunut Vahvialan M4rtta yhdistykseen.', True),
            ('ja ottanut osaa Lotta- ja Martta-järj3stön toimintaan.', True),
            ('hänelle on myönnetty Marttal1iton kultainen ansiomerkki.', True),
        ], result_map, in_spouse=False, sex='Female')

    def should_return_true_if_primaryperson_is_male_and_extractor_is_in_spouse_extractor(self, result_map):
        self._verify_flags([
            ('Rouva kuului Marttayhdistykseen.', True)
        ], result_map, in_spouse=True, sex='Male')

    def should_return_false_if_text_contains_Martta_as_name_primaryperson_is_female_and_extractor_is_not_in_spouse_extractor(self, result_map):
        self._verify_flags([
            ('Rouvan nimi oli Martta Marttakainen.', False)
        ], result_map, in_spouse=False, sex='Female')

    def should_return_false_if_text_contains_no_mention_of_marttaism_and_primaryperson_is_female_and_extractor_is_not_in_spouse_extractor(self, result_map):
        self._verify_flags([
            ('Rouva eli lottaelämää sotarintaman hiekkarannoilla.', False)
        ], result_map, in_spouse=False, sex='Female')

    def should_return_none_if_primaryperson_is_male_and_extractor_not_in_spouse_extractor(self, result_map):
        self._verify_flags([
            ('Rouva kuului Marttayhdistykseen.', None)
        ], result_map, in_spouse=False, sex='Male')

    def should_return_none_if_primaryperson_is_female_and_extractor_is_in_spouse_extractor(self, result_map):
        self._verify_flags([
            ('Rouva kuului Marttayhdistykseen.', None)
        ], result_map, in_spouse=True, sex='Female')
