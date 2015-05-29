# -*- coding: utf-8 -*-
from books.farmers.extraction.extractors.baseExtractor import BaseExtractor
from books.farmers.extractionkeys import KEYS
from interface.valuewrapper import ValueWrapper
from books.farmers.extraction.extractionExceptions import  HostessNameException
from books.farmers.extraction.extractors.birthdayExtractor import BirthdayExtractor
import shared.textUtils as textUtils
import shared.regexUtils as regexUtils
from shared.genderExtract import Gender
import re

class HostessExtractor(BaseExtractor):

    SEARCH_SPACE = 400
    def extract(self, text, entry):
        self.HOSTESS_NAME_PATTERN = r"emäntä(?:nä)?(?:\svuodesta\s\d\d\d\d)?(?P<name>[A-ZÄ-Öa-zä-ö\.\s-]+)," #r"(?P<name>[A-ZÄ-Öa-zä-ö -]+)(?:\.|,)\ssynt"
        self.HOSTESS_OPTIONS = (re.UNICODE | re.IGNORECASE)
        self.entry = entry
        self.first_names = ValueWrapper("")
        self.surname = ValueWrapper("")
        self.hostess_gender = ValueWrapper("Female")
        self.birthday = {KEYS["birthDay"]:  ValueWrapper(""), KEYS["birthMonth"]:  ValueWrapper(""),
                KEYS["birthYear"]:  ValueWrapper(""), KEYS["birthLocation"]:  ValueWrapper("")}
        self._find_hostess(text)
        return self._constructReturnDict()


    def _find_hostess(self, text):
        text = textUtils.takeSubStrBasedOnRange(text, self.matchStartPosition, self.SEARCH_SPACE)

        self._find_hostess_name(text)


    def _find_hostess_birthday(self, text):
        birthdayExt = BirthdayExtractor(self.entry, self.errorLogger, self.xmlDocument)
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
            self.first_names.error = HostessNameException.eType
            self.surname.error = HostessNameException.eType

    def _split_names(self, name):
        name = re.sub(r"(?:<|>|&|')", r"", name)
        names = re.split(" ", name)

        self.surname.value = names[len(names)-1].strip(" ")
        if len(names) > 1:
            for i in range(0, len(names)-1):
                if names[i].strip(" ") != "o.s.":
                    self.first_names.value += names[i].strip(" ") + " "
            self.first_names.value = self.first_names.value.strip(" ")



    def _constructReturnDict(self):
        return {KEYS["hostess"] : ValueWrapper({
                KEYS["firstnames"] : self.first_names,
                KEYS["surname"] : self.surname,
                KEYS["gender"] : self.hostess_gender,
                KEYS["hostessBirthData"] : ValueWrapper(self.birthday)
        })}

