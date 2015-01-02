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

#tranforms the dict of the entry to a format which can be written into csv
def createRow(d):
    row = [d["surname"], d["firstnames"], d["birthDay"], d["birthMonth"], d["birthYear"], d["birthLocation"], d["deathDay"], d["deathMonth"], d["deathYear"], d["kaatunut"], d["deathLocation"], d["talvisota"], d["talvisotaregiments"], d["jatkosota"], d["jatkosotaregiments"], d["rank"], d["kotiutusDay"], d["kotiutusMonth"], d["kotiutusYear"], d["kotiutusPlace"], d["medals"], d["hasSpouse"]]
    """
    """
    if "children" in d:
        row += [d["children"], d["childCount"]]
    else:
        row += ["", ""]
    #list all spouses data:
    if d["spouseCount"] > 0:
        for wife in d["wifeList"]:
            wifeRow = [wife["weddingYear"], wife["spouseName"], wife["spouseBirthData"]["birthDay"], wife["spouseBirthData"]["birthMonth"], wife["spouseBirthData"]["birthYear"],
                                 wife["spouseBirthLocation"],  wife["spouseDeathData"]["deathDay"], wife["spouseDeathData"]["deathMonth"], wife["spouseDeathData"]["deathYear"],
                                 wife["spouseDeathData"]["deathLocation"], wife["children"]["childCount"], wife["children"]["children"]]
            row += wifeRow

    #add other children which don't have wife associated into them

    return row



#save the extract4ed info to a csv file:
with open("soldiers8.csv", "wb") as results:
    with open("errors8.csv", "wb") as errorcsv:
        writer = unicodecsv.writer(results, delimiter=";")
        writer.writerow(["surname", "first names", "birthDay", "birthMonth", "birthYear", "birthLocation", "deathDay", "deathMonth", "deathYear", "fallen", "deathLocation", "Served in Talvisota", "Talvisota regiments", "Served in Jatkosota", "Jatkosota regiments","Rank", "DemobilizationDay", "DemobilizationMonth", "DemobilizationYear", "DemobilizationPlace", "Medals", "hasSpouse", "otherChildren", "otherChildrenCount", "weddingYear",
                         "spouseName", "spouseBirthDay", "spouseBirthMonth","spouseBirthYear","spouseBirthLocation", "spouseDeathDay", "spouseDeathMonth","spouseDeathYear", "spouseDeathLocation", "childCount", "children",
                         "weddingYear2",
                         "spouseName2", "spouseBirthDay2", "spouseBirthMonth2","spouseBirthYear2","spouseBirthLocation2", "spouseDeathDay2", "spouseDeathMonth2","spouseDeathYear2", "spouseDeathLocation2", "childCount2", "children2"
                         ])

        ewriter = unicodecsv.writer(errorcsv, delimiter=";")
        ewriter.writerow(["Exception","Details", "type", "Entry text"])

        for child in root:
            try:
                d = extractor.extraction(child.text)
                writer.writerow(createRow(d))
                count +=1
            except ExtractionException as e:
                errorNodes.append({"child": child})
                ewriter.writerow([e.message, e.details, e.eType, child.text])
                errors +=1
                count +=1
            continue


print "Errors encountered: " + str(errors) + "/" + str(count)




"""
###############################################################
print "Start error fix tool..."

CombineTool.startGUI(errorNodes, root)
print "gui loppu"

#write modifications to a new xml-file:
f = open("fixed_combined.xml", 'w')
f.write(etree.tostring(root, pretty_print=True, encoding='unicode').encode("utf8"))
f.close()
"""