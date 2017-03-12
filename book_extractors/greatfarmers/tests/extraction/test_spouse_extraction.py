import pytest
from book_extractors.greatfarmers.extraction.extractors.spouseextractor import SpouseExtractor


class TestSpouseExtraction:

    @pytest.yield_fixture(autouse=True)
    def spouse_extractor(self):
        return SpouseExtractor(None, None)

    def should_extract_spouse_details_correctly(self, spouse_extractor):
        spouse_text = "om vsta 1951 Testi Mies Testilä s 25. 9.—12, vmo Anna-Liisa o.s. Testilä s 19. 4. -21. Lapset: Lapsi Lapsekas -38, Lapsikas"
        result = spouse_extractor.extract({'text': spouse_text}, {'data': {}, 'cursor_locations': {}})['data']['spouse']

        assert result == {
            'originalFamily': 'Testilä',
            'spouseName': 'Anna-Liisa',
            'birthData': {
                'birthDay': '19',
                'birthMonth': '4',
                'birthYear': '1921',
            }
        }

    def should_return_none_if_spouse_not_available(self, spouse_extractor):
        spouse_text = "om. Testi Testisen perikunta. Viljelijä Mies Testinen. Tila sijaitsee Antooran kylässä. Kokonaispinta-ala on 80,67 ha."
        result = spouse_extractor.extract({'text': spouse_text}, {'data': {}, 'cursor_locations': {}})['data']['spouse']

        assert result is None




