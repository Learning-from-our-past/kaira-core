from books.farmers.extraction.extractors.baseExtractor import BaseExtractor
from books.farmers.extractionkeys import KEYS
from interface.valuewrapper import ValueWrapper
from shared.geo.geocoding import GeoCoder, LocationNotFound
import re


class MetadataExtractor(BaseExtractor):

    geocoder = GeoCoder()
    def extract(self, text, entry):

        self.page = ""
        self.name = ""
        self.location = {"locationName": ValueWrapper(""), "latitude": ValueWrapper(""), "longitude": ValueWrapper("")}
        self.location_name = ""

        try:
            self.name= entry["xml"].attrib["name"]
        except KeyError as e:
            pass

        try:
            self.location_name = entry["xml"].attrib["location"]
            print(self.location_name)
            try:
                geo = self.geocoder.get_coordinates(self.location_name.lower(), "finland")

            except LocationNotFound as e:
                geo = self.geocoder.get_empty_coordinates()

            print(geo["latitude"])
            self.location = {"locationName": ValueWrapper(self.location_name),
                             "latitude": ValueWrapper(geo["latitude"]),
                             "longitude": ValueWrapper(geo["longitude"])}


        except KeyError as e:
            pass

        try:
            self.page = entry["xml"].attrib["approximated_page"]
        except KeyError as e:
            pass
        return self._constructReturnDict()

    def _constructReturnDict(self):


        return {KEYS["name"] : ValueWrapper(self.name), KEYS["approximatePage"] : ValueWrapper(self.page),
                KEYS["farmLocation"] : ValueWrapper(self.location)
                }
