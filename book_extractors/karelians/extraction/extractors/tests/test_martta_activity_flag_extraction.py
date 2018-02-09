import pytest
from book_extractors.extraction_pipeline import ExtractionPipeline, configure_extractor
from book_extractors.karelians.extraction.extractors.martta_activity_flag_extractor import MarttaActivityFlagExtractor


class TestMarttaActivityFlagExtraction:
    @pytest.yield_fixture(autouse=True)
    def extractor(self):
        return MarttaActivityFlagExtractor(None, {'in_spouse_extractor': False})

    def _verify_flags(self, expected_flags_and_texts, in_spouse=False, sex='Female'):
        flag = MarttaActivityFlagExtractor.extraction_key
        parent_data = {'extraction_results': {'name': {'gender': sex}},
                       'parent_data': None}

        pipeline = ExtractionPipeline([
            configure_extractor(MarttaActivityFlagExtractor, extractor_options={'in_spouse_extractor': in_spouse},
                                dependencies_contexts=['main'])
        ])

        for e in expected_flags_and_texts:
            results, metadata = pipeline.process({'text': e[0]}, parent_pipeline_data=parent_data)
            assert results[flag] is e[1]

    def should_return_true_if_text_contains_mentions_of_participating_in_martta_org_and_primaryperson_is_female_and_extractor_not_in_spouse_extractor(self):
        self._verify_flags([
            ('Rouva Nimetön on kuulunut Vahvialan Marttayhdistykseen.', True),
            ('ja ottanut osaa Lotta- ja Marttajärjestön toimintaan.', True),
            ('hänelle on myönnetty Marttaliiton kultainen ansiomerkki.', True),
            ('Rouva Tanskanen on Kurkijoen Marttaseuran jäsen.', True),
            ('on osal listunut nuorisoseura ja marttatoimintaan.', True),
            ('Emäntä Hoikka on Ostamon Marttakerhon perustajajäsen', True),
            ('Hän on kuulunut Vanajan Marttoihin,', True),
            (' on toiminut Ojaisten marttojen puheenjohtajana', True)
        ], in_spouse=False, sex='Female')

    def should_return_true_if_text_contains_mentions_of_participating_in_martta_org_with_typos_and_spaces_and_hyphens_and_primaryperson_is_female_and_extractor_not_in_spouse_extractor(self):
        self._verify_flags([
            ('Rouva Nimetön on kuulunut Vahvialan M4rtta yhdistykseen.', True),
            ('ja ottanut osaa Lotta- ja Martta-järj3stön toimintaan.', True),
            ('hänelle on myönnetty Marttal1iton kultainen ansiomerkki.', True),
        ], in_spouse=False, sex='Female')

    def should_return_true_if_primaryperson_is_male_and_extractor_is_in_spouse_extractor(self):
        self._verify_flags([
            ('Rouva kuului Marttayhdistykseen.', True)
        ], in_spouse=True, sex='Male')

    def should_return_false_if_text_contains_Martta_as_name_primaryperson_is_female_and_extractor_is_not_in_spouse_extractor(self):
        self._verify_flags([
            ('Rouvan nimi oli Martta Marttakainen.', False)
        ], in_spouse=False, sex='Female')

    def should_return_false_if_text_contains_no_mention_of_marttaism_and_primaryperson_is_female_and_extractor_is_not_in_spouse_extractor(self):
        self._verify_flags([
            ('Rouva eli lottaelämää sotarintaman hiekkarannoilla.', False)
        ], in_spouse=False, sex='Female')

    def should_return_none_if_primaryperson_is_male_and_extractor_not_in_spouse_extractor(self):
        self._verify_flags([
            ('Rouva kuului Marttayhdistykseen.', None)
        ], in_spouse=False, sex='Male')

    def should_return_none_if_primaryperson_is_female_and_extractor_is_in_spouse_extractor(self):
        self._verify_flags([
            ('Rouva kuului Marttayhdistykseen.', None)
        ], in_spouse=True, sex='Female')
