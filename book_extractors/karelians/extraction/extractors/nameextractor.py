from book_extractors.common.base_extractor import BaseExtractor
from book_extractors.common.extraction_keys import KEYS
from book_extractors.extraction_exceptions import NameException
from shared.genderExtract import Gender, GenderException
import re

class NameExtractor(BaseExtractor):
    """ Tries to extract the name of the person in this entry. Assumed that it can be found from
    name attribute from person entry.
    """
    def extract(self, text, entry):
        self.first_names = ""
        self.surname = ""
        try:
            namestr = entry["name"]
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
        try:
            gender = Gender.find_gender(self.first_names)
        except GenderException as e:
            self.errorLogger.logError(e.eType, self.currentChild)
            gender = ""
        return {KEYS["firstnames"] : self.first_names, KEYS["gender"] : gender,KEYS["surname"]: self.surname}