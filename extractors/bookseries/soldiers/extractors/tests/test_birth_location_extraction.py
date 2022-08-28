import pytest
from extractors.bookseries.soldiers.extractors.birthday_extractor import (
    BirthdayExtractor,
)
from extractors.bookseries.soldiers.extractors.birthlocation_extractor import (
    BirthLocationExtractor,
)


class TestSoldierBirthLocationExtraction:
    @pytest.yield_fixture(autouse=True)
    def location_extractor(self, th):
        return th.setup_extractor(BirthLocationExtractor(BirthdayExtractor, None))

    def should_extract_location_with_coordinates(self, location_extractor):
        text = 'Testi Testinen s 12,3.05 Paimio, mv. Pso'
        previous_metadata = {BirthdayExtractor.extraction_key: {'cursorLocation': 16}}

        results, metadata = location_extractor.extract(
            {'text': text}, {}, previous_metadata
        )

        assert results['birthLocation']['locationName'] == 'Paimio'
        assert results['birthLocation']['latitude'] is not None
        assert results['birthLocation']['longitude'] is not None
        assert results['birthLocation']['region'] == 'other'

        assert (
            metadata['birthLocation']['cursorLocation'] == 32
        )  # Match ends at position 32 after "Paimio,"

    def should_set_coordinates_to_none_if_they_are_not_found(self, location_extractor):
        text = 'Testi Testinen s 12,3.05 Muumilaakso, mv. Pso'
        previous_metadata = {BirthdayExtractor.extraction_key: {'cursorLocation': 16}}

        results, metadata = location_extractor.extract(
            {'text': text}, {}, previous_metadata
        )

        assert results['birthLocation']['locationName'] == 'Muumilaakso'
        assert results['birthLocation']['latitude'] is None
        assert results['birthLocation']['longitude'] is None
