from books.karelians.extraction.extractors.baseExtractor import BaseExtractor
from books.karelians.extractionkeys import KEYS
from interface.valuewrapper import ValueWrapper
from books.karelians.extraction.extractionExceptions import NameException
import re

class ImageExtractor(BaseExtractor):

    def extract(self, text, entry):
        self.image_path = ""
        try:
            self.image_path = entry["xml"].attrib["img_path"]
        except KeyError as e:
            pass
        return self._constructReturnDict()

    def _constructReturnDict(self):
        return {KEYS["imagepath"] : ValueWrapper(self.image_path)}
