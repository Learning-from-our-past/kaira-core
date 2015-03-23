# -*- coding: utf-8 -*-
import re
from operator import itemgetter

import regex
import extraction.extractors.regexUtils as regexUtils
import extraction.extractors.textUtils as textUtils
import extraction.extractors.locationPreparingUtils as locationPreparingUtils
from extraction.extractionExceptions import *
from extraction.extractors.addressExtractor import AddressExtractor
from extraction.extractors.medalsExtractor import MedalsExtractor
from extraction.extractors.rankExtractor import RankExtractor
from extraction.extractors.regimentExtractor import RegimentsExtractor
from extraction.extractors.hobbiesExtractor import HobbiesExtractor
from extraction.extractors.professionExtractor import ProfessionExtractor
from extraction.extractors.nameExtractor import NameExtractor
from extraction.extractors.warExtractor import WarExtractor
from extraction.extractors.birthdayExtractor import BirthdayExtractor
from extraction.extractors.locationExtractor import BirthdayLocationExtractor
from extraction.extractors.demobilizationExtractor import DemobilizationExtractor
from extraction.extractors.deathExtractor import DeathExtractor
from extraction.extractors.childrenExtractor import ChildrenExtractor
from extraction.extractors.spouseExtractor import SpouseExtractor
from extractionkeys import KEYS
"""Extraction process is handled here for one entry per time. This class calls all the extractor
classes to execute extraction in specific order."""
class DataExtraction:
    errorLogger = None
    currentChild = None

    def __init__(self, xmlDocument):
        self.xmlDocument = xmlDocument

    def extraction(self, text, entry, eLogger):
        self.errorLogger = eLogger
        self.currentChild = entry
        text = self.cleanText(text)

        nE = NameExtractor(self.currentChild, self.errorLogger, self.xmlDocument)
        personData = nE.extract(text)

        bE = BirthdayExtractor(self.currentChild, self.errorLogger, self.xmlDocument)
        bE.dependsOnMatchPositionOf(nE)
        personBirthday = bE.extract(text)

        plE = BirthdayLocationExtractor(self.currentChild, self.errorLogger, self.xmlDocument)
        plE.dependsOnMatchPositionOf(bE)
        personLocation = plE.extract(text)

        p = ProfessionExtractor(self.currentChild, self.errorLogger, self.xmlDocument)
        p.dependsOnMatchPositionOf(plE)
        profession = p.extract(text)    #text[personLocation["cursorLocation"]:]

        pDE = DeathExtractor(self.currentChild, self.errorLogger, self.xmlDocument)
        pDE.dependsOnMatchPositionOf(bE)
        personDeath = pDE.extract(text)

        spouseExtractor = SpouseExtractor(self.currentChild, self.errorLogger, self.xmlDocument)
        spouseExtractor.dependsOnMatchPositionOf(plE)
        spouseData = spouseExtractor.extract(text)

        #TODO: OWN FUNCTION
        #if there is no spouse, try to still find children:
        if spouseData[KEYS["spouseCount"]].value == 0:
            otherCh = ChildrenExtractor(self.currentChild, self.errorLogger, self.xmlDocument)
            otherCh.dependsOnMatchPositionOf(plE)
            children = otherCh.extract(text)

            #children = self.findChildren(text, personLocation["cursorLocation"])
        else:
            children = {}

        dmE = DemobilizationExtractor(self.currentChild, self.errorLogger, self.xmlDocument)
        kotiutus = dmE.extract(text)

        wE = WarExtractor(self.currentChild, self.errorLogger, self.xmlDocument)
        wars = wE.extract(text)

        r = RankExtractor(self.currentChild, self.errorLogger, self.xmlDocument)
        rank = r.extract(text)

        m = MedalsExtractor(self.currentChild, self.errorLogger, self.xmlDocument)
        medals = m.extract(text)

        a = AddressExtractor(self.currentChild, self.errorLogger, self.xmlDocument)
        address = a.extract(text)

        h = HobbiesExtractor(self.currentChild, self.errorLogger, self.xmlDocument)
        hobbies = h.extract(text)

        d = personData.copy()
        d.update(personBirthday)
        d.update(personLocation)
        d.update(profession)
        d.update(personDeath)
        d.update(spouseData)
        d.update(children)
        d.update(wars)
        d.update(rank)
        d.update(medals)
        d.update(kotiutus)
        d.update(address)
        d.update(hobbies)
        return d
        return dict(personData.items() + personBirthday.items() + personLocation.items() + profession.items() + personDeath.items()+ spouseData.items() + children.items() + wars.items() + rank.items() + medals.items() + kotiutus.items() + address.items() + hobbies.items())

    def cleanText(self, text):
        text = text.replace("\n", ' ')
        text = ' '.join(text.split())   #remove excess whitespace and linebreaks
        return text
