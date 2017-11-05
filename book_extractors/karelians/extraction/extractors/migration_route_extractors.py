import re
from book_extractors.common.postprocessors import place_name_cleaner
from book_extractors.common.extraction_keys import KEYS
from book_extractors.common.extractors.base_extractor import BaseExtractor
from book_extractors.karelians.extraction.extractors.bnf_parsers import migration_parser
from book_extractors.extraction_pipeline import ExtractionPipeline, configure_extractor
from support_datasheets import location_name_white_list
from shared import regexUtils, text_utils
from shared.geo.geocoding import GeoCoder, LocationNotFound
from book_extractors.karelians.extraction.postprocessors.returned_to_karelia import check_if_person_returned_karelia_in_between_wars

MAX_PLACE_NAME_LENGTH = 15
MIN_PLACE_NAME_LENGTH = 4
# Known words which often after in migration results which should clip the string which is parsed to list of places
KNOWN_INCORRECT_WORDS_IN_MIGRATION_LISTS = ['rouva', 'saima(?!a)', 'muutasuinp']

def validate_location_name(entry_name, geocoordinates):
    if len(entry_name) > MAX_PLACE_NAME_LENGTH and geocoordinates['latitude'] is None and geocoordinates['longitude'] is None:
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

    if len(entry_name) < MIN_PLACE_NAME_LENGTH:
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

    return entry_name


def validate_village_name(village_name):
    if village_name is not None and (len(village_name) > MAX_PLACE_NAME_LENGTH or len(village_name) < MIN_PLACE_NAME_LENGTH):
        return None
    else:
        return village_name


class FinnishLocationsExtractor(BaseExtractor):
    """
    Tries to extract the locations of the person in oter places than karelia
    """
    OTHER_REGION_ID = 'other'
    extraction_key = 'finnishLocations'

    def __init__(self, key_of_cursor_location_dependent, options, dependencies_contexts=None):
        super(FinnishLocationsExtractor, self).__init__(key_of_cursor_location_dependent, options)
        self.LOCATION_PATTERN = r"Muut\.?,?\s?(?:asuinp(\.|,)?){i<=1}(?::|;)?(?P<asuinpaikat>[A-ZÄ-Öa-zä-ö\s\.,0-9——-]*—)"
        self.LOCATION_OPTIONS = (re.UNICODE | re.IGNORECASE)

    def _extract(self, entry, extraction_results, extraction_metadata):
        location_listing_results = self._find_locations(entry['text'])

        return self._add_to_extraction_results({
            KEYS["otherlocations"]: location_listing_results[0]},
            extraction_results, extraction_metadata, location_listing_results[1])

    def _postprocess(self, entry, extraction_results, extraction_metadata):
        places = extraction_results[self.extraction_key][KEYS["otherlocations"]]

        for i in range(0, len(places)):
            places[i] = place_name_cleaner.normalize_place_name_with_known_list_of_places(places[i])

        return extraction_results, extraction_metadata

    def _find_locations(self, text):
        # Replace all weird invisible white space characters with regular space
        text = re.sub(r"\s", r" ", text)

        cursor_location = 0
        location_entries = []

        def _get_location_entries(location):
            location_records = []
            # If there is municipality information, use it as an main entry name
            village_name = None

            if 'municipality' in location:
                # Try to normalize place names first so that the coordinate fetch from DB might work better
                entry_name, entry_region = place_name_cleaner.try_to_normalize_place_name_with_known_aliases(location['municipality'], True)
                village_name = place_name_cleaner.try_to_normalize_place_name_with_known_aliases(location['place'])
            else:
                entry_name, entry_region = place_name_cleaner.try_to_normalize_place_name_with_known_aliases(location['place'], True)

            def get_coordinates_by_name(place_name):
                try:
                    return GeoCoder.get_coordinates(place_name)
                except LocationNotFound:
                    return {"latitude": None, "longitude": None}

            geocoordinates = get_coordinates_by_name(entry_name)

            entry_name = validate_location_name(entry_name, geocoordinates)
            village_name = validate_village_name(village_name)

            # FIXME: Village coordinates are not trivial to deduce because of multiple same named
            # villages and locations in map name data sets.
            village_coordinates = {"latitude": None, "longitude": None}

            village_information = {
                KEYS["otherlocation"]: village_name or None,
                KEYS["othercoordinate"]: {
                    KEYS["latitude"]: village_coordinates["latitude"],
                    KEYS["longitude"]: village_coordinates["longitude"]
                }
            }

            moved_in = None
            moved_out = None

            def get_location_entry():
                return {
                    KEYS["otherlocation"]: entry_name,
                    KEYS["othercoordinate"]: {
                        KEYS["latitude"]: geocoordinates["latitude"],
                        KEYS["longitude"]: geocoordinates["longitude"]
                    },
                    KEYS["movedOut"]: moved_out,
                    KEYS["movedIn"]: moved_in,
                    KEYS["region"]: entry_region or self.OTHER_REGION_ID,
                    KEYS["village"]: village_information
                }

            if 'year_information' in location:
                for migration in location['year_information']:
                    if 'moved_in' in migration:
                        moved_in = text_utils.int_or_none(migration['moved_in'])
                    else:
                        moved_in = None

                    if 'moved_out' in migration:
                        moved_out = text_utils.int_or_none(migration['moved_out'])
                    else:
                        moved_out = None

                    location_records.append(
                        # FIXME: Refactor this to the _postprocess method?
                        place_name_cleaner.clean_place_name(
                            get_location_entry()
                        )
                    )
            else:
                location_records.append(
                    # FIXME: Refactor this to the _postprocess method?
                    place_name_cleaner.clean_place_name(
                        get_location_entry()
                    )
                )

            return location_records

        try:
            found_locations = regexUtils.safe_search(self.LOCATION_PATTERN, text, self.LOCATION_OPTIONS)
            cursor_location = found_locations.end()
            locations = found_locations.group("asuinpaikat")
            locations = self._clean_locations_string(locations)

            # Parse location string with BNF parser
            parsed_locations = migration_parser.parse_locations(locations)

            try:
                for loc in parsed_locations:
                    location_entries += _get_location_entries(loc)
            except InvalidLocationException as e:
                pass
        except regexUtils.RegexNoneMatchException:
            self.metadata_collector.add_error_record('otherLocationNotFound', 5)

        return location_entries, cursor_location

    @staticmethod
    def _clean_locations_string(locations):
        locations = locations.strip(",")
        locations = locations.strip(".")
        locations = locations.strip()
        locations = re.sub(r"([a-zä-ö])(?:\s|\-)([a-zä-ö])", r"\1\2", locations)
        locations = locations.lstrip()

        # if string contains word some of known incorrect words, split string from that position
        lowercase = locations.lower()
        for word in KNOWN_INCORRECT_WORDS_IN_MIGRATION_LISTS:
            position = re.search(word, lowercase)

            if position is not None:
                locations = locations[0:position.start()]

        return locations


