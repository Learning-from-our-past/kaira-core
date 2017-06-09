from book_extractors.common.postprocessors import place_name_cleaner
from book_extractors.common.extraction_keys import KEYS
from book_extractors.common.metadata_helper import MetadataCollector
import pytest


class TestPlaceNameNormalizationWithManualLists:

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
            KEYS['region']: None,
            KEYS['coordinates']: {
                KEYS['latitude']: '12.00',
                KEYS['longitude']: '12.00'
            }
        }

        result = place_name_cleaner.try_to_normalize_place_name(entry)
        assert result[KEYS['locationName']] == 'Testimaa'
        assert result[KEYS['region']] is None

    def should_augment_region_to_entries(self):
        # Sample of most common place names which lacked region data before updating place names json

        def check_place(data):
            entry = {
                KEYS['locationName']: data[0],
                KEYS['region']: None
            }
            result = place_name_cleaner.try_to_normalize_place_name(entry)
            assert result[KEYS['locationName']] == data[1]
            assert result[KEYS['region']] == data[2]

        places = [
            ('Antreassa', 'Antrea', 'karelia'),
            ('Kivennapa', 'Kivennapa', 'karelia'),
            ('Helsinlg', 'Helsinki', 'other'),
            ('Parikkala', 'Parikkala', 'other'),
            ('Harlu', 'Harlu', 'karelia'),
        ]

        for data in places:
            check_place(data)


class TestPlaceNameNormalizationWithPlaceList:

    @pytest.yield_fixture(autouse=True)
    def metadata_collector(self):
        return MetadataCollector()

    def should_not_use_name_list_if_manual_list_had_match(self, mocker):
        mocker.patch('book_extractors.common.postprocessors.place_name_cleaner.normalize_place_name_with_known_list_of_places')
        entry = {
            KEYS['locationName']: 'Rääkkylässä',
            KEYS['region']: None
        }

        result = place_name_cleaner.try_to_normalize_place_name(entry)
        assert result[KEYS['locationName']] == 'Rääkkylä'
        assert result[KEYS['region']] == 'other'
        assert not place_name_cleaner.normalize_place_name_with_known_list_of_places.called

    def should_skip_if_place_has_coordinate_data(self):
        entry = {
            KEYS['locationName']: 'Alastarosa',
            KEYS['region']: 'other',
            KEYS['coordinates']: {
                KEYS['latitude']: '12.00',
                KEYS['longitude']: '12.00'
            }
        }

        result = place_name_cleaner.try_to_normalize_place_name(entry)
        assert result[KEYS['locationName']] == 'Alastarosa'    # Because coordinates, this name was not changed even if it could have
        assert result[KEYS['region']] == 'other'

    def should_change_name_to_one_from_list_with_same_stem(self):
        # TODO: spying the function would be nice...

        entry = {
            KEYS['locationName']: 'Aavasaksassa',
            KEYS['region']: None,
            KEYS['coordinates']: {
                KEYS['latitude']: None,
                KEYS['longitude']: None
            }
        }

        result = place_name_cleaner.try_to_normalize_place_name(entry)
        assert result[KEYS['locationName']] == 'Aavasaksa'

    def should_find_closest_match_with_jw_if_stem_was_not_found_from_list_and_cache_result(self, metadata_collector):
        assert ('kalliokos' in place_name_cleaner.place_list_index) is False

        entry = {
            KEYS['locationName']: 'Kalliokos',
            KEYS['region']: None,
            KEYS['coordinates']: {
                KEYS['latitude']: None,
                KEYS['longitude']: None
            }
        }

        result = place_name_cleaner.try_to_normalize_place_name(entry, metadata_collector)
        assert result[KEYS['locationName']] == 'Kalliokoski'
        assert ('kalliokos' in place_name_cleaner.place_list_index) is True
        assert place_name_cleaner.place_list_index['kalliokos']['addedByKaira'] is True

        # Should have recorded to the result metadata that JW was used.
        assert metadata_collector.get_metadata()['jaroWinklerFuzzyLocationNameFixFrom'] == 'Kalliokos'

    def should_use_place_as_is_if_no_jw_match_was_found(self, metadata_collector):
        entry = {
            KEYS['locationName']: 'Testikäspaikka',
            KEYS['region']: None,
            KEYS['coordinates']: {
                KEYS['latitude']: None,
                KEYS['longitude']: None
            }
        }

        result = place_name_cleaner.try_to_normalize_place_name(entry, metadata_collector)
        assert result[KEYS['locationName']] == 'Testikäspaikka'

        # Should have recorded to the metadata that place name was not found from available lists
        assert metadata_collector.get_metadata()['errors']['locationNameNotFoundFromLists'] == 2
