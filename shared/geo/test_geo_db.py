import pytest
from shared.geo.dbhandler import Place


class TestGeoDatabase:

    def should_connect_to_the_db(self):
        # Query should run ok
        result = len(Place.select().execute())
        assert result == 0
