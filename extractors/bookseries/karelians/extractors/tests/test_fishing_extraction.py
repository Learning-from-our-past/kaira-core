import pytest
from extractors.bookseries.karelians.extractors.fishing_extractor import (
    FishingExtractor,
)


class TestFishingExtraction:
    @pytest.yield_fixture(autouse=True)
    def extractor(self, th):
        return th.setup_extractor(FishingExtractor(None, None))

    def _verify_fishing(self, expected_texts_and_years, extractor):
        flag = 'fishing'

        for text, year in expected_texts_and_years:
            results, metadata = extractor.extract({'text': text}, {}, {})

            assert results[flag] == year

    def should_correctly_extract_fishing(self, extractor):
        self._verify_fishing(
            [('X harrastaa kalastusta ja metsästystä.', True)], extractor
        )

    def should_not_extract_fishing(self, extractor):
        self._verify_fishing(
            [
                (
                    'X:n perheellä on 27 ha:n suuruinen maahankintalain mukaan saatu tila',
                    False,
                )
            ],
            extractor,
        )
