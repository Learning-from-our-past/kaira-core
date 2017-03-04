from books.karelians.extraction.extractors.baseExtractor import BaseExtractor
from books.karelians.extractionkeys import KEYS
from interface.valuewrapper import ValueWrapper
from books.karelians.extraction.extractionExceptions import KarelianLocationException
from shared import regexUtils
import re
from shared.geo.geocoding import GeoCoder, LocationNotFound
from books.karelians.extraction.extractors.bnf_parsers import migration_parser
from names import location_name_white_list


class KarelianLocationsExtractor(BaseExtractor):
    """ Tries to extract the locations of the person in karelia.
    """
    geocoder = GeoCoder()
    KARELIAN_REGION_ID = 'karelia'
    MAX_PLACE_NAME_LENGTH = 15
    MIN_PLACE_NAME_LENGTH = 4

    def extract(self, text):
        self.LOCATION_PATTERN = r"Asuinp{s<=1}\.?,?\s?(?:Karjalassa){i<=1}(?::|;)?(?P<asuinpaikat>[A-ZÄ-Öa-zä-ö\s\.,0-9——-]*)(?=\.?\s(Muut))" # r"Muut\.?,?\s?(?:asuinp(\.|,)){i<=1}(?::|;)?(?P<asuinpaikat>[A-ZÄ-Öa-zä-ö\s\.,0-9——-]*)(?=—)"
        self.LOCATION_OPTIONS = (re.UNICODE | re.IGNORECASE)
        self.SPLIT_PATTERN1 = r"(?P<place>[A-ZÄ-Öa-zä-ö-]+)\s?(?P<years>[\d,\.\s—-]*)" # r"(?P<place>[A-ZÄ-Öa-zä-ö\s-]+)\s(?P<years>[\d,\.\s—-]*)"
        self.SPLIT_OPTIONS1 = (re.UNICODE | re.IGNORECASE)
        self.coordinates_notfound = False   # used to limit error logging to only single time
        self.returned = ""
        self.locations = ""
        self.location_listing = []
        self.location_error = False
        self._find_locations(text)

        return self._constructReturnDict()

    def _find_locations(self, text):
        # Replace all weird invisible white space characters with regular space
        text = re.sub(r"\s", r" ", text)

        try:
            found_locations = regexUtils.safeSearch(self.LOCATION_PATTERN, text, self.LOCATION_OPTIONS)
            self.matchFinalPosition = found_locations.end()
            self.locations = found_locations.group("asuinpaikat")
            self._clean_locations()

            parsed_locations = migration_parser.parse_locations(self.locations)

            try:
                for location in parsed_locations:
                    self._create_location_entry(location)
            except InvalidLocationException:
                pass

        except regexUtils.RegexNoneMatchException as e:
            self.errorLogger.logError(KarelianLocationException.eType, self.currentChild)
            self.location_error = KarelianLocationException.eType

    def _clean_locations(self):
        self.locations = self.locations.strip(",")
        self.locations = self.locations.strip(".")
        self.locations = self.locations.strip()

        # Strip away spaces and hyphens from center of words
        self.locations = re.sub(r"([a-zä-ö])(?:\s|\-)([a-zä-ö])", r"\1\2", self.locations)

        self.locations = self.locations.lstrip()

    def _create_location_entry(self, location):
        # If there is municipality information, use it as an main entry name
        village_name = None

        if 'municipality' in location:
            entry_name = location['municipality']
            village_name = location['place']
        else:
            entry_name = location['place']

        def get_coordinates_by_name(place_name):
            try:
                return self.geocoder.get_coordinates(place_name, "russia")
            except LocationNotFound:
                if not self.coordinates_notfound:
                    self.coordinates_notfound = True
                return {"latitude": "", "longitude": ""}

        geocoordinates = get_coordinates_by_name(entry_name)

        if len(entry_name) > self.MAX_PLACE_NAME_LENGTH and geocoordinates['latitude'] == '' and geocoordinates['longitude'] == '':
            name_is_ok = False

            # Check if there is white list pattern which matches to current name
            for pattern in location_name_white_list.WHITE_LIST['patterns']:
                result = pattern['find'].subn(pattern['replace'], entry_name)

                if result[1] > 0:  # Replace success, end loop
                    entry_name = result[0]
                    name_is_ok = True
                    break

            if not name_is_ok:
                raise InvalidLocationException(entry_name)

        if len(entry_name) < self.MIN_PLACE_NAME_LENGTH:
            name_is_ok = False
            ln = entry_name.lower()
            if ln in location_name_white_list.WHITE_LIST['names']:
                # The name is in white list, so it is ok to use!
                # Also check if there is known alias for it
                name_is_ok = True
                if 'alias' in location_name_white_list.WHITE_LIST['names'][ln]:
                    entry_name = location_name_white_list.WHITE_LIST['names'][ln]['alias']

            if not name_is_ok:
                raise InvalidLocationException(entry_name)

        if village_name is not None and (len(village_name) > self.MAX_PLACE_NAME_LENGTH or len(village_name) < self.MIN_PLACE_NAME_LENGTH):
            village_name = None

        village_coordinates = {"latitude": "", "longitude": ""}
        if village_name is not None:
            village_coordinates = get_coordinates_by_name(village_name)

        village_information = {
            KEYS["karelianlocation"]: ValueWrapper(village_name or None),
            KEYS["kareliancoordinate"]: ValueWrapper({
                KEYS["latitude"]: village_coordinates["latitude"],
                KEYS["longitude"]: village_coordinates["longitude"]
            })
        }

        moved_in = ''
        moved_out = ''

        def add_location_to_list():
            self.location_listing.append(ValueWrapper({
                KEYS["karelianlocation"]: ValueWrapper(entry_name),
                KEYS["kareliancoordinate"]: ValueWrapper({
                    KEYS["latitude"]: ValueWrapper(geocoordinates["latitude"]),
                    KEYS["longitude"]: ValueWrapper(geocoordinates["longitude"])
                }),
                KEYS["movedOut"]: ValueWrapper(moved_out),
                KEYS["movedIn"]: ValueWrapper(moved_in),
                KEYS["region"]: self.KARELIAN_REGION_ID,
                KEYS["village"]: ValueWrapper(village_information)
            }))

        if 'year_information' in location:
            for migration in location['year_information']:
                if 'moved_in' in migration:
                    moved_in = migration['moved_in']
                else:
                    moved_in = ''

                if 'moved_out' in migration:
                    moved_out = migration['moved_out']
                else:
                    moved_out = ''

                try:
                    if 41 <= int(moved_in) <= 43:
                        self.returned = True
                except ValueError:
                    pass

                add_location_to_list()
        else:
            add_location_to_list()

    def _constructReturnDict(self):
        loc = ValueWrapper(self.location_listing)
        loc.error = self.location_error
        return {KEYS["karelianlocations"]: loc,
                KEYS["returnedkarelia"]: ValueWrapper(self.returned),
                KEYS["karelianlocationsCount"]: ValueWrapper(len(self.location_listing))}

# FIXME: Move this to common module to be used by both location extractor classes. Or maybe move both location extractor classes to same module...?
class InvalidLocationException(Exception):
    message = "Location name likely not a valid place: "

    def __init__(self, place_name):
        self._place_name = place_name

    def __unicode__(self):
        return repr(self.message + self._place_name)
