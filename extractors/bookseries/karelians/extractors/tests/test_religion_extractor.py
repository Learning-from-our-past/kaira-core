import pytest
from extractors.bookseries.karelians.extractors.religion_extractor import (
    ReligionExtractor,
)


class TestReligionExtraction:
    @pytest.yield_fixture(autouse=True)
    def extractor(self, th):
        return th.setup_extractor(ReligionExtractor(None, None))

    def _verify_religion(self, expected_texts_and_years, extractor):
        flag = 'religion'

        for text, year in expected_texts_and_years:
            results, metadata = extractor.extract({'text': text}, {}, {})

            assert results[flag] == year

    def should_correctly_extract_religion(self, extractor):
        self._verify_religion(
            [
                (
                    'Rouva X kuuluu ortodoksisen kirkon laulu-kuoroon ja Karjalaseuraan.',
                    True,
                )
            ],
            extractor,
        )

    def should_not_extract_religion(self, extractor):
        self._verify_religion(
            [
                (
                    'Perheellä on myös maatila, jota he yhteisesti hoitavat. Puolisoiden yhteinen harrastus on seurakuntatyö',
                    False,
                )
            ],
            extractor,
        )
