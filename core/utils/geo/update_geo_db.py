from core.utils.geo.dbhandler import Place, Location
import csv

"""
A script to populate location data to the Sqlite database.

Format of the csv should be following:

Name1, Name2, ... , region<karelia|other>, latitude, longitude

Basically all columns before column with content "karelia" or "other" are considered as alternative names
for the place. Empty columns as names are ignored. Latitude and longitude follow region data and should
be defined. Note that file should not have header row.

Database can be created with SQL:

CREATE TABLE Location (
  id INTEGER PRIMARY KEY,
  latitude TEXT NOT NULL,
  longitude TEXT NOT NULL,
  region TEXT NOT NULL,
  UNIQUE (latitude, longitude) ON CONFLICT IGNORE
);

CREATE TABLE Place (
  id INTEGER PRIMARY KEY,
  name TEXT NOT NULL,
  locationId INTEGER NOT NULL,
  FOREIGN KEY(locationId) REFERENCES Location(id),
  UNIQUE(name) ON CONFLICT IGNORE
);

CREATE INDEX place_name ON Place(name);

"""


def _get_names(row):
    names = []
    region_found = False
    for col in row:
        if col.lower() == 'karelia' or col.lower() == 'other':
            region_found = True
            break

        names.append(col)

    if not region_found:
        raise Exception('Row is missing region data: ' + row)

    return names


def _populate_place(place_data):

    try:
        new_location = Location.get(
            (Location.latitude == place_data['latitude']) &
            (Location.longitude == place_data['longitude']))
    except Location.DoesNotExist:
        new_location = Location.create(
            latitude=place_data['latitude'],
            longitude=place_data['longitude'],
            region=place_data['region'])

    for name in place_data['names']:
        if name:
            try:
                Place.get(Place.name == name)
            except Place.DoesNotExist:
                Place.create(
                    name=name,
                    location=new_location
                )



def update_location_db(datasheet_path):
    file = open(datasheet_path, 'r', encoding='utf-8')
    reader = csv.reader(file)

    def map_to_dict(place_data_row):
        names = _get_names(place_data_row)
        region_idx = len(names)
        return {
            'names': names,
            'region': place_data_row[region_idx],
            'latitude': place_data_row[region_idx + 1],
            'longitude': place_data_row[region_idx + 2]
        }

    place_rows = map(map_to_dict, reader)

    for place_row in place_rows:
        _populate_place(place_row)
