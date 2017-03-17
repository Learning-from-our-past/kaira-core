from shared.geo.dbhandler import DatabaseHandler


class GeoCoder():

    def __init__(self):
        self.db = DatabaseHandler()

    def get_coordinates(self, location_name, collection):
        locations = self.db.getFromDb({"$text": {"$search": "\"" + location_name + "\""}}, collection)
        if len(locations) == 0:
            raise LocationNotFound()
        else:
            return {"latitude": locations[0]["latitude"], "longitude": locations[0]["longitude"]}

    def get_empty_coordinates(self):
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