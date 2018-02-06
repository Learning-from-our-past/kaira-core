import pytest
from book_extractors.karelians.extraction.extractors.spouse_extractor import SpouseExtractor


class TestSpouseExtraction:

    @pytest.yield_fixture(autouse=True)
    def spouse_extractor(self):
        return SpouseExtractor(None, None)

    def should_extract_spouse_details_correctly(self, spouse_extractor, th):
        spouse_text = 'Puol. Maija Nyymi o.s. Testaaja, emäntä, synt. 30. 6. -19 Testilässä. Avioit. -44. Poika: Joku Jälkeäinen -46 Nyymilä.'
        parent_data = {'extraction_results': {'primaryPerson': {'name': {'gender': 'Male'}}},
                       'parent_data': None}
        result, metadata = spouse_extractor.extract({'text': spouse_text}, {}, {}, parent_pipeline_data=parent_data)
        spouse_details = result['spouse']

        th.omit_property(spouse_details, 'kairaId')

        assert spouse_details == {
            'formerSurname': 'Testaaja',
            'firstNames': 'Maija Nyymi',
            'hasSpouse': True,
            'deathYear': None,
            'weddingYear': 1944,
            'birthData': {
                'birthDay': 30,
                'birthMonth': 6,
                'birthYear': 1919,
                'birthLocation': {
                    'locationName': 'Testilässä',
                    'region': None,
                    'latitude': None,
                    'longitude': None
                }
            },
            'profession': {
                'professionName': 'emäntä',
                'extraInfo': {
                    'SESgroup1989': 1,
                    'agricultureOrForestryRelated': True,
                    'education': True,
                    'englishName': 'Farm housewife',
                    'manualLabor': True,
                    'occupationCategory': 3,
                    'socialClassRank': 5
                }
            },
            'warData': {
                'injuredInWarFlag': None,
                'servedDuringWarFlag': None,
                'lottaActivityFlags': {'lotta': False,
                                       'foodLotta': False,
                                       'officeLotta': False,
                                       'nurseLotta': False,
                                       'antiairLotta': False,
                                       'pikkulotta': False}
            }
        }

        assert metadata == {
            'spouse': {
                'cursorLocation': 79,
                'errors': {}
            }
        }

    def should_return_none_if_spouse_not_available(self, spouse_extractor):
        spouse_text = 'om. Testi Testisen perikunta. Viljelijä Mies Testinen. Tila sijaitsee Antooran kylässä. Kokonaispinta-ala on 80,67 ha.'
        result, metadata = spouse_extractor.extract({'text': spouse_text}, {}, {})
        spouse_details = result['spouse']

        assert spouse_details is None
