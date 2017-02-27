"""
This class defines the progress and order of the extraction process by initializing and calling
required extractors.
"""
from books.karelians.extraction.extractors.nameextractor import NameExtractor
from books.karelians.extraction.extractors.origfamilyextractor import OrigFamilyExtractor
from books.karelians.extraction.extractors.professionextractor import ProfessionExtractor
from books.karelians.extraction.extractors.imageextractor import ImageExtractor
from books.karelians.extraction.extractors.omakotitaloextractor import OmakotitaloExtractor
from books.karelians.extraction.extractors.birthdayExtractor import BirthdayExtractor
from books.karelians.extraction.extractors.locationExtractor import BirthdayLocationExtractor
from books.karelians.extraction.extractors.karelianlocations import KarelianLocationsExtractor
from books.karelians.extraction.extractors.finnishlocations import FinnishLocationsExtractor
from books.karelians.extraction.extractors.spouseextractor import SpouseExtractor
from books.karelians.extraction.extractors.childextractor import ChildExtractor
from shared.genderExtract import Gender
import re

from interface.valuewrapper import ValueWrapper


class ExtractionPipeline:

    def __init__(self, xml_document):
        self.xml_document = xml_document
        Gender.load_names()

    def process(self, text, entry, eLogger):

        # Replace all weird invisible white space characters with regular space
        text = re.sub(r"\s", r" ", text)

        name_ext = NameExtractor(entry, eLogger, self.xml_document)
        names = name_ext.extract(text, entry)
        image_ext = ImageExtractor(entry, eLogger, self.xml_document)
        image = image_ext.extract(text, entry)

        orig_family_ext = OrigFamilyExtractor(entry, eLogger, self.xml_document)
        orig_family_ext.setDependencyMatchPositionToZero()
        orig_family = orig_family_ext.extract(text, entry)

        profession_ext = ProfessionExtractor(entry, eLogger, self.xml_document)
        profession_ext.dependsOnMatchPositionOf(orig_family_ext)
        profession = profession_ext.extract(text, entry)

        birthday_ext = BirthdayExtractor(entry, eLogger, self.xml_document)
        birthday_ext.dependsOnMatchPositionOf(orig_family_ext)
        birthday = birthday_ext.extract(text, entry)

        birth_loc_ext = BirthdayLocationExtractor(entry, eLogger, self.xml_document)
        birth_loc_ext.dependsOnMatchPositionOf(birthday_ext)
        birthday_location = birth_loc_ext.extract(text)

        karelian_loc_ext = KarelianLocationsExtractor(entry, eLogger, self.xml_document)
        karelian_locations = karelian_loc_ext.extract(text)

        finnish_loc_ext = FinnishLocationsExtractor(entry, eLogger, self.xml_document)
        finnish_locations = finnish_loc_ext.extract(text, entry)

        omakotitalo_ext = OmakotitaloExtractor(entry, eLogger, self.xml_document)
        omakotitalo = omakotitalo_ext.extract(text, entry)

        spouse_ext = SpouseExtractor(entry, eLogger, self.xml_document)
        spouse = spouse_ext.extract(text, entry)

        child_ext = ChildExtractor(entry, eLogger, self.xml_document)
        children = child_ext.extract(text, entry)

        d = names.copy()
        d.update(image)
        d.update(orig_family)
        d.update(profession)
        d.update(omakotitalo)
        d.update(birthday)
        d.update(birthday_location)
        d.update(karelian_locations)
        d.update(finnish_locations)
        d.update(spouse)
        d.update(children)
        d["originalText"] = ValueWrapper(text)
        return d
