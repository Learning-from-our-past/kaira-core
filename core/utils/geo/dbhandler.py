from peewee import SqliteDatabase, TextField, Model, ForeignKeyField

database_connection = SqliteDatabase('support_datasheets/location.db')
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
        column_name='locationId', null=True, model=Location, field='id'
    )

    class Meta:
        database = database_connection
