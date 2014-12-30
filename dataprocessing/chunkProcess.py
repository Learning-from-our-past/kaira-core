# -*- coding: utf-8 -*-
import readData
import re
import unicodecsv
import unicodedata
from extractionExceptions import *
from chunkerCheck import ChunkChecker
import guitool.main as GUITool
import guitool.combineTool as CombineTool
from lxml import etree

#This script checks the chunked XML file trying to find suspicious entries
errors = 0
count = 0
path = "Modified_rintamamiehet8_tags.xml"
root = readData.getXMLroot(path)
checker = ChunkChecker()

for child in root:
    try:
        d = checker.checkEntry(child, child.sourceline)
    except ExtractionException as e:
        continue

checker.showResults()

CombineTool.startGUI(checker.getSuspiciousEntries(), root)
print "gui loppu"

#write modifications to a new xml-file:
f = open("koe.xml", 'w')
f.write(etree.tostring(root, pretty_print=True, encoding='unicode').encode("utf8"))
f.close()