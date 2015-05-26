# -*- coding: utf-8 -*-
"""
This class defines the progress and order of the extraction process by initializing and calling
required extractors.
"""

from books.farmers.extraction.extractors.metadataextractor import MetadataExtractor
from books.farmers.extraction.extractors.ownerextractor import OwnerExtractor
from books.farmers.extraction.extractors.hostessextractor import HostessExtractor
from books.farmers.extraction.extractors.childextractor import ChildExtractor
from books.farmers.extraction.extractors.farmextractor import FarmExtractor
from books.farmers.extraction.extractors.boolextractor import BoolExtractor
from books.farmers.extraction.extractors.quantityextractor import QuantityExtractor
from books.farmers.extractionkeys import KEYS
from shared.genderExtract import Gender

class ExtractionPipeline():

    def __init__(self, xmlDocument):
        self.xmlDocument = xmlDocument
        Gender.load_names()


    def process(self, text, entry, eLogger):
        metaExt = MetadataExtractor(entry, eLogger, self.xmlDocument)
        meta = metaExt.extract(text, entry)

        ownerExt = OwnerExtractor(entry, eLogger, self.xmlDocument)
        ownerExt.setDependencyMatchPositionToZero()
        ownerdata = ownerExt.extract(text, entry)


        hostessExt = HostessExtractor(entry, eLogger, self.xmlDocument)
        hostessExt.setDependencyMatchPositionToZero()
        hostessdata = hostessExt.extract(text, entry)

        farmExt = FarmExtractor(entry, eLogger, self.xmlDocument)
        farmExt.setDependencyMatchPositionToZero()
        farmdata = farmExt.extract(text, entry)

        childExt = ChildExtractor(entry, eLogger, self.xmlDocument)
        children = childExt.extract(text, entry)

        flagExt = BoolExtractor(entry, eLogger, self.xmlDocument)
        patterns = {
            KEYS["oat"] : r"kaura",
            KEYS["barley"] : r"ohra",
            KEYS["hay"] : r"heinä",
            KEYS["potatoes"] : r"peruna",
            KEYS["wheat"] : r"vehnä",
            KEYS["sugarbeet"] : r"sokerijuuri",
            KEYS["puimakone"] : r"puimakone",
            KEYS["tractor"] : r"traktori",
            KEYS["horse"] : r"hevonen|hevos",
            KEYS["chicken"] : r"kanoja|\skanaa",
            KEYS["siirtotila"] : r"siirtotila",
            KEYS["kantatila"] : r"kantatila",
            KEYS["moreeni"] : r"moreeni",
            KEYS["hiesu"] : r"hiesu",
            KEYS["hieta"] : r"hieta",
            KEYS["muta"] : r"muta",
            KEYS["savi"] : r"savi",
            KEYS["multa"] : r"multa",
            KEYS["salaojitus"] : r"(salaojitettu|salaojitus)"
        }
        flagExt.set_patterns_to_find(patterns)
        flags = flagExt.extract(text, entry)

        quantityExt = QuantityExtractor(entry, eLogger, self.xmlDocument)
        qpatterns = {
            KEYS["rooms"] : r"(?:(?:asuinhuonetta){s<=1,i<=1}|(?:huonetta){s<=1,i<=1})",
            KEYS["lypsylehma"] : r"(?:lypsylehmää){s<=1,i<=1}",
            KEYS["teuras"] : r"(?:teuras){s<=1,i<=1}",
            KEYS["lammas"] : r"(?:lammasta){s<=1,i<=1}",
            KEYS["lihotussika"] : r"(?:lihotus-?sik){s<=1,i<=1}",
            KEYS["emakko"] : r"(?:emakko){s<=1,i<=1}",
            KEYS["nuori"] : r"(?:nuori|(?:nuorta{s<=1,i<=1}))",
            KEYS["kanoja"] : r"(?:kanoja|(?:kanaa{s<=1,i<=1}))"
         }

        quantityExt.set_patterns_to_find(qpatterns)
        quantities = quantityExt.extract(text, entry)

        d = meta.copy()
        d.update(ownerdata)
        d.update(hostessdata)
        d.update(children)
        d.update(farmdata)
        d.update(flags)
        d.update(quantities)
        return d
