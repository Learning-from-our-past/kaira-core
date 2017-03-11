# -*- coding: utf-8 -*-
from abc import ABCMeta, abstractmethod


class BaseExtractor():
    __metaclass__ = ABCMeta

    def __init__(self, options=None):
        self.REQUIRES_MATCH_POSITION = False    # Set this to true in subclass if you want to enforce dependsOnMatchPositionOf() before extract()
        self.matchStartPosition = 0             # position in string where to begin match. Only used on certain classes
        self.matchFinalPosition = 0             # after extractor is finished, save the ending position of the match

    @abstractmethod
    def extract(self, entry, start_position=0):
        self._checkIfMatchPositionIsRequiredBeforeExtract()

    def getFinalMatchPosition(self):
        return self.matchFinalPosition

    def _constructReturnDict(self, data, cursor_location=0):
        self.matchFinalPosition = cursor_location   # FIXME: Temporary fix until Pipeline is ready and each extractor has access to previous extractors' results (and cursor_location)
        return {**data, 'cursorLocation': cursor_location}

    def _checkIfMatchPositionIsRequiredBeforeExtract(self):
        if self.REQUIRES_MATCH_POSITION and self.matchStartPosition == -1:
            raise MatchPositionRequiredException()


class MatchPositionRequiredException(Exception):
    message = u"Match position required to supplied with dependsOnMatchPositionOf before extract call. "

    def __init__(self, details = ""):
        self.message += details

    def __unicode__(self):
        return self.message
