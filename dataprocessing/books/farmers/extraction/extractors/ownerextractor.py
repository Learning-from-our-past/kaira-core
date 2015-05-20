# -*- coding: utf-8 -*-
from books.farmers.extraction.extractors.baseExtractor import BaseExtractor
from books.farmers.extractionkeys import KEYS
from interface.valuewrapper import ValueWrapper
from books.farmers.extraction.extractionExceptions import OwnerYearException, OwnerNameException
import shared.textUtils as textUtils
import shared.regexUtils as regexUtils
import re

class OwnerExtractor(BaseExtractor):

    SEARCH_SPACE = 200
    def extract(self, text, entry):
        self.OWNER_YEAR_PATTERN = r"om(?:\.|,)\s?vuodesta\s(?P<year>\d\d\d\d)"
        self.OWNER_NAME_PATTERN = r"(?P<name>[A-ZÄ-Öa-zä-ö -]+)(?:\.|,)\ssynt"
        self.OWNER_OPTIONS = (re.UNICODE | re.IGNORECASE)

        self.owner_year = ""
        self.owner_name = ""
        self.first_names = ""
        self.surname = ""
        self._find_owner(text)
        return self._constructReturnDict()


    def _find_owner(self, text):
        text = textUtils.takeSubStrBasedOnRange(text, self.matchStartPosition, self.SEARCH_SPACE)
        self._find_owner_year(text)
        self._find_owner_name(text)

    def _find_owner_name(self, text):
        try:
            ownerName= regexUtils.safeSearch(self.OWNER_NAME_PATTERN, text, self.OWNER_OPTIONS)
            self.matchFinalPosition = ownerName.end()
            self._split_names(ownerName.group("name"))

        except regexUtils.RegexNoneMatchException as e:
            self.errorLogger.logError(OwnerNameException.eType, self.currentChild)

    def _split_names(self, name):
        name = re.sub(r"(?:<|>|&|')", r"", name)
        names = re.split(" ", name)

        self.surname = names[len(names)-1].strip(" ")
        if len(names) > 1:
            for i in range(0, len(names)-1):
                self.first_names += names[i] + " "
            self.first_names = self.first_names.strip(" ")


    def _find_owner_year(self, text):
        try:
            ownerYear= regexUtils.safeSearch(self.OWNER_YEAR_PATTERN, text, self.OWNER_OPTIONS)
            self.matchFinalPosition = ownerYear.end()
            self.owner_year = ownerYear.group("year")
        except regexUtils.RegexNoneMatchException as e:
            self.errorLogger.logError(OwnerYearException.eType, self.currentChild)

    def _constructReturnDict(self):
        return {KEYS["ownerFrom"] : ValueWrapper(self.owner_year),
                KEYS["ownerName"] : ValueWrapper({KEYS["firstnames"] : ValueWrapper(self.first_names),
                                     KEYS["surname"] : ValueWrapper(self.surname)})}