# -*- coding: utf-8 -*-
"""
This class defines the progress and order of the extraction process by initializing and calling
required extractors.
"""

from book_extractors.farmers.extraction.extractors.metadataextractor import MetadataExtractor
from book_extractors.farmers.extraction.extractors.ownerextractor import OwnerExtractor
from book_extractors.farmers.extraction.extractors.hostessextractor import HostessExtractor
from book_extractors.farmers.extraction.extractors.childextractor import ChildExtractor
from book_extractors.farmers.extraction.extractors.farmextractor import FarmExtractor
from book_extractors.farmers.extraction.extractors.boolextractor import BoolExtractor
from book_extractors.farmers.extraction.extractors.quantityextractor import QuantityExtractor
from book_extractors.farmers.extractionkeys import KEYS
from shared.genderExtract import Gender
import re


class ExtractionPipeline:

    def __init__(self):
        Gender.load_names()

    def process(self, person, eLogger):
        # Replace all weird invisible white space characters with regular space
        text = person['text'] = re.sub(r"\s", r" ", person['text'])

        meta_ext = MetadataExtractor(person, eLogger)
        meta = meta_ext.extract(text, person)

        owner_ext = OwnerExtractor(person, eLogger)
        owner_ext.setDependencyMatchPositionToZero()
        owner_data = owner_ext.extract(text, person)

        hostess_ext = HostessExtractor(person, eLogger)
        hostess_ext.setDependencyMatchPositionToZero()
        hostess_data = hostess_ext.extract(text, person)

        farm_ext = FarmExtractor(person, eLogger)
        farm_ext.setDependencyMatchPositionToZero()
        farm_data = farm_ext.extract(text, person)

        child_ext = ChildExtractor(person, eLogger)
        children = child_ext.extract(text, person)

        flag_ext = BoolExtractor(person, eLogger)
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
        flags = flag_ext.extract(text, person)

        quantity_ext = QuantityExtractor(person, eLogger)
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
        quantities = quantity_ext.extract(text, person)

        d = meta.copy()
        d.update(owner_data)
        d.update(hostess_data)
        d.update(children)
        d.update(farm_data)
        d.update(flags)
        d.update(quantities)
        return d
