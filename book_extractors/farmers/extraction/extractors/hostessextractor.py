# -*- coding: utf-8 -*-
from book_extractors.common.base_extractor import BaseExtractor
from book_extractors.farmers.extractionkeys import KEYS
from book_extractors.farmers.extraction.extractionExceptions import  HostessNameException
from book_extractors.farmers.extraction.extractors.birthdayExtractor import BirthdayExtractor
import shared.textUtils as textUtils
import shared.regexUtils as regexUtils
import re


class HostessExtractor(BaseExtractor):

    SEARCH_SPACE = 400

    def extract(self, text, entry):
        self.HOSTESS_NAME_PATTERN = r"emäntä(?:nä)?(?:\svuodesta\s\d\d\d\d)?(?P<name>[A-ZÄ-Öa-zä-ö\.\s-]+)," #r"(?P<name>[A-ZÄ-Öa-zä-ö -]+)(?:\.|,)\ssynt"
        self.HOSTESS_OPTIONS = (re.UNICODE | re.IGNORECASE)
        self.entry = entry
        self.first_names = ""
        self.surname = ""
        self.hostess_gender = "Female"
        self.birthday = {KEYS["birthDay"]:  "", KEYS["birthMonth"]:  "",
                KEYS["birthYear"]:  "", KEYS["birthLocation"]:  ""}
        self._find_hostess(text)
        return self._constructReturnDict()


    def _find_hostess(self, text):
        text = textUtils.takeSubStrBasedOnRange(text, self.matchStartPosition, self.SEARCH_SPACE)

        self._find_hostess_name(text)

    def _find_hostess_birthday(self, text):
        birthdayExt = BirthdayExtractor(self.entry, self.errorLogger)
        birthdayExt.setDependencyMatchPositionToZero()
        self.birthday = birthdayExt.extract(text, self.entry)

    def _find_hostess_name(self, text):
        try:
            hostessName= regexUtils.safeSearch(self.HOSTESS_NAME_PATTERN, text, self.HOSTESS_OPTIONS)
            self.matchFinalPosition = hostessName.end()
            self._split_names(hostessName.group("name"))

            self._find_hostess_birthday(text[self.matchFinalPosition:])

        except regexUtils.RegexNoneMatchException as e:
            self.errorLogger.logError(HostessNameException.eType, self.currentChild)

    def _split_names(self, name):
        name = re.sub(r"(?:<|>|&|')", r"", name)
        names = re.split(" ", name)

        self.surname = names[len(names)-1].strip(" ")
        if len(names) > 1:
            for i in range(0, len(names)-1):
                if names[i].strip(" ") != "o.s.":
                    self.first_names += names[i].strip(" ") + " "
            self.first_names = self.first_names.strip(" ")

    def _constructReturnDict(self):
        return {KEYS["hostess"] : {
                KEYS["firstnames"] : self.first_names,
                KEYS["surname"] : self.surname,
                KEYS["gender"] : self.hostess_gender,
                KEYS["hostessBirthData"] : self.birthday
        }}

