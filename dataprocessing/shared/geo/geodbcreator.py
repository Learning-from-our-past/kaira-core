""" A simple script to create a mongodb from csv-geocode data from Geonames.com
"""

from shared.geo.dbhandler import DatabaseHandler
import csv

db = DatabaseHandler()

with open("finland_names.csv", "rU", encoding="utf8") as csvfile:
    reader = csv.DictReader(csvfile, delimiter=";")
    for row in reader:
        db.storeToDb(row, "finland")
