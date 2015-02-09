# -*- coding: utf-8 -*-
from abc import ABCMeta, abstractmethod
import re

class BaseExtractor():
    __metaclass__ = ABCMeta
    regexPattern = ur''
    currentChild = None
    errorLogger = None

    def __init__(self, currentChild, errorLogger):
        self.currentChild = currentChild
        self.errorLogger = errorLogger

    @abstractmethod
    def extract(self, text):
        pass

    def _executeSearchRegex(self, text, options=re.UNICODE | re.IGNORECASE):
        r = re.compile(self.regexPattern, options)
        return r.search(unicode(text))

    @abstractmethod
    def _constructReturnDict(self):
        pass