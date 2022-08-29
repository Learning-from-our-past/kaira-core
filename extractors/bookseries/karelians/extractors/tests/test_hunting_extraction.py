import pytest
from extractors.bookseries.karelians.extractors.hunting_extractor import (
    HuntingExtractor,
)


class TestHuntingExtraction:
    @pytest.yield_fixture(autouse=True)
    def extractor(self, th):
        return th.setup_extractor(HuntingExtractor(None, None))

    def _verify_hunting(self, expected_texts_and_years, extractor):
        flag = 'hunting'

        for text, year in expected_texts_and_years:
            results, metadata = extractor.extract({'text': text}, {}, {})

            assert results[flag] == year

    def should_correctly_extract_hunting(self, extractor):
        self._verify_hunting(
            [('X harrastaa kalastusta ja metsästystä.', True)], extractor
        )

    def should_not_extract_hunting(self, extractor):
        self._verify_hunting(
            [
                (
                    'X:n perheellä on 27 ha:n suuruinen maahankintalain mukaan saatu tila',
                    False,
                )
            ],
            extractor,
        )
