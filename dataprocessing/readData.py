# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET

def getXMLroot(filepath):
    #read the data in XML-format to be processed
    tree = ET.parse(filepath)
    return tree.getroot()
