# -*- coding: utf-8 -*-
import ntpath
import csv
from abc import abstractmethod

class ResultJsonBuilderInterface:


    def __init__(self):
        pass

    @abstractmethod
    def openJson(self, filepath):
        pass

    @abstractmethod
    def writeEntry(self, dataDict):
        pass

    @abstractmethod
    def closeJson(self):
        pass