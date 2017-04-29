import json
import nltk.stem.snowball as snowball
from book_extractors.common.extraction_keys import KEYS

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
data_file = open('support_datasheets/place_names_with_alternative_forms.json', encoding='utf8')
fixed_place_names = json.load(data_file)
stemmer = snowball.SnowballStemmer('finnish')
place_name_index = {}

# Create a hash map which has as a key different writing styles of place names
# which refer to correct data entry for those place names
for key, item in fixed_place_names.items():
    place_name_index[key] = item
    for name in item['alternative_stemmed_names']:
        place_name_index[name] = item


def try_to_normalize_place_name(location_entry):
    search_key = stemmer.stem(location_entry[KEYS['locationName']])
    if search_key in place_name_index:
        location_entry[KEYS['locationName']] = place_name_index[search_key]['fixed_name']
        location_entry[KEYS['region']] = place_name_index[search_key]['region']

    return location_entry
