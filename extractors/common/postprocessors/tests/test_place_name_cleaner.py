from extractors.common.postprocessors import place_name_cleaner
from extractors.common.extraction_keys import KEYS
from extractors.common.metadata_helper import MetadataCollector
import pytest


class TestPlaceNameNormalizationWithManualLists:
    def should_return_fixed_name(self):
        result = place_name_cleaner.try_to_normalize_place_name_with_known_aliases(
            'Rääkkylässä'
        )
        assert result == 'Rääkkylä'

    def should_return_place_name_unmodified_if_it_was_not_found_from_list(self):
        result = place_name_cleaner.try_to_normalize_place_name_with_known_aliases(
            'Testimaa'
        )
        assert result == 'Testimaa'

    def should_return_region_if_it_is_asked(self):
        (
            place_name,
            region,
        ) = place_name_cleaner.try_to_normalize_place_name_with_known_aliases(
            'Rääkkylässä', True
        )
        assert place_name == 'Rääkkylä'
        assert region == 'other'

    def should_return_region_as_None_if_it_was_not_found(self):
        (
            place_name,
            region,
        ) = place_name_cleaner.try_to_normalize_place_name_with_known_aliases(
            'Testimaa', True
        )
        assert place_name == 'Testimaa'
        assert region is None


class TestPlaceNameNormalizationWithPlaceList:
    @pytest.yield_fixture(autouse=True)
    def metadata_collector(self):
        return MetadataCollector()

    def should_skip_if_place_has_coordinate_data(self):
        entry = {
            KEYS['locationName']: 'Alastarosa',
            KEYS['region']: 'other',
            KEYS['coordinates']: {
                KEYS['latitude']: '12.00',
                KEYS['longitude']: '12.00',
            },
        }

        result = place_name_cleaner.normalize_place_name_with_known_list_of_places(
            entry
        )
        assert (
            result[KEYS['locationName']] == 'Alastarosa'
        )  # Because coordinates, this name was not changed even if it could have
        assert result[KEYS['region']] == 'other'

    def should_change_name_to_one_from_list_with_same_stem(self):
        # TODO: spying the function would be nice...

        entry = {
            KEYS['locationName']: 'Aavasaksassa',
            KEYS['region']: None,
            KEYS['coordinates']: {KEYS['latitude']: None, KEYS['longitude']: None},
        }

        result = place_name_cleaner.normalize_place_name_with_known_list_of_places(
            entry
        )
        assert result[KEYS['locationName']] == 'Aavasaksa'

    def should_find_closest_match_with_jw_if_stem_was_not_found_from_list_and_cache_result(
        self, metadata_collector
    ):
        assert ('kalliokos' in place_name_cleaner.place_list_index) is False

        entry = {
            KEYS['locationName']: 'Kalliokos',
            KEYS['region']: None,
            KEYS['coordinates']: {KEYS['latitude']: None, KEYS['longitude']: None},
        }

        result = place_name_cleaner.normalize_place_name_with_known_list_of_places(
            entry, metadata_collector
        )
        assert result[KEYS['locationName']] == 'Kalliokoski'
        assert ('kalliokos' in place_name_cleaner.place_list_index) is True
        assert place_name_cleaner.place_list_index['kalliokos']['addedByKaira'] is True

        # Should have recorded to the result metadata that JW was used.
        assert (
            metadata_collector.get_metadata()['jaroWinklerFuzzyLocationNameFixFrom']
            == 'Kalliokos'
        )

    def should_use_place_as_is_if_no_jw_match_was_found(self, metadata_collector):
        entry = {
            KEYS['locationName']: 'Testikäspaikka',
            KEYS['region']: None,
            KEYS['coordinates']: {KEYS['latitude']: None, KEYS['longitude']: None},
        }

        result = place_name_cleaner.normalize_place_name_with_known_list_of_places(
            entry, metadata_collector
        )
        assert result[KEYS['locationName']] == 'Testikäspaikka'

        # Should have recorded to the metadata that place name was not found from available lists
        assert (
            metadata_collector.get_metadata()['errors']['locationNameNotFoundFromLists']
            == 2
        )


class TestNormalizePlaceUtilityFunction:
    @pytest.yield_fixture(autouse=True)
    def metadata_collector(self):
        return MetadataCollector()

    def should_not_use_name_list_if_manual_list_had_match(self, mocker):
        mocker.patch(
            'extractors.common.postprocessors.place_name_cleaner.normalize_place_name_with_known_list_of_places'
        )
        entry = {KEYS['locationName']: 'Rääkkylässä', KEYS['region']: None}

        result = place_name_cleaner.normalize_place(entry)
        assert result[KEYS['locationName']] == 'Rääkkylä'
        assert result[KEYS['region']] == 'other'
        assert (
            not place_name_cleaner.normalize_place_name_with_known_list_of_places.called
        )
