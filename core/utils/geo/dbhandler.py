from peewee import *

database_connection = SqliteDatabase(
    'support_datasheets/location.db', threadlocals=True
)
database_connection.connect()


class Location(Model):
    latitude = TextField()
    longitude = TextField()
    region = TextField()

    class Meta:
        database = database_connection


class Place(Model):
    name = TextField()
    location = ForeignKeyField(
        db_column='locationId', null=True, rel_model=Location, to_field='id'
    )

    class Meta:
        database = database_connection
