# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
from lxml import etree

def getXMLroot(filepath):

    #read the data in XML-format to be processed
    tree = etree.parse(filepath) #ET.parse(filepath)


    return tree.getroot()
