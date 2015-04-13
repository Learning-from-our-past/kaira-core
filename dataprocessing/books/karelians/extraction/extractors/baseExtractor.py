# -*- coding: utf-8 -*-
from abc import ABCMeta, abstractmethod
import re

class BaseExtractor():
    __metaclass__ = ABCMeta

    def __init__(self, currentChild, errorLogger, xmlDocument):
        self.regexPattern = r''
        self.currentChild = None
        self.errorLogger = None
        self.REQUIRES_MATCH_POSITION = False   #Set this to true in subclass if you want to enforce dependsOnMatchPositionOf() before extract()
        self.matchStartPosition = -1         #position in string where to begin match. Only used on certain classes
        self.matchFinalPosition = 0          #after extractor is finished, save the ending position of the match
        self.currentChild = currentChild
        self.errorLogger = errorLogger
        self.xmlDocument = xmlDocument

    @abstractmethod
    def extract(self, text):
        self._checkIfMatchPositionIsRequiredBeforeExtract()

    def getFinalMatchPosition(self):
        return self.matchFinalPosition

    def dependsOnMatchPositionOf(self, extractor):
        self.matchStartPosition = extractor.getFinalMatchPosition()
        self.matchFinalPosition = self.matchStartPosition   #in case extractor doesn't find anything, we set finalPos as startPos

    def setDependencyMatchPositionToZero(self):
        self.matchStartPosition = 0
        self.matchFinalPosition = self.matchStartPosition   #in case extractor doesn't find anything, we set finalPos as startPos


    #TODO: REMOVE AND USE regexUtils
    def _executeSearchRegex(self, text, options=re.UNICODE | re.IGNORECASE):
        r = re.compile(self.regexPattern, options)
        return r.search(text)

    @abstractmethod
    def _constructReturnDict(self):
        pass

    def _checkIfMatchPositionIsRequiredBeforeExtract(self):
        if self.REQUIRES_MATCH_POSITION and self.matchStartPosition == -1:
            raise MatchPositionRequiredException()

class MatchPositionRequiredException(Exception):
    message = u"Match position required to supplied with dependsOnMatchPositionOf before extract call. "
    def __init__(self, details = ""):
        self.message += details
    def __unicode__(self):
        return self.message
