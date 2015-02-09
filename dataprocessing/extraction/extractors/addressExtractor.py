# -*- coding: utf-8 -*-
import re
import regex
from baseExtractor import BaseExtractor


class AddressExtractor(BaseExtractor):
    regexPattern = ur'(?:\W- ?Os\b|\W- ?os\b|\W- ?o5\b|\W- ?O5\b|\W- ?05\b)(?P<address>(?:.|\n)*?)(?=$|Rva|\.)'
    address = ""

    def extract(self, text):
        matches = self._executeSearchRegex(text)
        self.address = self._constructAddressFromMatch(matches)
        return self._constructReturnDict()

    def _constructAddressFromMatch(self, matches):
        if matches != None:
            self.address = matches.group("address")
        return self.address

    def _constructReturnDict(self):
        return {"address" : self.address}

