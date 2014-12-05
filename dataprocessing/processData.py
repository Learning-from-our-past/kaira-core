# -*- coding: utf-8 -*-
import readData
import re
import unicodecsv
import unicodedata
from extractionExceptions import *
from dataExtraction import DataExtraction

#This script runs the exctraction process by using DataExtraction class's services.
errors = 0
count = 0
root = readData.getXMLroot("rintamamiehet8_newtags.xml")
extractor = DataExtraction()
#save the extract4ed info to a csv file:
with open("soldiers.csv", "wb") as results:
    with open("errors.csv", "wb") as errorcsv:
        writer = unicodecsv.writer(results, delimiter=";")
        writer.writerow(["surname", "first names", "birthDay", "birthMonth", "birthYear", "birthLocation"])

        ewriter = unicodecsv.writer(errorcsv, delimiter=";")
        ewriter.writerow(["Exception","Details", "Entry text"])

        for child in root:
            try:
                d = extractor.extraction(child.text)
                writer.writerow([d["surname"], d["firstnames"], d["birthDay"], d["birthMonth"], d["birthYear"], d["birthLocation"]])
                count +=1
            except ExtractionException as e:
                ewriter.writerow([e.message, e.details, child.text])
                errors +=1
                count +=1
                continue


print "Errors encountered: " + str(errors) + "/" + str(count)