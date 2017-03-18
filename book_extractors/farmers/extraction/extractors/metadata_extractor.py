from book_extractors.common.extraction_keys import KEYS
from book_extractors.common.extractors.base_extractor import BaseExtractor
from shared.geo.geocoding import GeoCoder, LocationNotFound


class MetadataExtractor(BaseExtractor):
    extraction_key = KEYS['personMetadata']
    geocoder = GeoCoder()

    def extract(self, entry, extraction_results):
        page = None
        name = None
        location = {"locationName": None, "latitude": None, "longitude": None}
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

            location = {"locationName": location_name, "latitude": geo["latitude"], "longitude": geo["longitude"]}
        except KeyError:
            pass

        try:
            page = entry["approximated_page"]
        except KeyError:
            pass

        return self._add_to_extraction_results({
            KEYS["name"]: name,
            KEYS["approximatePage"]: page,
            KEYS["farmLocation"]: location,
            KEYS['originalText']: original_text}, extraction_results, 0)