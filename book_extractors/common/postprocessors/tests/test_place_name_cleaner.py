from book_extractors.common.postprocessors import place_name_cleaner
from book_extractors.common.extraction_keys import KEYS


class TestPlaceNameNormalization:

    def should_augment_place_entry_with_fixed_name_and_region(self):
        entry = {
            KEYS['locationName']: 'Rääkkylässä',
            KEYS['region']: None
        }

        result = place_name_cleaner.try_to_normalize_place_name(entry)
        assert result[KEYS['locationName']] == 'Rääkkylä'
        assert result[KEYS['region']] == 'other'


    def should_augment_place_entry_with_name_even_if_region_is_missing(self):
        entry = {
            KEYS['locationName']: 'Kortesjärvellä',
            KEYS['region']: None
        }

        result = place_name_cleaner.try_to_normalize_place_name(entry)
        assert result[KEYS['locationName']] == 'Kortesjärvi'
        assert result[KEYS['region']] is None

    def should_return_place_unmodified_if_it_was_not_found_from_list(self):
        entry = {
            KEYS['locationName']: 'Testimaa',
            KEYS['region']: None
        }

        result = place_name_cleaner.try_to_normalize_place_name(entry)
        assert result[KEYS['locationName']] == 'Testimaa'
        assert result[KEYS['region']] is None
