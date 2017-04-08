from shared.geo.dbhandler import DatabaseHandler
from math import radians, cos, sin, asin, sqrt

class GeoCoder:

    loc_count = 0
    mul_count = 0
    all_locations_count = 0
    long_distance_error = 0

    def __init__(self):
        self.db = DatabaseHandler()

    @staticmethod
    def haversine(lon1, lat1, lon2, lat2):
        """
        Calculate the great circle distance between two points 
        on the earth (specified in decimal degrees)
        http://stackoverflow.com/questions/15736995/how-can-i-quickly-estimate-the-distance-between-two-latitude-longitude-points
        """
        # convert decimal degrees to radians
        lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
        # haversine formula
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        c = 2 * asin(sqrt(a))
        km = 6367 * c
        return km

    def get_coordinates(self, location_name, collection):
        locations = self.db.get_from_db({"$text": {"$search": "\"" + location_name + "\""}}, collection)
        if len(locations) == 0:
            raise LocationNotFound()
        else:
            GeoCoder.loc_count += 1
            if len(locations) > 1:
                # TODO: WIP. We should figure out which location to use for geoname. There is multiple locations for each name (1.95 on avg)
                # This is difficult since how do we know which locations should we use? It would be easy with only A class locations but we need
                # P class which however includes small villages and locations which have more likely overlapping names,
                result = []
                for idx, loc in enumerate(locations):
                    for n in locations[idx+1:]:
                        result.append(self.haversine(float(loc['longitude']), float(loc['latitude']), float(n['longitude']), float(n['latitude'])))

                dist = max(result)
                if dist > 100:
                    print('long distance error', dist)
                    GeoCoder.long_distance_error += 1

                print('Multiple locations', GeoCoder.mul_count, '/', GeoCoder.loc_count, 'on average', GeoCoder.all_locations_count / GeoCoder.loc_count, 'long distance errors', GeoCoder.long_distance_error)

            return {"latitude": locations[0]["latitude"], "longitude": locations[0]["longitude"]}

    @staticmethod
    def get_empty_coordinates():
        return {"latitude" : None, "longitude": None}

    def get_coordinates_geojson(self, location_name, collection):
        location = self.get_coordinates(location_name, collection)

        return {
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": [float(location["longitude"]),float(location["latitude"])],
        },
        "properties": {
                "locationName": location_name
            }

        }

    def get_empty_geojson(self):
         return {
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": [None, None],
        },
        "properties": {
                "locationName": None
            }

        }


class LocationNotFound(Exception):
    message = u"Coordinates not found from database"
    details = u""
    eType = "COORDINATES NOT FOUND"

    def __init__(self):
        pass

    def __unicode__(self):
        return self.message


if __name__ == "__main__":
    coder = GeoCoder()