class KarelianLocationsExtractor(BaseExtractor):
    """
    Tries to extract the locations of the person in karelia.
    """
    KARELIAN_REGION_ID = 'karelia'

    extraction_key = 'karelianLocations'

    def __init__(self, key_of_cursor_location_dependent, options, dependencies_contexts=None):
        super(KarelianLocationsExtractor, self).__init__(key_of_cursor_location_dependent, options)
        self.LOCATION_PATTERN = r"Asuinp{s<=1}\.?,?\s?(?:Karjalassa){i<=1}(?::|;)?(?P<asuinpaikat>[A-ZÄ-Öa-zä-ö\s\.,0-9——-]*)(?=\.?\s(Muut))"  # r"Muut\.?,?\s?(?:asuinp(\.|,)){i<=1}(?::|;)?(?P<asuinpaikat>[A-ZÄ-Öa-zä-ö\s\.,0-9——-]*)(?=—)"
        self.LOCATION_OPTIONS = (re.UNICODE | re.IGNORECASE)

    def _extract(self, entry, extraction_results, extraction_metadata):
        location_listing_results = self._find_locations(entry['text'])

        return self._add_to_extraction_results({
            KEYS["karelianlocations"]: location_listing_results[0],
        }, extraction_results, extraction_metadata, location_listing_results[1])

    def _postprocess(self, entry, extraction_results, extraction_metadata):
        places = extraction_results[self.extraction_key][KEYS["karelianlocations"]]

        for i in range(0, len(places)):
            places[i] = place_name_cleaner.normalize_place_name_with_known_list_of_places(places[i])

        return extraction_results, extraction_metadata

    def _find_locations(self, text):
        # Replace all weird invisible white space characters with regular space
        text = re.sub(r"\s", r" ", text)

        cursor_location = 0
        location_entries = []

        def _get_location_entries(location):
            # If there is municipality information, use it as an main entry name
            village_name = None
            location_records = []

            if 'municipality' in location:
                # Try to normalize place names first so that the coordinate fetch from DB might work better
                entry_name, entry_region = place_name_cleaner.try_to_normalize_place_name_with_known_aliases(location['municipality'], True)
                village_name = place_name_cleaner.try_to_normalize_place_name_with_known_aliases(location['place'])
            else:
                entry_name, entry_region = place_name_cleaner.try_to_normalize_place_name_with_known_aliases(location['place'], True)

            def get_coordinates_by_name(place_name):
                try:
                    return GeoCoder.get_coordinates(place_name)
                except LocationNotFound:
                    return {"latitude": None, "longitude": None}

            geocoordinates = get_coordinates_by_name(entry_name)

            entry_name = validate_location_name(entry_name, geocoordinates)
            village_name = validate_village_name(village_name)

            village_coordinates = {"latitude": None, "longitude": None}
            if village_name is not None:
                village_coordinates = get_coordinates_by_name(village_name)

            village_information = {
                KEYS["karelianlocation"]: village_name or None,
                KEYS["kareliancoordinate"]: {
                    KEYS["latitude"]: village_coordinates["latitude"],
                    KEYS["longitude"]: village_coordinates["longitude"]
                }
            }

            moved_in = None
            moved_out = None

            def get_location_entry():
                return {
                    KEYS["karelianlocation"]: entry_name,
                    KEYS["kareliancoordinate"]: {
                        KEYS["latitude"]: geocoordinates["latitude"],
                        KEYS["longitude"]: geocoordinates["longitude"]
                    },
                    KEYS["movedOut"]: moved_out,
                    KEYS["movedIn"]: moved_in,
                    KEYS["region"]: entry_region or self.KARELIAN_REGION_ID,
                    KEYS["village"]: village_information
                }

            if 'year_information' in location:
                for migration in location['year_information']:
                    if 'moved_in' in migration:
                        moved_in = text_utils.int_or_none(migration['moved_in'])
                    else:
                        moved_in = None

                    if 'moved_out' in migration:
                        moved_out = text_utils.int_or_none(migration['moved_out'])
                    else:
                        moved_out = None

                    location_records.append(
                        # FIXME: Refactor this to the _postprocess method?
                        place_name_cleaner.clean_place_name(
                            get_location_entry()
                        )
                    )
            else:
                location_records.append(
                    # FIXME: Refactor this to the _postprocess method?
                    place_name_cleaner.clean_place_name(
                        get_location_entry()
                    )
                )

            return location_records

        try:
            found_locations = regexUtils.safe_search(self.LOCATION_PATTERN, text, self.LOCATION_OPTIONS)
            cursor_location = found_locations.end()
            locations = found_locations.group("asuinpaikat")
            locations = self._clean_locations(locations)

            # Parse location string with BNF parser
            parsed_locations = migration_parser.parse_locations(locations)

            try:
                for loc in parsed_locations:
                    location_entries += _get_location_entries(loc)
            except InvalidLocationException as e:
                pass
        except regexUtils.RegexNoneMatchException as e:
            self.metadata_collector.add_error_record('karelianLocationNotFound', 5)

        return location_entries, cursor_location

    @staticmethod
    def _clean_locations(locations):
        locations = locations.strip(",")
        locations = locations.strip(".")
        locations = locations.strip()

        # Strip away spaces and hyphens from center of words
        locations = re.sub(r"([a-zä-ö])(?:\s|\-)([a-zä-ö])", r"\1\2", locations)

        # if string contains word some of known incorrect words, split string from that position
        lowercase = locations.lower()
        for word in KNOWN_INCORRECT_WORDS_IN_MIGRATION_LISTS:
            position = re.search(word, lowercase)

            if position is not None:
                locations = locations[0:position.start()]

        return locations.lstrip()


