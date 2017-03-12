from book_extractors.common.base_extractor import BaseExtractor
from book_extractors.common.extraction_keys import KEYS
from book_extractors.extraction_exceptions import ShortEntryException
from shared.geo.geocoding import GeoCoder, LocationNotFound


class MetadataExtractor(BaseExtractor):

    geocoder = GeoCoder()

    def extract(self, entry, start_positions=0):
        page = ""
        name = ""
        short = False
        location = {"locationName": "", "latitude": "", "longitude": ""}
        original_text = entry['text']

        try:
            name = entry["name"]
        except KeyError:
            pass

        try:
            location_name = entry["location"]
            try:
                geo = self.geocoder.get_coordinates(location_name.lower(), "finland")

            except LocationNotFound:
                geo = self.geocoder.get_empty_coordinates()

            location = {"locationName": location_name,
                             "latitude": geo["latitude"],
                             "longitude": geo["longitude"]}
        except KeyError:
            pass

        try:
            page = entry["approximated_page"]
        except KeyError:
            pass

        # note that this entry is short
        if len(entry['text']) < 200:
            # TODO: Metadata logging here self.errorLogger.logError(ShortEntryException.eType, self.currentChild)
            short = True

        return self._constructReturnDict({KEYS["name"]: name,
                                          KEYS["approximatePage"]: page,
                                          KEYS["farmLocation"] : location,
                                          KEYS["shortentry"] : short,
                                          KEYS["originalText"] : original_text}, 0)
