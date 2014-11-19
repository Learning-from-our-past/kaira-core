#!/usr/bin/env python

# Requires GDAL with python installed https://pypi.python.org/pypi/GDAL

import osgeo.ogr as ogr
import osgeo.osr as osr
import re
import unicodecsv

# Adapted from http://lists.osgeo.org/pipermail/gdal-dev/2009-October/022284.html

def transformCoordinate(lat, long, sourceSystem=3067, targetSystem=4326):
    # Create wkt string of point coords
    # Sample coordinates taken from https://github.com/teelmo/YlePlus/blob/master/euref-fin2wgs84/example_data.csv
    wkt = 'POINT({0} {1})'.format(lat, long)

    # Create projection objects
    euref_fin = osr.SpatialReference()
    # http://spatialreference.org/ref/epsg/3067/
    euref_fin.ImportFromEPSG(sourceSystem)
    wgs84 = osr.SpatialReference()
    # http://spatialreference.org/ref/epsg/4326/
    wgs84.ImportFromEPSG(targetSystem)          #WGS84: 4326 EPSG: 3785 (Google Maps)

    # Create ogr point object, assign projection, reproject
    point = ogr.CreateGeometryFromWkt(wkt)
    point.AssignSpatialReference(euref_fin)
    point.TransformTo(wgs84)

    print wkt
    p = str(point)
    r = re.compile('\((.*?)\)')
    m = r.search(p)
    if m:
        coordinates = m.group(1)
        return coordinates.split( )





#muunna kylanimiston koordinaatit WGS84:een
with open('suomenkylanimisto.csv', 'rbU') as source:
    reader = unicodecsv.DictReader(source, delimiter=';')

    with open('suomenkylanimisto_WSG84.csv', 'wb') as resultcsv:
        writer = unicodecsv.writer(resultcsv, delimiter=';')
        writer.writerow(['name', 'locationtype', 'locationTypeCode', 'latitude','longitude'])

        for row in reader:
            #transform coordinate to WSG84
            coord = transformCoordinate(float(row["latitude"]), float(row["longitude"]))
            writer.writerow([row["name"], row["locationtype"], row["locationTypeCode"], coord[1], coord[0]])




