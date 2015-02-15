# -*- coding: utf-8 -*-
import re
import regex
from baseExtractor import BaseExtractor
import regexUtils, textUtils
from extraction.extractionExceptions import *
from extraction.extractors.childrenExtractor import ChildrenExtractor
from extraction.extractors.birthdayExtractor import BirthdayExtractor
from extraction.extractors.locationExtractor import LocationExtractor
from extraction.extractors.deathExtractor import DeathExtractor

class SpouseExtractor(BaseExtractor):
    PATTERN_SPOUSE_EXISTS = ur'(?P<spouseExists>\b(?:P|p)so\b)'
    OPTIONS = re.UNICODE

    REQUIRES_MATCH_POSITION = True
    SPOUSE_WINDOW_WIDTH = 120
    foundSpouse = False
    spouseData = {"spouseCount" : 0, "hasSpouse": False}

    def extract(self, text):
        super(SpouseExtractor, self).extract(text)
        preparedText = self._prepareTextForExtraction(text)
        self._findSpouses(preparedText)
        return self._constructReturnDict()

    def _prepareTextForExtraction(self, text):
        t = textUtils.takeSubStrBasedOnPos(text, self.matchStartPosition-5)
        #snip the string if there is ts or js markers to avoid taking spouse's old men.
        pos = regexUtils.findFirstPositionWithRegexSearch(ur'(?P<match>ts:|js:)', text, re.IGNORECASE | re.UNICODE)
        t = textUtils.takeSubStrBasedOnPos(t, 0, pos+10)
        return t

    def _findSpouses(self, text):
        try:
            spouseExists= regexUtils.safeSearch(self.PATTERN_SPOUSE_EXISTS, text, self.OPTIONS)
            self._findAllSpouses(text)
            self.matchFinalPosition = spouseExists.end()
        except regexUtils.RegexNoneMatchException as e:
           pass

    def _constructReturnDict(self):
        return self.spouseData

    def _findAllSpouses(self, text):
        spouseCount = self._getSpouseCount(text)
        wives = []

        for i in range(0, len(spouseCount)):
            extractionStrs = self._constructSpouseExtractionStrings(spouseCount, i, text)

            childExtractor = ChildrenExtractor(self.currentChild, self.errorLogger)
            childExtractor.setDependencyMatchPositionToZero()
            children = childExtractor.extract(extractionStrs["childString"])

            wifeExt = WifeDataExtractor(self.currentChild, self.errorLogger)

            wife = wifeExt.extract(extractionStrs["spouseString"])

            if wife["spouseName"] != "":
                wife["children"] = children
                wives.append(wife)

        if len(wives) >= 2: #make a note that there is lots of wives which may indicate chunking error in XML
            self.errorLogger.logError(TooManyWivesException.eType, self.currentChild)

        spouseData = { "spouseCount" : len(wives), "wifeList": wives} #self.extractSpouse(text2, cursorLocation)
        spouseData["hasSpouse"] = True
        spouseData["spouseCount"] = len(wives)
        self.spouseData = spouseData

    def _getSpouseCount(self, text):
        spouseCount = regexUtils.regexIter(self.PATTERN_SPOUSE_EXISTS, text, self.OPTIONS)
        spouseCount = tuple(spouseCount)

        return spouseCount

    def _constructSpouseExtractionStrings(self, spouseCount, i, text):
        #decide the end position of the substring where to find the spouse
        if i+1 < len(spouseCount):
            #take substring for one spouse from one to the next.
            endPos = spouseCount[i+1].start()
            spouseString = textUtils.takeSubStrBasedOnRange(text, spouseCount[i].start(), endPos+4)
            childString = spouseString
        else:
            #there is no next spouse, so take substr to the end
            endPos = spouseCount[i].start() + self.SPOUSE_WINDOW_WIDTH
            spouseString = textUtils.takeSubStrBasedOnRange(text, spouseCount[i].start(), endPos)
            childString = textUtils.takeSubStrBasedOnPos(text, spouseCount[i].start())
        return {"spouseString": spouseString, "childString": childString}



