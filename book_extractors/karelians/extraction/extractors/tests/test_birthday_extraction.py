import pytest
from book_extractors.karelians.extraction.extractors.location_extractor import BirthdayLocationExtractor
from book_extractors.karelians.extraction.extractors.birthday_extractor import BirthdayExtractor


class TestBirthDayLocation:
    @pytest.yield_fixture(autouse=True)
    def location_extractor(self):
        return BirthdayLocationExtractor(BirthdayExtractor.extraction_key, None)

    def should_extract_birth_location_and_fill_in_region_and_coordinates_from_geo_db(self, location_extractor):
        # Simulate the stopping location of the previous extractor which gives this extractor the "anchor point" to
        # begin the extraction.
        previous_metadata = {
            BirthdayExtractor.extraction_key: {
                'cursorLocation': 16
            }
        }

        result, metadata = location_extractor.extract({'text': 'synt. 10. 8. -17 Sippola. Avioit. -38.'}, {},
                                                      previous_metadata)

        assert result['birthLocation']['locationName'] == 'Sippola'
        assert result['birthLocation']['region'] == 'other'
        assert result['birthLocation']['latitude'] is not None
        assert result['birthLocation']['longitude'] is not None

    def should_extract_birth_location_but_leave_region_and_coordinates_empty_if_they_were_not_found(self, location_extractor):
        previous_metadata = {
            BirthdayExtractor.extraction_key: {
                'cursorLocation': 16
            }
        }

        result, metadata = location_extractor.extract({'text': 'synt. 10. 8. -17 Räävinpyrstö. Avioit. -38.'}, {},
                                                      previous_metadata)

        assert result['birthLocation']['locationName'] == 'Räävinpyrstö'
        assert result['birthLocation']['region'] is None
        assert result['birthLocation']['latitude'] is None
        assert result['birthLocation']['longitude'] is None
