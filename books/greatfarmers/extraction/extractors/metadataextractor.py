from books.greatfarmers.extraction.extractors.baseExtractor import BaseExtractor
from books.greatfarmers.extractionkeys import KEYS
from books.greatfarmers.extraction.extractionExceptions import ShortEntryException
from shared.geo.geocoding import GeoCoder, LocationNotFound


class MetadataExtractor(BaseExtractor):

    geocoder = GeoCoder()
    def extract(self, text, entry):

        self.page = ""
        self.name = ""
        self.short = False
        self.location = {"locationName": "", "latitude": "", "longitude": ""}
        self.location_name = ""

        try:
            self.name= entry["xml"].attrib["name"]
        except KeyError as e:
            pass

        try:
            self.location_name = entry["xml"].attrib["location"]
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
            self.page = entry["xml"].attrib["approximated_page"]
        except KeyError as e:
            pass

        #note that this entry is short
        if len(text) < 200:
            self.errorLogger.logError(ShortEntryException.eType, self.currentChild)
            self.short = True

        return self._constructReturnDict()

    def _constructReturnDict(self):
        return {KEYS["name"] : self.name, KEYS["approximatePage"] : self.page,
                KEYS["farmLocation"] : self.location, KEYS["shortentry"] : self.short
                }