class MigrationRouteExtractor(BaseExtractor):
    extraction_key = 'migrationHistory'

    def __init__(self, key_of_cursor_location_dependent, options, dependencies_contexts=None):
        super(MigrationRouteExtractor, self).__init__(key_of_cursor_location_dependent, options)

        self._sub_extraction_pipeline = ExtractionPipeline([
            configure_extractor(KarelianLocationsExtractor),
            configure_extractor(FinnishLocationsExtractor),
        ])

    def _extract(self, entry, extraction_results, extraction_metadata):
        results = self._sub_extraction_pipeline.process(entry)

        return self._add_to_extraction_results({
            KEYS["locations"]: results[0]['karelianLocations'][KEYS['karelianlocations']] + results[0]['finnishLocations'][KEYS['otherlocations']]
        },
            extraction_results,
            extraction_metadata,
            cursor_location=results[1]['finnishLocations']['cursorLocation'])

    def _postprocess(self, entry, extraction_results, extraction_metadata):
        self._get_output_path(extraction_results)['migrationHistory'][KEYS["returnedkarelia"]] = check_if_person_returned_karelia_in_between_wars(self._get_output_path(extraction_results)['migrationHistory']['locations'], self.metadata_collector)
        return extraction_results, extraction_metadata


class LocationThresholdException(Exception):
    message = "Locations couldn't be found from db"

    def __unicode__(self):
        return repr(self.message)


class InvalidLocationException(Exception):
    message = "Location name likely not a valid place: "

    def __init__(self, place_name):
        self._place_name = place_name

    def __unicode__(self):
        return repr(self.message + self._place_name)
