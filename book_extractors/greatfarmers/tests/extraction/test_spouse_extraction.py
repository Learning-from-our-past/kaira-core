import pytest
from book_extractors.greatfarmers.extraction.extractors.spouse_extractor import SpouseExtractor


class TestSpouseExtraction:

    @pytest.yield_fixture(autouse=True)
    def spouse_extractor(self):
        return SpouseExtractor(None, None)

    def should_extract_spouse_details_correctly(self, spouse_extractor, th):
        spouse_text = "om vsta 1951 Testi Mies Testilä s 25. 9.—12, vmo Anna-Liisa o.s. Testilä s 19. 4. -21. Lapset: Lapsi Lapsekas -38, Lapsikas"
        result, metadata = spouse_extractor.extract({'text': spouse_text}, {}, {})
        spouse_details = result['spouse']

        th.omit_property(spouse_details, 'kairaId')

        assert spouse_details == {
            'formerSurname': 'Testilä',
            'firstNames': 'Anna-Liisa',
            'birthData': {
                'birthDay': 19,
                'birthMonth': 4,
                'birthYear': 1921
            }
        }

        assert metadata == {
            'spouse': {
                'cursorLocation': 83,
                'errors': {}
            }
        }

    def should_return_none_if_spouse_not_available(self, spouse_extractor):
        spouse_text = "om. Testi Testisen perikunta. Viljelijä Mies Testinen. Tila sijaitsee Antooran kylässä. Kokonaispinta-ala on 80,67 ha."
        result, metadata = spouse_extractor.extract({'text': spouse_text}, {}, {})
        spouse_details = result['spouse']

        assert spouse_details is None




