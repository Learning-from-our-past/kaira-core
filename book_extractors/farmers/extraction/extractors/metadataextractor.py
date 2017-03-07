from book_extractors.common.base_extractor import BaseExtractor
from book_extractors.farmers.extractionkeys import KEYS
from shared.geo.geocoding import GeoCoder, LocationNotFound


class MetadataExtractor(BaseExtractor):

    geocoder = GeoCoder()

    def extract(self, text, entry):
        self.page = ""
        self.name = ""
        self.location = {"locationName": "", "latitude": "", "longitude": ""}
        self.location_name = ""

        try:
            self.name = entry["name"]
        except KeyError as e:
            pass

        try:
            self.location_name = entry["location"]
            try:
                geo = self.geocoder.get_coordinates(self.location_name.lower(), "finland")

            except LocationNotFound as e:
                geo = self.geocoder.get_empty_coordinates()

            self.location = {"locationName": self.location_name,
                             "latitude": geo["latitude"],
                             "longitude": geo["longitude"]}


        except KeyError as e:
            pass

        try:
            self.page = entry["approximated_page"]
        except KeyError as e:
            pass
        return self._constructReturnDict()

    def _constructReturnDict(self):
        return {KEYS["name"] : self.name, KEYS["approximatePage"] : self.page,
                KEYS["farmLocation"] : self.location
                }
