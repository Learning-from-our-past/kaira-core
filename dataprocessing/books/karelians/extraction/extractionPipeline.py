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

class ExtractionPipeline():

    def __init__(self, xmlDocument):
        self.xmlDocument = xmlDocument
        Gender.load_names()


    def process(self, text, entry, eLogger):
        nameExt = NameExtractor(entry, eLogger, self.xmlDocument)
        names = nameExt.extract(text, entry)
        imageExt = ImageExtractor(entry, eLogger, self.xmlDocument)
        image = imageExt.extract(text, entry)

        origFamilyExt = OrigFamilyExtractor(entry, eLogger, self.xmlDocument)
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

        childExt = ChildExtractor(entry, eLogger, self.xmlDocument)
        children = childExt.extract(text, entry)



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
        d.update(children)

        return d
