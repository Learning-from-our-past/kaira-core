import json
import collections
import csv
import nltk.stem.snowball as snowball
import jellyfish
from extractors.common.extraction_keys import KEYS

"""
Post processor function which tries to find given place name from list of manually fixed place names so that
Finnish difficult conjugations or typos can be resolved to a correct Place name. As a bonus fills in region when
it is recorded in the Place name list. List itself was generated from csv with karelian-db repository's 
fix_place_names script. 

This processor should be run for Place names which are in conjugated format, for example birth places, which in karelian
books are usually written in form of "Ahlaisissa". Some conjugations are difficult to deal with naive Snowball stemmer 
and many OCR typos also seem to trip stemmer. Therefore a list of around 2500 place names were corrected by hand and rest
should be possible to merge with stemmer and string distance metric such as Jaro-Winkler.  
"""
manually_fixed_place_names_file = open('support_datasheets/place_names_with_alternative_forms.json', encoding='utf8')
manually_fixed_place_names = json.load(manually_fixed_place_names_file)
stemmer = snowball.SnowballStemmer('finnish')
manual_place_name_index = {}

"""
Every place name should be found from existing list of place names when searched by conservative Jaro-Winkler distance
of stemmed form of the name. This should minimize the problem of creating useless unique place names to the result set just
because same place name has slight difference in the end of the word such as conjugation.
"""
list_of_known_places_file = open('support_datasheets/place_name_list.csv', encoding='utf8')
list_of_known_places = list(csv.DictReader(list_of_known_places_file))
place_list_index = collections.OrderedDict()

# Create a hash map which has as a key different writing styles of place names
# which refer to correct data entry for those place names
for key, item in manually_fixed_place_names.items():
    manual_place_name_index[key] = item
    for name in item['alternative_stemmed_names']:
        manual_place_name_index[name] = item

# Create starting dict for place names list which is later used for finding
# names for places which likely have conjugated or otherwise problematic name.
for item in list_of_known_places:
    place_list_index[item['stemmedName']] = item

manually_fixed_place_names_file.close()
list_of_known_places_file.close()


def try_to_normalize_place_name_with_known_aliases(location_name, return_region=False):
    """
    Try to normalize the name by using a list of known typos and aliases for the given place.
    place_names_with_alternative_forms.json contains list of place names and common typos and aliases for them. Using
    this manually created list we can normalize some of the most common typos in the data.

    If normalized name is not found, just return the name unchanged.

    If return_region is set true, this function returns possible region info too.

    :param location_name:
    :param return_region:
    :return:
    """
    fixed_name = location_name
    region = None

    if location_name:
        search_key = stemmer.stem(location_name)
        if search_key in manual_place_name_index:
            fixed_name = manual_place_name_index[search_key]['fixed_name']
            region = manual_place_name_index[search_key]['region']

    if return_region:
        return fixed_name, region
    else:
        return fixed_name


def normalize_place_name_with_known_list_of_places(location_entry, metadata_collector=None):
    """
    Try to normalize name to known places in the database. We have a list of place names from
    database. Try to avoid creating completely new place names because of some minor typo differences
    by finding closest match from existing place names with Jaro-Winkler distance.
    
    :param location_entry:
    :param metadata_collector:
    :return:
    """
    jaro_winkler_threshold = 0.97

    # If place has coordinates, it is likely a proper name already. Do nothing.
    if 'coordinates' in location_entry and location_entry['coordinates']['longitude']:
        return location_entry

    search_key = stemmer.stem(location_entry[KEYS['locationName']])

    if search_key in place_list_index:
        old_name = location_entry[KEYS['locationName']]
        location_entry[KEYS['locationName']] = place_list_index[search_key]['name']

        # If found name was cached by Kaira, mark it to the metadata
        if place_list_index[search_key]['addedByKaira'] is True and metadata_collector is not None:
            metadata_collector.set_metadata_property('jaroWinklerFuzzyLocationNameFixFrom', old_name)

        return location_entry
    else:
        best_match = None
        rating = 0

        for key, item in place_list_index.items():
            jw_rating = jellyfish.jaro_winkler(key, search_key)

            if jw_rating > rating:
                rating = jw_rating
                best_match = item

        if best_match is not None and rating >= jaro_winkler_threshold:
            old_name = location_entry[KEYS['locationName']]
            location_entry[KEYS['locationName']] = best_match['name']

            if metadata_collector is not None:
                metadata_collector.set_metadata_property('jaroWinklerFuzzyLocationNameFixFrom', old_name)

            # Cache this result for faster lookup in following persons:
            place_list_index[search_key] = {
                'name': best_match['name'],
                'region': '',
                'stemmedName': search_key,
                'extractedName': old_name,
                'latitude': '',
                'longitude': '',
                'addedByKaira': True
            }

            return location_entry
        else:
            # Could not find any match so do not modify place name in any way
            if metadata_collector is not None:
                metadata_collector.add_error_record('locationNameNotFoundFromLists', 2)
            return location_entry


def normalize_place(location_entry, metadata_collector=None):
    """
    Run both normalization processes for location_entry. This is utility function for cases when both
    normalizations can be run sequentially. If fix from manual json list is found, we do not need to run the
    known places list check.

    :param location_entry:
    :param metadata_collector:
    :return:
    """

    fixed_name, region = try_to_normalize_place_name_with_known_aliases(location_entry[KEYS['locationName']], True)

    if location_entry[KEYS['locationName']] != fixed_name:
        location_entry[KEYS['locationName']] = fixed_name
        location_entry[KEYS['region']] = region
    else:
        location_entry = normalize_place_name_with_known_list_of_places(location_entry, metadata_collector)

    return location_entry


def clean_place_name(location_entry):
    """
    Utility function to clean up the locationName and stemmedName if one is available from useless
    characters.
    :param location_entry: 
    :return: 
    """
    location_entry[KEYS['locationName']] = location_entry[KEYS['locationName']].strip('-')

    if KEYS['stemmedName'] in location_entry:
        location_entry[KEYS['stemmedName']] = location_entry[KEYS['stemmedName']].strip('-')

    return location_entry
