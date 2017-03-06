# -*- coding: utf-8 -*-
"""
This class defines the progress and order of the extraction process by initializing and calling
required extractors.
"""

from books.greatfarmers.extraction.extractors.metadataextractor import MetadataExtractor
from books.greatfarmers.extraction.extractors.ownerextractor import OwnerExtractor
from books.greatfarmers.extraction.extractors.childextractor import ChildExtractor
from books.greatfarmers.extraction.extractors.farmextractor import FarmExtractor
from books.greatfarmers.extraction.extractors.boolextractor import BoolExtractor
from books.greatfarmers.extraction.extractors.quantityextractor import QuantityExtractor
from books.greatfarmers.extraction.extractors.spouseextractor import SpouseExtractor
from books.greatfarmers.extractionkeys import KEYS
from shared.genderExtract import Gender
import re

class ExtractionPipeline():

    def __init__(self, person_data_input):
        self.person_data = person_data_input
        Gender.load_names()

    def process(self, person, eLogger):
        # Replace all weird invisible white space characters with regular space
        text = re.sub(r"\s", r" ", text)

        meta_ext = MetadataExtractor(person, eLogger, self.person_data)
        meta = meta_ext.extract(text, person)

        owner_ext = OwnerExtractor(person, eLogger, self.person_data)
        owner_ext.setDependencyMatchPositionToZero()
        owner_data = owner_ext.extract(text, person)

        spouse_ext = SpouseExtractor(person, eLogger, self.person_data)
        spouse = spouse_ext.extract(text, person)

        farm_ext = FarmExtractor(person, eLogger, self.person_data)
        farm_ext.setDependencyMatchPositionToZero()
        farm_data = farm_ext.extract(text, person)

        child_ext = ChildExtractor(person, eLogger, self.person_data)
        children = child_ext.extract(text, person)

        flag_ext = BoolExtractor(person, eLogger, self.person_data)
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
            KEYS["autotalli"] : r"autotalli",
            KEYS["viljankuivuri"] : r"viljankuivuri",
            KEYS["kotitalousmylly"] : r"kotitalousmylly",
            KEYS["ay-karja"] : r"ay-karja",
            KEYS["sk-karja"] : r"sk-karja",
            KEYS["someonedead"] : r"kuoli|kuollut|kaatui|kaatunut",
        }
        flag_ext.set_patterns_to_find(patterns)
        flags = flag_ext.extract(text, person)

        quantity_ext = QuantityExtractor(person, eLogger, self.person_data)
        qpatterns = {
            KEYS["rooms"] : r"(?:(?:asuinhuonetta){s<=1,i<=1}|(?:huonetta){s<=1,i<=1})",    #toimii
            KEYS["lypsylehma"] : r"(?:(?:lypsävää){s<=1,i<=1}|(?:lypsylehmää){s<=1,i<=1})", #toimii
            KEYS["lammas"] : r"(?:(?:(?:lampaita (?:on\s?)?){s<=1,i<=1})|(?:\slammasta))",
            KEYS["lihotussika"] : r"(?:lihotus-?sik){s<=1,i<=1}",                           #toimii
            KEYS["emakko"] : r"(?:(?:(?:emakkoja on\s?){s<=1,i<=1})|(?:\semakkoa))",
            KEYS["nuori"] : r"(?:(?:nuorta){s<=1,i<=1})",                                   #toimii
            KEYS["kanoja"] : r"(?:(?:(?:kanoja (?:on\s?)?){s<=1,i<=1})|(?:\skanaa))" #r"(?:kanoja|(?:kanaa{s<=1,i<=1}))"
         }

        quantity_ext.set_patterns_to_find(qpatterns)
        quantities = quantity_ext.extract(text, person)

        d = meta.copy()
        d.update(owner_data)
        d.update(children)
        d.update(farm_data)
        d.update(flags)
        d.update(quantities)
        d.update(spouse)
        return d
