from books.karelians.extraction.extractors.baseExtractor import BaseExtractor
from books.karelians.extractionkeys import KEYS
from interface.valuewrapper import ValueWrapper
from books.karelians.extraction.extractionExceptions import NameException
import re

class NameExtractor(BaseExtractor):
    """ Tries to extract the name of the person in this entry. Assumed that it can be found from
    name attribute from xml-entry.
    """
    def extract(self, text, entry):
        self.first_names = ""
        self.surname = ""
        try:
            namestr = entry["xml"].attrib["name"]
            self._split_names(namestr)
        except KeyError as e:
            self.errorLogger.logError(NameException.eType, self.currentChild)
        return self._constructReturnDict()

    def _split_names(self, name):
        name = re.sub(r"(?:<|>|&|')", r"", name)
        names = re.split("\.|,", name)

        self.surname = names[0].strip(" ")
        if len(names) > 1:
            self.first_names = names[1].strip(" ")
        else:
            self.errorLogger.logError(NameException.eType, self.currentChild)

    def _constructReturnDict(self):
        return {KEYS["firstnames"] : ValueWrapper(self.first_names), KEYS["surname"]: ValueWrapper(self.surname)}
