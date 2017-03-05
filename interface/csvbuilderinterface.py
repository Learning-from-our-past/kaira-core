# -*- coding: utf-8 -*-
from abc import abstractmethod


class ResultCsvBuilderInterface:

    def __init__(self):
        pass

    @abstractmethod
    def openCsv(self, filepath):
        pass

    @abstractmethod
    def writeRow(self, dataDict):
        pass

    #tranforms the dict of the entry to a format which can be written into csv
    def _createRowFromDict(self, persondatadict):
        pass

    @abstractmethod
    def closeCsv(self):
        pass
