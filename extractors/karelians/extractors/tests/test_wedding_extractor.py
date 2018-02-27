import pytest
from extractors.karelians.extractors.wedding_extractor import WeddingExtractor


class TestWeddingExtraction:

    @pytest.yield_fixture(autouse=True)
    def extractor(self, th):
        return th.setup_extractor(WeddingExtractor(None, None))

    def _verify_years(self, expected_texts_and_years, extractor):
        flag = 'wedding'

        for text, year in expected_texts_and_years:
            results, metadata = extractor.extract({'text': text}, {}, {})

            assert results[flag] == year

    def should_correctly_extract_wedding_year(self, extractor):
        self._verify_years([
            ('Testilässä. Avioit. -44. Poika: Joku', 1944)
        ], extractor)

    def should_correctly_extract_wedding_year_with_data_written_without_separator_or_whitespace(self, extractor):
        self._verify_years([
            ('Testilässä. Avioit-45. Poika: Joku', 1945)
        ], extractor)

    def should_correctly_extract_wedding_year_with_typo_and_uncommon_separator(self, extractor):
        self._verify_years([
            ('Testilässä. Aviqit! -48. Poika: Joku', 1948)
        ], extractor)

    def should_correctly_extract_none_if_wedding_year_is_not_present(self, extractor):
        self._verify_years([
            ('Testilässä. Poika: Joku Jälkeäinen -46 Nyymilä.', None)
        ], extractor)
