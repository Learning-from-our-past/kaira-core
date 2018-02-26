from core.utils.geo.dbhandler import Place, Location


class GeoCoder:

    @staticmethod
    def get_coordinates(location_name):
        try:
            place = Place.get(Place.name == location_name)
            return {
                'latitude': place.location.latitude,
                'longitude': place.location.longitude,
                'region': place.location.region
            }
        except (Place.DoesNotExist, Location.DoesNotExist):
            raise LocationNotFound()

    @staticmethod
    def get_empty_coordinates():
        return {'latitude': None, 'longitude': None}


class LocationNotFound(Exception):
    message = 'Coordinates not found from database'

    def __unicode__(self):
        return self.message
