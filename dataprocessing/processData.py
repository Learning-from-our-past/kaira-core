# -*- coding: utf-8 -*-
import readData
import re
import unicodecsv
import unicodedata
from extractionExceptions import *
from dataExtraction import DataExtraction
from extractionExceptions import *
from chunkerCheck import ChunkChecker
import guitool.main as GUITool
import guitool.combineTool as CombineTool
from lxml import etree

#This script runs the exctraction process by using DataExtraction class's services.
errors = 0
count = 0
root = readData.getXMLroot("fixed_combined.xml")
extractor = DataExtraction()

errorNodes = []


#save the extract4ed info to a csv file:
with open("soldiers8.csv", "wb") as results:
    with open("errors8.csv", "wb") as errorcsv:
        writer = unicodecsv.writer(results, delimiter=";")
        writer.writerow(["surname", "first names", "birthDay", "birthMonth", "birthYear", "birthLocation", "deathDay", "deathMonth", "deathYear", "fallen", "deathLocation", "hasSpouse", "weddingYear",
                         "spouseName", "spouseBirthDay", "spouseBirthMonth","spouseBirthYear","spouseBirthLocation", "spouseDeathDay", "spouseDeathMonth","spouseDeathYear", "spouseDeathLocation", "childCount", "children"])

        ewriter = unicodecsv.writer(errorcsv, delimiter=";")
        ewriter.writerow(["Exception","Details", "type", "Entry text"])

        for child in root:
            try:
                d = extractor.extraction(child.text)
                writer.writerow([d["surname"], d["firstnames"], d["birthDay"], d["birthMonth"], d["birthYear"], d["birthLocation"], d["deathDay"], d["deathMonth"], d["deathYear"], d["kaatunut"], d["deathLocation"], d["hasSpouse"], d["weddingYear"], d["spouseName"],
                                 d["spouseBirthData"]["birthDay"], d["spouseBirthData"]["birthMonth"], d["spouseBirthData"]["birthYear"],
                                 d["spouseBirthLocation"],  d["spouseDeathData"]["deathDay"], d["spouseDeathData"]["deathMonth"], d["spouseDeathData"]["deathYear"], d["spouseDeathData"]["deathLocation"], d["childCount"], d["children"]])

                count +=1
            except ExtractionException as e:
                errorNodes.append({"child": child})
                ewriter.writerow([e.message, e.details, e.eType, child.text])
                errors +=1
                count +=1
            continue


print "Errors encountered: " + str(errors) + "/" + str(count)


###############################################################
print "Start error fix tool..."

CombineTool.startGUI(errorNodes, root)
print "gui loppu"

#write modifications to a new xml-file:
f = open("fixed_combined.xml", 'w')
f.write(etree.tostring(root, pretty_print=True, encoding='unicode').encode("utf8"))
f.close()