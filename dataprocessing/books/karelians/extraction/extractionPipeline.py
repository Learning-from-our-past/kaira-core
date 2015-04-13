"""
This class defines the progress and order of the extraction process by initializing and calling
required extractors.
"""
from books.karelians.extraction.extractors.nameextractor import NameExtractor
from books.karelians.extraction.extractors.origfamilyextractor import OrigFamilyExtractor
from books.karelians.extraction.extractors.professionextractor import ProfessionExtractor

class ExtractionPipeline():

    def __init__(self, xmlDocument):
        self.xmlDocument = xmlDocument


    def process(self, text, entry, eLogger):
        nameExt = NameExtractor(entry, eLogger, self.xmlDocument)
        names = nameExt.extract(text, entry)

        origFamilyExt = OrigFamilyExtractor(entry, eLogger, self.xmlDocument)
        origFamilyExt.setDependencyMatchPositionToZero()
        origFamily = origFamilyExt.extract(text, entry)

        professionExt = ProfessionExtractor(entry, eLogger, self.xmlDocument)
        professionExt.dependsOnMatchPositionOf(origFamilyExt)
        profession = professionExt.extract(text, entry)

        d = names.copy()
        d.update(origFamily)
        d.update(profession)
        return d
