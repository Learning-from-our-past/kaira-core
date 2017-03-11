from book_extractors.common.base_extractor import BaseExtractor
from book_extractors.common.extraction_keys import KEYS
from book_extractors.extraction_exceptions import ShortEntryException
from shared.geo.geocoding import GeoCoder, LocationNotFound


class MetadataExtractor(BaseExtractor):

    geocoder = GeoCoder()

    def extract(self, entry, start_positions=0):
        self.page = ""
        self.name = ""
        self.short = False
        self.location = {"locationName": "", "latitude": "", "longitude": ""}
        self.location_name = ""
        self.original_text = entry['text']

        try:
            self.name= entry["name"]
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

        #note that this entry is short
        if len(entry['text']) < 200:
            # TODO: Metadata logging here self.errorLogger.logError(ShortEntryException.eType, self.currentChild)
            self.short = True

        return self._constructReturnDict()

    def _constructReturnDict(self):
        return {KEYS["name"] : self.name, KEYS["approximatePage"] : self.page,
                KEYS["farmLocation"] : self.location, KEYS["shortentry"] : self.short,
                KEYS["originalText"] : self.original_text
        }
