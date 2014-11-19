# -*- coding: utf-8 -*-
import unicodecsv
import re

def saveResultsInCsv(tweetList):
        f = open('lovetwiitit2.csv', 'wb')
        keys = ['text']
        writer = unicodecsv.DictWriter(f, keys, delimiter=';', extrasaction='ignore')
        #writer.writer.writerow(keys)
        #print len(tweetList)
        writer.writerows(tweetList)


#tagien nimet tiedostossa
PAIKKATYYPPI = "paikkatyyppiKoodi"
PAIKKANIMI = "kirjoitusasu"




with open('paikkanayte.xml', 'rbU') as gmlfile:
    with open('karsittu.csv', 'wb') as resultcsv:




            writer = unicodecsv.writer(resultcsv, delimiter=';')
            writer.writerow(['name','locationtype', 'locationTypeCode',"latitude", "longitude"])

            #attributes to save:
            locationTypeCode = -1    #should be 540, 550, 560
            locationtype = ""
            pointCoordLat = -1
            pointCoordLon = -1
            locationName = ""
            i = 0

            for line in gmlfile:

                lineTag = ""
                lineCoord = ""
                #check tag:
                tagr = re.compile('<pnr:(.*?)>')
                tagm = tagr.search(line)

                if tagm is not None:
                    lineTag = tagm.group(1)
                else:
                    tagGML = re.compile('<gml:pos>(.*?)<')
                    tagGML = tagGML.search(line)

                    #save the coordinates
                    if tagGML is not None:
                        coord = tagGML.group(1).split(" ")
                        pointCoordLat = coord[0]           #koordinaatit
                        pointCoordLon = coord[1]

                #save the type
                if lineTag == PAIKKATYYPPI:
                    r = re.compile('>(.*?)<')
                    m = r.search(line)
                    if m:
                        locationTypeCode = m.group(1)

                        if locationTypeCode == "540":
                            locationtype = "kunta/kaupunki"
                        if locationTypeCode == "550":
                            locationtype = "kunta/maaseutu"
                        if locationTypeCode == "560":
                            locationtype = "kylä"

                #save the name
                if lineTag == PAIKKANIMI:
                    r = re.compile('>(.*?)<')
                    m = r.search(line)
                    if m:
                        locationName = m.group(1)


                #check if all data is found and write it to csv and reset variables:
                if locationTypeCode != -1 and pointCoordLat != -1 and pointCoordLon != -1 and locationName != "":
                    i += 1
                    if locationTypeCode == "540" or locationTypeCode == "550" or locationTypeCode == "560":
                        writer.writerow([locationName, locationtype, locationTypeCode, pointCoordLat, pointCoordLon])
                    locationTypeCode = -1    #should be 540, 550, 560
                    pointCoordLat = -1
                    pointCoordLon = -1
                    locationName = ""
                    locationtype = ""

                    print str(i)

