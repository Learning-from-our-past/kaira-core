import pytest
from extractors.bookseries.karelians.extractors.forest_extractor import ForestExtractor


class TestForestExtraction:
    @pytest.yield_fixture(autouse=True)
    def extractor(self, th):
        return th.setup_extractor(ForestExtractor(None, None))

    def _verify_forest(self, expected_texts_and_years, extractor):
        flag = 'metsää'

        for text, year in expected_texts_and_years:
            results, metadata = extractor.extract({'text': text}, {}, {})

            assert results[flag] == year

    def should_correctly_extract_forest(self, extractor):
        self._verify_forest(
            [
                (
                    'X:n perheellä on pika-asutustila. joka käsittää 24 ha viljeltyä maata ja 18,5 ha metsää',
                    True,
                )
            ],
            extractor,
        )

    def should_not_extract_forest(self, extractor):
        self._verify_forest(
            [
                (
                    'X:n perheellä on 27 ha:n suuruinen maahankintalain mukaan saatu tila',
                    False,
                )
            ],
            extractor,
        )
