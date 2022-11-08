import pytest
from extractors.bookseries.karelians.extractors.forest_extractor import (
    ForestAreaExtractor,
)


class TestForestAreaExtraction:
    @pytest.yield_fixture(autouse=True)
    def extractor(self, th):
        return th.setup_extractor(ForestAreaExtractor(None, None))

    def _verify_forest_area(self, expected_texts_and_years, extractor):
        flag = 'forest_area'

        for text, year in expected_texts_and_years:
            results, metadata = extractor.extract({'text': text}, {}, {})

            assert results[flag] == year

    def should_correctly_extract_forest_area(self, extractor):
        self._verify_forest_area(
            [
                (
                    'X:n perheellä on pika-asutustila. joka käsittää 24 ha viljeltyä maata ja 18,5 ha metsää',
                    True,
                )
            ],
            extractor,
        )

    def should_not_extract_forest_area(self, extractor):
        self._verify_forest_area(
            [
                (
                    'X:n perheellä on 27 ha:n suuruinen maahankintalain mukaan saatu tila',
                    False,
                )
            ],
            extractor,
        )
