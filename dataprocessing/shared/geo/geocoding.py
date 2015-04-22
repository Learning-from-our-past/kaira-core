from shared.geo.dbhandler import DatabaseHandler


class GeoCoder():

    def __init__(self):
        self.db = DatabaseHandler()

    def get_coordinates(self, location_name, collection):
        locations = self.db.getFromDb({"$text": {"$search": location_name}}, collection)
        print(locations)
        if len(locations) == 0:
            raise LocationNotFound()
        else:
            return {"latitude": locations[0]["latitude"], "longitude": locations[0]["longitude"]}





class LocationNotFound(Exception):
    message = u"Coordinates not found from database"
    details = u""
    eType = "OTHER"

    def __init__(self):
        pass

    def __unicode__(self):
        return self.message


if __name__ == "__main__":
    coder = GeoCoder()
    print(coder.get_coordinates("Kirvu", "russia"))