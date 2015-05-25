# -*- coding: utf-8 -*-
"""
This class defines the progress and order of the extraction process by initializing and calling
required extractors.
"""

from books.farmers.extraction.extractors.metadataextractor import MetadataExtractor
from books.farmers.extraction.extractors.nameextractor import NameExtractor

from books.farmers.extraction.extractors.origfamilyextractor import OrigFamilyExtractor
from books.farmers.extraction.extractors.ownerextractor import OwnerExtractor
from books.farmers.extraction.extractors.hostessextractor import HostessExtractor

from books.farmers.extraction.extractors.omakotitaloextractor import OmakotitaloExtractor
from books.farmers.extraction.extractors.birthdayExtractor import BirthdayExtractor
from books.farmers.extraction.extractors.locationExtractor import BirthdayLocationExtractor
from books.farmers.extraction.extractors.karelianlocations import KarelianLocationsExtractor
from books.farmers.extraction.extractors.finnishlocations import FinnishLocationsExtractor
from books.farmers.extraction.extractors.spouseextractor import SpouseExtractor
from books.farmers.extraction.extractors.childextractor import ChildExtractor
from books.farmers.extraction.extractors.farmextractor import FarmExtractor
from books.farmers.extraction.extractors.boolextractor import BoolExtractor
from books.farmers.extractionkeys import KEYS
from books.farmers.extraction.extractors.deathextractor import DeathExtractor
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


        """origFamilyExt = OrigFamilyExtractor(entry, eLogger, self.xmlDocument)
        origFamilyExt.setDependencyMatchPositionToZero()
        origFamily = origFamilyExt.extract(text, entry)

        professionExt = ProfessionExtractor(entry, eLogger, self.xmlDocument)
        professionExt.dependsOnMatchPositionOf(origFamilyExt)
        profession = professionExt.extract(text, entry)

        birthdayExt = BirthdayExtractor(entry, eLogger, self.xmlDocument)
        birthdayExt.dependsOnMatchPositionOf(origFamilyExt)
        birthday = birthdayExt.extract(text, entry)

        birthLocExt = BirthdayLocationExtractor(entry, eLogger, self.xmlDocument)
        birthLocExt.dependsOnMatchPositionOf(birthdayExt)
        birthdayLocation = birthLocExt.extract(text)

        karelianLocExt = KarelianLocationsExtractor(entry, eLogger, self.xmlDocument)
        karelianLocations = karelianLocExt.extract(text, entry)

        finnishLocExt = FinnishLocationsExtractor(entry, eLogger, self.xmlDocument)
        finnishLocations = finnishLocExt.extract(text, entry)

        omakotitaloExt = OmakotitaloExtractor(entry, eLogger, self.xmlDocument)
        omakotitalo = omakotitaloExt.extract(text, entry)

        #spouse
        spouseExt = SpouseExtractor(entry, eLogger, self.xmlDocument)
        spouse = spouseExt.extract(text, entry)
        """

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
        }
        flagExt.set_patterns_to_find(patterns)
        flags = flagExt.extract(text, entry)

        d = meta.copy()
        d.update(ownerdata)
        d.update(hostessdata)
        d.update(children)
        d.update(farmdata)
        d.update(flags)
        """
        d = names.copy()
        d.update(image)
        d.update(origFamily)
        d.update(profession)
        d.update(omakotitalo)
        d.update(birthday)
        d.update(birthdayLocation)
        d.update(karelianLocations)
        d.update(finnishLocations)
        d.update(spouse)

        """

        return d
