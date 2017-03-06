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
import re


class ExtractionPipeline:

    def __init__(self, person_data_input):
        self.person_data = person_data_input
        Gender.load_names()

    def process(self, text, entry, eLogger):
        # Replace all weird invisible white space characters with regular space
        text = re.sub(r"\s", r" ",text)

        meta_ext = MetadataExtractor(entry, eLogger, self.person_data)
        meta = meta_ext.extract(text, entry)

        owner_ext = OwnerExtractor(entry, eLogger, self.person_data)
        owner_ext.setDependencyMatchPositionToZero()
        owner_data = owner_ext.extract(text, entry)


        hostess_ext = HostessExtractor(entry, eLogger, self.person_data)
        hostess_ext.setDependencyMatchPositionToZero()
        hostess_data = hostess_ext.extract(text, entry)

        farm_ext = FarmExtractor(entry, eLogger, self.person_data)
        farm_ext.setDependencyMatchPositionToZero()
        farm_data = farm_ext.extract(text, entry)

        child_ext = ChildExtractor(entry, eLogger, self.person_data)
        children = child_ext.extract(text, entry)

        flag_ext = BoolExtractor(entry, eLogger, self.person_data)
        patterns = {
            KEYS["oat"] : r"(kaura(?!nen))",
            KEYS["barley"] : r"ohra",
            KEYS["hay"] : r"(heinä(?!mäki))",
            KEYS["potatoes"] : r"peruna",
            KEYS["wheat"] : r"vehnä",
            KEYS["rye"] : r"ruis",
            KEYS["sugarbeet"] : r"sokerijuuri",
            KEYS["lanttu"] : r"lanttu",
            KEYS["puimakone"] : r"puimakone",
            KEYS["tractor"] : r"traktori",
            KEYS["horse"] : r"hevonen|hevos",
            KEYS["chicken"] : r"kanoja|\skanaa",
            KEYS["siirtotila"] : r"siirtotila",
            KEYS["kantatila"] : r"kantatila",
            KEYS["moreeni"] : r"moreeni",
            KEYS["hiesu"] : r"hiesu",
            KEYS["hieta"] : r"(hieta(?!nen))",
            KEYS["muta"] : r"muta",
            KEYS["savi"] : r"(savi(?!taipale))",
            KEYS["multa"] : r"multa",
            KEYS["salaojitus"] : r"(salaojitettu|salaojitus)",

            KEYS["talli"] : r"(?!auto)talli",
            KEYS["pine"] : r"mänty(?!nen)",
            KEYS["spruce"] : r"kuusi(?!nen)",
            KEYS["birch"] : r"koivu(?!nen|niem)",
            KEYS["sauna"] : r"sauna",
            KEYS["navetta"] : r"navetta|navetan",
            KEYS["lypsykone"] : r"lypsykone",
            KEYS["autotalli"] : r"autotalli",
            KEYS["someonedead"] : r"kuoli|kuollut|kaatui|kaatunut",

        }
        flag_ext.set_patterns_to_find(patterns)
        flags = flag_ext.extract(text, entry)

        quantity_ext = QuantityExtractor(entry, eLogger, self.person_data)
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

        quantity_ext.set_patterns_to_find(qpatterns)
        quantities = quantity_ext.extract(text, entry)

        d = meta.copy()
        d.update(owner_data)
        d.update(hostess_data)
        d.update(children)
        d.update(farm_data)
        d.update(flags)
        d.update(quantities)
        return d