class WifeDataExtractor(BaseExtractor):
    WEDDINGYEAR_NAME_PATTERN = ur'\b(?:P|p)so\b(?: \bvst?l?a ?(?P<weddingYear>\d{1,2})\.?)? ?(?P<spouseName>[A-ZÄ-Ö][A-ZÄ-Öa-zä-ö -]+)(?:,|.)'
    OPTIONS = re.UNICODE
    BIRTHYEAR_WINDOW_LEFTOFFSET = 10
    spouseName = ""
    weddingYear = ""
    birthData = {"birthDay": "","birthMonth": "", "birthYear": ""}
    birthPlace = ""
    deathData = ""
    wifeData = None


    def extract(self, text):
        super(WifeDataExtractor, self).extract(text)
        try:
            self._findSpouseNameAndWeddingYear(text)
            self._findBirthday(text)
            self._findBirthPlace(text)
            self._findDeath(text)
        except NoWifeException as e:
            #extraction failed to find anything so skip the rest extractions
            pass
        return self._constructReturnDict()

    def _findSpouseNameAndWeddingYear(self, text):
        try:
            found = regexUtils.safeSearch(self.WEDDINGYEAR_NAME_PATTERN, text, self.OPTIONS)
            self.matchFinalPosition = found.end()

            #TODO: OWN FUNCTIONS FOR CLARITY?
            try:
                self.weddingYear = int(found.group("weddingYear"))
            except Exception as e:
                self.errorLogger.logError(WeddingException.eType, self.currentChild)
            try:
                self.spouseName = found.group("spouseName")
            except Exception as e:
                self.errorLogger.logError(SpouseNameException.eType, self.currentChild)
        except regexUtils.RegexNoneMatchException as e:
            #no wife data found.
            raise NoWifeException()

    def _findBirthday(self, text):
        try:
            bDayExt = BirthdayExtractor(self.currentChild, self.errorLogger)
            preparedText = textUtils.takeSubStrBasedOnPos(text, self.matchFinalPosition - self.BIRTHYEAR_WINDOW_LEFTOFFSET, 64)
            bDayExt.setDependencyMatchPositionToZero()
            self.birthData = bDayExt.extract(preparedText) #self.extractBirthday(text[(m.end()-birthYearWindowLeftOffset):], 0, 64)
            #self.matchFinalPosition += bDayExt.getFinalMatchPosition()- self.BIRTHYEAR_WINDOW_LEFTOFFSET
        except BirthdayException as e:
            self.errorLogger.logError(SpouseBirthdayException.eType, self.currentChild)

    def _findBirthPlace(self, text):
        try:
            locationExt = LocationExtractor()
            preparedText = textUtils.takeSubStrBasedOnPos(text, self.matchFinalPosition)
            self.birthPlace = locationExt.extract(preparedText).group("location")
            #self.matchFinalPosition += locationExt.getFinalMatchPosition() - 15
        except LocationException as e:
            self.errorLogger.logError(SpouseBirthplaceException.eType, self.currentChild)

    def _findDeath(self, text):
        deathExt = DeathExtractor(self.currentChild, self.errorLogger)
        preparedText = textUtils.takeSubStrBasedOnPos(text, self.matchFinalPosition, 60)
        deathExt.targetIsSpouse()
        deathExt.setDependencyMatchPositionToZero()
        self.deathData = deathExt.extract(preparedText)

    def _constructReturnDict(self):
        return {"cursorLocation": self.getFinalMatchPosition(), "weddingYear": self.weddingYear, "spouseName": self.spouseName, "spouseBirthData": self.birthData, "spouseDeathData": self.deathData, "spouseBirthLocation": self.birthPlace}


class NoWifeException(Exception):
    message = "Couldn't find wife data."
    def __unicode__(self):
        return repr(self.message)


def extractSdfgfdgfdgdfgfedgpouse(self, text, cursorLocation):
        birthYearWindowLeftOffset = 10

        if m != None:



            deathData = self.extractDeath(text, m.end(), 40, False)
            return {"cursorLocation": deathData["cursorLocation"], "weddingYear": weddingYear, "spouseName": spouseName, "spouseBirthData": spouseBirthYear, "spouseDeathData": deathData,"spouseBirthLocation": birthPlace["location"]}
        else:
            return None

