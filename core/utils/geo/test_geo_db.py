import pytest
from core.utils.geo.geocoding import GeoCoder, LocationNotFound


class TestGeoDatabase:

    @pytest.fixture(scope='session')
    def geocoder(self):
        return GeoCoder()

    def should_get_coordinates_by_name(self, geocoder):
        result = geocoder.get_coordinates('Kemijärvi')
        assert result == {
            'latitude': '66.71',
            'longitude': '27.43',
            'region': 'other'
        }

    def should_raise_error_when_coordinates_for_place_was_not_found(self, geocoder):
        with pytest.raises(LocationNotFound):
            geocoder.get_coordinates('Arkham')
