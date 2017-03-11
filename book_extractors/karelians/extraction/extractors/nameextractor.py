from book_extractors.common.base_extractor import BaseExtractor
from book_extractors.common.extraction_keys import KEYS
from shared.genderExtract import Gender, GenderException
import re


class NameExtractor(BaseExtractor):
    """ Tries to extract the name of the person in this entry. Assumed that it can be found from
    name attribute from person entry.
    """

    def extract(self, entry, start_position=0):
        result = {
            KEYS["surname"]: '',
            KEYS['firstnames']: ''
        }

        try:
            result = self._split_names(entry["name"])
        except KeyError as e:
            # TODO: Metadata logging here self.errorLogger.logError(NameException.eType, self.currentChild)
            pass

        try:
            result[KEYS['gender']] = Gender.find_gender(result[KEYS['firstnames']])
        except GenderException as e:
            # TODO: Metadata logging here self.errorLogger.logError(e.eType, self.currentChild)
            result[KEYS['gender']] = ""

        return self._constructReturnDict(result)

    @staticmethod
    def _split_names(name):
        name = re.sub(r"(?:<|>|&|')", r"", name)
        names = re.split("\.|,", name)

        name_results = {KEYS["surname"]: names[0].strip(" "), KEYS['firstnames']: ''}

        if len(names) > 1:
            name_results[KEYS["firstnames"]] = names[1].strip(" ")
        else:
            # TODO: Metadata logging here self.errorLogger.logError(NameException.eType, self.currentChild)
            pass

        return name_results
